> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 47**
> **Módulo:** MODULO3
> **Tema:** Clase 47
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 47. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Castillo** (Carlos Castillo).

Hay contexto del Mundial España --- la sesión anterior se hizo speedrun para ver el partido, hoy se retoma el ritmo normal.

**Anuncio importante --- Planificación del resto del máster:** - **Estas 2 semanas:** web con PortSwigger + laboratorios (Castillo y Carlos juntos). - **Agosto:** sin clase (vacaciones completas para el grupo). - **Septiembre:** mini-repaso al volver + continuar web + comenzar **Bluetooth** con Edu (responsable de Satek, experto en BLE). - **Tras el módulo web:** práctica 2 (auditoría web real con informe). - **Posterior:** Directorio Activo.

**Las 3 prácticas del máster:** - **Práctica 1 (Carlos):** en preparación, se anuncia antes de agosto. - **Práctica 2 (Yuba):** hacking web real de una web real en Internet.

Cada alumno tiene vulnerabilidades diferentes asignadas (no todos encuentran las mismas).

Sin objetivo final fijo --- puede haber 3 vulnerabilidades o 20. - **Práctica 3 (Castillo):** entorno de 4 máquinas, solo se ve la primera.

Hay que pivotar de máquina en máquina para ver la siguiente.

Kali → máquina 1 → máquina 2 → máquina 3.

Basada en pivoting y escalada de privilegios.

## 2.

PortSwigger Web Security Academy --- Introducción

**PortSwigger** (portswigger.net/web-security) es la plataforma de laboratorios de los creadores de Burp Suite.

Es el recurso más completo para aprender hacking web con laboratorios prácticos.

### Estructura de la plataforma

- **Learning paths:** rutas de aprendizaje por tema (SQL Injection, XSS, Authentication, etc.).
- **Labs:** laboratorios interactivos, uno por vulnerabilidad.

Gratuitos.

Se generan instancias en la nube bajo demanda.
- **Teoría:** documentación completa para cada vulnerabilidad (con ejemplos y explicación).
- **Soluciones y vídeos:** disponibles para cada laboratorio, aunque Castillo recomienda no mirarlos hasta haberlo intentado.

### Por qué usarlo en el máster

Los laboratorios de PortSwigger tienen una ventaja clave sobre las máquinas de HTB: están 100% enfocados en una sola vulnerabilidad, sin "relleno" de enumeración, sin SSH, sin escalada de privilegios.

Son **micro-retos** donde se aprende una casuística concreta en cada uno.

Un mismo tipo de vulnerabilidad (ej.

Path Traversal) tiene **6 laboratorios** que van de lo más simple a lo más evasivo --- mismo concepto, seis contextos distintos.

Eso construye el mapa mental de "cuando veo X, pienso Y y pruebo Z".

**La dinámica:** en clase se harán 4-5 de los laboratorios más importantes.

El resto, los alumnos los hacen por su cuenta.

## 3.

Certificación BSCP --- Burp Suite Certified Practitioner

**BSCP** (*Burp Suite Certified Practitioner*) --- la certificación propia de PortSwigger, 100% centrada en hacking web.

### Características

Aspecto Detalle
 ----------------------------- ------------------------------------------------------------------------------
 **Precio** 89€
 **Duración** 4 horas
 **Formato** 3 laboratorios encadenados (aplicación web real)
 **Objetivo** Conseguir usuario admin, escalar privilegios dentro de la app y conseguir RCE
 **Tipo de examen** Proctored (con cámara supervisando al menos en parte del examen)
 **Herramienta obligatoria** Burp Suite Pro (hay versión "pirata" en Telegram del grupo)
 **Caduca** Posiblemente 2 años, pendiente de confirmar

**¿Vale la pena?** - A nivel de aprendizaje: **sí, mucho**.

Es de las mejores certificaciones para especialización web. - A nivel de mercado: está ganando reconocimiento pero todavía no tiene el peso del OSCP (\~2.000€, mucho más conocido). - En pliegos públicos y contrataciones de empresa: el eJPT se pide más.

El BSCP es más específico de web.

**BSCP vs.

