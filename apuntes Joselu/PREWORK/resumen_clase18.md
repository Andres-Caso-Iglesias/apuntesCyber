> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 18**
> **Módulo:** PREWORK
> **Tema:** Clase 18
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 18. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

| Resumen “ Clase 18: Diccionarios, Credenciales y Ataques de Fuerza Bruta Máster de Ciberseguridad e Inteligencia Artificial “ Evolve Academy 1. Introducción Esta sesión cubre cinco bloques interrelacionados: el concepto y uso de los diccionarios en pentesting, los ataques de fuerza bruta, los mecanismos de autenticación y el concepto de credenciales, los gestores de contraseñas y, finalmente, las principales colecciones de diccionarios y la herramienta de generación personalizada CUPP. 2. Ataques de fuerza bruta Un ataque de fuerza bruta | consiste en probar automáticamente todas las combinaciones posibles de caracteres para encontrar una contraseña. La herramienta itera carácter a carácter desde la €˜a€™ minúscula hasta la €˜Z€™ mayúscula, pasando por todos los caracteres especiales, para cada posición de la contraseña. Velocidad y capacidad de cómputo: | - Una tarjeta gráfica RTX 4090 rompe una contraseña de 8 caracteres en 40 minutos. - Cuanto mayor sea la longitud y complejidad de la contraseña, más tiempo computacional se requiere. - La capacidad de cómputo aumenta con el tiempo: lo que hoy tarda 40 minutos, mañana tardará menos. Características que debe tener una contraseña segura: Característica Detalle Longitud Mínimo 12 caracteres Complejidad Mayúsculas, minúsculas, números y caracteres especiales Unicidad Nunca reutilizar la misma contraseña en distintos servicios No predecible No usar patrones del tipo €œNombreEmpresa+Año+!€ Por qué la unicidad es crítica (caso real): | en un congreso de seguridad, un ponente explicó que usaba un patrón para sus contraseñas (nombre del servicio + año + símbolo). Un asistente del público encontró su correo en Dehashed, dedujo el patrón y accedió a sus otras cuentas en tiempo real durante la propia charla. Fuerza bruta vs. diccionario: la fuerza bruta garantiza encontrar la contraseña (prueba todas las 1 |
|---|---|---|---|

| combinaciones posibles), pero tarda más. El ataque por diccionario es más rápido pero solo tiene éxito si la contraseña está en la lista. 3. Verificación de filtraciones: Have I Been Pwned Have I Been Pwned | (haveibeenpwned.com) es un servicio gratuito que permite comprobar si un correo electrónico ha sido comprometido en alguna brecha de datos conocida y pública. Devuelve el nombre del servicio donde se filtró, la fecha y los tipos de datos expuestos (correo, contraseña, IP, navegador, etc.). Ejemplos de filtraciones reales del profesor: Town of Salem (juego online, dic. 2018), MyFitnessPal (app de calorías), Canva, Wattpad. Moraleja: cualquier aplicación sin medidas de seguridad correctamente implementadas puede filtrar las contraseñas de sus usuarios en texto claro. Auditorías de contraseñas en Active Directory: | cuando se obtiene el fichero ntds.dit del controlador de dominio, se realiza un análisis de la calidad de las contraseñas del dominio completo. Los patrones más frecuentes encontrados son: usuario igual a contraseña (ej. €œagomez€ →’ €œagomez€), ciudad + año (ej. €œMadrid24!€), nombre de la empresa + año + símbolo (ej. €œEvolve2024!€). Esto refleja el bajo nivel de madurez en políticas de contraseñas de muchas organizaciones. 4. Mecanismos de autenticación: los tres pilares Los sistemas de verificación de identidad digital se construyen sobre tres pilares: Pilar Descripción Ejemplos Algo que yo sé Información memorizada Usuario + contraseña, PIN, pregunta de seguridad Algo que yo tengo Dispositivo o token físico Token RSA, tarjeta inteligente, móvil (OTP/TOTP) Algo que yo soy Características biológicas Huella dactilar, reconocimiento facial, iris La combinación de dos o más pilares da lugar a la autenticación multifactor (MFA) . Un sistema que combine €œalgo que sé€ + €œalgo que tengo€ (ej. contraseña + código SMS) es exponencialmente más difícil de comprometer que uno que solo use contraseña. 5. Gestores de contraseñas Dado que las contraseñas deben ser largas, complejas y únicas para cada servicio, memorizarlas 2 |
|---|---|---|

