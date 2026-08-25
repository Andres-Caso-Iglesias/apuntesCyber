> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 12**
> **Módulo:** PREWORK
> **Tema:** Clase 12
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 12. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 12: Introducción a Redes Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción y objetivos Esta sesión introduce los fundamentos de redes necesarios para comprender las auditorías técnicas.

No se busca un dominio profundo (eso corresponde a ingenieros de redes), sino una base conceptual que permita identificar la infraestructura durante una auditoría, entender los protocolos que se explotan y correlacionar los conceptos con las herramientas que se usarán a lo largo del máster.

El triplete fundamental del máster que se introduce en esta sesión es: Puerto – Protocolo – Servicio (PPS), que estará presente en el 98 % de las prácticas de hacking ofensivo. 2.

Tipos de redes Redes externas (Internet) Una organización se comunica con Internet a través de un Gateway, que es la puerta de salida de la red interna hacia el exterior.

El Gateway asigna la IP pública (externa), proporcionada por el ISP (Internet Service Provider ): Movistar (Telefónica), Orange, V odafone, Abatel, etc.

Tipos de IP pública: - IP dinámica: cambia periódicamente y al reiniciar el router.

Es la habitual en conexiones domésticas.

Útil en auditorías: si el auditor es baneado por IP, basta con reiniciar el router 10 segundos para obtener una IP nueva. - IP estática: no cambia nunca.

La usan los servidores, ya que los DNS deben apuntar siempre a la misma dirección.

Tener IP estática es más costoso. ¿Cómo funciona el DNS?

Cuando se escribe google.com, el sistema DNS traduce ese nombre a la IP real (8.8.8.8) y redirige la conexión.

Internet funciona en realidad con IPs, no con nombres de dominio; los DNS son simplemente un sistema de ayuda para memorización humana.

Estructura de una dirección IP Una IP está formada por cuatro octetos en binario (8 bits cada uno), separados por puntos.

Cada octeto puede tomar valores de 0 a 255 (2⁸ = 256 combinaciones).

Ejemplo: la IP 81.34.117.X se obtiene convirtiendo cada número a su representación binaria con pesos 1, 2, 4, 8, 16, 32, 64, 128. 1

Dentro de un rango de red (/24): - La dirección .0 es el nombre de red (reservada). - La dirección .1 suele estar reservada como Gateway. - La dirección .255 es la dirección de Broadcast. - Por tanto, hay 254 IPs útiles por subred.

Redes internas Red local (192.168.x.x): red doméstica estándar.

Capacidad máxima de 255×255 dispositivos.

Suficiente para entornos pequeños.

Red NAT (10.x.x.x): utilizada en entornos empresariales.

Ofrece un espacio de direccionamiento mucho mayor (255³ = ~16 millones de IPs posibles).

Más escalable y más segura que la red local simple.

Hardware de red relevante en auditorías internas: - Router: enruta el tráfico entre redes, asigna IPs vía DHCP y actúa como mini-firewall doméstico. - Switch: conecta dispositivos dentro del mismo segmento de red. - Hub: versión más antigua y menos eficiente del switch (reenvía el tráfico a todos los puertos). - Access Point (AP) : proporciona conectividad Wi-Fi. - Endpoint: cualquier dispositivo final conectado (PC, portátil, móvil).

Al hacer un escaneo de red en una auditoría interna se encontrarán IPs de todos estos dispositivos.

Es fundamental identificar a qué tipo de hardware corresponde cada IP, ya que pueden ser vulnerables.

### Ejemplo real: en 2024 se descubrió una vulnerabilidad de RCE en switches Cisco que permitía ejecutar código directamente en el dispositivo.

Topologías de red Topología Descripción Valoración del profesor Point-to-Point Comunicación exclusiva entre dos nodosMás segura; usada en defensa, militar y aeroespacial (OTAN, NASA) En bus Cable compartido por todos los nodosInsegura: un actor malicioso puede capturar y modificar el tráfico En estrella Todos los nodos conectados al nodo centralPoco flexible; no hay comunicación directa entre nodos periféricos En anillo circular Todos los nodos conectados en círculoLa más común en empresas; permite comunicación entre todos los nodos Doble anillo Dos caminos circulares (izquierda/derecha)Muy usada; añade redundancia al anillo simple En malla Múltiples interconexiones cruzadasCompleja y poco funcional según el profesor En árbol Jerarquía estricta de nodos La información solo fluye de arriba hacia abajo Híbrida/mixta Combinación de topologías Depende del caso de uso 2

Segmentación de red (recapitulación desde auditorías) La segmentación divide la red en subredes por departamento o función (RRHH, IT, Desarrollo, IA, etc.), usando routers, switches y firewalls para controlar qué IPs pueden comunicarse con qué.

La segmentación por IP/MAC de equipo es más segura que por usuario, ya que con un usuario comprometido (mediante Mimikatz) se podría moverse lateralmente entre equipos.

Esto es precisamente lo que se explotará en las auditorías internas del máster.

Redes privadas (VPN) Una VPN (Virtual Private Network ) crea una red virtualizada entre equipos dispersos en Internet, haciendo que se comporten como si estuviesen en la misma red interna.

