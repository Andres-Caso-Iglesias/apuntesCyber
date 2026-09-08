

> **Relacionado:** [[Wireshark - Análisis de Tráfico]] · [[Nmap - Escaneo y Enumeración]] · [[OSINT - Metodología y Fuentes]]

---

## 1. Qué es un SOC y cómo se organiza

Un SOC (Security Operations Center) vigila, analiza y responde a incidentes 24/7, estructurado en tres niveles:

| Nivel | Función |
|-------|---------|
| **N1** | Triage inicial, resuelve falsos positivos evidentes |
| **N2** | Investigaciones complejas, ajuste de reglas, automatizaciones |
| **N3** | Incidentes críticos, threat hunting avanzado, forense — interviene muy raramente |

> **Diferencia con pentesting:** El SOC es operaciones continuas (defensa), el pentesting es un proyecto puntual (ofensiva). Un buen profesional de ciberseguridad entiende ambos lados.

---

## 2. Modelo operativo de detección

**Hipótesis → Evidencia → Verificación → Acción**

Antes de cualquier regla, se formula una hipótesis concreta: *"si un atacante compromete una cuenta, veremos intentos de RDP desde orígenes atípicos y fallos seguidos de éxitos"*. Se selecciona la telemetría mínima que la prueba, se correlacionan señales independientes (nunca depender de un solo indicador) y cada alerta termina en una acción operativa concreta.

### Telemetría mínima viable por fuente

| Fuente | Eventos clave |
|--------|--------------|
| **Windows/AD** | Security log 4624/4625 (logon éxito/fallo), 4672 (privilegios especiales), 4769 (Kerberos TGS), 4771/4776 (fallos Kerberos/NTLM). Sysmon: evento 1 (procesos), 3 (conexiones), 10 (comandos), 11 (creación de ficheros), 15 (cambios de registro) |
| **Linux/Unix** | auth.log/journald (SSH), auditd (spawns, módulos) |
| **Red** | DNS (consultas y rcode), proxy/firewall (SNI/URL), NetFlow/IPFIX (5-tupla, bytes, duración) |

---

## 3. Wireshark para el SOC: filtros reales por escenario

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

## 4. Detecciones de alto valor

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

## 5. IOC vs IOA

| Concepto | Definición | Dirección |
|----------|-----------|-----------|
| **IOC** (Indicador de Compromiso) | Evidencia de que un sistema ya ha sido comprometido — IP maliciosa, hash, dominio de phishing | Mira al **pasado** |
| **IOA** (Indicador de Ataque) | Comportamiento sospechoso que sugiere un ataque en curso, aunque no coincida con ninguna huella ya catalogada — usuario probando credenciales en múltiples sistemas, escaneo interno | **Anticipa** |

> **Diferencia clave:** El IOC confirma; el IOA anticipa.

---

## 6. MITRE ATT&CK: tácticas, técnicas y subtécnicas

MITRE no detecta por sí mismo: clasifica lo ya detectado por otras herramientas.

| Táctica | Técnica | Ejemplo |
|---------|---------|---------|
| **Initial Access** | Phishing | Correo diseñado para que el usuario pulse un enlace o entregue credenciales |
| **Execution** | PowerShell | Uso de una herramienta legítima del sistema para ejecutar código (LOLBin) |
| **Discovery** | Network Service Discovery | Una IP externa conectando a 150 puertos de un único host en un minuto |
| **Credential Access** | Password Spraying | Veinte intentos fallidos sobre veinte cuentas distintas con la misma contraseña común |
| **Command and Control** | Web Protocols | Un host interno conectando a una IP externa por el puerto 443 |
| **Lateral Movement** | Pass the Hash | Autenticación usando hash NTLM sin crackear la contraseña |
| **Exfiltration** | Exfiltration Over C2 Channel | Datos subidos a través del mismo canal C2 used for command and control |

---

## 7. Wazuh: reglas reales paso a paso

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

> **Principio clave de Wazuh:** Una alerta no siempre señala el efecto más llamativo, sino el mecanismo subyacente. Por ejemplo, una alerta por uso de sudo no salta por el comando ejecutado en sí, sino por el propio uso del privilegio elevado — hay que leer siempre la descripción completa de la regla.

---

## 8. SOAR: anatomía de un playbook

