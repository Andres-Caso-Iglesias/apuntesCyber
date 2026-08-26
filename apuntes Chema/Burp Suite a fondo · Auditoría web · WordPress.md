# 2. Conceptos clave

## 2.1. Â¿QuÃ© es Burp Suite?

La definiciÃ³n rÃ¡pida y correcta es: **Burp Suite es un framework de auditorÃ­a web**. Es una recopilaciÃ³n de funcionalidades/herramientas dentro de un mismo programa que permiten realizar multitud de acciones sobre pÃ¡ginas web y, por tanto, auditarlas.

| |
|---|
|**âš ï¸Â  Error comÃºn de definiciÃ³n**<br><br>Decir que "Burp es un proxy" es **incompleto**. El proxy es la **funcionalidad principal y dependencia crÃ­tica** (sin proxy no se puede operar), pero Burp es mucho mÃ¡s: Repeater, Intruder, Decoder, Comparer, etc.|

## 2.2. Front vs Back: dÃ³nde tenemos el control

Una web se compone de **front** (corre en TU ordenador, dentro del navegador) y **back** (corre en el servidor, fuera de tu alcance). El Ãºnico punto donde tenemos control total es el navegador: ahÃ­ se **forja** la peticiÃ³n antes de enviarse por la red.

La idea central de Burp: colocar un **bloqueo (proxy)** justo despuÃ©s de que el front genera la peticiÃ³n y **antes** de que salga del ordenador hacia el back. En ese instante la peticiÃ³n estÃ¡ en **texto claro** (aÃºn no ha entrado el cifrado TLS/SSL de HTTPS) y se puede **leer y modificar**.

| |
|---|
|**â„¹ï¸Â  AnalogÃ­a de Carlos: "la abuela y el paquete"**<br><br>TÃº metes unos calcetines (peticiÃ³n legÃ­tima) en un buzÃ³n. La pÃ¡gina web te ve enviarlo y se queda tranquila porque cumpliste sus reglas de seguridad del front. Pero **justo antes de que llegue el cartero**, Chema (Burp) abre el paquete, cambia el contenido y lo vuelve a cerrar.<br><br>El servidor (la abuela) recibe algo muy distinto a lo enviado. Si el back no valida bien, "explota". Por eso se pone un **WAF** justo delante para protegerla.|

ConclusiÃ³n: si los controles de seguridad estÃ¡n **solo en el front**, son **bypasseables**. Por eso la tendencia actual es **securizar el back** y validar la **integridad del dato** en el servidor.

| |
|---|
|FRONT (tu navegador) â€” generas la peticiÃ³n Â· TIENES EL CONTROL|

**â–¼**

| |
|---|
|PROXY de Burp intercepta (texto claro, antes de TLS)|

**â–¼**

| |
|---|
|Modificas la peticiÃ³n â†’ se salta los controles del front|

**â–¼**

| |
|---|
|WAF (Web Application Firewall) â€” Ãºltima defensa antes del server|

**â–¼**

| |
|---|
|BACK (servidor) â€” valida integridad del dato (o explota)|

## 2.3. Sesiones, cookies e ID de sesiÃ³n

Cuando varios usuarios entran a la vez a una web, el servidor no puede servir lo mismo a todos. Asigna a cada uno un **ID de sesiÃ³n** (cookie tipo SID) que identifica quiÃ©n es cada cual y quÃ© "plantilla" de la pÃ¡gina le corresponde. De ahÃ­ la importancia de la **gestiÃ³n de identidades**.

