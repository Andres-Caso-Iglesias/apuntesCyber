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

- [[../../comandos/WPScan.md|WPScan]] — Hydra, WPScan, WordPress
- [[../05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]] — Hydra, WPScan, WordPress
- [[../../comandos/BurpSuite.md|BurpSuite]] — Hydra, WPScan, WordPress
- [[../05 - Auditoria Web/WordPress - Auditoría con WPScan.md|WordPress - Auditoría con WPScan]] — Command Injection / RCE, Hydra, WPScan
- [[../../apuntes Joselu/MODULO3/resumen_master_clase37.md|resumen_master_clase37]] — Command Injection / RCE, Hydra, WPScan
- [[../../comandos/Google_Dorks.md|Google_Dorks]] — Redes, WordPress

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #hydra #redes #wordpress #wpscan
