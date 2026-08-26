# â‘  ¿Qué es OSINT y marco legal?

OSINT (Open Source Intelligence) es la recopilación de información **desde fuentes públicas** sin necesitar credenciales ni exploits. Es el primer paso de cualquier auditoría.

| | |
|---|---|
|**âš– LEGAL**|El OSINT en sí mismo es legal: uses información pública. El límite está en cómo se usa: un escaneo de puertos a una empresa sin contrato es ilegal. La autorización explícita del cliente es la clave.|

|**Estado**|**Descripción**|
|---|---|
|Legal|Consultar redes sociales, WHOIS, LinkedIn, registros DNS, Shodan sobre IPs públicas con contrato.|
|Zona gris|Usar bases de datos de contraseñas filtradas para auditoría interna (consultar ≠  usar contra terceros).|
|Ilegal|Escanear sin autorización, usar credenciales filtradas para acceder, comprar bases robadas.|

# ② Metodología OSINT — El ciclo de inteligencia

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**1. Definir objetivo**|->|**2. Recolección**|->|**3. Procesamiento**|->|**4. Análisis**|->|**5. Informe**|

**Antes de abrir cualquier herramienta:** define exactamente qué información necesitas. ¿Empleados? ¿Infraestructura expuesta? ¿Credenciales filtradas? Objetivo concreto = menos ruido.

| | |
|---|---|
|**ðŸ’¡ PRIMER PASO**|Cuando un cliente te contrata para una auditoría externa, lo primero que le preguntas es: ¿qué activos son tuyos? Dominio principal, filiales, rangos de IP. Eso es el 'scope'.|

# ③ Google Dorks — Búsqueda avanzada

| |
|---|
|# Operadores de búsqueda avanzada en Google:<br><br>site:empresa.com                   # solo resultados de ese dominio<br><br>site:empresa.com filetype:pdf      # PDFs de ese dominio<br><br>site:empresa.com inurl:admin       # URLs con 'admin'<br><br>site:empresa.com intitle:login     # páginas con 'login' en el título<br><br>intext:'contraseña' site:emp.com   # texto específico en la página<br><br># Dorks útiles en auditorías:<br><br>site:empresa.com filetype:xlsx     # hojas Excel expuestas<br><br>site:empresa.com filetype:sql      # dumps de BD expuestos<br><br>inurl:/wp-content/uploads site:emp # uploads de WordPress<br><br>site:pastebin.com empresa.com      # menciones en Pastebin<br><br>site:github.com empresa.com        # código en GitHub<br><br># Encontrar subdominios:<br><br>site:*.empresa.com<br><br># Recursos:<br><br># exploit-db.com/google-hacking-database (GHDB)|

| | |
|---|---|
|**ðŸ” EXPOSICIÃ“N**|Muchas empresas tienen documentos internos, copias de seguridad (.bak, .old) o paneles de administración indexados en Google por error. Los Google Dorks los encuentran en segundos.|

# ④ Sherlock y Maigret — Búsqueda por username

| |
|---|
|# Sherlock: busca un username en cientos de redes sociales<br><br># Instalación:<br><br>pip install sherlock-project<br><br># o desde GitHub:<br><br>git clone https://github.com/sherlock-project/sherlock<br><br>cd sherlock && pip install -r requirements.txt<br><br># Uso básico:<br><br>sherlock usuario_objetivo<br><br># Guardar resultados en fichero:<br><br>sherlock usuario_objetivo --output resultados.txt<br><br># Con Tor (más anónimo):<br><br>sherlock usuario_objetivo --tor<br><br># Maigret: más completo, análisis de perfiles<br><br>pip install maigret<br><br>maigret usuario_objetivo<br><br>maigret usuario_objetivo --report html  # informe HTML|

| | |
|---|---|
|**âš  FALSOS POSITIVOS**|Sherlock y Maigret solo verifican el código HTTP de respuesta (200 vs 404). Algunas webs devuelven 200 aunque el usuario no exista →’ hay que verificar manualmente los resultados clave.|

# ⑤ WHOIS y DNS — Infraestructura del objetivo