OSCP:** - OSCP: general (enumeración, explotación, escalada, pivoting).

Para quien quiera ir por el camino general, tirar por HTB. - BSCP: full web.

Para quien quiera especializarse en web pentesting.

> [!important] **Lo más importante:** antes que tener la certificación, entender de verdad las vulnerabilidades.

Un papel que no va acompañado de comprensión no da valor en una auditoría real.

### Qué vulnerabilidades entran en el BSCP

Todas las categorías de PortSwigger pueden aparecer.

Las más probables: - Path Traversal / LFI - SQL Injection (incluyendo Blind SQLi) - XSS - Authentication failures - File Upload - Access control (IDOR)

## 4.

Vulnerabilidades que se verán en el módulo web (plan de Castillo)

Castillo presenta el mapa de lo que se cubrirá en las próximas semanas:

Vulnerabilidad Estado
 -------------------------------- -------------------------------------------------------
 **SQL Injection** Próxima semana, en profundidad
 **Cross-Site Scripting (XSS)** Ya visto, se refuerza
 **CSRF** Se verá algo, con foco en informes
 **Clickjacking** Solo teoría --- "relleno de informe"
 **Path Traversal / LFI / RFI** HOY --- 6 laboratorios
 **OS Command Injection** Se verá
 **Authentication failures** Se verá algo
 **Access Control (IDOR)** Se verá
 **File Upload** Se verá por PortSwigger
 **Information Disclosure** Se menciona brevemente en informes
 **WebSockets** Solo por cuenta propia (3 laboratorios en PortSwigger)
 **Prototype Pollution** Demasiado avanzado, no se cubre
 **LLM Hacking** Con Carlos, en paralelo
 **APIs** No se cubre en este bloque

**Nota sobre CSRF y Clickjacking:** son vulnerabilidades que aparecen mucho en informes reales pero que en la práctica tienen impacto limitado.

Castillo las llama "relleno de informe" --- reportables, pero no llevan a comprometer el sistema por sí solas.

## 5.

Path Traversal --- Repaso conceptual y detección

### ¿Qué es Path Traversal?

La vulnerabilidad que permite navegar fuera del directorio permitido usando `../`.

Al encontrar un parámetro que acepta una ruta de fichero sin validación, se puede usar para leer cualquier fichero del sistema.

**Distinción Path Traversal / LFI / RFI (repaso):**

Path Traversal → la vulnerabilidad base (parámetro acepta ../ sin filtrar) ↓ consecuencia LFI (Local File Inclusion) → leer ficheros locales del servidor ↓ variante RFI (Remote File Inclusion) → cargar ficheros desde servidor remoto

### Dónde buscar Path Traversal --- la clave de la detección

> [!important] **La pregunta clave:** ¿hay un parámetro en la petición HTTP que haga una llamada a un fichero del servidor?

La URL visible en el navegador no siempre lo muestra.

Muchas peticiones de carga de imágenes, recursos, CSS o scripts van "por detrás" y solo son visibles en: - **Burp HTTP History** (con Intercept OFF y proxy activo). - **DevTools → Network** (F12 → pestaña Red → recargar la página).

**Ejemplo del laboratorio 1:**

La URL del producto tiene `?productId=15` --- eso parece SQL, no fichero.

No es el vector.

Pero si en Burp se hace forward de las peticiones, aparece:

GET /image?filename=9.jpg

### Ahí está: `filename=9.jpg` → es una llamada directa a un fichero.

Eso activa todas las alarmas.

**El principio de detección:** \> "Cuando veas algo que hace una llamada a un archivo que puede estar contenido dentro de una ruta del servidor, ahí tienes un candidato a Path Traversal."

## 6.

Los 6 casos de Path Traversal (laboratorios de PortSwigger)

Castillo presentó los 6 laboratorios de Path Traversal que se harán en las próximas clases.

No se hace spoiler completo, pero el mapa mental:

