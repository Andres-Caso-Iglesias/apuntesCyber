# Comandos Windows (CMD y PowerShell)

> [!info] Herramienta
> Referencia completa de comandos Windows: CMD (clásico) y PowerShell (moderno).
## CMD — Navegación

> [!tip] Comandos básicos
> Los comandos esenciales para navegar en CMD.

| Comando | Descripción |

| `dir` | Listar contenido |
| `cd` | Cambiar directorio |
| `md` | Crear directorios |
| `rd` / `rmdir` | Eliminar directorios |
| `cls` | Limpiar pantalla |

### dir - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `/w` | Formato ancho |
| `/p` | Pausar por página |
| `/a` | Mostrar ocultos |
| `/o` | Ordenar |
| `/t` | Clasificar |

### cd - Rutas

| Parámetro | Descripción |
|-----------|-------------|
| `..` | Subir un nivel |
| `\` | Raíz |
| `%CD%` | Directorio actual |

---

## CMD — Archivos

| Comando | Descripción |
|---------|-------------|
| `copy` | Copiar archivos |
| `move` | Mover/renombrar |
| `del` / `erase` | Eliminar archivos |
| `xcopy` | Copiar árboles |
| `robocopy` | Copia robusta |
| `attrib` | Atributos de archivos |

### robocopy — Copia Robusta

> [!important] Reemplaza xcopy
> Más rápido, confiable y con opciones avanzadas.

| Parámetro | Descripción |
|-----------|-------------|
| `/s` | Recursivo |
| `/e` | Todo (incluye vacíos) |
| `/mir` | Espejo |
| `/purge` | Limpiar destino |
| `/mt:n` | Hilos paralelos |

### attrib — Atributos

| Parámetro | Descripción |
|-----------|-------------|
| `+r/-r` | Solo lectura |
| `+h/-h` | Oculto |
| `+s/-s` | Sistema |
| `/s` | Recursivo |

---

## CMD — Procesos

| Comando | Descripción |
|---------|-------------|
| `tasklist` | Mostrar procesos |
| `taskkill` | Matar procesos |
| `systeminfo` | Info del sistema |
| `taskmgr` | Administrador de tareas |

### tasklist

```bash
# Filtrar por nombre
tasklist /fi "imagename eq chrome.exe"

# Formato CSV
tasklist /fo csv /nh
```

### taskkill

```bash
# Matar por PID
taskkill /pid 1234 /f

# Matar por nombre
taskkill /im notepad.exe /f

# Matar árbol de procesos
taskkill /pid 1234 /t /f
```

---

## CMD — Red

| Comando | Descripción |
|---------|-------------|
| `ipconfig` | Configuración de red |
| `ping` | Verificar conectividad |
| `tracert` | Ruta de paquetes |
| `netstat` | Conexiones de red |
| `arp` | Tabla ARP |
| `nslookup` | Consultas DNS |
| `net view` | Ver equipos en dominio |
| `net use` | Conectar recursos compartidos |

### ipconfig — Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `/all` | Toda la información |
| `/release` | Liberar DHCP |
| `/renew` | Renovar DHCP |
| `/flushdns` | Limpiar caché DNS |

### net use — Recursos Compartidos

```bash
# Mapear unidad
net use Z: \\servidor\recurso

# Desconectar
net use Z: /delete

# Persistente
net use Z: \\servidor\recurso /persistent:yes
```

---

## CMD — Usuarios

| Comando | Descripción |
|---------|-------------|
| `net user` | Gestión de usuarios |
| `net localgroup` | Gestión de grupos |
| `net accounts` | Políticas de cuentas |
| `net share` | Recursos compartidos |
| `net session` | Sesiones activas |
| `net start/stop` | Servicios |

### net user

```bash
# Ver usuario
net user administrator

# Crear usuario
net user nombre contraseña /add

# Activar/desactivar
net user nombre /active:yes
```

### net localgroup

```bash
# Ver grupo
net localgroup Administrators

# Añadir usuario a grupo
net localgroup Administrators nombre /add
| ```
## PowerShell — Navegación

> [!note] Moderno
> PowerShell usa cmdlets con formato `Verb-Noun`.

| Cmdlet | Alias | Descripción |

| `Get-ChildItem` | `ls`, `dir` | Listar contenido |
| `Set-Location` | `cd` | Cambiar directorio |
| `New-Item` | `md` | Crear directorios/archivos |
| `Remove-Item` | `rd`, `del` | Eliminar |
| `Clear-Host` | `cls` | Limpiar pantalla |

### Get-ChildItem

```powershell
# Listar todo
Get-ChildItem

# Recursivo
Get-ChildItem -Recurse

# Solo ocultos
Get-ChildItem -Hidden

# Solo archivos
Get-ChildItem -File

# Solo directorios
Get-ChildItem -Directory
```

---

## PowerShell — Archivos

| Cmdlet | Alias | Descripción |
|--------|-------|-------------|
| `Copy-Item` | `copy` | Copiar |
| `Move-Item` | `move` | Mover |
| `Get-Content` | `cat`, `type` | Leer archivo |
| `Set-Content` | - | Escribir archivo |
| `Select-String` | `grep` | Buscar patrones |
| `Out-File` | - | Redirigir a archivo |

### Get-Content

```powershell
# Leer archivo completo
Get-Content archivo.txt

# Primeras N líneas
Get-Content archivo.txt -TotalCount 10

# Últimas N líneas
Get-Content archivo.txt -Tail 5
```

### Select-String

```powershell
# Buscar patrón
Select-String -Pattern "error" -Path archivo.txt

# Case sensitive
Select-String -Pattern "Error" -Path archivo.txt -CaseSensitive

# Con contexto
Select-String -Pattern "error" -Path archivo.txt -Context 3
```

---

## PowerShell — Procesos

| Cmdlet | Alias | Descripción |
|--------|-------|-------------|
| `Get-Process` | `ps`, `gps` | Ver procesos |
| `Stop-Process` | `kill`, `spps` | Matar proceso |
| `Get-Service` | `gsv` | Ver servicios |
| `Start-Service` | - | Iniciar servicio |
| `Stop-Service` | - | Detener servicio |

```powershell
# Ver proceso específico
Get-Process -Name chrome

# Ver con usuario
Get-Process -IncludeUserName

# Matar proceso
Stop-Process -Name notepad -Force
```

---

## PowerShell — Red

| Cmdlet | Alias | Descripción |
|--------|-------|-------------|
| `Test-Connection` | `ping`, `tnc` | Verificar conectividad |
| `Get-NetIPAddress` | - | Direcciones IP |
| `Get-NetRoute` | - | Tabla de enrutamiento |
| `Get-NetAdapter` | - | Adaptadores de red |
| `Resolve-DnsName` | `nslookup` | Consultas DNS |

```powershell
# Ping con ICMP
Test-Connection -TargetName 8.8.8.8 -Ping

# Test de puerto TCP
Test-Connection -TargetName 8.8.8.8 -TcpPort 80

# Consulta DNS
Resolve-DnsName -Name google.com
```

---

#checklist
- [ ] CMD: `dir`, `cd`, `copy`, `del` dominados
- [ ] CMD: `ipconfig`, `ping`, `netstat` configurados
- [ ] CMD: `tasklist`, `taskkill` para procesos
- [ ] PowerShell: `Get-ChildItem`, `Get-Content` practicados
- [ ] PowerShell: `Select-String`, `Test-Connection` manejados
- [ ] PowerShell: Cmdlets `Verb-Noun` entendidos
