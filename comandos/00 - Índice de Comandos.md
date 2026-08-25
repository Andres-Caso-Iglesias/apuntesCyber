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
│ ├── Descubrir hosts → [[Nmap#Descubrimiento de Hosts|Nmap -sn]]
│ ├── Escanear puertos → [[Nmap#Escaneo de Puertos|Nmap -p-]]
│ ├── Detectar servicios → [[Nmap#Detección de Servicios y OS|Nmap -sV]]
│ └── Enumerar SMB → [[SMB_Impacket#Enumeración SMB|smbclient -L]]
│
├── 🔓 Explotar vulnerabilidades
│ ├── Inyección SQL → [[SQLMap#Detección Básica|sqlmap -u]]
│ ├── Explotar servicios → [[Metasploit#Exploits — Selección|msfconsole - use]]
│ ├── WordPress → [[WPScan#Escaneo Básico|wpscan --url]]
│ ├── Web testing → [[BurpSuite#Proxy|Burp Suite]]
│ └── EternalBlue → [[Nmap#Scripts NSE — Vulnerabilidades|nmap --script smb-vuln*]]
│
├── 🔑 Fuerza bruta
│ ├── Credenciales → [[Hydra#Básico|hydra -l -P]]
│ ├── Hashes → [[John_Hashcat#John the Ripper — Básico|john hashfile]]
│ └── Hashes GPU → [[John_Hashcat#Hashcat — Básico|hashcat -m]]
│
├── 🌐 Web fuzzing
│ ├── Directorios → [[FFUF#Básico|ffuf -u -w]]
│ ├── Recursivo → [[Feroxbuster#Escaneo Básico|feroxbuster -u]]
│ ├── DNS/VHOST → [[GoBuster#Modo DNS (Subdominios)|gobuster dns/vhost]]
│ ├── Python → [[DirSearch#Escaneo Básico|dirsearch -u]]
│ └── Parámetros → [[FFUF#Fuzzing de Parámetros|ffuf ?FUZZ=]]
│
├── 🖥️ Post-explotación
│ ├── Meterpreter → [[Metasploit#Meterpreter — Comandos Básicos|meterpreter - sysinfo]]
│ ├── Pass-the-Hash → [[SMB_Impacket#Pass-the-Hash|impacket-psexec -hashes]]
│ ├── Extracción hashes → [[SMB_Impacket#Impacket — SecretsDump|secretsdump]]
│ └── Escalada → [[Metasploit#Post-Explotación|run post/multi/recon/...]]
│
├── 🔐 Acceso remoto y tunnels
│ ├── Conexión → [[SSH#Conexión Básica|ssh user@host]]
│ ├── Claves → [[SSH#Claves SSH|ssh-keygen -t ed25519]]
│ ├── Transferencia → [[SSH#Transferencia de Archivos|scp / sftp]]
│ └── Tunnels → [[SSH#Tunel SSH (Port Forwarding)|ssh -L / -R / -D]]
│
└── 🛠️ Sistema y utilidades
 ├── Linux → [[Linux#Navegación de Directorios|ls, cd, find, grep...]]
 ├── Windows → [[Windows#CMD — Navegación|dir, cd, ipconfig...]]
 ├── Terminal → [[Tmux#Sesiones|tmux new -s]]
 ├── Google Dorks → [[Google_Dorks#Operadores de Búsqueda|site:, inurl:, intitle:]]
 └── Testing rápido → [[Telnet#Conexión Básica|telnet host puerto]]
```

---

## Referencia por Herramienta

| Herramienta | Uso principal | Cuándo usarla |
|-------------|---------------|---------------|
| [[Linux]] | Comandos del sistema | Trabajando en Linux/Kali |
| [[Windows]] | CMD y PowerShell | En máquinas Windows |
| [[Google_Dorks]] | Búsqueda avanzada | Fase de reconocimiento |
| [[Nmap]] | Escaneo de red | Primer paso en cualquier pentest |
| [[Metasploit]] | Explotación | Explotar vulnerabilidades encontradas |
| [[BurpSuite]] | Testing web | Proxy, scanner y fuzzing web |
| [[Telnet]] | Testing manual | Probar puertos y protocolos |
| [[Hydra]] | Fuerza bruta | Romper contraseñas de servicios |
| [[FFUF]] | Web fuzzing | Encontrar directorios/parámetros ocultos |
| [[Tmux]] | Multiplexor | Organizar terminal en paneles/ventanas |
| [[SQLMap]] | Inyección SQL | Explotar formularios web |
| [[WPScan]] | Auditoría WordPress | Analizar sitios WordPress |
| [[SMB_Impacket]] | SMB y Windows | Enumerar/explotar servicios Windows |
| [[John_Hashcat]] | Cracking hashes | Romper contraseñas hasheadas |
| [[Feroxbuster]] | Fuzzing recursivo | Encontrar directorios profundos |
| [[GoBuster]] | DNS/VHOST brute-force | Enumerar subdominios y virtual hosts |
| [[SSH]] | Acceso remoto y túneles | Conexión, transferencia, tunnels, pivoting || [[DirSearch]] | Fuzzing directorios | Alternativa Python a feroxbuster |

---

## Flujo de Pentest

> [!note] Proceso típico
> 1. **Reconocimiento** → [[Google_Dorks]], [[Nmap#Descubrimiento de Hosts|Nmap]]
> 2. **Enumeración** → [[Nmap#Scripts NSE — Información|Nmap -sC]], [[WPScan]], [[SMB_Impacket#Enumeración SMB|enum4linux]]
> 3. **Explotación** → [[Metasploit]], [[SQLMap]], [[Hydra]]
> 4. **Post-explotación** → [[Metasploit#Meterpreter — Comandos Básicos|Meterpreter]], [[SMB_Impacket#Impacket — SecretsDump|SecretsDump]]
> 5. **Cracking** → [[John_Hashcat]]
> 6. **Documentación** → [[Tmux#Copy Mode|Tmux copy mode]]

---

#checklist
- [ ] Herramienta según objetivo identificada
- [ ] Flujo de pentest comprendido
- [ ] Wiki-links funcionando

