> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 6**
> **Módulo:** PREWORK
> **Tema:** Clase 6
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 6. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 6: Auditorías de Código, IoT, Cloud y Bastionado Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción Esta sesión repasa cuatro tipologías de auditoría del Red Team menos comunes que las anteriores pero con gran potencial de especialización: auditoría de código, auditoría IoT, auditoría Cloud y bastionado.

Se destaca que las nuevas normativas europeas e internacionales están incorporando controles específicos sobre el desarrollo seguro y el bastionado, lo que convierte estas líneas en nichos de alto valor profesional futuro.

PARTE I: Auditoría de Código 2. ¿Qué es y en qué se diferencia de las auditorías dinámicas?

Las auditorías vistas anteriormente (web, externa, interna) son auditorías dinámicas : se interactúa con la aplicación en funcionamiento para detectar vulnerabilidades.

La auditoría de código es una auditoría de caja blanca que revisa el código fuente desde cero, analizando la lógica interna, la gestión de variables, los controles de acceso, las llamadas a bases de datos y las dependencias externas.

Lo óptimo es realizar ambas en paralelo: la auditoría dinámica puede revelar comportamientos que se confirman en el código, y la revisión de código puede exponer vulnerabilidades que la prueba dinámica no detectaría (ej. credenciales hardcodeadas, queries SQL embebidas directamente). 3.

Metodología y herramientas No existe un estándar universal como el OWASP Top 10 para este tipo de auditoría.

Cada empresa o auditor desarrolla su propia metodología.

En Cibersia se utiliza la metodología interna CibersiaSec CodeSec .

Las vulnerabilidades que se buscan son las mismas que en el OWASP Top 10: inyecciones, fallos en autenticación, exposición de datos sensibles, gestión incorrecta de errores y excepciones, etc.

Herramientas de análisis estático de código:
- SonarQube: detección de patrones de errores y malas prácticas.

- Checkmarx: análisis de seguridad en código fuente.
- Coverity + Black Duck (de Synopsys): análisis de composición de software.

Black
Duck en particular monitoriza de forma continua todas las librerías de terceros implementadas y alerta cuando aparece una nueva vulnerabilidad en alguna de ellas, siendo especialmente útil para gestionar la cadena de suministro del software.

Las herramientas automatizadas detectan patrones conocidos pero no comprenden la lógica de negocio ni el flujo entre métodos, por lo que la revisión manual del auditor es siempre imprescindible. 4.

El riesgo de las librerías de terceros En el 100 % de los desarrollos se usan librerías externas.

La vulnerabilidad Log4Shell (Log4j) estuvo activa durante 11 años sin ser detectada, afectando al 70 % de las aplicaciones Java del mundo, incluyendo Minecraft (RCE con CVSS 9.8).

Esto ilustra el peligro de confiar ciegamente en código de terceros sin monitorizarlo.

La recomendación es estudiar cada librería antes de implementarla y mantener una vigilancia continua de las versiones utilizadas.

PARTE II: Auditoría de Dispositivos IoT 5.

Por qué los dispositivos IoT son especialmente vulnerables Los dispositivos IoT combinan hardware, software y comunicaciones de red.

Se producen en masa a muy bajo coste (cámaras IP por 3 € de producción), lo que hace inviable invertir en seguridad manteniendo los márgenes.

### El resultado: credenciales por defecto, firmware sin actualizar, protocolos inseguros y ausencia total de controles de seguridad.

Los riesgos van desde cámaras domésticas accedidas por atacantes hasta dispositivos médicos críticos (marcapasos, parches de glucosa), robots industriales de cadena de montaje o vehículos conectados.

El profesor describe haber hackeado un marcapasos mediante Bluetooth modificando sus frecuencias de pulso, y haber presenciado la parada de un Jaguar a 200 km/h de forma remota.

La Botnet Mirai es el ejemplo más destacado: infectó millones de dispositivos IoT usando únicamente sus credenciales por defecto, creciendo de forma exponencial (1→2→4→8…) hasta superar en capacidad de ataque DDoS a los servidores de Google. 6.

Aspectos clave de la auditoría IoT Hardware: análisis físico del dispositivo.

