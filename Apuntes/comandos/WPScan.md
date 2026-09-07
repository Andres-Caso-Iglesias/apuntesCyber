# WPScan — Cheat Sheet

> Auditoría WordPress: CMS, plugins, fuerza bruta, RCE.

---

## Sintaxis básica

```bash
wpscan --url <URL>
```

## Enumeración

```bash
wpscan --url http://10.10.10.x --enumerate vp       # Plugins vulnerables
wpscan --url http://10.10.10.x --enumerate ap        # Todos los plugins
wpscan --url http://10.10.10.x --enumerate vt        # Templates vulnerables
wpscan --url http://10.10.10.x --enumerate at        # Todos los templates
wpscan --url http://10.10.10.x --enumerate u         # Usuarios
wpscan --url http://10.10.10.x --enumerate tt        # Timthumbs
```

## Fuerza bruta

```bash
# Usuarios
wpscan --url http://10.10.10.x --passwords /usr/share/wordlists/rockyou.txt --usernames admin

# Múltiples usuarios
wpscan --url http://10.10.10.x --passwords /usr/share/wordlists/rockyou.txt --usernames users.txt
```

## Detección de vulnerabilidades

```bash
wpscan --url http://10.10.10.x --enumerate vp --vulnerable-detection aggressive
```

## API de WPScan

```bash
wpscan --url http://10.10.10.x --api-token <token>
```

## Opciones útiles

```bash
--url <url>                       # URL del sitio WordPress
--enumerate <options>             # Qué enumerar
--passwords <wordlist>            # Wordlist para brute force
--usernames <user|file>           # Usuarios
--threads <n>                     # Threads (default: 5)
--proxy <proxy>                   # Proxy
--cookie-string <cookie>          # Cookie
--random-user-agent               # User-Agent aleatorio
--disable-tls-checks              # Ignorar SSL
--vulnerable-detection <mode>     # aggressive/Passive
--detection-mode <mode>           # mixed/Aggressive/Passive
-o <file>                         # Output
--api-token <token>               # API token para más info
```

## Ejemplos prácticos

```bash
# Enumeración completa
wpscan --url http://10.10.10.x --enumerate ap,vt,u --detection-mode aggressive

# Brute force con usuario conocido
wpscan --url http://10.10.10.x --passwords /usr/share/wordlists/rockyou.txt --usernames admin

# Con proxy
wpscan --url http://10.10.10.x --proxy http://127.0.0.1:8080 --enumerate ap
```

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[WordPress - Auditoría con WPScan]] — Teoría completa de WordPress audit

> #wpscan #herramientas #wordpress #web
