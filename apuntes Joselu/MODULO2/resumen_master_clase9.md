> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 9**
> **Módulo:** MODULO2
> **Tema:** Clase 9
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 9. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1.

Cierre del módulo OSINT y proyectos de herramientas

El profesor cierra el módulo de OSINT con una propuesta: los alumnos interesados en desarrollar herramientas propias de OSINT pueden coordinarse entre ellos por WhatsApp, crear un repositorio GitHub común y construir una herramienta colectiva mucho más potente que cualquier herramienta individual.

La idea es aplicar este mismo enfoque a otros módulos (forense, web, redes): equipos pequeños construyendo herramientas reales que refuercen el aprendizaje teórico.

**Recursos mencionados para seguir aprendiendo OSINT:** - **OSINTomático**: comunidad y eventos de referencia en OSINT en España. - **Ciberpatrulla** (ciberpatrulla.com): repositorio de herramientas OSINT muy completo, con recursos por categoría (búsqueda de imágenes, metadatos, geolocalización, redes sociales, etc.). - Repositorios GitHub especializados buscando "Google Dorks hacking".

## 2.

PimEyes: búsqueda de personas por reconocimiento facial

**PimEyes** (pimeyes.com) es la herramienta más potente para búsqueda inversa de imágenes de personas.

A diferencia de Google Images o Yandex, está especializada en detección facial y permite:

- Buscar a partir de una fotografía todas las apariciones de esa persona en internet.
- Incluye historial temporal: no solo fotos actuales, sino también fotos antiguas (el profesor encontró fotos de un alumno de cuando era pequeño en páginas rusas).
- Permite reconstruir la trayectoria de una persona y correlacionar perfiles en diferentes redes y plataformas.
- La información encontrada puede revelar datos sensibles: el profesor descubrió que un alumno aparecía en páginas rusas, lo que potencialmente le bloquearía la obtención del HPC (Habilitación Personal de Seguridad del CNI).

**Limitaciones y alternativas:** - PimEyes tiene un límite de búsquedas gratuitas.

Para más búsquedas, usar correos temporales para crear nuevas cuentas. - **Yandex Images**: alternativa potente, especialmente para contenido ruso.

Al no tener que cumplir el RGPD europeo, tiene menos restricciones.

Actualmente con mayor limitación que antes. - **Google Images** (búsqueda inversa): menos potente para reconocimiento facial. - Para mejores resultados: subir varias fotos de la misma persona desde diferentes ángulos.

## 3.

Ejercicio práctico de HUMINT: reconstruir un perfil desde un número de teléfono

### El ejercicio

El profesor facilitó un único dato --- un número de teléfono --- y los alumnos tenían 25 minutos para obtener: 1.

Nombre y apellidos completos 2.

Empleo actual 3.

Cinco lugares de trabajo anteriores 4.

Precio por hora en al menos uno de sus trabajos 5.

Deporte que practicaba 6. **Bonus:** número de DNI y alias/nickname

El objetivo era Yuba González Parrilla, otro profesor del máster.

### Solución paso a paso (write-up)

**Paso 1 --- Número de teléfono → Nombre:** Herramienta: **TrueCaller** (bot de Telegram).

Al introducir el número, devuelve automáticamente el nombre asociado: "Yuba González".

Solo un apellido; faltaba el segundo.

**Paso 2 --- Segundo apellido:** Búsqueda en Google de "Yuba González" → nombre poco común, pocos resultados → se encuentra fácilmente "Yuba González Parrilla".

**Paso 3 --- Empleo actual y trayectoria laboral:** LinkedIn → España Offensive Security Manager y European Cloud Security Lead en **Fujitsu**.

### Trayectoria completa: Fujitsu, OESIA, Cipherbit (Grupo OESIA), Wolf Academy (docente), TEF (Telefónica), UPM (profesor freelance), clases particulares.

**Paso 4 --- Precio por hora:** Plataforma **TuClaseParticular.com** → perfil de Yuba como profesor de clases particulares → tarifa visible en el perfil.

Alternativa rápida usada por un alumno: pasar la URL de LinkedIn a Claude/ChatGPT.

**Paso 5 --- Deporte:** Google → segunda página de resultados → "Federación Madrileña de Natación y Waterpolo" → aparece el nombre.

Deporte: **waterpolo**.

**Paso 6 --- DNI (bonus):** Vía más efectiva: los documentos del club de waterpolo o la federación filtran DNIs en PDFs públicos por un fallo de GDPR de terceros.

El DNI aparecía en una imagen dentro de los resultados de Google Images al buscar el nombre combinado con el deporte.

> [!important] **Técnica clave:** iterar las búsquedas variando el orden de nombre y apellidos (González Parrilla Yuba, Yuba González Parrilla, etc.) y con/sin tilde, ya que los documentos no siguen un orden estándar.

**Paso 7 --- Alias/nickname (bonus):** Herramientas: **What's My Name**, **Sherlock**, **Maigret** → perfil de Xbox con alias **Kronos**.