| |
|---|
|# WHOIS — información de registro de dominios:<br><br>whois empresa.com<br><br># Información que puede revelar:<br><br># Registrant (propietario), correos, teléfonos, fechas<br><br># Muchos usan privacy protection — datos ocultos<br><br># DNS — enumeración de subdominios:<br><br>dig empresa.com ANY           # todos los registros DNS<br><br>dig empresa.com MX            # servidores de correo<br><br>dig empresa.com NS            # servidores de nombre<br><br># Transferencia de zona (si está mal configurada):<br><br>dig axfr empresa.com @ns1.empresa.com<br><br># Si funciona: ORO. Revela todos los subdominios.<br><br># Herramientas de enumeración de subdominios:<br><br>subfinder -d empresa.com<br><br>amass enum -d empresa.com<br><br>dnsrecon -d empresa.com<br><br># Certificate Transparency (sin herramientas):<br><br># crt.sh/?q=%.empresa.com  → en el navegador<br><br>curl -s 'https://crt.sh/?q=%.empresa.com&output=json' | jq '.[].name_value'|

# ⑥ Shodan — El buscador de dispositivos

| |
|---|
|# Shodan indexa servicios expuestos en Internet<br><br># Web: shodan.io | CLI: pip install shodan<br><br># Búsquedas en Shodan web:<br><br>org:'Nombre Empresa'           # todos los activos de una empresa<br><br>net:185.12.34.0/24             # rango de IPs<br><br>hostname:empresa.com           # por hostname<br><br># Filtros útiles:<br><br>port:22 org:'empresa'          # SSH expuesto<br><br>port:3389 country:ES           # RDP en España<br><br>product:Apache version:2.2     # versiones vulnerables<br><br>vuln:CVE-2021-44228            # Log4Shell expuesto<br><br># CLI de Shodan:<br><br>export SHODAN_API_KEY='tu_api_key'<br><br>shodan init $SHODAN_API_KEY<br><br>shodan search 'org:empresa port:22'<br><br>shodan host 1.2.3.4|

| | |
|---|---|
|**ðŸ’¡ SHODAN**|Shodan no solo encuentra cámaras IP y routers: también servidores con versiones vulnerables, bases de datos abiertas, paneles de administración sin autenticación. Fundamental en auditorías externas.|

# ⑦ HIBP y bases de datos filtradas

| |
|---|
|# Have I Been Pwned (HIBP) — haveibeenpwned.com<br><br># Consultar si un email o dominio tiene credenciales filtradas.<br><br># API (requiere key gratuita para dominios):<br><br>curl 'https://haveibeenpwned.com/api/v3/breachedaccount/correo@empresa.com'<br><br># Herramientas similares:<br><br># dehashed.com (requiere suscripción)<br><br># intelx.io<br><br># hunter.io →’ correos corporativos por dominio<br><br># âš  IMPORTANTE:<br><br># Consultar HIBP = LEGAL (datos ya públicos)<br><br># Descargar/usar bases de datos robadas = ILEGAL<br><br># Usar credenciales filtradas contra sistemas = ILEGAL|

| | |
|---|---|
|**âš– LEGALIDAD**|Consultar si un email está en HIBP es legal. Comprar o descargar bases de datos de contraseñas es ilegal. Usarlas para acceder a sistemas ajenos es delito penal en todos los países de la UE.|

# ⑧ LinkedIn y OSINT de personas

| |
|---|
|# LinkedIn como fuente de OSINT organizacional:<br><br># Empleados →’ tecnologías usadas (Java developer, Azure admin...)<br><br># Organigramas →’ estructura de la empresa<br><br># Ofertas de trabajo →’ tecnologías y herramientas usadas internamente<br><br># Formato de email corporativo:<br><br># La mayoría sigue patrones: nombre.apellido@empresa.com<br><br># hunter.io puede verificar el formato de una empresa<br><br># Herramientas para LinkedIn:<br><br># linkedin2username →’ genera listas de usuarios<br><br># InSpy →’ enumera empleados por empresa<br><br># Construcción de perfil de un objetivo (persona):<br><br># 1. Nombre completo →’ variaciones (con/sin tilde)<br><br># 2. Username en redes →’ sherlock/maigret<br><br># 3. Correos →’ hunter.io, HIBP<br><br># 4. Foto →’ búsqueda inversa (Google Lens, pimeyes.com)<br><br># 5. Número de teléfono →’ truecaller, eyecon<br><br># 6. Documentos online →’ Google Dorks site:linkedin.com nombre|

| | |
|---|---|
|**ðŸ” SPEAR PHISHING**|Toda la información recopilada sobre una persona o empresa se usa para construir ataques de spear phishing altamente personalizados. Un email que menciona el nombre de tu jefe, tu cargo y tu proyecto actual tiene altísima tasa de éxito.|

→’

→’

→’

