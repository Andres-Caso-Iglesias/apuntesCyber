

> [!info] Relacionado con
>

---

## ① ¿Qué es Burp Suite?

**Burp Suite** es un **framework de auditoría web**. El proxy es su núcleo, pero es mucho más: Repeater, Intruder, Decoder, Comparer...

> [!warning] ERROR COMÚN
> Decir que "Burp es un proxy" es **incompleto**. Es un framework; el proxy es su dependencia crítica.

---

## ② Front vs Back "” Dónde tenemos el control

```
FRONT (tu navegador) "” TIENES EL CONTROL
 →“
PROXY de Burp "” intercepta (texto claro, antes de TLS)
 →“
Modificas la petición → saltas controles del front
 →“
WAF "” última defensa antes del server
 →“
BACK (servidor) "” valida integridad (o explota)
```

> [!important] CONCLUSIÓN
> Si los controles de seguridad están **solo en el front**, son **bypasseables**. La defensa moderna securiza el **back** y añade un **WAF**.

---

## ③ Configuración

### Certificado de Burp

1. Con Burp abierto → `http://localhost:8080` → **CA Certificate** → descargar
2. Firefox → Administrar certificados → Importar → seleccionar cacert
3. Verificar: debe aparecer **PortSwigger** como CA

### Foxy Proxy

| Campo | Valor |
|-------|-------|
| Nombre | Burp Suite |
| Host | 127.0.0.1 |
| Puerto | **8080** |

> [!tip] FLUJO
> Burp levanta proxy en `127.0.0.1:8080` → FoxyProxy reenvía el tráfico del navegador → Burp lo lanza a Internet.

---

## ④ Módulos principales

### Proxy (corazón de Burp)

| Función | Descripción |
|---------|------------|
| **Intercept ON/OFF** | Parar/reanudar captura de peticiones |
| **Forward** | Dejar pasar la petición actual |
| **Drop** | Descartar la petición actual (no llega al servidor) |
| **HTTP History** | Historial de todas las peticiones (no solo para borrar: sirve para consultar) |

> [!important] Analogía: el portero de discoteca
> Las peticiones forman una **cola**. Con **Intercept ON** ninguna avanza hasta que decides: **Forward** = deja entrar · **Drop** = echa al de fuera.

### Configuración del certificado CA (HTTPS)

1. Con Burp abierto → `http://localhost:8080` (o `http://burpsuite/`) → **CA Certificate** → descargar `cacert.der`
2. Firefox → about:preferences → Certificados → Administrar certificados → Importar
3. Verificar pestaña **Autoridades**: debe aparecer **PortSwigger** como CA

> [!warning] Sin el certificado
> Chrome/Firefox detectan el proxy "raro" y bloquean las conexiones HTTPS. Sin la CA de Burp instalada, no puedes interceptar HTTPS.

### Repeater

Reenvía y repite una misma petición modificándola. Ideal para "conocer" la web.

| Acción en Repeater | Ejemplo |
|-------------------|---------|
| Modificar parámetros | `admin` → `' OR 1=1 --` |
| Cambiar método | GET → POST, añadir cabeceras |
| Probar inyecciones | SQLi, XSS, Command Injection |
| Analizar respuestas | Ver qué devuelve el servidor ante cada cambio |

> [!tip] Forward vs Repeater
> **Forward**: la petición sigue su flujo normal (no interesa). **Repeater**: la guardas para reenviarla modificada (análisis en profundidad).

### Intruder (fuerza bruta / fuzzing)

| Tipo de ataque | Comportamiento |
|---------------|----------------|
| **Sniper** | Un payload por posición, una a una |
| **Battering ram** | Mismo payload en todas las posiciones |
| **Pitchfork** | Una lista por posición, en paralelo |
| **Cluster bomb** | Todas las combinaciones posibles |

> [!warning] BUENA PRÁCTICA
> Marca y fuzzea los parámetros **de uno en uno**. Cada parámetro controla algo distinto en el back.

> [!warning] VERSIÓN COMMUNITY
> En la gratuita el Intruder está **throttled** (limitado en velocidad). Para WordPress usa [[WPScan]].

### Otros módulos

| Módulo | Para qué |
|--------|---------|
| **Decoder** | Codificar/decodificar (URL-encode, Base64) |
| **Comparer** | Comparar valores (cookies, respuestas) — buscar patrones en generación de cookies |
| **Sequencer** | Analizar secuencias de peticiones |
| **Target/Scope** | Filtrar tráfico por dominio objetivo (quita ruido de analytics, redes sociales, heartbeats) |
| **Logger** | Registrar peticiones (ataques autenticados) |
| **Collaborator** | Detección de interacciones fuera de banda (Pro) |

> [!warning] El ruido es tu enemigo
> Pestañas de redes sociales, anuncios dinámicos y scripts de terceros generan tráfico constante. Trabajar en el navegador personal para pentesting es como intentar **concentrarse en una conversación importante en medio de una discoteca**. Usa Open Browser o un navegador limpio.

