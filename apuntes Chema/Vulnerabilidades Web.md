| **Campo** | **Detalle** |
| ------------- | -------------------------------------------------------------------- |
| SesiÃ³n | Vulnerabilidades Web â€” OWASP Top 10 2025 + IntroducciÃ³n a Burp Suite |

> â†’
| Instructor | Carlos (Castillo) |
| Fecha | 29/06/2026 |
| Bloque | Inicio del mÃ³dulo de Hacking Web (Red Team) |
| Tipo de clase | Mayoritariamente teÃ³rica + primera prÃ¡ctica con Burp Suite |

| |
|---|
|**INFO**<br><br>Esta sesiÃ³n abre el bloque de **hacking web**, que se extenderÃ¡ aproximadamente **dos meses**. El instructor avisa de que fue una clase con mucha teorÃ­a (metodologÃ­a) y poca prÃ¡ctica, sentando las bases antes de empezar a explotar mÃ¡quinas web.|

# 1. Objetivos de la sesiÃ³n

â€¢Â Â Â Â  Entender quÃ© es el **OWASP Top 10 (versiÃ³n 2025)** y para quÃ© sirve realmente en una auditorÃ­a.

â€¢Â Â Â Â  Conocer de forma general las 10 categorÃ­as de vulnerabilidades web y saber ubicar ejemplos en ellas.

â€¢Â Â Â Â  Introducir **CVSS** como sistema de puntuaciÃ³n de criticidad de las vulnerabilidades.

â€¢Â Â Â Â  Diferenciar la **metodologÃ­a de informe / cliente** de la **metodologÃ­a tÃ©cnica del hacker**.

â€¢Â Â Â Â  Comprender la **metodologÃ­a de auditorÃ­a web** y dÃ³nde encaja el anÃ¡lisis de vulnerabilidades.

â€¢Â Â Â Â  Dar los primeros pasos con **Burp Suite**: quÃ© es un proxy, interceptar peticiones y usar el Repeater.

# 2. OWASP Top 10 (2025)

El **OWASP Top 10** es un estÃ¡ndar que agrupa las **10 categorÃ­as de vulnerabilidades web mÃ¡s frecuentes**. Se construye analizando todos los **CVE** publicados durante los Ãºltimos aÃ±os y clasificÃ¡ndolos por tipo (inyecciÃ³n, criptografÃ­a, etc.).

| |
|---|
|**INFO**<br><br>SegÃºn lo comentado en clase, la versiÃ³n de **2025** se publicÃ³ en **enero de 2026** y sustituye a la de **2021**, con la que se trabajaba anteriormente. Antes de esa, la referencia conocida era la de **2017** (Ã©poca del Â«boomÂ» de SQL Injection, XSS y XXE).|

â†’

**Â¿Para quÃ© sirve realmente?** Para tener un enfoque global y una base metodolÃ³gica comÃºn, sobre todo de cara al **informe** y a la parte burocrÃ¡tica frente al cliente. Demuestra al CISO/CEO que se han revisado las vulnerabilidades mÃ¡s tÃ­picas de los Ãºltimos aÃ±os.

| |
|---|
|**AVISO**<br><br>**No hay que aprenderse el Top 10 de memoria ni obsesionarse con clasificar.** El instructor insiste: en una auditorÃ­a real, una vulnerabilidad encadenada puede tocar varias categorÃ­as a la vez y es difÃ­cil encasillarla. Hoy en dÃ­a una IA puede asignar la categorÃ­a (A06, A07...) al instante. El valor humano estÃ¡ en **entender** la vulnerabilidad y **defender el informe**, no en memorizar etiquetas.|

## 2.1. Las 10 categorÃ­as (resumen de clase)

