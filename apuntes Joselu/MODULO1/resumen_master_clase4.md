> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 4**
> **Módulo:** MODULO1
> **Tema:** Clase 4
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 4. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Dinámica de clase y novedades del máster

Carlos López Pintado presenta dos novedades importantes para esta convocatoria:

**Plataforma de ejercicios interactiva** (exercises.academics.es): plataforma propia con ejercicios gamificados, leaderboard y sistema de puntos que premia la asistencia, participación en clase, ayuda en el foro y resolución de ejercicios. Los tres primeros clasificados al final del máster recibirán: - 1º puesto: **OSCP** (\~2 000 €) - 2º puesto: portátil **MSI Katana** (\~1 500 €) - 3º puesto: certificación **eCPPT v2** (complemento al eJPT incluido en el curso)

**Integración de IA en todos los módulos:** el máster incorpora IA en cada bloque técnico --- enumeración de subdominios, creación de herramientas, explotación automatizada, configuración de SIEM, normativa (SGSI) y desarrollo de comandos personalizados. El objetivo es formar perfiles que hagan el trabajo de cinco personas usando herramientas de IA.

## 2. Repaso de comandos y ejercicios

### Tabla resumen de comandos vistos en el ejercicio de clase

| Comando | Descripción |
|---|---|
| ls | Listar archivos del directorio actual ls -l | Listar en formato detallado (vertical) ls -a | Listar incluyendo archivos ocultos (los que empiezan por .) ls -la | Listar en formato detallado incluyendo ocultos ll | Alias de ls -l en algunos sistemas pwd | Mostrar el directorio actual cd .. | Subir al directorio padre cd \~ o cd | Ir al directorio home del usuario actual mkdir nombre | Crear un directorio touch fichero.txt | Crear un archivo vacío cat fichero.txt | Mostrar el contenido de un archivo echo \"texto\" \> fichero.txt | Redirigir la salida a un fichero (sobrescribe) echo \"texto\" \>\> fichero.txt | Añadir al final del fichero (no sobrescribe) cp origen.txt destino.txt | Copiar un fichero mv origen.txt destino.txt | Mover o renombrar un fichero rm fichero.txt | Borrar un fichero rm -r carpeta/ | Borrar una carpeta recursivamente grep \"texto\" fichero.txt | Buscar texto dentro de un fichero wc -l fichero.txt | Contar líneas de un fichero head -n 10 fichero.txt | Ver las primeras 10 líneas tail -n 5 fichero.txt | Ver las últimas 5 líneas chmod 755 fichero | Cambiar permisos de un fichero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Trampa del ejercicio:** en Windows el comando dir lista archivos en CMD, pero **PowerShell también acepta** ls, por lo que la respuesta correcta en el ejercicio era que Windows acepta ambos.

### Navegación avanzada con ..

| cd ../.. | # Sube dos niveles en la jerarquía cd ../../etc | # Sube dos niveles y entra en etc |
|---|---|---|

Cuando las rutas son muy largas, usar .. es más rápido que escribir la ruta absoluta completa. En sentido contrario, usar **Tab** para autocompletar siempre es más seguro que escribir la ruta completa (evita errores tipográficos que pueden hacer que un exploit no funcione).

**Conexión con hacking web --- Path Traversal:** La técnica ../../../etc/passwd en una URL es el equivalente web de los .. en la terminal: permite navegar hacia atrás en el árbol de directorios del servidor para acceder a ficheros a los que no se debería tener acceso.

### Editores de texto en terminal

| Editor | Estilo | Cómo guardar y salir |
|---|---|---|
| vi / vim | Old school; muy extendido | i para insertar, Esc para salir del modo inserción, :wq guardar y salir, :q! salir sin guardar nano | Moderno y sencillo | Ctrl+X para salir, confirmar guardado micro | Más moderno con colores | Instalación necesaria; interfaz intuitiva touch | No es editor | Solo crea el fichero vacío; no permite edición cat | No es editor | Solo muestra el contenido, no permite modificarlo |
|---|---|---|---|---|---|---|---|---|---|---|

### Redirección de salida

| echo "texto" > fichero.txt | # Sobrescribe el contenido existente echo "texto" >> fichero.txt | # Añade al final sin borrar lo anterior |
|---|---|---|

