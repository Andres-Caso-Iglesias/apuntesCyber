

> [!info] Relacionado con
> [[Enumeración Web]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]]

---

## ① ¿Qué es el fuzzing?

Envío **automatizado** de entradas a una aplicación para descubrir comportamientos no documentados: rutas ocultas, parámetros, valores válidos.

> [!important] Fuzzing vs Enumeración
> La **enumeración** es la estrategia: QUÉ buscar.
> El **fuzzing** es la TÉCNICA activa que lo ejecuta a gran escala.

---

## ② El keyword FUZZ

```bash
[[FFUF]] -u http://OBJETIVO/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

| Dónde pones FUZZ | Qué descubres |
|-----------------|--------------|
| En la ruta (`/FUZZ`) | Directorios y ficheros |
| En Host (`FUZZ.x.com`) | Virtual hosts / subdominios |
| En query (`?FUZZ=valor`) | Nombres de parámetros |
| En valor (`?id=FUZZ`) | Valores válidos |
| En body POST (`user=FUZZ`) | Usuarios, credenciales |

---

## ③ Flujo de un fuzzing efectivo

```
1. Elegir punto FUZZ → 2. Elegir wordlist → 3. Lanzar baseline → 4. Filtrar respuestas → 5. Analizar hits
```

> [!warning] El paso crítico es el CUARTO
> Sin filtrado, la salida es interminable. La clave es **distinguir la respuesta anómala** del ruido.

---

## ④ Filtrado de respuestas

| Flag | Filtra/empareja por | Ejemplo |
|------|-------------------|---------|
| `-fc` | Código de estado | `-fc 404` oculta los 404 |
| `-fs` | Tamaño en bytes | `-fs 1234` oculta el tamaño baseline |
| `-fw` | Nº de palabras | `-fw 56` oculta 56 palabras |
| `-fl` | Nº de líneas | `-fl 10` oculta 10 líneas |
| `-mc` | Empareja por código | `-mc 200,301,302` solo muestra esos |

> [!warning] El problema del baseline
> Muchas apps devuelven 200 OK para CUALQUIER ruta. Solución: lanza una petición a una ruta inexistente, mira su tamaño y filtra por `-fs`.

---

## ⑤ Casos prácticos

### Directorios y ficheros

```bash
[[FFUF]] -u http://OBJETIVO/FUZZ \
 -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
 -mc 200,301,302,403

# Con extensiones según el stack
[[FFUF]] -u http://OBJETIVO/FUZZ \
 -w /usr/share/seclists/Discovery/Web-Content/common.txt \
 -e .php,.txt,.bak
```

### Virtual hosts

```bash
[[FFUF]] -u http://OBJETIVO \
 -H 'Host: FUZZ.OBJETIVO.com' \
 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
 -fs 0
```

> [!tip] HTB
> En HTB es muy habitual que una IP sirva varias webs según Host. Añade el vhost descubierto a `/etc/hosts`.

### Parámetros ocultos

```bash
[[FFUF]] -u 'http://OBJETIVO/page.php?FUZZ=1' \
 -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
 -fs 1234
```

### Login (fuerza bruta)

```bash
[[FFUF]] -u http://OBJETIVO/login -X POST \
 -d 'username=admin&password=FUZZ' \
 -H 'Content-Type: application/x-www-form-urlencoded' \
 -w /usr/share/seclists/Passwords/probable-v2-top1575.txt \
 -fc 200
```

> [!danger] SOLO EN LABORATORIOS
> La fuerza bruta de credenciales solo es legítima en entornos autorizados.

---

## ⑥ Fuzzing de parámetros: dos fases (nombre y valor)

No basta con probar valores de parámetros conocidos: a veces el parámetro **no aparece en la interfaz**. Se resuelve en dos fases consecutivas:

| Fase | Incógnita | Herramienta típica | Diccionario |
|------|-----------|-------------------|-------------|
| **1. Descubrir NOMBRE** | ¿Qué parámetro oculto procesa el backend? | x8 / x8_lite.py | Nombres de parámetro (`burp-parameter-names.txt`) |
| **2. Descubrir VALOR** | ¿Qué valor activa ese parámetro? | ffuf / valfuzz.py | Valores (contextuales, `rockyou.txt` si aplica) |

```
1. index.php responde pero no muestra nada útil (500)
 ↓
2. x8 → descubre el NOMBRE del parámetro: 'backdoor'
 ↓
3. ffuf → fuzzea el VALOR de 'backdoor' (500 → 200)
 ↓
