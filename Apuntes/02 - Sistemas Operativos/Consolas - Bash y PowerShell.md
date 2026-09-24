

> [!info] Relacionado con
> [[Linux - Fundamentos]] · [[Linux - Bash Scripting]] · [[Bash Scripting]] · [[Bash y PowerShell]] · [[Explotación de Servicios - Windows]] · [[Introducción a Consolas - Bash y PowerShell]]

---

## ① ¿Por qué la línea de comandos?

| Terminal (CLI) | GUI |
|---------------|-----|
| Automatizable con scripts | Más intuitiva para principiantes |
| Herramientas de hacking son CLI | No automatizable directamente |
| Menor consumo de recursos | Mayor consumo de recursos |
| Control total del sistema | Depende del entorno gráfico |

---

## ①bis Terminal vs Shell — no son lo mismo

| Concepto | Qué es | Ejemplos |
|----------|--------|---------|
| **Terminal** | El programa que muestra la ventana donde escribimos | GNOME Terminal, iTerm2, Windows Terminal |
| **Shell** | El intérprete que corre *dentro* de la terminal | **Bash**, **Zsh**, **PowerShell**, **CMD** |

Bash y PowerShell son dos shells distintas que pueden abrirse dentro del mismo programa Windows Terminal.

**Bash** (*Bourne Again Shell*) es el intérprete estándar de la gran mayoría de distribuciones Linux; fue el shell por defecto de macOS hasta Catalina (2019), cuando fue sustituido por **Zsh** (sintaxis prácticamente idéntica).

> [!info] Kali moderno
> Las versiones nuevas de Kali usan **ZSH** por defecto, pero el 99 % de los servidores que auditarás usan Bash. Especificar `#!/bin/bash` en el shebang garantiza que el script se interprete como Bash independientemente del shell activo.

---

## ②bis Estructura de un comando

```
comando [opciones] [argumento1] [argumento2]
```

- **Opciones cortas**: un guion + letra (`ls -l`); se pueden combinar (`ls -la` = `ls -l -a`).
- **Opciones largas**: dos guiones + palabra (`--help`, `--verbose`); no se combinan.
- Para ver todas las opciones: `comando --help` o `man comando`.

### Editores de texto en terminal

| Editor | Estilo | Guardar y salir |
|--------|--------|-----------------|
| **vi / vim** | Old school | `i` insertar, Esc, `:wq` guardar y salir, `:q!` salir sin guardar |
| **nano** | Moderno y sencillo | `Ctrl+X` para salir, confirmar guardado |
| **micro** | Más moderno con colores | Instalación necesaria; intuitivo |
| `touch` / `cat` | **No son editores** | `touch` solo crea el fichero; `cat` solo muestra |

---

## ② Anatomía de la terminal Bash

```
kali@kali:~$
│ │ │ ││
│ │ │ │└─ $ = usuario normal (# = root)
│ │ │ └── ~ = home del usuario
│ │ └──── directorio actual
│ └──────── hostname
└─────────── usuario
```

### Atajos de teclado

| Atajo | Función |
|-------|---------|
| `Ctrl+C` | Cancelar proceso |
| `Ctrl+Z` | Suspender (bg para background) |
| `Ctrl+L` | Limpiar pantalla |
| `Ctrl+A` | Inicio de línea |
| `Ctrl+E` | Final de línea |
| `Ctrl+R` | Búsqueda en historial |
| `Tab` | Autocompletar |
| `↑ / ↓` | Navegar historial |

---

## ③ Comparativa Bash → PowerShell

| Bash | PowerShell | Función |
|------|-----------|---------|
| `[[Linux#ls|ls]]` | `[[Windows#Get-ChildItem|Get-ChildItem]]` (gci) | Listar |
| `[[Linux#cat|cat]]` | `[[Windows#Get-Content|Get-Content]]` | Leer fichero |
| `[[Linux#echo|echo]]` | `[[Windows#Write-Host|Write-Host]]` | Imprimir |
| `[[Linux#rm|rm]]` | `[[Windows#Remove-Item|Remove-Item]]` | Borrar |
| `[[Linux#cp|cp]]` | `[[Windows#Copy-Item|Copy-Item]]` | Copiar |
| `[[Linux#mv|mv]]` | `[[Windows#Move-Item|Move-Item]]` | Mover |
| `[[Linux#grep|grep]]` | `[[Windows#Select-String|Select-String]]` | Buscar patrón |
| `[[Linux#find|find]]` | `[[Windows#Get-ChildItem|Get-ChildItem]] -Recurse` | Buscar ficheros |

> [!tip] PENTEST
> PowerShell permite ejecutar código en memoria, descargar payloads y moverse lateralmente. Por eso muchas empresas restringen su ejecución.

---

## ③bis CMD vs PowerShell (Windows)

| Característica | CMD | PowerShell |
|----------------|-----|-----------|
| Antigüedad | Heredado de MS-DOS | Moderno (2006) |
| Comandos Linux | No (solo `ls` en versiones recientes) | Sí (`ls`, `cat`, `cd`...) |
| Cmdlets propios | No | Sí (`Get-Process`, `Set-Item`...) |
| Scripting avanzado | Limitado | Completo (bucles, objetos, .NET) |
| Ejecutar `.exe` | Directamente por nombre | Con `.\ejecutable.exe` o ruta completa |
| Monitorización EDR | Menor | **PowerShell es más potente pero más monitorizado** |

