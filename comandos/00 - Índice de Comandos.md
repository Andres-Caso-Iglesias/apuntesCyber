# Índice de Comandos — Cheat Sheets

> [!info] Propósito
> Referencia rápida de todas las herramientas disponibles. Elegí la herramienta según lo que necesités hacer.
## ¿Qué herramienta uso?

> [!tip] Flujo de decisión
> Seguí la cadena según tu objetivo.

```

¿Qué necesés hacer?
│
├── 🔍 Explorar red y hosts
│ ├── Descubrir hosts│ ├── Escanear puertos│ ├── Detectar servicios│ └── Enumerar SMB│
├── 🔓 Explotar vulnerabilidades
│ ├── Inyección SQL│ ├── Explotar servicios│ ├── WordPress│ ├── Web testing│ └── EternalBlue│
├── 🔑 Fuerza bruta
│ ├── Credenciales│ ├── Hashes│ └── Hashes GPU│
├── 🌐 Web fuzzing
│ ├── Directorios│ ├── Recursivo│ ├── DNS/VHOST│ ├── Python│ └── Parámetros│
├── 🖥️ Post-explotación
│ ├── Meterpreter│ ├── Pass-the-Hash│ ├── Extracción hashes│ └── Escalada│
├── 🔐 Acceso remoto y tunnels
│ ├── Conexión│ ├── Claves│ ├── Transferencia│ └── Tunnels│
└── 🛠️ Sistema y utilidades
 ├── Linux├── Windows├── Terminal├── Google Dorks└── Testing rápido```
```

---

## Referencia por Herramienta

| Herramienta | Uso principal | Cuándo usarla |
|-------------|---------------|---------------|
|| Comandos del sistema | Trabajando en Linux/Kali |
|| CMD y PowerShell | En máquinas Windows |
|| Búsqueda avanzada | Fase de reconocimiento |
|| Escaneo de red | Primer paso en cualquier pentest |
|| Explotación | Explotar vulnerabilidades encontradas |
|| Testing web | Proxy, scanner y fuzzing web |
|| Testing manual | Probar puertos y protocolos |
|| Fuerza bruta | Romper contraseñas de servicios |
|| Web fuzzing | Encontrar directorios/parámetros ocultos |
|| Multiplexor | Organizar terminal en paneles/ventanas |
|| Inyección SQL | Explotar formularios web |
|| Auditoría WordPress | Analizar sitios WordPress |
|| SMB y Windows | Enumerar/explotar servicios Windows |
|| Cracking hashes | Romper contraseñas hasheadas |
|| Fuzzing recursivo | Encontrar directorios profundos |
|| DNS/VHOST brute-force | Enumerar subdominios y virtual hosts |
|| Acceso remoto y túneles | Conexión, transferencia, tunnels, pivoting ||| Fuzzing directorios | Alternativa Python a feroxbuster |

---

## Flujo de Pentest

> [!note] Proceso típico
> 1. **Reconocimiento**,> 2. **Enumeración**,,> 3. **Explotación**,,> 4. **Post-explotación**,> 5. **Cracking**> 6. **Documentación**---

#checklist
- [ ] Herramienta según objetivo identificada
- [ ] Flujo de pentest comprendido
- [ ] Wiki-links funcionando









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Chema/Maquinas/Cierre de Vaccine + Máquina Oopsie.md|Cierre de Vaccine + Máquina Oopsie]] — FFUF, GoBuster, Kali Linux
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables III - NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III - NFS, Tomcat y MySQL]] — Desarrollo Web, Kali Linux, SQL Injection
- [[../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]] — Desarrollo Web, Metodologia Pentest, SQL Injection
- [[../apuntes Joselu/MODULO3/resumen_master_clase44.md|resumen_master_clase44]] — GoBuster, SQL Injection, Testing
- [[../apuntes Chema/Maquinas/Auditoría de CMS - WordPress (máquina Academy).md|Auditoría de CMS - WordPress (máquina Academy)]] — FFUF, GoBuster, Kali Linux

### 🌐 Cross-Dominio

- [[../../programacion/Go/seguridad_go.md|seguridad_go]] — Programacion: Desarrollo Web, Linux, Testing
- [[../../programacion/Ciberseguridad/wordpress_security.md|wordpress_security]] — Programacion: Desarrollo Web, Linux, Testing

> #cli #feroxbuster #ffuf #go #gobuster #hydra #john_hashcat #kali #linux #linux_ciber #metasploitable #pentest #pivoting #post_explotacion #python #redes #redes_ciber #sql #sqli #testing #web #windows_ciber #wordpress
