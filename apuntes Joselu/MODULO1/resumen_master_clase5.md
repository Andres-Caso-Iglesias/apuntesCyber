> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 5**
> **Módulo:** MODULO1
> **Tema:** Clase 5
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 5. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Introducción y contexto

Esta sesión, impartida por el mismo instructor de las clases 3 y 5, tiene dos bloques principales: una introducción a Windows como sistema operativo corporativo y una sesión práctica de comandos CMD/PowerShell correlacionados con lo ya visto en Bash/Linux.

> [!important] **Dato clave:** más del **70-80 % de todas las empresas** usan Windows, y de esas, el **95-97 % utilizan Active Directory** (Directorio Activo) para gestionar sus infraestructuras. El entendimiento de Windows es, por tanto, imprescindible para cualquier pentester.

**Reflexión inicial sobre auditorías:** los clientes raramente contratan ciberseguridad por iniciativa propia. El verdadero motor del mercado es la normativa: ISO 27001, ENS, NIS 2, DORA, PCI DSS... Las auditorías técnicas son el servicio que se vende ligado al cumplimiento normativo, no un capricho. La normativa "da de comer" al sector.

## 2. Linux vs. Windows: diferencias fundamentales para el hacker

### Case sensitivity

- **Linux es case sensitive:** ls, Ls, LS son tres cosas distintas. Un error de mayúscula hace que el comando no funcione o no encuentre el fichero.
- **Windows es case insensitive:** acepta mayúsculas y minúsculas indistintamente.

**Truco para detectar el SO de un servidor web:** si cambiando una letra de la URL a mayúscula el servidor sigue respondiendo, es probablemente Windows. Si devuelve error, es Linux. Esto es útil en la fase de enumeración.

### Sistema de archivos y discos

- **Linux:** todo cuelga de una única raíz /. No hay letras de unidad.
- **Windows:** cada unidad tiene su letra (C:, D:, E:...). El sistema operativo vive habitualmente en C:\\. Puede haber múltiples discos con letras distintas.

### Separador de ruta

- **Linux:** barra derecha / (alt gr + 1 en teclado español).
- **Windows:** barra invertida \\ (alt gr + mayúscula + ç, o alt gr + tecla según distribución). **Regla mnemotécnica:** la primera barra de la W de Windows es \\.

⚠️ Error muy común en exploits: usar / (estilo Linux) cuando se está atacando un Windows. Dependiendo de la versión del servidor, puede funcionar o no. Siempre usar \\ en rutas Windows para garantizar compatibilidad.

### Estructura de carpetas de Windows vs. Linux

| Windows | Linux equivalente | Contenido |
|---|---|---|
| C:\\Windows\\System32 | /bin, /sbin, /lib | Binarios y ejecutables del sistema (cmd.exe, powershell.exe, notepad.exe, drivers, DLLs...) C:\\Program Files | /usr/local | Aplicaciones de 64 bits instaladas C:\\Program Files (x86) | --- | Aplicaciones de 32 bits instaladas C:\\Users | /home | Directorios de usuario (equivalente a \~) C:\\Windows\\Temp | /tmp | Ficheros temporales |
|---|---|---|---|---|---|---|---|---|---|---|

**Advertencia:** cuando se hackea un servidor en producción con idioma español, la carpeta se llama Archivos de programa, no Program Files. Lanzar un exploit con la ruta en inglés en un sistema en español puede hacer que falle. Tenerlo siempre en cuenta.

## 3. Terminales de Windows: CMD, PowerShell y Terminal

Windows tiene tres formas de abrir una terminal:

| Terminal | Descripción |
|---|---|
| **CMD** (símbolo del sistema) | Terminal clásica de Windows. Solo acepta comandos propios de CMD. |
|---|---|
| PowerShell | Terminal moderna y versátil. Acepta comandos CMD, comandos similares a Linux (ls, cd) y cmdlets propios (verbo-sustantivo como Get-Process). |
|---|---|
| **Terminal** (app de Windows 11) | Unificador que puede abrir CMD, PowerShell o WSL dentro de la misma aplicación con pestañas. |
|---|---|

