> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 38**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 38
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 38. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Dani** (Carlos, Cibersia Security), continuando con la mÃ¡quina HackerLabs Academy de la clase anterior.

La dinÃ¡mica es la misma: Chema comparte pantalla y ejecuta, el grupo sigue en paralelo, Carlos va guiando y corrigiendo.

**Resumen de lo visto hasta ahora:** - La mÃ¡quina tiene puertos 22 (SSH) y 80 (HTTP). - El puerto 80 tiene un Apache con un directorio `/wordpress`. - Dirsearch encontrÃ³ `/wordpress` y una carpeta de uploads. - WPScan sin API encontrÃ³ la versiÃ³n de WordPress 6.5.3 y el tema activo (Twenty Twenty Four), pero sin vulnerabilidades listadas.

## 2.

Tipos de pÃ¡ginas web --- Nativas vs.

CMS

Antes de continuar con la mÃ¡quina, Carlos diferencia dos tipos de aplicaciones web:

**Webs nativas:** PHP, .NET, Java, Python... cÃ³digo escrito completamente a medida.

En ellas es mÃ¡s fÃ¡cil encontrar vulnerabilidades directamente en el cÃ³digo (SQL Injection, XSS, etc.).

**CMS (*****Content Management System*****):** WordPress, Drupal, Joomla, Shopify, PrestaShop... plataformas pre-construidas.

La empresa detrÃ¡s del CMS (WordPress.org) mantiene el nÃºcleo con una calidad razonable. **Las vulnerabilidades reales en un CMS estÃ¡n casi siempre en los plugins, no en el nÃºcleo.**

**La arquitectura de un CMS en 3 capas (con analogÃ­a del coche):**

Capa WordPress AnalogÃ­a
 ----------------------------- ------------------------------- -----------------------------
 **Motor (WordPress core)** El nÃºcleo de WordPress Motor Lamborghini
 **CarrocerÃ­a (tema/theme)** La plantilla visual del sitio Carcasa: Urus, R8...
 **Accesorios (plugins)** Funcionalidades aÃ±adidas AlerÃ³n, asientos de cuero...

**Y aÃ±adiendo las librerÃ­as:** Cada plugin usa librerÃ­as (dependencias).

Cada librerÃ­a puede tener sus propias sub-dependencias.

Una vulnerabilidad en una librerÃ­a de tercer nivel puede "burbujear" hacia arriba y comprometer el sitio entero.

**Ejemplo real: Pegasus** La NSO decompiliÃ³ WhatsApp, extrajo el cÃ³digo fuente, analizÃ³ las librerÃ­as y sus dependencias hasta encontrar un 0-day en una librerÃ­a de nivel 3 de las llamadas.

Lo concatenÃ³ con una vulnerabilidad del kernel de iOS para conseguir RCE con una simple llamada de telÃ©fono entrante --- sin que el usuario hiciera nada.

**Vulnerabilidad en plugin â‰  vulnerabilidad en tu sitio:** Puedes tener un plugin con CVE de 9.8 instalado y **no ser vulnerable**, si: 1.

La funcionalidad afectada no estÃ¡ expuesta en tu sitio (no tienes el endpoint accesible), o 2.

Has comentado o desactivado el cÃ³digo vulnerable.

Ejemplo real de Carlos: Cash Converters tiene un plugin con RCE vÃ­a apertura de Excel (CVSS 9.8).

Como la pÃ¡gina no usa esa funcionalidad y la ha desactivado, el exploit no funciona.

## 3.

Por quÃ© los exploits deben apuntar al directorio correcto

**Concepto clave (la metÃ¡fora de la casa de pisos):**

Una pÃ¡gina web es como una casa con plantas: - **Planta baja / raÃ­z:** `/` --- el servidor base, sin tecnologÃ­a especÃ­fica. - **Primera planta:** `/wordpress/` --- el WordPress instalado. - **Segunda planta:** otra tecnologÃ­a diferente, quizÃ¡s un blog Drupal.

