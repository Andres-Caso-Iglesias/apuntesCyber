> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 37**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 37
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 37. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Dani** (Carlos, el profesor de Cibersia Security que da el enfoque mÃ¡s prÃ¡ctico del mÃ¡ster).

Es la continuaciÃ³n directa de la Clase 36: si Castillo introdujo Burp Suite teÃ³ricamente, hoy Dani lo consolida con prÃ¡ctica real y aÃ±ade la primera mÃ¡quina web del nuevo mÃ³dulo: **HackerLabs Academy** (WordPress).

**Estructura del dÃ­a:** 1.

Repaso de Burp Suite desde cero con demostraciÃ³n en vivo. 2.

ExplicaciÃ³n profunda de la arquitectura cliente-servidor y por quÃ© Burp puede interceptar. 3.

Primera mÃ¡quina web: HackerLabs Academy --- WordPress con metodologÃ­a completa.

**Adelanto de prÃ³ximas sesiones:** Dani menciona que en agosto harÃ¡ un speedrun de DevOps --- cÃ³mo desplegar una aplicaciÃ³n web completa (cloud, GitHub, dominio, DNS, servidor).

Bonus para el grupo.

## 2.

Burp Suite --- DefiniciÃ³n correcta

Un alumno define Burp Suite como "un proxy".

El profesor lo corrige con la definiciÃ³n mÃ¡s precisa:

> **Burp Suite es un framework de auditorÃ­a web.**

Un proxy es solo una de sus funcionalidades --- la mÃ¡s importante, sÃ­, pero Burp incluye muchas mÃ¡s.

Es una recopilaciÃ³n de herramientas que permiten realizar mÃºltiples acciones sobre pÃ¡ginas web para auditarlas:

MÃ³dulo FunciÃ³n
 ------------------ ----------------------------------------------------------------------------
 **Proxy** Interceptar peticiones HTTP/HTTPS antes de que lleguen al servidor
 **Target** Definir el scope (dominio objetivo) para filtrar el ruido
 **Intruder** Fuerza bruta sobre parÃ¡metros de peticiones con diccionarios
 **Repeater** Reenviar peticiones modificadas manualmente tantas veces como sea necesario
 **Decoder** Decodificar/encodear valores (URL, Base64, etc.)
 **Comparer** Comparar dos peticiones o respuestas para encontrar diferencias
 **Sequencer** Enviar secuencias de peticiones encadenadas
 **Collaborator** Extensiones de terceros (Pro)
 **Extensions** Plugins de la comunidad gratuitos

## 3.

Arquitectura cliente-servidor y por quÃ© Burp puede interceptar

### La explicaciÃ³n con dibujos del profesor

Dani explica con un Paint en vivo la arquitectura web:

[FRONT — corre en TU ordenador] â†’ [peticiÃ³n HTTP] â†’ [BACK — en el servidor] (navegador) (PHP, base de datos...)

> [!important] **Concepto clave:** el frontend corre en tu ordenador.

Eso significa que **tienes control total sobre Ã©l** antes de que envÃ­e la peticiÃ³n al servidor.

El backend, en cambio, estÃ¡ en el servidor remoto --- ahÃ­ no puedes tocar nada directamente.

**Por quÃ© el frontend puede tener controles de seguridad inÃºtiles:** El frontend puede restringir inputs (solo nÃºmeros, mÃ¡ximo 25 caracteres, solo imÃ¡genes...).

Pero como esas restricciones se ejecutan en tu mÃ¡quina, Burp puede interceptar la peticiÃ³n **despuÃ©s de que el frontend la haya** "**aprobado**" y antes de que salga hacia Internet, modificando cualquier campo.

**La metÃ¡fora del cartero:** \> TÃº preparas un paquete respetando todas las normas del front (el paquete estÃ¡ bien embalado).

Lo metes en el buzÃ³n.

Antes de que llegue el cartero, alguien (Burp) abre el buzÃ³n, cambia el contenido del paquete, y lo sella de nuevo.

El servidor recibe algo completamente diferente a lo que mandaste.

**La defensa correcta:** validar los datos **en el backend tambiÃ©n**, no solo en el frontend.

Si el servidor no verifica lo que recibe, cualquier restricciÃ³n del frontend es cosmÃ©tica.

### WAF (Web Application Firewall)

Entre el paquete modificado y el servidor puede haber un **WAF** (*Web Application Firewall*) que intenta detectar peticiones maliciosas.

El WAF es bypasseable con tÃ©cnicas especÃ­ficas.

Si se supera, solo queda el backend (los ficheros PHP del servidor).

## 4.

