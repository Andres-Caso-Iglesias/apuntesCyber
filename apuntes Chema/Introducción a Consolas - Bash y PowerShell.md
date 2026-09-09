# ① Terminal vs GUI — ¿Por qué la línea de comandos?

La terminal (CLI) es más potente, reproducible y automatizable que la interfaz gráfica (GUI). En auditorías, la mayoría de herramientas son de consola.

| | |
|---|---|
|**Terminal (CLI)**<br><br>*     Automatizable con scripts<br><br>*     Herramientas de hacking son CLI<br><br>*     Menor consumo de recursos<br><br>*     Control total del sistema<br><br>*     Más rápida para operaciones repetitivas|**GUI (Interfaz Gráfica)**<br><br>*     Más intuitiva para principiantes<br><br>*     Mejor para edición visual<br><br>*     No automatizable directamente<br><br>*     Mayor consumo de recursos<br><br>*     Depende del entorno gráfico|

# ② Configuración del entorno: Virtualización

El entorno de trabajo estándar en el máster es Kali Linux sobre VirtualBox o VMware. Kali incluye todas las herramientas preinstaladas.

| |
|---|
|# Opciones de virtualización:<br><br>VirtualBox   → Gratuito. Descargar imagen Kali (.ova) e importar.<br><br>VMware       → Más rendimiento. Preferido por el instructor.<br><br>WSL2         → Bash en Windows (no recomendado para el máster).<br><br>Nativo       → Instalación directa en hardware (máximo rendimiento).<br><br># Recursos recomendados por VM:<br><br>RAM: mínimo 2 GB (recomendado 4 GB)<br><br>CPU: 2 cores mínimo<br><br>Disco: 30 GB mínimo<br><br># Red en VMs:<br><br>NAT         → VM con internet, sin acceso desde el exterior<br><br>Host-Only   → VM aislada, solo comunica con host<br><br>Bridged     → VM en la misma red que el host (como un equipo más)|

| | |
|---|---|
|**💡 RECOMENDACIÓN**|Para laboratorios con varias VMs (atacante + víctima): usar red Host-Only o una red NAT interna para que estén aisladas de Internet.|

# ③ Anatomía de la terminal Bash

| |
|---|
|kali@kali:~$<br><br># └─ usuario@hostname:directorio_actual$<br><br># ~ = home del usuario (/home/kali)<br><br># $ = usuario normal  (# = root)<br><br># Atajos de teclado útiles:<br><br>Ctrl+C      → cancelar proceso actual<br><br>Ctrl+Z      → suspender proceso (bg para reanudar en background)<br><br>Ctrl+L      → limpiar pantalla (equivale a 'clear')<br><br>Ctrl+A      → ir al inicio de la línea<br><br>Ctrl+E      → ir al final de la línea<br><br>Ctrl+R      → búsqueda en historial<br><br>Tab         → autocompletar comando/ruta<br><br>Tab Tab     → mostrar todas las opciones posibles<br><br>↑ / ↓       → navegar por el historial de comandos|

# ④ Comandos esenciales de Bash

| |
|---|
|# Navegación:<br><br>pwd                  # directorio actual<br><br>ls -la               # listar con detalles y ocultos<br><br>cd /ruta             # cambiar directorio<br><br>cd ..                # subir al padre<br><br># Ficheros:<br><br>cat fichero.txt      # ver contenido<br><br>nano fichero.txt     # editor simple en terminal<br><br>cp src dst           # copiar<br><br>mv src dst           # mover/renombrar<br><br>rm fichero           # borrar<br><br>mkdir -p dir/subdir  # crear árbol de directorios<br><br># Información del sistema:<br><br>whoami               # usuario actual<br><br>id                   # UID, GID y grupos<br><br>uname -a             # información del kernel<br><br>hostname             # nombre del equipo<br><br>ifconfig / ip a      # interfaces de red<br><br>df -h                # espacio en disco<br><br>free -h              # memoria RAM|

# ⑤ Rutas: absoluta vs relativa

El concepto de **path** (ruta) es uno de los más importantes del máster. Aparece constantemente en escalada de privilegios.

| | |
|---|---|
|**Ruta absoluta**<br><br>Empieza siempre por /<br><br>/home/kali/documentos/fichero.txt<br><br>Funciona desde cualquier directorio|**Ruta relativa**<br><br>Parte desde el directorio actual<br><br>documentos/fichero.txt<br><br>Depende de dónde estés ahora|

| | |
|---|---|
|**🔐 ESCALADA**|En escalada de privilegios, la diferencia entre ruta absoluta y relativa en scripts SUID puede ser la vulnerabilidad. Si un script llama 'python' (relativo) podemos poner nuestro propio 'python' en el PATH.|

# ⑥ Introducción a PowerShell

PowerShell es la shell de Windows, también disponible en Linux/macOS. En pentesting Windows es fundamental para post-explotación.

| |
|---|
|# Comparativa rápida Bash → PowerShell:<br><br>ls / dir        → Get-ChildItem (gci, ls, dir — todos funcionan)<br><br>cd              → Set-Location (cd funciona también)<br><br>cat             → Get-Content<br><br>echo            → Write-Host / Write-Output<br><br>rm              → Remove-Item<br><br>cp              → Copy-Item<br><br>mv              → Move-Item<br><br>grep            → Select-String<br><br>find            → Get-ChildItem -Recurse<br><br># Obtener ayuda:<br><br>Get-Help Get-ChildItem    # ayuda de un comando<br><br>Get-Help Get-ChildItem -Examples<br><br># Información del sistema:<br><br>whoami<br><br>Get-LocalUser             # listar usuarios locales<br><br>Get-Process               # procesos (equivale a ps aux)<br><br>ipconfig /all             # interfaces de red|

| | |
|---|---|
|**💡 PENTEST**|PowerShell permite ejecutar código en memoria, descargar payloads, y moverse lateralmente. Herramientas como PowerView o PowerSploit lo aprovechan. Por eso muchas empresas restringen su ejecución.|

# ⑦ Gestión de paquetes en Kali Linux

| |
|---|
|# APT — gestor de paquetes de Debian/Kali<br><br>sudo apt update                      # actualizar lista de paquetes<br><br>sudo apt upgrade -y                  # actualizar paquetes instalados<br><br>sudo apt install nombre-paquete      # instalar herramienta<br><br>sudo apt remove nombre-paquete       # desinstalar<br><br>sudo apt search herramienta          # buscar paquete<br><br>apt-cache show nombre-paquete        # info del paquete<br><br># También disponible en Kali:<br><br>pip install herramienta              # paquetes Python<br><br>gem install herramienta              # paquetes Ruby<br><br>go install ...                       # paquetes Go|



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes/comandos/Metasploit.md|Metasploit]] — Linux, Post-Explotación, Windows
- [[../Apuntes/02 - Sistemas Operativos/Consolas - Bash y PowerShell.md|Consolas - Bash y PowerShell]] — Kali Linux, Linux, Windows
- [[../Apuntes/02 - Sistemas Operativos/Linux - Fundamentos.md|Linux - Fundamentos]] — Linux, Redes, Windows
- [[../Apuntes/comandos/John_Hashcat.md|John_Hashcat]] — Linux, Redes, Windows
- [[Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]] — Kali Linux, Linux, Windows
- [[../Apuntes/comandos/Hydra.md|Hydra]] — Linux, Redes, Windows

> #escalada-privilegios #kali #linux #pentest #post-explotacion #redes #windows