Si tienes que lanzar un exploit para WordPress, debes apuntarlo a `/wordpress/`, no a la raÃ­z `/`.

Si lo lanzas a la raÃ­z, responderÃ¡ el servidor genÃ©rico que no tiene WordPress instalado y el exploit no funcionarÃ¡.

**Esto es crÃ­tico en exÃ¡menes de certificaciÃ³n (OSCP, eJPT):** mucha gente falla porque lanza WPScan o un exploit a la URL raÃ­z cuando WordPress estÃ¡ en un subdirectorio.

# MAL â€” lanza WPScan contra la raÃ­z:

wpscan --url http://academy.th1/

# BIEN â€” lanza WPScan contra donde estÃ¡ el WordPress:

wpscan --url http://academy.th1/wordpress/

Wappalyzer es Ãºtil aquÃ­: cambia la tecnologÃ­a detectada segÃºn la ruta que estÃ¡s visitando.

Al navegar a `/wordpress/`, Wappalyzer detecta WordPress; en la raÃ­z, solo detecta Apache.

## 4.

Dirsearch con flag -r (recursivo) --- la opciÃ³n imprescindible

**El problema sin recursivo:** Si lanzas `dirsearch -u http://academy.th1/`, solo enumera rutas de la raÃ­z.

No entra dentro de `/wordpress/` para seguir buscando subdirectorios internos (como `/wordpress/wp-content/uploads/`).

**La soluciÃ³n:**

dirsearch -u http://academy.th1/ -r

El flag `-r` activa la **enumeraciÃ³n recursiva**: cuando encuentra un directorio (cÃ³digo 301), aÃ±ade automÃ¡ticamente ese directorio a la cola para escanearlo tambiÃ©n.

Es la razÃ³n por la que Carlos estuvo a punto de suspender el OSCP --- sin el recursivo, no encontraba ciertos directorios donde estaban los usuarios para la fuerza bruta.

**Herramientas equivalentes:** DirBuster, GoBuster, Feroxbuster (recursivo por defecto), FFUF.

La elecciÃ³n es personal --- todas funcionan igual con el mismo diccionario.

Carlos usa dirsearch porque le gustan los colores de la interfaz.

**Diccionario para mÃ¡quinas CTF:** `directory-list-2.3-medium.txt` de SecLists (tambiÃ©n disponible en `/usr/share/wordlists/dirbuster/`).

## 5.

WPScan --- Herramienta de auditorÃ­a completa para WordPress

**WPScan** es la herramienta de referencia para auditar sitios WordPress.

EstÃ¡ incluida en Kali por defecto.

### Uso bÃ¡sico

wpscan --url http://academy.th1/wordpress/

Sin API, el output incluye: - VersiÃ³n de Apache y del servidor. - VersiÃ³n de WordPress. - Tema activo (dem/theme) y su versiÃ³n. - Lista bÃ¡sica de plugins (sin vulnerabilidades).

### Lo que muestra WPScan sin API

El output viene de las cabeceras HTTP de las peticiones.

Para verlo a mano con Burp Suite: activar el proxy â†’ navegar al sitio â†’ HTTP History â†’ buscar en las cabeceras la lÃ­nea `Server:` â†’ ahÃ­ aparece `Apache/2.4.59`.

`xmlrpc.php`: WPScan detecta si estÃ¡ activo.

Es una API antigua de WordPress que sirve para acceso remoto.

No tiene valor para las primeras fases de explotaciÃ³n, pero puede usarse para fuerza bruta evitando los bloqueos del login normal.

### WPScan con API key (imprescindible para vulnerabilidades)

Registrarse gratis en **wpvulndb.com** (WPVulnDB) â†’ obtener un API token gratuito.

wpscan --url http://academy.th1/wordpress/ --api-token TU_TOKEN

