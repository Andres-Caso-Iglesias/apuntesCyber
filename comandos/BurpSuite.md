# Burp Suite — Testing Web

> [!info] Herramienta
> Suite de testing de seguridad web. Proxy interceptivo, scanner de vulnerabilidades, fuzzing y más. La herramienta estándar para pentesting web.
## Configuración Inicial

> [!tip] Primer paso
> Configurar el proxy y el navegador para interceptar tráfico.

### Proxy en Navegador

```bash
# Puerto por defecto: 8080
# Configurar proxy en navegador: 127.0.0.1:8080
# Importar certificado CA de Burp para HTTPS
# http://burpsuite → "CA Certificate" → descargar e instalar
```

### Configuración de Proyecto

| Opción | Descripción |
|---|---|---| ## Proxy | > [!note] Interceptación de tráfico |
> El core de Burp Suite — interceptar, modificar y reenviar requests.

### Intercept | | Función | Descripción |

| Intercept on/off | Activar/desactivar interceptación |
| Forward | Enviar request modificado |
| Drop | Descartar request |
| Action | Enviar a otras herramientas |

```bash
# Flujo típico:
# 1. Activar Intercept
# 2. Navegar a la web
# 3. Burp captura el request
# 4. Modificar si es necesario
# 5. Forward para continuar
```

### HTTP History

| Filtro | Descripción |
|--------|-------------|
| Filter by MIME type | HTML, JS, CSS, images |
| Filter by status code | 200, 301, 403, etc. |
| Filter by search term | Buscar en requests/responses |
| Filter by host | Filtrar por dominio |

### Options del Proxy

| Opción | Descripción |
|---|---|---| ## Repeater | > [!important] Manipulación manual |
> Reenviar requests modificados para probar respuestas. Ideal para inyecciones y bypass.

### Uso | ```bash

# 1. Enviar request desde Proxy → Repeater (Ctrl+R)
# 2. Modificar el request
# 3. Click "Send"
# 4. Analizar respuesta
```

### Funciones

| Función | Descripción |
|---------|-------------|
| Send | Enviar request |
| Show response in browser | Renderizar respuesta |
| Follow redirect | Seguir redirecciones |
| Change request method | Cambiar POST↔GET |
| Change body encoding | URL-encoded, multipart, etc. |

### Tips

```bash
# Probar inyección SQL
' OR 1=1--
' UNION SELECT NULL--
' AND SLEEP(5)--

# Probar XSS
<script>alert(1)</script>
<img src=x onerror=alert(1)>

# Probar path traversal
../../../etc/passwd
....//....//....//etc/passwd
| ```
## Intruder

> [!warning] Fuzzing automatizado
> Ataques de fuerza bruta y fuzzing con configuración de payloads.

### Posiciones

| Tipo | Descripción |
|------|-------------|
| Sniper | Una posición a la vez |
| Battering Ram | Mismo payload en todas las posiciones |
| Pitchfork | Payloads paralelos |
| Cluster Bomb | Todas las combinaciones |

### Configuración

```bash
# 1. Marcar posiciones con §
# Ejemplo: §password§

# 2. Seleccionar tipo de ataque
# Sniper → una posición
# Cluster Bomb → múltiples posiciones

# 3. Configurar payloads
# List → wordlists
# Runtime file → archivo
# Numbers → rango numéricc
# Dates → fechas
```

### Resource Pool

| Opción | Descripción |
|--------|-------------|
| Concurrent requests | Requests simultáneos |
| Delay between requests | Delay entre requests |
| Throttle | Limitar requests |

### Resultados

| Filtro | Descripción |
|--------|-------------|
| Status code | Filtrar por código |
| Length | Filtrar por tamaño |
| Words | Filtrar por palabras |
| Errors | Mostrar errores |

```bash
# Ataque de credenciales
| # Username: admin | # Payload: wordlist de contraseñas | ``` |
|---|---|---| ## Spider (Crawler) | > [!note] Descubrimiento automático |
> Rastrear la web para encontrar URLs, formularios y contenido.

### Configuración | | Opción | Descripción |

| Maximum link depth | Profundidad máxima |
| Maximum crawl time | Tiempo máximo |
| Form submission | Auto-submit formularios |
| Application login | Autenticación |

### Uso

```bash
| # 1. Ir a Spider → Configuration | # 3. Click "Start Spider" | ``` |
|---|---|---| ## Scanner | > [!important] Detección automática |
> Scanner de vulnerabilidades (solo versión Pro).

### Tipos de Scan | | Scan | Descripción |

| Live active scan | Scan en tiempo real |
| Live passive scan | Solo lectura, no modifica |
| Scan defined insertion points | Puntos específicos |

