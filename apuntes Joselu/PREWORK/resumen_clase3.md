> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 3**
> **Módulo:** PREWORK
> **Tema:** Clase 3
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 3. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 3: Líneas de Ciberseguridad y Auditorías de Redes Internas Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: los tres equipos de ciberseguridad La ciberseguridad profesional se organiza en torno a tres grandes equipos: Red Team (equipo ofensivo): realiza ataques controlados contra la infraestructura del cliente para detectar vulnerabilidades, intentar acceder a la red interna, exfiltrar datos o comprometer el controlador de dominio.

Blue Team (equipo defensivo): securiza los activos de la organización, implementa barreras de protección y corrige las vulnerabilidades que el Red Team detecta.

Purple Team: combina competencias ofensivas y defensivas.

Tiene menos especialización en cada área, pero resulta idóneo para roles como el equipo forense, la respuesta ante incidentes (DeFIR), DevSecOps y formación.

El profesor defiende que los mejores perfiles forenses provienen de equipos ofensivos, porque conocen de primera mano la metodología de los atacantes y sus técnicas de ocultación.

La colaboración Red Team – Blue Team genera un modelo de cross-selling: una auditoría detecta vulnerabilidades (Red) y abre la venta de un servicio de remediación (Blue), y viceversa. 2.

Servicios y tipologías de auditoría Red Team (más de 21 servicios) Los siete principales tratados en la sesión son: 1.Auditorías de redes internas 2.Auditorías de redes externas 3.Auditorías de aplicaciones web 4.Auditorías de redes Wi-Fi / inalámbricas 5.Ejercicios de Red Team avanzado 6.Ejercicios TIBER-EU (marco europeo para banca y aseguradoras, ligado a la normativa DORA) 7.Auditorías de car hacking (vehículos conectados) Otros servicios: auditorías de dispositivos IoT, frecuencias de radio (Airfeed), Bluetooth, 1

comunicaciones satelitales (Satcom) y energías renovables.

Blue Team
- Arquitecturas seguras (modelo Zero Trust)
- Monitorización 24/7 y resolución de tickets (SOC)
- Vigilancia digital y gestión de vulnerabilidades
- Normativa y cumplimiento: ISO/IEC 27001, ENS, DORA, SOC 2, NIS 2, framework
NIST, GDPR, continuidad de negocio Purple Team
- DeFIR: equipo de respuesta ante incidentes y forense
- Formación
- DevSecOps (desarrollo seguro)

## 3.

El perfil del hacker ético: demanda y características Los perfiles de hacking ético son los más demandados del sector por el alto nivel técnico requerido y la necesidad de formación continua diaria (lectura de vulnerabilidades, práctica en laboratorios, investigación de zero-days, certificaciones).

Es una disciplina que no termina con la jornada laboral: es una forma de vida.

Se valora especialmente al profesional que combina sólido nivel técnico con capacidad de gestión (cliente, proyecto, comunicación ejecutiva), ya que los clientes suelen ser directivos no técnicos que necesitan entender los resultados sin tecnicismos.

La certificación de entrada recomendada es la eJPT v2 (eLearnSecurity Junior Penetration Tester), objetivo final del máster, que permite acceder directamente a equipos de Red Team. 4.

Tipos de auditoría según el nivel de información (las “cajas”) Toda auditoría se clasifica en función del conocimiento previo que el auditor tiene del objetivo: Tipo Información disponible Ejemplo típico Caja negra Ninguna.

El auditor obtiene la superficie de ataque por sí mismoAuditorías externas Caja gris Parcial.

Se proporciona un acceso inicial pero no información completaAuditorías de redes internas Caja blanca Completa.

El cliente facilita accesos, listas de usuarios y Campañas de phishing controlado, auditorías de 2

Tipo Información disponible Ejemplo típico configuraciones configuraciones Las auditorías de redes internas son el ejemplo paradigmático de caja gris: se entrega acceso VPN a un equipo de la organización simulando un escenario de breach assume (se asume que ya existe una brecha inicial) y se evalúa hasta dónde podría llegar un atacante real. 5.

Auditorías de redes internas: la “reina” de las auditorías ¿Qué es el Active Directory (Directorio Activo)?

El Active Directory (AD) es el sistema centralizado de gestión de una organización: controla usuarios, grupos, políticas, contraseñas, permisos y toda la infraestructura IT.

Comprometer el AD equivale a comprometer toda la empresa, ya que contiene credenciales, accesos a cuentas bancarias, tickets y datos críticos.

Objetivos de la auditoría de redes internas
- Detectar fallos de configuración en el Active Directory.
- Verificar la política de contraseñas (mínimo 12 caracteres alfanuméricos con caracteres
especiales, cambio cada 30 días, sin repetición del último año).
- Evaluar protocolos como Kerberos, LDAP y Samba (SMB, puertos 445, 135 y 138).
- Identificar equipos con software obsoleto (legacy) o vulnerabilidades conocidas (ej.

EternalBlue en Windows Server 2003/2008 R2).
- Revisar las GPO (Group Policy Objects): políticas de grupo aplicadas a los objetos del
Active Directory.
- Comprobar permisos de carpetas compartidas para evitar escaladas de privilegios.

