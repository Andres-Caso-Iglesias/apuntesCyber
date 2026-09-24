

> [!info] Relacionado con
> [[Redes - Modelo OSI y TCP-IP]] · [[Redes - Topologías y Encapsulación]] · [[Nmap - Escaneo y Enumeración]] · [[OSINT - Metodología y Fuentes]]

---

## ① IPv4

```
 Formato: 4 octetos de 8 bits = 32 bits
 Ejemplo: 192.168.1.100
```

### Redes privadas (RFC 1918) — no enrutables en Internet

| Rango | Clase | Uso típico |
|-------|-------|-----------|
| `10.0.0.0/8` | A | Grandes empresas |
| `172.16.0.0/12` | B | Medianas empresas |
| `192.168.0.0/16` | C | Hogares y oficinas |

### IPs especiales

| IP | Uso |
|----|-----|
| `127.0.0.1` | Loopback (yo mismo) |
| `0.0.0.0` | Cualquier interfaz |
| `255.255.255.255` | Broadcast (todos en la red) |

---

## ② Máscara de subred y CIDR

```
192.168.1.0/24 → 255.255.255.0 → 256 hosts (254 usables)
192.168.1.0/16 → 255.255.0.0 → 65,536 hosts
192.168.1.0/8 → 255.0.0.0 → 16M hosts
```

### Pesos binarios de un octeto

De derecha a izquierda: 2⁰=1, 2¹=2, 2²=4, 2³=8, 2⁴=16, 2⁵=32, 2⁶=64, 2⁷=128. Máximo = 255 (todos los bits a 1); mínimo asignable = 1 (el 0 está reservado como nombre de red).

| CIDR | Bits de red | Hosts disponibles | Uso típico |
|------|-------------|-------------------|-----------|
| /8 | 8 | ≈16 millones | Grandes corporaciones |
| /16 | 16 | 65.025 | Redes empresariales grandes |
| /24 | 24 | 254 (253 útiles) | Redes empresariales estándar |
| /32 | 32 | 1 solo host | Rutas específicas |

### Calcular rango

```
Red: 192.168.1.0/24
Primera: 192.168.1.1 (router normalmente)
Última: 192.168.1.254
Broadcast: 192.168.1.255
```

> [!tip] HACKING
> Para escanear una red: `nmap -sn 192.168.1.0/24` descubre hosts activos.

> [!warning] Alcance de auditoría
> Si el cliente especifica el alcance `10.10.7.0/24`, **solo se auditan esas 254 IPs**. No se amplía el alcance sin autorización.

---

## ②bis IPv6 — por qué existe y bypass de firewall

IPv6 usa **6 grupos de 4 dígitos hexadecimales** (0–F) separados por dos puntos, porque las IPv4 (4.300 millones de direcciones) se estaban agotando.

> [!tip] HACKING — bypass de firewall
> Si un servidor tiene IPv4 e IPv6 y el firewall solo monitoriza la IPv4, el atacante puede enviar los paquetes por la IPv6 y pasar desapercibido.

---

## ③ DNS — Sistema de Nombres de Dominio

El DNS traduce nombres legibles (`google.com`) a IPs.

```
Navegador → google.com
 ↓
Caché local / /etc/hosts
 ↓
Servidor DNS
 ↓
Respuesta: 142.x.x.x
```

### Tipos de registros DNS

| Registro | Función |
|----------|---------|
| **A** | Nombre → IPv4 |
| **AAAA** | Nombre → IPv6 |
| **MX** | Servidor de correo |
| **CNAME** | Alias a otro nombre |
| **TXT** | Texto libre (SPF, DKIM) |
| **NS** | Servidores de nombres |
| **PTR** | IP → nombre (DNS inverso) |

### Herramientas DNS

```bash
nslookup google.com # consulta básica
dig google.com ANY # consulta avanzada
dig -x 8.8.8.8 # DNS inverso
host google.com # simple y rápido
```

> [!tip] HACKING
> El DNS es crítico en OSINT: subdominios, transferencias de zona (`dig axfr`), registros MX revelan infraestructura. Herramientas: `dnsrecon`, `subfinder`.

> [!info] Propagación DNS
> Los servidores DNS están distribuidos por todo el mundo y sincronizados entre sí. Un dominio nuevo puede tardar hasta **48 horas** en propagarse porque el registro debe sincronizarse con todos los servidores. Los subdominios son registros A independientes que apuntan a IPs distintas.

```bash
whois dominio.com # información del registrante del dominio
```

---

## ④ Conexión con otras áreas

| Área | Cómo encaja el DNS |
|------|-------------------|
| [[OSINT - Metodología y Fuentes]] | Enumeración de subdominios, WHOIS |
| [[Enumeración Web]] | Subfinder, fuzzing de vhosts |
| [[Nmap - Escaneo y Enumeración]] | Scripts DNS, detección de servicios |
| [[Wireshark - Análisis de Tráfico]] | Filtros DNS, detección de tunelización |

---

## Checklist de repaso

- [ ] ¿Sé calcular el rango de IPs de una subred /24?
- [ ] ¿Entiendo la función de cada registro DNS?
- [ ] ¿Sé usar dig y nslookup?
- [ ] ¿Relaciono el DNS con el OSINT y la enumeración web?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]] — Esteganografia, Linux, Metodologia Pentest
- [[../04 - OSINT y Recopilacion/OSINT - Metodología y Fuentes.md|OSINT - Metodología y Fuentes]] — Desarrollo Web, Esteganografia, Metodologia Pentest
- [[../../apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red.md|Redes-Tipologías, Datagramas y Paquetes de Red]] — Esteganografia, Linux, Metodologia Pentest
- [[../../apuntes Chema/OSINT y Esteganografía.md|OSINT y Esteganografía]] — Desarrollo Web, Esteganografia, Metodologia Pentest
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]] — Desarrollo Web, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../programacion/C/Networking_c.md|Networking_c]] — Programacion: Desarrollo Web, Linux, Redes
- [[../../../cloud/azure_functions.md|azure_functions]] — Cloud: Desarrollo Web, Linux, Redes

> #cloud_base #esteganografia #linux #linux_ciber #nmap #osint #pentest #redes #redes_ciber #web #wifi #wireshark
