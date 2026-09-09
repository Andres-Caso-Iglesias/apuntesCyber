> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 11**
> **Módulo:** MODULO2
> **Tema:** Clase 11
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 11. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Esta sesión cierra el módulo de OSINT y es la más práctica de todas las que lo componen. Gómez estructura la clase en tres bloques: reconocimiento facial con herramientas especializadas, un ejercicio real cronometrado donde a partir de un único número de teléfono hay que reconstruir el perfil completo de una persona, y un cierre rápido con Shodan, Censys y FOFA como herramientas de descubrimiento de superficie de exposición tecnológica. Al igual que en clases anteriores, el hilo conductor no son las herram ientas sino la metodología: iterar sobre la información disponible, descartar falsos positivos y conectar fuentes hasta llegar al objetivo.

| Reconocimiento facial: PimEyes y Yandex PimEyes | es la herramienta principal para búsqueda inversa de imágenes con r econocimiento facial. A diferencia de Google Lens, que busca la imagen como objeto, PimEyes está especializada en caras y tiene un histórico que puede remontarse años atrás. Su utilidad en OSINT es doble: confirmar que un perfil encontrado en LinkedIn u ot ra red pertenece realmente a la persona que investigamos, y descubrir presencias online antiguas que esa persona quizás ya no recuerda tener. Yandex Images | era hasta hace poco la herramienta más potente para este tipo de búsqueda, precisamente porque Rusia | no aplica el GDPR ni leyes equivalentes de protección biométrica. Su capacidad para reconocer escenarios, edificios y contextos más allá de caras la hacía especialmente útil para geolocalización de imágenes. En el momento de esta clase, Yandex ha empezado | a restringir esta funcionalidad para usuarios de fuera de Rusia, por lo que su fiabilidad es variable. La combinación de ambas herramientas sobre la misma imagen puede dar resultados diferentes: una foto reconocida en PimEyes puede no aparecer en Yandex y | viceversa, por lo que se recomienda usar las dos. |
|---|---|---|---|---|---|
- Si en la investigación de una persona aparecen múltiples resultados en dominios rusos o de
países con poca regulación de datos, eso es un hilo del que tirar. Puede indicar actividad pasada que la persona n o ha limpiado, registros en foros o plataformas que desconoce, o simplemente que sus datos fueron parte de una filtración que acabó en esos repositorios

| El ejercicio práctico: de un número de teléfono al DNI El ejercicio propuesto es un caso real: a parti r de un único número de teléfono, sacar nombre completo, empleo actual, cinco trabajos anteriores, precio por hora en al menos uno de ellos, deporte practicado, alias o nickname, y número de DNI. Todo pasivo, todo fuentes abiertas, veinticinco minutos. El write -up que desarrolla Gómez al final muestra el flujo completo: Paso 1 — Del teléfono al nombre: | TrueCaller (bot de Telegram) devuelve el primer apellido asociado al número. No es un nombre común, lo que reduce exponencialmente los falsos positivos. Paso | 2 — Del nombre al perfil completo: | búsqueda en Google del nombre parcial. Al ser poco común aparece directamente el perfil de LinkedIn con nombre completo, empleo actual y trayectoria profesional. El segundo apellido se confirma en varias fuentes cruzadas . Paso 3 — Iteraciones de búsqueda: | los resultados de Google cambian significativamente según si se usa el nombre con tildes y mayúsculas correctas, si se invierte el orden nombre -apellidos, o si se |
|---|---|---|---|---|

| añaden términos contextuales. Cambiar el orden a apellido s-nombre descubre resultados que la búsqueda directa no mostraba. Paso 4 — Del nombre al correo: | Bridge.vip | y OpenSense devuelven posibles correos asociados al nombre. El correo también aparece en la secció n de contacto del perfil de LinkedIn. Paso 5 — Del correo a las brechas: | Have I Been Pwned confirma si el correo aparece en filtraciones conocidas. LeakRadar permite ver las credenciales filtradas con suscripción. Paso 6 — El deporte: | búsqueda en Google de l nombre con el término UPM (Universidad Politécnica de Madrid, detectada como vínculo recurrente en los resultados) lleva a la Federación Madrileña de Natación. Allí aparece en resultados de competición de waterpolo. Paso 7 — El DNI: | la Federación tiene P DFs de competición con listados de participantes que incluyen fragmentos del número de documento. Combinando los dígitos encontrados en diferentes documentos y buscando con Google Dorks (filetype:pdf "González Parrilla") se reconstruye el número completo. La letra del DNI se calcula mediante el algoritmo público de validación de DNI español. Paso 8 — El alias: | la herramienta de username pivot (WhatsMyName o Maigret) lanzada sobre el correo o el nombre devuelve presencia en Xbox con un alias concreto, que a su vez se puede seguir investigando. Flujo resumido: Teléfono → TrueCaller → Nombre parcial Nombre parcial → Google → Nombre completo + LinkedIn LinkedIn → Empleo actual + historial + correo Nombre + UPM → Federación deportiva → Waterpolo + fragmentos DNI Google Dorks (filetype:pdf) → DNI completo Correo → WhatsMyName → Alias Correo → LeakRadar → Credenciales filtradas |
|---|---|---|---|---|---|---|
> [!important] - La idea clave: este ejercicio no requiere ninguna herramienta de pago, ningún acceso
| privilegiado y ninguna interacción con el objetivo. Todo está en fuentes abiertas. La diferencia entre tardarlo veinticinco minutos o tres horas está en conocer el ciclo de inteligencia | y saber qué buscar con qué herramienta en cada momento |
|---|---|

