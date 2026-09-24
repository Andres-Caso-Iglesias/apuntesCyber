

> [!info] Relacionado con
> [[Apuntes/05 - Auditoria Web/Repaso de Enumeración Web]] · [[Fuzzing Web con ffuf]] · [[Burp Suite - Framework de Auditoría]] · [[OSINT - Metodología y Fuentes]] · [[Apuntes/05 - Auditoria Web/Enumeración Web|Enumeración Web]] · [[Nmap - Escaneo y Enumeración]]
> 

---

## ① ¿Qué es la enumeración web?

Descubrir **toda la superficie** de una aplicación web: tecnologías, rutas, ficheros, subdominios y puntos de entrada. **No se explota nada todavía**, se construye el mapa.

> [!important] Idea central
> Cuanto más completo es el mapa, más superficie de ataque tienes. La mayoría de hallazgos críticos aparecen aquí, no explotando un 0-day.

---

## ② Pasiva vs Activa

| Tipo | Qué hace | Toca el objetivo |
|------|---------|-----------------|
| **Pasiva** | Recopila info sin tráfico directo | No |
| **Activa** | Interactúa con el servidor | Sí |

> [!warning] RUIDO
> La enumeración activa genera tráfico que queda en logs. Puede disparar WAFs/IDS. Empieza siempre por lo pasivo.

---

## ③ Metodología en 5 fases

```
1. Recon pasivo → 2. Fingerprint stack → 3. Subdominios → 4. Directorios → 5. Endpoints
```

### Fase 1 "” Reconocimiento pasivo

- **crt.sh** (certificados TLS): revelan subdominios
- **Wayback Machine**: rutas antiguas
- **Google Dorks**: site:objetivo.com filetype:pdf

### Fase 2 "” Fingerprint del stack

```bash
whatweb -a 3 http://OBJETIVO # identificar tecnologías
curl -sI http://OBJETIVO # cabeceras HTTP
```

| Pista | Qué revela |
|-------|-----------|
| Cabecera Server | Servidor web |
| X-Powered-By | Lenguaje/framework |
| Cookies | PHPSESSID → PHP, JSESSIONID → Java |
| Extensiones | .php, .aspx, .jsp |

> [!tip] CMS
> Si detectas WordPress → el siguiente paso es **[[WPScan]]**. Cada CMS tiene rutas y vulnerabilidades típicas.

### Fase 3 "” Subdominios

```bash
subfinder -d OBJETIVO.com -o subdominios.txt # fuentes pasivas
[[FFUF]] -u http://OBJETIVO -H 'Host: FUZZ.OBJETIVO.com' \
 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

### Fase 4 "” Directorios y ficheros

| Herramienta | Punto fuerte |
|------------|-------------|
| **[[Feroxbuster]]** | Recursividad automática |
| **Gobuster** | Control de extensiones (-x) |
| **[[FFUF]]** | El más flexible (FUZZ keyword) |
| **Dirsearch** | Diccionarios por defecto bien pensados |

```bash
[[Feroxbuster]] -u http://OBJETIVO -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
gobuster dir -u http://OBJETIVO -w common.txt -x php,txt,bak,old
```

### Fase 5 "” Endpoints y parámetros

```bash
[[FFUF]] -u 'http://OBJETIVO/index.php?FUZZ=test' \
 -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 0
