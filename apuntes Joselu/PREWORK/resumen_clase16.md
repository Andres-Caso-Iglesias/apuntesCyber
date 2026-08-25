> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 16**
> **Módulo:** PREWORK
> **Tema:** Clase 16
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 16. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 16: Metodología de Pentesting – Fases de la Auditoría Técnica Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción Esta sesión cierra el bloque de metodología, completando las cuatro fases que faltaban del ciclo de auditoría técnica: explotación, escalada de privilegios, pivoting/post-explotación y reporte .

Se abordan de forma conceptual porque son el núcleo de la parte práctica del máster, donde se verán en profundidad a lo largo de los seis meses. 2.

Fase 2 – Explotación ¿Qué es la explotación?

La explotación consiste en conseguir un acceso no autorizado a un sistema explotando una vulnerabilidad conocida (CVE).

En auditorías técnicas estándar no se buscan zero-days; éstos se reservan para ejercicios de Red Team avanzado.

Técnicas de explotación según el activo Las técnicas varían según el tipo de recurso que se está auditando:
- Aplicaciones web: SQL Injection, subida no autorizada de archivos, ejecución de una
reverse shell en PHP, XSS, IDOR, etc.
- Servidores: identificar servicios con versiones obsoletas o deprecated en los puertos
abiertos y lanzar el exploit correspondiente (ej. servidor FTP, servidor de correo, SMB).
- Active Directory: técnicas específicas como Pass-the-Hash, Kerberoasting, etc.

Técnicas de OPSEC (sigilo) Las técnicas de OPSEC (Operational Security ) son técnicas avanzadas de evasión de controles de seguridad: EDR, antivirus, IPS, SOAR, WAF, firewalls.

Se correlacionan con la certificación OSEP (siguiente nivel al OSCP).

Son propias de ejercicios de Red Team avanzado, donde el objetivo es no ser detectado.

En una auditoría técnica estándar el ruido no es problema: el auditor puede ser detectado porque el objetivo es encontrar vulnerabilidades, no evadir los sistemas de defensa. 1

## 3.

Fase 3 – Escalada de Privilegios Concepto y objetivo Tras una explotación exitosa se suele obtener acceso con un usuario estándar sin privilegios de root/administrador .

La escalada de privilegios es el proceso de pasar de ese usuario de bajo privilegio a root (Linux) o SYSTEM/Domain Admin (Windows).

Para poder escalar es necesario volver a la fase de enumeración , esta vez interna: identificar el sistema operativo y su versión exacta, la versión del kernel, los servicios que corren localmente y sus configuraciones.

Herramientas de escalada de privilegios
- LinPEAS (Linux Privilege Escalation Awesome Script ): script que enumera
automáticamente todas las vías de escalada posibles en sistemas Linux/Unix.
- WinPEAS (Windows Privilege Escalation Awesome Script ): equivalente para sistemas
Windows.
- Ambos generan un output muy detallado que el auditor analiza para identificar la vía de
escalada más efectiva.
- Ejemplo de vulnerabilidad de kernel citada: Dirty COW (Dirty Copy-On-Write ), exploit
que afectaba a versiones antiguas del kernel Linux y permitía escalada directa a root.

Escalada en Active Directory La escalada en entornos de Active Directory es diferente a la de máquinas independientes (standalone).

Sigue metodologías propias cubiertas en certificaciones como CRTP (Certified Red Team Professional ) y CRTO (Certified Red Team Operator ).

Durante el máster se parte de máquinas standalone para construir la base. 4.

Fase 4 – Pivoting y Post-Explotación Pivoting: movimiento lateral entre segmentos de red El pivoting es la técnica de saltar entre máquinas de distintos segmentos de red para alcanzar activos que no son directamente accesibles desde el punto de entrada inicial.

Ejemplo: una red segmentada en tres subredes (10.0.1.x, 10.0.2.x, 10.0.3.x).

La máquina 1 (en el primer segmento) no puede comunicarse directamente con la máquina 6 (en el tercer segmento), pero sí con la máquina 2, que a su vez puede comunicarse con la 4, y ésta con la 6.

El pivoting crea túneles a través de esa cadena para que la máquina 1 llegue a la 6.

Técnicas y herramientas: - Port forwarding: técnica base para redirigir tráfico a través de los 2

túneles. - Ligolo-ng: herramienta recomendada por el profesor para crear interfaces de red virtualizadas y gestionar el pivoting de forma sencilla.

Más eficiente que hacerlo con Metasploit.

Ciclo de movimientos laterales con hashes El patrón de trabajo en un entorno con múltiples máquinas sigue siempre el mismo ciclo: 1.Acceder a la máquina → escalar privilegios a administrador local. 2.V olcar todos los hashes de contraseñas con Mimikatz. 3.Romper los hashes con Hashcat (GPU) o John the Ripper (CPU) para obtener contraseñas en claro. 4.Usar esas credenciales para acceder a la siguiente máquina del segmento. 5.Si el hash no se puede romper, aplicar Pass-the-Hash: autenticarse enviando el hash directamente sin necesidad de conocer la contraseña en claro. 6.Repetir el ciclo en cada nueva máquina hasta llegar al controlador de dominio o al activo final.

Robustez de contraseñas y cracking de hashes Una contraseña en texto claro, independientemente de su longitud, no aporta seguridad cuando se roba la base de datos.

