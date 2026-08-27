> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 01 — Fundamentos y contexto
> **Contenido:** Historia del sector, roles, ética, tipos de hacker, normativa introductoria, mercado laboral y certificaciones

> [!tip] Cómo leer estos apuntes
> Este bloque sienta las bases del máster: historia de la ciberseguridad desde los años 60 hasta hoy, las tres líneas de defensa (Red/Blue/Purple Team), tipos de auditoría, ética profesional y panorama laboral con certificaciones.

---

## ① Historia y evolución de la ciberseguridad

La ciberseguridad nace ligada a la propia historia de la informática.

### Años 60 — Los orígenes

- Los primeros sistemas como **Multics** no tenían preocupaciones de seguridad externa porque los ordenadores no estaban conectados globalmente, sino mediante intranets físicas.
- Los primeros "hackers" eran investigadores universitarios (MIT) que exploraban los límites del hardware y software por pura curiosidad técnica, sin intención maliciosa.

### 1971 — Creeper, el primer malware

- **Creeper**: primer malware conocido, diseñado para moverse entre sistemas conectados por ARPANET (precursor de Internet).
- Comportamiento: infectaba un sistema → mostraba "Soy Creeper, ¡atrapadme si podéis!" → saltaba al siguiente equipo.
- Introduce un concepto que seguimos usando hoy: el **movimiento lateral**.
- Su aparición motivó la creación del primer antivirus: **Reaper**, diseñado específicamente para eliminarlo.
- > [!fun-fact] Curiosidad
 > El enemigo del videojuego Minecraft llamado "Creeper" toma su nombre de este primer virus.

### Años 80 — Expansión a usuarios domésticos

- Llegada de ordenadores personales (Apple II) y expansión de redes.
- **Cloner (1982)**: uno de los primeros virus en infectar PCs personales.
- **Gusano de Morris (1988)**: primer gusano de Internet, infectó miles de equipos en ARPANET.
- Disparó la creación de las primeras empresas comerciales de antivirus (McAfee, Norton).

### Desde los 90 hasta hoy

| Década | Evento clave | Impacto |
|--------|-------------|---------|
| 90s | Ingeniería social (primeros phishing) | Usuarios no desconfiaban de correos extraños |
| 2000s | Botnets IoT (Mirai) | Colapsaron redes enteras con dispositivos domésticos |
| 2010s | Stuxnet | Sabotaje industrial — guerra física → guerra digital |
| 2010s | Hacktivism (Anonymous) | Ataques con fines políticos/sociales |
| 2017 | WannaCry | Ransomware apoyado en EternalBlue (filtrado de la NSA) |
| 2020 | COVID-19 | Aceleró digitalización, expuso configuraciones VPN mal hechas |

> [!important] Lección perpetua
> "Todo, absolutamente todo, puede ser atacado, desde un servidor hasta un termostato de un casino."

---

## ② Líneas de la ciberseguridad: Red, Blue y Purple Team

Las empresas organizan sus esfuerzos de seguridad en tres grandes equipos que colaboran en un ciclo continuo:

### 🔴 Red Team (seguridad ofensiva)

- Simulan ataques reales: auditorías, pruebas de penetración, simulaciones tipo APT.
- Identifican vulnerabilidades antes de que lo haga un atacante real.
- En el marco europeo **TIBER-EU**: ejercicios con brechas reales y situaciones de crisis (ej: despliegues de ransomware controlados) para el sector financiero.

### 🔵 Blue Team (seguridad defensiva)

- Protegen sistemas, monitorean la red 24/7 desde un SOC.
- Configuran arquitecturas seguras (Zero Trust, segmentación de red).
- Responden a incidentes.
- Se desarrolla en profundidad en el **Bloque 11**.

### 🟣 Purple Team

- Puente entre ambos: traduce lecciones del Red Team en mejoras defensivas para el Blue Team y viceversa.
- Incluye la disciplina **DFIR** (Digital Forensics and Incident Response): investiga incidentes reconstruyendo qué ocurrió, cómo, y recopilando evidencias para posibles acciones legales — "los CSI de la informática".
- También trabaja en **DevSecOps**: integra seguridad desde el diseño del software (detectar un fallo en desarrollo es mucho más barato que solucionarlo tras el lanzamiento).

### Otras líneas especializadas en auge

- **Car Hacking**: auditoría de vehículos conectados (CAN Bus, llaves electrónicas, sensores de presión).
- **Forense digital**.
- **Vigilancia digital**: monitoreo de foros y dark web.
- **Cloud Security**.

---

## ③ Tipos de auditoría

### Auditorías de redes internas

- Se simula que el atacante ya está dentro (contraseñas débiles, permisos excesivos).
- Ejemplo: verificar que contraseñas de empleados cumplen política mínima (12 caracteres, letras, números y símbolos).

### Auditorías de redes externas

