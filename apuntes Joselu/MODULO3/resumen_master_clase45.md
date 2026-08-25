> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 45**
> **Módulo:** MODULO3
> **Tema:** Clase 45
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 45. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
**Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y estructura de la sesión

Esta sesión la imparte **Carlos (Dani)**.

Es una clase especial: se adelantó 30 minutos y se terminó a las 8:30 para que los alumnos pudieran ver la Final del Mundial de Fútbol (España en la Eurocopa o Mundial, el profesor no es seguidor).

Solo asistieron 13 personas.

**Novedad técnica:** Carlos ha integrado **Claude directamente en la terminal de Kali** como asistente embebido.

### Instalación con:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

# + login con cuenta de Anthropic

**También ha configurado un portapapeles múltiple en Kali:** permite copiar múltiples elementos, hacer scroll entre ellos y pegar el que se quiera.

Útil para copiar hashes, payloads, IPs simultáneamente durante una auditoría.

**Contenido de la clase:** en vez de continuar con máquinas, Carlos crea una aplicación web PHP real en vivo (**CyberLab**) para explicar desde dentro cómo funciona una aplicación web y por qué las vulnerabilidades que se han visto son donde están.

## 2.

El concepto fundamental: una página web es una carpeta expuesta

Una página web = una carpeta en un servidor, expuesta a Internet a través de un puerto.

**Diagrama completo de arquitectura web:**

INTERNET
 |
[WAF] ← Web Application Firewall
 |
[Servidor Web - DMZ] ┌─────────────────────┐ │ FRONT (navegador) │ ← HTML, CSS, JS — lo que el usuario ve │ ↕ Puerto 80/443 │ │ BACK (servidor) │ ← PHP, Python, Java — el código del servidor └─────────────────────┘
 |
[Firewall + reglas]
 |
[Servidor de BD - Red interna] ┌─────────────────────┐ │ Base de datos │ ← MySQL, PostgreSQL, SQLite... │ Red diferente │ └─────────────────────┘

**Lo que es vulnerable:** NO el front, NO el servidor, NO el puerto, NO la base de datos, NO la raíz. **Solo los ficheros PHP** que programan las funcionalidades de la web.

Son los únicos que escriben los desarrolladores y los únicos que pueden contener vulnerabilidades.

## 3.

SQL Injection --- dónde está realmente la vulnerabilidad

**La confusión frecuente:** SQL Injection no es una vulnerabilidad de la base de datos ni del gestor (phpMyAdmin, Adminer, MariaDB, etc.).

Es una vulnerabilidad del **fichero PHP** que hace la consulta a la base de datos.

**La analogía del profesor:**

> "Si tú tienes 5.000€ en el banco y nadie te ha dicho cuánto puedes dar, te pido 10.000 y me los das, te pido 5.000 y me los das.

Cuando ya tienes guardarraíles --- límites programados --- ya no puedes.

El problema no está en tu cuenta del banco, sino en *ti* como gestor."

El servidor web puede estar perfectamente securizado con firewalls y WAF.

Pero si el fichero PHP que consulta la base de datos no valida correctamente el input del usuario, la base de datos se puede atacar **a través de ese fichero autorizado**.

El PHP tiene permisos para consultar la base de datos --- el atacante simplemente manipula las consultas que ese PHP lanza.

**SQL Injection aplica a todos los motores SQL:** MariaDB, MySQL, PostgreSQL, SQLite, Oracle.

MongoDB (NoSQL) tiene su propia variante (NoSQL Injection).

ElasticSearch también tiene inyecciones equivalentes --- cualquier sistema que use un lenguaje estructurado para consultas puede ser inyectado si el código que hace las llamadas no valida el input.

**La regla general:** si yo no limito lo que puede hacer el fichero PHP, el fichero hace lo que le pidas.

Si le meto una consulta maliciosa, la ejecuta.

## 4.

Estructura segura de una aplicación web --- el proyecto CyberLab

