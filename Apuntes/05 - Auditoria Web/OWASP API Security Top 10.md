# OWASP API Security Top 10

> **Diferencia clave con el OWASP Top 10 web:** El API Top 10 se enfoca en **objetos** (usuarios, mascotas, documentos) y **funciones** (endpoints), no en páginas web. Las APIs son como cajones: cada endpoint es un cajón que puedes abrir, modificar o borrar.

---

## 1. Qué es una API

Una **API** (Application Programming Interface) es la interfaz que expone funciones y datos del backend. El cliente (navegador, app, script) envía peticiones HTTP a endpoints concretos; el servidor procesa y devuelve una respuesta.

**Flujo:** Cliente → request HTTP → endpoint/API → lógica del backend → respuesta → cliente

### Estructura de una petición HTTP

```
GET /api/v1/catalogo/abrigos HTTP/1.1
Host: https://ejemplo.tld
Authorization: Bearer <token>
Content-Type: application/json
```

| Elemento | Qué representa |
|----------|---------------|
| Método | Acción solicitada (GET, POST, PUT, PATCH, DELETE, OPTIONS) |
| Endpoint | Ruta concreta de la función o recurso |
| Host | Servidor al que va dirigida |
| Cabeceras | Metadatos: Authorization, API keys, Content-Type |
| Parámetros / cuerpo | Datos que el endpoint necesita |
| Código de respuesta | Resultado HTTP: 200, 404, 429, etc. |

---

## 2. Métodos HTTP

| Método | Función | Uso en auditoría |
|--------|---------|-----------------|
| **GET** | Leer/obtener un recurso | Enumerar objetos, comprobar si cambia la respuesta al modificar un ID |
| **POST** | Crear un recurso o disparar una acción | Crear recurso, login, acciones que escriben datos |
| **PUT** | Reemplazar un recurso completo | Modificar propiedades cuando el endpoint lo acepta |
| **PATCH** | Modificar parcialmente un recurso | Cambiar campos concretos (ej: cambio de rol) |
| **DELETE** | Eliminar un recurso | Borrar cuando la autorización lo permite |
| **OPTIONS** | Consultar métodos disponibles | Enumerar métodos habilitados antes de probar acciones |

> **PUT vs PATCH:** PUT reemplaza todo el recurso. PATCH modifica solo algunos campos. `PATCH role admin` → escalada de privilegios si no está protegido.

---

## 3. Autenticación vs Autorización

| Concepto | Pregunta | Ejemplo |
|----------|----------|---------|
| **Autenticación** | ¿Quién eres? | Validar usuario/contraseña, token u otra credencial |
| **Autorización** | ¿Qué puedes hacer? | Determinar si ese usuario puede leer, modificar o ejecutar una función concreta |

Primero debe resolverse la identidad; después se decide qué permisos tiene. **No confundir:** estar autenticado no implica estar autorizado para cualquier endpoint.

---

## 4. OWASP API Security Top 10 (2019/2023)

| ID | Riesgo | Descripción | Relación con auditoría |
|----|--------|-------------|----------------------|
| **API1** | Broken Object Level Authorization (BOLA) | IDOR: cambiar/iterar un identificador y acceder a objetos ajenos | `GET /api/pets/1` → `GET /api/pets/2` (objeto ajeno) |
| **API2** | Broken User Authentication | Fallos en login, tokens o recuperación de identidad | Login débil, tokens predecibles |
| **API3** | Broken Object Property Level Authorization | Exposición excesiva de datos o asignación masiva de propiedades | La API devuelve más datos de los necesarios |
| **API4** | Unrestricted Resource Consumption | Ausencia de límites de uso o frecuencia | Falta de rate limiting |
| **API5** | Broken Function Level Authorization | Acceso a funciones administrativas sin permiso | Usuario normal alcanza endpoints de admin |
| **API6** | Unrestricted Access to Sensitive Business Flows | Acceso no restringido a flujos sensibles del negocio | Modificar campos que no deberías (Mass Assignment) |
| **API7** | Server Side Request Forgery (SSRF) | El servidor hace peticiones a destinos elegidos por el atacante | `?url=http://169.254.169.254/` |
| **API8** | Security Misconfiguration | Configuraciones inseguras por defecto | TLS/CORS/errores innecesarios |
| **API9** | Improper Inventory Management | Versiones/endpoints antiguos sin inventario | API v1 olvidada sin controles |
| **API10** | Unsafe Consumption of APIs | Consumo inseguro de APIs externas | Inyecciones a través de APIs de terceros |

> **Edición 2023:** API3:2023 "Broken Object Property Level Authorization" combina API3:2019 (Excessive Data Exposure) y API6:2019 (Mass Assignment).

### Edición 2019 vs 2023 (mapa de correspondencias)

| 2019 | 2023 |
|------|------|
| API3 Excessive Data Exposure + API6 Mass Assignment | → API3 Broken Object Property Level Authorization |
| API7 SSRF, API8 Injection, API9 Assets, API10 Logging | Reordenados / renombrados |

