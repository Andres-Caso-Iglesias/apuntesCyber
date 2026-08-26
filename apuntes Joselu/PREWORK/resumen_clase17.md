> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 17**
> **MÃ³dulo:** PREWORK
> **Tema:** Clase 17
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 17. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
Resumen â€“ Clase 17: Principales Herramientas de Ciberseguridad Ofensiva en Kali Linux MÃ¡ster de Ciberseguridad e Inteligencia Artificial â€“ Evolve Academy 1.

IntroducciÃ³n: Kali Linux como sistema operativo del pentester Kali Linux es la distribuciÃ³n Linux de referencia para la ciberseguridad ofensiva.

Integra mÃ¡s de 600 herramientas organizadas en 13 categorÃ­as que cubren todas las fases de una auditorÃ­a tÃ©cnica.

Las herramientas pueden lanzarse desde el entorno grÃ¡fico ( Applications) o directamente desde la terminal escribiendo el nombre del comando.

Diferencia junior vs. senior: el perfil junior usa las herramientas sin entender exactamente quÃ© hacen internamente ni quÃ© ruido generan en la red.

El perfil senior sabe quÃ© trÃ¡fico genera cada herramienta, quÃ© estÃ¡ ocurriendo por debajo y cuÃ¡ndo es apropiado o no utilizarla.

Leer la documentaciÃ³n oficial de cada herramienta antes de usarla es imprescindible.

Advertencia crÃ­tica (caso real): en una auditorÃ­a a un servicio sanitario, el profesor lanzÃ³ SpiderFoot sin marcar la casilla de â€œsolo modo pasivoâ€.

La herramienta lanzÃ³ tambiÃ©n escaneos activos y tumbÃ³ varios servidores del cliente.

Moraleja: conocer exactamente quÃ© hace cada herramienta y en quÃ© modo se ejecuta antes de lanzarla en un entorno de producciÃ³n. 2.

CategorÃ­a 1: Information Gathering (RecopilaciÃ³n de informaciÃ³n) Herramientas para la fase de enumeraciÃ³n (pasiva y activa).

Nmap La herramienta mÃ¡s importante del pentesting.

El profesor la compara con el â€œcarnet de conducirâ€ del hacker: se usa para absolutamente todo.

Permite escanear puertos, identificar servicios y versiones, detectar sistemas operativos y enumerar la superficie de ataque.

Se verÃ¡ y practicarÃ¡ de forma intensiva a lo largo de todo el mÃ¡ster.

SpiderFoot Framework de OSINT con interfaz grÃ¡fica y terminal.

Recopila automÃ¡ticamente informaciÃ³n de fuentes abiertas (dominios, IPs, correos, redes sociales, etc.) sobre un objetivo.

Muy potente pero genera muchos resultados, incluidos falsos positivos, que requieren filtrado manual.

> [!important] Importante: tiene un modo mixto (activo+pasivo) y un modo solo pasivo â€” siempre verificar 1

cuÃ¡l estÃ¡ activo antes de lanzarlo en clientes sensibles.

Recon-ng Framework modular de reconocimiento, similar a Metasploit pero orientado exclusivamente a la recopilaciÃ³n de informaciÃ³n.

Agrupa multitud de mÃ³dulos para enumeraciÃ³n de dominios, personas, empresas y fuentes abiertas.

Maltego Herramienta visual de OSINT que presenta la informaciÃ³n recopilada en forma de grafos de relaciones.

Permite buscar y correlacionar informaciÃ³n corporativa y de perfiles personales de forma muy intuitiva.

Herramienta de referencia en el sector. theHarvester Herramienta para enumeraciÃ³n de subdominios, correos electrÃ³nicos y nombres de usuario a partir de mÃºltiples fuentes (Google, Bing, LinkedIn, etc.).

Muy utilizada en la fase de reconocimiento externo. enum4linux Herramienta de enumeraciÃ³n especÃ­fica para sistemas Linux y recursos SMB/Samba en redes internas.

Extrae informaciÃ³n sobre usuarios, grupos, recursos compartidos y polÃ­ticas de contraseÃ±as.

Muy Ãºtil en auditorÃ­as internas.

SMBMap / SMBClient Herramientas para enumerar y acceder a recursos compartidos a travÃ©s del protocolo SMB en entornos Windows y Samba.

Esenciales en auditorÃ­as de Active Directory.

Nikto EscÃ¡ner web que realiza un primer anÃ¡lisis rÃ¡pido de un servidor web buscando configuraciones inseguras, versiones vulnerables, directorios CGI, cookies mal configuradas y otras evidencias.

