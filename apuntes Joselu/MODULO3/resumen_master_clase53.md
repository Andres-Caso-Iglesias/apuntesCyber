> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 53**
> **Módulo:** MODULO3
> **Tema:** Clase 53
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 53. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y nota sobre esta clase

Esta sesión la imparte **Castillo** (Carlos Castillo).

Al leer la transcripción, el contenido técnico es **idéntico a la Clase 52**: misma sesión de repaso de SSRF, mismos ejemplos (Repsol, plátano con chorizo, bypass de whitelist y Open Redirect), misma práctica en vivo con Chema, mismo laboratorio de PortSwigger.

La razón es que el máster tiene **dos convocatoria paralelas**: el grupo A (14 alumnos, la Clase 52) y el grupo B (8 alumnos en este caso).

Castillo imparte la misma sesión para ambos grupos el mismo viernes.

**Para el contenido completo de esta sesión → ver el resumen de la Clase 52**, que cubre en detalle: - Los 4+1 tipos de bypass de SSRF (sin restricciones, scan de red con Intruder, blacklist, whitelist, Open Redirect). - El concepto de Open Redirect y sus usos (phishing en Red Team + bypass de whitelist en SSRF). - El flujo completo del laboratorio de PortSwigger con Chema en pantalla. - La metodología: buscar botones con funcionalidad → HTTP History de Burp → parámetro con URL → candidato a SSRF.

## 2.

Diferencias menores respecto a la Clase 52

La única diferencia observable entre ambas sesiones es la interacción con el grupo: - **Clase 52 (grupo A):** 14 alumnos, más participación, más preguntas en el chat. - **Clase 53 (grupo B):** 8 alumnos, sesión más íntima, ritmo ligeramente más lento para adaptarse a menos participantes.

Las explicaciones de Castillo son ligeramente distintas en el orden de exposición pero el contenido técnico es el mismo.

## 3.

Recordatorio de los conceptos clave de SSRF

Para completar el estudio de esta sesión, los conceptos fundamentales son:

### SSRF (Server-Side Request Forgery)

Usar el servidor web como mensajero para que haga peticiones HTTP a servicios de la red interna que no son accesibles desde Internet.

**Señal de detección:** parámetro cuyo valor es una URL visible en Burp HTTP History.

### Los 5 escenarios

Escenario Técnica
 --------------------------- -------------------------------------------------------
Sin restricciones `http://localhost/admin` directamente Scan de red interna Burp Intruder iterando IPs 192.168.0.1-254 Blacklist activa `127.1`, representación decimal, URL encoding Whitelist activa `@`, `#`, subdominio con el dominio autorizado Whitelist + Open Redirect URL de la app + `/redirect?url=http://127.0.0.1/admin`

### Open Redirect

Parámetro de redirección sin validar el dominio destino.

### Útil en: - **Phishing:** la URL comienza con el dominio legítimo (ej.

Repsol) pero redirige al sitio del atacante. - **Bypass de whitelist SSRF:** la whitelist valida el dominio inicial, pero no valida las redirecciones que ese dominio pueda hacer.

## 4.

Términos clave (ver tabla completa en resumen Clase 52)

Término Corrección
 ------------------------------------- --------------------------------------------------------------------------------
 *SCRF / SRF* **SSRF** (*Server-Side Request Forgery*)
 *el de plátano / el check de stock* **Check Stock** --- botón de la tienda del laboratorio PortSwigger, vector SSRF
 *Wild Lead / la de whitelist* **Whitelist** --- lista de valores permitidos
 *el repíter / repiltar* **Repeater** --- módulo de Burp Suite
 *Port Sweager / por swinger* **PortSwigger** --- plataforma de laboratorios

> [!note] *Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.* *Nota: Esta clase es la repetición de la Clase 52 para la segunda convocatoria del máster.

El resumen detallado está en el documento de la Clase 52.*

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF — Server-Side Request Forgery]— Burp Suite, Open Redirect, SSRF
- [[resumen_master_clase48.md|resumen_master_clase48]— Open Redirect, Redes, SSRF
- [[resumen_master_clase52.md|resumen_master_clase52]— Open Redirect, Redes, SSRF
- [[../PREWORK/resumen_clase5.md|resumen_clase5]— Burp Suite, Redes, SSRF
- [[../../apuntes Andres/24.07.2026 Repaso Semanal III.md|24.07.2026 Repaso Semanal III]— Open Redirect, Redes, SSRF
- [[../MODULO2/resumen_master_clase15.md|resumen_master_clase15]— Burp Suite, Redes, SSRF

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]

> #burpsuite #ia #open-redirect #pentest #redes #ssrf
