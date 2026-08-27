# ① Sistema de ficheros Linux

Linux organiza todo en una jerarquía de directorios que parte de la raíz (/). Cada fichero y dispositivo es un nodo de ese árbol.

|**Directorio**|**Contenido**|
|---|---|
|/|Raíz del sistema. Todo cuelga de aquí.|
|/home|Directorios personales de cada usuario (p.ej. /home/kali)|
|/etc|Ficheros de configuración del sistema|
|/var|Datos variables: logs, bases de datos, colas|
|/tmp|Ficheros temporales (se borran en cada reinicio)|
|/bin, /usr/bin|Ejecutables del sistema y de usuario|
|/root|Directorio home del usuario root|

| | |
|---|---|
|**💡 CLAVE**|/todo/es/un/fichero en Linux: discos, impresoras, procesos... esto permite manipularlo todo con los mismos comandos.|

# ② Comandos de navegación esenciales

| |
|---|
|pwd                    # dónde estoy ahora (Print Working Directory)<br><br>ls                     # listar ficheros del directorio actual<br><br>ls -la                 # listar con permisos, ocultos y tamaños<br><br>cd /ruta/absoluta      # ir a ruta absoluta (desde /)<br><br>cd ruta/relativa       # ir a ruta relativa (desde donde estoy)<br><br>cd ..                  # subir un nivel (directorio padre)<br><br>cd ~                   # ir al home del usuario<br><br>cd -                   # volver al directorio anterior|

| | |
|---|---|
|**ℹ RUTAS**|Ruta absoluta: empieza por / y lleva la ruta completa. Ruta relativa: parte desde donde estás ahora. Esto es crítico en escalada de privilegios.|

# ③ Gestión de ficheros y directorios

| |
|---|
|mkdir clase            # crear directorio<br><br>mkdir -p a/b/c         # crear árbol de directorios de una vez<br><br>touch fichero.txt      # crear fichero vacío (o actualizar timestamp)<br><br>cp origen destino      # copiar fichero<br><br>mv origen destino      # mover o renombrar<br><br>rm fichero             # borrar fichero<br><br>rm -rf directorio/     # ⚠ borrar directorio recursivamente SIN confirmación<br><br>cat fichero.txt        # mostrar contenido de un fichero<br><br>less fichero.txt       # ver fichero paginado (q para salir)<br><br>head -n 20 fichero.txt # primeras 20 líneas<br><br>tail -n 20 fichero.txt # últimas 20 líneas|

