

> [!info] Relacionado con
> [[Wireshark - Análisis de Tráfico]] · [[OSINT - Metodología y Fuentes]] · [[Enumeración Web]] · [[Metodología de Explotación]]

---

## ① ¿Qué es Nmap?

**Nmap** (Network Mapper) es la herramienta de referencia para descubrir hosts, puertos y servicios en una red. Primer paso de **cualquier** auditoría.

---

## ② Metodología de escaneo en 3 fases

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 1. Escaneo rápido│ ──→ │ 2. Todos los     │ ──→ │ 3. Scripts sobre │
│ (top 1000)       │     │ puertos (-p-)    │     │ puertos hall.    │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Fase 1 — Escaneo rápido

```bash
[[Nmap]] -oN recon/initial.txt <IP>
```

### Fase 2 — Todos los puertos

```bash
[[Nmap]] -p- -oN recon/allports.txt <IP>
# -p- escanea los 65,535 puertos
# Presionar VV durante el escaneo para ver progreso
```

### Fase 3 — Scripts y versiones

```bash
[[Nmap]] -sC --script default,vuln -sV -Pn -p <PUERTOS> -oA recon/full <IP>
```

| Flag | Función |
|------|---------|
| `-sC` | Scripts por defecto |
| `-sV` | Detectar versiones |
| `-Pn` | Omitir host discovery |
| `-oA` | Guardar en 3 formatos (normal, grepeable, XML) |
| `vuln` | Scripts de CVEs (más intrusiva) |

---

## ③ Comandos esenciales

### Descubrimiento de hosts

```bash
[[Nmap]] -sn 10.0.2.0/24 # hosts activos en el rango
sudo netdiscover -r 10.0.2.0/24 # por ARP (más sigiloso)
```

### Escaneo de puertos

```bash
[[Nmap]] <IP> # escaneo básico (top 1000)
[[Nmap]] -sCV <IP> # + scripts + versiones
[[Nmap]] -p- <IP> # TODOS los puertos
[[Nmap]] -sV -p22,80,443 <IP> # puertos concretos
```

### Guardar resultados

```bash
[[Nmap]] -oN archivo.txt <IP> # formato normal
[[Nmap]] -oG archivo.txt <IP> # formato grepeable
[[Nmap]] -oX archivo.xml <IP> # formato XML
[[Nmap]] -oA nombre <IP> # los 3 formatos a la vez
```

---

## ④ Detección de OS por TTL

| TTL | Sistema operativo |
|-----|------------------|
| 64 | Linux/Unix |
| 128 | Windows |
| 255 | Cisco / dispositivos |

---

## ④bis Tipos de escaneo — qué está pasando por la red

| Flag | Tipo | Cómo funciona | Notas |
|------|------|--------------|-------|
| `-sS` | **TCP SYN** (stealth) | SYN → SYN/ACK → **RST** (no completa el handshake) | Requiere root; el "puerto abierto" se deduce por el SYN/ACK |
| `-sT` | TCP Connect | Completa el handshake 3WHS con `connect()` | Lo usan usuarios sin root; más ruidoso y deja log de conexión |
| `-sU` | UDP | Envía datagrama UDP y espera ICMP *port unreachable* | **Lento**; imprescindible para DNS(53), SNMP(161), NTP(123) |
| `-sn` | Ping sweep | Solo descubrimiento de hosts, sin puertos | Reconocimiento inicial |
| `-Pn` | No ping | Trata el host como si respondiera a ping | Cuando hay firewalls que bloquean ICMP |

```bash
sudo [[Nmap]] -sS -sV <IP> # SYN stealth + versiones (recomendado con root)
[[Nmap]] -sT <IP> # TCP connect completo (sin root)
sudo [[Nmap]] -sU -p 53,161,123 <IP> # puertos UDP (siempre añadir en fase 2)
```

> [!info] SEÑALES
> El escaneo SYN funciona porque el kernel responde al SYN/ACK aunque la aplicación no tenga `accept()`: Nmap envía RST para no dejar la conexión "colgada" en el objetivo. Un IDS puede correlacionar SYN→RST anómalo como escaneo.

