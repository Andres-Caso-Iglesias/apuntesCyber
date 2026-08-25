

> [!info] Relacionado con
> [[MetodologÃ­a de ExplotaciÃ³n]] Â· [[ExplotaciÃ³n de Servicios - Linux]] Â· [[ExplotaciÃ³n de Servicios - Windows]] Â· [[Escalada de Privilegios]] Â· [[Reverse Shells y Post-ExplotaciÃ³n]]
> â†’

---

## â‘  Flujo general de un CTF

```
Superficie expuesta â†’ EnumeraciÃ³n â†’ ExplotaciÃ³n â†’ Shell â†’ Enumerar dentro â†’ Escalada â†’ Root
```

---

## â‘¡ RickdiculouslyEasy (VulnHub)

### Cadena completa

```
www-data (RCE web) â†’ summer (SSH:22222) â†’ Robo de ficheros â†’ [[Hydra]] â†’ RickSanchez â†’ sudo su â†’ root
```

### Fase externa

| Puerto | Servicio | Hallazgo |
|--------|---------|---------|
| 21 | FTP anon | Login anÃ³nimo, flag.txt |
| 80 | Web | Command Injection en cgi-bin |
| 60000 | TCP | Backdoor con shell vÃ­a nc |
| 22222 | SSH real | El SSH autÃ©ntico |

### Escalada

1. **Summer â†’ SSH** con contraseÃ±a `winter` (encontrada en passwords.html)
2. **Robo de ficheros** entre usuarios (binario safe, imagen con contraseÃ±a)
3. **[[Hydra]]** â†’ RickSanchez: `P7Curtains`
4. **sudo su** â†’ root (RickSanchez tiene `(ALL : ALL) ALL`)

---

## â‘¢ Mr. Robot (VulnHub)

### Cadena (hasta ahora)

```
[[Nmap]] (80/443) â†’ robots.txt â†’ fsocity.dic â†’ Limpiar diccionario â†’ Enumerar usuario: Elliot â†’ Fuerza bruta pwd (pendiente)
```

### TÃ©cnicas clave

- **robots.txt** â†’ diccionario de ~858K lÃ­neas â†’ limpiar con `sort | uniq` â†’ ~11K
- **EnumeraciÃ³n por longitud de respuesta** en Intruder de Burp
- **Information disclosure** en login de WordPress

---

## â‘£ Oopsie (HTB Starting Point)

### Cadena completa

```
[[Nmap]] â†’ web + Ctrl+U (/cdn-cgi/login) â†’ [[Feroxbuster]] â†’ Login as guest â†’ IDOR (id=1 â†’ admin) â†’ Cookie â†’ admin â†’ Upload webshell PHP â†’ www-data + TTY â†’ user.txt â†’ db.php â†’ cred robert â†’ SSH â†’ LinPEAS â†’ grupo bugtracker â†’ root
```

### TÃ©cnicas clave

- **IDOR**: iterar `id` en la URL â†’ Access ID del admin
- **Cookie tampering**: cambiar role/id â†’ acceso admin
- **Web shell PHP** en uploads â†’ reverse shell
- **ReutilizaciÃ³n de credenciales**: db.php â†’ SSH robert
- **Escalada**: grupo `bugtracker` â†’ binario SUID

---

## â‘¤ Archetype (HTB Starting Point)

### Cadena completa

```
[[Nmap]] (445, 1433) â†’ [[SMB_Impacket]] sesiÃ³n nula â†’ Credenciales en backups â†’ MSSQL â†’ xp_cmdshell â†’ Reverse shell + WinPEAS â†’ Credenciales en historial PowerShell â†’ psexec â†’ Administrator
```

### TÃ©cnicas clave

- **SMB sesiÃ³n nula** â†’ `smbclient -N -L //IP/`
- **Archivo config** con credenciales de SQL
- **[[SMB_Impacket]]** â†’ MSSQL â†’ sysadmin â†’ xp_cmdshell
- **WinPEAS** â†’ historial PowerShell con contraseÃ±a de Administrator

---

## â‘¥ Vaccine (HTB)

### Cadena completa

```
FTP anon â†’ backup.zip â†’ zip2john + [[John_Hashcat]] â†’ MD5 â†’ login admin:qwerty789 â†’ SQLi â†’ [[SQLMap]] --os-shell â†’ reverse shell â†’ dashboard.php (cred) â†’ SSH postgres â†’ sudo -l â†’ /bin/vi (GTFOBins) â†’ root
```

### TÃ©cnicas clave

- **[[SQLMap]]** con cookie para bypassear autenticaciÃ³n
- **GTFOBins**: `sudo /bin/vi` â†’ `:!/bin/bash` â†’ root
- **ReutilizaciÃ³n de credenciales**: PostgreSQL â†’ SSH

---

## â‘¦ Resumen de mÃ¡quinas

| MÃ¡quina | OS | Cadena resumida |
|---------|----|----------------|
| **RickdiculouslyEasy** | Linux | RCE web â†’ SSH â†’ Robo ficheros â†’ Hydra â†’ sudo su |
| **Mr. Robot** | Linux | robots.txt â†’ Diccionario â†’ Enumerar usuario â†’ Fuerza bruta |
| **Oopsie** | Linux | IDOR â†’ Cookie â†’ Webshell â†’ db.php â†’ bugtracker SUID |
| **Archetype** | Windows | SMB â†’ MSSQL â†’ xp_cmdshell â†’ WinPEAS â†’ psexec |
| **Vaccine** | Linux | FTP â†’ zip2john â†’ SQLi â†’ [[SQLMap]] â†’ GTFOBins vi |

â†’

---

## Checklist de repaso

- [ ] Â¿Puedo describir la cadena de explotaciÃ³n de cada mÃ¡quina?
- [ ] Â¿SÃ© aplicar IDOR y cookie tampering?
- [ ] Â¿Entiendo el secuestro de PATH y GTFOBins?
- [ ] Â¿SÃ© usar [[SMB_Impacket]] sesiÃ³n nula y MSSQL con [[SMB_Impacket]]?
- [ ] Â¿Recuerdo siempre dejar el listener antes de la reverse shell?

â†’

