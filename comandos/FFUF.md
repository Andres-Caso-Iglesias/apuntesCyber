# FFUF — Web Fuzzer

> [!info] Herramienta
> Fuzzing rápido de directorios, parámetros, subdominios y formularios HTTP.
## Básico

> [!tip] Formato general
> `ffuf -u <URL> -w <wordlist>`

```bash

# Fuzzing de directorios
ffuf -u http://target/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Con extensión
ffuf -u http://target/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.html,.txt

# Subdominios
ffuf -u http://FUZZ.target.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Parámetros GET
ffuf -u "http://target/page?FUZZ=test" -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt
```

---

## Filtros

> [!warning] Evitar ruido
| Filtro | Descripción |
|--------|-------------|
| `-fc <código>` | Filtrar por código HTTP |
| `-fs <tamaño>` | Filtrar por tamaño |
| `-fw <n>` | Filtrar por número de palabras |
| `-fl <n>` | Filtrar por número de líneas |
| `-fr <regex>` | Filtrar por regex |

```bash
# Filtrar 404
ffuf -u http://target/FUZZ -w wordlist.txt -fc 404

# Filtrar por tamaño
ffuf -u http://target/FUZZ -w wordlist.txt -fs 4523

# Filtrar por palabras
ffuf -u http://target/FUZZ -w wordlist.txt -fw 10
```

---

## Opciones Comunes

| Opción | Descripción |
|--------|-------------|
| `-u <URL>` | URL con FUZZ como placeholder |
| `-w <wordlist>` | Wordlist a usar |
| `-e <ext>` | Extensiones a probar |
| `-mc <código>` | Mostrar solo códigos específicos |
| `-t <n>` | Hilos (default 40) |
| `-p <seg>` | Delay entre requests |
| `-rate <n>` | Requests por segundo |
| `-o <archivo>` | Output JSON |
| `-of <formato>` | Formato: json, ejson, html, md, csv, all |
| `-H <header>` | Header custom |
| `-x <proxy>` | Proxy (http://127.0.0.1:8080) |
| `-b <cookie>` | Cookie |
| `-ac` | Auto-calibrate (auto-filtrar) |
| `-v` | Verbose (mostrar URL completa) |

```bash
# Con headers
ffuf -u http://target/FUZZ -w wordlist.txt -H "Authorization: Bearer token"

# Con proxy
ffuf -u http://target/FUZZ -w wordlist.txt -x http://127.0.0.1:8080

# Auto-calibrate
ffuf -u http://target/FUZZ -w wordlist.txt -ac

# Rate limit
ffuf -u http://target/FUZZ -w wordlist.txt -rate 100

# Output
ffuf -u http://target/FUZZ -w wordlist.txt -o results.json -of json
```

---

## Fuzzing de Parámetros

```bash
# Probar parámetros GET
ffuf -u "http://target/page?FUZZ=test" -w params.txt

# Probar valores de parámetro
ffuf -u "http://target/page?id=FUZZ" -w /usr/share/wordlists/seclists/Fuzzing/numbers/1-1000.txt

# POST data fuzzing
ffuf -u http://target/login -X POST -d "user=admin&pass=FUZZ" -w passwords.txt
```

---

## Fuzzing de Subdominios

```bash
# Subdominios
ffuf -u http://FUZZ.target.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -ac

# Virtual hosts
ffuf -u http://target.com -H "Host: FUZZ.target.com" -w subdomains.txt -ac
```

---

## Fuzzing de Directorios

```bash
# Directorios
ffuf -u http://target/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Con extensiones
ffuf -u http://target/FUZZ -w wordlist.txt -e .php,.html,.bak,.old,.zip

# Recursivo (usando ffuf-recursion)
ffuf -u http://target/FUZZ -w wordlist.txt -recursion -recursion-depth 2
```

---

## Wordlists Comunes

| Wordlist | Uso |
|----------|-----|
| `dirb/common.txt` | Directorios comunes |
| `seclists/Discovery/Web-Content/common.txt` | Web content |
| `seclists/Discovery/Web-Content/big.txt` | Web content extenso |
| `raft-large-directories.txt` | RAFT large |
| `seclists/Discovery/DNS/subdomains-top1million-5000.txt` | Subdominios |
| `seclists/Discovery/Web-Content/burp-parameter-names.txt` | Parámetros |

---

#checklist
- [ ] Wordlist seleccionado
- [ ] Placeholder FUZZ en URL configurado
- [ ] Filtros aplicados (fc, fs, fw)
- [ ] Headers custom si es necesario
- [ ] Output guardado para análisis
