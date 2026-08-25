> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 22**
> **Módulo:** MODULO3
> **Tema:** Clase 22
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 22. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy

## 1.

Contexto y objetivos de la sesión

Esta clase la imparte **Carlos** (el profesor principal), con un enfoque Blue Team: si en las sesiones anteriores se aprende a romper cosas, aquí se aprende qué rastros dejan esas acciones y cómo un forense puede investigarlas.

El objetivo del día es doble:

1. **Parte teórica guiada:** comprender el marco metodológico del forense digital, la cadena de custodia y cómo funciona el malware moderno. 2. **Parte práctica:** laboratorio guiado de análisis de malware usando VirusTotal, **Any.run** y la matriz **MITRE ATT&CK**, con un alumno resolviendo en directo mientras el profesor corrige.

> [!important] **Perspectiva clave:** entender el hacking desde el punto de vista del defensor no solo es útil para el Blue Team; también hace mejor al Red Teamer, porque sabe exactamente qué rastros está dejando.

## 2.

Ramas del forense digital

El forense digital se divide en dos grandes ramas:

**1.

Forense de red** - Análisis del tráfico de red capturado. - Herramienta principal: **Wireshark** (ya visto en clases anteriores). - Permite ver qué comunicaciones hubo, qué protocolos se usaron, desde qué IPs, a qué horas.

**2.

Forense de equipos (host forensics)** Se divide a su vez en dos tipos:

Tipo Memoria Características
 ---------- ----------- --------------------------------------------------------------------------------------------------------
Volátil RAM Se pierde al apagar el equipo.

Contiene procesos activos, conexiones abiertas, credenciales en memoria.

Estático HDD / SSD Persiste aunque se apague.

Contiene ficheros, logs, registros del sistema operativo.

**Herramienta de análisis de memoria volátil:** **Volatility** (para ambos sistemas operativos).

Para extracción de RAM en Linux se usa **LIME** (*Linux Memory Extractor*). **Herramienta de análisis de disco:** **Autopsy** (análisis de imágenes de HDD/SSD).

## 3.

Por qué la memoria RAM es crítica en forense

La RAM contiene en todo momento los **procesos activos** del sistema.

Esto es esencial porque:

- Un proceso malicioso anidado como **subproceso** de un proceso legítimo es una de las técnicas de persistencia más habituales.

En el Administrador de Tareas de Windows esto se ve desplegando la jerarquía de procesos.
- Cuando se hace un análisis forense se toma una **fotografía** del estado de la RAM en ese momento.

Si el sistema se apaga antes de hacer esa fotografía, **todos los procesos se pierden**, incluyendo el rastro del malware.
- **Error crítico muy común:** ante un incidente de ransomware, el instinto es apagar el equipo.

Resultado: se pierde toda la información de los procesos activos, el foco de infección y la cadena de ejecución del malware.

**Lo correcto:** tomar la imagen de RAM **antes** de apagar el equipo.

## 4.

Cadena de ejecución del malware moderno

Un malware moderno no funciona como un ejecutable simple.

La cadena habitual tiene dos variantes:

### Variante clásica:

Ejecutable malicioso → Lanza binarios → Persistencia → Autoborrado

Variante moderna (más habitual hoy):

Ejecutable señuelo (ej. vpn.exe) → Descarga malware 2 por PowerShell → Lanza binarios → Persistencia → Autoborrado

**Por qué se usa esta cadena:** - Los antivirus y EDR se basan en **firmas** (IOC): si el ejecutable inicial tiene una firma conocida, se detecta y se bloquea. - Al descargar el payload real desde una URL a través de PowerShell, el archivo inicial es limpio (no tiene firma maliciosa) y el payload llega y se ejecuta sin pasar por disco de forma convencional. - Tras establecer persistencia, el malware se **autoborta** para eliminar evidencias.

**Técnica de evasión base64:** Un payload codificado en Base64 no tiene strings detectables.

El comando es:

base64 -d <<< "CADENA" | execute

Los antivirus aprendieron a decodificar Base64 para analizarlo.

La respuesta de los atacantes fue la **doble codificación** (Base64 de Base64), y posteriormente la triple.

Hoy en día los antivirus también comprueban múltiples capas.