4. La respuesta revela usuario y contraseña
 ↓
5. Acceso con esas credenciales
```

> [!important] No confundir una fase con otra
> **x8** consume nombres de parámetro (¿existe este campo?). **ffuf/valfuzz** usan un nombre fijo y prueban valores (¿este valor hace algo?). Son fases consecutivas, no alternativas.

> [!warning] Señal de éxito: cambio 500 → 200
> Si una petición devolvía 500 y con un valor concreto pasa a 200 (o cambia la longitud de respuesta), has encontrado el valor que el backend procesa.

### Verificación manual con curl

```bash
curl -X POST http://OBJETIVO/index.php --data "parametro=valor"
```

### Fases internas de x8

| Fase | Qué hace |
|------|----------|
| **LEARN** | Aprende la respuesta baseline (ruta inexistente o parámetro inexistente) |
| **BATCH** | Lanza muchos nombres de parámetro a la vez |
| **COMPARE** | Diferencia cada respuesta contra el baseline |
| **BISECT** | Búsqueda binaria para aislar el parámetro que cambia la respuesta |
| **CUSTOM** | Prueba pares típicos: `admin=true`, `debug=1`, `id=1` |
| **VERIFY** | Reconfirma uno a uno los hallazgos |

> [!warning] x8 con Docker puede fallar
> Si `docker build -t x8 .` falla, alternativas: compilar con Cargo (`cargo build --release`) o escribir un fuzzer propio en Python (pattern `LEARN → BATCH → COMPARE → VERIFY`).

---

## ⑧ Wordlists recomendadas

| Diccionario | Uso |
|------------|-----|
| `SecLists/Discovery/Web-Content/common.txt` | Fuzzing rápido |
| `raft-medium-directories.txt` | Fuzzing web completo |
| `burp-parameter-names.txt` | Parámetros |
| `rockyou.txt` | Contraseñas |

---

## Checklist de repaso

- [ ] ¿Sé colocar FUZZ en diferentes puntos de la petición?
- [ ] ¿Domino el filtrado (-fc, -fs, -fw, -fl, -mc)?
- [ ] ¿Sé establecer un baseline antes de fuzzear?
- [ ] ¿Puedo fuzzear directorios, vhosts y parámetros?
- [ ] ¿Sé cuándo usar [[FFUF]] y cuándo [[Hydra]] para credenciales?
- [ ] ¿Diferencio la fase de descubrir NOMBRE de parámetro de la de descubrir VALOR?
- [ ] ¿Reconozco la señal 500 → 200 como indicador de parámetro procesado?
- [ ] ¿Conozco las fases internas de x8 (LEARN, BATCH, COMPARE, VERIFY)?

---

## Enlaces relacionados

- [[comandos/FFUF]] — Cheat sheet de comandos
- [[comandos/Feroxbuster]] — Cheat sheet de comandos









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 - Rockstar.md|Fuzzing de parámetros con x8 - Rockstar]] — DirSearch, GoBuster, Hack The Box
- [[../../apuntes Chema/Anonimato, Ingeniería Social y Enumeración Web.md|Anonimato, Ingeniería Social y Enumeración Web]] — x8, Fuzzing, Kali Linux
- [[../../apuntes Andres/06.07.2026 Fuzzing de Parámetros, Ingeniería Social y Anonimato.md|06.07.2026 Fuzzing de Parámetros, Ingeniería Social y Anonimato]] — Fuzzing, GoBuster, Kali Linux
- [[../../apuntes Andres/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking.md|02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]] — Fuzzing, Directory Listing, GoBuster
- [[../../comandos/FFUF.md|FFUF]] — Desarrollo Web, DirSearch, GoBuster
- [[../comandos/FFUF.md|FFUF]] — Desarrollo Web, DirSearch, GoBuster
- [[../02 - Sistemas Operativos/Migrar VM VirtualBox a VMware.md|Migrar VM VirtualBox a VMware]] — DirSearch, GoBuster, Hack The Box
- [[../../comandos/DirSearch.md|DirSearch]] — Desarrollo Web, DirSearch, GoBuster

### 🌐 Cross-Dominio

- [[../../../programacion/CSS/fundamentos_css.md|fundamentos_css]] — Programacion: Bases de Datos, Desarrollo Web, Redes
- [[../../../programacion/PHP/seguridad_php.md|seguridad_php]] — Programacion: Bases de Datos, Desarrollo Web, Redes

> #burpsuite #database #dirsearch #feroxbuster #ffuf #gobuster #hack_the_box #hydra #redes #web
