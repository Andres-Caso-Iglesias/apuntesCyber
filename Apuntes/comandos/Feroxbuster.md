# Feroxbuster — Cheat Sheet

> Fuzzing recursivo de directorios.

---

## Sintaxis básica

```bash
feroxbuster -u <URL> -w <wordlist>
```

## Uso básico

```bash
feroxbuster -u http://10.10.10.x
feroxbuster -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt
```

## Recursividad

```bash
feroxbuster -u http://10.10.10.x -d 3          # Profundidad 3
feroxbuster -u http://10.10.10.x --no-recursion # Sin recursión
```

## Filtrado

```bash
feroxbuster -u http://10.10.10.x -s 200 301 302    # Solo estos códigos
feroxbuster -u http://10.10.10.x -S 404             # Excluir códigos
feroxbuster -u http://10.10.10.x -s 200 --filters "word count=42"
```

## Opciones útiles

```bash
-u <url>                         # URL objetivo
-w <wordlist>                    # Wordlist
-d <depth>                       # Profundidad de recursión
-t <threads>                     # Threads (default: 50)
-p <proxy>                       # Proxy
-k                               # Ignorar certificados SSL
--no-recursion                   # No recursar
-s <status>                      # Match status codes
-S <status>                      # Filter status codes
-o <file>                        # Output
--rate-limit <rate>              # Rate limit
```

## Ejemplos prácticos

```bash
# Fuzzing rápido
feroxbuster -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt -t 100

# Con proxy
feroxbuster -u http://10.10.10.x -p http://127.0.0.1:8080

# Solo directorios
feroxbuster -u http://10.10.10.x -s 200 301 302 -d 2
```


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/GoBuster.md|GoBuster]] — FFUF, Feroxbuster, Redes
- [[FFUF.md|FFUF]] — FFUF, Redes
- [[../../comandos/DirSearch.md|DirSearch]] — FFUF, Feroxbuster, Redes
- [[../../comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, Redes
- [[GoBuster.md|GoBuster]] — FFUF, Redes
- [[../05 - Auditoria Web/Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]] — FFUF, Feroxbuster, Redes

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]

> #feroxbuster #ffuf #redes