> [!info] HTTP no tiene "solo seis" métodos
> RFC 9110 define GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS y TRACE; PATCH está estandarizado aparte. Piensa en **"métodos relevantes para el endpoint"**, no en una lista cerrada.

---

## 5. Superficie de ataque en APIs

Cada endpoint y cada método habilitado:
- Parámetros de ruta y consulta, cuerpo JSON/XML y cabeceras
- Flujos de registro, login, recuperación y refresco de sesión
- Versiones antiguas o entornos de prueba que sigan expuestos
- Integraciones con terceros y webhooks
- Errores y respuestas que revelen más información de la necesaria

**No confíes en la visibilidad de la interfaz:** Un endpoint no queda protegido porque el usuario "no tenga botón" para llamarlo.

---

## 6. Metodología de auditoría de APIs

1. **Identificar** la aplicación y la documentación de API disponible
2. **Interceptar** tráfico real del cliente con Burp Suite/FoxyProxy
3. **Enviar** peticiones a Repeater para modificarlas de forma controlada
4. **Enumerar** endpoints y métodos; OPTIONS puede revelar qué verbos acepta
5. **Observar** identificadores, nombres de campos y estructuras JSON devueltas
6. **Iterar IDs** dentro del laboratorio autorizado para comprobar autorización a nivel de objeto
7. **Probar** cambios de método o de propiedades cuando exista evidencia de que el endpoint los acepta
8. **Comparar** respuestas: código de estado, longitud, cuerpo y campos devueltos
9. **No destruir** recursos innecesariamente: DELETE puede impedir seguir investigando

### Herramientas principales

| Herramienta | Objetivo | Fase |
|-------------|----------|------|
| Burp Suite | Interceptar y modificar tráfico HTTP | Análisis / Explotación |
| curl | Realizar peticiones HTTP desde terminal | Análisis |
| dirsearch / ffuf / feroxbuster | Enumerar rutas/endpoints | Recogida / Análisis |
| Burp Intruder | Iterar identificadores y comparar respuestas | Análisis |
| jwt_tool | Analizar tokens JWT | Análisis |

---

## 6.1. JWT (JSON Web Token) — Autenticación en APIs

**Estructura:** `header.payload.signature` (base64url separado por puntos).

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJyb2xlIjoiYWRtaW4ifQ.XXXXX
```

| Parte | Contenido |
|-------|-----------|
| **Header** | Algoritmo de firma |
| **Payload** | Datos del usuario (ID, rol, etc.) |
| **Signature** | Firma para verificar integridad |

> [!warning] JWT ≠ cifrado
> RFC 7519 permite JWT **firmados** (JWS) y/o **cifrados** (JWE). Un JWT firmado normal **se puede leer en base64url**; la confidencialidad depende de TLS. No asumas "JWT = contenido cifrado".

> [!important] Cambiar el rol en BD no reescribe el JWT
> Modificar `role` en la base de datos **no** hace que un JWT ya emitido adquiera nuevos claims. Para que apliquen los nuevos permisos hay que **reemitir/rotar el token**. Por eso en el laboratorio, DELETE seguía dando Forbidden con el token normal aunque el rol en BD ya era `admin`.

---

## 7. Laboratorio práctico: BOLA/IDOR y Mass Assignment

### Ejemplo: IDOR/BOLA en endpoint de mascotas

```
GET /api/pets/1 → mascota del usuario
GET /api/pets/2 → mascota de OTRO usuario (vulnerabilidad)
GET /api/pets/3 → mascota de OTRO usuario
```

**Vulnerabilidad:** El backend devolvía objetos ajenos al usuario al recibir un identificador válido. El cambio de ID permitía acceder a un objeto que el usuario no está autorizado a consultar.

### Caso real: IDOR en la FIA (datos de Verstappen)

Los datos de Max Verstappen fueron filtrados desde la página de la FIA usando IDOR: registro como usuario normal → GET al endpoint de usuarios → el campo `role` era `user` → PUT para cambiarlo a `admin`.

### Ejemplo: Mass Assignment en endpoint de usuarios

```
PUT /api/users/1
{
  "role": "admin"
}