**Técnica de evasión con caracteres especiales:** Caso real citado: atacantes usaron el carácter chino 自由 (libertad), que en teclados europeos se codifica como espacio en blanco, para construir cadenas que el antivirus no reconocía como maliciosas porque el carácter no existía en su nomenclatura.

## 5.

Sistemas de detección: firmas e IOC

### Antivirus y EDR basados en firmas

Los sistemas de detección (antivirus, EDR, XDR, IPS, IDS) funcionan mediante **firmas** basadas en **IOC** (*Indicators of Compromise*).

Un IOC puede ser: - Una dirección IP conocida como maliciosa. - Un **hash** de un fichero malicioso. - El nombre de un fichero o ruta específica. - Una cadena de texto (string) concreta.

Cuando el antivirus detecta algo malicioso, extrae sus IOC (IPs, hashes, strings, nombres de fichero) y los envía a una **base de datos de firmas** compartida entre todos los fabricantes.

### VirusTotal: el proveedor universal

**VirusTotal** (virustotal.com) fue creado por un desarrollador de Málaga que ofreció un servicio gratuito donde subir ficheros y analizarlos con todos los antivirus del mundo simultáneamente.

Al guardar todos los ficheros maliciosos detectados, construyó **la base de datos de firmas de malware más grande del planeta**.

Hoy es una empresa de Google y es literalmente el **proveedor** de inteligencia de amenazas de Kaspersky, Bitdefender, CrowdStrike, Panda y prácticamente todos los fabricantes.

> [!important] **Importante:** cuando se trabaja para el CNI u otras agencias de inteligencia, **está prohibido subir muestras a VirusTotal**, porque indexar el malware en la base de datos pública alertaría al atacante y revelaría el conocimiento de la herramienta.

### Community Score vs.

Score de antivirus

> [!important] En VirusTotal hay dos métricas clave: - **Score de antivirus:** cuántos motores detectan el fichero como malicioso.

Un malware muy reciente puede tener score 0/70 porque las bases de datos no se han actualizado aún. - **Community Score:** la comunidad de investigadores de seguridad puede marcar un fichero como sospechoso antes de que los motores lo detecten.

Si hay score 0 en antivirus pero 99 en community, es una señal de alerta importante.

## 6.

Cadena de custodia: las reglas del forense judicial

La cadena de custodia es el protocolo que garantiza la integridad de las evidencias para que sean admisibles en un juicio.

Carlos ha visto pruebas rechazadas en juicios por fallos en la cadena de custodia.

### Elementos obligatorios

- **Nombre de la evidencia:** identificación clara de cada fichero/disco.

- **Método de recolección:** cómo, quién y cuándo se recogió la evidencia.

- **Hash del fichero:** usando siempre **SHA-256** (MD5 está roto, SHA-1 es rechazado preventivamente por muchos jueces).

- Dos copias + el original:

 - **Original:** solo para obtener los hashes y las copias.

No se manipula nunca.
 - **Copia de trabajo:** la única que se analiza.

Si se corrompe, se hace otra copia del original.
 - **Copia de seguridad:** se guarda intacta desde el primer momento.

### Trampas que invalidan evidencias

- Timestamps del sistema con hora incorrecta → la evidencia es manipulable.
- No poner precinto físico en el dispositivo al recogerlo → se puede alegar que fue manipulado durante el transporte.
- Diferencia entre creation time y modified time en los metadatos del fichero de evidencia y los timestamps del informe → invalida el informe completo.
- Más de 24 horas entre la recogida de la evidencia y su etiquetado.
- No grabar en vídeo el proceso de recogida de evidencias.

**Caso real:** Carlos contó haber contado caracteres de hashes en informes de la parte contraria para encontrar un error y desestimar las evidencias.

### El forense en juicios

En España, las Fuerzas y Cuerpos de Seguridad del Estado (Guardia Civil, Policía Nacional, Policía Municipal) tienen perfiles informáticos, pero según el profesor son técnicamente débiles por proceder de oposiciones generalistas.

Para casos complejos, el Estado **subcontrata a empresas privadas** (como **S21sec**) cuyos técnicos actúan como peritos judiciales.

El informe forense lo presenta la fiscalía; si hay que defenderlo, el técnico comparece como **perito judicial adscrito al juzgado**.

