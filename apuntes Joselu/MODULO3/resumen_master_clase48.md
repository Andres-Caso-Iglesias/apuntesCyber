> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 48**
> **Módulo:** MODULO3
> **Tema:** Clase 48
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 48. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

Esta sesión cubre la vulnerabilidad **SSRF (Server-Side Request Forgery)** dentro del módulo de PortSwigger.

El hilo conductor es simple pero poderoso: cuando un servidor hace peticiones a otras direcciones por cuenta propia, y esa dirección puede ser controlada por el atacante, el servidor se convierte en un **proxy involuntario** desde el que se puede alcanzar infraestructura interna, servicios en `localhost` y metadatos de cloud que normalmente son inaccesibles desde el exterior.

La sesión cubre los tres contextos canónicos de SSRF: contra el propio servidor, contra infraestructura interna, y contra servicios de metadatos de AWS.

# Qué es SSRF y por qué importa

SSRF ocurre cuando una aplicación web hace una petición HTTP a una URL que puede ser controlada, total o parcialmente, por el atacante.

La clave es que **la petición la hace el servidor, no el navegador del usuario**.

El servidor tiene acceso a recursos que el atacante no puede alcanzar directamente:

- `localhost` y servicios que solo escuchan en interfaces internas.
- Redes internas y servicios sin autenticación.
- Endpoints de metadatos de proveedores cloud.

**Vector de detección:** el mismo que en path traversal.

En Burp Suite se buscan parámetros que contengan URLs o partes de URLs, como `url=`, `api=`, `endpoint=`, `redirect=`, `fetch=` o `resource=`.

Cualquier parámetro que sugiera que el servidor va a hacer una petición a partir de ese valor es un candidato a SSRF.

> **Metáfora útil:** el servidor es el empleado con tarjeta de acceso que puede entrar en salas donde tú no puedes.

Si consigues decirle al empleado a qué sala ir y qué traerte, no necesitas la tarjeta.

# Caso 1 --- SSRF contra el propio servidor (localhost)

La aplicación de la tienda tiene un panel de administración en `/admin` que no es accesible desde el exterior: solo responde a peticiones provenientes de `localhost`.

Existe una funcionalidad de "comprobar stock" que hace una petición al backend usando un parámetro `stockApi` con la URL de la API interna.

Al interceptar esa petición en Burp y modificar el valor por `http://localhost/admin`, el servidor hace la petición a sí mismo.

Como el origen de la petición es el propio servidor, el panel de administración responde con el contenido completo (HTML del panel interno con los usuarios del sistema).

Para completar el laboratorio se **encadena** la petición:

## 1.

Se obtiene la URL del endpoint de borrado de usuarios a partir del HTML del panel. 2.

Se hace una segunda petición SSRF apuntando a esa URL:

<!-- -->

stockApi=http://localhost/admin/delete?username=carlos

El servidor ejecuta la petición de borrado como si viniera del propio sistema, con todos los privilegios que eso implica.

> [!important] > **Idea clave:** los paneles de administración que solo escuchan en `localhost` asumen que `localhost` es confiable.

SSRF rompe esa asunción porque el atacante puede hacer que el servidor hable consigo mismo.

# Caso 2 --- SSRF contra infraestructura interna

Aquí la aplicación hace peticiones a un servidor interno en la red `192.168.0.0/24`.

El atacante no conoce qué IP exacta ni qué puerto expone el servicio administrativo, así que usa el **Intruder de Burp** para hacer un escaneo de hosts y puertos dentro de la red interna.

## 1.

Se itera sobre las IPs del rango `192.168.0.1` a `192.168.0.255`, buscando respuestas con código distinto de 404.

La respuesta diferente delata el host activo. 2.

Una vez identificada la IP, se itera sobre los puertos comunes (en el laboratorio se acota al rango `8000`--`9000`) buscando la misma diferencia de respuesta.

El panel administrativo encontrado responde sin autenticación porque asume que nadie puede llegar a él desde el exterior.

SSRF lo convierte en accesible.

> [!important] > **Idea clave:** los servicios internos sin autenticación son el objetivo más valioso de SSRF.

Asumen que la red interna es confiable, y SSRF convierte al servidor público en un pivote hacia esa red.

**Nota sobre sigilo:** escanear todo un rango de IPs de golpe hace mucho ruido.

Para ser sigiloso conviene bajar el ritmo (thread pool) y trocear el escaneo en el tiempo: hoy del 1 al 50, mañana del 50 al 100, etc.

Se tarda más, pero se es mucho menos detectable.

# Caso 3 --- SSRF contra metadatos de AWS

En entornos cloud, las instancias EC2 de AWS exponen un endpoint de metadatos en la dirección `169.254.169.254`.