> [!important] | Huella digital: el problema de ser público La demostración en clase deja claro algo importante: cuanta más actividad pública tiene una persona, más fácil es construir su perfil completo. En este caso , el objetivo tiene libros publicados, perfiles en universidades, actas de federaciones deportivas, páginas de empresa con datos de contacto, y presencia en múltiples plataformas. Todo eso, que individualmente es inofensivo, combinado permite reconstruir d esde el número de teléfono hasta el DNI en menos de media hora. El derecho al olvido digital | existe en el marco del GDPR y permite solicitar la eliminación de datos de plataformas y motores de búsqueda. Sin embargo, su aplicación es fragmentada: se puede eliminar de Google, pero no del servidor donde está almacenado el dato original, y si ese servidor vuelve a publicarlo, el proceso empieza de nuevo. |
|---|---|

Shodan, Censys y FOFA: buscadores de tecnología

| Estos tres motores de búsqueda no indexan texto de páginas web, sino tecnologías, servicios, versiones de software y dispositivos expuestos a Internet. Son la herramienta natural para completar el mapeo de superficie de exposición de una organización más allá de sus dominios y subdominios. La diferencia con Google | es fundamental: si busco Windows Server 2008 en Google, obtengo artículos sobre Windows Server 2008. Si lo busco en Shodan, obtengo más de 300.000 servidores reales con esa versión expuestos a Internet, con su IP, sus puertos abiertos y las vulnerabilidad es conocidas asociadas. |
|---|---|

# Búsquedas útiles en Shodan

| Windows Server 2008 | → servidores vulnerables a EternalBlue (MS17 -010) apache 2.2 | → versiones con vulnerabilidades conocidas "default password" | → dispositivos con credenciales por defecto org:"Repsol" | → activos de una organización concreta port:21 anonymous | → servidores FTP con acceso anónimo Un concepto nuevo que introduce Shodan recientemente: la marcación de honeypots . Un honeypot es un servidor deliberadamente vulnerable puesto en Internet para atraer atacantes y estudiar sus técnicas. Se detectan porque tienen un número anormalmente alto de puertos abiertos y vulnerabilidades que no tiene ningún servidor real en producción. Atacar un honeypot no | solo es inútil, sino que revela las herramientas y técnicas del atacante a quien lo opera. |
|---|---|---|---|---|---|---|
- FOFA (chino) y Censys cubren rangos de dispositivos e IPs diferentes a los de Shodan.
Buscar el mismo objetivo en los tres y comparar resultados muestra que cada un o indexa activos que los otros no tienen. La superficie de exposición real es la unión de los tres

Recapitulación integrada del módulo OSINT Al cerrar este módulo, somos capaces de construir un perfil completo de una persona o una organización partiendo d e casi cualquier dato inicial: un número de teléfono, un correo, un username o un dominio. Sabemos que el OSINT es siempre pasivo, que la calidad del resultado depende de aplicar el ciclo de inteligencia con objetivos precisos, y que los falsos positivos s on inevitables y deben filtrarse con criterio analítico, no con herramientas. La próxima sesión abre el módulo de redes, que es la base técnica necesaria para entender todo lo que viene después: Wireshark, ataques de red, y eventualmente el movimiento late ral dentro de una infraestructura comprometida.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — Empleabilidad, Nmap, OSINT
- [[../../apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red.md|Redes-Tipologías, Datagramas y Paquetes de Red]] — Nmap, OSINT, Windows
- [[../../Apuntes/01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Nmap, OSINT, Redes
- [[../../apuntes evolve/BLOQUE 14.md|BLOQUE 14]] — Empleabilidad, Normativa / GRC, OSINT
- [[../../transcripciones/Julio/29.07.2026 Presentación Práctica 1.md|29.07.2026 Presentación Práctica 1]] — Empleabilidad, IA en Ciberseguridad, Windows
- [[../../Apuntes/15 - Certificaciones/Certificaciones - ISO 27001 y eJPTv2.md|Certificaciones - ISO 27001 y eJPTv2]] — Nmap, OSINT, Windows

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Nmap|Nmap]]

> #empleabilidad #google-dorks #ia #nmap #normativa #osint #pentest #redes #windows #wireshark
