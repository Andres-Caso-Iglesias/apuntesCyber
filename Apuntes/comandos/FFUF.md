# FFUF — Cheat Sheet

> Web fuzzing, directorios, parámetros.

---

## Sintaxis básica

```bash
ffuf -u <URL> -w <wordlist>
```

## Fuzzing de directorios

```bash
ffuf -u http://10.10.10.x/FUZZ -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://10.10.10.x/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

## Fuzzing de parámetros

```bash
ffuf -u "http://10.10.10.x/page?FUZZ=test" -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt
```

## Fuzzing de subdominios

```bash
ffuf -u http://FUZZ.ejemplo.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200
```

## Fuzzing de vhosts

```bash
ffuf -u http://10.10.10.x -H "Host: FUZZ.ejemplo.com" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200
```

## Filtrado de respuestas

```bash
# Filtrar por tamaño
ffuf -u http://10.10.10.x/FUZZ -w wordlist.txt -fs 4242

# Filtrar por código de estado
ffuf -u http://10.10.10.x/FUZZ -w wordlist.txt -fc 404

# Filtrar por palabras
ffuf -u http://10.10.10.x/FUZZ -w wordlist.txt -fw 42

# Filtrar por regex
ffuf -u http://10.10.10.x/FUZZ -w wordlist.txt -fr ".*not found.*"
```

## Opciones útiles

```bash
-u <url>                         # URL objetivo (usar FUZZ como keyword)
-w <wordlist>                    # Wordlist
-mc <code>                       # Match status code
-fc <code>                       # Filter status code
-ms <size>                       # Match size
-fs <size>                       # Filter size
-mw <words>                      # Match word count
-fw <words>                      # Filter word count
-t <threads>                     # Threads (default: 40)
-p <delay>                       # Delay entre requests
-rate <rate>                     # Rate limit
-x <proxy>                       # Proxy (http://127.0.0.1:8080)
-H <header>                      # Header adicional
-b <cookie>                      # Cookie
-replay-proxy <proxy>            # Replay con proxy
-o <file>                        # Output
-of <format>                     # Formato (json, csv, html)
```

## Recursos

```bash
# Wordlists comunes
/usr/share/wordlists/dirb/common.txt
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt
SecLists/Discovery/DNS/subdomains-top1million-5000.txt
```



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[GoBuster.md|GoBuster]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/DirSearch.md|DirSearch]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/GoBuster.md|GoBuster]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]

> #dirsearch #feroxbuster #ffuf #gobuster #redes
