> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 11 — Blue Team (SOC)
> **Contenido:** Logs, SIEM, MITRE ATT&CK, Wazuh, SOAR — con filtros de Wireshark, reglas y consultas reales

---

## ① Qué es un SOC y cómo se organiza

Un SOC vigila, analiza y responde a incidentes 24/7, estructurado en tres niveles:

| Nivel | Función |
|-------|---------|
| **N1** | Triage inicial, resuelve falsos positivos evidentes |
| **N2** | Investigaciones complejas, ajuste de reglas, automatizaciones |
| **N3** | Incidentes críticos, threat hunting avanzado, forense — interviene muy raramente |

---

## ② Modelo operativo de detección: hipótesis → evidencia → verificación → acción

Antes de cualquier regla, se formula una hipótesis concreta: *"si un atacante compromete una cuenta, veremos intentos de RDP desde orígenes atípicos y fallos seguidos de éxitos"*. Se selecciona la telemetría mínima que la prueba, se correlacionan señales independientes (nunca depender de un solo indicador) y cada alerta termina en una acción operativa concreta.

### Telemetría mínima viable por fuente

| Fuente | Eventos clave |
|--------|--------------|
| **Windows/AD** | Security log 4624/4625 (logon éxito/fallo), 4672 (privilegios especiales), 4769 (Kerberos TGS), 4771/4776 (fallos Kerberos/NTLM). Sysmon: evento 1 (procesos), 3 (conexiones), 10 (comandos), 11 (creación de ficheros), 15 (cambios de registro) |
| **Linux/Unix** | auth.log/journald (SSH), auditd (spawns, módulos) |
| **Red** | DNS (consultas y rcode), proxy/firewall (SNI/URL), NetFlow/IPFIX (5-tupla, bytes, duración) |

---

## ③ Wireshark para el SOC: filtros reales por escenario

Wireshark se usa para validar hipótesis puntuales, no como sonda 24/7.

```bash
# Inicios de conexión TCP (para detectar escaneo/reconocimiento)
tcp.flags.syn==1 && tcp.flags.ack==0

# ClientHello TLS (para detectar beaconing periódico)
tls.handshake.type==1

# Filtrar por SNI concreto (atribuir un servicio, ej. subida de datos)
tls.handshake.extensions_server_name contains "upload"

# QUIC con datagramas densos (posible exfiltración por HTTP/3)
quic && udp.length > 100 && frame.time_delta_displayed <= 0.5

# Movimiento lateral SMB (comandos CREATE/WRITE)
smb2 && smb2.cmd in {5,9}

# DNS anómalo: respuestas de error en ráfaga (posible DGA/túnel)
dns.flags.rcode != 0
dns.qry.type==16 # muchas consultas TXT también es señal de túnel DNS

# Diagnóstico de falsos incidentes por PMTUD roto ("no carga la web")
icmp.type in {3,11}
icmpv6.type==2
```

---

## ④ Detecciones de alto valor: señal, herramienta y acción

### Autenticación sospechosa (RDP/VPN)

**Señal:** múltiples eventos 4625 seguidos de un 4624 para el mismo usuario desde un origen atípico, NLA inactivo en RDP público.
**Acción:** obligar MFA, cerrar RDP a Internet (solo VPN + ACL), revisar la cuenta.

### Movimiento lateral (SMB/WinRM/RDP)

**Señal:** creación/escritura en `ADMIN$` seguida de un servicio temporal (patrón tipo psexec), tickets Kerberos hacia un servicio (`cifs/host`) no habitual.
**Acción:** exigir SMB signing, aislar la estación, rotar credenciales.

### Beaconing cifrado (C2)

**Señal:** ClientHello cada 60±2s con ALPN=h2, o flujo QUIC con tamaño de datagrama casi constante; JA3/JA3S repetido con IP/ASN rotando.
**Acción:** bloqueo por SNI/ASN/JA3, adquisición del endpoint.

### Exfiltración

**Señal:** Subida ≫ Bajada durante 10-20 minutos hacia un destino único, precedida de compresión (ZIP) en el servidor de archivos.
**Acción:** cortar el destino, preservar PCAP, revisar permisos del endpoint.

---

## ⑤ IOC vs IOA

| Concepto | Definición | Dirección |
|----------|-----------|-----------|
| **IOC** (Indicador de Compromiso) | Evidencia de que un sistema ya ha sido comprometido — IP maliciosa, hash, dominio de phishing | Mira al **pasado** |
| **IOA** (Indicador de Ataque) | Comportamiento sospechoso que sugiere un ataque en curso, aunque no coincida con ninguna huella ya catalogada — usuario probando credenciales en múltiples sistemas, escaneo interno | **Anticipa** |

> [!important] Diferencia clave
> El IOC confirma; el IOA anticipa.

---

## ⑥ MITRE ATT&CK: tácticas, técnicas y subtécnicas con ejemplos

MITRE no detecta por sí mismo: clasifica lo ya detectado por otras herramientas.

| Táctica | Técnica | Ejemplo |
|---------|---------|---------|
| **Initial Access** | Phishing | Correo diseñado para que el usuario pulse un enlace o entregue credenciales |
| **Execution** | PowerShell | Uso de una herramienta legítima del sistema para ejecutar código (LOLBin) |
| **Discovery** | Network Service Discovery | Una IP externa conectando a 150 puertos de un único host en un minuto — no es reconocimiento amplio de red, es enumeración centrada en una máquina concreta |
| **Credential Access** | Password Spraying | Veinte intentos fallidos sobre veinte cuentas distintas con la misma contraseña común — distinto de la fuerza bruta clásica (muchas contraseñas contra una sola cuenta) |
| **Command and Control** | Web Protocols | Un host interno conectando a una IP externa por el puerto 443 — muchos C2 se camuflan en protocolos que parecen tráfico normal |

