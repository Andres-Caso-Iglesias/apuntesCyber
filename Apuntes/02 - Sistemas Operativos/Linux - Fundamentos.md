

> [!info] Relacionado con
> [[Linux - Bash Scripting]] · [[Consolas - Bash y PowerShell]] · [[Explotación de Servicios - Linux]] · [[Escalada de Privilegios]]

---

## ① Sistema de ficheros

Linux organiza todo en una jerarquía desde la raíz `/`:

```
/
├── home/ ← Directorios personales (/home/kali)
├── etc/ ← Ficheros de configuración
├── var/ ← Logs, bases de datos
├── tmp/ ← Temporales (se borran al reiniciar)
├── bin, usr/bin ← Ejecutables
├── root/ ← Home del root
└── dev/ ← Dispositivos
```

> [!important] Concepto clave
> **TODO es un fichero** en Linux: discos, impresoras, procesos... Esto permite manipularlo todo con los mismos comandos.

---

## ② Navegación esencial

```bash
[[Linux#pwd|pwd]] # dónde estoy
[[Linux#ls|ls]] -la # listar con detalles y ocultos
[[Linux#cd|cd]] /ruta/absoluta # ir a ruta absoluta
[[Linux#cd|cd]] ruta/relativa # ir a ruta relativa
[[Linux#cd|cd]] .. # subir un nivel
[[Linux#cd|cd]] ~ # ir al home
[[Linux#cd|cd]] - # volver al directorio anterior
```

> [!tip] RUTAS
> **Absoluta**: empieza por `/` y funciona desde cualquier sitio.
> **Relativa**: parte desde donde estás. **Crucial en escalada de privilegios.**

---

## ③ Gestión de ficheros

```bash
[[Linux#mkdir|mkdir]] -p a/b/c # crear árbol de directorios
[[Linux#touch|touch]] fichero.txt # crear fichero vacío
[[Linux#cp|cp]] origen destino # copiar
[[Linux#mv|mv]] origen destino # mover/renombrar
[[Linux#rm|rm]] fichero # borrar
[[Linux#rm|rm]] -rf directorio/ # ⚠ BORRADO RECURSIVO SIN CONFIRMACIÓN
[[Linux#cat|cat]] fichero.txt # ver contenido
[[Linux#less|less]] fichero.txt # paginado (q para salir)
[[Linux#head|head]] -n 20 fichero.txt # primeras 20 líneas
[[Linux#tail|tail]] -n 20 fichero.txt # últimas 20 líneas
```

> [!danger] PELIGRO
> `rm -rf /` o `rm -rf /*` con root borra **TODO** el sistema. **NUNCA ejecutar contra la raíz.**

---

## ④ Permisos en Linux

Cada fichero tiene tres grupos de permisos:

```
 -rwxr-xr-- 1 kali kali 1234 jun 1 fichero.sh
 ^^^ ^^^ ^^^
 owner group others
```

| Permiso | Significado | Octal |
|---------|------------|-------|
| **r** | Leer | 4 |
| **w** | Escribir | 2 |
| **x** | Ejecutar | 1 |
| **SUID (s)** | Ejecuta con permisos del propietario | 4000 |
| **SGID (s)** | Ejecuta con permisos del grupo | 2000 |
| **Sticky (t)** | Solo el propietario puede borrar | 1000 |

```bash
[[Linux#chmod|chmod]] 755 fichero.sh # rwxr-xr-x
[[Linux#chmod|chmod]] +x fichero.sh # añadir ejecución
[[Linux#chown|chown]] usuario:grupo fich # cambiar propietario
```

> [!warning] HACKING
> Los ficheros con **SUID de root** (`[[Linux#find|find]] / -perm -4000`) son vectores clásicos de **escalada de privilegios**.

---

## ⑤ Redirección y pipes

```bash
comando > fichero.txt # stdout a fichero (sobreescribe)
comando >> fichero.txt # stdout añadiendo al final
comando 2> errores.txt # redirigir stderr
comando 2>/dev/null # descartar errores
cmd1 | cmd2 # pipe: stdout → stdin
```

### Ejemplos prácticos

```bash
[[Nmap]] -sV 192.168.1.1 | [[Linux#grep|grep]] open > puertos_abiertos.txt
cat /etc/passwd | [[Linux#grep|grep]] bash
ls -la | sort -k5 -n # ordenar por tamaño
```

> [!tip] PIPE
> El pipe `|` es la herramienta más potente de la terminal. Encadena comandos sin ficheros intermedios.

---

## ⑥ Búsqueda

