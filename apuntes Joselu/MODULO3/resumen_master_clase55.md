> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 55**
> **Módulo:** MODULO3
> **Tema:** Clase 55
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 55. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Castillo** (Carlos Castillo).

Es la continuación directa de la Clase 54 --- el grupo no asimiló del todo el SSTI con tres horas de clase encima, así que Castillo abre con un repaso reforzado y a continuación hace los laboratorios de PortSwigger.

**Estructura del día:** 1.

Repaso visual del SSTI (diagrama en draw.io, más limpio que el paint de ayer). 2.

Laboratorio PortSwigger Lab 1 --- SSTI básico (sin Burp, se ve directamente). 3.

Laboratorio PortSwigger Lab 2 --- SSTI con identificación de motor. 4.

Máquina **Casa Paco** (HackerLabs) --- repaso de metodología web completa.

**Consejo final de Castillo antes de vacaciones:** recomendará al cierre de clase los temas/recursos para aprovechar el mes de agosto.

Mañana (miércoles) viene Carlos/Gómez a presentar formalmente la Práctica 1 con el enunciado, plazos de entrega y detalles.

## 2.

Repaso conceptual reforzado --- SSTI desde cero

### El flujo completo en un diagrama

[Input del usuario] ↓ ┌─────────────────────────────────┐ │ MOTOR DE PLANTILLA │ │ (Jinja2, ERB, FreeMarker...) │ └─────────────────────────────────┘ ↓ ↓ [SEGURO] [VULNERABLE] Input como dato Input dentro separado de la de la plantilla plantilla ↓ ↓ "Hola Carlos" "Hola 49" ↓ Escalar a RCE

### La comparación con SQL Injection (reforzada)

Aspecto SQLi SSTI
 ---------------------------- ----------------------------- -----------------------------------------
 **Lo que se inyecta** Código SQL Expresión del motor de plantillas
 **Dónde se ejecuta** Base de datos Servidor (motor de plantillas)
 **Payload de prueba** `'` (comilla simple) `{{7*7}}` (o equivalente del motor)
 **Señal de éxito** Error SQL / datos de BD Resultado `49`
 **Qué se puede conseguir** Datos de BD, bypass de auth RCE, leer ficheros, claves del framework

### Por qué el SSTI es más potente que el SQLi

> "Con el SQL Injection abusábamos de esas tablas y los datos.

Con el SSTI podemos llegar a conseguir hasta un RCE, que es la ejecución de comando, a partir de un 7 por 7."

El SQLi está más limitado a la base de datos.

El SSTI puede escalar hasta ejecutar comandos del sistema operativo porque el motor de plantillas tiene acceso al entorno de ejecución del servidor.

### El auditor de código ya es la IA

Castillo menciona que la auditoría manual de código fuente (revisar si el código es seguro o no) está siendo reemplazada por la IA.

Si durante una auditoría el cliente comparte su código fuente, basta con anonimizarlo y pasárselo a Claude para que detecte si la implementación de las plantillas es vulnerable.

El conocimiento del auditor es saber **qué buscar**, no memorizar la sintaxis exacta de cada motor.

## 3.

Cómo detectar SSTI --- las 3 opciones

### Opción 1 --- Polyglot (la navaja suiza)

La cadena de detección universal que combina sintaxis de todos los motores:

```bash
${{<%[%'"}}%\.
```

Se mete en el campo sospechoso.

Si el servidor devuelve un error diferente al habitual o procesa alguna parte de la cadena, hay SSTI.

### Opción 2 --- Probar payloads por motor uno a uno

{{7*7}} → Jinja2 / Tornado (Python), Twig (PHP) <%= 7*7 %> → ERB (Ruby) ${7*7} → FreeMarker (Java)

#{7*7} → Ruby alternativo

 *{7*7} → Thymeleaf (Java)

Si alguno devuelve `49` → motor identificado + SSTI confirmado.

### Opción 3 --- Fuzzing con diccionario SSTI de SecLists

SecLists incluye diccionarios con payloads SSTI para todos los motores:

# Encontrar el diccionario de SSTI en SecLists:

find /usr/share/seclists -name "*ssti*" -o -name "*template*"

# Típicamente en: /usr/share/seclists/Fuzzing/template-engines/

Usar **Burp Intruder** con el diccionario SSTI → analizar diferencias en código de estado o longitud de respuesta → el payload que devuelve algo diferente es el motor.

**Cuándo usar el fuzzing:** cuando el polyglot no da información clara o cuando hay muchos campos y se quiere automatizar la búsqueda.

## 4.

Laboratorio 1 de PortSwigger --- SSTI básico

**Objetivo:** leer `/etc/passwd` en un servidor vulnerable con Jinja2.

### Descripción del lab

La aplicación tiene un campo de "mensaje de ausencia" (out-of-office message) donde el usuario introduce texto.

El texto se usa en una plantilla del servidor para generar emails automáticos.

### Paso 1 --- Identificar el campo vulnerable

Cualquier campo cuyo valor se refleje en la respuesta del servidor.

Sin Burp en este caso --- la vulnerabilidad se ve directamente en la web.

