> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 52**
> **Módulo:** MODULO3
> **Tema:** Clase 52
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 52. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Castillo** (Carlos Castillo).

Es la última sesión de repaso antes de las vacaciones de agosto --- quedan únicamente lunes, martes y miércoles de la semana siguiente.

**Anuncios importantes:** - **Clase hasta el miércoles** (lunes 18:00, martes 18:00, miércoles 16:00).

Después, agosto entero sin clase. - **Práctica 1 (Carlos):** se publicará en la plataforma con plazo de 1-2 meses para entregarla en agosto/septiembre. - **Septiembre:** vuelta con repaso de metodología web, cierre del módulo web, HTB, **módulo de Blue Team con Edu** (especialista en Bluetooth de Satek), y después **Directorio Activo**. - **Empleabilidad:** el equipo de Evolve (Raquel y Paula) pide CVs actualizados para buscar oportunidades a los alumnos. - **Consejo de búsqueda de trabajo:** escribir por LinkedIn directamente al responsable de RR.HH. de la empresa (sin esperar a una vacante publicada) es mucho más efectivo que enviar el CV por un formulario, donde compites con 30+ candidatos filtrados por certificaciones.

**Estructura de la clase:** 1.

Repaso de SSRF (toda la teoría, los 4 tipos de bypass). 2.

Laboratorio en vivo con Chema: SSRF con bypass Open Redirect. 3.

Intención de comenzar STI (Server-Side Template Injection) si queda tiempo.

## 2.

SSRF --- Server-Side Request Forgery (Repaso completo)

**Nota de nomenclatura:** durante toda la sesión Castillo usa los términos "SCRF", "SRF" y "SSRF" de forma intercambiable.

El término correcto es **SSRF** (*Server-Side Request Forgery*).

### ¿Qué es SSRF?

SSRF (*Server-Side Request Forgery*) es una vulnerabilidad web que permite **forzar al servidor a hacer peticiones HTTP en nombre del atacante**, incluyendo peticiones a recursos de la **red interna** del servidor que normalmente no son accesibles desde Internet.

> [!important] **La idea clave:**

Atacante → [Internet] → Servidor web → [Red interna] → Servicios internos

El atacante no puede acceder directamente a los servicios internos (bases de datos, paneles de admin, APIs privadas).

Pero si puede controlar a qué URL hace peticiones el servidor, usa el servidor como **mensajero** o **cabeza de turco** para llegar a esos servicios.

**La analogía:** es como tener un recadero que puede entrar al almacén cerrado al público.

Tú no puedes entrar, pero si le das una nota al recadero diciéndole "ve al almacén y tráeme X", él sí puede ir.

El servidor es el recadero.

**Diferencia con otras vulnerabilidades:** - Path Traversal/LFI → leer ficheros del servidor. - SSRF → hacer peticiones a servicios de la red interna del servidor. - Son conceptos distintos aunque ambos "leen" cosas.

### ¿Cómo detectarlo?

La señal de alarma principal: **un parámetro de la petición HTTP contiene una URL** que el servidor va a procesar.

POST /product/stock stockApi=https%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck...

Cuando en el HTTP History de Burp se ve que el valor de un parámetro (en el body de un POST o en la URL de un GET) **es una URL** → candidato a SSRF.

**Donde buscarlo:** - Botones que comprueban datos en tiempo real (check stock, verificar disponibilidad, obtener precio). - Formularios que cargan contenido desde una URL externa. - Parámetros de "callback" o "redirect" en la URL. - El HTTP History de Burp al hacer click en botones --- muchas peticiones que no se ven en la URL del navegador son visibles aquí.

**Truco de decodificación:** si el valor del parámetro parece basura, aplicar URL decode (`Ctrl+Shift+U` en Burp) para verlo claramente.

## 3.

Los 4 tipos de bypass SSRF (laboratorios de PortSwigger)

### Tipo 1 --- Sin restricciones (el más simple)

El servidor acepta cualquier URL sin validación.

Simplemente cambiar el valor del parámetro a `http://localhost/` o `http://127.0.0.1/` da acceso al panel de administración interno:

stockApi=http://localhost/admin stockApi=http://127.0.0.1/admin

### Tipo 2 --- Buscar servicios en la red interna (scan de red)

No se sabe la IP del servicio interno.

Usar **Burp Intruder** para iterar sobre el rango de IPs de la red interna, como si fuera un Nmap pero a través del SSRF:

stockApi=http://192.168.0.§1§/admin

Intruder con payload numérico del 1 al 254 → el que devuelve un código diferente (200 en vez de 404/500) = servicio encontrado.

> [!important] **Limitación importante:** SSRF solo descubre servicios **HTTP**.

No detecta SSH, MySQL, FTP, etc. a menos que haya una web en esos puertos.

