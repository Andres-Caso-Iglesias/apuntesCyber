

> [!info] Relacionado con
> [[OSINT - Metodología y Fuentes]] · [[Redes - Topologías y Encapsulación]] · [[Prácticas CTF - HTB y VulnHub]]

---

## ① Metadatos de imagen: EXIF

Las imágenes digitales llevan metadatos **EXIF** incrustados que pueden revelar información muy sensible.

| Campo EXIF | Información revelada |
|-----------|---------------------|
| **GPS Coordinates** | Geolocalización exacta |
| **Camera Make/Model** | Marca y modelo del dispositivo |
| **Date/Time Original** | Fecha y hora de la captura |
| **Software** | Programa de edición |
| **Author/Artist** | Nombre del autor |
| **Serial Number** | Número de serie (algunos modelos) |

> [!danger] CASO REAL
> John McAfee fue localizado por periodistas gracias a las coordenadas GPS en la EXIF de una foto publicada en Twitter. Las redes sociales eliminan EXIF, pero muchas webs corporativas y foros **NO**.

---

## ② exiftool — Extracción de metadatos

```bash
# Instalación
sudo apt install exiftool

# Uso básico
exiftool imagen.jpg # todos los metadatos
exiftool -GPS* imagen.jpg # solo datos GPS
exiftool -Author documento.pdf # autor del PDF

# Procesar múltiples ficheros
exiftool *.jpg # todos los JPG
exiftool -r /directorio/ # recursivo

# Exportar a CSV
exiftool -csv *.jpg > metadatos.csv

# Eliminar todos los metadatos (antes de publicar)
exiftool -all= imagen.jpg
exiftool -all= -r /directorio/ # recursivo

# Modificar metadatos
exiftool -Author='Anónimo' fichero.docx
exiftool -GPSLatitude= -GPSLongitude= imagen.jpg # borrar GPS
```

> [!tip] OSINT
> En una auditoría: descargar imágenes del sitio web corporativo y analizar sus EXIF puede revelar nombres de empleados, software interno y hasta coordenadas de la oficina.

---

## ③ Búsqueda inversa de imágenes

| Herramienta | Uso |
|------------|-----|
| **Google Lens** | Análisis completo, objetos y lugares |
| **Google Images** | Búsqueda inversa clásica |
| **Yandex Images** | Mejor para encontrar rostros |
| **TinEye** | Rastrea copia exacta |
| **PimEyes** | Reconocimiento facial |
| **FaceCheck.ID** | Búsqueda por rostro en redes sociales |

---

## ④ Steghide — Esteganografía

La esteganografía oculta información **dentro** de otro fichero. A diferencia de la criptografía, el objetivo es que **nadie sepa** que hay algo oculto.

```bash
# Instalación
sudo apt install steghide

# Ocultar mensaje en imagen
steghide embed -cf imagen.jpg -sf secreto.txt
# -cf = cover file (imagen contenedora)
# -sf = secret file (fichero a ocultar)
# Te pedirá contraseña

# Extraer mensaje oculto
steghide extract -sf imagen.jpg

# Ver info sin extraer
steghide info imagen.jpg

# Fuerza bruta de contraseña
pip install stegcracker
stegcracker imagen.jpg /usr/share/wordlists/rockyou.txt
```

> [!tip] CTF
> En CTFs, la esteganografía es muy común. Siempre que veas una imagen o audio, comprueba si contiene datos ocultos con `steghide`, `binwalk` o `strings`.

---

## ⑤ binwalk — Análisis forense

```bash
sudo apt install binwalk

binwalk imagen.jpg # analizar (muestra ficheros embebidos)
binwalk -e imagen.jpg # extraer todo
binwalk -Me imagen.jpg # recursivo (extrae dentro de lo extraído)
```

Útil para firmware de routers y dispositivos IoT.

---

## ⑥ strings — Texto en binarios

```bash
strings imagen.jpg
strings ejecutable.exe | grep -i password
strings firmware.bin | grep -E 'http|ftp|admin'

# En CTFs, buscar flags
strings fichero | grep 'CTF{|FLAG{'

# Combinado con file
file imagen.jpg # verifica tipo real
xxd imagen.jpg | head -20 # ver bytes en hex (magic bytes)
```

---

## ⑦ Resumen: herramientas por caso

| Herramienta | Uso principal |
|------------|--------------|
| **exiftool** | Metadatos de imagen, documentos, PDF |
| **steghide** | Ocultar/extraer datos en JPEG/BMP |
| **binwalk** | Ficheros incrustados en binarios |
| **strings** | Texto en binarios, credenciales hardcodeadas |
| **Google Lens / Yandex** | Búsqueda inversa, reconocimiento facial |
| **Shodan** | Dispositivos IoT, cámaras, servicios expuestos |
| **stegcracker** | Fuerza bruta contraseña de steghide |

---

## Checklist de repaso

- [ ] ¿Sé extraer metadatos EXIF con exiftool?
- [ ] ¿Entiendo qué información puede filtrar una foto?
- [ ] ¿Sé ocultar y extraer datos con steghide?
- [ ] ¿Puedo analizar binarios con binwalk y strings?
- [ ] ¿Conozco las herramientas de búsqueda inversa de imágenes?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]]— Forense Digital, Hydra, Redes
- [[../../apuntes Chema/OSINT y Esteganografía.md|OSINT y Esteganografía]]— Forense Digital, Hydra, OSINT
- [[../05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|Vulnerabilidades Web — OWASP Top 10 y Burp Suite]]— Hack The Box, Hydra, VulnHub
- [[../../apuntes Joselu/MODULO1/resumen_master_clase7.md|resumen_master_clase7]]— Hack The Box, Hydra, Redes
- [[../05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]]— Hack The Box, Hydra, VulnHub
- [[../07 - Empleabilidad/Mercado Laboral y Certificaciones.md|Mercado Laboral y Certificaciones]]— Hack The Box, Metodología Pentest, VulnHub

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]

> #esteganografia #forense #hack-the-box #hydra #osint #pentest #redes #vulnhub
