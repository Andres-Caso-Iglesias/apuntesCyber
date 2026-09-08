# ① ¿Qué es una red de comunicaciones?

Una red existe cuando dos o más dispositivos intercambian información **y hay respuesta de ambas partes**. Sin respuesta, no hay comunicación. El concepto fundamental es el intercambio bidireccional.

| | |
|---|---|
|**💡 DEFINICIÓN**|Para que haya red tiene que haber mínimo una respuesta por parte de cada equipo. Un paquete enviado sin respuesta no constituye comunicación.|

# ② Modelo OSI — Las 7 capas

El modelo OSI divide la comunicación en 7 capas. Cada capa solo habla con la de arriba y la de abajo. Permite diagnosticar en qué punto falla algo.

|**Capa**|**Función y protocolos**|
|---|---|
|7 — Aplicación|HTTP, FTP, DNS, SMTP. Lo que ve el usuario.|
|6 — Presentación|Cifrado, compresión, formato de datos (SSL/TLS aquí).|
|5 — Sesión|Gestión de sesiones entre aplicaciones.|
|4 — Transporte|TCP / UDP. Puertos. Control de flujo y errores.|
|3 — Red|IP. Enrutamiento entre redes. Routers.|
|2 — Enlace de datos|MAC. Switches. Comunicación en la misma red local.|
|1 — Física|Cables, WiFi, señales eléctricas / ópticas.|

| | |
|---|---|
|**🔐 HACKING**|Los ataques se clasifican por capa: ARP poisoning (L2), IP spoofing (L3), SYN flood (L4), SQLi/XSS (L7). Saber en qué capa operas es fundamental.|

# ③ TCP/IP — El modelo real

En la práctica se usa el modelo TCP/IP de 4 capas (simplificación del OSI):

|**Capa TCP/IP**|**Protocolos**|
|---|---|
|Aplicación|HTTP, HTTPS, DNS, FTP, SSH, SMTP, IMAP...|
|Transporte|TCP (fiable, con ACK) / UDP (rápido, sin confirmación)|
|Internet|IP, ICMP, ARP|
|Acceso a red|Ethernet, WiFi, PPP|

## TCP vs UDP

| | |
|---|---|
|**TCP — Fiable**<br><br>*     Orientado a conexión (handshake SYN/SYN-ACK/ACK)<br><br>*     Garantiza entrega y orden<br><br>*     Más lento por el control de errores<br><br>*     Usado en: HTTP, HTTPS, SSH, FTP, SMTP|**UDP — Rápido**<br><br>*     Sin conexión previa, sin ACK<br><br>*     No garantiza entrega ni orden<br><br>*     Más rápido, menor overhead<br><br>*     Usado en: DNS, DHCP, streaming, VoIP, videojuegos|

# ④ Puertos y servicios

Los puertos identifican servicios dentro de un host. Rango 0-65535. Los conocidos (**well-known**) son el 0-1023.

|**Puerto**|**Servicio**|
|---|---|
|20/21|FTP (transferencia de ficheros)|
|22|SSH (administración remota segura)|
|23|Telnet (remota sin cifrar — ¡no usar!)|
|25|SMTP (envío de correo)|
|53|DNS (resolución de nombres)|
|80|HTTP (web sin cifrar)|
|110|POP3 (recepción de correo)|
|143|IMAP (correo, acceso remoto)|
|443|HTTPS (web cifrada)|
|445|SMB (recursos compartidos Windows)|
|3306|MySQL|
|3389|RDP (escritorio remoto Windows)|
|8080|HTTP alternativo / proxies|

| | |
|---|---|
|**🔐 NMAP**|nmap -sV -p- <IP> descubre qué servicios corren en cada puerto abierto. El primer paso de cualquier auditoría.|

# ⑤ Direccionamiento IP

## IPv4

