

> [!info] Relacionado con
> [[Nmap - Escaneo y Enumeración]] · [[Enumeración Web]] · [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[Pivoting y Movilidad Lateral]]

---

## ① Las fases del pentest

```
Superficie expuesta → Enumeración → Explotación → Mov. lateral → Escalada → Persistencia → Reporte
```

### Las 5 fases de una auditoría (clase 25.05)

| Fase | Qué se hace | Herramientas |
|------|-------------|--------------|
| **1. Reconocimiento** | Descubrir qué hay en la red | Net-Discover, ARP-Scan, ping con TTL |
| **2. Enumeración** | Identificar servicios y versiones de cada host | `nmap -sC -sV`, smbclient, FTP anónimo |
| **3. Análisis de vulnerabilidades** | Buscar exploits conocidos para las versiones encontradas | SearchSploit, ExploitDB |
| **4. Explotación** | Usar esos exploits para obtener acceso | Metasploit, scripts Python, Hydra |
| **5. Post-explotación** | Dentro: escalar hasta root y mantener acceso (persistencia) | `sudo -l`, SUID, GTFOBins |

> [!important] EXPLOTACIÓN VS POST-EXPLOTACIÓN (BLOQUE 5)
> **Explotación** = entrar al sistema con cualquier usuario. **Post-explotación** = todo lo que ocurre después para aumentar el control: escalar privilegios, moverte lateralmente, persistir. En HTB el objetivo son las **flags** de usuario y root.

### Metasploit: cuanto menos, mejor (28.05)

> [!warning] DISCIPLINA DE HERRAMIENTAS
> En certificaciones principales (**OSCP, eCPPT**) Metasploit está prohibido o muy limitado. Acostumbrarse a hacer las cosas a mano (Python, herramientas específicas) desde el principio. Excepciones: **eJPT** y escenarios de **pivoting**, donde Metasploit centraliza bien las sesiones.
>
> *Si aprendes con Metasploit, cuando te lo quiten no sabes qué pasa por debajo. Si aprendes sin él, Metasploit se vuelve una comodidad opcional, no un requisito.*

### Metodología de trabajo: orden antes que velocidad (28.05)

- Crear siempre la **estructura de carpetas** del proyecto antes de lanzar herramientas (ver ⑥)
- Guardar salidas de Nmap con `-oN` o `-oA` (normal, grepeable y **XML** — el XML sirve para procesarlo con herramientas propias) para no tener que relanzarlo
- Dividir la terminal con **Tmux** para lanzar los tres Nmaps en paralelo

