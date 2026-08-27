> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 19**
> **Módulo:** MODULO3
> **Tema:** Clase 19
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 19. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Esta sesión la imparte Daniel, miembro del equipo de Red Team en Telefónica, y supone el arranque del módulo ofensivo del máster.

Es la primera vez que el grupo trabaja activamente con máquinas vulnerables: ya no se trata de analizar tráfico de red en diferido, sino de comprometer un objetivo real en un entorno controlado.

El hilo conductor es la metodología de un pentester desde cero: cómo se monta el laboratorio, cómo se localiza la víctima en la red sin saber su IP de antemano, cómo se enumera lo que hay expuesto y cómo se decide qué atacar primero.

La clase también abre una conversación sobre el contexto profesional real: tipos de auditoría, ruido operacional, certificaciones y por qué la enumeración es la fase que determina el éxito o el fracaso de todo lo que viene después.

### El laboratorio: Metasploitable y Kali en red compartida El entorno de trabajo de este módulo son dos máquinas virtuales corriendo en VirtualBox o VMware.

La máquina atacante es Kali Linux , la distribución estándar del sector par a pentesting.

La máquina víctima es Metasploitable , una distribución Linux deliberadamente vulnerable diseñada para practicar explotación.

Se trabaja con la versión 3, aunque la versión 2 es prácticamente equivalente en concepto.

La condición fundamental p ara que el laboratorio funcione es que ambas máquinas estén en la misma red.

Las opciones de configuración en VirtualBox son NAT (cada máquina tiene su propia red interna), Red NAT (permite crear un rango personalizado compartido) y adaptador puente (la máquina se integra en la red física del equipo host).

La opción más sencilla y limpia para este laboratorio es adaptador puente, que garantiza visibilidad entre máquinas sin conflictos de direccionamiento.

Las credenciales de acceso a Metasploitable 3 son va grant / vagrant.

Una vez arrancada, la máquina se deja en segundo plano: no se interactúa con ella directamente, solo se usa como objetivo desde Kali.
> [!important] - La idea clave: el laboratorio simula el escenario real de un pentester que se conecta a la red
de un clie nte.

Kali es su equipo de trabajo, Metasploitable es el activo que tiene autorización para atacar.

Todo lo que se aprende aquí tiene traducción directa a una auditoría real

Fase 1 — Descubrimiento: Net -Discover En una auditoría real, el primer problema es saber qué hay en la red.

No se conoce la IP del objetivo de antemano.

Net-Discover es la herramienta para resolver esto: envía peticiones ARP al rango de red especificado y recoge las respuestas de todos los hosts activos.

Es esencialmente un broadcast dirigido que mapea qué equipos están vivos. sudo netdiscover -r 10.0.2.0/24 El parámetro -r indica el rango a escanear.

La máscara /24 cubre las 254 IPs del último octeto.

El resultado es una tabla con las IPs activas, sus direcciones MAC y el fabricante del adaptador de red, lo que ya da pistas sobre el tipo de dispositivo.

La diferencia entre Net -Discover y Nmap para este propósito es el ruido generado.

Net -Discover hace pings silenciosos para ver quién responde.

Nmap, en cambio, escanea todos los puertos d e

cada IP, lo que genera un volumen de peticiones que puede disparar alertas en sistemas de detección.

En un entorno real, Net -Discover es el primer paso precisamente porque es más sigiloso.
- La metáfora útil: Net-Discover pregunta en silencio a toda la sal a "¿hay alguien aquí?" y
espera que levanten la mano.

Nmap entra ya a cada persona y le registra los bolsillos uno a uno.

Ambos tienen su momento, pero el orden importa

Fase 2 — Enumeración de puertos: Nmap Una vez localizada la IP del objetivo, el siguie nte paso es saber qué servicios tiene expuestos.

Nmap es la herramienta estándar para esto.

Daniel trabaja con un comando completo que combina varios parámetros: nmap -p- -sC -sV -Pn -T5 --open -oN full_scan IP_OBJETIVO Cada parámetro tiene su función:
- -p- escanea los 65.535 puertos, no solo los más comunes
- -sC lanza los scripts por defecto de la base de datos de Nmap sobre cada puerto abierto,
buscando vulnerabilidades conocidas y configuraciones débiles
- -sV detecta la versión exacta del servicio que corre en cada puerto
- -Pn omite el ping previo y escanea directamente los puertos aunque el host no responda a
ICMP, útil cuando el firewall bloquea ping pero el host sigue activo
- -T5 controla la velocidad (de T1 a T5, siendo T1 el más lento y sigiloso, T5 el má s rápido y
ruidoso); en CTF se usa T5 para ir rápido, en entorno real T1 para no levantar alertas
- --open filtra el output mostrando solo los puertos abiertos
- -oN full_scan guarda el resultado en un fichero de texto
En auditorías reales se recomienda hacerlo en dos fases: primero un escaneo rápido de todos los puertos sin scripts ( -p- únicamente) para obtener la lista de puertos abiertos, y después lanzar -sC - sV solo sobre esos puertos.

Esto reduce el tráfico generado y es más sigiloso.

El resultado d el escaneo sobre Metasploitable 3 devuelve varios servicios, entre ellos el puerto 21 (FTP) con la versión ProFTPD 1.3.5 , el puerto 22 (SSH) y el puerto 80 (HTTP con Apache y Drupal visible en el navegador).

Fase 3 — Búsqueda de exploits: SearchSploit y M etasploit Con la versión exacta del servicio identificada, el siguiente paso es buscar si existe un exploit conocido.

