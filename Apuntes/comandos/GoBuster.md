# GoBuster — Cheat Sheet

> Directory/DNS/VHOST brute-force.

---

## Sintaxis básica

```bash
gobuster dir -u <URL> -w <wordlist>
gobuster dns -d <domain> -w <wordlist>
gobuster vhost -u <URL> -w <wordlist>
```

## Directorios

```bash
gobuster dir -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt
gobuster dir -u http://10.10.10.x -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,html
```

## DNS

```bash
gobuster dns -d ejemplo.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

## VHOST

```bash
gobuster vhost -u http://10.10.10.x -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

## Opciones útiles

```bash
# Generales
-u <url>                         # URL objetivo
-w <wordlist>                    # Wordlist
-t <threads>                     # Threads (default: 10)
-p <proxy>                       # Proxy
-k                               # Ignorar SSL
--no-color                       # Sin colores
-o <file>                        # Output

# Dir
-x <ext>                         # Extensiones (php,txt,html)
-s <status>                      # Status codes (200,301,302)
-b <status>                      # Excluir status codes
-e                               # Imprimir URLs completas
-r                               # No seguir redirects
-n                               # No imprimir status code
--size <size>                    # Filtrar por tamaño

# DNS
-r                               # Resolver IPs
-c <chlist>                      # Characters to use
```

## Ejemplos prácticos

```bash
# Directorios con extensiones
gobuster dir -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 50

# Subdominios
gobuster dns -d ejemplo.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50

# VHOST
gobuster vhost -u http://10.10.10.x -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain
```







---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Feroxbuster.md|Feroxbuster]] — DirSearch, FFUF, Feroxbuster
- [[FFUF.md|FFUF]] — DirSearch, FFUF, Feroxbuster
- [[../../comandos/DirSearch.md|DirSearch]] — DirSearch, FFUF, Feroxbuster
- [[../../comandos/Feroxbuster.md|Feroxbuster]] — DirSearch, FFUF, Feroxbuster
- [[../../comandos/GoBuster.md|GoBuster]] — DirSearch, FFUF, Feroxbuster
- [[DirSearch.md|DirSearch]] — DirSearch, FFUF, Feroxbuster

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]

> #dirsearch #feroxbuster #ffuf #gobuster #redes
