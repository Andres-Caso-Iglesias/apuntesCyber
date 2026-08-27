> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 17**
> **Módulo:** PREWORK
> **Tema:** Clase 17
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 17. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen “ Clase 17: Principales Herramientas de Ciberseguridad Ofensiva en Kali Linux Máster de Ciberseguridad e Inteligencia Artificial “ Evolve Academy 1.

Introducción: Kali Linux como sistema operativo del pentester Kali Linux es la distribución Linux de referencia para la ciberseguridad ofensiva.

Integra más de 600 herramientas organizadas en 13 categorías que cubren todas las fases de una auditoría técnica.

Las herramientas pueden lanzarse desde el entorno gráfico ( Applications) o directamente desde la terminal escribiendo el nombre del comando.

Diferencia junior vs. senior: el perfil junior usa las herramientas sin entender exactamente qué hacen internamente ni qué ruido generan en la red.

El perfil senior sabe qué tráfico genera cada herramienta, qué está ocurriendo por debajo y cuándo es apropiado o no utilizarla.

Leer la documentación oficial de cada herramienta antes de usarla es imprescindible.

Advertencia crítica (caso real): en una auditoría a un servicio sanitario, el profesor lanzó SpiderFoot sin marcar la casilla de €œsolo modo pasivo€.

La herramienta lanzó también escaneos activos y tumbó varios servidores del cliente.

Moraleja: conocer exactamente qué hace cada herramienta y en qué modo se ejecuta antes de lanzarla en un entorno de producción. 2.

Categoría 1: Information Gathering (Recopilación de información) Herramientas para la fase de enumeración (pasiva y activa).

Nmap La herramienta más importante del pentesting.

El profesor la compara con el €œcarnet de conducir€ del hacker: se usa para absolutamente todo.

Permite escanear puertos, identificar servicios y versiones, detectar sistemas operativos y enumerar la superficie de ataque.

Se verá y practicará de forma intensiva a lo largo de todo el máster.

SpiderFoot Framework de OSINT con interfaz gráfica y terminal.

Recopila automáticamente información de fuentes abiertas (dominios, IPs, correos, redes sociales, etc.) sobre un objetivo.

Muy potente pero genera muchos resultados, incluidos falsos positivos, que requieren filtrado manual.

> [!important] Importante: tiene un modo mixto (activo+pasivo) y un modo solo pasivo — siempre verificar 1

cuál está activo antes de lanzarlo en clientes sensibles.

Recon-ng Framework modular de reconocimiento, similar a Metasploit pero orientado exclusivamente a la recopilación de información.

Agrupa multitud de módulos para enumeración de dominios, personas, empresas y fuentes abiertas.

Maltego Herramienta visual de OSINT que presenta la información recopilada en forma de grafos de relaciones.

Permite buscar y correlacionar información corporativa y de perfiles personales de forma muy intuitiva.

Herramienta de referencia en el sector. theHarvester Herramienta para enumeración de subdominios, correos electrónicos y nombres de usuario a partir de múltiples fuentes (Google, Bing, LinkedIn, etc.).

Muy utilizada en la fase de reconocimiento externo. enum4linux Herramienta de enumeración específica para sistemas Linux y recursos SMB/Samba en redes internas.

Extrae información sobre usuarios, grupos, recursos compartidos y políticas de contraseñas.

Muy útil en auditorías internas.

SMBMap / SMBClient Herramientas para enumerar y acceder a recursos compartidos a través del protocolo SMB en entornos Windows y Samba.

Esenciales en auditorías de Active Directory.

Nikto Escáner web que realiza un primer análisis rápido de un servidor web buscando configuraciones inseguras, versiones vulnerables, directorios CGI, cookies mal configuradas y otras evidencias.

Ideal como primer acercamiento antes de usar herramientas más profundas. wafw00f Herramienta de fingerprinting de WAF (Web Application Firewall ).

Identifica qué tipo de firewall de aplicaciones web protege el objetivo, lo que permite adaptar las técnicas de ataque para intentar evadirlo.

Ejemplo de la sesión: wafw00f https://omnia.dev →’ detectó que el sitio está protegido por Cloudflare. 2

