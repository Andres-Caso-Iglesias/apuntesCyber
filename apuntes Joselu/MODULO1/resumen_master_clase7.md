> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 7**
> **MÃ³dulo:** MODULO1
> **Tema:** Clase 7
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 7. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. IntroducciÃ³n y temario

La sesiÃ³n tiene dos bloques principales: la consolidaciÃ³n prÃ¡ctica de **comandos personalizados en Bash** (con alumnos compartiendo pantalla y creando sus propios comandos en directo) y una introducciÃ³n aplicada al **OSINT/HUMINT** con demostraciÃ³n en vivo de las herramientas mÃ¡s utilizadas en auditorÃ­as externas.

## 2. OSINT y HUMINT: concepto y aplicaciÃ³n profesional

**OSINT** (*Open Source Intelligence*) es la recopilaciÃ³n de inteligencia a partir de fuentes abiertas y pÃºblicas de Internet con el objetivo de conocer mejor a una organizaciÃ³n o persona antes de perpetrar un ataque.

**HUMINT** (*Human Intelligence*) es la variante centrada en personas fÃ­sicas: construir un perfil social completo de un individuo para personalizar el ataque (ingenierÃ­a social, phishing dirigido, suplantaciÃ³n).

**Â¿CuÃ¡ndo se usa en auditorÃ­as?** - Siempre en auditorÃ­as externas, como punto de partida. - Para identificar empleados y construir el directorio de objetivos antes del phishing. - Para detectar credenciales filtradas que se pueden reutilizar en portales corporativos. - Para localizar documentos internos filtrados que se pueden reportar como hallazgo.

**ReflexiÃ³n clave del profesor:** quien personaliza el ataque con informaciÃ³n OSINT puede cobrar 10.000 â‚¬ en vez de 4.000 â‚¬, porque la probabilidad de Ã©xito es exponencialmente mayor. Ejemplo real: una campaÃ±a de phishing a 1.200 empleados obtuvo un 80% de apertura de correo y un 27% de envÃ­o de datos.

## 3. Repaso: comandos personalizados en Bash (prÃ¡ctica en vivo)

### Ciclo completo para crear un comando personalizado

| 1. | **Crear el script** con nano nombre_comando: |
|---|---|

 - Primera lÃ­nea: #!/bin/bash (shebang --- indica que es un ejecutable Bash).
 - Contenido: comandos de terminal o lÃ³gica.

| 2. | **Dar permisos de ejecuciÃ³n:** chmod +x nombre_comando |
|---|---|

| 3. | **Moverlo al PATH** (con sudo porque las rutas del PATH son de root): |
|---|---|

```bash
sudo mv nombre_comando /usr/local/sbin/nombre_comando
```

| 4. | **Invocar desde cualquier parte del sistema** simplemente escribiendo el nombre. |
|---|---|

### Ejemplo creado en clase: rickroll

Script que muestra un Rick Roll en ASCII art en la terminal, utilizando curl:

#!/bin/bash

```bash
curl ascii.live/rick
```

**Variante mejorada:** pasar por parÃ¡metro \$1 el nÃºmero de segundos que debe durar, usando timeout:

#!/bin/bash

timeout $1 curl ascii.live/rick

Uso: rickroll 10 â†’ reproduce el Rick Roll durante 10 segundos y para automÃ¡ticamente.

### Errores mÃ¡s comunes detectados en clase

- \* **en lugar de** \# **al inicio del shebang:** el \* se interpreta como comodÃ­n, no como inicio de comentario/shebang. Siempre usar #!.
- **No meter el script en el PATH:** el script funciona si se ejecuta con ./nombre desde su carpeta, pero no es un "comando" hasta que se mueve a una ruta del PATH.
- **Ruta incorrecta al mover:** escribir mal la ruta destino (ej. bin en vez de .local/bin o usr/local/sbin) hace que el comando no aparezca. Usar echo \$PATH para confirmar las rutas disponibles.
- sudo su **innecesario:** no hace falta cambiar a root permanentemente; basta con usar sudo delante del comando especÃ­fico que lo requiere.

