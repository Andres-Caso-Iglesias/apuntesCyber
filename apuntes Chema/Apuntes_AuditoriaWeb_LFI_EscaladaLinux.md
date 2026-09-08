| **Campo**     | **Detalle**                                                   |
| ------------- | ------------------------------------------------------------- |
| Sesión        | Auditoría web y escalada de privilegios en Linux              |
| Instructor    | Carlos Gómez Pintado                                          |
| Fecha         | 08/07/2026                                                    |
| Bloque        | Repaso práctico de auditoría web + adelanto de escalada Linux |
| Tipo de clase | Práctica end-to-end sobre máquina real (TheHackerLabs)        |

| |
|---|
|**INFO**<br><br>Esta sesión combina dos bloques: vulnerabilidades web basadas en rutas y parámetros (Path Traversal, LFI, RFI, IDOR) y un adelanto de escalada de privilegios en Linux (permisos, SUID frente a sudoers, bit inmutable con chattr/lsattr, y tareas programadas cron). El vehículo práctico es la máquina "Banco" de TheHackerLabs, resuelta en directo de principio a fin.|

| |
|---|
|**INFO**<br><br>El instructor recalca varias veces que la escalada de privilegios se ve aquí "por encima", como cimientos. El módulo completo y dedicado de escalada llega a la vuelta de verano. El objetivo hoy es que los conceptos suenen, no dominarlos.|

# 1. Objetivos de la sesión

• Entender qué es un path (ruta) y en qué consiste una vulnerabilidad de Path Traversal (salto de directorio con `../`).

• Diferenciar Path Traversal, LFI (Local File Inclusion), RFI (Remote File Inclusion) e IDOR.

• Repasar el modelo de permisos de Linux: las 10 posiciones, owner/group/others y el cálculo binario (4-2-1).

• Distinguir un bit SUID de un permiso sudoers (`sudo -l`).

• Comprender el atributo inmutable y el uso de `chattr`/`lsattr` como técnica de escalada.

• Resolver la máquina Banco (TheHackerLabs) end-to-end: enumeración, acceso vía LFI y escalada a root.

# 2. Conceptos clave

## 2.1. Permisos de Linux

Al listar un fichero (`ls -l`), la primera columna tiene 10 posiciones. La primera indica el tipo (`-` archivo, `d` directorio, `l` enlace). Las 9 restantes se dividen en tres grupos de tres:

| **Grupo** | **Posiciones** | **Significado** |
|---|---|---|
| Owner (propietario) | 1ª, 2ª, 3ª | Un usuario concreto |
| Group (grupo) | 4ª, 5ª, 6ª | Grupo de usuarios (si no hay definido, por defecto es el propio owner) |
| Others (el resto) | 7ª, 8ª, 9ª | Cualquier otro usuario |

Cada grupo tiene tres permisos en orden fijo: lectura (`r`), escritura (`w`) y ejecución (`x`).

El valor binario de cada permiso es una potencia de 2: `r = 4`, `w = 2`, `x = 1`. La suma máxima por grupo es 7 (`rwx`).

| **Octal** | **Binario** | **Permisos** | **Significado** |
|---|---|---|---|
| 7 | 111 | rwx | Lectura + escritura + ejecución |
| 6 | 110 | rw- | Lectura + escritura |
| 5 | 101 | r-x | Lectura + ejecución |
| 4 | 100 | r-- | Solo lectura |
| 1 | 001 | --x | Solo ejecución |
| 0 | 000 | --- | Sin permisos |

**Ejemplo:** `755` significa owner con todo (`7 = rwx`), y grupo y others con lectura y ejecución (`5 = r-x`).

### `chmod` (change mode)

`chmod` cambia permisos. Con letras se puede sumar (`+`) o quitar (`-`) un permiso a la vez sobre las tres posiciones: `chmod -x fichero` quita ejecución a owner, group y others simultáneamente.

Con números octales se especifican los tres grupos de golpe, que es lo más cómodo y exacto.

## 2.2. Path — la ruta

Un **path** es la ruta a un archivo concreto, p. ej. `/etc/hosts`. El punto (`.`) representa el directorio actual, y `..` representa el directorio superior (padre). Por eso `cd ../../../` retrocede tres niveles.

