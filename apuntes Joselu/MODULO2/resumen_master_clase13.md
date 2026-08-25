> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 13**
> **Módulo:** MODULO2
> **Tema:** Clase 13
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 13. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Esta sesión la imparte Carlos Castillo y cierra el módulo de OSINT con un bloque temático poco habitual: la esteganografía, el arte de ocultar información dentro de otros archivos.

La clase tiene un tono más experimental y práctico que las anteriores, y conecta de forma directa con todo lo visto en el módulo.

Si en sesiones previas aprendimos a extraer información de personas y organizaciones desde fuentes abiertas, hoy aprendemos que esa información puede estar escondida en lugares donde nadie pensaría m irar: dentro de las propias imágenes.

El hilo conductor es que el OSINT no termina cuando encontramos una foto, sino que empieza de nuevo cuando la analizamos.

Qué es la esteganografía y por qué importa en OSINT La esteganografía es la técnica de ocultar información dentro de otra información.

A diferencia de la criptografía, que cifra el contenido haciéndolo ilegible, la esteganografía lo esconde haciéndolo invisible: el archivo contenedor parece completamente normal.

Una imagen PNG puede contener un fichero de texto, un ZIP, un malware o unas credenciales, y abrirla con el visor de imágenes no revela nada anómalo.

Esto conecta directamente con el OSINT porque cuando encontramos imágenes de un objetivo, la reacción natural es mirarlas visualmente.

Pero cua lquiera de esas imágenes puede contener información que no está visible, y sin las herramientas adecuadas, pasará completamente desapercibida.

Hay dos perspectivas desde las que usar estas técnicas, y ambas son relevantes en ciberseguridad:
- Ofensiva: ocult ar datos en imágenes para transmitirlos sin levantar sospechas, o para
bypassear filtros de subida de archivos en aplicaciones web
- Defensiva/forense: detectar si un archivo contiene información oculta, extraerla, y evaluar
si puede ser evidencia en una inv estigación

Preparación del laboratorio Antes de usar las herramientas se crea una estructura de archivos de trabajo:
```bash
```bash
mkdir lab_estego && cd lab_estego
```

# Descargar una imagen cualquiera en PNG (ej: logo de Evolve)

# Crear copia en PNG y convertir a J PG

```bash
cp base.png cover.png
```
```

convert base.png cover.jpg

# Crear el archivo "flag" que simula el dato a ocultar

```bash
echo "flag{aqui_estuvo_castillo}" >> flag.txt
```

# Resultado: cuatro archivos en la carpeta

# base.png cover.png cover.jpg flag.txt

El >> es import ante: usa uno (>) y borra el contenido del archivo si ya existía.

Con dos (>>) añade al final sin sobrescribir.

Herramienta 1: file — qué es realmente este archivo El comando file analiza el contenido interno de un archivo, independientemente de su extensión, y devuelve su tipo real.
```bash
file cover.jpg # JPEG image data, JFIF standard file cover.png # PNG image data
```

La trampa que esto detecta: si alguien renombra /etc/passwd como fake.jpg, la extensión dice imagen pero file dice text o.

Esto ocurre en entornos reales cuando atacantes quieren camuflar archivos maliciosos con extensiones benignas, o cuando analizamos un sistema comprometido y encontramos una carpeta llena de supuestas imágenes.
```bash

# Analizar todos los JPG y PNG de un d irectorio de una vez

file *.jpg *.png
```

> [!important] - La idea clave: nunca confiar en la extensión para saber qué es un archivo.

En un forense,
file * sobre una carpeta sospechosa puede revelar inmediatamente qué archivos no son lo que dicen ser

Herramienta 2: strings — leer lo que hay dentro Un ejecutable, una imagen o cualquier binario contiene datos que no son texto legible, pero también puede contener cadenas de texto embebidas que sí lo son. strings extrae únicamente esas cadenas.
```bash
```

strings cover.jpg # Muestra todas las cadenas de texto strings -n 8 cover.jpg # Solo cadenas de 8 caracteres o más (reduce el ruido) strings cover.jpg | grep flag # Buscar una cadena específica strings cover.jpg | tail -50 # Ver solo el final del archivo Si alguien ha incrustado una contraseña, una URL, una flag o cualquier texto en una imagen, strings lo revelará aunque el archivo parezca una imagen normal.

También es útil en análisis de malware para extraer indicadores como URLs de servidores de comando y co ntrol, nombres de funciones o mensajes de error hardcodeados.

Herramienta 3: exiftool — metadatos al completo ExifTool es la herramienta de referencia para leer y escribir metadatos de imágenes.

Los metadatos contienen información sobre cómo, cuándo y dón de se tomó una foto: fabricante y modelo del dispositivo, fecha y hora, coordenadas GPS, software usado, nombre del autor, comentarios, y mucho más.
```bash
```

