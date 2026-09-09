# ① Repaso: operadores de redirección

La redirección controla a dónde van la entrada y salida de los comandos. Fundamental para guardar resultados y encadenar herramientas.

|**Operador**|**Función**|**Ejemplo**|
|---|---|---|
|>|Redirigir stdout a fichero (sobreescribe)|nmap -sV IP > resultados.txt|
|>>|Redirigir stdout añadiendo al final|echo 'nuevo' >> fichero.txt|
|<|Usar fichero como stdin|sort < lista.txt|
|2>|Redirigir stderr (errores)|find / -name x 2> /dev/null|
|2>&1|Mezclar stderr con stdout|cmd > todo.txt 2>&1|
|||Pipe: stdout → stdin del siguiente|cat /etc/passwd | grep bash|
|||OR lógico: ejecutar si el anterior falla|cmd1 | cmd2|
|&&|AND lógico: ejecutar si el anterior tuvo éxito|apt update && apt upgrade|
|;|Ejecutar en secuencia independiente|cmd1; cmd2; cmd3|

| | |
|---|---|
|**💡 /dev/null**|/dev/null es un 'agujero negro': todo lo que se redirija aquí desaparece. Útil para suprimir mensajes de error que no interesan.|

# ② Operadores lógicos en la práctica

| |
|---|
|# AND (&&) — ejecutar solo si el anterior tiene éxito:<br><br>mkdir proyecto && cd proyecto && touch README.md<br><br>nmap -sV 192.168.1.1 && echo 'Scan completado'<br><br># OR (|) — ejecutar solo si el anterior falla:<br><br>ping -c1 8.8.8.8 | echo 'Sin conectividad'<br><br>cat fichero.txt | echo 'Fichero no existe'<br><br># Punto y coma (;) — siempre ejecuta ambos:<br><br>echo 'inicio'; whoami; id; uname -a<br><br># Encadenamiento típico en pentesting:<br><br>nmap -p- IP 2>/dev/null | grep open | tee puertos.txt && echo 'Done'|

# ③ grep — Búsqueda de patrones

| |
|---|
|grep 'patrón' fichero.txt          # búsqueda básica<br><br>grep -i 'patrón' fichero.txt       # ignorar mayúsculas<br><br>grep -r 'patrón' /directorio/      # recursivo<br><br>grep -v 'patrón' fichero.txt       # líneas que NO contienen<br><br>grep -n 'patrón' fichero.txt       # mostrar número de línea<br><br>grep -c 'patrón' fichero.txt       # contar coincidencias<br><br>grep -o 'patrón' fichero.txt       # mostrar solo la parte que coincide<br><br>grep -E 'pat1|pat2' fichero.txt    # regex extendida (OR)<br><br>grep -A3 'patrón' fichero.txt      # 3 líneas después de la coincidencia<br><br>grep -B3 'patrón' fichero.txt      # 3 líneas antes<br><br># Ejemplos en pentesting:<br><br>grep 'open' nmap_result.txt        # filtrar puertos abiertos<br><br>grep -r 'password' /var/www/       # buscar passwords en código fuente<br><br>cat /etc/passwd | grep '/bin/bash' # usuarios con bash|

# ④ find — Búsqueda de ficheros

| |
|---|
|find / -name 'fichero.txt'          # buscar por nombre<br><br>find / -name '*.conf'               # todos los .conf<br><br>find / -name '*.conf' -type f       # solo ficheros (no dirs)<br><br>find /home -user kali               # ficheros de un usuario<br><br>find / -perm -4000 2>/dev/null      # ficheros con SUID ← escalada de privs<br><br>find / -perm -2000 2>/dev/null      # ficheros con SGID<br><br>find / -writable -type f 2>/dev/null# ficheros escribibles<br><br>find / -mtime -7                    # modificados en los últimos 7 días<br><br>find . -size +10M                   # ficheros mayores de 10 MB<br><br># Con acción:<br><br>find /tmp -name '*.tmp' -delete     # borrar temporales<br><br>find . -name '*.py' -exec cat {} \; # ejecutar cat en cada .py|

| | |
|---|---|
|**🔐 SUID**|find / -perm -4000 2>/dev/null es uno de los primeros comandos tras comprometer un equipo. Los ficheros SUID con propietario root son vectores clásicos de escalada.|

# ⑤ Comandos de texto y procesamiento

