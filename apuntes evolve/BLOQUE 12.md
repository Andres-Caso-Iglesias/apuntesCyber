> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 12 — Normativa y GRC
> **Contenido:** ISO 27001 en profundidad, ENS, GDPR, PCI DSS, DORA, NIS2 y gestión de riesgos

---

## ① Por qué importa la normativa

Las normativas obligan a implementar medidas mínimas que de otro modo podrían ignorarse, generan confianza entre clientes y socios, evitan sanciones económicas y reputacionales, y generan demanda de profesionales capaces de implementarlas (auditoría, formación, consultoría).

---

## ② ISO 27001: qué es y para qué sirve

ISO/IEC 27001 es la norma internacional de referencia para implantar un **SGSI** (Sistema de Gestión de Seguridad de la Información): el conjunto de políticas, procesos, controles y responsabilidades con el que una organización gestiona la seguridad de la información de forma sistemática y con mejora continua.

> [!important] No certifica "un producto seguro"
> Certifica que la organización gestiona sus riesgos de seguridad de forma metódica y auditable.

El SGSI se apoya en el ciclo **PDCA** (Plan-Do-Check-Act):

| Fase | Actividad |
|------|-----------|
| **Plan** | Planificar el sistema y evaluar riesgos |
| **Do** | Implementar controles y procesos |
| **Check** | Auditar y medir el desempeño |
| **Act** | Corregir y mejorar |

---

## ③ Estructura completa de la norma: cláusulas 4 a 10

### Cláusula 4 — Contexto de la organización
Exige identificar el contexto interno y externo de la organización, las partes interesadas (clientes, empleados, reguladores, proveedores) y sus expectativas de seguridad, y definir formalmente el **alcance del SGSI**: qué procesos, ubicaciones, sistemas y activos quedan dentro del sistema de gestión y cuáles quedan fuera (y por qué).

### Cláusula 5 — Liderazgo
La alta dirección debe demostrar compromiso activo: aprobar y comunicar la política de seguridad, asignar roles y responsabilidades claras (quién es el responsable de seguridad, quién aprueba excepciones, quién gestiona incidentes), y garantizar que el SGSI dispone de los recursos necesarios.

> [!warning] No conformalidad habitual
> En una auditoría de certificación, la ausencia de evidencia de compromiso de dirección (actas de reuniones, presupuesto asignado) es una de las no conformidades más habituales.

### Cláusula 6 — Planificación
Cubre la metodología de evaluación de riesgos (cómo se identifican, analizan y valoran los riesgos de seguridad), el tratamiento de riesgos (qué controles se aplican para reducirlos) y la fijación de objetivos de seguridad medibles (por ejemplo: *"reducir el tiempo medio de aplicación de parches críticos a menos de 15 días"*).

### Cláusula 7 — Soporte
Recursos (personal, presupuesto, herramientas), competencia (formación adecuada del personal con responsabilidades de seguridad), concienciación (que todo el personal entienda su papel en la seguridad, no solo el equipo técnico), comunicación (interna y externa sobre temas de seguridad) e información documentada (control de versiones, aprobación y disponibilidad de los documentos del SGSI).

### Cláusula 8 — Operación
Es la cláusula más "operativa": exige planificación y control operacional de los procesos de seguridad del día a día, y la realización de evaluaciones de riesgo periódicas (no solo una vez al implantar el sistema, sino de forma recurrente y ante cambios significativos).

### Cláusula 9 — Evaluación del desempeño
Exige monitorización y medición continua de la eficacia del SGSI, auditorías internas periódicas (realizadas por personal cualificado, idealmente independiente del área auditada) y revisión por la dirección (una reunión formal y documentada, normalmente anual, donde la alta dirección revisa el estado del SGSI y toma decisiones).

### Cláusula 10 — Mejora
Gestión de no conformidades (desviaciones respecto a lo exigido por la norma o por la propia documentación interna) y acciones correctivas, dentro de un ciclo de mejora continua del sistema.

---

## ④ Anexo A: los 93 controles en 4 categorías (versión 2022)

| Categoría | Controles | Contenido |
|-----------|-----------|-----------|
| **A.5 — Organizativos** | 37 | Política de seguridad, roles y responsabilidades, gestión de activos, control de acceso a nivel organizativo, gestión de proveedores y terceros, gestión de incidentes de seguridad, continuidad de negocio y cumplimiento legal. Ejemplos: A.5.1 (políticas de seguridad de la información), A.5.7 (inteligencia de amenazas — nueva en la versión 2022), A.5.23 (seguridad de la información en el uso de servicios cloud — también nueva), A.5.30 (preparación de TIC para la continuidad de negocio) |
| **A.6 — Personas** | 8 | Selección de personal (verificación de antecedentes proporcional al puesto), términos y condiciones de empleo, formación y concienciación en seguridad, proceso disciplinario ante incumplimientos, responsabilidades tras la finalización o cambio de empleo, y acuerdos de confidencialidad |
| **A.7 — Físicos** | 14 | Perímetros de seguridad física, controles de entrada, protección contra amenazas físicas y ambientales, seguridad del cableado, mantenimiento de equipos, política de escritorio despejado y pantalla despejada, y eliminación segura de equipos y soportes |
| **A.8 — Tecnológicos** | 34 | El bloque más extenso y el más cercano al trabajo técnico diario: gestión de dispositivos de usuario final, control de acceso privilegiado, protección contra malware, gestión de vulnerabilidades técnicas, configuración segura, copias de seguridad, redundancia, registro de eventos (logging) y monitorización, sincronización de relojes, uso de criptografía, seguridad en el ciclo de vida del desarrollo de software, y gestión de cambios |

