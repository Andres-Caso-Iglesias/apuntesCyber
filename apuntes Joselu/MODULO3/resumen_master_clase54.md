> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 54**
> **Módulo:** MODULO3
> **Tema:** Clase 54
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 54. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Castillo** (Carlos Castillo).

Es la última semana antes de las vacaciones de agosto --- quedan solo lunes, martes y miércoles.

La clase tiene dos bloques:

1. **SSTI (Server-Side Template Injection)** --- vulnerabilidad nueva, explicada desde cero. 2. **Máquina de HTB** con metodología repasada (práctica en vivo).

**Apertura técnica relevante:** Castillo comparte que PortSwigger acaba de anunciar **Burp AI** --- una IA integrada en Burp Suite Pro que audita aplicaciones web de forma autónoma, detecta vulnerabilidades y lanza peticiones sin intervención humana.

El scope y el nivel de ruido son configurables.

La novedad es tan reciente que Castillo aún no la ha probado.

Menciona que internamente en Cibersia Security tienen una herramienta propia equivalente llamada "el bicho", que hace auditorías web pasivas y activas de forma completamente automatizada.

**Anuncio:** el miércoles vendrá Carlos (Dani/Gómez) a presentar formalmente la Práctica 1 del máster.

## 2. ¿Qué son las plantillas (templates)?

Para entender SSTI primero hay que entender qué es una **plantilla**.

Una plantilla es un texto con **huecos variables** que el servidor rellena dinámicamente para cada usuario.

En vez de hardcodear el texto completo (lo que haría que todos vieran lo mismo), se define la estructura una sola vez y se inserta el valor correcto en tiempo de ejecución.

**Ejemplo visual:**

# La plantilla (con la variable entre llaves):

"Hola, {{ nombre }}.

Bienvenidos de nuevo."

# Los datos del usuario:

nombre = "Carlos"

# El resultado que devuelve el servidor:

"Hola, Carlos.

Bienvenidos de nuevo."

**¿Dónde se usan las plantillas?** - Cualquier texto de la web que cambia según el usuario: "Bienvenido, \[nombre de usuario\]", "Tu empresa \[nombre de empresa\]", mensajes de email personalizados, facturas, etc. - En la demo en vivo: el panel de Cibersia Security SL mostraba "Bienvenido de vuelta a Cibersia Security SL" --- el nombre de la empresa viene de una plantilla.

### Motor de plantillas (template engine)

El **motor** es el componente de software que procesa la plantilla, busca las variables y sustituye los huecos con los valores reales.

Cada lenguaje de programación tiene su(s) propio(s) motores:

Lenguaje Motores de plantillas
 ------------- ----------------------
 **Ruby** ERB
 **Python** Tornado, Jinja2, Mako
 **Java** FreeMarker, Velocity
 **PHP** Twig, Smarty
 **Node.js** Nunjucks, Pug
 **.NET** Razor

La sintaxis de cómo se insertan las variables varía entre motores --- por eso es tan importante identificar cuál se usa.

## 3. ¿Qué es SSTI? (Server-Side Template Injection)

**SSTI** (*Server-Side Template Injection*) es una vulnerabilidad que ocurre cuando el **input del usuario se inserta directamente en la plantilla** (en lugar de pasarlo como dato al motor), permitiendo al atacante inyectar código que el motor ejecuta.

### El flujo seguro vs. el vulnerable

**Lado seguro (correcto):**

# El input del usuario llega como DATO, separado de la plantilla:

plantilla = "Hola, {{ nombre }}" datos = {"nombre": input_del_usuario} resultado = motor.render(plantilla, datos)

Si el usuario escribe `7*7`, la plantilla recibe el texto literal `"7*7"` y muestra: `Hola, 7*7`.

Sin ejecutar nada.

**Lado vulnerable (incorrecto):**

# El input del usuario se concatena DENTRO de la plantilla:

plantilla = "Hola, " + input_del_usuario # ← el problema resultado = motor.render(plantilla)

Si el usuario escribe `{{ 7*7 }}`, la plantilla queda como `"Hola, {{ 7*7 }}"`, y el motor **evalúa la expresión** y devuelve: `Hola, 49`.

### El test de detección: `7*7 = 49`

**El payload de detección universal:** si el usuario introduce `{{7*7}}` (o la sintaxis equivalente del motor) en un campo y la respuesta muestra `49` en vez de `7*7`, el motor está ejecutando el código → **SSTI confirmado**.

> "En el momento que veis el 49, pensar que ya lo habéis conseguido." --- Castillo

**¿Por qué** `7*7`**?** Es la convención del sector --- todos los writeups, tutoriales y referencias lo usan como test de confirmación.

Si buscas SSTI en HackTricks o en cualquier referencia, siempre aparece `7*7 = 49` como el indicador.

### La analogía con SQL Injection

SQLi SSTI
 -------------- ---------------------------------------------------- ------------------------------------------------
 **Concepto** El input del usuario se inserta en la consulta SQL El input del usuario se inserta en la plantilla
 **Ejecuta** Código SQL en la base de datos Expresiones del motor de plantillas
 **Detectar** `'` provoca error SQL `{{7*7}}` devuelve 49
 **Objetivo** Manipular la BD, extraer datos RCE, leer ficheros, robar claves

