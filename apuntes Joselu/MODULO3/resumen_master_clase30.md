> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 30**
> **Módulo:** MODULO3
> **Tema:** Clase 30
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 30. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos**.

Es la continuación directa de la Clase 29, completando la máquina "Ridiculously Easy".

La alumna voluntaria de hoy es **Sira** (nominada por Charchas la semana anterior).

El objetivo es introducir por primera vez los conceptos de **post-explotación**: movimiento lateral entre cuentas y escalada de privilegios hasta root.

**Repaso de la Clase 29 (lo que ya tenemos):** - Puerto 21 (FTP anónimo) → flag.txt descargada con `get` → 10 puntos. - Puerto 22 → TCP envuelto, no funciona (puerto muerto). - Puerto 80 → `robots.txt` → `/supercoolwebpage/` → Command Injection → `/etc/passwd` → usuarios reales: `root`, `Rick Sanchez`, `Morty`, `Summer`.

Directorio `/passwords/` → contraseña `Winter` en comentario del código fuente. - Puerto 9090 → Cockpit Fedora, rabbit hole, nada explotable. - Escaneo `-p-` → puertos extra: **13773** (backdoor con Netcat), **6000** (otra shell directa) y **22222** (SSH real).

**Puntuación acumulada al empezar:** 60 puntos de 120.

## 2.

### Marco conceptual: tipos de cuentas y fases de un pentest

Carlos explica con la pizarra el flujo completo de una auditoría antes de continuar con la máquina.

### Los tres tipos de cuentas en un sistema Linux

Tipo Descripción Directorio Shell
----------------------------- ----------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------- --------------------
**Cuenta de servicio** Gestiona un servicio (FTP, Apache, SSH).

Permisos muy reducidos sobre el sistema pero amplios sobre su servicio Sin `/home`.

Usa el directorio del servicio (ej. `/var/www/html`) `nologin` o `false`
 **Cuenta de usuario** Persona real del sistema.

Puede usar la terminal, tiene `/home/usuario` propio `/home/usuario` `/bin/bash`
 **Cuenta de administrador** Root.

Control total del sistema `/root` `/bin/bash`

**Cómo identificarlos en** `/etc/passwd`**:** - Campo `home`: `/home/X` → usuario real; `/root` → root; ruta de servicio → cuenta de servicio. - Último campo: `/bin/bash` o `/bin/sh` → puede usar terminal; `nologin` → no puede.

### Flujo completo de un pentest

Reconocimiento (netdiscover, Nmap) ↓ Enumeración de servicios (Nmap -sCV) ↓ Explotación → compromiso inicial (normalmente cuenta de servicio: www-data, ftp...) ↓ Movimiento lateral: cuenta de servicio → cuenta de usuario (con /home) ↓ Movimiento lateral entre usuarios (puede haber varios saltos) ↓ Escalada de privilegios → root ↓ Persistencia → Reporte

**Por qué es importante la cuenta de usuario:** tiene `/home` propio donde puede leer, escribir y ejecutar.

Las cuentas de servicio no tienen este espacio y están muy limitadas.

**El directorio** `/tmp` **como alternativa:** cuando se compromete una cuenta de servicio sin `/home`, `/tmp` es escribible y ejecutable para todos.

Es el directorio favorito del atacante para depositar y ejecutar herramientas porque cualquier cuenta puede usarlo.

Por eso los administradores deben monitorizarlo --- ahí suelen aterrizar las herramientas maliciosas.

## 3.

Acceso SSH como Summer (puerto 22222)

Con las credenciales obtenidas en la Clase 29:

```bash
ssh summer@10.0.2.15 -p 22222
```

# Contraseña: Winter

whoami # → summer

**Confirmación:** dentro de la máquina víctima como usuario `summer`.

La terminal que se obtiene es una shell de sistema (Bash), a diferencia de la shell restringida del FTP.

**Por qué trabajar desde Kali en vez de desde la consola de la máquina:** - Desde Kali se tienen todas las herramientas instaladas (exiftool, strings, Hydra...). - Se puede transferir ficheros fácilmente entre máquinas. - Es más cómodo para análisis offline.

### Flag de Summer (10 puntos)

