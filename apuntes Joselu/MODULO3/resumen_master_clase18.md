> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 18**
> **Módulo:** MODULO3
> **Tema:** Clase 18
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 18. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Esta sesión la imparte Carlos Gómez y tiene tres ejes bien diferenciados que terminan convergiendo.

Arranca con un anuncio que cambia el temario del máster: habrá un módulo nuevo de hacking a LLMs.

Sigue con una inmersión en normativa de ciberseguridad (ISO 27001, ISO 42001, NIS2) protagonizada también por César, un alumno que demuestra en directo lo que se puede construir con IA en pocas semanas.

Y cierra con la corrección detallada del laboratorio de forense web, donde Castillo aprovecha para introduci r SQL Injection desde los fundamentos: tablas de verdad, operadores booleanos, queries SQL y por qué OR 1=1 rompe todo.

### Módulo nuevo: Hacking a LLMs Castillo anuncia que incorpora un módulo de hacking a modelos de lenguaje (LLMs).

### El motivo: el nivel y la actitud del grupo lo justifican, y el tema es cada vez más relevante en el sector.

El módulo cubrirá fundamentos de IA (arquitecturas, contexto, memoria, modelos), hacking a LLMs con laboratorio propio, y la ISO 42001 (normativa de IA).

La razón de inclui r la ISO 42001 con solo 38 controles es que muy poca gente la tiene y abre puertas directamente.

Un matiz importante sobre la práctica con LLMs: el prompt injection no es reproducible.

El mismo prompt puede dar resultados distintos en el mismo modelo porqu e la IA no es determinista.

Eso hace que los laboratorios de hacking a IA sean necesariamente individuales: lo que a uno le funciona puede no funcionarle a otro.

Normativa: ISO 27001, ISO 42001 y NIS2 La normativa no es un adorno académico, es lo que just ifica económicamente la mayor parte del trabajo en ciberseguridad.

La lógica es la siguiente: una empresa pequeña que quiere trabajar con una empresa crítica (energía, banca, infraestructura) tiene que demostrar que cumple ciertos controles de seguridad.

E sa demostración se hace o mediante un Excel de noventa y tres preguntas que hay que rellenar cada vez, o con el sello de una ISO.
- ISO 27001: estándar de ciberseguridad, 93 controles.

Justifica la existencia del pentesting,
la monitorización 24/7 y la intel igencia de amenazas.

Certificar no es opcional para quien quiera trabajar con empresas del sector crítico
- ISO 42001: estándar de IA, 38 controles.

Muy poca gente la tiene.

Castillo acaba de
comprarse el examen
- NIS2: directiva europea de ciberseguridad, obl igatoria (no voluntaria como la ISO).

Afecta a
empresas críticas y, por extensión, a toda su cadena de suministro.

España lleva ventaja porque el Esquema Nacional de Seguridad (ENS) lleva años activo y está siendo adoptado como referencia a nivel europeo La cadena de suministro es el vector clave que conecta normativa con negocio real: si Iberdrola tiene que cumplir NIS2, tú como proveedor suyo también tienes que cumplir.

El contrato de un millón no existe si no tienes el sello.

Las cuatro fases de la norma tiva son implementación, auditoría interna, firma y auditoría externa.

Las dos primeras las puede hacer cualquiera con conocimiento.

La firma de la auditoría interna

requiere certificación (Certiprof recomienda Castillo: económica, tipo test, válida para f irmar).

La auditoría externa solo la pueden hacer entidades reguladas como AENOR, BSI o TUV Rheinland.
> [!important] - La idea clave: una vez manejas una norma de ciberseguridad, manejas todas, porque
comparten entre el 70 y el 80 por ciento de los controles.

Hacer ENS ni vel medio equivale aproximadamente a hacer ISO 27001 más NIS2 con un 20 por ciento de esfuerzo adicional

Demostración en directo: herramientas construidas con IA César, alumno de la convocatoria, muestra dos herramientas propias construidas en un mes con Python, PostgreSQL, Google AI Studio (Gemini) y APIs de terceros.

La primera es una plataforma de gobernanza y normativa que mapea controles entre ISO 27001, ENS y otras normas, genera análisis de riesgos, impacto financiero, reportes de DAFO y checklists de cumplimiento.

La segunda es una herramienta de vigilancia digital que monitoriza dominios para detectar typosquatting y phishing, cruza con LeakRadar para credenciales filtradas, y permite lanzar takedowns automáticos contra dominios fraudulentos.

Ambas trabajan con clientes reales, incluyendo administraciones públicas.

Tiempo de desarrollo: una semana para la de hacking, un mes para la de gobernanza.

El punto pedagógico que Castillo subraya: esto es lo que la práctica 1 del máster pide.

No hace falta ser programador.

Hace falta saber lo que se quiere construir, conocer las APIs disponibles, y saber darle instrucciones precisas a la IA.

La diferencia entre una herramienta mediocre y una útil está en la especificidad del prompt y en conocer el dominio.

Corrección del laboratorio: Web Investigation (SQL Injection) La corrección del PCAP de la sesión anterior sirve de excusa para introducir SQL Injection desde cero.

