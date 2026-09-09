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

## 7. Laboratorio práctico: BOLA/IDOR y Mass Assignment

### Ejemplo: IDOR/BOLA en endpoint de mascotas

```
GET /api/pets/1 → mascota del usuario
GET /api/pets/2 → mascota de OTRO usuario (vulnerabilidad)
GET /api/pets/3 → mascota de OTRO usuario
```

**Vulnerabilidad:** El backend devolvía objetos ajenos al usuario al recibir un identificador válido. El cambio de ID permitía acceder a un objeto que el usuario no está autorizado a consultar.

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

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[XSS — Cross-Site Scripting.md|XSS — Cross-Site Scripting]] — FFUF, Redes, SQL Injection
- [[../../apuntes Andres/03.09.2026 OWASP API Top 10 La API habla de más.md|03.09.2026 OWASP API Top 10 La API habla de más]] — IDOR, Redes, SQL Injection
- [[../../apuntes Chema/OWASP API Top 10.md|OWASP API Top 10]] — FFUF, Feroxbuster, IDOR
- [[../../apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]] — FFUF, Feroxbuster, SQL Injection
- [[../../apuntes evolve/BLOQUE 4.md|BLOQUE 4]] — Burp Suite, Redes, SQL Injection
- [[../08 - Metodologías/Metodologia - Aplicaciones Web.md|Metodologia - Aplicaciones Web]] — FFUF, Feroxbuster, IDOR

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #dirsearch #escalada-privilegios #feroxbuster #ffuf #idor #pentest #redes #sqli #ssrf #xss #xxe