---

## ⑤ Documentos obligatorios del SGSI

### Ejemplo simplificado de Declaración de Aplicabilidad (SoA)

| Control Anexo A | Aplicable | Justificación |
|----------------|-----------|---------------|
| A.5.1 Políticas de SI | Sí | Existe política aprobada por dirección |
| A.8.1 Inventario activos | Sí | Se mantiene CMDB actualizada |
| A.8.24 Uso de cifrado | Sí | Cifrado AES-256 en datos en reposo |
| A.7.4 Seguridad física | No | Infraestructura 100% en cloud (AWS) |

### Ejemplo simplificado de matriz de riesgos

| Riesgo | Prob. | Impacto | Nivel | Tratamiento |
|--------|-------|---------|-------|-------------|
| Fuga de credenciales por phishing | Alta | Alto | Crítico | Mitigar (MFA + formación) |
| Fallo de backup no detectado | Media | Alto | Alto | Mitigar (test restauración) |
| Acceso físico no autorizado | Baja | Medio | Bajo | Aceptar (control OK) |

### Documentos exigidos por la norma

Alcance del SGSI, política de seguridad, metodología de evaluación de riesgos, objetivos de seguridad medibles, Declaración de Aplicabilidad, Plan de Tratamiento de Riesgos, procedimiento de auditoría interna, procedimiento de gestión de no conformidades y registro de incidentes de seguridad.

---

## ⑥ El proceso de certificación: cómo funciona en la práctica

| Fase | Descripción |
|------|-------------|
| **1. Preparación** | Implantar el SGSI, aplicar controles, generar evidencias (puede llevar de 6 a 18 meses según el tamaño de la organización) |
| **2. Auditoría interna** | Realizada por personal propio o externo, previa a la certificación, para detectar no conformidades antes de la auditoría oficial |
| **3. Auditoría de certificación — Fase 1** | El organismo certificador (acreditado por ENAC en España, por ejemplo) revisa la documentación del SGSI |
| **4. Auditoría de certificación — Fase 2** | Auditoría in situ, donde se revisa la implementación real de los controles y se entrevista a personal de distintas áreas |
| **5. Emisión del certificado** | Válido 3 años, con auditorías de seguimiento anuales para mantenerlo vigente |

### Tipos de no conformidad detectadas en auditoría

| Tipo | Descripción |
|------|-------------|
| **No conformidad mayor** | Incumplimiento grave o sistémico que puede bloquear la certificación hasta resolverse |
| **No conformidad menor** | Incumplimiento puntual, se admite un plan de acción con plazo para resolverlo sin bloquear la certificación |

---

## ⑦ Esquema Nacional de Seguridad (ENS)

Marco obligatorio para la administración pública española y sus proveedores, categorizado por niveles según criticidad: **Básico**, **Medio** y **Alto**, cada uno con un conjunto creciente de controles obligatorios.

ISO 27001 y ENS están ampliamente alineados: buena parte de la evidencia recopilada para uno sirve para el otro, lo que en la práctica permite a muchas organizaciones certificarse en ambos marcos con un esfuerzo incremental relativamente bajo tras haber implantado el primero.

---

## ⑧ GDPR: checklist de cumplimiento básico

| Requisito | Detalle |
|-----------|---------|
| Consentimiento | Explícito y documentado para tratar datos personales |
| Notificación de brechas | Máximo 72 horas a la autoridad de control |
| RAT | Registro de Actividades de Tratamiento actualizado |
| Derechos de usuario | Acceso, rectificación, supresión, portabilidad |
| Multas | Hasta 10 millones de euros o el 10% de la facturación anual (hasta 20M€ o 4% en infracciones más graves) |

---

## ⑨ PCI DSS

Obligatorio para bancos y empresas que procesan pagos con tarjeta. Requisitos clave:

- Cifrado de datos de tarjeta en tránsito y en reposo
- Monitorización continua de accesos a los sistemas de pago
- Segmentación de red que aísle el entorno de datos de tarjeta (CDE) del resto de la infraestructura

---

## ⑩ DORA y NIS2

**DORA** (sector financiero/asegurador UE): no solo prevenir ataques, sino garantizar la continuidad operativa asumiendo que las entidades serán atacadas. Exige pruebas de resiliencia operativa digital periódicas.

**NIS2** (infraestructuras críticas: salud, energía, transporte, agua): resiliencia digital, multas más estrictas, cooperación entre estados miembros.

---

## ⑪ GRC en la práctica diaria

El trabajo de un consultor GRC se traduce en documentos muy concretos: matriz de riesgos, Plan de Tratamiento de Riesgos, Declaración de Aplicabilidad, y preparación de evidencias para auditorías de certificación externa.

### Estructura mínima de un Plan de Continuidad de Negocio (BCP)

1. **Análisis de Impacto en el Negocio (BIA):** identificar procesos críticos y su tiempo máximo de interrupción tolerable (RTO)
2. **Estrategias de recuperación** por proceso crítico (sistemas redundantes, sitio alternativo, backups probados)
3. **Plan de comunicación de crisis** (a quién se avisa, en qué orden, con qué mensaje)
4. **Pruebas periódicas del plan** (simulacros) y actualización tras cada lección aprendida