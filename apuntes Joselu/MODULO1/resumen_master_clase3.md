> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 3**
> **Módulo:** MODULO1
> **Tema:** Clase 3
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 3. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Dinámica del máster y filosofía de aprendizaje

El profesor (tercer instructor del máster) abre la sesión con una reflexión clave sobre cómo sacar el máximo partido al aprendizaje:

- No se trata de aprender Linux por sí mismo, sino de entender **cómo aplica cada comando a la ciberseguridad ofensiva**.
- Para los alumnos más avanzados: a cada nuevo comando, darle la vuelta y pensar --- ¿cómo puedo usar esto para hackear? ¿Y para defenderme?
- Para los que empiezan: preguntar sin miedo, intentar las cosas, equivocarse y volver a intentarlo.
- Herramienta de estudio recomendada: **XMind** (mapas mentales para estructurar el aprendizaje).
- Recurso útil: usar IAs (Claude, ChatGPT) para resolver dudas entre sesiones y explorar aplicaciones ofensivas de los comandos.

**Concepto del máster:** "**idea feliz**" --- en hacking, a veces hay que imaginar posibilidades que parecen absurdas y probarlas. Muchos ataques parecen "idea feliz" hasta que funcionan.

## 2. Repaso de comandos anteriores con enfoque ofensivo

### history --- el historial de comandos

- Muestra todos los comandos ejecutados en la sesión con su número de orden.

- **Enfoque forense:** un atacante que no borra su historial deja un rastro completo de todo lo que hizo en el sistema.

 - Caso real mencionado: un conocido hacker español dejó su historial sin borrar y eso permitió reconstruir toda su actividad.

- **Enfoque ofensivo:** al comprometer una máquina, revisar el history puede revelar credenciales, rutas, conexiones SSH y comandos con contraseñas en texto claro escritos directamente en la terminal.

- La "capa 8" del modelo OSI es la **capa humana**: el 90% de las brechas vienen del error humano.

- Borrar el historial:

 - history -c o bash -c \"history -p\" borra la sesión actual.
 - Redirigir el historial a /dev/null hace que nunca se almacene.
 - Archivo donde se guarda: .bash_history o .zsh_history en el home del usuario.

### uname -a --- enfoque ofensivo

- Al comprometer una máquina, lo más importante de uname -a es la **versión del kernel** y la **arquitectura**.
- Diferentes exploits de escalada de privilegios funcionan solo en ciertas arquitecturas (32/64 bits) y versiones de kernel.
- Hay exploits que funcionan en x86 pero no en x64 y viceversa.

### gunzip / unzip --- descomprimir archivos

| sudo gunzip /usr/share/wordlists/rockyou.txt.gz | # Descomprime el diccionario RockYou |
|---|---|

- El diccionario **rockyou.txt** viene comprimido en Kali Linux.
- Requiere sudo porque la ruta /usr/share/wordlists/ pertenece a root.

## 3. El comando find --- búsqueda avanzada de ficheros

### Estructura básica

find [desde_dónde] [filtros] [acciones]

| Elemento | Descripción |
|---|---|
| desde_dónde | Ruta a partir de la cual buscar. / para todo el sistema, . para el directorio actual, /home/kali para el home filtros | Criterios de búsqueda: nombre, tipo, tamaño, fecha, permisos acciones | Qué hacer con los resultados: mostrar, borrar, ejecutar otro comando |
|---|---|---|---|

### Filtros más importantes

| Filtro | Ejemplo | Descripción |
|---|---|---|
 -name find / -name \"\*.txt\" Busca por nombre (case sensitive)
 -name con comodín find / -name \".\*\" Busca archivos ocultos (punto al inicio)
 -type f find / -type f Solo ficheros
 -type d find / -type d Solo directorios
 -size +10M find / -size +10M Archivos de más de 10 MB
 -mtime -7 find . -mtime -7 Modificados en los últimos 7 días
 -perm u+x find . -perm u+x Archivos que el usuario puede ejecutar
 -name \"user.txt\" find / -name \"user.txt\" 2\>/dev/null Busca la flag de Hack The Box

### Acciones con find

| find /home/kali -name "*.tmp" -delete | # Borra todos los .tmp encontrados find / -name "archivo" 2>/dev/null | # Suprime errores de permiso |
|---|---|---|

