# Tmux — Terminal Multiplexer

> [!info] Herramienta
> Multiplexor de terminales: sesiones persistentes, paneles, ventanas y copy mode.
## Sesiones

> [!tip] Gestión de sesiones
> Las sesiones sobreviven a la desconexión SSH.

| Comando | Descripción |

| `tmux` | Nueva sesión |
| `tmux new -s <nombre>` | Sesión con nombre |
| `tmux ls` | Listar sesiones |
| `tmux a` | Última sesión |
| `tmux a -t <nombre>` | Sesión específica |
| `tmux kill-session -t <nombre>` | Cerrar sesión |
| `tmux kill-server` | Cerrar todas las sesiones |

```bash
# Crear sesión
tmux new -s pentest

# Listar sesiones
tmux ls

# Reanudar sesión
tmux a -t pentest
| ```
## Atajos de Teclado

> [!abstract] Prefijo
> Todos los atajos empiezan con `Ctrl+b` (prefijo).

| Atajo | Descripción |

| `Ctrl+b` | Prefijo (indicador) |
| `Ctrl+b d` | Desacoplar sesión (detach) |
| `Ctrl+b z` | Zoom panel (full screen toggle) |
| `Ctrl+b ?` | Listar atajos |
| `Ctrl+b :` | Modo comando |
| `Ctrl+b [` | Enter copy mode |
| `Ctrl+b ]` | Pegar buffer |

---

## Ventanas

| Atajo | Descripción |
|-------|-------------|
| `Ctrl+b c` | Nueva ventana |
| `Ctrl+b ,` | Renombrar ventana |
| `Ctrl+b n` | Siguiente ventana |
| `Ctrl+b p` | Ventana anterior |
| `Ctrl+b <número>` | Ir a ventana número |
| `Ctrl+b w` | Listar ventanas |
| `Ctrl+b &` | Cerrar ventana |

---

## Paneles

| Atajo | Descripción |
|-------|-------------|
| `Ctrl+b %` | Dividir vertical |
| `Ctrl+b "` | Dividir horizontal |
| `Ctrl+b ←↑↓→` | Navegar paneles |
| `Ctrl+b o` | Siguiente panel |
| `Ctrl+b q` | Mostrar números |
| `Ctrl+b x` | Cerrar panel |
| `Ctrl+b z` | Zoom panel |
| `Ctrl+b {` | Mover panel izquierda |
| `Ctrl+b }` | Mover panel derecha |
| | `Ctrl+b Espacio` | Cambiar layout |
|--------------------------------------------|-------------------------|
## Copy Mode

> [!note] Navegación
> Navegar por el historial de la terminal.

| Atajo | Descripción |

| `Ctrl+b [` | Entrar a copy mode |
| `q` | Salir de copy mode |
| `Espacio` | Iniciar selección |
| `Enter` | Copiar selección |
| `Ctrl+b ]` | Pegar |
| `↑↓←→` | Navegar |
| `/` | Buscar adelante |
| `?` | Buscar atrás |
| `n` | Siguiente resultado |
| `N` | Resultado anterior |

---

## Comandos de Shell

```bash
# Renombrar ventana
tmux rename-window -t 0 "nmap"

# Mover ventana
tmux move-window -t 1

# Enviar comando a panel
tmux send-keys -t 1 "ls -la" Enter

# Capturar contenido de panel
tmux capture-pane -t 0 > /tmp/panel.txt
```

---

## Layouts

| Layout | Descripción |
|--------|-------------|
| `even-horizontal` | Paneles iguales horizontal |
| `even-vertical` | Paneles iguales vertical |
| `main-horizontal` | Grande abajo, pequeños arriba |
| `main-vertical` | Grande a la derecha, pequeños a la izquierda |
| `tiled` | Cuadrícula |

```bash
# Cambiar layout
Ctrl+b Espacio

# Seleccionar layout específico
Ctrl+b :select-layout main-horizontal
```

---

## Configuración

```bash
# Archivo de configuración
~/.tmux.conf

# Recargar configuración
Ctrl+b :source-file ~/.tmux.conf
```

### Configuración Común

```
# Cambiar prefijo a Ctrl+a
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Navegación con mouse
set -g mouse on

# Iniciar paneles en 1
split-window -h
split-window -v

# Navegar paneles con Alt+arrow
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D
```

---

#checklist
- [ ] Sesiones con `tmux new -s` creadas
- [ ] Atajos `Ctrl+b` dominados
- [ ] Paneles con `Ctrl+b %` y `Ctrl+b "` creados
- [ ] Ventanas con `Ctrl+b c` gestionadas
- [ ] Copy mode con `Ctrl+b [` explorado
- [ ] Configuración personalizada en `.tmux.conf`



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Telnet.md|Telnet]] — Linux, Post-Explotación, Tmux
- [[../apuntes Andres/09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot.md|09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot]] — Hydra, Linux, Tmux
- [[../Apuntes/comandos/Metasploit.md|Metasploit]] — Linux, Metasploit, Redes
- [[../Apuntes/comandos/SSH.md|SSH]] — Hydra, Linux, Metasploit
- [[../informes/Informe_Banco.md|Informe_Banco]] — Linux, Metasploit, Redes
- [[../informes/Informe_Rockstars.md|Informe_Rockstars]] — Hydra, Linux, Post-Explotación

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]
- [[comandos/Tmux|Tmux]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #escalada-privilegios #hydra #lfi #linux #metasploit #pentest #post-explotacion #redes #ssh #telnet #tmux #wireshark
