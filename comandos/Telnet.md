# Telnet — Testing de Puertos y Protocolos

> [!info] Herramienta
> Cliente TCP para testing manual de puertos, debugging de protocolos y testing de conectividad.
## Conexión Básica

> [!tip] Uso principal
> Testing rápido de puertos y banner grabbing.

| Comando | Descripción |

| `telnet <host> <puerto>` | Conectar a puerto específico |
| `telnet <host>` | Conectar a puerto 23 (default) |
| `telnet -l <usuario> <host>` | Conectar con usuario |
| `open <host> <puerto>` | Abrir conexión (dentro de telnet) |
| `close` | Cerrar conexión (mantener cliente) |
| `quit` / `exit` | Salir completamente |

```bash
# Testing de puerto
telnet 192.168.1.1 80

# Con usuario
telnet -l admin 192.168.1.1
| ```
## Modo Escape y Comandos

> [!note] Ctrl+] para escape
> Acceder a comandos internos de Telnet.

| Comando | Descripción |

| `Ctrl+]` | Entrar al modo escape |
| `status` | Estado de la conexión |
| `send <secuencia>` | Enviar secuencias de control |
| `set / unset <opción>` | Configurar opciones |
| `toggle <opción>` | Alternar opciones |
| `display <opción>` | Ver valor de opción |

### Opciones Comunes

| Opción | Descripción |
|--------|-------------|
| `echo` | Eco local |
| `crlf` | Convertir LF a CRLF |
| `binary` | Modo binario |
| `skip` | Saltar procesamiento |

```bash
# Ver estado
telnet> status

# Toggle echo
telnet> toggle echo

# Logging
telnet> log session.log

# Suspender (vuelve con fg)
telnet> z
```

---

## Debug

| Comando | Descripción |
|---------|-------------|
| `telnet -d <host> <puerto>` | Debug desde inicio |
| `toggle options` | Ver negociación de opciones |
| `toggle trace` | Hex dump del tráfico |
| `toggle prettydump` | Hex + ASCII legible |
| | `log <archivo>` | Guardar sesión en archivo |
|-----------------------------------------------|---------------------------|
## Protocolo Telnet

> [!abstract] Negociación
> Telnet usa comandos para negociar opciones.

| Comando | Descripción |

| `WILL / WONT` | Servidor anuncia opciones |
| `DO / DONT` | Cliente solicita opciones |
| `SB / SE` | Subnegociación |
| | `IAC (0xFF)` | Interpret As Command |
|------------------------------------|-----------------------------------|
## Testing de Puertos Comunes

> [!important] Diagnóstico rápido
> Probar conectividad manualmente.

| Puerto | Servicio | Comando |

| 21 | FTP | `telnet <host> 21` |
| 22 | SSH | `telnet <host> 22` |
| 23 | Telnet | `telnet <host> 23` |
| 25 | SMTP | `telnet <host> 25` |
| 53 | DNS (TCP) | `telnet <host> 53` |
| 80 | HTTP | `telnet <host> 80` |
| 110 | POP3 | `telnet <host> 110` |
| 143 | IMAP | `telnet <host> 143` |
| 443 | HTTPS | `telnet <host> 443` |
| 3306 | MySQL | `telnet <host> 3306` |

### Diagnóstico

| Mensaje | Significado |
|---------|-------------|
| `Connection refused` | Puerto cerrado |
| | `Timeout` | Firewall o host caído |
|-------------------------------------------|-----------------------|
## Interacción Manual con Protocolos

> [!warning] Práctica
> Envío manual de comandos de protocolos.

### HTTP Manual

```bash
telnet target 80
GET / HTTP/1.1
Host: target.com
[Enter x2]
```

### SMTP

```bash
telnet mail 25
EHLO test.com
VRFY root
QUIT
```

### FTP

```bash
telnet ftp 21
USER anonymous
PASS guest@
LIST
QUIT
```

---

#checklist
- [ ] Testing de puertos con `telnet <host> <puerto>` practicado
- [ ] Modo escape con `Ctrl+]` dominado
- [ ] Debug con `toggle trace` y `log` usado
- [ ] HTTP manual via Telnet probado
- [ ] Diagnóstico: refused vs timeout entendido

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Hydra.md|Hydra]— Redes, SSH, Telnet
- [[../apuntes Chema/Introducción a Redes.md|Introducción a Redes]— Redes, SSH, Telnet
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Anonimato e Ingeniería Social.md|Anonimato e Ingeniería Social]— Redes, SSH
- [[../apuntes Chema/Wireshark.md|Wireshark]— Redes, SSH
- [[Linux.md|Linux]— Redes, SSH
- [[SSH.md|SSH]— Redes, SSH

### 🛠️ Herramientas

- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

> #redes #ssh #telnet
