> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 11**
> **MÃ³dulo:** PREWORK
> **Tema:** Clase 11
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 11. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
Resumen “ Clase 11: Purple Team “ DeFIR, Forense Digital, DevSecOps y FormaciÃ³n MÃ¡ster de Ciberseguridad e Inteligencia Artificial “ Evolve Academy 1. Â¿QuÃ© es el Purple Team?

El Purple Team es el equipo que une las perspectivas del Red Team (ofensiva) y el Blue Team (defensiva) para maximizar la eficacia de la seguridad organizacional.

Su color surge de la mezcla de rojo y azul: no muy original, reconoce el propio profesor, pero descriptivo.

El Purple Team actÃºa como puente: facilita el intercambio de conocimientos, herramientas y estrategias entre ambos equipos, eliminando la barrera tradicional entre atacantes y defensores.

Si el Red Team usa una tÃ©cnica que evade la detecciÃ³n, el Purple Team ayuda al Blue Team a reconocer ese patrÃ³n en el futuro; a la inversa, los defensores aportan al Red Team informaciÃ³n sobre los controles mÃ¡s efectivos para que sus simulaciones sean mÃ¡s realistas.

> [!important] ### Nota importante: los servicios asignados al Purple Team son una elecciÃ³n personal del profesor.

No existe una estandarizaciÃ³n universal; cada empresa y profesional puede decidir quÃ© pertenece a quÃ© equipo.

Purple Team como â€œoficina de seguridadâ€ Un modelo de Purple Team muy comÃºn en las administraciones pÃºblicas son las oficinas de ciberseguridad: la empresa proveedora asume la gestiÃ³n integral de seguridad del cliente — perfiles normativos, auditores tÃ©cnicos de Red Team, especialistas de Blue Team para remediar hallazgos y un equipo de monitorizaciÃ³n y respuesta ante incidentes — de modo que la organizaciÃ³n puede despreocuparse por completo de la ciberseguridad.

> [!important] ### Elemento clave: comunicaciÃ³n constante La comunicaciÃ³n continua entre Red Team y Blue Team es imprescindible.

Dos equipos que trabajan conjuntamente y se retroalimentan en tiempo real son exponencialmente mÃ¡s efectivos que dos equipos independientes.

Un ejemplo prÃ¡ctico propuesto: un alumno de Blue Team basta una mÃ¡quina virtual, la refuerza y la pasa al equipo de Red Team para que la vulneren; con el informe de cÃ³mo lo han conseguido, el Blue Team la bastiona mejor y vuelve a pasarla.

Se repite el ciclo, aumentando continuamente la dificultad. 1

## 2.

Servicio 1: DeFIR “ Digital Forensics and Incident Response Â¿QuÃ© es el DeFIR?

El DeFIR (Digital Forensics and Incident Response ) es la unidad especializada en gestionar los aspectos crÃ­ticos de la respuesta a incidentes de ciberseguridad y la investigaciÃ³n forense digital.

Corresponde al perfil N3 del SOC: el mÃ¡s experto, el que entra cuando ya ha habido una brecha confirmada.

El profesor lo describe como â€œel CSI de la informÃ¡ticaâ€ y defiende que el mejor forense es quien ha sido atacante , ya que conoce exactamente el camino seguido por el intruso: - Sabe que se ha usado Mimikatz para volcar credenciales. - Sabe quÃ© usuarios han sido comprometidos y quÃ© escaladas de privilegios se han realizado. - Sabe a quÃ© equipos se ha hecho pivoting y puede trazar toda la ruta hasta el Active Directory. - Puede reconstruir el path completo del ataque hacia atrÃ¡s, identificando cada paso y evidencia.

Muchos informes forenses elaborados por el equipo del profesor han sido utilizados por fuerzas y cuerpos de seguridad del Estado para identificar las IPs y VPNs de los atacantes y llevarlos ante la justicia.

El trabajo de DeFIR trasciende lo privado para convertirse en un servicio a la sociedad.

