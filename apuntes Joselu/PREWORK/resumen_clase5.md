> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 5**
> **Módulo:** PREWORK
> **Tema:** Clase 5
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 5. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 5: Auditorías de Aplicaciones Web y Redes Wi-Fi Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy PARTE I: Auditorías de Aplicaciones Web 1.

Por qué son necesarias Cada vez más empresas tienen aplicaciones propias expuestas a internet (páginas corporativas, portales de gestión, acceso en teletrabajo), lo que amplía continuamente la superficie de ataque.

Las auditorías de aplicaciones web tienen un objetivo muy concreto: identificar y mitigar las vulnerabilidades potencialmente críticas antes de que puedan ser explotadas.

Los servidores de aplicaciones web suelen estar alojados en la red interna de la organización, por lo que un acceso exitoso a través de la web puede derivar en un movimiento lateral que comprometa toda la infraestructura interna.

Junto a las auditorías internas de redes, las auditorías web son las segundas más demandadas por los clientes debido a la sensibilidad de los datos que manejan. 2.

Metodología: OWASP Top 10 y OSSTMM Las auditorías de aplicaciones web siguen dos marcos de referencia principales:
- OWASP Top 10 (Open Web Application Security Project ): estándar que identifica las
diez vulnerabilidades más comunes y peligrosas en aplicaciones web.

Es el marco mínimo indispensable para cualquier auditoría web y cubre controles desde el diseño hasta la monitorización.
- OSSTMM v3.0 (Open Source Security Testing Methodology Manual ): utilizado en
auditorías internas y externas de redes.

El OWASP Top 10 no abarca la lógica de negocio (truncar funcionalidades propias de la aplicación para llevar a cabo acciones no previstas), que es la parte más valorada por el profesor y que ninguna herramienta automatizada puede detectar por sí sola. 3.

Los controles del OWASP Top 10 Broken Access Control: verificar que los controles de acceso y roles estén bien implementados. 1

Incluye comprobar escaladas de privilegios, acceso a recursos restringidos mediante manipulación de URLs, tokens de sesión robados o parámetros alterados.

### Fallos criptográficos: uso de algoritmos obsoletos o rotos (ej.

MD5), versiones antiguas de TLS (1.0, 1.1), cifrado incorrecto de datos en tránsito, en reposo o en comunicaciones entre componentes.

Inyección: la parte más crítica e interesante para el profesor.

Incluye inyecciones SQL, XPath, LDAP, Cross-Site Scripting (XSS con JavaScript), inyecciones en PHP o .NET, subida de reverse shells y ejecución remota de código (RCE).

Una RCE tiene una puntuación CVSS de 9.8, la más alta posible.

Diseño inseguro (Insecure Design): una aplicación puede ser vulnerable desde su fase de diseño si los arquitectos priorizan funcionalidad o estética sobre seguridad.

Es crítico incorporar perfiles de DevSecOps desde el inicio del desarrollo.

### Ejemplo real: cliente al que se recomendó rehacer una aplicación valorada en más de 200 000 € porque no superó ningún control de seguridad.

Security Misconfiguration: cabeceras de seguridad mal configuradas, archivos de configuración con credenciales expuestas, puertos abiertos innecesariamente.

Los desarrolladores no tienen por qué conocer estas configuraciones de seguridad; para eso existen los auditores.

Componentes vulnerables y desactualizados: uso de librerías de terceros sin verificar su estado de seguridad.

### Ejemplo paradigmático: Log4Shell (Log4j), librería de Java con una vulnerabilidad activa durante 11 años sin que nadie la detectara.

Fallos en identificación y autenticación: mecanismos de login bypassables, validación incorrecta de caracteres, sesiones mal gestionadas.

Integridad de datos y software: los datos deben ser inmutables.

Si un atacante puede modificar la base de datos o truncar funcionalidades (ej. verificación de edad), la información de toda la empresa queda corrompida.

Fallos en registros y monitorización: si los eventos de seguridad no se registran correctamente, es imposible rastrear el origen de un incidente.