InstalaciÃ³n completa de Burp Suite con FoxyProxy (paso a paso)

### Por quÃ© hace falta el certificado CA

Burp intercepta tanto HTTP como HTTPS.

Para poder descifrar el trÃ¡fico HTTPS (que estÃ¡ cifrado con TLS), necesita presentarse como una autoridad de certificaciÃ³n de confianza.

Sin el certificado, las pÃ¡ginas HTTPS dan error de seguridad.

**Instalar el certificado CA de Burp en Firefox:**

## 1.

Con Burp abierto, navegar a http://localhost:8080 (o http://burpsuite) 2.

Hacer clic en "CA Certificate" para descargar el fichero cacert.der 3.

Firefox â†’ about:preferences â†’ buscar "certificados" 4.

ConfiguraciÃ³n avanzada â†’ Certificados â†’ Administrar certificados 5.

PestaÃ±a "Autoridades" â†’ Importar â†’ seleccionar cacert.der 6.

Marcar las DOS casillas de confianza â†’ Aceptar

PortSwigger (los creadores de Burp) es una autoridad de certificaciÃ³n reconocida.

El certificado dura hasta 2036.

**Verificar:** buscar "PortSwigger" en la lista de autoridades.

Aparece como "PortSwigger CA".

### Configurar FoxyProxy en Firefox

FoxyProxy es una extensiÃ³n que activa/desactiva el proxy con un clic:

## 1.

Instalar FoxyProxy Standard desde los addons de Firefox 2.

Click en el icono de FoxyProxy â†’ Options 3.

Proxies â†’ Add 4.

Nombre: Burp Suite 5.

Host: 127.0.0.1 6.

Puerto: 8080 (el mismo que en Proxy Settings de Burp) 7.

Guardar

**Verificar el puerto de Burp:** Burp â†’ Proxy â†’ Proxy Settings â†’ Proxy Listeners â†’ confirmar que escucha en `127.0.0.1:8080`.

**Por quÃ© 8080:** Burp se pone a escuchar en el puerto 8080 de localhost.

FoxyProxy redirige el trÃ¡fico del navegador a ese puerto.

Burp recibe la peticiÃ³n, la registra (y la pausa si Intercept estÃ¡ ON), y la reenvÃ­a al servidor.

**Problema habitual:** si ambos (FoxyProxy y Burp) estaban configurados en el mismo puerto incorrecto, cambiar a 8081 en los dos y reiniciar Burp.

Lo importante es que el puerto coincida en ambos sitios.

## 5.

MÃ³dulos de Burp --- Repaso prÃ¡ctico

### Target â†’ Scope

Al navegar con el proxy activo, el HTTP History captura **todo** --- incluyendo peticiones de Google Analytics, extensiones del navegador, CDNs, publicidad, etc.

Para centrar el anÃ¡lisis solo en el objetivo:

## 1.

Burp â†’ Target â†’ Site Map 2.

Clic derecho en el dominio objetivo â†’ Add to Scope 3.

Confirmar que se ignoran las peticiones fuera del scope

### Decoder

Cuando se captura un parÃ¡metro encodado (ej. en URL encoding o Base64), pegarlo en el mÃ³dulo Decoder para legibilizarlo:

Decoder â†’ pegar valor â†’ Decode as: URL / Base64 / etc.

Ejemplo del profesor: analizar la cookie de sesiÃ³n de YouTube con doble encoding Base64 + URL.

El Comparer se usa para comparar varias cookies y buscar el patrÃ³n de generaciÃ³n.

**Principio importante en informÃ¡tica:** no existe la aleatoriedad pura.

Todo nÃºmero "aleatorio" tiene una semilla (seed).

Si se descubre el patrÃ³n de generaciÃ³n de los session tokens, se puede predecir el siguiente â†’ session token prediction.

### Intruder --- Modos de ataque

Modo DescripciÃ³n CuÃ¡ndo usarlo
 ------------------- ----------------------------------------------------------- --------------------------------------------------
 **Sniper** Un payload, una posiciÃ³n a la vez Fuerza bruta de usuario o contraseÃ±a por separado
 **Battering Ram** Mismo payload en todas las posiciones simultÃ¡neamente Cuando usuario = contraseÃ±a
 **Pitchfork** Un payload por posiciÃ³n, coordinados Listas de usuarios+contraseÃ±as emparejadas
 **Cluster Bomb** CombinaciÃ³n de todos los payloads en todas las posiciones MÃ¡xima cobertura, genera muchas peticiones

> [!note] **Nota:** en Burp Community, el Intruder tiene rate limiting (delay artificial).

Burp Pro elimina ese lÃ­mite.