**Relación CMD--PowerShell:** desde una PowerShell se puede lanzar cmd.exe para entrar en CMD, y desde CMD se puede lanzar powershell.exe. En entornos comprometidos (reverse shells, exploits), la calidad de la terminal recibida depende mucho del vector de acceso; una RDP da una terminal "al 100%", mientras que un exploit puede dar solo un 30%.

**Ejecutar como administrador:** clic derecho → "Ejecutar como administrador". Equivalente al sudo su de Linux. Cuando la terminal se ejecuta como admin, la barra de título lo indica explícitamente.

## 4. Comandos CMD: comparativa con Linux

### Navegación y listado

| Acción | Linux | CMD Windows |
|---|---|---|
| Listar directorio | ls / ls -la | dir / dir /a Listar sin formato extra | ls | dir /b Listar ordenado por fecha | --- | dir /o:d Buscar archivos recursivos | find / -name \"\*.txt\" | dir /s \*.txt Directorio actual | pwd | cd (sin argumentos) Cambiar directorio | cd ruta | cd ruta Subir al padre | cd .. | cd .. Guardar directorio y moverse | pushd | pushd ruta Volver al directorio guardado | popd | popd Crear directorio | mkdir | mkdir / md Borrar directorio (vacío) | rmdir | rd Borrar directorio (recursivo) | rm -rf | rd /s /q (silencioso, sin alertas) Ver contenido de fichero | cat | type Limpiar pantalla | clear | cls Filtrar texto (grep) | grep \"texto\" fichero | findstr \"texto\" fichero Historial de comandos | history | doskey /history Copiar fichero | cp | copy Mover/renombrar fichero | mv | move |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Diferencia** /s /q **en** rd**:** el flag /q borra en modo silencioso sin pedir confirmación ni generar alertas en el SIEM del Blue Team. Relevante para operaciones de limpieza de rastros en Red Team.

pushd **y** popd**:** permiten guardar la ruta actual, moverse a otra y volver a la anterior con un solo comando. Muy útil cuando se está navegando por un servidor grande y se necesita ir a un directorio temporal sin perder la referencia de dónde se estaba.

## 5. Comandos de información del sistema

### whoami y sus opciones ofensivas

| whoami | # Nombre de máquina\usuario actual whoami /all | # Todo: usuario, SID, grupos y privilegios whoami /priv | # Solo privilegios del usuario actual whoami /groups | # Grupos a los que pertenece el usuario |
|---|---|---|---|---|

### SID: el DNI de Windows

El **SID** (*Security Identifier*) es el identificador único de cada usuario/grupo en Windows. Es análogo al DNI: el nombre puede cambiar pero el SID es permanente. Muchas técnicas de ataque en Windows requieren especificar el SID en lugar del nombre de usuario.

### Privilegios: la clave de la escalada

whoami /priv muestra todos los privilegios del usuario actual. El privilegio más explotable es **SeImpersonatePrivilege** (también llamado "Impersonate"):

- Cuando está en estado **Enabled**, permite al usuario actuar en nombre de otro usuario del sistema.
- Herramientas que lo explotan: **PrintSpoofer**, familia **Potato** (GoodPotato, JuicyPotato, SweetPotato...).
- Funcionamiento: inyectar un ejecutable malicioso que se ejecuta como nt authority(el equivalente a root), escalando de usuario normal a administrador total.
- Esto es muy frecuente en servidores web con IIS o en servicios mal configurados.

## 6. Comandos net: gestión de usuarios, grupos y red

### net user

| net user | # Lista todos los usuarios locales de la máquina net user <nombre> | # Detalle de un usuario: estado activo, expiración, grupos... net user castillo Pass123! /add # Crea un nuevo usuario local |
|---|---|---|