| |
|---|
|**⚠ AVISO**<br><br>Poner `cd ..` para retroceder **NO** es Path Traversal: ahí estás ejecutando un comando. El Path Traversal aparece cuando un **parámetro** que apunta a un fichero (una variable que la aplicación usa para abrir/leer un archivo) está mal controlado y permite inyectar `../` para escapar del directorio previsto.|

## 2.3. Path Traversal, LFI y RFI

### Path Traversal (Directory Traversal)

Se da cuando una variable/parámetro que la app usa para localizar un fichero **no está validada**, y se puede inyectar `../../../` para salir del directorio base y acceder a otros ficheros del sistema.

### LFI (Local File Inclusion)

Es la consecuencia del Path Traversal. Permite acceder a (o incluir) un fichero local del sistema a través de esa variable mal controlada. Ejemplo clásico de lectura: `/etc/passwd`.

### RFI (Remote File Inclusion)

En lugar de leer un fichero local, la aplicación hace una llamada remota (a un servidor externo) e incluye/ejecuta un fichero que nosotros alojamos. Se explota levantando un servidor propio (p. ej. `python3 -m http.server`) y forzando a la máquina objetivo a solicitarlo.

| |
|---|
|**✓ Patrón vulnerable (LFI)**<br><br>Ejemplo de código PHP vulnerable descrito en clase: se toma el nombre del fichero de un parámetro (`$_GET['nombre']` o similar), se concatena directamente a un directorio base y se hace `readfile()` / `file_open()` sin validación. Si el nombre es `../../../etc/passwd`, se escapa del directorio base y se lee el fichero del sistema.|

## 2.4. IDOR (Insecure Direct Object Reference)

Distinto del Path Traversal. Se da cuando un recurso se referencia por un identificador directo (p. ej. `?id=3`) **sin control de acceso**. Cambiando ese identificador (`?id=4`, `?id=5`...) se accede a ficheros o registros que no deberían corresponder al usuario.

En la sesión se mostró sobre una URL con un id numérico que, al modificarse, devolvía documentos distintos.

## 2.5. Enumeración: código fuente y ficheros PHP comunes

Revisar el **código fuente** de una web es un paso fundamental: es frecuente encontrar credenciales hardcodeadas o comentarios de desarrolladores. En la máquina Banco, el usuario y contraseña del panel de login estaban en el código fuente.

Ficheros PHP habituales que conviene mirar en cualquier servidor PHP/Apache/Linux (especialmente si hay Path Traversal/LFI):

• `config.php` (suele contener credenciales o rutas de base de datos)

• `phpinfo.php`

• `php.ini`

• `phpMyAdmin`

• El clásico `/etc/passwd`

| |
|---|
|**ℹ NOTA**<br><br>`/etc/passwd` solo habilita saber qué usuarios existen y hacer fuerza bruta; **no contiene contraseñas**. El verdadero premio en un LFI suele ser `config.php` u otros ficheros de configuración con credenciales reales.|

## 2.6. SUID frente a sudoers

Son dos mecanismos distintos y es clave no confundirlos:

| **Mecanismo** | **Afecta a** | **Cómo se detecta** | **Descripción** |
|---|---|---|---|
| **sudoers / `sudo -l`** | El usuario | `sudo -l` | Lista los ficheros/comandos que mi usuario concreto puede ejecutar como otro usuario (no necesariamente root). Es específico de quién lo ejecuta: www-data, root y otro usuario obtendrán resultados distintos. |
| **SUID (Set User ID)** | El fichero | `find / -perm -4000` | Es un bit de permiso especial del fichero. Donde está ese bit, cualquier usuario del sistema ejecuta ese binario con los privilegios del propietario (típicamente root). Afecta al fichero, es común a todos. |

### Cómo se ve el SUID

En `ls -l`, el bit SUID aparece como una `s` en la posición de ejecución del owner (`-rws...`) en lugar de la `x`. Ejemplo visto en clase: `chsh` aparecía como `-rwsr-xr-x`.

## 2.7. Atributo inmutable — `chattr` / `lsattr`

Más allá de los permisos `rwx` existen atributos extendidos. El atributo `i` (inmutable) hace que un fichero no se pueda modificar, borrar, renombrar ni enlazar, ni siquiera por root. Está **por encima** del modelo de permisos normal.

