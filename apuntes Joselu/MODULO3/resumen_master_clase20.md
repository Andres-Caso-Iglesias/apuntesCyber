> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 20**
> **Módulo:** MODULO3
> **Tema:** Clase 20
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 20. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1.

Contexto y estructura del bloque práctico

Esta sesión de viernes marca el inicio del bloque de práctica ofensiva del máster.

El objetivo es una primera toma de contacto real con el hacking, usando la máquina vulnerable **Metasploitable 2** como objetivo desde Kali Linux.

El profesor (Carlos, en sesión de repaso) explica que esta primera fase no es el hacking definitivo, sino aprender a:

- Configurar correctamente el entorno de virtualización.
- Descubrir la red y encontrar la máquina objetivo.
- Usar Nmap con criterio, entendiendo el ruido que genera.
- Analizar los puertos abiertos y comenzar a comprender cada protocolo.

**Roadmap del bloque práctico:** - Esta semana y la siguiente: Metasploitable 2 (servicios básicos: FTP, SSH, Telnet, SMB, web...) - Siguiente fase: hacking web intensivo (2 semanas) - Fase posterior: **Hack The Box** con licencia (sin máquinas locales, conexión directa) - Últimas semanas: Active Directory con Castillo (pivoting avanzado)

**Consejo sobre idioma en GitHub:** publicar proyectos y herramientas en inglés, aunque sea complicado, abre muchas más puertas en entrevistas y da mayor visibilidad internacional.

## 2.

Configuración del adaptador de red en VirtualBox

Para que Kali Linux y Metasploitable 2 estén en la misma red y puedan comunicarse:

- Ambas máquinas deben tener configurado **Adaptador Puente** (*Bridged Adapter*), no NAT.
- Seleccionar la misma tarjeta de red en ambas: si se va por cable → **Realtek**; si se va por WiFi → adaptador **Intel WiFi**.
- Si ambas se conectan por el mismo medio (cable o WiFi), tendrán IPs en el mismo rango (192.168.1.x) y podrán comunicarse.
- **Problema habitual con NAT:** asigna la misma IP a ambas máquinas, generando conflictos de conectividad.

Solución: cambiar siempre a Bridge.
- Tras cambiar el adaptador con la máquina encendida, puede no actualizarse la IP automáticamente.

Solución: cerrar y reiniciar la máquina, o ejecutar if down / if up en la interfaz de red.

**Credenciales de Metasploitable 2:** usuario msfadmin, contraseña msfadmin.

Entrar en la máquina y ejecutar ifconfig o ip a para obtener su IP directamente, si no se quiere hacer el proceso de descubrimiento.

## 3.

Fase de descubrimiento de red

### Comprobación de conectividad: ping

Antes de cualquier escaneo, verificar que hay conectividad ejecutando ping 8.8.8.8 (Google) desde Kali.

Si responde, hay Internet.

ping -c 4 IP_objetivo

El **TTL** (*Time To Live*) del ping indica el sistema operativo aproximado del objetivo:

TTL Sistema Operativo
 ------------------- -----------------------------------------
Cercano a **64** Linux/Unix Cercano a **128** Windows Cercano a **255** Dispositivo de red (router/switch Cisco)

El TTL va disminuyendo en 1 por cada salto de red.

En Hack The Box siempre es 1 menos (63 para Linux, 127 para Windows) por la VPN intermedia.

**Limitación del ping en AWS:** por defecto, AWS desactiva las trazas ICMP, por lo que el ping no funciona.

En ese caso hay que usar Nmap directamente con -Pn.

### Herramientas de descubrimiento de red

```bash
sudo netdiscover -r 192.168.1.0/24 Escanea la red ARP y muestra todas las IPs activas con su dirección MAC y fabricante.
```

La MAC del fabricante "PC System Technic GMBH" identifica máquinas virtuales VirtualBox.

```bash
sudo arp-scan 192.168.1.0/24 Equivalente a netdiscover pero basado en ARP directamente.
```

