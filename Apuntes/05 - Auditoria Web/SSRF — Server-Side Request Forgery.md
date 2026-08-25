

> [!info] Relacionado con
> [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[SSTI — Server-Side Template Injection]]

---

## ① Definición

**SSRF (Server-Side Request Forgery)** = el servidor ejecuta peticiones HTTP controladas por el atacante.

```
Atacante → envía URL/param → Servidor hace la petición → Responde al atacante
```

> [!important] La clave
> El servidor actúa como **proxy involuntario**. El atacante no ve la petición directamente, sino que el servidor la ejecuta por él y devuelve el resultado.

---

## ② 3 contextos canónicos

| Contexto | Dirección | Qué se obtiene |
|----------|-----------|----------------|
| **Localhost** | `http://127.0.0.1` o `http://localhost` | Servicios internos del propio servidor (paneles admin, APIs internas) |
| **Red interna** | `http://192.168.x.x`, `http://10.x.x.x` | Otros servidores de la red corporativa inalcanzables externamente |
| **AWS Metadata** | `http://169.254.169.254` | Credenciales IAM, configuración de la instancia EC2 |

> [!warning] AWS Metadata es CRÍTICO
> En entornos cloud, la metadata devuelve **credenciales temporales de IAM** que pueden comprometer toda la infraestructura. Siempre probar `http://169.254.169.254/latest/meta-data/`.

---

## ③ Bypasses de restricciones

| Técnica | Descripción | Ejemplo |
|---------|-------------|---------|
| **IP decimal** | Convertir IP a número decimal | `2130706433` = `127.0.0.1` |
| **IP octal** | Usar notación octal | `0177.0.0.1` = `127.0.0.1` |
| **DNS trick** | Usar dominio que resuelve a interna | `localtest.me` → `127.0.0.1` |
| **Open redirect chain** | Encadenar redirect para evadir validación | Redirigir a `http://127.0.0.1` vía 302 |
| **UserInfo + Fragment** | Insertar credenciales ficticias y fragmentos | `http://127.0.0.1@attacker.com` o `http://evil.com#@127.0.0.1` |
| **Double encoding** | Codificar el encode | `%252e%252e%252f` (doble `%25`) |

> [!tip] No os memorices payloads
> **Entiende la LÓGICA**: el servidor valida la URL de entrada. Si un filtro bloquea `127.0.0.1`, busca la misma dirección en otro formato. El objetivo siempre es el mismo: hacer que el servidor pida a un destino interno.

---

## ④ Blind SSRF

Cuando el servidor **no devuelve** la respuesta de la petición interna en la respuesta HTTP.

### Detección con Burp Collaborator

1. Crear un dominio Collaborator
2. Inyectarlo como parámetro: `url=http://YOUR-COLLABORATOR.burpcollaborator.net`
3. Si el servidor hace la petición → aparece un hit en Collaborator
4. Confirmar SSRF aunque no veas la respuesta

> [!note] Blind SSRF es igual de peligroso
> Aunque no veas la respuesta, el servidor **sí hizo la petición**. Sirve para: confirmar existencia de servicios internos, exfiltrar datos por DNS, y ejecutar webhooks internos.

---

## ⑤ Checklist mental (flowchart)

```
¿El servidor acepta URL/parámetros de usuario?
 → SÍ → Probar localhost (127.0.0.1, 0.0.0.0, localhost)
 → ¿Responde algo? → SSRF confirmado
 → No responde → Probar red interna (10.x, 192.168.x)
 → BLOQUEA la IP directa → Probar bypasses:
 → IP decimal/octal
 → DNS trick (localtest.me)
 → Open redirect chain
 → UserInfo/Fragment con double encoding
 → ¿No devuelve contenido? → Blind SSRF
 → Probar Collaborator/DNS para confirmar
```

---

## ⑥ PortSwigger Labs

> [!tip] Practicar en PortSwigger Web Security Academy
> Los labs de SSRF cubren desde básico hasta bypasses avanzados:
> - SSRF con filter bypass from internal network
> - SSRF with filter bypass via URL resolution
> - Blind SSRF with out-of-band detection
> - SSRF via Webhook

---

## ⑦ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar y modificar peticiones con payloads SSRF |
| **Burp Intruder** | Iterar IPs, puertos, formatos de bypass |
| **Burp Collaborator** | Detección de Blind SSRF vía DNS/HTTP callbacks |
| **curl** | Testing rápido de SSRF desde terminal |

---

## Checklist de repaso

- [ ] ¿Sé explicar qué es SSRF y por qué el servidor ejecuta las peticiones?
- [ ] ¿Conozco los 3 contextos canónicos (localhost, red interna, AWS metadata)?
- [ ] ¿Entiendo al menos 3 técnicas de bypass?
- [ ] ¿Sé qué es Blind SSRF y cómo detectarlo con Collaborator?
- [ ] ¿Puedo seguir el flowchart mental de SSRF en un lab?
- [ ] ¿Entiendo que SSRF está en OWASP Top 10 A01 (2025)?