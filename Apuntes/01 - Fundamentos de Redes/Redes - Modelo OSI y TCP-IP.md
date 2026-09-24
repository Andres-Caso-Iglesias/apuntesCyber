

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

| | |
|---|---|
| **Contexto de uso** | TCP se usa el 99 % de las veces en auditorías IT; UDP aparece en CTFs con puertos UDP y en entornos OT/industriales (Modbus, SCADA, CAN Bus). Detectar tráfico UDP inesperado en una red IT es señal de anomalía para un SOC. |

---

## ⑤ Puertos y servicios

Los puertos identifican servicios dentro de un host. Rango 0–65535; los conocidos (**well-known**) son 0–1023.

| Puerto | Servicio | Importancia ofensiva |
|--------|----------|---------------------|
| 20/21 | FTP | Transferencia de ficheros, a veces credenciales en claro |
| 22 | SSH | Acceso remoto seguro; objetivo de fuerza bruta |
| 23 | Telnet | Remota sin cifrar — ¡no usar! |
| 25 | SMTP | Envío de correo |
| 53 | DNS | Resolución de nombres |
| 80 | HTTP | Web sin cifrar; Man-in-the-Middle trivial |
| 110/143 | POP3/IMAP | Recepción/acceso a correo |
| 443 | HTTPS | Web cifrada |
| 445 | SMB/Samba | Compartición de recursos; EternalBlue |
| 3306 | MySQL | |
| 3389 | RDP | Escritorio remoto Windows; BlueKeep, fuerza bruta |
| 8080 | HTTP alternativo / proxies | |

> [!important] Regla clave
> **En un puerto solo puede correr un servicio a la vez**, y **lo vulnerable es el servicio, no el servidor**: un Windows Server 2008 R2 sin SMB expuesto no es vulnerable a EternalBlue.

> [!tip] NMAP
> `nmap -sV -p- <IP>` descubre qué servicios corren en cada puerto abierto. Primer paso de cualquier auditoría.

---

## ⑥ TCP Three-Way Handshake

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

## ⑦ Cierre de conexión

```
FIN → ACK → FIN → ACK (4 mensajes)
```

---

## ⑧ Fingerprinting de SO con ping (TTL)

El campo **TTL** (Time To Live) del paquete ICMP revela el sistema operativo de origen:

| TTL inicial observado | SO probable |
|----------------------|-------------|
| ~64 | Linux |
| ~128 | Windows |
| ~256 | Solaris / macOS |

```bash
ping 8.8.8.8 # ver TTL en la respuesta
```

> [!info] Capa 8
> La "capa 8" del modelo OSI es la **capa humana**: el 90 % de las brechas vienen del error humano.

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

- [[../../apuntes Joselu/MODULO2/resumen_master_clase14.md|resumen_master_clase14]] — Desarrollo Web, SQL Injection, XSS
- [[../../apuntes Chema/Introducción a Redes.md|Introducción a Redes]] — Desarrollo Web, SQL Injection, XSS
- [[../../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Criptografia, Nmap, Redes
- [[../03 - Herramientas de Analisis/Wireshark - Análisis de Tráfico.md|Wireshark - Análisis de Tráfico]] — Desarrollo Web, Nmap, SQL
- [[../../comandos/Hydra.md|Hydra]] — Desarrollo Web, Nmap, SQL

### 🌐 Cross-Dominio

- [[../../../programacion/SQL/cursores_sql.md|cursores_sql]] — Programacion: Desarrollo Web, Redes, SQL
- [[../../../cloud/gcp_cloudsql.md|gcp_cloudsql]] — Cloud: Desarrollo Web, Redes, SQL

> #burpsuite #crypto #nmap #redes #redes_ciber #sql #sqli #ssh_tool #web #wifi #wireshark #xss