Más rápido y directo.

Script de descubrimiento con ping (one-liner):

for i in $(seq 1 254); do ping -c 1 -W 1 192.168.1.$i | grep "bytes from" | cut -d' ' -f4 | tr -d ':' & done

Itera todas las IPs del rango, hace un ping a cada una y muestra las que responden.

Permite además filtrar por TTL para distinguir Linux (64) de Windows (128).

```bash
nmap -sn 192.168.1.0/24 Descubrimiento de hosts sin escanear puertos (flag -sn).
```

Más completo que el ping manual pero genera más ruido.

Útil cuando el ping está desactivado en el entorno.

## 4.

Nmap: metodología de escaneo en dos fases

### ¿Por qué dos comandos?

Hacer un solo Nmap completo sobre todos los puertos con scripts de versión es muy lento.

La metodología en dos fases es mucho más eficiente:

Fase 1 --- Escaneo rápido (descubrir puertos abiertos):

```bash
sudo nmap -p- --min-rate 5000 192.168.1.X
```

- -p-: escanea todos los puertos (del 1 al 65535).
- \--min-rate 5000: envía al menos 5000 paquetes por segundo (máximo técnico \~1500; poner 5000 forza la velocidad máxima).

Se puede reducir a 1000-1500 si el entorno es sensible al ruido.
- Resultado: lista de puertos abiertos en segundos.

Fase 2 --- Escaneo en profundidad (solo puertos abiertos):

```bash
sudo nmap -p 21,22,23,25,53,80,111,139,445,512,3306,5900 -sV -sC 192.168.1.X
```

- -p 21,22,\...: solo analiza los puertos descubiertos en la fase 1.
- -sV: detecta versiones de los servicios.
- -sC: lanza scripts básicos de Nmap (enumeración, detección de FTP anónimo, etc.).
- Resultado: versiones exactas de cada servicio, información de configuración y resultados de scripts.

**Parámetros adicionales útiles:** - -v o -vvvv: verbosidad --- muestra los resultados a medida que se van descubriendo, sin esperar al final del escaneo. - -Pn: omite el ping previo (imprescindible en AWS o cuando ICMP está bloqueado). - -oN resultado.txt: guarda el output en un fichero de texto. - -O: detección del sistema operativo. - -A: modo agresivo (versiones + scripts + OS + traceroute). - -h: ayuda con todos los parámetros disponibles.

### El concepto de "ruido" en hacking

Un escaneo masivo de Nmap genera mucho tráfico de red y puede ser detectado por el SOC/Blue Team del cliente.

En contextos reales: - En redes corporativas con restricciones de ruido: lanzar el escaneo durante horas de máximo tráfico (mediodía) para camuflarse. - Reducir el \--min-rate para ir más lento y ser menos detectable. - En laboratorio y CTF: no importa el ruido, usar los valores máximos.

### Falsos positivos en los nombres de servicio

Nmap asigna nombres de servicio por convención del puerto (ej: puerto 21 → FTP).

A veces no es correcto si el servidor usa un puerto no estándar.

El segundo escaneo con -sV confirma el servicio real con mayor precisión.

## 5.

FTP (puerto 21): análisis y vectores de ataque

### ¿Qué es el FTP?

El **FTP** (*File Transfer Protocol*) es un protocolo de transferencia de archivos.

El profesor lo describe como "un pendrive inteligente en la nube": dependiendo del usuario que se conecte, accede a una información u otra.

Es antiguo, no cifrado por defecto, y muy frecuente en entornos mal configurados.

### Tres vectores de ataque sobre FTP

1. **FTP Anónimo:** si está habilitado, cualquier persona puede conectarse al servidor FTP con usuario anonymous y contraseña vacía (o cualquier texto) sin necesidad de credenciales reales.

El script -sC de Nmap lo detecta automáticamente. 2. **Versión vulnerable:** si la versión del FTP tiene CVEs conocidos (ej. **vsftpd 2.3.4** tiene una backdoor que abre el puerto 6200 al enviar :) en el usuario).

