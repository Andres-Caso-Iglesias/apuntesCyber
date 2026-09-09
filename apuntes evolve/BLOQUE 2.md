> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 02 — Sistemas y redes
> **Contenido:** Linux, Windows, Kali Linux, consolas de comandos (Bash/PowerShell/CMD) y fundamentos de redes, con comandos reales

> [!tip] Cómo leer estos apuntes
> Este bloque cubre los fundamentos de redes (protocolos, topologías), la diferencia entre Windows y Linux en seguridad, instalación de Kali Linux, las tres consolas de comandos (Bash, PowerShell, CMD) y una introducción al scripting.

---

## ① Fundamentos de redes

Una red conecta **dispositivos finales** a través de dispositivos intermedios (switches para redes locales, routers para conectar redes distintas) y medios de transmisión (cable Ethernet o inalámbrico).

### Protocolos clave y su función

| Protocolo | Función |
|-----------|---------|
| **IP** (Internet Protocol) | Dirección única que identifica cada dispositivo |
| **TCP** | Garantiza que los datos llegan completos y en orden (correo, descargas, HTTP) |
| **UDP** | Prioriza velocidad sobre fiabilidad (streaming, videollamadas, DNS) |
| **HTTP/HTTPS** | Navegación web; HTTPS cifra el tráfico con TLS |

### Topologías de red

| Topología | Descripción | Ventaja / Riesgo |
|-----------|-------------|------------------|
| **Estrella** | Todo pasa por un switch central | Si falla el switch, cae toda la red |
| **Bus** | Cable compartido, simple | Un fallo del cable tumba la conexión |
| **Malla** | Todos conectados con todos | Más robusta pero más cara |

### Comandos básicos de diagnóstico

```bash
# Comprobar conectividad
ping google.com

# Ver configuración de red en Linux
ip a
ip route

# Ver configuración de red en Windows / PowerShell
Get-NetIPConfiguration
ipconfig /all

# Cambiar disposición de teclado en Kali recién instalado
setxkbmap es
```

---

## ② Windows vs Linux para ciberseguridad

### Windows

- Organiza la seguridad mediante **registros de memoria** (datos temporales, incluidas contraseñas mientras se usa el sistema).
- Jerarquía de usuarios: usuario normal → administrador local → administrador de dominio.
- Técnicas como el **buffer overflow** explotan estos registros para escalar privilegios.

### Linux

- Se organiza en torno a **permisos de archivo**.
- La salida de `ls -l` muestra algo como `rwxr-xr--`:

```
rwxr-xr--
│││└┴┴──── otros usuarios: r-- (solo lectura)
│└┴─────── grupo: r-x (lectura y ejecución)
└──────── propietario: rwx (lectura, escritura y ejecución)
```

> [!warning] Importante
> Si un archivo tiene permisos mal configurados, alguien podría ejecutarlo como administrador (root), abriendo la puerta a una **escalada de privilegios** (desarrollado con comandos completos en el Bloque 6).

---

## ③ Kali Linux: historia, instalación y estructura

### Evolución

```
Whoppix (2004, CD en vivo)
 → BackTrack (2006, basado en Ubuntu)
 → Kali Linux (2013, basado en Debian)
```

- Actualizaciones automáticas y más de **600 herramientas preinstaladas**.

### Instalación práctica con VirtualBox

1. Descargar e instalar VirtualBox (gratuito): `virtualbox.org`
2. Descargar la máquina virtual preconfigurada de Kali (usuario/contraseña por defecto: `kali/kali`): `kali.org/get-kali/`
3. En VirtualBox: "Nueva" → nombre "Kali Linux" → Tipo: Linux → Versión: Debian (64-bit).
4. Asignar recursos: RAM 2-4 GB (si el equipo tiene 8 GB), 2 núcleos de CPU (si tiene al menos 4).
5. Adjuntar el archivo descargado como disco óptico virtual o directamente la VM preconfigurada.
6. Configurar red en modo **NAT** (acceso a Internet) para uso general, o "Solo anfitrión" para laboratorios aislados.

```bash
# Verificación tras el primer arranque
ping google.com # verificar conexión a Internet
setxkbmap es # cambiar teclado a español
```