```bash
ls # Aparece flag.txt directamente en el home de Summer head -n 20 flag.txt # CAT está bloqueado con alias → usar head
```

**Total acumulado: 70 puntos.**

## 4.

Enumeración interna del sistema

Cuando se accede a una máquina, siempre hay que **conocerla primero antes de intentar explotar nada**.

Comandos de enumeración interna estándar:

# Ver usuarios del sistema (campos importantes: nombre y shell)

head -n 30 /etc/passwd

# Ver versión del kernel (para buscar exploits de escalada)

uname -a

# Ver permisos sudo del usuario actual

```bash
sudo -l
```

# Buscar binarios con bit SUID

find / -perm -4000 -type f 2>/dev/null

`sudo -l` **en Summer:** resultado: no puede ejecutar nada con sudo.

No significa error --- simplemente no hay vector de sudo para este usuario. **Siempre lanzarlo igual, porque si da resultado es un vector de escalada inmediato.**

**Bit SUID:** similar a los permisos sudo, pero a nivel de fichero.

Un fichero con SUID se ejecuta siempre con los permisos del propietario (aunque lo lance otro usuario).

Si el propietario es root y el fichero tiene SUID → cualquier usuario puede ejecutarlo como root.

Referencia: **GTFOBins** para saber cómo aprovechar binarios SUID.

## 5.

Permisos de Linux: la regla de lectura y escritura para copiar

Uno de los conceptos más importantes de la clase:

**Para copiar un fichero hacen falta exactamente dos condiciones:** 1. **Permiso de lectura (**`r`**) en el fichero origen.** 2. **Permiso de escritura (**`w`**) en la carpeta destino.**

No es necesario tener permiso de ejecución ni de escritura sobre el fichero original.

**Analogía del profesor:** si alguien te presta un libro (permiso de lectura) pero no puedes escribir en él, puedes copiarlo a mano en tus propios folios (donde sí tienes escritura).

El resultado es una copia completa sin tocar el original.

**Práctica:** Summer puede leer ficheros en `/home/RickSanchez/` → los copia a `/home/Summer/` o a `/tmp/` (ambos son carpetas donde Summer tiene escritura).

# Copiar fichero de Rick a la carpeta de Summer

```bash
cp /home/RickSanchez/RickSafe/Safe ../../home/Summer/
```

# O con doble tabulador para autocompletar la ruta

**Color verde en** `ls`**:** indica que el fichero es ejecutable.

## 6.

SCP: transferir ficheros a través de SSH

**SCP** (*SSH Copy*) es la versión segura de `cp` a través de SSH.

Permite copiar ficheros entre máquinas de forma bidireccional.

# Descargar un fichero de la máquina víctima a Kali:

scp -P 22222 summer@10.0.2.15:/home/summer/Safe .

# Subir un fichero desde Kali a la máquina víctima:

scp -P 22222 /home/kali/herramienta.sh summer@10.0.2.15:/home/summer/

# Parámetros:

# -P 22222 → especificar puerto (P mayúscula, distinto de SSH que usa p minúscula)

# usuario@IP:ruta → origen o destino remoto

# . → directorio actual en Kali

**Diferencia SSH vs.

SCP:** - SSH → conexión remota interactiva (terminal). - SCP → transferencia de ficheros a través de SSH.

**Por qué hay que especificar** `-P 22222`**:** por defecto SCP usa el puerto 22.

Como en esta máquina el SSH real está en el 22222, hay que indicarlo explícitamente.

## 7.

Análisis de ficheros con `strings` y `exiftool`

### `strings`

Extrae cadenas de texto imprimibles de cualquier fichero (ejecutables, imágenes, binarios).

Fundamental para análisis de malware y para encontrar pistas en CTFs.

strings Save # Mostrar strings del fichero ejecutable strings SafepassFile.jpg # Mostrar strings de la imagen

En la imagen de Morty (`SafepassFile.jpg`), el comando `strings` reveló una contraseña oculta mediante **esteganografía**.

### `exiftool`

Herramienta de análisis de metadatos.

Disponible en Kali pero no en la máquina víctima.

Por eso hay que transferir los ficheros con SCP a Kali antes de analizarlos.

exiftool SafepassFile.jpg # Ver metadatos de la imagen

