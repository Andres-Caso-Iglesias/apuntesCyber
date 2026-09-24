

> [!info] Relacionado con
> [[Burp Suite - Framework de Auditoría]] · [[Apuntes/05 - Auditoria Web/Enumeración Web]] · [[Metodología de Explotación]] · [[Normativa - ISO 27001, GDPR, ENS]]
> 

---

## ① El vocabulario de la industria

| Sigla | Significa | Quién lo mantiene |
|-------|-----------|-------------------|
| **OWASP** | Open Worldwide Application Security Project | Comunidad OWASP |
| **CWE** | Common Weakness Enumeration (tipos de debilidad) | MITRE |
| **CVE** | Common Vulnerabilities and Exposures (vulnerabilidad concreta) | MITRE / NVD |
| **CVSS** | Common Vulnerability Scoring System (puntuación 0-10) | FIRST |

> [!important] La analogía
> **CWE** = enfermedad genérica ("infección respiratoria")
> **CVE** = caso clínico concreto ("neumonía de Juan")
> **CVSS** = gravedad (de leve a crítica)
> **OWASP Top 10** = ranking de enfermedades más frecuentes

---

## ② CWE "” Common Weakness Enumeration

Catálogo de **tipos de debilidad** genéricos (no un producto concreto).

| CWE | Debilidad | Categoría OWASP |
|-----|----------|-----------------|
| CWE-89 | [[SQLMap]] Injection | A05 Inyección |
| CWE-79 | XSS | A05 Inyección |
| CWE-22 | Path Traversal / LFI | A01 Access Control |
| CWE-287 | Improper Authentication | A07 Autenticación |
| CWE-209 | Info en errores | A10 Excepciones |

---

## ③ CVE "” Common Vulnerabilities and Exposures

El **"DNI"** de cada vulnerabilidad pública.

```
CVE-2021-44228
 │ │ │
 │ │ ┘── Número secuencial
 │ ┘──────── Año de asignación
 ┘───────────── Prefijo fijo
```

**Ejemplo:** CVE-2021-44228 = **Log4Shell**

> [!info] NVD
> La NVD (National Vulnerability Database) enriquece cada CVE con su CWE, CVSS y productos afectados.

---

## ④ CVSS "” Puntuación de severidad

| Score | Severidad |
|-------|----------|
| 0.0 | None |
| 0.1 "“ 3.9 | **Low** |
| 4.0 "“ 6.9 | **Medium** |
| 7.0 "“ 8.9 | **High** |
| 9.0 "“ 10.0 | **Critical** |

### Métricas base del CVSS

| Métrica | Qué mide |
|---------|---------|
| **Attack Vector (AV)** | Cómo se accede (red, adyacente, local, físico) |
| **Attack Complexity (AC)** | Lo difícil que es explotarlo |
| **Privileges Required (PR)** | Permisos necesarios |
| **User Interaction (UI)** | Si requiere interacción de la víctima |
| **Impacto CIA** | Confidencialidad, Integridad, Disponibilidad |

### Ejemplo de vector

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
 │ │ │ │ │ │ │ │
 │ │ │ │ │ ┘──┤──┤─ Alto impacto CIA
 │ │ │ │ ┘── Sin impacto en otros componentes
 │ │ │ ┘── Sin interacción
 │ │ ┘── Sin privilegios
 │ ┘── Complejidad baja
 ┘── Vector de red
