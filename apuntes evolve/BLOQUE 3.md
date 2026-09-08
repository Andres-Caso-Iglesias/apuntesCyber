> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 03 — Metodología y OSINT
> **Contenido:** Metodología de auditoría, fases del pentest, enumeración pasiva/activa, Deep y Dark Web, comandos de OSINT reales

> [!tip] Cómo leer estos apuntes
> Este bloque establece la metodología de trabajo de un pentester: las 5 fases de un pentest, técnicas de enumeración pasiva (Google Dorking, Shodan, Censys) y activa (Nmap), acceso responsable a Deep/Dark Web, y un flujo OSINT completo paso a paso.

---

## ① Las cinco fases de un pentest

| Fase | Descripción |
|------|-------------|
| **1. Enumeración** | Recopilar toda la información posible del objetivo. La fase más importante — cuanto mejor se haga, más rápidas y eficientes serán las siguientes. |
| **2. Explotación** | Usar las vulnerabilidades detectadas para obtener acceso. |
| **3. Escalada de privilegios** | Pasar de usuario básico a administrador/root. |
| **4. Post-explotación / Pivoting** | Analizar el impacto obtenido y moverse a otros sistemas usando el acceso ya logrado. |
| **5. Reporte** | Documentar todo lo realizado, incluso si no hay hallazgos. |

---

## ② Enumeración pasiva: Google Dorking

La enumeración pasiva investiga **sin interactuar directamente** con el objetivo. Google Dorking usa filtros de búsqueda para encontrar archivos, subdominios o información expuesta sin que la organización lo perciba:

```bash
site:empresa.com # limita la búsqueda a un dominio
filetype:pdf site:empresa.com # busca PDFs públicos de esa web
filetype:doc site:empresa.com # busca documentos Word públicos
inurl:login # encuentra URLs que contienen "login"
site:empresa.com filetype:xml|conf|env # ficheros de config expuestos
```

> [!example] Ejemplo real de clase
> Buscar `filetype:doc site:empresa.com` puede revelar documentos Word públicos con datos confidenciales que la empresa no sabe que están expuestos.

---

## ③ Enumeración pasiva: Shodan, Censys y credenciales filtradas

| Herramienta | Función |
|-------------|---------|
| **Shodan** | Motor de búsqueda de dispositivos conectados a Internet y sus vulnerabilidades conocidas, filtrables por país, organización y tecnología |
| **Censys** | Similar a Shodan, enfocado en certificados y configuraciones |
| **Have I Been Pwned** | Comprobar si un correo de la organización ya ha sido filtrado en una brecha de datos conocida |
| **DeHashed** | Comprobar si contraseñas de la organización están en brechas conocidas |

> [!important] Relevancia
> Esta información es crítica para evaluar el riesgo de **password spraying** antes incluso de tocar la red objetivo.

---

## ④ Enumeración activa: primer contacto con el objetivo

La enumeración activa ya interactúa con el sistema. El escaneo de puertos con **Nmap** es el punto de partida universal:

```bash
nmap -p- <IP> # escanea todos los puertos TCP (1-65535)
nmap -sV <IP> # detecta versiones y banners de servicios
nmap -sU <IP> # escaneo UDP (más lento, útil DNS/SNMP)
nmap -sS <IP> # escaneo SYN sigiloso (requiere privilegios)
nmap --open <IP> # muestra solo los puertos abiertos
nmap -Pn -sV -vvv -p- <IP> -oN salida.nmap # escaneo completo guardado
```

El fingerprinting web identifica tecnologías con extensiones de navegador como **Wappalyzer**, o desde terminal con `whatweb` / `wappalyzer -cli`. Esto revela frameworks, CDN, WAF y versiones que orientan toda la auditoría posterior.

---

## ⑤ Deep Web y Dark Web como herramientas de inteligencia

### Conceptos

| Capa | Descripción |
|------|-------------|
| **Web Superficial** | Lo indexado por buscadores habituales |
| **Deep Web** | Contenido legítimo no indexado (bases de datos privadas, foros, bibliotecas) |
| **Dark Web** | Porción accesible solo mediante Tor, donde convive investigación legítima con actividad ilegal |

