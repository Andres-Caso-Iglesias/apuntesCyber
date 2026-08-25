> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 29**
> **Módulo:** MODULO3
> **Tema:** Clase 29
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 29. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos** (vuelta de Barcelona donde dio un curso de 8 horas en 2 días).

Es una clase práctica de viernes con un alumno voluntario, **John**, que ejecuta en vivo mientras Carlos va guiando.

El resto del grupo sigue en paralelo o toma notas para repetirlo después.

**Máquina:** "Ridiculously Easy" --- se descarga como archivo `.zip` desde la descripción de la clase en el campus de Evolve, se descomprime y el archivo `.ovf` se importa con doble clic en VirtualBox.

**Configuración de red:** ambas máquinas (Kali y la víctima) en la misma **Red NAT interna** (la misma red que se creó para Metasploitable 2) para tener visibilidad entre ellas.

**Dinámica pedagógica:** Carlos propone dos formas de sacar partido a las clases prácticas: 1.

Seguir punto a punto copiando comandos (aprende lo que hace cada cosa). 2.

Entender el proceso conceptual y repetirla sola después (aprende a pensar).

Recomienda combinar ambas.

El hilo conductor: **cuanto mejor sea la enumeración, menos tiempo se pierde en la explotación**.

**Estructura del CTF:** 120 puntos en total.

Cada flag vale 10 puntos.

**Hardware recomendado para hacking ofensivo:** portátiles con GPU y mucha RAM (el profesor usa MSI de su empresa, Cibersia Security).

La GPU es necesaria para Hashcat, múltiples VMs y laboratorios de AD.

Para Blue Team o normativa, una máquina mucho más sencilla es suficiente.

Los Mac funcionan bien (Castillo lo usa), pero la virtualización es un coñazo hasta que se tiene todo configurado.

## 2.

Metodología de reconocimiento de red

### Paso 1 --- Identificar la propia IP

ifconfig # Ver la interfaz y la IP de Kali (ej. 10.0.2.3)

### Paso 2 --- Descubrir la IP de la víctima

**netdiscover** (protocolo ARP):

```bash
sudo netdiscover -r 10.0.2.0/24
```

- Flag `-r`: lanzar a un rango de red (obligatorio para rango, `-i` para IP concreta).
- `--help` en cualquier herramienta muestra los flags disponibles.
- **AWS no acepta ARP** → usar Nmap con `-Pn` en ese entorno.
- La propia máquina víctima muestra su IP en pantalla al arrancar, pero se hace el proceso completo para simular un ataque real.

### Paso 3 --- Escaneo inicial de puertos (puertos comunes)

```bash
nmap -sV IP_OBJETIVO
```

Resultado de la demo: - **Puerto 21** → FTP (vsftpd 3.0.3) - **Puerto 22** → ? (nmap no está seguro de que sea SSH, pone interrogación) - **Puerto 80** → HTTP (Apache 2.4.27) - **Puerto 9090** → Cockpit Web Service v161

> [!important] **Importante:** los puertos no son todos iguales.

Lo que importa es el **servicio y la versión**, no el número de puerto en sí.

## 3.

Marco de vectores de ataque por servicio

Para cualquier servicio (FTP, SSH, Telnet, SMB...) existen siempre los mismos vectores:

Vector Descripción
 ---------------------------- -------------------------------------------------------------
 **Fuerza bruta** Si tiene login y no hay rate limit ni bloqueo de cuenta
 **Versión vulnerable** CVE conocido → exploit disponible en Exploit-DB o Metasploit
 **Credenciales conocidas** Obtenidas de otro servicio, filtración o mala configuración
 **Misconfiguration** Configuración incorrecta (ej.

FTP anónimo habilitado)

## 4.

Puerto 21 --- FTP (vsftpd 3.0.3)

### searchsploit

searchsploit vsftpd 3.0.3

Resultado: solo hay un exploit de **DoS** (Denial of Service) --- no sirve para RCE.

Sin exploit útil.

### Verificar FTP anónimo

Nmap con `-sC` (scripts por defecto) detecta automáticamente si el FTP permite sesión anónima.