Puertos como JTAG permiten extraer el firmware o modificar configuraciones.

Se evalúan también las medidas anti-tamper (resistencia a manipulaciones): desde carcasas selladas hasta sistemas militares que borran el firmware si detectan variaciones de presión o temperatura. 2

Firmware: software que controla el hardware.

Se analiza con herramientas como Binwalk o Firmwalker en busca de versiones vulnerables, configuraciones por defecto y puertas traseras.

Caso real documentado: Huawei introdujo backdoors en actualizaciones de firmware de sus routers, detectados en varios países.

Cualquier fabricante con control sobre las actualizaciones puede modificar el comportamiento del dispositivo de forma remota.

Comunicaciones: cifrado de datos, protocolos inseguros y servicios expuestos innecesariamente (análogo a las auditorías de redes externas).

Configuración y autenticación: credenciales por defecto, gestión de usuarios y seguridad por diseño.

### Ecosistema vinculado: muchos dispositivos IoT tienen una aplicación móvil asociada (ej.

Oura Ring).

Comprometer la app o el dispositivo puede derribar el ecosistema completo.

PARTE III: Auditorías Cloud 7.

Qué es la nube y por qué auditarla La nube no es más que servidores físicos alquilados ubicados en centros de datos (principalmente en Holanda y EE.

UU.).

Los principales proveedores son Amazon Web Services (AWS), Microsoft Azure y Google Cloud.

Una auditoría cloud se parece a una auditoría interna o externa, pero con sus propias particularidades: no usa Active Directory con GPOs, sino roles IAM (Identity and Access Management ) y políticas propias de cada plataforma.

Una ventaja importante de migrar a cloud es heredar el cumplimiento normativo del proveedor (ej. si AWS tiene ISO 27001, el cliente hereda sus controles de infraestructura).

Sin embargo, la responsabilidad se comparte: el proveedor asegura la infraestructura subyacente, pero el cliente es responsable de sus aplicaciones, datos y configuraciones.

### Moraleja principal: cloud es extremadamente seguro, pero el usuario es quien lo hace inseguro, igual que en cualquier infraestructura IT. 8.

Principales riesgos y áreas clave de auditoría Configuración de la infraestructura: - AWS entrega instancias totalmente cerradas (filosofía whitelist): solo el puerto 22 con clave privada RSA está abierto, y el acceso requiere doble factor de autenticación. - Los errores de configuración son la principal causa de brechas en la nube.

Se revisan las VPC (Virtual Private Clouds ), la exposición de servicios (bases de datos, buckets S3) y las políticas de firewalls y grupos de seguridad. - Ejemplo real: el profesor accedió a una cuenta AWS completa de un cliente a través de una aplicación web vulnerable que exponía tokens de autenticación en el código, sin necesidad de atacar la infraestructura de Amazon.

Gestión de accesos e identidad (IAM): - Principio de mínimo privilegio : cada usuario y 3

servicio solo accede a lo que necesita. - Caso real: cliente con 9 administradores de dominio en una empresa de 230 personas (lo correcto serían 1-2). - Contraseñas robustas y autenticación multifactor (MFA) obligatoria. - Permisos temporales con revocación inmediata tras su uso.

Es muy común encontrar accesos de auditores, proveedores o exempleados que siguen activos años después.

Protección de datos: - Cifrado en tránsito y en reposo. - Backups redundantes almacenados en ubicaciones geográficamente separadas para evitar pérdida total en caso de incendio o desastre en un CPD. - Retención de datos según normativa (GDPR, ISO 27001, PCI DSS).

Monitorización y respuesta a incidentes: - Integración con SIEM (Security Information and Event Management ): herramientas como Splunk o AWS CloudWatch para análisis de logs en tiempo real. - Planes de respuesta documentados y probados.

Se menciona el servicio de simulación de incidentes con directivos: se crea un incidente real controlado para evaluar la respuesta sin notificar a la AEPD ni a los clientes.

PARTE IV: Bastionado y Auditoría de Bastionado 9. ¿Qué es el bastionado?

El bastionado es el proceso de asegurar un sistema (servidor, estación de trabajo, dispositivo de red o entorno cloud) mediante la eliminación de configuraciones innecesarias, la reducción al mínimo de la superficie de ataque y la aplicación de controles de seguridad estrictos.

