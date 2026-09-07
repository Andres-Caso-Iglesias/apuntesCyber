

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

- [[../../apuntes Joselu/MODULO1/resumen_master_clase2.md|resumen_master_clase2]— Escalada de Privilegios, Redes, Windows
- [[../../apuntes Joselu/MODULO3/resumen_master_clase22.md|resumen_master_clase22]— Redes, Windows, Wireshark
- [[../../apuntes Joselu/MODULO3/resumen_master_clase17.md|resumen_master_clase17]— Escalada de Privilegios, Redes, Windows
- [[../../apuntes Joselu/MODULO1/resumen_master_clase5.md|resumen_master_clase5]— Escalada de Privilegios, Redes, Windows
- [[../09 - Pivoting y Movilidad Lateral/Pivoting y Movilidad Lateral.md|Pivoting y Movilidad Lateral]— Escalada de Privilegios, Post-Explotación, Redes
- [[../../apuntes evolve/BLOQUE 11.md|BLOQUE 11]— Redes, Windows, Wireshark

### 🛠️ Herramientas

- [[comandos/Netcat|Netcat / Reverse Shells]]

> #blue-team #escalada-privilegios #forense #linux #netcat #post-explotacion #redes #reverse-shell #windows #wireshark