**En este caso:** FTP anónimo **sí** está habilitado.

Conectarse:

ftp -a IP_OBJETIVO # Flag -a = anonymous (ahorro de teclear usuario/contraseña)

> [!important] ### Concepto clave: la shell del FTP no es una shell de Linux

Cuando se entra en un servicio (FTP, base de datos, VNC...) lo que se obtiene es **la shell de ese servicio**, no la shell completa del sistema Linux.

ftp> ? # Ver todos los comandos disponibles en esta shell ftp> ls # Funciona ftp> cat flag.txt # NO funciona — cat no existe en la shell FTP ftp> pwd # Ver directorio actual ftp> get flag.txt # Descargar el fichero a Kali ftp> put fichero # Subir fichero (si se tienen permisos de escritura)

**Concepto: raíz del FTP ≠ raíz del sistema**

La raíz del FTP es la carpeta donde está montado el servicio.

Todo lo que está "a la izquierda" de esa ruta en el sistema de ficheros NO es accesible.

El usuario que interactúa no es el usuario humano, sino la **cuenta de servicio FTP** (con sus propios permisos, limitados a lo que tiene configurado).

**Modo pasivo vs. activo:** - FTP usa dos conexiones: una para comandos y otra para transferencia de datos. - `passive` en la shell FTP alterna entre modo pasivo y modo activo. - Modo activo = más rápido; modo pasivo = más compatible con NATs y firewalls.

### Navegación y descarga de la flag

ftp> ls # Ver contenido → aparece flag.txt ftp> get flag.txt # Descarga a la carpeta local de Kali ftp> exit cat flag.txt # Leer la flag desde Kali → 10 puntos

**Intentar subir ficheros con anonymous:** no permitido por permisos de escritura.

Con un usuario real del FTP (no anónimo) sí sería posible, y si la carpeta FTP coincide con el servidor web, subir un PHP malicioso → RCE.

## 5.

Puerto 80 --- Introducción al hacking web

Carlos introduce el módulo de hacking web que vendrá a continuación (\~2 meses dedicados).

Las vulnerabilidades de hoy son sencillas pero asientan conceptos fundamentales.

### Fundamentos cliente-servidor repasados

- **Frontend (cliente):** HTML, CSS, JavaScript --- lo que el usuario ve.
- **Backend (servidor):** PHP, Python, Java, .NET --- donde se ejecuta la lógica.
- **GET:** pide información al servidor.
- **POST:** envía información al servidor.

El código fuente visible desde el navegador (`Ctrl+U` / clic derecho → Ver código fuente) es **solo el frontend**.

No es el código del servidor.

### Metodología de reconocimiento web --- "sota, caballo, rey"

Antes de intentar explotar nada, **conocer la página**:

1. **Ver el código fuente** → buscar comentarios, credenciales hardcodeadas, directorios ocultos.

Más de 20-30 líneas: pasárselo a la IA para que resuma lo importante.

2. **robots.txt** → indica qué URLs no se quieren indexar en Google.

Es lo primero que mira un auditor:

http://IP/robots.txt

Demo: PP → no tiene nada; PSOE → sitemap con muchos directorios; Vaticano → también tiene robots.txt.

3. **Fuzzing de directorios** --- siempre obligatorio en cualquier web:

dirsearch -u http://IP_OBJETIVO

### Herramientas equivalentes: DirBuster, Gobuster, Feroxbuster, DIRB. **Todas usan diccionarios**; mismas herramientas con mismo diccionario → mismos resultados.

La diferencia entre herramientas es el diccionario por defecto.

 **Códigos de respuesta:**

 - 200 → existe y hay acceso ✓
 - 403 → existe pero acceso denegado
 - 404 → no existe

4. **Consola del navegador (DevTools → Network)** → ver peticiones HTTP enviadas, parámetros de la URL, cookies.

### Hallazgos en la web de la máquina

**robots.txt** encontró: - `/CGI-BIN/` → 403 (existe pero sin acceso) - `/supercoolwebpage/` → accesible

**Fuzzing con dirsearch** encontró: - `/passwords/` → ¡directorio accesible! - `flag.txt` → 10 puntos más - `passwords.txt` → contraseña en texto claro: "**Winter**"

