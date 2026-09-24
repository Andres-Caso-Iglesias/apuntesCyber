# 🎓 Curiosidades y Anécdotas — Clases de Julio 2026

> Compilación de datos curiosos, anécdotas, opiniones y "gemas" sueltas por Carlos, Yuba y los compañeros durante las clases del máster.

---

## 🔧 Herramientas y Software

**Clase:** 01.07.2026 (WPScan, File Upload, Reverse Shell)

- **WPScan** es un escáner de vulnerabilidades específico para WordPress: busca versiones, plugins, themes y usuarios
- **File Upload**: si el servidor acepta un .php con código malicioso, puedes obtener un **reverse shell**
- Los CMS (WordPress, Joomla, Drupal) son más vulnerables que las webs nativas porque cualquiera puede meter un plugin
- Los plugins de WordPress son como las extensiones del navegador: cada una puede contener vulnerabilidades

> 💡 **Dato curioso:** Un plugin abandonado sin actualizaciones es una puerta abierta para atacantes.

---

## 🎯 Fuzzing de Parámetros

**Clase:** 02.07.2026 (Fuzzing, Directory Listing, Script Hijacking)

- **Fuzzing** = lanzar miles de peticiones con payloads diferentes para encontrar comportamientos anómalos
- **Directory Listing** = cuando el servidor muestra todos los archivos de un directorio
- **Script Hijacking** = si tienes acceso a un script que ejecuta comandos, puedes inyectar los tuyos
- Carlos explicó el concepto como "un guante del hacking" — cada herramienta es un dedo que hace algo diferente
- Chema llevaba tomando notas todos los días desde el inicio del máster

> 💡 **Metáfora de Carlos:** "El fuzzing es como lanzar comandos a saco y ver cuál pega."

---

## 🕵️ Anonimato y Tor

**Clase:** 06.07.2026 (Fuzzing de Parámetros I, Ingeniería Social, Anonimato)

- El **anonimato** es esa cualidad que "nos permite a los seres humanos ser subnormales" (Carlos)
- CharChas le decía cosas a Ilya Tupuria por Twitter que **a la cara no se las diría ni en pedo**
- **Monero** es la criptomoneda favorita de los ciberdelincuentes porque es verdaderamente anónima (no como Bitcoin)
- Para ser anónimo: **VPN** (no NordVPN, mejor ProtonVPN) → **Tor Browser** → **nuevos emails** → **nuevos nicks**
- La gente reutiliza nicks por comodidad, igual que reutiliza contraseñas: es un error garrafal
- **OSINT** puede encontrar la identidad real detrás de un nick si siempre usas el mismo alias

> 💡 **Lección:** El anonimato no es solo cambiar la IP — es cambiar TODO: nick, email, hábitos, forma de escribir.

---

## 📐 URL Parameters y LFI

**Clase:** 07.07.2026 (Fuzzing de Parámetros II, Escalada de Privilegios, MultiPivote)

- Carlos explicó los parámetros de URL con el ejemplo: `argentinahoypierde.com/goles=3`
- **LFI (Local File Inclusion)** = consecuencia de un **Path Traversal**
- El Path Traversal es la vulnerabilidad; el LFI es el resultado
- Para explotar un LFI necesitas que el servidor tenga una **variable** donde puedas inyectar una ruta
- Los servidores interpretan rutas relativas: `../../etc/passwd` sube directorios

> 💡 **Chiste de Carlos:** "Argentina hoy pierde... goles=3, así me ahorro el sufrimiento."

---

## 🖥️ Privilegios Linux y el Tablet Roto

**Clase:** 08.07.2026 (OWASP Top 10, LFI Fundamentos)

- Carlos se volvió a romper la tablet (la había roto el día anterior también)
- **sudo -l** = listar qué comandos puedes ejecutar como root
- **chmod 755** = Owner (rwx), Group (r-x), Others (r-x) — el 7 es rwx, el 5 es r-x
- **Cronjobs** = tareas programadas en Linux que se ejecutan automáticamente
- **Hackjacking** (así lo escribía Carlos) = cuando aprovechas un script con permisos elevados para inyectar código
- Si el servidor ejecuta un script como root y tú puedes editarlo, puedes meter un reverse shell

> 💡 **Frase de Carlos:** "Os podría explicar este máster en un bootcamp de Ironhack en 3 semanas, pero seríais chimpancés lanzando comandos."

---

## 🎂 Cumpleaños de Miquel y el Cubículo de Cristal

**Clase:** 09.07.2026 (OWASP Top 10 XXE, Labs with Castor)