|**CÃ³digo**|**CategorÃ­a**|**DescripciÃ³n vista en clase**|
|---|---|---|
|A01|Control de acceso defectuoso (Broken Access Control)|Acceder a datos de otros usuarios. Caso tÃ­pico: IDOR (cambiar id=4 â†’ id=5 en la URL sin control de sesiÃ³n). Muy frecuente en auditorÃ­a diaria.|
|A02|ConfiguraciÃ³n de seguridad incorrecta (Security Misconfiguration)|Credenciales por defecto, paneles expuestos, cabeceras inseguras, mensajes de error que filtran rutas del sistema. Suele deberse al error humano.|
|A03|Fallos en la cadena de suministro de software|CategorÃ­a nueva. LibrerÃ­as y dependencias vulnerables o comprometidas (backdoors). Gran preocupaciÃ³n actual de los CISO por el desarrollo masivo con IA.|
|A04|Fallos criptogrÃ¡ficos|Cifrados dÃ©biles, claves mal gestionadas, TLS mal configurado.|
|A05|DiseÃ±o inseguro|LÃ³gica de negocio, subidas de archivos sin validaciÃ³n (p. ej. permitir subir un PHP cuando solo se deberÃ­a poder subir un PDF), falta de lÃ­mites.|
|A06|InyecciÃ³n|SQL Injection, XSS, inyecciÃ³n de comandos, LDAP, NoSQL. Sigue muy alto en el ranking.|
|A07|Fallos de autenticaciÃ³n|EnumeraciÃ³n de usuarios, contraseÃ±as dÃ©biles, ausencia de bloqueo / rate limit. Permite fuerza bruta cuando no hay protecciÃ³n.|
|A08|Fallos en la integridad del software o de los datos|Pipelines (CI/CD) sin verificaciÃ³n de integridad. Relacionado con el desarrollo masivo de software y la gestiÃ³n de datos.|
|A09|Fallos de registro y monitorizaciÃ³n (logging)|Falta de logs y alertas. Impide hacer un forense posterior (analogÃ­a: pedir a la policÃ­a que investigue cuando no habÃ­a cÃ¡maras instaladas).|
|A10|Mala gestiÃ³n de situaciones excepcionales|Manejo de errores que filtra informaciÃ³n de mÃ¡s. Muy ligado a A02.|
|**RIESGO / LAB**<br><br>**Ejercicio mental de la sesiÃ³n:** si una aplicaciÃ³n permite **fuerza bruta porque no bloquea** las peticiones, Â¿en quÃ© categorÃ­a cae? No es A01 (control de acceso) â†’ es **A07, fallo de autenticaciÃ³n**. La ausencia de firewall/bloqueo es lo que lo habilita, pero la vulnerabilidad reportada es la enumeraciÃ³n de usuarios / fuerza bruta.| | |
|**INFO**<br><br>**Nota:** la mÃ¡quina que se usarÃ¡ en prÃ¡cticas prÃ³ximas es una mÃ¡quina de **WordPress**, donde plugins y dependencias inseguras (relacionado con A03/A05) son especialmente relevantes.| | |

# 3. CVSS, CVE y categorizaciÃ³n

El **CVSS (Common Vulnerability Scoring System)** es la **nota** que se asigna a cada vulnerabilidad. Se calcula con el **CVSS Calculator**, donde se rellenan mÃ©tricas (por ejemplo, impacto en confidencialidad: High, etc.). En el ejemplo de clase, con cierto contexto, una vulnerabilidad daba una puntuaciÃ³n de **6,8**.

|**Concepto**|**QuÃ© es**|
|---|---|
|CVE|Identificador Ãºnico de una vulnerabilidad concreta y pÃºblica.|
|CVSS|Sistema de puntuaciÃ³n que asigna una nota (criticidad) a la vulnerabilidad.|
|Niveles|CrÃ­tico / Alto / Medio / Bajo segÃºn la puntuaciÃ³n.|
|Informativa|Apartado SIN puntuaciÃ³n. Se usa cuando hay indicios de algo vulnerable pero no se ha explotado.|
|**INFO**<br><br>**Nota:** el CWE (clasificaciÃ³n de tipos de debilidad) y el detalle del cÃ¡lculo CVSS se trabajarÃ¡n mÃ¡s adelante, junto con un mini-informe y un informe real anonimizado. El instructor no entrÃ³ en profundidad porque es mÃ¡s "parte de informe".| |
|**RIESGO / LAB**<br><br>**Principio clave:** "Si yo no exploto esa vulnerabilidad, no hay vulnerabilidad." Solo se categoriza como crÃ­tico/alto/medio/bajo lo que se ha **explotado**. Si solo hay indicios â†’ se reporta como informativa.| |

