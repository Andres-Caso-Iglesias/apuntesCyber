# â‘  Â¿QuÃ© es OSINT y marco legal?

OSINT (Open Source Intelligence) es la recopilaciÃ³n de informaciÃ³n **desde fuentes pÃºblicas** sin necesitar credenciales ni exploits. Es el primer paso de cualquier auditorÃ­a.

| | |
|---|---|
|**âš– LEGAL**|El OSINT en sÃ­ mismo es legal: uses informaciÃ³n pÃºblica. El lÃ­mite estÃ¡ en cÃ³mo se usa: un escaneo de puertos a una empresa sin contrato es ilegal. La autorizaciÃ³n explÃ­cita del cliente es la clave.|

|**Estado**|**DescripciÃ³n**|
|---|---|
|Legal|Consultar redes sociales, WHOIS, LinkedIn, registros DNS, Shodan sobre IPs pÃºblicas con contrato.|
|Zona gris|Usar bases de datos de contraseÃ±as filtradas para auditorÃ­a interna (consultar â‰  usar contra terceros).|
|Ilegal|Escanear sin autorizaciÃ³n, usar credenciales filtradas para acceder, comprar bases robadas.|

# â‘¡ MetodologÃ­a OSINT â€” El ciclo de inteligencia

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**1. Definir objetivo**|->|**2. RecolecciÃ³n**|->|**3. Procesamiento**|->|**4. AnÃ¡lisis**|->|**5. Informe**|

**Antes de abrir cualquier herramienta:** define exactamente quÃ© informaciÃ³n necesitas. Â¿Empleados? Â¿Infraestructura expuesta? Â¿Credenciales filtradas? Objetivo concreto = menos ruido.

| | |
|---|---|
|**ðŸ’¡ PRIMER PASO**|Cuando un cliente te contrata para una auditorÃ­a externa, lo primero que le preguntas es: Â¿quÃ© activos son tuyos? Dominio principal, filiales, rangos de IP. Eso es el 'scope'.|

# â‘¢ Google Dorks â€” BÃºsqueda avanzada

| |
|---|
|# Operadores de bÃºsqueda avanzada en Google:<br><br>site:empresa.comÂ Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â Â  # solo resultados de ese dominio<br><br>site:empresa.com filetype:pdfÂ Â Â Â Â  # PDFs de ese dominio<br><br>site:empresa.com inurl:adminÂ Â Â Â Â Â  # URLs con 'admin'<br><br>site:empresa.com intitle:loginÂ Â Â Â  # pÃ¡ginas con 'login' en el tÃ­tulo<br><br>intext:'contraseÃ±a' site:emp.comÂ Â  # texto especÃ­fico en la pÃ¡gina<br><br># Dorks Ãºtiles en auditorÃ­as:<br><br>site:empresa.com filetype:xlsxÂ Â Â Â  # hojas Excel expuestas<br><br>site:empresa.com filetype:sqlÂ Â Â Â Â  # dumps de BD expuestos<br><br>inurl:/wp-content/uploads site:emp # uploads de WordPress<br><br>site:pastebin.com empresa.comÂ Â Â Â Â  # menciones en Pastebin<br><br>site:github.com empresa.comÂ Â Â Â Â Â Â  # cÃ³digo en GitHub<br><br># Encontrar subdominios:<br><br>site:*.empresa.com<br><br># Recursos:<br><br># exploit-db.com/google-hacking-database (GHDB)|

| | |
|---|---|
|**ðŸ” EXPOSICIÃ“N**|Muchas empresas tienen documentos internos, copias de seguridad (.bak, .old) o paneles de administraciÃ³n indexados en Google por error. Los Google Dorks los encuentran en segundos.|

# â‘£ Sherlock y Maigret â€” BÃºsqueda por username

| |
|---|
|# Sherlock: busca un username en cientos de redes sociales<br><br># InstalaciÃ³n:<br><br>pip install sherlock-project<br><br># o desde GitHub:<br><br>git clone https://github.com/sherlock-project/sherlock<br><br>cd sherlock && pip install -r requirements.txt<br><br># Uso bÃ¡sico:<br><br>sherlock usuario_objetivo<br><br># Guardar resultados en fichero:<br><br>sherlock usuario_objetivo --output resultados.txt<br><br># Con Tor (mÃ¡s anÃ³nimo):<br><br>sherlock usuario_objetivo --tor<br><br># Maigret: mÃ¡s completo, anÃ¡lisis de perfiles<br><br>pip install maigret<br><br>maigret usuario_objetivo<br><br>maigret usuario_objetivo --report htmlÂ  # informe HTML|

| | |
|---|---|
|**âš  FALSOS POSITIVOS**|Sherlock y Maigret solo verifican el cÃ³digo HTTP de respuesta (200 vs 404). Algunas webs devuelven 200 aunque el usuario no exista â†’ hay que verificar manualmente los resultados clave.|

# â‘¤ WHOIS y DNS â€” Infraestructura del objetivo