Ideal como primer acercamiento antes de usar herramientas mÃ¡s profundas. wafw00f Herramienta de fingerprinting de WAF (Web Application Firewall ).

Identifica quÃ© tipo de firewall de aplicaciones web protege el objetivo, lo que permite adaptar las tÃ©cnicas de ataque para intentar evadirlo.

Ejemplo de la sesiÃ³n: wafw00f https://omnia.dev â†’ detectÃ³ que el sitio estÃ¡ protegido por Cloudflare. 2

Herramientas DNS DNSEnum, DNSMap, DNSRecon: enumeraciÃ³n y anÃ¡lisis de registros DNS para descubrir subdominios, IPs asociadas y configuraciones DNS dÃ©biles.

NSLookup / curl + nslookup Para resolver dominios a IPs.

Ejemplo de la sesiÃ³n: nslookup omnia.dev â†’ obtenciÃ³n de la IP del servidor para lanzar enum4linux sobre ella. 3.

CategorÃ­a 2: Vulnerability Analysis (AnÃ¡lisis de vulnerabilidades) WPScan EscÃ¡ner especÃ­fico para sitios WordPress.

Identifica versiones vulnerables del core, plugins y temas.

Dispone de un modo con API key gratuita que amplÃ­a el nÃºmero de escaneos diarios.

Regla: siempre que se encuentre un WordPress en una auditorÃ­a, lanzar WPScan.

Nikto TambiÃ©n incluida en esta categorÃ­a por su capacidad de identificar vulnerabilidades conocidas en servidores web. 4.

CategorÃ­a 3: Web Applications (Aplicaciones web) Burp Suite La herramienta mÃ¡s importante para auditorÃ­as de aplicaciones web; el profesor la llama la â€œnavaja suiza de la webâ€.

ActÃºa como proxy interceptador entre el navegador y el servidor, permitiendo ver y modificar todas las peticiones HTTP/HTTPS en tiempo real.

Se analizarÃ¡ en profundidad en el mÃ³dulo de auditorÃ­as web.

Gobuster / DirBuster / Dirsearch Herramientas de fuzzing de rutas y directorios .

Prueban combinaciones de palabras (con diccionarios propios o personalizados) contra el dominio objetivo para descubrir rutas, paneles de administraciÃ³n, archivos de configuraciÃ³n y recursos ocultos.

Interpretan los cÃ³digos de estado HTTP: 200 (recurso encontrado), 301/302 (redirecciÃ³n), 404 (no encontrado).

Ejemplo: descubrimiento de /login en omnia.dev durante la demostraciÃ³n. 3

SQLMap Herramienta de inyecciÃ³n SQL automatizada.

Detecta y explota vulnerabilidades de SQL Injection en bases de datos.

Muy utilizada en auditorÃ­as web.

SQLite Browser Visor de bases de datos SQLite.

Necesario cuando se extrae una base de datos .db de una aplicaciÃ³n para examinar su contenido. robots.txt No es una herramienta sino un archivo estÃ¡ndar de cualquier servidor web que indica a los motores de bÃºsqueda quÃ© rutas no deben indexar.

Para un auditor es muy valioso porque revela rutas ocultas que el administrador no quiere que se encuentren â€” paradÃ³jicamente, es uno de los mejores puntos de partida del fuzzing. 5.

CategorÃ­a 4: Password Attacks (Ataques a contraseÃ±as) Hashcat Herramienta de cracking de hashes basada en GPU.

Extremadamente rÃ¡pida para ataques de fuerza bruta, diccionario y reglas.

Herramienta principal para romper hashes obtenidos en auditorÃ­as.

John the Ripper Herramienta de cracking de hashes basada en CPU.

MÃ¡s lenta que Hashcat pero mÃ¡s versÃ¡til en algunos formatos de hash especÃ­ficos.

Hydra Herramienta de fuerza bruta para portales de login en mÃºltiples protocolos: SSH, HTTP, FTP, RDP, SMB, etc.

Permite probar diccionarios de credenciales contra formularios de autenticaciÃ³n.

CeWL Generador de wordlists personalizadas a partir del contenido de una web objetivo.

Extrae palabras del sitio web para construir diccionarios adaptados al contexto del cliente (ej. tÃ©rminos especÃ­ficos del sector, nombres de empleados, proyectos). 4

## 6.

CategorÃ­a 5: Post Exploitation (Post-explotaciÃ³n) CrackMapExec (CME) Suite de post-explotaciÃ³n orientada a entornos Windows/Active Directory.

