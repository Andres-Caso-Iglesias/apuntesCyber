> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 51**
> **Módulo:** MODULO3
> **Tema:** Clase 51
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 51. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

La sesión más completa del módulo de IA hasta ahora.

Arranca donde quedó la anterior (el grafo relacional de Obsidian con cien mil coches sigue procesando en segundo plano, lo que recuerda la diferencia entre red relacional y red neuronal) y desciende hasta los cimientos: **qué es realmente una IA, qué es un LLM, qué son los tokens** y por qué la IA de navegador tiene límites claros.

La segunda mitad demuestra en directo cómo **Claude Code** supera esos límites, y cierra con la **arquitectura real de agentes, subagentes, skills y ficheros MD** que Carlos usa en proyectos profesionales.

# Qué es realmente una IA --- desmontando el mito

Una IA no es inteligencia en el sentido humano.

Es **un buscador muy rápido con mucha información conectada** que, basándose en el contexto de quien pregunta, devuelve el resultado que cree que el usuario quiere recibir.

### Lo crítico: **la IA no busca la verdad, busca la satisfacción del usuario.**

Esto viene del **entrenamiento por refuerzo con AB testing**: respuesta buena → recompensa; respuesta mala → castigo.

Igual que un perro que aprende a dar la pata.

Los modelos iniciales (GPT-3.5, GPT-4) tenían este comportamiento tan marcado que si el usuario corregía una respuesta correcta diciéndole que estaba mal, la IA cedía y daba la incorrecta que el usuario esperaba.

Los modelos actuales lo han reducido, pero no eliminado.

La frase que resume cómo funciona: el 95 % de las veces "se fuma un porro y te da un contexto random, pero lo hace conociéndote, por eso acierta".

La IA no genera: **busca, conecta, une y expone.**

> [!important] > **Idea clave:** cuanto más contexto tiene la IA sobre el usuario y la tarea, mejor resultado da.

No porque sea más inteligente, sino porque tiene más información conectada desde la que deducir qué se espera de ella.

# Qué es un LLM y qué son los tokens

Un **LLM (Large Language Model)** guarda un historial del chat y lo consulta: ese historial es el **contexto**.

A más contexto, mejor resultado, pero también mayor coste computacional, porque con cada nuevo prompt el modelo revisa todo el historial para deducir qué viene a continuación.

Un **token** no es una letra ni una palabra: es un **fragmento de palabra**.

El modelo no lee como nosotros; lee tokens y deduce el siguiente más probable por contexto.

Si va procesando "el" tras haber leído que se habla de un veterinario, deduce que viene un sustantivo (probablemente animal); si el siguiente token es "gat", ya sabe que la palabra es "gato" o "gata".

Esa **deducción encadenada** es lo que genera la respuesta.

Por eso los modelos más potentes cuestan más: tienen más **parámetros** para deducir con más contexto, lo que requiere más cómputo. **DeepSeek** fue disruptivo porque redujo el coste de cómputo por token en un factor de 20-30 respecto a OpenAI, entrenando la red para que las operaciones de deducción fueran más ligeras sin perder calidad.

### Regla práctica: usar el modelo más grande para todo es "encender una bombilla con un reactor nuclear".

Funciona, pero es absurdo. **Haiku** para búsquedas y tareas simples, **Sonnet** para desarrollo, **Opus** (o equivalente) para razonamiento complejo.

> **Metáfora útil:** los tokens son las fichas de un juego de palabras.

El modelo no ve las palabras enteras, ve las fichas y reconstruye el significado combinándolas.

Cuantas más fichas puede mirar a la vez (más contexto), más precisa es la combinación.

# La IA de navegador vs.

Claude Code --- por qué importa la diferencia

La IA de navegador (claude.ai, ChatGPT web) corre en un **mini-docker** en los servidores de Anthropic que se crea para cada conversación y desaparece al terminar.

No tiene acceso a las herramientas del ordenador del usuario: no ejecuta scripts, no comprueba si algo funciona, no interactúa con el sistema de ficheros local.

Cuando genera código, lo devuelve como texto y es el usuario quien lo copia, pega y prueba.

La demostración lo dejó claro con el ejercicio del **Buscaminas** (un script que abre el juego, configura la dificultad y lo resuelve en tiempo real):

- **IA de navegador:** tardó mucho más, requirió múltiples correcciones manuales y el resultado fue parcialmente funcional.
- **Claude Code:** lo hizo en **4 min 43 s**, generando 629 líneas de Python, comprobando si había un Buscaminas instalado, detectando que era Windows 11 (que ya no lo incluye), descargándolo de la Microsoft Store con su identificador de producto verificado y, al no gustar ese, programando uno desde cero con la interfaz clásica.

La diferencia no es el modelo de IA, sino **las herramientas disponibles**.

Claude Code puede ejecutar comandos, comprobar resultados, iterar automáticamente hasta que funcione, abrir programas del sistema, leer y escribir ficheros, y paralelizar tareas en pestañas con contextos distintos.