### Herramientas agrupadas por fase de auditoría

| Fase | Herramientas |
|------|-------------|
| **Information Gathering** | Nmap, SpiderFoot, Maltego, The Harvester |
| **Análisis de vulnerabilidades** | OpenVAS, Nessus |
| **Explotación** | Metasploit, SQLMap, Hydra |
| **Ingeniería social** | Social-Engineer Toolkit (SET) |
| **Forense** | Autopsy, Binwalk |

---

## ④ Consolas de comandos: Bash, PowerShell y CMD

La estructura de un comando sigue el patrón: `comando + opciones + argumentos`.

Ejemplo: `ls -l /home/usuario` significa "ejecuta ls, con la opción -l (modo largo), sobre la carpeta /home/usuario".

### Bash (Linux) — comandos esenciales

```bash
pwd # muestra el directorio actual
cd /home/usuario/Documentos # cambiar de directorio
cd .. # subir un nivel
ls -al # listar todo, incluidos ocultos
mkdir proyecto # crear carpeta
touch archivo.txt # crear archivo vacío
echo "Hola mundo" > archivo.txt # crear archivo con contenido (sobreescribe)
echo "Mas texto" >> archivo.txt # añadir contenido sin sobreescribir
cat archivo.txt # ver contenido
rm archivo.txt # borrar archivo
rm -r proyecto/ # borrar carpeta y su contenido
rm -rf proyecto/ # forzar sin confirmación (¡cuidado!)
```

### PowerShell (Windows) — comandos esenciales

```powershell
Get-Location # equivalente a pwd
Set-Location C:\Usuarios\Nombre\Documentos # cambiar de directorio
Get-ChildItem -Force # listar (equivalente a ls -al)
New-Item -ItemType Directory -Name "proyectos"
New-Item -ItemType File -Path "proyectos\readme.txt"
Get-Content proyectos\readme.txt # ver contenido
Remove-Item readme.txt
Remove-Item -Recurse -Force proyectos\
Clear-Host # limpiar pantalla
Get-NetIPConfiguration # ver red
```

### CMD (Windows clásico) — comandos esenciales

```cmd
cd "Mi Carpeta" # nombres con espacios van entre comillas
dir # listar directorio (equivalente a ls)
mkdir nombre_carpeta
copy origen destino
move origen destino
cls # limpiar pantalla (equivalente a clear)
```

> [!note] Detalle importante
> Linux distingue **mayúsculas/minúsculas** (case sensitive); Windows no. Y en cualquier consola: usa **Tab** para autocompletar y la **flecha arriba** para repetir comandos anteriores.

---

## ⑤ Introducción al scripting

El scripting automatiza tareas repetitivas mediante bucles, condicionales y variables.

### Script Bash sencillo de verificación de conectividad

```bash
#!/bin/bash
for ip in 192.168.1.1 192.168.1.2 192.168.1.3; do
 if ping -c 1 "$ip" &> /dev/null; then
 echo "$ip está activo"
 else
 echo "$ip no responde"
 fi
done
```

> [!important] Relevancia
> Dominar esto es la base para crear herramientas propias de auditoría, y más adelante para entender cómo se automatizan tanto ataques como defensas (ver SOAR en el Bloque 11).



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/MODULO1/resumen_master_clase3.md|resumen_master_clase3]] — Linux, Metasploit, Windows
- [[../transcripciones/Junio/09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot.md|09.06.2026 Escalada de Privilegios y Hacking Web Máquina Ridiculously Easy II y Mr. Robot]] — Linux, Nmap, Windows
- [[../apuntes Andres/11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad.md|11.06.2026 HTB Starting Point Tier 2 Appointment Completa y SQL Injection en Profundidad]] — Linux, Nmap, Windows
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Reverse Shells y Post-Explotación]] — Linux, Metasploit, Windows
- [[../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Linux, Metasploit, Nmap
- [[../apuntes Joselu/MODULO1/resumen_master_clase5.md|resumen_master_clase5]] — Linux, Metasploit, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #escalada-privilegios #esteganografia #forense #hydra #kali #linux #metasploit #metasploitable #netcat #nmap #post-explotacion #redes #reverse-shell #sqli #sqlmap #windows