Lab Tipo de caso Payload típico
 ----------- ---------------------------------------------- ---------------------------------------------
 **Lab 1** Simple sin restricciones `../../../../etc/passwd`
 **Lab 2** Ruta absoluta obligatoria `/etc/passwd` (sin `../`)
 **Lab 3** Secuencias `../` eliminadas (no recursivo) `....//....//etc/passwd`
 **Lab 4** Secuencias `../` URL-encoded `..%2F..%2F..%2Fetc/passwd`
 **Lab 5** Double URL encoding `..%252F..%252Fetc/passwd`
 **Lab 6** Validación del inicio de la ruta + null byte `/var/www/images/../../../etc/passwd%00.png`

### El Null Byte --- concepto nuevo

El **null byte** (`%00` o `\0`) es un carácter especial que en muchos lenguajes de programación (especialmente C/C++ y PHP antiguo) marca el final de una cadena.

Si el servidor valida que el fichero solicitado termine en `.jpg` o `.png`, se puede hacer:

../../../../etc/passwd%00.jpg

El servidor valida que la cadena termina en `.jpg` ✓.

Pero al procesarlo, el null byte actúa como fin de cadena y lee solo `../../../../etc/passwd`.

En versiones modernas de PHP (5.3+) este bypass ya no funciona, pero aparece en versiones antiguas y en otros lenguajes.

### Double URL Encoding

Si el servidor filtra `../` pero decodifica la URL antes de validar: - `../` → URL-encoded una vez: `..%2F` - Si lo filtra, double-encode: `..%252F` (el `%25` es el `%` encoded, dando `%2F` tras decodificar)

El servidor decodifica `%25` → `%` y sirve `%2F` que luego se interpreta como `/`.

### El parámetro de ruta absoluta

En algunos casos, el servidor requiere que la ruta empiece con un directorio específico (ej. `/var/www/images/`).

Técnicas: - Poner la ruta requerida + `/../../../etc/passwd` para salir de ella. - Si el servidor solo verifica el inicio pero no filtra `../`.

## 7.

Metodología en los laboratorios de PortSwigger

### Flujo de trabajo con Burp Suite

## 1.

Abrir PortSwigger Lab → acceder al link 2.

Activar FoxyProxy → proxy a 127.0.0.1:8080 3.

Intercept OFF (para no parar cada petición) 4.

Navegar por la aplicación — hacer clic en productos, imágenes, etc. 5.

Burp HTTP History → buscar peticiones con parámetros de fichero (filename=, file=, path=, img=...) 6.

Clic derecho → Send to Repeater 7.

Modificar el parámetro con los payloads de Path Traversal 8.

Analizar la respuesta: ¿devuelve el contenido del fichero?

### La trampa del productId

En el laboratorio 1, el parámetro visible es `?productId=15`.

Muchos alumnos van a probar Path Traversal aquí --- es incorrecto.

El productId es un identificador de base de datos, no una ruta de fichero.

El vector real está en la petición de carga de la imagen: `GET /image?filename=9.jpg`.

Eso solo se ve en el HTTP History de Burp, no en la URL del navegador.

**Lección:** Burp no sirve solo para modificar peticiones --- sirve para **ver peticiones que de otra forma son invisibles**.

## 8.

Notas sobre Burp Suite Pro

Castillo menciona que el BSCP obliga a usar **Burp Suite Pro**.

La versión Community (gratuita) tiene limitaciones: - El Intruder tiene rate limiting (delays artificiales entre peticiones). - No se pueden guardar proyectos entre sesiones. - Algunas extensiones no están disponibles.

La versión Pro (\~500€/año) quita esas limitaciones.

Existe una versión no oficial en el grupo de Telegram del máster.

### Alternativa oficial: PortSwigger ofrece 30 días de prueba que se pueden usar para el examen.

## 9.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
---------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------
 *Port Swinger / Port Suigger / Burpswider / por subirer* **PortSwigger** -- empresa creadora de Burp Suite y la plataforma de laboratorios web