- **Miquel** celebró su cumpleaños en clase — la clase le cantó "Feliz Cumpleaños"
- Carlos estaba a **59 grados** en su "cubículo de cristal" porque el aire acondicionado no funcionaba
- Chema había **soñado con castores** (las máquinas de Hack the Box) que le decían "tu muere, castor de puta"
- Chema: "Me flipa que ya estéis en el punto de soñar con las máquinas de Hack the Box"
- **Castor** y **Nike** eran máquinas de Hack the Box que estaban haciendo en clase
- Carlos usaba la tableta para dibujar diagramas y explicar conceptos en tiempo real

> 💡 **Frase de Chema:** "He tenido suficiente con el sueño de esta noche. He soñado con castores riéndose de mí."

---

## 📡 Repaso Máquinas y OBS

**Clase:** 10.07.2026 (Repaso y Explotación Avanzada, Máquinas Nike y Castor)

- Carlos seguía teniendo problemas con **OBS** (el software de grabación)
- Las máquinas **Nike** y **Castor** eran las que estaban explotando en ese momento
- Había problemas de casting — Carlos intentaba que los alumnos vieran su pantalla
- Se seguía discutiendo la metodología de explotación: enumeration → exploitation → privilege escalation

---

## 🐂 Castillo y San Fermín

**Clase:** 11.07.2026 (OWASP Top 10 XXE, Labs II)

- **Castillo** (el otro profesor) volvió de **San Fermín** (Pamplona, 6-14 julio)
- Castillo: "Ni un toro visto" — fue a San Fermín y no vio ni un solo encierro
- Dato curioso: Pamplona tiene **50.000 habitantes** pero recibe **2 millones de visitantes** durante San Fermín
- Se siguió con XXE (XML External Entity) y los labs de PortSwigger

> 💡 **Dato curioso:** San Fermín dura 9 días y la población se multiplica x40.

---

## 🗄️ SQL Injection — La Reina de las Vulnerabilidades

**Clase:** 14.07.2026 (Fundamentos Web, SQL Injection, Máquina Injected)

- **SQL Injection** = la vulnerabilidad web más antigua y más común
- **UNION SELECT** = unir dos queries para sacar datos de otras tablas
- En MySQL el comment es `--`, en Oracle puede necesitar un espacio después: `-- `
- `OR 1=1` siempre es verdadero → bypass de condiciones en WHERE
- Las comillas rompen la distinción entre datos y código SQL
- El hash MD5 se crackea fácilmente con tablas de hashes (RockYou + John the Ripper)

> 💡 **Tip:** Si ves un login que falla, intenta `admin' --` en el usuario. Si el comment funciona, probablemente hay SQLi.

---

## 🤖 IA, Vibe Coding y el Chatbot Vulnerable

**Clase:** 15.07.2026 (IA Introducción, Vibe Coding, Docker)

- Carlos mostró una web que hizo en **3 prompts** mientras daba clase → le pagaron **4.000 euros**
- El cliente tenía una web que parecía un **MySpace** → Carlos la transformó con IA
- **Vibe Coding** = programar con IA describiendo lo que quieres en lenguaje natural
- Se montaron **Docker containers** con chatbots vulnerables para practicar hacking a LLMs
- Carlos explicó **DevOps**: repo local → GitHub → servidor → SSH keys → deploy automático
- "Con 10 centavos le he creado esto" (refiriéndose al coste de los tokens de IA)

> 💡 **Frase de Carlos:** "Para qué trabajar nosotros si lo pueden hacer los demás. La cosa es estar en ese flujo y aguantar hasta que la IA nos quite el trabajo."

---

## 🕸️ PortSwigger y sus Labs

**Clase:** 17.07.2026 (PortSwigger Introducción, Repaso Path Traversal)

- **PortSwigger** es la plataforma de práctica más importante para web security
- Tiene **Path Traversal**, **SSRF**, **SSTI**, **SQLi** y muchas más categorías
- El libro "The Web Application Hacker's Handbook" (cap. 21) tiene la metodología completa
- Hay learning paths organizados por dificultad: practitioner → expert

---

## 🔄 Path Traversal Explicado por Charchas

**Clase:** 20.07.2026 (PortSwigger SSRF)

- **Charchas** intentó explicar Path Traversal a Carlos y no se lo explicó bien
- Carlos: "Es que Charchas me lo explicó y no se lo explicó bien" — risas generales
- Se vio **SSRF (Server-Side Request Forgery)** — hacer que el servidor haga peticiones internas
- SSRF puede usarse para escanear la red interna, acceder a servicios que no están expuestos