• **`lsattr`** (list attributes): lista los atributos extendidos de ficheros/directorios.

• **`chattr`** (change attributes): cambia atributos. `chattr +i` pone inmutable; `chattr -i` lo quita.

| |
|---|
|**ℹ ¿Para qué sirve la inmutabilidad?**<br><br>Utilidad legítima: proteger ficheros. Un backup que solo debe ejecutarse en momentos concretos se deja preparado y se marca inmutable para que una tarea programada no lo dispare hasta que se le retire el atributo.|

# 3. Desarrollo práctico — Máquina Banco (TheHackerLabs)

Escenario planteado en clase: hemos conseguido acceso a la red interna de un banco (vía WiFi / phishing) y atacamos desde dentro.

## 3.1. Descubrimiento de red y escaneo

Primero identificamos nuestra IP y descubrimos máquinas activas en la red con Netdiscover. Aparece el objetivo `10.0.2.15`. A continuación escaneamos con Nmap.

```bash
netdiscover
nmap -sCV -Pn --min-rate 5000 10.0.2.15
```

Parámetros vistos:

• `-sCV`: detección de versión de servicios + scripts por defecto

• `-Pn`: no hacer ping/host discovery previo

• `--min-rate`: acelerar el escaneo

**Resultado:** puerto 22 (SSH) y puerto 80 (HTTP) abiertos. El 22 no interesa de momento (requiere usuario/contraseña); nos centramos en el 80.

| |
|---|
|**⚠ AVISO**<br><br>El instructor usa la forma abreviada `-sCV`. En la propia clase se comenta que `--min-rate` es la forma correcta con doble guion. Verifica siempre los parámetros con `nmap --help` o `man nmap`.|

## 3.2. Enumeración web

Abrimos el puerto 80 en el navegador: aparece un panel de login.

**Buenas prácticas antes de nada:**

1. Probar credenciales triviales (`admin/admin`)

2. Detectar tecnología con Wappalyzer (revela Debian + Apache 2.4.66)

Se muestra cómo buscar CVEs/vulnerabilidades de esa versión de Apache, aunque en este caso no aportan vector útil.

**El paso decisivo** es revisar el código fuente de la página: al final del HTML hay un script y, en las primeras líneas, un usuario y una contraseña hardcodeados que permiten autenticarse. También se identifica un botón de descarga que apunta a `descargar.php` mediante un campo oculto (`hidden`).

| |
|---|
|**ℹ NOTA**<br><br>Al autenticarse, el escenario cambia por completo: código fuente nuevo, directorios enumerable nuevos, etc. Conviene re-enumerar como usuario autenticado.|

En paralelo se lanza fuzzing de directorios con Dirsearch para descubrir rutas ocultas, dejándolo trabajar en segundo plano mientras se explora la web.

```bash
dirsearch -u http://10.0.2.15/
```

## 3.3. Análisis de descargar.php e identificación del LFI

El botón "descargar" envía una petición POST a `descargar.php` con un parámetro `archivo` (formato `application/x-www-form-urlencoded`). Ese parámetro es la variable que la app usa para localizar el fichero: candidato perfecto a Path Traversal → LFI.

Se intercepta la petición con Burp Suite (Proxy → interceptar) y se envía al Repeater (clic derecho → Send to Repeater, o `Ctrl+R`). Desde Repeater se manipula el parámetro `archivo`.

| |
|---|
|**⚠ ERRORES COMUNES EN BURP**<br><br>En Repeater hay que pulsar **Send** para ver la respuesta (pestaña Response). Si aparece vacía es porque no se ha enviado la petición. Ojo también con el salto de línea: pegar un valor con un `\n` accidental (pulsar Enter al escribir) rompe la petición.|

## 3.4. Explotación del LFI

Inyectando `../` repetidamente en el parámetro `archivo` se escapa del directorio base hasta la raíz y se leen ficheros del sistema. El instructor usa 9 niveles de `../` ("la ruta más larga que me encontré"): con pasarse de niveles no ocurre nada, hay un límite natural (no se puede subir más allá de `/`).

```bash
archivo=../../../../../../../../../etc/passwd
```

