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

### 2.3 Descubrimiento de parametros en dos capas (02.09)

```bash
# wfuzz con filtro --hl 1 (hide lines): oculta respuestas de 1 sola linea
# y deja visibles solo las que devuelven contenido real (parametro valido)
wfuzz -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hl 1 http://<target>/page?FUZZ=x
```

> [!important] IDEA CLAVE
> No existe una receta unica de LFI/parametros: primero se descubre el **parametro vulnerable** (fuerza bruta) y despues se itera sobre los **tipos de traversal**, porque el comportamiento depende de como el programador construyo la ruta. Metafora: encontrar el LFI correcto es probar distintas llaves en la misma cerradura.

### 2.4 WAF (clase 37)

Entre el paquete modificado y el servidor puede haber un **WAF** (*Web Application Firewall*) que intenta detectar peticiones maliciosas. Es bypasseable con tecnicas especificas. Si se supera, solo queda el backend (los ficheros PHP del servidor).

---

## Fase 3: Explotacion (OWASP Top 10)

### A01: Broken Access Control
- IDOR, path traversal

### A02: Cryptographic Failures
- TLS/SSL, cookies seguras, HSTS, CSP

### A03: Injection
- sqlmap (SQLi)
- NoSQLi: operadores `$ne`, `$gt` en consultas JSON
- Command Injection: `; id`, `| id`, `&& id`, `|| id`
- Diferencia con SSTI: CI inyecta **comando del SO** (terminal); SSTI inyecta **plantilla** (motor de plantillas)

### A04: Insecure Design
- Threat modeling, rate limiting, logica de negocio

### A05: Security Misconfiguration
- /.git/, /.env, /backup.zip, headers faltantes

### A06: Vulnerable Components
- npm audit, pip-audit, dependency-check

### A07: Authentication Failures
- hydra (fuerza bruta), credential stuffing, session fixation
- Session IDs predecibles (historico): iterar sobre valores → hoy pseudoaleatorios, practicamente inviable
- Robo de cookies moderno: **Adversary in the Middle** — phishing con pagina identica que roba la **cookie de sesion** en vez de usuario/contrasena
- WordPress: WPScan para enum de usuarios (API REST), plugins y vulnerabilidades; la fuerza bruta es el **ultimo recurso**

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
- Variantes de traversal a probar en orden:
  - `../../` — el clasico, cuando el codigo concatena una carpeta base
  - `....//` — doble encode, util cuando el desarrollador filtra literalmente la cadena `../`
  - Ruta absoluta (`/etc/passwd`) — cuando el codigo parte desde la raiz y el relativo no aplica
- `php://filter` (lectura de fuente PHP), RFI
- De LFI a clave SSH: leer `/home/<usuario>/.ssh/id_rsa` → `ssh usuario@IP -i id_rsa` (sin contrasena)
- Si no hay clave: `hydra -l <usuario> -P diccionario.txt ssh://<IP>`

### XXE
- External entities, OOB XXE
- Payload clasico (write-ups Castor/Nike):

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
```

### SSTI
- `{{7*7}}`, config, subclasses

### File Upload (3 vias — clase 35)
- Plugin de administracion de ficheros (ej. WP File Manager)
- Editor de temas del CMS (inyectar PHP en plantilla)
- Editor de fichero de error/404 (ej. `404.php`) → reverse shell
- Deteccion: si el servidor **muestra el codigo fuente** del PHP subido → no interpreta; si ejecuta → explotable

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
| Fuzzing | ffuf, feroxbuster, gobuster, dirsearch, wfuzz |
| SQLi | sqlmap |
| XSS | dalfox, xsstrike |
| SSRF | ssrfmap, Gopherus |
| SSTI | tplmap |
| XXE | xxeinjector |
| CMS | wpscan (enum usuarios, plugins, vulnerabilidades) |
| Automatizado | nuclei, wapiti, nikto |
| Proxy | Burp Suite, OWASP ZAP |

---

## Referencias

- OWASP Top 10 2021/2025
- OWASP Testing Guide
- PortSwigger Web Security Academy
- HackTricks Web
- PayloadsAllTheThings









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Repaso de Enumeración Web.md|Repaso de Enumeración Web]] — GoBuster, Seguridad, XXE
- [[../00 - Referencia/Glosario de Ciberseguridad.md|Glosario de Ciberseguridad]] — File Upload, Seguridad, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase55.md|resumen_master_clase55]] — GoBuster, Seguridad, XXE
- [[../../apuntes Chema/PortSwigger - Introducción y Path Traversal.md|PortSwigger - Introducción y Path Traversal]] — File Upload, Seguridad, XXE
- [[../../apuntes Chema/Glosario de Ciberseguridad.md|Glosario de Ciberseguridad]] — FFUF, Seguridad, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Node/seguridad_node.md|seguridad_node]] — Programacion: Funcional, Seguridad, Testing
- [[../../../programacion/JavaScript/seguridad_javascript.md|seguridad_javascript]] — Programacion: DevOps, Seguridad, Testing

> #burpsuite #cli #cloud_base #command_injection #crypto #database #devops #dirsearch #feroxbuster #ffuf #file_upload #funcional #git #gobuster #hydra #idor #javascript #lfi #metasploit #metasploitable #netcat #osint #pentest #pivoting #post_explotacion #python #redes #rfi #seguridad #sql #sqli #sqlmap_tool #ssh_tool #ssrf #ssti #testing #web #xss #xxe
