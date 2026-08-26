# â‘¡ Conceptos clave

La **enumeraciÃ³n web** es el proceso de descubrir toda la superficie de una aplicaciÃ³n web: quÃ© tecnologÃ­as usa, quÃ© rutas existen, quÃ© ficheros estÃ¡n expuestos, quÃ© subdominios hay y quÃ© puntos de entrada (inputs) acepta. Es **reconocimiento dirigido**: no se explota nada todavÃ­a, se construye el mapa.

| |
|---|
|**â„¹Â  Idea central**<br><br>Cuanto mÃ¡s completo es el mapa, mÃ¡s superficie de ataque tienes. La mayorÃ­a de los hallazgos crÃ­ticos (paneles de admin, backups .bak/.old, ficheros de configuraciÃ³n, endpoints de API) aparecen en esta fase, no explotando un 0-day.|

## EnumeraciÃ³n pasiva vs activa

|**Tipo**|**QuÃ© hace**|**Toca el objetivo**|**Ejemplos**|
|---|---|---|---|
|**Pasiva**|Recopila info sin enviar trÃ¡fico directo al objetivo|No (o mÃ­nimo)|WHOIS, DNS pÃºblico, crt.sh, Google Dorks, Wayback Machine|
|**Activa**|InteractÃºa directamente con el servidor|SÃ­|Escaneo de directorios, fingerprinting, fuzzing de parÃ¡metros|
|**âœ—Â  Ruido y autorizaciÃ³n**<br><br>La enumeraciÃ³n activa genera trÃ¡fico y queda en logs. En auditorÃ­a real puede disparar WAFs/IDS. Empieza siempre por lo pasivo y confirma el alcance (scope) antes de lanzar herramientas activas.|

# â‘¢ MetodologÃ­a de enumeraciÃ³n web (flujo recomendado)

| |
|---|
|**1. Recon pasivo**|
|**â†“**|
|**2. Fingerprint stack**|
|**â†“**|
|**3. Subdominios**|
|**â†“**|
|**4. Directorios/ficheros**|
|**â†“**|
|**5. Endpoints/parÃ¡metros**|

El orden importa: cada fase alimenta a la siguiente. Identificar el CMS (fase 2) te dice quÃ© wordlists usar al buscar directorios (fase 4); los subdominios encontrados (fase 3) se convierten en nuevos objetivos que vuelves a fingerprintear.

## Fase 1 â€” Reconocimiento pasivo

Antes de tocar el servidor, recopila lo que ya es pÃºblico:

â€¢Â Â Â Â  **Certificados TLS** (crt.sh): revelan subdominios incluidos en el certificado.

â€¢Â Â Â Â  **Wayback Machine**: rutas y ficheros antiguos que quizÃ¡ sigan accesibles.

â€¢Â Â Â Â  **Google Dorks**: site:objetivo.com filetype:pdf, inurl:admin, etc. (visto en la sesiÃ³n de OSINT de Superficie).

| |
|---|
|**â„¹Â  ConexiÃ³n con OSINT**<br><br>Esta fase es directamente la metodologÃ­a OSINT de superficie que ya trabajaste: Google Dorks, Shodan y consultas DNS. La enumeraciÃ³n web es OSINT aplicado a un dominio concreto, ya dentro del scope.|

## Fase 2 â€” Fingerprinting del stack tecnolÃ³gico

Identifica servidor web, lenguaje, framework y CMS. Esto condiciona toda la estrategia posterior.

| |
|---|
|# WhatWeb: identifica tecnologÃ­as de una web<br><br>whatweb -a 3 http://OBJETIVO<br><br># Cabeceras HTTP a mano con curl (Server, X-Powered-By, Set-Cookie)<br><br>curl -sI http://OBJETIVO|

â€¢Â Â Â Â  **Wappalyzer** (extensiÃ³n de navegador): equivalente visual, muy rÃ¡pido para una primera ojeada.

â€¢Â Â Â Â  Pistas Ãºtiles: cabecera Server, X-Powered-By, nombre de las cookies (PHPSESSID, JSESSIONID, laravel_session), extensiones de fichero (.php, .aspx, .jsp).

| |
|---|
|**âœ“Â  Por quÃ© importa el CMS**<br><br>Si detectas WordPress, el siguiente paso natural es WPScan (auditorÃ­a web dinÃ¡mica, perfil junior mÃ¡s demandado). Cada CMS tiene rutas y vulnerabilidades tÃ­picas conocidas.|

