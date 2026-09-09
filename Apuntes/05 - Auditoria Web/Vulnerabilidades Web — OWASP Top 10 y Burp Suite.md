

> [!info] Relacionado con
> [[OWASP Top 10 - CVE CVSS CWE]] · [[Burp Suite - Framework de Auditoría]] · [[Apuntes/05 - Auditoria Web/Enumeración Web]] · [[Metodología de Explotación]]
> 

---

## ① OWASP Top 10:2025 "” Las 10 categorías

El **OWASP Top 10** agrupa las **10 categorías de vulnerabilidades web más frecuentes**. Se construye analizando todos los CVE publicados y clasificándolos por tipo.

> [!important] Para qué sirve de verdad
> Sirve como **marco común para el informe** y la parte burocrática frente al cliente. Demuestra al CISO/CEO que se han revisado las vulnerabilidades más típicas. **No hay que memorizarlo de memoria ni obsesionarse con clasificar**: en una auditoría real, una vulnerabilidad encadenada puede tocar varias categorías a la vez.

| # | Categoría | Descripción |
|---|----------|-------------|
| **A01** | Broken Access Control | IDOR, escalada, Path Traversal. Muy frecuente en auditoría diaria. |
| **A02** | Security Misconfiguration | Credenciales por defecto, paneles expuestos, cabeceras inseguras, mensajes de error que filtran rutas. |
| **A03** | Software Supply Chain Failures | **NUEVA**. Librerías y dependencias vulnerables o comprometidas (backdoors). Gran preocupación de los CISO por el desarrollo masivo con IA. |
| **A04** | Cryptographic Failures | Cifrados débiles, claves mal gestionadas, TLS mal configurado. |
| **A05** | Insecure Design | Lógica de negocio, subidas de archivos sin validación, falta de límites. |
| **A06** | Injection | [[SQLMap]], XSS, command injection, LDAP, NoSQL. Sigue muy alto en el ranking. |
| **A07** | Authentication Failures | Enumeración de usuarios, contraseñas débiles, ausencia de bloqueo/rate limit. |
| **A08** | Software/Data Integrity Failures | CI/CD sin verificación de integridad, deserialización insegura. |
| **A09** | Security Logging & Alerting | Falta de logs y alertas. Impide forense posterior. |
| **A10** | Mishandling of Exceptional Conditions | **NUEVA**. Manejo de errores que filtra información de más. Ligado a A02. |

> [!warning] CAMBIOS vs 2021
> Dos categorías nuevas (A03, A10), SSRF absorbido en A01, Injection y Cryptographic bajan. Si ves material con Injection en #3, es de 2021.



> [!tip] Ejercicio mental
> Si una aplicación permite fuerza bruta porque no bloquea peticiones, ¿en qué categoría cae? No es A01 → es **A07**, fallo de autenticación. La ausencia de firewall/bloqueo lo habilita, pero la vulnerabilidad reportada es la enumeración/fuerza bruta.

---

## ② CVSS, CWE y CVE "” Vocabulario de la industria

| Sigla | Significa | Qué puntúa/clasifica |
|-------|-----------|----------------------|
| **CWE** | Common Weakness Enumeration | Tipos de debilidad genéricos (no un producto concreto) |
| **CVE** | Common Vulnerabilities and Exposures | Vulnerabilidad concreta y pública (el "DNI" de cada fallo) |
| **CVSS** | Common Vulnerability Scoring System | Puntuación 0-10 de criticidad |

> [!important] La analogía
> **CWE** = enfermedad genérica ("infección respiratoria")
> **CVE** = caso clínico concreto ("neumonía de Juan")
> **CVSS** = gravedad (de leve a crítica)
> **OWASP Top 10** = ranking de enfermedades más frecuentes

| Score | Severidad |
|-------|----------|
| 0.0 | None |
| 0.1 "“ 3.9 | **Low** |
| 4.0 "“ 6.9 | **Medium** |
| 7.0 "“ 8.9 | **High** |
| 9.0 "“ 10.0 | **Critical** |

> [!tip] Principio clave
> Solo se categoriza como crítico/alto/medio/bajo lo que se ha **explotado**. Si solo hay indicios → se reporta como **informativa** (sin puntuación).

---

## ③ Dos metodologías que NO hay que confundir