PUT /api/users/1
{
  "vip": 1
}
```

**Vulnerabilidad:** El backend aceptó cambios en propiedades sensibles como `role` y `vip`. Un usuario normal puede modificar su propio rol a administrador.

### Autorización distinta por método

```
DELETE /api/pets/{id} → Forbidden con token normal
DELETE /api/pets/{id} → Aceptado con token de administrador
```

> **Lección:** La autorización debe evaluarse por endpoint y por método. No basta con que "/api/pets" tenga una política general si GET y DELETE terminan aplicando controles diferentes.

### Walkthrough del laboratorio HappyPets (PortSwinger)

```
1. POST /api/login  → JWT + user_id + role (información revelada en la respuesta)
2. OPTIONS /api/pets → Allow: GET, POST, PUT, DELETE, OPTIONS  [flag: Options Explorer]
3. POST /api/pets   → crear mascota (id asignado)
4. GET /api/pets/5  → mascota de OTRO usuario (owner: admin) → IDOR confirmado
5. GET /api/users/0 → datos del admin (email, role) → Information Disclosure [flag: Data Exposed]
6. PUT /api/users/1 { "role": "admin" }  → escalada de privilegios
7. DELETE /api/pets/4 → 200 OK (solo accesible con rol admin)
8. PUT /api/users/1 { "role": "vip" }   → doble escalada
```

| Vulnerabilidad | Categoría | Señal |
|----------------|-----------|-------|
| IDOR en mascotas | API1 | `GET /api/pets/5` sin ser propietario |
| Info expuesta | API3 | `GET /api/users/0` devuelve datos del admin |
| Escalada de rol | API5/6 | `PUT` con `role: admin` aceptado |
| DELETE por método | API1/5 | Forbidden con token normal, OK con admin |
| Mass Assignment | API6 | `role` y `vip` editables desde el cliente |

### Enumeración de usuarios con Burp Intruder

```
GET /api/users/1  → 200 OK
GET /api/users/2  → 200 OK
GET /api/users/4  → 404 Not Found
```

Comparando **longitud de respuesta** en Intruder, sabes cuántos usuarios existen sin iterar a mano.

---

## 8. Errores comunes

- Confiar en que el frontend oculta una funcionalidad y asumir que el endpoint no existe
- Proteger GET/POST pero olvidar PUT, PATCH, DELETE u OPTIONS
- Usar un identificador como si fuese autorización: "si conoce el ID, puede verlo"
- Permitir que el cliente modifique propiedades sensibles como role, vip, owner o permisos
- Asumir que un JWT está cifrado por el simple hecho de ser JWT
- Usar DELETE sin necesidad y destruir evidencia/recursos útiles dentro del laboratorio

---

## 9. Buenas prácticas

- Autorización en backend por objeto, función, método y propiedad
- Allowlists de campos editables; no vincular automáticamente todo el JSON a un modelo sensible
- Rotar/reemitir tokens cuando cambian roles o permisos
- Limitar métodos habilitados a los necesarios y revisar la respuesta de OPTIONS
- Comparar respuesta, status code, longitud y contenido en cada prueba
- Inventariar dependencias, mantenerlas actualizadas y vigilar vulnerabilidades conocidas

---

## 10. Checklist de repaso

- [ ] ¿Explico la diferencia entre autenticación y autorización?
- [ ] ¿Enumero los métodos HTTP relevantes y sé usar OPTIONS para descubrir verbos?
- [ ] ¿Sé que un JWT se puede leer si solo está firmado (no cifrado)?
- [ ] ¿Entiendo por qué cambiar el rol en BD no actualiza un JWT ya emitido?
- [ ] ¿Detecto IDOR/BOLA iterando IDs y comparando respuestas?
- [ ] ¿Distingo Mass Assignment de una modificación legítima de perfil?
- [ ] ¿Evalúo la autorización por endpoint Y por método (GET vs DELETE)?
- [ ] ¿Resuelvo el flujo HappyPets: login → OPTIONS → IDOR → escalada → DELETE?
- [ ] ¿Mapeo hallazgos a la edición 2019 y 2023 del API Top 10?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/OWASP API Top 10 Labs.md|OWASP API Top 10 Labs]] — IDOR, JWT, Burp Suite, HappyPets
- [[../../apuntes Andres/04.09.2026 OWASP API Top 10 Labs.md|04.09.2026 OWASP API Top 10 Labs]] — IDOR, Escalada, PortSwinger
- [[../../apuntes Andres/03.09.2026 OWASP API Top 10 La API habla de más.md|03.09.2026 OWASP API Top 10 La API habla de más]] — JWT, IDOR, OPTIONS
- [[XSS - Cross-Site Scripting.md|XSS - Cross-Site Scripting]] — Metodologia Pentest, SQL Injection, XSS
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — SQL Injection, XSS, XXE
- [[../../apuntes Chema/OWASP API Top 10.md|OWASP API Top 10]] — DirSearch, Redes, XSS
- [[../../apuntes Chema/OWASP Top 10, CVSS, CWE y CVE.md|OWASP Top 10, CVSS, CWE y CVE]] — SQL Injection, XSS, XXE

### 🌐 Cross-Dominio

- [[../../../programacion/Ruby/seguridad_ruby.md|seguridad_ruby]] — Programacion: Desarrollo Web, SQL, Seguridad
- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, SQL, Seguridad

> #burpsuite #cli #crypto #dirsearch #escalada_privilegios #feroxbuster #ffuf #idor #jwt #pentest #redes #seguridad #sql #sqli #ssrf #web #xss #xxe #bola #mass-assignment #happypets
