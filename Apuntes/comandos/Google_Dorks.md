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

### Errores y vulnerabilidades

```
site:ejemplo.com intext:"error"
site:ejemplo.com intext:"warning"
site:ejemplo.com intext:"mysql_fetch"
site:ejemplo.com intext:"syntax error"
site:github.com "password" "ejemplo.com"
```

> [!tip] GHDB
> Base de datos de dorks: `exploit-db.com/google-hacking-database`

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

- [[../../apuntes Joselu/MODULO2/resumen_master_clase11.md|resumen_master_clase11]] — Desarrollo Web, Metodologia Pentest, OSINT
- [[../05 - Auditoria Web/Enumeración Web.md|Enumeración Web]] — Desarrollo Web, Metodologia Pentest, OSINT
- [[../../comandos/Google_Dorks.md|Google_Dorks]] — Desarrollo Web, Google Dorks, Redes
- [[../../apuntes evolve/BLOQUE 3.md|BLOQUE 3]] — Desarrollo Web, Metodologia Pentest, OSINT
- [[../01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Desarrollo Web, Metodologia Pentest, Redes

### 🌐 Cross-Dominio

- [[../../../programacion/SQL/cursores_sql.md|cursores_sql]] — Programacion: Desarrollo Web, Redes
- [[../../../cloud/aws_route53.md|aws_route53]] — Cloud: Desarrollo Web, Redes

> #google_dorks #osint #pentest #redes #web
