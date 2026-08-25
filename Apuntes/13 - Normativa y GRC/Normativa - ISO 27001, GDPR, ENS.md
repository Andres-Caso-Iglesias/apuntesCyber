

> **Relacionado:** [[Blue Team - SOC e Incidentes]] · [[Mercado Laboral y Certificaciones]]

---

## 1. Por qué importa la normativa

Las normativas obligan a implementar medidas mínimas que de otro modo podrían ignorarse, generan confianza entre clientes y socios, evitan sanciones económicas y reputacionales, y generan demanda de profesionales capaces de implementarlas (auditoría, formación, consultoría).

---

## 2. ISO 27001: qué es y para qué sirve

ISO/IEC 27001 es la norma internacional de referencia para implantar un **SGSI** (Sistema de Gestión de Seguridad de la Información): el conjunto de políticas, procesos, controles y responsabilidades con el que una organización gestiona la seguridad de la información de forma sistemática y con mejora continua.

> **Importante:** No certifica "un producto seguro". Certifica que la organización gestiona sus riesgos de seguridad de forma metódica y auditable.

### Ciclo PDCA (Plan-Do-Check-Act)

| Fase | Actividad |
|------|-----------|
| **Plan** | Planificar el sistema y evaluar riesgos |
| **Do** | Implementar controles y procesos |
| **Check** | Auditar y medir el desempeño |
| **Act** | Corregir y mejorar |

---

## 3. Estructura completa de la norma: cláusulas 4 a 10

### Cláusula 4 — Contexto de la organización
Exige identificar el contexto interno y externo de la organización, las partes interesadas (clientes, empleados, reguladores, proveedores) y sus expectativas de seguridad, y definir formalmente el **alcance del SGSI**.

### Cláusula 5 — Liderazgo
La alta dirección debe demostrar compromiso activo: aprobar y comunicar la política de seguridad, asignar roles y responsabilidades claras, y garantizar que el SGSI dispone de los recursos necesarios.

> **No conformidad habitual:** La ausencia de evidencia de compromiso de dirección (actas de reuniones, presupuesto asignado) es una de las no conformidades más habituales en auditoría de certificación.

### Cláusula 6 — Planificación
Cubre la metodología de evaluación de riesgos, el tratamiento de riesgos y la fijación de objetivos de seguridad medibles.

### Cláusula 7 — Soporte
Recursos, competencia, concienciación, comunicación e información documentada.

### Cláusula 8 — Operación
Planificación y control operacional de los procesos de seguridad del día a día, y evaluaciones de riesgo periódicas.

### Cláusula 9 — Evaluación del desempeño
Monitorización continua, auditorías internas periódicas y revisión por la dirección.

### Cláusula 10 — Mejora
Gestión de no conformidades y acciones correctivas, dentro de un ciclo de mejora continua.

---

## 4. Anexo A: los 93 controles en 4 categorías (versión 2022)

| Categoría | Controles | Contenido |
|-----------|-----------|-----------|
| **A.5 — Organizativos** | 37 | Política de seguridad, roles, gestión de activos, control de acceso organizativo, gestión de proveedores, gestión de incidentes, continuidad de negocio |
| **A.6 — Personas** | 8 | Selección de personal, formación, concienciación, proceso disciplinario, acuerdos de confidencialidad |
| **A.7 — Físicos** | 14 | Perímetros de seguridad, controles de entrada, protección ambientales, escritorio despejado |
| **A.8 — Tecnológicos** | 34 | Gestión de dispositivos, control de acceso privilegiado, protección malware, gestión de vulnerabilidades, cifrado, logging |

---

## 5. Documentos obligatorios del SGSI

### Declaración de Aplicabilidad (SoA)

| Control Anexo A | Aplicable | Justificación |
|----------------|-----------|---------------|
| A.5.1 Políticas de SI | Sí | Existe política aprobada por dirección |
| A.8.1 Inventario activos | Sí | Se mantiene CMDB actualizada |
| A.8.24 Uso de cifrado | Sí | Cifrado AES-256 en datos en reposo |
| A.7.4 Seguridad física | No | Infraestructura 100% en cloud (AWS) |

