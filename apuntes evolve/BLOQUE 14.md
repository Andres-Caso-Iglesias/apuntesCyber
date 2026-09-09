> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 14 — Examen ISO 27001
> **Contenido:** Qué evalúa el examen, cómo estudiarlo, cómo practicar, simulacros y errores frecuentes

---

## ① Qué debes tener claro antes de empezar a estudiar

El examen de ISO 27001 **no evalúa tu capacidad de "hackear" nada**: evalúa si comprendes la estructura de la norma, el vocabulario específico de la gestión de riesgos, y si eres capaz de aplicar ese conocimiento a situaciones prácticas de gestión (no técnicas de explotación).

> [!warning] Error más habitual
> El error más habitual de quien viene de la rama ofensiva del máster es abordar este examen como si fuera técnico: la clave aquí no es "saber hackear", es saber **clasificar, ubicar y razonar sobre procesos de gestión**. Es un cambio de chip mental importante.

---

## ② Formato y estructura del examen

| Característica | Detalle |
|----------------|---------|
| **Tipo de preguntas** | Test de opción múltiple (normalmente 4 opciones, una correcta); en algunos formatos también verdadero/falso o emparejar conceptos |
| **Duración** | Entre 40 y 90 minutos según el proveedor de la certificación y el nivel |
| **Nota de corte** | Típicamente alrededor del 65-70% de aciertos |
| **Distribución** | Terminología y conceptos básicos, estructura de cláusulas (4-10), Anexo A y sus categorías, gestión de riesgos, y proceso de auditoría/certificación |

---

## ③ Desglose de contenidos por peso aproximado

| Prioridad | Contenido | Detalle |
|-----------|-----------|---------|
| **1** | Terminología ISO 27000 y conceptos fundamentales | Activo, amenaza, vulnerabilidad, riesgo, riesgo residual, la tríada CIA — base de casi todas las demás preguntas |
| **2** | Estructura de cláusulas 4 a 10 | Qué actividad de gestión corresponde a cada cláusula |
| **3** | Anexo A: las 4 categorías (A.5/A.6/A.7/A.8) | Ser capaz de clasificar un control concreto dentro de la categoría correcta |
| **4** | Gestión de riesgos | Metodología, las 4 estrategias de tratamiento (mitigar, transferir, evitar, aceptar), riesgo inherente vs residual |
| **5** | Proceso de certificación | Fases de auditoría, tipos de no conformidad, periodicidad de las auditorías de seguimiento |
| **6** | Documentación obligatoria del SGSI | Qué documentos exige la norma y para qué sirve cada uno (SoA, Plan de Tratamiento de Riesgos, política de seguridad...) |

---

## ④ Plan de estudio recomendado (2 semanas)

### Semana 1 — Teoría y estructura

| Días | Actividad |
|------|-----------|
| **1-2** | Leer y resumir con tus propias palabras las cláusulas 4 a 10. Crear una tabla de una sola página con "Cláusula → qué exige → ejemplo real" — esa tabla será tu chuleta mental para el examen |
| **3-4** | Estudiar el Anexo A por categorías. Para cada categoría (A.5/A.6/A.7/A.8), memoriza 3-4 controles representativos y su número — no hace falta memorizar los 93 controles, pero sí saber reconocer patrones ("si habla de cifrado o backups, es A.8; si habla de contratos con proveedores o política, es A.5") |
| **5-7** | Gestión de riesgos y terminología ISO 27000. Practica clasificar riesgos de ejemplo en las 4 estrategias de tratamiento hasta que sea automático |

### Semana 2 — Práctica y simulacro

| Días | Actividad |
|------|-----------|
| **8-10** | Resolver baterías de preguntas tipo test y anotar en qué área concreta fallas más — ahí es donde debes volver a repasar teoría |
| **11-12** | Repasar exclusivamente las áreas donde has fallado más en los simulacros |
| **13** | Simulacro completo cronometrado en condiciones de examen real (sin apuntes, con el tiempo límite exacto) |
| **14** | Descanso activo — repasar solo la chuleta de una página, sin estudiar contenido nuevo el día antes del examen |

---

## ⑤ Cómo practicar: más allá de leer la norma

Leer la norma o los apuntes no es suficiente para un examen tipo test: hace falta practicar con el formato real de pregunta.

1. **Crea tus propias preguntas tipo test** a partir de cada cláusula y control que estudies — el propio ejercicio de redactar una pregunta con distractores plausibles obliga a entender el concepto en profundidad, no solo memorizarlo
2. **Practica con simulacros oficiales** o de terceros si el proveedor de la certificación los ofrece
3. **Estudia en grupo** con compañeros del máster: explicarle a otra persona la diferencia entre no conformidad mayor y menor, o entre riesgo inherente y residual, consolida el concepto mucho mejor que releerlo en solitario
4. **Usa mapas mentales o tablas comparativas** para las cosas que se confunden fácilmente (por ejemplo: Fase 1 vs Fase 2 de auditoría de certificación; ISO 27001 vs ENS; auditoría interna vs auditoría de certificación)

---

## ⑥ Batería de preguntas de práctica (con respuesta razonada)

### Pregunta 1
**¿Qué cláusula de ISO 27001 exige la revisión por la dirección del SGSI?**

a) Cláusula 7 &emsp; b) Cláusula 8 &emsp; c) Cláusula 9 &emsp; d) Cláusula 10

**Respuesta:** c) Cláusula 9 (Evaluación del desempeño). La revisión por dirección es una actividad de medición/evaluación del sistema, no de operación (8) ni de mejora tras detectar fallos (10).

