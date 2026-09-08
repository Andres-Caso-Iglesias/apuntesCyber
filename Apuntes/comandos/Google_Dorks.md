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

- [[../../comandos/Google_Dorks.md|Google_Dorks]] — Google Dorks, OSINT, Redes
- [[../../apuntes evolve/BLOQUE 3.md|BLOQUE 3]] — Google Dorks, OSINT, Redes
- [[../../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — Google Dorks, OSINT, Redes
- [[../01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Metodología Pentest, OSINT, Redes
- [[../../apuntes Joselu/MODULO2/resumen_master_clase11.md|resumen_master_clase11]] — Google Dorks, OSINT, Redes
- [[../04 - OSINT y Recopilacion/OSINT - Metodología y Fuentes.md|OSINT - Metodología y Fuentes]] — Metodología Pentest, OSINT, Redes

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]

> #google-dorks #osint #pentest #redes