Falsificación de solicitudes del lado del servidor (SSRF) y CSRF: interponiendo un proxy entre la aplicación y el servidor se pueden modificar tanto las solicitudes como las respuestas.

La herramienta principal para esto es Burp Suite. 4.

Lógica de negocio e IDOR: los ataques más “sencillos” y devastadores El profesor destaca dos tipos de vulnerabilidades que no detecta ninguna herramienta automatizada: Lógica de negocio: ejemplo real de una aplicación médica que solo debería aceptar archivos 2

PDF o Word.

Si un atacante consigue subir un archivo .php eludiendo el control de extensiones, puede ejecutarlo en el servidor y obtener una RCE (CVSS 9.8) con acceso a todos los historiales clínicos.

IDOR (Insecure Direct Object Reference ): vulnerabilidad de iteración de parámetros en APIs.

Ejemplo real de impacto nacional: una aplicación de salud de una comunidad autónoma española exponía llamadas a su API con parámetros numéricos de ID de paciente (/api/v1/paciente/19 ).

Al iterar el identificador (19 → 20 → 21…), un atacante accedió a los historiales clínicos de todos los ciudadanos españoles, incluyendo los de miembros de la familia real y políticos de relevancia nacional. 5.

Fases de la auditoría de aplicaciones web 1.Recopilación de información: uso de herramientas como Burp Suite, FOCA, Google Dorking, sitemap, archivo robots.txt, enumeración de APIs y subdominios. 2.Mapeo del flujo de la aplicación: entender cómo interactúan los usuarios con la aplicación, identificar puntos de entrada (formularios, parámetros, APIs).

Es lo que diferencia a un auditor experto de una herramienta automatizada. 3.Análisis del Broken Access Control: escaladas de privilegios, manipulación de tokens y parámetros. 4.Análisis de fallos criptográficos: revisión de algoritmos, versiones de TLS, cifrado en tránsito y en reposo. 5.Explotación controlada: pruebas manuales para verificar y evidenciar las vulnerabilidades detectadas.

Herramienta de práctica recomendada: WebGoat. 6.Validación de hallazgos y reporte: informe con resumen ejecutivo, detalles técnicos y recomendaciones (disponibles en la propia web de OWASP), categorizando el impacto en integridad, confidencialidad y disponibilidad.

PARTE II: Auditorías de Redes Wi-Fi 6.

Por qué toda comunicación inalámbrica es insegura por diseño Cualquier señal que viaje por ondas puede ser interceptada.

Aunque se implementen capas de cifrado, la interceptación es siempre posible, por lo que el profesor considera que toda comunicación inalámbrica es insegura por definición .

El cifrado puede romperse; solo es cuestión de tiempo y recursos.

Las auditorías Wi-Fi tienen una característica única: no se pueden realizar de forma remota .

El alcance de las redes inalámbricas es de 50 a 200 metros, lo que obliga al auditor a desplazarse físicamente a las instalaciones del cliente. 3

## 7.

Protocolos de cifrado Wi-Fi y su nivel de seguridad Protocolo Estado Observaciones WEP Obsoleto y roto Se rompe en ~15 minutos con ataque de diccionario WPA Débil Mejor que WEP pero vulnerable WPA2-PSK Estándar doméstico Seguro si la contraseña es robusta; vulnerable a KRACK WPA2-Enterprise Estándar corporativo Autenticación mediante usuario/contraseña corporativos contra servidor RADIUS + Kerberos (Active Directory) WPA3 Más seguro Incluso con WPS activo, WPA3 puede ser vulnerable El protocolo WPS activo invalida cualquier nivel de cifrado y es un vector de ataque inmediato. 8.

Metodología: OWASP Wi-Fi Testing Guide Análogamente al OWASP Top 10 para aplicaciones web, el OWASP Wi-Fi Testing Guide es el estándar de referencia para auditorías de redes inalámbricas.

Define las pruebas mínimas e indispensables que deben realizarse sobre cualquier infraestructura Wi-Fi. 9.

