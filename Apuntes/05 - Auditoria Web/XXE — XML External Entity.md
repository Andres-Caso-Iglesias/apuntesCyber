

> [!info] Relacionado con
> [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[SSRF — Server-Side Request Forgery]]

---

## ① Fundamentos de XML

**XML (eXtended Markup Language)** = formato de datos estructurado. No es HTML.

| Concepto | Descripción |
|----------|-------------|
| **Estructurado** | Datos con jerarquía (etiquetas, atributos) |
| **No estructurado** | Texto libre, sin formato predefinido |
| **Entidades** | Variables que representan valores. Pueden ser internas o externas |
| **SYSTEM attribute** | Indica que la entidad carga un recurso externo (fichero, URL) |

### Ejemplo de entidad

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

> [!important] El SYSTEM attribute es la clave
> Cuando el servidor procesa `SYSTEM "file:///etc/passwd"`, **lee el fichero y lo sustituye** en la respuesta. Ahí es donde se explota XXE.

---

## ② Detección

### Cabeceras para forzar XML

| Cabecera | Valor | Efecto |
|----------|-------|--------|
| `Accept` | `application/xml` | El servidor responde en XML |
| `Content-Type` | `application/xml` | Envías XML al servidor |

> [!tip] Siempre probar estas cabeceras
> Muchas APIs aceptan XML aunque no lo muestren. Forzar `Accept: application/xml` puede revelar endpoints que procesan XML ocultos.

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
> Los ficheros PHP **no se pueden leer directamente** con `file://` porque contienen caracteres especiales. Usa `php://filter/convert.base64-encode` y decodifica el resultado con `base64 -d`.

---

## ⑤ XXE vs Path Traversal

| Característica | XXE | Path Traversal |
|---------------|-----|----------------|
| **Mecanismo** | Entidad XML externa | Ruta relativa `../` |
| **Formato** | XML (parámetros, bodies) | URLs, formularios, parámetros |
| **Ficheros** | Cualquier fichero legible | Mismos ficheros |
| **Blind** | Sí (con error-based) | Sí (con response timing) |
| **Filtrado** | Validación de XML | Validación de rutas |

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

---

## ⑦ File Upload y XXE

Las 4 formas en que un file upload puede ejecutar código:

| Forma | Mecanismo | Nivel |
|-------|-----------|-------|
| **Form 1** | Upload directo de fichero ejecutable (shell.php) | Básico |
| **Form 2** | Upload con rename → bypass de extensión | Intermedio |
| **Form 3** | Upload con validación de cabecera → bypass MIME | Intermedio |
| **Form 4** | Upload de fichero XML → XXE en el procesamiento | **Preview de XXE** |

> [!warning] Form 4 es la preview
> Cuando el servidor procesa ficheros XML subidos (SVG, DOCX, XLSX) y no valida el contenido, puedes inyectar XXE directamente en el fichero subido.

---

## ⑧ Quote de la sesión

> [!important] "Ya no estamos jugando con vulnerabilidades de 'hago un SQL'. Ahora ya tenemos algo más de chicha."
> XXE, SSTI y SSRF son vulnerabilidades que escalan directamente a RCE o compromiso de infraestructura. No son glitches menores.

---

## ⑨ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar peticiones XML modificadas |
| **curl** | Testing rápido de XXE desde terminal |
| **XXEtest (Burp extension)** | Automatización de tests XXE |

### curl de ejemplo

```bash
curl -X POST http://target/api \
 -H "Content-Type: application/xml" \
 -d '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>'
```

---

## Checklist de repaso

- [ ] ¿Sé qué es XML y qué es una entidad SYSTEM?
- [ ] ¿Puedo detectar XXE forzando cabeceras Accept/Content-Type?
- [ ] ¿Sigo el ciclo de explotación XXE correctamente?
- [ ] ¿Sé leer /etc/passwd y ficheros PHP con XXE?
- [ ] ¿Entiendo la diferencia entre XXE y Path Traversal?
- [ ] ¿Conozco el concepto de Error Base XXE?
- [ ] ¿Entiendo cómo un file upload puede vector de XXE?



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]] — Metasploit, Netcat / Reverse Shells, Redes
- [[../../apuntes Andres/20.07.2026 PortSwigger SSRF.md|20.07.2026 PortSwigger SSRF]] — Metasploit, Netcat / Reverse Shells, Redes
- [[../../apuntes Chema/SSTI — PortSwigger.md|SSTI — PortSwigger]] — Metasploit, Netcat / Reverse Shells, Redes
- [[SSTI — Server-Side Template Injection.md|SSTI — Server-Side Template Injection]] — Metasploit, Netcat / Reverse Shells, Redes
- [[../../apuntes Andres/11.07.2026 Owasp Top 10 XXE Labs II.md|11.07.2026 Owasp Top 10 XXE Labs II]] — Metasploit, Netcat / Reverse Shells, Redes
- [[../../apuntes Chema/Repaso Metodología Web — SSTI CasaPaco.md|Repaso Metodología Web — SSTI CasaPaco]] — Metasploit, Netcat / Reverse Shells, Redes

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]

> #burpsuite #command-injection #file-upload #lfi #metasploit #netcat #pentest #post-explotacion #redes #reverse-shell #ssrf #ssti #xxe
