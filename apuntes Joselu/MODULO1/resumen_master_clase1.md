> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 1**
> **Módulo:** MODULO1
> **Tema:** Clase 1
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 1. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Presentación del profesor y filosofía del máster

**Carlos López Pintado** abre la primera sesión del máster presentándose brevemente:

- Fundador y propietario de **Cibersia Security**.
- Procedente del **Grupo OESIA** (multinacional de +5.500 empleados), donde empezó como becario y llegó a director de ciberseguridad en 5 años.
- Especialización principal: **Red Team** (ciberseguridad ofensiva), aunque también trabaja en forense, normativa y Blue Team.
- Sectores en los que ha trabajado: banca, seguros, ejército, defensa, aeroespacial, satélite, inteligencia y colaboración con fuerzas de seguridad del Estado.
- Certificaciones: OSCP, OSWP, CRTP, CRTO, eJPT v2, CEHv10, CSFPC, CHPT, ISO 27001 Internal Auditor, ISO 27001 Lead Auditor, ISO 27001 Implementador, ENS.
- Director del máster: los contenidos los diseña y actualiza él personalmente en cada convocatoria para adaptarlos a las tecnologías del momento.

**Filosofía del máster:** - Ritmo adaptado al nivel más bajo del grupo, con paciencia solicitada a los alumnos más avanzados durante las primeras semanas. - Aprendizaje bidireccional: el profesor aprende de los alumnos tanto como éstos de él. - Enfoque desde la experiencia profesional real: "os voy a contar todas las mierdas que me han pasado y que me pasan a día de hoy". - Novedad en esta convocatoria respecto a la anterior: se sustituye la enseñanza de **N8N** por el desarrollo de **redes neuronales con pseudo-conciencia** para auditorías automatizadas, pen testing, búsqueda de zero-days e investigación de binarios.

## 2. Configuración del entorno de trabajo: VirtualBox y Kali Linux

### ¿Por qué virtualización?

Un ordenador normal solo puede tener un sistema operativo instalado de forma nativa. La virtualización permite **tener un sistema operativo dentro de otro** (ej. Kali Linux dentro de Windows), asignando recursos de CPU, RAM y disco de la máquina anfitriona al sistema operativo invitado.

- Número de máquinas virtuales posibles: limitado por la RAM disponible (el profesor trabaja con 32 GB; los laboratorios están diseñados para funcionar en equipos modestos).
- Recomendación del profesor: máximo 1-2 máquinas virtuales simultáneas para garantizar estabilidad.

### VirtualBox vs. VMware

| Herramienta | Opinión del profesor |
|---|---|
| VirtualBox | Preferida. Open source, estándar del sector. Los Guest Additions pueden dar problemas de redimensionamiento de pantalla (es "una lotería"). VMware | Funciona muy bien (lo admite con dolor), pero no es su primera opción. WSL (Windows Subsystem for Linux) | Alternativa válida para algunos perfiles; hay profesionales que lo usan con éxito. |
|---|---|---|---|

### Descarga e instalación de Kali Linux

Se usa siempre la imagen preconfigurada para VirtualBox (.ova), nunca la ISO (evita el proceso de instalación manual). Pasos: 1. Descargar VirtualBox desde virtualbox.org. 2. Descargar Kali Linux en formato **Virtual Machines \> VirtualBox** desde kali.org. 3. Doble clic en el archivo descargado → se importa automáticamente en VirtualBox. 4. Al iniciar por primera vez: **no tocar nada** hasta que se instalen los Guest Additions (habilitan redimensionamiento de pantalla y copiar/pegar). 5. Credenciales por defecto: usuario kali, contraseña kali.

### Gestión de máquinas virtuales: copias de seguridad

El profesor rompió **17 máquinas virtuales en 9 meses** de máster. Kali Linux está diseñada para instalar mucho software con muchas dependencias que colisionan. Estrategia recomendada:

