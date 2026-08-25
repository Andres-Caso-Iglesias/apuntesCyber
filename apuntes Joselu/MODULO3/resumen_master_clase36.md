> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 36**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 36
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 36. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Castillo** (Carlos Castillo), que vuelve tras el parÃ³n que hubo en el mÃ¡ster.

Es la primera clase del **mÃ³dulo de hacking web**, el bloque mÃ¡s largo e importante del mÃ¡ster segÃºn el propio profesor.

La dinÃ¡mica de clase tambiÃ©n cambia: habrÃ¡ mÃ¡s teorÃ­a contextual antes de la parte prÃ¡ctica, y se trabajarÃ¡ combinando **PortSwigger Web Security Academy** con **mÃ¡quinas de HackerLab**.

**SituaciÃ³n del mÃ¡ster:** hubo un pequeÃ±o "bache" burocrÃ¡tico entre Evolve y los profesores, ya resuelto.

Las clases continÃºan con la misma dinÃ¡mica y los mismos profesores.

Se recuperarÃ¡n las sesiones perdidas.

**Roadmap del mÃ³dulo de hacking web:** - **DuraciÃ³n estimada:** entre 1 y 2 meses, segÃºn el ritmo del grupo. - **Herramienta central:** PortSwigger Web Security Academy --- se recorrerÃ¡n todos los laboratorios relevantes, uno por uno, no haciendo scroll sino entrando en cada vulnerabilidad. - **Mix de prÃ¡ctica:** laboratorios de PortSwigger + mÃ¡quinas web (primera: HackerLab mÃ¡quina 1). - **PrÃ¡ctica 2 del mÃ¡ster:** auditorÃ­a real de una aplicaciÃ³n web alojada en Internet con vulnerabilidades sin definir.

Cada alumno encontrarÃ¡ mÃ¡s o menos vulnerabilidades.

Es la primera vez que se enfrentan a algo que no estÃ¡ preparado para ser hackeado. - **PrÃ¡ctica 1 del mÃ¡ster:** la publica Carlos prÃ³ximamente.

Por grupos de 2-4 personas.

**Sistema de premios de participaciÃ³n confirmado:** SP (puntos de participaciÃ³n), un ordenador y un tercer premio por confirmar.

Se baraja tambiÃ©n una beca de excelencia para los 2 mejores alumnos del mÃ¡ster (0 coste), pendiente de confirmaciÃ³n.

## 2.

La diferencia entre HTB y una auditorÃ­a web real

Castillo explica la diferencia conceptual antes de entrar en materia:

- En HTB, las mÃ¡quinas tienen exactamente lo necesario para ser comprometidas.

La superficie de ataque estÃ¡ definida y acotada.
- En una auditorÃ­a web real, hay subdominios, rutas no documentadas, APIs, ficheros expuestos, configuraciones incorrectas, y mucha informaciÃ³n que el propio cliente desconoce que tiene.
- Encontrar un IDOR en HTB da un punto.

Encontrar un IDOR en la web de Repsol que expone datos de clientes (tarjetas, datos personales) es una vulnerabilidad crÃ­tica con impacto real en negocio.

**El caso personal de Castillo:** encontrÃ³ una vulnerabilidad IDOR en la UPM (Universidad PolitÃ©cnica de Madrid) que permitÃ­a ver expedientes mÃ©dicos de otros estudiantes cambiando el ID en la URL.

Empresa grande = mÃ¡s superficie de ataque = mÃ¡s probable encontrar algo.

## 3.

OWASP Top 10 2025 --- Las 10 categorÃ­as de vulnerabilidades web

**OWASP** (*Open Web Application Security Project*) publica periÃ³dicamente el **Top 10**, una lista de las categorÃ­as de vulnerabilidades web mÃ¡s frecuentes y crÃ­ticas, basada en anÃ¡lisis de miles de CVEs reales.

La versiÃ³n de 2025 (publicada en enero de 2026) es la mÃ¡s actualizada.

El estÃ¡ndar anterior era el de 2021.

**Para quÃ© sirve en la prÃ¡ctica:** - No hay que aprenderse de memoria en quÃ© categorÃ­a cae cada vulnerabilidad.

La IA lo puede decir automÃ¡ticamente. - Sirve para estructurar informes y dar coherencia metodolÃ³gica al trabajo frente al cliente. - El CISO o director de seguridad del cliente quiere saber que se han revisado las vulnerabilidades mÃ¡s habituales de los Ãºltimos aÃ±os.

