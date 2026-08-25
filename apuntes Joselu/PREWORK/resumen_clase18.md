> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 18**
> **MÃ³dulo:** PREWORK
> **Tema:** Clase 18
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 18. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

| Resumen â€“ Clase 18: Diccionarios, Credenciales y Ataques de Fuerza Bruta MÃ¡ster de Ciberseguridad e Inteligencia Artificial â€“ Evolve Academy 1. IntroducciÃ³n Esta sesiÃ³n cubre cinco bloques interrelacionados: el concepto y uso de los diccionarios en pentesting, los ataques de fuerza bruta, los mecanismos de autenticaciÃ³n y el concepto de credenciales, los gestores de contraseÃ±as y, finalmente, las principales colecciones de diccionarios y la herramienta de generaciÃ³n personalizada CUPP. 2. Ataques de fuerza bruta Un ataque de fuerza bruta | consiste en probar automÃ¡ticamente todas las combinaciones posibles de caracteres para encontrar una contraseÃ±a. La herramienta itera carÃ¡cter a carÃ¡cter desde la â€˜aâ€™ minÃºscula hasta la â€˜Zâ€™ mayÃºscula, pasando por todos los caracteres especiales, para cada posiciÃ³n de la contraseÃ±a. Velocidad y capacidad de cÃ³mputo: | - Una tarjeta grÃ¡fica RTX 4090 rompe una contraseÃ±a de 8 caracteres en 40 minutos. - Cuanto mayor sea la longitud y complejidad de la contraseÃ±a, mÃ¡s tiempo computacional se requiere. - La capacidad de cÃ³mputo aumenta con el tiempo: lo que hoy tarda 40 minutos, maÃ±ana tardarÃ¡ menos. CaracterÃ­sticas que debe tener una contraseÃ±a segura: CaracterÃ­stica Detalle Longitud MÃ­nimo 12 caracteres Complejidad MayÃºsculas, minÃºsculas, nÃºmeros y caracteres especiales Unicidad Nunca reutilizar la misma contraseÃ±a en distintos servicios No predecible No usar patrones del tipo â€œNombreEmpresa+AÃ±o+!â€ Por quÃ© la unicidad es crÃ­tica (caso real): | en un congreso de seguridad, un ponente explicÃ³ que usaba un patrÃ³n para sus contraseÃ±as (nombre del servicio + aÃ±o + sÃ­mbolo). Un asistente del pÃºblico encontrÃ³ su correo en Dehashed, dedujo el patrÃ³n y accediÃ³ a sus otras cuentas en tiempo real durante la propia charla. Fuerza bruta vs. diccionario: la fuerza bruta garantiza encontrar la contraseÃ±a (prueba todas las 1 |
|---|---|---|---|

| combinaciones posibles), pero tarda mÃ¡s. El ataque por diccionario es mÃ¡s rÃ¡pido pero solo tiene Ã©xito si la contraseÃ±a estÃ¡ en la lista. 3. VerificaciÃ³n de filtraciones: Have I Been Pwned Have I Been Pwned | (haveibeenpwned.com) es un servicio gratuito que permite comprobar si un correo electrÃ³nico ha sido comprometido en alguna brecha de datos conocida y pÃºblica. Devuelve el nombre del servicio donde se filtrÃ³, la fecha y los tipos de datos expuestos (correo, contraseÃ±a, IP, navegador, etc.). Ejemplos de filtraciones reales del profesor: Town of Salem (juego online, dic. 2018), MyFitnessPal (app de calorÃ­as), Canva, Wattpad. Moraleja: cualquier aplicaciÃ³n sin medidas de seguridad correctamente implementadas puede filtrar las contraseÃ±as de sus usuarios en texto claro. AuditorÃ­as de contraseÃ±as en Active Directory: | cuando se obtiene el fichero ntds.dit del controlador de dominio, se realiza un anÃ¡lisis de la calidad de las contraseÃ±as del dominio completo. Los patrones mÃ¡s frecuentes encontrados son: usuario igual a contraseÃ±a (ej. â€œagomezâ€ â†’ â€œagomezâ€), ciudad + aÃ±o (ej. â€œMadrid24!â€), nombre de la empresa + aÃ±o + sÃ­mbolo (ej. â€œEvolve2024!â€). Esto refleja el bajo nivel de madurez en polÃ­ticas de contraseÃ±as de muchas organizaciones. 4. Mecanismos de autenticaciÃ³n: los tres pilares Los sistemas de verificaciÃ³n de identidad digital se construyen sobre tres pilares: Pilar DescripciÃ³n Ejemplos Algo que yo sÃ© InformaciÃ³n memorizada Usuario + contraseÃ±a, PIN, pregunta de seguridad Algo que yo tengo Dispositivo o token fÃ­sico Token RSA, tarjeta inteligente, mÃ³vil (OTP/TOTP) Algo que yo soy CaracterÃ­sticas biolÃ³gicas Huella dactilar, reconocimiento facial, iris La combinaciÃ³n de dos o mÃ¡s pilares da lugar a la autenticaciÃ³n multifactor (MFA) . Un sistema que combine â€œalgo que sÃ©â€ + â€œalgo que tengoâ€ (ej. contraseÃ±a + cÃ³digo SMS) es exponencialmente mÃ¡s difÃ­cil de comprometer que uno que solo use contraseÃ±a. 5. Gestores de contraseÃ±as Dado que las contraseÃ±as deben ser largas, complejas y Ãºnicas para cada servicio, memorizarlas 2 |
|---|---|---|