| Metodología de informe / cliente | Metodología técnica del hacker |
|---|---|
| Lo que paga y espera el cliente | Lo que el auditor hace realmente por detrás |
| Se basa en OWASP Top 10 y categorización | Enumeración → análisis → explotación encadenada |
| Reporta solo el **QUÉ** (vulnerabilidad concreta) | Prueba muchas cosas, encadena fallos, descarta caminos |
| No es un write-up paso a paso | Sí puede ser exploratoria y desordenada |

> [!warning] ERROR COMÚN
> Una auditoría real **no es un write-up** del estilo "hice nmap, luego curl, luego tal". En el informe se reporta la **vulnerabilidad concreta** (ej: enumeración de usuario → A07), no toda la cadena de comandos.

### "Pruebas realizadas"

Apartado del informe donde se documenta **lo que se ha probado aunque no haya dado resultado** (ej: "probé un SQLi en el buscador X, metí la comilla y estaba sanitizado"). Da valor al cliente y demuestra el trabajo realizado.

> [!warning] Cuidado con SQLMAP
> Si el cliente pide pocas peticiones y adjuntas una captura de **SQLMAP** (que lanza muchísimas peticiones) como "prueba realizada", queda muy mal. Controla el ruido y respeta el alcance acordado.

---

## ④ Metodología de auditoría web

```
Reconocimiento y enumeración
 →“
Análisis de vulnerabilidades (mapeo del stack → CVE / exploits)
 →“
Explotación
 →“
Post-explotación y escalada (poco peso en web)
→
 →“
Documentación e informe
```

> [!tip] El paso intermedio
> Durante el **análisis de vulnerabilidades** el auditor se hace su propio mapa mental: ¿hay control de acceso? ¿puedo inyectar en alguna parte? ¿los componentes están desactualizados? El contexto manda.

### Web real vs máquina de HTB

| Aspecto | Máquina HTB / VulnHub | Auditoría web real |
|---------|----------------------|-------------------|
| Información expuesta | La justa y necesaria | Muchísima: subdominios, datos, configuraciones |
| Permiso | Todo está habilitado para hackear | Hay un scope y reglas que respetar |
| Impacto de un IDOR | Suele dar igual (datos ficticios) | Crítico: ver datos, tarjetas, info de clientes reales |
| Denegación de servicio | Te reinician el lab | Puede tirar un servicio real → problema grave con el cliente |

> [!warning] Scope y ruido importan
> Aunque un servicio bloquee la fuerza bruta, con Burp Suite se puede simular la secuencia más lenta (tardando horas en vez de minutos) imitando a una persona haciendo clic. Pero hay que valorar siempre si la denegación de servicio entra o no en el alcance: cada cliente es un mundo.

---

## ⑤ Burp Suite "” Proxy man-in-the-middle

**Burp Suite** actúa como **man in the middle** entre el navegador y el servidor: intercepta las peticiones antes de que lleguen al servidor, permite **verlas, modificarlas y decidir si pasan o no**.

```
Navegador (tú)
 →“
Proxy de Burp "” 127.0.0.1:8080 (intercepta / modifica)
 →“
Servidor web
```

### Pestañas principales

| Pestaña | Para qué |
|---------|---------|
| **Proxy** | Núcleo de Burp. Intercept ON/OFF, Forward, HTTP History |
| **Repeater** | Repite y modifica una petición concreta tantas veces como se quiera |
| **Intruder** | Automatiza/itera valores (fuerza bruta de credenciales, fuzzing) |
| **Target / Dashboard** | Vista general del objetivo y la actividad |

> [!info] Para esta sesión basta con dominar **Proxy** y entender un poco el **Repeater**. Son las dos que más se usan.

### Flujo básico de trabajo

1. Activar **Intercept ON** en la pestaña Proxy
2. Navegar en la web y dejar que Burp capture las peticiones
3. Ir haciendo **Forward** para dejar pasar las que no interesan
4. Cuando aparece una petición interesante → **clic derecho → Send to Repeater**
5. En el **Repeater**, pulsar **Send** y analizar/modificar parámetros y respuestas

### Dos formas de enrutar el tráfico

| Opción | Descripción | Ventaja / inconveniente |
|--------|------------|------------------------|
| **Open Browser** | Navegador interno preconfigurado para el proxy | Recomendado al empezar: menos ruido, sin líos de configuración |
| **FoxyProxy** | Extensión que mete tu navegador en el proxy (127.0.0.1:8080) | Más rápido para gente experta, pero mucho ruido y requiere activarlo manualmente |

