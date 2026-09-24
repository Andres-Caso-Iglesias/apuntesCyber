

> [!info] Relacionado con
> [[Redes - Modelo OSI y TCP-IP]] · [[Redes - Direccionamiento IP y DNS]] · [[Wireshark - Análisis de Tráfico]]

---

## ① Tipos de red por alcance

| Tipo | Alcance | Ejemplo |
|------|---------|---------|
| **PAN** | ~10m | Bluetooth, USB |
| **LAN** | Edificio/campus | Ethernet, WiFi |
| **MAN** | Una ciudad | Cableado urbano |
| **WAN** | Global | Internet |
| **VPN** | Red privada sobre pública | Acceso remoto corporativo |
| **VLAN** | Segmentación lógica | Redes dentro de una LAN |

---

## ② Topologías de red

```
     BUS        ESTRELLA     ANILLO    MALLA
              ┌───┐  ┌───┐  ○→○→○→○   ○──○──○
 ○──○──○──○   │   ├──┤   │  ↑     ↓   │  │  │
              └───┘  └───┘  ○←○←○←○   ○──○──○
```

| Topología | Descripción |
|-----------|------------|
| **Bus** | Todos comparten un cable. Un fallo corta la red. |
| **Estrella** | Todos a un switch central. La más común en LAN. |
| **Anillo** | Datos circulan en un sentido. |
| **Malla** | Redundancia máxima. Internet. |
| **Árbol** | Jerarquía de switches. Empresas grandes. |

> [!info] PRÁCTICA
> En entornos reales: **estrella** (switches) dentro de LAN + **malla** a nivel WAN/Internet.

---

## ③ Encapsulación — Cómo viajan los datos

Cada capa OSI añade su cabecera:

```
 Datos (App) → Segmento (TCP) → Paquete (IP) → Trama (Ethernet) → Bits (Física)
```

| Capa | Nomenclatura |
|------|-------------|
| 7 (Aplicación) | Datos / Mensaje |
| 4 (Transporte) | Segmento (TCP) / Datagrama (UDP) |
| 3 (Red) | Paquete (IP) |
| 2 (Enlace) | Trama (Frame) |
| 1 (Física) | Bits |

---

## ③bis Cabecera IP — campos clave

| Campo | Tamaño | Función |
|-------|--------|---------|
| Version | 4 bits | IPv4 = 4 |
| TTL | 8 bits | Time To Live: se decrementa en cada router; 0 → paquete descartado (evita bucles infinitos) |
| Protocol | 8 bits | 6=TCP, 17=UDP, 1=ICMP |
| Source IP | 32 bits | IP origen |
| Destination IP | 32 bits | IP destino |

> [!tip] Fingerprinting
> El TTL inicial revela el origen: **64 → Linux/Unix**, **128 → Windows**, **255 → Cisco / algunos dispositivos de red**.

---

## ④ ARP — Resolución de direcciones

ARP traduce **IP → MAC** en la red local (capa 2).

```
¿Quién tiene 192.168.1.1? → ARP Request (broadcast)
192.168.1.1 está en MAC AA:BB:CC → ARP Reply (unicast)
```

```bash
arp -a # ver tabla ARP local
arp -n # sin resolución de nombres
```

> [!warning] ARP POISONING
> Un atacante en la misma red envía ARP Replies falsos para decir *"la IP del router soy yo"* → **Man in the Middle**. Herramientas: `arpspoof`, `ettercap`.

---

## ⑤ ICMP — Control y diagnóstico

ICMP opera en **capa 3** directamente (no es TCP ni UDP).

| Tipo | Mensaje |
|------|---------|
| Type 0 | Echo Reply (respuesta a ping) |
| Type 3 | Destination Unreachable |
| Type 8 | Echo Request (el ping) |
| Type 11 | Time Exceeded (TTL=0, respuesta de traceroute) |

```bash
ping 8.8.8.8 # verificar conectividad
traceroute 8.8.8.8 # ver saltos hasta el destino
traceroute -I 8.8.8.8 # usando ICMP en lugar de UDP
```

> [!info] FIREWALLS
> Muchos firewalls bloquean ICMP. Por eso `nmap -Pn` omite el ping y escanea directamente los puertos.

---

## ⑥ MTU: por qué Ethernet y WiFi fragmentan distinto

El **MTU** (Maximum Transmission Unit) es el tamaño máximo del paquete que admite un medio:

| Medio | MTU típico |
|-------|-----------|
| Ethernet | ~1500 bytes |
| WiFi (wireless) | ~2300 bytes |

Los paquetes se **fragmentan de manera diferente** según el medio de transporte, y las cabeceras Ethernet y wireless son distintas: una antena WiFi es físicamente tangible, pero la conectividad que llega al equipo es *wireless*.

---

## ⑦ Tipos de adaptador de red en VirtualBox

| Modo | Comportamiento |
|------|---------------|
| **NAT** | Salida a internet + visibilidad con el resto de máquinas de la red NAT |
| **Puente (Bridge)** | La VM recibe IP del router: expande la red local del host |
| **Red interna** | Solo visibilidad interna entre VMs, **sin salida a internet** (ideal para sandboxes: el "bicho" no se escapa) |
| **NAT Network** | Red interna propia creada por nosotros + salida a internet vía NAT; con DHCP activo las VMs se autoasignan IP y "se van a ver" |

> [!important] Sandbox aislada
> Para analizar malware o hacer un forense de un ransomware **no interesa que la VM tenga conectividad con el host**: si no, el bicho podría salir e infectar la máquina real. Corta las interfaces de red.

---

## ⑧ VPN y proxy: dos cosas distintas

| | Proxy | VPN |
|---|-------|-----|
| Mecanismo | Haces las peticiones a través de un servidor que las reenvía a internet | Túnel cifrado punto a punto; enmascara tu tráfico |
| Alcance | Un salto desde un punto | Puede dar varios saltos (una VPN es un conglomerado de proxies) |

**VPN doméstica** (Mullvad, Proton, Nord): encapsulan y te sueltan en internet anónimo. **VPN corporativa**: túnel para entrar en la red interna de la empresa con autenticación contra el servidor (p. ej. OpenVPN con certificado). Una VPN crea una **interfaz virtual TUN/TAP** en el sistema.

---

## Checklist de repaso

- [ ] ¿Puedo nombrar los tipos de red por alcance?
- [ ] ¿Distingo las topologías y cuándo se usa cada una?
- [ ] ¿Entiendo la encapsulación por capas?
- [ ] ¿Sé qué hace ARP y por qué el ARP poisoning es peligroso?
- [ ] ¿Conozco los tipos de mensaje ICMP más comunes?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/Nmap.md|Nmap]] — Nmap, Redes, Redes
- [[../../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Nmap, Redes, Redes
- [[../03 - Herramientas de Analisis/Wireshark - Análisis de Tráfico.md|Wireshark - Análisis de Tráfico]] — Nmap, Redes, Redes
- [[Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Nmap, Redes, Redes
- [[Redes - Modelo OSI y TCP-IP.md|Redes - Modelo OSI y TCP-IP]] — Nmap, Redes, Redes

### 🌐 Cross-Dominio

- [[../../../ia/ia_pentesting.md|ia_pentesting]] — IA: Redes
- [[../../../ia/wandb.md|wandb]] — IA: Redes

> #nmap #redes #redes_ciber #wifi #wireshark
