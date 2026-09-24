

> **Relacionado:** [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]] · [[Wireshark - Análisis de Tráfico]]

---

## 1. Orden de volatilidad y cadena de custodia

El orden de volatilidad define qué evidencia expira antes: registros en caché y tablas ARP, después conexiones activas, después la RAM, y en último lugar el disco.

> **Pregunta guía:** ¿Qué perdería para siempre si reinicio el sistema ahora?

### Orden de volatilidad (de más a menos volátil)

```
1. Registros de caché, tablas ARP, cache DNS
2. Conexiones de red activas (TCP/UDP)
3. Tablas de procesamiento (RAM, procesos en ejecución)
4. Información de disco (archivos, logs)
5. Datos en cintas, backups remotos
```

### Cadena de custodia

Documentar quién, cuándo, dónde y cómo se realizó la captura, calculando un hash del volcado para garantizar su integridad:

```bash
sha256sum equipo1.mem > equipo1.mem.sha256
```

**Documentación obligatoria:**
- Fecha y hora exacta de la captura (UTC)
- Nombre del analista responsable
- Herramienta utilizada
- Hash SHA-256 del volcado
- Estado del sistema antes de la captura (encendido, suspendido, etc.)

### Analizar antes de volcar

Antes de tocar nada: **analizar la situación** — ¿el incidente es de red? ¿podría estar todo cifrado? ¿cuál es el trabajo mínimo indispensable? Solo después se decide el volcado. Orden correcto: **análisis de situación → volcado de volátil → copia de disco → análisis**. La volátil se volca siempre antes que el disco porque para copiar el disco hay que apagar el equipo, y al apagarlo se pierde la RAM.

### Reglas periciales de integridad (juicio)

- **Tres copias:** *original* (solo para obtener hashes y copias, nunca se manipula), *copia de trabajo* (la única analizable; si se corrompe, se recrea del original) y *copia de seguridad* (guardada intacta desde el primer momento).
- **Hash admisible:** SHA-256 — y por prudencia también SHA-512. **MD5 está roto** (vulnerable a colisión: dos ficheros distintos pueden compartir hash) y **SHA-1 se rechaza preventivamente** por muchos jueces; un informe firmado con MD5 se desestima en juicio.
- **Herramienta de hash pericial:** 7-Zip — menú CRC SHA → SHA-256/512 sobre el fichero (nombre + tamaño + hash verifican integridad).
- **Evidencia física:** foto del disco donde se vea pegatina, **serial number y PAN** (únicos por modelo), garantizando que el disco fotografiado es el del informe.
- **Conservación:** el perito guarda las copias de seguridad **5 años** por ley (o deposita el original en custodia judicial si el caso puede revisarse).
- **Cadena de custodia ≠ cadena de acceso:** la custodia garantiza la integridad de las pruebas; el acceso se documenta con timestamps de quién entró, cuándo y qué acción hizo, con firma del perito responsable.

> **Trampas que invalidan evidencias:** hora del sistema incorrecta, falta de precinto físico al recoger el dispositivo, más de 24 horas entre recogida y etiquetado, diferencia entre creation/modified time del fichero y los timestamps del informe, recogida sin grabación en vídeo.

### Timestamps: qué revela cada fecha

| Timestamp | Significado |
|-----------|-------------|
| **Creation time** | Cuándo se creó/compiló el fichero (la creación real es la compilación, no escribir el código) |
| **Modified time** | Última lectura o escritura |
| **First submission (VT)** | Primera vez que se subió a VirusTotal |
| **First seen in the wild** | Primera vez detectado en uso real en Internet |

**Caso Yellow Cockatoo:** creado el 24-09-2020, subido a VirusTotal 20 días después (15-10-2020), visto "in the wild" unos 2 meses después de la creación → malware dirigido a un objetivo concreto, refinado en laboratorio privado, que al ser ya detectable se liberó masivamente para amortizar el desarrollo. El gap creation/first-submission es señal de OPSEC: el atacante prueba el malware contra los antivirus de la víctima — cómo saber qué antivirus usa esa empresa sin acceder a sus sistemas: PDFs públicos de la organización analizados con **FOCA** revelan SO, hostname, versión de software y usuario.

### DeFIR: respuesta a incidentes (4 fases)

El **DeFIR** (Digital Forensics and Incident Response) corresponde al perfil **N3** del SOC: entra cuando hay una **brecha confirmada** (no ante un simple intento de fuerza bruta). Ciclo: **detección y análisis inicial → contención** (desconectar sistemas, aislar segmentos, bloquear cuentas) **→ erradicación** (borrar backdoors/malware, corregir vulnerabilidades explotadas) **→ recuperación** (restaurar desde copias verificadas y bastionar). Aquí se ve todo el valor de la segmentación de red y el Zero Trust. Los peritos con certificación adecuada pueden testificar ante el juez.

