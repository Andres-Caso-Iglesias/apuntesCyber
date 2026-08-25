# **Contexto de la sesiÃ³n**

La sesiÃ³n continÃºa el bloque de **auditorÃ­a web**. Tras haber visto en clases anteriores el **OWASP Top 10** y **Burp Suite**, se aplica ahora la metodologÃ­a a un tipo concreto de aplicaciÃ³n: los **CMS** (gestores de contenidos), usando **WordPress** como caso prÃ¡ctico sobre la mÃ¡quina **Academy** de TheHackerLabs.

Se decidiÃ³ realizar toda la prÃ¡ctica desde **Kali Linux**, ya que Kali trae por defecto las dependencias necesarias (WPScan, diccionarios, etc.) y hacerlo desde Windows complicaba la instalaciÃ³n de dependencias.

| |
|---|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Contenido visto en clase.** El instructor recorre la *kill chain* completa hasta el acceso inicial: reconocimiento â†’ enumeraciÃ³n web â†’ detecciÃ³n del CMS â†’ WPScan â†’ obtenciÃ³n de credenciales â†’ RCE mediante el editor de temas â†’ reverse shell â†’ usuario www-data.|

# **Objetivos de aprendizaje**

1.Â  Diferenciar una **web nativa** (PHP, .NET, Javaâ€¦) de una web basada en **CMS** (WordPress, Joomla, Drupalâ€¦) y entender por quÃ© se auditan de forma distinta.

2.Â  Comprender que en WordPress **la mayor superficie de ataque estÃ¡ en los plugins**, no en el nÃºcleo.

3.Â  Enumerar un WordPress con **WPScan**: versiÃ³n, usuarios, plugins y sus vulnerabilidades.

4.Â  Entender la diferencia entre lanzar WPScan **con y sin API token**.

5.Â  Reconocer la **enumeraciÃ³n de usuarios por mensajes de error** en el login.

6.Â  Situar la **fuerza bruta como Ãºltimo recurso** y saber por quÃ© en WordPress se prefiere WPScan frente a Hydra o Burp Intruder.

7.Â  Conseguir **RCE** subiendo una *reverse shell* PHP a travÃ©s del **editor de temas** (plantilla 404.php).

8.Â  Entender la transiciÃ³n de trÃ¡fico **HTTP â†’ TCP** al obtener la shell y estabilizarla.

# **Conceptos clave**

|**Concepto**|**ExplicaciÃ³n sencilla**|**Uso en auditorÃ­a**|**Visto en la clase**|
|---|---|---|---|
|CMS|Gestor de contenidos: un nÃºcleo desarrollado por una empresa (WordPress) al que se aÃ±aden extensiones.|Cambia la forma de auditar respecto a una web nativa.|SÃ­|
|Plugin|Conector/extensiÃ³n que aÃ±ade funciones al CMS. Muchos son de terceros y nadie revisa su seguridad.|Principal vector de entrada en WordPress.|SÃ­|
|Web nativa|Web programada directamente (PHP, .NET, Java).|MÃ¡s habitual encontrar SQLi, XSS, etc. de forma directa.|SÃ­|
|EnumeraciÃ³n recursiva|Al hallar un directorio, el fuzzer repite el escaneo dentro de Ã©l automÃ¡ticamente.|Descubre rutas ocultas dentro de /wordpress.|SÃ­ (flag -r)|
|User enumeration|El login revela si un usuario existe segÃºn el mensaje de error.|Reduce la fuerza bruta de exponencial a lineal.|SÃ­|
|API token (WPScan)|Clave que conecta WPScan con su base de datos de vulnerabilidades.|Sin token solo lista; con token aÃ±ade CVEs.|SÃ­|
|Binomio uploader/upload|Poder subir un fichero + poder ejecutarlo = RCE.|VÃ­a tÃ­pica de acceso inicial en web.|SÃ­|
|Reverse shell|La mÃ¡quina vÃ­ctima se conecta de vuelta al atacante.|Acceso inicial al sistema operativo.|SÃ­|

â†’

# **Desarrollo tÃ©cnico**

## **1. CMS frente a web nativa**

El instructor distingue dos tipos de pÃ¡ginas web:

â—Â Â Â Â Â  **Nativas**: programadas directamente en PHP, .NET, Java, etc. Es mÃ¡s sencillo encontrar directamente inyecciones SQL, XSS y similares.