Para escanear puertos, hacer lo mismo con el rango de puertos:

stockApi=http://192.168.0.1:§8080§/

**Consejo de Castillo:** no iterar sobre los 65.535 puertos.

Usar Claude para generar un diccionario de los 1.000-3.000 puertos más probables para servicios web (80, 443, 8080, 8443, 8888, 3000, 5000, etc.), excluyendo los que típicamente no son web (22, 21, 23, 53, 445...).

### Tipo 3 --- Bypass de Blacklist

El servidor tiene una lista negra de valores prohibidos: `localhost`, `127.0.0.1`, `admin`, `::1`, etc.

**Técnicas de bypass:**

# Abreviar la IP (los ceros intermedios son opcionales)

127.0.0.1 → 127.1 192.168.0.1 → 192.168.1 # (el último .0 se puede omitir)

# Representaciones alternativas de localhost

http://2130706433/ # 127.0.0.1 en decimal http://017700000001/ # 127.0.0.1 en octal http://[::1]/ # IPv6 loopback

# URL encoding de caracteres en la palabra prohibida

admin → %61%64%6d%69%6e # URL encoding de 'admin' admin → a%64min # Solo un carácter encoded

# Double URL encoding

%61%64%6d%69%6e → %2561%2564%6d%69%6e

**Regla:** si bloquea `localhost` pero no `127.1`, úsalo.

Si bloquea `127.1`, prueba la representación decimal.

La blacklist solo bloquea exactamente lo que el desarrollador puso en ella.

### Tipo 4 --- Bypass de Whitelist

El más difícil.

El servidor solo acepta URLs que contengan un dominio específico (ej. solo URLs de `stock.weliketoshop.net`).

Cualquier otra URL se rechaza.

**Técnicas de bypass usando la estructura de la URL:**

https://usuario@dominio.malo.com # El @ hace que usuario sea el host visible https://stock.weliketoshop.net@127.0.0.1 # La whitelist ve "stock.weliketoshop.net" pero el server resuelve 127.0.0.1 https://127.0.0.1#stock.weliketoshop.net # El # hace que lo que sigue sea un fragmento (ignorado por el servidor) https://stock.weliketoshop.net.attacker.com # Subdominio del atacante que la whitelist confunde con el dominio legítimo

**La idea:** explotar cómo los diferentes parsers de URL interpretan los componentes de una URL (host, usuario, fragmento, subdominio).

El validador ve el dominio autorizado en la cadena, pero el servidor HTTP que hace la petición resuelve la IP del atacante.

### Tipo 5 --- Bypass con Open Redirect

Si la whitelist obliga a que la URL sea de la propia aplicación, pero la aplicación tiene una funcionalidad de **Open Redirect**, se puede combinar:

## 1.

La whitelist valida que la URL empiece por `https://mi-aplicacion.com/` → ✓ 2.

Pero `/mi-aplicacion.com/redirigir?url=http://127.0.0.1/admin` redirige al servidor hacia la IP interna. 3.

El servidor sigue la redirección sin volver a validar la URL destino.

**Por qué es poderoso:** la whitelist solo valida la URL inicial, no las URLs a las que esa URL redirige.

Una vez que el servidor sigue la redirección, va a donde el atacante quiere.

## 4.

Open Redirect --- Concepto y usos

Un **Open Redirect** ocurre cuando la aplicación acepta una URL controlada por el usuario como destino de una redirección, sin validar que sea un dominio seguro.

**Detección:** parámetros como `?next=`, `?redirect=`, `?url=`, `?return=`, `?goto=` que aparecen después de una acción (login, logout, compra).

**Usos ofensivos:**

**En phishing (Red Team):**

https://repsol.es/gasolineras/promociones?pais=https://repsol-falso.com

El link comienza con el dominio legítimo de Repsol → el usuario confía.

Pero al hacer clic, el servidor redirige a la página maliciosa.

**En bypass de SSRF con whitelist:**

stockApi=https://mi-aplicacion.com/redirigir?url=http://127.0.0.1/admin

**Por qué los Open Redirects son frecuentes:** Los desarrolladores implementan el redirect para funcionalidad legítima (volver a la página anterior después del login) pero olvidan validar que la URL destino sea del propio dominio.

## 5.

Laboratorio en vivo: SSRF + Open Redirect bypass

### Flujo completo (ejecutado por Chema en pantalla)

**Paso 1 --- Navegar y activar Burp:**

FoxyProxy activado → Intercept OFF → navegar por la tienda

**Paso 2 --- Identificar el vector:** Al hacer clic en el botón "Check Stock" de un producto, en el HTTP History de Burp aparece:

POST /product/stock Body: stockApi=https%3A%2F%2Fstock...

Decodificar: `Ctrl+Shift+U` → se ve claramente una URL.

