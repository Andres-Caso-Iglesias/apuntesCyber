# ① ¿Qué es un script de Bash?

Un script es un fichero de texto con comandos Bash que se ejecutan secuencialmente. Permite automatizar tareas repetitivas.

| |
|---|
|#!/bin/bash<br><br># La primera línea es el 'shebang': indica qué intérprete usar<br><br># Crear y ejecutar un script:<br><br>nano mi_script.sh          # crear el fichero<br><br>chmod +x mi_script.sh      # dar permiso de ejecución<br><br>./mi_script.sh             # ejecutar<br><br>bash mi_script.sh          # ejecutar sin dar permiso x|

| | |
|---|---|
|**💡 SHEBANG**|El #!/bin/bash al inicio es obligatorio para que el sistema sepa que es un script Bash. Sin él, puede interpretarse con sh (shell básica) con diferencias de sintaxis.|

# ② Variables

| |
|---|
|#!/bin/bash<br><br># Asignar variables (sin espacios alrededor del =):<br><br>nombre='Kali'<br><br>ip='192.168.1.1'<br><br>contador=0<br><br># Usar variables (con $):<br><br>echo "Hola $nombre"<br><br>echo "Escaneando: $ip"<br><br># Variables especiales:<br><br>$0    # nombre del script<br><br>$1    # primer argumento<br><br>$2    # segundo argumento<br><br>$#    # número de argumentos<br><br>$@    # todos los argumentos<br><br>$?    # código de retorno del último comando (0=éxito)<br><br>$$    # PID del script actual<br><br># Capturar salida de un comando:<br><br>fecha=$(date)<br><br>usuarios=$(cat /etc/passwd | grep bash | cut -d: -f1)<br><br>echo "Fecha: $fecha"|

| | |
|---|---|
|**⚠ ESPACIOS**|nombre='valor' ← correcto. nombre = 'valor' ← error. Bash es sensible a los espacios en las asignaciones.|

# ③ Entrada de usuario y argumentos

| |
|---|
|#!/bin/bash<br><br># Leer input interactivo:<br><br>echo -n 'Introduce la IP objetivo: '<br><br>read ip_objetivo<br><br>echo "Escaneando $ip_objetivo..."<br><br># Leer con prompt integrado:<br><br>read -p 'Usuario: ' usuario<br><br>read -sp 'Contraseña: ' password   # -s = silencioso (no muestra lo escrito)<br><br>echo<br><br># Argumentos desde línea de comandos:<br><br># ./script.sh 192.168.1.1 80<br><br>ip=$1<br><br>puerto=$2<br><br># Verificar que se pasaron argumentos:<br><br>if [ $# -lt 2 ]; then<br><br>    echo 'Uso: $0 <ip> <puerto>'<br><br>    exit 1<br><br>fi|

# ④ Condicionales (if/elif/else)

| |
|---|
|#!/bin/bash<br><br># Sintaxis básica:<br><br>if [ condición ]; then<br><br>    # comandos si es verdad<br><br>elif [ otra_condición ]; then<br><br>    # comandos si la segunda es verdad<br><br>else<br><br>    # si ninguna es verdad<br><br>fi<br><br># Comparaciones numéricas:<br><br># -eq   igual           [ $a -eq $b ]<br><br># -ne   no igual        [ $a -ne $b ]<br><br># -lt   menor que       [ $a -lt $b ]<br><br># -gt   mayor que       [ $a -gt $b ]<br><br># -le   menor o igual   [ $a -le $b ]<br><br># -ge   mayor o igual   [ $a -ge $b ]<br><br># Comparaciones de strings:<br><br># =     igual           [ "$a" = "$b" ]<br><br># !=    no igual        [ "$a" != "$b" ]<br><br># -z    vacío           [ -z "$var" ]<br><br># -n    no vacío        [ -n "$var" ]<br><br># Ficheros:<br><br># -f    existe y es fichero     [ -f fichero.txt ]<br><br># -d    existe y es directorio  [ -d /ruta ]<br><br># -x    es ejecutable           [ -x script.sh ]<br><br># -r    es legible              [ -r fichero ]<br><br># Ejemplo real:<br><br>if ping -c1 -W1 $ip &>/dev/null; then<br><br>    echo "$ip está activo"<br><br>else<br><br>    echo "$ip no responde"<br><br>fi|

