> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 50**
> **Módulo:** MODULO3
> **Tema:** Clase 50
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 50. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

Sesión con estructura de **debate abierto** más que de clase magistral.

El hilo conductor es la **evolución histórica y técnica de la IA**: desde los árboles de decisión estáticos hasta las redes neuronales con autoaprendizaje, pasando por grafos relacionales y ontologías vectoriales.

La segunda mitad es una **demostración en vivo con Obsidian y Neo4J** usando un dataset de cien mil coches, que ilustra la diferencia crucial entre tener datos *organizados* y tener datos que *razonan*.

La sesión conecta con la clase anterior de vibe coding y sienta las bases conceptuales para el módulo de prácticas de verano.

# Por qué ha explotado la IA ahora --- de los árboles de decisión a las redes neuronales

La IA existía hace doce años como concepto académico, pero era un **árbol de decisión glorificado**: `if` anidados (si el input contiene "dolor", haz esto; si además "rodilla", esto otro) que se vendía como IA.

El salto real ocurrió con **GPT-3.5**, el primer modelo que **razona en lugar de categorizar**.

La diferencia no es de grado sino de naturaleza: el árbol de decisión busca la rama correcta; la red neuronal genera una respuesta que no existía previamente en su estructura.

Y una vez que ese primer modelo funcionó, se usó para algo que aceleró todo: **generar datasets**.

Lo que antes requería meses de etiquetado humano, ahora GPT lo mapea y clasifica automáticamente.

Por eso los modelos nuevos se entrenan sobre datasets que el modelo anterior ayudó a construir.

> [!important] > **Idea clave:** la IA ha entrado en un ciclo de retroalimentación donde cada generación de modelos acelera la creación de los datos que entrenarán a la siguiente.

Por eso la evolución es exponencial y no lineal.

# Cómo aprende una red neuronal --- pesos, capas y AB testing

El mecanismo de aprendizaje se explicó con el **Tetris** como ejemplo.

Cada posición del tablero con una pieza concreta es un escenario.

Para cada escenario, distintas personas puntúan del 1 al 10 cada movimiento posible.

La red registra esas puntuaciones como **pesos ponderados**.

Con suficientes ejemplos etiquetados, construye una regla interna que aplica a escenarios que nunca ha visto.

Las **capas** de la red no son otra cosa que niveles de profundidad del dato.

En una red de coches: capa 1 marca (peso alto), capa 2 modelo (peso alto), capa 3 motor (peso medio), capa 4 color (peso bajo).

Un dato entra, pasa por cada capa que lo filtra según sus pesos, y sale un output.

El **autoaprendizaje** ocurre cuando la red genera conexiones que nadie le programó: detecta un patrón no observado por humanos y crea un nodo nuevo.

Nadie sabe exactamente qué pasa dentro del modelo durante ese proceso, ni siquiera los creadores de los algoritmos.

Se sabe que aprende, no cómo exactamente.

> **Metáfora útil:** un árbol de decisión es un mapa de carreteras (de A a B, coges esta autopista).

Una red neuronal es un conductor con experiencia: puede llegar de A a B por una ruta que nunca nadie trazó porque ha detectado un patrón que el mapa no muestra.

# Datasets --- la materia prima que determina la calidad del modelo

El dataset es el factor **más importante** de cualquier entrenamiento, por encima del hardware y del algoritmo.

Tres requisitos para que sea útil:

- **Etiquetado:** cada dato lleva una marca que dice qué es o cuánto vale.
- **Ejemplos negativos:** para entrenar un detector de toros necesitas toros etiquetados como toros, pero también vacas, cabras y delfines etiquetados como *no-toros*.

Hay que cubrir las casuísticas reales.
- **10 % para validación:** ese porcentaje nunca se usa en el entrenamiento; se reserva para medir la precisión.

Si de 100.000 imágenes el modelo acierta 95.000, tiene un 95 % de precisión.

**El caso husky vs. lobo:** una red para distinguir huskies de lobos alcanzó precisión altísima.

Al investigar el patrón, resultó que detectaba **nieve** (el 90 % de las fotos de lobos tenían nieve de fondo).

Aprendió "nieve = lobo": funcionaba dentro del dataset, pero fallaría en el mundo real.

**El caso GPT-4:** funcionó peor que GPT-3.5 porque se retroalimentó del uso de sus propios usuarios sin control de calidad.

El mal uso generó datos de entrenamiento corruptos que el modelo ingirió sin supervisión.

Regla: nunca entrenar un modelo en producción con datos de usuarios reales sin curación previa.

Siempre hay un humano en el bucle validando antes de que el dato llegue al entrenamiento.

> **Idea clave (seguridad):** meter datos de producción sin curación en un modelo es uno de los ataques más efectivos que existen.

Se llama **envenenamiento de dataset** (dataset poisoning) y puede corromper un modelo completo inyectando una muestra representativa de datos falsos.

# El caso Pokémon Go --- datasets a escala planetaria

El ejemplo más brillante del módulo: **Pokémon Go no fue un juego**, fue una operación de recolección de dataset para construir un sistema de navegación por reconocimiento de imágenes para drones autónomos.

Al hacer que millones de personas caminaran por sus ciudades con el móvil en alto, se mapeó el mundo entero frame a frame, foto a foto, desde la perspectiva de alguien caminando por la calle.

### El resultado: un sistema de navegación **sin GPS** que reconoce el entorno por imagen.

En contextos militares tiene valor obvio: una señal GPS es fácil de inhibir, un sistema de reconocimiento visual no.

> [!important] > **Idea clave:** el verdadero oro de este siglo son los datos.

