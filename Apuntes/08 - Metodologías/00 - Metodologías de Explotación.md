

> [!abstract] Mapa de Contenidos
> GuÃ­as concisas de cÃ³mo explotar diferentes tipos de mÃ¡quinas y entornos.

> â†’
---

## Flujo de Decisiones

> [!tip] Â¿QuÃ© tipo de mÃ¡quina es?

```
Â¿Es Windows o Linux?
â”œâ”€â”€ Linux â†’ [[MetodologÃ­a - ExplotaciÃ³n Linux]]
â””â”€â”€ Windows
 â”œâ”€â”€ Â¿Tiene Active Directory? â†’ [[MetodologÃ­a - Active Directory]]
 â””â”€â”€ Solo mÃ¡quina local â†’ [[MetodologÃ­a - ExplotaciÃ³n Windows]]

Â¿Es una aplicaciÃ³n web?
â””â”€â”€ SÃ­ â†’ [[Metodologia - Aplicaciones Web]]
```

---

## MetodologÃ­as

| # | MetodologÃ­a | Objetivo | Fases |
|---|-------------|----------|-------|
| 1 | [[MetodologÃ­a - ExplotaciÃ³n Linux|ExplotaciÃ³n Linux]] | MÃ¡quinas Linux standalone | Recon â†’ Enum â†’ Explot â†’ Escalar |
| 2 | [[MetodologÃ­a - ExplotaciÃ³n Windows|ExplotaciÃ³n Windows]] | MÃ¡quinas Windows standalone | Recon â†’ Enum â†’ Explot â†’ Escalar â†’ PSExec |
| 3 | [[Metodologia - Aplicaciones Web|Aplicaciones Web]] | Auditar y explotar webapps | Recon â†’ Enum â†’ Fuzz â†’ SQLi/XSS/SSRF |
| 4 | [[MetodologÃ­a - Active Directory|Active Directory]] | Entornos AD corporativos | Enum â†’ Kerberoast â†’ DCSync â†’ Golden Ticket |

â†’

---

## Flujo GenÃ©rico de Pentest

```
1. Reconocimiento
 â”œâ”€â”€ Descubrir hosts
 â”œâ”€â”€ Identificar servicios
 â””â”€â”€ Buscar tecnologÃ­as

2. EnumeraciÃ³n
 â”œâ”€â”€ Directorios y archivos
 â”œâ”€â”€ Usuarios y contraseÃ±as
 â”œâ”€â”€ Vulnerabilidades conocidas
 â””â”€â”€ Configuraciones dÃ©biles

3. ExplotaciÃ³n
 â”œâ”€â”€ Obtener acceso (shell/credenciales)
 â””â”€â”€ Confirmar vulnerabilidad

4. Escalada de Privilegios
 â”œâ”€â”€ Local (root/SYSTEM)
 â””â”€â”€ Lateral (otros usuarios)

5. Post-ExplotaciÃ³n
 â”œâ”€â”€ Extraer datos
 â”œâ”€â”€ Mantener acceso
 â””â”€â”€ Reportar hallazgos
```

---

## Referencia RÃ¡pida por Tipo de MÃ¡quina

| Tipo | Vectores Comunes | Herramientas Clave |
|------|------------------|-------------------|
| **Linux Web Server** | Web app + SSH | feroxbuster, sqlmap, hydra |
| **Linux File Server** | SMB/FTP + SUID | enum4linux, linpeas |
â†’
| **Windows Web Server** | IIS/ASPX + SMB | feroxbuster, smbexec, winpeas |
| **Windows DC** | AD + Kerberos | bloodhound, impacket, mimikatz |
| **WordPress** | Plugins + WPScan | wpscan, sqlmap |
| **MÃ¡quina CTF** | Todo lo anterior | Depends on services |

â†’

---

## Checklist General

- [ ] Host descubierto
- [ ] Servicios identificados
- [ ] TecnologÃ­as determinadas
- [ ] MetodologÃ­a aplicada segÃºn tipo
- [ ] Acceso obtenido
- [ ] Escalada completada
- [ ] Datos extraÃ­dos
- [ ] Reporte escrito

---

#checklist
- [ ] MetodologÃ­as revisadas
- [ ] Herramientas instaladas
- [ ] Wordlists preparadas
- [ ] Entorno de testing configurado

â†’

