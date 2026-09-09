> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 10**
> **Módulo:** PREWORK
> **Tema:** Clase 10
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 10. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 10: Bastionado de Equipos, Segmentación de Redes, Firewalls y WAF Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción Esta sesión cierra la parte de Blue Team abordando tres servicios estrechamente relacionados: el bastionado de equipos , la segmentación de redes y la implementación de firewalls y WAF.

Todos ellos son respuesta directa a las normativas vistas en la sesión anterior y son controles que las empresas deben demostrar ante las auditorías normativas (ISO 27001, ENS, PCI DSS, NIS 2, DORA).

PARTE I: Bastionado de Equipos 2. ¿Qué es el bastionado?

El bastionado (hardening) es la técnica de configurar un equipo de forma segura para reducir al máximo su superficie de ataque y su exposición a amenazas.

Consiste en eliminar configuraciones inseguras, implementar controles de seguridad robustos y garantizar el cumplimiento normativo.

Nunca puede eliminar el riesgo al 100 %, especialmente en equipos legacy, pero lo minimiza al máximo.

La referencia oficial en España son las guías de bastionado del CCN-CERT (Centro Criptológico Nacional), que cubren cada sistema operativo y versión de forma detallada y son de descarga pública en su web. 3.

Áreas clave del bastionado 1.

Revisión y eliminación de servicios innecesarios: Todo lo que no sea estrictamente necesario para la funcionalidad del equipo debe deshabilitarse.

Ejemplo: un Windows Server 2008 que no necesita Samba debe tener cerrados los puertos 445, 135 y 139.

Si no hay Samba activo, EternalBlue no puede explotarse aunque la vulnerabilidad exista en el sistema.

El mismo principio aplica a: - Cuentas predeterminadas (admin, invitado, mantenimiento): si no se usan, se desactivan. - Aplicaciones instaladas que no se usen. - Conectividad de red no requerida (si el equipo solo necesita comunicación local, no se le da acceso a internet). 2.

Configuración segura del sistema operativo: - Actualizar el sistema operativo y todas las aplicaciones necesarias con los últimos parches de seguridad disponibles compatibles con el 1

funcionamiento del equipo (sin romper la funcionalidad). - Desactivar cuentas predeterminadas e inactivas. - Políticas de contraseñas robustas: mínimo 12-13 caracteres alfanuméricos con mayúsculas, minúsculas, números y caracteres especiales.

Cambio obligatorio cada mes como máximo, de modo que el tiempo necesario para romper el hash supere siempre el ciclo de renovación. - Restricciones de permisos con principio de mínimo privilegio .

Herramienta recomendada para inventariar usuarios y permisos en Windows: net user. 3.

Configuración de redes y accesos: - Aislar equipos según su función dentro de la red. - Equipos legacy deben estar en una red legacy separada . - Control de puertos y protocolos: cerrar todo lo que no sea imprescindible.

Protocolos como Telnet o SMBv1 deben estar deshabilitados si no se usan. - Acceso remoto (RDP, VPN) siempre con autenticación multifactor (MFA) .

Nunca exponer RDP directamente al exterior. 4.

Políticas de seguridad: - Bloqueo automático de sesión tras un máximo de 3 minutos de inactividad.

Sin bloqueo, cualquier persona con acceso físico puede abrir puertos, rehabilitar servicios o lanzar una reverse shell desde el equipo. - Auditorías de acceso y eventos críticos: revisar los logs de Windows mensual o trimestralmente para detectar accesos no autorizados.

Los registros de eventos de Windows permanecen aunque un atacante haya bypasseado las alertas del SIEM.

Medidas complementarias (de sentido común): - Protección antimalware : antivirus con políticas personalizadas (nunca por defecto), IDS/IPS y soluciones EDR. - Monitorización y registro: logs de intentos fallidos de acceso, cambios de configuración y accesos no autorizados.

Integración con SIEM para detección centralizada. - Cifrado de datos: AES-256 para datos en reposo, TLS 1.3 para datos en tránsito, discos y particiones cifrados.

PARTE II: Segmentación de Redes 4.

Concepto y finalidad La segmentación de redes divide una red grande en subredes o segmentos más pequeños y aislados, controlando estrictamente el tráfico entre ellos.

Es la implementación práctica de la arquitectura Zero Trust a nivel de red.

Si un segmento es comprometido (ej. por ransomware), el atacante no puede moverse libremente al resto de la organización.