## 4.

Las 3 fases del ataque SSTI

### Fase 1 --- Detección (¿existe SSTI?)

Buscar campos de la aplicación cuyo valor se **refleje en la web** --- campos de nombre de usuario, nombre de empresa, configuración de perfil, asunto de email, etc.

> [!warning] Probar con el **payload polyglot** --- una cadena que combina la sintaxis de todos los motores principales para provocar un error:

```bash
${{<%[%'"}}%\.
```

Si la aplicación procesa este payload y devuelve un error diferente al habitual, hay indicios de SSTI.

Si devuelve el texto literal, probablemente está bien sanitizado.

**Después del polyglot**, probar con los payloads específicos de cada motor para confirmar cuál produce el `49`.

### Fase 2 --- Identificación del motor

Identificar qué motor de plantillas está en uso es **crítico** porque la sintaxis de explotación es diferente en cada uno.

**Métodos de identificación:**

1. **Error-based:** el payload polyglot puede provocar un error que revela el nombre del framework en el stack trace. 2. **Fingerprinting por sintaxis:** probar los payloads de cada motor y ver cuál devuelve 49. 3. **Wappalyzer / cabeceras HTTP:** a veces revelan el framework backend (ej. `X-Powered-By: Jinja2`).

**Payloads de detección por motor:**

Motor Payload de prueba Resultado esperado
 ------------------------------- ------------------- -------------------
 **ERB (Ruby)** `<%= 7*7 %>` `49`
 **Tornado / Jinja2 (Python)** `{{ 7*7 }}` `49`
 **FreeMarker (Java)** `${7*7}` `49`
 **Twig (PHP)** `{{ 7*7 }}` `49`

### Fase 3 --- Explotación

Una vez identificado el motor, usar la sintaxis específica para ejecutar comandos del sistema.

El objetivo es escalar del `49` a un **RCE** (*Remote Code Execution*).

**Ejemplo con Jinja2 (Python):**

# Leer /etc/passwd via SSTI en Jinja2:

{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read() }}

**Referencia:** HackTricks → buscar "SSTI" → seleccionar el motor identificado → copiar el payload de RCE.

**Nota importante de Castillo:** no hace falta memorizar estos payloads.

La IA o HackTricks los proporcionan en segundos una vez que se sabe el motor.

Lo importante es entender el concepto y el flujo.

## 5.

Qué se puede conseguir con SSTI

Dependiendo del motor y sus restricciones:

Acción Posibilidad
 ------------------------------------------------ ---------------------------------------------
 **RCE** (ejecutar comandos del sistema) Sí --- el objetivo principal
 **Leer ficheros del servidor** (`/etc/passwd`) Sí
 **Robar la clave secreta del framework** Sí --- da acceso total en algunos frameworks
 **Listar variables internas de la aplicación** Sí
 **Saltar un sandbox/Docker** Posible con técnicas avanzadas

### El caso Django

Django tiene su propio motor de plantillas y **restringe** el acceso a objetos del sistema --- no permite pivotar directamente a RCE.

Pero sí permite leer atributos internos del framework, y si se consigue **la clave secreta** (`SECRET_KEY`), se puede falsificar tokens de sesión y comprometer toda la aplicación.

### SSTI y Docker/sandboxes

Si el motor de plantillas corre dentro de un contenedor Docker (sandbox), un SSTI exitoso solo da acceso al contenedor, no al host.

Para saltar del contenedor al host hace falta una vulnerabilidad adicional de escape de contenedor --- técnicas avanzadas que entran en el módulo de pivoting.

## 6.

El polyglot SSTI --- el payload universal

El **polyglot** combina sintaxis de todos los motores en una sola cadena:

```bash
${{<%[%'"}}%\.
```

**Por qué funciona:** cada motor intentará parsear la cadena con su propia sintaxis.

Si alguno reconoce su sintaxis y la evalúa, devolverá un error o un resultado diferente al esperado.

Eso es el indicio.

**No es magia:** si la aplicación está bien sanitizada, el polyglot llegará como texto literal y no pasará nada.

La ausencia de error también es información --- indica que probablemente no hay SSTI o que está bien mitigado.

## 7.

Dónde buscar SSTI en una aplicación

Cualquier campo que: 1. **Acepte input del usuario**, y 2. **Refleje ese input en la web** (en la misma página u otra).

### Ejemplos comunes: - Campo de nombre de usuario o empresa (se muestra en el dashboard). - Asunto o cuerpo de emails generados por la aplicación. - Nombres de plantillas de documentos (facturas, contratos). - Parámetros de URL que se muestran en mensajes de error. - Campo de búsqueda cuyo término se muestra en "Resultados para: \[término\]".

**Lo que no es candidato:** campos cuyo valor no se refleja en ningún sitio de la web.

## 8.

Limitaciones prácticas

### Longitud del campo

Si el campo vulnerable tiene un límite de caracteres (ej. nombre de empresa = 30 chars), el payload de explotación puede ser demasiado largo para caber.

