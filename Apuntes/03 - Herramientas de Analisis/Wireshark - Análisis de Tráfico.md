

> [!info] Relacionado con
> [[Nmap - Escaneo y Enumeración]] · [[Redes - Modelo OSI y TCP-IP]] · [[Redes - Topologías y Encapsulación]] · [[Blue Team - SOC e Incidentes]] · [[Auditoría WiFi y Car Hacking]]

---

## ① ¿Qué es Wireshark?

**Wireshark** es el analizador de protocolos de red más utilizado del mundo. Captura y muestra el tráfico paquete a paquete. Fundamental tanto para pentesting como para defensa.

---

## ② Interfaz de Wireshark

| Elemento | Descripción |
|----------|------------|
| **Barra de captura** | Botones iniciar/parar. Selección de interfaz. |
| **Filtro de captura** | BPF syntax. Se aplica **ANTES** de capturar. |
| **Filtro de visualización** | Se aplica **DESPUÉS**. Más flexible. |
| **Lista de paquetes** | Panel superior: resumen. |
| **Detalle de paquete** | Panel medio: desglose por capas OSI. |
| **Vista hex/ASCII** | Panel inferior: bytes crudos. |

---

## ③ Filtros de captura (BPF)

Se aplican **durante** la captura. Más eficientes.

```bash
host 192.168.1.1 # solo tráfico de/hacia esa IP
src host 192.168.1.1 # solo tráfico que SALE
dst host 192.168.1.1 # solo tráfico que VA
port 80 # solo puerto 80
port 80 or port 443 # HTTP o HTTPS
not port 22 # todo excepto SSH
tcp # solo TCP
udp # solo UDP
icmp # solo ICMP (pings)
host 192.168.1.1 and port 80 # combinaciones
src net 192.168.1.0/24 # toda la red local
```

---

## ④ Filtros de visualización

Se aplican **después** de capturar. Más potentes.

```bash
# Por protocolo
http # todo HTTP
dns # consultas DNS
arp # tráfico ARP
ssl or tls # tráfico cifrado

# Por IP
ip.addr == 192.168.1.1
ip.src == 192.168.1.1
ip.dst == 192.168.1.1
ip.addr == 192.168.1.0/24

# Por puerto
tcp.port == 80
tcp.dstport == 443
udp.port == 53

# HTTP específico
http.request.method == 'POST'
http.response.code == 200
http contains 'password' # texto en el paquete
http.request.uri contains '/login'

# DNS
dns.qry.name == 'google.com'
dns.flags.response == 1 # solo respuestas

# TCP flags
tcp.flags.syn == 1 && tcp.flags.ack == 0 # solo SYN
tcp.flags.rst == 1 # RST (conexión rechazada)
```

---

## ⑤ Análisis del TCP Handshake

```
→ SYN (cliente) → ← SYN-ACK (servidor) → → ACK (cliente) → [DATOS]
```

```bash
# Filtrar solo el handshake
tcp.flags.syn == 1

# Ver todas las conversaciones TCP
# Statistics → Conversations → TCP

# Reconstruir sesión HTTP completa
# Click derecho → Follow → TCP Stream
```

> [!warning] CREDENCIALES
> En HTTP sin cifrar (puerto 80), el **Follow TCP Stream** puede mostrar usuario y contraseña **en texto plano** en peticiones POST. Por eso HTTPS es obligatorio.

---

## ⑥ Detección de ataques

### SYN Flood (DoS)

```bash
tcp.flags.syn == 1 && tcp.flags.ack == 0
# Miles de SYN sin completar handshake → SYN Flood
```

### ARP Poisoning

```bash
arp
# Señales: ARP Replies gratuitous, misma IP con dos MACs
# Statistics → Resolved Addresses para ver MAC → IP
```

### Port Scan ([[Nmap]])

```bash
tcp.flags.syn == 1 && ip.dst == 192.168.1.1
# Muchos SYN a diferentes puertos → escaneo secuencial
```

---

## ⑦ Protocolos específicos

### DNS — Tunelización

```bash
dns.qry.name contains '.'
# Nombres como 'aGVsbG8gd29ybGQ=.malware.com' → DNS tunneling
```

---

## ⑧ tshark — Wireshark por línea de comandos

```bash
tshark -D # listar interfaces
tshark -i eth0 # capturar
tshark -i eth0 -f 'port 80' # con filtro BPF
tshark -i eth0 -w captura.pcap # guardar a fichero
tshark -r captura.pcap -Y 'http' # leer y filtrar .pcap
tshark -r captura.pcap -Y 'http.request.method == POST' \
 -T fields -e http.host -e http.request.uri
```

> [!tip] AUTOMATIZACIÓN
> `tshark` permite analizar capturas en scripts. Capturar durante 60s, filtrar credenciales HTTP y guardarlas. Muy útil en post-explotación.

---

## Checklist de repaso

- [ ] ¿Sé diferenciar filtro de captura (BPF) y de visualización?
- [ ] ¿Puedo filtrar por protocolo, IP y puerto?
- [ ] ¿Sé interpretar el TCP handshake en Wireshark?
- [ ] ¿Reconozco las firmas de SYN Flood y ARP Poisoning?
- [ ] ¿Sé usar tshark desde línea de comandos?

---

## Enlaces relacionados

- [[Nmap - Escaneo y Enumeración]] — Escaneo de red complementario

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Wireshark.md|Wireshark]— Post-Explotación, Redes, Wireshark
- [[../01 - Fundamentos de Redes/Redes - Topologías y Encapsulación.md|Redes - Topologías y Encapsulación]— Redes, WiFi / Hardware, Wireshark
- [[../01 - Fundamentos de Redes/Redes - Modelo OSI y TCP-IP.md|Redes - Modelo OSI y TCP-IP]— Redes, WiFi / Hardware, Wireshark
- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]— Redes, WiFi / Hardware, Wireshark
- [[../../apuntes Joselu/PREWORK/resumen_clase8.md|resumen_clase8]— Blue Team / SOC, Redes, Wireshark
- [[../09 - Pivoting y Movilidad Lateral/Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]— Post-Explotación, Redes, WiFi / Hardware

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

> #blue-team #nmap #post-explotacion #redes #wifi #wireshark