---

## ⑦ Wazuh: reglas reales paso a paso

### Estructura de una regla local (XML)

```xml
<group name="local,syslog,">
 <rule id="100100" level="10">
 <if_sid>530</if_sid>
 <match>demo alert</match>
 <description>Regla de prueba: patrón "demo alert" detectado</description>
 </rule>
</group>
```

### Probar una regla con un log de ejemplo antes de producción

```bash
# Inyectar un log de prueba en el archivo monitorizado
echo "$(date) demo alert desde host de prueba" >> /var/log/demo.log

# Reiniciar el servicio tras cualquier cambio de configuración
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager
```

### Añadir una nueva fuente de logs (ossec.conf)

```xml
<localfile>
 <log_format>syslog</log_format>
 <location>/var/log/demo.log</location>
</localfile>
```

> [!note] Principio clave de Wazuh
> Una alerta no siempre señala el efecto más llamativo, sino el mecanismo subyacente. Por ejemplo, una alerta por uso de sudo no salta por el comando ejecutado en sí, sino por el propio uso del privilegio elevado — hay que leer siempre la descripción completa de la regla.

---

## ⑧ Reglas de correlación tipo Sigma/KQL (idea + umbral)

```yaml
# RDP sospechoso
# idea: usuario con >5 fallos + 1 éxito en 30 min desde IP nueva

# SMB escritura en admin shares
# idea: evento de creación/escritura remota + servicio creado después (<=5 min)

# Beaconing
# idea: coeficiente de variación de inter-arrivals < 0.2 durante >= 30 min

# Exfiltración
# idea: sum(bytes_out) / sum(bytes_in) > 5 y duración > 600s

# DNS DGA/túnel
# idea: NXDOMAIN > N y TXT > X en 10 minutos por cliente
```

> [!note] Regla de oro
> Cada umbral debe llevar una justificación documentada y revisarse en post-mortems para reducir el ruido de falsos positivos sin perder cobertura real.

---

## ⑨ SOAR: anatomía de un playbook

Un playbook combina: **disparador** (la alerta inicial) → **clasificador** (qué tipo de incidente es) → **mapper** (traduce campos de origen a variables) → **condicionales** (¿la IP es maliciosa? ¿hubo tráfico permitido?) → **acciones** (bloquear, abrir ticket, notificar, escalar).

### Ejemplo de playbook para login desde país inusual

1. Recuperar datos del usuario en el directorio corporativo
2. Enviar correo de confirmación
3. Si no confirma en un tiempo razonable → escalar a N1/contacto directo
4. Si confirma que **no** fue él:
 - Bloquear cuenta, revocar sesiones
 - Forzar cambio de contraseña
 - Bloquear IP en firewall
5. Si confirma que **sí** era él → cerrar como falso positivo y añadir una excepción temporal para ese contexto

> [!important] Regla de oro
> Primero se ajusta la detección (reducir falsos positivos) y solo después se automatiza la respuesta. Automatizar una detección mal calibrada solo acelera el ruido.

---

## ⑩ Análisis de phishing paso a paso

1. Revisar remitente, asunto, contenido y enlaces del correo sospechoso
2. Escribir cualquier URL sospechosa con el punto entre corchetes para evitar clics accidentales: `malicious[.]com`
3. Comprobar reputación del dominio/URL en VirusTotal o URLScan
4. Buscar en el SIEM si algún usuario llegó a hacer clic o a introducir credenciales
5. Si hubo acceso permitido a un sitio que imitaba un portal de autenticación real: revocar sesiones activas, forzar cambio de contraseña, bloquear dominio/URL

---

## ⑪ EDR, LOLBins y firewalls

El EDR vigila directamente el endpoint, lo que resulta crítico en teletrabajo: si un usuario no pasa por la red corporativa, el firewall no ve su tráfico, pero el EDR sí acompaña al dispositivo.

Los **LOLBins** (Living Off the Land Binaries) son herramientas legítimas del sistema (PowerShell, certutil, mshta) reutilizadas con fines maliciosos precisamente para evitar levantar sospechas — el análisis de procesos debe distinguir siempre entre un uso legítimo y un uso anómalo de estas mismas herramientas.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/MODULO3/resumen_master_clase22.md|resumen_master_clase22]] — Forense Digital, Linux, Windows
- [[../Apuntes/12 - Blue Team y SOC/Blue Team - SOC e Incidentes.md|Blue Team - SOC e Incidentes]] — Forense Digital, Linux, SMB / Impacket
- [[../Apuntes/02 - Sistemas Operativos/Linux - Bash Scripting.md|Linux - Bash Scripting]] — Forense Digital, Linux, Windows
- [[../Apuntes/comandos/Hydra.md|Hydra]] — Hydra, Linux, SSH
- [[../transcripciones/Septiembre/07.09.2026 SQLi - Fundamentos de SQL.md|07.09.2026 SQLi - Fundamentos de SQL]] — Hydra, Linux, SSH
- [[../apuntes Chema/Bash Scripting.md|Bash Scripting]] — Forense Digital, Linux, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

> #blue-team #forense #hydra #linux #redes #smb-impacket #ssh #windows #wireshark