| todas es humanamente imposible. Los gestores de contraseñas | resuelven este problema: se accede a todos con una única contraseña maestra . KeePass (solución local) |
|---|---|
- Almacena las contraseñas en un fichero cifrado con extensión .kdbx localmente.
- Incluye generador de contraseñas aleatorias configurables en longitud y complejidad.
- Función Auto-Type: rellena automáticamente usuario y contraseña en el portal web con
un atajo de teclado.
- Ventaja: muy seguro; las contraseñas no salen del equipo.
- Desventaja: fichero local sin sincronización cloud →’ múltiples versiones del archivo,
inaccesible desde otros dispositivos. LastPass (solución cloud)
- Equivalente cloud de KeePass. Sincroniza contraseñas entre dispositivos.
- Disponible con planes gratuitos, familiares y de empresa.
Vaultwarden / Bitwarden (solución cloud self-hosted)
- El profesor lo usa personalmente en su propio servidor ( pass.omnia.dev).
- Vaultwarden es una implementación open source de Bitwarden que se puede autoalojar.
- Protegido con Cloudflare Tunnels: solo accesible con su cuenta de Google como segundo
factor.
- Ventaja: combina la seguridad del control propio con la comodidad cloud.
| 6. Diccionarios: concepto y tipos Un diccionario (wordlist) es una lista de palabras o cadenas de texto que se usa para optimizar los ataques de fuerza bruta, evitando tener que generar todas las combinaciones posibles desde cero. El objetivo es que la contraseña objetivo esté en la lista. Cuándo usar diccionarios vs. | fuerza bruta pura: | - Diccionario: más rápido si la contraseña es predecible o común. No garantiza resultado. - Fuerza bruta: garantiza encontrar la contraseña (si se tiene suficiente tiempo/hardware). Más lento. Aplicaciones de los diccionarios más allá de contraseñas: | - Fuzzing de subdominios: | probar palabras de una lista como prefijos de un dominio para descubrir subdominios existentes (ej. comidas.omnia.dev ). - Fuzzing de rutas web: | descubrir directorios y archivos ocultos en un servidor web (como vimos con Gobuster/Dirsearch en la clase 17). - Cuanto más ajustado esté el diccionario al contexto del objetivo, más eficiente será el ataque. 3 |
|---|---|---|---|---|---|

7. Principales diccionarios y colecciones RockYou (rockyou.txt)
- Ruta en Kali: /usr/share/wordlists/rockyou.txt
- La wordlist más conocida y utilizada. Fue filtrada en la brecha de la empresa RockYou
(2009) y contiene ~14 millones de contraseñas reales.
- Uso recomendado: exclusivamente para entornos CTF, máquinas de laboratorio (Hack
The Box, TryHackMe, VulnHub) porque los creadores de retos la utilizan como referencia.
- No recomendado en auditorías reales: en el mundo corporativo real las contraseñas
siguen otros patrones y raramente aparecen en esta lista. SecLists
- Colección masiva de wordlists para múltiples propósitos: credenciales, subdominios,
rutas web, fuzzing de APIs, usuarios comunes, etc.
- Instalable en Kali con apt install seclists o mediante git clone desde GitHub.
- Ruta en Kali: /usr/share/wordlists/
- Contiene, entre otras, las 10.000 contraseñas más comunes ordenadas por frecuencia de
uso real (las primeras: password, 123456, 123456789, qwerty, 111111€¦).
- También incluye listas de subdominios típicos en español para fuzzing de
infraestructura. Kaonashi
- Colección de diccionarios especializada en cracking de hashes construida a partir del
análisis de miles de millones de contraseñas reales filtradas en brechas de datos.
- Orientada al mundo corporativo real: sus contraseñas siguen los patrones de
comportamiento humano real (empresa+año, nombre+símbolo, etc.).
- Se usa junto con Hashcat y reglas personalizadas para optimizar la ruptura de hashes
obtenidos en auditorías internas (ej. del fichero ntds.dit).
- Permite aplicar reglas de transformación: dada una palabra base (ej. €œEvolve€), generar
todas las variantes con años del 2012 al 2025 y caracteres especiales, creando una lista derivada muy eficiente. 8. CUPP: generador de diccionarios personalizados CUPP (Common User Password Profiler ) es una herramienta de GitHub que genera una wordlist personalizada a partir de información OSINT sobre la víctima. Inspirada en la serie Mr. Robot (capítulo donde el protagonista genera un diccionario personalizado a partir de datos del objetivo). Instalación: 4