---

## ⑤ Scripts útiles

```bash
# Scripts de enumeración
[[Nmap]] --script smb-enum-shares <IP> # shares SMB
[[Nmap]] --script http-enum <IP> # rutas HTTP
[[Nmap]] --script dns-brute <IP> # subdominios

# Scripts de vulnerabilidades
[[Nmap]] --script vuln <IP> # buscar CVEs
[[Nmap]] --script http-sql-injection <IP> # SQLi
```

---

## ⑥ Conexión con otras áreas

| Área | Cómo usa Nmap |
|------|--------------|
| [[OSINT - Metodología y Fuentes]] | Descubrir hosts en la red |
| [[Enumeración Web]] | Descubrir puertos 80/443 |
| [[Fuzzing Web con ffuf]] | Servicios para fuzzear |
| [[Metodología de Explotación]] | Primer paso de cualquier pentest |
| [[Wireshark - Análisis de Tráfico]] | Detectar escaneos Nmap |

---

## ⑦ Errores comunes

> [!warning] ERRORES
> - **Olvidar `-p-`**: solo ves los 1000 puertos comunes, te pierdes los no estándar.
> - **Lanzar `vuln` sin `-Pn`**: si el host no responde a ping, Nmap lo descarta.
> - **No guardar resultados**: pierdes el trabajo de enumeración.
> - **Confundir servicio esperado con real**: sin `-sCV`, Nmap muestra el servicio por defecto del puerto, no el real.
> - **Ignorar UDP**: servicios críticos (DNS, SNMP) viven en UDP; un pentest sin `-sU` está incompleto.
> - **Ejecutar `vuln` sin autorización**: los scripts de vulnerabilidades son intrusivos y pueden tumbar servicios; siempre con scope firmado.

---

## Puertos comunes de referencia

| Puerto | Servicio | Puerto | Servicio |
|--------|----------|--------|----------|
| 21 | FTP | 3306 | MySQL |
| 22 | SSH | 3389 | RDP |
| 23 | Telnet | 5432 | PostgreSQL |
| 25 | SMTP | 5985/5986 | WinRM |
| 53 | DNS | 6379 | Redis |
| 80 | HTTP | 8080/8443 | Proxy/Alt HTTPS |
| 110 | POP3 | 8000/8888 | HTTP alternativo |
| 143 | IMAP | 5900 | VNC |
| 443 | HTTPS | 9200 | Elasticsearch |
| 445 | SMB | 11211 | Memcached |

---

## Checklist de repaso

- [ ] ¿Sé hacer un escaneo en 3 fases (rápido → completo → scripts)?
- [ ] ¿Conozco los flags más importantes (-sC, -sV, -p-, -Pn, -oA)?
- [ ] ¿Sé guardar resultados en diferentes formatos?
- [ ] ¿Entiendo la diferencia entre netdiscover y nmap?
- [ ] ¿Sé interpretar el TTL para detectar el OS?

---

## Enlaces relacionados

- [[comandos/Nmap]] — Cheat sheet de comandos









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../15 - Certificaciones/Certificaciones - ISO 27001 y eJPTv2.md|Certificaciones - ISO 27001 y eJPTv2]] — Hack The Box, Metodologia Pentest, SQL Injection
- [[../12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Hack The Box, Metodologia Pentest, SQL Injection
- [[../01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Desarrollo Web, Linux, Metodologia Pentest
- [[../../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Hack The Box, Metodologia Pentest, SQL Injection
- [[../../apuntes Joselu/MODULO3/resumen_master_clase27.md|resumen_master_clase27]] — Hack The Box, Metodologia Pentest, SQL Injection

### 🌐 Cross-Dominio

- [[../../../programacion/SQL/cursores_sql.md|cursores_sql]] — Programacion: Desarrollo Web, Redes, SQL
- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Redes, SQL

> #ffuf #hack_the_box #lfi #linux #linux_ciber #metasploit #nmap #normativa #osint #pentest #redes #redes_ciber #sql #sqli #web #wifi #windows_ciber #wireshark
