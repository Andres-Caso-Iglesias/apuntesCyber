# Nmap — Cheat Sheet

> Escaneo de red, puertos, servicios y scripts NSE.

---

## Escaneo básico

```bash
nmap <target>                    # Escaneo por defecto (1000 puertos TCP)
nmap -sn <target>                # Ping sweep (sin escaneo de puertos)
nmap -Pn <target>                # Tratar todos los hosts como online
```

## Tipos de escaneo

```bash
nmap -sS <target>                # SYN stealth (requiere root)
nmap -sT <target>                # TCP connect (no requiere root)
nmap -sU <target>                # UDP scan
nmap -sV <target>                # Detectar versiones de servicio
nmap -sC <target>                # Scripts por defecto
nmap -A <target>                 # Agresivo (OS, versiones, scripts, traceroute)
```

## Rango de puertos

```bash
nmap -p 80 <target>              # Puerto específico
nmap -p 80,443 <target>          # Múltiples puertos
nmap -p 1-1000 <target>          # Rango
nmap -p- <target>                # Todos los puertos (65535)
nmap --top-ports 100 <target>    # Top 100 puertos
```

## Velocidad

```bash
nmap -T0 <target>                # Paranoico (lento)
nmap -T3 <target>                # Normal (default)
nmap -T4 <target>                # Agresivo
nmap -T5 <target>                # Insano (rápido, poco sigiloso)
nmap --min-rate 1000 <target>    # Mínimo de paquetes/segundo
```

## Output

```bash
nmap -oN scan.txt <target>       # Output normal
nmap -oG scan.gnmap <target>     # Output grepeable (grep-able)
nmap -oX scan.xml <target>       # Output XML
nmap -oA scan <target>           # Todos los formatos
```

## UDP y descubrimiento

```bash
nmap -sU --top-ports 20 <target>     # Top 20 puertos UDP
nmap -sn 10.10.10.0/24               # Hosts vivos en rango
sudo nmap -sS <target>               # SYN stealth (root)
```

## Scripts NSE

```bash
nmap --script=default <target>           # Scripts por defecto
nmap --script=vuln <target>              # Detección de vulnerabilidades
nmap --script=http-enum <target>         # Enumeración web
nmap --script=smb-enum-shares <target>   # Enumeración SMB
nmap --script=ssh-auth-methods <target>  # Métodos de auth SSH
nmap --script=ssl-heartbleed <target>    # Heartbleed
```

## Ejemplos prácticos

```bash
# Escaneo completo de una máquina HTB
nmap -sC -sV -oA initial 10.10.10.x

# Todos los puertos rápido
nmap -p- --min-rate 10000 -oA allports 10.10.10.x

# Enumeración de servicios web
nmap -sV -p 80,443,8080 --script=http-enum 10.10.10.x

# SMB
nmap -p 445 --script=smb-enum-shares,smb-enum-users 10.10.10.x
```









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../informes/Informe_Blue.md|Informe_Blue]] — Linux, Linux, Windows
- [[../02 - Sistemas Operativos/Consolas - Bash y PowerShell.md|Consolas - Bash y PowerShell]] — Linux, Linux, Windows
- [[../02 - Sistemas Operativos/Linux - Bash Scripting.md|Linux - Bash Scripting]] — Linux, Linux, Windows
- [[../../apuntes Chema/Bash Scripting.md|Bash Scripting]] — Linux, Linux, Windows
- [[../../comandos/SMB_Impacket.md|SMB_Impacket]] — Linux, Linux, Windows

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #cli #linux #linux_ciber #nmap #redes #redes_ciber #telnet #windows_ciber