# 4. Dos metodologÃ­as que NO hay que confundir

El instructor remarca con fuerza que conviene separar mentalmente dos cosas:

|**MetodologÃ­a de informe / cliente**|**MetodologÃ­a tÃ©cnica del hacker**|
|---|---|
|Es lo que paga y espera el cliente.|Es lo que el auditor hace realmente por detrÃ¡s.|
|Se basa en el OWASP Top 10 y la categorizaciÃ³n.|EnumeraciÃ³n â†’ anÃ¡lisis â†’ explotaciÃ³n encadenada.|
|Reporta solo el QUÃ‰ (la vulnerabilidad concreta).|Prueba muchas cosas, encadena fallos, descarta caminos.|
|No es un write-up paso a paso.|SÃ­ puede ser exploratoria y desordenada.|
|**AVISO**<br><br>Una auditorÃ­a real **no es un write-up** del estilo "hice nmap, luego curl, luego tal". En el informe se reporta la **vulnerabilidad concreta** (por ejemplo: enumeraciÃ³n de usuario â†’ A07), no toda la cadena de comandos.| |

## 4.1. Pruebas realizadas

Apartado del informe donde se documenta **lo que se ha probado aunque no haya dado resultado** (p. ej. "probÃ© un SQLi en el buscador X, metÃ­ la comilla y estaba sanitizado"). Da valor al cliente y demuestra el trabajo realizado.

| |
|---|
|**RIESGO / LAB**<br><br>**Cuidado con SQLMAP:** si el cliente pide no hacer muchas peticiones y se adjunta una captura de **SQLMAP** (que lanza muchÃ­simas peticiones) como prueba realizada, queda muy mal. Hay que saber controlar el ruido y respetar el alcance acordado.|

# 5. MetodologÃ­a de auditorÃ­a web

La metodologÃ­a es la de siempre, pero con un paso intermedio importante: el **anÃ¡lisis de vulnerabilidades**, donde se mapea el stack tecnolÃ³gico contra posibles CVE / exploits antes de explotar.

| |
|---|
|Reconocimiento y enumeraciÃ³n|
|**â†“**|
|AnÃ¡lisis de vulnerabilidades (mapeo del stack â†’ CVE / exploits)|
|**â†“**|
|ExplotaciÃ³n|
|**â†“**|
|Post-explotaciÃ³n y escalada (poco peso en web)|
|**â†“**|
|DocumentaciÃ³n e informe|

Durante el **anÃ¡lisis de vulnerabilidades** el auditor se hace su propio mapa mental: Â¿hay control de acceso? Â¿puedo inyectar en alguna parte? Â¿los componentes estÃ¡n desactualizados? Si no hay login, quizÃ¡ no interesa centrarse en autenticaciÃ³n; el contexto manda.

## 5.1. Web real vs mÃ¡quina de HTB

Una aplicaciÃ³n web real **no es como una mÃ¡quina de Hack The Box**. Aparecen subdominios, scope/alcance, entornos de producciÃ³n vs preproducciÃ³n y muchÃ­sima informaciÃ³n y ruido que en HTB no existe.