### Resultados

| Columna | Descripción |
|---|---|---| ## Comparador | > [!tip] Análisis de diferencias |
> Comparar responses para encontrar cambios sutiles.

### Uso | ```bash

# 1. Enviar responses al Comparador (Ctrl+Shift)
# 2. Seleccionar modos de comparación
# 3. Analizar diferencias resaltadas
```

### Aplicaciones

```bash
# Detectar usuarios válidos
# Request 1: usuario existente
# Request 2: usuario ficticio
# Comparar responses → diferencias revelan información

| # Bypass de control de acceso | # Request 2: usuario admin | ``` |
|---|---|---| ## Decoder | > [!note] Decodificación |
> Decodificar/encodificar datos en múltiples formatos.

### Formatos | | Formato | Ejemplo |

| URL | %20 → espacio |
| HTML | &lt; → < |
| Base64 | YWRtaW4= → admin |
| Hex | 61646d696e → admin |
| Gzip | Compressed data |

### Uso

```bash
# Decodificar cookie
# Copiar cookie → Decoder → URL decode

# Decodificar base64
| # Copiar string → Decoder → Base64 decode | # Encode para bypass | ``` |
|---|---|---| ## Logger | > [!note] Historial completo |
> Registro de todas las peticiones HTTP/HTTPS.

### Filtros | | Filtro | Descripción |

|---|---|---| ## Extender | > [!tip] Extensiones |
> Instalar plugins para ampliar funcionalidades.

### Extensiones Comunes | | Extensión | Uso |

| Autorize | Testing de control de acceso |
| Active Scan++ | Escaneo activo mejorado |
| Param Miner | Descubrir parámetros ocultos |
| Turbo Intruder | Fuzzing ultrarrápido |
| Backslash Powered Scanner | Detección de WAF |
| Logger++ | Logger mejorado |

```bash
# Instalar extensión
# Extender → BApp Store → Buscar extensión → Install
```

---

## Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl+R` | Enviar a Repeater |
| `Ctrl+I` | Enviar a Intruder |
| `Ctrl+Shift+T` | Cambiar pestaña |
| `Ctrl+F` | Buscar |
| `Ctrl+L` | Ir a Logger |
| `Ctrl+Tab` | Siguiente pestaña |
| `Ctrl+Shift+Z` | Undo |
| `F6` | Toggle intercept |

---

## Workflows de Pentest Web

### Fase 1: Reconocimiento

```bash
# 1. Configurar proxy en navegador
# 2. Navegar por toda la aplicación
# 3. Dejar que Spider rastree
# 4. Revisar Site Map
```

### Fase 2: Enumeración

```bash
# 1. Revisar HTTP History
# 2. Buscar parámetros interesantes
# 3. Identificar puntos de inserción
# 4. Exportar endpoints a Repeater
```

### Fase 3: Explotación

```bash
# 1. Probar inyecciones en Repeater
# 2. Configurar Intruder para fuzzing
# 3. Usar Scanner para vulnerabilidades
# 4. Documentar hallazgos
```

### Fase 4: Bypass

```bash
# 1. Identificar WAF/defensas
# 2. Probar encoding en Decoder
# 3. Usar extensiones de bypass
# 4. Testear control de acceso con Autorize
```

---

## Proxy Alternativos

```bash
# Cuando Burp no es opción
mitmproxy -p 8080 # Terminal
zaproxy # OWASP ZAP
paros # Alternativa ligera
```

---

#checklist
- [ ] Proxy configurado en navegador
- [ ] Certificado CA instalado
- [ ] Site map revisado
- [ ] Parámetros identificados
- [ ] Inyecciones probadas en Repeater
- [ ] Fuzzing completado con Intruder
- [ ] Vulnerabilidades documentadas
- [ ] Control de acceso testeado


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[WPScan.md|WPScan]] — Hydra, WPScan, WordPress
- [[../Apuntes/05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]] — Hydra, WPScan, WordPress
- [[../Apuntes/comandos/WPScan.md|WPScan]] — Hydra, WPScan, WordPress
- [[../Apuntes/05 - Auditoria Web/WordPress - Auditoría con WPScan.md|WordPress - Auditoría con WPScan]] — Hydra, WPScan, WordPress
- [[../Apuntes/05 - Auditoria Web/Enumeración Web.md|Enumeración Web]] — Burp Suite, WPScan, WordPress
- [[../apuntes Joselu/MODULO3/resumen_master_clase37.md|resumen_master_clase37]] — Hydra, SSH, WPScan

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

> #burpsuite #ffuf #hydra #pentest #redes #ssh #wordpress #wpscan
