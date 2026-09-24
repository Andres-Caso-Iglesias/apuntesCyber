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

- [[../05 - Auditoria Web/XXE - XML External Entity.md|XXE - XML External Entity]] — Netcat / Reverse Shells, WPScan, XXE
- [[../05 - Auditoria Web/SSTI - Server-Side Template Injection.md|SSTI - Server-Side Template Injection]] — Netcat / Reverse Shells, WPScan, XXE
- [[../../apuntes Andres/30.06.2026 Explotación web PortSwigger.md|30.06.2026 Explotación web PortSwigger]] — Netcat / Reverse Shells, WPScan, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]] — Desarrollo Web, Netcat / Reverse Shells, XXE
- [[../../comandos/WPScan.md|WPScan]] — Desarrollo Web, WPScan, WordPress

### 🌐 Cross-Dominio

- [[../../../ia/mlflow.md|mlflow]] — IA: CLI/Scripting, Desarrollo Web, Redes
- [[../../../programacion/PHP/seguridad_php.md|seguridad_php]] — Programacion: CLI/Scripting, Desarrollo Web, Redes

> #burpsuite #cli #command_injection #hydra #metasploit #netcat #redes #ssrf #ssti #web #wordpress #wpscan #xxe
