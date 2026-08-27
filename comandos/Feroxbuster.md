# Feroxbuster — Fuzzing Directorios

> [!info] Herramienta
> Fuzzing de directorios y archivos ocultos en servidores web. Escrit en Rust, rápido y con recursión.
## Escaneo Básico

> [!tip] Primer paso
> Empezar simple y escalar complejidad según necesidad.

```bash

# Escaneo básico
feroxbuster -u http://target

# Con wordlist específica
feroxbuster -u http://target -w /usr/share/wordlists/dirb/common.txt

# 50 hilos
feroxbuster -u http://target -t 50

# Solo resultados
feroxbuster -u http://target --silent
```

### Output

| Comando | Descripción |
|---------|-------------|
| `-o results.txt` | Guardar en archivo |
| `--json` | Output JSON |
| `-v` | Verbose |
| `-vv` | Double verbose |
| | `--debug-log debug.log` | Debug log |
|------------------------------------------------------------------------|-------------------------------|
## Métodos HTTP

> [!note] Por defecto usa GET
> Para descubrir formularios o endpoints, probar POST y otros métodos.

```bash

# Solo GET (default)
feroxbuster -u http://target --methods GET

# GET y POST
feroxbuster -u http://target --methods GET,POST

# PUT y DELETE
feroxbuster -u http://target -m PUT,DELETE
| ```
## Extensiones

> [!important] Archivos ocultos
> Las extensiones revelan backups, configs y archivos sensibles.

```bash

# PHP, HTML, TXT
feroxbuster -u http://target -x php,html,txt

# Backups
| feroxbuster -u http://target -x php,bak,old,zip | # Windows/Java | ``` |
|---|---|---| ## Filtros | > [!warning] Evitar ruido |
> Filtrar respuestas irrelevantes para ver solo lo importante.

### Status Codes | ```bash

# Solo mostrar estos status
feroxbuster -u http://target -s 200,301,302

# Filtrar 404
feroxbuster -u http://target --filter-status 404

# Filtrar 403 y 404
feroxbuster -u http://target --filter-status 403,404
```

### Filtros de Tamaño

| Comando | Descripción |
|---------|-------------|
| `--filter-size 4523` | Filtrar por tamaño exacto |
| `--filter-regex "Not Found"` | Filtrar por regex |
| `--filter-wordcount 1234` | Filtrar por número de palabras |
| `--filter-linecount 45` | Filtrar por número de líneas |

```bash
# Múltiples patrones regex
feroxbuster -u http://target --filter-regex "error|forbidden"

# Cadena exacta
feroxbuster -u http://target -C "Not Found"
| ```
## Recursión

> [!tip] Profundizar en directorios
> La recursión descubre subdirectorios automáticamente.

```bash

# Habilitar recursión
feroxbuster -u http://target -r

# Con extracción de links
feroxbuster -u http://target -r -e

# Profundidad máxima
feroxbuster -u http://target -r --depth 3

# Forzar recursión (ignorar filters)
feroxbuster -u http://target -r --force-recursion
```

---

## Headers y Autenticación

```bash
# Auth header
feroxbuster -u http://target -H "Authorization: Bearer token"

# Cookie
feroxbuster -u http://target -H "Cookie: session=abc123"

# Basic Auth
feroxbuster -u http://target --basic-auth user:pass
```

---

## Proxy

```bash
# Proxy HTTP
feroxbuster -u http://target --proxy http://127.0.0.1:8080

# Proxy SOCKS5 (Tor)
feroxbuster -u http://target --proxy socks5://127.0.0.1:9050
```

---

## Otras Opciones

| Comando | Descripción |
|---------|-------------|
| `--user-agent "Mozilla/5.0"` | Custom User-Agent |
| `--delay 1` | 1 segundo entre requests |
| `--timeout 10` | Timeout de 10 segundos |
| `--dont-filter` | No aplicar filtros automáticos |
| `--no-recursion` | No recursar directorios |
| `--insecure` | No verificar TLS/SSL |

---

## Wordlists para Directorios

| Wordlist | Tamaño | Uso |
|----------|--------|-----|
| `dirbuster/directory-list-2.3-medium.txt` | 220K | Medium |
| `dirb/common.txt` | 4.6K | Common |
| `seclists/Discovery/Web-Content/common.txt` | Variado | Common |
| `seclists/Discovery/Web-Content/big.txt` | Variado | Big |
| `raft-large-directories.txt` | Variado | RAFT Large |
| `raft-medium-directories.txt` | Variado | RAFT Medium |

```bash
# Wordlist personalizada
feroxbuster -u http://target -w /path/to/wordlist.txt

# Wordlist + extensiones
feroxbuster -u http://target -w common.txt -x php
```

---

#checklist
- [ ] Escaneo básico completado
- [ ] Extensiones relevantes probadas
- [ ] Filtros aplicados (404, tamaño)
- [ ] Recursión explorada
- [ ] Headers personalizados probados
- [ ] Proxy configurado si es necesario

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[GoBuster.md|GoBuster]— FFUF, Feroxbuster
- [[FFUF.md|FFUF]— FFUF
- [[../Apuntes/05 - Auditoria Web/Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]— FFUF, Feroxbuster
- [[DirSearch.md|DirSearch]— FFUF
- [[../apuntes Chema/Fuzzing Web.md|Fuzzing Web]— FFUF, Feroxbuster
- [[../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 — Rockstar.md|Fuzzing de parámetros con x8 — Rockstar]— FFUF, Feroxbuster

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]

> #feroxbuster #ffuf
