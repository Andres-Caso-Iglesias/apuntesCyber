

> [!info] Relacionado con
> [[Redes - Direccionamiento IP y DNS]] · [[Redes - Topologías y Encapsulación]] · [[Nmap - Escaneo y Enumeración]] · [[Wireshark - Análisis de Tráfico]] · [[Auditoría WiFi y Car Hacking]]

---

## ① ¿Qué es una red?

Una red existe cuando **dos o más dispositivos intercambian información y hay respuesta**. Sin respuesta, no hay comunicación.

> [!important] Concepto fundamental
> Para que haya red tiene que haber **mínimo una respuesta** por parte de cada equipo. Un paquete enviado sin respuesta no constituye comunicación.

---

## ② Modelo OSI — Las 7 capas

```
┌─────────────────────────────────────────────────┐
│ 7. Aplicación   │ HTTP, FTP, DNS, SMTP          │ ← Lo que ve el usuario
│ 6. Presentación │ Cifrado, compresión (SSL)     │
│ 5. Sesión       │ Gestión de sesiones           │
│ 4. Transporte   │ TCP / UDP — Puertos           │
│ 3. Red          │ IP — Routers                  │
│ 2. Enlace       │ MAC — Switches                │
│ 1. Física       │ Cables, WiFi, señales         │
└─────────────────────────────────────────────────┘
```

| Capa | Función | Protocolos |
|------|---------|-----------|
| **7 — Aplicación** | Lo que ve el usuario | HTTP, FTP, DNS, SMTP |
| **6 — Presentación** | Cifrado, compresión | SSL/TLS |
| **5 — Sesión** | Gestión de sesiones | NetBIOS |
| **4 — Transporte** | Puertos, control de flujo | **TCP** / **UDP** |
| **3 — Red** | Enrutamiento entre redes | IP, ICMP, ARP |
| **2 — Enlace** | Comunicación en red local | MAC, Ethernet |
| **1 — Física** | Cables y señales | WiFi, cable |

> [!tip] HACKING
> Los ataques se clasifican por capa: **ARP poisoning** (L2), **IP spoofing** (L3), **SYN flood** (L4), **SQLi/XSS** (L7). Saber en qué capa operas es fundamental.

---

## ③ TCP/IP — El modelo real

En la práctica se usa el modelo **TCP/IP de 4 capas**:

| Capa TCP/IP | Protocolos |
|-------------|-----------|
| **Aplicación** | HTTP, HTTPS, DNS, FTP, SSH, SMTP |
| **Transporte** | TCP (fiable) / UDP (rápido) |
| **Internet** | IP, ICMP, ARP |
| **Acceso a red** | Ethernet, WiFi |

---

## ④ TCP vs UDP

| TCP — Fiable | UDP — Rápido |
|-------------|-------------|
| Orientado a conexión (handshake) | Sin conexión previa |
| Garantiza entrega y orden | No garantiza entrega |
| Más lento (control de errores) | Más rápido, menor overhead |
| HTTP, HTTPS, SSH, FTP, SMTP | DNS, DHCP, streaming, VoIP |

---

## ⑤ TCP Three-Way Handshake

```
 Cliente Servidor
 │ │
 │──── SYN ────────────→│ "Quiero conectar, seq=X"
 │ │
 │←─── SYN-ACK ─────────│ "Ok, seq=Y, ack=X+1"
 │ │
 │──── ACK ────────────→│ "ack=Y+1"
 │ │
 │════ [DATOS] ════════=│ Conexión establecida
```

> [!warning] Ataque SYN Flood
> Enviar miles de SYN **sin completar el handshake** → el servidor agota recursos esperando ACK que nunca llega.

> [!tip] NMAP
> `nmap -sS` (SYN scan) envía un SYN y espera SYN-ACK **sin completar el handshake** → puerto abierto. Rápido y sigiloso.

---

## ⑥ Cierre de conexión

```
 FIN → ACK → FIN → ACK (4 mensajes)
```

---

## Resumen visual

```
 OSI (teórico) TCP/IP (real)
┌──────────────┐   ┌──────────────────┐
│ 7. Aplicación│   │ Aplicación       │
│ 6. Presentac.│ → │ (HTTP,DNS,SSH)   │
│ 5. Sesión    │   ├──────────────────┤
├──────────────┤   │ Transporte       │
│ 4. Transporte│ → │ (TCP / UDP)      │
├──────────────┤   ├──────────────────┤
│ 3. Red       │ → │ Internet         │
├──────────────┤   │ (IP,ICMP,ARP)    │
│ 2. Enlace    │ → ├──────────────────┤
│ 1. Física    │   │ Acceso a red     │
└──────────────┘   └──────────────────┘
```

---

## Checklist de repaso

- [ ] ¿Puedo nombrar las 7 capas OSI y sus protocolos?
- [ ] ¿Entiendo la diferencia entre TCP y UDP?
- [ ] ¿Sé describir el Three-Way Handshake?
- [ ] ¿Relaciono ataques con su capa OSI?
- [ ] ¿Distingo el modelo OSI del TCP/IP?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Joselu/MODULO2/resumen_master_clase14.md|resumen_master_clase14]]— SSH, WiFi / Hardware, XSS
- [[../../apuntes Chema/Introducción a Redes.md|Introducción a Redes]]— SSH, WiFi / Hardware, XSS
- [[../../apuntes Joselu/MODULO2/resumen_master_clase15.md|resumen_master_clase15]]— Redes, SSH, XSS
- [[../../apuntes Chema/Wireshark.md|Wireshark]]— Redes, SSH, Wireshark
- [[../03 - Herramientas de Analisis/Wireshark - Análisis de Tráfico.md|Wireshark - Análisis de Tráfico]]— Redes, WiFi / Hardware, Wireshark
- [[Redes - Topologías y Encapsulación.md|Redes - Topologías y Encapsulación]]— Redes, WiFi / Hardware, Wireshark

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #nmap #redes #sqli #ssh #wifi #wireshark #xss