**Esteganografía:** técnica para ocultar información dentro de otros ficheros (imágenes, audio, vídeo) modificando píxeles específicos.

### El truco: usar píxeles ya negros para ocultar datos, ya que no deja una huella visual (un píxel negro más no es detectable a simple vista).

## 8.

Carpeta de Morty: ficheros y contraseña oculta en imagen

```bash
ls -la /home/Morty/ # Ficheros: SafepassFile.jpg, journal.txt, archivo.zip
```

### Proceso de investigación

**Paso 1:** Copiar los ficheros a `/home/Summer/` para poder analizarlos.

**Paso 2:** Transferir a Kali con SCP.

**Paso 3:** `strings SafepassFile.jpg` → revela contraseña oculta.

**Paso 4:** Descomprimir el zip con esa contraseña (clic derecho → "Extract here" → introducir contraseña).

**Paso 5:** El zip contiene un `.txt` con un mensaje de Morty a Rick → **flag** (10 puntos) + pista para la contraseña de Rick.

**Total acumulado: 90 puntos.**

## 9.

Fichero `Safe` en la carpeta de Rick

En `/home/RickSanchez/RickSafe/` había un ejecutable llamado `Safe`.

Con `strings Safe` se veía que acepta un argumento en la línea de comandos y tiene lógica de descifrado (función `decrypt`).

El mensaje del zip de Morty revelaba que el argumento correcto para `Safe` era el **número extraño de la flag anterior**.

./Save NÚMERO_DE_LA_FLAG

Resultado: **otra flag** (20 puntos) + pista de contraseña de Rick: "*política de contraseñas: 1 mayúscula + 1 dígito + 1 palabra de mi antigua banda*".

**Total acumulado: 110 puntos.**

## 10.

Generar diccionario con Claude y escalar a root con Hydra

### Política de contraseña de Rick

De la pista obtenida: - 1 letra mayúscula - 1 número - 1 palabra del nombre de la banda ("ABCD" --- nombre ficticio de la banda de Rick)

Claude generó todas las combinaciones posibles → 780 opciones → guardadas en `diccionario.txt`.

### Fuerza bruta con Hydra al SSH de Rick

hydra -l "Rick Sanchez" -P /root/Desktop/diccionario.txt ssh://10.0.2.15:22222

Parámetros de Hydra: - `-l usuario` → usuario concreto (l minúscula). - `-L fichero` → lista de usuarios (L mayúscula). - `-p contraseña` → contraseña concreta (p minúscula). - `-P fichero` → lista de contraseñas (P mayúscula). - `servicio://IP:puerto` → target.

Resultado: contraseña de Rick encontrada → `P7Curtains` (ejemplo).

### Entrar como Rick y escalar a root

```bash
ssh "Rick Sanchez"@10.0.2.15 -p 22222
```

# Contraseña: P7Curtains

whoami # → RickSanchez

```bash
sudo -l # → (ALL) ALL
```

# Rick Sanchez puede ejecutar CUALQUIER comando como sudo

```bash
sudo su # → root whoami # → root
```

**Flag de root:** en `/root/flag.txt` → **últimos puntos, máquina completada.**

**Total final: 120 puntos.

Máquina 100% completada.**

## 11.

Nmap sin `-sCV`: información por convención vs. información real

Una aclaración importante surgida durante la clase:

**Nmap sin** `-sV` **ni** `-sC` devuelve el servicio que *normalmente* corre en ese puerto por convención (ej: puerto 22 → "ssh").

Esto puede ser **falso** si el administrador ha puesto otro servicio en ese puerto.

**Con** `-sCV`, Nmap lanza scripts de detección activa y determina el servicio **real** que está escuchando en ese puerto.

En esta máquina: - Puerto 22 sin `-sCV` → aparece como "ssh" (convención). - Puerto 22 con `-sCV` → confirma que **no es SSH** (TCP wrappado sin servicio real). - Puerto 22222 con `-sCV` → confirma que **sí es SSH**.

Por eso siempre hay que hacer el segundo escaneo con `-sCV` sobre los puertos encontrados.

## 12.

Flujo completo de la máquina "Ridiculously Easy" --- resumen final

