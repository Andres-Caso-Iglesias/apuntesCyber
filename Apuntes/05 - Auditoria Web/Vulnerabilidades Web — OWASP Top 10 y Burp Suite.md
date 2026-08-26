

> [!info] Relacionado con
> [[OWASP Top 10 - CVE CVSS CWE]] Â· [[Burp Suite - Framework de AuditorÃ­a]] Â· [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web]] Â· [[MetodologÃ­a de ExplotaciÃ³n]]
> â†’

---

## â‘  OWASP Top 10:2025 â€” Las 10 categorÃ­as

El **OWASP Top 10** agrupa las **10 categorÃ­as de vulnerabilidades web mÃ¡s frecuentes**. Se construye analizando todos los CVE publicados y clasificÃ¡ndolos por tipo.

> [!important] Para quÃ© sirve de verdad
> Sirve como **marco comÃºn para el informe** y la parte burocrÃ¡tica frente al cliente. Demuestra al CISO/CEO que se han revisado las vulnerabilidades mÃ¡s tÃ­picas. **No hay que memorizarlo de memoria ni obsesionarse con clasificar**: en una auditorÃ­a real, una vulnerabilidad encadenada puede tocar varias categorÃ­as a la vez.

| # | CategorÃ­a | DescripciÃ³n |
|---|----------|-------------|
| **A01** | Broken Access Control | IDOR, escalada, Path Traversal. Muy frecuente en auditorÃ­a diaria. |
| **A02** | Security Misconfiguration | Credenciales por defecto, paneles expuestos, cabeceras inseguras, mensajes de error que filtran rutas. |
| **A03** | Software Supply Chain Failures | **NUEVA**. LibrerÃ­as y dependencias vulnerables o comprometidas (backdoors). Gran preocupaciÃ³n de los CISO por el desarrollo masivo con IA. |
| **A04** | Cryptographic Failures | Cifrados dÃ©biles, claves mal gestionadas, TLS mal configurado. |
| **A05** | Insecure Design | LÃ³gica de negocio, subidas de archivos sin validaciÃ³n, falta de lÃ­mites. |
| **A06** | Injection | [[SQLMap]], XSS, command injection, LDAP, NoSQL. Sigue muy alto en el ranking. |
| **A07** | Authentication Failures | EnumeraciÃ³n de usuarios, contraseÃ±as dÃ©biles, ausencia de bloqueo/rate limit. |
| **A08** | Software/Data Integrity Failures | CI/CD sin verificaciÃ³n de integridad, deserializaciÃ³n insegura. |
| **A09** | Security Logging & Alerting | Falta de logs y alertas. Impide forense posterior. |
| **A10** | Mishandling of Exceptional Conditions | **NUEVA**. Manejo de errores que filtra informaciÃ³n de mÃ¡s. Ligado a A02. |

> [!warning] CAMBIOS vs 2021
> Dos categorÃ­as nuevas (A03, A10), SSRF absorbido en A01, Injection y Cryptographic bajan. Si ves material con Injection en #3, es de 2021.

â†’

> [!tip] Ejercicio mental
> Si una aplicaciÃ³n permite fuerza bruta porque no bloquea peticiones, Â¿en quÃ© categorÃ­a cae? No es A01 â†’ es **A07**, fallo de autenticaciÃ³n. La ausencia de firewall/bloqueo lo habilita, pero la vulnerabilidad reportada es la enumeraciÃ³n/fuerza bruta.

---

## â‘¡ CVSS, CWE y CVE â€” Vocabulario de la industria

| Sigla | Significa | QuÃ© puntÃºa/clasifica |
|-------|-----------|----------------------|
| **CWE** | Common Weakness Enumeration | Tipos de debilidad genÃ©ricos (no un producto concreto) |
| **CVE** | Common Vulnerabilities and Exposures | Vulnerabilidad concreta y pÃºblica (el "DNI" de cada fallo) |
| **CVSS** | Common Vulnerability Scoring System | PuntuaciÃ³n 0-10 de criticidad |

> [!important] La analogÃ­a
> **CWE** = enfermedad genÃ©rica ("infecciÃ³n respiratoria")
> **CVE** = caso clÃ­nico concreto ("neumonÃ­a de Juan")
> **CVSS** = gravedad (de leve a crÃ­tica)
> **OWASP Top 10** = ranking de enfermedades mÃ¡s frecuentes