*BSCP / Bursoid Certificate test / Bursoite Certified* **BSCP** (*Burp Suite Certified Practitioner*) -- certificación de PortSwigger de hacking web, 89€
 *OSCP / USCP / SCP* **OSCP** (*Offensive Security Certified Professional*) -- certificación de pentesting general (\~2.000€)
 *los laps / los labos* **Labs** -- laboratorios interactivos de PortSwigger, uno por tipo de vulnerabilidad
 *el FTPT / el de pivotting* **Entorno de pivoting** -- práctica 3 de Castillo con 4 máquinas encadenadas
 *Bluetooth / Blooting / BLE* **Bluetooth / BLE** (*Bluetooth Low Energy*) -- módulo que se dará en septiembre con Edu de Satek
 *Pad Traversal / Paz Traversal / Path transversal* **Path Traversal** -- vulnerabilidad que usa `../` para navegar fuera del directorio permitido
 *LFI / local five inclusing* **LFI** (*Local File Inclusion*) -- leer ficheros locales del servidor
 *RFI / remote find inclusing* **RFI** (*Remote File Inclusion*) -- cargar ficheros desde un servidor remoto
 *null bytes / el null byte / los nullbytes* **Null byte** (`%00`) -- carácter de fin de cadena que bypasea validaciones de extensión de fichero
 *double encoding / doble encoding / doblar* **Double URL encoding** (`%252F`) -- encodear dos veces para bypassear filtros que decodifican una vez
*el filename / el de las imágenes* **Parámetro** `filename=` -- el vector de Path Traversal en el laboratorio 1 (invisible en la URL del navegador, solo visible en Burp)
*las peticiones de detrás / las que no se ven* **Peticiones HTTP** "**background**" -- peticiones que el navegador hace automáticamente y que solo se ven en Burp HTTP History o en DevTools → Network
 *productID / el product ID* `?productId=` -- parámetro que apunta a la BD, NO a un fichero → no es el vector de Path Traversal
 *el repíter / el de enviar peticiones* **Repeater** -- módulo de Burp Suite para reenviar peticiones modificadas manualmente
 *Crossai scripting / Cross Scripting* **XSS** (*Cross-Site Scripting*) -- inyección de JavaScript en páginas web
 *SCRF / CSRF* **CSRF** (*Cross-Site Request Forgery*) -- fuerza al navegador de la víctima a hacer peticiones no autorizadas
 *Clic Hi jacking / Clickhuyack* **Clickjacking** -- técnica que superpone elementos invisibles para engañar al usuario sobre lo que está clicando
 *LMA hacking / LLM hacking* **LLM Hacking** -- ataques a modelos de lenguaje (prompt injection, jailbreaking, data exfiltration)
 *ProPointer / Proofpoint* **ProofPoint** -- plataforma de simulaciones de phishing para empresas
 *Satek / Saket* **Satek** -- empresa especializada en Bluetooth, cuyo responsable Edu impartirá el módulo de BLE

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/PortSwigger — Introducción y Path Traversal.md|PortSwigger — Introducción y Path Traversal]] — Certificaciones, IA en Ciberseguridad, Metasploit
- [[../../apuntes Andres/17.07.2026 PortSwigger Intro y 6 Casos Path Traversal.md|17.07.2026 PortSwigger Intro y 6 Casos Path Traversal]] — Certificaciones, IA en Ciberseguridad, Metasploit
- [[../../apuntes Chema/SSTI — PortSwigger.md|SSTI — PortSwigger]] — IA en Ciberseguridad, Metasploit, Netcat / Reverse Shells
- [[resumen_master_clase41.md|resumen_master_clase41]] — IA en Ciberseguridad, IDOR, Metasploit
- [[../../transcripciones/Julio/17.07.2026 PortSwigger Introduccion y repaso Path Traversal.md|17.07.2026 PortSwigger Introduccion y repaso Path Traversal]] — Certificaciones, Metasploit, Post-Explotación
- [[../../apuntes Chema/Maquinas/Vaccine (Tier 2) — Repaso en profundidad.md|Vaccine (Tier 2) — Repaso en profundidad]] — Certificaciones, IDOR, Metasploit

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #certificaciones #command-injection #csrf #escalada-privilegios #file-upload #hack-the-box #ia #idor #kali #lfi #metasploit #netcat #pentest #pivoting #post-explotacion #redes #reverse-shell #rfi #sqli #ssh #ssti #xss
