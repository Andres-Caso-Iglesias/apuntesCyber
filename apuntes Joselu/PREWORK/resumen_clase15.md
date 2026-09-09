> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 15**
> **Módulo:** PREWORK
> **Tema:** Clase 15
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 15. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 15: Metodologías de Pentesting – Deep Web y Dark Web Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: la Deep Web como enumeración pasiva avanzada La Deep Web (y por extensión la Dark Web) es la continuación natural de la fase de enumeración pasiva vista en la sesión anterior.

A través de ella se obtiene la información más sensible del objetivo: credenciales filtradas, bases de datos robadas, documentos internos expuestos y declaraciones de intenciones de grupos cibercriminales.

Para los profesionales de ciberseguridad, la Deep Web tiene dos usos fundamentales y legítimos: 1.Enumeración en auditorías técnicas: obtener credenciales y datos filtrados para usarlos en la fase de explotación (con permiso del cliente). 2.Vigilancia digital: monitorización continua para detectar si los datos de un cliente han sido robados y publicados antes de que el cliente lo sepa.

### Advertencia legal: acceder a la Deep Web no es ilegal.

Comprar bases de datos robadas o interactuar con grupos cibercriminales sí lo es, salvo permiso explícito de un cuerpo de seguridad del Estado o del propio cliente para monitorizar su información. 2.

Deep Web vs.

> [!important] Dark Web: diferencias y estructura Se usa la metáfora del iceberg para explicar las capas de Internet: Capa Nombre Descripción Punta del iceberg Surface Web (Internet normal) Lo indexado por Google, Bing, Yandex; accesible desde cualquier navegador Zona media Deep Web Contenido no indexado por los motores de búsqueda; incluye intranets, bases de datos privadas, recursos de pago y foros especializados Fondo del iceberg Dark Web Subconjunto de la Deep Web accesible únicamente a través de proxies/TOR; dominio .onion; alto contenido ilegal Puntos clave: - La Dark Web es una parte de la Deep Web, no una entidad separada. - Ambas 1

nacen para proporcionar anonimato frente a la trazabilidad de Internet convencional. - El anonimato es relativo: muchos nodos de la red TOR, especialmente los nodos de salida, están controlados por el FBI y otros cuerpos de seguridad.

No se puede descifrar de dónde viene el paquete, pero sí el contenido que viaja por el nodo de salida.

Usar la Dark Web para actividades ilegales conlleva un riesgo real de identificación.

Para los profesionales: el foco está en la Deep Web (foros, plataformas de credenciales, vigilancia de grupos de ransomware), no en la Dark Web, cuyo contenido habitual (armas, drogas, material ilegal) no tiene utilidad profesional. 3.

TOR: el navegador de acceso a la Deep/Dark Web TOR (The Onion Router) es el navegador que permite acceder a la red anónima y a los sitios .onion.

Descargable en torproject.org para Windows, Mac, Linux y Android.

### Cómo funciona: Al conectarse a través de TOR, el tráfico pasa por una cadena de nodos (cada uno es un usuario real de la red).

Cada nodo conoce únicamente el nodo anterior y el siguiente, nunca el origen ni el destino completo.

### Sin embargo: - Los nodos de salida (el último salto antes de llegar al destino en Internet) pueden desencriptar el contenido del paquete. - Muchos de estos nodos de salida están controlados por agencias gubernamentales (FBI, etc.). - Por tanto, el anonimato en TOR no es absoluto y no debe usarse para actividades ilegales.

Buscador dentro de TOR: DuckDuckGo — permite buscar sin dejar rastro de cookies ni historial.

Las páginas .onion no están indexadas en ningún motor de búsqueda convencional; solo son accesibles con la URL exacta. 4.

Herramientas de monitorización de credenciales filtradas Dehashed Plataforma que indexa bases de datos filtradas y permite buscar por dominio, correo, nombre de usuario o contraseña.

Ejemplo de la sesión: búsqueda de moeve.es → 1 credencial filtrada ya con el nuevo nombre de marca; búsqueda de cepsa.es → 29 credenciales filtradas con correos y contraseñas corporativas listas para ser probadas en los portales de login identificados durante la enumeración pasiva.

Intelligence X Similar a Dehashed pero con mayor profundidad de búsqueda.

Además de credenciales, indexa documentos filtrados, correos y otro tipo de información sensible.

Ejemplo: búsqueda de moeve.es → varios correos, contraseñas y documentos filtrados; búsqueda de cepsa.es → gran 2

volumen de documentación interna expuesta.

Valor estratégico de las credenciales filtradas: - Revelan la política de contraseñas de la organización (patrón, longitud, caracteres). - Permiten construir diccionarios personalizados para ataques de fuerza bruta. - Pueden reutilizarse directamente en portales corporativos si el empleado no ha cambiado la contraseña filtrada. - Con el volumen de credenciales que se obtiene, en muchos casos el acceso se consigue sin necesidad de explotar ninguna vulnerabilidad técnica . 5.

BreachForums: el foro de referencia de la Deep Web BreachForums (anteriormente conocido como RaidForums) es el foro más importante de la Deep Web para los profesionales de ciberseguridad ofensiva y el servicio de vigilancia digital.

Accesible tanto desde Internet normal como desde TOR a través de su dirección .onion (siempre recomendable usar TOR para no ser rastreado).

