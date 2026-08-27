> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 2**
> **Módulo:** MODULO1
> **Tema:** Clase 2
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 2. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Introducción y objetivos de la sesión

Esta sesión la imparte un segundo profesor (Yuba), distinto a Carlos. Los objetivos del día son:

- Consolidar los conceptos de terminal vistos en la clase anterior.
- Ampliar el catálogo de comandos Bash: navegación, creación, eliminación, copia, movimiento, lectura de ficheros e información del sistema.
- Entender los conceptos de **pipe**, **ruta absoluta vs. relativa**, **recursividad** y **variables de entorno**.
- Introducir el concepto de **alias** y funciones personalizadas en Bash.
- Primera práctica guiada en la terminal.
- Herramienta de estudio: **XMind** (mapas mentales para estructurar el aprendizaje).

**Filosofía de aprendizaje transmitida:** - Entender antes que memorizar y copiar-pegar. - Técnica recomendada: explicar el concepto en voz alta a un objeto inanimado (técnica del punto). - Proceso en tres fases: ver → replicar → hacerlo solo sin ayuda. - Las mismas bases del sistema de ficheros y la recursividad aparecerán una y otra vez a lo largo del máster (escalada de privilegios, pivoting, enumeración...).

## 2. Terminal vs. Shell: diferencia conceptual

Un error muy habitual es usar "terminal" y "shell" como sinónimos. No lo son:

- **Terminal:** el programa que muestra la ventana negra donde escribimos. Ejemplos: GNOME Terminal (Linux), Terminal.app / iTerm2 (macOS), Windows Terminal (Windows).
- **Shell:** el intérprete que corre *dentro* de la terminal, lee los comandos, los analiza y los ejecuta. Ejemplos: **Bash**, **Zsh**, **PowerShell**, **CMD**.

Bash y PowerShell son dos shells distintas que pueden abrirse dentro del mismo programa Windows Terminal.

## 3. ¿Qué es Bash?

**Bash** (*Bourne Again Shell*) es el intérprete de comandos presente en la gran mayoría de distribuciones Linux (Debian, Ubuntu, Kali...) y fue también el shell por defecto de macOS hasta la versión Catalina (2019), cuando fue sustituido por **Zsh** (sintaxis prácticamente idéntica).

**Características principales:** - Orientado a texto: todo lo que fluye por la terminal son cadenas de caracteres. - Permite encadenar comandos con **pipes** (|): la salida de un comando se convierte en la entrada del siguiente. - Soporta **scripting** completo: variables, condicionales (if/else), bucles y funciones. - Permite definir **alias** y funciones personalizadas para simplificar comandos complejos. - Los archivos .bashrc y .bash_profile permiten hacer persistentes los alias y las configuraciones entre sesiones.

**Cómo abrirlo:** - Ubuntu/Debian/Kali: Ctrl + Alt + T - macOS: Cmd + Espacio → escribir "Terminal" - Windows: mediante **WSL2** (Windows Subsystem for Linux), instalable desde la Microsoft Store.

## 4. Estructura de un comando en Bash

Todo comando en Bash sigue la misma estructura:

comando [opciones] [argumento1] [argumento2]

- **Opciones cortas:** un guion + letra. Ej.: ls -l, ls -a. Se pueden combinar: ls -la equivale a ls -l -a.
- **Opciones largas:** dos guiones + palabra. Ej.: \--help, \--verbose. Son más legibles pero no se pueden combinar.
- Para ver todas las opciones de un comando: comando \--help o man comando.

## 5. Comandos de navegación y sistema de ficheros

### Moverse por el sistema

| Comando | Descripción |
|---|---|
| pwd | Muestra la ruta actual (*Print Working Directory*) cd directorio | Cambia al directorio indicado cd .. | Sube un nivel al directorio padre cd ../otro | Sube un nivel y entra en otro directorio cd - | Vuelve al directorio anterior (el último visitado) cd \~ | Va al directorio home del usuario actual |
|---|---|---|---|---|---|---|

**Ruta absoluta vs. ruta relativa:** la ruta absoluta parte siempre desde la raíz del sistema (/home/kali/documentos); la ruta relativa parte desde donde estás en ese momento (./documentos o simplemente documentos). Esta distinción es clave en escalada de privilegios: hay técnicas que explotan la diferencia entre cómo Linux busca binarios con ruta relativa y con ruta absoluta.

### Listar contenido

| Comando | Descripción |
|---|---|
| ls | Lista el contenido del directorio actual ls -l | Lista con información detallada (permisos, tamaño, fecha) ls -la | Lista todo incluyendo archivos ocultos ls -la -d .\* | Lista solo los archivos ocultos (los que empiezan por .) ls -laR | Lista recursivamente todos los subdirectorios |
|---|---|---|---|---|---|

**Colores en el listado:** - Azul: directorio. - Blanco: fichero estándar. - Verde: fichero ejecutable.

### Crear directorios y ficheros