INCIBE no investiga directamente --- deriva los casos a los cuerpos correspondientes según el tipo de incidente.

## 7.

Timestamps y metadatos en el análisis forense

La diferencia entre timestamps es crucial:

Timestamp Significado
 ------------------------------- ----------------------------------------------------
Creation time Cuándo se creó el fichero Modified time Última modificación (puede ser lectura o escritura) First submission (VirusTotal) Primera vez que se subió a VirusTotal First seen in the wild Primera vez detectado en uso real en Internet

**Análisis del caso del laboratorio:** - El malware se creó el **24 de septiembre de 2020**. - Se subió a VirusTotal por primera vez el **15 de octubre de 2020** (20 días después). - Se vio por primera vez "in the wild" (en uso real) **2 meses después** de la creación.

**Interpretación:** el malware se creó con un objetivo específico (no para distribución masiva), fue probado internamente durante 20 días, atacó a una organización concreta, que lo detectó y lo subió a VirusTotal.

Una vez indexado y detectable, el atacante lo liberó masivamente para aprovechar el tiempo de desarrollo ya invertido.

**Técnica de inteligencia:** el gap entre creación y despliegue puede indicar que los atacantes pasaron ese tiempo refinando el malware contra los antivirus de la víctima, usando muestras de esos mismos antivirus en su laboratorio privado.

Cómo saber qué antivirus usa una empresa sin acceso a sus sistemas: descargar documentos públicos de la empresa (PDFs en Google), analizar sus metadatos con **FOCA** → revelan sistema operativo, versión de software, hostname, usuario.

## 8.

Herramientas del laboratorio práctico

### CyberDefenders

Plataforma de laboratorios Blue Team con escenarios forenses guiados.

Los laboratorios usados en clase pertenecen a la categoría de análisis de malware.

Los alumnos tienen que responder preguntas concretas investigando con las herramientas.

### VirusTotal (virustotal.com)

El flujo de análisis en VirusTotal: 1.

Subir el fichero o pegar el hash. 2.

Ver el **score** de motores que lo detectan (ej. 61/70 = muy malicioso). 3. **Pestaña Details → History:** fechas de creación, primera subida, última subida, primera vez in the wild. 4. **Pestaña Relations:** URLs y dominios con los que el malware contacta (**C2 servers**), ficheros relacionados (.php, .dll...). 5. **Nombres del malware:** los distintos antivirus usan nombres distintos; la familia coincidente revela el tipo (RAT, ransomware, stealer...). - En el laboratorio: **Yellow Cockatoo RAT** (Remote Access Trojan).

### Any.run (any.run)

**Sandbox de análisis dinámico** --- ejecuta el malware en un entorno controlado y captura todo lo que hace: procesos creados, ficheros modificados, tráfico de red, claves de registro, DLLs cargadas.

Secciones clave de Any.run: - **Árbol de procesos:** jerarquía de procesos creados por el malware. - **Connections:** tráfico de red generado (URLs, IPs, peticiones HTTP). - **Files:** ficheros creados, modificados y eliminados. - **Command lines (CMD):** comandos ejecutados directamente en CMD. - **Técnicas MITRE ATT&CK:** Any.run asigna automáticamente IDs de la matriz MITRE a cada comportamiento detectado.

**Del laboratorio:** el malware analizado: 1.

Ejecutó vpn.exe como señuelo → descargó el payload real. 2.

Cargó una DLL maliciosa (primera librería cargada tras infección). 3.

Accedió a cookies de sesión del navegador (robo de credenciales). 4.

Leyó el password store del sistema. 5.

Usó cifrado **RC4** para ofuscar strings de configuración codificadas en Base64. 6.

Ejecutó cmd.exe con el comando: timeout /t 5 seguido de borrado de ficheros en %AppData%\\ProgramData → **autoborrado** en 5 segundos. 7.

Se autodesinstaló para no dejar evidencias.

**RC4** (*Rivest Cipher 4*): algoritmo de cifrado de flujo.

Muy usado en malware porque el código completo cabe en \~30 líneas, no tiene dependencias externas, y dificulta el análisis estático (las cadenas de configuración aparecen cifradas en lugar de en texto claro).

