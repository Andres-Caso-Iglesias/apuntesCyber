# 🧠 Red de Conocimiento — Ciberseguridad

> **Tu red neuronal de ciberseguridad.** Cada nodo es un apunte. Cada enlace es una sinapsis. Navega por temas, conceptos o máquinas.

> **Archivos:** 243 .md | **Última actualización:** 25 de Agosto 2026

---

## 🌐 01 — Fundamentos de Redes

| Apunte | Tema clave |
| -------------------------------------- | ----------------------------------------------- |
| [[Redes - Modelo OSI y TCP-IP]] | Las 7 capas, TCP vs UDP, puertos |
| [[Redes - Direccionamiento IP y DNS]] | IPv4, CIDR, subredes, resolución DNS |
| [[Redes - Topologías y Encapsulación]] | Tipos de red, topologías, cómo viajan los datos |

> [!note] Notas de clase (Chema)
> - [[Introducción a Redes]] — Conceptos de red, OSI, TCP/IP, puertos, DNS
> - [[Redes-Tipologías, Datagramas y Paquetes de Red]] — Tipología de red, datagramas, paquetes

---

## 💻 02 — Sistemas Operativos

| Apunte | Tema clave |
|--------|-----------|
| [[Linux - Fundamentos]] | Ficheros, permisos, comandos esenciales |
| [[Linux - Bash Scripting]] | Variables, bucles, funciones, automatización |
| [[Consolas - Bash y PowerShell]] | Comparativa, atajos, gestores de paquetes |

> [!note] Notas de clase (Chema)
> - [[Migrar una Máquina Virtual de VirtualBox a VMware Workstation]] — VirtualBox → VMware, formato VMDK

---

## 🔍 03 — Herramientas de Análisis

| Apunte | Tema clave |
|--------|-----------|
| [[Nmap - Escaneo y Enumeración]] | Fases de escaneo, scripts, detección de servicios |
| [[Wireshark - Análisis de Tráfico]] | Filtros BPF/visualización, TCP handshake, detección de ataques |

> [!note] Notas de clase (Chema)
> - [[Wireshark]] — Análisis de tráfico, filtros, captura de paquetes

---

## 🕵️ 04 — OSINT y Recopilación

| Apunte | Tema clave |
|--------|-----------|
| [[OSINT - Metodología y Fuentes]] | Google Dorks, Sherlock, WHOIS, DNS, Shodan |
| [[Esteganografía y Metadatos]] | EXIF, steghide, binwalk, strings, búsqueda inversa |

> [!note] Notas de clase (Chema)
> - [[OSINT - Mapeando la Superficie de una Organización]] — Superficie de ataque, fuentes OSINT
> - [[OSINT y Esteganografía]] — OSINT práctico + esteganografía (EXIF, steghide, binwalk)

---

## 🌍 05 — Auditoría Web

| Apunte | Tema clave |
|--------|-----------|
| [[OWASP Top 10 - CVE CVSS CWE]] | Los 4 marcos de referencia y la cascada |
| [[Burp Suite - Framework de Auditoría]] | Proxy, Repeater, Intruder, configuración |
| [[Enumeración Web]] | Fases: recon pasivo → fingerprint → subdominios → directorios |
| [[apuntes Chema/Repaso de Enumeración Web]] | Repaso práctico: URLs, endpoints, spraying, fuzzing, caso Bashed |
| [[Fuzzing Web con ffuf]] | FUZZ keyword, wordlists, filtrado de respuestas |
| [[WordPress - Auditoría con WPScan]] | CMS, plugins, fuerza bruta, RCE por editor de temas |
| [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] | OWASP 2025, CVSS/CWE/CVE, Burp Suite desde cero |
| [[Auditoria Web — Práctica con Metasploitable]] | FTP anon, Command Injection, robots.txt, SSH no estándar |
| [[Fuzzing de parámetros con x8 — Rockstar]] | Motor x8: learn/batch/bisect, parámetro backdoor |
| [[Anonimato, Ingeniería Social y Enumeración Web]] | VPN/Monero/Tor, QRishing, RaaS, enum web Rockstar |
| [[apuntes Andres/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress\|Andrés — WordPress Academy]] | WPScan, file upload, reverse shell |
| [[apuntes Andres/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking\|Andrés — Fuzzing + Script Hijacking]] | Fuzzing, directory listing, script hijacking |
| [[06.07.2026 Fuzzing de Parámetros, Ingeniería Social y Anonimato\|Andrés — Fuzzing params + OSINT]] | Fuzzing de parámetros, OSINT, anonimato |
| [[09.07.2026 XXE - XML External Entity y Máquina Castor\|Andrés — XXE + Castor]] | XXE, máquina Castor |
| [[apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor\|Andrés — XXE avanzado + Nike/Castor]] | XXE avanzado, Nike, Castor |
| [[11.07.2026 Owasp Top 10 XXE Labs II\|Andrés — XXE Labs II]] | XXE labs OWASP |
| [[apuntes Andres/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)\|Andrés — SQLi + Injected]] | SQLi, máquina Injected |
| [[17.07.2026 PortSwigger Intro y 6 Casos Path Traversal\|Andrés — Path Traversal 6 casos]] | Path Traversal, PortSwigger |
| [[20.07.2026 PortSwigger SSRF\|Andrés — SSRF]] | SSRF, PortSwigger |
| [[21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI\|Andrés — SSRF avanzado + SSTI]] | SSRF avanzado, SSTI |
| [[SSRF — Server-Side Request Forgery]] | SSRF: definición, bypasses, Blind SSRF, checklist |
| [[SSTI — Server-Side Template Injection]] | SSTI: detección, motores, RCE, labs |
| [[XXE — XML External Entity]] | XXE: XML, SYSTEM entity, lectura ficheros, 4 file upload |
| [[Path Traversal — 6 Casos y Bypasses]] | Path Traversal: 6 casos, bypasses, flowchart |
| [[SQL Injection]] | SQLi: definición, técnicas (UNION/error/blind), SQLMap, prepared statements, máquina Injected |

