# Google Dorks — Búsquedas Web Avanzadas

> [!info] Herramienta
> Técnicas de búsqueda avanzada en Google para descubrir información sensible, vulnerabilidades y archivos ocultos.

---

## Operadores de Búsqueda

| Operador    | Descripción                    | Ejemplo                   |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| ----------- | ------------------------------ | ------------------------- | ----------------------- | ---------------------- | --- | ----------- | ---------------- | ---------------- | --- | --- | ---------- | ------------------- | --------------------- | --- |
| `site:`     | Restringe a un dominio         | `site:ejemplo.com`        |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| `inurl:`    | Busca palabras en la URL       | `inurl:login`             |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| `intitle:`  | Busca palabras en el título    | `intitle:admin`           |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| `intext:`   | Busca en el texto de la página | `intext:password`         |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| `filetype:` | Busca por tipo de archivo      | `filetype:pdf`            |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
| `ext:`      | Alias de filetype              | `ext:log`                 |                         |                        |     |             |                  |                  |     |     |            |                     |                       |     |
|             | `allinurl:`                    | Todos los términos en URL | `allinurl:admin login`  |                        |     | `inanchor:` | Busca en anchors | `inanchor:login` |     |     | `related:` | Sitios relacionados | `related:example.com` |     |
| ---         | ---                            | ---                       | ## Dorks para Seguridad | > [!warning] Uso ético |     |             |                  |                  |     |     |            |                     |                       |     |
> Solo usar en sistemas que tengas autorización para auditarr.

### Archivos Sensibles | | Dork | Objetivo |

| `filetype:sql "password"` | Archivos SQL con contraseñas |
| `filetype:env "password"` | Variables de entorno |
| `filetype:log "password"` | Logs con credenciales |
| `filetype:bak "password"` | Backups |
| `filetype:cfg "password"` | Configuraciones |
| `filetype:ini "password"` | Archivos INI |
| `filetype:xml "password"` | Archivos XML |

### Login y Admin

| Dork | Objetivo |
|------|----------|
| `inurl:login` | Páginas de login |
| `intitle:"admin login"` | Login de administrador |
| `inurl:admin` | Paneles de admin |
| `intitle:"index of" "admin"` | Directorios de admin abiertos |
| `inurl:wp-admin` | WordPress admin |

### Directorios Abiertos

| Dork | Objetivo |
|------|----------|
| `intitle:"index of"` | Directorios abiertos |
| `intitle:"index of" "parent directory"` | Listado de archivos |
| `intitle:"index of" .git` | Repositorios Git expuestos |
| `intitle:"index of" .env` | Archivos .env expuestos |

### Errores y Debug

| Dork | Objetivo |
|------|----------|
| `intext:"syntax error"` | Errores de PHP |
| `intext:"Warning: mysql_connect"` | Errores de MySQL |
| `intext:"Fatal error"` | Errores fatales |
| `intext:"PHP Error"` | Errores PHP |

### Configuraciones

| Dork | Objetivo |
|------|----------|
| `filetype:conf "password"` | Configuraciones con passwords |
| `filetype:htpasswd` | Archivos htpasswd |
| `filetype:env` | Variables de entorno |
| | `filetype:json "password"` | JSON con credenciales |
|------------------------------------------------------|------------------------------|
## Combinaciones Avanzadas

> [!tip] Combinar operadores
> La potencia está en combinar múltiples operadores.

```bash

# Login en un sitio específico
site:ejemplo.com inurl:login

# Archivos SQL en un dominio
site:ejemplo.com filetype:sql

# PDFs con información sensible
site:ejemplo.com filetype:pdf intext:"confidential"

# Directorios abiertos en un sitio
site:ejemplo.com intitle:"index of"

# Configuraciones expuestas
site:ejemplo.com filetype:env OR filetype:cfg

# Errores PHP en un dominio
site:ejemplo.com intext:"PHP Error"
```

---

## Herramientas Relacionadas

| Herramienta | Uso |
|-------------|-----|
| `theHarvester` | Recopilar emails y subdominios |
| `Maltego` | OSINT visual |
| `Shodan` | IoT y servicios expuestos |
| `Censys` | Escaneo de infraestructura |

---

#checklist
- [ ] Operadores básicos (`site:`, `inurl:`, `intitle:`, `intext:`) entendidos
- [ ] `filetype:` y `ext:` para archivos dominados
- [ ] Dorks de seguridad practicados
- [ ] Combinaciones de operadores dominadas
- [ ] Ética de uso recordada



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/comandos/Google_Dorks.md|Google_Dorks]] — Google Dorks, OSINT, Redes
- [[../Apuntes/05 - Auditoria Web/Enumeración Web.md|Enumeración Web]] — OSINT, Redes, WordPress
- [[../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — OSINT, Redes, WordPress
- [[WPScan.md|WPScan]] — Redes, WPScan, WordPress
- [[../apuntes Chema/Enumeración Web.md|Enumeración Web]] — OSINT, Redes, WordPress
- [[../Apuntes/05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]] — Redes, WPScan, WordPress

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/WPScan|WPScan]]

> #google-dorks #osint #redes #wordpress #wpscan
