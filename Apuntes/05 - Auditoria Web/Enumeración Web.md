

> [!info] Relacionado con
> [[Apuntes/05 - Auditoria Web/Repaso de EnumeraciÃ³n Web]] Â· [[Fuzzing Web con ffuf]] Â· [[Burp Suite - Framework de AuditorÃ­a]] Â· [[OSINT - MetodologÃ­a y Fuentes]] Â· [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web|EnumeraciÃ³n Web]] Â· [[Nmap - Escaneo y EnumeraciÃ³n]]
> â†’

---

## â‘  Â¿QuÃ© es la enumeraciÃ³n web?

Descubrir **toda la superficie** de una aplicaciÃ³n web: tecnologÃ­as, rutas, ficheros, subdominios y puntos de entrada. **No se explota nada todavÃ­a**, se construye el mapa.

> [!important] Idea central
> Cuanto mÃ¡s completo es el mapa, mÃ¡s superficie de ataque tienes. La mayorÃ­a de hallazgos crÃ­ticos aparecen aquÃ­, no explotando un 0-day.

---

## â‘¡ Pasiva vs Activa

| Tipo | QuÃ© hace | Toca el objetivo |
|------|---------|-----------------|
| **Pasiva** | Recopila info sin trÃ¡fico directo | No |
| **Activa** | InteractÃºa con el servidor | SÃ­ |

> [!warning] RUIDO
> La enumeraciÃ³n activa genera trÃ¡fico que queda en logs. Puede disparar WAFs/IDS. Empieza siempre por lo pasivo.

---

## â‘¢ MetodologÃ­a en 5 fases

```
1. Recon pasivo â†’ 2. Fingerprint stack â†’ 3. Subdominios â†’ 4. Directorios â†’ 5. Endpoints
```

### Fase 1 â€” Reconocimiento pasivo

- **crt.sh** (certificados TLS): revelan subdominios
- **Wayback Machine**: rutas antiguas
- **Google Dorks**: site:objetivo.com filetype:pdf

### Fase 2 â€” Fingerprint del stack

```bash
whatweb -a 3 http://OBJETIVO # identificar tecnologÃ­as
curl -sI http://OBJETIVO # cabeceras HTTP
```

| Pista | QuÃ© revela |
|-------|-----------|
| Cabecera Server | Servidor web |
| X-Powered-By | Lenguaje/framework |
| Cookies | PHPSESSID â†’ PHP, JSESSIONID â†’ Java |
| Extensiones | .php, .aspx, .jsp |

> [!tip] CMS
> Si detectas WordPress â†’ el siguiente paso es **[[WPScan]]**. Cada CMS tiene rutas y vulnerabilidades tÃ­picas.

### Fase 3 â€” Subdominios

```bash
subfinder -d OBJETIVO.com -o subdominios.txt # fuentes pasivas
[[FFUF]] -u http://OBJETIVO -H 'Host: FUZZ.OBJETIVO.com' \
 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

### Fase 4 â€” Directorios y ficheros

| Herramienta | Punto fuerte |
|------------|-------------|
| **[[Feroxbuster]]** | Recursividad automÃ¡tica |
| **Gobuster** | Control de extensiones (-x) |
| **[[FFUF]]** | El mÃ¡s flexible (FUZZ keyword) |
| **Dirsearch** | Diccionarios por defecto bien pensados |

```bash
[[Feroxbuster]] -u http://OBJETIVO -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
gobuster dir -u http://OBJETIVO -w common.txt -x php,txt,bak,old
```

### Fase 5 â€” Endpoints y parÃ¡metros

```bash
[[FFUF]] -u 'http://OBJETIVO/index.php?FUZZ=test' \
 -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 0
```

> [!tip] Marco mental de 4 elementos
> Cada parÃ¡metro descubierto es una **FUENTE** que el servidor **PROCESA**. Identificarlos aquÃ­ es localizar dÃ³nde podrÃ¡s atacar despuÃ©s.

---

## â‘£ Errores comunes

- **Saltarse el recon pasivo**: pierdes subdominios y contexto
- **No respetar el scope**: ilegal
- **Ignorar el fingerprint**: wordlists genÃ©ricas reducen hallazgos
- **No filtrar respuestas**: el ruido de 404 esconde lo importante

---

## Checklist de repaso

- [ ] Â¿SÃ© la diferencia entre enumeraciÃ³n pasiva y activa?
- [ ] Â¿Puedo hacer fingerprint con WhatWeb y curl?
- [ ] Â¿SÃ© enumerar subdominios con Subfinder y [[FFUF]]?
- [ ] Â¿Domino [[Feroxbuster]]/Gobuster/[[FFUF]] para directorios?
- [ ] Â¿Entiendo cÃ³mo descubrir parÃ¡metros ocultos?

â†’

â†’

