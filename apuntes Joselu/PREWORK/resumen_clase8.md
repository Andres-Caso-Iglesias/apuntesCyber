> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 8**
> **Módulo:** PREWORK
> **Tema:** Clase 8
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 8. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 8: Blue Team – Arquitecturas Seguras y Monitorización SOC 24/7 Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción al Blue Team El Blue Team es el equipo encargado de la defensa dentro de una organización.

Su función principal es proteger sistemas, redes, aplicaciones y datos frente a ciberamenazas.

Este servicio puede ofrecerse de forma interna o como servicio externo a través de consultoras (Deloitte, PwC, Big Four u otras empresas de nicho que suelen ofrecer servicios más especializados).

Una reflexión importante del profesor: comenzar la carrera en Blue Team (concretamente en un SOC como N1) lejos de ser un paso atrás, es uno de los mejores aprendizajes posibles para un futuro pentester, ya que permite entender en detalle cómo se defienden las organizaciones, qué se monitoriza y cómo reaccionan ante los ataques, conocimiento imprescindible para después romper esas defensas.

Ramas principales del Blue Team
- Arquitecturas seguras (on-premise y cloud)
- Monitorización 24/7 / SOC (Security Operations Center )
- Vigilancia digital (tratada en la siguiente sesión)
- Normativa y cumplimiento
- Respuesta ante incidentes (DeFIR, tratada en la sesión de Purple Team)
PARTE I: Arquitecturas Seguras 2. ¿Qué es una arquitectura segura?

Una arquitectura segura es el diseño estructural de sistemas, redes y aplicaciones que integra los principios de ciberseguridad desde su concepción ( security by design).

No se trata solo de añadir seguridad a lo ya construido, sino de planificarla desde el inicio para que cualquier cambio posterior sea menos costoso y no genere nuevas vulnerabilidades.

Actualmente, muchas empresas aprovechan las migraciones a cloud para rediseñar completamente su arquitectura con enfoque Zero Trust, cumpliendo al mismo tiempo con normativas como ISO 27001, NIS 2 o el ENS. 1

## 3.

Cuándo es necesario el servicio de arquitecturas seguras
- Diseño de nuevos sistemas : cualquier nueva plataforma, red, aplicación o activo debe
integrarse de forma segura desde el inicio.
- Transformación digital : migración a cloud, adopción de Docker, microservicios, etc.
- Corrección tras una auditoría : cuando una auditoría detecta vulnerabilidades, las
correcciones deben realizarse siguiendo criterios de arquitectura segura y verificarse con una nueva auditoría.
- Cumplimiento normativo : las regulaciones exigen controles específicos de seguridad.
- Sectores críticos: banca, salud e industria, donde un ciberataque puede tener impacto
crítico. 4.

Pilares de una arquitectura segura Seguridad por diseño (Security by Design): la seguridad se incorpora desde las etapas iniciales.

Se basa en tres principios:
- Mínimo privilegio : cada usuario, sistema o proceso tiene solo los permisos estrictamente
necesarios.

Caso habitual en auditorías: encontrar 9-15 cuentas de Domain Admin cuando debería haber 1-2 como máximo.
- Zero Trust (Confianza Cero) : no confiar automáticamente en nada ni en nadie, dentro ni
fuera de la red.

Se verifica constantemente la identidad y el contexto de cada acceso.

En la práctica se implementa mediante Kerberos, que autentica y autoriza los accesos a todos los servicios sin requerir una contraseña nueva en cada uno.
- Defense in Depth (Defensa en profundidad) : múltiples capas de seguridad superpuestas
para proteger los activos.

Si una capa falla, las siguientes contienen el ataque.

Segmentación de red y control de accesos: - Dividir la red en zonas aisladas (usuarios, servidores críticos, servidores IoT, red legacy, DMZ) para limitar el impacto de un ataque.

Un ransomware bien contenido por segmentación no se propaga al resto de la infraestructura ni a los servidores de backup. - Implementar controles de autenticación robustos: doble factor de autenticación (MFA) y políticas de autorización basadas en roles.

Protección de datos: - Cifrado de datos en tránsito y en reposo con algoritmos robustos y vigentes: AES-256 y TLS 1.2 / 1.3. - Algoritmos obsoletos e inseguros que no deben usarse: MD5, DES, CBC (en configuraciones débiles).

