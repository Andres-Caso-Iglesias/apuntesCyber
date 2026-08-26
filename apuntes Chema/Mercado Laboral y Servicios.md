# â‘  Nota sobre Metasploit

> â†’

| | |
|---|---|
|**âš  AVISO**|Cuanto menos Metasploit, mejor. En OSCP y eCPPT estÃ¡ prohibido o muy limitado. Si aprendes con Ã©l, cuando te lo quiten no sabes quÃ© pasa por debajo.|

| | |
|---|---|
|**âœ—Â  Evitar en general**<br><br>Reemplazar con herramientas especÃ­ficas: scripts Python, Nmap, Hydra, NetExec. AsÃ­ se entiende el protocolo subyacente.|**âœ“Â  ExcepciÃ³n: eJPT + pivoting**<br><br>En el eJPT no hay restricciones. En escenarios de pivoting (saltar entre redes) Metasploit centraliza las sesiones de forma prÃ¡ctica.|

| | |
|---|---|
|**ðŸ’¡ CLAVE**|Si aprendes SIN Metasploit â†’ se convierte en una comodidad opcional. Si aprendes CON Ã©l â†’ se vuelve un requisito del que no puedes prescindir.|

# â‘¡ Mercado laboral en seguridad ofensiva

Mapa de servicios de un equipo de seguridad ofensiva, ordenados por nivel de entrada.

## Perfil junior â€” foco del mÃ¡ster

|**Nivel**|**Servicio**|**DescripciÃ³n**|
|---|---|---|
|**Junior â˜…â˜…â˜…**|**AuditorÃ­as web dinÃ¡micas**|El mayor foco de entrada. Apps web en ejecuciÃ³n, WordPress/WPScan, vulnerabilidades comunes. Es lo mÃ¡s demandado en perfiles junior.|
|**Junior â˜…â˜…â˜…**|**APIs y web services**|Similar a web dinÃ¡mica, se trabaja con Burp Suite. Hay que conocer la diferencia entre REST y SOAP, pero el proceso de ataque es anÃ¡logo.|
|**Junior â˜…â˜…**|**AuditorÃ­as externas**|Simular atacante sin info previa. OSINT, enumeraciÃ³n de perÃ­metro, bÃºsqueda de servicios vulnerables. Caja negra. Objetivo: acceso inicial al servidor.|
|**Junior â˜…â˜…**|**Vulnerability Management**|EscÃ¡neres: Nessus, OpenVAS, Qualys. VerificaciÃ³n de falsos positivos y comprobaciÃ³n manual. Rutinario pero habitual en equipos con poco personal.|
|**Junior â˜…**|**AuditorÃ­as WiFi**|Redes WPA2-PSK domÃ©sticas y redes Enterprise corporativas. Incluido en el mÃ¡ster.|

## Perfil avanzado / senior

|**Nivel**|**Servicio**|**DescripciÃ³n**|
|---|---|---|
|**Medio-senior**|**AuditorÃ­as internas / AD**|Infraestructura Windows interna. Kerberos, Pass-the-Hash, movimiento lateral. El mÃ¡ster lo toca pero no es el primer trabajo junior.|
|**Senior**|**Red Team**|Ejercicios de 4-5 meses simulando un APT real. FÃ­sico, ingenierÃ­a social, externa, interna y pivoting correlacionados. Requiere perfiles senior.|
|**Especialidad**|**Cloud (AWS/Azure/GCP)**|Mundo propio, hiper especializado. Queda fuera del mÃ¡ster.|
|**Medio**|**IngenierÃ­a social**|Phishing con GoPhish, vishing (llamadas), baiting con USBs. El phishing sÃ­ entra en el mÃ¡ster.|
|**Especialidad**|**IoT y OT/ICS**|Dispositivos embebidos, PLCs, infraestructuras industriales. Especializaciones independientes.|

| | |
|---|---|
|**â„¹ NOTA**|Caja negra / gris / blanca: la distinciÃ³n no siempre implica diferencia de dificultad o precio. Depende de cuÃ¡nta informaciÃ³n facilita el cliente. Lo habitual es moverse entre caja negra y caja gris.|