Condiciones laborales El equipo de DeFIR trabaja en guardias, habitualmente una o dos semanas al mes.

Las guardias nocturnas se remuneran con bonus econÃ³mico.

El responsable del equipo debe estar localizable 24/7 los 365 dÃ­as del aÃ±o, en un radio de acciÃ³n mÃ¡ximo de una hora desde cualquier posible incidente.

Las dos grandes Ã¡reas del DeFIR Respuesta ante incidentes: 1.DetecciÃ³n y anÃ¡lisis inicial : identificar los primeros indicios de actividad anÃ³mala, validar la existencia del incidente y clasificar su criticidad.

El DeFIR entra cuando hay una brecha confirmada, no ante un intento de fuerza bruta en un WordPress. 2.ContenciÃ³n: implementar medidas inmediatas para limitar la propagaciÃ³n.

Desconectar sistemas comprometidos, aislar segmentos de red afectados o bloquear cuentas involucradas.

AquÃ­ se aprecia todo el valor de tener una correcta segmentaciÃ³n de redes, firewalls bien configurados y arquitectura Zero Trust. 3.ErradicaciÃ³n: eliminar el acceso de los atacantes, borrar backdoors y malware, corregir las vulnerabilidades explotadas. 4.RecuperaciÃ³n: restaurar sistemas desde copias de seguridad verificadas (comprobando que no queden restos del ataque) y bastionar los equipos afectados. 2

Forense digital (servicio independiente pero complementario): InvestigaciÃ³n meticulosa de evidencias digitales siguiendo una cadena de custodia estricta para garantizar su validez ante un tribunal.

Incluye: - InvestigaciÃ³n de ransomware, macrovirus o reversing de malware. - AnÃ¡lisis de fugas de datos: quÃ© informaciÃ³n fue comprometida y cÃ³mo. - Amenazas internas: abuso de privilegios o sabotaje por parte de empleados (ej. caso de directiva que exportÃ³ documentaciÃ³n financiera antes de marcharse a la competencia). - Soporte a litigios: las pruebas digitales deben ser admisibles en procesos judiciales.

Los peritos forenses con la certificaciÃ³n adecuada pueden testificar ante el juez, quien carece de conocimiento tÃ©cnico para interpretar los hechos por sÃ­ mismo. 3.

Servicio 2: DevSecOps “ Desarrollo Seguro de Aplicaciones Â¿QuÃ© es DevSecOps?

DevSecOps integra la seguridad ( Sec) en cada etapa del ciclo de vida del desarrollo de software, combinando Dev (Development), Ops (Operations) y Sec (Security).

El objetivo es que la seguridad no sea una auditorÃ­a posterior al desarrollo, sino una parte continua y automÃ¡tica del proceso desde el primer dÃ­a.

> [!important] ### Principio clave: cuanto antes se detecta una vulnerabilidad en el ciclo de desarrollo, mÃ¡s barato es corregirla.

El profesor menciona haber auditado aplicaciones valoradas en 250 000 â‚¬ que tuvieron que rehacerse desde cero por vulnerabilidades detectadas en producciÃ³n.

Pilares fundamentales Cultura de colaboraciÃ³n: - Responsabilidad compartida entre desarrolladores, operadores y especialistas en seguridad. - FormaciÃ³n de desarrolladores en codificaciÃ³n segura. - Incorporar los requisitos de seguridad desde la fase de diseÃ±o ( threat modeling).

### Seguridad automatizada: Los controles de seguridad se integran en los pipelines de CI/CD (Continuous Integration / Continuous Deployment ) sin ralentizar el desarrollo: - Escaneos automÃ¡ticos de vulnerabilidades en cÃ³digo y dependencias. - AnÃ¡lisis estÃ¡tico (SAST) : revisa el cÃ³digo fuente antes de ejecutarlo. - AnÃ¡lisis dinÃ¡mico (DAST) : evalÃºa la aplicaciÃ³n en ejecuciÃ³n simulando ataques. - ValidaciÃ³n de firmas digitales para detectar componentes maliciosos.