### El rol del forense

El forense es, en la práctica, **el N3 de un SOC**. Según la experiencia de clase, los mejores forenses suelen venir del **Red Team**: quien ataca a diario sabe exactamente qué rastros deja y dónde mirar — mira en muchos sitios en los que no miraría un N3 de SOC. En España, para casos complejos el Estado subcontrata peritos privados (p. ej. S21sec): el informe lo presenta la fiscalía y el técnico comparece como perito adscrito al juzgado. INCIBE no investiga directamente: deriva los casos a los cuerpos correspondientes según el tipo de incidente.

---

## 2. Adquisición según el sistema operativo

### Windows (WinPMEM)

```bash
.\winpmem_mini_x64.exe --format raw --output \\servidor\caso\equipo1.mem

# O en formato AFF4 (más compacto, con metadatos y firma)
.\winpmem_mini_x64.exe --format aff4 --output \\servidor\caso\equipo1.aff4
```

### Linux (LiME)

```bash
insmod lime.ko "path=/mnt/forense/host.mem format=raw"

# Envío por red (con un receptor netcat en el recolector):
insmod lime.ko "path=tcp:192.168.1.50:4444 format=raw"
```

### Entornos virtualizados

La RAM de una VM puede tomarse desde el hipervisor (snapshot con memoria), evitando contaminar el sistema comprometido. Se documenta la hora exacta del snapshot y el estado (quiesced).

> **Importante:** Nunca apagar la máquina antes de adquirir memoria. Se pierde la evidencia más rica de forma irreversible.

---

## 3. Triage rápido antes de Volatility

```bash
# Buscar dominios/IPs sospechosas en texto plano dentro del volcado
strings equipo1.mem | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u

# Identificar familias de malware conocidas con reglas YARA
yara -s -r rules/index.yar equipo1.mem > hallazgos_yara.txt

# Buscar cadenas de texto relevantes (credenciales, URLs, comandos)
strings equipo1.mem | grep -iE '(password|passwd|admin|login|http|https|cmd|powershell)'
```

### Flujo de análisis de malware: estático → dinámico

1. **Análisis estático** sobre el volcado: procesos y ficheros raros, strings, YARA — sin ejecutar nada.
2. Si aparece algo, **análisis dinámico** en una **sandbox** (máquina virtual sin conectividad ni visibilidad al resto de la red, donde se puede desplegar ransomware o lo que sea sin riesgo). La más conocida es **Any.run** (versión gratuita utilizable): árbol de procesos, Connections (URLs/IPs), Files, command lines y asignación automática de IDs **MITRE ATT&CK** a cada comportamiento detectado.

### VirusTotal como inteligencia (con restricciones)

- **Proveedor universal:** hoy es el proveedor de inteligencia de amenazas de Kaspersky, Bitdefender, CrowdStrike, Panda y prácticamente todos los fabricantes — la base de datos de firmas de malware más grande del planeta.
- **Dos métricas clave:** *score de antivirus* (motores que lo detectan — un malware muy reciente puede tener 0/70) y *community score* (investigadores que lo marcan antes que los motores: 0 en antivirus + 99 en comunidad = señal de alerta importante).
- **Flujo:** subir fichero o pegar hash → score → pestaña *Details → History* (creation, first submission, in the wild) → pestaña *Relations* (URLs/dominios C2 contactados, ficheros relacionados) → nombres por familia (RAT, ransomware, stealer…).

> **Restricción CNI:** cuando se trabaja para el CNI u otras agencias de inteligencia **está prohibido subir muestras a VirusTotal** — indexar la muestra en la base pública alertaría al atacante y revelaría el conocimiento de la herramienta.

### Forense de red: reconstruir desde un PCAP

El forense digital se divide en **forense de red** (tráfico capturado, herramienta principal Wireshark) y **forense de equipo** (volátil con Volatility, estático con Autopsy). Ante un PCAP con decenas de miles de paquetes, el método es siempre macro → detalle:

1. **Statistics → Protocol Hierarchy:** % por protocolo — TCP 99%+ = entorno IT Windows; SMBv2 = intercambio de ficheros Windows; HTTP = texto claro analizable. Pocos paquetes pero muchos bytes = posible exfiltración.
2. **Statistics → Conversations (IPv4):** qué IPs hablan, cuántos paquetes y en qué dirección fluye más tráfico (un desequilibrio grande de bytes revela el rol de cada actor).
3. **Casos de laboratorio (CyberDefenders):** movimiento lateral **PSEXEC sobre SMB** — en la autenticación NTLM el campo *Target Name* revela el hostname víctima y el usuario comprometido (el challenge/response previo solo existe en TCP); y en HTTP, una `%27` (comilla simple) en parámetros seguida de `500 Internal Server Error` es casi siempre SQL Injection confirmada.

**CyberDefenders** es la plataforma de laboratorios Blue Team (el HackTheBox del perfil defensivo): descargas PCAP/logs protegidos con contraseña, abres en Wireshark y respondes preguntas que simulan un proceso de investigación real.

---

## 4. Flujo completo con Volatility 3

### 1. Inventario de procesos y jerarquía

```bash
vol -f equipo1.mem windows.pslist
vol -f equipo1.mem windows.pstree

# Buscar procesos huérfanos, nombres "casi legítimos", timestamps anómalos
```

### 2. Ejecución oculta e inyecciones

```bash
vol -f equipo1.mem windows.psscan
vol -f equipo1.mem windows.malfind
vol -f equipo1.mem windows.cmdline

# Comparar pslist vs psscan: procesos que aparecen en psscan pero no en
# pslist pueden estar ocultos mediante técnicas anti-forenses (DKOM)
```

### 3. Módulos y DLLs

```bash
vol -f equipo1.mem windows.dlllist
vol -f equipo1.mem windows.handles

# DLLs cargadas fuera de rutas típicas, handles a sockets/archivos raros
```

### 4. Red en vivo

```bash
vol -f equipo1.mem windows.netscan

# Conexiones salientes a infraestructura maliciosa, puertos inusuales
```

### 5. Credenciales y secretos

```bash
vol -f equipo1.mem windows.hashdump # SAM en memoria
vol -f equipo1.mem windows.lsadump # LSA secrets/tickets
vol -f equipo1.mem windows.ssdt # hooks en kernel (evasion)
```

> **Advertencia:** No reutilizar credenciales obtenidas fuera del ámbito estrictamente forense de la investigación.

### 6. Artefactos de usuario

```bash
vol -f equipo1.mem windows.registry.printkey --key \
 "Software\Microsoft\Windows\CurrentVersion\Run"
vol -f equipo1.mem windows.clipboard
```

### 7. Extracción de binarios para reversing

```bash
vol -f equipo1.mem windows.dumpfiles --name malware.exe -o ./exhibits
sha256sum ./exhibits/malware.exe
```

**Equivalentes en Linux:** `linux.pslist`, `linux.netstat`, `linux.hashdump`, `linux.lsmod`

---

## 5. Errores frecuentes

| Error | Consecuencia |
|-------|-------------|
| Apagar la máquina antes de adquirir memoria | Se pierde la evidencia más rica de forma irreversible |
| Usar herramienta incompatible con versión/driver del SO | Dump incompleto |
| No documentar contexto (hora exacta, zona horaria, build del SO) | Dificulta la interpretación |
| Confiar solo en pslist sin comparar con psscan | Procesos ocultos quedan fuera del análisis |
| No calcular hash del volcado | No se puede verificar integridad en auditoría |

---

## 6. Checklist de repaso

- [ ] Conozco el orden de volatilidad y por qué importa
- [ ] Sé adquirir memoria en Windows (WinPMEM) y Linux (LiME)
- [ ] Documento la cadena de custodia correctamente
- [ ] Uso Volatility 3 para análisis de procesos, red y credenciales
- [ ] Comparo pslist vs psscan para detectar DKOM
- [ ] Nunca apago una máquina antes de adquirir memoria

---

> **Siguiente tema:** [[Blue Team - SOC e Incidentes]] — SOC, SIEM, MITRE ATT&CK, Wazuh, SOAR









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../comandos/Metasploit.md|Metasploit]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../09 - Pivoting y Movilidad Lateral/Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]] — Blue Team / SOC, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../comandos/Netcat.md|Netcat]] — Linux, Metodologia Pentest, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../programacion/PowerShell/seguridad_powershell.md|seguridad_powershell]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../programacion/Ciberseguridad/hacking_etico.md|hacking_etico]] — Programacion: CLI/Scripting, Linux, Redes

> #blue_team #cli #crypto #escalada_privilegios #forense #linux #linux_ciber #metasploit #netcat #pentest #pivoting #post_explotacion #redes #reverse_shell #windows_ciber #wireshark