### Paso 2 --- Confirmar SSTI

Introducir en el campo de mensaje:

{{7*7}}

Si la respuesta muestra `49` → **SSTI confirmado en Jinja2**.

### Paso 3 --- Identificar el motor

El `{{7*7}}` que devuelve `49` ya confirma que es **Jinja2** (o Tornado), ambos de Python y con la misma sintaxis de llaves dobles.

### Paso 4 --- Explotar para leer /etc/passwd

{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read() }}

**Por qué funciona este payload:** navega por la cadena de objetos de Python hasta llegar a `os`, importa el módulo y ejecuta el comando `cat /etc/passwd` con `popen`.

**Alternativa más limpia (si el anterior falla):**

{{ ''.__class__.__mro__.__subclasses__()('/etc/passwd').read() }}

**Referencia:** HackTricks → "SSTI" → "Jinja2" → sección de RCE.

## 5.

Laboratorio 2 de PortSwigger --- SSTI con identificación de motor

**Objetivo:** identificar el motor de plantillas correcto y explotar la vulnerabilidad.

### Por qué este lab es más complejo

A diferencia del lab 1, aquí no se sabe de antemano qué motor usa la aplicación.

Hay que pasar por las 3 fases:

### Fase 1 --- Detectar el campo y confirmar SSTI

Buscar en la aplicación campos que se reflejen: - En el lab: el campo de nombre de la plantilla de email o el nombre del producto/blog.

Meter el polyglot o el `{{7*7}}` básico.

### Fase 2 --- Identificar el motor mediante el error

**La técnica del error forzado:**

Si se mete una cadena que el motor no puede procesar correctamente, devolverá un error en el que aparece el nombre del framework/motor:

> [!warning] Ejemplo de error de Jinja2: TemplateSyntaxError: unexpected char '§' at position 0 in expression '§' Ejemplo de error de FreeMarker (Java): FreeMarker template error: Error evaluating expression...

El mensaje de error revela el motor.

Una vez identificado, consultar HackTricks con el nombre exacto del motor.

**Forzar el error de forma controlada:** meter una cadena incompleta o inválida para la sintaxis del motor:

{{ → FreeMarker devuelve un error específico <% + nada → ERB devuelve un error con "ERB" en el mensaje

### Fase 3 --- Explotar con el payload del motor identificado

Con el motor confirmado, buscar en HackTricks el payload de RCE correspondiente y adaptarlo.

## 6.

Consideraciones de detección y falsos positivos

### El campo NO refleja el input

Si meto `{{7*7}}` y la aplicación muestra literalmente `{{7*7}}` (no `49`), el campo está bien sanitizado para ese motor o la aplicación no usa plantillas ahí.

Probar otros campos.

### La longitud del campo como limitación

Si el campo tiene un límite de caracteres (ej. nombre de producto = 30 chars) y el payload de explotación tiene 80 caracteres: - Interceptar con **Burp Repeater** (Ctrl+R). - Modificar el valor directamente en el body de la petición, saltando el límite del frontend.

### Palabras bloqueadas por WAF

Si el payload devuelve `49` pero cuando se añade `import` o `system` devuelve un error 403 o un mensaje de bloqueo: - Usar técnicas de bypass: concatenación de strings (`'imp'+'ort'`), encoding, variables intermedias. - Consultar HackTricks → sección "bypass de filtros" del motor identificado.

## 7.

Máquina Casa Paco --- HackerLabs (repaso metodología web)

### Por qué esta máquina

Es una máquina "sencillita" que combina toda la metodología web en un único flujo.

Castillo la eligió específicamente para el repaso de metodología antes de las vacaciones --- no tiene una vulnerabilidad muy específica sino que aplica el workflow completo.

**Objetivo pedagógico:** que los alumnos vean que con la metodología vista hasta ahora (dirsearch, Wappalyzer, Burp, código fuente, fuzzing de parámetros) pueden resolver máquinas reales sin que les digan de antemano qué vulnerabilidad buscar.

### Metodología web repasada con Casa Paco

## 1.

Nmap → puertos abiertos (22 SSH + 80 HTTP) ↓ 2.

Wappalyzer → tecnologías (Apache, PHP, CMS, framework) ↓ 3.

Código fuente (Ctrl+U) → comentarios, rutas ocultas ↓ 4. robots.txt → directorios no indexados ↓ 5.

Dirsearch / GoBuster (-r recursivo) → directorios y ficheros ↓ 6.

Identificar funcionalidades interactivas: → Formularios → probar SQLi, SSTI, XSS → Subida de ficheros → probar File Upload → Parámetros de URL con nombres de fichero → probar Path Traversal/LFI → Parámetros con URLs → probar SSRF ↓ 7.

Burp Suite (Intercept OFF + HTTP History) → ver peticiones "ocultas" ↓ 8.

Explotar la vulnerabilidad encontrada ↓ 9.

Estabilizar shell → escalada de privilegios

### El mensaje de metodología de Castillo

> "Quiero que os deis cuenta de que con máquinas ya muy sencillitas no es ultrafácil, pero tampoco es una buena habilidad.

Para que os deis cuenta de que lo que necesitáis es soltura, que eso lo vamos a ganar poco a poco."

## 8.

Resumen de payloads SSTI por motor

Motor Lenguaje Payload de detección Resultado
 ---------------- ---------- ---------------------- ----------
 **Jinja2** Python `{{ 7*7 }}` `49`
 **Tornado** Python `{{ 7*7 }}` `49`
 **Mako** Python `${7*7}` `49`
 **ERB** Ruby `<%= 7*7 %>` `49`
 **FreeMarker** Java `${7*7}` `49`
 **Twig** PHP `{{ 7*7 }}` `49`
 **Nunjucks** Node.js `{{ 7*7 }}` `49`
 **Razor** .NET `@(7*7)` `49`

**Para el payload de explotación (RCE) una vez identificado el motor:** consultar HackTricks → "SSTI" → seleccionar el motor.

## 9.

Recomendaciones para el mes de agosto

Castillo indicó que al final de clase daría recomendaciones de qué hacer en vacaciones.

### El resumen:

- **Si queréis seguir practicando:** máquinas de HackerLabs (gratuitas, sin suscripción) con metodología web.

Son más accesibles que HTB para el nivel actual.
- **Si tenéis HTB:** aprovechar el Starting Point y algunas máquinas Easy del listado actual.
- **Si queréis estudiar teoría:** PortSwigger Web Security Academy --- completar los laboratorios de las vulnerabilidades ya vistas (Path Traversal, SSRF, SSTI, SQLi).
- **No hacer Directorio Activo todavía** --- ese módulo llega en septiembre con Yuba.
- **La Práctica 1** (presentada por Gómez el miércoles) tendrá plazo de 1-2 meses → no hay que hacerla en agosto si no se quiere.

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
-------------------------------------------- ---------------------------------------------------------------------------------------------------------------
 *STI / SCI / ese TI* **SSTI** (*Server-Side Template Injection*) -- inyección en motores de plantillas del lado del servidor
 *el 7 por 7 / el famoso 49* Payload de detección SSTI: si `{{7*7}}` devuelve `49`, el motor evalúa la expresión → SSTI confirmado
 *el polyglot / la cadena rara* **Polyglot SSTI** (`${{<%[%'"}}%\.`) -- payload que combina sintaxis de todos los motores para forzar un error
 *Ginja 2 / Jingya 2* **Jinja2** -- motor de plantillas Python para Flask/Django
 *ERP / el de Ruby* **ERB** (*Embedded Ruby*) -- motor de plantillas Ruby
 *Freemark / FreeMarkit* **FreeMarker** -- motor de plantillas Java
 *Tornado / el Python* **Tornado** -- framework web Python con motor de plantillas propio
 *el fucing de diccionario / foozing* **Fuzzing con diccionario SSTI** -- usar Burp Intruder con diccionarios SecLists de payloads SSTI
 *Port Sweager / los laboratorios* **PortSwigger Web Security Academy** -- plataforma de laboratorios de hacking web
 *el intruder / el de fuerza bruta* **Burp Intruder** -- módulo de Burp para iterar payloads automáticamente
 *Casa Paco / la máquina del nombre raro* **Casa Paco** -- máquina de HackerLabs con metodología web completa
 *Hacker Labs / HackerLab* **HackerLabs** (hackerlabs.academy) -- plataforma de máquinas vulnerables web gratuitas
 *GoFit / GoFish* **GoPhish** -- framework para campañas de phishing controlado
 *la práctica / la de Gómez / la de Carlos* **Práctica 1 del máster** -- entregable presentado por Carlos (Dani/Gómez) el miércoles
 *SAGPT / la IA* **ChatGPT / Claude** -- IAs usadas para generar diccionarios de payloads SSTI
 *Claudia / Claude* **Claude** (Anthropic) -- mencionado como herramienta para revisar código vulnerable
 *el parsear / al parsear* **Parsear** -- el proceso por el que el motor de plantillas interpreta y sustituye las variables

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Repaso Metodología Web — SSTI CasaPaco.md|Repaso Metodología Web — SSTI CasaPaco]] — Metasploit, Netcat / Reverse Shells, Nmap
- [[resumen_master_clase45.md|resumen_master_clase45]] — IA en Ciberseguridad, Metasploit, Nmap
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] — IA en Ciberseguridad, Metasploit, Nmap
- [[../../apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor.md|09.07.2026 XXE - XML External Entity y Máquina Castor]] — GoBuster, IA en Ciberseguridad, Nmap
- [[../../transcripciones/Septiembre/02.09.2026 Repaso General II.md|02.09.2026 Repaso General II]] — IA en Ciberseguridad, Metasploit, SSRF
- [[../../apuntes Andres/28.07.2026 Repaso General Metodologia Web y Command Injection.md|28.07.2026 Repaso General Metodologia Web y Command Injection]] — Hydra, Metasploit, Netcat / Reverse Shells

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #dirsearch #escalada-privilegios #file-upload #gobuster #hack-the-box #hydra #ia #lfi #metasploit #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #sqli #ssh #ssrf #ssti #xss #xxe