El link a la versiÃ³n Pro no oficial fue compartido por el profesor en el grupo de WhatsApp del mÃ¡ster.

### Repeater --- Para investigar sin fuerza bruta

Cuando se quiere explorar cÃ³mo responde una web a distintas peticiones sin lanzar fuerza bruta, usar el Repeater:

HTTP History â†’ clic derecho â†’ Send to Repeater

Desde Repeater se pueden modificar manualmente los parÃ¡metros y enviar la peticiÃ³n tantas veces como se quiera, viendo la respuesta completa.

Es el equivalente a hacer `curl` manualmente pero con interfaz grÃ¡fica.

## 6.

Cookies de sesiÃ³n --- Funcionamiento y vulnerabilidades

### Por quÃ© existen las cookies de sesiÃ³n

Cuando mÃºltiples usuarios acceden a la misma web simultÃ¡neamente, el servidor necesita saber a quiÃ©n servirle quÃ© contenido.

Para eso crea un **identificador de sesiÃ³n Ãºnico** (session ID) por usuario.

**Flujo:** 1.

Usuario hace login correctamente. 2.

El servidor genera una cookie con un session ID Ãºnico. 3.

En cada peticiÃ³n siguiente, el navegador envÃ­a esa cookie. 4.

El servidor sabe quiÃ©n es sin necesidad de volver a pedir usuario y contraseÃ±a. 5.

La cookie expira (tÃ­picamente 30 dÃ­as) o al borrar la cachÃ©.

`Ctrl+Shift+R` = hard reset = borra la cachÃ© = borra las cookies = nueva sesiÃ³n.

### Session Hijacking (ataque histÃ³rico)

Antiguamente, si los session IDs se generaban con patrones predecibles (ej.

ID incremental), un atacante podÃ­a iterar sobre los valores para encontrar sesiones activas de otros usuarios.

Hoy los session IDs son pseudoaleatorios y no se reciclan, lo que hace este ataque muy difÃ­cil --- pero no imposible con tÃ©cnicas avanzadas.

### Robo de cookies via phishing moderno (Adversary in the Middle)

El phishing moderno ya no roba usuario/contraseÃ±a --- roba la cookie de sesiÃ³n:

## 1.

Atacante crea pÃ¡gina de phishing idÃ©ntica al original 2.

VÃ­ctima introduce usuario y contraseÃ±a 3.

El atacante los reenvÃ­a en tiempo real al servidor real 4.

El servidor pide 2FA 5.

El atacante muestra el campo de 2FA a la vÃ­ctima en su pÃ¡gina falsa 6.

VÃ­ctima introduce el cÃ³digo 2FA 7.

El atacante lo reenvÃ­a al servidor real 8.

El servidor genera la cookie de sesiÃ³n y se la envÃ­a al atacante 9.

El atacante tiene 30 dÃ­as de acceso sin necesidad de usuario, contraseÃ±a ni 2FA

Esta tÃ©cnica se llama **AiTM** (*Adversary in the Middle*) y bypasea completamente el doble factor.

Es la razÃ³n por la que herramientas como **Evilginx** o **GoPhish** son tan efectivas en red teams modernos.

**El XSS stored** tambiÃ©n puede robar cookies: inyectar JavaScript que envÃ­e la cookie del usuario a un servidor del atacante cuando cualquier otro usuario cargue la pÃ¡gina.

## 7.

MÃ¡quina HackerLabs Academy --- MetodologÃ­a web completa

### Â¿QuÃ© es HackerLabs?

**HackerLabs** (hackerlabs.academy) es una plataforma similar a HTB orientada a mÃ¡quinas web.

Las mÃ¡quinas se descargan como archivos `.ova` o `.zip`, se importan en VirtualBox, y se les configura la red NAT para tener visibilidad con Kali.

**ConfiguraciÃ³n de red:**

VirtualBox â†’ mÃ¡quina Academy â†’ clic derecho â†’ ConfiguraciÃ³n â†’ Red â†’ Adaptador puente (o RedNat si Kali estÃ¡ en la misma red)

### Reconocimiento de la mÃ¡quina

Sin Kali disponible (la de la clase estaba rota), el profesor usa Windows + PowerShell:

### Puertos identificados:

 - Puerto 22 â†’ SSH (Apache 2.4.0.591, Debian)
 - Puerto 80 â†’ HTTP (WordPress)

**LecciÃ³n del profesor:** \> Puerto 22 sin credenciales â†’ poco que hacer.

Puerto 80 con WordPress â†’ mucho por explorar.

Siempre empezar por la web.

### Paso 1 --- AÃ±adir el dominio al archivo hosts