Lo que importa es la dificultad computacional de romper el hash :
- Algoritmos débiles como Blowfish (habitual en páginas web pequeñas) se rompen con
rapidez.
- Romper un hash consiste en generar el hash de todas las combinaciones posibles y
compararlo con el hash robado hasta encontrar una coincidencia.

Las GPUs son exponencialmente más rápidas que las CPUs para este proceso.
- Una contraseña tipo “admin” se rompe en 5 segundos; con 12 caracteres alfanuméricos y
especiales el tiempo se vuelve inviable.
- Los atacantes no hackean bancos directamente: hackean plataformas pequeñas y mal
protegidas, obtienen credenciales en claro tras romper los hashes débiles, y reutilizan esas mismas credenciales en el banco (credential stuffing), aprovechando que la mayoría de usuarios reutilizan contraseñas.

Persistencia Una vez conseguido el acceso y la escalada de privilegios, se instala un mecanismo de persistencia para mantener el acceso aunque se parchee la vulnerabilidad original.

Ejemplo del profesor: archivo .php colocado en una ruta concreta de la web del servidor comprometido, que permite recuperar la reverse shell en cualquier momento.

El equipo del profesor mantiene accesos a activos comprometidos con más de cinco años de antigüedad gracias a estos mecanismos. 3

## 5.

Fase 5 – Reporte Por qué el reporte es tan importante como la enumeración El cliente nunca ve las horas de trabajo frente a la pantalla, los diccionarios probados, la investigación en la Deep Web ni los exploits fallidos.

Lo único que ve es el informe.

Un reporte deficiente hace que una auditoría técnica brillante no tenga ningún valor para el cliente.

A lo largo del máster cada máquina practicada llevará su propio mini-reporte, y periódicamente se defenderán informes completos ante el profesor.

Los dos tipos de informe Informe técnico: - Dirigido a los técnicos de la organización que deben remediar las vulnerabilidades. - Incluye: roadmap completo de la explotación, técnicas utilizadas, capturas de pantalla como evidencias, CVEs explotados, herramientas, recomendaciones técnicas específicas para cada hallazgo.

### Informe ejecutivo: - Dirigido a la dirección y perfiles no técnicos (el que finalmente firma el contrato y paga). - Mismo contenido pero sin tecnicismos: resultados, impacto en el negocio, nivel de riesgo y recomendaciones en lenguaje comprensible. - Tan importante o más que el técnico: si el directivo no entiende el problema, no invertirá en remediarlo. 6.

### Resumen visual: el ciclo completo de una auditoría técnica Enumeración pasiva (Shodan, Censys, Dehashed, Deep Web, Google Dorking) ↓ Enumeración activa (Nmap, Sublist3r, fuzzing) ↓ Explotación (CVE + exploit, SQL Injection, reverse shell, etc.) ↓ Enumeración interna (LinPEAS / WinPEAS → versión kernel, servicios) ↓ Escalada de privilegios (root / SYSTEM / Domain Admin) ↓ Volcado de hashes (Mimikatz) → cracking (Hashcat / John the Ripper) ↓ Pivoting (Ligolo-ng, port forwarding) → siguiente segmento/máquina ↓ Persistencia (reverse shell oculta, backdoor) ↓ Reporte técnico + ejecutivo 4

## 7.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración Ciudad de Seguridad Defensiva Ciberseguridad – término mal transcrito OBSSEC / off-sec OPSEC (Operational Security ) – técnicas de sigilo y evasión; Offensive Security (empresa de certificaciones) OSEP OSEP (Offensive Security Experienced Penetration Tester) – certificación avanzada de Offensive Security OSCP OSCP (Offensive Security Certified Professional) – certificación estándar de pentesting Unix for Linux / WinPyth LinPEAS y WinPEAS – scripts de enumeración para escalada de privilegios en Linux y Windows Deartico Dirty COW (Dirty Copy-On-Write , CVE-2016-5195) – exploit de escalada de privilegios en kernels Linux antiguos CRTP / CRTO CRTP (Certified Red Team Professional ) y CRTO (Certified Red Team Operator ) – certificaciones de Active Directory ligolo Ligolo-ng – herramienta de pivoting mediante interfaces de red virtualizadas mimi cats / Mimikatz Mimikatz – herramienta de volcado de credenciales y hashes de memoria Windows john de ripper / has cat John the Ripper y Hashcat – herramientas de cracking de hashes pas de has Pass-the-Hash (PtH) – técnica de autenticación con el hash sin conocer la contraseña en claro blowfish Bcrypt/Blowfish – algoritmo de hashing de contraseñas usado en muchas aplicaciones web has / hases Hash / hashes – resultado de una función criptográfica aplicada a una contraseña gneus / geneo GPUs (Graphics Processing Units ) – tarjetas gráficas usadas para cracking masivo de hashes entro vuelco Referencia al ciclo “ entro → vuelco hashes → rompo → accedo a siguiente máquina ” de los movimientos laterales reversal Reverse shell – conexión de retorno desde el equipo comprometido al servidor del atacante stand alone Standalone – máquina independiente, no integrada en un dominio Active Directory metasploit Metasploit Framework – framework de 5

Término en la transcripción Corrección / Aclaración explotación y post-explotación bridge forums BreachForums – foro de la Deep Web para filtración de bases de datos de haced Dehashed – plataforma de búsqueda de credenciales filtradas Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6