# Nmap — Escaneo de Red

> [!info] Herramienta
> Network Mapper — escaneo de puertos, descubrimiento de hosts, detección de servicios y OS, scripts NSE.
## Descubrimiento de Hosts

> [!tip] Primer paso
> Encontrar hosts activos antes de escanear puertos.

| Comando | Descripción |

| `nmap -sn <target>` | Ping scan — descubre hosts sin escanear puertos |
| `nmap -sP <target>` | Alias de -sn (versiones antiguas) |
| `nmap -sL <target>` | Lista de escaneo — resuelve DNS sin paquetes |
| `nmap -PR <target>` | ARP ping scan (red local) |
| `nmap -PE -PP -PM <target>` | ICMP echo/timestamp/netmask |
| `nmap -PS<puertos> <target>` | TCP SYN ping |

```bash
# Descubrir hosts en red
nmap -sn 192.168.1.0/24

# ARP scan (local)
nmap -PR 192.168.1.0/24
```

---

## Escaneo de Puertos

> [!important] Tipos de scan
| Scan | Flag | Descripción |
|------|------|-------------|
| TCP SYN | `-sS` | Half-open, más común |
| TCP Connect | `-sT` | Completa handshake, sin root |
| UDP | `-sU` | Servicios UDP, lento |
| NULL | `-sN` | Sin flags |
| FIN | `-sF` | Solo flag FIN |
| Xmas | `-sX` | FIN+PSH+URG |
| ACK | `-sA` | Mapear firewalls |
| Window | `-sW` | Window size |

```bash
# Escaneo básico (1000 puertos comunes)
nmap <target>

# Puertos específicos
nmap -p 80,443,8080 <target>

# Todos los puertos
nmap -p- <target>

# SYN scan (requiere root)
nmap -sS <target>

# Top 100 puertos
nmap --top-ports 100 <target>
```

---

## Detección de Servicios y OS

| Comando | Descripción |
|---------|-------------|
| `nmap -sV <target>` | Detección de versión |
| `nmap -O <target>` | Detección de OS (requiere root) |
| `nmap -A <target>` | Agresivo (OS + versiones + scripts + traceroute) |
| `nmap --traceroute <target>` | Traceroute al objetivo |

```bash
# Agresivo
nmap -A <target>

# Versión máxima intensidad
nmap -sV --version-all <target>
| ```
## Escaneo Stealth

> [!warning] Evasión
> Estos scan evitan firewalls e IDS simples.

| Comando | Descripción |

| `nmap -sN <target>` | NULL scan — sin flags |
| `nmap -sF <target>` | FIN scan — solo FIN |
| `nmap -sX <target>` | Xmas scan — FIN+PSH+URG |
| `nmap -sA <target>` | ACK scan — mapear reglas firewall |
| `nmap -sW <target>` | Window scan |
| `nmap --scanflags URGPSHACK <target>` | Flags personalizados |

### Decoy y Fragmentación

```bash
# Decoy scan (IPs falsas)
nmap -D RND:10 <target>

# Fragmentación
nmap -f <target>
nmap -ff <target> # 16 bytes

# MTU personalizado
nmap --mtu 24 <target>
```

---

## Evasión de Firewall / IDS

| Comando | Descripción |
|---------|-------------|
| `nmap --source-port 53 <target>` | Puerto fuente DNS |
| `nmap --data-length 25 <target>` | Datos aleatorios |
| `nmap --randomize-hosts <target>` | Orden aleatorio |
| `nmap --spoof-mac 0 <target>` | MAC aleatoria |
| `nmap --badsum <target>` | Checksums inválidos |
| `nmap -S 192.168.1.100 <target>` | IP fuente falsa |

---

## Control de Rendimiento

