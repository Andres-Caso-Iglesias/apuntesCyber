

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
| **HTTP History** | Historial de todas las peticiones |

### Repeater

Reenvía y repite una misma petición modificándola. Ideal para "conocer" la web.

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
| **Comparer** | Comparar valores (cookies, respuestas) |
| **Sequencer** | Analizar secuencias de peticiones |
| **Target/Scope** | Filtrar tráfico por dominio objetivo |

---

## ⑤ Sesiones y cookies

| Concepto | Descripción |
|---------|------------|
| **ID de sesión** | Cookie que identifica al usuario |
| **Session hijacking** | Iterar el ID para colarse en la sesión de otro |
| **Robo de cookie** | Mantener acceso sin usuario/contraseña/2FA |

---

## ⑥ Conexión con otras áreas

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

---

## Enlaces relacionados

- [[comandos/BurpSuite]] "” Cheat sheet de comandos




---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/WPScan.md|WPScan]] — FFUF, Redes, WordPress
- [[../../comandos/BurpSuite.md|BurpSuite]] — FFUF, Redes, WordPress
- [[Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]] — Burp Suite, FFUF, Redes
- [[../comandos/WPScan.md|WPScan]] — Burp Suite, Redes, WordPress
- [[../../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 — Rockstar.md|Fuzzing de parámetros con x8 — Rockstar]] — Burp Suite, FFUF, Redes
- [[../08 - Metodologías/00 - Metodologías de Explotación.md|00 - Metodologías de Explotación]] — Redes, VulnHub, WordPress

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/WPScan|WPScan]]

> #burpsuite #ffuf #hack-the-box #hydra #redes #vulnhub #wordpress #wpscan