> [!important] ### Herramientas clave: - SonarQube: anÃ¡lisis estÃ¡tico de cÃ³digo, tambiÃ©n disponible como open source. - Black Duck (Synopsys): anÃ¡lisis de composiciÃ³n de software, monitoriza librerÃ­as de terceros en busca de vulnerabilidades conocidas. - Coverity (Synopsys): anÃ¡lisis estÃ¡tico avanzado. - Checkmarx / Synopsys : escÃ¡neres de vulnerabilidades en cÃ³digo y bibliotecas. - EDR / XDR: detecciÃ³n de amenazas en entornos de producciÃ³n. - IAM (ej.

AWS IAM): protecciÃ³n de pipelines y recursos crÃ­ticos. 3

Las cinco etapas del ciclo DevSecOps 1.PlanificaciÃ³n: identificar riesgos y diseÃ±ar controles desde los requisitos iniciales.

Threat modeling para entender las necesidades de seguridad del producto (ej. un TPV virtual necesita protecciÃ³n de datos de tarjeta y conexiones seguras). 2.Desarrollo: anÃ¡lisis estÃ¡tico en tiempo real integrado en el IDE del desarrollador.

RevisiÃ³n de dependencias externas con herramientas como Black Duck.

ValidaciÃ³n de entradas para prevenir inyecciones. 3.ConstrucciÃ³n (CI/CD) : escaneo automÃ¡tico de contenedores e infraestructura como cÃ³digo.

VerificaciÃ³n de firmas digitales para detectar librerÃ­as vulnerables. 4.Pruebas: anÃ¡lisis dinÃ¡mico (DAST), pruebas de intrusiÃ³n simulando el OWASP Top 10, detecciÃ³n de fugas de datos sensibles.

Estas pruebas finales siguen siendo necesarias aunque DevSecOps las haga mÃ¡s ligeras. 5.ImplementaciÃ³n y monitorizaciÃ³n : monitoreo continuo en producciÃ³n.

Ante nuevas vulnerabilidades (ej.

Log4Shell afectando a una librerÃ­a previamente segura), los sistemas de detecciÃ³n levantan alertas en tiempo real.

Pruebas periÃ³dicas anuales alineadas con los ciclos normativos.

Beneficios del DevSecOps
- ReducciÃ³n de riesgos : detecciÃ³n temprana de vulnerabilidades.
- Eficiencia operativa : automatizaciÃ³n que reduce tiempo y esfuerzo.
- Cumplimiento normativo continuo : la seguridad es parte del proceso, no un parche
final.
- Escalabilidad segura : ideal para entornos cloud y dinÃ¡micos.
- Mejora de calidad : el sello de â€œdesarrollo seguroâ€ es hoy uno de los mejores argumentos
de marketing para vender software.

Perfil profesional y salarios: un DevSecOps junior parte de 32 000-35 000 â‚¬/aÃ±o; un senior alcanza los 45 000-50 000 â‚¬.

Es uno de los perfiles mÃ¡s demandados gracias a las normativas. 4.

Servicio 3: FormaciÃ³n y ConcienciaciÃ³n de Empleados Por quÃ© el Red Team debe impartir la formaciÃ³n El profesor defiende que la formaciÃ³n en ciberseguridad debe ser impartida por perfiles ofensivos, no por Blue Teams teÃ³ricos, porque: - El Red Team ya realiza phishing, smishing, vishing y otras tÃ©cnicas de ingenierÃ­a social en sus auditorÃ­as diarias. - Puede diseÃ±ar ataques simulados reales, dirigidos y personalizados, haciendo caer a los empleados en la trampa. - La formaciÃ³n posterior, mostrando los resultados reales de la campaÃ±a de phishing sobre los propios empleados, tiene un impacto mucho mayor que cualquier presentaciÃ³n teÃ³rica. 4