Tener las contraseñas cifradas con MD5 es equivalente a tenerlas en texto claro, ya que se rompe en segundos. - Clasificación y etiquetado de datos sensibles según la normativa aplicable (ej.

PCI DSS exige protección específica para datos de tarjetas: nombre, número, fecha de caducidad y CVV).

Seguridad en el perímetro: - Firewalls: el servicio mejor pagado y peor configurado según el profesor.

Solo debería modificarlos el perfil especializado.

Configuración óptima en modo whitelist (todo bloqueado por defecto, solo se permite lo necesario). - IDS/IPS (Intrusion Detection/Prevention Systems ): monitorización y bloqueo de accesos no autorizados. - Balanceadores de carga : para mitigar ataques DDoS distribuyendo el tráfico. - VPN y portales seguros (Citrix, etc.): para acceso remoto seguro.

### Caso real: compromiso completo de la infraestructura interna de un cliente a través de un portal Citrix mal configurado que permitía 2

reutilización de credenciales. - SIEM + EDR: centralización y análisis de logs para detección de amenazas en tiempo real. - SOAR (Security Orchestration, Automation and Response ): automatización de la respuesta a incidentes.

Detecta comportamientos anómalos y activa respuestas automáticas (ej. bloquear una IP en el firewall).

PARTE II: Monitorización SOC 24/7 5. ¿Qué es el SOC?

El SOC (Security Operations Center ) es un centro especializado en ciberseguridad que combina herramientas avanzadas, procesos definidos y personal capacitado para monitorizar, detectar, responder y prevenir incidentes de seguridad en tiempo real.

Existen dos modalidades: - SOC 24/7: vigilancia los 365 días del año a cualquier hora. - SOC 8x5: solo en horario laboral de lunes a viernes.

Las fuentes de datos que analiza un SOC incluyen: endpoints (equipos de trabajo de cada empleado), dispositivos IoT, aplicaciones internas y externas, logs de todos los servidores y trazabilidad de patrones de comportamiento de la organización.

No basta con monitorizar solo el perímetro externo: es fundamental monitorizar también el interior (Assumed Breach). 6.

Los tres perfiles del SOC: N1, N2 y N3 Perfil N1 – Analista Junior: Perfil de inicio, sin experiencia previa.

Gestiona el mayor volumen de alertas siguiendo hojas de ruta (playbooks) predefinidas para cada tipo de incidente.

Actúa como filtro: analiza la alerta, aplica el procedimiento establecido y la eleva si supera su nivel.

Aunque el trabajo parece mecánico, proporciona una visibilidad enorme sobre los patrones de ataque reales (qué IPs atacan, qué técnicas usan, qué formularios web son objetivos frecuentes de SQL Injection, etc.).

Perfil N2 – Analista Senior: Perfil más autónomo.

No solo sigue el playbook sino que actúa directamente sobre las tecnologías: configura reglas en firewalls (Fortinet, Palo Alto, Check Point, Microsoft Defender), bloquea geolocalizaciones, investiga alertas complejas.

Trabaja directamente con la tecnología de seguridad, lo que le da un conocimiento muy valioso para el hacking ofensivo posterior (quien sabe configurar y desactivar un Fortinet sabe cómo atacarlo).

Perfil N3 – Experto / Respuesta ante Incidentes: El nivel más alto.

Perfil híbrido ofensivo- defensivo-forense con varios años de experiencia.

Se activa en casos de ransomware o compromisos graves.

Gestiona la contención, remediación y recuperación del incidente, interpreta los hallazgos forenses y trabaja contra el reloj (guardias 24/7, desplazamientos urgentes).

El profesor describe haber tenido que leer 14 millones de líneas de logs durante una semana en un caso forense. 3

## 7.

Ciclo operativo del SOC El SOC funciona en cuatro fases continuas: Monitorización: recopilación y análisis en tiempo real de datos de todas las fuentes (red, endpoints, aplicaciones, logs).

Las sondas de red capturan todo el tráfico y lo filtran con reglas e inteligencia artificial.

Herramienta de referencia para análisis de paquetes: Wireshark.

El dato bruto no tiene valor por sí solo: debe ser tratado y correlacionado para generar información útil.

Detección avanzada (Threat Intelligence): - Análisis de comportamiento: identificar actividades inusuales (ej. un archivo llamado “esto_no_es_un_virus.exe” creado en una carpeta temporal del sistema activa inmediatamente un IOC). - Correlación de eventos: relacionar múltiples datos para detectar patrones complejos de ataque que individualmente parecen inofensivos. - IA y Machine Learning : automatización de la detección de anomalías mediante modelos entrenados con datos históricos.