Técnicas y herramientas principales
- Nmap: escaneo de puertos y servicios en la red.
- BloodHound: mapeo del Active Directory y análisis de rutas de ataque.
- Nessus, OpenV AS, Qualys : escáneres automatizados de vulnerabilidades.
- Pentera: herramienta automatizada de auditoría de Active Directory (licencia ~500 000
€/año; solo rentable en organizaciones de más de 20 000 empleados).
- Responder: herramienta para capturar hashes de autenticación NTLM a través de
LLMNR/NBT-NS.
- MAC Spoofing / MAC Flooding : técnicas de suplantación y saturación de tablas
ARP/CAM en la red local.

Metodología de la auditoría de redes internas 1.Reconocimiento y enumeración : mapeo de la red, identificación de activos y priorización de los más críticos. 3

2.Identificación de vulnerabilidades : escáneres automatizados combinados con técnicas manuales. 3.Explotación controlada : se simulan ataques reales para demostrar el impacto efectivo.

Un activo “potencialmente vulnerable” sin evidencia de explotación no aporta valor al cliente. 4.Post-explotación: movimiento lateral, escalada de privilegios, acceso al controlador de dominio. 5.Reporte de hallazgos : informe técnico y ejecutivo con vulnerabilidades confirmadas, criticidad y recomendaciones de remediación.

Solo se reportan positivos verificados; las sospechas sin confirmar se indican como recomendaciones.

Auditoría de configuraciones (subcategoría, caja blanca) Dentro de las redes internas existe una subcategoría de auditoría de configuraciones , donde el cliente facilita acceso total a sus herramientas de seguridad.

### Se revisan:

- Firewalls: lo óptimo es configurarlos en modo whitelist (solo permitir comunicaciones
explícitamente autorizadas).

### Ejemplo real: firewall Palo Alto de 200 000 € en un ministerio público con una regla final “any-any” que invalidaba las 347 reglas previas.

- Routers, switches y access points : configuración WPA2-PSK o WPA2-Enterprise con
certificados, segmentación de red de invitados.
- Permisos de carpetas compartidas : control estricto de accesos en herramientas como
SharePoint o Samba.
- Equipos legacy: dispositivos sin soporte oficial (Windows XP, 7, Server 2003/2008).

La
solución recomendada es aislarlos en una red legacy separada mediante firewall, cortando la visibilidad desde el resto de la infraestructura.

Valor e importancia de las auditorías de redes internas
- Identifican riesgos actuales antes de que los atacantes los exploten.
- Garantizan el cumplimiento normativo: ISO/IEC 27001, GDPR, PCI DSS, ENS, DORA,
NIS 2.
- Aumentan la resiliencia: cada vulnerabilidad parcheada cierra una puerta a los atacantes.
- Coste orientativo: ~120 horas × 70-80 €/h ≈ 8 400 €, frente a los 500 000 €/año de una
herramienta como Pentera. 6.

### Reflexión final: especialización y orientación profesional Se anima a los alumnos a explorar todas las líneas antes de decidir su especialización.

Muchas (forense, threat hunting, vigilancia digital, DevSecOps) son desconocidas para quien llega al sector solo por la imagen popular del hacking ofensivo.

El objetivo de Wolf Academy es que los alumnos puedan ingresar directamente en equipos de Red Team al terminar el máster gracias a la certificación eJPT v2 como carta de presentación. 4

## 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración ejercicios tiber.eu TIBER-EU – marco europeo de pruebas de ciberresiliencia para banca y seguros virginacia digital Vigilancia digital – monitorización de amenazas e imagen de marca en la red equipo de defir DeFIR (Digital Forensics and Incident Response) – equipo de forense y respuesta ante incidentes hackinético / haka en ético Hacker ético – profesional de seguridad ofensiva autorizado bruce aún BloodHound – herramienta de análisis y mapeo del Active Directory nesus / open bus Nessus y OpenV AS – escáneres de vulnerabilidades acu netics Acunetix – escáner de vulnerabilidades web eje o tapete eJPT v2 (eLearnSecurity Junior Penetration Tester) – certificación de entrada en pentesting sniper Referencia al uso de Responder para captura de hashes NTLM Mac Fluid MAC Flooding – técnica de saturación de tablas CAM en switches LANIS 2 NIS 2 – Directiva europea de seguridad de redes e información wonder eyes Probablemente OneDrive u otra herramienta de compartición de archivos “freezhunting” Threat Hunting – búsqueda proactiva de amenazas en la red PCI DSS PCI DSS (Payment Card Industry Data Security Standard) – norma de seguridad para datos de tarjetas de pago Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 5