â—Â Â Â Â Â  **CMS**: WordPress, Joomla, Drupal, plataformas de e-commerce, etc. Tienen un **nÃºcleo** (la "troncal") mantenido por la empresa y se les aÃ±aden **plugins**.

| |
|---|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Idea central de la clase.** El nÃºcleo de WordPress rara vez es vulnerable: estÃ¡ muy revisado. Las grandes vulnerabilidades aparecen en los **plugins**, porque hay miles, cualquiera los publica y **nadie audita su seguridad**.<br><br>Por muy fortificado que estÃ© el WordPress, si instalas un plugin vulnerable estÃ¡s abriendo una puerta de entrada.|

## **2. Reconocimiento y enumeraciÃ³n de puertos**

Primer paso habitual en el laboratorio: localizar el host en la red con **netdiscover**, y luego escanear puertos con **nmap**.

| |
|---|
|sudo netdiscover -r 10.0.2.0/24<br><br>sudo nmap -sV -p- {IP_OBJETIVO}|

**Resultado observado en clase:** la mÃ¡quina expone el puerto **22 (SSH)** y el **80 (HTTP)**. El interÃ©s se centra en el 80.

| |
|---|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Nota (fidelidad).** netdiscover se usÃ³ de forma explÃ­cita en clase sobre el rango 10.0.2.0/24. El comando exacto de nmap no se detallÃ³ literalmente en la grabaciÃ³n; se incluye el comando de enumeraciÃ³n de puertos habitual del mÃ¡ster con un placeholder {IP_OBJETIVO}. Solo se confirmÃ³ el resultado: puertos 22 y 80 abiertos.|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria.** netdiscover funciona con el protocolo **ARP**, que **no** estÃ¡ permitido en la infraestructura de red de AWS. Por eso no sirve para descubrir hosts en entornos cloud de Amazon.|

## **3. EnumeraciÃ³n web y descubrimiento del CMS**

Al abrir http://{IP_OBJETIVO} en el navegador se identifica un servidor **Apache**. Sobre cualquier web, el paso siguiente es el *fuzzing* de directorios. En clase se usÃ³ **Dirsearch** (el instructor lo prefiere por su interfaz), pero es equivalente a Gobuster, Feroxbuster o ffuf: lo importante es el **diccionario** que se use.

| |
|---|
|dirsearch -u http://{IP_OBJETIVO}/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt|

El flag **`-r`** activa la **enumeraciÃ³n recursiva**: cuando encuentra /wordpress, relanza el escaneo dentro de esa ruta, y asÃ­ sucesivamente. Sin recursividad no se habrÃ­an descubierto las rutas internas.

**Rutas descubiertas en clase:** /wordpress (cÃ³digo 301, redirecciÃ³n), wp-login.php y wp-content/uploads.

| |
|---|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria: por quÃ© un 301.** Al acceder a /wordpress la web responde con **301 Moved Permanently** porque redirige al dominio real. La mÃ¡quina usa el dominio academy.thehackerlabs, asÃ­ que hay que aÃ±adirlo al fichero /etc/hosts para que resuelva:|
|sudo nano /etc/hosts<br><br># aÃ±adir la lÃ­nea:Â Â  {IP_OBJETIVO}Â Â  academy.thehackerlabs|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Error comÃºn.** Un mismo diccionario lanzado solo sobre la raÃ­z **no** encuentra rutas que sÃ­ estÃ¡n bajo /wordpress (p. ej. wp-content/uploads). La palabra puede estar en el diccionario, pero si no se enumera recursivamente sobre la subruta correcta, no aparece. Distintas herramientas traen distintos diccionarios por defecto â†’ distintas salidas.|

## **4. WPScan: enumeraciÃ³n de la tecnologÃ­a**

**WPScan** es la herramienta de referencia para auditar WordPress. Se lanza siempre **apuntando al directorio que contiene el WordPress** (/wordpress), no a la raÃ­z del dominio: un exploit o escaneo lanzado contra una tecnologÃ­a que no estÃ¡ ahÃ­ no sirve de nada.

| |
|---|
|wpscan --url http://academy.thehackerlabs/wordpress|

