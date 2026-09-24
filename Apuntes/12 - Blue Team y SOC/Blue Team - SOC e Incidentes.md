

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

### Operativa del SOC: modalidades, fuentes y ciclo

| Aspecto | Detalle |
|---------|---------|
| **Modalidades** | SOC **24/7** (365 días a cualquier hora) · SOC **8x5** (solo horario laboral de lunes a viernes) |
| **Fuentes de datos** | endpoints, dispositivos IoT, aplicaciones internas y externas, logs de todos los servidores y trazabilidad de patrones de comportamiento de la organización |
| **Principio** | No basta con monitorizar el perímetro externo: también se monitoriza el interior (**Assumed Breach**) |

**Ciclo operativo en 4 fases continuas:**

1. **Monitorización:** recopilación y análisis en tiempo real de todas las fuentes; el dato bruto sin tratar no tiene valor por sí solo — debe correlacionarse para generar información útil.
2. **Detección avanzada (Threat Intelligence):** análisis de comportamiento (actividades inusuales), correlación de eventos (patrones complejos que individualmente parecen inofensivos) e IA/ML para anomalías — herramientas relacionadas: **NDR** y **UEBA**.
3. **Respuesta:** contención (bloqueo de IPs, desconexión de dispositivos, suspensión de cuentas), remediación y recuperación (restauración segura desde backup verificando que el malware no persiste).
4. **Prevención:** nuevos IOCs, reglas de firewall, arquitecturas mejoradas, formación de usuarios — cuanto mejor la prevención, menos respuesta será necesaria.

**Reporting y métricas:** informes mensuales con alertas detectadas y su resolución, vulnerabilidades recurrentes con recomendaciones y **KPIs/SLAs** (tiempos límite de actuación comprometidos contractualmente). Herramienta habitual de visualización: **Kibana** (panel de estado de seguridad en tiempo real).

> **Perspectiva de carrera:** empezar en Blue Team, concretamente en un SOC como N1, lejos de ser un paso atrás, es una de las mejores escuelas para un futuro pentester — permite entender qué se monitoriza y cómo reaccionan las organizaciones ante los ataques, conocimiento imprescindible para después romper esas defensas. El N1, aunque el trabajo parezca mecánico (hojas de ruta/playbooks), gana visibilidad enorme sobre patrones de ataque reales: qué IPs atacan, qué técnicas usan, qué formularios son objetivos frecuentes.

### Vigilancia digital

Línea del Blue Team orientada a amenazas externas en internet: monitoreo de **dark web y foros** de ciberdelincuentes, grupos de Discord y Telegram, con listados de keywords generados por cliente. En el ámbito del phishing, se generan masivamente iteraciones del dominio del cliente y se vigilan **comprobaciones DNS** para detectar registros fraudulentos → **takedown** vía el contacto `abuse@` del registrador (solo procede con motivo: dominio fraudulento). Cruce con **LeakRadar** para credenciales filtradas de empleados. En los ejercicios **TIBER-EU**, la vigilancia digital es el equipo que proporciona al Red Team toda la superficie de exposición de la organización. El **Purple Team** puentea ambos lados: traduce las lecciones del Red Team en mejoras defensivas para el Blue Team y viceversa.

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

### IOC y C2 en la práctica

Un IOC puede ser: dirección IP conocida maliciosa, **hash** de un fichero malicioso (inmutable: dos ficheros con el mismo hash son el mismo fichero), nombre/ruta de fichero o cadena de texto (string) concreta. Los antivirus/EDR/IPS/IDS extraen estos IOC y los envían a una base de datos de firmas compartida entre fabricantes.

El **C2** (Command & Control) es el servidor intermediario que recibe los comandos del atacante y los replica a todos los nodos comprometidos — con cientos de miles de equipos no se va uno por uno a ejecutar `ls`. Más allá de dominios/IPs dedicados, en la práctica se observan C2 sobre infraestructura legítima: **webhooks de Discord** (~3 años de uso), **Telegram** (sobre el webhook, que es simplemente un listener), **subforos de Reddit** (un watcher correlaciona lo publicado con comandos en una base de datos y responde en comentarios) — cualquier servicio con conectividad sirve de C2 si se le da conectividad.

**Caso Yellow Cockatoo (RAT):** se comunicaba con su C2 en el dominio `gogohide.com` (parametrizado con la info del host ya codificada); identificar el dominio C2 y **bloquearlo** corta la comunicación del atacante — prioridad sobre bloquear IPs sueltas, porque al atacante le da igual que le bloqueen una IP si no pierde el C2.

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

### Técnica en profundidad: T1555

**T1555 — Credentials from Password Stores** (táctica Credential Access): robo de credenciales almacenadas en el password store del navegador y del sistema. Sub-técnica observada en laboratorio: **Steal Web Session Cookie** (robo de cookies de sesión). En el análisis dinámico con Any.run, los IDs MITRE se asignan directamente a cada comportamiento detectado, cruzando las acciones observadas con la taxonomía estándar del sector.

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

