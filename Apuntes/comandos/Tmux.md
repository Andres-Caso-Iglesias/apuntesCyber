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

- [[Linux.md|Linux]] — Linux, Tmux, Windows
- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Linux, Tmux, Windows
- [[../../comandos/Windows.md|Windows]] — Linux, Tmux, Windows
- [[../08 - Metodologías/Metodología - Active Directory.md|Metodología - Active Directory]] — Linux, Redes, Tmux
- [[Windows.md|Windows]] — Metodología Pentest, Redes, Tmux
- [[../../comandos/John_Hashcat.md|John_Hashcat]] — Linux, Tmux, Windows

### 🛠️ Herramientas

- [[comandos/Tmux|Tmux]]

> #linux #pentest #redes #tmux #windows
