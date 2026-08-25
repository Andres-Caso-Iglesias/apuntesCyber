> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 46**
> **Módulo:** MODULO3
> **Tema:** Clase 46
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 46. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)** --- pero es radicalmente diferente a todas las anteriores.

No hay máquinas, no hay exploits.

La sesión tiene un formato abierto de debate sobre **emprendimiento con IA**, y Carlos preparó dos opciones para que el grupo eligiera:

1. **Hacking a LLMs** --- arquitectura de LLMs, agentes, tokens, contexto, montar un chatbot vulnerable para hacer prompt injection y hacking de IA. 2. **DevOps + Vibe Coding** --- despliegue de aplicaciones, arquitecturas seguras, flujo repositorio local → GitHub → servidor, y cómo construir productos con IA.

El grupo eligió la opción 2.

La clase se convirtió en una sesión de "pensar en producto y negocio" usando IA como herramienta de construcción.

**Hilo conductor:** la IA no es solo una herramienta técnica --- es un multiplicador de negocio.

La diferencia entre alguien que sabe usarla y alguien que no se mide en ordenes de magnitud de productividad.

## 2.

Demo en vivo: web de cliente generada con IA en 3 prompts

Carlos mostró una web completa para un cliente de desguace de coches que: - **Scrapeó** automáticamente todos los productos de la web original. - Generó el **diseño** modernizado buscando referencias similares en Internet. - Integró un **GIF animado** en la cabecera. - Mejoró el **UX/UI** al estilo Amazon. - Era completamente **funcional** (navegación, fichas de producto, formularios).

**Prompts usados (aproximadamente):** 1. "Busca negocios similares con páginas modernas, coge ideas y quiero que la hagas con un GIF animado al principio y con fotos gratuitas." 2. "Mejórame el UX/UA y ponlo modo Amazon." 3.

Un prompt más de refinamiento.

**Coste real:** \~0,10€ en tokens. **Cobrado al cliente:** 4.000€.

**El modelo de negocio del upselling:** Una vez que el cliente triste (desconfianza, mala experiencia anterior) se convierte en cliente feliz (confianza ganada), se abren las siguientes ventas:

Servicio Precio
 ------------------------------------------------------------------------- ----------------------
Rediseño web 4.000€ (ya entregado) Pasarela de pago con Stripe 1.500€ + 300€/mes Automatización de facturas (OCR + envío automático) 1.500€ + 200€/mes Automatización de contabilidad (extracción PDF + categorización) 2.000€ + 200€/mes Generación de leads (scraping de talleres mecánicos + email automático) 1.000€ + variable
 **Mantenimiento recurrente total** \~800€/mes

**El concepto de** "**cliente triste → cliente feliz → upselling**"**:** El primer trabajo bien hecho genera confianza.

La confianza abre la puerta a vender soluciones a los siguientes problemas del cliente.

El cliente del desguace tenía el problema visible (web lenta) pero no sabía que tenía el problema oculto (sin cobros online, sin facturas automatizadas, sin clientes potenciales).

## 3.

Conceptos clave de negocio con IA

### MVP de cartón piedra

Un **MVP** (*Minimum Viable Product*) ya no requiere semanas de desarrollo.

Con IA se puede montar en 2-3 tardes un prototipo funcional para validar si la idea tiene tracción antes de invertir tiempo en el producto real.

**La regla de Carlos:** si el MVP no funciona, el producto tampoco.

Si funciona, entonces se invierte en escalarlo.

### No reinventar la rueda

Si algo ya existe (scraper de precios de Mercadona, carrito de compra, reconocimiento de recibos), se integra y se reutiliza.

La habilidad no está en construir cada componente desde cero, sino en saber **qué conectar con qué**.

### La idea viene de problemas reales

Las mejores ideas de producto vienen de problemas del día a día: - Un amigo entrenador que necesita gestionar a sus alumnos → aplicación fitness con IA. - Un amigo al que roban el pedido de Glovo → verificación biométrica de entregas. - Un cliente con una web que no carga → rediseño + automatizaciones.

### Debatir la idea con Claude antes de construirla

Antes de escribir una línea de código, usar Claude para: 1.

Analizar la competencia (tabla de features de competidores). 2.

Identificar el valor diferencial (qué tienen los otros que no tenemos y viceversa). 3.

Encontrar el modelo de negocio (freemium, suscripción, comisión, upselling). 4.

Definir los "must-have" de la aplicación.

**Prompt base sugerido:**

Tengo una idea para una aplicación web.