exiftool cover.jpg # Mostrar todos los metadatos exiftool -GPS:all cover.jpg # Mostra r solo datos GPS exiftool -c "%.6f" cover.jpg # Coordenadas en formato decimal

# Escribir metadatos (modificar o añadir)

exiftool -Artist="Castillo" -Comment="password:holamundo123" cover.jpg El caso que ilustra la clase: si las coordenadas GPS están en formato DMS (grados, minutos, segundos) hay que convertirlas al formato decimal antes de pegarlas en Google Maps.

ExifTool tiene un parámetro de formato ( -c) que hace esa conversión directamente.

La implicación forense: los metadatos son modificables.

Y o puedo cambiar el autor de una foto, su fecha de creación o sus coordenadas GPS.

Esto hace que los metadatos solos no sean evidencia jurídicamente válida sin un hash que certifique la integridad del archivo.

Herramienta 4: binwalk — detectar archivos den tro de archivos Binwalk analiza el contenido binario de un archivo buscando firmas de otros formatos embebidos.

Si dentro de una imagen hay un ZIP, un ejecutable o cualquier otro tipo de archivo, binwalk lo detecta y puede extraerlo.
```bash

# Crear un archiv o con contenido oculto

```

zip flag.zip flag.txt # Crear el ZIP cat cover.jpg flag.zip >> master.jpg # Incrustar ZIP al final de la imagen

# Analizar si hay archivos embebidos

binwalk master.jpg

# Extraer todo lo que encuentre

binwalk -e master.jpg # Crea carpeta master.jpg.extracted/ Resultado: dentro de la carpeta extraída aparece el ZIP y, dentro de él, el flag.txt original.

> [!important] Importante: binwalk puede generar falsos positivos, especialmente en imágenes g randes.

Hay que revisar los tamaños y los offsets antes de asumir que todo lo que reporta es real.

Herramienta 5: steghide — esteganografía con contraseña Steghide permite incrustar un archivo dentro de una imagen protegiéndolo con contraseña.

A diferenci a de los métodos anteriores, la información embebida con steghide no es detectable por binwalk ni por strings.
```bash

# Incrustar flag.txt dentro de cover.jpg con contraseña

```

steghide embed -cf cover.jpg -ef flag.txt -p "iloveyou"

# Comprobar si una imagen t iene contenido embebido

steghide info cover.jpg

# Extraer el contenido (requiere contraseña)

steghide extract -sf cover.jpg -p "iloveyou" Para crackear la contraseña cuando no la conocemos se usa stegcracker con un diccionario:

```bash
```

stegcracker cover.jpg /usr/share/wordlists/rockyou.txt
- La metáfora útil: steghide es una caja fuerte dentro de una imagen.

Binwalk puede decirte
que hay una caja fuerte, pero sin la combinación no puedes abrirla.

Stegcracker la intenta abrir a martillazos usando el diccionario más popular del mundo
> [!important] - La idea clave: el hecho de que steghide pida contraseña al inspeccionar una imagen no
significa que tenga contenido embebido.

Siempre pide contraseña.

Hay que interpretar el resultado correctamente

El ejercicio práctico: de una image n de Windows XP al domicilio de su autor La clase cierra con un reto real de TryHackMe que conecta esteganografía, metadatos y OSINT en una sola investigación.

El punto de partida es una imagen aparentemente inocua.

El flujo de resolución:
- exiftool imagen. jpg revela coordenadas GPS y el campo Copyright con el username
OWoodFlint
- Las coordenadas llevan a una zona concreta de Reino Unido, cerca de Manchester, que
coincide con el lugar donde fue tomada la imagen original de fondo de escritorio de Windows XP
- Buscando OWoodFlint en Twitter aparece un post donde menciona haber hackeado un WiFi
desde su casa e incluye el BSSID de esa red
- Con ese BSSID se accede a Wigle.net (base de datos geolocalizada de redes WiFi) y se
localiza exactamente la red mencionada, lo que permite acotar la zona donde vive el objetivo con una precisión de pocos metros
- En GitHub, bajo el mismo username, aparece información adicional que permite completar
el perfil Todo esto a partir de una s ola imagen con metadatos sin borrar.

Recapitulación integrada Esta sesión cierra el módulo de OSINT con una lección que lo cambia todo: la información que buscamos puede estar en los archivos que ya tenemos.

Sabemos usar file para verificar que un archivo es lo que dice ser, strings para leer su contenido interno, exiftool para extraer y modificar sus metadatos, binwalk para detectar y extraer archivos embebidos, y steghide para ocultar o desenterrar información protegida por contraseña.

Y sabemos que los metadatos GPS de una imagen pueden llevar, en combinación con OSINT sobre redes WiFi, desde una foto anónima hasta la dirección donde vive su autor.

A partir de la próxima sesión arranca el hacking activo: enumeración de servicios, puertos y las primeras m áquinas vulnerables.