| Acción | Linux | CMD Windows |
|--------|-------|-------------|
| Listar | `ls` / `ls -la` | `dir` / `dir /a` |
| Listar recursivo | `find / -name "*.txt"` | `dir /s *.txt` |
| Limpiar pantalla | `clear` | `cls` |
| Filtrar texto | `grep "texto" fichero` | `findstr "texto" fichero` |
| Historial | `history` | `doskey /history` |
| Borrar recursivo (silencioso) | `rm -rf` | `rd /s /q` (el `/q` evita alertas en el SIEM) |
| Guardar/volver de directorio | — | `pushd ruta` / `popd` |

- Desde CMD se puede lanzar `powershell.exe` y viceversa (`cmd.exe`).
- `sudo !!` (en Bash) repite el último comando con privilegios; en Windows: clic derecho → "Ejecutar como administrador".
- **Trampa de PowerShell**: también acepta `ls`, por lo que en ejercicios "¿Windows acepta ls?" la respuesta es sí.

### Equivalencias clave whoami

```powershell
whoami # máquina\usuario actual
whoami /all # usuario, SID, grupos y privilegios
whoami /priv # solo privilegios (buscar SeImpersonatePrivilege)
whoami /groups # grupos a los que pertenece
```

> [!important] SID
> El **SID** (*Security Identifier*) es el DNI de Windows: el nombre puede cambiar pero el SID es permanente; muchas técnicas exigen especificar el SID.

---

## ④ Comandos de red

```bash
# Bash
[[Linux#ip|ip]] a # interfaces (moderno)
ifconfig # interfaces (legacy)
[[Linux#ss|ss]] -tulnp # puertos abiertos (moderno)
[[Linux#netstat|netstat]] -tulnp # puertos abiertos (legacy)
[[Linux#ping|ping]] -c4 8.8.8.8 # conectividad
[[Linux#curl|curl]] ifconfig.me # IP pública
nc -lvnp 4444 # escuchar puerto
```

```powershell
# PowerShell
[[Windows#ipconfig|ipconfig]] /all # interfaces de red
Get-NetTCPConnection # conexiones TCP
whoami # usuario actual
Get-LocalUser # usuarios locales
[[Windows#Get-Process|Get-Process]] # procesos
```

---

## ⑤ Gestión de paquetes en Kali

```bash
sudo apt update # actualizar lista
sudo apt upgrade -y # actualizar paquetes
sudo apt install nombre # instalar
sudo apt remove nombre # desinstalar
sudo apt search herramienta # buscar
pip install herramienta # paquetes Python
```

---

## ⑥ Virtualización — Entorno de trabajo

| Opción | Notas |
|--------|-------|
| **VirtualBox** | Gratuito. Para empezar. |
| **VMware** | Más rendimiento. Preferido en el máster. |
| **WSL2** | Bash en Windows. No recomendado para el máster. |

### Formatos de disco virtual

| Formato | Hipervisor |
|---------|-----------|
| **VDI** | VirtualBox |
| **VMDK** | VMware (también lo genera VirtualBox) |
| **OVA/OVF** | Paquete exportable con VM + configuración (doble clic para importar) |

Una VM descargada puede venir solo como `.vmdk` (disco con todo el sistema dentro) sin `.ova`: en VirtualBox se monta creando la VM a mano y eligendo **"Usar un disco duro virtual existente"**.

> [!tip] Instantáneas
> En VirtualBox: botón derecho sobre la máquina → *Instantáneas* → *Tomar instantánea* (con la máquina encendida o apagada). Es una "foto" del estado: permite volver a él si rompes algo (p. ej. con `rm -rf`). Complemento ideal: guardar siempre una imagen base limpia como `.ova`.

### Red en VMs

| Modo | Comunicación | Uso |
|------|-------------|-----|
| **NAT** | VM con internet | Si necesita internet |
| **Host-Only** | VM ↔ Host solamente | CTF / laboratorio (aislado) |
| **Bridged** | VM como equipo más en la red real | Producción |

> [!tip] LABS
> Para laboratorios con varias VMs: usar **Host-Only** para aislamiento de Internet.

---

## Checklist de repaso

- [ ] ¿Sé navegar por la terminal con atajos de teclado?
- [ ] ¿Conozco las equivalencias Bash → PowerShell?
- [ ] ¿Sé configurar una VM con red Host-Only?
- [ ] ¿Entiendo por qué la CLI es preferible al GUI en pentesting?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]] — Kali Linux, Linux, Redes
- [[../comandos/Tmux.md|Tmux]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/SMB_Impacket.md|SMB_Impacket]] — Linux, Metodologia Pentest, Windows
- [[../comandos/Windows.md|Windows]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/Windows.md|Windows]] — Linux, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #cli #kali #linux #linux_ciber #nmap #pentest #redes #tmux #windows_ciber