> [!note] Notas de clase (Chema)
> - [[Vulnerabilidades Web]] — Vulnerabilidades web comunes, explotación
> - [[Burp Suite a fondo · Auditoría web · WordPress]] — Burp Suite completo, auditoría WordPress
> - [[Fuzzing Web]] — Fuzzing de directorios y parámetros
> - [[Auditoria web]] — Metodología completa: reconocimiento → escaneo → FTP → Command Injection → SSH

---

## ⚔️ 06 — Explotación y Post-Explotación

| Apunte | Tema clave |
|--------|-----------|
| [[Metodología de Explotación]] | Marco mental de 4 elementos, fases del pentest |
| [[Explotación de Servicios - Linux]] | NFS, SSH, hashes, John/Hashcat |
| [[Explotación de Servicios - Windows]] | SMB, MSSQL, xp_cmdshell, WinPEAS |
| [[Escalada de Privilegios]] | SUID, PATH hijacking, GTFOBins, LinPEAS |
| [[Reverse Shells y Post-Explotación]] | Tipos de shell, estabilización TTY, transferencia de archivos |
| [[Prácticas CTF - HTB y VulnHub]] | Máquinas resueltas: RickdiculouslyEasy, Mr. Robot, Oopsie, Archetype, Vaccine |
| [[Explotación de Máquinas Locales I — Oopsie y Archetype]] | IDOR, web shell, SMB null session, MSSQL xp_cmdshell, WinPEAS |
| [[Explotación Avanzada de Servicios Vulnerables II — Metasploitable]] | SMTP enum, NFS montaje, hashes, SSH keys, VNC, Burp Suite |
| [[Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]] | NFS, PostgreSQL, Tomcat WAR upload, Command/SQL Injection |
| [[Rockstar — Escalada Linux y LFI]] | Cadena shark→root, 4 técnicas sudo -l, LFI/Path Traversal |
| [[07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]] | Rockstar: 4 escaladas (ejecutable, Hydra, library hijacking, sh) |
| [[08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] | Banco: Path traversal → LFI → credenciales → SUID + cronjob |
| [[Son ROBOTS — RickdiculouslyEasy y Mr. Robot]] | CTF interna: enum, robo ficheros, Hydra, Burp Intruder |
| [[Cierre de Vaccine + Máquina Oopsie]] | SQLMap, TTY upgrade, GTFOBins vi, IDOR, cookie tampering |
| [[Anonimato e Ingeniería Social]] | VPN, Tor, Monero, cadena de anonimización, phishing/QRishing, RaaS, fuzzing de parámetros |

---

## 🎯 17 — Máquinas Resueltas

> [!tip] Organizadas por plataforma
> Cada máquina es un caso real de explotación. Estudialas en orden de dificultad.

### 🟣 Hack The Box

| Máquina | Dificultad | Servicios clave | Apunte | Notas Chema |
|---------|-----------|-----------------|--------|-------------|
| **Vaccine** | Easy | [[comandos/Nmap\|FTP]], [[comandos/SQLMap\|PostgreSQL]], PHP webapp | [[Cierre de Vaccine + Máquina Oopsie]] | [[Vaccine]] · [[Cierre de Vaccine + Máquina Oopsie]] |
| **Vaccine (Tier 2)** | Easy | Repaso en profundidad | [[Vaccine (Tier 2) — Repaso en profundidad]] | [[Vaccine (Tier 2) — Repaso en profundidad]] |
| **Oopsie** | Easy | IDOR, [[comandos/Metasploit\|web shell]], [[comandos/BurpSuite\|cookie tampering]] | [[Explotación de Máquinas Locales I — Oopsie y Archetype]] | [[Explotación de Máquinas Locales I]] |
| **Archetype** | Easy | [[comandos/SMB_Impacket\|SMB]], [[comandos/SMB_Impacket\|MSSQL]], [[comandos/SMB_Impacket\|xp_cmdshell]] | [[Explotación de Máquinas Locales I — Oopsie y Archetype]] | [[Explotación de Máquinas Locales I]] |
| **Starting Point T0** | Very Easy | [[comandos/Telnet\|Telnet]] (Meow), [[comandos/Nmap\|FTP]] (Fawn), [[comandos/SMB_Impacket\|SMB]] (Dancing), Redis (Redeemer) | [[Hack The Box- Starting Point — Tier 0]] | [[Hack The Box- Starting Point — Tier 0]] |
| **Starting Point T1** | Very Easy | Servicios varios | [[HackTheBox Starting Point — Tier 1]] | [[HackTheBox Starting Point — Tier 1]] |
| **Nibbles** | Easy/Medium | [[apuntes Chema/Maquinas/Nibbles_HTB\|CVE-2015-6967]] Nibbleblog, [[comandos/SSH\|sudo NOPASSWD]], SUID bash | [[apuntes Chema/Maquinas/Nibbles_HTB]] | [[apuntes Chema/Maquinas/Nibbles_HTB]] |
| **Reactor** | Medium/High | [[apuntes Chema/Maquinas/Reactor_HTB\|CVE-2025-29927]] Next.js, Node.js Inspector, WebSocket CDP | [[apuntes Chema/Maquinas/Reactor_HTB]] | [[apuntes Chema/Maquinas/Reactor_HTB]] |
| **Starting Point T2** | Easy | Repaso y escalada | [[HTB Starting Point — Repaso e inicio de Tier 2]] | [[HTB Starting Point — Repaso e inicio de Tier 2]] |

### 🔵 HackerLabs / Evolve Academy

| Máquina | Plataforma | Servicios clave | Apunte | Notas Chema |
|---------|-----------|-----------------|--------|-------------|
| **Rockstar** | HackerLabs | Escalada linux, [[apuntes Chema/Enumeración Web\|LFI]], [[apuntes Chema/Enumeración Web\|Path Traversal]] | [[Rockstar — Escalada Linux y LFI]] | [[Rockstar — Escalada Linux y LFI]] |
| **Rockstar (x8)** | HackerLabs | [[comandos/FFUF\|Fuzzing]], backdoor | [[Fuzzing de parámetros con x8 — Rockstar]] | [[Fuzzing de parámetros con x8 — Rockstar]] |
| **Rockstar (Andres)** | HackerLabs | Fuzzing de parámetros, infraestructura anónima, ingeniería social | [[06.07.2026 Fuzzing de Parámetros, Ingeniería Social y Anonimato]] | — |
| **Academy** | HackerLabs | [[comandos/WPScan\|WordPress]], plugins, RCE | [[Auditoría de CMS — WordPress (máquina Academy)]] | [[Auditoría de CMS — WordPress (máquina Academy)]] |
| **Rockstar (Andres)** | HackerLabs | Escalada 4 técnicas: ejecutable, Hydra, library hijacking, sh | [[07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]] | — |
| **Banco (Andres)** | HackerLabs | Path traversal, LFI, credenciales, SUID + cronjob | [[08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] | — |
| **RickdiculouslyEasy** | CTF interna | [[comandos/FFUF\|Enum web]], robo ficheros | [[Son ROBOTS — RickdiculouslyEasy y Mr. Robot]] | [[Son ROBOTS]] |
| **Mr. Robot** | CTF interna | [[comandos/Hydra\|Hydra]], [[comandos/BurpSuite\|Burp Intruder]], diccionario | [[Son ROBOTS — RickdiculouslyEasy y Mr. Robot]] | [[Son ROBOTS]] |

### 🟢 Lab Local (Metasploitable / DVWA)

| Máquina | Entorno | Servicios clave | Apunte | Notas Chema |
|---------|---------|-----------------|--------|-------------|
| **Metasploitable 2** | VMware/VirtualBox | [[comandos/Nmap\|SMTP]], [[comandos/SMB_Impacket\|NFS]], [[comandos/Nmap\|SSH]], [[comandos/Nmap\|VNC]], [[comandos/BurpSuite\|Burp Suite]] | [[Explotación Avanzada de Servicios Vulnerables II — Metasploitable]] | [[Explotación avanzada de servicios vulnerables II]] |
| **Metasploitable (servicios)** | Lab local | [[comandos/SMB_Impacket\|NFS]], [[comandos/SQLMap\|PostgreSQL]], [[comandos/Nmap\|Tomcat]], [[comandos/Metasploit\|Command Injection]], [[comandos/SQLMap\|SQL Injection]] | [[Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]] | [[Explotación Avanzada de Servicios Vulnerables III]] |
| **Oopsie + Archetype** | HTB | IDOR, [[comandos/SMB_Impacket\|SMB]], [[comandos/SMB_Impacket\|MSSQL]] | [[Explotación de Máquinas Locales I — Oopsie y Archetype]] | [[Explotación de Máquinas Locales I]] |

### 📊 Resumen por plataforma

| Platforma | Máquinas | Dificultad media |
|-----------|----------|-----------------|
| Hack The Box | 9 | Easy-Medium |
| HackerLabs / Evolve | 8 | Easy-Medium |
| Lab Local | 3 | Easy-Medium |
| **Total** | **20** | |

---

## 💼 07 — Empleabilidad

> [!tip] Tu futuro no depende solo de saber hackear
> Saber explotar máquinas no sirve de nada si nadie lo sabe. Esta sección te ayuda a convertir conocimiento en carrera.

| Apunte | Tema clave |
|--------|-----------|
| [[Mercado Laboral y Certificaciones]] | Diferencias con programación, nivel junior, certificaciones (eJPT, CREST, OSCP), roadmap de estudio |
| [[Portafolio y Visibilidad]] | Blog, GitHub, HTB, LinkedIn, presencia pública, cómo te encuentran las empresas |

### Notas de clase (Chema)

| Apunte | Tema clave |
|--------|-----------|
| [[Mercado Laboral y Servicios]] | Servicios del sector, tipos de empresa, qué buscan |
| [[Empleabilidad en Ciberseguridad]] | Plan de acción, hábitos, cómo posicionarte |

### Checklist de empleabilidad

- [ ] Perfil activo en HTB/THM con máquinas resueltas
- [ ] GitHub con proyectos/scripts propios
- [ ] LinkedIn optimizado con keywords de ciberseguridad
- [ ] Al menos 1 certificación en progreso o obtenida
- [ ] Blog o artículos publicados (1 mínimo)
- [ ] Perfil de bug bounty (HackerOne, Bugcrowd)

---

## 📋 08 — Metodologías de Explotación

> [!tip] Guías concisas por tipo de máquina

| Metodología | Objetivo |
|-------------|----------|
| [[Metodología - Explotación Linux\|Explotación Linux]] | Máquinas Linux standalone |
| [[Metodología - Explotación Windows\|Explotación Windows]] | Máquinas Windows standalone |
| [[Metodologia - Aplicaciones Web\|Aplicaciones Web]] | Auditar y explotar webapps |
| [[Metodología - Active Directory\|Active Directory]] | Entornos AD corporativos |

---

## 🔀 09 — Pivoting y Movilidad Lateral

> [!tip] Trampolines entre redes
> Una vez comprometida una máquina, el pivoting te permite alcanzar subredes internas inalcanzables directamente.

| Apunte | Tema clave |
|--------|-----------|
| [[Pivoting y Movilidad Lateral]] | Túneles SSH (local/remote/dynamic), ProxyChains, socat, port forwarding |

> [!note] Relacionado con:
> - [[Metodología de Explotación]] — Marco mental para el pentest
> - [[Escalada de Privilegios]] — Después del pivoting, escalar en la nueva máquina
> - [[Reverse Shells y Post-Explotación]] — Tipos de shell y estabilización

---

## 📡 10 — Redes WiFi y Hardware

> [!tip] Auditoría inalámbrica y emergentes
> WiFi es un vector de ataque frecuente en entornos corporativos. Car Hacking es una línea emergente con alto impacto.

| Apunte | Tema clave |
|--------|-----------|
| [[Auditoría WiFi y Car Hacking]] | WPA/WPA2 handshake, WiFi Enterprise (EAP), Evil Twin, Car Hacking |

> [!note] Relacionado con:
> - [[Nmap - Escaneo y Enumeración]] — Descubrimiento de redes WiFi
> - [[Wireshark - Análisis de Tráfico]] — Análisis de tráfico WiFi capturado

---

## 🔬 11 — Forense Digital

> [!tip] Evidencia digital y análisis de memoria
> El forense es la contraparte defensiva del pentesting: preservar y analizar evidencia de compromisos.

| Apunte | Tema clave |
|--------|-----------|
| [[Análisis Forense y Memoria]] | Orden de volatilidad, cadena de custodia, adquisición de memoria, Volatility 3 |

> [!note] Relacionado con:
> - [[Escalada de Privilegios]] — Técnicas que dejan huella forense
> - [[Wireshark - Análisis de Tráfico]] — Análisis de tráfico como evidencia

---

## 🛡️ 12 — Blue Team y SOC

> [!tip] Defensa activa y operaciones de seguridad
> El SOC vigila, analiza y responde a incidentes 24/7. Complemento esencial al lado ofensivo.

| Apunte | Tema clave |
|--------|-----------|
| [[Blue Team - SOC e Incidentes]] | SOC (N1/N2/N3), SIEM, MITRE ATT&CK, Wazuh, SOAR, phishing, EDR, LOLBins |

> [!note] Relacionado con:
> - [[Wireshark - Análisis de Tráfico]] — Filtros para el SOC
> - [[OSINT - Metodología y Fuentes]] — Inteligencia de amenazas
> - [[Anonimato, Ingeniería Social y Enumeración Web]] — Ingeniería social y defensa

---

## 📜 13 — Normativa y GRC

> [!tip] Marco regulatorio y gestión de riesgos
> ISO 27001, GDPR, ENS... Las normativas obligan a implementar medidas mínimas y generan demanda de profesionales.

| Apunte | Tema clave |
|--------|-----------|
| [[Normativa - ISO 27001, GDPR, ENS]] | ISO 27001 (SGSI, PDCA, cláusulas, Anexo A), ENS, GDPR, PCI DSS, DORA, NIS2, BCP |

> [!note] Relacionado con:
> - [[Blue Team - SOC e Incidentes]] — El SOC como parte del SGSI
> - [[Mercado Laboral y Certificaciones]] — Certificaciones de gestión

---

## 🤖 14 — IA en Ciberseguridad

> [!tip] Machine Learning, Deep Learning y LLMs aplicados a seguridad
> La IA amplifica tanto capacidades defensivas (detección) como ofensivas (phishing avanzado).

| Apunte | Tema clave |
|--------|-----------|
| [[IA en Ciberseguridad]] | Clasificador de spam (ML), autocodificadores (DL), LLMs en SOC, IA ofensiva, vulnerabilidades en LLMs |
| [[apuntes Andres/15.07.2026 IA Introducción y Vibe Coding\|Andrés — Vibe Coding + Agentes]] | Vibe Coding, agentes de IA, IA ofensiva |

> [!note] Relacionado con:
> - [[Blue Team - SOC e Incidentes]] — LLMs para triage y documentación
> - [[Anonimato, Ingeniería Social y Enumeración Web]] — IA para phishing y deepfakes

---

## 🎓 15 — Certificaciones

> [!tip] Preparación para exámenes de certificación
> ISO 27001 (gestión) y eJPTv2 (práctico) son las dos certificaciones clave para empezar en ciberseguridad.

| Apunte | Tema clave |
|--------|-----------|
| [[Certificaciones - ISO 27001 y eJPTv2]] | Formato, contenidos, planes de estudio, preguntas de práctica, errores frecuentes |

> [!note] Relacionado con:
> - [[Normativa - ISO 27001, GDPR, ENS]] — Teoría para el examen ISO 27001
> - [[Mercado Laboral y Certificaciones]] — Roadmap de certificaciones
> - [[Prácticas CTF - HTB y VulnHub]] — Práctica para eJPTv2

---

## 🛠️ 16 — Cheat Sheets (Comandos)

> [!info] Referencia rápida
> Tablas de comandos por herramienta. Cada apunte de teoría enlaza con su cheat sheet correspondiente.

| Cheat Sheet | Uso principal |
|-------------|---------------|
| [[comandos/Nmap\|Nmap]] | Escaneo de red, puertos, servicios, scripts NSE |
| [[comandos/Metasploit\|Metasploit]] | Framework de explotación, Meterpreter, post-explotación |
| [[comandos/BurpSuite\|Burp Suite]] | Proxy, Repeater, Intruder, scanning web |
| [[comandos/Hydra\|Hydra]] | Fuerza bruta contra servicios |
| [[comandos/FFUF\|FFUF]] | Web fuzzing, directorios, parámetros |
| [[comandos/Feroxbuster\|Feroxbuster]] | Fuzzing recursivo de directorios |
| [[comandos/GoBuster\|GoBuster]] | Directory/DNS/VHOST brute-force |
| [[comandos/SSH\|SSH]] | Acceso remoto, túneles, pivoting |
| [[comandos/SQLMap\|SQLMap]] | Inyección SQL automatizada |
| [[comandos/WPScan\|WPScan]] | Auditoría WordPress |
| [[comandos/John_Hashcat\|John / Hashcat]] | Cracking de hashes |
| [[comandos/SMB_Impacket\|SMB / Impacket]] | Enumeración y explotación SMB/Windows |
| [[comandos/Google_Dorks\|Google Dorks]] | Búsqueda avanzada OSINT |
| [[comandos/DirSearch\|DirSearch]] | Fuzzing de directorios (Python) |
| [[comandos/Telnet\|Telnet]] | Testing manual de puertos |
| [[comandos/Tmux\|Tmux]] | Multiplexor de terminal |
| [[comandos/Linux\|Linux]] | Comandos del sistema |
| [[comandos/Windows\|Windows]] | CMD y PowerShell |

---

## 📘 Bloques del Máster — Evolve Academy

> [!info] Programa completo del máster
> Cada bloque cubre un área del conocimiento de ciberseguridad. Orden secuencial recomendado.

| Bloque | Tema |
|--------|------|
| [[apuntes evolve/BLOQUE 1]] | Fundamentos: historia, roles, ética, tipos de hacker, normativa, mercado laboral |
| [[apuntes evolve/BLOQUE 2]] | Sistemas y redes: Linux, Windows, Kali, consolas, fundamentos de redes |
| [[apuntes evolve/BLOQUE 3]] | Metodología y OSINT: fases del pentest, enumeración pasiva/activa |
| [[apuntes evolve/BLOQUE 4]] | Explotación Web (OWASP Top 10): SQLi, XSS, LFI, SSRF, XXE, File Upload |
| [[apuntes evolve/BLOQUE 5]] | Explotación de SO: Linux (Shocker, SUID) y Windows (AD, BloodHound) |
| [[apuntes evolve/BLOQUE 6]] | Escalada de privilegios: SUID, cronjobs, sudo -l, capabilities, tokens |
| [[apuntes evolve/BLOQUE 7]] | Pivoting y movilidad lateral: túneles SSH, ProxyChains, socat |
| [[apuntes evolve/BLOQUE 8]] | Active Directory: BloodHound, NetExec, Kerberoasting, GPP, Responder |
| [[apuntes evolve/BLOQUE 9]] | Redes WiFi y Hardware: WPA/WPA2/WPA3, WiFi Enterprise, Car Hacking |
| [[apuntes evolve/BLOQUE 10]] | Forense y análisis de memoria: adquisición, Volatility |
| [[apuntes evolve/BLOQUE 11]] | Blue Team (SOC): logs, SIEM, MITRE ATT&CK, Wazuh, SOAR |
| [[apuntes evolve/BLOQUE 12]] | Normativa y GRC: ISO 27001, ENS, GDPR, PCI DSS, DORA, NIS2 |
| [[apuntes evolve/BLOQUE 13]] | IA en ciberseguridad: ML/DL, LLMs en SOC, IA ofensiva |
| [[apuntes evolve/BLOQUE 14]] | Examen ISO 27001: formato, cómo estudiar, simulacros |
| [[apuntes evolve/BLOQUE 15]] | Examen eJPTv2: formato, laboratorios, metodología de examen |

---

## 📝 Notas de Clase — Chema

> [!note] Apuntes de las clases impartidas por Chema
> Organizados por tema para facilitar la consulta por área de conocimiento.

### Redes

- [[apuntes Chema/Introducción a Redes]]
- [[apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red]]

### Sistemas

- [[apuntes Chema/Fundamentos de Linux]]
- [[apuntes Chema/Bash Scripting]]
- [[apuntes Chema/Bash y PowerShell]]
- [[apuntes Chema/Introducción a Consolas - Bash y PowerShell]]
- [[apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation]]

### Herramientas

- [[apuntes Chema/Wireshark]]

### OSINT

- [[apuntes Chema/OSINT - Mapeando la Superficie de una Organización]]
- [[apuntes Chema/OSINT y Esteganografía]]

### Auditoría Web

- [[Enumeración Web]]
- [[apuntes Chema/Repaso de Enumeración Web]]
- [[apuntes Chema/Fuzzing Web]]
- [[apuntes Chema/Auditoria web]]
- [[apuntes Chema/Burp Suite a fondo · Auditoría web · WordPress]]
- [[apuntes Chema/Vulnerabilidades Web]]
- [[apuntes Chema/OWASP Top 10, CVSS, CWE y CVE]]
- [[apuntes Chema/Anonimato, Ingeniería Social y Enumeración Web]]

### Explotación

- [[apuntes Chema/Apuntes_AuditoriaWeb_LFI_EscaladaLinux]]
- [[apuntes Chema/Apuntes_Sesion27_XXE_LFI_Nike]]

### Empleabilidad

- [[apuntes Chema/Mercado Laboral y Servicios]]
- [[apuntes Chema/Empleabilidad en Ciberseguridad]]
- [[apuntes Chema/Sesion_25_Repaso_MercadoLaboral_Servicios]]

---

## 📝 Notas de Sesión — Andrés

> [!note] Apuntes de las sesiones prácticas de Andrés
> Cada sesión cubre explotación real en máquinas o labs.

| Sesión | Tema clave |
|--------|-----------|
| [[apuntes Andres/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]] | WPScan, file upload, reverse shell |
| [[apuntes Andres/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]] | Fuzzing, directory listing, script hijacking |
| [[apuntes Andres/06.07.2026 Fuzzing de Parámetros, Ingeniería Social y Anonimato]] | Fuzzing params, OSINT, anonimato |
| [[apuntes Andres/07.07.2026 Explotación Avanzada - Escalada de Privilegios MultiPivote]] | 4 técnicas escalada |
| [[apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] | Path traversal, LFI, SUID |
| [[apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor]] | XXE, máquina Castor |
| [[apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]] | XXE avanzado |
| [[apuntes Andres/11.07.2026 Owasp Top 10 XXE Labs II]] | XXE labs OWASP |
| [[apuntes Andres/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]] | SQLi |
| [[apuntes Andres/15.07.2026 IA Introducción y Vibe Coding]] | Vibe Coding, agentes IA |
| [[apuntes Andres/17.07.2026 PortSwigger Intro y 6 Casos Path Traversal]] | Path Traversal |
| [[apuntes Andres/20.07.2026 PortSwigger SSRF]] | SSRF |
| [[apuntes Andres/20.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]] | IA profunda |
| [[apuntes Andres/21.07.2026 PortSwigger Cierre SSRF + Introduccion SSTI]] | SSRF avanzado, SSTI |
| [[apuntes Andres/24.07.2026 Repaso Semanal III]] | Repaso semanal |

---

## 📝 Apuntes — Joselu

> [!note] Clases del máster impartidas por Joselu (Evolve Academy)
> Organizadas por módulo. 72 resúmenes de clase.

### Prework

- [[apuntes joselu/PREWORK/PREWORK]]
- [[apuntes joselu/PREWORK/resumen_clase1_]]
- [[apuntes joselu/PREWORK/resumen_clase2]]
- [[apuntes joselu/PREWORK/resumen_clase3]]
- [[apuntes joselu/PREWORK/resumen_clase4]]
- [[apuntes joselu/PREWORK/resumen_clase5]]
- [[apuntes joselu/PREWORK/resumen_clase6]]
- [[apuntes joselu/PREWORK/resumen_clase7]]
- [[apuntes joselu/PREWORK/resumen_clase8]]
- [[apuntes joselu/PREWORK/resumen_clase9]]
- [[apuntes joselu/PREWORK/resumen_clase10]]
- [[apuntes joselu/PREWORK/resumen_clase11]]
- [[apuntes joselu/PREWORK/resumen_clase12]]
- [[apuntes joselu/PREWORK/resumen_clase13]]
- [[apuntes joselu/PREWORK/resumen_clase14]]
- [[apuntes joselu/PREWORK/resumen_clase15]]
- [[apuntes joselu/PREWORK/resumen_clase16]]
- [[apuntes joselu/PREWORK/resumen_clase17]]
- [[apuntes joselu/PREWORK/resumen_clase18]]

### Módulo 1

- [[apuntes joselu/MODULO1/resumen_master_clase1]]
- [[apuntes joselu/MODULO1/resumen_master_clase2]]
- [[apuntes joselu/MODULO1/resumen_master_clase3]]
- [[apuntes joselu/MODULO1/resumen_master_clase4]]
- [[apuntes joselu/MODULO1/resumen_master_clase5]]
- [[apuntes joselu/MODULO1/resumen_master_clase6]]
- [[apuntes joselu/MODULO1/resumen_master_clase7]]

### Módulo 2

- [[apuntes joselu/MODULO2/resumen_master_clase8]]
- [[apuntes joselu/MODULO2/resumen_master_clase9]]
- [[apuntes joselu/MODULO2/resumen_master_clase10]]
- [[apuntes joselu/MODULO2/resumen_master_clase11]]
- [[apuntes joselu/MODULO2/resumen_master_clase12]]
- [[apuntes joselu/MODULO2/resumen_master_clase13]]
- [[apuntes joselu/MODULO2/resumen_master_clase14]]
- [[apuntes joselu/MODULO2/resumen_master_clase15]]
- [[apuntes joselu/MODULO2/resumen_master_clase16]]

### Módulo 3

- [[apuntes joselu/MODULO3/resumen_master_clase17]]
- [[apuntes joselu/MODULO3/resumen_master_clase18]]
- [[apuntes joselu/MODULO3/resumen_master_clase19]]
- [[apuntes joselu/MODULO3/resumen_master_clase20]]
- [[apuntes joselu/MODULO3/resumen_master_clase21]]
- [[apuntes joselu/MODULO3/resumen_master_clase22]]
- [[apuntes joselu/MODULO3/resumen_master_clase23]]
- [[apuntes joselu/MODULO3/resumen_master_clase24]]
- [[apuntes joselu/MODULO3/resumen_master_clase25]]
- [[apuntes joselu/MODULO3/resumen_master_clase26]]
- [[apuntes joselu/MODULO3/resumen_master_clase27]]
- [[apuntes joselu/MODULO3/resumen_master_clase29]]
- [[apuntes joselu/MODULO3/resumen_master_clase30]]
- [[apuntes joselu/MODULO3/resumen_master_clase32]]
- [[apuntes joselu/MODULO3/resumen_master_clase33]]
- [[apuntes joselu/MODULO3/resumen_master_clase34]]
- [[apuntes joselu/MODULO3/resumen_master_clase35]]
- [[apuntes joselu/MODULO3/resumen_master_clase36]]
- [[apuntes joselu/MODULO3/resumen_master_clase37]]
- [[apuntes joselu/MODULO3/resumen_master_clase38]]
- [[apuntes joselu/MODULO3/resumen_master_clase39]]
- [[apuntes joselu/MODULO3/resumen_master_clase40]]
- [[apuntes joselu/MODULO3/resumen_master_clase41]]
- [[apuntes joselu/MODULO3/resumen_master_clase42]]
- [[apuntes joselu/MODULO3/resumen_master_clase43]]
- [[apuntes joselu/MODULO3/resumen_master_clase44]]
- [[apuntes joselu/MODULO3/resumen_master_clase45]]
- [[apuntes joselu/MODULO3/resumen_master_clase46]]
- [[apuntes joselu/MODULO3/resumen_master_clase47]]
- [[apuntes joselu/MODULO3/resumen_master_clase48]]
- [[apuntes joselu/MODULO3/resumen_master_clase49]]
- [[apuntes joselu/MODULO3/resumen_master_clase50]]
- [[apuntes joselu/MODULO3/resumen_master_clase51]]
- [[apuntes joselu/MODULO3/resumen_master_clase52]]
- [[apuntes joselu/MODULO3/resumen_master_clase53]]
- [[apuntes joselu/MODULO3/resumen_master_clase54]]
- [[apuntes joselu/MODULO3/resumen_master_clase55]]

---

## 🎙️ Transcripciones de Sesiones

> [!note] Transcripciones completas de cada sesión
> Organizadas por mes para localizar cualquier clase rápida y fácilmente.

### Junio

- [[transcripciones/Junio/19.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]]
- [[transcripciones/Junio/22.06.2026 Metodologías de Enumeración Web]]
- [[transcripciones/Junio/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]]
- [[transcripciones/Junio/30.06.2026 Explotación web Port Swinger]]

### Julio

- [[transcripciones/Julio/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]]
- [[transcripciones/Julio/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]]
- [[transcripciones/Julio/06.07.2026 Fuzzing de Parámetros I Ingeniería Social y Anonimato]]
- [[transcripciones/Julio/07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote]]
- [[transcripciones/Julio/08.07.2026 Owasp Top 10 LFI Fundamentos]]
- [[transcripciones/Julio/09.07.2026 Owasp Top 10 XXE  Labs with Castor]]
- [[transcripciones/Julio/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]]
- [[transcripciones/Julio/11.07.2026 Owasp Top 10 XXE  Labs II]]
- [[transcripciones/Julio/14.07.2026 Fundamentos Web y SQL Injection Máquina Injected (HackerLab)]]
- [[transcripciones/Julio/15.07.2026 IA Introducción y Vibe Coding]]
- [[transcripciones/Julio/17.07.2026 PortSwigger Introduccion y repaso Path Traversal]]
- [[transcripciones/Julio/20.07.2026 PortSwigger SSRF (Server-Side Request Forgery)]]
- [[transcripciones/Julio/21.07.2026 PortSwigger SSTI + cierre SSRF]]
- [[transcripciones/Julio/22.06.2026 Metodologías de Enumeración Web]]
- [[transcripciones/Julio/22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento]]
- [[transcripciones/Julio/23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]]
- [[transcripciones/Julio/24.07.2026 Repaso Semanal III]]
- [[transcripciones/Julio/27.07.2026 PortSwigger SSTI]]

---

## 📄 Write-ups — The Hackers Labs

> [!note] Resolución de máquinas de The Hackers Labs
> Cada write-up documenta el proceso completo de explotación.

| Máquina | Apunte |
|---------|--------|
| Academy | [[write-ups/Academy-THL]] |
| Banco | [[write-ups/Banco-THL]] |
| Castor | [[write-ups/Castor-THL]] |
| Inj3ctCrew | [[write-ups/Inj3ctCrew-THL]] |
| Nike | [[write-ups/Nike-THL]] |
| Rockstars | [[write-ups/Rockstars-THL]] |

---

## 📋 Informes Técnicos

> [!note] Informes formales de cada máquina resuelta
> Documentación profesional para portafolio.

| Informe | Máquina |
|---------|---------|
| [[informes/Informe_Academy]] | Academy |
| [[informes/Informe_Banco]] | Banco |
| [[informes/Informe_Castor]] | Castor |
| [[informes/Informe_Inj3ctCrew]] | Inj3ctCrew |
| [[informes/Informe_Nike]] | Nike |
| [[informes/Informe_Rockstars]] | Rockstars |

---

## 🔗 Enlaces Rápidos por Concepto

### Herramientas (teoría)
[[Nmap - Escaneo y Enumeración]] · [[Wireshark - Análisis de Tráfico]] · [[Burp Suite - Framework de Auditoría]] · [[Fuzzing Web con ffuf]] · [[WordPress - Auditoría con WPScan]]

### Herramientas (comandos)
[[comandos/Nmap|Nmap]] · [[comandos/Metasploit|Metasploit]] · [[comandos/BurpSuite|Burp Suite]] · [[comandos/Hydra|Hydra]] · [[comandos/FFUF|FFUF]] · [[comandos/Feroxbuster|Feroxbuster]] · [[comandos/GoBuster|GoBuster]] · [[comandos/SSH|SSH]] · [[comandos/SQLMap|SQLMap]] · [[comandos/WPScan|WPScan]] · [[comandos/John_Hashcat|John / Hashcat]] · [[comandos/SMB_Impacket|SMB / Impacket]] · [[comandos/Google_Dorks|Google Dorks]] · [[comandos/DirSearch|DirSearch]] · [[comandos/Telnet|Telnet]] · [[comandos/Tmux|Tmux]] · [[comandos/Linux|Linux]] · [[comandos/Windows|Windows]]

### Técnicas ofensivas
[[Metodología de Explotación]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]] · [[Pivoting y Movilidad Lateral]] · [[Auditoría WiFi y Car Hacking]] · [[SSRF — Server-Side Request Forgery]] · [[SSTI — Server-Side Template Injection]] · [[XXE — XML External Entity]] · [[Path Traversal — 6 Casos y Bypasses]]

### Defensa y operaciones
[[Blue Team - SOC e Incidentes]] · [[Análisis Forense y Memoria]] · [[IA en Ciberseguridad]]

### Frameworks de referencia
[[OWASP Top 10 - CVE CVSS CWE]] · [[Normativa - ISO 27001, GDPR, ENS]]

### Práctica y certificaciones
[[Prácticas CTF - HTB y VulnHub]] · [[Certificaciones - ISO 27001 y eJPTv2]] · [[Mercado Laboral y Certificaciones]]

---

> [!tip] Cómo usar estos apuntes
> - **Por tema**: navega la tabla de arriba
> - **Por concepto**: usa los enlaces rápidos
> - **Por máquina CTF**: ve a [[Prácticas CTF - HTB y VulnHub]]
> - **Para comandos**: ve a la sección 16 o seguí los enlaces de cada apunte
> - **Para repasar**: cada apunte tiene un `## Checklist de repaso` al final
