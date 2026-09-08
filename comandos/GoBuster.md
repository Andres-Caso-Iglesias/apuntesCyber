# GoBuster — Directory & DNS Brute-forcer

> [!info] Herramienta
> Brute-force de directorios, archivos, subdominios y virtual hosts. Escrita en Go, rápida y con soporte multi-modo.

---

## Modos de uso

> [!tip] Tres modos principales
> - `dir` — Fuzzing de directorios y archivos
> - `dns` — Enumeración de subdominios
> - `vhost` — Enumeración de virtual hosts

---

## Modo DIR (Directorios)

```bash
# Escaneo básico
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt

# Con extensiones
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,py

# Con wordlist más completa
gobuster dir -u http://target -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt

# 50 hilos
gobuster dir -u http://target -w wordlist.txt -t 50

# Sin mostrar resultados 403
gobuster dir -u http://target -w wordlist.txt --no-error

# Recursivo (2 niveles)
gobuster dir -u http://target -w wordlist.txt --wildcard

# Output a archivo
gobuster dir -u http://target -w wordlist.txt -o results.txt
```

---

## Modo DNS (Subdominios)

```bash
# Básico
gobuster dns -d target.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Con resolución de IP
gobuster dns -d target.com -w wordlist.txt -r

# 50 hilos
gobuster dns -d target.com -w wordlist.txt -t 50

# Output a archivo
gobuster dns -d target.com -w wordlist.txt -o subdomains.txt
```

---

## Modo VHOST (Virtual Hosts)

```bash
# Básico
gobuster vhost -u http://target -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Con append-domain (para dominios que no resuelven)
gobuster vhost -u http://target -w wordlist.txt --append-domain

# 50 hilos
gobuster vhost -u http://target -w wordlist.txt -t 50
```

---

## Opciones Comunes

| Opción | Descripción |
|--------|-------------|
| `-u <URL>` | URL objetivo (modo dir/vhost) |
| `-d <dominio>` | Dominio (modo dns) |
| `-w <wordlist>` | Wordlist a usar |
| `-x <ext>` | Extensiones (modo dir) |
| `-t <n>` | Hilos (default 10) |
| `-o <archivo>` | Guardar resultado en archivo |
| `--no-error` | No mostrar errores 403 |
| `--wildcard` | Forzar escaneo wildcard |
| `-r` | Resolver IPs (modo dns) |
| `--append-domain` | Agregar dominio a cada palabra (vhost) |
| `-q` | Modo quiet (sin banner) |
| `--delay <dur>` | Delay entre requests (e.g., `100ms`) |

---

## Filtros por Status Code

```bash
# Solo mostrar 200 y 301
gobuster dir -u http://target -w wordlist.txt -s 200,301

# Excluir 404
gobuster dir -u http://target -w wordlist.txt --exclude-status 404

# Excluir 403 y 404
gobuster dir -u http://target -w wordlist.txt --exclude-status 403,404
```

---

## Wordlists Recomendadas

| Wordlist | Uso |
|----------|-----|
| `/usr/share/wordlists/dirb/common.txt` | Escaneo rápido, básico |
| `/usr/share/wordlists/dirb/big.txt` | Más completo |
| `/usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt` | Medium, balance |
| `/usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-big.txt` | Big, exhaustivo |
| `/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt` | Subdominios |

---

## Ejemplos Prácticos

```bash
# Primer paso: escaneo rápido con common.txt
gobuster dir -u http://10.0.2.9 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt

# Con extensiones y filtrar 403
gobuster dir -u http://10.0.2.9 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt --exclude-status 403

# Enumeración de subdominios
gobuster dns -d target.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Virtual hosts
gobuster vhost -u http://target.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain
```

---

## GoBuster vs FFUF vs Feroxbuster

| Característica | GoBuster | FFUF | Feroxbuster |
|----------------|----------|------|-------------|
| Velocidad | Rápida | Muy rápida | Rápida |
| Escritura en | Go | Go | Rust |
| Recursión | Limitada | No nativa | Nativa y robusta |
| Filtros | Básicos | Muy potentes | Buenos |
| Output | Archivo | JSON/TXT | JSON/TXT/CSV |
| Vhost/DNS | Sí | Subdominios | No |
| Uso recomendado | DNS/VHOST | Dir fuzzing rápido | Dir fuzzing con recursión |

> [!note] En el máster
> GoBuster se usa en la máquina **castor** para enumeración de directorios. FFUF y Feroxbuster son alternativas más modernas para dir fuzzing. GoBuster brilla en modo DNS y VHOST.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[DirSearch.md|DirSearch]] — FFUF, Feroxbuster, GoBuster
- [[Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[../Apuntes/comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, Redes
- [[../Apuntes/comandos/GoBuster.md|GoBuster]] — FFUF, GoBuster, Redes
- [[../Apuntes/05 - Auditoria Web/Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]] — FFUF, Feroxbuster, GoBuster
- [[FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]

> #feroxbuster #ffuf #gobuster #redes