| Comando | Descripción |
|---|---|
| mkdir nombre | Crea un directorio mkdir -p a/b/c | Crea una jerarquía completa de directorios (flag -p) touch fichero.txt | Crea un fichero vacío (o actualiza su timestamp si ya existe) |
|---|---|---|---|

### Eliminar

| Comando | Descripción |
|---|---|
| rm fichero.txt | Elimina un fichero rm -r carpeta/ | Elimina una carpeta recursivamente rm -rf carpeta/ | Elimina recursivamente **y sin confirmación** rmdir carpeta/ | Elimina una carpeta vacía |
|---|---|---|---|---|

⚠️ **Advertencia crítica:** rm -rf / elimina todo el sistema de archivos del sistema operativo sin posibilidad de recuperación. Nunca ejecutar contra una ruta que empiece por /.

### Copiar y mover/renombrar

| Comando | Descripción |
|---|---|
| cp origen.txt destino.txt | Copia un fichero cp -r carpeta/ destino/ | Copia una carpeta con todo su contenido (recursivo) mv origen.txt destino.txt | Mueve un fichero a otra ruta mv nombre.txt nuevonombre.txt | Renombra un fichero (mismo directorio, distinto nombre) |
|---|---|---|---|---|

Punto . como destino significa "el directorio actual": cp /ruta/fichero.txt . copia el fichero al directorio donde estás.

## 6. Leer ficheros

| Comando | Descripción |
|---|---|
| cat fichero.txt | Muestra todo el contenido de golpe less fichero.txt | Muestra el contenido paginado (Q para salir, / para buscar) head -n 5 fichero.txt | Muestra las primeras 5 líneas tail -n 5 fichero.txt | Muestra las últimas 5 líneas tail -f fichero.txt | Sigue el fichero en tiempo real (muy útil para monitorizar logs) wc -l fichero.txt | Cuenta el número de líneas (*word count*) |
|---|---|---|---|---|---|---|

**Aplicación ofensiva de** tail -f**:** cuando se está en una máquina comprometida y se quiere monitorizar en tiempo real un archivo de log (ej. /var/log/auth.log) para detectar actividad o credenciales.

## 7. Información del sistema

| Comando | Descripción |
|---|---|
| uname -a | Muestra toda la información del kernel (versión, arquitectura, nombre de máquina) df -h | Muestra el espacio libre y usado en discos (*disk free*, legible en humano) free -h | Muestra la memoria RAM disponible y usada whoami | Muestra el usuario actual hostname | Muestra el nombre de la máquina |
|---|---|---|---|---|---|

**Uso ofensivo de** uname -a**:** al comprometer una máquina, el primer objetivo es identificar el kernel. Una versión desactualizada puede tener exploits conocidos para escalar privilegios (ej. Dirty COW en kernels Linux antiguos).

## 8. Recursividad: concepto clave

La **recursividad** es la capacidad de iterar automáticamente sobre todas las carpetas, subcarpetas y archivos de una estructura jerárquica, sin límite de profundidad, hasta que no quede nada más por recorrer.

Se representa con la flag -r o -R en la mayoría de comandos. Ejemplos:

- cp -r carpeta/ destino/ → copia todos los archivos y subcarpetas.
- rm -rf carpeta/ → elimina todo recursivamente y sin confirmación.
- grep -r \"password\" /ruta/ → busca la cadena "password" en todos los archivos de toda la jerarquía.

**Uso ofensivo:** una vez dentro de una máquina comprometida, usar grep -r recursivamente sobre todo el sistema para localizar ficheros con contraseñas, bases de datos (.db), credenciales en claro, etc.

## 9. Búsqueda: grep y find

### grep -- búsqueda dentro de ficheros

| grep "password" fichero.txt | # Busca "password" en un fichero grep -r "password" /ruta/ | # Busca recursivamente en toda la jerarquía grep -r "password" /ruta/ 2>/dev/null # Suprime los errores de permisos |
|---|---|---|

El operador 2\>/dev/null redirige los mensajes de error (stderr, descriptor 2) a /dev/null (el "agujero negro" de Linux), haciendo desaparecer los mensajes de "permiso denegado" que contaminan la salida. Permite ver solo los resultados relevantes.

### find -- búsqueda de ficheros

| find / -name "apuntes.txt" 2>/dev/null | # Busca "apuntes.txt" en todo el sistema |
|---|---|

find es uno de los comandos más útiles del máster para localizar ficheros sin saber su ruta exacta.

## 10. Extensiones en Linux vs. Windows

En **Windows** las extensiones (.txt, .pdf, .exe) determinan cómo el sistema trata el archivo.

En **Linux** las extensiones no tienen significado para el sistema. Lo que importa es el **tipo de contenido real**, que se identifica mediante:

| 1. | **El primer carácter del listado** ls -l: - (fichero regular), d (directorio), l (enlace simbólico), s (socket), p (pipe). 2. | **Magic bytes**: los primeros bytes del archivo en binario indican el tipo de archivo (PNG, PDF, ELF ejecutable, script Bash...). Los scripts Bash se identifican por el *shebang* (#!/bin/bash) al principio. |
|---|---|---|

**Implicación ofensiva:** en Linux se puede nombrar un archivo .jpg con contenido de script y el sistema lo ejecutará perfectamente, lo que es una técnica habitual para ocultar malware o reverse shells.

## 11. Instantáneas (Snapshots) en VirtualBox

Dado que se rompió una Kali Linux en directo durante la clase (con rm -rf), se refuerza la recomendación de usar **instantáneas**:

- En VirtualBox: botón derecho sobre la máquina → *Instantáneas* → *Tomar instantánea*.
- Se pueden hacer con la máquina encendida o apagada.
- Es como una "foto" del estado exacto de la máquina en ese momento; permite volver a ese estado en cualquier momento.
- Complemento ideal: tener siempre una imagen base limpia como .ova para importar de nuevo si todo falla.

## 12. Contexto ofensivo: qué implica ser Red Teamer

La sesión incluye reflexiones valiosas sobre la amplitud de conocimientos que un Red Teamer necesita:

- **Forense**: para saber qué rastro deja cada acción y poder borrarlo.
- **Blue Team y logs**: para conocer dónde se registra la actividad y poder eliminarla selectivamente.
- **Redes**: para saber qué protocolos están bloqueados y exfiltrar datos por los que no lo están (ej. DNS tunneling).
- **Infraestructura y servidores**: para montar la propia infraestructura de un ejercicio de phishing (Postfix, GoPhish, redirectores, C2).
- **Normativa**: para saber qué se puede atacar y qué no en entornos cloud (AWS, Google, Azure tienen sus propias reglas).

Ejemplo real del profesor: para una campaña de phishing a 600 empleados, el Gmail tiene un límite de \~300 correos/día, lo que obligó a montar un servidor **Postfix** propio con cabeceras personalizadas para que los destinatarios viesen el remitente suplantado en lugar de la cuenta de Gmail real.

## 13. Próximos temas

- Encadenamiento de comandos con **pipes** (|) y operadores (&&, ||).
- Variables de entorno y su uso en escalada de privilegios.
- **Alias** y funciones personalizadas en Bash.
- Scripting básico en Bash: if/else, bucles.
- Introducción a **PowerShell**.

## 14. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| VAS / BAS / VAZ | **Bash** (*Bourne Again Shell*) -- intérprete de comandos de Linux Powercell | **PowerShell** -- intérprete de comandos de Windows Xmile / Xmain | **XMind** -- herramienta de mapas mentales para organizar el aprendizaje Mecadir | **mkdir** (*make directory*) -- comando para crear directorios Touch | **touch** -- correcto; crea un fichero vacío o actualiza su timestamp Errm / Errm-RF | **rm** y **rm -rf** -- eliminar ficheros y directorios recursivamente Chain directory | **cd** (*change directory*) -- comando para moverse entre directorios guion P / guion la | **-p** / **-la** -- flags de los comandos mkdir y ls respectivamente less / les | **less** -- visor de ficheros paginado tail guion F | **tail -f** -- seguir un fichero en tiempo real work count | **wc** (*word count*) -- comando para contar líneas, palabras y caracteres uname guion O / guion A | **uname -a** -- muestra toda la información del kernel DF guion H / Free guion H | **df -h** / **free -h** -- espacio en disco y memoria RAM Huamai | **whoami** -- muestra el usuario actual magic bytes / shitbank | **Magic bytes** / **shebang** (#!/bin/bash) -- identificación del tipo de archivo en Linux rector | **TOR** (*The Onion Router*) -- red de comunicaciones anónimas dev null | **/dev/null** -- "agujero negro" del sistema; descarta todo lo que se redirige a él Go Fish / GoFish | **GoPhish** -- framework open source para campañas de phishing controlado Postfix | **Postfix** -- servidor de correo para Linux, usado en ejercicios de phishing Blue Timer | **Blue Teamer** -- profesional de ciberseguridad defensiva OmniAdev | **omnia.dev** -- dominio del profesor con su infraestructura de aplicaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase5.md|resumen_master_clase5]— Escalada de Privilegios, Kali Linux, Normativa / GRC
- [[resumen_master_clase4.md|resumen_master_clase4]— Escalada de Privilegios, Kali Linux, Normativa / GRC
- [[../../Apuntes/11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]— Escalada de Privilegios, Redes, Windows
- [[../PREWORK/resumen_clase10.md|resumen_clase10]— Normativa / GRC, Pivoting / Movilidad Lateral, Redes
- [[../MODULO3/resumen_master_clase40.md|resumen_master_clase40]— Escalada de Privilegios, Kali Linux, Redes
- [[resumen_master_clase1.md|resumen_master_clase1]— Kali Linux, Normativa / GRC, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Netcat / Reverse Shells]]

> #blue-team #escalada-privilegios #forense #ia #kali #linux #netcat #normativa #pivoting #redes #reverse-shell #windows