Se aplica especialmente a sistemas legacy que no pueden actualizarse pero deben seguir operando.

La referencia normativa en España son las guías del CCN-CERT (Centro Criptológico Nacional, división de ciberseguridad del CNI).

Estas guías detallan cómo bastionar cada sistema operativo y versión.

Para superar una auditoría normativa con un sistema legacy, es obligatorio demostrar que está correctamente bastionado según estas guías. 10.

Aspectos clave de la auditoría de bastionado Servicios y configuraciones activas: - Deshabilitar todo lo que no sea estrictamente necesario: servicios del sistema, puertos, aplicaciones (ej.

Paint, Word, acceso a internet) en máquinas industriales. - Las configuraciones predeterminadas ( next, next, finish) son el mayor enemigo del bastionado.

Gestión de usuarios y privilegios: - Un único usuario por persona para trazabilidad de actividad. - Principio de mínimo privilegio aplicado estrictamente. - Contraseñas más exigentes en sistemas legacy que en sistemas modernos: mínimo 12 caracteres, rotación mensual, MFA para administradores. - Bloqueo automático de sesión por inactividad a los 2 minutos.

Actualizaciones y parches: - Actualizar hasta el máximo nivel compatible con el correcto funcionamiento de la aplicación legacy, sin intentar llevar el sistema a la última versión si ello 4

rompe la funcionalidad. - En sistemas que sí pueden actualizarse, mantenerlos siempre en el último parche de seguridad.

Configuración de red y firewall: - Política whitelist: solo permitir las comunicaciones estrictamente necesarias. - Segmentación de red: aislar sistemas legacy en una red legacy separada para minimizar la visibilidad del atacante. - Limitar los intentos de acceso fallidos para prevenir fuerza bruta. - Deshabilitar el acceso administrativo desde redes públicas.

Registros y monitorización: - Registrar todos los eventos importantes: accesos fallidos, cambios de configuración, actividad en puertos críticos. - Retención de logs durante 3 años como mínimo según normativa. - Integración con SIEM para análisis en tiempo real. - Un sistema bastionado bien monitorizado puede usarse como honeypot para estudiar el comportamiento de los atacantes con total seguridad. 11.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración WAPTOP10 / no was top ten OWASP Top 10 – estándar de vulnerabilidades en aplicaciones web Source Sonar Cube SonarQube – herramienta de análisis estático de código Checkmark Checkmarx – herramienta de análisis de seguridad en código fuente Coverti de sinopsis / BlackDuck Coverity + Black Duck (Synopsys) – herramientas de análisis de composición de software Log4G Log4Shell / Log4j – vulnerabilidad crítica en librería Java bing walk / firm analyzer Binwalk y Firmwalker – herramientas de análisis de firmware IoT jota tajos los guard JTAG – puerto de depuración hardware utilizado para extraer firmware finware / fin de Firmware – software embebido que controla el hardware de un dispositivo anti tamper Anti-tamper – mecanismos de resistencia a manipulaciones físicas UAV UA V (Unmanned Aerial Vehicle ) – vehículo aéreo no tripulado / dron de reconocimiento ayam / iam IAM (Identity and Access Management ) – gestión de identidades en entornos cloud vpc VPC (Virtual Private Cloud ) – red privada virtual en entornos cloud es plan Splunk – plataforma SIEM de análisis de logs cloud watch AWS CloudWatch – servicio de 5

Término en la transcripción Corrección / Aclaración monitorización de Amazon Web Services sien SIEM (Security Information and Event Management) – sistema de gestión de eventos de seguridad CCN / guías de CCN CCN-CERT – Centro Criptológico Nacional, organismo de ciberseguridad del CNI español nesus open bar Nessus y OpenV AS – escáneres de vulnerabilidades aura ring Oura Ring – dispositivo IoT de monitorización de salud tpv / atm TPV (Terminal Punto de Venta) / ATM (cajero automático) ya war / type x type f Jaguar F-Type / I-Pace – vehículos eléctricos conectados mencionados como ejemplo de hackeo Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6