| |
|---|
|# WHOIS â€” informaciÃ³n de registro de dominios:<br><br>whois empresa.com<br><br># InformaciÃ³n que puede revelar:<br><br># Registrant (propietario), correos, telÃ©fonos, fechas<br><br># Muchos usan privacy protection â€” datos ocultos<br><br># DNS â€” enumeraciÃ³n de subdominios:<br><br>dig empresa.com ANYÂ Â Â Â Â Â Â Â Â Â  # todos los registros DNS<br><br>dig empresa.com MXÂ Â Â Â Â Â Â Â Â Â Â  # servidores de correo<br><br>dig empresa.com NSÂ Â Â Â Â Â Â Â Â Â Â  # servidores de nombre<br><br># Transferencia de zona (si estÃ¡ mal configurada):<br><br>dig axfr empresa.com @ns1.empresa.com<br><br># Si funciona: ORO. Revela todos los subdominios.<br><br># Herramientas de enumeraciÃ³n de subdominios:<br><br>subfinder -d empresa.com<br><br>amass enum -d empresa.com<br><br>dnsrecon -d empresa.com<br><br># Certificate Transparency (sin herramientas):<br><br># crt.sh/?q=%.empresa.comÂ  â† en el navegador<br><br>curl -s 'https://crt.sh/?q=%.empresa.com&output=json' | jq '.[].name_value'|

# â‘¥ Shodan â€” El buscador de dispositivos

| |
|---|
|# Shodan indexa servicios expuestos en Internet<br><br># Web: shodan.io | CLI: pip install shodan<br><br># BÃºsquedas en Shodan web:<br><br>org:'Nombre Empresa'Â Â Â Â Â Â Â Â Â Â  # todos los activos de una empresa<br><br>net:185.12.34.0/24Â Â Â Â Â Â Â Â Â Â Â Â  # rango de IPs<br><br>hostname:empresa.comÂ Â Â Â Â Â Â Â Â Â  # por hostname<br><br># Filtros Ãºtiles:<br><br>port:22 org:'empresa'Â Â Â Â Â Â Â Â Â  # SSH expuesto<br><br>port:3389 country:ESÂ Â Â Â Â Â Â Â Â Â  # RDP en EspaÃ±a<br><br>product:Apache version:2.2Â Â Â Â  # versiones vulnerables<br><br>vuln:CVE-2021-44228Â Â Â Â Â Â Â Â Â Â Â  # Log4Shell expuesto<br><br># CLI de Shodan:<br><br>export SHODAN_API_KEY='tu_api_key'<br><br>shodan init $SHODAN_API_KEY<br><br>shodan search 'org:empresa port:22'<br><br>shodan host 1.2.3.4|

| | |
|---|---|
|**ðŸ’¡ SHODAN**|Shodan no solo encuentra cÃ¡maras IP y routers: tambiÃ©n servidores con versiones vulnerables, bases de datos abiertas, paneles de administraciÃ³n sin autenticaciÃ³n. Fundamental en auditorÃ­as externas.|

# â‘¦ HIBP y bases de datos filtradas

| |
|---|
|# Have I Been Pwned (HIBP) â€” haveibeenpwned.com<br><br># Consultar si un email o dominio tiene credenciales filtradas.<br><br># API (requiere key gratuita para dominios):<br><br>curl 'https://haveibeenpwned.com/api/v3/breachedaccount/correo@empresa.com'<br><br># Herramientas similares:<br><br># dehashed.com (requiere suscripciÃ³n)<br><br># intelx.io<br><br># hunter.io â†’ correos corporativos por dominio<br><br># âš  IMPORTANTE:<br><br># Consultar HIBP = LEGAL (datos ya pÃºblicos)<br><br># Descargar/usar bases de datos robadas = ILEGAL<br><br># Usar credenciales filtradas contra sistemas = ILEGAL|

| | |
|---|---|
|**âš– LEGALIDAD**|Consultar si un email estÃ¡ en HIBP es legal. Comprar o descargar bases de datos de contraseÃ±as es ilegal. Usarlas para acceder a sistemas ajenos es delito penal en todos los paÃ­ses de la UE.|

# â‘§ LinkedIn y OSINT de personas

| |
|---|
|# LinkedIn como fuente de OSINT organizacional:<br><br># Empleados â†’ tecnologÃ­as usadas (Java developer, Azure admin...)<br><br># Organigramas â†’ estructura de la empresa<br><br># Ofertas de trabajo â†’ tecnologÃ­as y herramientas usadas internamente<br><br># Formato de email corporativo:<br><br># La mayorÃ­a sigue patrones: nombre.apellido@empresa.com<br><br># hunter.io puede verificar el formato de una empresa<br><br># Herramientas para LinkedIn:<br><br># linkedin2username â†’ genera listas de usuarios<br><br># InSpy â†’ enumera empleados por empresa<br><br># ConstrucciÃ³n de perfil de un objetivo (persona):<br><br># 1. Nombre completo â†’ variaciones (con/sin tilde)<br><br># 2. Username en redes â†’ sherlock/maigret<br><br># 3. Correos â†’ hunter.io, HIBP<br><br># 4. Foto â†’ bÃºsqueda inversa (Google Lens, pimeyes.com)<br><br># 5. NÃºmero de telÃ©fono â†’ truecaller, eyecon<br><br># 6. Documentos online â†’ Google Dorks site:linkedin.com nombre|

| | |
|---|---|
|**ðŸ” SPEAR PHISHING**|Toda la informaciÃ³n recopilada sobre una persona o empresa se usa para construir ataques de spear phishing altamente personalizados. Un email que menciona el nombre de tu jefe, tu cargo y tu proyecto actual tiene altÃ­sima tasa de Ã©xito.|

â†’

â†’

â†’