---

## ⑤ Sesiones y cookies

| Concepto | Descripción |
|---------|------------|
| **ID de sesión** | Cookie que identifica al usuario ante múltiples sesiones simultáneas |
| **Session hijacking** | Iterar el ID para colarse en la sesión de otro (histórico, hoy difícil por tokens) |
| **Robo de cookie** | Mantener acceso sin usuario/contraseña/2FA mientras viva la cookie (XSS almacenado, phishing 2FA) |
| **Hard reset** | Ctrl+Shift+R borra caché → nuevo ID de sesión |
| **Comparer en cookies** | Buscar patrones en cómo se generan los IDs (no existe aleatoriedad pura) |

> [!warning] Cookies de sesión son sensibles
> Si se roba una cookie válida, se mantiene acceso sin credenciales ni 2FA durante su tiempo de vida. Solo aplicable en laboratorios/auditorías autorizadas.

---

## ⑥ Práctica típica: interceptar un login

```
1. Proxy → Open Browser (o FoxyProxy activo)
2. Navegar al objetivo → Intercept ON
3. Hacer login → Burp captura la petición
4. Identificar: parámetros, cookies, headers, tokens
5. Clic derecho → Send to Repeater
6. Modificar parámetros → Send → analizar respuesta
```

> [!info] Incluso sin hacer nada malicioso
> Simplemente interceptando el tráfico de una web "normal" se expone información que no debería ser visible: cookies, public keys, IDs de tienda, configuración interna.

---

## ⑦ Conexión con otras áreas

| Área | Cómo usa Burp |
|------|--------------|
| [[Apuntes/05 - Auditoria Web/Enumeración Web]] | Inspeccionar peticiones, cabeceras |
| [[Fuzzing Web con ffuf]] | Alternativa al Intruder |
| [[WordPress - Auditoría con WPScan]] | Analizar login de WordPress |
| [[OWASP Top 10 - CVE CVSS CWE]] | Framework de referencia |
| [[Prácticas CTF - HTB y VulnHub]] | Herramienta diaria en CTFs |

---

## Checklist de repaso

- [ ] ¿Defino Burp como framework y no solo como proxy?
- [ ] ¿Entiendo front vs back y dónde tengo el control?
- [ ] ¿Sé instalar el certificado CA y configurar FoxyProxy?
- [ ] ¿Distingo los 4 tipos de ataque del Intruder?
- [ ] ¿Sé para qué sirven Repeater, Decoder, Comparer?
- [ ] ¿Distingo Forward, Drop y Send to Repeater?
- [ ] ¿Sé por qué el ruido del navegador personal arruina una auditoría?
- [ ] ¿Conozco HTTP History y Target/Scope para filtrar tráfico?

---

## Enlaces relacionados

- [[comandos/BurpSuite]] "” Cheat sheet de comandos
- [[../../apuntes Chema/Sesión 30 - Burp Suite y WordPress.md|Sesión 30 - Burp Suite y WordPress]] — Módulos, certificado CA, WordPress
- [[../../apuntes Chema/Burp Suite a fondo · Auditoría web · WordPress.md|Burp Suite a fondo · Auditoría web · WordPress]] — Framework, Proxy, Intruder
- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — Proxy, Repeater, FoxyProxy
- [[../05 - Auditoria Web/Vulnerabilidades Web - OWASP Top 10 y Burp Suite.md|Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] — Proxy man-in-the-middle, Intercept










---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../07 - Empleabilidad/Portafolio y Visibilidad.md|Portafolio y Visibilidad]] — Esteganografia, Hack The Box, Seguridad
- [[../04 - OSINT y Recopilacion/Esteganografía y Metadatos.md|Esteganografía y Metadatos]] — Desarrollo Web, Esteganografia, Hack The Box
- [[../07 - Empleabilidad/Mercado Laboral y Certificaciones.md|Mercado Laboral y Certificaciones]] — Esteganografia, Hack The Box, Seguridad
- [[../../comandos/Google_Dorks.md|Google_Dorks]] — Desarrollo Web, Seguridad, WPScan
- [[../../comandos/WPScan.md|WPScan]] — Desarrollo Web, WPScan, WordPress
- [[../../apuntes Chema/Sesión 30 - Burp Suite y WordPress.md|Sesión 30 - Burp Suite y WordPress]] — Burp Suite, WordPress, WPScan
- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — Proxy, Repeater, OWASP

### 🌐 Cross-Dominio

- [[../../../cloud/azure_nsg.md|azure_nsg]] — Cloud: Desarrollo Web, Redes, Seguridad
- [[../../../cloud/azure_blob.md|azure_blob]] — Cloud: Desarrollo Web, Redes, Seguridad

> #burpsuite #cloud_base #empleabilidad #esteganografia #ffuf #hack_the_box #hydra #osint #proxy #redes #redes_ciber #repeater #intruder #seguridad #vulnhub #web #wordpress #wpscan