**Resultado observado:** WordPress **versiÃ³n 6.5.3**, presencia de xmlrpc.php, readme.html y wp-content/uploads. A partir de la versiÃ³n ya se puede buscar (wordpress 6.5.3 vulnerabilities) una primera idea de ataque.

| |
|---|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria: XML-RPC.** xmlrpc.php es una API antigua de WordPress. En el contexto de esta auditorÃ­a el instructor la descarta como vÃ­a Ãºtil de entrada. TambiÃ©n se aprecia en las cabeceras (vistas con Burp) que el servidor es **Apache** sobre **Linux**.|

## **5. WPScan: enumeraciÃ³n de usuarios**

El objetivo intermedio es conseguir un **usuario** vÃ¡lido. WPScan tiene una funciÃ³n propia de enumeraciÃ³n de usuarios (-e u, con **U mayÃºscula** para pasarle un diccionario de nombres):

| |
|---|
|wpscan --url http://academy.thehackerlabs/wordpress -e u<br><br>wpscan --url http://academy.thehackerlabs/wordpress --enumerate u -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Nota (fidelidad).** En clase se usÃ³ un diccionario de **usernames de SecLists** (se eligiÃ³ una lista de "top usernames"). El nombre exacto del fichero no se dictÃ³ con precisiÃ³n en la grabaciÃ³n; se indica una ruta representativa de SecLists como placeholder editable.|

## **6. WPScan: enumeraciÃ³n de plugins y API token**

Para enumerar los plugins se usa --enumerate ap (*all plugins*). AquÃ­ aparece la diferencia clave con el **API token**:

â—Â Â Â Â Â  **Sin** API token â†’ WPScan **lista** los plugins y sus versiones (p. ej. se detectÃ³ **Elementor**), pero **no** dice quÃ© vulnerabilidades tienen.

â—Â Â Â Â Â  **Con** API token â†’ WPScan consulta su **base de datos de vulnerabilidades** y aÃ±ade los **CVE** asociados a cada plugin y a la versiÃ³n de WordPress.

| |
|---|
|wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap<br><br>wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria.** El API token **no** aporta capacidades ofensivas extra; solo es la conexiÃ³n a la base de datos de vulnerabilidades de WPScan. Se obtiene gratis registrÃ¡ndose en el portal de WPScan (wpscan.com).|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Matiz importante de la clase: no toda vulnerabilidad listada es explotable.**<br><br>Muchas vulnerabilidades de plugins requieren estar **autenticado** o un **rol** concreto (p. ej. distribuidor), o afectan a una funcionalidad que **no estÃ¡ accesible/activa** en la web. Como todavÃ­a se busca el **acceso inicial**, se **descartan** temporalmente y no se pierde tiempo con ellas.<br><br>El trabajo del auditor es entender **en quÃ© funciÃ³n y en quÃ© endpoint** aplica cada CVE y si es realmente accesible. AhÃ­ estÃ¡ la auditorÃ­a web de verdad.|

## **7. EnumeraciÃ³n de usuarios por mensajes de error (login)**

El login de WordPress puede **filtrar** si un usuario existe: si escribes un usuario inexistente responde *"el nombre de usuario X no estÃ¡ registrado en este sitio"*. Eso confirma quÃ© usuarios existen.

| |
|---|
|**â›”Â  RIESGO / EXPLOTACIÃ“N EN LABORATORIO**<br><br>**Riesgo / concepto de seguridad.** Un login **mal implementado** distingue entre "usuario no existe" y "contraseÃ±a incorrecta". Eso convierte la bÃºsqueda de credenciales de **exponencial** (adivinar usuario y contraseÃ±a a la vez) a **lineal** (primero el usuario, luego su contraseÃ±a).<br><br>Un login **bien implementado** responde siempre lo mismo: *"usuario o contraseÃ±a incorrectos"*, sin dar pistas.|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Nota (fidelidad).** El instructor demostrÃ³ este comportamiento sobre un sitio **de un cliente propio** (con autorizaciÃ³n) a modo de ejemplo real, no sobre la mÃ¡quina Academy. Se recoge aquÃ­ como **concepto**, no como paso de la mÃ¡quina.|

## **8. Fuerza bruta con WPScan (Ãºltimo recurso)**

Solo cuando se han agotado otras vÃ­as se recurre a la fuerza bruta. WPScan puede hacer el ataque de contraseÃ±as con --passwords:

| |
|---|
|wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt|