### Estructura de directorios del proyecto

/var/www/CyberLab/ ← directorio raíz del proyecto ├── public/ ← raíz de la URL (lo único expuesto en Internet) │ ├── index.php ← página principal (se carga con barra /) │ ├── login.php ← panel de login │ ├── registro.php ← registro de usuarios │ ├── perfil.php ← perfil del usuario │ ├── trabaja.php ← formulario de subida de CV │ ├── assets/ ← CSS, JS, imágenes (directorio) │ ├── uploads/ ← ficheros subidos por usuarios │ └── includes/ ← header, footer, funciones PHP │ ├── header.php │ ├── footer.php │ └── functions.php └── data/ ← datos internos (NO expuesto en Internet) └── cyberlab.db ← base de datos SQLite

### Por qué esta estructura es segura

**El servidor Apache está configurado para servir solo la carpeta** `/public/`**.**

Cuando alguien accede a `http://servidor/`, lo que ve es el contenido de `/public/`.

La carpeta `/data/` está en el mismo nivel que `/public/`, no dentro de ella.

**Para acceder a** `/data/` **desde la URL:**

http://servidor/../data/ → Necesita Path Traversal

El atacante necesita `../` (subir un directorio) para salir de `/public/` y llegar a `/data/`.

Sin Path Traversal, `/data/` es inaccesible desde la URL --- está protegida **por diseño**.

**La diferencia entre un problema de arquitectura y un problema de código:** - **Problema de arquitectura:** el arquitecto/sistemas pone la base de datos dentro de `/public/` → accesible directamente desde la URL → culpa del arquitecto. - **Problema de código:** el arquitecto lo montó bien (datos fuera de `/public/`), pero un desarrollador escribió un fichero PHP vulnerable a Path Traversal → culpa del desarrollador.

### El fichero index.php y Apache

<?php // Variables de configuración $active = 'home'; // Página activa por defecto $pageTitle = 'Inicio'; ?> <!DOCTYPE html> <html> <!-- HTML + CSS desde aquí -->

**Por qué no hay que poner la URL como** `localhost:8080/index.php`**:** Apache está configurado para servir automáticamente el fichero `index.php` (o `index.html`) cuando se accede a un directorio.

Por eso `localhost:8080/` carga `index.php` sin necesidad de especificarlo.

**Lo que ves al navegar a** `/login` **o** `/perfil`**:** No es una "pestaña nueva" de la misma página.

Es un PHP diferente (`login.php`, `perfil.php`).

Cada URL = un fichero PHP diferente.

La barra de estado del navegador lo revela: al pasar el ratón sobre los enlaces, aparece la ruta real del PHP.

## 5.

Qué ve un auditor en una aplicación web (la metodología en contexto)

Cuando Carlos navega por su propia aplicación CyberLab, señala exactamente lo que un auditor buscaría:

Lo que ve el auditor Lo que hay detrás Vector potencial
 ----------------------------------- ----------------------------------------------------- -------------------------------------
Formulario "Trabaja con nosotros" `trabaja.php` con subida de ficheros File Upload → RCE Carpeta `/uploads/` accesible Directorio donde se guardan los CVs Si se puede subir PHP → ejecución Formulario de login `login.php` que consulta la BD SQL Injection Barra de búsqueda PHP que hace `SELECT * WHERE nombre LIKE '%input%'` SQL Injection
 `/includes/` en el fuzzing Directorio con `functions.php`, `header.php` LFI para leer el código fuente
 `/data/` en el fuzzing Base de datos fuera de `/public/` Path Traversal necesario para llegar

**El fuzzing revela la estructura de directorios:** GoBuster, dirsearch, FFUF --- todos hacen lo mismo con el mismo diccionario.

La diferencia está en el diccionario por defecto, no en la herramienta.

## 6.

GoBuster / Dirsearch / FFUF --- todos hacen lo mismo