La web usa el dominio `academy.th1` en vez de la IP.

Sin aÃ±adirlo al hosts, las imÃ¡genes y recursos no cargan.

**En Windows (equivalente al** `/etc/hosts` **de Linux):**

C:\Windows\System32\drivers\etc\hosts

Abrir con Bloc de Notas **como administrador** y aÃ±adir:

192.168.1.121 academy.th1

Guardar.

A partir de ahÃ­ navegar a `http://academy.th1` en vez de a la IP directamente.

**Este paso es idÃ©ntico al de las mÃ¡quinas de HTB** que tienen dominios personalizados.

Con 90 mÃ¡quinas hechas, ese fichero hosts acaba siendo enorme.

### Paso 2 --- Fuzzing de directorios

# Con SecLists descargado y PowerShell (sin Kali disponible):

# Claude generÃ³ un script de fuzzing en PowerShell que usa el diccionario

# directory-list-2.3-medium.txt y lanza peticiones HTTP a cada ruta

**Herramienta descargada:** SecLists (github.com/danielmiessler/SecLists) --- el mejor repositorio de diccionarios para pentesting.

Contiene: - `Discovery/Web-Content/` â†’ para fuzzing de directorios y ficheros - `Discovery/DNS/` â†’ para subdominios - `Passwords/` â†’ para ataques de contraseÃ±as

**Resultado del fuzzing:** directorio `/wordpress` encontrado.

### Paso 3 --- Fingerprinting con Wappalyzer

Instalar la extensiÃ³n **Wappalyzer** en Firefox â†’ navegar a la web â†’ clic en el icono â†’ detecta tecnologÃ­as: - WordPress (versiÃ³n especÃ­fica) - PHP - Apache

**Principio clave del profesor:** \> Una web no es vulnerable en sÃ­.

Lo vulnerable es una **funcionalidad** o **tecnologÃ­a en una versiÃ³n concreta**.

> [!important] Por eso el fingerprinting es tan importante: necesitamos saber quÃ© versiones tiene para buscar CVEs.

### Paso 4 --- Referencia metodolÃ³gica: HackTricks para WordPress

HackTricks â†’ buscar "WordPress"

HackTricks tiene una pÃ¡gina completa con todos los ficheros de WordPress, rutas sensibles, comandos de enumeraciÃ³n con WPScan, y CVEs comunes.

Siempre consultarlo al encontrar un CMS conocido.

**Ficheros importantes de WordPress:** - `wp-login.php` â†’ panel de administraciÃ³n - `wp-config.php` â†’ credenciales de base de datos (no accesible desde web, pero sÃ­ por LFI) - `wp-content/plugins/` â†’ plugins instalados (vector de CVEs) - `wp-content/themes/` â†’ temas activos (vector de file upload si se tiene acceso) - `xmlrpc.php` â†’ API XML-RPC, vector de fuerza bruta si no estÃ¡ desactivada

## 8.

Fundamentos web para el mÃ³dulo de hacking

### El /etc/hosts (Linux) y su equivalente Windows

El fichero `hosts` es la "guÃ­a telefÃ³nica local" del sistema --- se consulta antes que cualquier servidor DNS externo.

Si se aÃ±ade una entrada, el sistema resuelve ese dominio localmente sin hacer una consulta DNS real.

- **Linux:** `/etc/hosts`
- **Windows:** `C:\Windows\System32\drivers\etc\hosts`

En ambos casos, el formato es:

IP dominio 192.168.1.121 academy.th1

### Protocolo DNS explicado

Cuando navegas a `google.com`: 1.

El sistema consulta primero `/etc/hosts`. 2.

Si no estÃ¡ ahÃ­, consulta el servidor DNS configurado (Google 8.8.8.8, Cloudflare 1.1.1.1, el del router...). 3.

El servidor DNS devuelve la IP correspondiente. 4.

El navegador envÃ­a la peticiÃ³n HTTP a esa IP.

**Por quÃ© importa en hacking web:** las mÃ¡quinas de HTB y HackerLabs a menudo usan dominios ficticios (`.htb`, `.th1`) que solo existen localmente.

Sin el fichero hosts no hay resoluciÃ³n DNS posible.