### MITRE ATT&CK

Matriz de tácticas y técnicas de ataque con IDs estandarizados.

En el laboratorio se usó para identificar la técnica exacta de robo de credenciales:

- **Credential Access** → **Credentials from Password Stores** → sub-técnica **Steal Web Session Cookie**
- ID buscado: T1555 (Credentials from Password Stores) con sub-técnica de cookies de sesión.

Any.run incluye directamente los IDs de MITRE en su análisis, lo que permite cruzar las acciones observadas con la taxonomía estándar del sector.

## 9.

Dinámica de la práctica libre

El segundo bloque fue una práctica libre del laboratorio **Yellow Rut Lab** (CyberDefenders).

El profesor seleccionó a un alumno para resolver el laboratorio en directo compartiendo pantalla, con el resto del grupo siguiéndolo en paralelo.

Las preguntas del laboratorio cubrían:

## 1.

Identificar el nombre del malware y su familia. 2.

Determinar la fecha de creación del malware (VirusTotal → Details → History → Creation time). 3.

Identificar el servidor C2 con el que se comunica el malware (VirusTotal → Relations → Contacted URLs). 4.

Identificar la primera biblioteca (DLL) cargada tras la infección (Any.run → árbol de procesos). 5.

Identificar la clave RC4 usada para descifrar strings codificadas en Base64 (Any.run → análisis de cadenas). 6.

Identificar qué directorio señala el malware para el borrado (CMD → comando de autoborrado). 7.

Identificar cuántos segundos tarda el malware en autoborarse (parámetro /t del timeout). 8.

Identificar la técnica MITRE de robo de contraseñas (MITRE ATT&CK → Credential Access → T1555).

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------
Wizark / Wizar **Wireshark** -- analizador de tráfico de red volátil / estático / bolatility **Volatility** -- herramienta de análisis de memoria RAM forense la memoria volátil de Linux **LIME** (*Linux Memory Extractor*) -- herramienta de extracción de volcados de RAM en Linux Autopsi **Autopsy** -- herramienta de análisis forense de discos duros e imágenes ios / IOC **IOC** (*Indicator of Compromise*) -- indicador de compromiso (hash, IP, nombre de fichero...) CDR / EDR / DDR **EDR** (*Endpoint Detection and Response*) -- sistema de detección y respuesta en endpoints DLC / DLL / LLL **DLL** (*Dynamic Link Library*) -- librería dinámica de funciones en Windows cloud decode / Claudia / Claude **Claude** (Anthropic) -- IA usada para resolver dudas durante la práctica annie punto ran / lenny run **Any.run** -- sandbox de análisis dinámico de malware online ciberdefender / Cyberdefender **CyberDefenders** -- plataforma de laboratorios Blue Team RC 4 / más de 4 **RC4** (*Rivest Cipher 4*) -- algoritmo de cifrado de flujo ligero, frecuente en malware la patricia Mitre / Mitre **MITRE ATT&CK** -- matriz de tácticas y técnicas de ataque con IDs estandarizados Yellow Coco tu Rat / Yellow Cocatoo **Yellow Cockatoo RAT** -- nombre del malware analizado en el laboratorio (Remote Access Trojan) steel / steal **Credential Stealer** -- tipo de malware que roba credenciales almacenadas password stop **Password Stores** -- almacenamiento de contraseñas del sistema (técnica T1555 de MITRE) Rust tiempo muerto **timeout /t 5** -- comando Windows que espera N segundos antes de ejecutar el siguiente comando in the wild **In the wild** -- término del sector que indica que el malware ha sido detectado en uso real fuera de entornos controlados FOCA de Chema Alonso **FOCA** -- herramienta de extracción y análisis de metadatos de documentos públicos S21 red / On Red Tribal **S21sec** -- empresa española de ciberseguridad que colabora con Guardia Civil, Policía Nacional y CNI INCIBE **INCIBE** -- Instituto Nacional de Ciberseguridad de España; agrega y deriva alertas a los cuerpos competentes (no investiga directamente) CCN / CNI **CCN-CERT** / **CNI** -- Centro Criptológico Nacional / Centro Nacional de Inteligencia Charcha / Charchas Apodo para el alumno que compartió pantalla en la práctica (Chema)

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.