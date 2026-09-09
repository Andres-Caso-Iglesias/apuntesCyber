# Telnet — Cheat Sheet

> Testing manual de puertos.

---

## Conexión

```bash
telnet <host> <port>              # Conectar a puerto
telnet 10.10.10.x 21              # FTP
telnet 10.10.10.x 25              # SMTP
telnet 10.10.10.x 80              # HTTP
telnet 10.10.10.x 445             # SMB
```

## Banner grabbing

```bash
telnet 10.10.10.x 21              # Banner del servicio
telnet 10.10.10.x 25              # SMTP banner
telnet 10.10.10.x 110             # POP3 banner
```

## Nmap como alternativa

```bash
nmap -sV -p <port> <host>         # Detectar versión
nmap -sC -p <port> <host>         # Scripts por defecto
```



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/Hydra.md|Hydra]] — Hydra, Redes, Telnet
- [[Nmap.md|Nmap]] — Nmap, Redes, Telnet
- [[../../comandos/Nmap.md|Nmap]] — Hydra, Nmap, Redes
- [[../../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Hydra, Nmap, Redes
- [[../../comandos/Telnet.md|Telnet]] — Hydra, Redes, Telnet
- [[../../write-ups/Banco-THL.md|Banco-THL]] — Hydra, Nmap, Redes

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/Telnet|Telnet]]

> #hydra #nmap #redes #telnet