Herramientas DNS DNSEnum, DNSMap, DNSRecon: enumeración y análisis de registros DNS para descubrir subdominios, IPs asociadas y configuraciones DNS débiles.

NSLookup / curl + nslookup Para resolver dominios a IPs.

Ejemplo de la sesión: nslookup omnia.dev →’ obtención de la IP del servidor para lanzar enum4linux sobre ella. 3.

Categoría 2: Vulnerability Analysis (Análisis de vulnerabilidades) WPScan Escáner específico para sitios WordPress.

Identifica versiones vulnerables del core, plugins y temas.

Dispone de un modo con API key gratuita que amplía el número de escaneos diarios.

Regla: siempre que se encuentre un WordPress en una auditoría, lanzar WPScan.

Nikto También incluida en esta categoría por su capacidad de identificar vulnerabilidades conocidas en servidores web. 4.

Categoría 3: Web Applications (Aplicaciones web) Burp Suite La herramienta más importante para auditorías de aplicaciones web; el profesor la llama la €œnavaja suiza de la web€.

Actúa como proxy interceptador entre el navegador y el servidor, permitiendo ver y modificar todas las peticiones HTTP/HTTPS en tiempo real.

Se analizará en profundidad en el módulo de auditorías web.

Gobuster / DirBuster / Dirsearch Herramientas de fuzzing de rutas y directorios .

Prueban combinaciones de palabras (con diccionarios propios o personalizados) contra el dominio objetivo para descubrir rutas, paneles de administración, archivos de configuración y recursos ocultos.

Interpretan los códigos de estado HTTP: 200 (recurso encontrado), 301/302 (redirección), 404 (no encontrado).

Ejemplo: descubrimiento de /login en omnia.dev durante la demostración. 3

SQLMap Herramienta de inyección SQL automatizada.

Detecta y explota vulnerabilidades de SQL Injection en bases de datos.

Muy utilizada en auditorías web.

SQLite Browser Visor de bases de datos SQLite.

Necesario cuando se extrae una base de datos .db de una aplicación para examinar su contenido. robots.txt No es una herramienta sino un archivo estándar de cualquier servidor web que indica a los motores de búsqueda qué rutas no deben indexar.

Para un auditor es muy valioso porque revela rutas ocultas que el administrador no quiere que se encuentren — paradójicamente, es uno de los mejores puntos de partida del fuzzing. 5.

Categoría 4: Password Attacks (Ataques a contraseñas) Hashcat Herramienta de cracking de hashes basada en GPU.

Extremadamente rápida para ataques de fuerza bruta, diccionario y reglas.

Herramienta principal para romper hashes obtenidos en auditorías.

John the Ripper Herramienta de cracking de hashes basada en CPU.

Más lenta que Hashcat pero más versátil en algunos formatos de hash específicos.

Hydra Herramienta de fuerza bruta para portales de login en múltiples protocolos: SSH, HTTP, FTP, RDP, SMB, etc.

Permite probar diccionarios de credenciales contra formularios de autenticación.

CeWL Generador de wordlists personalizadas a partir del contenido de una web objetivo.

Extrae palabras del sitio web para construir diccionarios adaptados al contexto del cliente (ej. términos específicos del sector, nombres de empleados, proyectos). 4

## 6.

Categoría 5: Post Exploitation (Post-explotación) CrackMapExec (CME) Suite de post-explotación orientada a entornos Windows/Active Directory.

Permite autenticarse en múltiples máquinas del dominio, ejecutar comandos remotos, volcar credenciales y realizar movimientos laterales de forma automatizada.

Evil-WinRM Permite obtener una shell interactiva en máquinas Windows a través del protocolo WinRM (Windows Remote Management ).

Muy utilizada una vez se tienen credenciales de administrador.

Impacket Colección de scripts Python para interactuar con protocolos de red Windows (SMB, LDAP, Kerberos, etc.).

Incluye herramientas como psexec.py, secretsdump.py y otras esenciales en auditorías de Active Directory.