**Especializaciones avanzadas (referencia cultural):** Car hacking Â· 5G / telcos Â· Guerra electrÃ³nica Â· ATMs Â· AuditorÃ­as de LLMs/IA Â· Pipelines CI/CD Â· Docker Â· OT/ICS industrial

# â‘¢ Marco mental: 4 elementos para atacar servicios

Aplicable a cualquier vulnerabilidad de servicio, independientemente del protocolo (FTP, SMB, SSH, HTTP...).

| | | | |
|---|---|---|---|
|**01**<br><br>**FUENTE**<br><br>Origen de la info que dispara la vulnerabilidad: entrada de usuario, cabecera HTTP, fichero de config, librerÃ­a...|**02**<br><br>**PROCESO**<br><br>QuÃ© hace el servicio con esa informaciÃ³n. AquÃ­ ocurre la mayorÃ­a de las vulnerabilidades.|**03**<br><br>**PRIVILEGIOS**<br><br>Con quÃ© permisos corre el proceso. Un mismo fallo puede ser trivial o crÃ­tico segÃºn si es user o root.|**04**<br><br>**DESTINO**<br><br>QuÃ© se hace con el resultado. A dÃ³nde llega la informaciÃ³n procesada.|

## Ejemplo aplicado: Log4Shell (CVE-2021-44228)

| | |
|---|---|
|**01 FUENTE**|Cabecera User-Agent manipulada por el atacante con un payload JNDI malicioso.|
|**02 PROCESO**|Log4j interpreta y ejecuta la cadena en lugar de solo registrarla.|
|**03 PRIVILEGIOS**|Si el proceso de logging corre con permisos elevados, el comando ejecutado hereda esos permisos.|
|**04 DESTINO**|RCE (Remote Code Execution) en la mÃ¡quina vÃ­ctima.|

| | |
|---|---|
|**âœ“ RECUERDA**|Las vulnerabilidades suelen venir de malas configuraciones, no de zero-days: credenciales por defecto, autenticaciÃ³n anÃ³nima habilitada, permisos excesivos.|

# â‘£ MetodologÃ­a: orden antes que velocidad

## Estructura de carpetas â€” primer paso siempre

| |
|---|
|mkdir metasploitable2<br><br>cd metasploitable2<br><br>mkdir recon<br><br>mkdir exploits|

## Nmap en tres fases

| | | | | |
|---|---|---|---|---|
|**1. Escaneo rÃ¡pido (top 1000)**|â†’|**2. Todos los puertos (-p-)**|â†’|**3. Scripts sobre puertos hallados**|

**Fase 1 â€”** escaneo bÃ¡sico rÃ¡pido:

| |
|---|
|nmap -oN recon/initial.txt <IP>|

**Fase 2 â€”** todos los puertos:

| |
|---|
|nmap -p- -oN recon/allports.txt <IP>|

**Fase 3 â€”** scripts y versiones sobre puertos abiertos:

| |
|---|
|nmap -sC --script default,vuln -sV -Pn -p <PUERTOS> -oA recon/full <IP>|

â€¢Â Â Â Â  **-oA:** guarda en los 3 formatos: normal, grepeable y XML.

â€¢Â Â Â Â  **-Pn:** omite el host discovery (Ãºtil si no hay respuesta a ping).

â€¢Â Â Â Â  **-sC:** equivale a --script=default. Lanza scripts de la categorÃ­a default.

â€¢Â Â Â Â  **vuln:** scripts especÃ­ficos de CVEs. MÃ¡s intrusiva y lenta, pero puede revelar vulnerabilidades directamente. Usar con cautela en auditorÃ­as reales.

## Tmux â€” trabajo en paralelo

| | |
|---|---|
|Ctrl+B â†’ "Â Â  dividir horizontal|Ctrl+B â†’ %Â Â  dividir vertical|
|Ctrl+B â†’ â†‘â†“â†â†’Â Â  moverse entre paneles|Ctrl+B :source-file ~/.tmux.confÂ Â  recargar config|