Qué se puede encontrar en BreachForums Bases de datos robadas: - Se publican y venden bases de datos con correos y contraseñas de todo tipo de organizaciones. - Cada publicación incluye una demo (muestra parcial) para que el comprador evalúe la calidad. - Los precios van desde 1-2 € para bases de datos pequeñas hasta 5.000-1.000.000 € para las más valiosas (gobiernos, grandes corporaciones, entidades financieras). - También se encuentran datos de tarjetas de crédito robadas para carding.

Habitualmente, quien roba los datos de las tarjetas no es quien hace el carding; los vende a un tercero especializado.

Grupos de ransomware: Los grupos más conocidos (LockBit, ALPHV/BlackCat, Cl0p…) tienen sus propias páginas .onion donde publican los datos de las empresas que no han pagado el rescate.

Esta información es fundamental para el servicio de vigilancia digital: si el cliente de un consultor aparece listado aquí, hay que actuar inmediatamente.

Se pueden encontrar los enlaces actualizados a estos sitios buscando el nombre del grupo en BreachForums.

Otros recursos útiles: - Wordlists y diccionarios para cracking de contraseñas. - Tutoriales, cursos y certificaciones (incluyendo material de exámenes). - Servicios de acceso a cuentas de plataformas (Netflix, Amazon, etc.) ya comprometidas. - Contratación de hackers para encargos (ilegal). - Información sobre amenazas emergentes y nuevas técnicas de ataque. - Foros especializados como XSS.is para debate técnico en hacking ofensivo.

Uso ético y legal de BreachForums El uso profesional y legítimo se limita a: - Monitorizar si los datos de los clientes han sido filtrados. - Identificar credenciales del objetivo para usarlas en auditorías autorizadas. - Mantenerse informado sobre nuevas amenazas y técnicas de los grupos cibercriminales. 3

Comprar bases de datos robadas sin autorización expresa es ilegal, aunque en la práctica el negocio del cibercrimen se retroalimenta con cada compra. 6.

El servicio de vigilancia digital y la Deep Web Como se explicó en el módulo de Blue Team, la vigilancia digital se basa en gran medida en la monitorización automatizada de la Deep Web.

Los scripts que rastrean BreachForums, las páginas de los grupos de ransomware y otras fuentes permiten:
- Detectar en tiempo real si aparece información del cliente en alguna filtración.
- Alertar al cliente antes de que el daño sea irreversible.
- Proporcionar evidencias para la notificación de brecha de datos a la AEPD (obligatoria en
72 horas según el RGPD).

Este es precisamente el tipo de automatización que se construirá a lo largo del máster. 7.

Próxima sesión La siguiente sesión abordará la fase de explotación (la segunda de las cinco fases), con una introducción a las técnicas de OPSEC (Operational Security ), seguida de la escalada de privilegios, la post-explotación y el reporte, completando así el ciclo metodológico completo. 8.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración DIG web / adic web / di web Deep Web – parte no indexada de Internet; accesible sin TOR en su mayor parte DART web Dark Web – subconjunto de la Deep Web accesible solo a través de TOR/proxies; dominio .onion bridge forums / the bridge forums BreachForums – foro principal de la Deep Web para filtración y venta de bases de datos robadas hayden Hidden – referencia a hidden services (servicios ocultos) de la red TOR tor project / tor TOR (The Onion Router) – red y navegador de acceso anónimo a la Deep/Dark Web dac dac go DuckDuckGo – motor de búsqueda sin rastreo, el más usado dentro del navegador TOR de haces / hashet Dehashed – plataforma de búsqueda de credenciales filtradas 4

Término en la transcripción Corrección / Aclaración intelligence ex / inteligencia ex Intelligence X – plataforma de búsqueda de datos e información filtrada loc bit LockBit – grupo de ransomware de alto impacto mundial xss.its XSS.is – foro especializado en hacking ofensivo en la Deep Web carding Carding – fraude mediante clonación y uso ilícito de datos de tarjetas de crédito robadas con vos list Wordlists – diccionarios de contraseñas usados para ataques de fuerza bruta y cracking OPSEC OPSEC (Operational Security ) – técnicas para mantener el anonimato y evitar ser detectado durante una operación obsec OPSEC – misma corrección, variante de transcripción volve Wolf (Academy) – plataforma del máster nodos de salida Exit nodes – últimos nodos de la cadena TOR antes de salir a Internet; los más monitorizados por agencias gubernamentales Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 5



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../MODULO1/resumen_master_clase5.md|resumen_master_clase5]] — IA en Ciberseguridad, Linux, Windows
- [[../../apuntes Andres/23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes.md|23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]] — IA en Ciberseguridad, Linux, Windows
- [[../MODULO3/resumen_master_clase22.md|resumen_master_clase22]] — IA en Ciberseguridad, Linux, Windows
- [[resumen_clase3.md|resumen_clase3]] — IA en Ciberseguridad, Post-Explotación, Windows
- [[../../apuntes Chema/IA/IA — Introducción y VibeCoding.md|IA — Introducción y VibeCoding]] — IA en Ciberseguridad, Linux, Windows
- [[../MODULO3/resumen_master_clase44.md|resumen_master_clase44]] — IA en Ciberseguridad, Linux, Windows

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #blue-team #burpsuite #escalada-privilegios #forense #hydra #ia #linux #post-explotacion #redes #windows #xss