| |
|---|
|# Formato: 4 octetos de 8 bits = 32 bits total<br><br># Ejemplo: 192.168.1.100<br><br># Clases de redes privadas (RFC 1918) — no enrutables en internet:<br><br>10.0.0.0/8          # Clase A (grandes empresas)<br><br>172.16.0.0/12       # Clase B (medianas empresas)<br><br>192.168.0.0/16      # Clase C (hogares y oficinas pequeñas)<br><br># Especiales:<br><br>127.0.0.1           # loopback (yo mismo)<br><br>0.0.0.0             # cualquier interfaz<br><br>255.255.255.255     # broadcast (todos en la red)|

## Máscara de subred y CIDR

| |
|---|
|192.168.1.0/24      # /24 = 255.255.255.0 = 256 hosts (254 usables)<br><br>192.168.1.0/16      # /16 = 255.255.0.0   = 65.536 hosts<br><br>192.168.1.0/8       # /8  = 255.0.0.0     = 16M hosts<br><br># Calcular rango:<br><br># Red: 192.168.1.0/24<br><br># Primera IP: 192.168.1.1  (router normalmente)<br><br># Última IP:  192.168.1.254<br><br># Broadcast:  192.168.1.255|

# ⑥ DNS — Sistema de Nombres de Dominio

El DNS traduce nombres legibles (google.com) a IPs. Es una base de datos distribuida y jerárquica.

| | | | | | | |
|---|---|---|---|---|---|---|
|**Navegador solicita google.com**|->|**Caché local / hosts**|->|**Servidor DNS**|->|**Respuesta: IP 142.x.x.x**|

| |
|---|
|# Tipos de registros DNS:<br><br>A      → nombre → IPv4<br><br>AAAA   → nombre → IPv6<br><br>MX     → servidor de correo<br><br>CNAME  → alias a otro nombre<br><br>TXT    → texto libre (SPF, DKIM...)<br><br>NS     → servidores de nombres autoritativos<br><br>PTR    → IP → nombre (DNS inverso)<br><br># Herramientas:<br><br>nslookup google.com      # consulta básica<br><br>dig google.com ANY       # consulta avanzada<br><br>dig -x 8.8.8.8           # DNS inverso<br><br>host google.com          # simple y rápido|

| | |
|---|---|
|**🔐 HACKING**|El DNS es crítico en OSINT: subdominios, transferencias de zona (dig axfr), registros MX revelan infraestructura. Herramientas: dnsrecon, subfinder.|

# ⑦ Virtualización

Permite correr múltiples sistemas operativos dentro del mismo equipo físico. Fundamental para crear laboratorios de ciberseguridad.

|**Hipervisor**|**Notas**|
|---|---|
|VirtualBox|Gratuito, open source. Bueno para empezar.|
|VMware Workstation|Más rendimiento y estabilidad. Preferido en el máster.|
|Hyper-V|Integrado en Windows Pro/Enterprise.|
|UTM / Parallels|Soluciones para macOS (especialmente Apple Silicon).|

| | |
|---|---|
|**💡 LABS**|Para este máster: 2 VMs máximo simultáneas en una máquina con 8GB RAM. Con 16GB+ puedes levantar un directorio activo completo.|


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/01 - Fundamentos de Redes/Redes - Modelo OSI y TCP-IP.md|Redes - Modelo OSI y TCP-IP]] — SQL Injection, SSH, WiFi / Hardware
- [[../apuntes Joselu/MODULO2/resumen_master_clase14.md|resumen_master_clase14]] — SQL Injection, SSH, WiFi / Hardware
- [[IA/IA — De los cimientos a la cima.md|IA — De los cimientos a la cima]] — Post-Explotación, SQL Injection, SSH
- [[../apuntes Joselu/MODULO2/resumen_master_clase15.md|resumen_master_clase15]] — Post-Explotación, SQL Injection, SSH
- [[../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Post-Explotación, SSH, WiFi / Hardware
- [[../apuntes evolve/BLOQUE 1.md|BLOQUE 1]] — Post-Explotación, SQL Injection, WiFi / Hardware

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #nmap #osint #post-explotacion #redes #sqli #ssh #telnet #wifi #windows #xss
