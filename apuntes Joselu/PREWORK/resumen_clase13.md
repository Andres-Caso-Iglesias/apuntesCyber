> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 13**
> **Módulo:** PREWORK
> **Tema:** Clase 13
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 13. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 13: Conceptos de la Informática Moderna Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción Esta sesión cubre tres bloques esenciales para el hacking ofensivo: los tres pilares de la informática moderna (Cloud, computación cuántica y GPUs), los conceptos clave de Windows (registros de memoria, buffer overflow y gestión de usuarios) y los permisos y grupos en Linux (el sistema rwx).

El objetivo no es dominar estos conceptos ahora, sino tenerlos como marco de referencia para cuando aparezcan durante el máster.

PARTE I: Los tres pilares de la informática moderna 2.

Cloud Computing La nube no es ningún concepto mágico: es el servidor físico de un tercero (generalmente en Holanda) alquilado bajo las marcas de Amazon Web Services (AWS) , Microsoft Azure o Google Cloud.

Cada proveedor ha implementado su propio estándar de funcionamiento, lo que hace que las auditorías cloud sean especializadas y diferentes a las auditorías on-premise convencionales.

Las auditorías cloud siguen la metodología general del pentesting (enumeración, explotación, etc.), pero las herramientas y el enfoque son radicalmente distintos.

El máster se centra en las auditorías técnicas on-premise (redes internas y externas, web, ingeniería social), que siguen siendo el estándar mayoritario, ya que migrar a cloud es muy costoso y la inmensa mayoría de las empresas coexistirán durante años con infraestructuras físicas propias. 3.

Computación cuántica y su impacto en criptografía La computación cuántica no es ciencia ficción: es una forma de aumentar drásticamente la capacidad de cómputo multiplicando por ~100 la potencia de procesamiento actual.

Su relevancia para la ciberseguridad es enorme porque toda la criptografía actual se basa en la dificultad computacional de romper ciertos algoritmos . ¿Cómo funciona un hash?

Una contraseña se pasa por un algoritmo criptográfico (SHA-256, SHA-512, etc.) que produce una cadena aparentemente aleatoria: el hash.

Para “romper” ese hash, un atacante prueba por fuerza bruta todas las combinaciones posibles hasta reproducir el mismo hash y así descubrir la contraseña original.

La fortaleza de un hash depende del tiempo 1

necesario para recorrer todas las combinaciones posibles con la capacidad de cómputo disponible.

Analogía con las criptomonedas: los mineros de Bitcoin hacen exactamente lo mismo: rompen el hash del bloque de blockchain para obtener la recompensa en moneda.

La velocidad a la que se rompen hashes se llama hash rate.

Computación cuántica = hash rate exponencialmente mayor.

Consecuencias para la ciberseguridad: - El primer país que alcance la computación cuántica real podrá romper cualquier cifrado vigente de cualquier otro país, accediendo a toda la información en texto claro. - Afecta a SSL/TLS (el candado HTTPS de los navegadores), al cifrado de comunicaciones y al almacenamiento de contraseñas. - Se compara con la máquina Enigma en la Segunda Guerra Mundial: quien pueda descifrar las comunicaciones del enemigo tiene ventaja estratégica total. - Obligará a desarrollar nuevos algoritmos criptográficos post- cuánticos.

Para el día a día del pentester: la computación cuántica no es imprescindible dominarla, pero sí entender que los rigs de cracking (clústeres de tarjetas gráficas) ya son la herramienta actual para romper hashes obtenidos en auditorías (ej. el archivo ntds.dit del Active Directory). 4.

GPUs vs.

CPUs en ciberseguridad Característica CPU GPU Núcleos Pocos (ej. 20 núcleos en un Intel 13ª gen)Millones de microprocesadores Velocidad por hilo Alta (ej. 2,4 GHz) Muy baja (ej. 1 Hz por hilo) Hilos paralelos Decenas Millones Uso óptimo Procesamiento secuencial complejoProcesamiento masivo en paralelo Aplicación en hacking Ejecución de herramientas Cracking de hashes , entrenamiento de IA Una CPU de 20 núcleos a 2,4 GHz frente a una GPU con 10 millones de hilos a 1 Hz: la GPU pierde en velocidad por hilo pero gana masivamente en paralelismo.

