# ① Metadatos de imagen: EXIF

Las imágenes digitales llevan metadatos EXIF incrustados. Pueden revelar información muy sensible de forma involuntaria.

|**Campo EXIF**|**Información revelada**|
|---|---|
|GPS Coordinates|Geolocalización exacta donde se tomó la foto|
|Camera Make/Model|Marca y modelo del dispositivo|
|Date/Time Original|Fecha y hora exacta de la captura|
|Software|Programa usado para editar/exportar|
|Author/Artist|Nombre del autor en documentos Word/PDF|
|GPS Altitude|Altitud sobre el nivel del mar|
|Serial Number|Número de serie del dispositivo (algunos modelos)|

| | |
|---|---|
|**🔐 CASO REAL**|John McAfee fue localizado por periodistas gracias a las coordenadas GPS en la EXIF de una foto publicada en Twitter. Las redes sociales eliminan EXIF, pero muchas webs corporativas y foros NO.|

# ② exiftool — Extracción de metadatos

| |
|---|
|# Instalación:<br><br>sudo apt install exiftool<br><br># Uso básico:<br><br>exiftool imagen.jpg              # ver todos los metadatos<br><br>exiftool -GPS* imagen.jpg        # solo datos GPS<br><br>exiftool -Author documento.pdf   # autor del PDF<br><br># Procesar múltiples ficheros:<br><br>exiftool *.jpg                   # todos los JPG del directorio<br><br>exiftool -r /directorio/         # recursivo<br><br># Exportar a CSV:<br><br>exiftool -csv *.jpg > metadatos.csv<br><br># Eliminar todos los metadatos (antes de publicar):<br><br>exiftool -all= imagen.jpg<br><br>exiftool -all= -r /directorio/   # recursivo<br><br># Modificar metadatos:<br><br>exiftool -Author='Anónimo' fichero.docx<br><br>exiftool -GPSLatitude= -GPSLongitude= imagen.jpg  # borrar GPS|

| | |
|---|---|
|**💡 OSINT**|En una auditoría: descargar imágenes del sitio web corporativo y analizar sus EXIF puede revelar: nombres de empleados (Author), software interno, y hasta coordenadas de la oficina.|

# ③ Búsqueda inversa de imágenes

Permite encontrar dónde más aparece una imagen o identificar personas/lugares a partir de una foto.

|**Herramienta**|**Uso**|
|---|---|
|Google Lens|Análisis de imagen completo, objetos y lugares|
|Google Images|Búsqueda inversa clásica (arrastrar imagen)|
|Yandex Images|Muy efectivo para encontrar rostros (mejor que Google)|
|TinEye|Rastrea copia exacta de imágenes en internet|
|PimEyes|Reconocimiento facial (uso ético discutible)|
|FaceCheck.ID|Búsqueda por rostro en redes sociales|

| |
|---|
|# Técnica 4chan / Forza: geolocalización por imagen<br><br># Caso famoso: localizar una bandera solo viendo el cielo<br><br># Proceso:<br><br># 1. Analizar objetos en la imagen (señales, edificios, vegetación)<br><br># 2. Analizar patrones de estrellas visibles → hora y latitud aprox.<br><br># 3. Rastrear patrones de aviones sobrevolando (flightradar24)<br><br># 4. Cruzar con mapas de satélite (Google Earth)<br><br># → En <48 horas encontraron la bandera en un campo de Tennessee|

# ④ Steghide — Esteganografía

La esteganografía oculta información **dentro** de otro fichero (imagen, audio). A diferencia de la criptografía, el objetivo es que nadie sepa que hay información oculta.

| |
|---|
|# Instalación:<br><br>sudo apt install steghide<br><br># Ocultar mensaje en imagen:<br><br>steghide embed -cf imagen.jpg -sf secreto.txt<br><br># -cf = cover file (la imagen contenedora)<br><br># -sf = secret file (el fichero a ocultar)<br><br># Te pedirá contraseña para proteger el secreto<br><br># Extraer mensaje oculto:<br><br>steghide extract -sf imagen.jpg<br><br># Te pedirá la contraseña<br><br># Ver información sobre el contenido oculto (sin extraer):<br><br>steghide info imagen.jpg<br><br># Fuerza bruta de contraseña (con stegcracker):<br><br>pip install stegcracker<br><br>stegcracker imagen.jpg /usr/share/wordlists/rockyou.txt|

