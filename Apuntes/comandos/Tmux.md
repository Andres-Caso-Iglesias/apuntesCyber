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

- [[Windows.md|Windows]] — Linux, Linux, Metodologia Pentest
- [[../02 - Sistemas Operativos/Consolas - Bash y PowerShell.md|Consolas - Bash y PowerShell]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/Windows.md|Windows]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/SMB_Impacket.md|SMB_Impacket]] — Linux, Linux, Metodologia Pentest
- [[SMB_Impacket.md|SMB_Impacket]] — Linux, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #cli #linux #linux_ciber #pentest #redes #tmux #windows_ciber