### Caso real: el profesor y Carlos Castillo completaron una auditorÃ­a externa en seis minutos mediante ingenierÃ­a social, obteniendo credenciales vÃ¡lidas para acceder a la organizaciÃ³n.

Objetivos del servicio
- Aumentar la sensibilidad sobre amenazas digitales.
- Reforzar buenas prÃ¡cticas : no abrir correos fraudulentos, no conectar USBs
desconocidos, uso de contraseÃ±as robustas, etc.
- Cumplir normativas : formaciÃ³n periÃ³dica en ciberseguridad es un control exigido por
ISO 27001, ENS, NIS 2 y DORA.
- Construir una cultura de seguridad proactiva que convierta a los empleados en la
primera lÃ­nea de defensa, no en el eslabÃ³n mÃ¡s dÃ©bil.

El servicio se personaliza segÃºn el sector, el nivel de madurez de los empleados y los riesgos especÃ­ficos de la organizaciÃ³n. 5.

Cierre del mÃ³dulo de lÃ­neas de ciberseguridad Con esta sesiÃ³n concluye el bloque completo de lÃ­neas de ciberseguridad (Red Team, Blue Team y Purple Team).

La prÃ³xima sesiÃ³n abordarÃ¡ los tipos de hackers y, tras ello, se pasarÃ¡ definitivamente a la parte prÃ¡ctica del mÃ¡ster. 6.

Conceptos y tÃ©rminos clave corregidos TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n parper team / parpel team Purple Team “ equipo colaborativo entre Red y Blue Team equipo de decir / decir / de fir DeFIR (Digital Forensics and Incident Response) “ equipo de forense y respuesta ante incidentes fornse / fornise / forense digital Forense digital “ disciplina de investigaciÃ³n de evidencias digitales de secops / depth sec ops DevSecOps “ integraciÃ³n de seguridad en el ciclo de vida del desarrollo software de de box / de de ops DevOps “ metodologÃ­a de desarrollo y operaciones pipelines de c y cd Pipelines de CI/CD (Continuous Integration / Continuous Deployment ) “ integraciÃ³n y despliegue continuos sas / sars SAST (Static Application Security Testing ) “ anÃ¡lisis estÃ¡tico de seguridad de aplicaciones das / dust DAST (Dynamic Application Security Testing ) 5

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n “ anÃ¡lisis dinÃ¡mico de seguridad de aplicaciones sonar cube SonarQube “ herramienta de anÃ¡lisis estÃ¡tico de cÃ³digo blackdak / black duck Black Duck (Synopsys) “ herramienta de anÃ¡lisis de composiciÃ³n de software cover / coverity Coverity (Synopsys) “ herramienta de anÃ¡lisis estÃ¡tico avanzado checkmark Checkmarx “ escÃ¡ner de vulnerabilidades en cÃ³digo a yam / ayam IAM (Identity and Access Management ) “ gestiÃ³n de identidades y accesos yam / haces Referencias a YAML e IaC (Infrastructure as Code) “ infraestructura como cÃ³digo cÃ­clic haunting Threat Hunting “ bÃºsqueda proactiva de amenazas tiberegu TIBER-EU “ marco europeo de ejercicios de Red Team para banca y seguros mÃ­mica / mÃ­mica 100% Mimikatz “ herramienta de volcado de credenciales de memoria en Windows macrovirus Macro-virus “ malware embebido en documentos de Office cadena de custodio Cadena de custodia “ protocolo forense para garantizar la integridad de las evidencias vision querying sin 20 Vishing / Quishing / Smishing “ variantes de ingenierÃ­a social por voz, QR y SMS log 4g Log4Shell / Log4j “ vulnerabilidad crÃ­tica en librerÃ­a Java xdr XDR (Extended Detection and Response ) “ soluciÃ³n de detecciÃ³n y respuesta extendida FNS DeFIR o DFIR “ Digital Forensics and Incident Response (siglas usadas indistintamente) Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial “ Wolf Academy. 6
â†’
â†’
â†’
â†’