### Formación y concienciación: el Red Team como formador

La formación en ingeniería social debe impartirla el **Red Team**, no un Blue Team teórico: ya ejecuta phishing, smishing y vishing en sus auditorías, puede diseñar ataques simulados personalizados y, mostrando después a los empleados los resultados reales de la campaña sobre ellos mismos, el impacto es mucho mayor que cualquier presentación teórica.

> **Caso real:** auditoría externa completada en **6 minutos** mediante ingeniería social, obteniendo credenciales válidas para acceder a la organización.

Objetivos: convertir a los empleados en la **primera línea de defensa** (no en el eslabón más débil), reforzar buenas prácticas (no abrir correos fraudulentos, no conectar USB desconocidos, contraseñas robustas) y cumplir normativa — la formación periódica en ciberseguridad es un control exigido por **ISO 27001, ENS, NIS 2 y DORA**. Se personaliza según sector, madurez de los empleados y riesgos específicos de la organización.

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

## 11. Arquitecturas seguras y defensa en profundidad

Una arquitectura segura es el diseño estructural de sistemas, redes y aplicaciones que integra la seguridad desde su concepción (**Security by Design**), no como añadido posterior — planificarla desde el inicio hace cualquier cambio menos costoso y evita generar nuevas vulnerabilidades. Muchas empresas aprovechan las migraciones a cloud para rediseñar con enfoque Zero Trust, cumpliendo ISO 27001, NIS 2 o ENS.

### Pilares

| Pilar | Detalle |
|-------|---------|
| **Mínimo privilegio** | Cada usuario, sistema o proceso solo con los permisos estrictamente necesarios. Hallazgo habitual en auditorías: **9-15 cuentas de Domain Admin cuando debería haber 1-2 como máximo** |
| **Zero Trust** | No confiar automáticamente en nada ni en nadie, dentro ni fuera de la red; verificación constante de identidad y contexto. En la práctica se implementa mediante **Kerberos**, que autentica y autoriza los accesos a todos los servicios sin requerir una contraseña nueva en cada uno |
| **Defense in Depth** | Múltiples capas de seguridad superpuestas: si una capa falla, las siguientes contienen el ataque |

### Segmentación, datos y perímetro

- **Segmentación de red:** dividir la red en zonas aisladas (usuarios, servidores críticos, IoT, red legacy, DMZ) para limitar el impacto — un ransomware bien contenido por segmentación no se propaga al resto de la infraestructura ni a los servidores de backup. Complementar con MFA y autorización basada en roles.
- **Protección de datos:** cifrado en tránsito y reposo con **AES-256** y **TLS 1.2/1.3**. Algoritmos obsoletos que no deben usarse: **MD5, DES, CBC** (en configuraciones débiles) — tener contraseñas cifradas con MD5 es equivalente a tenerlas en texto plano, ya que se rompe en segundos. PCI DSS exige protección específica de nombre, número, caducidad y CVV de tarjetas.
- **Firewalls:** solo deberían modificarlos el perfil especializado; configuración óptima en modo **whitelist** (todo bloqueado por defecto, solo se permite lo necesario). Acompañar de IDS/IPS, balanceadores (DDoS) y VPN/portales seguros de acceso remoto.
- **Caso real:** compromiso completo de la infraestructura interna de un cliente a través de un **portal Citrix mal configurado** que permitía reutilización de credenciales.
- **SIEM + EDR:** centralización y análisis de logs para detección de amenazas en tiempo real, sobre la arquitectura anterior.

---

## 12. Checklist de repaso

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

- [[../../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Hack The Box, Seguridad, Windows
- [[../../apuntes evolve/BLOQUE 11.md|BLOQUE 11]] — Blue Team / SOC, SQL Injection, Seguridad
- [[../../transcripciones/Junio/03.06.2026 HTB Starting Point Tier 1 - SQLi, Responder y LFI en Windows.md|03.06.2026 HTB Starting Point Tier 1 - SQLi, Responder y LFI en Windows]] — Hack The Box, Seguridad, Windows
- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point - Tier 0.md|Hack The Box- Starting Point - Tier 0]] — Blue Team / SOC, Hack The Box, Metodologia Pentest
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]] — Hack The Box, Metodologia Pentest, SQL Injection

### 🌐 Cross-Dominio

- [[../../../programacion/Rust/fundamentos_rust.md|fundamentos_rust]] — Programacion: Desarrollo Web, Linux, Seguridad
- [[../../../programacion/Rust/seguridad_rust.md|seguridad_rust]] — Programacion: Desarrollo Web, Linux, Seguridad

> #blue_team #crypto #error_handling #forense #go #hack_the_box #javascript #kubernetes #lfi #linux #linux_ciber #metasploit #nmap #normativa #osint #pentest #pivoting #post_explotacion #redes #redes_ciber #seguridad #smb_impacket #sqli #ssh_tool #web #windows_ciber #wireshark