```bash
[[Linux#grep|grep]] 'patrón' fichero.txt # buscar patrón
[[Linux#grep|grep]] -r 'patrón' directorio/ # recursivo
[[Linux#grep|grep]] -r 'password' /ruta/ 2>/dev/null # suprime "Permission denied"
[[Linux#find|find]] / -name 'fichero.txt' # buscar por nombre
[[Linux#find|find]] / -name '*.txt' 2>/dev/null # por extensión (comodines)
[[Linux#find|find]] / -type f # solo ficheros | -type d solo directorios
[[Linux#find|find]] / -size +10M # más de 10 MB
[[Linux#find|find]] / -mtime -7 # modificados en los últimos 7 días
[[Linux#find|find]] / -perm u+x # ejecutables por el propietario
[[Linux#find|find]] / -perm -4000 2>/dev/null # ficheros con SUID ← ESCALADA
[[Linux#find|find]] / -name 'user.txt' 2>/dev/null # flags de HTB
[[Linux#find|find]] /home -name '*.tmp' -delete # borrar resultados
which python3 # ruta del ejecutable
[[Linux#locate|locate]] fichero.txt # búsqueda rápida en DB
file nombre_archivo # tipo REAL por magic bytes
```

> [!important] Extensiones en Linux
> En Windows las extensiones (`.txt`, `.exe`) determinan cómo se trata el archivo; **en Linux no significan nada para el sistema**. Lo que importa es el **tipo real**: el primer carácter de `ls -l` (`-` fichero, `d` directorio, `l` enlace) y los **magic bytes**. Los scripts se identifican por el *shebang* (`#!/bin/bash`).
>
> **Implicación ofensiva**: se puede nombrar un `.jpg` con contenido de script y el sistema lo ejecutará — técnica habitual para ocultar malware o reverse shells.

> [!tip] Case sensitivity
> Linux es **case sensitive** (`find / -name "Antonio"` ≠ `"antonio"`); Windows no. Truco para detectar el SO de un servidor web: cambiar una letra de la URL a mayúscula — si carga, es Windows; si da error, Linux.

---

## ⑦ Procesos

```bash
[[Linux#ps|ps]] aux # listar todos los procesos
[[Linux#top|top]] / [[Linux#htop|htop]] # monitor en tiempo real
[[Linux#kill|kill]] -9 PID # matar proceso (SIGKILL)
[[Linux#kill|kill]] -15 PID # terminar educadamente (SIGTERM)
comando & # background
[[Linux#fg|fg]] # traer al frente
```

---

## ⑧ Variables y alias

```bash
alias ll='ls -la' # atajo
export PATH=$PATH:/nueva # añadir ruta al PATH
echo $PATH # ver rutas de búsqueda
```

### PATH Hijacking (escalada)

El `PATH` se lee **de izquierda a derecha**: si colocas un ejecutable con el mismo nombre que un comando legítimo en una carpeta que aparece **antes**, el sistema ejecutará el tuyo. Aplicación ofensiva: si un **cron job** corre como root y llama a un comando por nombre relativo (sin ruta absoluta) y existe una carpeta del PATH escribible por el usuario → shell como root.

```bash
# Persistencia de alias y configuración entre sesiones:
# ~/.bashrc y ~/.bash_profile
```

---

## ⑨ Historial y limpieza

```bash
history # ver historial
history | [[Linux#grep|grep]] [[Nmap]] # buscar en historial
history -c # limpiar en memoria
cat /dev/null > ~/.bash_history # vaciar fichero
export HISTFILE=/dev/null # deshabilitar en sesión
```

> [!info] FORENSE
> El historial se guarda en varios sitios (`~/.bash_history`, `/var/log/auth.log`). Conocer dónde es clave tanto para atacar como para defender. **Enfoque ofensivo**: al comprometer una máquina, revisar el `history` puede revelar credenciales, rutas y conexiones SSH escritas en texto claro. **Enfoque forense**: un atacante que no borra su historial deja un rastro completo — caso real: un hacker español famoso permitió reconstruir toda su actividad.

```bash
# Descomprimir el diccionario de Kali (viene comprimido):
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# tail -f para monitorizar logs en tiempo real (post-explotación):
[[Linux#tail|tail]] -f /var/log/auth.log
```

---

## Checklist de repaso

- [ ] ¿Navego cómodamente por el sistema de ficheros?
- [ ] ¿Entiendo los permisos y cómo se leen?
- [ ] ¿Sé usar pipes y redirecciones?
- [ ] ¿Sé buscar ficheros con find y grep?
- [ ] ¿Conozco los permisos SUID y por qué importan?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../comandos/Linux.md|Linux]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../apuntes Andres/09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot.md|09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../apuntes evolve/BLOQUE 8.md|BLOQUE 8]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../comandos/Tmux.md|Tmux]] — Linux, Linux, Metodologia Pentest
- [[../../comandos/Windows.md|Windows]] — Linux, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/PowerShell/seguridad_powershell.md|seguridad_powershell]] — Programacion: CLI/Scripting, Desarrollo Web, Redes
- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes

> #cli #escalada_privilegios #forense #hydra #linux #linux_ciber #pentest #redes #tmux #web #windows_ciber
