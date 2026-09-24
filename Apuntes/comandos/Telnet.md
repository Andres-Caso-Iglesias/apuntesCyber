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
nc -v 10.10.10.x 21               # Alternativa con netcat
echo | nc 10.10.10.x 25           # Fuerza banner SMTP
```

## Interacción manual con servicios

```bash
telnet 10.10.10.x 25              # SMTP: HELO/MAIL FROM/RCPT TO
telnet 10.10.10.x 110             # POP3: USER/PASS
telnet 10.10.10.x 143             # IMAP
```

> [!warning] TELNET
> Telnet transmite en **texto plano** (sin cifrar): credenciales y datos viajan visibles. Solo usar en laboratorios/CTFs — en producción, SSH siempre.

## Nmap como alternativa

```bash
nmap -sV -p <port> <host>         # Detectar versión
nmap -sC -p <port> <host>         # Scripts por defecto
```









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/Hydra.md|Hydra]] — Nmap, Redes, Redes
- [[../../comandos/Nmap.md|Nmap]] — Nmap, Redes, Redes
- [[Nmap.md|Nmap]] — Redes, Redes, Telnet
- [[../01 - Fundamentos de Redes/Redes - Topologías y Encapsulación.md|Redes - Topologías y Encapsulación]] — Nmap, Redes, Redes
- [[../../apuntes evolve/BLOQUE 9.md|BLOQUE 9]] — Hydra, Redes, Redes

### 🌐 Cross-Dominio

- [[../../../programacion/Haskell/patrones_haskell.md|patrones_haskell]] — Programacion: Redes, Testing
- [[../../../ia/ia_payloads.md|ia_payloads]] — IA: Redes, Testing

> #hydra #nmap #redes #redes_ciber #telnet #testing