**Activar ratÃ³n:**

| |
|---|
|echo "set -g mouse on" >> ~/.tmux.conf|

| | |
|---|---|
|**ðŸ“– HackTricks**|Para cada servicio/protocolo consulta book.hacktricks.xyz/<servicio>. Cada pÃ¡gina incluye comandos de enumeraciÃ³n, ataques tÃ­picos y recursos.|

# â‘¤ FTP â€” flujo de ataque

| | | | | | | |
|---|---|---|---|---|---|---|
|**Identificar versiÃ³n (Nmap)**|â†’|**searchsploit**|â†’|**Descargar exploit (-m)**|â†’|**Ejecutar â†’ shell**|

## BÃºsqueda y descarga del exploit

**Buscar exploits para la versiÃ³n detectada:**

| |
|---|
|searchsploit vsftpd 2.3.4|

**Descargar con flag -m (mirror):**

| |
|---|
|searchsploit -m unix/remote/49757.py|

**Ejecutar:**

| |
|---|
|python3 49757.py -h <IP_OBJETIVO>|

| | |
|---|---|
|**â„¹ NOTA**|Si la conexiÃ³n se rechaza en el primer intento, relanzar. Las mÃ¡quinas de laboratorio pueden tener estados intermedios.|

## AutenticaciÃ³n anÃ³nima

| |
|---|
|ftp <IP><br><br># usuario: anonymous | contraseÃ±a: cualquiera|

Si estÃ¡ habilitada, da acceso sin credenciales vÃ¡lidas. Siempre verificar.

| | |
|---|---|
|**âœ“ OBJETIVO**|FTP: versiÃ³n â†’ searchsploit â†’ descargar exploit â†’ ejecutar â†’ obtener shell.|

# â‘¥ SMB / Samba â€” enumeraciÃ³n y acceso

SMB expone carpetas compartidas (shares) en red. La enumeraciÃ³n combina varias herramientas complementarias.

## Listar shares â€” smbclient (sesiÃ³n nula)

| |
|---|
|smbclient -N -L //<IP>|

## Ver permisos de lectura/escritura â€” NetExec

| |
|---|
|netexec smb <IP> -u '' -p '' --shares|

Muestra quÃ© carpetas permiten leer, escribir o ninguna de las dos. Las carpetas con escritura permiten subir ficheros.

## Conectarse a un share concreto

| |
|---|
|smbclient //<IP>/tmp -N<br><br>lsÂ Â Â Â Â Â Â Â Â Â Â Â Â  # listar<br><br>get <fichero>Â Â  # descargar<br><br>put <fichero>Â Â  # subir|

## EnumeraciÃ³n completa â€” enum4linux

| |
|---|
|enum4linux <IP>|

Extrae: nombre de dominio, versiÃ³n Samba, **usuarios del sistema**, shares y polÃ­ticas de contraseÃ±a. Los usuarios son valiosos para ataques posteriores de fuerza bruta.

## Password Spraying â€” NetExec

| |
|---|
|netexec smb <IP> -u usuarios.txt -p 'admin' --continue-on-success|

Prueba una sola contraseÃ±a contra todos los usuarios de la lista. Especialmente Ãºtil en Active Directory para evitar bloqueos de cuenta (no es fuerza bruta clÃ¡sica).

| | |
|---|---|
|**âš  CONTEXTO**|SMB/Samba es uno de los protocolos mÃ¡s utilizados en entornos corporativos (junto con LDAP) y uno de los mÃ¡s explotados. Eternal Blue (MS-17-010) es el ejemplo mÃ¡s conocido.|

| | |
|---|---|
|**âœ“ OBJETIVO**|SMB: listar shares â†’ ver permisos â†’ conectarse â†’ enum4linux (usuarios) â†’ password spraying si hay credenciales.|

â†’

â†’

â†’

â†’
â†’

