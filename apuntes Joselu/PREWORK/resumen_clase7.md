> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 7**
> **Módulo:** PREWORK
> **Tema:** Clase 7
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 7. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 7: Ejercicios de Red Team, TIBER-EU y Car Hacking Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: el Red Team como cumbre de la ciberseguridad ofensiva Los ejercicios de Red Team representan la auditoría máxima dentro de la ciberseguridad ofensiva.

A diferencia de un pentesting estándar —que audita activos concretos con alcance limitado—, un ejercicio de Red Team simula un ataque real y completo de un grupo de ciberdelincuentes sin limitaciones iniciales: ingeniería social, intrusiones físicas, robo de equipos, uso de ganzúas, manipulación de cámaras, explotación de vulnerabilidades externas e internas, todo integrado en un único ejercicio.

Combinan todas las auditorías vistas anteriormente (redes internas, externas, web, Wi-Fi, IoT, cloud, bastionado) adaptándose dinámicamente a las circunstancias que surgen durante el ejercicio.

Los ejercicios de Red Team están pensados para organizaciones con un nivel de madurez en ciberseguridad alto y su coste ronda los 150 000 – 250 000 € , con equipos de tres o más perfiles trabajando durante al menos tres meses. 2.

Fases de un ejercicio de Red Team Fase 1 – Reconocimiento amplio (primer mes completo) Es la fase más importante para el éxito del ejercicio.

Se construye un mapa completo de la organización usando:
- OSINT (Open Source Intelligence ): identificación de correos electrónicos, dominios,
subdominios, estructuras organizativas, proveedores, offices geográficas, rangos de red, operador de telecomunicaciones, números de teléfono y perfiles directivos (CEO, CISO, etc.) a suplantar en ingeniería social.
- Reconocimiento técnico : escaneo de puertos y servicios en todos los activos expuestos,
identificación de versiones de software, tecnologías y CVEs asociados.
- Si la organización tiene empresas filiales o pertenece a un holding, todas se convierten en
foco de ataque por la cadena de suministro.
- Especial atención a los portales de acceso remoto (Citrix, Outlook, WPAdmin, VPN,
RDP) como vectores de entrada prioritarios. 1

Fase 2 – Análisis de la superficie de ataque Con la información del reconocimiento se priorizan y categorizan los vectores de entrada:
- Credenciales filtradas en bases de datos públicas y de la dark web (BreachForums, etc.).
- Configuraciones inseguras y accesos remotos expuestos.
- Análisis de las políticas de contraseñas deducibles de las credenciales filtradas para crear
diccionarios personalizados.

### Caso real: compromiso completo de una organización a través de un portal Citrix con credenciales obtenidas por phishing y reutilización de contraseñas no conectadas por LDAP al Active Directory.

Fase 3 – Explotación inicial (acceso a la red interna) Los tres vectores principales para conseguir el acceso inicial son:
- Phishing avanzado / ingeniería social : robo de credenciales para reutilizarlas en
portales corporativos.
- Explotación de vulnerabilidades conocidas : servicios desactualizados identificados en
la fase de reconocimiento.
- Compromiso de proveedores o socios con acceso a la organización (cadena de
suministro).

Fase 4 – Movimiento lateral y escalada de privilegios Una vez dentro de la red interna:
- Escaneo interno para identificar servidores, bases de datos y estaciones de trabajo
administrativas.
- Uso de Mimikatz para volcar credenciales de la memoria RAM de Windows (hashes y
contraseñas en claro de usuarios que se han autenticado en ese equipo).

Los técnicos de sistemas se conectan remotamente a los equipos con cuentas de administrador de dominio, lo que permite obtener credenciales con privilegios de Domain Admin.
- Técnica Pass-the-Hash: reutilizar el hash de una contraseña sin necesidad de conocerla
en claro.
- Creación de backdoors y cuentas ocultas para mantener persistencia y acceso continuo
aunque se detecte alguno de los vectores.