### ZSH vs.Â Bash en Kali Linux

Las versiones mÃ¡s nuevas de Kali usan **ZSH** por defecto en lugar de Bash. Sin embargo: - El 99% de los servidores que se auditarÃ¡n en entornos reales usan Bash (Linux de versiones antiguas). - Especificar #!/bin/bash en el shebang garantiza que el script se interprete como Bash independientemente del shell activo. - El profesor prefiere Bash por ser mÃ¡s universal y estable.

### Modelos de IA para scripting: debate del aula

Se debatiÃ³ sobre quÃ© modelo de IA usar para generar scripts: - **Claude (Anthropic):** favorito del profesor. Usa Claude Sonnet y Opus. Para proyectos complejos usa **Claude Code** con agentes y redes neuronales vectoriales para ahorro de tokens. - **ChatGPT (OpenAI):** el nuevo modelo **o3** (*Cortex*) es muy competente para cÃ³digo; la batalla con Sonnet es constante. - **Cursor (IDE):** IDE de programaciÃ³n con modelos integrados (Sonnet, Haiku, GPT-4, Grok). Muy Ãºtil para proyectos de desarrollo. No necesita red neuronal ni agentes propios. - **Gemini:** gratis para estudiantes durante un aÃ±o (incluye 5 TB y la versiÃ³n Pro). Interesante como alternativa gratuita. - **Herramienta clave para automatizaciÃ³n de clics:** **Playwright** --- permite controlar un navegador Chromium programÃ¡ticamente. El profesor lo combina con Claude para automatizar cualquier tarea que no tenga API (ej. formularios en Power Automate, creaciÃ³n de flujos sin API).

## 4. OSINT/HUMINT en la prÃ¡ctica: herramientas demostradas en clase

### OpenSense (herramienta principal de OSINT con IA)

**OpenSense** es la alternativa moderna a Maltego: correlaciÃ³n de nodos mediante grafos con motor de IA integrado. Permite partir de un correo electrÃ³nico e ir iterando para descubrir: - Aliases y perfiles en GitHub, Twitter, foros. - Correos alternativos vinculados al mismo usuario. - **Hashes de contraseÃ±as** extraÃ­dos de bases de datos filtradas. - Conexiones entre personas (colaboradores, proyectos compartidos).

**DemostraciÃ³n en clase:** buscando el correo del profesor, OpenSense encontrÃ³ en minutos: alias *keyadimundi*, perfil en GitHub con proyecto compartido con un amigo del colegio de hace 15 aÃ±os, correo antiguo de Hotmail, presencia en BreachForums, y varios hashes de contraseÃ±as filtradas de mÃºltiples brechas.

### Maltego

Herramienta de correlaciÃ³n de nodos OSINT de referencia en el sector (\~5.000â‚¬/mes en licencia completa). Disponible en versiÃ³n gratuita con correos temporales: - Descarga desde maltego.com/downloads. - Se puede crear cuentas ilimitadas usando emails de un solo uso (**10minutemail**, **tempmail**, etc.). - Se conecta mediante APIs a fuentes externas: VirusTotal, Hunter.io, bases de datos de personas, fuentes corporativas, etc. - Plugins gratuitos recomendados: CasaFile Entities, CyberStreet Intelligence, Corporate Intelligence (500+ transformaciones). - **Advertencia:** la versiÃ³n de Kali Linux de Maltego es muy lenta; recomendable instalarlo en Windows.

### Have I Been Pwned (haveibeenpwned.com)

Servicio gratuito que comprueba si un correo ha aparecido en brechas de datos conocidas. Muestra el servicio donde se filtrÃ³, la fecha y el tipo de datos comprometidos. **Importante aclarar al cliente:** no significa que le hayan hackeado el correo, sino que los servicios donde estÃ¡ registrado fueron comprometidos.

### Dehashed (dehashed.com)

