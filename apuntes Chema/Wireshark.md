# ① ¿Qué es Wireshark?

Wireshark es el **analizador de protocolos de red** más utilizado del mundo. Captura y muestra en detalle el tráfico que pasa por una interfaz de red. Es fundamental tanto para pentesting como para defensa.

| | |
|---|---|
|**💡 COMUNICACIONES**|Una red existe cuando dos o más dispositivos intercambian información y hay respuesta. Wireshark captura exactamente ese intercambio, paquete a paquete.|

# ② Interfaz de Wireshark

|**Elemento**|**Descripción**|
|---|---|
|Barra de captura|Botones para iniciar/parar captura. Selección de interfaz.|
|Filtro de captura|BPF syntax. Se aplica ANTES de capturar (menos datos).|
|Filtro de visualización|Se aplica DESPUÉS. Más flexible, no descarta paquetes.|
|Lista de paquetes|Panel superior: resumen de cada paquete capturado.|
|Detalle de paquete|Panel medio: desglose por capas (OSI).|
|Vista hex/ASCII|Panel inferior: bytes crudos del paquete.|
|Barra de estado|Paquetes capturados, filtrados, tiempo de captura.|

# ③ Filtros de captura (BPF)

Los filtros BPF (Berkeley Packet Filter) se aplican **durante la captura**. Son más eficientes pero menos flexibles. Se escriben en la barra de filtro verde antes de iniciar.

| |
|---|
|# Filtros BPF comunes:<br><br>host 192.168.1.1           # solo tráfico de/hacia esa IP<br><br>src host 192.168.1.1       # solo tráfico que SALE de esa IP<br><br>dst host 192.168.1.1       # solo tráfico que VA a esa IP<br><br>port 80                    # solo tráfico por el puerto 80<br><br>port 80 or port 443        # HTTP o HTTPS<br><br>not port 22                # todo excepto SSH<br><br>tcp                        # solo protocolo TCP<br><br>udp                        # solo UDP<br><br>icmp                       # solo ICMP (pings)<br><br># Combinaciones:<br><br>host 192.168.1.1 and port 80<br><br>src net 192.168.1.0/24     # toda la red local<br><br>tcp and port 443 and host 10.0.0.5|

# ④ Filtros de visualización

Los filtros de visualización se aplican **después de capturar**. Son más potentes y permiten buscar por campos específicos de los protocolos.

| |
|---|
|# Por protocolo:<br><br>http                       # todo HTTP<br><br>dns                        # consultas y respuestas DNS<br><br>arp                        # tráfico ARP<br><br>tcp                        # solo TCP<br><br>ssl or tls                 # tráfico cifrado<br><br># Por IP:<br><br>ip.addr == 192.168.1.1<br><br>ip.src == 192.168.1.1<br><br>ip.dst == 192.168.1.1<br><br>ip.addr == 192.168.1.0/24   # red completa<br><br># Por puerto:<br><br>tcp.port == 80<br><br>tcp.dstport == 443<br><br>udp.port == 53<br><br># HTTP específico:<br><br>http.request.method == 'POST'<br><br>http.response.code == 200<br><br>http contains 'password'    # texto en el paquete<br><br>http.request.uri contains '/login'<br><br># DNS:<br><br>dns.qry.name == 'google.com'<br><br>dns.flags.response == 1     # solo respuestas<br><br># TCP flags:<br><br>tcp.flags.syn == 1 && tcp.flags.ack == 0   # solo SYN (inicio conexión)<br><br>tcp.flags.rst == 1          # RST (conexión rechazada/reseteada)|

# ⑤ Análisis del TCP Handshake

Wireshark muestra perfectamente el proceso de establecimiento de conexión TCP:

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**→ SYN (cliente)**|->|**← SYN-ACK (servidor)**|->|**→ ACK (cliente)**|->|**[DATOS]**|->|**→ FIN/← FIN**|

| |
|---|
|# Filtrar solo el handshake TCP:<br><br>tcp.flags.syn == 1<br><br># Ver todas las conversaciones TCP:<br><br># Statistics → Conversations → TCP<br><br># Reconstruir una sesión HTTP completa:<br><br># Click derecho en paquete HTTP → Follow → TCP Stream<br><br># Muestra la conversación completa en texto legible<br><br># Aplicable también a:<br><br># UDP Stream → protocolos UDP<br><br># TLS Stream → tráfico cifrado (no desencripta)<br><br># HTTP Stream → sesión HTTP completa|