### Usos ofensivos del find

- **Buscar credenciales:** find / -name \"\*.txt\" 2\>/dev/null puede revelar archivos con contraseñas dejados por desarrolladores.
- **Buscar logs:** find / -name \"\*.log\" 2\>/dev/null para forense o post-explotación.
- **Buscar flags en CTF:** las flags en Hack The Box suelen estar en /root/root.txt o /home/user/user.txt; si no están en la ruta habitual, find / -name \"user.txt\" las localiza.
- **Buscar archivos ejecutables con permisos especiales (SUID):** técnica avanzada de escalada de privilegios que se verá más adelante.
- **Borrar rastros:** find / -name \"mi_archivo_malicioso\" -delete elimina un archivo sin saber exactamente dónde está.

### find y Linux/Windows: case sensitivity

- Linux es **case sensitive**: find / -name \"Antonio\" ≠ find / -name \"antonio\".
- Windows es **case insensitive**: da igual mayúsculas y minúsculas.
- Aplicación web para detectar el SO del servidor: cambiar una letra a mayúscula en la URL. Si carga, es Windows; si da error, es Linux.

### Herramienta relacionada: file

| file nombre_archivo | # Detecta el tipo real del archivo por sus magic bytes |
|---|---|

> [!important] Recuerda: en Linux las extensiones no tienen significado para el sistema. El tipo real de un archivo se determina por sus **magic bytes** (primeros bytes del fichero en binario).

## 4. Pipes, redirecciones y operadores

### El pipe \| --- encadenar comandos

La salida (*output*) de un comando se convierte en la entrada (*input*) del siguiente.

| history | head -10 | # Los 10 últimos comandos del historial cat rockyou.txt | head -10 | # Las 10 primeras contraseñas del diccionario find / -name "*.txt" | head -5 # Los 5 primeros .txt encontrados du -h | sort -rh | head -10 | # Las 10 carpetas que más espacio ocupan |
|---|---|---|---|

**Aplicación ofensiva:** encadenar find, grep, sort, uniq, head, wc permite procesar grandes volúmenes de datos de una máquina comprometida en una sola línea.

### Redirección 2\>/dev/null

- 2\> redirige el **stderr** (descriptor de error, número 2).
- /dev/null es el "agujero negro" de Linux: todo lo que se redirige ahí desaparece.
- Uso práctico: eliminar los mensajes "Permission denied" al hacer búsquedas con find en rutas a las que no se tiene acceso.

<!-- -->

| find / -name "*.conf" 2>/dev/null | # Solo muestra resultados, no errores |
|---|---|

### Operadores lógicos

| Operador | Nombre | Comportamiento |
|---|---|---|
| && | AND (doble ampersand) | El segundo comando se ejecuta **solo si el primero tuvo éxito** (salida 0) \\\|\\\| | OR (doble pipe) | El segundo comando se ejecuta **solo si el primero falló** (salida distinta de 0) ; | Punto y coma (secuencia) | Ambos comandos se ejecutan **siempre**, independientemente del resultado del primero |
|---|---|---|---|---|---|---|

| mkdir dist && cp *.txt dist/ | # Crea el directorio y copia solo si mkdir tuvo éxito cat root.txt || find / -name "root.txt" | # Si cat falla, ejecuta find comando1 ; comando2 | # Ejecuta ambos siempre |
|---|---|---|---|

**Uso en scripting:** los operadores lógicos son la base de los *one-liners* y scripts Bash automatizados.

### Ampersand simple & --- ejecutar en segundo plano

| python3 -m http.server 8080 & | # Levanta un servidor HTTP en segundo plano |
|---|---|

- Sin &, el proceso ocupa la terminal y no se puede escribir nada más.
- Con &, el proceso se manda al fondo y se asigna un número de proceso (PID).
- Para matarlo: kill %1 (mata el último proceso en segundo plano) o kill -9 \<PID\>.
- Para ver todos los procesos activos: ps aux.

## 5. Primer vistazo a la inyección de comandos

Este es el punto más avanzado de la sesión: cómo los comandos de Bash que se están aprendiendo son exactamente los mismos que se explotan en ataques reales.

### El escenario

