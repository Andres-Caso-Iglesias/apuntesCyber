> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 2**
> **Módulo:** PREWORK
> **Tema:** Clase 2
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 2. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 2: Historia de la Ciberseguridad (Continuación) y Ciberseguridad Moderna Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: la globalización de Internet como punto de inflexión La clase arranca retomando el hilo de la sesión anterior y situando el auge de Internet como el mayor catalizador de la ciberseguridad moderna.

Sin Internet no existirían la educación online, la interconexión global ni, en consecuencia, la mayoría de los ataques que se estudian hoy.

Se invita a reflexionar sobre la seguridad de los dispositivos IoT, anticipando que serán una de las superficies de ataque más relevantes para los auditores del futuro. 2.

Década de 1990 – La era de Internet y las primeras amenazas masivas Ingeniería social y phishing Con la popularización de Internet aparece la ingeniería social y, concretamente, el phishing.

Se estima que esta técnica está detrás del 80 % de los accesos no autorizados registrados hasta la fecha.

El usuario doméstico de 1990, sin ninguna cultura de seguridad digital, era el objetivo perfecto: una llamada falsa de Microsoft o un correo de suplantación de identidad resultaban irresistibles para quien nunca había oído hablar de estafas digitales.

Se subraya que, décadas después, millones de usuarios siguen cayendo en estas mismas trampas, lo que demuestra que la concienciación sigue siendo uno de los retos más grandes del sector.

Ataques de Denegación de Servicio (DoS/DDoS) Junto al phishing aparece el ataque de denegación de servicio : si no puedo robar tus datos, al menos puedo dejar tu servicio fuera de línea.

Se describen usos concretos: competencia entre tiendas de comercio electrónico, guerra de audiencias entre medios digitales, etc.

En 1990 no existían tecnologías anti-DDoS ni balanceadores de red modernos como Cloudflare, por lo que la defensa era prácticamente inexistente.

Los zero-days y el límite de la seguridad perfecta Se introduce el concepto de zero-day: vulnerabilidades desconocidas presentes en cualquier 1

tecnología (software, librerías, firmware de sensores IoT) que nadie ha analizado previamente.

Dado que existen millones de tecnologías y los recursos para auditarlas son limitados, siempre habrá vulnerabilidades sin descubrir.

Quien encuentre un zero-day tiene dos opciones:
- Reportarlo responsablemente al fabricante a cambio de reconocimiento y un CVE
(Common Vulnerabilities and Exposures ).
- Venderlo en el mercado negro (dark web) por cifras millonarias.

### Ejemplo destacado: la librería Log4Shell (Log4j), que estuvo activa durante 11 años antes de ser descubierta en 2021.

Aparición de los primeros firewalls En 1990 nacen también los primeros firewalls (cortafuegos) comerciales, la primera barrera real de defensa perimetral para redes domésticas y empresariales.

Malware Michelangelo (1992) El virus Michelangelo (1992) representó un salto cualitativo en cuanto al impacto sobre los datos de los usuarios, consolidando la tendencia de que cada generación de malware es más dañina que la anterior. 3.

Década de 2000 – La ciberseguridad moderna toma forma Grupos criminales organizados Igual que las mafias tradicionales se organizan en estructuras con roles especializados, aparecen los primeros grupos organizados de ciberdelincuentes .

Comercializan datos bancarios robados, comparten herramientas y malware, y se dividen tareas, lo que multiplica exponencialmente su eficacia frente a defensores individuales.

### Ataques masivos: I Love You y Blaster Los virus I Love You (2000) y el gusano Blaster (2003) infectaron por primera vez millones de dispositivos en todo el mundo en un solo ataque, marcando el inicio de las amenazas globales a gran escala.

Hacktivismo y Anonymous Surgen los primeros hacktivistas: individuos y colectivos que usan el hacking como herramienta de protesta o reivindicación política, sin motivación económica directa.

El profesor señala que los actores ideológicos son particularmente peligrosos porque no tienen límite económico que los detenga. 2

Anonymous merece un análisis propio:
- No es un grupo cerrado, sino una bandera o sentimiento : cualquiera puede firmar sus
acciones bajo ese nombre.
- Esto explica por qué se han visto acciones de Anonymous en bandos opuestos de un
mismo conflicto (ej. conflicto Israel-Palestina, Ucrania-Rusia).
- Sí existen grupos españoles autoproclamados que operan bajo esa bandera (conocidos
como “los 7, 8 o 9 de Anón”), pero son grupos voluntariamente cerrados, no la esencia del colectivo.