- Enfoque **Black Box** desde fuera de la organización.
- Metodología en 4 fases: enumeración → explotación → post-explotación → reporte.
- Riesgos frecuentes: contraseñas débiles/reutilizadas, servicios desactualizados (SQL o FTP antiguos), subdominios olvidados de entornos de desarrollo, configuraciones de correo débiles (SPF/DKIM/DMARC).

### Auditorías de aplicaciones web

- Basadas en el **OWASP Top 10** (se detalla en el Bloque 4, con comandos).

### Auditorías de redes WiFi

- Cifrado, captura de handshake, DeAuth, Evil Twin (se detalla en el Bloque 9, con comandos).

### Auditorías de código, IoT, Cloud y bastionado

- Revisión de configuraciones, mínimo privilegio, segmentación de red.
- Cumplimiento de guías CCN-CERT.
- Monitoreo de logs (mínimo 3 años de retención según normativa española).

---

## ④ Tipos de hacker y ética profesional

Un hacker no es intrínsecamente un ciberdelincuente: es alguien con profundo conocimiento técnico capaz de explorar y modificar sistemas. Lo que le distingue es el **uso** que hace de ese conocimiento:

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Black Hat** | Actúa fuera de la ley con fines de lucro o daño | Grupos de ransomware como LockBit |
| **Gray Hat** | Accede sin permiso pero sin ánimo de dañar; detecta un fallo, avisa a la empresa, y a veces publica si no recibe respuesta | — |
| **White Hat** | Trabaja siempre dentro de la ley, con autorización explícita previa | El perfil que forma este máster |

**Hacktivismo** (Anonymous, WikiLeaks): usa el hacking para causas políticas o sociales mediante filtraciones, ataques DDoS o modificación de páginas web, sin ánimo de lucro.

> [!note] Recomendación de clase
> La serie **Mr. Robot** es una referencia realista sobre estos dilemas éticos — el creador contrató hackers reales para garantizar precisión técnica en cada escena.

### Los 4 pilares de la ética profesional

1. **Consentimiento y alcance firmado** antes de cualquier auditoría — nunca explorar sistemas fuera del contrato, aunque parezca sencillo o tentador.
2. **Evitar daños** — pruebas controladas; un escaneo agresivo mal calculado puede tumbar un servidor legacy y generar gastos reales de recuperación.
3. **Confidencialidad** — cifrado de la información recopilada y eliminación segura tras la auditoría; si se detectan datos bancarios, no se exploran más allá de lo estrictamente necesario.
4. **Transparencia** — documentar con precisión todo lo realizado y comunicar de inmediato cualquier vulnerabilidad crítica, antes de que un tercero pueda explotarla.

---

## ⑤ Mercado laboral y certificaciones

El sector afronta una escasez global de profesionales.

### Salarios de referencia

| Nivel | Salario |
|-------|---------|
| Junior 1 (con eJPT) | 24.500 - 28.000€ iniciales |
| Junior (pocos años) | ~30.000€ |
| Senior / Gestión | 55.000€+ |
| Dirección | 120.000€+ |

### Certificaciones destacadas por área

| Área | Certificación | Descripción |
|------|--------------|-------------|
| **Ofensivas** | OSCP | Pentesting general, examen práctico intensivo |
| | OSEP | Evasión y desarrollo de herramientas propias |
| | OSWE | Pentesting web |
| | OSWP | WiFi |
| **Defensivas** | GSEC (SANS) | Entrada |
| | GCFA (SANS) | Forense avanzado |
| | GCIH (SANS) | Respuesta a incidentes y threat hunting |
| **Cloud** | AWS Certified Security Specialist | — |
| | Google Professional Cloud Security Engineer | — |
| | Azure Security Engineer Associate | — |
| **Entrada** | eJPT (INE) | Certificación de referencia de este máster |
| **Web** | BSCP (Burp Suite) | Avala explotación de XSS y SQLi con Burp Suite |
| **Active Directory** | CRTP (Altered Security) | Retos avanzados de ataques a AD |

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../transcripciones/Junio/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]— Normativa / GRC, Post-Explotación, XSS
- [[../apuntes Joselu/PREWORK/resumen_clase3.md|resumen_clase3]— Normativa / GRC, Post-Explotación, Redes
- [[../apuntes Chema/Vulnerabilidades Web.md|Vulnerabilidades Web]— Post-Explotación, Redes, XSS
- [[../Apuntes/13 - Normativa y GRC/Normativa - ISO 27001, GDPR, ENS.md|Normativa - ISO 27001, GDPR, ENS]— Empleabilidad, Normativa / GRC, Redes
- [[../apuntes Joselu/PREWORK/resumen_clase11.md|resumen_clase11]— Normativa / GRC, Redes, Windows
- [[../apuntes Andres/24.07.2026 Repaso Semanal III.md|24.07.2026 Repaso Semanal III]— Post-Explotación, Redes, XSS

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #blue-team #burpsuite #certificaciones #empleabilidad #forense #normativa #pentest #post-explotacion #redes #sqli #wifi #windows #xss