# ⑤ Bucles

| |
|---|
|# FOR — iterar sobre lista:<br><br>for ip in 192.168.1.1 192.168.1.2 192.168.1.3; do<br><br>    echo "Probando $ip"<br><br>done<br><br># FOR con rango (secuencia):<br><br>for i in $(seq 1 254); do<br><br>    ping -c1 -W1 192.168.1.$i &>/dev/null && echo "192.168.1.$i activo"<br><br>done<br><br># FOR sobre fichero:<br><br>for linea in $(cat hosts.txt); do<br><br>    nmap -p 80,443 $linea<br><br>done<br><br># WHILE — mientras condición sea verdad:<br><br>contador=1<br><br>while [ $contador -le 10 ]; do<br><br>    echo "Intento $contador"<br><br>    contador=$((contador + 1))<br><br>done<br><br># WHILE para leer líneas de un fichero:<br><br>while read linea; do<br><br>    echo "Procesando: $linea"<br><br>done < lista.txt|

| | |
|---|---|
|**💡 AUTOMATIZACIÓN**|El bucle for con ping sobre el rango /24 es la base de un escáner de hosts casero. Mucho más lento que nmap pero útil para entender cómo funcionan.|

# ⑥ Funciones

| |
|---|
|#!/bin/bash<br><br># Definir función:<br><br>función_saludar() {<br><br>    local nombre=$1     # 'local' limita la variable a la función<br><br>    echo "Hola, $nombre!"<br><br>}<br><br># Llamar función:<br><br>función_saludar 'Chema'<br><br>función_saludar 'Carlos'<br><br># Función con retorno:<br><br>esta_activo() {<br><br>    ping -c1 -W1 $1 &>/dev/null<br><br>    return $?   # 0=éxito, 1=fallo<br><br>}<br><br>if esta_activo '192.168.1.1'; then<br><br>    echo 'Host activo'<br><br>fi<br><br># Función de banner para scripts:<br><br>banner() {<br><br>    echo '================================='<br><br>    echo " $1"<br><br>    echo '================================='<br><br>}<br><br>banner 'Scanner de puertos v1.0'|

# ⑦ Script completo: mini scanner de hosts

| |
|---|
|#!/bin/bash<br><br># Host scanner para red /24<br><br># Uso: ./hostscan.sh 192.168.1<br><br>RED=$1<br><br>ACTIVOS=()    # array para guardar resultados<br><br>if [ -z "$RED" ]; then<br><br>    echo "Uso: $0 <prefijo_red>  (ej: 192.168.1)"<br><br>    exit 1<br><br>fi<br><br>echo "[*] Escaneando $RED.0/24..."<br><br>for i in $(seq 1 254); do<br><br>    ip="$RED.$i"<br><br>    if ping -c1 -W1 $ip &>/dev/null; then<br><br>        echo "[+] $ip — ACTIVO"<br><br>        ACTIVOS+=("$ip")<br><br>    fi<br><br>done<br><br>echo ""<br><br>echo "[*] Hosts activos encontrados: ${#ACTIVOS[@]}"<br><br>for host in "${ACTIVOS[@]}"; do<br><br>    echo "    → $host"<br><br>done|

# ⑧ Limpieza de rastros y forense

| |
|---|
|# El historial registra todos los comandos en:<br><br>~/.bash_history<br><br>/var/log/auth.log    # intentos de login<br><br>/var/log/syslog      # log del sistema<br><br>/var/log/apache2/    # logs de Apache<br><br># Como atacante, limpiar rastros:<br><br>history -c && history -w       # borrar historial en memoria y disco<br><br>export HISTFILE=/dev/null      # deshabilitar historial esta sesión<br><br>shred -u ~/.bash_history       # borrado seguro<br><br># Como defensor (forense), buscar rastros:<br><br>cat ~/.bash_history<br><br>last                           # últimos logins<br><br>lastb                          # intentos fallidos de login<br><br>who                            # usuarios conectados ahora<br><br>w                              # qué están haciendo|

| | |
|---|---|
|**🔐 FORENSE**|Eliminar todos los rastros es más complejo de lo que parece: hay múltiples ficheros de log en diferentes rutas. Como defensor, los logs deben enviarse a un SIEM remoto para que el atacante no pueda borrarlos.|

---

## Enlaces relacionados

- [[comandos/Linux]] — Comandos de referencia