### Flujo completo de la investigación

Teléfono ↓ TrueCaller (Telegram bot) Nombre parcial → Google → Nombre completo ↓ LinkedIn Empleo + Trayectoria laboral ↓ TuClaseParticular.com Precio/hora ↓ Google (segunda página) Deporte + Federación ↓ PDFs de federación / Imágenes de Google Parte del DNI → iteración con Google Dorks → DNI completo ↓ Correo (encontrado en bridge.bib / LinkedIn / OpenSense) ↓ Have I Been Pwned ↓ LeakRadar → Contraseña filtrada ↓ What's My Name / Sherlock / Maigret → Alias: Kronos

## 4.

Herramientas OSINT usadas en el ejercicio

Herramienta URL Uso en el ejercicio
 ------------------------------- --------------------------- -----------------------------------------------
 **TrueCaller** (bot Telegram) Bot: \@truecallerbot Teléfono → nombre
Google (Dorks + iteraciones) google.com Segundo apellido, PDFs con DNI, precio/hora LinkedIn linkedin.com Empleo actual + trayectoria TuClaseParticular.com tuclaseparticular.com Precio por hora como profesor Bridge.bib bridge.bib Correo electrónico OpenSense opensense.eu Correlación de correo y redes sociales Have I Been Pwned haveibeenpwned.com Filtraciones con el correo LeakRadar leakradar.io Contraseña filtrada PimEyes pimeyes.com Reconocimiento facial para verificar identidad Sherlock GitHub (sherlock-project) Búsqueda de alias/username en redes Maigret GitHub Búsqueda de alias/username en redes What's My Name whatsmyname.app Búsqueda de alias/username en redes Gravatar gravatar.com Perfil asociado al correo OSINTDog osintdog.com Búsqueda adicional de perfil por correo

## 5.

Sherlock y Maigret: búsqueda de usernames

**Sherlock** y **Maigret** son herramientas de línea de comandos (instalables en Kali Linux) que buscan un username en decenas o cientos de redes sociales y plataformas simultáneamente, devolviendo todas las URLs donde ese alias existe.

sherlock nombre_usuario maigret nombre_usuario

Son equivalentes al **What's My Name** web pero ejecutadas desde terminal y automatizables con scripts Bash.

## 6.

Huella digital y derecho al olvido

**Lección del ejercicio:** quien tiene mucha actividad en internet (como el propio profesor Carlos, con varias empresas) tiene una huella digital enorme e imposible de ocultar completamente.

**Derecho al olvido digital:** cualquier persona puede ejercerlo a través de la **AEPD** (*Agencia Española de Protección de Datos*) o mediante servicios especializados como **Removable Group**.

Permite solicitar que se borren datos de páginas web concretas.

### Sin embargo:

- Es un proceso lento y manual (página por página).
- Aunque se borre de una página, otra puede volver a publicarlo.
- Los registros oficiales (partida de nacimiento, registros mercantiles, BORME) son imposibles de eliminar.
- La conclusión del profesor: **jamás se puede desaparecer completamente de internet**.

## 7.

Cierre de la superficie de exposición: Shodan, Censys y FOFA

Repaso rápido de los tres motores de búsqueda de activos para auditorías externas:

### Shodan (shodan.io)

- Búsqueda por tecnología, versión, organización y CVEs asociados.

- Novedad: ahora marca las IPs que son **Honeypots**:

 - Un Honeypot es un servidor trampa con versiones muy vulnerables y muchos puertos abiertos, diseñado para atraer atacantes y estudiar sus técnicas.
 - Se reconocen porque tienen una cantidad anormal de puertos abiertos y CVEs.

Un servidor real nunca tiene tantas vulnerabilidades visibles a la vez.
- Si se ataca un Honeypot, el defensor recopila toda la información del ataque: IPs, herramientas usadas, exploits propios del atacante, incluyendo posibles zero-days.
 - **Importante para Red Team:** evitar atacar Honeypots para no revelar las propias técnicas y herramientas.

- Demostración: búsqueda de "Windows Server 2008 EternalBlue" → millones de servidores reales aún vulnerables.

### FOFA (fofa.info)

- Motor chino, muy completo, con mayor índice de activos que Shodan para algunas tecnologías.

- Demostración en clase: búsqueda de "Open Cloud" (IA local de código abierto):

 - Encontró servidores de particulares con su IA local accesible desde internet sin autenticación.
 - El profesor demostró poder acceder al panel de configuración de uno de estos servidores y modificar sus parámetros.
- También encontró paneles FTP, servidores XAMPP con configuración por defecto, paneles cPanel con la vulnerabilidad de RCE reciente, y Cloudbot panels abiertos.

### Censys (search.censys.io)

- Mayor rendimiento en búsquedas por nombre de organización y certificados TLS.

**Ejercicio propuesto:** buscar "Windows Server 2008" en los tres motores y comparar los resultados para entender por qué hay que usar las tres herramientas de forma complementaria.