Necesito que me ayudes a refinar, mejorar y darle un valor diferencial sobre los competidores.

La aplicación se trata de [DESCRIPCIÓN].

Lo 1º que necesito es una tabla de la competencia con las features que tienen.

Además, mi idea tiene los siguientes puntos necesarios: [LISTA].

## 4.

Arquitectura de agentes de IA --- cómo Carlos lo construye

### El sistema de copiloto de Cibersia Security

Carlos describió el sistema interno de su empresa:

- **Un agente conectado a Teams** que "conoce" a cada empleado --- tiene acceso a todos los correos, documentos, ofertas, informes, llamadas grabadas y conversaciones.
- Toda esa información está en un **grafo de conocimiento** donde los nodos se correlacionan entre sí.
- El agente puede ser consultado sobre cualquier aspecto de la empresa y tiene contexto completo.
- **Proactivamente** propone automatizaciones: "Oye, vendría bien una skill que coja los adjuntos de los correos, los analice con OCR y los categorice en contabilidad. ¿La creo?"
- Si el usuario dice sí, el agente genera y despliega la automatización.

### Cómo se crean los agentes (sin entrenar modelos propios)

**La confusión común:** muchos piensan que hay que entrenar una red neuronal con datos propios para tener una IA especializada.

**La realidad:** para la inmensa mayoría de aplicaciones de negocio NO hace falta.

El proceso correcto es:

## 1.

Tomar un LLM de base (Claude, GPT-4, Gemini) ↓ 2.

Definir el rol y las skills del agente (hiperespecialización por prompt/instrucciones del sistema) ↓ 3.

Darle acceso a las herramientas que necesita (bases de datos, APIs, correo, calendario, ficheros) ↓ 4.

Definir el flujo de trabajo (cómo se encadenan varios agentes entre sí)

**Entrenar redes neuronales propias** (PyTorch, datasets, pesos del modelo) es para Google, OpenAI y BlackRock --- cuesta millones de euros y meses.

Para aplicaciones de negocio, tira de los LLMs ya entrenados y dale instrucciones específicas.

### El ejemplo de la aplicación fitness

Tres agentes especializados trabajando en paralelo: - **Agente de nutrición** --- genera la dieta según el perfil del usuario. - **Agente de entrenamiento** --- genera la rutina semanal. - **Agente de medicina deportiva** --- verifica que la combinación dieta+ejercicio sea segura para el perfil de salud.

Los tres agentes se coordinan para generar la respuesta final.

Ninguno "sabe" lo que saben los otros, pero el orquestador los combina.

## 5.

Ejemplo de aplicación desarrollada en vivo: finanzas personales (proyecto de John)

El grupo decidió usar la idea de John como proyecto en vivo.

Carlos demostró cómo plantear el prompt inicial a Claude para arrancar el desarrollo:

### Funcionalidades definidas en clase

Feature Descripción
--------------------------------- ---------------------------------------------------------------------------------------------------------------------
 **Regla 50/30/20** Distribución automática de ingresos: 50% necesidades, 30% deseos, 20% ahorro
 **Actualización automática** Los gráficos y métricas se actualizan en tiempo real al introducir un dato
 **Asistente IA integrado** Analiza la situación financiera actual y propone un plan de acción personalizado para llegar al objetivo del usuario
 **Comparativa de competidores** Tabla de features de YNAB, Mint, Fintonic, etc. para identificar huecos del mercado

**El valor diferencial** se define con Claude preguntando: ¿qué tienen todos los competidores que no ofrezco yo? ¿Qué podría ofrecer que ellos no tienen?

## 6.

Aspectos legales y técnicos mencionados

### Biometría y protección de datos

Surgió de una conversación con Mariana sobre su aplicación de reconocimiento de gestos faciales para niños con autismo/dislexia:

- **Identificación biométrica = dato de categoría especial** bajo el RGPD.

Requiere base legal explícita y consentimiento.
- **Escanear menores para identificarlos = ilegal** sin consentimiento parental documentado y base legal específica.
> [!important] - **La distinción clave:** identificar una persona (dato biométrico con nombre → ilegal sin consentimiento) vs. reconocer un patrón (¿esta cara muestra el gesto "feliz"? → legal si no se guarda ningún dato biométrico).
- **La solución:** entrenar el modelo con datasets de open source o comprados (nunca con datos de usuarios), guardar solo los patrones ya clasificados (no las imágenes), y hacer el procesamiento sin guardar datos personales.
- **Multa de referencia:** 600.000€ por escanear menores sin cumplir los requisitos legales.