| Score | Severidad |
|-------|----------|
| 0.0 | None |
| 0.1 â€“ 3.9 | **Low** |
| 4.0 â€“ 6.9 | **Medium** |
| 7.0 â€“ 8.9 | **High** |
| 9.0 â€“ 10.0 | **Critical** |

> [!tip] Principio clave
> Solo se categoriza como crÃ­tico/alto/medio/bajo lo que se ha **explotado**. Si solo hay indicios â†’ se reporta como **informativa** (sin puntuaciÃ³n).

---

## â‘¢ Dos metodologÃ­as que NO hay que confundir

| MetodologÃ­a de informe / cliente | MetodologÃ­a tÃ©cnica del hacker |
|---|---|
| Lo que paga y espera el cliente | Lo que el auditor hace realmente por detrÃ¡s |
| Se basa en OWASP Top 10 y categorizaciÃ³n | EnumeraciÃ³n â†’ anÃ¡lisis â†’ explotaciÃ³n encadenada |
| Reporta solo el **QUÃ‰** (vulnerabilidad concreta) | Prueba muchas cosas, encadena fallos, descarta caminos |
| No es un write-up paso a paso | SÃ­ puede ser exploratoria y desordenada |

> [!warning] ERROR COMÃšN
> Una auditorÃ­a real **no es un write-up** del estilo "hice nmap, luego curl, luego tal". En el informe se reporta la **vulnerabilidad concreta** (ej: enumeraciÃ³n de usuario â†’ A07), no toda la cadena de comandos.

### "Pruebas realizadas"

Apartado del informe donde se documenta **lo que se ha probado aunque no haya dado resultado** (ej: "probÃ© un SQLi en el buscador X, metÃ­ la comilla y estaba sanitizado"). Da valor al cliente y demuestra el trabajo realizado.

> [!warning] Cuidado con SQLMAP
> Si el cliente pide pocas peticiones y adjuntas una captura de **SQLMAP** (que lanza muchÃ­simas peticiones) como "prueba realizada", queda muy mal. Controla el ruido y respeta el alcance acordado.

---

## â‘£ MetodologÃ­a de auditorÃ­a web

```
Reconocimiento y enumeraciÃ³n
 â†“
AnÃ¡lisis de vulnerabilidades (mapeo del stack â†’ CVE / exploits)
 â†“
ExplotaciÃ³n
 â†“
Post-explotaciÃ³n y escalada (poco peso en web)
â†’
 â†“
DocumentaciÃ³n e informe
```

> [!tip] El paso intermedio
> Durante el **anÃ¡lisis de vulnerabilidades** el auditor se hace su propio mapa mental: Â¿hay control de acceso? Â¿puedo inyectar en alguna parte? Â¿los componentes estÃ¡n desactualizados? El contexto manda.

### Web real vs mÃ¡quina de HTB

| Aspecto | MÃ¡quina HTB / VulnHub | AuditorÃ­a web real |
|---------|----------------------|-------------------|
| InformaciÃ³n expuesta | La justa y necesaria | MuchÃ­sima: subdominios, datos, configuraciones |
| Permiso | Todo estÃ¡ habilitado para hackear | Hay un scope y reglas que respetar |
| Impacto de un IDOR | Suele dar igual (datos ficticios) | CrÃ­tico: ver datos, tarjetas, info de clientes reales |
| DenegaciÃ³n de servicio | Te reinician el lab | Puede tirar un servicio real â†’ problema grave con el cliente |

> [!warning] Scope y ruido importan
> Aunque un servicio bloquee la fuerza bruta, con Burp Suite se puede simular la secuencia mÃ¡s lenta (tardando horas en vez de minutos) imitando a una persona haciendo clic. Pero hay que valorar siempre si la denegaciÃ³n de servicio entra o no en el alcance: cada cliente es un mundo.

---

## â‘¤ Burp Suite â€” Proxy man-in-the-middle

**Burp Suite** actÃºa como **man in the middle** entre el navegador y el servidor: intercepta las peticiones antes de que lleguen al servidor, permite **verlas, modificarlas y decidir si pasan o no**.

```
Navegador (tÃº)
 â†“
Proxy de Burp â€” 127.0.0.1:8080 (intercepta / modifica)
 â†“
Servidor web
```

### PestaÃ±as principales

| PestaÃ±a | Para quÃ© |
|---------|---------|
| **Proxy** | NÃºcleo de Burp. Intercept ON/OFF, Forward, HTTP History |
| **Repeater** | Repite y modifica una peticiÃ³n concreta tantas veces como se quiera |
| **Intruder** | Automatiza/itera valores (fuerza bruta de credenciales, fuzzing) |
| **Target / Dashboard** | Vista general del objetivo y la actividad |

