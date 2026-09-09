| **Campo** | **Detalle** |
| --- | --- |
| **Sesión** | 25 — Repaso, Mercado Laboral y Servicios |
| **Instructor** | Yuba González |
| **Fecha** | (no especificada en el material) |
| **Máquina** | Metasploitable 2 |
| **Temas** | Metasploit · FTP · SMB · Mercado laboral · Marco mental · Nmap · Tmux |

| |
|---|
|ℹ **INFO**<br><br>Sesión de repaso y consolidación: marco mental de 4 elementos, metodología ordenada (carpetas → Nmap 3 fases), y práctica guiada sobre FTP y SMB en Metasploitable 2.|

# 1. Objetivos de la sesión

• Consolidar el **marco mental de 4 elementos** para atacar cualquier servicio.

• Entender el **mapa del mercado laboral** en seguridad ofensiva y situar el perfil junior.

• Aplicar **metodología ordenada**: estructura de carpetas → Nmap en 3 fases.

• Practicar **FTP** (búsqueda de exploit, descarga, autenticación anónima).

• Practicar **SMB/Samba** (enumeración shares, permisos, enum4linux, password spraying).

# 2. Conceptos clave

## 2.1. Marco mental: 4 elementos para atacar servicios

Aplicable a **cualquier vulnerabilidad de servicio**, independientemente del protocolo (FTP, SMB, SSH, HTTP...).

| Elemento | Qué responde | Ejemplo (Log4Shell CVE-2021-44228) |
| :--- | :--- | :--- |
| **1. Fuente** | ¿De dónde viene el input? | Cabecera HTTP `User-Agent`, `X-Forwarded-For`, log de aplicación |
| **2. Procesador** | ¿Qué lo interpreta? | Log4j (librería Java de logging) |
| **3. Ejecución** | ¿Cómo se ejecuta? | JNDI lookup → `ldap://attacker.com/payload` → descarga y ejecuta clase Java |
| **4. Impacto** | ¿Qué se consigue? | RCE como usuario que corre la app (tomcat, www-data...) |

> ✓ **Regla de oro** 
> Si no tienes claro los 4 elementos, **no atacas**. Primero enumeras y entiendes; luego explotas.

## 2.2. Metodología: orden antes que velocidad

### Estructura de carpetas — primer paso siempre

```
/escritorio/
└── objetivo_IP/
 ├── nmap/
 ├── web/
 ├── exploits/
 ├── credenciales/
 └── post-explotacion/
```

> ✓ **Por qué** 
> Evita perder hallazgos, permite reanudar días después y facilita el informe final.

### Nmap en tres fases

| Fase | Comando | Propósito |
| :--- | :--- | :--- |
| **1. Escaneo básico rápido** | `nmap -sC -sV -Pn --min-rate 5000 <IP>` | Puertos comunes, versiones, scripts default. Resultados inmediatos. |
| **2. Todos los puertos** | `nmap -p- -Pn --min-rate 5000 <IP>` | No dejar puertos ocultos (ej. SSH en 22222). |
| **3. Scripts y versiones sobre abiertos** | `nmap -sC -sV -p <puertos_abiertos> -oA nmap/completo <IP>` | Profundizar solo en lo abierto. `-oA` guarda normal, grepeable y XML. |

| Flag | Significado |
| :--- | :--- |
| `-oA` | Guarda en 3 formatos: normal (`.nmap`), grepeable (`.gnmap`), XML (`.xml`) |
| `-Pn` | Omite host discovery (útil si no responde a ping) |
| `-sC` | Equivale a `--script=default`. Lanza scripts de la categoría default |
| `vuln` | Scripts específicos de CVEs. Más intrusiva y lenta. **Usar con cautela en auditorías reales** |

### Tmux — trabajo en paralelo

| Acción | Comando / Teclas |
| :--- | :--- |
| Nueva sesión | `tmux new -s nombre` |
| Dividir panel (horizontal) | `Ctrl+b` → `"` |
| Dividir panel (vertical) | `Ctrl+b` → `%` |
| Moverse entre paneles | `Ctrl+b` → `flecha` |
| Activar ratón | `set -g mouse on` (en `.tmux.conf` o `Ctrl+b` → `:` → `set -g mouse on`) |

> ✓ **Práctica** 
> Panel 1: Nmap. Panel 2: búsqueda de exploits. Panel 3: listener. Panel 4: notas.

## 2.3. FTP — flujo de ataque