El OWASP Top 10 es el estÃ¡ndar de referencia para esa justificaciÃ³n. - Lo importante no es clasificar, sino entender el concepto y saber explotarlo.

### Las 10 categorÃ­as del OWASP Top 10 2025

**A01 --- Control de acceso defectuoso** (*Broken Access Control*) Usuarios que acceden a datos o funciones de otros usuarios o de niveles superiores.

### Ejemplo clÃ¡sico: **IDOR** --- un parÃ¡metro `?id=4` en la URL que al cambiarse a `?id=5` devuelve datos de otro usuario.

TambiÃ©n: **SSRF** (Server-Side Request Forgery).

Es la categorÃ­a mÃ¡s frecuente en auditorÃ­as reales.

**A02 --- Fallos criptogrÃ¡ficos** (*Cryptographic Failures*) Cifrados dÃ©biles, claves mal gestionadas, TLS mal configurado, datos sensibles en texto claro (contraseÃ±as en MD5 o sin hashear, credenciales hardcodeadas).

Era el A03 en 2021, ha subido posiciones.

**A03 --- InyecciÃ³n** (*Injection*) SQL Injection, XSS, Command Injection, LDAP Injection, NoSQL Injection.

Sigue muy arriba porque la superficie es enorme.

El XSS (Cross-Site Scripting) aparece aquÃ­ --- cÃ³digo JavaScript inyectado en pÃ¡ginas que ejecuta otros usuarios.

**A04 --- DiseÃ±o inseguro** (*Insecure Design*) Falta de lÃ­mites en la lÃ³gica de negocio.

Ejemplo: un formulario de subida de ficheros que dice aceptar solo PDFs pero no valida en el backend si se sube un PHP --- es un fallo de diseÃ±o, no de configuraciÃ³n.

**A05 --- ConfiguraciÃ³n de seguridad incorrecta** (*Security Misconfiguration*) Credenciales por defecto, paneles de administraciÃ³n expuestos, cabeceras HTTP inseguras, mensajes de error que revelan rutas internas del sistema, software sin actualizar.

Junto con A01, son las dos categorÃ­as que mÃ¡s aparecen en auditorÃ­as reales segÃºn el profesor. **La causa es el error humano en casi todos los casos.**

**A06 --- Componentes vulnerables y desactualizados** (*Vulnerable and Outdated Components*) Software, frameworks y librerÃ­as desactualizados con CVEs conocidos.

**A07 --- Fallos de autenticaciÃ³n** (*Authentication Failures*) EnumeraciÃ³n de usuarios (messages diferentes para "usuario no existe" vs "contraseÃ±a incorrecta"), contraseÃ±as dÃ©biles, falta de rate limiting o bloqueo de cuentas, ausencia de doble factor.

**A08 --- Fallos en la cadena de suministro de software** (*Software and Data Integrity Failures*) --- **NUEVA en 2025** Es la categorÃ­a que mÃ¡s destaca Castillo por su novedad e impacto actual.

Los desarrolladores incorporan miles de librerÃ­as y dependencias de terceros sin auditarlas.

La IA ha permitido auditar cÃ³digo y librerÃ­as de forma masiva, lo que estÃ¡ descubriendo vulnerabilidades y backdoors en librerÃ­as de open source que antes nadie revisaba.

El ejemplo citado: un desarrollador que introdujo una backdoor en una librerÃ­a de open source que fue usada por miles de proyectos.

Las grandes multinacionales tienen esto como preocupaciÃ³n nÃºmero uno de sus CISOs.

TambiÃ©n aplica a los plugins de WordPress.

**A09 --- Fallos en el registro y monitorizaciÃ³n** (*Security Logging and Monitoring Failures*) Falta de logs, falta de alertas, falta de monitorizaciÃ³n.

Sin logs, si alguien entra no hay forma de saberlo ni de hacer forense despuÃ©s.

Castillo cita un caso real: un cliente que llamÃ³ para hacer un forense de un ex-empleado y no tenÃ­a absolutamente ningÃºn sistema de monitorizaciÃ³n. "*Es como ir a la policÃ­a a decir que te han robado y que las cÃ¡maras te las ponen maÃ±ana.*"

**A10 --- Mala gestiÃ³n de situaciones excepcionales** (*Server-Side Request Forgery*) Mensajes de error que filtran informaciÃ³n sensible (rutas del sistema, versiones de software, queries SQL).