**Resultado observado en clase:** se obtuvo un usuario vÃ¡lido â€” **Dylan** â€” con una contraseÃ±a dÃ©bil del tipo **`password1`** (presente en rockyou.txt).

| |
|---|
|**âœ”Â  OBJETIVO / BUENA PRÃCTICA**<br><br>**Buena prÃ¡ctica (regla de oro).** La **fuerza bruta es el Ãºltimo recurso**: es ruidosa y "funciona 1 de cada 10 veces". Antes conviene enumerar usuarios, reutilizar credenciales, buscar fugas de informaciÃ³n, etc.<br><br>Para WordPress se prefiere **WPScan** frente a **Hydra** (que suele no responder bien al login de WordPress) o **Burp Intruder** (mÃ¡s lento). AdemÃ¡s, el plugin **Wordfence** actÃºa como "antivirus/WAF" de WordPress y limita el nÃºmero de intentos.|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Nota (fidelidad).** La transcripciÃ³n recoge la credencial como "Dylan" con "password 1". Se interpreta como usuario Dylan / contraseÃ±a password1 (una entrada tÃ­pica de rockyou.txt). Es un **valor de laboratorio** de esta mÃ¡quina; adÃ¡ptalo a tu instancia.|

## **9. Acceso inicial: RCE por el editor de temas**

Con las credenciales se inicia sesiÃ³n en el panel (/wp-admin). Desde **Apariencia â†’ Editor de temas** (Herramientas â†’ Editor de archivos de tema) se puede editar el cÃ³digo de las plantillas del tema. La idea: **inyectar cÃ³digo PHP** en una plantilla que luego se ejecute al visitarla.

Se elige la plantilla **`404.php`** y se pega dentro una **reverse shell PHP** (misma tÃ©cnica que en la mÃ¡quina **Mr. Robot**).

| |
|---|
|**â›”Â  RIESGO / EXPLOTACIÃ“N EN LABORATORIO**<br><br>**ExplotaciÃ³n en laboratorio.** La plantilla objetivo debe ser **PHP**. Si la plantilla es **HTML** (como ocurriÃ³ con una 404 en clase), el cÃ³digo PHP **no se ejecuta**. Hay que buscar un fichero de plantilla .php.|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria: servidor â†’ lenguaje.** Como regla general (â‰ˆ99,9 %):<br><br>â€¢ **Apache / Linux â†’ PHP** (webshells .php).<br><br>â€¢ **IIS / Windows â†’ ASP.NET (`.aspx`)**.<br><br>â€¢ Casos raros: Perl, Ruby, Go, Python, Node/JS, etc. Si subes una shell en el lenguaje equivocado, no se ejecuta.|

## **10. Reverse shell: de HTTP a TCP**

Tras guardar la 404.php maliciosa, se pone **Netcat** a la escucha y se **dispara** la shell visitando la pÃ¡gina 404 en el navegador:

| |
|---|
|nc -lvnp 1234|

Al acceder a la pÃ¡gina, la **mÃ¡quina vÃ­ctima se conecta de vuelta** al puerto 1234 del atacante. En ese instante el trÃ¡fico deja de ser peticiones de navegador (HTTP) y pasa a ser una conexiÃ³n **TCP** directa (handshake SYN â†’ SYN/ACK â†’ ACK).

| |
|---|
|**â„¹Â  INFORMACIÃ“N**<br><br>**ExplicaciÃ³n complementaria (se conectÃ³ con el forense visto antes).** En una captura de red, una rÃ¡faga de HTTP que de repente cambia a **TCP** es una seÃ±al tÃ­pica de reverse shell. AdemÃ¡s, una vez dentro del servidor, el **WAF** (Wordfence) ya no protege: actÃºa a nivel de aplicaciÃ³n; dentro solo queda el firewall del sistema.|

## **11. EstabilizaciÃ³n de la shell y usuario obtenido**

La shell inicial es limitada. Se estabiliza (tÃ©cnica ya vista en el mÃ¡ster):

| |
|---|
|python3 -c 'import pty; pty.spawn("/bin/bash")'<br><br>export TERM=xterm<br><br># Ctrl+Z ; luego en Kali:<br><br>stty raw -echo; fg|