Es una dirección **link-local** (no enrutable fuera de la instancia) que devuelve información sobre la instancia **sin ningún tipo de autenticación**: nombre, región, rol de IAM asignado y, lo más crítico, las **credenciales temporales del rol**.

Al apuntar el parámetro vulnerable a esa dirección, se navega el árbol de metadatos de forma incremental:

stockApi=http://169.254.169.254/latest/meta-data/

El response devuelve el índice de categorías disponibles.

Se profundiza hasta:

http://169.254.169.254/latest/meta-data/iam/security-credentials/

Que devuelve el nombre del rol asignado a la instancia.

Una última petición a:

http://169.254.169.254/latest/meta-data/iam/security-credentials/nombre-del-rol

Devuelve las credenciales temporales: **AccessKeyId, SecretAccessKey y Token**.

Con estas tres credenciales se puede autenticar contra cualquier servicio de AWS con los permisos que tenga el rol de la instancia.

> [!important] > **Idea clave:** el endpoint de metadatos de AWS es el objetivo más crítico de SSRF en entornos cloud.

Las credenciales IAM obtenidas pueden dar acceso a S3, RDS, Lambda o cualquier otro servicio permitido al rol.

En auditorías de aplicaciones cloud, SSRF siempre debe apuntar a este endpoint.

# Bypasses de filtros SSRF

Bypasses más comunes cuando el servidor intenta bloquear peticiones a direcciones prohibidas:

- **Bloqueo de** `127.0.0.1` **literal:** usar representaciones alternativas de la misma IP:

 - Decimal: `2130706433`
 - Abreviada: `127.1`
 - Octal: `0177.0.0.1`

Algunos parsers no las reconocen como equivalentes a `localhost`.

- **Bloqueo de la palabra** `localhost`**:** usar `127.0.0.1` directamente, o viceversa.

- **Bloqueo del dominio directamente:** usar un dominio propio que resuelva a la IP bloqueada.

Si el atacante controla un DNS, puede registrar un dominio que apunte a `127.0.0.1` y el servidor lo resolverá sin saber que es `localhost`.

- **Encadenar con Open Redirect:** si la aplicación tiene una redirección abierta, el parámetro vulnerable apunta a esa redirección, que a su vez redirige al destino interno.

Si el servidor sigue redirecciones automáticamente, llega al destino interno sin que el filtro de SSRF lo detecte.

# SSRF ciego (Blind SSRF)

El SSRF ciego ocurre cuando el servidor hace la petición pero el resultado **no aparece en el response** de la aplicación.

La petición se ejecuta en el backend, pero la respuesta queda en el servidor y el atacante no la ve directamente.

Para detectarlo se usa **Burp Collaborator**: un servidor externo controlado por el atacante que registra cualquier petición que reciba.

Al apuntar el parámetro vulnerable a la URL del Collaborator, si el servidor hace la petición, el Collaborator la registra aunque el atacante no vea nada en el response.

Esto confirma que hay SSRF aunque sea ciego.

La explotación del SSRF ciego es más compleja y se verá en sesiones avanzadas: requiere encadenar con otras vulnerabilidades o usar técnicas **out-of-band** para exfiltrar datos.

# Recapitulación integrada

SSRF completa el cuadro de vulnerabilidades que convierten al servidor en aliado del atacante:

- **Path traversal:** el servidor lee ficheros locales por cuenta del atacante.
- **XXE:** el servidor parsea XML externo con consecuencias locales.
- **SSRF:** el servidor hace peticiones de red que el atacante no puede hacer directamente.

Los tres vectores comparten la misma raíz: **una función del servidor acepta entrada de usuario sin validar y la usa para acceder a un recurso.**

La semana que viene se entra en **SQL Injection**, siguiendo la misma estructura progresiva: desde los casos más simples hasta blind SQLi y técnicas out-of-band.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF — Server-Side Request Forgery]] — Burp Suite, Open Redirect, Redes
- [[resumen_master_clase53.md|resumen_master_clase53]] — IA en Ciberseguridad, Open Redirect, Redes
- [[resumen_master_clase49.md|resumen_master_clase49]] — IA en Ciberseguridad, Redes, SQL Injection
- [[../../Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal — 6 Casos y Bypasses]] — Burp Suite, Redes, XXE
- [[../../apuntes Chema/PortSwigger — SSRF y cierre SSTI.md|PortSwigger — SSRF y cierre SSTI]] — IA en Ciberseguridad, Open Redirect, Redes
- [[../../Apuntes/comandos/BurpSuite.md|BurpSuite]] — Burp Suite, Redes, SQL Injection

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/SSTI — Server-Side Template Injection.md|SSTI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #ia #lfi #open-redirect #redes #sqli #ssrf #ssti #xxe