Fase 5 – Exfiltración de datos y simulación del impacto Un Red Team debe demostrar el daño real posible, no solo el acceso:
- Exfiltración de datos críticos usando canales cifrados y protocolos no convencionales
para evadir los controles de seguridad.
- Simulación de ransomware real (controlado): el equipo ha llegado a cifrar empresas
enteras y paralizar su producción durante dos días para demostrar el impacto real y entrenar la respuesta del cliente. 2
- Demostración de la posibilidad de cifrar todos los servidores y exfiltrar datos sensibles
(ej. expedientes de clientes en sector legal).

Fase 6 – Detección, evasión y generación de IOCs
- Se evalúan las capacidades de detección del Blue Team.

Solo el responsable máximo del
cliente sabe que el ejercicio está en curso; los técnicos N1 y N2 actúan con normalidad.
- Se prueban técnicas de evasión contra los EDR, IDS/IPS y firewalls que tenga el cliente.

Lo habitual es montar un laboratorio local con el mismo EDR del cliente para desarrollar técnicas de bypass antes de aplicarlas en el entorno real.
- Al finalizar el ejercicio se generan IOCs (Indicators of Compromise ) para que el Blue
Team pueda detectar esas mismas técnicas en el futuro. 3.

Assumed Breach: la brecha asumida Cuando tras semanas o meses de intentos el acceso externo resulta imposible (organización con medidas de seguridad muy maduras), se propone el escenario Assumed Breach: se asume que la brecha ya se produjo (por insider, phishing exitoso, descarga accidental de malware) y se continúa la auditoría desde dentro.

### Caso real: en una comunidad autónoma del sector sanitario con accesos protegidos por certificado digital en tarjeta física, el equipo no logró penetrar externamente en dos meses.

Se intentó robar una tarjeta de empleado (sin éxito), se comprometió parcialmente la red Wi-Fi pero estaba correctamente segmentada.

Se propuso el Assumed Breach.

Otro caso real: en una empresa de Barcelona, cinco miembros del equipo entraron físicamente a las instalaciones, conectaron una Raspberry Pi a una toma RJ45 plataformada con un agente de comunicación, obteniendo acceso a la red interna.

Finalmente escaparon del sandbox bastionado a través de Internet Explorer para escalar privilegios y comprometer el Active Directory. 4.

Ejercicios TIBER-EU ¿Qué es TIBER-EU?

TIBER-EU (Threat Intelligence Based Ethical Red Teaming ) es un marco creado por el Banco Central Europeo (BCE) para evaluar y mejorar la resiliencia cibernética de las entidades financieras críticas.

Es la primera normativa que obliga por ley a realizar este tipo de ejercicio al menos una vez al año, impulsada por la entrada en vigor de DORA (normativa de resiliencia digital para banca y seguros). 3

Diferencias clave con un Red Team estándar Aspecto Red Team avanzado TIBER-EU Equipos Red Team + Blue Team (no informado)Red Team + Blue Team (parcial) + White Team Duración 3-6 meses 6-12 meses Perfiles 3-5 Hasta 6+ Reconocimiento Lo hace el Red Team (1 mes) Lo proporciona el White Team Obligatoriedad V oluntario Obligatorio por DORA Sector Cualquier empresa madura Exclusivamente banca y seguros El White Team es un comité compuesto por un delegado del Red Team, un delegado del cliente y un delegado del Blue Team.

Actúa como coordinador: el Red Team no pierde tiempo en reconocimiento (el cliente proporciona toda su superficie de exposición) y puede reinvertirlo en buscar zero-days en las tecnologías del cliente.

### Caso real: en un ejercicio TIBER-EU (simulado sobre Repsol como ejemplo), el equipo investigó el gateway de Fortinet que usaba el cliente, adquirieron el mismo hardware, hicieron reversing del firmware, descubrieron una vulnerabilidad de 0-day y la usaron como vector de entrada.

Esto generó además un CVE publicable.