| Comando | Descripción |
|---------|-------------|
| `nmap -T0 <target>` | Paranoico |
| `nmap -T3 <target>` | Normal (default) |
| `nmap -T4 <target>` | Agresivo |
| `nmap -T5 <target>` | Insane |
| `nmap --min-rate 1000 <target>` | Mínimo 1000 pps |
| `nmap --max-rate 100 <target>` | Máximo 100 pps |
| `nmap --host-timeout 30m <target>` | Timeout por host |

```bash
# Rápido y agresivo
nmap -T4 -p- <target>

# Desde archivo de targets
nmap -iL targets.txt
| ```
## Scripts NSE — Vulnerabilidades

> [!danger] Detección de vulns
> Estos scripts identifican vulnerabilidades conocidas.

```bash

# Todos los scripts de vuln
nmap --script vuln <target>

# SMB vulnerabilities
nmap --script smb-vuln* -p 445 <target>

# EternalBlue (MS17-010)
nmap --script smb-vuln-ms17-010 -p 445 <target>

# Heartbleed
nmap --script ssl-heartbleed -p 443 <target>

# Shellshock
nmap --script http-shellshock -p 80,443 <target>

# SQL Injection
nmap --script http-sql-injection -p 80,443 <target>
| ```
## Scripts NSE — Información

> [!note] Enumeración
> Scripts para obtener información del target.

```bash

# Scripts default (seguros)
nmap -sC <target>

# Enumerar directorios web
nmap --script http-enum -p 80,443 <target>

# DNS brute force
nmap --script dns-brute <target>

# Enumerar usuarios SMB
nmap --script smb-enum-users -p 445 <target>

# Enumerar shares SMB
nmap --script smb-enum-shares -p 445 <target>

# Headers HTTP
nmap --script http-headers -p 80,443 <target>

# Certificado SSL
nmap --script ssl-cert -p 443 <target>
| ```
## Scripts NSE — Fuerza Bruta

> [!warning] Brute force
> Lento pero útil para encontrar credenciales débiles.

```bash

# FTP brute
nmap --script ftp-brute -p 21 <target>

# SSH brute
nmap --script ssh-brute -p 22 <target>

# HTTP brute
nmap --script http-brute -p 80,443 <target>

# MySQL brute
nmap --script mysql-brute -p 3306 <target>

# SMB brute
nmap --script smb-brute -p 445 <target>
```

---

## Output

| Formato | Flag | Descripción |
|---------|------|-------------|
| Normal | `-oN output.txt` | Texto legible |
| XML | `-oX output.xml` | Para parsers |
| Grepable | `-oG output.gnmap` | Para grep/awk |
| Todos | `-oA output` | Genera .nmap .xml .gnmap |

```bash
# Solo puertos abiertos
nmap --open <target>

# Verbose
nmap -v <target>
nmap -vv <target>

# Razón del estado
nmap --reason <target>
```

### Otras Opciones

| Comando | Descripción |
|---------|-------------|
| `nmap --iflist` | Listar interfaces |
| `nmap -e eth0 <target>` | Interfaz específica |
| `nmap -n <target>` | Sin DNS (más rápido) |
| `nmap -R <target>` | Siempre DNS |

---

#checklist
- [ ] Descubrimiento de hosts con `-sn` practicado
- [ ] Tipos de scan (SYN, Connect, UDP) entendidos
- [ ] Detección de servicios con `-sV` y `-A`
- [ ] Scripts NSE de vulnerabilidades ejecutados
- [ ] Output en múltiples formatos generado
- [ ] Evasión de firewall con stealth scan

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes evolve/BLOQUE 9.md|BLOQUE 9]— Hydra, Redes
- [[../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]— Nmap, Redes
- [[Hydra.md|Hydra]— Hydra, Redes
- [[SMB_Impacket.md|SMB_Impacket]— Nmap, Redes
- [[../Apuntes/10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]— Hydra, Nmap, Redes
- [[../write-ups/Banco-THL.md|Banco-THL]— Hydra, Nmap, Redes

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]

> #hydra #nmap #redes