| | |
|---|---|
|**🔐 CREDENCIALES**|En HTTP sin cifrar (puerto 80), el Follow TCP Stream puede mostrar usuario y contraseña en texto plano en peticiones POST. Esto es por lo que HTTPS es obligatorio.|

# ⑥ Detección de ataques con Wireshark

## SYN Flood (DoS)

| |
|---|
|# Filtro para detectar SYN Flood:<br><br>tcp.flags.syn == 1 && tcp.flags.ack == 0<br><br># Si ves miles de SYN desde múltiples IPs sin completar handshake<br><br># → está ocurriendo un SYN Flood / DDoS|

## ARP Poisoning / Spoofing

| |
|---|
|# Filtro ARP:<br><br>arp<br><br># Señales de ARP Poisoning:<br><br># 1. Muchos ARP Replies gratuitous (sin previa solicitud)<br><br># 2. Misma IP respondida por dos MACs diferentes<br><br># 3. ARP Replies desde la IP del gateway pero con MAC diferente<br><br># En Statistics → Resolved Addresses puedes ver MAC → IP<br><br># Si el gateway tiene dos entradas = ARP Poisoning en curso|

## Port Scan (Nmap)

| |
|---|
|# Un escaneo Nmap genera un patrón muy reconocible:<br><br># Muchos SYN hacia diferentes puertos de la misma IP destino<br><br># Filtro para detectar:<br><br>tcp.flags.syn == 1 && ip.dst == 192.168.1.1<br><br># Si ves peticiones a puertos 1,2,3,4... es un escaneo secuencial<br><br># Nmap -sS (SYN scan) deja RST en los puertos cerrados:<br><br>tcp.flags.rst == 1|

# ⑦ Análisis de protocolos específicos

## HTTP — Ver contraseñas en texto plano

| |
|---|
|# Capturar y analizar login en HTTP:<br><br>http.request.method == 'POST'<br><br># → Seguir TCP Stream para ver las credenciales<br><br># Buscar cookies de sesión:<br><br>http.cookie<br><br># Las cookies de sesión permiten secuestrar sesiones (session hijacking)|

## DNS — Detección de tunelización

| |
|---|
|# DNS Tunneling: usar DNS para exfiltrar datos (bypass firewalls)<br><br># Señales: consultas DNS muy largas o con muchos subdominios<br><br>dns.qry.name contains '.'     # ver todas las consultas<br><br># Si ves nombres como 'aGVsbG8gd29ybGQ=.malware.com' (base64)<br><br># → posible DNS tunneling<br><br># Estadísticas de DNS:<br><br># Statistics → DNS → muestra dominios más consultados|

# ⑧ tshark — Wireshark por línea de comandos

| |
|---|
|# tshark es Wireshark sin interfaz gráfica (ideal para scripts)<br><br># Listar interfaces disponibles:<br><br>tshark -D<br><br># Capturar en interfaz eth0:<br><br>tshark -i eth0<br><br># Capturar con filtro BPF:<br><br>tshark -i eth0 -f 'port 80'<br><br># Guardar captura a fichero:<br><br>tshark -i eth0 -w captura.pcap<br><br># Leer y filtrar un .pcap:<br><br>tshark -r captura.pcap -Y 'http'<br><br># Extraer campos específicos:<br><br>tshark -r captura.pcap -Y 'http.request.method == POST' -T fields -e http.host -e http.request.uri<br><br># Extraer credenciales HTTP básicas:<br><br>tshark -r captura.pcap -Y 'http.authorization' -T fields -e http.authorization|

| | |
|---|---|
|**💡 AUTOMATIZACIÓN**|tshark permite analizar capturas en scripts. Por ejemplo: capturar durante 60 segundos, filtrar credenciales HTTP y guardarlas en fichero. Muy útil en post-explotación.|

---

## Enlaces relacionados



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../informes/Informe_Banco.md|Informe_Banco]] — Linux, Metasploit, Nmap
- [[../comandos/Metasploit.md|Metasploit]] — Linux, Metasploit, Nmap
- [[../Apuntes/02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — Linux, Metasploit, Nmap
- [[../apuntes Joselu/PREWORK/resumen_clase12.md|resumen_clase12]] — Metasploit, Nmap, Post-Explotación
- [[../Apuntes/comandos/Metasploit.md|Metasploit]] — Linux, Metasploit, Redes
- [[../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Nmap, Post-Explotación, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

> #linux #metasploit #nmap #post-explotacion #redes #ssh #wireshark
