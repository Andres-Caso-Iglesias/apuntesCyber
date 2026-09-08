> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 4**
> **Módulo:** PREWORK
> **Tema:** Clase 4
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 4. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 4: Auditorías de Redes Externas Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: las auditorías de redes externas Tras repasar las redes internas —“la reina” de las auditorías— la sesión se centra en las auditorías de redes externas , consideradas la segunda tipología más importante.

Su objetivo es evaluar todos los activos de una organización que están expuestos a internet, detectar vulnerabilidades y reducir la superficie de ataque visible desde el exterior.

Por naturaleza son auditorías de caja negra: el auditor no recibe información previa y debe descubrir por sí mismo toda la superficie de exposición, replicando el comportamiento de un atacante real.

Sin embargo, existe una variante híbrida muy utilizada en la práctica: comenzar con una fase de caja negra (enumeración propia) y posteriormente contrastar y completar los hallazgos con el cliente (pasando a caja gris), de modo que ningún activo quede sin revisar. 2.

Por qué las empresas no conocen su propia superficie de exposición Uno de los hallazgos más frecuentes en este tipo de auditorías es que las propias organizaciones desconocen qué tienen expuesto a internet.

Las causas más habituales son:
- Alta rotación de personal en los equipos de IT sin transferencia de conocimiento.
- Subdominios de preproducción y entornos de testing que se crearon para un desarrollo
puntual y nunca se dieron de baja.

El profesor menciona haber encontrado servidores olvidados activos en internet 20 años después de su despliegue.
- Falta de inventario actualizado de activos digitales.

La auditoría externa, por tanto, no solo detecta vulnerabilidades, sino que también proporciona al cliente un inventario real y completo de sus activos expuestos. 3. ¿Qué abarca una auditoría de redes externas?

Los cuatro bloques principales son: Superficie de exposición: todos los servicios y sistemas accesibles públicamente.

Un mismo servidor puede exponer múltiples tecnologías a través de diferentes puertos, cada una con sus propias vulnerabilidades.

Las aplicaciones web, aunque forman parte de la superficie, tienen su 1

propia línea de auditoría y normalmente quedan fuera del alcance de una auditoría de redes externas salvo petición expresa del cliente.

Vulnerabilidades en dispositivos: versiones obsoletas de software, configuraciones débiles, accesos predeterminados y dispositivos sin soporte (routers, cámaras IoT, etc.).

### Credenciales comprometidas: verificación de si existen credenciales de empleados o sistemas filtradas en bases de datos de la dark web, y si siguen siendo válidas.

Seguridad de las comunicaciones: evaluación de protocolos de cifrado y configuraciones web (por ejemplo, uso de HTTP en lugar de HTTPS, cabeceras de seguridad ausentes, ausencia de doble factor de autenticación). 4.

Metodología de la auditoría de redes externas Al igual que en toda auditoría de pentesting, las fases son siempre las mismas: Fase 1 – Reconocimiento y enumeración (fingerprinting) El auditor identifica y categoriza todos los activos expuestos ligados al dominio o a la organización objetivo.

La información que se puede obtener incluye: subdominios, páginas web y sus directorios, usuarios y correos electrónicos, contraseñas filtradas, rangos de IP, CDN y servicios de terceros relacionados.

> [!important] ### Herramientas clave:

- Shodan (shodan.io): motor de búsqueda de dispositivos conectados a internet.

Permite
buscar por tecnología, versión de software, sistema operativo o protocolo, y devuelve la IP y los CVEs asociados.

### Ejemplo real: búsqueda de “Windows Server 2008 R2” devuelve más de 321 000 servidores en todo el mundo aún expuestos y vulnerables a EternalBlue, 7 años después de WannaCry.

- Censys (censys.io): similar a Shodan pero con mejor rendimiento en búsquedas por
nombre de organización o dominio.

En la demostración con Repsol, Censys encontró más de 3 000 activos frente a los 16 de Shodan, lo que ilustra que ambas herramientas son complementarias y deben usarse en paralelo.
- Nmap: escaneo activo de puertos y servicios en los activos identificados.
- Google Dorking: búsquedas avanzadas en Google para encontrar información sensible
indexada públicamente.

Puertos y servicios más relevantes a identificar: Puerto Protocolo/Servicio 80 HTTP 443 HTTPS 21 FTP 22 SSH 2

Puerto Protocolo/Servicio 3389 RDP (Remote Desktop Protocol) 445 SMB / Samba 1433 / 3306 SQL Server / MariaDB Los portales de acceso remoto (RDP, SSH, VPN, Citrix, TeamViewer) son la prioridad absoluta en la categorización de activos, ya que representan la vía más directa hacia la red interna.

Fase 2 – Detección de vulnerabilidades Con la superficie de exposición definida, se utilizan escáneres automatizados (Nessus, OpenV AS, Qualys) para detectar vulnerabilidades conocidas en versiones de software desactualizadas y configuraciones débiles.