## 8.

Geolocalización y triangulación de señal telefónica

Reflexión surgida en clase sobre cómo se localiza a sospechosos digitalmente: - El historial de **Google Maps** si no está configurado como privado puede estar accesible en internet. - La **triangulación de señal telefónica** funciona por hexágonos: cada torre de telefonía cubre un área.

Al conectarse a tres torres consecutivas, se puede calcular la zona de presencia con bastante precisión (no exacta, pero suficiente para seguimiento físico). - **Identificación por IP:** los ISPs guardan registros de qué IP tenía cada cliente en cada momento durante 5 años.

La policía solo necesita pedir al ISP quién tenía esa IP ese día. - El único escudo real frente a esto: **Mullvad VPN** pagada con **Monero** obtenido en P2P (sin registro).

## 9.

### Forense digital: herramientas y distribuciones Linux

Surgido en debate al final de la clase:

- **Kali Linux**: principalmente ofensivo, pero también tiene herramientas forenses.

El repositorio APT de Kali (/etc/apt/sources.list) puede ampliarse añadiendo los repositorios de otras distribuciones especializadas.
- **Kaine Linux** (no "Caine"): distribución basada en Debian con herramientas forenses preinstaladas.

Equivalente a Kali pero orientada a análisis forense.
- **Volatility**: análisis de memoria RAM forense.
- **Autopsy**: análisis de discos e imágenes forenses.
- **ArtOxy (Autopsy)**: funciona mejor en Windows que en Linux.
- **WiFi Pineapple**: dispositivo hardware para ataques Wi-Fi, que el profesor tiene conectado vía cable a **Claude Code** para automatizar ataques.

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
--------------------------------------------- ---------------------------------------------------------------------------------------------------------------
Pimais / Pimai / PinMy **PimEyes** (pimeyes.com) -- motor de búsqueda por reconocimiento facial Trucoler / Truco Oler / Truecaller Telegram **TrueCaller** -- bot de Telegram para identificar números de teléfono Migrait / Mograyt **Maigret** -- herramienta de búsqueda de usernames en múltiples plataformas Sherlock **Sherlock** -- herramienta de búsqueda de usernames (correcto) What's My Name **whatsmyname.app** -- buscador de aliases en redes sociales bridge.bib **BridgeBib** o **bib.bridgebib** -- plataforma de correlación OSINT de perfiles open-sense.eu / Opensense **OpenSense** (opensense.eu) -- herramienta de correlación OSINT en grafos ligradar / League Radar **LeakRadar** (leakradar.io) -- plataforma de credenciales filtradas Hafai Bin / Half-Life Empowerment **Have I Been Pwned** (haveibeenpwned.com) Half-fiving pound **Have I Been Pwned** -- misma herramienta, otra transcripción tus clases particulares **TuClaseParticular.com** -- plataforma para clases particulares con tarifas visibles OSINTomático **OSINTomático** -- comunidad y evento de OSINT en España Ciberpatrolla / Ciberpatrulla **Ciberpatrulla** (ciberpatrulla.com) -- repositorio de herramientas OSINT Removable Group **Removable Group** -- empresa especializada en derecho al olvido digital Kaine / Cayne **Kaine Linux** -- distribución Debian con herramientas de análisis forense Volatility **Volatility Framework** -- herramienta de análisis forense de memoria RAM ArtOxy **Autopsy** -- herramienta de análisis forense de discos HPC **HPC** (Habilitación Personal de Seguridad) -- acreditación del CNI para trabajar con información clasificada AEPD **AEPD** (Agencia Española de Protección de Datos) -- organismo que gestiona el derecho al olvido digital OSIA / grupo OESIA **Grupo OESIA** -- multinacional de tecnología donde trabajó el profesor Pineapple / WiFi Pineapple **WiFi Pineapple** -- dispositivo hardware de Hak5 para auditorías Wi-Fi Claudio / Claud Code **Claude Code** -- herramienta de Anthropic para programación asistida por IA

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../PREWORK/resumen_clase7.md|resumen_clase7]] — Netcat / Reverse Shells, Normativa / GRC, Post-Explotación
- [[resumen_master_clase12.md|resumen_master_clase12]] — Empleabilidad, Netcat / Reverse Shells, Post-Explotación
- [[../MODULO1/resumen_master_clase3.md|resumen_master_clase3]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../MODULO1/resumen_master_clase6.md|resumen_master_clase6]] — Empleabilidad, Netcat / Reverse Shells, Post-Explotación
- [[../PREWORK/resumen_clase2.md|resumen_clase2]] — Netcat / Reverse Shells, Normativa / GRC, Post-Explotación
- [[../MODULO1/resumen_master_clase2.md|resumen_master_clase2]] — Netcat / Reverse Shells, Normativa / GRC, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #empleabilidad #forense #google-dorks #ia #kali #linux #netcat #normativa #osint #post-explotacion #redes #reverse-shell #wifi #windows
