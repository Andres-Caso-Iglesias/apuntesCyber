# ① Tipos de redes por alcance

|**Tipo**|**Descripción**|
|---|---|
|PAN|Personal Area Network. Alcance ~10m. Bluetooth, USB.|
|LAN|Local Area Network. Un edificio/campus. Ethernet, WiFi.|
|MAN|Metropolitan Area Network. Una ciudad.|
|WAN|Wide Area Network. Global. Internet es la WAN más grande.|
|VPN|Red privada virtual sobre red pública (Internet).|
|VLAN|Red local virtual — segmentación lógica dentro de una LAN.|

# ② Topologías de red

|**Topología**|**Descripción**|
|---|---|
|Bus|Todos comparten un único cable. Un fallo corta la red.|
|Estrella|Todos conectados a un switch central. La más común en LAN.|
|Anillo|Cada nodo conectado al siguiente. Datos circulan en un sentido.|
|Malla|Cada nodo conectado a varios otros. Redundancia máxima. Internet.|
|Árbol|Jerarquía de switches. Entornos empresariales grandes.|

| | |
|---|---|
|**💡 PRÁCTICA**|En entornos reales casi siempre encontramos topología en estrella (switches) dentro de una LAN y topología en malla a nivel de WAN/Internet.|

# ③ Encapsulación: cómo viajan los datos

Cada capa del modelo OSI añade su propia cabecera al bloque de datos (encapsulación). Al recibir, cada capa quita su cabecera (desencapsulación).

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|**Datos (App)**|->|**Segmento (TCP)**|->|**Paquete (IP)**|->|**Trama (Ethernet)**|->|**Bits (Física)**|

| |
|---|
|# Nomenclatura por capa:<br><br>Capa 7 (Aplicación) → Datos / Mensaje<br><br>Capa 4 (Transporte) → Segmento (TCP) / Datagrama (UDP)<br><br>Capa 3 (Red)        → Paquete (IP)<br><br>Capa 2 (Enlace)     → Trama (Frame)<br><br>Capa 1 (Física)     → Bits|

# ④ TCP — Three-Way Handshake

Antes de enviar datos, TCP establece una conexión con 3 mensajes:

| | | | | | | |
|---|---|---|---|---|---|---|
|**SYN →**|->|**← SYN-ACK**|->|**ACK →**|->|**[Conexión establecida]**|

| |
|---|
|# SYN      → Cliente dice: 'quiero conectar, seq=X'<br><br># SYN-ACK  → Servidor dice: 'ok, seq=Y, ack=X+1'<br><br># ACK      → Cliente confirma: 'ack=Y+1'<br><br># Cierre de conexión (4 mensajes):<br><br># FIN → ACK → FIN → ACK<br><br># Ataque SYN Flood: enviar miles de SYN sin completar el handshake<br><br># → el servidor agota sus recursos esperando ACK que nunca llega|

| | |
|---|---|
|**🔐 HACKING**|El SYN scan de Nmap (-sS) envía un SYN y espera SYN-ACK sin completar el handshake → el puerto está abierto. Rápido y sigiloso.|

# ⑤ Cabecera IP

| |
|---|
|# Campos principales de la cabecera IPv4:<br><br>Version (4 bits)      → IPv4 = 4<br><br>TTL (8 bits)          → Time To Live: se decrementa en cada router<br><br>                         0 → paquete descartado (evita bucles infinitos)<br><br>Protocol (8 bits)     → 6=TCP, 17=UDP, 1=ICMP<br><br>Source IP (32 bits)   → IP origen<br><br>Destination IP (32bits)→ IP destino<br><br># TTL sirve para fingerprinting del OS:<br><br># TTL=64  → Linux/Unix<br><br># TTL=128 → Windows<br><br># TTL=255 → Cisco / algunos dispositivos de red|

# ⑥ ICMP — Control y diagnóstico

| |
|---|
|# ICMP no es TCP ni UDP: opera en capa 3 directamente<br><br># Tipos de mensajes ICMP:<br><br>Type 0  → Echo Reply (respuesta a ping)<br><br>Type 3  → Destination Unreachable (host/puerto inalcanzable)<br><br>Type 8  → Echo Request (el ping que envías)<br><br>Type 11 → Time Exceeded (TTL=0, respuesta de traceroute)<br><br># Herramientas que usan ICMP:<br><br>ping 8.8.8.8              # verificar conectividad<br><br>traceroute 8.8.8.8        # ver saltos hasta el destino<br><br>traceroute -I 8.8.8.8     # usando ICMP en lugar de UDP|

| | |
|---|---|
|**ℹ FIREWALLS**|Muchos firewalls bloquean ICMP. Por eso nmap -Pn omite el ping y escanea directamente los puertos aunque el host no responda a pings.|

# ⑦ ARP — Resolución de direcciones

ARP traduce direcciones IP a direcciones MAC en la red local. Opera en capa 2.

| |
|---|
|# ¿Quién tiene 192.168.1.1? — ARP Request (broadcast)<br><br># 192.168.1.1 está en MAC AA:BB:CC:DD:EE:FF — ARP Reply (unicast)<br><br>arp -a                    # ver tabla ARP local<br><br>arp -n                    # sin resolución de nombres<br><br># Caché ARP: se guarda temporalmente para no preguntar siempre|

| | |
|---|---|
|**🔐 ARP POISONING**|Un atacante en la misma red puede enviar ARP Replies falsos (Gratuitous ARP) para decir 'la IP del router soy yo' → Man in the Middle. Herramienta: arpspoof, ettercap.|

# ⑧ Metadatos de imagen y OSINT de red

Los metadatos (EXIF) de imágenes pueden revelar información crítica para OSINT de personas y organizaciones.

| |
|---|
|exiftool imagen.jpg       # ver todos los metadatos<br><br># Campos interesantes:<br><br># GPS coordinates → geolocalización exacta<br><br># Camera make/model<br><br># Date/Time Original<br><br># Software → versión de edición<br><br># Herramientas online:<br><br># Jeffrey's Exif Viewer, Exif.regex.info<br><br># Fotoforensics.com (análisis de manipulaciones)|

| | |
|---|---|
|**💡 OSINT**|Una foto de LinkedIn puede contener coordenadas GPS si fue tomada con móvil sin desactivar ubicación. Fundamental verificarlo antes de publicar.|

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/MODULO2/resumen_master_clase13.md|resumen_master_clase13]— Redes, WiFi / Hardware, Windows
- [[../Apuntes/03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]— Linux, Redes, Windows
- [[../Apuntes/04 - OSINT y Recopilacion/OSINT - Metodología y Fuentes.md|OSINT - Metodología y Fuentes]— Empleabilidad, Esteganografía, OSINT
- [[../apuntes Joselu/MODULO1/resumen_master_clase6.md|resumen_master_clase6]— Redes, WiFi / Hardware, Windows
- [[../apuntes Joselu/MODULO2/resumen_master_clase9.md|resumen_master_clase9]— Redes, WiFi / Hardware, Windows
- [[Introducción a Redes.md|Introducción a Redes]— Redes, WiFi / Hardware, Windows

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

> #empleabilidad #esteganografia #linux #nmap #osint #redes #wifi #windows