Una aplicación web tiene un formulario de búsqueda de archivos. Por detrás, el servidor ejecuta algo como:

find /home/castillo -name "TEXTO_INTRODUCIDO_POR_EL_USUARIO"

### El ataque con punto y coma

Si el desarrollador no sanitiza la entrada, el usuario puede inyectar comandos adicionales usando el operador ; (secuencia):

hola.txt ; id

El servidor ejecutaría:

find /home/castillo -name "hola.txt" ; id

Resultado: el servidor ejecuta id y devuelve el usuario con el que corre el proceso web. Esto es una **inyección de comandos (Command Injection)**, que puede llevar a una RCE completa.

### La defensa: comillas dobles

Si el desarrollador envuelve la entrada del usuario en comillas dobles:

find /home/castillo -name "$INPUT"

El punto y coma dentro de las comillas se interpreta como texto literal, no como operador, bloqueando la inyección.

### Conexión con SQL Injection

El mecanismo es análogo a la **SQL Injection**: se altera el flujo de ejecución de un programa introduciendo caracteres especiales con significado propio en el lenguaje subyacente (en SQL son \', \", \--, ;; en Bash son ;, &&, \|, etc.).

### LinPEAS y WinPEAS

Se mencionan por primera vez las herramientas de escalada de privilegios automática: - **LinPEAS** (Linux Privilege Escalation Awesome Script) --- autor español: Carlos Polop. - **WinPEAS** --- equivalente para Windows. - Lanzan automáticamente decenas de comandos find, uname, comprobaciones de permisos, etc., y colorean los resultados según su criticidad. - Se estudiarán en profundidad cuando llegue la fase de escalada de privilegios.

## 6. Próximos temas

- Continuación con **Bash scripting**: variables, condicionales, bucles, funciones.
- **Variables de entorno** y su explotación en escalada de privilegios.
- **Alias** y funciones personalizadas.
- **PowerShell** (terminal de Windows).
- Primera máquina virtual vulnerable: **Metasploitable**.
- Primer hackeo real en laboratorio.

## 7. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| Xmine / X-Mine | **XMind** -- herramienta de mapas mentales Hubbox / HUB de Box | **Hack The Box (HTB)** -- plataforma de práctica de pentesting world list / world list rock you | **wordlist / rockyou.txt** -- diccionario de contraseñas Wunzip / Wunzit / Gunzit | **gunzip** -- comando para descomprimir archivos .gz heat | **head** -- comando que muestra las primeras N líneas de un fichero unique -c | **uniq -c** -- comando que cuenta ocurrencias únicas de líneas caché de Firefox y GUFS | Referencias a **caché del navegador** y metadatos del sistema de ficheros ampersand / ampersan | **Ampersand (**&**)** -- carácter &; doble ampersand: && (operador AND) doble pipe / pi | **Double pipe (**\\\|\\\|**)** -- operador OR en Bash punto y coma | **Semicolon (**;**)** -- operador de secuencia en Bash Limpiz / Winpiz | **LinPEAS / WinPEAS** -- scripts de enumeración para escalada de privilegios Carlos Polo | **Carlos Polop** -- autor de LinPEAS/WinPEAS IDE / id | id -- comando Linux que muestra el usuario y grupos actuales PSAux | ps aux -- lista todos los procesos activos del sistema kill guión 9 | kill -9 \<PID\> -- fuerza el cierre de un proceso por su PID python3 -m http server | python3 -m http.server 8080 -- levanta un servidor HTTP simple en Python magic bytes / bytes mágicos | **Magic bytes** -- primeros bytes de un fichero que identifican su tipo real en Linux caso sensitivo / case insensitive | **Case sensitive** (Linux) vs. **case insensitive** (Windows) mtime / mtime 7 | -mtime -7 -- flag de find para archivos modificados en los últimos N días perm u+x | -perm u+x -- flag de find para archivos ejecutables por el propietario SQL Y / SQL Inyección | **SQL Injection (SQLi)** -- inyección de código en consultas SQL Metasploitable | **Metasploitable** -- máquina virtual vulnerable para práctica de pentesting Bike Coding | **Vibe Coding** -- programación asistida por IA con lenguaje natural Notebook LME | **NotebookLM** -- herramienta de Google para análisis y resumen de documentos con IA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.