Cuando el backend falla y devuelve mÃ¡s informaciÃ³n de la debida.

### EvoluciÃ³n histÃ³rica del OWASP

2017 2021 2025
 --------------------------- ------------------------------- ---------------------------------------------------------------
SQL Injection dominaba Access Control sube al A01 Cadena de suministro entra como nueva XSS muy presente DiseÃ±o inseguro nuevo IA impulsa el descubrimiento de vulnerabilidades en librerÃ­as Configuraciones inseguras Integridad del software nueva Shift hacia lo que genera el desarrollo masivo asistido por IA

**ConclusiÃ³n del profesor:** el OWASP Top 10 no es una lista arbitraria.

Refleja cÃ³mo avanza la tecnologÃ­a.

Que la cadena de suministro sea nueva en 2025 y no existÃ­a en 2021 tiene todo el sentido dado el boom del desarrollo asistido por IA (vibe coding, Copilot, Claude Code...).

## 4.

MetodologÃ­a de auditorÃ­a web --- Las fases

Castillo presenta su visiÃ³n de la metodologÃ­a de auditorÃ­a web, que amplÃ­a ligeramente la metodologÃ­a general vista hasta ahora:

## 1.

Reconocimiento y enumeraciÃ³n (subdominios, tecnologÃ­as, versiones, superficie de ataque) â†“ 2.

AnÃ¡lisis de vulnerabilidades (mapear quÃ© aplica segÃºn el stack tecnolÃ³gico: Â¿hay login? â†’ probar autenticaciÃ³n Â¿hay buscador? â†’ probar SQLi Â¿hay subida de ficheros? â†’ probar file upload Â¿hay parÃ¡metros de ID? â†’ probar IDOR) â†“ 3.

ExplotaciÃ³n (si no se explota, no hay vulnerabilidad â€” solo indicio) â†“ 4.

Post-explotaciÃ³n y escalada (se ve muy poco en auditorÃ­as web reales â€” RCE en producciÃ³n es raro y valioso) â†“ 5.

DocumentaciÃ³n e informe (lo que no se documenta, no existe)

> [!important] ### El principio clave: si no se explota, no hay vulnerabilidad

Una sospecha sin demostraciÃ³n es **hallazgo informativo** (sin puntuaciÃ³n CVSS).

Solo se reporta como vulnerabilidad real lo que se ha podido explotar y demostrar con evidencias.

**Las** "**pruebas realizadas**" en un informe son tan importantes como las vulnerabilidades encontradas.

Si se ha probado SQLi en todos los formularios y no hay ninguna, hay que documentarlo.

Da valor al cliente: demuestra que se ha revisado, no que no se ha hecho nada.

### CVSS --- PuntuaciÃ³n de vulnerabilidades

**CVSS** (*Common Vulnerability Scoring System*) es la mÃ©trica estÃ¡ndar para puntuar la criticidad de cada vulnerabilidad (de 0 a 10).

Los parÃ¡metros incluyen: impacto en confidencialidad, integridad, disponibilidad, si se necesita autenticaciÃ³n, si el vector de ataque es remoto, etc.

- **CrÃ­tica (9-10):** RCE sin autenticaciÃ³n, SQLi con acceso total a BD
- **Alta (7-8.9):** SQLi con datos sensibles, IDOR con datos de clientes
- **Media (4-7):** XSS reflejado, fuerza bruta sin bloqueo
- **Baja (0.1-3.9):** cabeceras de seguridad faltantes, verbose errors
- **Informativa (0):** indicios sin explotaciÃ³n confirmada

**Consejo de Castillo:** no obsesionarse con la puntuaciÃ³n.

Hay clientes que discuten la nota en vez de arreglar las 10 vulnerabilidades encontradas.

El valor estÃ¡ en entender y saber defender el informe tÃ©cnicamente.

## 5.

Burp Suite --- Repaso desde cero

### QuÃ© es Burp Suite

**Burp Suite** es un **proxy** --- un intermediario que se sitÃºa entre el navegador y el servidor web.

Todo el trÃ¡fico HTTP/HTTPS pasa por Ã©l antes de llegar al destino.

**MetÃ¡fora del profesor:** imagina tres calles para ir del punto A al punto B.

Si te colocas tÃº en el medio de una de esas calles, solo los que vayan por esa calle pasan por ti.

Burp es esa calle --- el navegador tiene que estar configurado para ir por ella.