**Uso ofensivo:** cuando se tiene acceso remoto a un sistema (reverse shell, exploit), net user castillo Pass123! /add crea un usuario desde dentro de la máquina víctima para mantener persistencia.

**Lo que revela** net user \<nombre\>**:** - Si la cuenta está activa o inactiva. - Si la contraseña expira (¡una cuenta que nunca expira es un hallazgo reportable!). - Privilegios asignados. - Comentarios del campo descripción (¡pueden contener contraseñas por defecto!).

**Truco de enumeración:** los administradores de IT suelen dejar la contraseña por defecto de las cuentas nuevas en el campo "Comentario". Hacer un script que itere net user sobre todos los usuarios y filtre el campo comentario puede revelar credenciales sin necesidad de ningún exploit.

### net localgroup

| net localgroup | # Lista todos los grupos locales net localgroup Administrators | # Lista los miembros del grupo Administradores net localgroup Administrators castillo /add # Añade un usuario al grupo de Admins |
|---|---|---|

**Uso ofensivo:** añadir el usuario creado (persistencia) al grupo de Administradores para tener privilegios completos. Muchas veces se puede ejecutar siendo un usuario poco privilegiado si los permisos del sistema están mal configurados.

**Distinguir Admin local de Admin de dominio:** un administrador local solo tiene privilegios sobre su equipo. El Domain Admin tiene privilegios sobre todos los equipos del dominio. En auditorías de Active Directory, el objetivo es comprometer el Domain Admin.

### net accounts

| net accounts | # Muestra la política de contraseñas: longitud mínima, umbral de bloqueo... |
|---|---|

**Uso ofensivo crítico --- caso real:** el campo "umbral de bloqueo" indica cuántos intentos fallidos bloquean la cuenta. Lanzar un ataque de fuerza bruta configurando el script para **un intento menos que el umbral** evita bloquear cuentas. En el ejemplo real: el equipo no revisó este dato, el umbral era 3 (ellos creían que 5) y bloquearon a **toda la compañía** de un bufete de abogados a las 12 de la mañana durante la auditoría.

### net use

Lista las unidades de red mapeadas (carpetas compartidas accesibles desde la red, SMB/Samba).

### net share

Muestra las carpetas compartidas del equipo actual. Permite identificar recursos disponibles para movimiento lateral.

### net time

Sincroniza la hora del equipo con la del Domain Controller. Crítico para algunos exploits (ej. Kerberoasting) que requieren que la diferencia de tiempo entre atacante y servidor sea menor de 5 minutos.

Herramienta complementaria: **ntpdate** --- sincroniza la hora de Kali con la del servidor objetivo antes de lanzar ataques dependientes del tiempo.

## 7. Diferencias CMD vs. PowerShell

| Característica | CMD | PowerShell |
|---|---|---|
| Antigüedad | Heredado de MS-DOS | Moderno (2006) Comandos Linux | No (solo ls en versiones recientes) | Sí (ls, cat, cd, etc.) Cmdlets propios | No | Sí (Get-Process, Set-Item, Invoke-Command...) Scripting avanzado | Limitado | Completo (bucles, objetos, .NET) Ejecutar .exe | Directamente por nombre | Con .\\ejecutable.exe o ruta completa Versatilidad | Menor | Mayor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

En auditorías, ambas sirven y se puede saltar entre una y otra. La elección depende del vector de acceso y del entorno. PowerShell es más potente pero también más monitorizado por los EDR modernos.

## 8. Consideraciones prácticas para auditorías de Windows