|**Aspecto**|**MÃ¡quina HTB / VulnHub**|**AuditorÃ­a web real**|
|---|---|---|
|InformaciÃ³n expuesta|La justa y necesaria.|MuchÃ­sima: subdominios, datos, configuraciones.|
|Permiso|Todo estÃ¡ habilitado para hackear.|Hay un scope y reglas que respetar.|
|Impacto de un IDOR|Suele dar igual (datos ficticios).|CrÃ­tico: ver datos, tarjetas, info de clientes reales.|
|DenegaciÃ³n de servicio|Te reinician el lab.|Puede tirar un servicio real â†’ problema grave con el cliente.|
|**RIESGO / LAB**<br><br>**Scope y ruido importan.** Aunque un servicio bloquee la fuerza bruta, con Burp Suite se puede **simular la secuencia mÃ¡s lenta** (tardando horas en vez de minutos) imitando a una persona haciendo clic. Pero hay que valorar siempre si la denegaciÃ³n de servicio entra o no en el alcance: cada cliente es un mundo.| | |
|**INFO**<br><br>El puesto al que mÃ¡s probablemente se accede empezando es **auditorÃ­a web** (equipos pool). Por eso este bloque recibirÃ¡ mucha caÃ±a. Saber **reflejar el trabajo en el informe** vale tanto como saber hackear.| | |

# 6. IntroducciÃ³n a Burp Suite

**Burp Suite es un proxy.** ActÃºa como **man in the middle** entre el navegador y el servidor: intercepta las peticiones antes de que lleguen al servidor, permite **verlas, modificarlas y decidir si pasan o no**. Funciona con cualquier mÃ©todo (GET, POST, PUT...).

| |
|---|
|Navegador (tÃº)|
|**â†“**|
|Proxy de Burp â€” 127.0.0.1:8080 (intercepta / modifica)|
|**â†“**|
|Servidor web|

| |
|---|
|**INFO**<br><br>AnalogÃ­a de clase: el proxy es una "calle" por la que debe viajar el trÃ¡fico (puerto **8080**). Si el navegador no va por esa calle, Burp no captura nada. El navegador tiene que apuntar al proxy de Burp para que la interceptaciÃ³n funcione.|

## 6.1. PestaÃ±as principales

|**PestaÃ±a**|**Para quÃ©**|
|---|---|
|Proxy|NÃºcleo de Burp. Intercepta el trÃ¡fico HTTP/HTTPS (Intercept ON/OFF, Forward).|
|Repeater|Repite y modifica una peticiÃ³n concreta tantas veces como se quiera para analizarla.|
|Intruder|Automatiza/itera valores de una peticiÃ³n (p. ej. fuerza bruta de credenciales en un login).|
|Target / Dashboard|Vista general del objetivo y la actividad.|
|Sequencer / Collaborator|Funciones avanzadas (se verÃ¡n mÃ¡s adelante).|
|**INFO**<br><br>Para esta sesiÃ³n basta con dominar **Proxy** y entender un poco el **Repeater**. Son las dos que mÃ¡s se usan.| |

## 6.2. Flujo bÃ¡sico de trabajo

1.Â Â  Activar **Intercept ON** en la pestaÃ±a Proxy.

2.Â Â  Navegar en la web y dejar que Burp capture las peticiones.

3.Â Â  Ir haciendo **Forward** para dejar pasar las que no interesan.

4.Â Â  Cuando aparece una peticiÃ³n interesante (un login, una API interna...), **clic derecho â†’ Send to Repeater**.

5.Â Â  En el **Repeater**, pulsar **Send** y analizar/modificar parÃ¡metros, cabeceras y respuestas las veces que haga falta.

En el ejemplo de clase, al interceptar el inicio de sesiÃ³n de una web se veÃ­an **muchas peticiones** (login, una internal API, recursos de terceros como Circle/Clarity). Enviando la peticiÃ³n de login al Repeater se podÃ­a inspeccionar informaciÃ³n como un Android Story ID o una public key, descubriendo asÃ­ la tecnologÃ­a usada por detrÃ¡s.

## 6.3. Dos formas de enrutar el trÃ¡fico hacia Burp