- Mantener siempre una **imagen base limpia** (recién instalada con apt update && apt upgrade).
- Clonar esa imagen base cada vez que se necesite una nueva máquina de trabajo.
- **Nunca guardar información importante dentro de Kali**; mover siempre los datos (capturas, informes, hallazgos) al sistema anfitrión inmediatamente.
- Los **snapshots** en VirtualBox son poco fiables porque llevan hardcodeada la ruta del VDisc; si se mueve a otra carpeta puede generar conflictos.

### Configuración del teclado en Kali

Kali Linux viene por defecto con distribución de teclado estadounidense. Para cambiarlo al español:

**Opción gráfica:** *Settings \> Keyboard \> Layout \> desmarcar* "*Use system defaults*" *\> Add \> Spanish \> Remove English \> Close.*

Comando de terminal (permanente):

setxkbmap es

## 3. Fundamentos de la terminal Linux

### Concepto de interfaz gráfica vs. terminal

La interfaz gráfica es simplemente una "traducción visual" de lo que ocurre en el sistema: carpetas, iconos y ventanas no son más que una representación de estructuras de datos en disco. Todo lo que se hace con el ratón puede hacerse con comandos de terminal, y generalmente de forma más eficiente.

### Estructura del sistema de archivos: path, directorio y fichero

- **Path (ruta):** cadena completa que indica la ubicación de un recurso. Ej.: /home/kali/Desktop/fichero.txt.

- **Directorio (carpeta):** cada elemento entre barras / de un path.

- **Fichero (archivo):** el elemento final de un path cuando termina en una extensión (.txt, .php, .exe...).

- **Barra separadora:** en Linux es / (barra derecha); en Windows es \\ (barra izquierda).

 - Regla mnemotécnica: Windows empieza por **W** → la primera barra de W es \\; Linux empieza por **L** → la barra doblada es /.

- **Directorio actual:** representado por . (punto).

- **Directorio padre (anterior):** representado por .. (dos puntos).

- **Directorio home del usuario actual:** representado por \~ (tilde). Equivalente a /home/kali.

### Comandos básicos de Linux vistos en clase

| Comando | Significado | Uso |
|---|---|---|
| ls | List | Lista el contenido del directorio actual ls -la | List Advanced (ocultos) | Lista todo el contenido incluyendo archivos ocultos, con permisos, tamaño y timestamp cd directorio | Change Directory | Cambia al directorio indicado cd .. | Change Directory (atrás) | Sube un nivel en la jerarquía cd ../directorio | Change Directory relativo | Sube y entra en otro directorio pwd | Print Working Directory | Muestra la ruta actual mkdir nombre | Make Directory | Crea un directorio cat fichero | Concatenate | Muestra el contenido de un fichero sudo apt update | Actualizar repositorios | Descarga la lista de paquetes actualizados sudo apt upgrade | Actualizar paquetes | Instala las versiones más recientes whoami | ¿Quién soy? | Muestra el usuario actual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Truco de productividad:** la tecla **Tab** autocompleta nombres de directorios y ficheros. Si hay varias opciones, Tab muestra todas las posibilidades y permite seleccionar.

### Colores en el listado ls -la

- **Azul:** directorios.
- **Blanco:** ficheros estándar.
- **Verde:** ficheros con permisos de ejecución activos.

### Archivos y directorios ocultos en Linux

Un nombre que empieza por . está oculto y no aparece con ls normal; solo con ls -la. El truco de los administradores que quieren esconder algo: nombrarlo \... (tres puntos), que visualmente el ojo lo omite al ver tantos listados.

## 4. Sistema de permisos en Linux (rwx)

Ya visto conceptualmente en el prework; en esta sesión se aplica en la terminal en tiempo real.

### Estructura de permisos

El comando ls -la muestra los permisos con el formato: \[tipo\]\[owner\]\[group\]\[others\]

Ejemplo: drwxr-xr\-- - d → es un directorio. - rwx → el propietario (owner) puede leer, escribir y ejecutar. - r-x → el grupo puede leer y ejecutar, pero no escribir. - r\-- → otros usuarios solo pueden leer.