| | |
|---|---|
|**⚠ PELIGRO**|rm -rf / o rm -rf /* con permisos de root borra TODO el sistema sin confirmación. Nunca ejecutar contra la raíz /.|

# ④ Permisos en Linux

Cada fichero tiene tres grupos de permisos: propietario (u), grupo (g) y otros (o).

| |
|---|
|# Formato de ls -la:<br><br># -rwxr-xr--  1  kali  kali  1234  jun  1  fichero.sh<br><br>#  ^^^           = permisos propietario (rwx = leer, escribir, ejecutar)<br><br>#     ^^^        = permisos grupo (r-x = leer y ejecutar)<br><br>#        ^^^     = permisos otros (r-- = solo leer)<br><br>chmod 755 fichero.sh   # rwxr-xr-x  (octal)<br><br>chmod +x fichero.sh    # añadir permiso de ejecución<br><br>chmod u-w fichero.txt  # quitar escritura al propietario<br><br>chown usuario:grupo fichero  # cambiar propietario|

|**Permiso**|**Significado**|
|---|---|
|r (4)|Leer el contenido del fichero / listar el directorio|
|w (2)|Modificar el fichero / crear o borrar ficheros en el directorio|
|x (1)|Ejecutar el fichero / entrar al directorio (cd)|
|SUID (s)|El fichero se ejecuta con los permisos de su propietario|
|SGID (s)|El fichero se ejecuta con los permisos del grupo|
|Sticky (t)|Solo el propietario puede borrar ficheros en el directorio|

| | |
|---|---|
|**🔐 HACKING**|Los ficheros con SUID de root (find / -perm -4000) son vectores clásicos de escalada de privilegios.|

# ⑤ Redirección y pipes

| |
|---|
|comando > fichero.txt   # redirigir stdout a fichero (sobreescribe)<br><br>comando >> fichero.txt  # redirigir stdout añadiendo al final<br><br>comando 2> errores.txt  # redirigir stderr<br><br>comando 2>/dev/null     # descartar errores<br><br>comando < entrada.txt   # usar fichero como stdin<br><br>cmd1 | cmd2             # pipe: stdout de cmd1 → stdin de cmd2<br><br># Ejemplos prácticos:<br><br>nmap -sV 192.168.1.1 | grep open > puertos_abiertos.txt<br><br>cat /etc/passwd | grep bash<br><br>ls -la | sort -k5 -n    # ordenar por tamaño|

| | |
|---|---|
|**💡 PIPE**|El pipe | es la herramienta más potente de la terminal. Encadena comandos sin ficheros intermedios. Fundamental en bash scripting.|

# ⑥ Búsqueda: grep, find y which

| |
|---|
|grep 'patrón' fichero.txt       # buscar patrón en fichero<br><br>grep -r 'patrón' directorio/    # buscar recursivamente<br><br>grep -i 'patrón' fichero.txt    # sin distinguir mayúsculas<br><br>grep -v 'patrón' fichero.txt    # líneas que NO contienen el patrón<br><br>find / -name 'fichero.txt'      # buscar por nombre desde la raíz<br><br>find / -perm -4000 2>/dev/null  # buscar ficheros con SUID<br><br>find /home -user kali           # ficheros de un usuario concreto<br><br>find . -mtime -7                # modificados en los últimos 7 días<br><br>which python3                   # ruta del ejecutable<br><br>locate fichero.txt              # búsqueda rápida en base de datos|

# ⑦ Procesos

| |
|---|
|ps aux                 # listar todos los procesos<br><br>ps aux | grep nginx    # buscar proceso concreto<br><br>top                    # monitor de procesos en tiempo real<br><br>htop                   # monitor visual (más cómodo)<br><br>kill -9 PID            # matar proceso por ID<br><br>killall nombre         # matar todos los procesos con ese nombre<br><br>jobs                   # listar procesos en background de esta sesión<br><br>comando &              # lanzar proceso en background<br><br>fg                     # traer último proceso background al frente|

| | |
|---|---|
|**ℹ SEÑALES**|kill -9 (SIGKILL) fuerza la terminación sin que el proceso pueda limpiarse. kill -15 (SIGTERM) es más educado: pide al proceso que termine.|

# ⑧ Alias y variables de entorno

| |
|---|
|# Alias (atajos para comandos)<br><br>alias ll='ls -la'<br><br>alias update='sudo apt update && sudo apt upgrade -y'<br><br>unalias ll             # eliminar alias<br><br>alias                  # listar todos los alias activos<br><br># Para que persistan: añadir al fichero ~/.bashrc o ~/.zshrc<br><br># Variables de entorno<br><br>export MI_VAR='valor'  # crear variable de entorno<br><br>echo $MI_VAR           # usar variable<br><br>env                    # listar todas las variables de entorno<br><br>PATH=$PATH:/nueva/ruta # añadir ruta al PATH<br><br>echo $PATH             # ver rutas de búsqueda de ejecutables<br><br># Variables importantes:<br><br># $HOME  → directorio home del usuario<br><br># $USER  → nombre del usuario actual<br><br># $SHELL → shell en uso<br><br># $PWD   → directorio actual|

# ⑨ Historial y limpieza de rastros

| |
|---|
|history                # ver historial de comandos<br><br>history | grep nmap    # buscar en el historial<br><br>!42                    # re-ejecutar el comando número 42<br><br>!!                     # re-ejecutar el último comando<br><br>Ctrl+R                 # búsqueda reversa en el historial<br><br># Limpiar rastros:<br><br>history -c             # limpiar historial en memoria<br><br>cat /dev/null > ~/.bash_history   # vaciar fichero de historial<br><br>export HISTFILE=/dev/null         # deshabilitar historial en esta sesión|

| | |
|---|---|
|**⚠ FORENSE**|En una auditoría real, el historial se guarda en varios sitios (~/.bash_history, /var/log/auth.log...). Conocer dónde se almacena es clave tanto para atacar como para defender.|

---

## Enlaces relacionados

- [[comandos/Linux]] — Cheat sheet de comandos

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Bash Scripting.md|Bash Scripting]— Forense Digital, Kali Linux, Nmap
- [[../Apuntes/02 - Sistemas Operativos/Linux - Fundamentos.md|Linux - Fundamentos]— Escalada de Privilegios, Forense Digital, Linux
- [[Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]— Kali Linux, Linux, Nmap
- [[../Apuntes/02 - Sistemas Operativos/Linux - Bash Scripting.md|Linux - Bash Scripting]— Forense Digital, Linux, Nmap
- [[Bash y PowerShell.md|Bash y PowerShell]— Kali Linux, Linux, Nmap
- [[../apuntes evolve/BLOQUE 2.md|BLOQUE 2]— Escalada de Privilegios, Kali Linux, Linux

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

> #escalada-privilegios #forense #kali #linux #nmap