|**OpciÃ³n**|**DescripciÃ³n**|**Ventaja / inconveniente**|
|---|---|---|
|Open Browser (navegador interno de Burp)|Navegador que ya viene preconfigurado para pasar por el proxy. Solo hay que preocuparse de Intercept ON/OFF.|Recomendado al empezar: menos ruido, sin lÃ­os de configuraciÃ³n.|
|FoxyProxy (Firefox/Chrome propio)|ExtensiÃ³n que mete tu navegador en el proxy de Burp (127.0.0.1:8080).|MÃ¡s rÃ¡pido para gente experta, pero mucho ruido (pestaÃ±as, recursos de terceros) y requiere activarlo manualmente.|
|**AVISO**<br><br>**Ruido:** trabajar en el navegador habitual con muchas pestaÃ±as abiertas genera muchÃ­simo trÃ¡fico irrelevante (analytics, redes sociales, etc.). Por eso al empezar conviene el **Open Browser** o un navegador limpio dedicado.| | |

## 6.4. ConfiguraciÃ³n de FoxyProxy (visto en clase)

Si se usa FoxyProxy en lugar del Open Browser, la configuraciÃ³n del proxy es:

| |
|---|
|TÃ­tuloÂ Â Â  : Burp<br><br>TipoÂ Â Â Â Â  : HTTP<br><br>Host / IP : 127.0.0.1<br><br>PuertoÂ Â Â  : 8080|

Con FoxyProxy activado, todo el navegador pasa por Burp. Para desactivarlo se selecciona **Disable** y se vuelve a navegar normal.

## 6.5. Certificado de Burp

Al navegar con un navegador propio (no el Open Browser), el navegador **no detecta el proxy de Burp como seguro**. Hay que instalar el **certificado de Burp (PortSwigger)** como certificado de confianza.

Con Burp y el proxy **encendidos**, se accede desde el navegador a:

| |
|---|
|http://burpsuite/<br><br>(tambiÃ©n vale poner simplemente: burpsuite/ )|

Desde ahÃ­ se descarga el **CA Certificate** y se importa en la gestiÃ³n de certificados del navegador (Chrome: Administrar certificados â†’ instalados por ti â†’ importar como certificado de confianza). AparecerÃ¡ como **PortSwigger**, indicando al navegador que el proxy es seguro.

| |
|---|
|**INFO**<br><br>**Nota sobre entornos HTB:** al trabajar con mÃ¡quinas de HTB se estÃ¡ conectado por VPN dentro de Kali, en una red interna **sin acceso a internet**, por lo que el ruido de terceros desaparece. Recordatorio de clase: la VPN debe usarse desde Kali, no desde Windows.|

# 7. Herramientas utilizadas en la sesiÃ³n

|**Herramienta**|**Objetivo**|**Fase de auditorÃ­a**|**Comando o uso visto**|**Nivel**|**Notas**|
|---|---|---|---|---|---|
|Burp Suite (Proxy/Repeater/Intruder)|Interceptar y modificar trÃ¡fico HTTP/HTTPS|Reconocimiento, anÃ¡lisis y explotaciÃ³n web|Intercept ON/OFF, Forward, Send to Repeater|Introducida|Proxy man-in-the-middle en 127.0.0.1:8080. Foco en Proxy y Repeater.|
|FoxyProxy|Enrutar el navegador hacia el proxy de Burp|ConfiguraciÃ³n previa|HTTP Â· 127.0.0.1 Â· 8080|Introducida|Alternativa al Open Browser interno de Burp.|
|CVSS Calculator|Puntuar la criticidad de una vulnerabilidad|AnÃ¡lisis / informe|SelecciÃ³n de mÃ©tricas â†’ nota (ej. 6,8)|Mencionada|Se profundizarÃ¡ junto al informe.|
|Nmap|Detectar puertos y servicios|EnumeraciÃ³n|Repaso anunciado para prÃ³xima clase|Recurrente|Se aplicarÃ¡ ahora al contexto web.|
|Curl|InteracciÃ³n manual con servicios web|EnumeraciÃ³n web|Mencionado para prÃ³xima clase|Mencionada|Se verÃ¡ con Nmap en el repaso web.|
|SQLMAP|Automatizar SQL Injection|ExplotaciÃ³n|Mencionado como ejemplo de ruido|Mencionada|Cuidado: genera muchas peticiones; respetar el scope.|
|Hydra|Fuerza bruta de credenciales|ExplotaciÃ³n / autenticaciÃ³n|Citado como alternativa al Intruder|Practicada|Comparado con el Intruder de Burp.|
|**INFO**<br><br>**Nota:** Nmap, Curl y SQLMAP solo se **mencionan** en esta sesiÃ³n (se repasarÃ¡n o aplicarÃ¡n en la siguiente clase). No se desarrollan en profundidad en el material proporcionado.| | | | | |