> [!info] Para esta sesiÃ³n basta con dominar **Proxy** y entender un poco el **Repeater**. Son las dos que mÃ¡s se usan.

### Flujo bÃ¡sico de trabajo

1. Activar **Intercept ON** en la pestaÃ±a Proxy
2. Navegar en la web y dejar que Burp capture las peticiones
3. Ir haciendo **Forward** para dejar pasar las que no interesan
4. Cuando aparece una peticiÃ³n interesante â†’ **clic derecho â†’ Send to Repeater**
5. En el **Repeater**, pulsar **Send** y analizar/modificar parÃ¡metros y respuestas

### Dos formas de enrutar el trÃ¡fico

| OpciÃ³n | DescripciÃ³n | Ventaja / inconveniente |
|--------|------------|------------------------|
| **Open Browser** | Navegador interno preconfigurado para el proxy | Recomendado al empezar: menos ruido, sin lÃ­os de configuraciÃ³n |
| **FoxyProxy** | ExtensiÃ³n que mete tu navegador en el proxy (127.0.0.1:8080) | MÃ¡s rÃ¡pido para gente experta, pero mucho ruido y requiere activarlo manualmente |

> [!warning] RUIDO
> Trabajar en el navegador habitual con muchas pestaÃ±as abiertas genera muchÃ­simo trÃ¡fico irrelevante (analytics, redes sociales, etc.). Al empezar conviene el **Open Browser** o un navegador limpio dedicado.

### ConfiguraciÃ³n de FoxyProxy

| Campo | Valor |
|-------|-------|
| Nombre | Burp Suite |
| Tipo | HTTP |
| Host / IP | 127.0.0.1 |
| Puerto | **8080** |

### Certificado de Burp (PortSwigger)

1. Con Burp abierto â†’ `http://localhost:8080` â†’ **CA Certificate** â†’ descargar
2. Firefox â†’ Administrar certificados â†’ Importar â†’ seleccionar cacert
3. Verificar: debe aparecer **PortSwigger** como CA

> [!info] Si usas el navegador de HTB (VPN dentro de Kali), estÃ¡s en una red interna sin internet, por lo que el ruido de terceros desaparece.

---

## â‘¥ Herramientas de la sesiÃ³n

| Herramienta | Objetivo | Fase | Nivel |
|------------|---------|------|-------|
| **Burp Suite** (Proxy/Repeater/Intruder) | Intercept y modificaciÃ³n de trÃ¡fico HTTP/HTTPS | Recon, anÃ¡lisis y explotaciÃ³n web | Introducida |
| **FoxyProxy** | Enrutar el navegador hacia el proxy de Burp | ConfiguraciÃ³n previa | Introducida |
| **CVSS Calculator** | Puntuar criticidad de una vulnerabilidad | AnÃ¡lisis / informe | Mencionada |
| **Nmap** | Detectar puertos y servicios | EnumeraciÃ³n | Recurrente |
| **Curl** | InteracciÃ³n manual con servicios web | EnumeraciÃ³n web | Mencionada |
| **SQLMAP** | Automatizar SQL Injection | ExplotaciÃ³n | Mencionada |
| **Hydra** | Fuerza bruta de credenciales | ExplotaciÃ³n / autenticaciÃ³n | Practicada |

â†’

---

## Checklist de repaso

- [ ] Â¿SÃ© explicar quÃ© es el OWASP Top 10 y para quÃ© sirve realmente?
- [ ] Â¿Puedo poner un ejemplo de A01 (IDOR), A02 (misconfiguration) y A07 (autenticaciÃ³n)?
- [ ] Â¿Entiendo quÃ© es CVSS y la diferencia entre crÃ­tico/alto/medio/bajo e informativa?
- [ ] Â¿Distingo la metodologÃ­a de informe de la metodologÃ­a tÃ©cnica del hacker?
- [ ] Â¿SÃ© por quÃ© una web real no es como una mÃ¡quina de HTB (scope, ruido, DoS)?
- [ ] Â¿SÃ© quÃ© es Burp Suite y por quÃ© es un proxy / man in the middle?
- [ ] Â¿SÃ© interceptar, hacer Forward y enviar una peticiÃ³n al Repeater?
- [ ] Â¿Entiendo la diferencia entre Open Browser y FoxyProxy?
- [ ] Â¿SÃ© instalar el certificado de PortSwigger desde http://burpsuite/?

â†’

â†’
â†’
