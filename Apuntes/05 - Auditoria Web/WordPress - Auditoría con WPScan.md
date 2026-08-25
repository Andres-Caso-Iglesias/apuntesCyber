

> [!info] Relacionado con
> [[Burp Suite - Framework de AuditorÃ­a]] Â· [[Apuntes/05 - Auditoria Web/EnumeraciÃ³n Web]] Â· [[OWASP Top 10 - CVE CVSS CWE]] Â· [[Fuzzing Web con ffuf]]

---

## â‘  CMS vs Web nativa

| Tipo | DescripciÃ³n |
|------|------------|
| **Web nativa** | Programada directamente (PHP, .NET, Java). SQLi, XSS directos. |
| **CMS** | WordPress, Joomla, Drupal. NÃºcleo + plugins de terceros. |

â†’

> [!important] Idea central
> El nÃºcleo de WordPress rara vez es vulnerable (estÃ¡ muy revisado). Las grandes vulnerabilidades aparecen en los **plugins**, porque hay miles y **nadie audita su seguridad**.

---

## â‘¡ MetodologÃ­a de auditorÃ­a WordPress

```
1. EnumeraciÃ³n web â†’ /wordpress detectado
 â†“
2. [[WPScan]] â†’ versiÃ³n, plugins, temas, usuarios
 â†“
3. Enumerar usuarios (mensajes de error del login)
 â†“
4. Fuerza bruta con [[WPScan]] (ÃšLTIMO recurso)
 â†“
5. Login â†’ Editor de temas â†’ RCE
 â†“
6. Reverse shell â†’ www-data â†’ Estabilizar TTY
```

---

## â‘¢ [[WPScan]] â€” La navaja suiza

```bash
# Escaneo base (detecta versiÃ³n)
[[WPScan]] --url http://OBJETIVO/wordpress

# Enumerar usuarios con diccionario
[[WPScan]] --url http://OBJETIVO/wordpress -e u \
 -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt

# Enumerar plugins
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate ap

# Plugins vulnerables con API token (aÃ±ade CVEs)
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate vp --api-token TOKEN

# Fuerza bruta de contraseÃ±as
[[WPScan]] --url http://OBJETIVO/wordpress --enumerate ap \
 --passwords /usr/share/wordlists/rockyou.txt
```

| Flag | FunciÃ³n |
|------|---------|
| `-e u` | Enumerar usuarios |
| `-e ap` | Todos los plugins |
| `-e vp` | Plugins vulnerables (con token) |
| `--passwords` | Fuerza bruta |
| `--api-token` | Conectar con BD de vulnerabilidades |

> [!tip] API TOKEN
> El token **no** aporta capacidades ofensivas. Solo conecta con la BD de vulnerabilidades. Se obtiene gratis en wpscan.com.

---

## â‘£ EnumeraciÃ³n de usuarios por mensajes de error

| Mensaje | Significado |
|---------|-----------|
| "El nombre de usuario X no estÃ¡ registrado" | Usuario **no existe** |
| "La contraseÃ±a es incorrecta" | Usuario **sÃ­ existe** |

> [!warning] INFORMATION DISCLOSURE
> Un login bien diseÃ±ado responde siempre: "usuario o contraseÃ±a incorrectos". Cuando distingue entre ambos, **filtra informaciÃ³n**.

---

## â‘¤ RCE por editor de temas

Con acceso al panel `/wp-admin`:

1. **Apariencia â†’ Editor de temas**
2. Seleccionar plantilla **PHP** (ej: `404.php`)
3. Pegar **reverse shell PHP**
4. Guardar
5. Poner Netcat a la escucha
6. Visitar la pÃ¡gina 404 en el navegador

```bash
nc -lvnp 1234
# Visitar http://OBJETIVO/wordpress/404.php
# â†’ ConexiÃ³n recibida como www-data
```

> [!warning] LA PLANTILLA DEBE SER PHP
> Si es HTML, el cÃ³digo PHP **no se ejecuta**. Busca un fichero `.php`.

---

## â‘¥ Rutas WordPress a comprobar

| Ruta | QuÃ© nos dice |
|------|-------------|
| `/wordpress/license.txt` | Confirma WordPress, instalaciÃ³n reciente |
| `/wp-login.php` | Login â†’ posible fuerza bruta |
| `/wp-admin/` | Panel de administraciÃ³n |
| `/wp-content/uploads/` | Subidas â†’ posible file upload |
| `/xmlrpc.php` | API antigua |

---

## â‘¦ EstabilizaciÃ³n de la shell

```bash
# En la vÃ­ctima (desde la reverse shell)
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z (suspender)
# En Kali:
stty raw -echo; fg
# Enter una o dos veces
```

---

## Checklist de repaso

- [ ] Â¿Distingo una web nativa de un CMS?
- [ ] Â¿Entiendo por quÃ© el peligro estÃ¡ en los plugins?
- [ ] Â¿SÃ© enumerar versiÃ³n, usuarios y plugins con [[WPScan]]?
- [ ] Â¿Conozco la diferencia entre [[WPScan]] con y sin API token?
- [ ] Â¿SÃ© conseguir RCE con el editor de temas?
- [ ] Â¿Entiendo la transiciÃ³n HTTP â†’ TCP al obtener la shell?

---

## Enlaces relacionados

- [[comandos/WPScan]] â€” Cheat sheet de comandos

â†’

â†’