> [!important] ### Marco legislativo: Sarbanes-Oxley y el RGPD Aparecen regulaciones clave:

- Ley Sarbanes-Oxley (EE.

UU., 2002): control financiero y responsabilidad corporativa.
- RGPD (Reglamento General de Protección de Datos , Europa): norma vigente que regula
el tratamiento de datos personales y establece las multas que hoy utilizan los grupos de ransomware como palanca de extorsión.

Hasta 2002 muchos ataques de robo y espionaje de datos quedaron completamente impunes por ausencia de marco legal aplicable. 4.

Década de 2010 – La ciberseguridad como asunto geopolítico Stuxnet: la guerra digital El gusano Stuxnet (2010), presuntamente desarrollado por Estados Unidos e Israel, fue el primer ciberarma conocida dirigida a infraestructura física: atacó las centrifugadoras del programa nuclear iraní.

A partir de este momento los gobiernos empiezan a crear sus propios ciberejércitos e inyectan grandes presupuestos en operaciones ofensivas y defensivas.

Se señalan ejemplos de daño físico a través de ataques digitales: manipulación de gasoductos, sabotaje de cadenas de montaje, alteración de paneles solares o molinos eólicos, o modificación de parámetros de frenado en vehículos.

WannaCry y EternalBlue (2017) WannaCry fue el mayor ataque de ransomware conocido hasta la fecha.

Explotó la vulnerabilidad EternalBlue, una herramienta de espionaje de la NSA (National Security Agency ) de EE.

UU. que fue robada y filtrada por el grupo Shadow Brokers.

Afectó a organizaciones de todo el mundo, incluida Telefónica en España.

> [!important] ### Puntos clave:

- EternalBlue permitía RCE (Remote Code Execution ) con privilegios de administrador en
sistemas Windows sin parchear, llegando hasta el Active Directory. 3
- Todavía en 2024 se encuentran servidores Windows 2003/2008 R2 sin parchear en redes
corporativas internas, lo que convierte esta vulnerabilidad en algo muy vigente.
- EternalBlue habría sido utilizada por la NSA para espionaje masivo desde
aproximadamente 2015, sin conocimiento público.

Pegasus: el espionaje sin interacción Pegasus es un malware de espionaje móvil desarrollado por NSO Group (empresa privada israelí), capaz de instalarse en cualquier dispositivo con una simple llamada perdida, sin ninguna interacción por parte de la víctima.

Su precio de adquisición era de 6 millones de dólares , con soporte 24/7.

Fue empleado en espionajes a figuras como Jeff Bezos, Elon Musk y líderes políticos en múltiples países, incluyendo España.

Botnet Mirai y el peligro del IoT La Botnet Mirai demostró el peligro extremo de los dispositivos IoT al infectar masivamente cámaras de seguridad, routers y electrodomésticos conectados utilizando únicamente credenciales por defecto .

Su fuerza no residía en la potencia de cada dispositivo, sino en el volumen: millones de dispositivos con mínimo ancho de banda individual generan un tráfico DDoS devastador de forma exponencial.

Ejemplos reales mencionados por el profesor:
- Hackeo de un casino de Las Vegas a través del termostato de una pecera .
- Ataques a través de lavadoras que usaron EternalBlue para comprometer redes internas.
- Acceso a cámaras de vigilancia de bebés.

En 2024, la botnet Mirai está experimentando un resurgimiento porque la producción de dispositivos IoT crece exponencialmente mientras su seguridad permanece prácticamente nula (coste de producción de 3 euros por unidad = inversión en seguridad: cero).

Inteligencia Artificial y Machine Learning En la década de 2010 el Machine Learning comienza a aplicarse en ciberseguridad para la detección de amenazas en tiempo real.

Sin embargo, las mismas herramientas sirven para los atacantes: deepfakes en tiempo real, clonación de voz, suplantación de número de teléfono o generación de textos personalizados para phishing, todo con un solo clic. 5.

Década de 2020 – La ciberseguridad en el centro COVID-19 y la expansión del teletrabajo La pandemia aceleró la transformación digital y disparó los ciberataques.