| todas es humanamente imposible. Los gestores de contraseÃ±as | resuelven este problema: se accede a todos con una Ãºnica contraseÃ±a maestra . KeePass (soluciÃ³n local) |
|---|---|
- Almacena las contraseÃ±as en un fichero cifrado con extensiÃ³n .kdbx localmente.
- Incluye generador de contraseÃ±as aleatorias configurables en longitud y complejidad.
- FunciÃ³n Auto-Type: rellena automÃ¡ticamente usuario y contraseÃ±a en el portal web con
un atajo de teclado.
- Ventaja: muy seguro; las contraseÃ±as no salen del equipo.
- Desventaja: fichero local sin sincronizaciÃ³n cloud â†’ mÃºltiples versiones del archivo,
inaccesible desde otros dispositivos. LastPass (soluciÃ³n cloud)
- Equivalente cloud de KeePass. Sincroniza contraseÃ±as entre dispositivos.
- Disponible con planes gratuitos, familiares y de empresa.
Vaultwarden / Bitwarden (soluciÃ³n cloud self-hosted)
- El profesor lo usa personalmente en su propio servidor ( pass.omnia.dev).
- Vaultwarden es una implementaciÃ³n open source de Bitwarden que se puede autoalojar.
- Protegido con Cloudflare Tunnels: solo accesible con su cuenta de Google como segundo
factor.
- Ventaja: combina la seguridad del control propio con la comodidad cloud.
| 6. Diccionarios: concepto y tipos Un diccionario (wordlist) es una lista de palabras o cadenas de texto que se usa para optimizar los ataques de fuerza bruta, evitando tener que generar todas las combinaciones posibles desde cero. El objetivo es que la contraseÃ±a objetivo estÃ© en la lista. CuÃ¡ndo usar diccionarios vs. | fuerza bruta pura: | - Diccionario: mÃ¡s rÃ¡pido si la contraseÃ±a es predecible o comÃºn. No garantiza resultado. - Fuerza bruta: garantiza encontrar la contraseÃ±a (si se tiene suficiente tiempo/hardware). MÃ¡s lento. Aplicaciones de los diccionarios mÃ¡s allÃ¡ de contraseÃ±as: | - Fuzzing de subdominios: | probar palabras de una lista como prefijos de un dominio para descubrir subdominios existentes (ej. comidas.omnia.dev ). - Fuzzing de rutas web: | descubrir directorios y archivos ocultos en un servidor web (como vimos con Gobuster/Dirsearch en la clase 17). - Cuanto mÃ¡s ajustado estÃ© el diccionario al contexto del objetivo, mÃ¡s eficiente serÃ¡ el ataque. 3 |
|---|---|---|---|---|---|