### Notación numérica (octal)

Cada permiso tiene un peso binario:

| Permiso | Binario | Valor |
|---|---|---|
| r (read) | 100 | 4 w (write) | 010 | 2 x (execute) | 001 | 1 |
|---|---|---|---|---|---|---|

El valor final de cada trío es la suma de los permisos activos. Ejemplos: - rwx = 4+2+1 = **7** - rw- = 4+2+0 = **6** - r-x = 4+0+1 = **5** - r\-- = 4+0+0 = **4** - \-\-- = 0+0+0 = **0**

Así, chmod 777 da todos los permisos a todos (owner+group+others = 7+7+7). Es **la peor práctica posible**: cualquiera puede leer, modificar y ejecutar el fichero. Si ese fichero es un script ejecutable con sudo, cualquier usuario puede modificarlo y obtener una shell con privilegios de administrador.

### Relación con las IPs

La misma lógica binaria de los permisos aplica a los octetos de una dirección IP: 8 bits por octeto, máximo 255 (2⁰+2¹+2²+2³+2⁴+2⁵+2⁶+2⁷ = 1+2+4+8+16+32+64+128 = 255).

### Comando chmod

| chmod 660 fichero.txt | # rw-rw---- : owner y group pueden leer y escribir; others nada chmod 777 fichero.txt | # rwxrwxrwx : todos pueden hacer todo (¡mala práctica!) chmod +x fichero.txt | # Añade permiso de ejecución a todos |
|---|---|---|---|

### Concepto de hardcoding y variables de entorno