Uso práctico en auditorías: nmap -sV IP \> resultado.txt guarda el resultado del escaneo; después se le puede hacer grep \"open\" para filtrar solo los puertos abiertos.

### grep: uso avanzado

| grep "error" log.txt | # Busca la palabra error grep "don quijote" fichero.txt | # Expresiones con espacios: entre comillas dobles cat fichero.txt | grep "palabra" # Equivalente usando pipe |
|---|---|---|

Caso práctico: grep con comillas dobles es imprescindible cuando se busca una frase o cuando la cadena contiene caracteres especiales o espacios.

### Pipes y operadores de concatenación

| Operador | Nombre | Comportamiento |
|---|---|---|
| | | Pipe | La salida del primero es la entrada del segundo ; | Punto y coma | Ejecuta ambos comandos de forma independiente siempre && | AND | Ejecuta el segundo solo si el primero tuvo éxito |
|---|---|---|---|---|---|---|

**Analogía del pipe:** como las tuberías de Super Mario --- lo que entra por un lado sale por el otro.

**Conexión con hacking:** el punto y coma es exactamente la técnica de inyección de comandos. Si un formulario web lanza un find con el input del usuario sin sanitizarlo, meter ; reverse_shell ejecuta la reverse shell después del find.

## 3. La variable de entorno PATH

### ¿Qué es el PATH?

\$PATH es una **variable de entorno del sistema** (reconocible por el símbolo \$ delante) que contiene una lista de rutas separadas por :. Cuando se escribe un comando en la terminal, Linux busca el ejecutable de ese comando recorriendo estas rutas **de izquierda a derecha**, en orden de prioridad.

| echo $PATH | # Muestra las rutas del PATH actual |
|---|---|

Ejemplo de PATH típico en Kali:

/home/kali/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

### Rutas del PATH y sus ejecutables

Si se navega a cualquiera de estas rutas (ej. /usr/sbin) y se hace ls, se verán todos los comandos del sistema en color verde (ejecutables). Los comandos como ls, cat, grep, chmod... son simplemente pequeños programas almacenados en estas carpetas.

| cd /usr/sbin ls | # Todos en verde: son ejecutables del sistema |
|---|---|

### PATH Hijacking (secuestro del PATH)

> [!important] **Concepto clave:** dado que el PATH se lee de izquierda a derecha, si se coloca un ejecutable con el mismo nombre que un comando legítimo en una carpeta que aparece **antes** en el PATH, el sistema ejecutará el nuestro en lugar del legítimo.

**Ejemplo demostrativo:** 1. La carpeta /home/kali/.local/bin es la primera del PATH y está vacía por defecto. 2. Se crea un script llamado cat en esa carpeta que en vez de mostrar ficheros ejecuta un echo \"hola mundo\". 3. Ahora, cualquier uso de cat en cualquier lugar del sistema ejecutará el script falso.

**Aplicación ofensiva --- PATH Hijacking como técnica de escalada de privilegios:** Si existe un **cron job** (tarea programada) que se ejecuta como root y llama a un comando por su nombre relativo (sin ruta absoluta), y además hay una carpeta del PATH que el usuario actual puede escribir, se puede inyectar un ejecutable malicioso con ese mismo nombre. Cuando el cron job se ejecute, llamará al comando falso con privilegios de root, y el atacante obtiene una shell como root.

Esto se verá en profundidad en el módulo de escalada de privilegios.

**Relación con Vanguard (anti-cheat de League of Legends):** Riot Vanguard se instala a nivel de kernel y añade una entrada al PATH de Windows para poder ejecutarse desde el inicio del sistema. Tener acceso a nivel de kernel equivale a ser root: puede monitorizar todos los procesos, servicios y aplicaciones. Esto lo convierte en un vector de ataque muy peligroso si tiene vulnerabilidades (zero-days en Vanguard permitirían ejecutar código arbitrario en la máquina de cualquier jugador en partida).

## 4. Crear comandos personalizados (scripts Bash)

### Concepto

Un **comando** en Linux no es más que un pequeño programa almacenado en una carpeta del PATH. Se puede programar en C, Python, PHP o **Bash**. Para crear un comando personalizado:

| 1. | Crear un fichero de texto con el código Bash. 2. | Añadir el **shebang** #!/bin/bash en la primera línea (indica al sistema que es un script Bash ejecutable). 3. | Dar permisos de ejecución: chmod +x fichero o chmod 777 fichero. 4. | Mover el fichero a una carpeta del PATH con sudo mv fichero /usr/local/bin/nombre_comando. 5. | Invocar el comando desde cualquier lugar del sistema escribiendo su nombre. |
|---|---|---|---|---|---|

### El shebang #!/bin/bash

#!/bin/bash

```bash
echo "hola mundo"
```

Sin el shebang, el sistema trata el fichero como texto plano y lo muestra en pantalla en lugar de ejecutarlo. Con el shebang, file fichero muestra "Bourne-Again shell script" y el sistema lo ejecuta como programa.

### Parámetros en scripts Bash

Dentro del script, \$1 recibe el primer argumento, \$2 el segundo, etc.

#!/bin/bash

# fibonacci: muestra N números de la secuencia de Fibonacci

# Uso: fibonacci 15

Al llamar fibonacci 15, el \$1 dentro del script recibe el valor 15.

### Desarrollo de scripts con IA (Claude)

El profesor demuestra en directo cómo crear scripts complejos sin saber programar: 1. Se le pide a Claude en lenguaje natural: "*Hazme un script en Bash que reciba un número por parámetro y muestre esa cantidad de números de la secuencia de Fibonacci*". 2. Claude genera el código completo. 3. Se copia, se pega en un fichero con vi, se le da permisos y se mueve al PATH. 4. El comando funciona inmediatamente.

**Segundo ejemplo más complejo:** script que recopila el uso del sistema (procesos, memoria, servicios), lo muestra en formato JSON con una barra de progreso. Este tipo de script es la base de una herramienta de monitorización de equipos --- el profesor menciona haber comercializado una herramienta similar a clientes empresariales empezando de un script PowerShell.

**Comandos creados en clase:** - fibonacci N --- muestra los N primeros números de Fibonacci. - uso --- muestra el uso del sistema en formato JSON con barra de progreso. - cat personalizado con una imagen ASCII de gato (demostración de PATH hijacking; colapsó la Kali por un bucle infinito al llamar cat dentro del propio script).

### sudo !!

!! repite el último comando ejecutado. sudo !! ejecuta el último comando con privilegios de root, muy útil cuando un comando falla por permisos y se necesita repetirlo como administrador.

## 5. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| Cajut / Cáchit | **Quiz / ejercicio** --- prueba de preguntas en la plataforma de clase Leaderboard / Liverboard | **Leaderboard** -- tabla de clasificación OSCP | **OSCP** (*Offensive Security Certified Professional*) -- certificación premium de pentesting (\~2 000 €) WPT V2 / eCPPT | **eCPPTv2** (*eLearnSecurity Certified Professional Penetration Tester*) -- certificación intermedia ChainMod / changemod | **chmod** (*change mode*) -- comando para cambiar permisos de ficheros Make Deed / Makedir | **mkdir** (*make directory*) -- crear directorio Bone and gain shell | **Bourne-Again Shell (Bash)** -- lo que muestra file cuando detecta un script Bash shebang / hashtag exclamación barra bin bash | **Shebang** (#!/bin/bash) -- primera línea de un script que indica el intérprete pathhacking / path in checking | **PATH Hijacking** -- técnica de escalada de privilegios que sobreescribe un comando en el PATH cron job / tarea programada | **Cron job** -- tarea programada que se ejecuta automáticamente en intervalos definidos Vanguard (de Riot) | **Riot Vanguard** -- anti-cheat de League of Legends que opera a nivel de kernel Fibonacci | **Sucesión de Fibonacci** -- secuencia numérica donde cada número es la suma de los dos anteriores webhook a la escucha | **Webhook** -- endpoint HTTP que recibe datos enviados automáticamente por otro sistema formato JSON | **JSON** (*JavaScript Object Notation*) -- formato ligero de intercambio de datos parámetro \$1 | \$1 -- variable en Bash que recibe el primer argumento pasado al script sudo exclamación exclamación | sudo !! -- repite el último comando ejecutado con privilegios de root Byte Coding / Bike coding | **Vibe Coding** -- programación asistida por IA en lenguaje natural sin necesidad de saber programar MSI Katana | **MSI Katana** -- portátil gaming de gama media (\~1 500 €) Softtonic | **Softonic** -- plataforma de descarga de software de terceros (potencialmente peligrosa) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.