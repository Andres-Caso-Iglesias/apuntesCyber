> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 11**
> **Módulo:** PREWORK
> **Tema:** Clase 11
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 11. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen “ Clase 11: Purple Team “ DeFIR, Forense Digital, DevSecOps y Formación Máster de Ciberseguridad e Inteligencia Artificial “ Evolve Academy 1. ¿Qué es el Purple Team?

El Purple Team es el equipo que une las perspectivas del Red Team (ofensiva) y el Blue Team (defensiva) para maximizar la eficacia de la seguridad organizacional.

Su color surge de la mezcla de rojo y azul: no muy original, reconoce el propio profesor, pero descriptivo.

El Purple Team actúa como puente: facilita el intercambio de conocimientos, herramientas y estrategias entre ambos equipos, eliminando la barrera tradicional entre atacantes y defensores.

Si el Red Team usa una técnica que evade la detección, el Purple Team ayuda al Blue Team a reconocer ese patrón en el futuro; a la inversa, los defensores aportan al Red Team información sobre los controles más efectivos para que sus simulaciones sean más realistas.

> [!important] ### Nota importante: los servicios asignados al Purple Team son una elección personal del profesor.

No existe una estandarización universal; cada empresa y profesional puede decidir qué pertenece a qué equipo.

Purple Team como €œoficina de seguridad€ Un modelo de Purple Team muy común en las administraciones públicas son las oficinas de ciberseguridad: la empresa proveedora asume la gestión integral de seguridad del cliente — perfiles normativos, auditores técnicos de Red Team, especialistas de Blue Team para remediar hallazgos y un equipo de monitorización y respuesta ante incidentes — de modo que la organización puede despreocuparse por completo de la ciberseguridad.

> [!important] ### Elemento clave: comunicación constante La comunicación continua entre Red Team y Blue Team es imprescindible.

Dos equipos que trabajan conjuntamente y se retroalimentan en tiempo real son exponencialmente más efectivos que dos equipos independientes.

Un ejemplo práctico propuesto: un alumno de Blue Team basta una máquina virtual, la refuerza y la pasa al equipo de Red Team para que la vulneren; con el informe de cómo lo han conseguido, el Blue Team la bastiona mejor y vuelve a pasarla.

Se repite el ciclo, aumentando continuamente la dificultad. 1

## 2.

Servicio 1: DeFIR “ Digital Forensics and Incident Response ¿Qué es el DeFIR?

El DeFIR (Digital Forensics and Incident Response ) es la unidad especializada en gestionar los aspectos críticos de la respuesta a incidentes de ciberseguridad y la investigación forense digital.

Corresponde al perfil N3 del SOC: el más experto, el que entra cuando ya ha habido una brecha confirmada.

El profesor lo describe como €œel CSI de la informática€ y defiende que el mejor forense es quien ha sido atacante , ya que conoce exactamente el camino seguido por el intruso: - Sabe que se ha usado Mimikatz para volcar credenciales. - Sabe qué usuarios han sido comprometidos y qué escaladas de privilegios se han realizado. - Sabe a qué equipos se ha hecho pivoting y puede trazar toda la ruta hasta el Active Directory. - Puede reconstruir el path completo del ataque hacia atrás, identificando cada paso y evidencia.

Muchos informes forenses elaborados por el equipo del profesor han sido utilizados por fuerzas y cuerpos de seguridad del Estado para identificar las IPs y VPNs de los atacantes y llevarlos ante la justicia.

El trabajo de DeFIR trasciende lo privado para convertirse en un servicio a la sociedad.

Condiciones laborales El equipo de DeFIR trabaja en guardias, habitualmente una o dos semanas al mes.

Las guardias nocturnas se remuneran con bonus económico.

El responsable del equipo debe estar localizable 24/7 los 365 días del año, en un radio de acción máximo de una hora desde cualquier posible incidente.

Las dos grandes áreas del DeFIR Respuesta ante incidentes: 1.Detección y análisis inicial : identificar los primeros indicios de actividad anómala, validar la existencia del incidente y clasificar su criticidad.

El DeFIR entra cuando hay una brecha confirmada, no ante un intento de fuerza bruta en un WordPress. 2.Contención: implementar medidas inmediatas para limitar la propagación.

Desconectar sistemas comprometidos, aislar segmentos de red afectados o bloquear cuentas involucradas.

