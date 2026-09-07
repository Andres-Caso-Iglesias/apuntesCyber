# Google Dorks — Cheat Sheet

> Búsqueda avanzada OSINT con Google.

---

## Operadores

| Operador | Función | Ejemplo |
|----------|---------|---------|
| `site:` | Buscar en un dominio | `site:ejemplo.com` |
| `inurl:` | Texto en la URL | `inurl:admin` |
| `intitle:` | Texto en el título | `intitle:"login"` |
| `intext:` | Texto en el contenido | `intext:"password"` |
| `filetype:` | Tipo de archivo | `filetype:pdf` |
| `ext:` | Extensión | `ext:sql` |
| `cache:` | Versión cacheada | `cache:ejemplo.com` |
| `link:` | Páginas que enlazan | `link:ejemplo.com` |
| `related:` | Sitios similares | `related:ejemplo.com` |
| `info:` | Info de un sitio | `info:ejemplo.com` |
| `define:` | Definición | `define:hacking` |
| `numrange:` | Rango numérico | `numrange:1-100` |
| `before:` | Fecha anterior | `before:2024-01-01` |
| `after:` | Fecha posterior | `after:2023-01-01` |

## Dorks comunes

### Archivos sensibles

```
site:ejemplo.com filetype:pdf
site:ejemplo.com filetype:doc
site:ejemplo.com filetype:xls
site:ejemplo.com filetype:sql
site:ejemplo.com filetype:log
site:ejemplo.com filetype:conf
site:ejemplo.com filetype:bak
site:ejemplo.com ext:sql | ext:bak | ext:log
```

### Login y admin

```
site:ejemplo.com inurl:admin
site:ejemplo.com intitle:"login"
site:ejemplo.com inurl:login | inurl:admin
site:ejemplo.com intitle:"index of" "parent directory"
```

### Errores y漏洞

```
site:ejemplo.com intext:"error"
site:ejemplo.com intext:"warning"
site:ejemplo.com intext:"mysql_fetch"
site:ejemplo.com intext:"syntax error"
```

### Directorios abiertos

```
site:ejemplo.com intitle:"index of" "parent directory"
site:ejemplo.com intitle:"index of" "backup"
site:ejemplo.com intitle:"index of" "config"
```

### Configuraciones

```
site:ejemplo.com filetype:env
site:ejemplo.com filetype:yml | filetype:yaml
site:ejemplo.com filetype:ini | filetype:conf
site:ejemplo.com inurl:.git
site:ejemplo.com inurl:.env
```

### Correos y contactos

```
site:ejemplo.com "@ejemplo.com"
site:ejemplo.com intext:"email" | intext:"correo"
site:ejemplo.com filetype:vcf
```

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[OSINT - Metodología y Fuentes]] — OSINT completo
- [[Anonimato, Ingeniería Social y Enumeración Web]] — Enumeración web

> #google-dorks #herramientas #osint #web
