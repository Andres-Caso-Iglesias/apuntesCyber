

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

### Calcular rango

```
 Red: 192.168.1.0/24
 Primera: 192.168.1.1 (router normalmente)
 Última: 192.168.1.254
 Broadcast: 192.168.1.255
```

> [!tip] HACKING
> Para escanear una red: `nmap -sn 192.168.1.0/24` descubre hosts activos.

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

- [[Redes - Topologías y Encapsulación.md|Redes - Topologías y Encapsulación]] — Nmap, Redes, Wireshark
- [[../04 - OSINT y Recopilacion/OSINT - Metodología y Fuentes.md|OSINT - Metodología y Fuentes]] — Nmap, OSINT, WiFi / Hardware
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]] — Nmap, OSINT, WiFi / Hardware
- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]] — Nmap, OSINT, WiFi / Hardware
- [[../../apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red.md|Redes-Tipologías, Datagramas y Paquetes de Red]] — Nmap, OSINT, WiFi / Hardware
- [[../../apuntes Joselu/MODULO2/resumen_master_clase11.md|resumen_master_clase11]] — Nmap, OSINT, Redes

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

> #nmap #osint #pentest #redes #wifi #wireshark