Aquí se aprecia todo el valor de tener una correcta segmentación de redes, firewalls bien configurados y arquitectura Zero Trust. 3.Erradicación: eliminar el acceso de los atacantes, borrar backdoors y malware, corregir las vulnerabilidades explotadas. 4.Recuperación: restaurar sistemas desde copias de seguridad verificadas (comprobando que no queden restos del ataque) y bastionar los equipos afectados. 2

Forense digital (servicio independiente pero complementario): Investigación meticulosa de evidencias digitales siguiendo una cadena de custodia estricta para garantizar su validez ante un tribunal.

Incluye: - Investigación de ransomware, macrovirus o reversing de malware. - Análisis de fugas de datos: qué información fue comprometida y cómo. - Amenazas internas: abuso de privilegios o sabotaje por parte de empleados (ej. caso de directiva que exportó documentación financiera antes de marcharse a la competencia). - Soporte a litigios: las pruebas digitales deben ser admisibles en procesos judiciales.

Los peritos forenses con la certificación adecuada pueden testificar ante el juez, quien carece de conocimiento técnico para interpretar los hechos por sí mismo. 3.

Servicio 2: DevSecOps “ Desarrollo Seguro de Aplicaciones ¿Qué es DevSecOps?

DevSecOps integra la seguridad ( Sec) en cada etapa del ciclo de vida del desarrollo de software, combinando Dev (Development), Ops (Operations) y Sec (Security).

El objetivo es que la seguridad no sea una auditoría posterior al desarrollo, sino una parte continua y automática del proceso desde el primer día.

> [!important] ### Principio clave: cuanto antes se detecta una vulnerabilidad en el ciclo de desarrollo, más barato es corregirla.

El profesor menciona haber auditado aplicaciones valoradas en 250 000 € que tuvieron que rehacerse desde cero por vulnerabilidades detectadas en producción.

Pilares fundamentales Cultura de colaboración: - Responsabilidad compartida entre desarrolladores, operadores y especialistas en seguridad. - Formación de desarrolladores en codificación segura. - Incorporar los requisitos de seguridad desde la fase de diseño ( threat modeling).

### Seguridad automatizada: Los controles de seguridad se integran en los pipelines de CI/CD (Continuous Integration / Continuous Deployment ) sin ralentizar el desarrollo: - Escaneos automáticos de vulnerabilidades en código y dependencias. - Análisis estático (SAST) : revisa el código fuente antes de ejecutarlo. - Análisis dinámico (DAST) : evalúa la aplicación en ejecución simulando ataques. - Validación de firmas digitales para detectar componentes maliciosos.

> [!important] ### Herramientas clave: - SonarQube: análisis estático de código, también disponible como open source. - Black Duck (Synopsys): análisis de composición de software, monitoriza librerías de terceros en busca de vulnerabilidades conocidas. - Coverity (Synopsys): análisis estático avanzado. - Checkmarx / Synopsys : escáneres de vulnerabilidades en código y bibliotecas. - EDR / XDR: detección de amenazas en entornos de producción. - IAM (ej.

AWS IAM): protección de pipelines y recursos críticos. 3

Las cinco etapas del ciclo DevSecOps 1.Planificación: identificar riesgos y diseñar controles desde los requisitos iniciales.

Threat modeling para entender las necesidades de seguridad del producto (ej. un TPV virtual necesita protección de datos de tarjeta y conexiones seguras). 2.Desarrollo: análisis estático en tiempo real integrado en el IDE del desarrollador.

Revisión de dependencias externas con herramientas como Black Duck.

Validación de entradas para prevenir inyecciones. 3.Construcción (CI/CD) : escaneo automático de contenedores e infraestructura como código.

Verificación de firmas digitales para detectar librerías vulnerables. 4.Pruebas: análisis dinámico (DAST), pruebas de intrusión simulando el OWASP Top 10, detección de fugas de datos sensibles.

Estas pruebas finales siguen siendo necesarias aunque DevSecOps las haga más ligeras. 5.Implementación y monitorización : monitoreo continuo en producción.

Ante nuevas vulnerabilidades (ej.

Log4Shell afectando a una librería previamente segura), los sistemas de detección levantan alertas en tiempo real.

Pruebas periódicas anuales alineadas con los ciclos normativos.