## Fase 3 â€” EnumeraciÃ³n de subdominios

Cada subdominio es una web potencialmente distinta y un nuevo objetivo. Combina fuentes pasivas con resoluciÃ³n activa.

| |
|---|
|# Subfinder: subdominios desde fuentes pasivas<br><br>subfinder -d OBJETIVO.com -o subdominios.txt<br><br># ffuf por fuzzing de subdominios vÃ­a cabecera Host (vhosts)<br><br>ffuf -u http://OBJETIVO -H 'Host: FUZZ.OBJETIVO.com' -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt|
|**â„¹Â  Virtual hosts en laboratorio**<br><br>En HTB es muy habitual que la IP sirva varias webs segÃºn la cabecera Host. Si una web responde igual ante cualquier Host, filtra por tamaÃ±o de respuesta (-fs) para descartar el falso positivo. El fuzzing de vhosts se profundiza el martes 23.|

## Fase 4 â€” EnumeraciÃ³n de directorios y ficheros

Descubre rutas no enlazadas: paneles, backups, ficheros de configuraciÃ³n, directorios de subida.

|# Feroxbuster: descubrimiento recursivo de rutas<br><br>feroxbuster -u http://OBJETIVO -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt<br><br># Gobuster: con extensiones concretas segÃºn el stack detectado<br><br>gobuster dir -u http://OBJETIVO -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,txt,bak,old|
|**Herramienta**|**Punto fuerte**|
|---|---|
|**Feroxbuster**|Recursividad automÃ¡tica, muy rÃ¡pido, ideal para mapear toda la estructura|
|**Gobuster**|Sencillo y directo, control fino de extensiones con -x|
|**ffuf**|El mÃ¡s flexible: directorios, ficheros, vhosts y parÃ¡metros con el keyword FUZZ|
|**Dirsearch**|Trae diccionarios y extensiones por defecto bien pensados|
|**âœ—Â  Errores comunes**<br><br>Lanzar el diccionario equivocado (rutas de IIS contra un servidor Apache/PHP), no filtrar cÃ³digos de respuesta y ahogarte en 404, u olvidar las extensiones (-x) acordes al lenguaje detectado en la fase 2.|

## Fase 5 â€” Endpoints y parÃ¡metros

El Ãºltimo nivel: descubrir parÃ¡metros GET/POST ocultos y endpoints de API que reciben entrada de usuario. Son los futuros puntos de inyecciÃ³n (LFI, SQLi, etc.).

â†’

| |
|---|
|# Descubrir parÃ¡metros GET ocultos con ffuf<br><br>ffuf -u 'http://OBJETIVO/index.php?FUZZ=test' -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 0|
|**â„¹Â  Marco mental de 4 elementos**<br><br>Cada parÃ¡metro descubierto es una FUENTE (sesiÃ³n 25): una entrada que el servidor PROCESA. Identificarlos aquÃ­ es localizar dÃ³nde podrÃ¡s atacar despuÃ©s.|

# â‘£ Herramientas utilizadas en la sesiÃ³n

|**Herramienta**|**Objetivo**|**Fase de auditorÃ­a**|**Comando o uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|WhatWeb|Fingerprint de tecnologÃ­as|Enum. web|whatweb -a 3 URL|Introducida|Ya aparecÃ­a en sesiones previas|
|Wappalyzer|Fingerprint visual|Enum. web|ExtensiÃ³n navegador|Introducida|Complemento rÃ¡pido de WhatWeb|
|Subfinder|Subdominios pasivos|Enum. web|subfinder -d dominio|Mencionada|Herramienta NUEVA en esta sesiÃ³n|
|Feroxbuster|Rutas web recursivas|Enum. web|feroxbuster -u URL -w wl|Practicada|Recursividad automÃ¡tica|
|Gobuster|Directorios/ficheros|Enum. web|gobuster dir -u URL -x php|Practicada|Control de extensiones|
|ffuf|Fuzzing flexible|Enum. web|ffuf -u URL/FUZZ -w wl|Practicada|Vhosts y parÃ¡metros|
|Dirsearch|Directorios con dicc. propio|Enum. web|dirsearch -u URL|Mencionada|Diccionarios por defecto|
|curl|Cabeceras HTTP|Enum. web|curl -sI URL|Practicada|Fingerprint manual|
|**âœ—Â  Nota sobre Subfinder**<br><br>Subfinder no estaba en tu registro previo: es una herramienta nueva a anotar. Mencionada en este material de preparaciÃ³n; confirma en clase los flags y fuentes que recomienda el instructor antes de marcarla como Practicada.|