# 8. Riesgos, errores comunes y buenas prÃ¡cticas

| |
|---|
|**RIESGO / LAB**<br><br>Lanzar fuerza bruta a lo loco contra un servicio (como pasÃ³ en el examen final tipo eJPT) puede **tirar el laboratorio o el servicio del cliente**. En real esto significa llamadas a medianoche y problemas serios.|
|**AVISO**<br><br>Adjuntar capturas de **SQLMAP** como "prueba realizada" cuando el cliente pidiÃ³ pocas peticiones delata que no se hizo el SQLi manual y rompe el acuerdo de ruido.|
|**AVISO**<br><br>Trabajar en el navegador personal con muchas pestaÃ±as mete **ruido** que dificulta identificar la peticiÃ³n relevante en Burp.|
|**BUENA PRÃCTICA**<br><br>Usar el **Open Browser** de Burp (o un navegador limpio dedicado) al empezar, mantener **Intercept** controlado y enviar al **Repeater** solo lo que interesa.|
|**BUENA PRÃCTICA**<br><br>Separar siempre la **metodologÃ­a de informe** (lo que ve el cliente) de la **metodologÃ­a tÃ©cnica**, y documentar bien: "lo que no se documenta, no existe".|
|**BUENA PRÃCTICA**<br><br>Antes de atacar, hacer **anÃ¡lisis de vulnerabilidades**: mapear el stack y decidir quÃ© tiene sentido probar segÃºn el contexto (no probar autenticaciÃ³n si no hay login, etc.).|

# 9. ConexiÃ³n con sesiones anteriores

Esta sesiÃ³n retoma el enfoque **Red Team** tras un parÃ©ntesis de Blue Team y conecta directamente con lo ya trabajado:

â€¢Â Â Â Â  **Nmap** y **fuzzing**, vistos en sesiones previas, ahora se aplicarÃ¡n al contexto **web** (se anuncia un repaso de Nmap + Curl).

â€¢Â Â Â Â  La **fuerza bruta** ya practicada con **Hydra** se relaciona ahora con el **Intruder** de Burp: misma idea (iterar credenciales) desde un proxy web.

â€¢Â Â Â Â  La metodologÃ­a **enumeraciÃ³n â†’ explotaciÃ³n â†’ escalada** practicada en HTB (Starting Point, Mr. Robot...) se reordena para web aÃ±adiendo el paso de **anÃ¡lisis de vulnerabilidades**.

â€¢Â Â Â Â  La **SQL Injection** introducida en Metasploitable 2 (DVWA) reaparece como categorÃ­a OWASP (A06) y como ejemplo de "prueba realizada" en el informe.

â€¢Â Â Â Â  Los **plugins de WordPress** (relevantes en la cadena de suministro, A03) enlazan con la prÃ³xima mÃ¡quina de prÃ¡cticas, que serÃ¡ de WordPress.

# 10. Resumen final

