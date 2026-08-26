

> [!info] Relacionado con
>

---

## â‘  Â¿QuÃ© es Burp Suite?

**Burp Suite** es un **framework de auditorÃ­a web**. El proxy es su nÃºcleo, pero es mucho mÃ¡s: Repeater, Intruder, Decoder, Comparer...

> [!warning] ERROR COMÃšN
> Decir que "Burp es un proxy" es **incompleto**. Es un framework; el proxy es su dependencia crÃ­tica.

---

## â‘¡ Front vs Back â€” DÃ³nde tenemos el control

```
FRONT (tu navegador) â€” TIENES EL CONTROL
 â†“
PROXY de Burp â€” intercepta (texto claro, antes de TLS)
 â†“
Modificas la peticiÃ³n â†’ saltas controles del front
 â†“
WAF â€” Ãºltima defensa antes del server
 â†“
BACK (servidor) â€” valida integridad (o explota)
```

> [!important] CONCLUSIÃ“N
> Si los controles de seguridad estÃ¡n **solo en el front**, son **bypasseables**. La defensa moderna securiza el **back** y aÃ±ade un **WAF**.

---

## â‘¢ ConfiguraciÃ³n

### Certificado de Burp

1. Con Burp abierto â†’ `http://localhost:8080` â†’ **CA Certificate** â†’ descargar
2. Firefox â†’ Administrar certificados â†’ Importar â†’ seleccionar cacert
3. Verificar: debe aparecer **PortSwigger** como CA

### Foxy Proxy

| Campo | Valor |
|-------|-------|
| Nombre | Burp Suite |
| Host | 127.0.0.1 |
| Puerto | **8080** |

> [!tip] FLUJO
> Burp levanta proxy en `127.0.0.1:8080` â†’ FoxyProxy reenvÃ­a el trÃ¡fico del navegador â†’ Burp lo lanza a Internet.

---

## â‘£ MÃ³dulos principales

### Proxy (corazÃ³n de Burp)

| FunciÃ³n | DescripciÃ³n |
|---------|------------|
| **Intercept ON/OFF** | Parar/reanudar captura de peticiones |
| **Forward** | Dejar pasar la peticiÃ³n actual |
| **HTTP History** | Historial de todas las peticiones |

### Repeater

ReenvÃ­a y repite una misma peticiÃ³n modificÃ¡ndola. Ideal para "conocer" la web.

### Intruder (fuerza bruta / fuzzing)

| Tipo de ataque | Comportamiento |
|---------------|----------------|
| **Sniper** | Un payload por posiciÃ³n, una a una |
| **Battering ram** | Mismo payload en todas las posiciones |
| **Pitchfork** | Una lista por posiciÃ³n, en paralelo |
| **Cluster bomb** | Todas las combinaciones posibles |

> [!warning] BUENA PRÃCTICA
> Marca y fuzzea los parÃ¡metros **de uno en uno**. Cada parÃ¡metro controla algo distinto en el back.

> [!warning] VERSIÃ“N COMMUNITY
> En la gratuita el Intruder estÃ¡ **throttled** (limitado en velocidad). Para WordPress usa [[WPScan]].

### Otros mÃ³dulos

| MÃ³dulo | Para quÃ© |
|--------|---------|
| **Decoder** | Codificar/decodificar (URL-encode, Base64) |
| **Comparer** | Comparar valores (cookies, respuestas) |
| **Sequencer** | Analizar secuencias de peticiones |
| **Target/Scope** | Filtrar trÃ¡fico por dominio objetivo |

---

## â‘¤ Sesiones y cookies

| Concepto | DescripciÃ³n |
|---------|------------|
| **ID de sesiÃ³n** | Cookie que identifica al usuario |
| **Session hijacking** | Iterar el ID para colarse en la sesiÃ³n de otro |
| **Robo de cookie** | Mantener acceso sin usuario/contraseÃ±a/2FA |

---

## â‘¥ ConexiÃ³n con otras Ã¡reas

| Ãrea | CÃ³mo usa Burp |
|------|--------------|
| [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web]] | Inspeccionar peticiones, cabeceras |
| [[Fuzzing Web con ffuf]] | Alternativa al Intruder |
| [[WordPress - AuditorÃ­a con WPScan]] | Analizar login de WordPress |
| [[OWASP Top 10 - CVE CVSS CWE]] | Framework de referencia |
| [[PrÃ¡cticas CTF - HTB y VulnHub]] | Herramienta diaria en CTFs |

---

## Checklist de repaso

- [ ] Â¿Defino Burp como framework y no solo como proxy?
- [ ] Â¿Entiendo front vs back y dÃ³nde tengo el control?
- [ ] Â¿SÃ© instalar el certificado CA y configurar FoxyProxy?
- [ ] Â¿Distingo los 4 tipos de ataque del Intruder?
- [ ] Â¿SÃ© para quÃ© sirven Repeater, Decoder, Comparer?

---

## Enlaces relacionados

- [[comandos/BurpSuite]] â€” Cheat sheet de comandos

â†’

â†’

â†’
