

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

- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]]— Kali Linux, Redes, Windows
- [[../../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]]— Kali Linux, Linux, Redes
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]]— Linux, Redes, Windows
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]]— Linux, Metodología Pentest, Redes
- [[../../apuntes Chema/Bash y PowerShell.md|Bash y PowerShell]]— Kali Linux, Linux, Redes
- [[../../apuntes Chema/Anonimato, Ingeniería Social y Enumeración Web.md|Anonimato, Ingeniería Social y Enumeración Web]]— Kali Linux, Redes, Windows

> #kali #linux #pentest #redes #windows
