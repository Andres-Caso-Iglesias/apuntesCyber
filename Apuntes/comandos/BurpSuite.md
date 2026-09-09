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
engine = TurboIntruder	attackívate糕点
queue = RequestQueue(base_request)
for word in open('/usr/share/wordlists/dirb/common.txt'):
    queue.add(base_request.shorten(word))
engine.run(queue, handle_response)
```



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[SQLMap.md|SQLMap]] — Redes, SQL Injection, SQLMap
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — Redes, SQL Injection, SQLMap
- [[../../apuntes Joselu/MODULO3/resumen_master_clase48.md|resumen_master_clase48]] — Burp Suite, Redes, SQL Injection
- [[../05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal — 6 Casos y Bypasses]] — Burp Suite, Path Traversal / LFI, Redes
- [[../05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF — Server-Side Request Forgery]] — Burp Suite, Path Traversal / LFI, Redes
- [[../05 - Auditoria Web/XSS — Cross-Site Scripting.md|XSS — Cross-Site Scripting]] — Burp Suite, Redes, SQL Injection

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]

> #burpsuite #lfi #redes #sqli #sqlmap #ssrf #wpscan
