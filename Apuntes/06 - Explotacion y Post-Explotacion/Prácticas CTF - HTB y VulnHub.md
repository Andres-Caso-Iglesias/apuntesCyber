

> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]]
> 

---

## ① Flujo general de un CTF

```
Superficie expuesta → Enumeración → Explotación → Shell → Enumerar dentro → Escalada → Root
```

---

## ② RickdiculouslyEasy (VulnHub)

### Cadena completa

```
www-data (RCE web) → summer (SSH:22222) → Robo de ficheros → [[Hydra]] → RickSanchez → sudo su → root
```

### Fase externa

| Puerto | Servicio | Hallazgo |
|--------|---------|---------|
| 21 | FTP anon | Login anónimo, flag.txt |
| 80 | Web | Command Injection en cgi-bin |
| 60000 | TCP | Backdoor con shell vía nc |
| 22222 | SSH real | El SSH auténtico |

### Escalada

1. **Summer → SSH** con contraseña `winter` (encontrada en passwords.html)
2. **Robo de ficheros** entre usuarios (binario safe, imagen con contraseña)
3. **[[Hydra]]** → RickSanchez: `P7Curtains`
4. **sudo su** → root (RickSanchez tiene `(ALL : ALL) ALL`)

---

## ③ Mr. Robot (VulnHub)

### Cadena completa (clase 16.06 — ver [[Son ROBOTS - RickdiculouslyEasy y Mr. Robot|detalle completo]])

```
Nmap (80/443) → robots.txt → fsocity.dic → sort | uniq (~11K) → WP login: elliot (Intruder, length + cookie WP) → editor 404.php → reverse shell → daemon → password.raw-md5 (CrackStation) → diccionario a-z → robot → SUID nmap --interactive → !sh → root
```

### Técnicas clave

- **robots.txt** → diccionario de ~858K líneas → limpiar con `sort | uniq` → ~11K
- **Enumeración por longitud de respuesta** en Intruder de Burp (cookie WP distinta en login OK)
- **Information disclosure** en login de WordPress (invalid username vs invalid password)
- **File upload 3 vías**: WP File Manager / editor de temas / editor 404.php
- **Lateral**: hash MD5 → CrackStation → diccionario contextual (`abcdefghijklmnopqrstuvwxyz`)
- **Escalada**: SUID `nmap --interactive` → `!sh` → root

---

## ④ Oopsie (HTB Starting Point)

### Cadena completa

```
[[Nmap]] → web + Ctrl+U (/cdn-cgi/login) → [[Feroxbuster]] → Login as guest → IDOR (id=1 → admin) → Cookie → admin → Upload webshell PHP → www-data + TTY → user.txt → db.php → cred robert → SSH → LinPEAS → grupo bugtracker → root
```

### Técnicas clave

- **IDOR**: iterar `id` en la URL → Access ID del admin
- **Cookie tampering**: cambiar role/id → acceso admin
- **Web shell PHP** en uploads → reverse shell
- **Reutilización de credenciales**: db.php → SSH robert
- **Escalada**: grupo `bugtracker` → binario SUID

---

## ⑤ Archetype (HTB Starting Point)

### Cadena completa

```
[[Nmap]] (445, 1433) → [[SMB_Impacket]] sesión nula → Credenciales en backups → MSSQL → xp_cmdshell → Reverse shell + WinPEAS → Credenciales en historial PowerShell → psexec → Administrator
```

### Técnicas clave

- **SMB sesión nula** → `smbclient -N -L //IP/`
- **Archivo config** con credenciales de SQL
- **[[SMB_Impacket]]** → MSSQL → sysadmin → xp_cmdshell
- **WinPEAS** → historial PowerShell con contraseña de Administrator

---

## ⑥ Vaccine (HTB)

### Cadena completa

```
FTP anon → backup.zip → zip2john + [[John_Hashcat]] → MD5 → login admin:qwerty789 → SQLi → [[SQLMap]] --os-shell → reverse shell → dashboard.php (cred) → SSH postgres → sudo -l → /bin/vi (GTFOBins) → root
```

### Técnicas clave

- **[[SQLMap]]** con cookie para bypassear autenticación
- **GTFOBins**: `sudo /bin/vi` → `:!/bin/bash` → root
- **Reutilización de credenciales**: PostgreSQL → SSH

---

## ⑦ Crocodile (HTB Tier 2)

### Cadena completa (fuente: Andres 12.06)

```
FTP Anonymous → backup.zip → zip2john + John → hash MD5 en index.php → CrackStation → admin:password789 → SQLMap → os-shell → reverse shell (netcat) → SSH con credenciales reutilizadas → sudo -l (vi) → root
```

### Escalada con VI + sudo

```bash
sudo -l
# → ALL · Allowed: /usr/bin/vi /etc/postgresql/11/main/pg_hba.conf

sudo vi /etc/postgresql/11/main/pg_hba.conf
# Dentro de VI:
:!sh
# → Shell como root
```