**Código fuente de los ficheros HTML** → comentario con contraseña hardcodeada.

Técnica del `tree -w` vía command injection para ver el árbol completo:

IP; tree -w

Resultado: estructura completa de la web → `cgi-bin/`, `HTML/` (con `index.html`, `/passwords/` con flag.txt y passwords.txt, `robots.txt`).

Confirma que no hay más directorios que explorar.

## 6.

Command Injection --- "la idea feliz"

### Descubrimiento de la vulnerabilidad

La página en `/supercoolwebpage/` tiene una funcionalidad de **traceroute**: un campo de texto donde el usuario mete una IP y el servidor ejecuta `traceroute IP` mostrando el resultado.

En la pestaña Network del navegador se ve la petición:

ip=10.0.2.15

El parámetro se llama `ip`.

El backend ejecuta: `traceroute $ip`.

**Si el programador no sanitiza el input**, se puede inyectar comandos usando el operador punto y coma (`;`):

10.0.2.15; uname -a

El servidor ejecuta: `traceroute 10.0.2.15 ; uname -a`

Resultado: muestra el output del traceroute **y** el output de `uname -a` → Apache, sistema operativo confirmado → **Command Injection confirmada**.

### Defensa: por qué ocurre

El programador no puso un filtro que verifique que el input sea **solo una IP** (formato número.número.número.número).

Sin ese filtro, cualquier carácter especial puede romper el comando original e inyectar uno nuevo.

### Defensas posibles: - Validar el formato: solo `N.N.N.N`. - Blacklist de caracteres especiales (`;`, `|`, `&&`). - URL encoding de los caracteres especiales (llegan como `%27`, `%3B`...).

### Explotación: leer /etc/passwd

**Problema:** `cat` está bloqueado con un alias personalizado en este servidor.

Alternativa:

IP; head -200 /etc/passwd

Resultado: muestra los usuarios del sistema.

**Leer el** `/etc/passwd`**:**

El fichero `/etc/passwd` tiene este formato:

usuario:x:UID:GID:descripción:carpeta_home:shell

**Usuarios reales del sistema** = los que tienen `/bin/bash` al final. **Cuentas de servicio** = los que tienen `/usr/sbin/nologin` o `/bin/false`.

Usuarios reales encontrados: `root`, `Rick Sanchez`, `Morty`, `Summer`.

Con la contraseña "Winter" encontrada en `passwords.txt` → candidato lógico: **Summer** (por la temática Rick y Morty: Summer + Winter).

## 7.

Puerto 9090 --- Cockpit Web Service

**Cockpit** es un panel de administración web para servidores Linux.

Permite gestionar servicios, ver logs, abrir terminales y más --- acceso casi total al servidor.

### Accesible en: `http://IP:9090`

Con las credenciales obtenidas: `Summer` / `Winter` → **acceso al panel de Cockpit** → control casi total del servidor.

**Lección:** a veces el puerto más interesante no es el 80 sino un servicio de administración en un puerto alto.

Siempre hay que enumerar **todos** los puertos.

## 8.

Metodología avanzada de Nmap en pentesting real

### Cuándo usar `-p-` (todos los puertos)

El escaneo de todos los puertos genera mucho ruido.

Carlos explica cuándo usarlo:

# Opción 1: Solo puertos comunes (primeros escaneos)

```bash
nmap -sV IP
```

# Opción 2: Todos los puertos (cuando los comunes no dan suficiente)

```bash
nmap -sCV -p- IP
```

**Regla práctica:** primero escanear los puertos comunes.

Si se han explotado todos los servicios encontrados y no se llega a root, entonces lanzar el escaneo completo.

No al revés --- genera ruido innecesario y puede ralentizar o alertar.

### Nmap en entornos reales

Carlos admite que en la vida real nunca le han pillado por un Nmap.

Si alguien tiene un IDS que detecta Nmap, hay 1000 formas alternativas de hacer fingerprinting sin Nmap (paquetes ARP, passive reconnaissance, Shodan...).

**Script para escanear un rango de IPs con todos los puertos:**