> 💡 **Broma:** Charchas intentando explicar algo a Carlos y equivocándose — momento clásico del máster.

---

## 📊 Paint vs Draw.io y SSTI

**Clase:** 21.07.2026 (PortSwigger SSTI + cierre SSRF)

- **SSTI (Server-Side Template Injection)** = inyectar código en plantillas del servidor
- Carlos usaba **Paint** para hacer diagramas — alguien sugirió **Draw.io** que es mucho mejor
- El debate sobre **blacklist vs whitelist**: whitelist siempre es mejor que blacklist
- SSTI puede escalar a **RCE (Remote Code Execution)** si el template engine lo permite
- Ejemplo clásico: `{{7*7}}` — si el servidor devuelve 49, hay SSTI

---

## 👨‍🏫 Nuevo Profesor: Sergio

**Clase:** 22.06.2026 (Metodologías de Enumeración Web)

- **Sergio** es un nuevo profesor que viene del sector **bancario**
- Trabaja como **Penetration Tester** y tiene experiencia en **Purple Team**
- Explicó las metodologías de enumeración web: cómo encontrar subdominios, puertos, tecnologías
- Purple Team = equipo que simula ataques (Red) y defensa (Blue) al mismo tiempo

---

## 🧠 Machine Learning y Obsidian Graph

**Clase:** 22.07.2026 (Redes Neuronales, Machine Learning, Arquitecturas de Conocimiento)

- Carlos mostró un **algoritmo de Tetris con ML** que aprendía a jugar solo
- El **grafo de Obsidian** se parece a una **red neuronal** — cada nota es un nodo conectado con otros
- La idea: tu Obsidian crece como una red neuronal a medida que añades notas
- Machine Learning = darle datos a un modelo para que aprenda patrones sin programarle reglas

> 💡 **Analogía:** "Tu Obsidian es como un cerebro — cada vez que añades una nota, creas una conexión."

---

## 📚 Skills, Scripts, Libraries y Claude Code

**Clase:** 23.07.2026 (IA: LLMs, Tokens, Claude Code, Arquitectura de Agentes)

- **Skills** = instrucciones específicas para que la IA sepa hacer algo concreto
- **Scripts** = código que la IA puede ejecutar para automatizar tareas
- **Libraries** = conjuntos de código reutilizable que la IA puede usar
- **Claude Code** = el entorno de desarrollo de Anthropic para programar con IA
- La IA va a "estallar el ordenador" si no se le ponen límites de contexto
- Los **agentes de IA** pueden trabajar en paralelo, cada uno con su especialidad

> 💡 **Concepto clave:** Skills + Scripts + Libraries = la trinidad para que la IA sea productiva.

---

## 📅 Última Semana de Julio

**Clases:** 24.07.2026 (Repaso Semanal III)

- **Horarios de la última semana:** Lunes 16:00, Martes 18:00, Miércoles 16:00
- **Planes para septiembre:** cerrar el módulo de auditoría web
- Se harán **presentaciones de prácticas** en septiembre
- La gente empezaba a preocuparse por las **prácticas** y el **proyecto final**

---

## 🚀 Burp AI — "Se Acabó Claude"

**Clase:** 27.07.2026 (PortSwigger SSTI, Anuncio Burp AI)

- **PortSwigger** anunció una **IA integrada en Burp Suite** que hace todo el trabajo de auditoría
- La IA de Burp puede: interceptar peticiones, fuzzear, analizar respuestas, y encontrar vulnerabilidades automáticamente
- Carlos: "Se acabó Claude" — la IA de Burp podría reemplazar a Claude para auditorías
- Ya hay una **beta pública** para probar
- La herramienta interna de Civersia se llama **"El Bicho"** — audita de forma pasiva y activa
- "Cada día creo que no va a hacer falta ni darle a un botón"

> 💡 **Opinión de Carlos:** "¿Para qué trabajar nosotros si lo pueden hacer los demás?"

---

## 🔄 Repaso General y Command Injection

**Clase:** 28.07.2026 (Repaso General, Metodología Web, Command Injection)

- Se hizo un **repaso general** de todo lo visto: SSTI, SSRF, SQLi, Path Traversal
- **Command Injection** = inyectar comandos del sistema operativo a través de la aplicación web
- Si la web ejecuta un ping y tú puedes meter comandos adicionales, tienes Command Injection
- El comando es `ping 8.8.8.8; ls` — el punto y coma separa comandos
- Se habló de la **certificación JPT (Junior Penetration Tester)** — "¿Me puedo hacer la JPT ya?"

