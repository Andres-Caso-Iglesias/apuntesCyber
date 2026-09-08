> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 49**
> **Módulo:** MODULO3
> **Tema:** Clase 49
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 49. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

Esta sesión cubre dos vulnerabilidades en paralelo: el **cierre de los laboratorios pendientes de SSRF** y la **introducción completa a SSTI (Server-Side Template Injection)**.

El hilo conductor entre ambas es el mismo principio que vertebra todo el módulo web: cuando el servidor procesa entrada de usuario como si fuera código o instrucciones propias, el atacante puede redirigir ese procesamiento hacia objetivos no previstos.

SSTI es quizás la vulnerabilidad más elegante del módulo: la diferencia entre **mostrar** una variable y **ejecutarla** es una sola línea de código, y esa línea puede dar **RCE completo**.

# Cierre de SSRF --- bypass con redirección abierta

Se completó el laboratorio de SSRF pendiente: el que usa una **redirección abierta** como vector para alcanzar infraestructura interna bloqueada.

**Contexto:** el servidor tiene un filtro que bloquea peticiones SSRF a `192.168.0.12`.

Sin embargo, la misma aplicación tiene una funcionalidad de "siguiente producto" que acepta una URL en el parámetro `path` y redirige a ella sin validación.

Esa es una redirección abierta.

La cadena de explotación aprovecha que **el filtro SSRF evalúa la URL antes de que se procesen las redirecciones**.

Si el parámetro SSRF apunta a la URL de la redirección abierta (una URL legítima del propio servidor), el filtro la deja pasar.

Cuando el servidor procesa la petición, sigue la redirección automáticamente y termina haciendo la petición al destino interno bloqueado:

stockApi=/product/nextProduct?path=http://192.168.0.12/admin

El filtro ve `/product/nextProduct` y lo considera una URL interna legítima.

El servidor sigue la redirección a `192.168.0.12/admin` y devuelve el contenido.

> [!important] > **Idea clave:** un filtro que evalúa la URL inicial pero no el destino final de las redirecciones siempre puede ser bypasseado encadenando con cualquier redirección abierta del sistema.

# Qué es SSTI y por qué ocurre

Los motores de plantillas como **Jinja2, Twig, Freemarker o Smarty** permiten que el backend inyecte variables dinámicas en el HTML antes de enviarlo al navegador.

La sintaxis varía por motor, pero el principio es el mismo: una expresión entre delimitadores especiales se evalúa en el servidor y se sustituye por su resultado.

En Jinja2 la sintaxis es doble llave: si el template contiene `{{ nombre }}`, el servidor sustituye esa expresión por el valor de la variable `nombre`.

El problema aparece cuando el desarrollador construye el template **concatenando directamente la entrada del usuario** en la cadena que va a ser procesada:

template = "Hola " + request.args.get('nombre') render_template_string(template)

Si el usuario introduce `{{ 7*7 }}` como nombre, el motor evalúa la expresión y devuelve `49`.

El servidor ha ejecutado código arbitrario del atacante.

Si en lugar de una multiplicación se introduce código que llame a funciones del sistema operativo, se obtiene **RCE**.

> **Metáfora útil:** el desarrollador ha dejado abierto el canal entre el front y el motor de ejecución del servidor.

La diferencia entre *mostrar* lo que escribe el usuario y *ejecutar* lo que escribe el usuario es una función de render.

# Detección de SSTI --- el árbol de decisión

La detección sigue un árbol sistemático: se inyectan expresiones matemáticas con la sintaxis de distintos motores y se observa si el resultado aparece **evaluado** o como **texto literal**.

**Nivel 1 --- ¿hay motor de plantillas?**

- Si `${7*7}` aparece como `49` → hay un motor de plantillas activo.
- Si aparece como el texto literal `${7*7}` → no hay motor, o el valor está siendo escapado.

**Nivel 2 --- identificar el motor concreto** (por diferencias de sintaxis):

- Si `{{7*7}}` da `49` → puede ser Jinja2 o Twig.
- Si `{{7*'7'}}` da `49` → es **Jinja2** (evalúa como multiplicación).
- Si da `7777777` → es **Twig** (PHP evalúa entero × string como repetición).
- Si `${7*7}` da `49` → puede ser **Freemarker** o **Smarty**.

Una vez identificado el motor, el payload de explotación varía.

Para **Jinja2**, el camino hacia RCE pasa por la jerarquía de clases de Python:

{{config.__class__.__init__.__globals__['os'].popen('id').read()}}

Para **Twig** se usa la función `_self.env`:

{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

> [!important] > **Idea clave:** antes de buscar el payload hay que identificar el motor.

El mismo síntoma (expresión evaluada) puede tener payloads completamente distintos.

Usar el payload equivocado da error sin resultado y puede alertar al sistema.

# Laboratorio 1 --- SSTI básico en Jinja2

La aplicación devuelve mensajes de error que incluyen directamente el valor del parámetro en la respuesta.

Al inyectar `{{7*7}}` en el parámetro de búsqueda, el response devuelve `49`. **Confirmado SSTI en Jinja2.**

El payload para leer `/etc/passwd` en Jinja2 usa la cadena de clases de Python para alcanzar el módulo `os` y ejecutar comandos: clase del objeto de configuración → método de inicialización → variables globales → módulo `os` → `popen` → lectura del output.

La cadena de clases varía entre versiones de Python y entre aplicaciones, así que en la práctica se usa **PayloadsAllTheThings** o **HackTricks** para encontrar el payload correcto del contexto.

# Laboratorio 2 --- SSTI en Jinja2 sin conocer el nombre del objeto

Aquí no hay un objeto de configuración directamente accesible.

La técnica es **traversar la jerarquía de clases de Python** desde el objeto más básico disponible: una cadena de texto vacía.

En Python todos los objetos heredan de `object`.

Desde cualquier instancia se accede a la clase base y, desde ahí, a todas las subclases registradas en el intérprete.

Una de esas subclases es `subprocess.Popen`, que permite ejecutar comandos:

''.__class__.__mro__[1].__subclasses__()

Esto devuelve la lista de todas las subclases disponibles.

Se busca el índice de `subprocess.Popen` en esa lista y se invoca con el comando deseado.

El índice **varía entre entornos**, por lo que hay que iterarlo.

# Laboratorio 3 --- SSTI en Freemarker

Freemarker es un motor de plantillas de **Java** muy común en aplicaciones empresariales.

La sintaxis para ejecutar comandos usa la clase `freemarker.template.utility.Execute`:

<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}

La primera parte asigna una instancia de la clase `Execute` a la variable `ex`.

La segunda ejecuta el comando `id` llamando a esa instancia como si fuera una función.

El resultado aparece directamente en el response.

> **Nota de mercado (Castillo):** Freemarker aparece con frecuencia en aplicaciones Java de **banca y sector público**, dos entornos con alta presencia en auditorías reales en España.

Conocer este payload tiene valor directo en el mercado laboral.

# Laboratorio 4 --- SSTI con salida en contexto de código

Aquí la expresión inyectada aparece dentro de un bloque de código **JavaScript** en el HTML de respuesta, no en texto visible.

Esto no cambia la vulnerabilidad, pero sí la forma de confirmarla: hay que **inspeccionar el código fuente** de la respuesta, no el HTML renderizado, para ver si la expresión fue evaluada.

El payload y la técnica son idénticos, pero el **contexto de salida** importa para entender por qué el resultado no aparece visible en la página aunque la vulnerabilidad esté activa.

# SSTI ciego (Blind SSTI)

Si la expresión evaluada no aparece en ningún lugar del response (ni en HTML visible ni en código fuente), hay **SSTI ciego**.

La detección se hace igual que en el SSRF ciego: con **Burp Collaborator**.

Si la expresión inyectada incluye una petición HTTP a la URL del Collaborator, y esa petición llega, se confirma que la expresión fue evaluada en el servidor aunque no se vea el resultado.

Para exfiltrar datos se usan técnicas **out-of-band**: el payload ejecuta un comando que hace un `curl` o `wget` a la URL del Collaborator, incluyendo el output del comando en la URL como parámetro.

# Recapitulación integrada

SSTI cierra el ciclo de vulnerabilidades de inyección del lado del servidor construido a lo largo del módulo:

- **Path traversal:** inyectaba rutas de ficheros.
- **XXE:** inyectaba entidades XML.
- **SSRF:** inyectaba URLs.
- **SQL Injection:** inyectaba código SQL.
- **SSTI:** inyecta directamente en el motor de ejecución del servidor → el vector de escalada más directo a **RCE** cuando está presente.

El mapa mental que queda: **encontrar el parámetro → identificar el motor → buscar el payload en PayloadsAllTheThings o HackTricks para ese motor → confirmar ejecución → escalar a RCE.**

La próxima sesión abre el módulo de **SQL Injection**, el más extenso del bloque web y el que más variantes tiene en entornos reales.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI — Server-Side Template Injection]] — SQL Injection, SSTI, XXE
- [[../../Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE — XML External Entity]] — Post-Explotación, SSTI, XXE
- [[../../transcripciones/Julio/22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento.md|22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento]] — Empleabilidad, SQL Injection, SSTI
- [[../../apuntes Andres/21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI.md|21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI]] — Empleabilidad, SQL Injection, XXE
- [[../../transcripciones/Julio/21.07.2026 PortSwigger SSTI + cierre SSRF.md|21.07.2026 PortSwigger SSTI + cierre SSRF]] — Empleabilidad, SQL Injection, XXE
- [[../../apuntes Andres/20.07.2026 PortSwigger SSRF.md|20.07.2026 PortSwigger SSRF]] — SQL Injection, SSTI, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #empleabilidad #ia #lfi #netcat #post-explotacion #redes #reverse-shell #sqli #ssrf #ssti #xxe