Carlos desmitifica de una vez por todas la diferencia entre estas herramientas:

> "¿Qué sabor de helado quieres?

Fresa, tarta de queso, turrón... son todos helados.

La base es la misma: hacer peticiones HTTP con un diccionario y ver el código de respuesta.

Si le pones el mismo diccionario a todas las herramientas, te dan el mismo resultado."

**La diferencia real:** el diccionario por defecto.

Cada herramienta incluye uno diferente.

Pero si les das el mismo diccionario (SecLists `directory-list-2.3-medium.txt`), producen resultados idénticos.

**Todas hacen lo mismo:**

# Equivalentes — mismo resultado con el mismo diccionario:

gobuster dir -u http://IP -w diccionario dirsearch -u http://IP ffuf -u http://IP/FUZZ -w diccionario dirb http://IP diccionario

**El 200 no siempre significa que existe:** si la aplicación tiene una página de error 404 personalizada que devuelve código HTTP 200, el fuzzer va a pensar que todas las rutas existen.

### Para filtrar:

```bash
curl URL | grep "404" # Buscar el texto del mensaje de error en la respuesta
```

# Si aparece el texto "404" en una respuesta con código 200 → falso positivo

## 7.

Lo que se intercepta con Burp y lo que no

**Una duda frecuente:** ¿se puede leer el código PHP de la aplicación interceptando la petición con Burp?

**Respuesta:** NO.

Nunca.

Cuando se hace una petición a `index.php`, el servidor ejecuta el PHP y devuelve **únicamente el resultado HTML** --- lo que el navegador renderiza.

El código PHP (el backend) nunca sale del servidor.

Lo que sí se puede interceptar con Burp: - El HTML renderizado (frontend). - Las cabeceras HTTP (servidor, versión, cookies...). - Los parámetros de las peticiones (formularios, tokens...). - El CSS y JavaScript (frontend).

Lo que NO se puede interceptar con Burp: - El código fuente PHP del backend. - Las credenciales de la base de datos en `functions.php`. - Los datos de la base de datos que no hayan sido enviados en la respuesta.

**Excepción:** si hay un LFI, se puede usar para leer el código PHP --- pero eso ya es explotar una vulnerabilidad, no interceptar tráfico normal.

## 8.

La defensa contra Path Traversal --- las dos capas

**Capa 1 --- Diseño (arquitectura):** separar los datos sensibles (base de datos, configuraciones) fuera de la carpeta pública.

Un atacante necesita Path Traversal para llegar a ellos.

**Capa 2 --- Código (validación del input):** en el fichero PHP, filtrar que el input no contenga `../`:

// Validación básica — rechazar si contiene '../' $input = $_GET['file']; if (strpos($input, '..') !== false || strpos($input, '/') !== false) { die('Acceso denegado'); }

// Mejor: usar basename() que elimina rutas y deja solo el nombre del fichero $input = basename($_GET['file']);

// Todavía mejor: whitelist explícita de ficheros permitidos $allowed = ['doc1.pdf', 'doc2.pdf']; if (!in_array($input, $allowed)) { die('Fichero no permitido'); }

**Capa 3 --- WAF:** filtrar peticiones que contengan `../`, `%2e%2e%2f` (URL encoding de `../`) o variantes de evasión.

**La analogía del obrero y el electricista:** \> "¿Está bien que un obrero sepa un mínimo de electricidad para no cometer errores graves?

Sí, se agradece.

Un desarrollador que sabe ciberseguridad básica evita crear vulnerabilidades en su código.

No necesita ser pentester, pero sí conocer los errores más comunes."

## 9.

Flujo de ataque completo visto desde dentro de la aplicación

Con el conocimiento de la estructura interna, el flujo de ataque de las máquinas vistas tiene ahora todo el sentido:

## 1.

Nmap → detecta puerto 80 (Apache) + 22 (SSH) ↓ 2.