Características principales
- Los ejercicios se basan en Threat Intelligence real: el cliente proporciona su panorama
de amenazas y los activos más críticos.
- Se simulan ataques de APTs (Advanced Persistent Threats ) reales con TTPs ( Tactics,
Techniques and Procedures ) documentados.
- Objetivos concretos: acceso a sistemas de pago, exfiltración de datos sensibles,
interrupción de operaciones.
- Obligatoriamente ejecutados por equipos externos, para garantizar la independencia del
informe sellado. 5.

Car Hacking Por qué el car hacking es una línea de futuro Los vehículos modernos son esencialmente pequeñas empresas digitales con una red interna de sensores, centralitas, sistemas de entretenimiento, comunicaciones inalámbricas y servicios cloud.

A partir de 2025 se prevé la obligatoriedad de un certificado de ciberseguridad para nuevos modelos de vehículo, lo que hace del car hacking una especialización con gran proyección laboral. 4

Componentes y vectores de ataque principales Redes internas del vehículo (CAN Bus): El CAN Bus (Controller Area Network ) es el bus de datos que conecta todos los módulos de control del vehículo (centralitas, sensores, frenos, acelerador).

Al ser mayoritariamente no cifrado, es posible:
- Sniffing: interceptar los códigos que envían los sensores (ej. código de aceleración, de
frenado) y analizarlos.
- Inyección de mensajes : una vez conocidos los códigos, inyectarlos directamente en el
bus para controlar funciones críticas (frenar, acelerar, mover retrovisores).

### Caso real: inyección de un parámetro de presión de neumático a 0 en un Tesla forzando el frenado de emergencia automático; freno en seco de un Jaguar a 200 km/h en una pista de aterrizaje.

- Falta de segmentación entre el sistema de infotainment (entretenimiento) y el CAN Bus:
a través de la pantalla de los niños viendo Peppa Pig en el asiento trasero podría llegarse al bus de datos del vehículo.

Caso real documentado: hacker conectó un USB a la pantalla de entretenimiento de un avión y comprometió el resto de la red del aparato.
- Las ECUs (Electronic Control Units , centralitas) son los puntos de control de cada
sistema mecánico-electrónico del vehículo.

Interfaces externas y comunicaciones inalámbricas:
- Bluetooth: protocolo muy vulnerable.

Ataques como BlueBorne (RCE via Bluetooth).

Investigación de Tarlogic (empresa española): RCE crítico mediante Bluetooth que podría afectar a cualquier vehículo del mercado.

El profesor desarrolló su TFG sobre hacking al protocolo Bluetooth.
- Radio / llaves de apertura : clonación de la frecuencia de radio de la llave con un
Flipper Zero o una antena SDR.

### Caso documentado: robo de BMWs en Alemania con esta técnica.

Apertura y cierre de la tapa de carga de Teslas en movimiento por la carretera.
- USB y puertos físicos : cargar malware para Android (que usan todos los navegadores de
a bordo) y obtener acceso completo.
- Telemática y apps móviles (Mercedes Me, Tesla app, BMW Connected): la
comunicación permanente vía 4G/LTE entre el vehículo y la nube es un vector de acceso remoto.

Atacando la app o la API se puede controlar el vehículo.
- OTA (Over-the-Air updates ): actualizaciones de firmware que si no están correctamente
firmadas pueden ser interceptadas con un ataque Man-in-the-Middle e inyectar una versión de firmware modificada con backdoor.

Sensores y sistemas ADAS: Los vehículos autónomos o con sistemas de asistencia avanzada (ADAS) dependen de cámaras, LIDAR, radar y ultrasonidos.

Es posible falsificar sus lecturas (ej. emitir ondas que engañen al sensor de aparcamiento haciéndole creer que hay un obstáculo constante), lo que puede provocar decisiones de control incorrectas. 5

## 6.