```

---

## ⑤ OWASP Top 10:2025

| # | Categoría | Notas |
|---|----------|-------|
| **A01** | Broken Access Control | IDOR, escalada, Path Traversal. SSRF absorbido aquí. |

| **A02** | Security Misconfiguration | Credenciales por defecto, cabeceras inseguras. Sube al #2. |
| **A03** | Software Supply Chain Failures | **NUEVA**. Dependencias vulnerables. |
| **A04** | Cryptographic Failures | Cifrado débil, TLS mal configurado. |
| **A05** | Injection | [[SQLMap]], XSS, command injection, LDAP. |
| **A06** | Insecure Design | Fallos de diseño, falta de threat modeling. |
| **A07** | Authentication Failures | Enumeración de usuarios, fuerza bruta. |
| **A08** | Software/Data Integrity Failures | CI/CD sin verificación, deserialización insegura. |
| **A09** | Security Logging & Alerting | Falta de logs y alertas. |
| **A10** | Mishandling of Exceptional Conditions | **NUEVA**. Mala gestión de errores. |


> [!warning] CAMBIOS vs 2021
> Dos categorías nuevas (A03, A10), SSRF absorbido en A01, Injection y Cryptographic bajan. Si ves material con Injection en #3, es de 2021.

> [!info] Notas de detalle
> - **A02** (Security Misconfiguration) incluye también problemas de **XXE** por configuración del parser XML.
> - **A10** en 2025 = *Mishandling of Exceptional Conditions* (manejo deficiente de excepciones). Material anticuado puede etiquetar A10 como *SSRF* (nombre de 2021); en 2025 SSRF está **absorbido en A01**. Desconfía de tablas mixtas (nombre viejo + descripción nueva).

### Evolución temporal

| Año | Enfoque principal |
|---|---|
| **2017** | Injection, XXE, XSS, deserialization |
| **2021** | Access control, crypto, injection |
| **2025** | Supply chain, integridad del software (refleja desarrollo masivo con IA) |

> [!important] Metáfora
> Comparar 2017, 2021 y 2025 es como ver **fotografías de la misma ciudad en distintas décadas**: las calles principales siguen siendo las mismas (inyección, control de acceso), pero aparecen barrios nuevos (cadena de suministro, integridad del software).

---

## ⑥ La cascada en la auditoría

```
OWASP Top 10 → CWE → CVE → CVSS → Priorización
```

1. **OWASP** te dice qué categorías buscar
2. **CWE** clasifica el tipo de fallo
3. **CVE** lo identifica concreto (si es público)
4. **CVSS** puntúa para priorizar

> [!tip] BUENA PRÁCTICA
> En tus informes, acostúmbrate a etiquetar cada hallazgo con su categoría OWASP y su CWE. Es exactamente lo que se espera en una auditoría web junior.

### Calculadora oficial de CVSS

```bash
https://www.first.org/cvss/calculator/3.1
```

### Doble uso del Top 10

| Uso | Para qué sirve | Peso real |
|---|---|---|
| **Comunicación con el cliente** | Justificar que se revisaron las categorías más relevantes | Alto (burocrático) |
| **Metodología técnica del auditor** | Clasificar hallazgos en categorías | Bajo (la IA lo hace en segundos) |

> [!important] Las vulnerabilidades reales son cadenas
> Un fallo de autenticación habilita una configuración incorrecta que a su vez habilita una inyección. Clasificar cada eslabón en una sola categoría es artificial: el Top 10 es el **lenguaje del informe**, no la lógica del hacker.

---

## Checklist de repaso

- [ ] ¿Distingo CWE (tipo), CVE (caso) y CVSS (puntuación)?
- [ ] ¿Puedo nombrar las categorías OWASP 2025?
- [ ] ¿Sé leer un vector CVSS?
- [ ] ¿Entiendo la cascada OWASP → CWE → CVE → CVSS?
- [ ] ¿Relaciono Log4Shell con su CWE y categoría OWASP?
- [ ] ¿Señalo cuándo una tabla mezcla el nombre A10 de 2021 con la descripción de 2025?
- [ ] ¿Sé que A02 incluye XXE y que SSRF (2021) cae en A01 (2025)?
- [ ] ¿Diferencio el uso burocrático del Top 10 (cliente) del uso técnico (auditor)?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — Post-Explotacion, Seguridad, XXE
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]] — Post-Explotacion, Seguridad, XXE
- [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite.md|Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] — Command Injection / RCE, Post-Explotacion, Seguridad
- [[../../apuntes Joselu/MODULO3/resumen_master_clase36.md|resumen_master_clase36]] — Post-Explotacion, Seguridad, XXE
- [[../../apuntes Andres/11.07.2026 Owasp Top 10 XXE Labs II.md|11.07.2026 Owasp Top 10 XXE Labs II]] — Command Injection / RCE, Post-Explotacion, XXE
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — SQL Injection, XSS, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, SQL, Seguridad
- [[../../../programacion/Go/testing_go.md|testing_go]] — Programacion: Bases de Datos, SQL, Seguridad

> #blue_team #burpsuite #cli #command_injection #crypto #database #devops #go #hydra #idor #java #lfi #metasploit #netcat #normativa #pentest #post_explotacion #redes #seguridad #sql #sqli #sqlmap_tool #ssrf #web #xss #xxe