La diferencia entre un modelo mediocre y uno excelente no está en el algoritmo, sino en la calidad y cantidad del dataset con el que fue entrenado.

# El ecosistema de modelos --- quién gana realmente la carrera de la IA

Reflexión sobre el panorama competitivo:

- La **carrera visible** (OpenAI, Anthropic, Google, Grok, Perplexity) es la del software, financiada a pérdidas para crear dependencia.

La lógica del dealer: la primera es gratis, la segunda la pagas.
- Quienes ganan **dinero real** son los del **hardware**: NVIDIA con sus chips especializados y Apple con el Mac Mini y sus chips optimizados.

Mientras los modelos se pelean por cuota a pérdidas, el fabricante de chips factura por cada instancia de entrenamiento de todos ellos.
- La entrada del modelo chino **GLM 5.2** (gratuito y con capacidades comparables a los mejores occidentales) es un elemento desestabilizador: una guerra de precios asimétrica que suele salir justo después de un evento bursátil de OpenAI o Anthropic para maximizar el impacto en la valoración.

La postura pragmática de Carlos: un **orquestador Claude** que decide qué modelo usar para cada tarea (Haiku para búsquedas, Sonnet para desarrollo, modelos de OpenAI para tareas de ciberseguridad donde Anthropic bloquea), sin depender de un único proveedor.

# Base de datos vs. grafo relacional vs. red neuronal --- la progresión

El núcleo conceptual de la sesión, ilustrado con el dataset de cien mil coches y la comparación Obsidian / Neo4J:

- **Base de datos SQL = una tabla.** Filas y columnas.

Puedes filtrar, pero los datos no tienen relaciones entre sí más allá de las claves foráneas que programes.

No hay peso, ni jerarquía, ni contexto.
- **Grafo de Obsidian = red de nodos** conectados por hipervínculos.

Cada nodo es un documento.

El enlace no tiene semántica: dice que Borja está relacionado con Mariana, pero no *cómo* ni *por qué*.

Es una enciclopedia navegable, no un sistema que razona.

Útil como repositorio de conocimiento, no como base de inferencia.
- **Grafo vectorial en Neo4J = añade pesos a las relaciones.** Ahora "Borja es compañero de clase de Mariana" y esa relación tiene un peso que indica su importancia.

### Permite jerarquía: el modelo de un coche pesa más que su color porque es más discriminativo.

El agente navega por la red usando esas ontologías para ir directo al nodo relevante.
- **Red neuronal con machine learning = añade la capa de aprendizaje.** Los pesos se ajustan automáticamente según los resultados.

El modelo detecta patrones que nadie le enseñó y crea conexiones nuevas.

Aquí hay autoaprendizaje real.

> **Metáfora útil:** Obsidian es la estantería de tu casa (sabes dónde está cada libro, pero los libros no hablan entre sí).

Neo4J es Internet (las páginas están relacionadas y saltas de una a otra).

Una red neuronal con ML es un cerebro que ha leído todo Internet y puede generar conocimiento nuevo que no existía en ninguna página.

# Demostración en vivo --- de SQL a Obsidian con cien mil coches

Carlos ejecutó en directo la transformación del dataset de 100.000 coches (SQLite, 15 MB) a nodos de Obsidian usando **Claude Code**:

## 1.

Claude lee el SQL línea por línea y genera un fichero **Markdown por cada coche**, estructurado con sus características. 2.

En Obsidian, el **Graph View** muestra los nodos y sus conexiones visuales.

Lo que quedó visible: al incluir hipervínculos entre coches de la misma marca, el grafo forma **clusters automáticamente** (todos los Toyota se agrupan, todos los Jaguar se agrupan).

Visualmente *parece* una red neuronal, pero no lo es: son hipervínculos sin peso semántico.

La diferencia entre eso y Neo4J es exactamente la diferencia entre **parecer inteligente y serlo**.

**Siguiente paso (próxima sesión):** pasar de Obsidian a Neo4J añadiendo ontologías (el nodo "Toyota" tiene la relación "es fabricado en" con el nodo "Japón"), y luego añadir un algoritmo de machine learning sobre el grafo vectorial resultante para detectar patrones de demanda en el mercado de segunda mano.

# Recapitulación integrada

Esta sesión construye el mapa conceptual completo del módulo de IA:

- La IA moderna no es un árbol de decisión glorificado, sino una **red de nodos con pesos ponderados** que aprende de datasets etiquetados mediante AB testing.
- La **calidad del dataset** es más importante que el algoritmo o el hardware.
- **Obsidian** es un repositorio de conocimiento, no una red neuronal.
- **Neo4J** añade semántica y peso a las relaciones.
- El **machine learning** añade autoaprendizaje.

La siguiente sesión completará la demostración llevando el grafo de coches a Neo4J y añadiendo la primera capa de aprendizaje automático.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento.md|22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento]] — IA en Ciberseguridad, Redes, SQL Injection
- [[../../apuntes Chema/IA/IA — Redes Neuronales.md|IA — Redes Neuronales]] — IA en Ciberseguridad, Redes, SQL Injection
- [[../../Apuntes/comandos/SQLMap.md|SQLMap]] — IA en Ciberseguridad, Redes, SQL Injection
- [[../../apuntes Andres/15.07.2026 IA Introducción y Vibe Coding.md|15.07.2026 IA Introducción y Vibe Coding]] — IA en Ciberseguridad, Redes, SQL Injection
- [[resumen_master_clase46.md|resumen_master_clase46]] — IA en Ciberseguridad, Redes
- [[../../apuntes evolve/BLOQUE 13.md|BLOQUE 13]] — IA en Ciberseguridad, Redes

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #ia #redes #sqli