> **Metáfora útil:** la IA de navegador es como explicarle a alguien por teléfono cómo montar un mueble.

Claude Code es tenerle en casa con todas las herramientas encima de la mesa.

# Cómo funciona Claude Code por dentro --- el cerebro y los agentes

Claude Code tiene un fichero de configuración central que es el **cerebro** de la instalación: `claude.md`.

En Markdown, contiene las **instrucciones permanentes** que Claude sigue en todos los proyectos.

Todo lo que se escribe ahí se convierte en norma global.

Dentro de los proyectos existe un `project.md` con instrucciones específicas que **sobreescriben** al `claude.md`.

### La jerarquía: la excepción (`project.md`) tiene más poder que la norma (`claude.md`), pero la excepción no existe sin la norma.

Es la **lógica del zero trust aplicada a agentes de IA**: se define el comportamiento base y se permiten excepciones controladas, no al revés.

- Los **agentes** son ficheros Markdown que definen la **identidad**: personalidad, objetivo, herramientas disponibles y herramientas prohibidas de un subproceso especializado de Claude.

Un agente es un `.md` con instrucciones claras (qué eres, qué puedes hacer, qué no, cómo actuar).

Claude lee el documento y se mimetiza con él hasta terminar la tarea.
- Las **skills** son también ficheros de texto, pero definen el **método**: cómo llevar a cabo un tipo de trabajo concreto, no quién lo hace.

> En una frase: **el agente define quién, la skill define cómo.**

# La arquitectura de agentes en producción

El flujo estándar que Carlos tiene configurado en su `claude.md` para cualquier proyecto:

## 1.

El **usuario** hace una petición. 2.

Llega al **orquestador** (agente director del proyecto). 3.

El orquestador la pasa al **agente prompter**, que hiperoptimiza el prompt: lo estructura, añade contexto, lo alinea con los objetivos y lo convierte en una instrucción precisa para un LLM. 4.

El prompt optimizado vuelve al orquestador, que lo pasa al **selector de modelos**. 5.

El **selector de modelos** elige el modelo más **eficiente** para esa tarea (no el más potente, el más apropiado). 6.

El modelo seleccionado ejecuta la tarea.

Este flujo consume **más tokens** que ir directo al modelo, pero el output es cualitativamente superior porque el prompt final está estructurado, contextualizado y optimizado.

El coste se recupera en la **reducción de iteraciones** para llegar al resultado correcto.

Para proyectos con diseño hay un agente adicional, **design architect**, que se invoca siempre antes de generar cualquier interfaz: investiga en Internet los patrones de UX del sector, extrae guías de estilo y genera las especificaciones visuales antes de que nadie escriba una línea de código de interfaz.

> [!important] > **Idea clave:** un agente sin skills es un empleado sin formación.

La diferencia entre un resultado mediocre y uno profesional no está en el modelo de IA, sino en la calidad de las instrucciones que recibe, tanto en el agente (quién es) como en las skills (cómo trabaja).

# Por qué una IA local es (casi siempre) mala idea

Desarrollar una IA local propia tiene sentido muy raramente.

El coste de entrenamiento, mantenimiento y actualización de un modelo propio no se amortiza frente a usar la **API de los modelos existentes con un orquestador** que seleccione el mejor en cada momento.

El ejemplo de la clase: una empresa gasta **8.000 €/mes** en IA porque usa siempre el modelo más caro para todo, sin optimización.

Con un orquestador bien configurado, ese coste se reduce drásticamente manteniendo la misma calidad.

# Recapitulación integrada

La sesión cierra el arco conceptual del módulo de IA.

La cadena completa:

- La IA es un **buscador con contexto** que deduce tokens encadenados.
- La diferencia entre modelos es la **cantidad de parámetros** y la **eficiencia** de ese cómputo.
- La diferencia entre IA de navegador y Claude Code son las **herramientas disponibles**.
- La diferencia entre usar Claude y **usarlo bien** son los **agentes, las skills y el** `claude.md`.

El proyecto del **ajedrez con machine learning** queda abierto para la siguiente sesión, donde se construirá la arquitectura completa con orquestador, agentes especializados, grafo vectorial en Neo4J y algoritmo de aprendizaje reforzado.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/comandos/SMB_Impacket.md|SMB_Impacket]] — Metodología Pentest, Redes, Windows
- [[../../Apuntes/comandos/Windows.md|Windows]] — Metodología Pentest, Redes, Windows
- [[../../apuntes Chema/IA/IA — Redes Neuronales.md|IA — Redes Neuronales]] — IA en Ciberseguridad, Metodología Pentest, Redes
- [[../../transcripciones/Julio/23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes.md|23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]] — IA en Ciberseguridad, Metodología Pentest, Redes
- [[../../Apuntes/comandos/Tmux.md|Tmux]] — Metodología Pentest, Redes, Windows
- [[../../apuntes Chema/IA/IA — Introducción y VibeCoding.md|IA — Introducción y VibeCoding]] — IA en Ciberseguridad, Metodología Pentest, Redes

> #ia #pentest #redes #windows