Permite autenticarse en mÃºltiples mÃ¡quinas del dominio, ejecutar comandos remotos, volcar credenciales y realizar movimientos laterales de forma automatizada.

Evil-WinRM Permite obtener una shell interactiva en mÃ¡quinas Windows a travÃ©s del protocolo WinRM (Windows Remote Management ).

Muy utilizada una vez se tienen credenciales de administrador.

Impacket ColecciÃ³n de scripts Python para interactuar con protocolos de red Windows (SMB, LDAP, Kerberos, etc.).

Incluye herramientas como psexec.py, secretsdump.py y otras esenciales en auditorÃ­as de Active Directory.

Mimikatz Herramienta para volcar credenciales, hashes NTLM y tickets Kerberos de la memoria RAM de Windows.

La herramienta mÃ¡s importante del hacking ofensivo en entornos Windows.

NetExec Herramienta similar a CrackMapExec para la enumeraciÃ³n y explotaciÃ³n de protocolos de red en entornos corporativos.

ProxyChains Herramienta de post-explotaciÃ³n para encadenar proxies y redirigir el trÃ¡fico a travÃ©s de mÃºltiples saltos, ocultando la IP real del atacante.

TambiÃ©n se usa para enrutar el trÃ¡fico de las herramientas a travÃ©s de los tÃºneles de pivoting creados con Ligolo-ng. 7.

CategorÃ­a 6: Wireless Attacks (Ataques Wi-Fi) Aircrack-ng Suite completa para auditorÃ­as de redes Wi-Fi: captura de handshakes WPA/WPA2, ataques de diccionario, anÃ¡lisis de redes y creaciÃ³n de puntos de acceso falsos. 5

WiFite Herramienta automatizada para auditorÃ­as Wi-Fi.

Detecta redes en el entorno y lanza ataques de forma automÃ¡tica para intentar obtener las credenciales.

Requiere antena Wi-Fi en modo monitor.

BetterCap Framework multipropÃ³sito para ataques de red.

Muy utilizado para ataques Man-in-the-Middle en redes inalÃ¡mbricas y redes internas.

Permite capturar trÃ¡fico, modificar paquetes y realizar ataques de ARP poisoning. 8.

CategorÃ­a 7: Sniffing & Spoofing Wireshark Analizador de trÃ¡fico de red por excelencia.

Permite capturar y examinar en tiempo real todos los paquetes que circulan por la red, analizar protocolos, identificar credenciales en claro y comparar trÃ¡fico cifrado vs. no cifrado.

Responder Herramienta de envenenamiento de trÃ¡fico SMB/LLMNR/NBT-NS.

Captura hashes NTLMv2 cuando los equipos de la red intentan resolver nombres de host mediante protocolos dÃ©biles.

Esencial en auditorÃ­as de redes internas.

MacChanger Permite modificar la direcciÃ³n MAC del adaptador de red del atacante para evitar ser identificado o filtrado por controles de acceso basados en MAC. 9.

CategorÃ­a 8: Exploitation Tools (Herramientas de explotaciÃ³n) Metasploit Framework El framework de explotaciÃ³n mÃ¡s completo del mundo.

Integra miles de exploits, payloads y mÃ³dulos auxiliares.

En el contexto del mÃ¡ster y la certificaciÃ³n eJPT v2 se usarÃ¡ como Command & Control para gestionar las sesiones de acceso remoto obtenidas. 6

SearchSploit Herramienta de bÃºsqueda local en la base de datos Exploit-DB.

Permite buscar, descargar y personalizar exploits para vulnerabilidades especÃ­ficas sin necesidad de acceso a internet.

SET (Social Engineering Toolkit) Framework para ataques de ingenierÃ­a social: phishing, clonaciÃ³n de pÃ¡ginas web, generaciÃ³n de payloads maliciosos, etc.

El profesor prefiere realizar la ingenierÃ­a social de forma manual, pero es una herramienta de referencia. 10.

CategorÃ­a 9: Forensics (Forense digital) Autopsy La herramienta de anÃ¡lisis forense mÃ¡s completa integrada en Kali.

Permite analizar imÃ¡genes de disco, recuperar archivos eliminados, examinar el historial de navegaciÃ³n, correos y evidencias digitales.

Binwalk Herramienta de anÃ¡lisis de firmware.

Esencial en auditorÃ­as IoT para extraer y analizar el contenido de imÃ¡genes de firmware. 11.

