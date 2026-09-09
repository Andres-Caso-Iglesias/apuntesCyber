> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 16**
> **Módulo:** MODULO2
> **Tema:** Clase 16
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 16. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

Esta sesión la imparte Carlos Castillo y es la primera clase completamente práctica del módulo de redes. Todo lo aprendido sobre protocolos, capas OSI, TCP/UDP y el modelo conceptual de Wireshark tiene aquí su traducción directa a un escenario real: un analista de seguridad que recibe una captura de red y tiene que reconstruir qué ha ocurrido. La clase usa la plataforma **CyberDefenders** como entorno de laboratorio, el equivalente de HackTheBox para perfiles defensivos y Blue Team, y trabaja dos ejercicios completos: uno de movimiento lateral con SMB y otro de SQL Injection sobre tráfico HTTP.

**CyberDefenders: laboratorio de Blue Team**

La plataforma [cyberdefenders.org](http://cyberdefenders.org/) permite practicar análisis forense de red, análisis de logs y respuesta a incidentes con escenarios reales. El flujo es siempre el mismo: descargar los ficheros del laboratorio (protegidos con contraseña), abrirlos con Wireshark, y responder preguntas que simulan un proceso de investigación real. Es gratuita y funciona exactamente igual que HackTheBox, solo que en lugar de comprometer máquinas el objetivo es reconstruir ataques ya ocurridos.

**Metodología inicial de análisis de una captura**

Cuando se recibe un fichero PCAP con decenas de miles de paquetes, leerlos uno a uno no es viable. La metodología correcta empieza siempre por una visión macro antes de entrar en el detalle.

**Paso 1 --- Jerarquía de protocolos**

Estadísticas → Protocol Hierarchy muestra qué porcentaje de los paquetes corresponde a cada protocolo, organizado jerárquicamente. De un vistazo se puede determinar el tipo de entorno y los vectores de ataque probables:

- Si predomina **TCP** (99%+), estamos en un entorno IT empresarial
- Si predomina **UDP**, podemos estar en entorno industrial OT o ante streaming
- La presencia de **SMBv2** sobre TCP indica intercambio de ficheros Windows
- La presencia de **HTTP** indica tráfico web sin cifrar, analizable en texto claro

Además, revisar la proporción de bytes por protocolo permite detectar transferencias anómalas: pocos paquetes pero muchos bytes puede indicar exfiltración de datos.

**Paso 2 --- Conversaciones**

Estadísticas → Conversaciones → IPv4 muestra qué pares de IPs han hablado entre sí, cuántos paquetes han intercambiado y en qué dirección fluye más tráfico. Un desequilibrio grande en bytes revela el rol de cada actor: si B envía muchos más bytes a A de los que recibe, B está sirviendo datos a A. En un incidente, eso orienta hacia exfiltración o hacia command and control.

> [!important] - **La idea clave:** antes de mirar un solo paquete, la jerarquía de protocolos y las conversaciones ya dicen qué protocolos están involucrados, quiénes son los actores y cuál de ellos inicia la actividad. Eso reduce los ochenta mil paquetes a dos o tres conversaciones relevantes

**Ejercicio 1: PSEXEC Lateral Movement (SMB)**

El primer laboratorio analiza un movimiento lateral realizado mediante **PSEXEC** sobre **SMB**. Este es uno de los patrones de ataque más comunes en entornos Windows corporativos.

**Qué es SMB y por qué importa:** SMB (Server Message Block) es el protocolo de Windows para compartir carpetas y ficheros en red. Las carpetas compartidas se llaman **shares**. Por defecto, cualquier sistema Windows tiene dos shares administrativos: IPC\$ (para comunicación de red y enumeración) y ADMIN\$ (acceso administrativo al sistema). Si un atacante tiene credenciales válidas, puede acceder a estos shares y ejecutar código remotamente.

**Qué es PSEXEC:** herramienta legítima de Microsoft incluida en Sysinternals que permite ejecutar comandos en equipos remotos mediante autenticación. Los administradores de sistemas la usan para gestión remota; los atacantes la usan para movimiento lateral. Cuando se ejecuta, despliega un servicio temporal en la máquina víctima (PSEXESVC.exe) que actúa como intermediario.

**Análisis de la captura:**

La jerarquía de protocolos muestra 99,9% TCP con SMBv2 como subprotocolo dominante, confirmando entorno IT Windows. Las conversaciones muestran que 10.0.0.130 tiene la actividad más intensa hacia 10.0.0.133 (38.000+ paquetes), lo que la señala como origen del ataque.

Siguiendo los paquetes en orden se reconstruye la secuencia completa del ataque:

- Negociación SMB: ¿Qué versión usamos? → SMBv2
- Autenticación NTLM: usuario \"sales\" se autentica contra 10.0.0.133
- Conexión al share IPC\$ → enumeración de interfaces de red
- Conexión al share ADMIN\$ → subida del ejecutable PSEXESVC.exe
- Cambio a TCP puro: ejecución remota de comandos

En el paquete de autenticación NTLM hay un campo Target Name que contiene el hostname de la máquina víctima: SALES-PC. Este campo aparece siempre en la fase de challenge/response previa a la autenticación, que existe porque TCP requiere ese intercambio antes de establecer la sesión. UDP no hace este challenge, por eso SMBv1 sobre UDP no revela hostname ni usuario.

| Resultados del laboratorio: IP atacante: | 10.0.0.130 Hostname víctima: | SALES-PC (del campo NTLM Target Name) Usuario comprometido: sales | (del campo NTLM user) Shares accedidos: | IPC$ → ADMIN$ Ejecutable desplegado: PSEXESVC.exe Segundo pivote: | MARKETING-PC |
|---|---|---|---|---|---|

> [!important] - **La idea clave:** el protocolo NTLM, al requerir un challenge/response previo a la autenticación, deja en los paquetes el hostname y el usuario que se está autenticando. Esos datos son la huella que permite al analista reconstruir quién comprometió qué y en qué orden

**Ejercicio 2: Web Investigation (SQL Injection)**

El segundo laboratorio analiza un ataque web. La jerarquía de protocolos muestra HTTP como protocolo dominante (93,9%), confirmando tráfico web sin cifrar analizable directamente.

**Exportar objetos HTTP**

Archivo → Exportar objetos → HTTP reconstruye todos los ficheros que han viajado por la red: páginas HTML, CSS, imágenes y, crucialmente, todas las peticiones GET con sus parámetros. Permite ver el comportamiento de navegación completo del atacante sin necesitar filtros complejos.

**Identificar al atacante**

Filtrando las conversaciones IPv4 se identifican dos actores principales: la IP 73.124.22.98 (servidor web, recibe GETs) y la IP 111.224.250.131 (cliente, hace peticiones). Como un servidor web no ataca a un cliente, el atacante es el cliente.

Para filtrar solo su actividad:

ip.src == 111.224.250.131

**Decodificación URL y detección del ataque**

Los caracteres especiales en URLs se codifican con %XX. Los más relevantes en ataques web son %27 (comilla simple) y %20 (espacio). La comilla simple es el carácter que cierra cadenas en SQL y puede romper la lógica de una consulta.

El patrón que delata el ataque es siempre el mismo: navegación normal primero (GET a index, categorías, búsquedas legítimas) seguida de búsquedas con caracteres especiales. Cuando aparece %27 en los parámetros y el servidor responde con un 500 Internal Server Error, la vulnerabilidad está confirmada: la aplicación no sanitiza la entrada antes de incluirla en la consulta SQL.

**Cómo funciona la inyección**

Una query SQL de buscador selecciona registros donde el nombre coincide con el valor introducido por el usuario. Si el usuario introduce una comilla simple, rompe la sintaxis y el motor SQL no puede procesar la instrucción: error 500.

Para explotar esto, el atacante introduce un payload que cierra la comilla del parámetro e introduce una condición adicional con OR que siempre es verdadera. Como OR devuelve verdadero si al menos uno de sus operandos lo es, y la segunda condición siempre se cumple, la query devuelve todos los registros de la tabla en lugar del libro pedido. Los dos guiones al final actúan como comentario SQL y anulan todo lo que venga después.

A partir del primer 200 OK tras un payload con caracteres especiales, el atacante usa **SQLMap** (herramienta que automatiza cientos de payloads) para enumerar el esquema de la base de datos. La tabla information_schema contiene la estructura de todas las bases de datos del servidor y es siempre el primer objetivo de enumeración.

- **La metáfora útil:** un buscador web que no sanitiza entradas es como una caja de sugerencias donde en vez de escribir una queja escribes un comando que dice \"dime también el contenido de todos los archivos del edificio\". La aplicación no distingue entre datos y comandos, así que obedece
> [!important] - **La idea clave:** en una captura HTTP, un 500 Internal Server Error justo después de una petición con %27 en los parámetros es casi siempre SQL Injection. No hace falta decodificar nada para detectarlo, basta con ver el par petición-respuesta

**Recapitulación integrada**

Al cerrar esta sesión hemos convertido en práctica real todo el marco teórico de las semanas anteriores. Sabemos que lo primero ante un PCAP es la jerarquía de protocolos y las conversaciones, no el análisis paquete a paquete. Sabemos leer un intercambio SMB y localizar en los paquetes NTLM el hostname y el usuario comprometido. Sabemos que HTTP en texto claro permite exportar objetos y reconstruir toda la actividad web, y que una comilla simple en los parámetros de búsqueda seguida de un 500 es la firma de una SQL Injection en curso. La próxima sesión continúa con más laboratorios de forense de redes, y en paralelo arranca ya la fase activa con Metasploitable: enumeración de servicios y las primeras explotaciones reales.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Julio/23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes.md|23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]] — IA en Ciberseguridad, SQLMap, Windows
- [[../../Apuntes/12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Post-Explotación, SMB / Impacket, Windows
- [[../../comandos/SQLMap.md|SQLMap]] — IA en Ciberseguridad, SQLMap, Windows
- [[../../apuntes Chema/IA/IA — De los cimientos a la cima.md|IA — De los cimientos a la cima]] — IA en Ciberseguridad, SQLMap, Windows
- [[../../apuntes evolve/BLOQUE 11.md|BLOQUE 11]] — SMB / Impacket, SQL Injection, Windows
- [[../MODULO3/resumen_master_clase18.md|resumen_master_clase18]] — IA en Ciberseguridad, SQL Injection, SQLMap

### 🛠️ Herramientas

- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #blue-team #forense #hack-the-box #ia #metasploitable #pentest #post-explotacion #redes #smb-impacket #sqli #sqlmap #windows #wireshark