| | |
|---|---|
|**🎯 CTF**|En CTFs, la esteganografía es muy común. Siempre que veas una imagen o audio, comprueba si contiene datos ocultos con steghide, binwalk o strings.|

# ⑤ binwalk — Análisis forense de ficheros

| |
|---|
|# binwalk analiza ficheros binarios buscando ficheros incrustados<br><br>sudo apt install binwalk<br><br># Analizar un fichero:<br><br>binwalk imagen.jpg<br><br># Muestra ficheros embebidos (ZIP, PDF, EXE...)<br><br># Extraer todo lo encontrado:<br><br>binwalk -e imagen.jpg<br><br># Crea directorio _imagen.jpg.extracted/ con los ficheros<br><br># Recursivo (extrae dentro de lo extraído):<br><br>binwalk -Me imagen.jpg<br><br># También útil para firmware de routers y dispositivos IoT|

# ⑥ strings — Texto en ficheros binarios

| |
|---|
|# strings extrae cadenas de texto legibles de cualquier fichero binario<br><br>strings imagen.jpg<br><br>strings ejecutable.exe \| grep -i password<br><br>strings firmware.bin \| grep -E 'http\|ftp\|admin'<br><br># Filtrar solo strings relevantes:<br><br>strings fichero \| grep -i 'pass\\|user\\|key\\|secret\\|token'<br><br># En CTFs, buscar flags:<br><br>strings fichero \| grep 'CTF{\\|FLAG{'<br><br># Combinado con file para identificar primero el tipo:<br><br>file imagen.jpg      # verifica si es realmente una imagen<br><br>xxd imagen.jpg \| head -20  # ver bytes en hex (magic bytes)|

# ⑦ Shodan para OSINT de cámaras e IoT

| |
|---|
|# Shodan indexa miles de dispositivos IoT expuestos<br><br># Búsqueda de cámaras IP:<br><br>title:'webcamXP 5'              # cámaras con panel web<br><br>product:'Hikvision'             # marca específica<br><br>port:554 has_screenshot:true    # cámaras RTSP con captura<br><br># Bases de datos expuestas:<br><br>product:MongoDB port:27017      # MongoDB sin autenticación<br><br>product:Elasticsearch           # Elasticsearch expuesto<br><br># ICS/SCADA (infraestructura crítica):<br><br>product:'Siemens'               # PLCs Siemens<br><br># ⚠ ACLARACIÓN:<br><br># Las cámaras 'públicas' son accesibles porque están mal configuradas<br><br># Acceder a ellas puede ser legal (son públicas) pero:<br><br># - Manipularlas es ilegal<br><br># - Usarlas para vigilancia sin consentimiento es ilegal<br><br># - En auditorías: documenta y notifica, no manipules|

| | |
|---|---|
|**🔐 FOOTPRINTING**|En una auditoría externa real: buscar en Shodan los activos del cliente revela cámaras, paneles de administración y servicios desconocidos que el propio cliente olvidó que tenía expuestos.|

# ⑧ Resumen: herramientas por caso de uso

|**Herramienta**|**Uso principal**|
|---|---|
|exiftool|Metadatos de imagen, documentos Office, PDF|
|steghide|Ocultar/extraer datos en imágenes JPEG/BMP|
|binwalk|Ficheros incrustados en binarios, firmware IoT|
|strings|Texto en binarios, credenciales hardcodeadas|
|Google Lens / Yandex|Búsqueda inversa de imágenes, reconocimiento facial|
|Shodan|Dispositivos IoT, cámaras, servicios expuestos|
|stegcracker|Fuerza bruta contraseña de steghide|
|pngcheck|Validar/analizar PNGs (CTFs)|
|zsteg|Esteganografía en PNG y BMP|