Para romper hashes, lo que importa es el número de combinaciones que se pueden probar simultáneamente, por lo que las GPUs son mucho más eficaces.

En auditorías prácticas: cuando se obtiene el archivo ntds.dit (base de datos del Active Directory con todos los usuarios y contraseñas hasheadas), se usa un rig de cracking (múltiples GPUs en paralelo, exactamente igual que un rig de minería de criptomonedas) para romper los hashes.

Herramientas: Hashcat (con GPUs), John the Ripper (con CPU). 2

PARTE II: Conceptos clave de Windows 5.

Registros de memoria y buffer overflow Windows organiza su memoria en registros de memoria , que son celdas estructuradas donde se almacena información.

Los registros son fundamentales en auditorías ofensivas porque:
- Almacenan credenciales, contraseñas y tokens de autenticación que el usuario no sabe
que están ahí.
- Herramienta principal para extraerlos: Mimikatz (pronunciado “Mimikatz”), la
herramienta más importante del hacking ofensivo según el profesor.

Buffer overflow (desbordamiento de buffer): Es una técnica de escalada de privilegios y obtención de RCE que explota los registros de memoria: 1.Un registro de memoria tiene una longitud máxima definida (ej. 32 bits) y se ejecuta con permisos de usuario normal. 2.El registro contiguo se ejecuta con permisos de administrador. 3.Si un atacante logra escribir un bit de más (33 bits en lugar de 32), ese bit extra “desborda” al registro siguiente y se ejecuta con los permisos de administrador. 4.Si ese bit de más es una shell, el atacante obtiene una shell con privilegios SYSTEM (el nivel más alto en Windows).

El buffer overflow es una de las técnicas más utilizadas para escalada de privilegios y RCE en Windows.

En 2024 se publicó un CVE que explotaba precisamente un registro de memoria de Windows para conseguir escalada directa a SYSTEM. 6.

Jerarquía de usuarios y grupos en Windows Windows organiza los permisos en una jerarquía de tres niveles: 1.Usuario estándar (ej. “carlos”, “rafael”): permisos básicos, sin capacidad de modificar el sistema. 2.Administrador local : privilegios elevados sobre el equipo local únicamente. 3.Administrador de dominio (Active Directory) : los permisos más altos, con autoridad sobre todos los equipos del dominio.

> [!important] ### Principio clave: el Active Directory siempre tiene prioridad sobre la parte local.

Un administrador de dominio puede gobernar y ejecutar acciones sobre cualquier equipo del directorio, independientemente de su configuración local.

Por eso comprometer el Active Directory equivale a comprometer toda la organización .

Los grupos son colecciones de usuarios a los que se asignan permisos de forma centralizada (análogo a los grupos en Linux).

Gestionar permisos por grupos es mucho más eficiente que hacerlo usuario a usuario. 7.

Terminales de Windows
- CMD (Command Prompt): terminal clásico de Windows.

### Comandos útiles: net user

(lista usuarios y grupos), ipconfig, etc.
- PowerShell: terminal más moderno y potente.

Permite scripting avanzado y es el
preferido para automatización en auditorías.

Se dedicará una sesión completa a familiarizarse con ambos terminales y sus comandos más relevantes para pentesting.

PARTE III: Permisos y grupos en Linux 8.

El sistema de permisos rwx En Linux, cada archivo o directorio tiene tres grupos de permisos representados por las letras r (Read/Lectura), w (Write/Escritura) y x (Execute/Ejecución) , aplicados a tres categorías de usuarios:
- Owner (propietario del archivo): segundo trío de bits.
- Group (grupo al que pertenece el propietario): primer trío de bits.
- Others (todos los demás usuarios): tercer trío de bits.

El comando ls -la muestra estos permisos a la izquierda de cada archivo con el formato: rwxrwxrwx.