Cuando el usuario se conecta a una VPN, su tráfico pasa por distintos nodos antes de salir a Internet con una IP diferente a la original, lo que genera una falsa sensación de anonimato .

El camino de saltos puede trazarse y determinarse la IP real de origen.

Se menciona que durante el máster se verá en detalle si una VPN proporciona anonimato real y se trabajará con Mullvad, una VPN orientada al anonimato real, y la construcción de infraestructuras anónimas basadas en VPS. 3.

El modelo OSI El modelo OSI (Open Systems Interconnection ) es el marco teórico que describe cómo viaja la información a través de una red, organizado en 7 capas.

Los datagramas suben y bajan por estas capas sumando o restando bytes a sus cabeceras.

Capa Nombre Descripción breve Relevancia en hacking 7 Aplicación Interfaz con el usuario (WhatsApp, navegador)Ataques a aplicaciones web, OWASP Top 10 6 Presentación Formateo y cifrado/descifrado de datosFallos criptográficos 5 Sesión Gestión de conexiones y sesionesSecuestro de sesión (session hijacking) 4 Transporte TCP/UDP; control de flujo y segmentaciónAtaques DoS (capa 4), escaneo de puertos 3 Red Direccionamiento IP y enrutamientoAtaques de enrutamiento 2 Enlace de datos Comunicación entre dispositivos en la misma redMAC Spoofing, ARP Poisoning 1 Física Transmisión de bits Hardware hacking, 3

Capa Nombre Descripción breve Relevancia en hacking por el medio físico tapping En la práctica del máster: los firewalls “de capa 7” inspeccionan el contenido del paquete (NGFW/WAF); los de “capa 4” solo filtran por puerto e IP.

Los ataques DoS más habituales actúan en capas 4 y 7. 4.

Datagramas Un datagrama es la unidad de información que viaja por Internet.

Su estructura es:
- Cabecera (Header) : contiene metadatos — IP de origen, IP de destino, tipo de
datagrama, etc.
- Carga útil (Payload) : el contenido real del mensaje.

En el contexto de exploits, el
payload es la parte del código malicioso que se inyecta en el sistema víctima para obtener una shell u otro acceso.

El MTU (Maximum Transmission Unit ) es el tamaño máximo de un datagrama en Internet: 1500 bytes.

Si el dato es más grande, se fragmenta ( split) y se reensambla en el destino.

Herramienta que se verá para analizar datagramas: Wireshark. 5.

TCP vs.

UDP Característica TCP UDP Uso principal Web, correo, FTP, auditorías IoT, VPNs industriales, videojuegos, streaming Conexión Orientado a conexión (three- way handshake: SYN, SYN- ACK, ACK)Sin conexión Fiabilidad Alta (verifica entrega) Baja (envío sin confirmación) Velocidad Más lento Más rápido Autenticación Sí (handshake entre endpoints) No En el 99 % de las auditorías técnicas del máster se trabajará con TCP. 6.

Puertos, protocolos y servicios (el triplete PPS) Un puerto es un canal de entrada/salida de un servidor.

Un protocolo define cómo se comunican.

Un servicio es el software concreto que corre sobre ese protocolo.

Puertos estándar más importantes: 4

Puerto Protocolo Servicio habitual 21 FTP Transferencia de ficheros 22 SSH Acceso remoto seguro 25 SMTP Correo electrónico 80 HTTP Web sin cifrado 135, 139, 445 SMB/Samba Compartición de recursos en red 443 HTTPS Web con cifrado TLS 3389 RDP Escritorio remoto (Windows) Los puertos estándar son una convención, no una obligación: cualquier servicio puede correr en cualquier puerto.

Si se usa un puerto no estándar, hay que especificarlo explícitamente en la URL (ej. http://dominio.com:8080 ).

> [!important] ### Distinción importante: el protocolo (ej.

FTP) define la forma de comunicación; el servicio (ej.

SFTP v1.3) es la implementación concreta que usa ese protocolo en un puerto dado. 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración IPS (empresa de telecomunicaciones) ISP (Internet Service Provider ) – proveedor de servicios de Internet MTEU MTU (Maximum Transmission Unit ) – tamaño máximo de un datagrama (1500 bytes) Abatel Adamo o Avatel – operadora de telecomunicaciones española multa Mullvad – servicio VPN orientado al anonimato ck y el sí / ack sí SYN / SYN-ACK / ACK – three-way handshake de TCP modelo o si / o si Modelo OSI (Open Systems Interconnection ) htps / htp HTTPS / HTTP – protocolos web sh SSH (Secure Shell) – protocolo de acceso remoto seguro y cubo W3C (World Wide Web Consortium ) – organización que estandariza protocolos web mímica Mimikatz – herramienta de volcado de credenciales en Windows RJ45 RJ-45 – conector estándar de cable Ethernet redes en anillo circular Topología en anillo (ring topology) point to point Topología punto a punto (point-to-point) red NATeada / NATeo Red NAT (Network Address Translation ) – red con traducción de direcciones de secops DevSecOps (mencionado de forma tangencial) 5

Término en la transcripción Corrección / Aclaración data link y physical layer Capa de enlace de datos (L2) y capa física (L1) del modelo OSI Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6