Ataques más comunes en redes Wi-Fi Ataques de deautenticación: se envían paquetes de deautenticación (frames 802.11) que saturan la comunicación entre el access point y los dispositivos conectados, forzándolos a desconectarse.

Todos los dispositivos conectados a una red inalámbrica están permanentemente “a la escucha”, lo que los hace vulnerables a recibir estos paquetes aunque no provengan del access point legítimo.

Evil Twin / Rogue Access Point: se levanta un punto de acceso falso con el mismo SSID que la red legítima.

El atacante combina este ataque con la deautenticación para obligar a los dispositivos a conectarse a la red falsa.

Se puede añadir un portal cautivo que clone la página de login de la organización para robar credenciales.

### Ejemplo real: el profesor levantó una red con el SSID “EMT_Madrid” (red del autobús público) en la Puerta del Sol, consiguiendo en segundos más de 200 dispositivos conectados a su red, actuando como proxy entre ellos e internet.

Ataque KRACK (Key Reinstallation Attack ): ataque al protocolo WPA2 que explota el proceso del four-way handshake.

Solo es viable bajo configuraciones muy específicas; no es una vulnerabilidad generalizada del protocolo. 4

Identificación de dispositivos no autorizados: detección de dispositivos desconocidos conectados a la red o de rogue access points utilizando herramientas como Kismet.

También se pueden usar verificaciones de MAC para detectar si dispositivos legítimos se han conectado a una red que suplanta la red corporativa. 10.

Redes empresariales WPA2-Enterprise y servidor RADIUS Las redes corporativas utilizan WPA2-Enterprise , donde la autenticación se realiza con credenciales corporativas (usuario + contraseña) contra un servidor RADIUS alojado en el Active Directory, usando el protocolo Kerberos para obtener un ticket de acceso.

Comprometer esta red equivale a tener un acceso inicial a la red interna de la organización. 11.

### Certificación especializada: OSWP La empresa Offensive Security ofrece la certificación OSWP (Offensive Security Wireless Professional), dedicada exclusivamente a redes inalámbricas.

El examen requiere vulnerar tres máquinas: una con WEP, una con WPA2 y una con WPA2-Enterprise mediante falsificación de certificados y servidor de autenticación propio.

Plataforma de práctica recomendada: Wi-Fi Labs, entorno virtual que simula antenas y comunicaciones inalámbricas para practicar sin necesidad de hardware real. 12.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración log4g Log4Shell / Log4j – vulnerabilidad crítica en librería Java (2021) bursuit / bullshit Burp Suite – proxy de interceptación para auditorías web cross-side script Cross-Site Scripting (XSS) – inyección de código JavaScript en páginas web cross site request forgy CSRF (Cross-Site Request Forgery ) – falsificación de solicitudes entre sitios sidos / sids IDOR (Insecure Direct Object Reference ) – iteración de parámetros de objetos en APIs no was top ten / owas OWASP Top 10 – estándar de vulnerabilidades en aplicaciones web owas wifi testing guide OWASP Wi-Fi Testing Guide – estándar de auditorías de redes inalámbricas caice Caché o referencia a validación de caché en la 5

Término en la transcripción Corrección / Aclaración aplicación foca de ser FOCA – herramienta de extracción de metadatos de documentos webgoat WebGoat – aplicación vulnerable deliberadamente para práctica de pentesting web querberos / querberos Kerberos – protocolo de autenticación en redes corporativas servidor de radios Servidor RADIUS – servidor de autenticación para redes Wi-Fi empresariales crack (ataque wpa2) KRACK (Key Reinstallation Attack ) – ataque al handshake de WPA2 kiss me Kismet – herramienta de detección de redes y dispositivos inalámbricos oswp / ofensiv security wireless pen test OSWP (Offensive Security Wireless Professional) – certificación de redes Wi-Fi wifi labs Wi-Fi Labs – plataforma virtual de práctica en auditorías Wi-Fi rc de RCE (Remote Code Execution ) – ejecución remota de código emt guión bajo madrid EMT_Madrid – SSID de la red Wi-Fi gratuita de los autobuses de Madrid Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6