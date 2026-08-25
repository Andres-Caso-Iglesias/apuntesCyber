

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
 BUS ESTRELLA ANILLO MALLA
───────────── ┌───┐ ┌───┐ ○→○→○→○ ○──○──○
 ○──○──○──○ │ ├──┤ │ ↑ ↓ │ │ │
 └───┘ └───┘ ○←○←○←○ ○──○──○
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

## Checklist de repaso

- [ ] ¿Puedo nombrar los tipos de red por alcance?
- [ ] ¿Distingo las topologías y cuándo se usa cada una?
- [ ] ¿Entiendo la encapsulación por capas?
- [ ] ¿Sé qué hace ARP y por qué el ARP poisoning es peligroso?
- [ ] ¿Conozco los tipos de mensaje ICMP más comunes?