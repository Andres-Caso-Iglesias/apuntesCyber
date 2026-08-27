# WPScan — Auditoría WordPress

> [!info] Herramienta
> Escaneo de vulnerabilidades en sitios WordPress: plugins, themes, usuarios y brute force.
## Escaneo Básico

> [!tip] Primer paso
> Siempre empezar con un escaneo básico para identificar la versión y componentes.

```bash

# Escaneo básico
wpscan --url http://target

# Sin banner
wpscan --url http://target --no-banner

# Output legible
wpscan --url http://target -o results.txt
```

### Output

| Comando | Descripción |
|---------|-------------|
| `-o results.txt` | Guardar en archivo |
| `--format json` | Output JSON |
| | `--format cli-no-colour` | Sin colores |
|-----------------------------------------------------------------------------|---------------------------|
## Enumeración

> [!important] Qué buscar
> Enumerar TODO: plugins vulnerables, todos los plugins, themes y usuarios.

```bash

# Plugins vulnerables
wpscan --url http://target -e vp

# Todos los plugins (no solo vuln)
wpscan --url http://target -e ap

# Todos los themes
wpscan --url http://target -e at

# Usuarios
wpscan --url http://target -e u

# Combinado
wpscan --url http://target -e vp,u
```

### Flags de Enumeración

| Flag | Descripción |
|------|-------------|
| `-e vp` | Plugins vulnerables |
| `-e ap` | Todos los plugins |
| `-e vt` | Themes vulnerables |
| `-e at` | Todos los themes |
| `-e u` | Usuarios |
| `-e tt` | Timthumbs |
| | `-e m` | Medias (uploads) |
|--------------------------------------------------------|--------------------------------|
## Enumeración de Usuarios

> [!note] Métodos alternativos
> Si WPScan no encuentra usuarios, probar manualmente.

```bash

# API REST
curl http://target/wp-json/wp/v2/users

# Author archive (redirige a /author/admin)
http://target/?author=1
http://target/?author=2
| ```
## Plugins Vulnerables

> [!warning] Detección
> Usar detección agresiva para encontrar más plugins.

```bash

# Detección agresiva
wpscan --url http://target -e vp --plugins-detection aggressive

# Forzar detección de versión
wpscan --url http://target -e vp --plugins-version-detection aggressive
```

---

## Themes Vulnerables

```bash
# Themes con vulnerabilidades
wpscan --url http://target -e vt

# Detección agresiva
wpscan --url http://target -e vt --themes-detection aggressive
| ```
## Brute Force

> [!danger] Contraseñas
> Necesitás una lista de usuarios (de `-e u`) y un wordlist.

```bash

# Brute force con diccionario
wpscan --url http://target --passwords users.txt --wordlist rockyou.txt

# Limitar hilos y velocidad
wpscan --url http://target --passwords users.txt --threads=5 --throttle=2

# Crear lista de usuarios
echo -e "admin\neditor\nuser1" > users.txt
```

### XML-RPC

> [!tip] Bypass rate limiting
> XML-RPC permite múltiples intentos en un solo request via `system.multicall`.

| Endpoint | Método |
|----------|--------|
| `xmlrpc.php` | Endpoint XML-RPC |
| `wp.getUsersBlogs` | Brute force |
| `system.multicall` | Múltiples intentos |

---

## Stealth

```bash
# User-Agent aleatorio
wpscan --url http://target --random-user-agent

# Throttle entre requests
wpscan --url http://target --throttle=5

# Limitar hilos
wpscan --url http://target --max-threads=5
| ```
## API Token

> [!info] Datos de vulnerabilidades
> Con un token de API, WPScan obtiene información detallada de vulnerabilidades.

```bash

# Con token
wpscan --url http://target --api-token "TOKEN"

# Variable de entorno
export WPSCAN_API_TOKEN="TOKEN"
```

---

## Proxy y Autenticación

```bash
# Proxy HTTP
wpscan --url http://target --proxy "http://127.0.0.1:8080"

# Proxy SOCKS5 (Tor)
wpscan --url http://target --proxy "socks5://127.0.0.1:9050"

# Cookie para autenticación
wpscan --url http://target --cookie-string "session=abc"
```

---

#checklist
- [ ] Escaneo básico completado
- [ ] Plugins vulnerables identificados
- [ ] Themes verificados
- [ ] Usuarios enumerados
- [ ] Brute force intentado
- [ ] XML-RPC verificado

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]— Hydra, WPScan, WordPress
- [[../Apuntes/05 - Auditoria Web/WordPress - Auditoría con WPScan.md|WordPress - Auditoría con WPScan]— Hydra, WPScan, WordPress
- [[../Apuntes/08 - Metodologías/00 - Metodologías de Explotación.md|00 - Metodologías de Explotación]— Hydra, WPScan, WordPress
- [[../apuntes Joselu/MODULO3/resumen_master_clase37.md|resumen_master_clase37]— Hydra, WPScan, WordPress
- [[../apuntes evolve/BLOQUE 9.md|BLOQUE 9]— Hydra
- [[BurpSuite.md|BurpSuite]— Hydra

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/WPScan|WPScan]]

> #hydra #wordpress #wpscan