SearchSploit es una herramienta de línea de comandos que consulta la base de datos de ExploitDB localmente: searchsploit ProFTPD 1.3.5 El resultado muestra cuatro entradas, incluyendo un RCE (Remote Code Execution) disponible tanto como módulo de Metasploit (escrito en Ruby) como en un script independiente en Python.

Metasploit (msfconsole) es el framework de explotación más completo del sec tor.

No es solo para lanzar exploits: incluye módulos de enumeración, fuerza bruta, post -explotación y gestión de sesiones.

Para trabajar con el exploit de ProFTPD: search ProFTPD 1.3.5 use 0 show options set RHOSTS IP_OBJETIVO run
- search localiza el módul o dentro de la base de datos de Metasploit
- use 0 carga el primer resultado (el índice que aparece en la tabla)
- show options muestra los parámetros configurables del módulo: RHOSTS (IP objetivo),
LHOST (IP local, la nuestra), puertos, etc.
- set asigna valore s a esos parámetros
- run lanza el exploit
Cada módulo tiene su propia configuración y los parámetros no se comparten entre módulos.

Si se cambia a otro módulo hay que configurarlo desde cero.

Fase 4 — Fuerza bruta sobre FTP Cuando un exploit no funciona directamente o falta información (como el SITEPATH que pedía el módulo de ProFTPD), una alternativa para FTP es el ataque de fuerza bruta con diccionarios.

Se realizó de dos formas: Con Metasploit, usando el módulo auxiliar de escaneo de login FTP: search ftp/login use 0 set RHOSTS IP_OBJETIVO set USER_FILE /ruta/usuarios.txt set PASS_FILE /ruta/passwords.txt run Con Hydra , herramienta dedicada a fuerza bruta de autenticación: hydra -L usuarios.txt -P passwords.txt ftp://IP_OBJETIVO En ambos casos se requieren dos ficheros de texto: uno con usuarios candidatos y otro con contraseñas.

Para construirlos en un entorno real se combina OSINT previo (credenciales filtradas en LeakRadar, patrones de contraseñas detectados, información de emp leados) con usuarios por defecto universales: admin, administrator, ftp, anonymous, el nombre de la máquina.

La herramienta CUPP (Common User Passwords Profiler) permite generar diccionarios personalizados a partir de información del objetivo: nombre, apel lidos, fecha de nacimiento, empresa, mascotas.

El resultado del ataque confirmó que las credenciales vagrant/vagrant usadas para acceder a la máquina también funcionan en el servicio FTP.

Reutilización de credenciales entre servicios: uno de los fallos más comunes en entornos reales.
> [!important] - La idea clave: guardar siempre evidencia de todos los intentos, incluyendo los fallidos.

En
una auditoría real, el informe tiene que demostrar qué se probó y qué no funcionó, no solo lo que se comprometió

### Contexto profesional: tipos de auditoría y ruido operacional Daniel abre un debate sobre cómo se trabaja en Red Team en la práctica.

Los tres tipos de auditoría son caja negra (sin información previa, solo el objetivo), caja blanca (con acceso completo al código, infraestructu ra y credenciales) y caja gris (acceso parcial, por ejemplo un usuario de dominio sin privilegios).

La caja negra es la más cara y la que más se parece al trabajo de un atacante real; la mayoría del mercado en España opta por grises y blancas por coste.

En un Red Team ejercicio real, el Blue Team puede detectar y cortar el ataque.

Por eso el ruido operacional importa: lanzar Nmap con T5 contra toda la red genera tráfico que cualquier SIEM con reglas básicas detecta.

La disciplina de ir lento (T1, escaneos p or fases, Net -Discover antes que Nmap) no es perfeccionismo, es supervivencia operacional.

### Sobre certificaciones: el EJPT permite usar Metasploit sin restricciones.

El OSCP lo permite una sola vez por examen; si se usa y no funciona, se pierde esa carta.

E l OSCP+ tiene caducidad (dos años), igual que el EJPT (tres años).
> [!important] - La idea clave: la enumeración es la fase que determina el éxito de todo lo que viene
después.

Un exploit bien elegido sobre un servicio mal enumerado falla.

Un exploit mediocre sobre un ser vicio perfectamente enumerado tiene muchas más posibilidades

Recapitulación integrada Al cerrar esta sesión hemos montado por primera vez un laboratorio de explotación real y recorrido las cuatro primeras fases de un pentest: descubrimiento de hosts con N et-Discover, enumeración de puertos y versiones con Nmap, búsqueda de exploits con SearchSploit y Metasploit, y fuerza bruta sobre FTP con Metasploit y Hydra.

Sabemos que ir por fases genera menos ruido que lanzar todo de golpe, que la reutilización de cre denciales entre servicios es un fallo real y frecuente, y que documentar los fallos es tan importante como documentar los éxitos.

La próxima sesión continúa con la explotación de los servicios restantes de Metasploitable y la escalada de privilegios.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase29.md|resumen_master_clase29]— Kali Linux, Metasploit, SSH
- [[resumen_master_clase26.md|resumen_master_clase26]— Kali Linux, OSINT, SSH
- [[resumen_master_clase30.md|resumen_master_clase30]— Escalada de Privilegios, Kali Linux, SSH
- [[resumen_master_clase20.md|resumen_master_clase20]— Kali Linux, Redes, SSH
- [[../../transcripciones/Junio/19.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking.md|19.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]— Kali Linux, Metasploit, SSH
- [[../../apuntes Andres/01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress.md|01.07.2026 Explotación Web WPScan File Upload y Reverse Shell en WordPress]— Escalada de Privilegios, Kali Linux, SSH

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #blue-team #certificaciones #command-injection #escalada-privilegios #hydra #ia #kali #linux #metasploit #metasploitable #nmap #osint #pentest #redes #ssh