### Pregunta 2
**Un control que exige cifrado de datos en reposo pertenece a:**

a) A.5 Organizativos &emsp; b) A.6 Personas &emsp; c) A.7 Físicos &emsp; d) A.8 Tecnológicos

**Respuesta:** d) A.8 Tecnológicos. El cifrado es una medida técnica aplicada sobre sistemas, no un proceso organizativo ni una medida física.

### Pregunta 3
**Si el riesgo residual tras aplicar controles sigue siendo alto pero el coste de mitigarlo supera el beneficio, ¿qué estrategia de tratamiento es la más adecuada?**

a) Mitigar &emsp; b) Transferir &emsp; c) Aceptar &emsp; d) Evitar

**Respuesta:** c) Aceptar (siempre documentado y aprobado formalmente por dirección). Mitigar más allá de lo razonable no es coste-eficiente; transferir (ej. un seguro) no elimina el riesgo operativo; evitar implicaría dejar de realizar la actividad, una medida desproporcionada si el riesgo ya es bajo tras los controles existentes.

### Pregunta 4
**El documento que justifica qué controles del Anexo A se aplican y por qué se llama:**

a) Política de seguridad &emsp; b) Declaración de Aplicabilidad (SoA) &emsp; c) Plan de Tratamiento de Riesgos &emsp; d) Registro de Activos

**Respuesta:** b) Declaración de Aplicabilidad (SoA).

### Pregunta 5
**Durante una auditoría de certificación se detecta que la política de seguridad nunca ha sido revisada ni aprobada por la dirección. Esto se clasifica como:**

a) Observación &emsp; b) No conformidad menor &emsp; c) No conformidad mayor &emsp; d) Oportunidad de mejora

**Respuesta:** c) No conformidad mayor. Afecta directamente al liderazgo y compromiso de dirección (Cláusula 5), un requisito fundamental — no es un fallo puntual y aislado.

### Pregunta 6
**¿Cuál es la diferencia principal entre riesgo inherente y riesgo residual?**

a) No hay diferencia, son sinónimos &emsp; b) El inherente es antes de aplicar controles; el residual, después &emsp; c) El residual es siempre cero si el SGSI funciona bien &emsp; d) El inherente solo aplica a riesgos físicos

**Respuesta:** b) El inherente es el riesgo antes de aplicar controles; el residual es el que queda tras aplicarlos — nunca es necesariamente cero.

### Pregunta 7
**¿Qué ciclo de mejora continua subyace a toda la norma ISO 27001?**

a) DMAIC &emsp; b) PDCA (Plan-Do-Check-Act) &emsp; c) OODA &emsp; d) Kanban

**Respuesta:** b) PDCA.

---

## ⑦ Errores frecuentes que hacen perder puntos

| Error | Corrección |
|-------|-----------|
| Confundir auditoría interna con auditoría de certificación | La interna la realiza la propia organización o un tercero contratado por ella, de forma preparatoria. La de certificación la realiza un organismo acreditado externo e independiente, y es la que otorga el certificado |
| Pensar que el Anexo A es obligatorio aplicar entero | En realidad la organización justifica en la SoA qué controles aplica y cuáles no, según su propio contexto y análisis de riesgos |
| Confundir el alcance del SGSI con el alcance de la certificación de un producto | ISO 27001 certifica la **gestión**, no un software o sistema concreto |
| No distinguir bien las 4 estrategias de tratamiento de riesgo entre sí en preguntas donde se describe un escenario | Hay que elegir la más adecuada según el contexto (ver pregunta 3 de la batería anterior) |

---

## ⑧ El día del examen

1. **Lee cada pregunta dos veces** antes de mirar las opciones — muchas preguntas usan negaciones ("¿cuál de las siguientes NO es...") que se pasan por alto con lectura rápida
2. **Si dudas entre dos opciones**, vuelve a tu chuleta mental de "cláusula → qué exige" o "categoría del Anexo A → tipo de control" construida durante el estudio — la mayoría de dudas se resuelve ubicando bien el concepto, no memorizando literalmente el texto de la norma
3. **Gestiona el tiempo**: si una pregunta te bloquea más de un minuto, márcala y sigue — vuelve a ella al final si el formato del examen lo permite
4. **Repasa las respuestas marcadas como dudosas** al final si queda tiempo, pero evita cambiar respuestas por simple inseguridad sin una razón concreta para el cambio



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[BLOQUE 12.md|BLOQUE 12]] — Certificaciones, Normativa / GRC, Redes
- [[../Apuntes/13 - Normativa y GRC/Normativa - ISO 27001, GDPR, ENS.md|Normativa - ISO 27001, GDPR, ENS]] — Certificaciones, Empleabilidad, Normativa / GRC
- [[../Apuntes/07 - Empleabilidad/Mercado Laboral y Certificaciones.md|Mercado Laboral y Certificaciones]] — Certificaciones, Empleabilidad, OSINT
- [[../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — Empleabilidad, Normativa / GRC, OSINT
- [[../apuntes Joselu/MODULO2/resumen_master_clase11.md|resumen_master_clase11]] — Empleabilidad, Normativa / GRC, OSINT
- [[../Apuntes/04 - OSINT y Recopilacion/OSINT - Metodología y Fuentes.md|OSINT - Metodología y Fuentes]] — Metodología Pentest, OSINT, Redes

> #certificaciones #empleabilidad #normativa #osint #pentest #redes