**Paso 3 --- Send to Repeater (**`Ctrl+R`**):** Modificar el valor de `stockApi` directamente en el Repeater.

**Paso 4 --- Confirmación de SSRF:**

stockApi=http://localhost/ → respuesta diferente ✓ stockApi=http://127.0.0.1/admin → panel de administración

**Paso 5 --- Con bypass de Open Redirect (caso whitelist):** Encontrar primero en la aplicación una URL que haga redirect (inspeccionando el código fuente o probando parámetros comunes).

Luego:

stockApi=http://stock.weliketoshop.net/product/nextProduct?path=http://192.168.0.12/admin

El servidor valida `stock.weliketoshop.net` ✓, sigue la petición, el endpoint `/nextProduct` redirige al path, y el servidor acaba haciendo la petición a `192.168.0.12`.

## 6.

Metodología web repasada en esta sesión

### Lo que más importa en una web

El **código fuente** (`Ctrl+U`) solo merece atención para buscar comentarios con credenciales o rutas.

No hay que leerlo entero --- con experiencia, se va directamente a lo interesante.

**Lo que realmente importa:** los **botones con funcionalidad** que hacen llamadas al backend.

Un botón de "Check Stock", "Verificar disponibilidad" o "Calcular precio" implica que el servidor hace una petición a algún sitio.

Eso es superficie de ataque.

**La diferencia entre hacer una petición como usuario vs. como servidor:** - Usuario desde navegador → hace la petición tú mismo. - SSRF → el servidor hace la petición por ti. - El valor de SSRF: el servidor tiene acceso a la red interna; el usuario desde fuera de Internet, no.

### El razonamiento ante un SSRF

## 1.

Veo un parámetro con una URL → candidato a SSRF 2.

Intento lo más simple: localhost / 127.0.0.1 3.

Si hay blacklist → probar variantes (127.1, decimal, octal, encoding) 4.

Si hay whitelist → buscar Open Redirect en la aplicación 5.

Si hay whitelist sin Open Redirect → probar bypasses con @, #, subdominios

## 7.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------
 *SCRF / SRF / ese CRF / ese CRF* **SSRF** (*Server-Side Request Forgery*) -- el servidor hace peticiones en nombre del atacante
 *STI / ese TI* **SSTI** (*Server-Side Template Injection*) -- inyección en motores de plantillas del servidor; se menciona como próximo tema
 *Port Sweager / Port Swigger / por su guía* **PortSwigger** -- plataforma de laboratorios de hacking web y creadores de Burp Suite
 *burn / bour / burp* **Burp Suite** -- framework de auditoría web
 *repetiter / el de mandar peticiones / repiltar* **Repeater** -- módulo de Burp Suite para reenviar peticiones modificadas manualmente
 *control r / ctrl r* `Ctrl+R` -- atajo en Burp para enviar la petición seleccionada al Repeater
 *control shift u / desencodearlo* `Ctrl+Shift+U` -- atajo en Burp para decodificar URL encoding en el valor seleccionado
*Open redirect / el de redirect / redireccionamiento* **Open Redirect** -- vulnerabilidad que permite redirigir a cualquier URL sin validar el dominio destino
 *whitelist / la lista blanca / la de los buenos* **Whitelist** -- lista de valores permitidos; en SSRF, solo se aceptan URLs de dominios autorizados
*blacklist / la lista negra / la de bloquear* **Blacklist** -- lista de valores prohibidos; bypasseable con variantes de encoding o representaciones alternativas
 *Localhost / el 127.0.0.1 / el loopback* **localhost /** `127.0.0.1` -- apunta al propio servidor; primer payload a probar en SSRF
 *el 127.1 / recortar ceros* `127.1` -- forma abreviada de `127.0.0.1`; bypasea blacklists que bloquean el formato completo
 *decimal / IP en decimal* Representación decimal de `127.0.0.1` = `2130706433`; bypasea algunas validaciones
 *Net Discover pero con intruder* Usar **Burp Intruder** para iterar IPs/puertos en SSRF, de forma análoga a netdiscover o Nmap
 *check stock / el botón del stock* Funcionalidad de comprobar disponibilidad de producto; vector típico de SSRF en laboratorios de PortSwigger
 *stockApi / la API del stock* Parámetro POST que contiene la URL del servicio de stock; el vector SSRF del laboratorio
*el Hardcodeado de la URL / URL sin HTTP* Una URL puede estar parcialmente hardcodeada en el código --- si ves `/product/stock/check` como valor, puede ser la raíz de un SSRF
 *Edu / el de Satek / el del bluetooth* **Edu** -- experto en Bluetooth de la empresa Satek, que impartirá el módulo de BLE en septiembre
 *Claudia / Claude / la IA* **Claude** -- usado para generar el diccionario de puertos probables para el scan de SSRF

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*