El puerto por defecto de Burp: **127.0.0.1:8080**

### Las dos formas de usar Burp

**OpciÃ³n 1 --- Open Browser de Burp:** Burp incluye un navegador Chromium preconfigurado.

Al abrirlo desde Burp â†’ ya tiene el proxy configurado automÃ¡ticamente.

Es la opciÃ³n mÃ¡s simple y la que menos falla.

**OpciÃ³n 2 --- Navegador propio + FoxyProxy:** Configurar el proxy del navegador (Firefox/Chrome) para apuntar a `127.0.0.1:8080`.

FoxyProxy permite hacer esto con un clic sin tocar la configuraciÃ³n del sistema.

**Error mÃ¡s frecuente:** tener FoxyProxy activo pero el Intercept de Burp desactivado, o viceversa.

### Los mÃ³dulos principales de Burp

**Proxy --- el nÃºcleo:** - **Intercept ON:** captura y pausa cada peticiÃ³n.

Se puede ver y modificar cualquier parÃ¡metro antes de enviarla. - **Intercept OFF:** las peticiones pasan automÃ¡ticamente pero quedan registradas en **HTTP History**.

Ãštil para navegar con normalidad y revisar despuÃ©s.

**Intruder:** Permite iterar (fuerza bruta) sobre uno o mÃ¡s parÃ¡metros de una peticiÃ³n interceptada.

Si se intercepta un login con `username=castillo&password=evolve2026`, se puede mandar al Intruder y sustituir el campo de usuario por una lista completa.

Los modos mÃ¡s usados: **Sniper** (un parÃ¡metro) y **Cluster Bomb** (varios parÃ¡metros en combinaciÃ³n).

**Repeater:** Permite reenviar una misma peticiÃ³n modificada manualmente tantas veces como se quiera, sin necesidad de interceptar en tiempo real.

Muy Ãºtil para probar variaciones de un payload.

### Burp y el protocolo HTTP

Burp trabaja con peticiones HTTP/HTTPS de todos los mÃ©todos: GET, POST, PUT, DELETE, PATCH, etc.

Al interceptar se puede ver y modificar: - ParÃ¡metros de la URL (`?id=1`) - Cabeceras HTTP (User-Agent, Cookie, Authorization...) - Cuerpo de la peticiÃ³n POST (formularios, JSON, XML) - Cookies de sesiÃ³n

**Inspector del navegador vs.

Burp:** el Inspector (DevTools â†’ Network) tambiÃ©n muestra las peticiones, pero de forma desordenada y difÃ­cil de modificar en tiempo real.

Burp lo organiza y facilita la modificaciÃ³n.

### Burp Community vs.

Pro

- **Community (gratuita):** todas las funciones bÃ¡sicas (proxy, repeater, intruder bÃ¡sico).

Solo proyectos temporales (no guarda el estado entre sesiones).
- **Pro (\~500â‚¬/aÃ±o):** proyectos persistentes, Intruder sin throttling, escÃ¡ner activo de vulnerabilidades.

Se suele facilitar en empresas.

PortSwigger tambiÃ©n tiene licencias educativas.

## 6.

PortSwigger Web Security Academy

**PortSwigger** (portswigger.net/web-security) es la plataforma de aprendizaje de los creadores de Burp Suite.

Tiene laboratorios gratuitos para cada tipo de vulnerabilidad web: SQLi, XSS, IDOR, SSRF, XXE, CSRF, Path Traversal, File Upload, y muchos mÃ¡s.

â†’

La dinÃ¡mica del mÃ³dulo serÃ¡: para cada vulnerabilidad â†’ ver la teorÃ­a en PortSwigger â†’ resolver los laboratorios correspondientes.

## 7.

ProducciÃ³n vs.

PreproducciÃ³n --- Una distinciÃ³n crÃ­tica

Antes de atacar cualquier cosa, siempre hay que saber si se estÃ¡ en un entorno de producciÃ³n o de pruebas:

ProducciÃ³n PreproducciÃ³n
 ---------------------- ------------------------------------- --------------------------------
 **Usuarios reales** SÃ­ No
 **Datos reales** SÃ­ No (o anonimizados)
 **Impacto de caÃ­da** Clientes sin servicio Sin impacto
 **Fuerza bruta** Peligroso (puede tirar el servicio) Permitida en general
 **SQLMap** Pedir permiso explÃ­cito Sin restricciones habitualmente