Con API, el output aÃ±ade: - Vulnerabilidades de la versiÃ³n de WordPress core (con CVE y CVSS). - Vulnerabilidades del tema activo. - Vulnerabilidades de cada plugin detectado.

> [!important] **Diferencia clave:** sin API â†’ lista plugins, pero no dice si tienen CVEs.

Con API â†’ cruza la versiÃ³n de cada componente con la base de datos de WPVulnDB y lista todos los CVEs asociados.

### Interpretar los resultados de WPScan

Para cada vulnerabilidad encontrada, fijarse en: 1. **Rol requerido:** Â¿dice `authenticated`, `contributor`, `author`? â†’ sin credenciales vÃ¡lidas, no es explotable todavÃ­a. **Descartar temporalmente.** 2. **Tipo de vulnerabilidad:** XSS stored, SQLi, RCE, LFI... â†’ determina el vector. 3. **Â¿Es explotable en el estado actual?** â†’ si requiere que cierta funcionalidad estÃ© activa y en el sitio no lo estÃ¡, no aplica.

â†’

**La jerarquÃ­a de bÃºsqueda de vulnerabilidades:**

Apache (versiÃ³n) â†’ Â¿CVE accesible sin autenticaciÃ³n? â†’ si no, siguiente â†“ WordPress core â†’ Â¿CVE explotable sin credenciales? â†’ si no, siguiente â†“ Tema activo â†’ Â¿CVE explotable? â†’ si no, siguiente â†“ Plugins â†’ Â¿CVE explotable? â†’ si no... â†“ LibrerÃ­as de plugins â†’ Â¿CVE en dependencias? â†“ Si nada â†’ cambiar de vector â†’ login / enumeraciÃ³n de usuarios

### EnumeraciÃ³n de usuarios con WPScan

> [!warning] **Information disclosure en el login de WordPress:** WordPress por defecto, cuando introduces un usuario que no existe, dice: "*Error: El nombre de usuario XXX no estÃ¡ registrado en este sitio.*" Cuando el usuario existe pero la contraseÃ±a es incorrecta, dice: "*Error: La contraseÃ±a es incorrecta para el nombre de usuario XXX.*"

Esta diferencia permite enumerar usuarios vÃ¡lidos. **Una web bien configurada** devuelve el mismo mensaje genÃ©rico ("nombre de usuario o contraseÃ±a incorrectos") para ambos casos, sin dar pistas.

**Enumerar usuarios automÃ¡ticamente con WPScan:**

wpscan --url http://academy.th1/wordpress/ \
 --enumerate u \
 --wordlist /ruta/a/usernames.txt

Alternativamente, sin lista de usuarios (WPScan hace la enumeraciÃ³n por defecto si no se pasa `-u`):

wpscan --url http://academy.th1/wordpress/

# Sin usuario especificado â†’ WPScan enumera automÃ¡ticamente usando la API REST de WordPress

### Fuerza bruta de contraseÃ±as con WPScan

Una vez encontrado el usuario, lanzar la fuerza bruta:

wpscan --url http://academy.th1/wordpress/ \
 --enumerate u \
 --passwords /usr/share/wordlists/rockyou.txt

**Por quÃ© WPScan en vez de Hydra para WordPress:** Hydra no maneja correctamente la autenticaciÃ³n de WordPress (cookies, tokens CSRF).

WPScan estÃ¡ diseÃ±ado especÃ­ficamente para ello y funciona de forma fiable.

**Por quÃ© WPScan en vez de Burp Intruder:** Burp Intruder en la versiÃ³n Community tiene rate limiting (aÃ±ade delays).

Para una lista como RockYou con \~14 millones de entradas, tardarÃ­a dÃ­as.

WPScan es mucho mÃ¡s rÃ¡pido.

**Resultado en la demo:** usuario `dylan` con contraseÃ±a `password1`.

### La fuerza bruta es el ÃšLTIMO recurso

**Regla del profesor:** \> La fuerza bruta es el Ãºltimo cartucho.

