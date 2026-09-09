

> **Relacionado:** [[Normativa - ISO 27001, GDPR, ENS]] · [[Mercado Laboral y Certificaciones]] · [[Portafolio y Visibilidad]]
>

---

## Examen ISO 27001

### Qué evalúa

El examen **no evalúa capacidad de "hackear"**: evalúa si comprendes la estructura de la norma, el vocabulario de gestión de riesgos, y si eres capaz de aplicar ese conocimiento a situaciones prácticas de gestión.

> **Error más habitual:** Abordar este examen como si fuera técnico. La clave es saber **clasificar, ubicar y razonar sobre procesos de gestión**.

### Formato

| Característica | Detalle |
|----------------|---------|
| **Tipo** | Test de opción múltiple |
| **Duración** | 40-90 minutos según proveedor |
| **Nota de corte** | ~65-70% |
| **Distribución** | Terminología, cláusulas, Anexo A, gestión de riesgos, certificación |

### Contenidos por peso

| Prioridad | Contenido |
|-----------|-----------|
| **1** | Terminología ISO 27000 (activo, amenaza, vulnerabilidad, riesgo, CIA) |
| **2** | Estructura de cláusulas 4-10 |
| **3** | Anexo A: 4 categorías (A.5/A.6/A.7/A.8) |
| **4** | Gestión de riesgos: 4 estrategias de tratamiento |
| **5** | Proceso de certificación |
| **6** | Documentación obligatoria del SGSI |

### Plan de estudio (2 semanas)

**Semana 1 — Teoría:**
- Días 1-2: Cláusulas 4-10, tabla resumen
- Días 3-4: Anexo A por categorías, 3-4 controles representativos por categoría
- Días 5-7: Gestión de riesgos y terminología

**Semana 2 — Práctica:**
- Días 8-10: Baterías de preguntas tipo test
- Días 11-12: Repasar áreas débiles
- Día 13: Simulacro completo cronometrado
- Día 14: Descanso activo, solo chuleta de una página

### Preguntas de práctica

**P1:** ¿Qué cláusula exige la revisión por la dirección? → Cláusula 9
**P2:** ¿Cifrado de datos en reposo pertenece a? → A.8 Tecnológicos
**P3:** ¿Riesgo residual alto pero mitigation costosa? → Aceptar
**P4:** ¿Documento que justifica qué controles aplica? → SoA
**P5:** ¿Política nunca revisada por dirección? → No conformidad mayor
**P6:** ¿Diferencia riesgo inherente vs residual? → Inherente antes de controles, residual después
**P7:** ¿Qué ciclo subyace a ISO 27001? → PDCA

---

## Examen eJPTv2

### Qué evalúa

Examen **100% práctico**: acceso a red de laboratorio real con máquinas Windows y Linux, y cuestionario cuya respuesta solo se obtiene enumerando y explotando.

> **Diferencia con ISO 27001:** Aquí no sirve memorizar. Hacen falta horas de práctica real con las manos en el teclado.

### Formato

| Característica | Detalle |
|----------------|---------|
| **Duración** | Varios días de acceso al laboratorio |
| **Formato** | Opción múltiple o respuesta corta |
| **Acceso** | VPN a red de laboratorio aislada |
| **Nota de corte** | ~70-75% |
| **Informe** | No se exige informe formal |

### Contenidos por módulo

| Módulo | Temas clave |
|--------|-------------|
| **1. Information Gathering** | OSINT, Google Dorks, Shodan/Censys |
| **2. Scanning** | Nmap (todos los tipos), interpretación de puertos |
| **3. Vulnerability Assessment** | Nessus/OpenVAS |
| **4. Host & Network Pentest** | SMB, FTP, SSH, HTTP y sus vectores |
| **5. Explotación con Metasploit** | msfconsole, msfvenom, Meterpreter |
| **6. Post-Exploitation** | Escalada Linux/Windows, pivoting |
| **7. Web Application Pentest** | OWASP Top 10, SQLMap, fuzzing |

