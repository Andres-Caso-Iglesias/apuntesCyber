> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 8**
> **Módulo:** MODULO2
> **Tema:** Clase 8
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 8. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1.

Estructura del temario

La sesión cubre cuatro bloques principales: 1. **Marco legal del OSINT** --- qué es legal, qué es ilegal, qué es "alegal". 2. **Cadena de custodia y validez de pruebas** --- OSINT como evidencia judicial. 3. **Ciclo de inteligencia OSINT** --- cómo estructurar una investigación. 4. **Parte práctica:** Deep Web con TOR/BreachForums, Google Dorks y superficie de exposición.

## 2.

Marco legal del OSINT

### Reconocimiento pasivo vs. activo

Tipo Descripción Legalidad
-------- ----------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------
Pasivo Consulta información ya disponible sin interactuar con la infraestructura objetivo (buscar en Shodan, leer en Google, consultar BreachForums) Legal (salvo excepciones) Activo Interacción directa con la infraestructura objetivo (lanzar Nmap, hacer ping, enviar paquetes) Solo legal con autorización explícita por contrato

El término técnico para la parte activa de la enumeración es **footprinting** (incluye fingerprinting y escaneo activo).

**Regla de oro:** todo en legislación se basa en la **autorización explícita**.

Sin contrato firmado, ninguna acción activa es legal; sin embargo, las acciones pasivas sobre fuentes abiertas son generalmente legales.

### Límites concretos

- **Suplantación de identidad:** crear un perfil falso usando la cara real de una persona es ilegal.

Crear un perfil con imagen generada por IA que se parezca pero no sea la persona real es una zona gris legal.
- **Credenciales filtradas:** consultarlas en plataformas como LeakRadar o Dehashed es *alegal* (nadie te va a detener si lo tienes en el ordenador, pero tenerlas y usarlas es ilegal).

El Ministerio de Defensa español gastó 15 millones en licencias de estas plataformas --- es un ejemplo de uso legal dentro de un contexto profesional autorizado.
- **Nmap a servidores sin permiso:** completamente ilegal.

En un laboratorio controlado o con contrato firmado, es el primer paso de cualquier auditoría.

### El concepto de "alegal"

Existe una zona gris entre legal e ilegal que el profesor llama "alegal": acciones que nadie va a perseguir activamente si no dejas rastros, pero que técnicamente infringen la ley.

El límite práctico es: **no te pillen** y **si tienes contrato firmado que lo cubra, estás limpio**.

## 3.

Cadena de custodia y validez de pruebas

### Por qué es crítica en OSINT

Las pruebas obtenidas por OSINT pueden usarse en juicios, pero son muy fáciles de invalidar si no se gestionan correctamente.

El profesor ha sido perito de la parte contraria y ha conseguido que se rechazaran decenas de evidencias por defectos técnicos.

### Requisitos de una evidencia OSINT válida

**1.

Reproducibilidad:** la evidencia solo es válida si cualquier persona puede seguir los mismos pasos y llegar al mismo resultado.

Si una evidencia clave desaparece (ej. una foto de Instagram borrada), se rompe la cadena y el informe pierde validez.

**2.

### Timestamp correcto:** la captura de pantalla debe incluir la fecha y hora real del sistema (no manipulada).

Si el timestamp del ordenador está cambiado, la evidencia es manipulable y puede ser invalidada.

El profesor describe haber visto 54 evidencias rechazadas por tener el reloj del sistema redondeado en la barra de tareas.

**3.

Persistencia (mínimo dos fuentes):** toda evidencia debe estar respaldada por al menos dos fuentes independientes.

Si una fuente desaparece, la otra mantiene la reproducibilidad.

**4.

Hash de integridad:** cada fichero de evidencia debe tener su hash calculado y documentado: - **MD5:** roto a nivel práctico.

Dos ficheros diferentes pueden generar el mismo MD5.

Nunca usarlo. - **SHA-128 (SHA-1):** roto solo a nivel teórico, no en la práctica, pero muchos jueces lo rechazan preventivamente. - **SHA-256:** el estándar actual.

Robusto.

Usar siempre.

**Truco de la defensa:** basta con mencionar al juez que el algoritmo de hash usado tiene vulnerabilidades teóricas para que, por ignorancia técnica, invalide la evidencia.

Por eso SHA-256 es imprescindible.

### Caso real: investigación Bellingcat sobre el GRU

El grupo de investigación periodística **Bellingcat** desveló información clasificada sobre el GRU (inteligencia militar rusa) utilizando únicamente OSINT y fuentes abiertas.

Es el caso de referencia para entender el poder del OSINT como herramienta investigadora legítima.

## 4.

Ciclo de inteligencia OSINT

El ciclo tiene cinco pasos y se ejecuta en **bucle**, no de forma lineal:

Objetivo → Recolección → Filtrado → Análisis → Feedback → (volver a Objetivo)

1. **Objetivo (PIR --- Priority Intelligence Requirements):** el paso más crítico.

Un objetivo mal definido lleva a recopilar información irrelevante.