Antes de llegar a ella, intenta: enumeraciÃ³n de usuarios, information disclosure, OSINT del objetivo, ingenierÃ­a social, phishing.

Solo cuando todo eso falla, lanzas la fuerza bruta.

**Motivos:** - Las mÃ¡quinas CTF estÃ¡n diseÃ±adas para que la soluciÃ³n no requiera fuerza bruta masiva --- siempre hay una pista o un usuario enumerable. - En entornos reales con rate limiting o bloqueo de IP, la fuerza bruta es inviable. - Genera ruido masivo que los sistemas de detecciÃ³n identifican inmediatamente.

## 6.

File Upload --- Las dos condiciones necesarias para RCE

WPScan encontrÃ³ `/wp-content/uploads/` como directorio accesible.

Carlos explica cuÃ¡ndo esto es explotable:

**CondiciÃ³n 1 --- Upload:** necesitas una manera de subir un fichero al servidor.

### Puede ser: - Un formulario de subida de ficheros en la web. - FTP con acceso de escritura. - SMB con permisos de escritura. - MÃ©todo HTTP PUT habilitado. - El panel de administraciÃ³n de WordPress (si tienes credenciales).

**CondiciÃ³n 2 --- EjecuciÃ³n:** el fichero subido debe ser accesible vÃ­a navegador Y el servidor debe interpretarlo (no servirlo como texto plano).

**La demostraciÃ³n:** navegar a `http://academy.th1/wordpress/wp-content/uploads/` muestra el contenido del directorio.

Al hacer clic en una imagen JPG, el servidor la "ejecuta" (compila el cÃ³digo de la imagen --- sus pÃ­xeles --- y la muestra).

Si en vez de un JPG hubiera un PHP, al clicar lo ejecutarÃ­a.

**El binomio upload + execution:** - Tener `/uploads/` accesible = la ejecuciÃ³n estÃ¡ confirmada. - Falta conseguir subir un fichero PHP a ese directorio. - La vÃ­a de subida (formulario, FTP, etc.) debe almacenar el fichero exactamente en ese directorio accesible.

> [!note] **Nota:** si subes un fichero a `/foto-de-perfil/` pero ese directorio no es accesible desde el navegador, el fichero no se puede ejecutar aunque estÃ© en el servidor.

## 7.

DOM --- Â¿QuÃ© es?

SurgiÃ³ en la clase al ver la vulnerabilidad "Author DOM-Based Stored XSS" en WPScan.

**DOM** = *Document Object Model* = el **navegador**.

El DOM es la representaciÃ³n del HTML de una pÃ¡gina en memoria del navegador.

Un ataque DOM-Based XSS ocurre cuando el cÃ³digo malicioso se ejecuta en el contexto del navegador del usuario (no en el servidor), aprovechando cÃ³mo el navegador parsea y ejecuta JavaScript.

**Por quÃ© ya no existe Flash:** Adobe Flash Player era un motor de ejecuciÃ³n en el navegador con decenas de vulnerabilidades que permitÃ­an RCE en el equipo del cliente.

Adobe lo retirÃ³ definitivamente en 2020 por eso.

## 8.

Herramientas vistas en clase

# Dirsearch recursivo (siempre poner -r)

dirsearch -u http://URL/directorio/ -r

# WPScan bÃ¡sico

wpscan --url http://URL/wordpress/

# WPScan con API (para ver vulnerabilidades)

wpscan --url http://URL/wordpress/ --api-token TU_TOKEN

# WPScan con API y enumeraciÃ³n de plugins activos

wpscan --url http://URL/wordpress/ --api-token TU_TOKEN --enumerate ap

# WPScan con enumeraciÃ³n de usuarios + fuerza bruta

wpscan --url http://URL/wordpress/ \
 --enumerate u \
 --passwords /usr/share/wordlists/rockyou.txt

# Ver opciones de WPScan filtradas