### Shadow IT

### Concepto mencionado: los empleados que tienen prohibido usar Claude en los ordenadores de la empresa lo usan en el móvil personal.

La política de seguridad que prohíbe herramientas sin abordar el problema real (mejorar la productividad de los empleados) genera Shadow IT --- uso de herramientas no autorizadas fuera de los canales corporativos.

### AI Act europeo

Regulación que afecta a aplicaciones de IA en la UE, especialmente en áreas de alto riesgo (biometría, menores, toma de decisiones con impacto legal).

Hay que declarar qué tecnología se usa y cómo se procesa cada dato.

## 7.

Herramientas y plataformas mencionadas

Herramienta Descripción
--------------------------------------- ----------------------------------------------------------------------------------------------------------------------
**Lovable** (antes Fable/Lovable.dev) Plataforma para construir aplicaciones web completas con prompts.

Es "Claude con skills de diseño UX" según Carlos
 **Stripe** Pasarela de pago.

Se integra con un solo prompt y una API key
 **Playwright** Librería de Python/Node.js para scraping web automatizado y control de navegador
 **PyTorch** Framework de deep learning para redes neuronales propias --- para cuando sí se necesita entrenar un modelo específico
 **n8n** Plataforma de automatizaciones open source (mencionada brevemente)
 **Supabase** Backend as a service (mencionado como opción para montar backend rápido)
 **Heroku / Render** Hosting simple para MVPs --- opción barata para arrancar
 **Raspberry Pi** Hardware para alojar proyectos en casa sin coste de servidor
 **ProofPoint** Herramienta de simulaciones de phishing para empresas --- el grupo mencionó querer automatizarla

## 8.

Flujo de desarrollo recomendado por Carlos

## 1.

Tener la idea ↓ 2.

Debatir y refinar con Claude (tabla de competidores, valor diferencial, must-haves) ↓ 3.

Definir la arquitectura (qué va en el front, qué en el back, dónde está la BD, qué datos son sensibles, dónde van los agentes) ↓ 4.

Crear MVP con Claude Code / Lovable en 2-3 tardes ↓ 5.

Validar: ¿funciona? ¿hay usuarios reales dispuestos a pagar? ↓ 6.

Iterar basándose en el feedback (el propio producto define hacia dónde va) ↓ 7.

### Si funciona: escalar (más usuarios, más features, inversión) Si no: pivotar o descartar sin haber gastado meses

## 9.

Conceptos y términos clave

Término Explicación
------------------------------------------- ----------------------------------------------------------------------------------------------------------------------
 **Vibe coding** Desarrollo de software asistido completamente por IA con prompts, sin escribir código manualmente
 **MVP** (*Minimum Viable Product*) Versión mínima funcional de un producto para validar la idea con usuarios reales
 **Upselling** Vender servicios adicionales de mayor valor a un cliente ya existente y satisfecho
 **Agente de IA** LLM con instrucciones específicas, acceso a herramientas y capacidad de ejecutar acciones autónomamente
 **Skills de agente** Capacidades específicas que se le dan a un agente (buscar en web, enviar emails, leer ficheros, etc.)
 **Freemium** Modelo de negocio con versión gratuita limitada y versión premium de pago
 **Shadow IT** Uso de herramientas tecnológicas no autorizadas por la empresa, generalmente en dispositivos personales
 **AI Act** Regulación europea para aplicaciones de inteligencia artificial, especialmente en usos de alto riesgo
 **Biometría** Datos que identifican a una persona por características físicas (cara, huella, iris) --- categoría especial bajo RGPD
 **Scraper** Programa que extrae automáticamente datos de páginas web
 **OCR** (*Optical Character Recognition*) Tecnología que extrae texto de imágenes o documentos escaneados
 **Grafo de conocimiento** Representación de información en forma de nodos y relaciones (como D3.js en CyberKB)
 **Embedding** Representación matemática de texto/datos que permite compararlos semánticamente
 **RGPD** Reglamento General de Protección de Datos --- normativa europea de privacidad
 **Copiloto** Nombre que Carlos da a su agente de IA personal conectado a toda la información de Cibersia Security
 **Fable 5 / Claude Opus** Modelos avanzados de IA usados por Carlos para las demos
 **Playwright** Librería para automatización de navegadores (web scraping, testing)
 **Webhook** Endpoint HTTP que recibe notificaciones automáticas de un servicio externo cuando ocurre un evento

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*