José Manuel hace la corrección en vivo.

Identificar el fichero vulnerable Filtrando por la IP del atacante y el protocolo HTTP en Wireshark, se observa navegación normal al principio (GET a index, contacto, categorías) seguida de búsquedas en el buscador.

La extensión .php en la URL ya dice que el servidor es Linux con Apache.

El fichero vulnerabl e es search.php, visible en la URL de las peticiones GET al buscador.

Detectar el intento de inyección Las primeras búsquedas son normales: "word", "book", respuestas 200 OK.

Cuando aparece %27 en la URL, algo cambia. %27 es URL encoding de la comilla simp le.

La respuesta del servidor pasa a ser 500 Internal Server Error.
- %27 equivale a la comilla simple
- %20 equivale a un espacio
- %3D equivale al signo igual

Un 500 tras una comilla simple significa que el servidor ha intentado ejecutar la query SQL con la comilla rota y ha crasheado.

La aplicación no sanitiza la entrada.

Eso es el indicio de vulnerabilidad, no el ataque en sí.

Cómo funciona OR 1=1 Una query SQL de buscador tiene esta forma: SELECT title FROM libros WHERE name = 'harry potter' El valor entre comillas simples viene directamente del input del usuario.

Si el usuario introduce una comilla simple, rompe la sintaxis: las comillas quedan impares y el motor SQL no puede procesar la instrucción.

Para explotar esto, el atacante construye un payload que cierra la comilla del parámetro e introduce una condición adicional con OR.

La lógica es la siguiente: se busca un nombre vacío, seguido del operador OR y una condición que siempre sea verdadera (que un número sea igual a sí mismo), seguido de un comentar io SQL con dos guiones que anula todo lo que venga después.

Como el operador OR devuelve verdadero si al menos uno de sus operandos es verdadero, y la segunda condición siempre se cumple, la query devuelve todos los registros de la tabla en lugar del libro buscado.

Una tabla de verdad simplificada del operador OR:
- Condición A falsa + Condición B verdadera → resultado verdadero
- Condición A verdadera + Condición B verdadera → resultado verdadero
- Condición A falsa + Condición B falsa → resultado falso
Como 1=1 nunca puede ser falso, el resultado del OR siempre será verdadero, y la base de datos devolverá todo su contenido.
> [!important] - La idea clave: el atacante no está buscando un libro, está inyectando lógica SQL en el
parámetro del buscador.

Si el servidor ejecuta esa ló gica sin sanitizar, devuelve toda la base de datos, no solo el libro pedido Confirmar el éxito del ataque El primer paquete donde el atacante obtiene un 200 OK tras meter caracteres especiales es el punto exacto donde la inyección surte efecto.

A partir de ahí, el atacante usa SQLMap (herramienta automatizada que prueba cientos de payloads) para enumerar el esquema de la base de datos, acceder a information_schema (la tabla maestra que contiene la estructura de todas las bases de datos del servidor) y event ualmente volcar credenciales u otros datos sensibles.

El fichero information_schema aparece visible en Wireshark si vamos a Archivo → Exportar objetos → HTTP.

Para filtrar en Wireshark solo las interacciones HTTP del atacante: ip.src == 111.224.250.131 && http

Recapitulación integrada

Esta sesión construye sobre varios hilos al mismo tiempo.

Ahora entendemos que la normativa no es burocracia: es el motor económico que hace que existan los trabajos de ciberseguridad, y que dominar una ISO equivale a dominar todas.

Sabemos que construir herramientas útiles con IA no requiere ser programador, sino tener criterio sobre lo que se quiere construir y conocimiento del dominio.

Y hemos cerrado el análisis forense del laboratorio web entendiendo por qué un 500 Intern al Server Error tras una comilla simple es una bandera roja, por qué OR 1=1 siempre devuelve verdadero, y cómo un atacante pasa de un indicio a una exfiltración completa de base de datos.

La próxima sesión arranca con Metasploitable y las primeras explotac iones reales.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../PREWORK/resumen_clase8.md|resumen_clase8]] — IA en Ciberseguridad, Normativa / GRC, SQL Injection
- [[../../apuntes Andres/15.07.2026 IA Introducción y Vibe Coding.md|15.07.2026 IA Introducción y Vibe Coding]] — IA en Ciberseguridad, Linux, SQLMap
- [[../MODULO2/resumen_master_clase16.md|resumen_master_clase16]] — IA en Ciberseguridad, SQL Injection, SQLMap
- [[../../Apuntes/14 - IA en Ciberseguridad/IA en Ciberseguridad.md|IA en Ciberseguridad]] — Certificaciones, IA en Ciberseguridad, Linux
- [[resumen_master_clase22.md|resumen_master_clase22]] — IA en Ciberseguridad, Linux, Redes
- [[../PREWORK/resumen_clase9.md|resumen_clase9]] — Certificaciones, IA en Ciberseguridad, Redes

### 🛠️ Herramientas

- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #certificaciones #forense #ia #linux #metasploitable #normativa #redes #sqli #sqlmap #wireshark