Mimikatz Herramienta para volcar credenciales, hashes NTLM y tickets Kerberos de la memoria RAM de Windows.

La herramienta más importante del hacking ofensivo en entornos Windows.

NetExec Herramienta similar a CrackMapExec para la enumeración y explotación de protocolos de red en entornos corporativos.

ProxyChains Herramienta de post-explotación para encadenar proxies y redirigir el tráfico a través de múltiples saltos, ocultando la IP real del atacante.

También se usa para enrutar el tráfico de las herramientas a través de los túneles de pivoting creados con Ligolo-ng. 7.

Categoría 6: Wireless Attacks (Ataques Wi-Fi) Aircrack-ng Suite completa para auditorías de redes Wi-Fi: captura de handshakes WPA/WPA2, ataques de diccionario, análisis de redes y creación de puntos de acceso falsos. 5

WiFite Herramienta automatizada para auditorías Wi-Fi.

Detecta redes en el entorno y lanza ataques de forma automática para intentar obtener las credenciales.

Requiere antena Wi-Fi en modo monitor.

BetterCap Framework multipropósito para ataques de red.

Muy utilizado para ataques Man-in-the-Middle en redes inalámbricas y redes internas.

Permite capturar tráfico, modificar paquetes y realizar ataques de ARP poisoning. 8.

Categoría 7: Sniffing & Spoofing Wireshark Analizador de tráfico de red por excelencia.

Permite capturar y examinar en tiempo real todos los paquetes que circulan por la red, analizar protocolos, identificar credenciales en claro y comparar tráfico cifrado vs. no cifrado.

Responder Herramienta de envenenamiento de tráfico SMB/LLMNR/NBT-NS.

Captura hashes NTLMv2 cuando los equipos de la red intentan resolver nombres de host mediante protocolos débiles.

Esencial en auditorías de redes internas.

MacChanger Permite modificar la dirección MAC del adaptador de red del atacante para evitar ser identificado o filtrado por controles de acceso basados en MAC. 9.

Categoría 8: Exploitation Tools (Herramientas de explotación) Metasploit Framework El framework de explotación más completo del mundo.

Integra miles de exploits, payloads y módulos auxiliares.

En el contexto del máster y la certificación eJPT v2 se usará como Command & Control para gestionar las sesiones de acceso remoto obtenidas. 6

SearchSploit Herramienta de búsqueda local en la base de datos Exploit-DB.

Permite buscar, descargar y personalizar exploits para vulnerabilidades específicas sin necesidad de acceso a internet.

SET (Social Engineering Toolkit) Framework para ataques de ingeniería social: phishing, clonación de páginas web, generación de payloads maliciosos, etc.

El profesor prefiere realizar la ingeniería social de forma manual, pero es una herramienta de referencia. 10.

Categoría 9: Forensics (Forense digital) Autopsy La herramienta de análisis forense más completa integrada en Kali.

Permite analizar imágenes de disco, recuperar archivos eliminados, examinar el historial de navegación, correos y evidencias digitales.

Binwalk Herramienta de análisis de firmware.

Esencial en auditorías IoT para extraer y analizar el contenido de imágenes de firmware. 11.

Categoría 10: Reporting Tools CherryTree Gestor de notas jerárquico utilizado durante las auditorías para organizar y almacenar evidencias, comandos ejecutados y hallazgos.

Herramienta de referencia para la documentación del trabajo. 12.

Herramientas externas (GitHub, no incluidas en Kali) Además de las herramientas integradas en Kali, existen numerosas herramientas de terceros en GitHub que se descargan e instalan manualmente.

Son imprescindibles para casos de uso específicos y se irán presentando a lo largo del máster según se necesiten. 7

## 13.

