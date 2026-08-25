

> [!info] Relacionado con
> [[Burp Suite - Framework de AuditorÃ­a]] Â· [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web]] Â· [[MetodologÃ­a de ExplotaciÃ³n]] Â· [[Normativa - ISO 27001, GDPR, ENS]]
> â†’

---

## â‘  El vocabulario de la industria

| Sigla | Significa | QuiÃ©n lo mantiene |
|-------|-----------|-------------------|
| **OWASP** | Open Worldwide Application Security Project | Comunidad OWASP |
| **CWE** | Common Weakness Enumeration (tipos de debilidad) | MITRE |
| **CVE** | Common Vulnerabilities and Exposures (vulnerabilidad concreta) | MITRE / NVD |
| **CVSS** | Common Vulnerability Scoring System (puntuaciÃ³n 0-10) | FIRST |

> [!important] La analogÃ­a
> **CWE** = enfermedad genÃ©rica ("infecciÃ³n respiratoria")
> **CVE** = caso clÃ­nico concreto ("neumonÃ­a de Juan")
> **CVSS** = gravedad (de leve a crÃ­tica)
> **OWASP Top 10** = ranking de enfermedades mÃ¡s frecuentes

---

## â‘¡ CWE â€” Common Weakness Enumeration

CatÃ¡logo de **tipos de debilidad** genÃ©ricos (no un producto concreto).

| CWE | Debilidad | CategorÃ­a OWASP |
|-----|----------|-----------------|
| CWE-89 | [[SQLMap]] Injection | A05 InyecciÃ³n |
| CWE-79 | XSS | A05 InyecciÃ³n |
| CWE-22 | Path Traversal / LFI | A01 Access Control |
| CWE-287 | Improper Authentication | A07 AutenticaciÃ³n |
| CWE-209 | Info en errores | A10 Excepciones |

---

## â‘¢ CVE â€” Common Vulnerabilities and Exposures

El **"DNI"** de cada vulnerabilidad pÃºblica.

```
CVE-2021-44228
 â”‚ â”‚ â”‚
 â”‚ â”‚ â””â”€â”€ NÃºmero secuencial
 â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€ AÃ±o de asignaciÃ³n
 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Prefijo fijo
```

**Ejemplo:** CVE-2021-44228 = **Log4Shell**

> [!info] NVD
> La NVD (National Vulnerability Database) enriquece cada CVE con su CWE, CVSS y productos afectados.

---

## â‘£ CVSS â€” PuntuaciÃ³n de severidad

| Score | Severidad |
|-------|----------|
| 0.0 | None |
| 0.1 â€“ 3.9 | **Low** |
| 4.0 â€“ 6.9 | **Medium** |
| 7.0 â€“ 8.9 | **High** |
| 9.0 â€“ 10.0 | **Critical** |

### MÃ©tricas base del CVSS

| MÃ©trica | QuÃ© mide |
|---------|---------|
| **Attack Vector (AV)** | CÃ³mo se accede (red, adyacente, local, fÃ­sico) |
| **Attack Complexity (AC)** | Lo difÃ­cil que es explotarlo |
| **Privileges Required (PR)** | Permisos necesarios |
| **User Interaction (UI)** | Si requiere interacciÃ³n de la vÃ­ctima |
| **Impacto CIA** | Confidencialidad, Integridad, Disponibilidad |

### Ejemplo de vector

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
 â”‚ â”‚ â”‚ â”‚ â”‚ â”‚ â”‚ â”‚
 â”‚ â”‚ â”‚ â”‚ â”‚ â””â”€â”€â”´â”€â”€â”´â”€ Alto impacto CIA
 â”‚ â”‚ â”‚ â”‚ â””â”€â”€ Sin impacto en otros componentes
 â”‚ â”‚ â”‚ â””â”€â”€ Sin interacciÃ³n
 â”‚ â”‚ â””â”€â”€ Sin privilegios
 â”‚ â””â”€â”€ Complejidad baja
 â””â”€â”€ Vector de red
```

---

## â‘¤ OWASP Top 10:2025

| # | CategorÃ­a | Notas |
|---|----------|-------|
| **A01** | Broken Access Control | IDOR, escalada, Path Traversal. SSRF absorbido aquÃ­. |
â†’
| **A02** | Security Misconfiguration | Credenciales por defecto, cabeceras inseguras. Sube al #2. |
| **A03** | Software Supply Chain Failures | **NUEVA**. Dependencias vulnerables. |
| **A04** | Cryptographic Failures | Cifrado dÃ©bil, TLS mal configurado. |
| **A05** | Injection | [[SQLMap]], XSS, command injection, LDAP. |
| **A06** | Insecure Design | Fallos de diseÃ±o, falta de threat modeling. |
| **A07** | Authentication Failures | EnumeraciÃ³n de usuarios, fuerza bruta. |
| **A08** | Software/Data Integrity Failures | CI/CD sin verificaciÃ³n, deserializaciÃ³n insegura. |
| **A09** | Security Logging & Alerting | Falta de logs y alertas. |
| **A10** | Mishandling of Exceptional Conditions | **NUEVA**. Mala gestiÃ³n de errores. |

â†’

> [!warning] CAMBIOS vs 2021
> Dos categorÃ­as nuevas (A03, A10), SSRF absorbido en A01, Injection y Cryptographic bajan. Si ves material con Injection en #3, es de 2021.

â†’

---

## â‘¥ La cascada en la auditorÃ­a

```
OWASP Top 10 â†’ CWE â†’ CVE â†’ CVSS â†’ PriorizaciÃ³n
```

1. **OWASP** te dice quÃ© categorÃ­as buscar
2. **CWE** clasifica el tipo de fallo
3. **CVE** lo identifica concreto (si es pÃºblico)
4. **CVSS** puntÃºa para priorizar

> [!tip] BUENA PRÃCTICA
> En tus informes, acostÃºmbrate a etiquetar cada hallazgo con su categorÃ­a OWASP y su CWE. Es exactamente lo que se espera en una auditorÃ­a web junior.

---

## Checklist de repaso

- [ ] Â¿Distingo CWE (tipo), CVE (caso) y CVSS (puntuaciÃ³n)?
- [ ] Â¿Puedo nombrar las categorÃ­as OWASP 2025?
- [ ] Â¿SÃ© leer un vector CVSS?
- [ ] Â¿Entiendo la cascada OWASP â†’ CWE â†’ CVE â†’ CVSS?
- [ ] Â¿Relaciono Log4Shell con su CWE y categorÃ­a OWASP?

â†’

â†’