Ejemplo: "quiero saber todo sobre el CFO" es demasiado vago. "¿Tiene vínculos con sociedades en jurisdicciones offshore?" es un PIR concreto y accionable. 2. **Recolección:** extracción de datos de fuentes abiertas (Shodan, Google Dorks, redes sociales, BreachForums, bases de datos públicas). 3. **Filtrado:** de cientos de resultados, seleccionar los que son relevantes para el PIR.

Sin filtrado, el ruido ahoga la señal. 4. **Análisis:** interpretar la información filtrada y construir el "storytelling" con pruebas encadenadas. 5. **Feedback y bucle:** la diferencia entre un junior y un senior es este paso.

El junior termina en el análisis; el senior vuelve al objetivo con la información ya filtrada para formular nuevas preguntas más precisas y hacer otra ronda de búsqueda.

Cada iteración da una capa más profunda de información.

**Ejemplo cotidiano del bucle:** la historia de la amiga que descubrió que su novio le era infiel mediante Instagram: - Historias del novio → identifica la discoteca → seguidores de la discoteca → perfil de la persona → imagen con ella → persona que la acompaña → descubrimiento final.

Cuatro iteraciones del ciclo en lugar de una sola búsqueda superficial.

**OSINT aplicado en contextos no técnicos:** - RRHH de empresas IBEX35 contratan OSINT para due diligence de directivos: vínculos offshore, litigios, huella digital con pensamiento político/religioso, relaciones con accionistas \>3%. - Partidos políticos tienen equipos de 20-30 personas dedicadas exclusivamente a OSINT de la competencia. - El periodismo de investigación usa OSINT masivamente (caso Coldo-Ábalos).

## 5.

Deep Web / Dark Web con TOR

### TOR (The Onion Router)

- Navegador gratuito de **torproject.org** para acceder a páginas .onion.
- Funciona mediante saltos entre nodos de la red (cada nodo solo conoce el anterior y el siguiente).
- **Dato crítico:** el 80% de los nodos activos pertenecen al FBI u otros organismos gubernamentales.

El nodo de salida puede descifrar el contenido del tráfico.
- Para mayor anonimato: VPN **Mullvad** pagada con **Monero** (criptomoneda de privacidad) adquirido en P2P (sin identificación).

### BreachForums

Principal foro de la Deep Web para profesionales de ciberseguridad.

Contiene: - **Databases:** bases de datos robadas de empresas (Travel Club, Airbnb España, Basic Fit, etc.).

Algunas gratuitas, otras de pago con créditos pagables en crypto. - **Stealer logs:** registros de infostealers (malware que roba credenciales). - **Código fuente:** de malware, ransomware, herramientas. - **Cuentas comprometidas:** Netflix, Spotify, servicios de streaming. - **Docsets (doxing):** compilaciones de información personal de individuos. - **Walkthrough de máquinas de Hack The Box** (no publicables hasta que estén retiradas).

**Sistema de reputación del foro:** los usuarios tienen rangos (Miembro, Dios, Baneado).

Para contratar exploits o bases de datos, se busca a usuarios con rangos altos y reputación verificada.

**Para registrarse:** usar ProtonMail u otro correo anónimo (los temporales suelen estar bloqueados).

### HiddenWiki (hiddenwiki.org)

Directorio de URLs .onion organizadas por categoría.

Muchos enlaces están desactualizados o caídos.

Permite encontrar marketplaces, foros especializados y otros recursos de la Dark Web.

## 6.

Google Dorks (búsquedas avanzadas)

Los **Google Dorks** son operadores avanzados de búsqueda que permiten filtrar resultados con gran precisión.

Se pueden usar en Google, Bing, DuckDuckGo y Yandex (con resultados diferentes en cada uno).

### Operadores principales

Operador Sintaxis Uso
 ------------------ ---------------------------- -----------------------------------------------------------------
site: site:repsol.com Solo resultados del dominio indicado; también revela subdominios inurl: inurl:admin URL que contiene la cadena indicada intitle: intitle:login Título (H1-H5) de la página contiene la cadena intext: intext:password Cuerpo del texto de la página contiene la cadena filetype: filetype:pdf Busca archivos de ese tipo concreto \"frase exacta\" \"contraseña admin\" Busca la cadena literal entre comillas or site:pp.es or site:psoe.es Agrupa búsquedas de varios sitios
 **-** (menos) admin -login Excluye términos del resultado
\* (asterisco) site:\*.repsol.com Comodín para cualquier subdominio

### Combinaciones y ejemplos en clase

site:repsol.com → Todos los subdominios e índice de Repsol site:psoe.es inurl:admin → Paneles de administración del PSOE site:pp.es filetype:pdf intext:password → PDFs del PP con la palabra "password" site:gobierno.es filetype:sql → Posibles dumps de bases de datos del gobierno intitle:m.rajoy → Noticias con "m.rajoy" en el titular

