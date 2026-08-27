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

- [[../Apuntes/05 - Auditoria Web/Auditoria Web — Práctica con Metasploitable.md|Auditoria Web — Práctica con Metasploitable]— GoBuster, Kali Linux, Post-Explotación
- [[../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 — Rockstar.md|Fuzzing de parámetros con x8 — Rockstar]— GoBuster, Hydra, Kali Linux
- [[../apuntes Joselu/MODULO3/resumen_master_clase27.md|resumen_master_clase27]— GoBuster, Hydra, Kali Linux
- [[../apuntes Chema/Anonimato, Ingeniería Social y Enumeración Web.md|Anonimato, Ingeniería Social y Enumeración Web]— GoBuster, Kali Linux, Redes
- [[../apuntes Chema/Auditoria web.md|Auditoria web]— GoBuster, Kali Linux, Redes
- [[../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]— GoBuster, Hydra, Kali Linux

### 🛠️ Herramientas

- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #feroxbuster #ffuf #gobuster #hydra #john #kali #linux #pentest #pivoting #post-explotacion #redes #sqli #windows #wordpress