Resumen por fase de auditoría Fase Herramientas principales Enumeración pasiva SpiderFoot, Maltego, theHarvester, Recon-ng, wafw00f Enumeración activa Nmap, enum4linux, SMBMap, DNSRecon, Nikto, WPScan Fuzzing web Gobuster, DirBuster, Dirsearch Análisis web Burp Suite, SQLMap, Nikto Cracking de hashes Hashcat (GPU), John the Ripper (CPU) Fuerza bruta / login Hydra, CeWL (generación de wordlists) Post-explotación / AD Mimikatz, CrackMapExec, Impacket, Evil- WinRM Pivoting / proxies ProxyChains, Ligolo-ng Wi-Fi Aircrack-ng, WiFite, BetterCap Sniffing / spoofing Wireshark, Responder, MacChanger Explotación Metasploit, SearchSploit Forense Autopsy, Binwalk Documentación CherryTree 14.

→’

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración Neva / En el map Nmap “ herramienta de escaneo de puertos y servicios SpiderFood / Sparehood SpiderFoot “ framework de OSINT y recopilación de fuentes abiertas Recone NG Recon-ng “ framework modular de reconocimiento y OSINT en un forlinus / en un forlinux enum4linux “ herramienta de enumeración SMB/Samba en Linux de Harvester / de hecho de Harvester theHarvester “ herramienta de enumeración de subdominios y correos UWP Scan / UWFood WPScan / WFuzz “ escáner de WordPress / herramienta de fuzzing web CFFood / Glores Gobuster / DirBuster “ herramientas de fuzzing de directorios y rutas DeepBuster / DeepSearch DirBuster / Dirsearch “ herramientas de descubrimiento de rutas web Bursuit / Bursui Burp Suite “ proxy de interceptación para auditorías web CrabMapSEQ CrackMapExec (CME) “ suite de post- explotación para entornos Windows/AD EviWinMR Evil-WinRM “ shell remota vía WinRM 8

Término en la transcripción Corrección / Aclaración InPacket Impacket “ colección de scripts para protocolos Windows NetSEQ NetExec “ herramienta de explotación de protocolos de red corporativos Max Sanger MacChanger “ herramienta para cambiar la dirección MAC iCrack Aircrack-ng “ suite de auditoría de redes Wi- Fi Wi-Fi-T WiFite “ herramienta automatizada de ataques Wi-Fi mining the middles Man-in-the-Middle (MitM) “ ataque de interceptación de comunicaciones ProxyChange ProxyChains “ herramienta de encadenamiento de proxies BingWall Binwalk “ herramienta de análisis de firmware Set Toolkit SET (Social Engineering Toolkit) “ framework de ingeniería social SearchSploit SearchSploit “ buscador local de exploits en Exploit-DB Hydra / Aydra Hydra “ herramienta de fuerza bruta en protocolos de autenticación Cvless CeWL “ generador de wordlists a partir del contenido web WAF00F / WAF wafw00f “ herramienta de fingerprinting de WAF curr en ese lookup curl + nslookup “ herramientas de resolución DNS e inspección HTTP LJPT eJPT v2 (eLearnSecurity Junior Penetration Tester) “ certificación objetivo del máster DSMB SMBMap “ herramienta de enumeración de recursos SMB compartidos Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial “ Wolf Academy. 9

→’

→’

→’

→’
→’
→’

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[PREWORK.md|PREWORK]— GoBuster, SSH, WiFi / Hardware
- [[../../transcripciones/Junio/30.06.2026 Explotación web Port Swinger.md|30.06.2026 Explotación web Port Swinger]— GoBuster, SSH, WiFi / Hardware
- [[../../Apuntes/00 - Mapa de Contenidos/MOC - Ciberseguridad.md|MOC - Ciberseguridad]— GoBuster, SSH, WiFi / Hardware
- [[../../apuntes Chema/Mercado Laboral y Servicios.md|Mercado Laboral y Servicios]— Metasploit, SSH, WiFi / Hardware
- [[../MODULO3/resumen_master_clase24.md|resumen_master_clase24]— Hydra, Metasploit, SSH
- [[../../transcripciones/Junio/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]— Kali Linux, Post-Explotación, WiFi / Hardware

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #burpsuite #certificaciones #dirsearch #empleabilidad #esteganografia #forense #gobuster #hydra #ia #john #kali #linux #metasploit #nmap #osint #pivoting #post-explotacion #redes #smb-impacket #sqli #sqlmap #ssh #wifi #windows #wireshark #wordpress #wpscan