Regla práctica ante ransomware: al detectar infección en un segmento, tirar del cable para aislar el segmento afectado y evitar la propagación.

Perder un segmento es mucho mejor que perder toda la organización. 5.

Arquitectura de segmentación recomendada
- Red de usuarios: empleados con acceso a sus recursos habituales.
- Red de servidores críticos : bases de datos, servidores financieros, Active Directory.
- DMZ (Demilitarized Zone ): zona intermedia entre internet y la red interna.

Aloja

servidores web, VPN, correo electrónico.

Es la primera línea de defensa y el objetivo habitual del atacante externo.
- Red IoT: dispositivos conectados con bajo nivel de seguridad, aislados del resto.
- Red legacy: equipos obsoletos sin soporte oficial, totalmente aislados.

Un firewall filtra
el tráfico hacia y desde este segmento para que estos equipos sean invisibles desde el resto de la red.

Tecnología Obscura: herramienta de proxy-firewall que actúa como “espejo” delante de una red legacy, rebotando los escaneos de red y haciéndola invisible.

Es un ejemplo de seguridad por oscuridad (no debe ser el único control, pero complementa la segmentación). 6.

Beneficios de la segmentación
- Aislamiento de amenazas : contiene malware y ataques en el segmento afectado.
- Mejora del rendimiento : reduce la congestión al dividir el flujo de tráfico y evitar el
“cuello de botella”.
- Cumplimiento normativo : facilita demostrar a los auditores que los datos sensibles
están aislados.
- Facilidad de gestión : permite aplicar GPOs (Group Policy Objects ) del Active Directory
por segmento, en lugar de equipo a equipo.
- Mayor visibilidad : el tráfico por segmento tiene una identidad conocida, facilitando la
monitorización y el análisis forense.

Pivoting y doble interfaz de red: el punto débil de la segmentación es un equipo con dos interfaces de red (dos tarjetas de red en dos segmentos distintos).

Comprometiendo ese equipo, el atacante puede saltar al segundo segmento.

Esta técnica, llamada pivoting, se verá en detalle en la parte práctica del máster con el laboratorio de pivoting.

PARTE III: Firewalls y WAF 7.

Firewalls Un firewall es un dispositivo o software que monitoriza y controla el tráfico entrante y saliente de una red según reglas de seguridad predefinidas.

Puede ser hardware (appliance físico en el CPD) o software (agente instalado en los equipos).

Filosofía correcta de configuración: whitelist, no blacklist.

Todo tráfico bloqueado por defecto; solo se permite lo estrictamente necesario.

La filosofía contraria (todo abierto, se va bloqueando lo sospechoso) es la más extendida y la más peligrosa: cuando detectas algo raro, ya te han atacado.

Tipos de firewalls: Tipo Descripción Firewall de red Bloquea tráfico malicioso en puntos de 3

Tipo Descripción entrada/salida.

Actúa como “portero de discoteca”: deja pasar o bloquea según IP y protocolo.

NGFW (Next-Generation Firewall )Incluye DPI (Deep Packet Inspection ): analiza el contenido del datagrama, no solo origen y destino.

Integra IPS, Threat Intelligence e IA para detectar tráfico malicioso aunque provenga de una IP no bloqueada.

### Fabricantes principales: - Palo Alto: considerado el mejor del mercado, con IA y Machine Learning integrados.

El más caro pero también el más demandado.

Ofrece certificaciones propias. - Fortinet (FortiGate) : solución escalable y de alto rendimiento para empresas de todos los tamaños.

También ofrece certificaciones. - Cisco: combina firewalls, IPS y capacidades de detección avanzada.

Complementa las soluciones anteriores.

Advertencia: los firewalls son bypasseables.

Herramienta usada en Red Team para identificar la tecnología de WAF/firewall del objetivo: wafw00f (WAF fingerprinting tool ). 8.

WAF (Web Application Firewall) Un WAF es un firewall especializado en proteger aplicaciones web.

Actúa como escudo entre el servidor web e internet, analizando las solicitudes HTTP/HTTPS e identificando y bloqueando amenazas específicas de aplicaciones web (las del OWASP Top 10): inyecciones SQL, XSS, fuerza bruta, robo de datos, etc.

Un WAF es técnicamente un NGFW aplicado a la capa de aplicación: analiza el payload del datagrama para determinar si la comunicación es maliciosa.