> [!important] VI COMO VECTOR
> El usuario puede ejecutar VI como **cualquier usuario** (incluido root). VI no es solo un editor: `:!sh` lanza shell. Siempre consultar **GTFOBins** para cada binario con sudo.

---

## ⑧ Tier 0 — HTB Starting Point (Chema)

| Máquina | Puerto / Servicio | Vector | Acceso |
|---------|-------------------|--------|--------|
| **Meow** | 23 / Telnet | Login `root` sin contraseña | root directo |
| **Fawn** | 21 / FTP | Login anónimo (`anonymous`) | Lectura de ficheros (`get flag.txt`) |
| **Dancing** | 445 / SMB | Null session + share `WorkShares` (READ,WRITE) | Ficheros del share |
| **Redeemer** | 6379 / Redis | Sin autenticación → `select 0` → `keys *` → `get flag` | Lectura de la BD |

```bash
# Fawn
ftp <IP> → anonymous → ls → get flag.txt
# Dancing
smbclient -N -L //<IP>          # listar shares
netexec smb <IP> -u '' -p '' --shares   # ver permisos
smbclient -N //<IP>/WorkShares  # conectar
# Redeemer
nmap -p- -Pn <IP>               # el top-1000 NO encuentra 6379
redis-cli -h <IP> → info → select 0 → keys * → get flag
```

> [!tip] PATRÓN TIER 0
> Enumerar con Nmap → identificar el servicio → HackTricks → explotar una **mala configuración** (credenciales por defecto, acceso anónimo, falta de autenticación) → leer la flag. *Los servicios son siempre los mismos: a la quincuagésima vez los explotas con los ojos cerrados.*

> [!info] FLAGS EN HTB
> Casi siempre en el escritorio o home: `/root/flag.txt` o `/home/<usuario>/...`. Acostúmbrate a `pwd` y `ls` nada más entrar. Las flags suelen ser dinámicas por usuario.

---

## ⑨ Resumen de máquinas

| Máquina | OS | Cadena resumida |
|---------|----|----------------|
| **Meow / Fawn / Dancing / Redeemer** | Linux/Windows | Tier 0: mala configuración → flag directa (Telnet/FTP anon/SMB/Redis) |
| **RickdiculouslyEasy** | Linux | RCE web → SSH → Robo ficheros → Hydra → sudo su |
| **Mr. Robot** | Linux | robots.txt → Diccionario → Enumerar usuario → Fuerza bruta → 404.php → SUID nmap |
| **Oopsie** | Linux | IDOR → Cookie → Webshell → db.php → bugtracker SUID |
| **Archetype** | Windows | SMB → MSSQL → xp_cmdshell → WinPEAS → psexec |
| **Vaccine** | Linux | FTP → zip2john → SQLi → [[SQLMap]] → GTFOBins vi |
| **Crocodile** | Linux | FTP anon → zip2john → CrackStation → SQLMap → GTFOBins vi (`:!sh`) |

---

## Checklist de repaso

- [ ] ¿Puedo describir la cadena de explotación de cada máquina?
- [ ] ¿Sé aplicar IDOR y cookie tampering?
- [ ] ¿Entiendo el secuestro de PATH y GTFOBins?
- [ ] ¿Sé usar [[SMB_Impacket]] sesión nula y MSSQL con [[SMB_Impacket]]?
- [ ] ¿Recuerdo siempre dejar el listener antes de la reverse shell?
- [ ] ¿Sé escalar con `sudo vi` + `:!sh` (Crocodile / Vaccine)?
- [ ] ¿Conozco las 4 máquinas del Tier 0 y sus vectores de mala configuración?
- [ ] ¿Sé usar Redis (`redis-cli`, `keys *`, `get`) y enumerar shares con NetExec?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Hack The Box, Post-Explotacion, Windows
- [[../../apuntes Andres/15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows.md|15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows]] — Hack The Box, Post-Explotacion, Windows
- [[Reverse Shells y Post-Explotación.md|Reverse Shells y Post-Explotación]] — Hack The Box, Linux, Windows
- [[../../apuntes Joselu/MODULO3/resumen_master_clase35.md|resumen_master_clase35]] — File Upload, Hack The Box, Windows
- [[../../apuntes Joselu/MODULO3/resumen_master_clase30.md|resumen_master_clase30]] — File Upload, Post-Explotacion, Windows

### 🌐 Cross-Dominio

- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Linux, SQL
- [[../../../programacion/Bash/seguridad_bash.md|seguridad_bash]] — Programacion: Desarrollo Web, Linux, SQL

> #burpsuite #cli #command_injection #escalada_privilegios #file_upload #hack_the_box #hydra #idor #java #linux #linux_ciber #metasploit #netcat #pentest #post_explotacion #redes #redes_ciber #reverse_shell #smb_impacket #sql #sqli #sqlmap_tool #ssh_tool #vulnhub #web #windows_ciber #wordpress