### Matriz de riesgos simplificada

| Riesgo | Prob. | Impacto | Nivel | Tratamiento |
|--------|-------|---------|-------|-------------|
| Fuga de credenciales por phishing | Alta | Alto | Crítico | Mitigar (MFA + formación) |
| Fallo de backup no detectado | Media | Alto | Alto | Mitigar (test restauración) |
| Acceso físico no autorizado | Baja | Medio | Bajo | Aceptar (control OK) |

### Documentos exigidos por la norma

Alcance del SGSI, política de seguridad, metodología de evaluación de riesgos, objetivos de seguridad medibles, Declaración de Aplicabilidad, Plan de Tratamiento de Riesgos, procedimiento de auditoría interna, procedimiento de gestión de no conformidades y registro de incidentes.

---

## 6. El proceso de certificación

| Fase | Descripción |
|------|-------------|
| **1. Preparación** | Implantar el SGSI, aplicar controles, generar evidencias (6-18 meses) |
| **2. Auditoría interna** | Realizada por personal propio o externo, previa a la certificación |
| **3. Auditoría de certificación — Fase 1** | El organismo certificador revisa la documentación del SGSI |
| **4. Auditoría de certificación — Fase 2** | Auditoría in situ, revisión de implementación real |
| **5. Emisión del certificado** | Válido 3 años, con auditorías de seguimiento anuales |

### Tipos de no conformidad

| Tipo | Descripción |
|------|-------------|
| **Mayor** | Incumplimiento grave o sistémico que puede bloquear la certificación |
| **Menor** | Incumplimiento puntual, se admite plan de acción con plazo |

---

## 7. Esquema Nacional de Seguridad (ENS)

Marco obligatorio para la administración pública española y sus proveedores, categorizado por niveles: **Básico**, **Medio** y **Alto**.

ISO 27001 y ENS están ampliamente alineados: buena parte de la evidencia recopilada para uno sirve para el otro.

---

## 8. GDPR: checklist de cumplimiento

| Requisito | Detalle |
|-----------|---------|
| Consentimiento | Explícito y documentado para tratar datos personales |
| Notificación de brechas | Máximo 72 horas a la autoridad de control |
| RAT | Registro de Actividades de Tratamiento actualizado |
| Derechos de usuario | Acceso, rectificación, supresión, portabilidad |
| Multas | Hasta 10 millones de euros o el 10% de la facturación (hasta 20M€ o 4% en infracciones graves) |

---

## 9. PCI DSS

Obligatorio para bancos y empresas que procesan pagos con tarjeta:

- Cifrado de datos de tarjeta en tránsito y en reposo
- Monitorización continua de accesos a sistemas de pago
- Segmentación de red que aísle el entorno CDE

---

## 10. DORA y NIS2

**DORA** (sector financiero/asegurador UE): garantizar la continuidad operativa asumiendo que las entidades serán atacadas. Exige pruebas de resiliencia operativa digital periódicas.

**NIS2** (infraestructuras críticas: salud, energía, transporte, agua): resiliencia digital, multas más estrictas, cooperación entre estados miembros.

---

## 11. GRC en la práctica diaria

### Estructura mínima de un Plan de Continuidad de Negocio (BCP)

1. **Análisis de Impacto en el Negocio (BIA):** identificar procesos críticos y su RTO
2. **Estrategias de recuperación** por proceso crítico
3. **Plan de comunicación de crisis**
4. **Pruebas periódicas del plan** (simulacros) y actualización

---

## 12. Checklist de repaso

- [ ] Explico qué certifica ISO 27001 (gestión, no productos)
- [ ] Conozco las cláusulas 4-10 y qué exige cada una
- [ ] Clasifico controles del Anexo A en sus 4 categorías
- [ ] Distinguo entre no conformidad mayor y menor
- [ ] Conozco los requisitos clave del GDPR
- [ ] Sé qué es el ENS y cuándo es obligatorio
- [ ] Entiendo la diferencia entre riesgo inherente y residual

---

> **Siguiente tema:** [[IA en Ciberseguridad]] — ML, Deep Learning, LLMs en SOC