Cierre: resumen de auditorías del Red Team El profesor hace balance de las diez tipologías cubiertas en el módulo de Red Team: 1.Auditoría de redes internas 2.Auditoría de redes externas 3.Auditoría de aplicaciones web 4.Auditoría de código 5.Auditoría de redes Wi-Fi 6.Auditorías IoT 7.Auditorías Cloud 8.Bastionado 9.Ejercicios de Red Team avanzado y TIBER-EU 10.Car Hacking La siguiente sesión se dedicará al Blue Team (arquitecturas seguras, monitorización 24/7, normativa) y al Purple Team (forense, DevSecOps, respuesta a incidentes). 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración auditorio de ciberseguridad Auditor de ciberseguridad CVs CVEs (Common Vulnerabilities and Exposures) – identificadores de vulnerabilidades Mimikatz Mimikatz – herramienta correcta; extrae credenciales y hashes de la memoria de Windows pass de hash Pass-the-Hash – técnica de reutilización de hashes de contraseñas sin conocerlas en claro Active Domain Admits Active Directory Domain Admins – administradores de dominio en Active Directory IOCs IOCs (Indicators of Compromise ) – indicadores de compromiso para detección futura tiberego / tiberiu / tiber.eu TIBER-EU – marco del BCE para pruebas de ciberresiliencia en banca y seguros Assummed Bridge / Bridge Asylum Assumed Breach – escenario en que se asume que el atacante ya tiene acceso inicial summit bridge Assumed Breach – mismo concepto C4G / Log4G Log4Shell / Log4j – vulnerabilidad crítica en librería Java APTs APTs (Advanced Persistent Threats ) – grupos 6

Término en la transcripción Corrección / Aclaración de atacantes avanzados y persistentes TTPs TTPs (Tactics, Techniques and Procedures ) – tácticas, técnicas y procedimientos de los atacantes CAN Bus / Cambus CAN Bus (Controller Area Network ) – bus de datos interno del vehículo ECUs / EQUUS ECUs (Electronic Control Units ) – centralitas electrónicas del vehículo ADAS ADAS (Advanced Driver Assistance Systems ) – sistemas avanzados de asistencia a la conducción OTA OTA (Over-the-Air) – actualizaciones remotas de firmware en vehículos OBD2 OBD2 (On-Board Diagnostics II ) – puerto de diagnóstico estándar de los vehículos fliper 0 Flipper Zero – dispositivo de hacking de radiofrecuencia y protocolos inalámbricos Blueborn BlueBorne – ataque de RCE a través del protocolo Bluetooth Bluetooth BLE Bluetooth Low Energy (BLE) – versión de Bluetooth optimizada para IoT sniping / snifar Sniffing – captura y análisis de tráfico de red o bus de datos fuzzing de protocolos Protocol Fuzzing – técnica de inyección de datos malformados para encontrar vulnerabilidades reversing Reverse Engineering – ingeniería inversa de software o firmware EDR EDR (Endpoint Detection and Response ) – solución de seguridad en endpoints Tarlogic Tarlogic – empresa española de ciberseguridad destacada en Red Team Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 7



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_clase2.md|resumen_clase2]] — IA en Ciberseguridad, Metasploit, Windows
- [[resumen_clase6.md|resumen_clase6]] — IA en Ciberseguridad, Metasploit, Windows
- [[../MODULO1/resumen_master_clase2.md|resumen_master_clase2]] — IA en Ciberseguridad, Metasploit, Windows
- [[../MODULO1/resumen_master_clase5.md|resumen_master_clase5]] — IA en Ciberseguridad, Metasploit, Windows
- [[../MODULO1/resumen_master_clase6.md|resumen_master_clase6]] — IA en Ciberseguridad, Nmap, OSINT
- [[../MODULO2/resumen_master_clase9.md|resumen_master_clase9]] — IA en Ciberseguridad, OSINT, Windows

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #blue-team #command-injection #escalada-privilegios #forense #ia #metasploit #netcat #nmap #normativa #osint #post-explotacion #redes #reverse-shell #windows