| |
|---|
|**â„¹ï¸Â  Datos sobre cookies de sesiÃ³n**<br><br>Las cookies se eliminan al cerrar el navegador y **purgar la cachÃ©**. Un Ctrl+Shift+R hace un _hard reset_ (borra cachÃ© â†’ nuevo ID de sesiÃ³n).<br><br>**En informÃ¡tica no existe la aleatoriedad pura**: siempre hay una semilla. Por eso el _Comparer_ sirve para buscar patrones en cÃ³mo se generan las cookies.|
|**ðŸ”´Â  Robo de sesiÃ³n (laboratorio / concienciaciÃ³n)**<br><br>**Session hijacking** (histÃ³rico): iterar el ID de la cookie para colarse en la sesiÃ³n de otro usuario. Muy usado antiguamente en e-commerce. Hoy es complejo por el uso de tokens.<br><br>**Robo de cookie de sesiÃ³n actual:** si se roba la cookie de sesiÃ³n vÃ¡lida (p. ej. mediante XSS almacenado o phishing avanzado que intercepta el 2FA en tiempo real), se puede mantener acceso durante el tiempo de vida de la cookie **sin usuario, contraseÃ±a ni 2FA**. Por eso las cookies de sesiÃ³n son tan sensibles.<br><br>_Solo aplicable en laboratorios y auditorÃ­as autorizadas._|

# 3. Desarrollo tÃ©cnico: mÃ³dulos de Burp Suite

## 3.1. Proxy (corazÃ³n de Burp)

Intercepta la peticiÃ³n entre front y back. Permite **pararla, leerla y modificarla**. Dentro del Proxy:

â€¢Â Â Â Â  **Intercept on/off:** activa/desactiva la retenciÃ³n de paquetes.

â€¢Â Â Â Â  **HTTP History:** historial de todas las peticiones (Ãºtil para consultar lo ya capturado, no solo para borrarlo).

â€¢Â Â Â Â  **Proxy Settings â†’ Proxy listeners:** aquÃ­ se ve/define el puerto de escucha (por defecto **8080**).

## 3.2. ConfiguraciÃ³n del proxy: certificado + Foxy Proxy

Para interceptar HTTPS sin que las webs desconfÃ­en, hay que instalar el **certificado de la CA de Burp** (Burp actÃºa como entidad certificadora vÃ¡lida, certificado vigente hasta ~2036).

1.Â  Con Burp abierto, ir a http://localhost:8080 (o 127.0.0.1:8080) â†’ botÃ³n **CA Certificate** (arriba derecha) â†’ descargar cacert.der.

2.Â  En **Firefox** (recomendado por Carlos): about:preferences â†’ buscar _certificados_ â†’ **ConfiguraciÃ³n avanzada â†’ Administrar certificados â†’ Importar** â†’ seleccionar el cacert â†’ aceptar.

3.Â  Verificar en pestaÃ±a **Autoridades**: debe aparecer **PortSwigger** como CA.

Luego se configura el **proxy real** con la extensiÃ³n **Foxy Proxy** (alternativa a configurar el proxy manualmente en cada web):

4.Â  Instalar Foxy Proxy como extensiÃ³n de Firefox.

5.Â  Opciones â†’ Proxies â†’ aÃ±adir un proxy, nombre **Burp Suite**.

6.Â  Host: 127.0.0.1, Puerto: **8080** (el mismo del _Proxy listener_ de Burp).

| |
|---|
|**â„¹ï¸Â  CÃ³mo encaja todo**<br><br>Burp levanta su proxy en 127.0.0.1:8080 y se pone a la escucha. **Foxy Proxy reenvÃ­a** los paquetes del navegador a Burp, y Burp es quien finalmente los lanza a Internet. Igual que una reverse shell: uno escucha, otro envÃ­a.|

## 3.3. Target / Scope

Cuando auditas una web te llega muchÃ­simo ruido (Google Analytics, cookies de terceros, telemetrÃ­aâ€¦). El **Target â†’ Scope** permite aÃ±adir solo el dominio objetivo para filtrar y trabajar limpio. Poco usado, pero muy Ãºtil.

| |
|---|
|**â„¹ï¸Â  Por quÃ© hay tanto trÃ¡fico de fondo**<br><br>Aunque estÃ©s "quieto" en una web, hay subprocesos en 2Âº plano (heartbeats, "sigo vivo") manteniendo sesiones: APIs del chat, conectores, comprobaciones de conectividadâ€¦ Ya se vio este efecto en su dÃ­a con **Wireshark**.|

## 3.4. Intruder (fuerza bruta y fuzzing)