Del `/etc/passwd` se extraen los usuarios con shell válida (los que interesan para loguear). Aparecen entre otros `www-data` y `root`.

Pero el paso realmente productivo es leer el fichero de configuración:

```bash
archivo=../../../../../../../../../var/www/html/config.php
```

`config.php` define en sus primeras líneas la ruta del fichero de base de datos (algo tipo `db_supersecret...json`). Leyendo ese JSON aparecen credenciales de varios usuarios (admin, root de base de datos, www-data, debian...).

| |
|---|
|**ℹ Distinguir usuario de servicio vs. sistema**<br><br>La credencial de "root" del JSON era del usuario root de la base de datos (MySQL), no del sistema — por eso SSH con root falló. La que funcionó por SSH fue la del usuario www-data, que casualmente compartía nombre y contraseña entre servicio y sistema.|

## 3.5. Acceso inicial por SSH

Con las credenciales válidas del usuario de sistema, entramos por SSH y obtenemos la primera flag (user).

```bash
ssh www-data@10.0.2.15
```

## 3.6. Enumeración para escalada de privilegios

**Orden de comprobaciones que el instructor fija como rutina** al entrar en cualquier máquina Linux:

```bash
whoami # quién soy
pwd # en qué ruta estoy (al entrar por SSH, típicamente /home/usuario)
uname -a # versión del kernel (por si hay exploit de kernel, p. ej. Dirty Cow)
sudo -l # qué puedo ejecutar como otro usuario/root
find / -perm -4000 -type f 2>/dev/null # binarios con bit SUID
```

En Banco, `sudo -l` no da resultados útiles (incluso da error de resolución de host y no permite listar). Por tanto se pasa a la segunda vía: buscar binarios SUID.

| |
|---|
|**ℹ NOTA**<br><br>`-perm -4000` busca SUID; `-perm -2000` buscaría SGID. En clase se recuerda que el valor 4000 es el peso binario del bit SUID (equivalente en la familia de los especiales a lo que 7 es para rwx).|

## 3.7. Identificación del binario vulnerable (`chattr`) con GTFOBins

El `find` de SUID devuelve una lista. La mayoría son binarios normales y esperables (`sudo`, `su`, `mount`, `umount`, `passwd`, `chsh`, `chfn`, `newgrp`, `gpasswd`...): buscarlos en GTFOBins no aporta nada.

**Lo que chirría** es encontrar `chstr` (y justo encima `lsattr`), comandos que no son habituales en esa lista.

En GTFOBins (Get The F* Out Bins) se busca `chstr`: aparece con sección **SUID** (la técnica que hemos usado para encontrarlo) y **Privilege Escalation**. GTFOBins indica cómo abusar del binario.

| |
|---|
|**✓ Regla de oro de GTFOBins**<br><br>Si encuentras el binario por la vía **SUID** (`find -perm -4000`), en GTFOBins consultas la sección **SUID**. Si lo hubieras encontrado por `sudo -l`, consultarías la sección **Sudo**. La técnica de consulta debe coincidir con cómo lo encontraste.|

La presencia de `chstr` con SUID más `lsattr` justo al lado es una pista deliberada de la máquina: `chstr` permite quitar la inmutabilidad de cualquier fichero (aun de root) porque se ejecuta con privilegios del propietario, y `lsattr` sirve para localizar qué fichero es inmutable.

## 3.8. Localización del fichero inmutable

Se listan los ficheros con atributo inmutable:

```bash
find / -type f -exec lsattr {} \; 2>/dev/null | grep -i '\----i'
```

Fichero encontrado: `/usr/local/bin/backup.sh` (referido en clase como `backup.sh`/`backup.bill.sh`), propiedad de `root:root`, con atributo inmutable.

| |
|---|
|**ℹ Ampliación**<br><br>Este comando `find ... -exec lsattr` es una ampliación para automatizar la búsqueda; en clase el comando exacto se obtuvo pidiéndoselo a la IA. Verifica su comportamiento antes de usarlo y ajústalo a tu entorno.|

## 3.9. Explotación: quitar inmutabilidad, modificar y esperar al cron

Con el SUID de `chstr` retiramos la inmutabilidad del backup y comprobamos que ya no aparece como inmutable:

```bash
chstr -i /usr/local/bin/backup.sh
lsattr /usr/local/bin/backup.sh
```

Ahora tenemos permiso de escritura sobre el script (others con `rwx`).

**El razonamiento crítico de la clase:** no basta con meter `/bin/bash` y ejecutarlo, porque lo ejecutaríamos como `www-data`, no como root. La escalada funciona porque una **tarea programada (cron)** ejecuta ese backup como root periódicamente. Por tanto, dejamos el script preparado para que, al ejecutarse como root, otorgue SUID a una shell.

```bash
echo 'chmod +s /bin/bash' > /usr/local/bin/backup.sh
```

Se espera a que el cron ejecute el script como root (se puede confirmar viendo cambiar el timestamp del fichero con `ls -l` repetido). Tras la ejecución, `/bin/bash` queda con bit SUID y podemos lanzar una shell con privilegios de root:

```bash
ls -la /bin/bash
/bin/bash -p
```

**¡Root conseguido!**

La `-p` es clave: mantiene los privilegios del SUID al lanzar bash. Sin ella, bash suele descartar los privilegios efectivos. Al ejecutarla obtenemos shell de root y la flag final.

### Analogía de la clase (SUID + cron)

El instructor lo explicó con una analogía: tener SUID escribible sin poder ejecutarlo como root es como dejar en el felpudo de una casa un bote de pintura rosa, un rodillo y una brocha. Tú no puedes entrar, pero sabes que cada día a una hora fija alguien (la tarea cron, "la madre") le dirá al dueño que pinte. El dueño (root) ejecuta sin pensar con lo que le has dejado preparado, y la casa acaba pintada de rosa. Has aprovechado una causalidad que se repite (el cron) para que otro con más privilegios ejecute tu preparación.

## 3.10. Regla mental de escalada en CTF (resumen del instructor)

Esquema condicional que sintetiza las vías vistas:

• **Si hay un fichero en `sudo -l`** que puedo ejecutar como otro usuario y tengo permiso de escritura sobre él → escalada directa (lo modifico y lo ejecuto con sudo).

• **Si hay un fichero SUID ejecutable** y puedo escribirlo pero no ejecutarlo como root → hay (casi seguro en CTF) una tarea cron que lo ejecuta como root: lo preparo y espero.

• **Si no se da ninguna de las dos** → buscar un script que al ejecutarse revele una contraseña, o tirar de exploit de kernel.

# 4. Comandos importantes

```bash
# Descubrimiento de red
netdiscover

# Escaneo de puertos
nmap -sCV -Pn --min-rate 5000 10.0.2.15

# Fuzzing de directorios
dirsearch -u http://10.0.2.15/

# Explotación del LFI
archivo=../../../../../../../../../etc/passwd
archivo=../../../../../../../../../var/www/html/config.php

# Acceso inicial por SSH
ssh www-data@10.0.2.15

# Enumeración post-acceso
whoami
pwd
uname -a
sudo -l
find / -perm -4000 -type f 2>/dev/null

# Localizar fichero inmutable
find / -type f -exec lsattr {} \; 2>/dev/null | grep -i '\----i'

# Explotación: quitar inmutabilidad y preparar escalada
chstr -i /usr/local/bin/backup.sh
echo 'chmod +s /bin/bash' > /usr/local/bin/backup.sh

# Escalada a root
ls -la /bin/bash
/bin/bash -p
```

| |
|---|
|**⚠ AVISO**<br><br>Rutas, nombres de fichero y credenciales concretos (`config.php`, `backup.sh`, usuario `www-data`) proceden de la resolución en directo y pueden variar en tu instancia. Trátalos como referencia, no como valores fijos: enumera y confirma en tu máquina.|

# 5. Herramientas utilizadas en la sesión