| git clone https://github.com/Mebus/cupp cd cupp python3 cupp.py -h Uso en modo interactivo ( -i): CUPP pregunta por los datos de la víctima que se hayan podido recopilar mediante OSINT (fuentes abiertas: LinkedIn, Instagram, Twitter, etc.): - Nombre y apellidos - Nickname - Fecha de nacimiento - Nombres de pareja, hijos, mascotas - Empresa - Palabras clave relacionadas (hobbies, aficiones) - Si añadir números aleatorios o caracteres especiales al final Con estos datos genera un fichero .txt con todas las combinaciones posibles derivadas de esa información, formando un diccionario altamente personalizado y orientado al objetivo concreto. Ejemplo de la sesión: | el profesor generó un diccionario sobre sí mismo con datos públicamente disponibles (nombre: Yuba González, nickname: YubarGP, fecha de nacimiento: 17/09/1999, nombre del padre: Roberto, hermana: Aruna, gatos: Tizón, empresa: Cibersia, aficiones: hacker, water polo€¦). Por qué es poderoso: | los datos de OSINT permiten construir listas muy ajustadas al comportamiento del objetivo, reduciendo drásticamente el espacio de búsqueda frente a un diccionario genérico. 9. Flujo de trabajo completo con diccionarios en una auditoría 1.Obtener el hash: desde el fichero ntds.dit del Active Directory (Mimikatz), desde una base de datos web comprometida o desde un formulario de login capturado. 2.Elegir el diccionario adecuado: | RockYou para CTF/laboratorio; Kaonashi o wordlist personalizada (CUPP) para auditorías corporativas reales. 3.Aplicar reglas de transformación | (Hashcat rules): derivar variantes automáticas de las palabras base del diccionario. 4.Lanzar el cracking con Hashcat | (GPU) o John the Ripper (CPU). 5.Obtener la contraseña en claro | →’ usarla para pivoting, acceso a más máquinas o demostración de impacto en el reporte. 10. Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración Half-I€™ve-Been-Pwned Have I Been Pwned | (haveibeenpwned.com) “ servicio de comprobación de filtraciones Kipas / KeePass PowerSafe KeePass “ gestor de contraseñas local con fichero .kdbx Laspas LastPass “ gestor de contraseñas cloud Ball Ward / Valwarden Vaultwarden / Bitwarden | “ gestor de contraseñas cloud open source 5 |
|---|---|---|---|---|---|---|---|---|

| Término en la transcripción Corrección / Aclaración KDBX .kdbx “ formato de fichero cifrado de KeePass Open Pass Word in Horizon Password Generator | “ generador de contraseñas integrado en KeePass Perform Auto Type Auto-Type “ función de KeePass para rellenar credenciales automáticamente ntds.d / ntds punto dit ntds.dit “ base de datos del Active Directory con todos los hashes del dominio CAP / cap.pi CUPP (Common User Password Profiler ) “ generador de diccionarios personalizados Cognasi / Kaonasi Kaonashi “ colección de diccionarios para cracking de hashes en entornos corporativos Seclis / Seclix SecLists “ colección masiva de wordlists para múltiples propósitos de pentesting RockU RockYou / rockyou.txt | “ wordlist clásica de 14M contraseñas reales setCadMapS / setWorldList setxkbmap (cambio de teclado) + ruta /usr/share/wordlists/ | “ directorio de diccionarios en Kali HashCut Hashcat “ herramienta de cracking de hashes con GPU padwalk cracking Password cracking | “ proceso de ruptura de contraseñas hasheadas OSIN OSINT (Open Source Intelligence ) “ inteligencia de fuentes abiertas Bird Suite Burp Suite “ proxy de interceptación para auditorías web RTX 4090 NVIDIA GeForce RTX 4090 | “ tarjeta gráfica de gama alta usada para cracking de hashes VTF CTF (Capture The Flag) “ competiciones de hacking Town of Salem Town of Salem “ videojuego online que sufrió una brecha en 2018 Cambas Canva “ plataforma de diseño gráfico que sufrió una filtración de datos Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial “ Wolf Academy. 6 |
|---|---|---|---|---|---|

→’

→’