Permite hacer **fuerza bruta / fuzzing** sustituyendo uno o varios parÃ¡metros marcados por las entradas de una _wordlist_ (payload). Se vio por primera vez en la mÃ¡quina **Mr. Robot** (login de WordPress).

| |
|---|
|**âš ï¸Â  Buena prÃ¡ctica con Intruder**<br><br>Marca y fuzzea los parÃ¡metros **de uno en uno** (Add/Clear sobre la posiciÃ³n en verde, entre $...$). Cada parÃ¡metro controla algo distinto en el back; fuzzear varios a la vez mezcla resultados y no sabes quÃ© provoca quÃ©.<br><br>Y recuerda: **sin diccionario (payload) cargado, el ataque no hace nada** ("make sense").|

**Tipos de ataque** (desplegable del Intruder):

|**Tipo**|**Comportamiento**|
|---|---|
|Sniper|Un payload por cada posiciÃ³n, una a una (1 lista).|
|Battering ram|El mismo payload en todas las posiciones a la vez.|
|Pitchfork|Una lista por posiciÃ³n, en paralelo (1-1).|
|Cluster bomb|Todas las combinaciones posibles entre listas ("explota todo").|
|**âš ï¸Â  LimitaciÃ³n de la versiÃ³n Community (gratuita)**<br><br>En la versiÃ³n gratuita el Intruder estÃ¡ **throttled** (limitado en velocidad). Para fuerza bruta seria sobre WordPress es mejor **WPScan**. La versiÃ³n Pro (~500 â‚¬/aÃ±o) levanta esa limitaciÃ³n.|

## 3.5. Repeater

Permite **reenviar y repetir** una misma peticiÃ³n tantas veces como quieras, modificÃ¡ndola y viendo cÃ³mo responde el servidor. Es como hacer un curl, pero sin lanzarlo desde la sesiÃ³n activa de pantalla. Ideal para "conocer" la web antes de lanzar una fuerza bruta.

## 3.6. Decoder, Comparer, Sequencer y otros

|**MÃ³dulo**|**Para quÃ© sirve**|
|---|---|
|Decoder|Codificar/decodificar (URL-encode, Base64â€¦). Ej.: una cookie con doble Base64 + URL-encode.|
|Comparer|Comparar dos valores (p. ej. varias cookies de sesiÃ³n) para buscar patrones de generaciÃ³n.|
|Sequencer|Encadenar/analizar secuencias de peticiones (vulnerabilidades que requieren varios paquetes).|
|Logger|Registrar y autenticar peticiones (ataques autenticados con credenciales).|
|Extensions / BApp|Plugins de terceros para detectar vulnerabilidades (mayormente Ãºtil en Pro).|
|Collaborator|DetecciÃ³n de interacciones fuera de banda (Pro).|

# 4. PrÃ¡ctica: auditorÃ­a de una web WordPress (HackersLabs "Academy")

| |
|---|
|**â„¹ï¸Â  Sobre la mÃ¡quina**<br><br>MÃ¡quina **"Academy"** descargada de **HackersLabs** (plataforma tipo Hack The Box, requiere registro gratuito). Importada en VirtualBox/VMware con la red en **NAT Network** (misma que la Kali).<br><br>Por problemas con la Kali, gran parte se hizo desde **Windows con PowerShell**. Aviso de honestidad: en la transcripciÃ³n **no se llegÃ³ a completar la explotaciÃ³n** (instalaciÃ³n de Ruby/WPScan pendiente).|

## 4.1. Recordatorio de fases de pentesting

Repaso pedido en clase del prework:

| |
|---|
||
||![](file:///C:/Users/intri/AppData/Local/Packages/oice_16_974fa576_32c1d314_36b8/AC/Temp/msohtmlclip1/01/clip_image002.jpg)|

 

Cuando aparece un servicio web (puerto 80), se abre una **"subauditorÃ­a"** propia y se repiten estas fases sobre la web.

## 4.2. Reconocimiento de red

Primero localizar la IP de la mÃ¡quina objetivo en la red interna:

| |
|---|
|# En Kali â€” descubrir hosts de la red interna<br><br>netdiscover -r 192.168.1.0/24<br><br># Comprobar tu propia IP y rango primero<br><br>ip a|
|**âš ï¸Â  Incidencia real con la red (Kali en NAT)**<br><br>La Kali estaba en **NAT Network** y cogÃ­a una IP rara porque el **DHCP** de esa red no estaba habilitado. SoluciÃ³n: habilitar el DHCP de la NAT Network (Archivo â†’ Herramientas â†’ Red) y/o **apagar y encender la tarjeta de red** de la VM.<br><br>Por estos problemas se decidiÃ³ tirar **desde Windows** con PowerShell, curl y diccionarios de SecLists.|

## 4.3. EnumeraciÃ³n web: SecLists + fuzzing de directorios

**SecLists** es el repositorio de referencia con los mejores diccionarios (contraseÃ±as, fuzzing, discovery, subdominiosâ€¦). Se descarga como ZIP desde GitHub.

| |
|---|
|# SecLists (repositorio de diccionarios) â€” clonar o descargar ZIP<br><br>git clone https://github.com/danielmiessler/SecLists<br><br># Diccionario habitual para fuzzing de directorios:<br><br># SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt|

El diccionario por defecto de la mayorÃ­a de herramientas (Dirsearch, Gobuster, Feroxbuster) es **directory-list-2.3-medium.txt**. Como la Kali estaba rota, en clase se usÃ³ un **script propio en PowerShell** generado con ayuda de Claude para enumerar directorios con curl y un diccionario local.

| |
|---|
|**â„¹ï¸Â  Equivalencias para fuzzear directorios**<br><br>En Linux: feroxbuster -u URL -w wordlist, gobuster dir -u URL -w wordlist o dirsearch -u URL.<br><br>En Windows/PowerShell se puede replicar la idea con un bucle sobre el diccionario lanzando peticiones con curl y mirando el cÃ³digo de respuesta (200 = existe).|

**Resultado de la enumeraciÃ³n:** se encontrÃ³ un Ãºnico directorio relevante â†’ /wordpress.

## 4.4. Identificar tecnologÃ­a: Wappalyzer + fichero hosts

La extensiÃ³n **Wappalyzer** (Firefox/Chrome) revela las tecnologÃ­as de la web. AquÃ­ la principal: **WordPress** (sobre Apache).

| |
|---|
|**â„¹ï¸Â  Recordatorio de concepto**<br><br>Igual que un servidor no es vulnerable (lo es un _servicio en una versiÃ³n_), **una web no es vulnerable**: lo es **una funcionalidad o tecnologÃ­a en una versiÃ³n** (p. ej. un plugin).|

La mÃ¡quina usa un **dominio** (academy.thl/similar). Para que el navegador resuelva ese nombre a la IP hay que editar el fichero **hosts** (somos nuestro propio servidor DNS):

|**Sistema**|**Ruta del fichero hosts**|
|---|---|
|Linux|/etc/hosts|
|Windows|C:\Windows\System32\drivers\etc\hosts|
|# LÃ­nea a aÃ±adir en el fichero hosts (IP <TAB> dominio):<br><br>192.168.1.XÂ Â Â  academy.thl|
|**âš ï¸Â  Detalles del hosts en Windows**<br><br>Hay que abrir el Bloc de notas **como administrador** para poder guardar.<br><br>En el explorador, mostrar **todos los archivos** para ver hosts (no tiene extensiÃ³n).<br><br>Tras aÃ±adir el dominio, la web confÃ­a mÃ¡s y empieza a servir imÃ¡genes/recursos correctamente.<br><br>Casi todas las mÃ¡quinas tipo HTB requieren este paso de mapear DNS â†’ IP.|

## 4.5. EnumeraciÃ³n de WordPress (HackTricks + rutas conocidas)

**HackTricks** es la "Wikipedia/biblia del hacking". Para WordPress documenta los archivos y rutas tÃ­picas a comprobar:

|**Ruta**|**QuÃ© nos dice**|
|---|---|
|/wordpress/index.php|PÃ¡gina principal (suele redirigir a la home).|
|/wordpress/license.txt|Si estÃ¡, confirma WordPress y que la instalaciÃ³n estÃ¡ "reciÃ©n hecha" (sin limpiar).|
|/wp-login.php|Login. Un **302 redirect** a wp-login indica panel de acceso (igual que en Mr. Robot) â†’ posible fuerza bruta.|
|/wp-admin/|Panel de administraciÃ³n.|
|/wp-content/uploads/|Carpeta de subidas. Si hay un _uploader_, posible vector de **file upload** â†’ subir shell.|
|**ðŸ”´Â  Vector de ataque en mente (laboratorio)**<br><br>Si se encuentra un punto donde **subir ficheros** (uploader) y luego se pueden **ejecutar**, el vector clÃ¡sico es: subir una **web shell**, ejecutarla y obtener acceso. Requiere encontrar las dos piezas (subida + ejecuciÃ³n).<br><br>_Solo en la mÃ¡quina de laboratorio autorizada._|

## 4.6. WPScan (enumeraciÃ³n activa de WordPress)

**WPScan** es la herramienta clave para enumerar WordPress: detecta versiÃ³n, **plugins**, **temas** y **usuarios**, y permite fuerza bruta contra el login. Las vulnerabilidades de WordPress suelen venir de **plugins de terceros**, no del core.

EstÃ¡ escrita en **Ruby**. En Kali viene/instala fÃ¡cil; en Windows requiere instalar Ruby primero (de ahÃ­ los problemas de la clase).

| |
|---|
|# InstalaciÃ³n en Debian/Kali<br><br>sudo apt install -y build-essential ruby ruby-dev<br><br>gem install wpscan<br><br># Uso bÃ¡sico: enumerar la web objetivo<br><br>wpscan --url http://academy.thl|
|**â„¹ï¸Â  API Token de WPScan**<br><br>WPScan ofrece un **API token gratuito** (tras registro) que enriquece los resultados con la base de datos de vulnerabilidades. Se pasa con --api-token <TOKEN>.|
|**âš ï¸Â  Estado de la prÃ¡ctica al cierre**<br><br>La clase terminÃ³ **instalando Ruby/WPScan en Windows** sin llegar a lanzar el escaneo completo ni a la explotaciÃ³n. Carlos lo dejÃ³ para la **sesiÃ³n siguiente**, donde se harÃ­a la mÃ¡quina entera desde Windows (vÃ­a WSL si hace falta).<br><br>**No se inventan aquÃ­ credenciales, versiones, plugins ni flags**: no aparecieron en el material.|

# 5. Herramientas utilizadas en la sesiÃ³n

|**Herramienta**|**Objetivo**|**Fase**|**Comando / uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|Burp Suite|Framework de auditorÃ­a web (proxy, Intruder, Repeaterâ€¦)|ExplotaciÃ³n web|Proxy 127.0.0.1:8080 + CA cert|Practicada|Tu dÃ­a a dÃ­a ante cualquier web|
|Foxy Proxy|Conmutar el proxy del navegador hacia Burp|Config. web|Host 127.0.0.1 : 8080|Introducida|ExtensiÃ³n de Firefox/Chrome|
|Wappalyzer|Detectar tecnologÃ­as de la web|Enum. web|ExtensiÃ³n de navegador|Introducida|DetectÃ³ WordPress|
|netdiscover|Descubrir hosts de la red interna|Reconocimiento|netdiscover -r <rango>|Practicada|Primer paso en red local|
|SecLists|Diccionarios de fuzzing/contraseÃ±as|Enum. web|directory-list-2.3-medium.txt|Introducida|Repo de referencia en GitHub|
|Feroxbuster / Gobuster / Dirsearch|Fuzzing de directorios web|Enum. web|-u URL -w wordlist|Practicada|Alternativas; en Windows, script propio|
|WPScan|Enumerar WordPress (plugins, users, versiÃ³n)|Enum. web|wpscan --url <URL>|Introducida|Ruby; API token gratuito|
|HackTricks|DocumentaciÃ³n de metodologÃ­a|Apoyo|Rutas WP, file uploadâ€¦|Recurrente|"Biblia del hacking"|
|curl|Lanzar peticiones HTTP|Enum. web|Peticiones desde PowerShell|Practicada|Sustituto puntual de Burp/Repeater|
|PowerShell|Entorno alternativo de ataque|Soporte|Scripts de enumeraciÃ³n|Practicada|Plan B cuando la Kali falla|

# 6. Comandos importantes

| |
|---|
|# Reconocimiento de red<br><br>ip a<br><br>netdiscover -r 192.168.1.0/24<br><br># Diccionarios<br><br>git clone https://github.com/danielmiessler/SecLists<br><br># Fichero hosts (mapear dominio -> IP)<br><br># Linux:Â Â  /etc/hosts<br><br># Windows: C:\Windows\System32\drivers\etc\hosts<br><br>192.168.1.XÂ Â Â  academy.thl<br><br># Rutas WordPress a comprobar<br><br># /wordpress/license.txtÂ Â  /wp-login.phpÂ Â  /wp-admin/Â Â  /wp-content/uploads/<br><br># WPScan (Kali)<br><br>sudo apt install -y build-essential ruby ruby-dev<br><br>gem install wpscan<br><br>wpscan --url http://academy.thl --api-token <TOKEN>|

# 7. Riesgos, errores comunes y buenas prÃ¡cticas

| |
|---|
|**âš ï¸Â  Errores comunes**<br><br>Definir Burp solo como "un proxy": es un **framework**; el proxy es su nÃºcleo.<br><br>Lanzar el **Intruder sin payload** (no hace nada) o fuzzear varios parÃ¡metros a la vez.<br><br>Olvidar **instalar el certificado de la CA de Burp** â†’ las webs HTTPS fallan al interceptar.<br><br>No habilitar el **DHCP** de la NAT Network â†’ la VM coge IP incorrecta.<br><br>Editar el hosts de Windows **sin permisos de administrador** â†’ no deja guardar.|
|**âœ…Â  Buenas prÃ¡cticas**<br><br>Usar **Target â†’ Scope** para filtrar ruido al auditar.<br><br>Conocer **dÃ³nde estÃ¡ el control** (front local) frente a lo que corre en el servidor.<br><br>Confirmar tecnologÃ­a con **Wappalyzer** antes de elegir herramienta (WordPress â†’ WPScan).<br><br>Mapear siempre **dominio â†’ IP** en el hosts en mÃ¡quinas tipo HTB.<br><br>Tener un **plan B en Windows/PowerShell** por si la Kali falla.<br><br>Trabajar **solo en laboratorios y entornos autorizados**.|

# 8. ConexiÃ³n con sesiones anteriores

â€¢Â Â Â Â  **Mr. Robot:** ya se vio el **302 redirect a `wp-login.php`** y el uso del **Intruder** para fuerza bruta sobre WordPress. Hoy se formaliza la metodologÃ­a.

â€¢Â Â Â Â  **RickdiculouslyEasy / Mr. Robot:** se retoma el vector **file upload â†’ web shell**, mencionado hoy como objetivo en wp-content/uploads.

â€¢Â Â Â Â  **SesiÃ³n OWASP/Web/Burp (29/06):** introducciÃ³n a Burp; hoy se completa con la configuraciÃ³n real (proxy + certificado) y todos sus mÃ³dulos.

â€¢Â Â Â Â  **Wireshark:** el trÃ¡fico de fondo "heartbeat" que vimos capturando paquetes explica por quÃ© el Scope de Burp es necesario para filtrar ruido.

â€¢Â Â Â Â  **Fases de pentesting (prework):** se aplican de nuevo, esta vez como subauditorÃ­a del servicio web.

â€¢Â Â Â Â  **Fuzzing de directorios:** misma idea que Feroxbuster/Gobuster/Dirsearch de sesiones previas, ahora con SecLists y, en Windows, script propio.

# 9. Resumen final

Burp Suite es un **framework de auditorÃ­a web** cuyo corazÃ³n es el **proxy**: interceptamos la peticiÃ³n en el navegador (donde tenemos el control, antes del cifrado TLS) para leerla y modificarla, saltÃ¡ndonos los controles de **front**. La defensa moderna securiza el **back** y aÃ±ade un **WAF**.

ConfiguraciÃ³n real: instalar el **certificado de la CA de Burp** y enrutar el navegador con **Foxy Proxy** a 127.0.0.1:8080. MÃ³dulos clave: **Proxy, Target/Scope, Intruder** (fuerza bruta/fuzzing con sus 4 tipos de ataque), **Repeater** (repetir peticiones), **Decoder, Comparer, Sequencer**.

En la prÃ¡ctica se iniciÃ³ la auditorÃ­a de una web **WordPress**: enumeraciÃ³n de directorios con **SecLists**, identificaciÃ³n con **Wappalyzer**, mapeo de dominio en el fichero **hosts**, rutas tÃ­picas vÃ­a **HackTricks** y enumeraciÃ³n activa con **WPScan**. La explotaciÃ³n **queda pendiente** para la siguiente sesiÃ³n por incidencias tÃ©cnicas (Kali rota, WPScan en Windows).

# 10. Checklist de repaso

â€¢Â Â Â Â  Â¿SÃ© definir Burp como **framework de auditorÃ­a web** y explicar por quÃ© el proxy es dependencia crÃ­tica?

â€¢Â Â Â Â  Â¿Entiendo la diferencia **front vs back** y dÃ³nde tengo el control?

â€¢Â Â Â Â  Â¿SÃ© instalar el **certificado de la CA de Burp** y configurar **Foxy Proxy** (127.0.0.1:8080)?

â€¢Â Â Â Â  Â¿Distingo los 4 tipos de ataque del **Intruder** (Sniper, Battering ram, Pitchfork, Cluster bomb)?

â€¢Â Â Â Â  Â¿SÃ© para quÃ© sirven **Repeater, Decoder, Comparer, Sequencer**?

â€¢Â Â Â Â  Â¿Entiendo el papel de un **WAF** y por quÃ© los controles de front son bypasseables?

â€¢Â Â Â Â  Â¿SÃ© editar el fichero **hosts** en Linux y Windows para mapear dominio â†’ IP?

â€¢Â Â Â Â  Â¿Conozco las rutas tÃ­picas de **WordPress** y el vector **file upload â†’ web shell**?

â€¢Â Â Â Â  Â¿SÃ© enumerar WordPress con **WPScan** (versiÃ³n, plugins, usuarios)?

# 11. ActualizaciÃ³n del registro de herramientas

Para copiar a la base de conocimiento del proyecto. Cambios de esta sesiÃ³n:

|**Herramienta**|**Nivel anterior**|**Nivel ahora**|**Motivo del cambio**|
|---|---|---|---|
|Burp Suite|Practicada|Practicada|SesiÃ³n completa de mÃ³dulos y configuraciÃ³n real|
|Foxy Proxy|â€” (nueva)|Introducida|ConfiguraciÃ³n del proxy del navegador hacia Burp|
|Wappalyzer|â€” (nueva)|Introducida|DetecciÃ³n de tecnologÃ­as web|
|SecLists|â€” (nueva)|Introducida|Repositorio de diccionarios para fuzzing|
|WPScan|Mencionada|Introducida|EnumeraciÃ³n activa de WordPress (Ruby + API token)|
|HackTricks|â€” (referencia)|Recurrente|MetodologÃ­a y rutas WordPress|
|curl|Practicada|Practicada|Usado como sustituto puntual del Repeater en PowerShell|
|netdiscover|Practicada|Practicada|Reconocimiento de red en la mÃ¡quina prÃ¡ctica|

| |
|---|
|**â„¹ï¸Â  Pendiente para la prÃ³xima sesiÃ³n**<br><br>Completar la mÃ¡quina **Academy** (WordPress) **desde Windows** (posible WSL): lanzar WPScan completo, fuerza bruta del login si procede y explotaciÃ³n (file upload â†’ shell).<br><br>Profundizar en Burp con mÃ¡s ejercicios prÃ¡cticos hasta final de curso (es herramienta de uso diario).|

â†’

â†’

â†’
â†’
