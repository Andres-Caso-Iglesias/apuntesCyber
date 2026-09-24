# Burp Suite — Cheat Sheet

> Proxy, Repeater, Intruder, scanning web.

---

## Configuración del proxy

```bash
# Puertos por defecto
Proxy: 127.0.0.1:8080
SOCKS: 127.0.0.1:1080

# Configurar en navegador/FoxyProxy
# Tipo: HTTP
# Host: 127.0.0.1
# Puerto: 8080
```

## Intercept

```
Intercept is on/off               # Toggle intercept
Forward                           # Enviar petición
Drop                             # Descartar petición
Intercept requests from          # Filtrar por host
Intercept responses from         # Filtrar respuestas
```

## Repeater

```
Ctrl+R                           # Enviar a Repeater
Ctrl+Shift+R                     # Enviar a Repeater (nueva pestaña)
+ / -                            # Añadir/quitar pestaña
Send                             # Enviar request
```

## Intruder

```
Ctrl+I                           # Enviar a Intruder
Sniper                           # Un payload por position
Battering Ram                    # Mismo payload en todas las posiciones
Pitchfork                       # Payloads paralelos
Cluster Bomb                     # Combinación de payloads
```

### Positions

```
Add §                            # Añadir position
Clear §                          # Quitar todas las positions
Auto §                           # Detectar positions automáticamente
```

### Payloads

```
Simple list                      # Lista manual
Runtime file                     # Archivo en disco
Numbers                          # Rango numérico
Dates                            # Fechas
Brute forcer                     # Fuerza bruta
Null payloads                    # Payloads vacíos
Username generator               # Generador de usuarios
```

## Scanner

```
Scan per host                    # Escanear por host
Scan per URL                     # Escanear por URL
Actively scan                   # Escaneo activo
Passively scan                  # Escaneo pasivo
```

## Comparador

```
Ctrl+Shift+D                     # Añadir a Comparador
Text / Hex / Words               # Modo de comparación
```

## Decoder

```
URL encode/decode                # Codificación URL
HTML encode/decode               # Codificación HTML
Base64 encode/decode             # Codificación Base64
MD5 / SHA-*                      # Hashing
Gzip decompress                  # Descompresión
```

## Turbo Intruder

```python
# Ejemplo: fuzzing de directorios
engine = TurboIntruder.basicRequests()
queue = RequestQueue(base_request)
for word in open('/usr/share/wordlists/dirb/common.txt'):
    queue.add(base_request.shorten(word))
engine.run(queue, handle_response)
```









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — Path Traversal / LFI, SQL Injection, XSS
- [[../05 - Auditoria Web/XSS - Cross-Site Scripting.md|XSS - Cross-Site Scripting]] — Desarrollo Web, SQL Injection, XSS
- [[SQLMap.md|SQLMap]] — Desarrollo Web, SQL Injection, SQLMap
- [[../../transcripciones/Septiembre/15.09.2026 SQLi - Inyecciones - Labs - Avanzado II.md|15.09.2026 SQLi - Inyecciones - Labs - Avanzado II]] — Path Traversal / LFI, SQL Injection, XSS
- [[../05 - Auditoria Web/XXE - XML External Entity.md|XXE - XML External Entity]] — Desarrollo Web, Path Traversal / LFI, WPScan

### 🌐 Cross-Dominio

- [[../../../ia/mlflow.md|mlflow]] — IA: Desarrollo Web, Redes, SQL
- [[../../../programacion/PHP/seguridad_php.md|seguridad_php]] — Programacion: Desarrollo Web, Redes, SQL

> #burpsuite #cli #lfi #redes #sql #sqli #sqlmap_tool #ssrf #ssti #web #wpscan #xss