### Checklist de comandos esenciales

```bash
# Reconocimiento
nmap -sn 10.10.10.0/24
nmap -p- -sV -oN scan.txt <IP>

# Enumeración
smbclient -L //<IP>/ -N
enum4linux -a <IP>
showmount -e <IP>

# Explotación
msfconsole
search <servicio>
use exploit/ruta
set RHOSTS <IP>
run

# Post-explotación
sysinfo; getuid; hashdump
run post/multi/recon/local_exploit_suggester

# Web
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
sqlmap -u "http://<IP>/page.php?id=1" --dbs
```

### Metodología de examen

1. **Primeros 20-30 min:** escaneo completo de TODA la red (`nmap -p- -sV`)
2. **Responder preguntas de reconocimiento** primero (puntos rápidos y seguros)
3. **Priorizar máquinas** con vulnerabilidades más evidentes
4. **Probar credenciales** encontradas en otros servicios inmediatamente
5. **Documentar sobre la marcha** (usuario, contraseña, hash, flag)

### Plan de práctica (4 semanas)

| Semana | Actividad |
|--------|-----------|
| **1-2** | 8-10 máquinas Easy con write-ups, luego repetir sin apoyo |
| **3** | 5-6 máquinas nuevas sin write-up, cronometrado |
| **4** | Simulacro: 3-4 máquinas variadas en sesión continua |

### Recursos de práctica

| Recurso | Nota |
|---------|------|
| **TryHackMe** — ruta "Jr Penetration Tester" | Progresión guiada alineada con eJPT |
| **Hack The Box** — máquinas Easy/Medium | Especialmente las retiradas |
| **Laboratorios INE** | Los más representativos del formato de examen |
| **Walkthroughs del máster** | Repetir sin mirar solución |

### Errores frecuentes

| Error | Consecuencia |
|-------|-------------|
| No guardar resultados de Nmap (`-oN`) | Hay que re-escanear |
| No usar `-p-` completo | Se pierden servicios en puertos altos |
| No probar credenciales reutilizadas | Se pierden puntos fáciles |
| Explotar antes de leer la pregunta | Muchas no requieren explotación completa |
| No documentar sobre la marcha | Hay que repetir pasos |

---

## Checklist de repaso

### ISO 27001
- [ ] Sé qué evalúa el examen (gestión, no hacking)
- [ ] Conozco el formato (test, 65-70% corte)
- [ ] Estudio terminología, cláusulas, Anexo A, gestión de riesgos
- [ ] Practico con baterías de preguntas tipo test
- [ ] Leo cada pregunta dos veces (negaciones se pasan por alto)

### eJPTv2
- [ ] Sé qué evalúa (100% práctico, máquinas reales)
- [ ] Conozco el formato (VPN, cuestionario, 70-75% corte)
- [ ] Domino los comandos esenciales de memoria
- [ ] Aplico la metodología: escaneo completo primero, exploits después
- [ ] Documento todo sobre la marcha
- [ ] No me atasco en una máquina, maximizo preguntas correctas

---

> **Volver al:** [[MOC - Ciberseguridad]]



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Linux, Nmap, OSINT
- [[../../transcripciones/Junio/02.06.2026 Introducción a HackTheBox Starting Point Tier0.md|02.06.2026 Introducción a HackTheBox Starting Point Tier0]] — Linux, Nmap, OSINT
- [[../12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Linux, Nmap, OSINT
- [[../../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — Empleabilidad, Nmap, OSINT
- [[../../apuntes Joselu/PREWORK/resumen_clase16.md|resumen_clase16]] — Linux, Nmap, OSINT
- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point — Tier 0.md|Hack The Box- Starting Point — Tier 0]] — Linux, Nmap, OSINT

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #certificaciones #empleabilidad #google-dorks #hack-the-box #linux #metasploit #nmap #normativa #osint #pentest #pivoting #redes #sqli #sqlmap #ssh #windows