> [!warning] RUIDO
> Trabajar en el navegador habitual con muchas pestañas abiertas genera muchísimo tráfico irrelevante (analytics, redes sociales, etc.). Al empezar conviene el **Open Browser** o un navegador limpio dedicado.

### Configuración de FoxyProxy

| Campo | Valor |
|-------|-------|
| Nombre | Burp Suite |
| Tipo | HTTP |
| Host / IP | 127.0.0.1 |
| Puerto | **8080** |

### Certificado de Burp (PortSwigger)

1. Con Burp abierto → `http://localhost:8080` → **CA Certificate** → descargar
2. Firefox → Administrar certificados → Importar → seleccionar cacert
3. Verificar: debe aparecer **PortSwigger** como CA

> [!info] Si usas el navegador de HTB (VPN dentro de Kali), estás en una red interna sin internet, por lo que el ruido de terceros desaparece.

---

## ⑥ Herramientas de la sesión

| Herramienta | Objetivo | Fase | Nivel |
|------------|---------|------|-------|
| **Burp Suite** (Proxy/Repeater/Intruder) | Intercept y modificación de tráfico HTTP/HTTPS | Recon, análisis y explotación web | Introducida |
| **FoxyProxy** | Enrutar el navegador hacia el proxy de Burp | Configuración previa | Introducida |
| **CVSS Calculator** | Puntuar criticidad de una vulnerabilidad | Análisis / informe | Mencionada |
| **Nmap** | Detectar puertos y servicios | Enumeración | Recurrente |
| **Curl** | Interacción manual con servicios web | Enumeración web | Mencionada |
| **SQLMAP** | Automatizar SQL Injection | Explotación | Mencionada |
| **Hydra** | Fuerza bruta de credenciales | Explotación / autenticación | Practicada |


---

## Checklist de repaso

- [ ] ¿Sé explicar qué es el OWASP Top 10 y para qué sirve realmente?
- [ ] ¿Puedo poner un ejemplo de A01 (IDOR), A02 (misconfiguration) y A07 (autenticación)?
- [ ] ¿Entiendo qué es CVSS y la diferencia entre crítico/alto/medio/bajo e informativa?
- [ ] ¿Distingo la metodología de informe de la metodología técnica del hacker?
- [ ] ¿Sé por qué una web real no es como una máquina de HTB (scope, ruido, DoS)?
- [ ] ¿Sé qué es Burp Suite y por qué es un proxy / man in the middle?
- [ ] ¿Sé interceptar, hacer Forward y enviar una petición al Repeater?
- [ ] ¿Entiendo la diferencia entre Open Browser y FoxyProxy?
- [ ] ¿Sé instalar el certificado de PortSwigger desde http://burpsuite/?



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../transcripciones/Julio/27.07.2026 PortSwigger SSTI.md|27.07.2026 PortSwigger SSTI]] — Linux, Metasploit, Nmap
- [[../../apuntes Chema/Maquinas/Vaccine (Tier 2) — Repaso en profundidad.md|Vaccine (Tier 2) — Repaso en profundidad]] — IDOR, Metasploit, VulnHub
- [[../../apuntes Andres/27.07.2026 PortSwigger SSTI.md|27.07.2026 PortSwigger SSTI]] — Linux, Metasploit, Netcat / Reverse Shells
- [[../../transcripciones/Julio/17.07.2026 PortSwigger Introduccion y repaso Path Traversal.md|17.07.2026 PortSwigger Introduccion y repaso Path Traversal]] — Linux, Metasploit, Nmap
- [[../../apuntes Andres/29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web.md|29.06.2026 Vulnerabilidades Web OWASP Top 10 y Reconocimiento Web]] — Linux, Metasploit, SQLMap
- [[OWASP Top 10 - CVE CVSS CWE.md|OWASP Top 10 - CVE CVSS CWE]] — IDOR, Metasploit, SQLMap

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]

> #burpsuite #command-injection #forense #hack-the-box #hydra #idor #kali #lfi #linux #metasploit #netcat #nmap #pentest #post-explotacion #redes #reverse-shell #sqli #sqlmap #ssrf #ssti #vulnhub #xss