1. **Detectar versión** con Nmap (`-sV`).
2. **Buscar exploit** para esa versión: `searchsploit vsftpd 2.3.4` / `msfconsole → search vsftpd`.
3. **Descargar exploit** con flag `-m` (mirror): `searchsploit -m 49757`.
4. **Ejecutar** (ajustar IP/puerto si hace falta).
5. **Verificar autenticación anónima**: `ftp -a <IP>` → `ls`, `cd`, `get`.

| |
|---|
|⚠ **AVISO**<br><br>La cuenta de servicio FTP **no es un usuario del sistema**: solo interactúa con el servicio FTP. Aplica a todos los servicios: Apache, PostgreSQL... cada uno tiene su cuenta de servicio con sus propios permisos.|

## 2.4. SMB / Samba — enumeración y acceso

SMB expone **carpetas compartidas (shares)** en red. La enumeración combina varias herramientas complementarias.

| Herramienta | Comando | Qué aporta |
| :--- | :--- | :--- |
| **smbclient (sesión nula)** | `smbclient -N -L //<IP>/` | Lista shares sin credenciales |
| **NetExec (permisos R/W)** | `nxc smb <IP> -u '' -p '' --shares` | Muestra qué carpetas permiten leer, escribir o ninguna |
| **Conectar a share** | `smbclient -N //<IP>/<share>` | Consola tipo FTP: `help`, `dir`, `get`, `put` |
| **enum4linux** | `enum4linux -a <IP>` | Extrae: dominio, versión Samba, usuarios del sistema, shares, políticas de contraseña |
| **Password Spraying (NetExec)** | `nxc smb <IP> -u usuarios.txt -p 'Password1' --continue-on-success` | Una contraseña contra todos los usuarios. Evita bloqueos en AD |

> ✓ **Usuarios de enum4linux** → alimentan ataques de fuerza bruta / password spraying posteriores.

# 3. Desarrollo técnico — Metasploitable 2 (repaso guiado)

> La sesión repasa la máquina Metasploitable 2 aplicando la metodología arriba. No se detalla paso a paso completo porque es repaso; los vectores clave son:

| Servicio | Puerto | Vector practicado |
| :--- | :--- | :--- |
| FTP | 21 | Autenticación anónima + búsqueda exploit versión |
| SMB | 139/445 | `smbclient -N`, NetExec shares, `enum4linux`, password spraying |

# 4. Mercado laboral en seguridad ofensiva

Mapa de servicios de un equipo de seguridad ofensiva, ordenados por nivel de entrada.

| Perfil | Servicios típicos | Nivel |
| :--- | :--- | :--- |
| **Junior** (foco del máster) | Auditoría web, auditoría de red interna, escalada Linux/Windows, reporting | Entrada |
| **Avanzado / Senior** | Red Team / Adversary Simulation, Cloud Security, Active Directory, Malware Dev, Evasion, C2 development | Senior |
| **Especializaciones** (referencia cultural) | Car hacking · 5G/telcos · Guerra electrónica · ATMs · Auditorías LLMs/IA · Pipelines CI/CD · Docker · OT/ICS industrial | Nicho |

# 5. Herramientas utilizadas en la sesión

| Herramienta | Objetivo | Fase | Comando / Uso visto | Nivel | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Nmap | Puertos, versiones, scripts | Enumeración | 3 fases (ver tabla) | Recurrente | Base de toda metodología |
| Tmux | Multiplexar terminal | Trabajo paralelo | `tmux new -s`, splits, mouse | Practicada | Imprescindible en labs |
| Searchsploit | Buscar exploits locales | Explotación | `searchsploit <servicio> <versión>` | Practicada | `-m` para descargar |
| Metasploit (msfconsole) | Explotación / auxiliares | Explotación | `search`, `use`, `set`, `run` | Introducida | Ver FTP, SMB, PostgreSQL... |
| smbclient | Enumerar / conectar shares SMB | Enumeración | `-N -L`, conectar a share | Practicada | Sesión nula |
| NetExec (nxc) | SMB enum, permisos, spray | Enumeración / Acceso | `nxc smb IP -u '' -p '' --shares` | Practicada | Sucesor de CrackMapExec |
| enum4linux | Enumeración profunda SMB | Enumeración | `enum4linux -a IP` | Practicada | Usuarios, dominio, políticas |
| FTP | Acceso anónimo, descarga | Acceso | `ftp -a IP`, `ls`, `get` | Practicada | Cuenta de servicio |