SesiÃ³n de apertura del mÃ³dulo de **hacking web**, centrada en la **metodologÃ­a**. El **OWASP Top 10 2025** sirve como marco comÃºn para el informe, pero lo importante es **entender** las vulnerabilidades, no memorizar categorÃ­as. El **CVSS** puntÃºa la criticidad y solo se categoriza lo que se **explota** (lo demÃ¡s, informativa).

Hay que distinguir la **metodologÃ­a de informe** (lo que paga el cliente) de la **metodologÃ­a del hacker**, y recordar que una web real no es una mÃ¡quina de HTB: hay scope, ruido y riesgo de denegaciÃ³n de servicio. La metodologÃ­a web aÃ±ade el paso de **anÃ¡lisis de vulnerabilidades** antes de explotar.

En la parte prÃ¡ctica se introdujo **Burp Suite** como **proxy man-in-the-middle**: interceptar con el **Proxy**, dejar pasar con **Forward**, enviar al **Repeater** lo interesante e iterar con el **Intruder**. Dos formas de enrutar el trÃ¡fico (**Open Browser** vs **FoxyProxy**) y la instalaciÃ³n del **certificado de PortSwigger** para navegadores propios.

# 11. Checklist de repaso

â€¢Â Â Â Â  Â¿SÃ© explicar quÃ© es el OWASP Top 10 y para quÃ© sirve realmente?

â€¢Â Â Â Â  Â¿Puedo poner un ejemplo de A01 (IDOR), A02 (misconfiguration) y A07 (autenticaciÃ³n)?

â€¢Â Â Â Â  Â¿Entiendo quÃ© es CVSS y la diferencia entre crÃ­tico/alto/medio/bajo e informativa?

â€¢Â Â Â Â  Â¿Distingo la metodologÃ­a de informe de la metodologÃ­a tÃ©cnica del hacker?

â€¢Â Â Â Â  Â¿SÃ© por quÃ© una web real no es como una mÃ¡quina de HTB (scope, ruido, DoS)?

â€¢Â Â Â Â  Â¿SÃ© quÃ© es Burp Suite y por quÃ© es un proxy / man in the middle?

â€¢Â Â Â Â  Â¿SÃ© interceptar, hacer Forward y enviar una peticiÃ³n al Repeater?

â€¢Â Â Â Â  Â¿Entiendo la diferencia entre Open Browser y FoxyProxy y sÃ© configurar el proxy (127.0.0.1:8080)?

â€¢Â Â Â Â  Â¿SÃ© instalar el certificado de PortSwigger desde http://burpsuite/?

# 12. ActualizaciÃ³n del registro de herramientas

Cambios y novedades tras esta sesiÃ³n (para copiar a la base de conocimiento del proyecto):

|**Herramienta**|**Nivel anterior**|**Nivel tras la sesiÃ³n**|**Motivo**|
|---|---|---|---|
|Burp Suite (Proxy/Repeater)|Practicada (Intruder)|Practicada|Se explica de cero el concepto de proxy, Intercept/Forward y Repeater. El Intruder ya se habÃ­a usado en Mr. Robot.|
|FoxyProxy|â€”|Introducida|Nueva: configuraciÃ³n HTTP 127.0.0.1:8080 para enrutar el navegador hacia Burp.|
|CVSS Calculator|â€”|Mencionada|Nueva referencia: puntuaciÃ³n de criticidad; se profundizarÃ¡ con el informe.|
|Curl|â€”|Mencionada|Anunciada para el repaso web junto a Nmap.|
|SQLMAP|â€”|Mencionada|Citada como ejemplo de herramienta ruidosa a usar con criterio.|

â†’

| |
|---|
|**INFO**<br><br>**PrÃ³ximos temas anunciados:** repaso de **Nmap + Curl** aplicados a web, prÃ¡ctica con una **mÃ¡quina de WordPress**, y desarrollo progresivo de la metodologÃ­a web (interpretaciÃ³n de peticiones, tipos de vulnerabilidades, mini-informe e informe real anonimizado).|

â†’

â†’

â†’
â†’
â†’