| |
|---|
|# sort — ordenar líneas:<br><br>sort fichero.txt                   # orden alfabético<br><br>sort -n fichero.txt                # orden numérico<br><br>sort -r fichero.txt                # orden inverso<br><br>sort -k2 fichero.txt               # ordenar por columna 2<br><br>sort -u fichero.txt                # eliminar duplicados al ordenar<br><br># uniq — eliminar duplicados (requiere input ordenado):<br><br>sort passwords.txt | uniq<br><br>sort passwords.txt | uniq -c       # contar repeticiones<br><br># cut — extraer columnas:<br><br>cut -d: -f1 /etc/passwd            # primer campo del /etc/passwd<br><br>cut -d',' -f2,4 datos.csv          # columnas 2 y 4 de CSV<br><br># awk — procesado más potente:<br><br>awk '{print $1}' fichero.txt       # primera columna<br><br>awk -F: '{print $1,$3}' /etc/passwd# usuario y UID<br><br># wc — contar:<br><br>wc -l fichero.txt                  # contar líneas<br><br>wc -w fichero.txt                  # contar palabras|

# ⑥ echo y creación de ficheros

| |
|---|
|# echo — imprimir texto:<br><br>echo 'Hola Mundo'<br><br>echo $USER                         # variable de entorno<br><br>echo -e 'línea1\nlínea2'           # interpretar \n<br><br># Crear ficheros con echo:<br><br>echo 'contenido' > fichero.txt     # crear/sobreescribir<br><br>echo 'más contenido' >> fichero.txt# añadir al final<br><br># Simular chat (demostración):<br><br>echo 'Hola' > chat.txt<br><br>echo 'Adiós' >> chat.txt           # añade sin borrar lo anterior<br><br>cat chat.txt                       # muestra ambas líneas<br><br># Heredoc — texto multilínea:<br><br>cat << EOF > script.sh<br><br>#!/bin/bash<br><br>echo 'Mi script'<br><br>EOF|

# ⑦ Plataforma de ejercicios: flujo de trabajo

El máster utiliza una plataforma de ejercicios (**ejercicios.academy**) donde se practican los comandos vistos. Flujo recomendado:

| | | | | | | |
|---|---|---|---|---|---|---|
|**Leer el enunciado**|->|**Probar en terminal Kali**|->|**Verificar solución**|->|**Anotar en apuntes**|

| |
|---|
|# Consejos para los ejercicios:<br><br># 1. La 'ls' básica vs 'ls -la':<br><br>ls             # lista simple (solo nombres)<br><br>ls -l          # lista larga (permisos, tamaño, fecha)<br><br>ls -la         # incluye ficheros ocultos (empiezan por .)<br><br>ls -lh         # tamaños legibles (KB, MB, GB)<br><br># 2. El flag -e en rm es peligroso:<br><br>rm -rf directorio/   # borra recursivamente sin confirmación<br><br># NUNCA: rm -rf /   o   rm -rf /*|

| | |
|---|---|
|**💡 CONSEJO**|La práctica supera a la memorización. Usa la plataforma de ejercicios todos los días aunque sean 15 minutos. Los comandos se interiorizan con el uso, no leyendo.|

# ⑧ Comandos de red en Bash

| |
|---|
|ip a                    # ver interfaces de red (moderno)<br><br>ifconfig                # ver interfaces (legacy, aún disponible en Kali)<br><br>ip route                # tabla de rutas<br><br>ss -tulnp               # puertos abiertos y procesos (moderno)<br><br>netstat -tulnp          # igual pero legacy<br><br>ping -c4 8.8.8.8        # test de conectividad<br><br>curl ifconfig.me        # ver IP pública<br><br>wget URL                # descargar fichero<br><br>curl -s URL             # petición HTTP silenciosa<br><br># Netcat — navaja suiza de red:<br><br>nc -lvnp 4444           # escuchar en puerto 4444<br><br>nc IP 4444              # conectar a IP:4444<br><br>nc -z IP 80             # comprobar si puerto está abierto|



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Bash Comandos Avanzados.md|Bash Comandos Avanzados]] — Linux, Nmap, Windows
- [[../informes/Informe_Nike.md|Informe_Nike]] — Linux, Nmap, Windows
- [[../apuntes Andres/10.06.2026 HTB Starting Point 2 Repaso.md|10.06.2026 HTB Starting Point 2 Repaso]] — Linux, Nmap, Windows
- [[../write-ups/Nike-THL.md|Nike-THL]] — Linux, Nmap, Windows
- [[../apuntes Andres/01.09.2026 Repaso General I.md|01.09.2026 Repaso General I]] — Linux, Nmap, Windows
- [[../apuntes Andres/02.09.2026 Repaso General II.md|02.09.2026 Repaso General II]] — Linux, Nmap, Windows

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]

> #kali #linux #metasploit #netcat #nmap #redes #reverse-shell #windows
