

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

---

## Checklist de repaso

- [ ] ¿Sé la diferencia entre enumeración pasiva y activa?
- [ ] ¿Puedo hacer fingerprint con WhatWeb y curl?
- [ ] ¿Sé enumerar subdominios con Subfinder y [[FFUF]]?
- [ ] ¿Domino [[Feroxbuster]]/Gobuster/[[FFUF]] para directorios?
- [ ] ¿Entiendo cómo descubrir parámetros ocultos?



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Enumeración Web.md|Enumeración Web]] — GoBuster, Nmap, OSINT
- [[../../comandos/FFUF.md|FFUF]] — FFUF, GoBuster, Nmap
- [[../../apuntes Chema/OWASP API Top 10.md|OWASP API Top 10]] — FFUF, Feroxbuster, Nmap
- [[Fuzzing Web con ffuf.md|Fuzzing Web con ffuf]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/BurpSuite.md|BurpSuite]] — FFUF, Redes, WordPress
- [[../comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Nmap|Nmap]]
- [[comandos/WPScan|WPScan]]

> #burpsuite #dirsearch #feroxbuster #ffuf #gobuster #google-dorks #nmap #osint #pentest #redes #wordpress #wpscan