Las empresas abrieron masivamente VPNs, accesos RDP (Remote Desktop Protocol ) y soluciones de acceso remoto sin 4

securizar correctamente.

V olvieron vulnerabilidades ya extintas como BlueKeep, que explota el protocolo RDP para acceder a equipos sin autenticación.

Ataques a la cadena de suministro: SolarWinds El ataque a SolarWinds (2020) es el ejemplo paradigmático: al comprometer la plataforma de gestión IT de SolarWinds, los atacantes accedieron a los sistemas de cientos de empresas y agencias gubernamentales en todo el mundo.

Este tipo de ataque dio origen a las normativas actuales más exigentes:
- ISO/IEC 27001 (revisada)
- Esquema Nacional de Seguridad (ENS)
- NIS 2 (Directiva europea)
- DORA (sector financiero europeo)
Arquitectura de Confianza Cero (Zero Trust) Frente a la imposibilidad de confiar en ningún elemento de la red, surge el modelo Zero Trust: verificación continua de identidad y permisos para cada usuario, servicio y dispositivo, limitando al máximo las acciones posibles dentro de la red.

Se profundizará en este modelo en la línea de Blue Team del máster.

La Pyme como objetivo preferente El 86 % de las pymes que sufrieron un ataque en el último año tuvieron que cerrar.

Las pymes son objetivo preferente precisamente porque no pueden afrontar grandes inversiones en seguridad.

Sin embargo, el profesor aclara que para proteger a una pyme no se necesitan auditorías complejas, sino aplicar buenas prácticas básicas , ya que su infraestructura raramente es atacada mediante zero-days sofisticados. 6.

### Ciberseguridad moderna: conclusiones y líneas de especialización La sesión cierra con un resumen visual de la evolución de la ciberseguridad desde Creeper/Reaper hasta la actualidad, destacando cómo la globalización de Internet y la entrada del sector militar-gubernamental en el ciberespacio han convertido la ciberseguridad en:

- Un negocio de venta de servicios de seguridad gestionada.
- Una responsabilidad ética y profesional de primer orden.
- Un campo con hiperespecialización necesaria (Red Team, Blue Team, Purple Team,
GRC, entre otros).

La próxima sesión abordará en detalle las diferentes líneas de la ciberseguridad y sus funciones concretas, para que cada alumno pueda orientar su carrera profesional. 5

## 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración botnet Mirei Botnet Mirai – botnet masiva basada en dispositivos IoT CVS CVE (Common Vulnerabilities and Exposures ) – identificador estándar de vulnerabilidades Lock4G Log4Shell / Log4j – vulnerabilidad crítica en la librería Apache Log4j (2021) Vista (gusano 2003) Blaster – gusano de 2003 que afectó a millones de equipos Windows NSA (empresa israelí) NSO Group – empresa privada israelí creadora de Pegasus (distinta de la NSA estadounidense) Transunware Ransomware – software de secuestro y cifrado de datos WebSphere de Java Probable referencia a vulnerabilidades en Log4j (librería Java) o en Apache Struts Vedrola / Enaga Iberdrola y Enagás – empresas energéticas españolas afectadas por la vulnerabilidad de Fortinet NIDS o Team Bware TeamViewer / AnyDesk – herramientas de acceso remoto corporativo CHAP GPT ChatGPT – modelo de lenguaje de OpenAI jactivismo Hacktivismo – uso del hacking como activismo político o social Blueteam / Redteam Blue Team / Red Team – equipos de defensa y ataque en ciberseguridad Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_clase6.md|resumen_clase6]] — Netcat / Reverse Shells, Normativa / GRC, Post-Explotación
- [[resumen_clase7.md|resumen_clase7]] — Netcat / Reverse Shells, Normativa / GRC, Post-Explotación
- [[resumen_clase12.md|resumen_clase12]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../MODULO1/resumen_master_clase6.md|resumen_master_clase6]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../MODULO2/resumen_master_clase9.md|resumen_master_clase9]] — Netcat / Reverse Shells, Normativa / GRC, Post-Explotación
- [[resumen_clase13.md|resumen_clase13]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #blue-team #command-injection #ia #netcat #normativa #post-explotacion #redes #reverse-shell #windows