7. Principales diccionarios y colecciones RockYou (rockyou.txt)
- Ruta en Kali: /usr/share/wordlists/rockyou.txt
- La wordlist mÃ¡s conocida y utilizada. Fue filtrada en la brecha de la empresa RockYou
(2009) y contiene ~14 millones de contraseÃ±as reales.
- Uso recomendado: exclusivamente para entornos CTF, mÃ¡quinas de laboratorio (Hack
The Box, TryHackMe, VulnHub) porque los creadores de retos la utilizan como referencia.
- No recomendado en auditorÃ­as reales: en el mundo corporativo real las contraseÃ±as
siguen otros patrones y raramente aparecen en esta lista. SecLists
- ColecciÃ³n masiva de wordlists para mÃºltiples propÃ³sitos: credenciales, subdominios,
rutas web, fuzzing de APIs, usuarios comunes, etc.
- Instalable en Kali con apt install seclists o mediante git clone desde GitHub.
- Ruta en Kali: /usr/share/wordlists/
- Contiene, entre otras, las 10.000 contraseÃ±as mÃ¡s comunes ordenadas por frecuencia de
uso real (las primeras: password, 123456, 123456789, qwerty, 111111â€¦).
- TambiÃ©n incluye listas de subdominios tÃ­picos en espaÃ±ol para fuzzing de
infraestructura. Kaonashi
- ColecciÃ³n de diccionarios especializada en cracking de hashes construida a partir del
anÃ¡lisis de miles de millones de contraseÃ±as reales filtradas en brechas de datos.
- Orientada al mundo corporativo real: sus contraseÃ±as siguen los patrones de
comportamiento humano real (empresa+aÃ±o, nombre+sÃ­mbolo, etc.).
- Se usa junto con Hashcat y reglas personalizadas para optimizar la ruptura de hashes
obtenidos en auditorÃ­as internas (ej. del fichero ntds.dit).
- Permite aplicar reglas de transformaciÃ³n: dada una palabra base (ej. â€œEvolveâ€), generar
todas las variantes con aÃ±os del 2012 al 2025 y caracteres especiales, creando una lista derivada muy eficiente. 8. CUPP: generador de diccionarios personalizados CUPP (Common User Password Profiler ) es una herramienta de GitHub que genera una wordlist personalizada a partir de informaciÃ³n OSINT sobre la vÃ­ctima. Inspirada en la serie Mr. Robot (capÃ­tulo donde el protagonista genera un diccionario personalizado a partir de datos del objetivo). InstalaciÃ³n: 4