Beneficios del DevSecOps
- Reducción de riesgos : detección temprana de vulnerabilidades.
- Eficiencia operativa : automatización que reduce tiempo y esfuerzo.
- Cumplimiento normativo continuo : la seguridad es parte del proceso, no un parche
final.
- Escalabilidad segura : ideal para entornos cloud y dinámicos.
- Mejora de calidad : el sello de €œdesarrollo seguro€ es hoy uno de los mejores argumentos
de marketing para vender software.

Perfil profesional y salarios: un DevSecOps junior parte de 32 000-35 000 €/año; un senior alcanza los 45 000-50 000 €.

Es uno de los perfiles más demandados gracias a las normativas. 4.

Servicio 3: Formación y Concienciación de Empleados Por qué el Red Team debe impartir la formación El profesor defiende que la formación en ciberseguridad debe ser impartida por perfiles ofensivos, no por Blue Teams teóricos, porque: - El Red Team ya realiza phishing, smishing, vishing y otras técnicas de ingeniería social en sus auditorías diarias. - Puede diseñar ataques simulados reales, dirigidos y personalizados, haciendo caer a los empleados en la trampa. - La formación posterior, mostrando los resultados reales de la campaña de phishing sobre los propios empleados, tiene un impacto mucho mayor que cualquier presentación teórica. 4

### Caso real: el profesor y Carlos Castillo completaron una auditoría externa en seis minutos mediante ingeniería social, obteniendo credenciales válidas para acceder a la organización.

Objetivos del servicio
- Aumentar la sensibilidad sobre amenazas digitales.
- Reforzar buenas prácticas : no abrir correos fraudulentos, no conectar USBs
desconocidos, uso de contraseñas robustas, etc.
- Cumplir normativas : formación periódica en ciberseguridad es un control exigido por
ISO 27001, ENS, NIS 2 y DORA.
- Construir una cultura de seguridad proactiva que convierta a los empleados en la
primera línea de defensa, no en el eslabón más débil.

El servicio se personaliza según el sector, el nivel de madurez de los empleados y los riesgos específicos de la organización. 5.

Cierre del módulo de líneas de ciberseguridad Con esta sesión concluye el bloque completo de líneas de ciberseguridad (Red Team, Blue Team y Purple Team).

La próxima sesión abordará los tipos de hackers y, tras ello, se pasará definitivamente a la parte práctica del máster. 6.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración parper team / parpel team Purple Team “ equipo colaborativo entre Red y Blue Team equipo de decir / decir / de fir DeFIR (Digital Forensics and Incident Response) “ equipo de forense y respuesta ante incidentes fornse / fornise / forense digital Forense digital “ disciplina de investigación de evidencias digitales de secops / depth sec ops DevSecOps “ integración de seguridad en el ciclo de vida del desarrollo software de de box / de de ops DevOps “ metodología de desarrollo y operaciones pipelines de c y cd Pipelines de CI/CD (Continuous Integration / Continuous Deployment ) “ integración y despliegue continuos sas / sars SAST (Static Application Security Testing ) “ análisis estático de seguridad de aplicaciones das / dust DAST (Dynamic Application Security Testing ) 5

Término en la transcripción Corrección / Aclaración “ análisis dinámico de seguridad de aplicaciones sonar cube SonarQube “ herramienta de análisis estático de código blackdak / black duck Black Duck (Synopsys) “ herramienta de análisis de composición de software cover / coverity Coverity (Synopsys) “ herramienta de análisis estático avanzado checkmark Checkmarx “ escáner de vulnerabilidades en código a yam / ayam IAM (Identity and Access Management ) “ gestión de identidades y accesos yam / haces Referencias a YAML e IaC (Infrastructure as Code) “ infraestructura como código cíclic haunting Threat Hunting “ búsqueda proactiva de amenazas tiberegu TIBER-EU “ marco europeo de ejercicios de Red Team para banca y seguros mímica / mímica 100% Mimikatz “ herramienta de volcado de credenciales de memoria en Windows macrovirus Macro-virus “ malware embebido en documentos de Office cadena de custodio Cadena de custodia “ protocolo forense para garantizar la integridad de las evidencias vision querying sin 20 Vishing / Quishing / Smishing “ variantes de ingeniería social por voz, QR y SMS log 4g Log4Shell / Log4j “ vulnerabilidad crítica en librería Java xdr XDR (Extended Detection and Response ) “ solución de detección y respuesta extendida FNS DeFIR o DFIR “ Digital Forensics and Incident Response (siglas usadas indistintamente) Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial “ Wolf Academy. 6
→’
→’
→’
→’