- **No confiar en versiones modernas:** la mayoría de servidores corporativos corren Windows Server 2008 R2, 2012 o 2016 --- versiones antiguas donde muchos de los "atajos" modernos no funcionan.
- **Comillas en rutas con espacios:** si una ruta tiene espacios (ej. Program Files), siempre ponerla entre comillas dobles para que no la interprete como dos argumentos.
- **TTL para identificar el SO:** al hacer ping, un TTL cercano a **64** indica Linux; cercano a **128** indica Windows. Dato muy útil en la fase de reconocimiento.
- **Comentarios en código fuente (Ctrl+U en navegador):** los comentarios de desarrolladores en el HTML/JS/CSS de una aplicación pueden contener credenciales, rutas internas o instrucciones sensibles. Revisarlos siempre.

## 9. Próximos temas

- Continuación con PowerShell en profundidad (cmdlets Get/Set, objetos .NET, scripting).
- Configuración de máquinas virtuales Windows para laboratorio.
- Ejercicios de la plataforma exercises.academics.es enfocados en CMD y PowerShell.
- Más adelante: Active Directory, escalada de privilegios en Windows, Pass-the-Hash, Kerberoasting.

## 10. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| PowerCell / Powercell | **PowerShell** -- terminal avanzada de Windows SMD / CMT | **CMD** (*Command Prompt*) -- terminal clásica de Windows directorio activo | **Active Directory (AD)** -- sistema de gestión de usuarios y recursos en entornos Windows corporativos domain control / DC | **Domain Controller (DC)** -- servidor que gestiona el Active Directory domain admin / administrador de dominio | **Domain Admin** -- usuario con privilegios sobre todos los equipos del dominio seiman personate / sein personate | **SeImpersonatePrivilege** -- privilegio de Windows que permite actuar en nombre de otro usuario Print Spoofer / Print Spoofer | **PrintSpoofer** -- herramienta de escalada de privilegios vía SeImpersonatePrivilege potatos / good potato | **Potato exploits (GoodPotato, JuicyPotato...)** -- familia de herramientas de escalada mediante SeImpersonatePrivilege SID / código del país | **SID** (*Security Identifier*) -- identificador único de usuario/grupo en Windows doski history / 2k mass history | doskey /history -- comando CMD para ver el historial de sesión jwamai / juamai / huamai | whoami -- comando que muestra el usuario actual (Linux y Windows) reversal / reverse | **Reverse shell** -- conexión de retorno desde el sistema comprometido al atacante net time / NTDate | net time / **ntpdate** -- sincronización de hora con el Domain Controller QEMU / CAHAS | **QEMU / KVM** -- soluciones de virtualización nativas en Linux DLS / DLL | **DLLs** (*Dynamic Link Libraries*) -- librerías dinámicas de Windows las 4G vulnerabilidad Linux | Probablemente referencia a **CVE-2024-6387 (regreSSHion)** o **Dirty COW** -- vulnerabilidades críticas de Linux que afectaron a todas las versiones fuzzing / fuerza bruta | **Brute force / Password spraying** -- técnica de probar contraseñas masivamente contra cuentas de usuario bufete / caso real | Caso real de auditoría de Active Directory que bloqueó todas las cuentas de un bufete de abogados control U | **Ctrl+U** en navegador -- ver el código fuente de una página web macro virus / herramienta de inventory | **Herramienta de inventario de activos** -- plataforma mostrada por César para SGSI y análisis de riesgos con IA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase2.md|resumen_master_clase2]] — IA en Ciberseguridad, Linux, Windows
- [[resumen_master_clase4.md|resumen_master_clase4]] — IA en Ciberseguridad, Linux, Windows
- [[../PREWORK/resumen_clase6.md|resumen_clase6]] — IA en Ciberseguridad, Metasploit, Windows
- [[../PREWORK/resumen_clase7.md|resumen_clase7]] — IA en Ciberseguridad, Metasploit, Windows
- [[../PREWORK/resumen_clase2.md|resumen_clase2]] — IA en Ciberseguridad, Metasploit, Windows
- [[../../Apuntes/11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Linux, Metasploit, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

> #blue-team #escalada-privilegios #forense #hydra #ia #kali #linux #metasploit #netcat #normativa #redes #reverse-shell #windows