Al igual que en las auditorías internas, los falsos positivos deben validarse manualmente, priorizando las vulnerabilidades críticas y altas.

Fase 3 – Verificación de credenciales filtradas Se consultan bases de datos de credenciales robadas (accesibles por unos pocos euros al mes) para comprobar si existen credenciales vigentes asociadas a la organización objetivo.

El valor de estas credenciales va más allá del acceso directo:
- Revelan la política de contraseñas implícita de la organización (longitud, uso de
mayúsculas, números, símbolos).
- Permiten crear diccionarios personalizados para ataques de fuerza bruta.

Si se encuentra
“Empresa2023”, es altamente probable que exista “Empresa2024”; si hay “Noviembre2024”, puede existir “Diciembre2024”.
- Cualquier contraseña inferior a 12 caracteres sin combinación de mayúsculas,
minúsculas, números y símbolos puede romperse en menos de 30 segundos con un servidor de cracking moderno.

### Aviso legal: el uso de estas bases de datos requiere autorización expresa y firmada por el cliente.

Utilizarlas sin permiso para acceder a cuentas de terceros es ilegal y conlleva penas de prisión.

Fase 4 – Evaluación de la seguridad de las comunicaciones Se analizan los protocolos de cifrado y las configuraciones web.

Un sitio que funciona en HTTP (sin cifrado) es vulnerable a ataques de Man-in-the-Middle (MitM) , lo que permite interceptar credenciales en tránsito.

La ausencia de cabeceras de seguridad básicas o de doble factor de autenticación (2FA) son indicadores de una postura de seguridad deficiente en toda la organización.

Fase 5 – Explotación controlada y reporte Se explotan de forma controlada las vulnerabilidades verificadas para demostrar su impacto real al cliente.

Se elabora un informe técnico y ejecutivo con los hallazgos confirmados, su criticidad y las recomendaciones de remediación. 3

## 5.

La cadena de terceros como vector de ataque Al enumerar los activos de una organización con herramientas como Censys o Shodan, también se descubren los proveedores y partners tecnológicos (CDN, servicios cloud, proveedores de seguridad).

Tal y como se vio en la demostración con Repsol, donde aparecían Telefónica, Akamai y Microsoft como terceros asociados, cualquiera de estos proveedores con acceso a la infraestructura del objetivo puede ser el punto de entrada para un ataque de cadena de suministro. 6.

Diferencias clave entre auditorías externas e internas Aspecto Auditoría interna Auditoría externa Tipo de caja Gris (acceso VPN inicial) Negra (sin información previa) Enfoque principal Active Directory, Kerberos, SMBSuperficie de exposición en internet Punto de partida Dentro de la red corporativa Desde internet, como un atacante externo Herramientas clave BloodHound, Responder, NmapShodan, Censys, Nmap, Google Dorking Mayor riesgo detectado Configuración del AD, escalada de privilegiosServicios con versiones obsoletas, credenciales filtradas 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración census / censis search Censys – motor de búsqueda de activos expuestos en internet en el map Nmap – herramienta de escaneo de puertos y servicios CVS CVE (Common Vulnerabilities and Exposures) – identificador estándar de vulnerabilidades OpenBus OpenV AS – escáner de vulnerabilidades de código abierto money in the middle Man-in-the-Middle (MitM) – ataque de interceptación de comunicaciones VPNs propagativas Probablemente VPNs corporativas o soluciones como Pulse Secure / GlobalProtect NIDS, 10Bware TeamViewer / AnyDesk – herramientas de acceso remoto corporativo shonan Shodan – motor de búsqueda de dispositivos 4

Término en la transcripción Corrección / Aclaración conectados a internet mariade ve MariaDB – sistema de gestión de bases de datos poc PoC (Proof of Concept) – prueba de concepto de explotación de una vulnerabilidad google docking Google Dorking – uso de operadores avanzados de Google para encontrar información sensible 4.4.3 / HTTPS Puerto 443 – HTTPS 3.3.8.9 / RDP Puerto 3389 – RDP (Remote Desktop Protocol) Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 5


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Anonimato e Ingeniería Social.md|Anonimato e Ingeniería Social]] — Hydra, IA en Ciberseguridad, SSH
- [[../../Apuntes/comandos/Hydra.md|Hydra]] — Hydra, SSH, Windows
- [[../../transcripciones/Julio/15.07.2026 IA Introducción y Vibe Coding.md|15.07.2026 IA Introducción y Vibe Coding]] — Hydra, SSH, Windows
- [[../../apuntes Chema/Repaso General II.md|Repaso General II]] — Hydra, SSH, Windows
- [[resumen_clase14.md|resumen_clase14]] — IA en Ciberseguridad, Nmap, Windows
- [[../MODULO2/resumen_master_clase11.md|resumen_master_clase11]] — IA en Ciberseguridad, Nmap, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

> #escalada-privilegios #hydra #ia #nmap #osint #pentest #redes #ssh #windows