| git clone https://github.com/Mebus/cupp cd cupp python3 cupp.py -h Uso en modo interactivo ( -i): CUPP pregunta por los datos de la vÃ­ctima que se hayan podido recopilar mediante OSINT (fuentes abiertas: LinkedIn, Instagram, Twitter, etc.): - Nombre y apellidos - Nickname - Fecha de nacimiento - Nombres de pareja, hijos, mascotas - Empresa - Palabras clave relacionadas (hobbies, aficiones) - Si aÃ±adir nÃºmeros aleatorios o caracteres especiales al final Con estos datos genera un fichero .txt con todas las combinaciones posibles derivadas de esa informaciÃ³n, formando un diccionario altamente personalizado y orientado al objetivo concreto. Ejemplo de la sesiÃ³n: | el profesor generÃ³ un diccionario sobre sÃ­ mismo con datos pÃºblicamente disponibles (nombre: Yuba GonzÃ¡lez, nickname: YubarGP, fecha de nacimiento: 17/09/1999, nombre del padre: Roberto, hermana: Aruna, gatos: TizÃ³n, empresa: Cibersia, aficiones: hacker, water poloâ€¦). Por quÃ© es poderoso: | los datos de OSINT permiten construir listas muy ajustadas al comportamiento del objetivo, reduciendo drÃ¡sticamente el espacio de bÃºsqueda frente a un diccionario genÃ©rico. 9. Flujo de trabajo completo con diccionarios en una auditorÃ­a 1.Obtener el hash: desde el fichero ntds.dit del Active Directory (Mimikatz), desde una base de datos web comprometida o desde un formulario de login capturado. 2.Elegir el diccionario adecuado: | RockYou para CTF/laboratorio; Kaonashi o wordlist personalizada (CUPP) para auditorÃ­as corporativas reales. 3.Aplicar reglas de transformaciÃ³n | (Hashcat rules): derivar variantes automÃ¡ticas de las palabras base del diccionario. 4.Lanzar el cracking con Hashcat | (GPU) o John the Ripper (CPU). 5.Obtener la contraseÃ±a en claro | â†’ usarla para pivoting, acceso a mÃ¡s mÃ¡quinas o demostraciÃ³n de impacto en el reporte. 10. Conceptos y tÃ©rminos clave corregidos TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n Half-Iâ€™ve-Been-Pwned Have I Been Pwned | (haveibeenpwned.com) â€“ servicio de comprobaciÃ³n de filtraciones Kipas / KeePass PowerSafe KeePass â€“ gestor de contraseÃ±as local con fichero .kdbx Laspas LastPass â€“ gestor de contraseÃ±as cloud Ball Ward / Valwarden Vaultwarden / Bitwarden | â€“ gestor de contraseÃ±as cloud open source 5 |
|---|---|---|---|---|---|---|---|---|

| TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n KDBX .kdbx â€“ formato de fichero cifrado de KeePass Open Pass Word in Horizon Password Generator | â€“ generador de contraseÃ±as integrado en KeePass Perform Auto Type Auto-Type â€“ funciÃ³n de KeePass para rellenar credenciales automÃ¡ticamente ntds.d / ntds punto dit ntds.dit â€“ base de datos del Active Directory con todos los hashes del dominio CAP / cap.pi CUPP (Common User Password Profiler ) â€“ generador de diccionarios personalizados Cognasi / Kaonasi Kaonashi â€“ colecciÃ³n de diccionarios para cracking de hashes en entornos corporativos Seclis / Seclix SecLists â€“ colecciÃ³n masiva de wordlists para mÃºltiples propÃ³sitos de pentesting RockU RockYou / rockyou.txt | â€“ wordlist clÃ¡sica de 14M contraseÃ±as reales setCadMapS / setWorldList setxkbmap (cambio de teclado) + ruta /usr/share/wordlists/ | â€“ directorio de diccionarios en Kali HashCut Hashcat â€“ herramienta de cracking de hashes con GPU padwalk cracking Password cracking | â€“ proceso de ruptura de contraseÃ±as hasheadas OSIN OSINT (Open Source Intelligence ) â€“ inteligencia de fuentes abiertas Bird Suite Burp Suite â€“ proxy de interceptaciÃ³n para auditorÃ­as web RTX 4090 NVIDIA GeForce RTX 4090 | â€“ tarjeta grÃ¡fica de gama alta usada para cracking de hashes VTF CTF (Capture The Flag) â€“ competiciones de hacking Town of Salem Town of Salem â€“ videojuego online que sufriÃ³ una brecha en 2018 Cambas Canva â€“ plataforma de diseÃ±o grÃ¡fico que sufriÃ³ una filtraciÃ³n de datos Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial â€“ Wolf Academy. 6 |
|---|---|---|---|---|---|

â†’

â†’