**Demostración con** site:psoe.es**:** se obtuvieron subdominios como electopsoe.es, cuarentacongreso.psoe.com, mapadelavergüenza.psoe.es, la intranet de acceso, formularios de microcréditos y la plataforma de donaciones.

**Automatización:** los Google Dorks se pueden automatizar con scripts Bash o Python para hacer búsquedas masivas y descargar todos los ficheros encontrados.

La herramienta **FOCA** (de Chema Alonso) automatiza la extracción y análisis de metadatos de documentos encontrados mediante Dorks.

### GHDB (Google Hacking Database)

Disponible en **exploit-db.com/google-hacking-database** --- biblioteca de Dorks ya construidos para encontrar paneles de admin expuestos, ficheros de configuración, credenciales en texto claro, versiones vulnerables, cámaras IP sin autenticación, etc.

## 7.

Superficie de exposición: motores de búsqueda de activos

Además de Google Dorks, para mapear la superficie de exposición externa de una organización se usan:

Herramienta URL Especialidad
 ----------------- -------------------- -------------------------------------------------------------------------
Shodan shodan.io Dispositivos IoT, servicios, versiones, CVEs Censys search.censys.io Dominios, certificados TLS, infraestructura FOFA fofa.info Motor chino; muy completo y con API Zoomeye zoomeye.org Alternativa china a Shodan Wayback Machine web.archive.org Versiones históricas de páginas web (páginas eliminadas, antiguas rutas) OSINT Framework osintframework.com Directorio completo de herramientas OSINT organizadas por categoría

## 8.

LeakRadar: herramienta nueva de credenciales filtradas

**LeakRadar** (leakradar.io) es la alternativa más reciente y completa a Dehashed para buscar credenciales filtradas por dominio.

Permite filtrar por \@domain.com directamente desde el menú lateral.

### Precio aproximado: 30€/mes.

Demostrado en clase buscando \@repsol.com.

## 9.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
--------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------
Oisin / o Sint / o cintas **OSINT** (*Open Source Intelligence*) Ossint / Ossinting **OSINT** -- inteligencia en fuentes abiertas Hossin / hosting En este contexto, el profesor usa "hosting" para referirse a **OSINT pasivo** (buscar información sin interactuar con la infraestructura) Haffa Bean Pounder / HuffaBeenPounded **Have I Been Pwned** (haveibeenpwned.com) Haset / Hese **Dehashed** -- plataforma de contraseñas filtradas LickRadar / Leak Radar **LeakRadar** (leakradar.io) -- herramienta de credenciales filtradas Bridge Forums / Dark Forums **BreachForums** -- foro principal de la Deep Web Haidenwiki / Heidenwiki **HiddenWiki** (hiddenwiki.org) -- directorio de páginas .onion Mulbat / mullbat **Mullvad** -- VPN recomendada por privacidad Monero **Monero (XMR)** -- criptomoneda de privacidad; no rastreable Adyweb / AdiWeb **Dark Web** -- parte de la Deep Web accesible solo por TOR Bellincat / Bellingcat **Bellingcat** -- grupo de investigación periodística con OSINT GRU **GRU** -- Inteligencia militar rusa (Главное Разведывательное Управление) PIR / Pir **PIR** (*Priority Intelligence Requirements*) -- objetivos prioritarios de inteligencia WordDocs / Weldorks **Google Dorks** -- operadores avanzados de búsqueda en motores de búsqueda FileType / file type filetype: -- operador de Google Dorks para buscar ficheros por extensión FOCA de Eche Malonso **FOCA** (Fingerprinting Organizations with Collected Archives) -- herramienta de análisis de metadatos de **Chema Alonso** Wayback Machine **Wayback Machine** (web.archive.org) -- archivo histórico de páginas web timestamp **Timestamp** -- marca de tiempo que indica cuándo se creó o modificó un fichero o evidencia SHA-128 **SHA-1 (SHA-128)** -- algoritmo de hash roto a nivel teórico UCO **UCO** (Unidad Central Operativa) -- unidad de investigación de la Guardia Civil española BADU **Badoo** -- red social de citas donde se filtraron credenciales corporativas por uso del correo de empresa

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/02 - Sistemas Operativos/Migrar VM VirtualBox a VMware.md|Migrar VM VirtualBox a VMware]] — IA en Ciberseguridad, Linux, Nmap
- [[resumen_master_clase13.md|resumen_master_clase13]] — IA en Ciberseguridad, Linux, OSINT
- [[resumen_master_clase10.md|resumen_master_clase10]] — IA en Ciberseguridad, Linux, OSINT
- [[../PREWORK/resumen_clase14.md|resumen_clase14]] — IA en Ciberseguridad, Linux, OSINT
- [[../../Apuntes/02 - Sistemas Operativos/Linux - Bash Scripting.md|Linux - Bash Scripting]] — Forense Digital, Linux, Redes
- [[resumen_master_clase11.md|resumen_master_clase11]] — IA en Ciberseguridad, Nmap, OSINT

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Nmap|Nmap]]

> #forense #google-dorks #hack-the-box #ia #linux #nmap #osint #redes