```

> [!tip] Marco mental de 4 elementos
> Cada parámetro descubierto es una **FUENTE** que el servidor **PROCESA**. Identificarlos aquí es localizar dónde podrás atacar después.

---

## ④ Errores comunes

- **Saltarse el recon pasivo**: pierdes subdominios y contexto
- **No respetar el scope**: ilegal
- **Ignorar el fingerprint**: wordlists genéricas reducen hallazgos
- **No filtrar respuestas**: el ruido de 404 esconde lo importante
- **No mirar el código fuente del front**: comentarios, rutas sensibles y endpoints desconocidos quedan ahí
- **Omitir robots.txt**: dice qué NO indexar — para el pentester son los directorios más interesantes

---

## ⑤ Auditoría manual paso a paso (antes de las herramientas)

```
Ver código fuente → robots.txt → DirSearch/ffuf → Analizar funcionalidades → Explotar
```

| Paso | Qué buscar |
|------|-----------|
| **Código fuente del front** | Comentarios con rutas sensibles, referencias a APIs, endpoints olvidados |
| **robots.txt** | Directorios ocultos (probar también en subdirectorios: `/twiki/robots.txt`) |
| **Enumeración con diccionario** | DirSearch / ffuf / Feroxbuster — la diferencia está en el diccionario |
| **Fingerprint (Wappalyzer)** | Tecnología detectada → elegir herramienta (WordPress → WPScan) |

> [!info] robots.txt como segundo paso
> Siempre es el segundo paso en cualquier auditoría web. Revela exactamente los directorios que el propietario quiere esconder.

### Cabeceras HTTP a inspeccionar

| Cabecera | Qué revela |
|----------|-----------|
| `Server` | Servidor web y versión |
| `X-Powered-By` | Lenguaje/framework (PHP, ASP.NET…) |
| `Set-Cookie` flags | `HttpOnly`, `Secure`, `SameSite` — ausencia = sesión vulnerable a robo vía XSS |
| `Location` | Redirecciones (301/302) → rutas internas |
| `Content-Security-Policy` | Política de seguridad del front |

```bash
curl -vI http://OBJETIVO   # verbose: muestra headers completos + redirecciones
curl -sI http://OBJETIVO    # solo cabeceras
```

### Herramientas complementarias

| Herramienta | Uso |
|-------------|-----|
| **Nikto** | Escáner genérico de servidor (config débil, ficheros peligrosos, versiones) |
| **Wappalyzer** | Fingerprint visual desde el navegador |
| **whatweb** | Fingerprint desde CLI |

> [!warning] HTTP 500 como señal
> Un 500 Internal Server Error durante la enumeración puede indicar que procesaste input de forma inesperada (posible SQLi, error de path…). No lo descartes: anota la ruta y prueba payloads.

### El bucle de auditoría

```
Enviar → Observar → Comparar → Documentar → Hipótesis → Evaluar
```

> [!important] Cada respuesta se compara con la anterior
> Sin una línea base (baseline), no puedes saber qué es anómalo. Documenta TODO aunque parezca irrelevante.

### Labs de PortSwigger para practicar

- **Web Cache Detection** — cómo detectar qué respuestas sirve la caché
- **HTTP Request Smuggling** — desincronización front/back
- **Information disclosure** — headers y respuestas que filtran datos

---

## ⑥ Casos de éxito típicos

| Hallazgo en enumeración | Siguiente paso |
|------------------------|----------------|
| `backup.zip` / `backup.php` | Descargar, crackear hashes (zip2john + John) |
| Formulario de login | Probar SQLi con comilla |
| `/uploads` | File upload → webshell |
| `/wp-login.php` (302) | WPScan + fuerza bruta de login |
| Comentarios HTML con usuarios | Candidatos a spraying |
| Versión antigua de software | Buscar CVE público |

---

## Checklist de repaso

- [ ] ¿Sé la diferencia entre enumeración pasiva y activa?
- [ ] ¿Puedo hacer fingerprint con WhatWeb y curl?
- [ ] ¿Sé enumerar subdominios con Subfinder y [[FFUF]]?
- [ ] ¿Domino [[Feroxbuster]]/Gobuster/[[FFUF]] para directorios?
- [ ] ¿Entiendo cómo descubrir parámetros ocultos?
- [ ] ¿Reviso siempre código fuente y robots.txt antes de lanzar diccionarios?
- [ ] ¿Inspecciono cabeceras (Server, Set-Cookie, Location) con curl?
- [ ] ¿Sé cuándo un 500 es una pista y no un fallo?
- [ ] ¿Aplico el bucle: Enviar → Observar → Comparar → Documentar?
- [ ] ¿Conozco Nikto como escáner complementario?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Enumeración Web.md|Enumeración Web]] — DirSearch, GoBuster, WPScan
- [[../../apuntes Chema/Auditoria web.md|Auditoria web]] — Robots.txt, Command Injection, Nmap
- [[../../apuntes Andres/22.06.2026 Metodologías de Enumeración Web.md|22.06.2026 Metodologías de Enumeración Web]] — DirSearch, GoBuster, WAF
- [[../../comandos/FFUF.md|FFUF]] — Desarrollo Web, DirSearch, GoBuster
- [[../../comandos/DirSearch.md|DirSearch]] — Desarrollo Web, DirSearch, GoBuster
- [[../../comandos/Feroxbuster.md|Feroxbuster]] — Desarrollo Web, DirSearch, GoBuster
- [[Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]] — Desarrollo Web, DirSearch, GoBuster
- [[../../apuntes Chema/Anonimato, Ingeniería Social y Enumeración Web.md|Anonimato, Ingeniería Social y Enumeración Web]] — GoBuster, Kali Linux, Fuzzing

### 🌐 Cross-Dominio

- [[../../../programacion/Perl/fundamentos_perl.md|fundamentos_perl]] — Programacion: Criptografia, Java, Redes
- [[../../../programacion/Ruby/seguridad_ruby.md|seguridad_ruby]] — Programacion: Desarrollo Web, Java, Redes

> #burpsuite #crypto #dirsearch #feroxbuster #ffuf #gobuster #google_dorks #java #nmap #nikto #osint #pentest #redes #web #wordpress #wpscan #headers #curl