CategorÃ­a 10: Reporting Tools CherryTree Gestor de notas jerÃ¡rquico utilizado durante las auditorÃ­as para organizar y almacenar evidencias, comandos ejecutados y hallazgos.

Herramienta de referencia para la documentaciÃ³n del trabajo. 12.

Herramientas externas (GitHub, no incluidas en Kali) AdemÃ¡s de las herramientas integradas en Kali, existen numerosas herramientas de terceros en GitHub que se descargan e instalan manualmente.

Son imprescindibles para casos de uso especÃ­ficos y se irÃ¡n presentando a lo largo del mÃ¡ster segÃºn se necesiten. 7

## 13.

Resumen por fase de auditorÃ­a Fase Herramientas principales EnumeraciÃ³n pasiva SpiderFoot, Maltego, theHarvester, Recon-ng, wafw00f EnumeraciÃ³n activa Nmap, enum4linux, SMBMap, DNSRecon, Nikto, WPScan Fuzzing web Gobuster, DirBuster, Dirsearch AnÃ¡lisis web Burp Suite, SQLMap, Nikto Cracking de hashes Hashcat (GPU), John the Ripper (CPU) Fuerza bruta / login Hydra, CeWL (generaciÃ³n de wordlists) Post-explotaciÃ³n / AD Mimikatz, CrackMapExec, Impacket, Evil- WinRM Pivoting / proxies ProxyChains, Ligolo-ng Wi-Fi Aircrack-ng, WiFite, BetterCap Sniffing / spoofing Wireshark, Responder, MacChanger ExplotaciÃ³n Metasploit, SearchSploit Forense Autopsy, Binwalk DocumentaciÃ³n CherryTree 14.

â†’

Conceptos y tÃ©rminos clave corregidos TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n Neva / En el map Nmap â€“ herramienta de escaneo de puertos y servicios SpiderFood / Sparehood SpiderFoot â€“ framework de OSINT y recopilaciÃ³n de fuentes abiertas Recone NG Recon-ng â€“ framework modular de reconocimiento y OSINT en un forlinus / en un forlinux enum4linux â€“ herramienta de enumeraciÃ³n SMB/Samba en Linux de Harvester / de hecho de Harvester theHarvester â€“ herramienta de enumeraciÃ³n de subdominios y correos UWP Scan / UWFood WPScan / WFuzz â€“ escÃ¡ner de WordPress / herramienta de fuzzing web CFFood / Glores Gobuster / DirBuster â€“ herramientas de fuzzing de directorios y rutas DeepBuster / DeepSearch DirBuster / Dirsearch â€“ herramientas de descubrimiento de rutas web Bursuit / Bursui Burp Suite â€“ proxy de interceptaciÃ³n para auditorÃ­as web CrabMapSEQ CrackMapExec (CME) â€“ suite de post- explotaciÃ³n para entornos Windows/AD EviWinMR Evil-WinRM â€“ shell remota vÃ­a WinRM 8

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n InPacket Impacket â€“ colecciÃ³n de scripts para protocolos Windows NetSEQ NetExec â€“ herramienta de explotaciÃ³n de protocolos de red corporativos Max Sanger MacChanger â€“ herramienta para cambiar la direcciÃ³n MAC iCrack Aircrack-ng â€“ suite de auditorÃ­a de redes Wi- Fi Wi-Fi-T WiFite â€“ herramienta automatizada de ataques Wi-Fi mining the middles Man-in-the-Middle (MitM) â€“ ataque de interceptaciÃ³n de comunicaciones ProxyChange ProxyChains â€“ herramienta de encadenamiento de proxies BingWall Binwalk â€“ herramienta de anÃ¡lisis de firmware Set Toolkit SET (Social Engineering Toolkit) â€“ framework de ingenierÃ­a social SearchSploit SearchSploit â€“ buscador local de exploits en Exploit-DB Hydra / Aydra Hydra â€“ herramienta de fuerza bruta en protocolos de autenticaciÃ³n Cvless CeWL â€“ generador de wordlists a partir del contenido web WAF00F / WAF wafw00f â€“ herramienta de fingerprinting de WAF curr en ese lookup curl + nslookup â€“ herramientas de resoluciÃ³n DNS e inspecciÃ³n HTTP LJPT eJPT v2 (eLearnSecurity Junior Penetration Tester) â€“ certificaciÃ³n objetivo del mÃ¡ster DSMB SMBMap â€“ herramienta de enumeraciÃ³n de recursos SMB compartidos Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial â€“ Wolf Academy. 9

â†’

â†’

â†’

â†’
â†’
â†’