Navegador → explorar la web, leer código fuente (Ctrl+U) → la barra de estado revela los ficheros PHP ↓ 3.

GoBuster/Dirsearch → enumerar directorios y ficheros → encuentra /uploads/, /includes/, datos.php ↓ 4.

Burp Repeater → probar cada endpoint encontrado → /upload.php devuelve "no proporcionado" → espera input → cabecera Accept incluye application/xml → acepta XML ↓ 5.

Payload XXE → leer /etc/passwd, /var/www/html/datos.php → datos.php contiene credenciales hardcodeadas ↓ 6.

Hydra → validar credenciales contra SSH ↓ 7.

SSH → shell de sistema → escalada de privilegios

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
--------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 *una página web es una carpeta expuesta* **Concepto fundamental**: una web = carpeta en servidor + servidor que la expone en un puerto
 *barra w w w / bar barra w w HTML* `/var/www/html/` -- directorio raíz por defecto de Apache en Linux
 *el fichero que hace la llamada a la base de datos* **Fichero PHP de conexión** -- el que es vulnerable a SQL Injection, no la BD en sí
 *PHP Miami / PHP Myat / el gestor visual* **phpMyAdmin** -- interfaz web para administrar bases de datos MySQL
*Maria DB / Mongol / SQLite* **MariaDB / MongoDB / SQLite** -- motores de bases de datos; SQL Injection aplica a los de SQL, NoSQL Injection a los demás
 *guardarraíles / guarriales / railing wards* **Guardarraíles** (*guardrails*) -- límites programados que impiden ciertos comportamientos
 *Pack Transversal / Pad transversal* **Path Traversal** -- vulnerabilidad que usa `../` para navegar fuera del directorio permitido
 *Transversal Paz / el Pack Traversal* **Path Traversal** -- mismo concepto
 *la carpeta data / la de la base* `/data/` -- carpeta que contiene la base de datos; correctamente situada fuera de `/public/`
*barra public / la carpeta pública / la raíz de la URL* `/public/` -- única carpeta expuesta en Internet; todo lo que hay dentro es accesible desde la URL
 *el CyberLab / la app que hizo Carlos* **CyberLab** -- aplicación PHP creada en vivo por Carlos para demostrar la arquitectura web
 *GoBaster / Dirt Search / FOOF* **GoBuster / dirsearch / FFUF** -- todas hacen lo mismo (fuzzing de directorios) con el mismo diccionario
 *el portapapeles múltiple / el de copiar varios* **Portapapeles múltiple** -- herramienta instalada en Kali para copiar/pegar múltiples elementos
*Claudia en la terminal / la IA embebida* **Claude integrado en la terminal de Kali** -- instalado con `curl -fsSL https://claude.ai/install.sh | bash`
*el WAF / el Web Application Fire* **WAF** (*Web Application Firewall*) -- capa de seguridad que filtra peticiones maliciosas entre el cliente y el servidor
 *el DNZ / la zona DMZ* **DMZ** (*DeMilitarized Zone*) -- segmento de red donde se alojan los servidores expuestos a Internet
 *el include de funciones / el de includes* `/includes/` -- directorio que contiene ficheros PHP reutilizables (header.php, footer.php, functions.php)
 *trabaja punto PHP / el formulario del CV* `trabaja.php` -- fichero PHP con formulario de subida de CVs; vector de File Upload
*el backend nunca sale / no se intercepta con bur* **El backend PHP no es interceptable con Burp** -- Burp solo ve el HTML renderizado que devuelve el servidor
*compilar / lo que hace el navegador* **Interpretar/ejecutar PHP** -- el servidor ejecuta el PHP antes de enviar el HTML al cliente; el código PHP nunca llega al navegador
*arquitecto vs desarrollador / quien tiene la culpa* Vulnerabilidades de diseño (datos en /public/) = responsabilidad del arquitecto/sistemas; vulnerabilidades de código (PHP sin validar) = responsabilidad del desarrollador

*Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*