Un playbook combina: **disparador** (la alerta inicial) → **clasificador** (qué tipo de incidente es) → **mapper** (traduce campos de origen a variables) → **condicionales** (¿la IP es maliciosa? ¿hubo tráfico permitido?) → **acciones** (bloquear, abrir ticket, notificar, escalar).

### Ejemplo de playbook para login desde país inusual

1. Recuperar datos del usuario en el directorio corporativo
2. Enviar correo de confirmación
3. Si no confirma en un tiempo razonable → escalar a N1/contacto directo
4. Si confirma que **no** fue él:
 - Bloquear cuenta, revocar sesiones
 - Forzar cambio de contraseña
 - Bloquear IP en firewall
5. Si confirma que **sí** era él → cerrar como falso positivo y añadir una excepción temporal

> **Regla de oro:** Primero se ajusta la detección (reducir falsos positivos) y solo después se automatiza la respuesta. Automatizar una detección mal calibrada solo acelera el ruido.

---

## 9. Análisis de phishing paso a paso

1. Revisar remitente, asunto, contenido y enlaces del correo sospechoso
2. Escribir cualquier URL sospechosa con el punto entre corchetes para evitar clics accidentales: `malicious[.]com`
3. Comprobar reputación del dominio/URL en VirusTotal o URLScan
4. Buscar en el SIEM si algún usuario llegó a hacer clic o a introducir credenciales
5. Si hubo acceso permitido a un sitio que imitaba un portal de autenticación real: revocar sesiones activas, forzar cambio de contraseña, bloquear dominio/URL

> **Relacionado con:** [[Anonimato, Ingeniería Social y Enumeración Web]]

---

## 10. EDR, LOLBins y firewalls

El EDR vigila directamente el endpoint, lo que resulta crítico en teletrabajo: si un usuario no pasa por la red corporativa, el firewall no ve su tráfico, pero el EDR sí acompaña al dispositivo.

Los **LOLBins** (Living Off the Land Binaries) son herramientas legítimas del sistema (PowerShell, certutil, mshta) reutilizadas con fines maliciosos precisamente para evitar levantar sospechas — el análisis de procesos debe distinguir siempre entre un uso legítimo y un uso anómalo de estas mismas herramientas.

### Ejemplos de LOLBins peligrosos

| Binario | Uso legítimo | Uso malicioso |
|---------|-------------|---------------|
| **PowerShell** | Gestión de sistemas | Ejecución de payloads, descarga de malware |
| **certutil** | Gestión de certificados | Descarga de archivos (certutil -urlcache -split -f) |
| **mshta** | Ejecutar archivos .hta | Ejecutar JavaScript malicioso |
| **wmic** | Gestión WMI | Ejecución remota de comandos |
| **regsvr32** | Registro de DLLs | Bypass de AppLocker, descarga de payloads |

---

## 11. Checklist de repaso

- [ ] Conozco la estructura de un SOC (N1/N2/N3)
- [ ] Aplico el modelo hipótesis → evidencia → verificación → acción
- [ ] Uso Wireshark para validar hipótesis con filtros específicos
- [ ] Distingo IOC (pasado) de IOA (anticipa)
- [ ] Clasifico técnicas en el marco MITRE ATT&CK
- [ ] Configuro reglas básicas en Wazuh
- [ ] Diseño playbooks SOAR para automatizar respuestas
- [ ] Analizo phishing siguiendo un proceso structured

---

> **Siguiente tema:** [[Normativa - ISO 27001, GDPR, ENS]] — Marco regulatorio y gestión de riesgos


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point — Tier 0.md|Hack The Box- Starting Point — Tier 0]] — Forense Digital, Linux, SMB / Impacket
- [[../../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Linux, Normativa / GRC, Post-Explotación
- [[../../apuntes evolve/BLOQUE 11.md|BLOQUE 11]] — Forense Digital, Linux, SMB / Impacket
- [[../../apuntes Joselu/MODULO2/resumen_master_clase16.md|resumen_master_clase16]] — Forense Digital, Post-Explotación, SMB / Impacket
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]] — Blue Team / SOC, Linux, Windows
- [[../../comandos/Metasploit.md|Metasploit]] — Linux, Post-Explotación, SSH

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

> #blue-team #forense #hack-the-box #linux #nmap #normativa #osint #pentest #post-explotacion #redes #smb-impacket #ssh #windows #wireshark