wpscan --help | grep enumerate wpscan --help | grep user wpscan --help | grep password

**Diccionario de fuerza bruta para CTF:** siempre `rockyou.txt`.

EstÃ¡ diseÃ±ado para ello.

**Diccionario de directorios:** `directory-list-2.3-medium.txt` (SecLists / DirBuster).

## 9.

Wordfence --- El antivirus de WordPress

Mencionado en la sesiÃ³n: **Wordfence** es el plugin de seguridad mÃ¡s popular para WordPress.

Entre otras cosas, implementa rate limiting y bloqueo de IP en el login (mÃ¡ximo N intentos).

Si estÃ¡ activo, las tÃ©cnicas de fuerza bruta directa contra el login quedan bloqueadas.

### Vector alternativo: XMLRPC.

## 10.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
-------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------
 *W Pescal / WPS Cam / Wpeskan / w p scan* **WPScan** -- herramienta de auditorÃ­a de sitios WordPress
 *dems / demo / el dem* **Tema (theme)** -- la plantilla visual de WordPress (ej.

Twenty Twenty Four)
 *guiÃ³n r / guion r* `-r` -- flag de dirsearch para activar la enumeraciÃ³n recursiva de directorios
 *DIRserch / Dearbuster / DeerBuster* **dirsearch** / **DirBuster** -- herramientas de fuzzing web de directorios
 *Flexbuster / Feroxbuster / peroxbuster / FeroxBuster* **Feroxbuster** -- herramienta de fuzzing web con recursivo activado por defecto
 *check list / sek list* **SecLists** (github.com/danielmiessler/SecLists) -- colecciÃ³n de diccionarios para pentesting
 *Rog you / RobJu / Rob you / RockyU* **RockYou (rockyou.txt)** -- el diccionario de fuerza bruta estÃ¡ndar en CTFs
 *enumÃ©ration / enumerate / enumeraciÃ³n de u* `--enumerate u` / `--enumerate ap` -- flags de WPScan para enumerar usuarios y plugins activos
 *API tokem / api guiÃ³n guiÃ³n token* `--api-token` -- flag de WPScan para autenticarse contra WPVulnDB y obtener vulnerabilidades
 *WordPress VDB / WP vuln DB* **WPVulnDB** (wpscan.com) -- base de datos de vulnerabilidades de WordPress de WPScan
 *w p content upload / los uploads* `/wp-content/uploads/` -- directorio de archivos subidos en WordPress
 *wp login punto PHP / el panel de WordPress* `/wp-login.php` -- panel de login de WordPress
 *XMLRP / XMLRCP / el XML* **XMLRPC** (`xmlrpc.php`) -- API antigua de WordPress para acceso remoto; vector para fuerza bruta evitando rate limiting
 *World Fence / WalFence* **Wordfence** -- plugin de seguridad para WordPress que implementa rate limiting y bloqueo de IP
*DOM / el de la librerÃ­a / navegador* **DOM** (*Document Object Model*) -- la representaciÃ³n de la pÃ¡gina en el navegador; un "DOM-Based XSS" se ejecuta en el navegador del usuario
*Zino / la informaciÃ³n que da el login* **Information disclosure** -- vulnerabilidad que revela si un usuario existe o no en funciÃ³n del mensaje de error del login
 *STP* **OSCP** / **eJPT** -- certificaciones de pentesting (contexto: "en los STP nunca se necesita fuerza bruta")
*guion u de Wpscan / guiÃ³n guiÃ³n user* `-U fichero` (lista de usuarios) / `--enumerate u` (enumeraciÃ³n automÃ¡tica) -- opciones de WPScan para usuarios
 *password attack / guion guion passwords* `--passwords /ruta/diccionario` -- flag de WPScan para fuerza bruta de contraseÃ±as
 *Claudia / Claude / Claudio* **Claude** (Anthropic) -- IA usada por los alumnos durante la clase

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’

â†’

â†’