Solución: interceptar con Burp Repeater y enviar el payload sin la limitación del frontend.

### Palabras bloqueadas

Algunos WAFs o validaciones bloquean palabras clave del payload (`import`, `system`, `os`, `class`).

Solución: técnicas de bypass (encoding, concatenación de strings, uso de variables intermedias).

### Motor que detecta pero no escala

Es raro, pero puede ocurrir que el motor evalúe `{{7*7}}` y devuelva `49`, pero bloquee los payloads de RCE.

En ese caso, intentar otras acciones (leer ficheros, robar la SECRET_KEY) antes de declarar que el RCE no es posible.

## 9.

Burp AI --- la novedad del día

PortSwigger anunció (el mismo día de la clase) **Burp AI** --- un agente de IA integrado en Burp Suite Pro que: - Audita aplicaciones web de forma autónoma. - Intercepta el tráfico como un auditor humano. - Detecta vulnerabilidades y lanza peticiones sin intervención. - Permite configurar el scope y el nivel de ruido.

**Conexión con el módulo de IA del máster:** el funcionamiento es exactamente lo que Carlos (Dani) ha estado enseñando en las clases de IA --- un agente con acceso a las herramientas de Burp Suite que toma decisiones autónomas.

La diferencia es que Burp AI tiene acceso nativo a toda la información del proxy, sin necesidad de integraciones externas.

Castillo planea probarlo y, si es interesante, mostrarlo en clase al día siguiente.

## 10.

Flujo completo de un ataque SSTI

## 1.

Reconocimiento de la aplicación → Identificar campos de input que se reflejan en la web ↓ 2.

Probar el polyglot: ${{<%[%'"}}%\. → ¿Error diferente? → Indicio de SSTI ↓ 3.

Probar payloads por motor: {{7*7}}, <%=7*7%>, ${7*7}... → ¿Devuelve 49? → SSTI confirmado ↓ 4.

Identificar el motor → Por el error, por la sintaxis que funcionó, por Wappalyzer ↓ 5.

Consultar HackTricks → SSTI → [motor identificado] → Copiar el payload de RCE ↓ 6.

Lanzar el payload (via Burp Repeater si hay límite de chars) → ¿Devuelve output de comando? → RCE confirmado ✓ ↓ 7.

Escalar: leer /etc/passwd, SSH, reverse shell...

## 11.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
-------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------
 *STI / SCI / SCTI / ese TI* **SSTI** (*Server-Side Template Injection*) -- inyección en motores de plantillas del lado del servidor
 *plantilla / template* **Template** -- texto con huecos de variable que el motor rellena dinámicamente
 *motor de plantilla / template engine* **Template engine** -- componente que procesa plantillas y sustituye variables: Jinja2, Twig, FreeMarker...
 *hardcoreado / hardcodeado* **Hardcodeado** -- valor fijo escrito directamente en el código, sin variación por usuario
 *RV / ERV / RB* **ERB** (*Embedded Ruby*) -- motor de plantillas de Ruby
 *Tornado / el de Python* **Tornado** -- framework web Python con motor de plantillas propio
 *Ginja 2 / Jingya 2 / Ginja 2* **Jinja2** -- motor de plantillas para Python, muy usado con Flask y Django
 *Frey Marker / Free Markit* **FreeMarker** -- motor de plantillas para Java
 *T Twing / el de PHP* **Twig** -- motor de plantillas para PHP
 *No DJS / Nunjungs / el de Node* **Nunjucks** -- motor de plantillas para Node.js
 *Razor / Radzor* **Razor** -- motor de plantillas para .NET (ASP.NET)
 *Django / el que lo restringe* **Django** -- framework Python cuyo motor de plantillas restringe el acceso a objetos del sistema
 *el 49 / el famoso 49* El resultado de `7*7 = 49` --- señal universal de que el motor evaluó la expresión → SSTI confirmado
 *el oneliner raro / el polyglot* **Polyglot SSTI** (`${{<%[%'"}}%\.`) -- payload que combina sintaxis de todos los motores para forzar un error
 *Burp AT / Burp IEA* **Burp AI** -- nueva funcionalidad de Burp Suite Pro que audita aplicaciones web de forma autónoma con IA
 *el bicho / el bicho Shu* Herramienta interna de Cibersia Security para auditorías web pasivas y activas automatizadas
 *PORT Sweager / Port Sweger* **PortSwigger** -- empresa creadora de Burp Suite y la plataforma de laboratorios web
 *Inventario / mi aplicación* **Aplicación demo de Castillo** (parece ser una herramienta de gestión interna de Cibersia)
*la SECRET KEY / la clave secreta del framework* **SECRET_KEY** -- clave interna del framework (ej.

Django) que, si se extrae via SSTI, permite falsificar tokens de sesión
 *sandbox / la minimáquina* **Sandbox / Docker** -- entorno aislado; un SSTI dentro de un contenedor solo da acceso al contenedor, no al host
 *Claudia / Claude / la IA* **Claude** (Anthropic) -- IA usada por los alumnos para buscar payloads y resolver dudas durante la clase

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*