# 6. Riesgos, errores comunes y buenas prácticas

| |
|---|
|⚠ **AVISO**<br><br>**No atacar sin metodología**. La estructura de carpetas y las 3 fases de Nmap no son opcionales: son lo que separa un trabajo profesional de "probar cosas a ver qué pasa".|

| |
|---|
|⚠ **AVISO**<br><br>**Scripts `vuln` de Nmap**: son intrusivos. En auditoría real, **pedir permiso explícito** antes de lanzarlos. Pueden tirar servicios.|

| |
|---|
|✓ **BUENA PRÁCTICA**<br><br>Guardar **todo** en la estructura de carpetas desde el minuto 1. Salidas de Nmap (`.xml` para parsing), capturas de pantalla, credenciales, hashes, rutas.|

| |
|---|
|✓ **BUENA PRÁCTICA**<br><br>Password spraying **antes** que fuerza bruta clásica en entornos AD. Una contraseña × todos los usuarios = 0 bloqueos.|

# 7. Conexión con sesiones anteriores

• **Nmap 3 fases**: consolida lo visto en sesiones de reconocimiento de red.

• **Estructura de carpetas**: introducida en sesiones previas de Metasploitable / HTB Starting Point.

• **FTP anónimo / SMB sesión nula**: vectores clásicos ya practicados; aquí se encuadran en la metodología ordenada.

• **Marco mental 4 elementos**: nuevo marco transversal para *cualquier* servicio.

# 8. Resumen final

La sesión 25 es un **parada y fonda** metodológica. Se repasa Metasploitable 2 no para "sacar flags", sino para **fijar el orden**: carpetas → Nmap 3 fases → enumeración dirigida (FTP, SMB) → explotación controlada. Se introduce el marco mental de 4 elementos (Fuente → Procesador → Ejecución → Impacto) como brújula para no perderse en cualquier servicio nuevo. Y se contextualiza el mercado laboral: el máster forma para perfil **junior de auditoría web/red**, base para especializarse después.

# 9. Checklist de repaso

☐ ¿Sigo la estructura de carpetas **antes** de lanzar la primera herramienta?

☐ ¿Aplico Nmap en **3 fases** (rápido → todos puertos → profundidad) y guardo `-oA`?

☐ ¿Uso Tmux para paralelizar escaneo, búsqueda de exploits y listener?

☐ ¿Identifico los **4 elementos** (fuente, procesador, ejecución, impacto) antes de explotar un servicio?

☐ ¿Distingo cuenta de servicio FTP/SMB de usuario de sistema?

☐ ¿Enumero SMB con **sesión nula** (`smbclient -N`), **permisos** (NetExec), **profundo** (enum4linux) y **password spray**?

☐ ¿Sé cuándo usar **password spraying** vs fuerza bruta clásica?

# 10. Actualización del registro de herramientas

Bloque copiable a la base de conocimiento del proyecto:

| Herramienta | Nivel | Cambio |
| :--- | :--- | :--- |
| Marco mental 4 elementos | **NUEVO** | Concepto transversal para atacar servicios |
| Estructura de carpetas obligatoria | **Reforzada** | Primer paso siempre |
| Nmap 3 fases | **Reforzada** | Metodología estándar |
| Tmux | **Practicada** | Trabajo paralelo en labs |
| NetExec (nxc) | **Practicada** | SMB enum + password spray |
| enum4linux | **Practicada** | Enumeración profunda SMB |
| searchsploit `-m` | **Practicada** | Descarga directa de exploit |

---

**Fin de apuntes — Sesión 25**



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/MODULO3/resumen_master_clase24.md|resumen_master_clase24]] — IA en Ciberseguridad, Linux, Nmap
- [[../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]] — IA en Ciberseguridad, Linux, Nmap
- [[Mercado Laboral y Servicios.md|Mercado Laboral y Servicios]] — IA en Ciberseguridad, Nmap, Windows
- [[../apuntes Joselu/MODULO3/resumen_master_clase23.md|resumen_master_clase23]] — IA en Ciberseguridad, Linux, Nmap
- [[../apuntes Joselu/MODULO3/resumen_master_clase20.md|resumen_master_clase20]] — IA en Ciberseguridad, Linux, Nmap
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Linux, Metasploit, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]
- [[comandos/Tmux|Tmux]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #empleabilidad #hack-the-box #hydra #ia #linux #metasploit #metasploitable #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #smb-impacket #ssh #tmux #windows