Sistema de ponderación numérica (octal): Número Binario Permisos 4 100 Solo lectura (r) 5 101 Lectura + ejecución (r-x) 6 110 Lectura + escritura (rw-) 7 111 Lectura + escritura + ejecución (rwx) Ejemplo: chmod 777 fichero asigna todos los permisos (rwx) a los tres grupos. chmod 640 fichero asigna rw al propietario, r al grupo y ningún permiso a otros.

Ejemplo práctico (Carlos y Yuba): Permisos rw-r-xr--: - Group (Evolve, del que es miembro Carlos): rw- → puede leer y escribir, pero NO ejecutar. - Owner: r-x → puede leer y ejecutar, pero NO escribir. - Others (Yuba): r– → solo puede leer. 9.

Por qué los permisos de Linux son críticos para escalada de privilegios Muchas escaladas de privilegios en Linux explotan configuraciones de permisos incorrectas:
- Si un archivo ejecutable pertenece a root y tiene el bit SUID activado (o si others puede
ejecutarlo con permisos de root), cualquier usuario que lo ejecute obtendrá temporalmente los privilegios de root.
- Análogamente al buffer overflow en Windows, el atacante obtiene una shell como root

(el equivalente a SYSTEM en Linux) aprovechando un archivo mal configurado.

La lógica es la misma que en el buffer overflow: se ejecuta código con permisos que no corresponden al usuario actual gracias a un fallo de configuración.

Por eso es tan importante para un pentester identificar archivos con permisos anómalos durante una auditoría de Linux.

El comando para modificar permisos es chmod (change mode).

La enumeración de permisos se realizará con ls -la y otras herramientas durante las sesiones prácticas del máster. 10.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración geneus / gneus GPUs (Graphics Processing Units ) – unidades de procesamiento gráfico; usadas para cracking de hashes e IA mimi cats / mímica Mimikatz – herramienta de volcado de credenciales y hashes de la memoria de Windows ntds punto dit ntds.dit – base de datos del Active Directory que contiene todos los usuarios y hashes de contraseñas hases / has rate Hashes / Hash rate – resultado de una función criptográfica / velocidad de cómputo de hashes SHA256 / SHA512 / SHA128 SHA-256 / SHA-512 / SHA-128 – algoritmos de hash criptográfico SSLTLS SSL/TLS – protocolos de cifrado de comunicaciones web (el “candado” HTTPS) bo buffer overflow Buffer Overflow – desbordamiento de buffer, técnica de escalada de privilegios y RCE threads / 3 Threads (hilos de ejecución) – unidades de procesamiento paralelo de x día dxdiag – herramienta de diagnóstico del sistema en Windows salto la rana / en fifo / en lifo Algoritmos de recorrido de hashes : FIFO (First In, First Out), LIFO (Last In, First Out) CGI de Linux CLI de Linux (Command Line Interface ) – interfaz de línea de comandos; el intérprete se llama Bash loaner Owner – propietario de un archivo en Linux Change Mod chmod (change mode) – comando Linux para cambiar permisos de archivos rig de cracking Cracking rig – clúster de GPUs para romper hashes de contraseñas (idéntico hardware a un rig de minería) 5

Término en la transcripción Corrección / Aclaración azul Azure – plataforma cloud de Microsoft blockchain Blockchain – cadena de bloques; tecnología base de las criptomonedas on premise / on-premise On-premise – infraestructura tecnológica alojada físicamente en las instalaciones propias Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Linux, Metasploit, Windows
- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]] — Linux, Metasploit, Windows
- [[resumen_clase6.md|resumen_clase6]] — IA en Ciberseguridad, Metasploit, Windows
- [[../../apuntes evolve/BLOQUE 6.md|BLOQUE 6]] — Linux, Metasploit, Windows
- [[../../Apuntes/comandos/Netcat.md|Netcat]] — Linux, Metasploit, Windows
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Linux, Metasploit, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #escalada-privilegios #hydra #ia #john #linux #metasploit #netcat #pentest #post-explotacion #redes #reverse-shell #windows
