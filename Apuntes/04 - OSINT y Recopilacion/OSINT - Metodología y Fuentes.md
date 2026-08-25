

> [!info] Relacionado con
> [[EsteganografÃ­a y Metadatos]] Â· [[Nmap - Escaneo y EnumeraciÃ³n]] Â· [[apuntes Chema/EnumeraciÃ³n Web]] Â· [[Redes - Direccionamiento IP y DNS]]
> â†’

---

## â‘  Â¿QuÃ© es OSINT?

**OSINT** (Open Source Intelligence) = recopilaciÃ³n de informaciÃ³n **desde fuentes pÃºblicas** sin credenciales ni exploits. Primer paso de cualquier auditorÃ­a.

| Estado | DescripciÃ³n |
|--------|------------|
| âœ… Legal | WHOIS, DNS, LinkedIn, Shodan sobre IPs pÃºblicas con contrato |
| âš ï¸ Zona gris | Bases de datos filtradas para auditorÃ­a interna |
| âŒ Ilegal | Escanear sin autorizaciÃ³n, usar credenciales filtradas |

> [!warning] LEGALIDAD
> El OSINT en sÃ­ mismo es legal. El lÃ­mite estÃ¡ en **cÃ³mo se usa**. La autorizaciÃ³n explÃ­cita del cliente es la clave.

---

## â‘¡ MetodologÃ­a â€” El ciclo de inteligencia

```
1. Definir objetivo â†’ 2. RecolecciÃ³n â†’ 3. Procesamiento â†’ 4. AnÃ¡lisis â†’ 5. Informe
```

> [!important] PRIMER PASO
> Antes de abrir cualquier herramienta: define **exactamente** quÃ© necesitas. Â¿Empleados? Â¿Infraestructura? Â¿Credenciales filtradas? Objetivo concreto = menos ruido.

---

## â‘¢ [[Google_Dorks]]

```bash
site:empresa.com # solo resultados de ese dominio
site:empresa.com filetype:pdf # PDFs
site:empresa.com inurl:admin # URLs con 'admin'
site:empresa.com intitle:login # pÃ¡ginas con 'login'
intext:'contraseÃ±a' site:emp.com # texto especÃ­fico

# Dorks Ãºtiles en auditorÃ­as
site:empresa.com filetype:xlsx # Excel expuestos
site:empresa.com filetype:sql # dumps de BD
inurl:/wp-content/uploads site:emp # uploads WordPress
site:github.com empresa.com # cÃ³digo en GitHub
site:*.empresa.com # subdominios
```

> [!tip] EXPOSICIÃ“N
> Muchas empresas tienen documentos internos, backups o paneles de admin indexados en Google por error. Los [[Google_Dorks]] los encuentran en segundos.

**Recurso:** `exploit-db.com/google-hacking-database` (GHDB)

---

## â‘£ Sherlock y Maigret â€” BÃºsqueda por username

```bash
# Sherlock: busca un username en cientos de redes sociales
pip install sherlock-project
sherlock usuario_objetivo
sherlock usuario_objetivo --output resultados.txt

# Maigret: mÃ¡s completo, genera informe HTML
pip install maigret
maigret usuario_objetivo --report html
```

> [!warning] FALSOS POSITIVOS
> Solo verifican el cÃ³digo HTTP (200 vs 404). Algunas webs devuelven 200 aunque el usuario no exista â†’ **verificar manualmente**.

---

## â‘¤ WHOIS y DNS

```bash
# WHOIS â€” informaciÃ³n de registro
whois empresa.com
# Registrant, correos, telÃ©fonos, fechas

# DNS â€” enumeraciÃ³n de subdominios
dig empresa.com ANY # todos los registros
dig empresa.com MX # servidores de correo
dig empresa.com NS # servidores de nombre

# Transferencia de zona (si estÃ¡ mal configurada)
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

## â‘¥ Shodan â€” El buscador de dispositivos

```bash
# BÃºsquedas en Shodan web
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
> No solo encuentra cÃ¡maras y routers: tambiÃ©n servidores con versiones vulnerables, bases de datos abiertas y paneles sin autenticaciÃ³n.

---

## â‘¦ HIBP â€” Bases de datos filtradas

```bash
# Have I Been Pwned â€” consultar si un email tiene credenciales filtradas
curl 'https://haveibeenpwned.com/api/v3/breachedaccount/correo@empresa.com'

# Alternativas
# dehashed.com (suscripciÃ³n)
# intelx.io
# hunter.io â†’ correos corporativos por dominio
```

> [!warning] LEGALIDAD
> Consultar HIBP = **LEGAL** (datos ya pÃºblicos).
> Descargar bases de datos robadas = **ILEGAL**.
> Usar credenciales filtradas = **DELITO PENAL**.

---

## â‘§ LinkedIn y OSINT de personas

```
LinkedIn como fuente:
- Empleados â†’ tecnologÃ­as usadas
- Organigramas â†’ estructura
- Ofertas de trabajo â†’ herramientas internas
- Formato de email: nombre.apellido@empresa.com
```

### ConstrucciÃ³n de perfil

1. Nombre completo â†’ variaciones
2. Username en redes â†’ Sherlock/Maigret
3. Correos â†’ hunter.io, HIBP
4. Foto â†’ bÃºsqueda inversa (Google Lens, PimEyes)
5. TelÃ©fono â†’ truecaller, eyecon
6. Documentos online â†’ [[Google_Dorks]]

> [!warning] SPEAR PHISHING
> Toda esta informaciÃ³n se usa para construir **ataques de phishing altamente personalizados**. Un email que menciona tu jefe, tu cargo y tu proyecto tiene altÃ­sima tasa de Ã©xito.

---

## Checklist de repaso

- [ ] Â¿SÃ© definir el objetivo antes de empezar?
- [ ] Â¿Domino los [[Google_Dorks]] mÃ¡s comunes?
- [ ] Â¿SÃ© usar Sherlock/Maigret para buscar usernames?
- [ ] Â¿Entiendo la diferencia entre WHOIS y DNS?
- [ ] Â¿Conozco Shodan y sus filtros principales?
- [ ] Â¿Distingo quÃ© es legal y quÃ© no en OSINT?

â†’

â†’

â†’
