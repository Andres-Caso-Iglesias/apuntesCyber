

> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]]
> →

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

### Cadena (hasta ahora)

```
[[Nmap]] (80/443) → robots.txt → fsocity.dic → Limpiar diccionario → Enumerar usuario: Elliot → Fuerza bruta pwd (pendiente)
```

### Técnicas clave

- **robots.txt** → diccionario de ~858K líneas → limpiar con `sort | uniq` → ~11K
- **Enumeración por longitud de respuesta** en Intruder de Burp
- **Information disclosure** en login de WordPress

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

## ⑦ Resumen de máquinas

| Máquina | OS | Cadena resumida |
|---------|----|----------------|
| **RickdiculouslyEasy** | Linux | RCE web → SSH → Robo ficheros → Hydra → sudo su |
| **Mr. Robot** | Linux | robots.txt → Diccionario → Enumerar usuario → Fuerza bruta |
| **Oopsie** | Linux | IDOR → Cookie → Webshell → db.php → bugtracker SUID |
| **Archetype** | Windows | SMB → MSSQL → xp_cmdshell → WinPEAS → psexec |
| **Vaccine** | Linux | FTP → zip2john → SQLi → [[SQLMap]] → GTFOBins vi |

→

---

## Checklist de repaso

- [ ] ¿Puedo describir la cadena de explotación de cada máquina?
- [ ] ¿Sé aplicar IDOR y cookie tampering?
- [ ] ¿Entiendo el secuestro de PATH y GTFOBins?
- [ ] ¿Sé usar [[SMB_Impacket]] sesión nula y MSSQL con [[SMB_Impacket]]?
- [ ] ¿Recuerdo siempre dejar el listener antes de la reverse shell?

→