**AnÃ©cdota real:** en el simulacro del eJPT, varios alumnos lanzaron fuerza bruta a mÃ¡xima velocidad y tumbaron los servicios del laboratorio.

En producciÃ³n, eso hubiera generado una llamada del cliente a las 2 de la noche y un problema contractual serio.

**Regla:** toda herramienta agresiva (SQLMap, fuerza bruta masiva, DoS) requiere confirmaciÃ³n explÃ­cita del cliente sobre el entorno y el alcance (*scope*).

Lo que no estÃ¡ en el scope, no se toca.

## 8.

PrÃ³ximas sesiones del mÃ³dulo web

- Recorrer los laboratorios de PortSwigger vulnerabilidad por vulnerabilidad.
- HackerLab mÃ¡quina 1 (mÃ¡quina web sencilla, descarga disponible en Google Drive).
- Aprendizaje del concepto: cÃ³mo analizar una peticiÃ³n HTTP, quÃ© parÃ¡metros atacar, quÃ© herramientas usar en cada contexto.
- Al finalizar el mÃ³dulo web: prÃ¡ctica 2 del mÃ¡ster (auditorÃ­a real de una web en Internet).

## 9.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
-------------------------------------------- ---------------------------------------------------------------------------------------------------------------------
*OSWAT / OSWARD / OSWAS top teng* **OWASP Top 10** (*Open Web Application Security Project*) -- estÃ¡ndar de las 10 vulnerabilidades web mÃ¡s frecuentes
 *Port Swinger / por Swiger / por sweiger* **PortSwigger** -- empresa creadora de Burp Suite y de la plataforma de laboratorios web
 *Bursuite / Boursuite / Burns Suite* **Burp Suite** -- proxy de interceptaciÃ³n para auditorÃ­as web
 *Fashei Proxy / Foxy Proxi* **FoxyProxy** -- extensiÃ³n del navegador para activar/desactivar el proxy
 *Man in the middle* **MITM** (*Man In The Middle*) -- interceptaciÃ³n del trÃ¡fico entre dos partes
 *los CuSS / el Cusss* **CVSS** (*Common Vulnerability Scoring System*) -- mÃ©trica de criticidad de vulnerabilidades (0-10)
 *Unido / IDOR* **IDOR** (*Insecure Direct Object Reference*) -- acceso a datos de otros usuarios cambiando un ID en la URL
 *SSRF / Serf* **SSRF** (*Server-Side Request Forgery*) -- fuerza al servidor a hacer peticiones a recursos internos
 *XSS / XXS / cross de scripting* **XSS** (*Cross-Site Scripting*) -- inyecciÃ³n de JavaScript en pÃ¡ginas web
 *SQL InyecciÃ³n / second injection* **SQL Injection (SQLi)** -- inyecciÃ³n de cÃ³digo en consultas SQL
 *supply chain / la cadena de suministro* **Cadena de suministro de software** -- vulnerabilidades en librerÃ­as y dependencias de terceros
 *la suppressline chain* **Supply chain** -- tÃ©rmino en inglÃ©s para cadena de suministro
 *by coding / byte coding* **Vibe coding** / **AI-assisted development** -- desarrollo masivo de cÃ³digo asistido por IA
 *el scope / el alcance* **Scope** -- alcance definido de la auditorÃ­a (quÃ© dominios/IPs estÃ¡n autorizados a atacar)
 *pimeline / Pimeline* **Pipeline** -- flujo automatizado de CI/CD (integraciÃ³n y despliegue continuo)
 *HackerLab / hacker la* **HackerLab** -- plataforma de mÃ¡quinas vulnerables para prÃ¡ctica web
 *repetiter / repeter* **Repeater** -- mÃ³dulo de Burp Suite para reenviar peticiones manualmente
 *el intruder / el inchruder* **Intruder** -- mÃ³dulo de Burp Suite para fuerza bruta en parÃ¡metros de peticiones
 *Claudia / Claudio / Claude / Claude Code* **Claude** (Anthropic) -- IA usada por los alumnos para resolver dudas durante la clase
 *las ISOs / la norma / normativa* **ISO 27001 / normativa de ciberseguridad** -- estÃ¡ndares que obligan a las empresas a auditar su seguridad
 *CISO / el CEO de ciber* **CISO** (*Chief Information Security Officer*) -- responsable de ciberseguridad de una empresa

â†’

â†’

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’

â†’
â†’
â†’
