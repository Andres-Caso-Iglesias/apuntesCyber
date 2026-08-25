> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 14**
> **Módulo:** MODULO2
> **Tema:** Clase 14
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 14. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Esta sesión la imparte Yuba González y conecta directamente con los fundamentos de redes que vimos con Carlos Gómez en la clase anterior. Si allí aprendimos qué son las IPs, los puertos y los protocolos, hoy construimos el modelo mental que organiza todo eso en capas. La diferencia de enfoque de Yuba es deliberada: en lugar de memorizar una pirámide de siete niveles, el objetivo es entender por qué existe cada capa y qué puede hacer un atacante en ella. La idea central que vertebra toda la clase es que cad a capa tiene su propia responsabilidad y, por tanto, su propio conjunto de vulnerabilidades.

| Por qué existe el modelo OSI y por qué importa al atacante La pregunta que abre la clase: ¿cómo es posible que un ordenador en Madrid se comunique con un servidor | en Tokio, pasando por veinte máquinas de fabricantes distintos, usando un cable que no entiende ningún idioma, y que el mensaje llegue completo, en orden y cifrado? La respuesta es que existen reglas comunes organizadas en capas. Eso es el modelo OSI. Hay dos versiones del modelo: el OSI, con siete capas, y el TCP/IP, con cuatro o cinco según quien lo cuente. TCP/IP es lo que realmente corre en Internet, pero el OSI es el modelo conceptual con el que se piensa en ciberseguridad, porque su mayor granularida d hace más fácil razonar sobre ataques y defensas. Las tres reglas fundamentales del modelo: |
|---|---|
- Cada capa tiene su propia responsabilidad y su propio conjunto de vulnerabilidades
- Una capa solo habla con su capa equivalente en el otro extremo de la comunicació n
- Si una capa está bien protegida, casi siempre hay otra capa por encima o por debajo que no
lo estará La consecuencia práctica de la segunda regla: para atacar la capa dos hay que estar en la red local. Para atacar la capa siete se puede hacer desde cualq uier parte del mundo.
> [!important] - La idea clave: una red no se ataca de un solo modo, se ataca por capas. Y para defender, se
hace exactamente igual. Si la defensa no piensa por capas, siempre habrá una que quede expuesta

| Capa 1 — Física La capa física mueve bits. No | entiende de IPs, contraseñas ni aplicaciones, solo de voltajes, pulsos de luz y ondas de radio. Su analogía: una carretera que aguanta el peso y deja pasar sin importarle qué va encima. Para atacarla se necesita presencia local. Si un atacante controla es ta capa, controla todo lo que va encima. Los vectores principales: |
|---|---|
- Cable tapping: dispositivos insertados entre el switch y el firewall que copian todo el
tráfico pasante, sin levantar ninguna alerta lógica
- USB dropping / BadUSB: pendrives abandonados en a parcamientos o cafeterías de
empresa que, al conectarse, se hacen pasar por teclados y ejecutan comandos automáticamente
- Keyloggers hardware: dispositivos conectados entre el teclado y el ordenador que capturan
cada tecla; ningún antivirus los detecta porq ue son un cable con memoria
- Captura de radiofrecuencia: cualquier antena puede recibir las emisiones WiFi, Bluetooth
| o IoT que emiten los dispositivos Contramedidas: seguridad física, puertos de red deshabilitados por defecto, formación a empleados para no | conectar USBs desconocidos, detectores de anomalías en el cableado. |
|---|---|

| Capa 2 — Enlace de datos La capa de enlace organiza las conversaciones dentro de una red local. Aquí aparece la dirección MAC , un identificador único grabado en cada tarjeta de red. Si l a capa tres es el edificio (la IP), la capa dos es el conserje que sabe quién está en qué habitación. El protocolo ARP | (Address Resolution Protocol) es el puente entre IPs y MACs. Funciona así: cuando un dispositivo quiere comunicarse con una IP que no con oce, grita en modo broadcast a toda la red local preguntando quién tiene esa IP. El dueño responde con su MAC y esa relación se guarda en caché local. |
|---|---|
```bash
```

| arp -a | # Ver la tabla ARP local: correlación IP → MAC El problema de ARP es que nadie verifica que quien responde sea realmente el dueño legítimo. Esa confianza ciega es la base de los ataques de esta capa: |
|---|---|
- ARP Spoofing / ARP Poisoning: el atacante responde a peticiones ARP diciendo ser el
router. A partir de ese momento, todo el tráfico de la red p asa por su máquina antes de llegar al destino real. Esto es un Man in the Middle (MitM)
- MAC Spoofing: cambiar la dirección MAC del propio equipo para suplantarse por otro
dispositivo ya registrado, saltando mecanismos de control basados en listas blancas d e MACs (portales cautivos de hoteles, hospitales, etc.)
```bash

# Cambiar la MAC con macchanger

ifconfig eth0 down
```

| macchanger -m 22:22:22:22:22:22 eth0 ifconfig eth0 up macchanger -s eth0 | # Ver MAC actual vs permanente |
|---|---|
- VLAN Hopping: si las VLANs están mal configuradas, un atacante puede etiquetar tramas
para saltar de una red virtual a otra, rompiendo la segmentación lógica
- Rogue Access Point: crear un punto WiFi falso al que se conectan los dispositivos
automáticamente, capturando su tráfico Herramientas d e esta capa: macchanger , aircrack -ng, bettercap , Wireshark .
- La metáfora útil: ARP confía en que solo Alejandro levantará la mano cuando preguntes
por él en la sala. El ARP Spoofing es el atacante que levanta la mano haciéndose pasar por Alejandro

