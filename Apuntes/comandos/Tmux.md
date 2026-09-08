# Tmux — Cheat Sheet

> Multiplexor de terminal.

---

## Sesiones

```bash
tmux                             # Nueva sesión
tmux new -s <name>               # Sesión con nombre
tmux ls                         # Listar sesiones
tmux a -t <name>                 # Adjuntar a sesión
tmux kill-session -t <name>      # Matar sesión
```

## Panes

```bash
Ctrl+b %                        # Dividir verticalmente
Ctrl+b "                        # Dividir horizontalmente
Ctrl+b o                        # Cambiar entre panes
Ctrl+b x                        # Cerrar pane
Ctrl+b z                        # Zoom pane
```

## Ventanas

```bash
Ctrl+b c                        # Nueva ventana
Ctrl+b ,                        # Renombrar ventana
Ctrl+b n                        # Siguiente ventana
Ctrl+b p                        # Ventana anterior
Ctrl+b 0-9                      # Ir a ventana por número
```

## Atajos útiles

```bash
Ctrl+b d                        # Detach de sesión
Ctrl+b [                        # Modo scroll (copiar)
Ctrl+b ]                        # Pegar
Ctrl+b :                        # Command prompt
```

## Configuración (~/.tmux.conf)

```bash
set -g mouse on                  # Habilitar mouse
set -g history-limit 50000       # Historial largo
set -g base-index 1              # Empezar en 1
setw -g pane-base-index 1
```


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../08 - Metodologías/Metodología - Active Directory.md|Metodología - Active Directory]] — Linux, Redes, Windows
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Redes, Windows
- [[../../comandos/Windows.md|Windows]] — Linux, Redes, Windows
- [[../02 - Sistemas Operativos/Linux - Fundamentos.md|Linux - Fundamentos]] — Linux, Redes, Windows
- [[../../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]] — Linux, Redes, Windows
- [[../../comandos/John_Hashcat.md|John_Hashcat]] — Linux, Redes, Windows

### 🛠️ Herramientas

- [[comandos/Tmux|Tmux]]

> #linux #redes #tmux #windows
