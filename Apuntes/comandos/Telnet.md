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

- [[Nmap - Escaneo y Enumeración]] — Mejor alternativa para banner grabbing

> #telnet #herramientas #recon