Plataforma de pago (\~7â‚¬/mes) que muestra las contraseÃ±as en texto claro de brechas filtradas. Usos en auditorÃ­as: - Buscar por dominio corporativo (ej. repsol.com) y obtener usuarios y contraseÃ±as potenciales. - Probar esas contraseÃ±as en portales no corporativos (Amazon, Canva) para verificar si el usuario reutiliza contraseÃ±a â†’ si funciona, usar esa contraseÃ±a en el portal VPN o Microsoft de la empresa. - Extraer el fichero CSV y usarlo como diccionario en un ataque de fuerza bruta o password spraying. - Identificar patrones de contraseÃ±as para crear diccionarios personalizados.

**Caso real en clase:** bÃºsqueda de contraseÃ±as de la PolicÃ­a Nacional encontrÃ³ contraseÃ±as tipo "tortosa", "tortogol" --- contraseÃ±as triviales que no cumplen ninguna polÃ­tica de seguridad. La IP 127.0.0.1 en la base de datos indica que la filtraciÃ³n fue interna (un ntds.dit extraÃ­do desde dentro de la red).

**RecomendaciÃ³n:** usar una cuenta de correo anÃ³nima (ProtonMail) para Dehashed; pagos con criptomonedas para mayor anonimato. **No usar** correo temporal porque los pagos requieren cuenta persistente.

### Truecaller

Herramienta que indexa bases de datos de nÃºmeros de telÃ©fono recopiladas de agendas robadas por aplicaciones maliciosas (el clÃ¡sico ejemplo de la linterna que pide acceso a contactos). Permite buscar un nÃºmero de telÃ©fono y obtener el nombre con el que estÃ¡ guardado en otras agendas. DemostraciÃ³n en vivo con nÃºmeros de telÃ©fono de los alumnos â†’ el profesor encontrÃ³ cÃ³mo tenÃ­an guardado su nÃºmero en las agendas de otras personas (apodos, nombres completos, etc.).

### EXIF Tool

Para extraer metadatos de imÃ¡genes (ubicaciÃ³n GPS, dispositivo, fecha/hora). Actualmente en desuso porque iOS y Android eliminan los metadatos EXIF por defecto al subir imÃ¡genes a redes sociales.

### CorrelaciÃ³n del flujo completo de una auditorÃ­a externa

1. Buscar el dominio en Dehashed/OpenSense â†’ credenciales filtradas 2. Verificar credenciales en servicios no corporativos (Amazon, Canva) 3. Si funciona â†’ probarla en portal VPN/Microsoft de la empresa 4. Si entra â†’ estamos dentro de la red corporativa sin explotar ninguna vulnerabilidad

## 5. PsicologÃ­a e ingenierÃ­a social

El HUMINT (stalking de perfiles) permite construir un perfil psicolÃ³gico de la vÃ­ctima a partir de sus Ãºltimos 30 "me gusta" en redes sociales. Estudio psicolÃ³gico citado: con solo 30 likes de Facebook se puede predecir la personalidad con mÃ¡s precisiÃ³n que la propia familia. AplicaciÃ³n ofensiva: personalizar el pretexto del ataque de ingenierÃ­a social con los gustos, intereses y rutinas de la vÃ­ctima.

**Serie recomendada para entender el OSINT aplicado a personas:** *You* (Netflix) --- muestra cÃ³mo a partir de una foto y OSINT se puede trazar la direcciÃ³n, rutina y cÃ­rculo social de una persona.

## 6. Roadmap del mÃ¡ster: cuÃ¡ndo llegan las mÃ¡quinas

| Semanas | Contenido |
|---|---|
| Semanas 1-4 | Bases de informÃ¡tica, terminal Linux y Windows, redes, OSINT \~Semana 5-6 | Primeros ataques en mÃ¡quina vulnerable (Metasploitable) \~Semanas 7-8 | MÃ³dulo de hacking web completo \~Mes 2.5 | Full Hack The Box (mÃ¡quinas reales) Ãšltimos 2 meses | PrÃ¡ctica 3: entorno Active Directory, pivoting avanzado |
|---|---|---|---|---|---|

