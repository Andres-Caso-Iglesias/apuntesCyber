> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 10 — Forense y Análisis de Memoria
> **Contenido:** Adquisición de memoria y análisis con Volatility — comandos completos por sistema operativo

---

## ① Orden de volatilidad y cadena de custodia

El orden de volatilidad define qué evidencia expira antes: registros en caché y tablas ARP, después conexiones activas, después la RAM, y en último lugar el disco.

> [!important] Pregunta guía
> ¿Qué perdería para siempre si reinicio el sistema ahora?

**Cadena de custodia:** documentar quién, cuándo, dónde y cómo se realizó la captura, calculando un hash del volcado para garantizar su integridad:

```bash
sha256sum equipo1.mem > equipo1.mem.sha256
```

---

## ② Adquisición según el sistema operativo

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

---

## ③ Triage rápido antes de Volatility

```bash
# Buscar dominios/IPs sospechosas en texto plano dentro del volcado
strings equipo1.mem | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u

# Identificar familias de malware conocidas con reglas YARA
yara -s -r rules/index.yar equipo1.mem > hallazgos_yara.txt
```

---

## ④ Flujo completo con Volatility 3

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

> [!warning] Nunca reutilizar credenciales
> No reutilizar credenciales obtenidas fuera del ámbito estrictamente forense de la investigación.

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

## ⑤ Errores frecuentes

| Error | Consecuencia |
|-------|-------------|
| Apagar la máquina antes de adquirir memoria | Se pierde la evidencia más rica de forma irreversible |
| Usar herramienta incompatible con versión/driver del SO | Dump incompleto |
| No documentar contexto (hora exacta, zona horaria, build del SO) | Dificulta la interpretación |
| Confiar solo en pslist sin comparar con psscan | Procesos ocultos quedan fuera del análisis |