netdiscover → IP víctima ↓ nmap -sV → puertos 21, 22, 80, 9090 ↓ FTP anónimo (21) → flag 1 (10pts) ↓ Puerto 80 → robots.txt → /supercoolwebpage/ → traceroute + Command Injection → /etc/passwd → usuarios: Summer, Morty, Rick → /passwords/ + código fuente → contraseña: Winter → flag 2 (10pts) ↓ Puerto 9090 → Cockpit → Rabbit Hole (nada) ↓ nmap -p- → puertos extra: 13773 (backdoor), 6000 (shell), 22222 (SSH real) ↓ SSH summer@IP:22222 / Winter → flag 3 (10pts) ↓ Enumeración interna: sudo -l, /etc/passwd, permisos → /home/Morty/ → SafepassFile.jpg → strings → contraseña del zip → zip → flag 4+5 (20pts) + pista contraseña Rick ↓ /home/RickSanchez/RickSafe/Safe → strings → ejecutar con número → flag 6 (20pts) + política pass ↓ Claude genera diccionario (780 combinaciones) → Hydra → SSH Rick:pass encontrada ↓ sudo -l → ALL ALL → sudo su → root → flag final (pts restantes) ↓ MÁQUINA COMPLETADA: 120/120 puntos

## 13.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
---------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------
 *Ridiculusly Easy / ridiculous* "**Ridiculously Easy**" -- nombre de la máquina CTF
 *SCH / SSH / sch* **SSH** (*Secure Shell*) -- protocolo de acceso remoto seguro
 *guion p guion / guión pe guión* `-p-` -- flag de Nmap para escanear todos los puertos
 *SCV / guion s CV* `-sCV` -- flags de Nmap para detección de versiones y scripts
 *SCP / ese-ce-pe* **SCP** (*Secure Copy Protocol*) -- transferencia de ficheros mediante SSH
 *guion P mayúscula / puerto del SCP* `-P 22222` -- especificar puerto en SCP (P mayúscula, distinto del SSH que usa `-p`)
 *sudo guion l / SUO menos L* `sudo -l` -- lista los comandos que el usuario puede ejecutar como root
 *sudo root / sudo su* `sudo su` -- escalar a root usando sudo
 *el All All de sudo* `(ALL) ALL` -- configuración en sudoers que permite ejecutar cualquier comando como root
 *SUID / SuID / bit de SUID* **SUID** (*Set User ID*) -- bit de permiso especial que hace que un fichero se ejecute con los permisos del propietario
 *GTFOBins* **GTFOBins** (gtfobins.github.io) -- referencia de escalada de privilegios mediante binarios
 *Bimbash / barra bin bash* `/bin/bash` -- shell Bash, indica que el usuario puede usar la terminal
 *no login / nologin* `nologin` -- indica que la cuenta no puede acceder a una shell del sistema
 *JuanMay / JuanMai / Huamai* `whoami` -- comando que muestra el usuario actual
 *barrahome / barra home* `/home` -- directorio donde residen los homes de los usuarios del sistema
 *barra temp / temp / barra TMP* `/tmp` -- directorio temporal con permisos de escritura y ejecución para todos
 *strings* `strings` -- comando que extrae cadenas de texto de cualquier fichero binario
 *Exip Tool / exit tool / exit pool* `exiftool` -- herramienta de análisis de metadatos de ficheros
 *esteganografía / estego / este de ografía* **Esteganografía** -- técnica de ocultación de información dentro de otros ficheros (imágenes, audio)
 *píxel muerto / píxel negro* En esteganografía: píxel donde se ha sustituido la información de color por datos ocultos
 *Rabbit Hole / rabito hold / Rabbit Howl* **Rabbit Hole** -- camino de investigación sin salida en CTFs
 *hydra / la de fuerza bruta* **Hydra** -- herramienta de fuerza bruta para múltiples protocolos
*guion l / guion L / guion p / guion P* `-l usuario` **/** `-L fichero` **/** `-p pass` **/** `-P fichero` -- flags de Hydra (minúscula = valor único, mayúscula = fichero)
 *Claudia / Claude / la IA* **Claude** (Anthropic) -- usado para generar el diccionario de contraseñas basándose en la política de la pista
 *la banda de Rick / Freshie / Presute Inves* **nombre de la banda de Rick Sanchez** -- dato necesario para generar el diccionario de contraseñas

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*