**Hardcodear** un valor en el código significa escribirlo directamente en el fuente (ej. password = \"Admin123\"). Si el código se filtra o es robado, la contraseña queda expuesta. La buena práctica es almacenar valores sensibles en **variables de entorno** del sistema, referenciadas desde el código con sintaxis del tipo \$PASSWORD. Así, aunque el código se robe, el valor real nunca aparece en él.

## 5. IA aplicada a la ciberseguridad: reflexiones y tendencias

El cierre de la sesión deriva en un debate espontáneo sobre el uso de la IA en ciberseguridad:

- **Herramientas más recomendadas** en este momento: **Claude (Anthropic)** y **Claude Code** para desarrollo y automatización; **ChatGPT** para tareas generales; **DeepSeek** y **Grok** para consultas más permisivas.
- **La IA no está limitada técnicamente, sino éticamente:** dar contexto adecuado (Bug Bounty, CTF, laboratorio propio) reduce notablemente las restricciones de los modelos.
- **Prompt injection y prompt engineering** como línea de auditoría emergente: evaluar si una IA o un chatbot corporativo puede ser manipulado para bypassear sus controles de seguridad.
- **N8N como herramienta de automatización** ya empieza a quedar superada por lo que Claude Code puede hacer directamente con lenguaje natural.
- **Redes neuronales con IA:** ya no es necesario conocer las matemáticas subyacentes; con lógica de negocio y prompting estructurado, cualquier alumno puede construir una en semanas (ejemplo real: alumno Oliver, sin base sólida, construyó un sistema de explotación automatizada dedicando \~12 horas diarias en tres meses).
- **Superficie de ataque creciente por IA:** más aplicaciones generadas con IA = más librerías potencialmente vulnerables = mayor demanda de auditores especializados.
- **Regulación:** la **AI Act** europea es el único marco regulatorio activo, pero no cubre jurisdicciones fuera de la UE. La velocidad de cambio del sector hace imposible tener expertos consolidados: "no puedo decir que soy experto en IA porque mentiría, igual que el 90% de las personas que lo dicen".

## 6. Contenidos próximos y estructura del máster

- **Próxima semana:** más comandos de Linux, terminal Windows (CMD y PowerShell), permisos en profundidad.
- **En \~2-3 semanas:** primera clase de IA y herramientas --- cómo montar un entorno de trabajo con IA, conectar herramientas entre sí y crear proyectos automatizados con lenguaje natural.
- **Prácticas del máster:** construcción de herramientas automatizadas con IA; proyectos personales del alumno son válidos y supervisados.
- **En \~5 meses:** práctica 3 de pivoting con Carlos Castillo (incluye la máquina de Active Directory que aún no está disponible).
- **Evento presencial (25 de junio):** Talent Day de Wolf Academy con las convocatorias de enero, octubre y la actual (abril).

## 7. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| Civersia / Cibersia | **Cibersia Security** -- empresa del profesor Grupo OECIA | **Grupo OESIA** -- multinacional de consultoría tecnológica OSVWP | **OSWP** (*Offensive Security Wireless Professional*) -- certificación de redes Wi-Fi EJPTV2 / EJPT-V2 | **eJPT v2** (*eLearnSecurity Junior Penetration Tester*) -- certificación de entrada CHV10 | **CEHv10** (*Certified Ethical Hacker v10*) -- certificación de hacking ético Hack the Box / DriveHandme / Moonhub | **Hack The Box / TryHackMe / VulnHub** -- plataformas de práctica de pentesting Cali / Kali | **Kali Linux** -- distribución Linux orientada a ciberseguridad ofensiva HardCode / hardcodear | **Hardcoding** -- práctica insegura de escribir valores sensibles directamente en el código Uedisc / VDisc | **VDisk** -- disco virtual de una máquina virtual get additions | **Guest Additions** -- componentes de VirtualBox para integración host-invitado Chain mod | **chmod** (*change mode*) -- comando Linux para cambiar permisos Cloud de Code / Cloud Code | **Claude Code** -- herramienta de Anthropic para desarrollo asistido por IA Cloud de Amtropic | **Claude de Anthropic** -- modelo de lenguaje de Anthropic Memlabs | **MemLabs** -- laboratorios de análisis forense de memoria RAM Volatility | **Volatility Framework** -- herramienta de forense de memoria (v2 y v3) PSPound | Probablemente **i3wm** o **tmux** / **Terminator** -- gestores de ventanas y terminales avanzados de Linux Parot / Parot OS | **Parrot OS** -- distribución Linux alternativa a Kali orientada a ciberseguridad Hard Box / Strike Army / Bullhub | **Hack The Box / TryHackMe / VulnHub** -- plataformas CTF y práctica OSINT / UMIN | **OSINT** (*Open Source Intelligence*) / **HUMINT** (*Human Intelligence*) -- tipos de inteligencia RPS / RPE | **RPC** (*Remote Procedure Call*) o **RPS** -- servicios remotos con vulnerabilidades zero-day MCP de Antropic | **MCP de Anthropic** (Model Context Protocol) -- protocolo de contexto de modelos de Anthropic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Septiembre/01.09.2026 Repaso General I.md|01.09.2026 Repaso General I]] — Forense Digital, Normativa / GRC, Pivoting / Movilidad Lateral
- [[../PREWORK/resumen_clase1_.md|resumen_clase1_]] — Normativa / GRC, Pivoting / Movilidad Lateral, VulnHub
- [[resumen_master_clase7.md|resumen_master_clase7]] — Linux, Pivoting / Movilidad Lateral, Windows
- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point — Tier 0.md|Hack The Box- Starting Point — Tier 0]] — Forense Digital, Linux, Pivoting / Movilidad Lateral
- [[resumen_master_clase2.md|resumen_master_clase2]] — Forense Digital, Normativa / GRC, Pivoting / Movilidad Lateral
- [[../PREWORK/resumen_clase11.md|resumen_clase11]] — Forense Digital, Normativa / GRC, Pivoting / Movilidad Lateral

### 🛠️ Herramientas

- [[comandos/Tmux|Tmux]]

> #blue-team #certificaciones #forense #hack-the-box #ia #kali #linux #normativa #osint #pivoting #redes #tmux #vulnhub #windows
