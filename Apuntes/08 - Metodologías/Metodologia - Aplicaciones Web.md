# Metodologia - Aplicaciones Web

> Guia concisa para auditar y explotar aplicaciones web: metodologia OWASP, reconocimiento, enumeracion, explotacion y post-explotacion.

>

---

## Fase 1: Reconocimiento Pasivo

> Mapear la superficie de ataque sin tocar el objetivo

- whatweb, wappalyzer-cli (tecnologias)
- testssl.sh, sslscan (SSL/TLS)
- subfinder, amass, dnsrecon (DNS/subdominios)
- waybackurls, gau (archivos historicos)
- shodan (infraestructura)

---

## Fase 2: Enumeracion Activa

> Identificar endpoints, parametros y superficies de entrada

### 2.1 Descubrimiento de Contenido

- ffuf (fuzzing directorios)
- feroxbuster (fuzzing recursivo)
- gobuster dns/vhost
- dirsearch

### 2.2 Analisis de Endpoints

- subjs, linkfinder (URLs en JS)
- arjun, ParamSpider (parametros ocultos)

---

## Fase 3: Explotacion (OWASP Top 10)

### A01: Broken Access Control
- IDOR, path traversal

### A02: Cryptographic Failures
- TLS/SSL, cookies seguras, HSTS, CSP

### A03: Injection
- sqlmap (SQLi)
- NoSQLi: , , 
- Command Injection: ; id, | id, id, 

### A04: Insecure Design
- Threat modeling, rate limiting, logica de negocio

### A05: Security Misconfiguration
- /.git/, /.env, /backup.zip, headers faltantes

### A06: Vulnerable Components
- npm audit, pip-audit, dependency-check

### A07: Authentication Failures
- hydra (fuerza bruta), credential stuffing, session fixation

### A08: Integrity Failures
- CI/CD sin firma, deserializacion insegura

### A09: Logging Failures
- Logs insuficientes, alertas ausentes

### A10: SSRF
- Cloud metadata, localhost, internal services

---

## Fase 4: Vulnerabilidades Web Especificas

### XSS
- Reflected, Stored, DOM-based

### LFI / RFI / Path Traversal
- ../../etc/passwd, php://filter, RFI

### XXE
- External entities, OOB XXE

### SSTI
- {{7*7}}, config, subclasses

---

## Fase 5: Post-Explotacion Web

> Consolidar acceso y pivotar

- Webshell (PHP, ASPX, JSP)
- Persistencia (.htaccess, web.config)
- Pivoting (SSH tunneling, ProxyChains)

---

## Herramientas Clave

| Categoria | Herramientas |
|-----------|--------------|
| Recon | whatweb, wappalyzer, subfinder, amass, gau |
| Fuzzing | ffuf, feroxbuster, gobuster, dirsearch |
| SQLi | sqlmap |
| XSS | dalfox, xsstrike |
| SSRF | ssrfmap, Gopherus |
| SSTI | tplmap |
| XXE | xxeinjector |
| Automatizado | nuclei, wapiti, nikto |
| Proxy | Burp Suite, OWASP ZAP |

---

## Referencias

- OWASP Top 10 2021/2025
- OWASP Testing Guide
- PortSwigger Web Security Academy
- HackTricks Web
- PayloadsAllTheThings