n=0 while [ $n -le 255 ]; do nmap -sCV -p- --min-rate 1500 10.0.2.$n & n=$((n+1)) done

En la práctica real, los becarios hacen esto manualmente o con scripts similares.

## 9.

Concepto de Rabbit Hole

Un **Rabbit Hole** (madriguera) es un camino de investigación que parece prometedor pero no lleva a ningún lado.

Muy común en CTFs.

El puerto 9090 (Cockpit) durante la clase fue un ejemplo previo al acceso con Summer/Winter: el fuzzing de directorios no encontró nada extra, el código fuente no tenía información útil, no había funcionalidades interactivas visibles.

Carlos lo usó intencionalmente para ilustrar que hay que **saber cuándo parar y volver a la enumeración inicial**.

**Señales de que estás en un Rabbit Hole:** - Llevas mucho tiempo en un path sin encontrar nada nuevo. - Los directorios dan 403/404 sistemáticamente. - No hay funcionalidades con las que interactuar.

Cuando se llega a ese punto: **volver al inicio y revisar si la enumeración fue completa**.

## 10.

Feedback de alumnos sobre Dani

Durante la clase, un alumno (en representación de varios) transmitió a Carlos feedback sobre las clases de Dani: sabe mucho pero va muy deprisa, da pocos ejemplos del día a día y asume un nivel técnico superior al del grupo.

Carlos lo recibió bien y se comprometió a hablar con Dani, Yuba y Castillo para mejorar el ritmo y añadir más contexto a sus explicaciones.

## 11.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
---------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------
 *Metrotable / MetaProtable / Metrasprotable* **Metasploitable 2** -- máquina vulnerable para práctica
 *Ridiculusly Easy / máquina ridiculous* "**Ridiculously Easy**" -- nombre de la máquina CTF de esta clase
 *animab / N más / Animab* **Nmap** -- escáner de puertos y servicios
 *Net Descubrir / Net Desco* **netdiscover** -- herramienta de descubrimiento de red por ARP
 *VSFTPD 3 0 3* **vsftpd 3.0.3** -- versión del servidor FTP de la máquina
 *Cockpit Web Service 161* **Cockpit** -- panel de administración web para Linux (versión 161)
 *guión a de FTP* `ftp -a` -- flag para conectarse al FTP como usuario anónimo
 *passive / activo* **Modo pasivo/activo FTP** -- modos de transferencia de datos del protocolo FTP
 *trace root / Trailsut / transferrute* **traceroute** -- herramienta de diagnóstico que muestra los saltos de red hasta un destino
 *Command Injecttion / inyectar comandos* **Command Injection** -- vulnerabilidad web que permite ejecutar comandos del servidor
 *fooder / footer / fucear* **fuzzing** de directorios -- enumerar rutas de una web con un diccionario
 *Deep Search / DirSearch / der search* **dirsearch** -- herramienta de fuzzing web
 *GoBuster / GoogleBaster* **Gobuster** -- herramienta de fuzzing web
 *supercool web page / supercoolwebpage* `/supercoolwebpage/` -- directorio encontrado en la web de la máquina
 *CGBIN / CGI-BIN* **/cgi-bin/** -- directorio de scripts CGI (403 en esta máquina)
 *robots punto TXT / RobotTXT* **robots.txt** -- fichero que lista URLs que no se quieren indexar en buscadores
 *Rabbit Hole / madriguera* **Rabbit Hole** -- camino de investigación sin salida en CTFs
*sota caballo rey* "**sota, caballo, rey**" -- expresión del profesor para la metodología web básica: interactuar con la página, código fuente, fuzzing de directorios
 *Claudia / Claudio / el Claude* **Claude** (Anthropic) -- IA que los alumnos usaron para resolver dudas durante la clase
 *Cibersia Security / Cybersias* **Cibersia Security** -- empresa de ciberseguridad del profesor Carlos
 *guión p guión / guión pe guión* `-p-` -- flag de Nmap para escanear todos los puertos (1-65535)
 *IDS / la herramienta que detecta Nmap* **IDS** (*Intrusion Detection System*) -- sistema de detección de intrusiones

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*