| Capa 3 — Red La capa de red es la responsable de que un paquete cruce redes distintas para llegar a su destino. Aquí viven las direcciones IP | y el protagonista es el router , que decide paquete a paquete por qué camino enviarlo. Una dirección IPv4 son 32 bits organizados en cuatro octetos. Cada octeto va del 0 al 255. El espacio total es de algo más de 4.300 millones de direcciones, insuficiente para todos los dispositivos existentes, de ahí la necesidad de IPv6 (128 bits, espacio prácticamente ilimitado). No todas las IPs son iguales. Los tres rangos privados reservados para redes locales no se enrutan por Internet: 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 El rango 127.0.0.0/8 ( localhost ) tampoco es enrutable exte rnamente. Esto tiene consecuencias directas en auditoría: escaneando Internet nunca se encontrarán dispositivos con estas IPs. Para llegar a ellos hay que estar dentro de la red o haber comprometido algo que sí sea accesible. Las IPs públicas las asignan l os operadores en bloques llamados ASNs . Identificar qué rangos de IPs pertenecen a un cliente es parte de la fase de reconocimiento en auditorías externas. Vectores ofensivos de capa tres: |
|---|---|
- IP Spoofing: falsificar la IP origen, usado principalmente en ataques de denegación de
servicio
- Escaneo de red con Nmap: identificar dispositivos activos, puertos abiertos y versiones de
servicios
```bash
```

| nmap -sV -vvv -Pn 192.168.1.0/24 | # Escaneo de red con detección | de versiones traceroute google.com | # Ver los saltos hasta el destino Contramedidas: firewalls que filtran IPs por origen y destino, segmentación de red, monitorización de tráfico ICMP. |
|---|---|---|---|

Capa 4 — Transporte La capa de transporte decide cómo s e transportan los datos y asigna un número de puerto, que es la forma de identificar qué servicio dentro de una máquina debe recibir cada paquete. La analogía: si la IP es la dirección del edificio, el puerto es el número de apartamento. Sin puerto no se s abe a qué puerta llamar.

| Los dos protocolos fundamentales ya los vimos en clases anteriores: TCP | (fiable, con handshake, espera confirmación) y UDP | (rápido, sin confirmación, sin verificación). Los puertos se dividen en tres grupos: |
|---|---|---|
- 0–1023: well-known , pue rtos conocidos. HTTP → 80, HTTPS → 443, SSH → 22, DNS →
53, FTP → 21
- 1024 –49151: registrados , asociados a aplicaciones concretas. MySQL → 3306, RDP →
3389
- 49152 –65535: dinámicos o efímeros , los que usa el navegador como cliente al conectarse a
un servidor Cuando abrimos una web, el navegador no contacta al servidor desde el puerto 80, sino desde un puerto efímero suyo (por ejemplo, 51234). El servidor responde al puerto 80 del servidor desde ese puerto origen.
```bash
```

| netstat -ano | # Ver todas las conexiones | activas: protocolo, IP, puerto, estado Cada línea del netstat -ano es una historia: qué programa de nuestra máquina está hablando con quién, por qué puerto y en qué estado. Útil para detectar conexiones sospechosas o malware. |
|---|---|---|
> [!important] - La idea clave: los puertos ab iertos son puertas. En auditoría, cada puerto abierto es un
vector potencial de entrada al servicio que corre detrás. El trabajo del pentester es identificarlos todos y analizar si alguno es vulnerable

Capa 5 — Sesión La capa de sesión se encarga de abrir , mantener y cerrar conversaciones entre dos máquinas. Se distingue de TCP en el alcance: TCP gestiona una conexión de transporte; una sesión puede englobar varias conexiones. El problema que resuelve: HTTP es un protocolo stateless , sin memoria. El servid or no recuerda entre peticiones si ya te has autenticado. Sin un mecanismo de sesión, habría que enviar usuario y contraseña en cada clic. La solución son las sesiones, implementadas principalmente de dos formas:
- Cookies de sesión: el servidor asigna un identificador (JSESSIONID, session_id, etc.) que
el navegador adjunta en cada petición. El servidor lo reconoce y sabe que ese usuario ya está autenticado
- Tokens JWT (JSON Web Tokens): usados sobre todo en APIs modernas. Tres partes
separadas por puntos, contienen información del usuario firmada criptográficamente En Wireshark, todos estos mecanismos son visibles en el tráfico HTTP (no cifrado). En HTTPS, están cifrados y no se pueden leer directamente.

Capa 6 — Presentación La capa de presentación se encarga del cifrado, la compresión y la traducción de formatos. Aquí vive TLS/SSL , que es lo que convierte HTTP en HTTPS. Cuando un protocolo como FTPS o HTTPS añade cifrado, está añadiendo esta capa por encima del protocolo original.

Capa 7 — Aplicación La capa de aplicación es donde viven los protocolos que usa el usuario directamente: HTTP , FTP, SSH, DNS, SMTP . Los ataques más conocidos del mundo del hacking web (SQL Injection, XSS, CSRF) operan en esta capa. Se puede atacar desde cua lquier parte del mundo, sin necesidad de estar en la red local.

Recapitulación integrada Al cerrar esta sesión sabemos organizar mentalmente cualquier comunicación de red en siete capas, y sabemos que cada capa tiene sus propias herramientas, sus propios ataques y sus propias defensas. En capa 1 controlamos el cable; en capa 2 manipulamos MACs y envenenamos ARP; en capa 3 trabajamos con IPs y ruteamos; en capa 4 identificamos puertos y servicios; en capas 5 y 6 gestionamos sesiones y cifrado; en capa 7 ata camos aplicaciones. La semana siguiente se empieza a aplicar todo esto en entornos reales: enumeración de servicios con Nmap, análisis de tráfico con Wireshark y las primeras máquinas vulnerables.