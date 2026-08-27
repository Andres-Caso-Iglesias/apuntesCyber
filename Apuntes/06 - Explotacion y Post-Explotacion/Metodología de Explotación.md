

> [!info] Relacionado con
> [[Nmap - Escaneo y Enumeración]] · [[Enumeración Web]] · [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[Pivoting y Movilidad Lateral]]

---

## ① Las fases del pentest

```
Superficie expuesta → Enumeración → Explotación → Mov. lateral → Escalada → Persistencia → Reporte
```

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
- [ ] ¿Sé aplicar el marco de 4 elementos a una vulnerabilidad?
- [ ] ¿Entiendo los 3 vectores de ataque a servicios con login?
- [ ] ¿Sé estructurar el trabajo en carpetas?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Son ROBOTS.md|Son ROBOTS]— Hack The Box, SSH, VulnHub
- [[Son ROBOTS — RickdiculouslyEasy y Mr. Robot.md|Son ROBOTS — RickdiculouslyEasy y Mr. Robot]— Hack The Box, SSH, VulnHub
- [[../../apuntes Joselu/MODULO3/resumen_master_clase20.md|resumen_master_clase20]— Hack The Box, Redes, SSH
- [[../../apuntes Joselu/MODULO3/resumen_master_clase41.md|resumen_master_clase41]— Hack The Box, Redes, SSH
- [[Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]— Hack The Box, SSH, VulnHub
- [[../../comandos/Metasploit.md|Metasploit]— Pivoting / Movilidad Lateral, Redes, SSH

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #burpsuite #command-injection #dirsearch #hack-the-box #linux #nmap #pentest #pivoting #redes #ssh #vulnhub #windows