> [!tip] HACKTRICKS COMO REFERENCIA
> [book.hacktricks.xyz](https://book.hacktricks.xyz) es la referencia de metodología por protocolo: cada servicio tiene su propia página con comandos de enumeración, ataques típicos y recursos.

---

## ② Marco mental: 4 elementos para atacar

Aplicable a **cualquier** vulnerabilidad de servicio (FTP, SMB, SSH, HTTP...).

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ 01 FUENTE   │ → │ 02 PROCESO  │ → │ 03 PRIVILEG.│ → │ 04 DESTINO  │
│ Origen de   │   │ Qué hace    │   │ Con qué     │   │ Qué se      │
│ la info     │   │ el servicio │   │ permisos    │   │ hace con    │
│             │   │             │   │ corre       │   │ el resultado│
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

### Ejemplo: Log4Shell (CVE-2021-44228)

| Elemento | Descripción |
|---------|------------|
| **FUENTE** | Cabecera User-Agent con payload JNDI |
| **PROCESO** | Log4j interpreta y ejecuta la cadena |
| **PRIVILEGIOS** | Si corre como root → RCE como root |
| **DESTINO** | Remote Code Execution en la víctima |

---

## ③ Metodología de Nmap en 3 fases

```
1. Escaneo rápido (-sC -sV) → 2. Todos los puertos (-p-) → 3. Scripts sobre puertos hallados
```

```bash
[[Nmap]] -oN recon/initial.txt <IP>
[[Nmap]] -p- -oN recon/allports.txt <IP>
[[Nmap]] -sC --script default,vuln -sV -Pn -p <PUERTOS> -oA recon/full <IP>
```

| Flag | Significado |
|------|-------------|
| `-sC` | Equivale a `--script=default` — lanza los scripts de la categoría default |
| `--script vuln` | Scripts específicos de CVEs contra los servicios detectados (más intrusivo y lento; en laboratorio/GVM válido, en auditorías reales con cautela) |
| `-Pn` | Omite el host discovery — Nmap escanea aunque no haya respuesta a ping |
| `-oA` | Guarda en los 3 formatos: normal, grepeable y XML |

---

## ④ Servicios con login — 3 vectores

```
┌─────────────────────────────────────┐
│ 1. Fuerza bruta                     │
│ 2. Versión con CVE explotable       │
│ 3. Mala configuración               │
└─────────────────────────────────────┘
```

> [!tip] ORDEN
> Explorar en ese orden. La mala configuración es lo más habitual.

---

## ⑤ Metodología web integrada

| Fase | Acciones |
|------|---------|
| 1. Reconocimiento de red | Net-Discover → identificar hosts |
| 2. Enumeración de puertos | [[Nmap]] -sC -sV → luego -p- |
| 3. Análisis por servicio | FTP: anon / CVE. HTTP: robots.txt + dirsearch |
| 4. Explotación de funcionalidades | Inputs que llegan al servidor |
| 5. Información extraída | Guardar TODO |
| 6. Correlacionar hallazgos | Credenciales de un servicio → otro |
| 7. Descartar rabbit holes | Sin auth no se puede explotar CVE que la requiere |

---

## ⑥ Estructura de carpetas

```bash
mkdir metasploitable2
cd metasploitable2
mkdir recon
mkdir exploits
```

### Tmux para escaneos en paralelo (28.05)

```
Ctrl+B, luego "    → divide horizontalmente
Ctrl+B, luego %    → divide verticalmente
Ctrl+B + flechas   → moverse entre paneles
```

```bash
# Activar el ratón en Tmux
echo "set -g mouse on" >> ~/.tmux.conf
# Recargar dentro de Tmux: Ctrl+B :source-file ~/.tmux.conf
```

---

## ⑦ Conexión con otras áreas

| Área | Cómo encaja |
|------|------------|
| [[Nmap - Escaneo y Enumeración]] | Primer paso de cualquier pentest |
| [[Enumeración Web]] | Subauditoría del servicio web |
| [[Burp Suite - Framework de Auditoría]] | Herramienta principal web |
| [[OWASP Top 10 - CVE CVSS CWE]] | Marco de referencia |
| [[Explotación de Servicios - Linux]] | Servicios específicos |
| [[Explotación de Servicios - Windows]] | Servicios específicos |
| [[Prácticas CTF - HTB y VulnHub]] | Aplicación práctica |

---

## Checklist de repaso

- [ ] ¿Puedo describir las 7 fases del pentest?
- [ ] ¿Distingo explotación de post-explotación?
- [ ] ¿Sé aplicar el marco de 4 elementos a una vulnerabilidad?
- [ ] ¿Entiendo los 3 vectores de ataque a servicios con login?
- [ ] ¿Sé estructurar el trabajo en carpetas?
- [ ] ¿Sé explicar por qué OSCP/eCPPT limitan Metasploit y cuándo sí usarlo?
- [ ] ¿Dominio los flags de Nmap (`-Pn`, `-sC`, vuln, `-oA`) y Tmux en paralelo?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/10.06.2026 HTB Starting Point 2 Repaso.md|10.06.2026 HTB Starting Point 2 Repaso]] — Hack The Box, Netcat / Reverse Shells, SQL Injection
- [[Prácticas CTF - HTB y VulnHub.md|Prácticas CTF - HTB y VulnHub]] — Hack The Box, Post-Explotacion, Windows
- [[../../apuntes Andres/15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows.md|15.06.2026 Repaso Semanal II Archetype Completa, SMB y Primera Máquina Windows]] — Hack The Box, Metodologia Pentest, SQL Injection
- [[../05 - Auditoria Web/Auditoria Web - Práctica con Metasploitable.md|Auditoria Web - Práctica con Metasploitable]] — Nmap, Post-Explotacion, Seguridad
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Hack The Box, Metodologia Pentest, SQL Injection

### 🌐 Cross-Dominio

- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Linux, Seguridad
- [[../../../programacion/Bash/seguridad_bash.md|seguridad_bash]] — Programacion: Desarrollo Web, Linux, Seguridad

> #burpsuite #cli #command_injection #dirsearch #hack_the_box #java #linux #linux_ciber #metasploit #netcat #nmap #pentest #pivoting #post_explotacion #redes #redes_ciber #seguridad #sql #sqli #ssh_tool #vulnhub #web #windows_ciber
