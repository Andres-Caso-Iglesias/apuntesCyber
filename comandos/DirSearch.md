# DirSearch — Fuzzing Directorios Web

> [!info] Herramienta
> Búsqueda de directorios y archivos ocultos en servidores web. Escrita en Python, fácil de usar y con recursión.
## Escaneo Básico

> [!tip] Primer paso
> Empezar simple y escalar complejidad según necesidad.

```bash

# Escaneo básico
dirsearch -u http://target

# Con wordlist específica
dirsearch -u http://target -w /usr/share/wordlists/dirb/common.txt

# 50 hilos
dirsearch -u http://target -t 50

# Solo resultados
dirsearch -u http://target --quiet
```

### Output

| Comando | Descripción |
|---------|-------------|
| `-o results.txt` | Guardar en archivo |
| `--format json` | Output JSON |
| `-v` | Verbose |
| | `--debug-log debug.log` | Debug log |
|------------------------------------------------------------------------|-------------------------------|
## Métodos HTTP

> [!note] Por defecto usa GET
> Para descubrir formularios o endpoints, probar POST y otros métodos.

```bash

# Solo GET (default)
dirsearch -u http://target --methods GET

# GET y POST
dirsearch -u http://target --methods GET,POST

# PUT y DELETE
dirsearch -u http://target -m PUT,DELETE
| ```
## Extensiones

> [!important] Archivos ocultos
> Las extensiones revelan backups, configs y archivos sensibles.

```bash

# PHP, HTML, TXT
dirsearch -u http://target -e php,html,txt

# Backups
| dirsearch -u http://target -e php,bak,old,zip | # Windows/Java | ``` |
|---|---|---| ## Filtros | > [!warning] Evitar ruido |
> Filtrar respuestas irrelevantes para ver solo lo importante.

### Status Codes | ```bash

# Solo mostrar estos status
dirsearch -u http://target --include-status 200,301,302

# Filtrar 404
dirsearch -u http://target --exclude-status 404

# Filtrar 403 y 404
dirsearch -u http://target --exclude-status 403,404
```

### Filtros de Tamaño

| Comando | Descripción |
|---------|-------------|
| `--exclude-size 4523` | Filtrar por tamaño exacto |
| `--exclude-regex "Not Found"` | Filtrar por regex |
| `--exclude-text "error"` | Filtrar por texto |
| `--exclude-redirects` | Filtrar redirecciones |

```bash
# Múltiples patrones regex
dirsearch -u http://target --exclude-regex "error|forbidden"

# Cadena exacta
dirsearch -u http://target --exclude-text "Not Found"
| ```
## Recursión

> [!tip] Profundizar en directorios
> La recursión descubre subdirectorios automáticamente.

```bash

# Habilitar recursión
dirsearch -u http://target -r

# Profundidad máxima
dirsearch -u http://target -r --max-depth 3

# Solo directorios específicos
dirsearch -u http://target -r --scope "admin,uploads"
```

---

## Headers y Autenticación

```bash
# Auth header
dirsearch -u http://target -H "Authorization: Bearer token"

# Cookie
dirsearch -u http://target -H "Cookie: session=abc123"

# Basic Auth
dirsearch -u http://target --basic-auth user:pass
```

---

## Proxy

```bash
# Proxy HTTP
dirsearch -u http://target --proxy http://127.0.0.1:8080

# Proxy SOCKS5 (Tor)
dirsearch -u http://target --proxy socks5://127.0.0.1:9050
```

---

## Otras Opciones

| Comando | Descripción |
|---------|-------------|
| `--user-agent "Mozilla/5.0"` | Custom User-Agent |
| `--delay 1` | 1 segundo entre requests |
| `--timeout 10` | Timeout de 10 segundos |
| `--random-agents` | User-Agent aleatorio |
| `--insecure` | No verificar TLS/SSL |
| `--crawl` | Rastrear para descubrir más rutas |
| `--full-url` | Mostrar URLs completas |
| `--no-color` | Sin colores en output |

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
dirsearch -u http://target -w /path/to/wordlist.txt

# Wordlist + extensiones
dirsearch -u http://target -w common.txt -e php
```

---

## Ejemplos Prácticos

```bash
# Escaneo completo con recursión y extensiones
dirsearch -u http://target -e php,html,txt,bak -r --max-depth 2

# Bypass de protección con headers
dirsearch -u http://target -H "X-Forwarded-For: 127.0.0.1" -H "X-Real-IP: 127.0.0.1"

# Fuzzing de formularios
dirsearch -u http://target -m POST -w passwords.txt

# Escaneo sigiloso
dirsearch -u http://target --delay 2 --random-agents --quiet
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

- [[../Apuntes/comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[../Apuntes/comandos/FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster
- [[../Apuntes/comandos/GoBuster.md|GoBuster]] — FFUF, Feroxbuster, GoBuster
- [[Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[GoBuster.md|GoBuster]] — FFUF, Feroxbuster, GoBuster
- [[FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]

> #dirsearch #feroxbuster #ffuf #gobuster #redes