Se comprueba el usuario con whoami / id: somos **`www-data`**. Revisando /etc/passwd se ve quÃ© shell usan los demÃ¡s usuarios (aquÃ­ **bash**), lo que confirma que la shell interactiva funcionarÃ¡.

| |
|---|
|**âœ”Â  OBJETIVO / BUENA PRÃCTICA**<br><br>**Acceso inicial conseguido:** usuario www-data en la mÃ¡quina Academy.|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Nota (fidelidad).** La **escalada de privilegios a root quedÃ³ pendiente**. El instructor indicÃ³ que esta mÃ¡quina se guarda y su escalada (descrita como "una fumada") se verÃ¡ en el mÃ³dulo de escalada de privilegios.|

# **Flujo de trabajo de la sesiÃ³n**

Kill chain seguida en el laboratorio (hasta acceso inicial):

| | | |
|---|---|---|
||Reconocimiento de red (netdiscover)||
||**â†“**||
||EnumeraciÃ³n de puertos (nmap) â†’ 22 y 80||
||**â†“**||
||Fuzzing web recursivo (dirsearch -r) â†’ /wordpress||
||**â†“**||
||Ajuste de /etc/hosts (academy.thehackerlabs)||
||**â†“**||
||DetecciÃ³n del CMS + versiÃ³n (WPScan) â†’ WP 6.5.3||
||**â†“**||
||EnumeraciÃ³n de usuarios y plugins (WPScan)||
||**â†“**||
||Credenciales vÃ¡lidas (fuerza bruta WPScan) â†’ Dylan||
||**â†“**||
||Login en /wp-admin||
||**â†“**||
||RCE: reverse shell PHP en 404.php (editor de temas)||
||**â†“**||
||Netcat a la escucha (1234) â†’ shell www-data||
||**â†“**||
||EstabilizaciÃ³n de la shell||
||**â†“**||
||Escalada de privilegios (PENDIENTE â€” prÃ³ximo mÃ³dulo)||

# **Herramientas utilizadas en la sesiÃ³n**

|**Herramienta**|**Objetivo**|**Fase**|**Comando o uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|netdiscover|Localizar hosts en la red|Reconocimiento|netdiscover -r 10.0.2.0/24|Practicada|Usa ARP; no vale en AWS|
|nmap|Puertos y servicios|EnumeraciÃ³n|nmap -sV -p- {IP}|Recurrente|Resultado: 22 y 80|
|dirsearch|Fuzzing de directorios|Enum. web|dirsearch -u URL -r -w dic|Practicada|-r = recursivo; equivale a Gobuster/ffuf|
|WPScan|Auditar WordPress|Enum. / ExplotaciÃ³n|wpscan --url URL/wordpress â€¦|Usada en auditorÃ­a|NÃºcleo de la sesiÃ³n|
|SecLists|Diccionarios|EnumeraciÃ³n|top-usernames-shortlist.txt|Introducida|Listas de usuarios|
|rockyou.txt|Diccionario de contraseÃ±as|Fuerza bruta|/usr/share/wordlists/rockyou.txt|Introducida|ContraseÃ±as comunes|
|Burp Suite|Interceptar/analizar HTTP|Enum. web|Proxy + FoxyProxy 127.0.0.1:8080|Practicada|Ver cabeceras y cookies|
|Netcat|Listener reverse shell|ExplotaciÃ³n|nc -lvnp 1234|Practicada|Recibe la shell (TCP)|
|/etc/hosts|Resolver dominio local|Enum. web|IP academy.thehackerlabs|Practicada|Necesario por la redirecciÃ³n 301|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Nota.** Wordfence aparece **mencionado** como el plugin "antivirus/WAF" de WordPress que limita intentos de login, pero **no se explota ni se configura** en el material.|

# **Comandos importantes**

## **Reconocimiento y enumeraciÃ³n**

| |
|---|
|sudo netdiscover -r 10.0.2.0/24<br><br>sudo nmap -sV -p- {IP_OBJETIVO}<br><br>dirsearch -u http://{IP_OBJETIVO}/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt|

netdiscover -r: descubre hosts vÃ­a ARP en el rango indicado. nmap -sV -p-: escanea los 65 535 puertos TCP e intenta detectar versiones. dirsearch -r: fuzzing **recursivo** de directorios.

## **Ajuste de /etc/hosts**

| |
|---|
|sudo nano /etc/hosts<br><br># {IP_OBJETIVO}Â Â  academy.thehackerlabs|