---

## 🎤 Práctica 1 y Machine Learning

**Clase:** 29.07.2026 (Presentación Práctica 1)

- Se presentó la **Práctica 1** — el primer proyecto formal del máster
- Se hizo un repaso del **grafo de Obsidian** y cómo usarlo como base de conocimiento
- Se repasó **Machine Learning** y cómo se conecta con la ciberseguridad
- Carlos: "Vosotros sois piletes de cinta de lomo como chimpancillo" (broma sobre los alumnos)

---

## 🍕 Anécdotas de Clase

| Fecha | Anécdota |
|---|---|
| 01.07 | Carlos explicó WPScan y reverse shell en WordPress — los alumnos flipaban con lo fácil que era |
| 02.07 | Chema empezó a tomar notas todos los días desde el primer día |
| 06.07 | CharChas trolleando a Ilya Tupuria por Twitter — "a la cara no se lo diría ni en pedo" |
| 07.07 | Carlos explicó URL params con "argentinahoypierde.com/goles=3" |
| 08.07 | Carlos se rompió la tablet (otra vez) — "he vuelto a romper la tablet" |
| 09.07 | Chema soñando con castores: "tu muere, castor de puta" |
| 09.07 | Cumpleaños de Miquel — la clase le cantó "Feliz Cumpleaños" |
| 09.07 | Carlos a 59 grados en su cubículo de cristal |
| 10.07 | Problemas con OBS y el casting de pantalla |
| 11.07 | Castillo volvió de San Fermín: "ni un toro visto" |
| 15.07 | Carlos hizo una web en 3 prompts y le pagaron 4.000 euros |
| 15.07 | "Argentina da igual" — discusión sobre el partido en clase |
| 20.07 | Charchas intentando explicar Path Traversal a Carlos y fallando |
| 22.07 | Nuevo profesor Sergio del sector bancario |
| 22.07 | Carlos mostró un Tetris con ML que aprendía a jugar |
| 27.07 | "Se acabó Claude" — anuncio de Burp AI |
| 27.07 | "El Bicho" — la herramienta interna de Civersia |
| 28.07 | Discusión sobre la certificación JPT |
| 29.07 | "Piletes de cinta de lomo como chimpancillo" — Carlos bromeando |

---

## 📊 Datos Técnicos Sueltos

| Dato | Contexto |
|---|---|
| **WPScan** | Escáner de vulnerabilidades para WordPress |
| **chmod 755** | Owner=rwx, Group=r-x, Others=r-x |
| **sudo -l** | Listar comandos ejecutables como root |
| **Path Traversal** | Acceder a archivos fuera del directorio web |
| **LFI** | Consecuencia del Path Traversal |
| **SSRF** | Hacer que el servidor haga peticiones internas |
| **SSTI** | Inyectar código en plantillas del servidor |
| **Command Injection** | Inyectar comandos del SO a través de la web |
| **UNION SELECT** | Unir queries SQL para sacar datos de otras tablas |
| **MD5 es frágil** | Se crackea con tablas RockYou + John |
| **Tor** | Red de anonimato que enruta tráfico por 3 nodos |
| **Monero** | Criptomoneda verdaderamente anónima |
| **Burp AI** | IA integrada en Burp Suite para auditoría automática |
| **Claude Code** | Entorno de desarrollo de Anthropic |
| **El Bicho** | Herramienta interna de Civersia para auditorías |

---

## 🎤 Frases Destacadas

> "El anonimato es esa fantástica y fabulosa cualidad que nos permite a los seres humanos ser subnormales." — Carlos

> "Os podría explicar este máster en un bootcamp de Ironhack en 3 semanas, pero seríais chimpancés lanzando comandos." — Carlos

> "He soñado con castores riéndose de mí y diciendo 'tu muere, castor de puta'." — Chema

> "Ni un toro visto" — Castillo, sobre San Fermín

> "Se acabó Claude" — Carlos, sobre Burp AI

> "Para qué trabajar nosotros si lo pueden hacer los demás." — Carlos

> "La cosa es estar en ese flujo y aguantar hasta que la IA nos quite el trabajo." — Carlos

> "Con 10 centavos le he creado esto" — Carlos, sobre una web hecha con IA

> "Vosotros sois piletes de cinta de lomo como chimpancillo." — Carlos

> "Si a la vuelta tenéis cualquier duda, nos ponemos a una NMAP, Sira, no lo digas dos veces." — Carlos

---

**Última actualización:** Julio 2026
**Fuentes:** Transcripciones de clases del máster