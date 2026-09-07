# Metodologías de Explotación

> [!abstract] Mapa de Contenidos
> Guías concisas de cómo explotar diferentes tipos de máquinas y entornos.

---

## Flujo de Decisiones

> [!tip] ¿Qué tipo de máquina es?

```
¿Es Windows o Linux?
├── Linux → [[Metodología - Explotación Linux]]
└── Windows
 ├── ¿Tiene Active Directory? → [[Metodología - Active Directory]]
 └── Solo máquina local → [[Metodología - Explotación Windows]]

¿Es una aplicación web?
└── Sí → [[Metodologia - Aplicaciones Web]]
```

---

## Metodologías

| #   | Metodología                           | Objetivo            | Fases                       |                                            |
| --- | ------------------------------------- | ------------------- | --------------------------- | ------------------------------------------ |
| 1   | [[Metodología - Explotación Linux]]   | Explotación Linux   | Máquinas Linux standalone   | Recon → Enum → Explot → Escalar            |
| 2   | [[Metodología - Explotación Windows]] | Explotación Windows | Máquinas Windows standalone | Recon → Enum → Explot → Escalar → PSExec   |
| 3   | [[Metodologia - Aplicaciones Web]]    | Aplicaciones Web    | Auditar y explotar webapps  | Recon → Enum → Fuzz → SQLi/XSS/SSRF        |
| 4   | [[Metodología - Active Directory]]    | Active Directory    | Entornos AD corporativos    | Enum → Kerberoast → DCSync → Golden Ticket |

---

## Flujo Genérico de Pentest

```
1. Reconocimiento
 ├── Descubrir hosts
 ├── Identificar servicios
 └── Buscar tecnologías

2. Enumeración
 ├── Directorios y archivos
 ├── Usuarios y contraseñas
 ├── Vulnerabilidades conocidas
 └── Configuraciones débiles

3. Explotación
 ├── Obtener acceso (shell/credenciales)
 └── Confirmar vulnerabilidad

4. Escalada de Privilegios
 ├── Local (root/SYSTEM)
 └── Lateral (otros usuarios)

5. Post-Explotación
 ├── Extraer datos
 ├── Mantener acceso
 └── Reportar hallazgos
```

---

## Referencia Rápida por Tipo de Máquina

| Tipo | Vectores Comunes | Herramientas Clave |
|------|------------------|-------------------|
| **Linux Web Server** | Web app + SSH | feroxbuster, sqlmap, hydra |
| **Linux File Server** | SMB/FTP + SUID | enum4linux, linpeas |
| **Windows Web Server** | IIS/ASPX + SMB | feroxbuster, smbexec, winpeas |
| **Windows DC** | AD + Kerberos | bloodhound, impacket, mimikatz |
| **WordPress** | Plugins + WPScan | wpscan, sqlmap |
| **Máquina CTF** | Todo lo anterior | Depends on services |

---

## Checklist General

- [ ] Host descubierto
- [ ] Servicios identificados
- [ ] Tecnologías determinadas
- [ ] Metodología aplicada según tipo
- [ ] Acceso obtenido
- [ ] Escalada completada
- [ ] Datos extraídos
- [ ] Reporte escrito

---

#checklist
- [ ] Metodologías revisadas
- [ ] Herramientas instaladas
- [ ] Wordlists preparadas
- [ ] Entorno de testing configurado

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Repaso de Enumeración Web.md|Repaso de Enumeración Web]]— SSH, SSRF, XSS
- [[../../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]]— Hydra, SSH, XSS
- [[../../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]]— Hydra, SSH, XSS
- [[../05 - Auditoria Web/Repaso de Enumeración Web.md|Repaso de Enumeración Web]]— Hydra, SSRF, XSS
- [[../06 - Explotacion y Post-Explotacion/Prácticas CTF - HTB y VulnHub.md|Prácticas CTF - HTB y VulnHub]]— Hydra, SMB / Impacket, SSH
- [[../../apuntes Joselu/MODULO3/resumen_master_clase39.md|resumen_master_clase39]]— SSH, SSRF, XSS

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SQLMap|SQLMap]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #feroxbuster #hydra #linux #pentest #smb-impacket #sqli #sqlmap #ssh #ssrf #windows #wordpress #wpscan #xss