### Pasos básicos de acceso responsable a la Deep Web

1. Descargar **Tor** desde su sitio oficial (nunca de fuentes de terceros).
2. Usar una **VPN** para una capa adicional de seguridad.
3. Navegar usando enlaces `.onion` específicos.

### Usos legítimos de un profesional

- Buscar credenciales o bases de datos filtradas de un cliente en **Breached Forums**, **Dehashed** o **Intelligence X**.
- Monitorear foros para detectar amenazas emergentes.

> [!warning] Reglas de uso ético
> - Monitorear sin participar en actividades ilegales.
> - No descargar nada sospechoso.
> - Mantener siempre el anonimato con VPN.

---

## ⑥ OSINT práctico paso a paso sobre un dominio

### Flujo completo

```
Semillas (nombre, dominio, alias, email, teléfono)
 → Perímetros (subdominios, ASN, rangos IP, certificados)
 → Personas (alias cruzados, huella laboral)
 → Artefactos (metadatos, repositorios, fugas)
 → Validación (cruzar siempre 2+ fuentes antes de afirmar nada)
```

### Paso 1: Contexto y huella tecnológica

- Visitar el sitio, leer el código fuente (`Ctrl + U`) buscando rutas internas, claves olvidadas o comentarios reveladores.
- Identificar CDN/WAF con Wappalyzer.

### Paso 2: Google Dorks (ver ②)

### Paso 3: Metadatos de archivos

Los documentos e imágenes contienen autor, fecha, software y a veces ubicación GPS:

```bash
exiftool foto.jpg | egrep 'GPS(Latitude|Longitude)|CreateDate'
pdfinfo documento.pdf # metadatos de PDF: autor, aplicación, fechas
```

### Paso 4: Subdominios y certificados

```bash
sublist3r -d empresa.com
subfinder -d empresa.com
curl -s 'https://crt.sh/?q=empresa.com&output=json' | head # certs TLS
```

### Paso 5: Patrones de correo y filtraciones

- Inferir el formato (inicial+apellido@empresa.com).
- Comprobar si aparece en bases de datos comprometidas.

> [!note] Regla ética constante en todo el OSINT
> Solo información pública, **redactar** cualquier dato personal sensible en los entregables, y **documentar** evidencias (fecha, hora, URL, hash) para trazabilidad.

---

## ⑦ Herramientas de organización del trabajo

| Herramienta | Tipo | Ideal para |
|-------------|------|-----------|
| **CherryTree** | Organización por nodos y subnodos | Chuletas rápidas de comandos, funciona en local |
| **Notion** | Todo terreno visual con sincronización en la nube | Proyectos grandes con documentación detallada |
| **Obsidian** | Máxima personalización en local con archivos Markdown | Mapa de grafos entre notas relacionadas |

> [!important] Habilidad clave
> El seguimiento de auditorías (bitácora detallada de cada acción) permite justificar decisiones ante un cliente y detectar errores rápidamente — y es una de las habilidades "blandas" más valoradas en las entrevistas de trabajo del sector.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/PREWORK/resumen_clase14.md|resumen_clase14]] — Metodología Pentest, Nmap, Post-Explotación
- [[../Apuntes/comandos/Google_Dorks.md|Google_Dorks]] — Google Dorks, OSINT, Redes
- [[BLOQUE 7.md|BLOQUE 7]] — Nmap, Pivoting / Movilidad Lateral, Post-Explotación
- [[../Apuntes/comandos/Metasploit.md|Metasploit]] — Escalada de Privilegios, Post-Explotación, Redes
- [[../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]] — Metodología Pentest, Nmap, OSINT
- [[../apuntes Joselu/PREWORK/resumen_clase4.md|resumen_clase4]] — Metodología Pentest, Nmap, OSINT

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Nmap|Nmap]]

> #escalada-privilegios #google-dorks #nmap #osint #pentest #pivoting #post-explotacion #redes