Mapea el dominio de la mÃ¡quina a su IP para que el navegador y WPScan resuelvan correctamente tras la redirecciÃ³n 301.

## **WPScan**

| |
|---|
|wpscan --url http://academy.thehackerlabs/wordpress<br><br>wpscan --url http://academy.thehackerlabs/wordpress -e u -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt<br><br>wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap<br><br>wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}<br><br>wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt|

De arriba a abajo: escaneo base (detecta versiÃ³n), enumeraciÃ³n de **usuarios** (-e u, -U = diccionario de nombres), enumeraciÃ³n de **plugins** (ap = all plugins), enumeraciÃ³n de **plugins vulnerables** con **API token** (aÃ±ade CVEs), y **fuerza bruta** de contraseÃ±as con rockyou.txt.

## **Reverse shell y estabilizaciÃ³n**

| |
|---|
|nc -lvnp 1234<br><br>python3 -c 'import pty; pty.spawn("/bin/bash")'<br><br>export TERM=xterm<br><br>stty raw -echo; fg<br><br>whoami; id|

nc -lvnp 1234: pone Netcat a la escucha para recibir la conexiÃ³n de vuelta. El resto estabiliza la TTY y confirma que somos www-data.

# **Riesgos, errores comunes y buenas prÃ¡cticas**

| |
|---|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Apuntar al directorio equivocado.** WPScan/exploits deben lanzarse contra /wordpress (donde vive el CMS), no contra la raÃ­z del dominio. Contra una ruta sin WordPress no obtendrÃ¡s nada.|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Confiar en toda vulnerabilidad listada.** Muchas requieren autenticaciÃ³n, un rol concreto o una funcionalidad accesible. Verifica endpoint y contexto antes de invertir tiempo.|
|**âš Â  AVISO / ERROR COMÃšN**<br><br>**Lenguaje de la webshell.** Subir una shell en el lenguaje equivocado (p. ej. HTML o .aspx en un Apache/Linux) hace que no se ejecute.|
|**âœ”Â  OBJETIVO / BUENA PRÃCTICA**<br><br>**Fuerza bruta al final.** Agota antes enumeraciÃ³n, reutilizaciÃ³n de credenciales y fugas de informaciÃ³n. Es ruidosa y poco fiable.|
|**âœ”Â  OBJETIVO / BUENA PRÃCTICA**<br><br>**Documenta** cada comando, su resultado y tu interpretaciÃ³n: no basta con lanzar herramientas, hay que entender quÃ© devuelven y por quÃ©.|
|**â›”Â  RIESGO / EXPLOTACIÃ“N EN LABORATORIO**<br><br>**Alcance.** Todo lo anterior se aplica **solo** en laboratorios y auditorÃ­as autorizadas. La demostraciÃ³n de *user enumeration* sobre un sitio real la hizo el instructor sobre un **cliente propio** con permiso.|

# **ConexiÃ³n con sesiones anteriores**

Esta sesiÃ³n enlaza directamente con varios bloques ya trabajados en el mÃ¡ster:

â—Â Â Â Â Â  **OWASP Top 10 y auditorÃ­a web**: se aplica la metodologÃ­a web a un CMS concreto.

â—Â Â Â Â Â  **Burp Suite / FoxyProxy**: se reutilizan para inspeccionar peticiones, cabeceras (Server: Apache) y cookies del login.

â—Â Â Â Â Â  **Fuzzing de directorios** (Gobuster, Feroxbuster, ffuf, Dirsearch): misma fase de enumeraciÃ³n web vista en mÃ¡quinas anteriores; aquÃ­ destaca la recursividad -r.

â—Â Â Â Â Â  **MÃ¡quina Mr. Robot**: la tÃ©cnica de RCE es idÃ©ntica â€” reverse shell PHP inyectada en una plantilla del tema (404.php) y disparada desde el navegador.

â—Â Â Â Â Â  **AnÃ¡lisis forense con PCAP**: se retoma la idea de detectar el cambio HTTP â†’ TCP como firma de una reverse shell.

â—Â Â Â Â Â  **Escalada de privilegios**: queda pendiente y conecta con el mÃ³dulo de *privesc* (como en Oopsie, Archetype o Mr. Robot).

# **Resumen final**