# â‘¤ Riesgos, errores comunes y buenas prÃ¡cticas

â€¢Â Â Â Â  **Saltarse el recon pasivo** y atacar a ciegas: pierdes subdominios y contexto.

â€¢Â Â Â Â  **No respetar el scope**: enumerar subdominios o IPs fuera de contrato es ilegal.

â€¢Â Â Â Â  **Ignorar el fingerprint**: usar wordlists genÃ©ricas en vez de las del stack real reduce muchÃ­simo los hallazgos.

â€¢Â Â Â Â  **No filtrar respuestas** (-fs, -fc): el ruido de 404/redirecciones esconde lo importante.

| |
|---|
|**âœ“Â  Buena prÃ¡ctica**<br><br>Guarda la salida de cada fase en ficheros (estructura recon/ vista en la sesiÃ³n 25). La enumeraciÃ³n es iterativa: cada subdominio nuevo reinicia el ciclo fingerprint â†’ directorios â†’ parÃ¡metros.|

# â‘¥ ConexiÃ³n con sesiones anteriores

Esta sesiÃ³n enlaza directamente con varias anteriores:

â€¢Â Â Â Â  **OSINT de Superficie**: la fase pasiva (Dorks, DNS, crt.sh) es OSINT aplicado dentro del scope.

â€¢Â Â Â Â  **Nmap (sesiÃ³n 25 y otras)**: Nmap descubre el puerto/servicio web; la enumeraciÃ³n web empieza justo donde Nmap termina (puerto 80/443 abierto).

â€¢Â Â Â Â  **Marco mental de 4 elementos**: cada parÃ¡metro/endpoint enumerado es una FUENTE que el servidor PROCESA.

â€¢Â Â Â Â  **Fuzzing (martes 23)**: la enumeraciÃ³n define dÃ³nde fuzzear; el fuzzing es la tÃ©cnica activa para hacerlo a fondo.

# â‘¦ Resumen final

La enumeraciÃ³n web es el mapa previo a cualquier ataque: de lo **pasivo a lo activo** y de lo **general a lo concreto**. Cinco fases encadenadas â€” recon pasivo, fingerprint del stack, subdominios, directorios/ficheros y endpoints/parÃ¡metros â€” que se retroalimentan. El stack detectado decide las wordlists; los subdominios generan nuevos objetivos; los parÃ¡metros descubiertos son los futuros puntos de inyecciÃ³n. Hacerla bien y de forma ordenada (guardando salidas) es lo que separa una auditorÃ­a web productiva de un ataque a ciegas.

# â‘§ Checklist de repaso

â˜Â Â  SÃ© explicar la diferencia entre enumeraciÃ³n pasiva y activa, y por quÃ© empezar por la pasiva.

â˜Â Â  Puedo hacer fingerprint de un stack con WhatWeb y leer cabeceras con curl -sI.

â˜Â Â  SÃ© enumerar subdominios con Subfinder y por fuzzing de vhosts con ffuf.

â˜Â Â  Domino Feroxbuster/Gobuster/ffuf para directorios y sÃ© ajustar extensiones segÃºn el stack.

â˜Â Â  Entiendo cÃ³mo descubrir parÃ¡metros ocultos y por quÃ© son puntos de inyecciÃ³n.

â˜Â Â  SÃ© filtrar respuestas (-fs/-fc) para reducir ruido.

â˜Â Â  Tengo claro cÃ³mo encadena la enumeraciÃ³n con el fuzzing del martes 23.

# â‘¨ ActualizaciÃ³n del registro de herramientas

---

## Enlaces relacionados

- [[comandos/Nmap]] â€” Cheat sheet de comandos
- [[comandos/BurpSuite]] â€” Cheat sheet de comandos
- [[comandos/FFUF]] â€” Cheat sheet de comandos

Para copiar a tu base de conocimiento tras validar en clase:

|**Herramienta**|**Nivel propuesto**|**Cambio**|
|---|---|---|
|Subfinder|Mencionada|NUEVA â€” enumeraciÃ³n de subdominios pasiva|
|WhatWeb|Introducida|Se mantiene|
|Wappalyzer|Introducida|Se mantiene|
|Feroxbuster|Practicada|Refuerzo en contexto de metodologÃ­a|
|ffuf|Practicada|Refuerzo (vhosts y parÃ¡metros)|
|Dirsearch|Mencionada|Se mantiene hasta uso prÃ¡ctico|

â†’