Casos de uso: incluso si una aplicación tiene vulnerabilidades en su código o en su funcionamiento dinámico, un WAF puede bloquear la explotación de esas vulnerabilidades como capa de seguridad adicional.

WAFs más destacados: - Cloudflare WAF: gratuito, ligero, eficaz.

Recomendado para cualquier aplicación web que no esté en AWS.

Se configura modificando dos registros DNS.

Para el profesor, es el más práctico y recomendable para uso general. - AWS WAF: solución integrada de Amazon Web Services.

Ideal si la aplicación ya está alojada en AWS. - Imperva WAF: solución robusta para protección contra amenazas avanzadas. - Palo Alto WAF / Fortinet FortiGate: también ofrecen soluciones WAF de alto rendimiento, recomendados para grandes organizaciones. 9.

Cierre del módulo Blue Team Esta sesión concluye el bloque completo de Blue Team.

Las líneas cubiertas han sido: arquitecturas seguras, monitorización SOC 24/7, vigilancia digital, normativa y cumplimiento, 4

bastionado de equipos, segmentación de redes, firewalls y WAF.

La siguiente sesión abordará el Purple Team: forense, DevSecOps, respuesta ante incidentes y formación. 10.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración caud Ticket – solicitud formal al servicio de soporte de IT (helpdesk) CEMS SIEM (Security Information and Event Management) – sistema de gestión de eventos de seguridad DSIPS IDS/IPS (Intrusion Detection/Prevention System) – sistemas de detección y prevención de intrusiones pipotein / pipoting Pivoting – técnica de salto entre segmentos de red a través de un equipo con doble interfaz WAV / web WAF (Web Application Firewall ) – cortafuegos para aplicaciones web OAV Top 10 OWASP Top 10 – estándar de vulnerabilidades web webWAF wafw00f – herramienta de fingerprinting para identificar tecnologías de WAF cross-site script XSS (Cross-Site Scripting ) – inyección de código JavaScript en aplicaciones web NG firewalls / new generation NGFW (Next-Generation Firewall ) – firewall de nueva generación con DPI e IPS DPI DPI (Deep Packet Inspection ) – inspección profunda del contenido de los paquetes de red any any Regla de firewall que permite todo el tráfico entrante y saliente, anulando toda la segmentación configurada CCN CERT CCN-CERT – Centro Criptológico Nacional, organismo de ciberseguridad del CNI español Obscura Obscura – tecnología de proxy-firewall que invisibiliza segmentos de red legacy frente a escaneos Modbus Modbus – protocolo de comunicación industrial estándar en redes OT/SCADA reversal Reverse shell – conexión de retorno desde el equipo comprometido al servidor del atacante rig de minería Rig de cracking – clúster de GPUs usado para romper hashes de contraseñas RTX 3080 en serie Referencia a GPUs NVIDIA RTX 3080 usadas 5

Término en la transcripción Corrección / Aclaración en paralelo para cracking de hashes eJPT eJPT v2 (eLearnSecurity Junior Penetration Tester) – certificación de entrada en pentesting Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../MODULO3/resumen_master_clase26.md|resumen_master_clase26]] — IA en Ciberseguridad, Metasploit, Windows
- [[../../transcripciones/Junio/08.06.2026 HTB Starting Point Tier 1 y 2 Burp Suite, Webshell y Reverse Shell.md|08.06.2026 HTB Starting Point Tier 1 y 2 Burp Suite, Webshell y Reverse Shell]] — IA en Ciberseguridad, Metasploit, Windows
- [[../MODULO1/resumen_master_clase2.md|resumen_master_clase2]] — IA en Ciberseguridad, Metasploit, Windows
- [[../MODULO1/resumen_master_clase5.md|resumen_master_clase5]] — IA en Ciberseguridad, Metasploit, Windows
- [[../../transcripciones/Julio/07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote.md|07.07.2026 Explotación Avanzada Fuzzing de Parámetros II y Escalada de Privilegios MultiPivote]] — IA en Ciberseguridad, Metasploit, Windows
- [[resumen_clase11.md|resumen_clase11]] — Certificaciones, IA en Ciberseguridad, Windows

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Telnet|Telnet]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #blue-team #burpsuite #certificaciones #file-upload #forense #hack-the-box #hydra #ia #metasploit #netcat #normativa #pivoting #redes #reverse-shell #telnet #windows #xss
