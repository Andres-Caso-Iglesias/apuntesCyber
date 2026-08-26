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

| # | Metodología | Objetivo | Fases |
|---|-------------|----------|-------|
| 1 | [[Metodología - Explotación Linux|Explotación Linux]] | Máquinas Linux standalone | Recon → Enum → Explot → Escalar |
| 2 | [[Metodología - Explotación Windows|Explotación Windows]] | Máquinas Windows standalone | Recon → Enum → Explot → Escalar → PSExec |
| 3 | [[Metodologia - Aplicaciones Web|Aplicaciones Web]] | Auditar y explotar webapps | Recon → Enum → Fuzz → SQLi/XSS/SSRF |
| 4 | [[Metodología - Active Directory|Active Directory]] | Entornos AD corporativos | Enum → Kerberoast → DCSync → Golden Ticket |

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