QuÃ© debe llevarse Chema de esta clase:

9.Â Â Â Â Â Â Â Â Â  En WordPress, **el peligro estÃ¡ en los plugins**, no en el nÃºcleo.

10.Â Â Â Â Â Â  **WPScan** es la navaja suiza del CMS: versiÃ³n, usuarios, plugins y, con **API token**, sus CVEs.

11.Â Â Â Â Â Â  Enumerar **antes** de forzar; la **fuerza bruta es el Ãºltimo recurso** y en WordPress se hace con WPScan.

12.Â Â Â Â Â Â  El **editor de temas** es una vÃ­a clÃ¡sica de **RCE** si consigues acceso al panel: PHP en 404.php.

13.Â Â Â Â Â Â  La **reverse shell** convierte el juego de HTTP a TCP; luego se **estabiliza** y se comprueba el usuario (www-data).

14.Â Â Â Â Â Â  La mÃ¡quina llega hasta **acceso inicial**; la **escalada a root** se verÃ¡ mÃ¡s adelante.

# **Checklist de repaso**

â˜Â  SÃ© diferenciar una web nativa de un CMS y por quÃ© se auditan distinto.

â˜Â  Entiendo por quÃ© la superficie de ataque de WordPress estÃ¡ en los plugins.

â˜Â  SÃ© lanzar netdiscover y nmap para reconocimiento y enumeraciÃ³n de puertos.

â˜Â  SÃ© por quÃ© uso el flag -r (recursivo) en el fuzzing de directorios.

â˜Â  SÃ© por quÃ© una ruta da 301 y cÃ³mo arreglar la resoluciÃ³n con /etc/hosts.

â˜Â  SÃ© enumerar versiÃ³n, usuarios y plugins con WPScan.

â˜Â  Entiendo la diferencia entre WPScan con y sin API token.

â˜Â  Reconozco la enumeraciÃ³n de usuarios por mensajes de error del login.

â˜Â  SÃ© por quÃ© la fuerza bruta es el Ãºltimo recurso y por quÃ© uso WPScan en WordPress.

â˜Â  SÃ© conseguir RCE con una reverse shell PHP en el editor de temas (404.php).

â˜Â  Entiendo la transiciÃ³n HTTP â†’ TCP al obtener la shell y cÃ³mo estabilizarla.

â˜Â  SÃ© identificar el usuario obtenido (www-data) y que la escalada queda pendiente.

# **ActualizaciÃ³n del registro de herramientas**

Cambios de nivel derivados de esta sesiÃ³n (para copiar a la base de conocimiento del proyecto):

|**Herramienta**|**Nivel anterior**|**Nivel nuevo**|**Motivo del cambio**|**Notas para futuras sesiones**|
|---|---|---|---|---|
|WPScan|Introducida|Usada en auditorÃ­a|EnumeraciÃ³n de versiÃ³n, usuarios y plugins + fuerza bruta dentro de la kill chain de una mÃ¡quina.|Repasar --enumerate (u/ap/vp) y el uso del API token.|
|Dirsearch|Mencionada|Practicada|Uso real con enumeraciÃ³n recursiva (-r) sobre /wordpress.|Comparar diccionarios por defecto entre herramientas.|
|Netcat|â€”|Practicada|Listener de la reverse shell (nc -lvnp 1234).|Ligado a la fase de acceso inicial.|
|SecLists|Introducida|Practicada|Diccionarios de usernames para WPScan.|Localizar las listas de usuarios mÃ¡s Ãºtiles.|
|rockyou.txt|â€”|Introducida|Diccionario de contraseÃ±as en la fuerza bruta con WPScan.|Diccionario por defecto en /usr/share/wordlists.|
|Netdiscover|Practicada|Practicada|Uso confirmado en reconocimiento (sin cambio de nivel).|Recordar: ARP, no vÃ¡lido en AWS.|
|Burp Suite|Practicada|Practicada|Apoyo para inspecciÃ³n de cabeceras/cookies (sin cambio de nivel).|Reutilizado del bloque anterior.|
|**â„¹Â  INFORMACIÃ“N**<br><br>**Herramientas nuevas registradas en esta sesiÃ³n:** Netcat (como listener) y el diccionario rockyou.txt. WPScan sube a **Usada en auditorÃ­a**.|

â†’

â†’

â†’
â†’
â†’