| **Herramienta** | **Objetivo** | **Fase de auditoría** | **Comando o uso visto** | **Nivel** | **Notas** |
|---|---|---|---|---|---|
| Netdiscover | Descubrir hosts en la red | Reconocimiento | `netdiscover` | Practicada (sube de Introducida) | Localiza el objetivo 10.0.2.15 |
| Nmap | Puertos, servicios y versiones | Enumeración | `nmap -sCV -Pn --min-rate 5000 IP` | Recurrente | Banner grabbing revela versiones |
| Wappalyzer | Detectar tecnología web | Enumeración web | Extensión de navegador | Practicada (confirmada) | Detecta Apache 2.4.66 / Debian |
| Dirsearch | Fuzzing de directorios | Enumeración web | `dirsearch -u URL` | Practicada (nueva) | En 2º plano mientras se explora |
| Burp Suite (Proxy/Repeater) | Interceptar y manipular peticiones | Explotación web | `Ctrl+R` → Send | Practicada (confirmada) | Manipula el parámetro `archivo` |
| FoxyProxy | Gestionar proxy del navegador | Explotación web | Activar/desactivar proxy | Practicada (nueva) | Recordar desactivarlo tras Burp |
| GTFOBins | Vías de abuso de binarios | Escalada de privilegios | Buscar `chstr` → SUID | Practicada (nueva) | Coincidir técnica (SUID/Sudo) con cómo encontraste el binario |
| `chstr` / `lsattr` | Gestionar atributo inmutable | Escalada de privilegios | `chstr -i fichero` | Introducida (nueva) | Vector SUID de la máquina |
| SSH | Acceso remoto autenticado | Acceso inicial | `ssh usuario@IP` | Recurrente | Login con credenciales del JSON |

| |
|---|
|**ℹ NOTA**<br><br>Se mencionan pero no se desarrollan en profundidad: la máquina Responder (HTB Tier 1) como ejemplo de RFI con `python3 -m http.server`, y las alternativas de fuzzing Feroxbuster/ffuf/Gobuster ("dirbuster recursiva").|

# 6. Riesgos, errores comunes y buenas prácticas

| |
|---|
|**⚠ No uses 777**<br><br>Nunca poner `777` a un fichero "por si acaso": es una mala práctica de seguridad grave que se comentó explícitamente en clase. Da permisos totales a cualquiera.|

| |
|---|
|**⚠ AVISO**<br><br>En Burp Repeater, si la Response sale vacía es que falta pulsar **Send**. Y cuidado con pegar valores con saltos de línea accidentales: un `\n` rompe la petición.|

| |
|---|
|**⚠ AVISO**<br><br>Recordar desactivar FoxyProxy/el proxy de Burp al terminar, o el navegador dejará de cargar páginas normalmente.|

| |
|---|
|**✓ Buena práctica**<br><br>Revisar **SIEMPRE** el código fuente y ficheros de configuración (`config.php`). Es donde con más frecuencia aparecen credenciales hardcodeadas.|

| |
|---|
|**✓ Buena práctica**<br><br>Al leer `/etc/passwd`, distinguir usuarios de sistema (con shell) de usuarios de servicio/base de datos. No toda credencial encontrada sirve para SSH.|

# 7. Conexión con sesiones anteriores

• **Escalada Linux y `sudo -l`**: enlaza directamente con la sesión de la máquina Rockstar, donde ya se trabajó el chain de movimiento lateral, `sudo -l` y el modelo de permisos de Linux. Aquí se añade la vía SUID + cron y el atributo inmutable, que amplían el repertorio de escalada.

• **Enumeración web**: nmap (puertos/servicios) sigue siendo el primer paso, y el fuzzing con Dirsearch cumple el mismo rol que Feroxbuster/ffuf en sesiones previas: descubrir rutas ocultas mientras se inspecciona la web.

• **RFI y Responder**: se retoma la máquina Responder (HTB Tier 1) ya conocida, ahora como ejemplo conceptual de RFI (hostear un fichero propio con `python3 -m http.server` y forzar su inclusión remota).

• **Burp Suite**: se reutiliza el flujo Proxy → Repeater visto en sesiones anteriores, ahora aplicado a manipular un parámetro POST para LFI.

# 8. Resumen final

La sesión encadena una auditoría web completa sobre la máquina Banco (TheHackerLabs) con un adelanto de escalada de privilegios en Linux.

El **acceso inicial** se logra explotando un LFI en `descargar.php` (parámetro `archivo` sin validar), leyendo `config.php` y de ahí las credenciales de base de datos; un usuario de servicio compartía credencial con uno de sistema, habilitando SSH.

