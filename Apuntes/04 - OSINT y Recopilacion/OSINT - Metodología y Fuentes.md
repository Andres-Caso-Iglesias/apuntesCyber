

> [!info] Relacionado con
> [[Esteganografía y Metadatos]] · [[Nmap - Escaneo y Enumeración]] · [[apuntes Chema/Enumeración Web]] · [[Redes - Direccionamiento IP y DNS]]
> 

---

## ① ¿Qué es OSINT?

**OSINT** (Open Source Intelligence) = recopilación de información **desde fuentes públicas** sin credenciales ni exploits. Primer paso de cualquier auditoría.

| Estado | Descripción |
|--------|------------|
| ✓ Legal | WHOIS, DNS, LinkedIn, Shodan sobre IPs públicas con contrato |
| ⚠️ Zona gris | Bases de datos filtradas para auditoría interna |
| ✗ Ilegal | Escanear sin autorización, usar credenciales filtradas |

> [!warning] LEGALIDAD
> El OSINT en sí mismo es legal. El límite está en **cómo se usa**. La autorización explícita del cliente es la clave.

---

## ② Metodología "” El ciclo de inteligencia

```
1. Definir objetivo → 2. Recolección → 3. Procesamiento → 4. Análisis → 5. Informe
```

> [!important] PRIMER PASO
> Antes de abrir cualquier herramienta: define **exactamente** qué necesitas. ¿Empleados? ¿Infraestructura? ¿Credenciales filtradas? Objetivo concreto = menos ruido.

---

## ③ [[Google_Dorks]]

```bash
site:empresa.com # solo resultados de ese dominio
site:empresa.com filetype:pdf # PDFs
site:empresa.com inurl:admin # URLs con 'admin'
site:empresa.com intitle:login # páginas con 'login'
intext:'contraseña' site:emp.com # texto específico

# Dorks útiles en auditorías
site:empresa.com filetype:xlsx # Excel expuestos
site:empresa.com filetype:sql # dumps de BD
inurl:/wp-content/uploads site:emp # uploads WordPress
site:github.com empresa.com # código en GitHub
site:*.empresa.com # subdominios
```

> [!tip] EXPOSICIÓN
> Muchas empresas tienen documentos internos, backups o paneles de admin indexados en Google por error. Los [[Google_Dorks]] los encuentran en segundos.

**Recurso:** `exploit-db.com/google-hacking-database` (GHDB)

---

## ④ Sherlock y Maigret "” Búsqueda por username

```bash
# Sherlock: busca un username en cientos de redes sociales
pip install sherlock-project
sherlock usuario_objetivo
sherlock usuario_objetivo --output resultados.txt

# Maigret: más completo, genera informe HTML
pip install maigret
maigret usuario_objetivo --report html
```

> [!warning] FALSOS POSITIVOS
> Solo verifican el código HTTP (200 vs 404). Algunas webs devuelven 200 aunque el usuario no exista → **verificar manualmente**.

---

## ⑤ WHOIS y DNS

```bash
# WHOIS "” información de registro
whois empresa.com
# Registrant, correos, teléfonos, fechas

# DNS "” enumeración de subdominios
dig empresa.com ANY # todos los registros
dig empresa.com MX # servidores de correo
dig empresa.com NS # servidores de nombre

# Transferencia de zona (si está mal configurada)
dig axfr empresa.com @ns1.empresa.com
# Si funciona: ORO. Revela todos los subdominios.

# Herramientas de subdominios
subfinder -d empresa.com
amass enum -d empresa.com
dnsrecon -d empresa.com

# Certificate Transparency (sin herramientas)
curl -s 'https://crt.sh/?q=%.empresa.com&output=json' | jq '.[].name_value'
```

---

## ⑥ Shodan "” El buscador de dispositivos

```bash
# Búsquedas en Shodan web
org:'Nombre Empresa' # todos los activos
net:185.12.34.0/24 # rango de IPs
port:22 org:'empresa' # SSH expuesto
vuln:CVE-2021-44228 # Log4Shell expuesto

# CLI
export SHODAN_API_KEY='tu_api_key'
shodan init $SHODAN_API_KEY
shodan search 'org:empresa port:22'
shodan host 1.2.3.4
```

> [!tip] SHODAN
> No solo encuentra cámaras y routers: también servidores con versiones vulnerables, bases de datos abiertas y paneles sin autenticación.

---

## ⑦ HIBP "” Bases de datos filtradas

```bash
# Have I Been Pwned "” consultar si un email tiene credenciales filtradas
curl 'https://haveibeenpwned.com/api/v3/breachedaccount/correo@empresa.com'

# Alternativas
# dehashed.com (suscripción)
# intelx.io
# hunter.io → correos corporativos por dominio
```

> [!warning] LEGALIDAD
> Consultar HIBP = **LEGAL** (datos ya públicos).
> Descargar bases de datos robadas = **ILEGAL**.
> Usar credenciales filtradas = **DELITO PENAL**.

---

## ⑧ LinkedIn y OSINT de personas

```
LinkedIn como fuente:
- Empleados → tecnologías usadas
- Organigramas → estructura
- Ofertas de trabajo → herramientas internas
- Formato de email: nombre.apellido@empresa.com
```

### Construcción de perfil

1. Nombre completo → variaciones
2. Username en redes → Sherlock/Maigret
3. Correos → hunter.io, HIBP
4. Foto → búsqueda inversa (Google Lens, PimEyes)
5. Teléfono → truecaller, eyecon
6. Documentos online → [[Google_Dorks]]

> [!warning] SPEAR PHISHING
> Toda esta información se usa para construir **ataques de phishing altamente personalizados**. Un email que menciona tu jefe, tu cargo y tu proyecto tiene altísima tasa de éxito.

---

## Checklist de repaso

- [ ] ¿Sé definir el objetivo antes de empezar?
- [ ] ¿Domino los [[Google_Dorks]] más comunes?
- [ ] ¿Sé usar Sherlock/Maigret para buscar usernames?
- [ ] ¿Entiendo la diferencia entre WHOIS y DNS?
- [ ] ¿Conozco Shodan y sus filtros principales?
- [ ] ¿Distingo qué es legal y qué no en OSINT?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/OSINT - Mapeando la Superficie de una Organización.md|OSINT - Mapeando la Superficie de una Organización]— Empleabilidad, Metodología Pentest, OSINT
- [[../../apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red.md|Redes-Tipologías, Datagramas y Paquetes de Red]— Empleabilidad, Esteganografía, OSINT
- [[../01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]— Metodología Pentest, Nmap, OSINT
- [[../03 - Herramientas de Analisis/Nmap - Escaneo y Enumeración.md|Nmap - Escaneo y Enumeración]— Metodología Pentest, Nmap, OSINT
- [[Esteganografía y Metadatos.md|Esteganografía y Metadatos]— Esteganografía, Metodología Pentest, OSINT
- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]— Metodología Pentest, Nmap, OSINT

### 🛠️ Herramientas

- [[comandos/Nmap|Nmap]]

> #empleabilidad #esteganografia #nmap #osint #pentest