## 9.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
-------------------------------------------------- -------------------------------------------------------------------------------------------------------------------
 *Bullsuite / Boursuite / Bootsuite / Bursuite* **Burp Suite** -- framework de auditorÃ­a web (proxy + intruder + repeater + decoder...)
 *policy* No es un "policy" --- es un **proxy** (intermediario que intercepta peticiones HTTP)
 *repetiter / el de repetir / cenarte una fabada* **Repeater** -- mÃ³dulo para reenviar peticiones modificadas manualmente
 *el Intoder / Intruded* **Intruder** -- mÃ³dulo para fuerza bruta en parÃ¡metros de peticiones
 *buttering / snipper / pitfork / clusterbomb* **Battering Ram / Sniper / Pitchfork / Cluster Bomb** -- modos de ataque del Intruder
 *el decoder / decodiador* **Decoder** -- mÃ³dulo para codificar/decodificar valores (URL, Base64, HTML...)
 *comparer / comparar* **Comparer** -- mÃ³dulo para comparar peticiones/respuestas y encontrar diferencias
 *Colaborator* **Collaborator** -- mÃ³dulo Pro para extensiones y detecciÃ³n de vulnerabilidades out-of-band
 *Foxyproxy / Fashei proxy / Fose Proxy* **FoxyProxy** -- extensiÃ³n de Firefox para activar/desactivar el proxy con un clic
 *el de burg / port de burg* **Burp Proxy Listener** -- `127.0.0.1:8080` donde Burp escucha las peticiones
 *certific / certificado de identidad* **Certificado CA de Burp** -- necesario para interceptar trÃ¡fico HTTPS
 *WAV / waff / webapplication fire* **WAF** (*Web Application Firewall*) -- capa de seguridad entre el cliente y el servidor
 *sesiÃ³n hit jacking / hijacking* **Session Hijacking** -- ataque que roba la cookie de sesiÃ³n de otro usuario
 *2 FA / 2 SFA / Factor de doble* **2FA** (*Two-Factor Authentication*) -- segundo factor de autenticaciÃ³n (Google Authenticator, SMS, llave fÃ­sica)
 *ETC host / los host / etc slash host* `/etc/hosts` -- fichero de resoluciÃ³n DNS local en Linux
 *sistema 32 drivers etc host* `C:\Windows\System32\drivers\etc\hosts` -- equivalente Windows del /etc/hosts
 *Hacker Labs / HackerLab / hackerlabss* **HackerLabs** (hackerlabs.academy) -- plataforma de mÃ¡quinas web para prÃ¡ctica
 *sek list / seklist / settings* **SecLists** (github.com/danielmiessler/SecLists) -- colecciÃ³n de diccionarios para pentesting
 *dictionary list 2 3 medium / directory list* `directory-list-2.3-medium.txt` -- diccionario de SecLists para fuzzing de directorios
 *Wappalizer / Wapalizer / Wapaliser* **Wappalyzer** -- extensiÃ³n del navegador para detectar tecnologÃ­as web
 *HakTrix / Haktrix / Hachstrix* **HackTricks** (book.hacktricks.xyz) -- referencia metodolÃ³gica por servicio/tecnologÃ­a
 *WP scanner / WPeskan* **WPScan** -- escÃ¡ner especÃ­fico de vulnerabilidades para WordPress
 *el wp config / wp-config punto PHP* `wp-config.php` -- fichero de configuraciÃ³n de WordPress con credenciales de base de datos
 *Claudia / Claudio / Klow* **Claude** (Anthropic) -- IA usada para generar el script de fuzzing en PowerShell
 *bycoding / vibe coding* **Vibe coding** / **AI-assisted development** -- desarrollo de cÃ³digo asistido por IA
 *AiTM / man in the middle de phishing* **AiTM** (*Adversary in the Middle*) -- phishing avanzado que roba la cookie de sesiÃ³n despuÃ©s del 2FA

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’

â†’

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/17.07.2026 PortSwigger Intro y 6 Casos Path Traversal.md|17.07.2026 PortSwigger Intro y 6 Casos Path Traversal]— Hack The Box, SSH, XSS
- [[../../apuntes Chema/Burp Suite a fondo · Auditoría web · WordPress.md|Burp Suite a fondo · Auditoría web · WordPress]— Hack The Box, Kali Linux, XSS
- [[resumen_master_clase35.md|resumen_master_clase35]— Hack The Box, Kali Linux, Redes
- [[../../transcripciones/Junio/30.06.2026 Explotación web Port Swinger.md|30.06.2026 Explotación web Port Swinger]— Hack The Box, SSH, XSS
- [[../../transcripciones/Julio/28.07.2026 Repaso General Metodologia Web y Command Injection.md|28.07.2026 Repaso General Metodologia Web y Command Injection]— Hack The Box, Kali Linux, SSH
- [[resumen_master_clase38.md|resumen_master_clase38]— Kali Linux, SSH, XSS

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #file-upload #hack-the-box #hydra #ia #kali #lfi #linux #redes #ssh #windows #wordpress #wpscan #xss