La **escalada a root** se apoya en un binario SUID inesperado (`chstr`) identificado vía `find -perm -4000` y GTFOBins: se retira la inmutabilidad de un script de backup, se modifica para dar SUID a `/bin/bash`, y una tarea cron que corre como root lo ejecuta, permitiendo `/bin/bash -p`.

**Conceptos transversales:** permisos de Linux (4-2-1), diferencia SUID vs sudoers, y atributo inmutable con `chstr`/`lsattr`.

# 9. Checklist de repaso

☐ ¿Sé calcular permisos octales (`r=4`, `w=2`, `x=1`) y explicar las 10 posiciones de `ls -l`?

☐ ¿Distingo Path Traversal, LFI, RFI e IDOR con un ejemplo de cada uno?

☐ ¿Sé por qué `../` en un parámetro es peligroso pero `cd ..` en shell no es Path Traversal?

☐ ¿Reviso el código fuente y los ficheros PHP comunes (`config.php`, `phpinfo.php`, `php.ini`, `phpMyAdmin`)?

☐ ¿Manejo el flujo Burp Proxy → Repeater y recuerdo pulsar Send?

☐ ¿Explico la diferencia entre SUID y sudoers sin dudar?

☐ ¿Ejecuto la rutina de escalada: `whoami` → `pwd` → `uname -a` → `sudo -l` → `find -perm -4000`?

☐ ¿Sé consultar GTFOBins coincidiendo la técnica (SUID vs Sudo) con cómo encontré el binario?

☐ ¿Entiendo el rol del cron en la escalada SUID+escritura y la analogía del bote de pintura?

☐ ¿Recuerdo lanzar `/bin/bash -p` (con `-p`) para conservar el SUID?

# 10. Actualización del registro de herramientas

Herramientas nuevas y cambios de nivel respecto al registro acumulado:

| **Herramienta** | **Nivel** | **Cambio** |
|---|---|---|
| GTFOBins | Practicada | NUEVA — vías de abuso de binarios |
| `chstr` / `lsattr` | Introducida | NUEVA — gestión de atributo inmutable |
| FoxyProxy | Practicada | NUEVA — gestión de proxy del navegador |
| Dirsearch | Practicada | NUEVA — fuzzing de directorios |
| Wappalyzer | Practicada | Confirmada — detección de tecnología web |
| Netdiscover | Practicada | Sube de Introducida |
| Burp Suite (Proxy/Repeater) | Practicada | Confirmada |
| SSH | Recurrente | Se mantiene |

---

**Bloque para memoria acumulativa (texto plano):**

En la sesión de auditoría web + escalada Linux (Carlos Gómez Pintado, 08/07/2026) se resolvió la máquina Banco de TheHackerLabs. Vector web: LFI en `descargar.php` (parámetro `archivo`) → lectura de `config.php` → credenciales de BBDD → SSH con usuario de sistema. Escalada: binario SUID inesperado `chstr` hallado con `find -perm -4000` y confirmado en GTFOBins; se quita inmutabilidad de `backup.sh` con `chstr -i`, se inyecta `chmod +s /bin/bash` y un cron que corre como root lo ejecuta; root con `/bin/bash -p`. Conceptos: permisos 4-2-1, SUID vs sudoers, atributo inmutable (`chstr`/`lsattr`), IDOR, Path Traversal/LFI/RFI. Nuevas: GTFOBins, `chstr`/`lsattr`, FoxyProxy.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]] — GoBuster, Hydra, Path Traversal / LFI
- [[Apuntes_Sesion27_XXE_LFI_Nike.md|Apuntes_Sesion27_XXE_LFI_Nike]] — GoBuster, Hydra, Path Traversal / LFI
- [[../apuntes Joselu/MODULO3/resumen_master_clase42.md|resumen_master_clase42]] — GoBuster, Hydra, RFI
- [[../write-ups/Banco-THL.md|Banco-THL]] — Hydra, Linux, Path Traversal / LFI
- [[Maquinas/Rockstar — Escalada Linux y LFI.md|Rockstar — Escalada Linux y LFI]] — GoBuster, Hydra, RFI
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]] — DirSearch, GoBuster, Hydra

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #burpsuite #dirsearch #escalada-privilegios #feroxbuster #ffuf #gobuster #hack-the-box #hydra #idor #lfi #linux #nmap #redes #rfi #ssh #wifi