La versión se obtiene con -sV. 3. **Credenciales obtenidas por otros medios:** si se obtuvieron credenciales de otros puertos, de bases de datos filtradas o de ingeniería social, se pueden probar directamente en el FTP.

Si ninguno de los tres vectores aplica, el FTP no es explotable de forma directa.

### Combinación FTP + web (puerto 80)

Un FTP no explotable de forma aislada puede convertirse en un vector de RCE si los archivos subidos al FTP se sirven o ejecutan desde una aplicación web.

Ejemplo: - Un atacante con acceso FTP anónimo sube un archivo PHP malicioso. - Si la web sirve los contenidos de ese FTP, al acceder a la URL del archivo PHP, el servidor lo ejecuta. - Resultado: **RCE** y posible escalada a root.

La analogía del profesor: "el FTP es la pistola (tiene los archivos), la web es la munición (los ejecuta).

Por separado no hacen nada; juntos, matan."

### Comando para conectarse al FTP

ftp 192.168.1.X

# Usuario: anonymous

# Contraseña: (vacía o cualquier texto)

Una vez dentro: ls para listar archivos, get fichero para descargar, put fichero para subir.

## 6.

Próxima sesión

La semana siguiente se continuará con Metasploitable 2, profundizando en más protocolos (SSH puerto 22, Telnet puerto 23, SMB puertos 139/445, web puerto 80) y comenzando a correlacionar servicios para construir cadenas de explotación.

## 7.

Conceptos y términos clave corregidos

Término en la transcripción Corrección / Aclaración
---------------------------------------------- ------------------------------------------------------------------------------------------------------------------
Metaprotable / MetaFlowtable / metasproteico **Metasploitable 2** -- máquina Linux vulnerable intencionalmente para práctica de pentesting Hubdevox / HadThe Box / Haddevox **Hack The Box (HTB)** -- plataforma de práctica de pentesting online LJPT / USCP **eJPT v2 / OSCP** -- certificaciones de pentesting de eLearnSecurity y Offensive Security En el map / animac / EMAD **Nmap** -- herramienta de escaneo de puertos y servicios guión p guión / guión SN / guión pene -p- **/** -sN **/** -pN -- flags de Nmap para escaneo de puertos, descubrimiento de hosts y omisión de ping guión min rate / minrate \--min-rate -- parámetro de Nmap para establecer la velocidad mínima de paquetes por segundo guión SVC / guión SC -sV -sC -- flags de Nmap para detección de versiones y lanzamiento de scripts net deskober / net discobar **netdiscover** -- herramienta de descubrimiento de hosts en red local mediante ARP TTL 64 / TTL 128 **TTL (Time To Live)** -- valor que indica el número de saltos restantes del paquete; 64 ≈ Linux, 128 ≈ Windows Adaptador Puente / Red Nat **Bridged Adapter / NAT** -- modos de red de VirtualBox If config / if up / if down ifconfig **/** if up **/** if down -- comandos para gestionar interfaces de red en Linux FTP anónimos / anónimos **FTP Anónimo (anonymous FTP)** -- acceso sin credenciales al servidor FTP Puerto 21 / veintiuno **Puerto 21 / FTP** -- puerto estándar del protocolo de transferencia de archivos SFTP **SFTP** (*Secure File Transfer Protocol*) -- versión cifrada del FTP sobre SSH RCA / RCE **RCE** (*Remote Code Execution*) -- ejecución remota de código PC System Technic GMVH **PC System Technic GMBH** -- fabricante asociado a la MAC de máquinas virtuales VirtualBox Clouddecode / Claudia / Claudio **Claude Code / Claude** -- herramientas de Anthropic para desarrollo asistido por IA Sabitar **Xabier (Sabitar)** -- alumno del máster que desarrolló herramientas propias durante el curso Eduardo Soriano de Satec **Eduardo Soriano** -- especialista en Blue Team de la consultora **Satec**, futuro profesor del módulo defensivo

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.