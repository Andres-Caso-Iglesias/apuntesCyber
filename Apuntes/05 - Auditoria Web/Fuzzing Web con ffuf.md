

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

## ⑥ Wordlists recomendadas

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

---

## Enlaces relacionados

- [[comandos/FFUF]] — Cheat sheet de comandos
- [[comandos/Feroxbuster]] — Cheat sheet de comandos



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../comandos/FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster
- [[../../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 — Rockstar.md|Fuzzing de parámetros con x8 — Rockstar]] — FFUF, Feroxbuster, GoBuster
- [[../comandos/Feroxbuster.md|Feroxbuster]] — FFUF, Feroxbuster, GoBuster
- [[../comandos/FFUF.md|FFUF]] — FFUF, Feroxbuster, GoBuster
- [[../comandos/GoBuster.md|GoBuster]] — FFUF, Feroxbuster, GoBuster
- [[../../comandos/DirSearch.md|DirSearch]] — FFUF, Feroxbuster, GoBuster

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]

> #burpsuite #dirsearch #feroxbuster #ffuf #gobuster #hack-the-box #hydra #redes