Permite reducir la carga de trabajo de los perfiles N1 y N2, liberándolos para tareas que requieren criterio humano experto.

### Herramientas relacionadas: NDR (Network Detection and Response ), UEBA (User and Entity Behavior Analytics ).

Respuesta: activación de procedimientos de contención (bloqueo de IPs, desconexión de dispositivos comprometidos, suspensión de cuentas), remediación (eliminación del malware, reparación de vulnerabilidades) y recuperación (restauración segura desde backup verificando previamente que el malware no persiste en ningún servidor).

Prevención: análisis de tendencias y patrones para mejorar defensas y reducir riesgos futuros.

Es la fase ideal: cuanto mejor sea la prevención, menos respuesta será necesaria.

Implementación de nuevos IOCs, reglas de firewall, arquitecturas mejoradas, formación de usuarios. 8.

Reporting y métricas del SOC El SOC proporciona informes mensuales que incluyen: alertas detectadas y su resolución, vulnerabilidades recurrentes con recomendaciones y KPIs (Key Performance Indicators ) como los SLAs (Service Level Agreements ), que son los tiempos límite de actuación comprometidos contractualmente.

Herramienta habitual de visualización: Kibana, que permite al cliente acceder a su panel de estado de seguridad en tiempo real. 9.

### Próxima sesión: Vigilancia Digital La siguiente sesión cubrirá la vigilancia digital, línea del Blue Team orientada a la monitorización de amenazas externas en internet, la dark web y foros de ciberdelincuentes.

Es el equipo que, en los ejercicios TIBER-EU, proporciona al Red Team toda la superficie de exposición de la organización. 4

## 10.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración Loitek / Pemegé Deloitte y PwC – consultoras de ciberseguridad (Big Four) shock / soc SOC (Security Operations Center ) – centro de operaciones de seguridad white shark Wireshark – herramienta de análisis de paquetes de red soars SOAR (Security Orchestration, Automation and Response) – automatización de respuesta a incidentes street intelligence Threat Intelligence – inteligencia de amenazas si en edr / si en soar SIEM (Security Information and Event Management) + EDR (Endpoint Detection and Response) ndr sensi mc en ips NDR (Network Detection and Response ), UEBA, IPS – tecnologías de detección de red gerberos / que veros Kerberos – protocolo de autenticación en redes corporativas Kibana Kibana – plataforma de visualización de datos y logs (parte del stack ELK) capéis / capeis KPIs (Key Performance Indicators ) – indicadores clave de rendimiento s la / sla SLA (Service Level Agreement ) – acuerdo de nivel de servicio / tiempo límite de actuación ae 256 AES-256 – algoritmo de cifrado simétrico estándar teles 1.2 o 1.3 TLS 1.2 / TLS 1.3 – protocolos de cifrado de comunicaciones jaseo Hashing – función de resumen criptográfico (ej.

SHA-256) ids y vps IDS/IPS (Intrusion Detection/Prevention Systems) – sistemas de detección y prevención de intrusiones dmc / DMZ DMZ (Demilitarized Zone ) – zona desmilitarizada, segmento de red entre internet y la red interna dockers Docker – plataforma de contenedores para despliegue de aplicaciones on premio / un premio On-premise – infraestructura tecnológica alojada en las instalaciones propias de la empresa pc y dss PCI DSS (Payment Card Industry Data Security Standard) – norma de seguridad para 5

Término en la transcripción Corrección / Aclaración datos de tarjetas n map Nmap – herramienta de escaneo de puertos y servicios Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../MODULO3/resumen_master_clase18.md|resumen_master_clase18]] — Forense Digital, Normativa / GRC, SQL Injection
- [[../MODULO3/resumen_master_clase22.md|resumen_master_clase22]] — Blue Team / SOC, Forense Digital, Wireshark
- [[../../apuntes evolve/BLOQUE 13.md|BLOQUE 13]] — Blue Team / SOC, IA en Ciberseguridad, Normativa / GRC
- [[resumen_clase3.md|resumen_clase3]] — Blue Team / SOC, Forense Digital, Normativa / GRC
- [[../../README.md|README]] — Forense Digital, Normativa / GRC, SQL Injection
- [[../MODULO2/resumen_master_clase16.md|resumen_master_clase16]] — Blue Team / SOC, Forense Digital, SQL Injection

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #blue-team #forense #ia #nmap #normativa #redes #sqli #wireshark
