# Linux — Comandos Esenciales

> Comandos del sistema para pentesting y administración.

---

## Navegación

```bash
pwd                              # Directorio actual
ls -la                           # Listar archivos (detallado)
cd <dir>                         # Cambiar directorio
find / -name <file> 2>/dev/null  # Buscar archivo
find / -perm -u=s -type f 2>/dev/null  # SUID files
```

## Archivos

```bash
cat <file>                       # Ver contenido
head -n 20 <file>                # Primeras 20 líneas
tail -n 20 <file>                # Últimas 20 líneas
less <file>                      # Visor paginado
cp <src> <dst>                   # Copiar
mv <src> <dst>                   # Mover/renombrar
rm <file>                        # Eliminar
mkdir <dir>                      # Crear directorio
chmod 777 <file>                 # Cambiar permisos
chown user:group <file>          # Cambiar propietario
```

## Búsqueda

```bash
grep -r "pattern" /path          # Buscar en archivos
grep -r "password" /etc/ 2>/dev/null
find / -name "*.conf" 2>/dev/null
find / -writable -type f 2>/dev/null
locate <file>                    # Buscar con locate
```

## Procesos

```bash
ps aux                           # Procesos activos
ps aux | grep <process>
top                              # Monitoreo en tiempo real
kill <pid>                       # Matar proceso
killall <name>                   # Matar por nombre
bg / fg                          # Background/Foreground
```

## Red

```bash
ifconfig / ip a                  # Interfaces de red
ip route                         # Tabla de rutas
netstat -tuln                    # Puertos abiertos
ss -tuln                         # Alternativa a netstat
ping <host>                      # ICMP ping
traceroute <host>                # Ruta
nslookup <domain>                # DNS lookup
dig <domain>                     # DNS completo
```

## Transferencia de archivos

```bash
wget <url>                       # Descargar
curl -o <file> <url>             # Descargar
python3 -m http.server 8000      # Servidor HTTP
scp <file> user@host:<path>      # Copiar por SSH
```

## Compresión

```bash
tar -cvf archive.tar <dir>       # Crear tar
tar -xvf archive.tar             # Extraer tar
tar -cvzf archive.tar.gz <dir>   # Crear gzip
tar -xvzf archive.tar.gz         # Extraar gzip
zip -r archive.zip <dir>         # Crear zip
unzip archive.zip                # Extraer zip
```

## Usuarios

```bash
whoami                           # Usuario actual
id                               # UID, GID, grupos
su - <user>                      # Cambiar usuario
sudo <cmd>                       # Ejecutar como root
useradd -ou 0 -g 0 backdoor     # Crear usuario root
echo "user:pass" | chpasswd      # Cambiar contraseña
cat /etc/passwd                  # Usuarios del sistema
cat /etc/shadow                  # Shadows (root)
```

## Permisos

```bash
chmod +x <file>                  # Ejecutable
chmod 600 <file>                 # Solo propietario
chmod 644 <file>                 # Lectura pública
chmod 777 <file>                 # Total (inseguro)
chown user:group <file>          # Cambiar propietario
```



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Tmux.md|Tmux]] — Linux, Tmux, Windows
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Tmux, Windows
- [[../../comandos/Windows.md|Windows]] — Linux, Tmux, Windows
- [[../08 - Metodologías/Metodología - Active Directory.md|Metodología - Active Directory]] — Linux, Redes, Tmux
- [[Windows.md|Windows]] — Metodología Pentest, Redes, Tmux
- [[Hydra.md|Hydra]] — Linux, Redes, Windows

### 🛠️ Herramientas

- [[comandos/SSH|SSH]]
- [[comandos/Tmux|Tmux]]

> #linux #pentest #redes #ssh #tmux #windows