## 7. Conceptos y tÃ©rminos clave corregidos

| TÃ©rmino en la transcripciÃ³n | CorrecciÃ³n / AclaraciÃ³n |
|---|---|
| UMINT / umint | **HUMINT** (*Human Intelligence*) -- inteligencia basada en personas Open Sense / OpenSense | **OpenSense** -- herramienta de correlaciÃ³n OSINT con motor de IA Maldego / Maltego | **Maltego** -- herramienta estÃ¡ndar de correlaciÃ³n OSINT en grafos Haunter.io / Hounder.io | **Hunter.io** -- herramienta para buscar correos electrÃ³nicos corporativos Half-Time Impounded / Half-fiving | **Have I Been Pwned** (haveibeenpwned.com) -- verificador de filtraciones de datos Hasset / Dehashed | **Dehashed** -- plataforma de contraseÃ±as filtradas Bridge Forums / BridgeForums | **BreachForums** -- foro principal de la Deep Web para filtraciÃ³n de datos Virus Total | **VirusTotal** -- plataforma de anÃ¡lisis de malware con mÃºltiples motores antivirus Exit Tool | **ExifTool** -- herramienta de extracciÃ³n de metadatos de imÃ¡genes Cortex / el nuevo de GPT | **GPT o3 (**"**Cortex**"**)** -- modelo avanzado de OpenAI para cÃ³digo y razonamiento Sonnet / Opus 4.7 | **Claude Sonnet / Claude Opus** -- modelos de lenguaje de Anthropic Cloud de Code / Claudio | **Claude Code** -- herramienta de Anthropic para desarrollo asistido por IA Cursor | **Cursor** -- IDE de programaciÃ³n con integraciÃ³n de mÃºltiples modelos de IA Playwright | **Playwright** -- librerÃ­a para automatizaciÃ³n de navegador (clics, formularios, scraping) Power Automate | **Microsoft Power Automate** -- herramienta de automatizaciÃ³n de flujos de trabajo Ã± de temp / el sÃ­mbolo | **Alt Gr + 4 + Espacio** â†’ \~ (tilde, sÃ­mbolo del directorio home en Linux) nntdc.dip | **ntds.dit** -- base de datos del Active Directory con todos los hashes de contraseÃ±as ascii.live/rick | **curl ascii.live/rick** -- URL que muestra el Rick Roll en ASCII art en terminal Bounsert Digital | **Bouncer Digital** -- empresa del profesor orientada a protecciÃ³n del menor en Internet un USCP | **OSCP** (*Offensive Security Certified Professional*) -- certificaciÃ³n premium de pentesting |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.

â†’

â†’

â†’



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Septiembre/07.09.2026 SQLi - Fundamentos de SQL.md|07.09.2026 SQLi - Fundamentos de SQL]] — IA en Ciberseguridad, Linux, Windows
- [[../../transcripciones/Septiembre/01.09.2026 Repaso General I.md|01.09.2026 Repaso General I]] — IA en Ciberseguridad, Linux, OSINT
- [[resumen_master_clase1.md|resumen_master_clase1]] — IA en Ciberseguridad, Linux, OSINT
- [[../../transcripciones/Junio/02.06.2026 Introducción a HackTheBox Starting Point Tier0.md|02.06.2026 Introducción a HackTheBox Starting Point Tier0]] — IA en Ciberseguridad, Linux, OSINT
- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point — Tier 0.md|Hack The Box- Starting Point — Tier 0]] — Linux, OSINT, Windows
- [[../MODULO3/resumen_master_clase26.md|resumen_master_clase26]] — IA en Ciberseguridad, Linux, OSINT

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #certificaciones #esteganografia #hack-the-box #hydra #ia #kali #linux #metasploitable #osint #pivoting #redes #sqli #windows
