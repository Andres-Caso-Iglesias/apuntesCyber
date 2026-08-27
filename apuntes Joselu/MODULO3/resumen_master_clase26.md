> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 26**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 26
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 26. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
**MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy**

## 1.

Contexto y objetivos de la sesiÃ³n

Esta sesiÃ³n la imparte **Yuba GonzÃ¡lez** y marca un hito importante en el mÃ¡ster: es el primer contacto real con **Hack The Box (HTB)**, la plataforma de prÃ¡ctica de hacking mÃ¡s importante del sector.

DespuÃ©s de semanas trabajando en Metasploitable 2 en un entorno local, ahora se trabaja contra mÃ¡quinas reales en la nube, conectadas a travÃ©s de una VPN.

**Nota sobre el nombre del archivo:** la transcripciÃ³n indica que falta el resumen oficial de Evolve --- se genera completamente a partir de la clase grabada.

## 2.

Hack The Box: ecosistema completo

### Â¿QuÃ© es Hack The Box?

Hack The Box (hackthebox.com) es la plataforma lÃ­der mundial para practicar habilidades de hacking de forma **legal y Ã©tica**.

Permite atacar mÃ¡quinas vulnerables en entornos controlados sin necesidad de explotar sistemas reales.

**Valor profesional real:** el perfil de HTB es visible pÃºblicamente.

Muchos reclutadores (incluido el propio Yuba en sus equipos) filtran candidatos consultando su historial de mÃ¡quinas completadas.

Es un diferenciador que se puede poner en el LinkedIn.

**RecomendaciÃ³n del profesor:** usar el correo personal real (no temporal) para crear la cuenta, ya que serÃ¡ una herramienta de desarrollo profesional a largo plazo.

## 3.

MÃ³dulos del ecosistema HTB

### HTB Labs --- el mÃ³dulo principal

Contiene las mÃ¡quinas vulnerables organizadas en categorÃ­as.

Cada mÃ¡quina tiene dos **flags** (archivos de texto con un cÃ³digo Ãºnico): - **user.txt** â†’ flag del usuario sin privilegios - **root.txt** â†’ flag del administrador/root

El objetivo es comprometer la mÃ¡quina, encontrar las flags y validarlas en la plataforma para obtener puntos.

Este sistema es idÃ©ntico al de los exÃ¡menes de certificaciones (OSCP, eJPT, etc.).

**Starting Point** --- la secciÃ³n para principiantes: - MÃ¡quinas clasificadas en **Tier 0, Tier 1 y Tier 2**. - Tier 0 = muy fÃ¡cil (*Very Easy*), un Ãºnico servicio a explotar. - Las mÃ¡quinas de Starting Point son **gratuitas**, accesibles sin suscripciÃ³n de pago. - Tienen un **modo guiado** con preguntas que van orientando el proceso, y un modo libre sin pistas.

### HTB Academy --- aprendizaje guiado

Plataforma de formaciÃ³n con mÃ³dulos organizados en *paths* (rutas de aprendizaje).

Para el profesor, es uno de los mejores recursos para aprender hacking de forma estructurada.

TambiÃ©n aloja las certificaciones propias de HTB.

**Certificaciones HTB:** precio aproximado 400â‚¬.

MÃ¡s asequibles que OSCP (\~2.000â‚¬) o eCPPT, pero con menor reconocimiento en el mercado a dÃ­a de hoy.

Ãštiles para aprender, no tanto para el currÃ­culum frente a RR.HH. no tÃ©cnicos.

**Consejo sobre certificaciones en general:** siempre negociarlas con la empresa al incorporarse.

Un junior puede negociar entre 24.000-28.000â‚¬ + una certificaciÃ³n anual pagada por la empresa (OSCP, CRTO o similar).

### HTB Academy mÃ³dulo relevante: HTBByAcademy

Buscador que cruza el mÃ³dulo tÃ©cnico que quieres practicar (ej. *pivoting*) con las mÃ¡quinas de HTB que tienen ese contenido.

Permite entrenar habilidades concretas de forma dirigida.

### Otras secciones

- **Challenges:** retos aislados por categorÃ­as (Web, Reversing, Forensics, OSINT, Crypto...).

Sin mÃ¡quina completa, solo un problema concreto.

La clase de anÃ¡lisis de malware con CyberDefenders era un reto de este tipo.
- **Sherlocks / EndgameBox:** retos defensivos (Blue Team, respuesta a incidentes, forense).
- **Tracks:** colecciones recomendadas de mÃ¡quinas y retos agrupadas por tema (Blockchain, AD, IoT...).

Creadas por HTB o partners.
- **Fortress:** laboratorios vulnerables creados por grandes empresas (AWS, Synack, Falabella).

Son entornos reales de esas compaÃ±Ã­as recreados como ejercicio de seguridad.
- **Pro Labs:** entornos corporativos completos con mÃºltiples mÃ¡quinas y Active Directory real.

Nivel avanzado.

SuscripciÃ³n aparte.

Incluyen certificado de completion.
- **HTB Business:** versiÃ³n corporativa para que las empresas gestionen rutas de aprendizaje para sus equipos.

Poco extendida todavÃ­a.

## 4.

ConfiguraciÃ³n del entorno: VPN de HTB

Para atacar las mÃ¡quinas de HTB desde la Kali propia, es necesario conectarse a la red privada de HTB mediante una VPN.

### Descargar el archivo VPN

## 1.

Entrar a hackthebox.com â†’ botÃ³n **Connect** (arriba a la derecha).

## 2.

Seleccionar la red a la que conectarse:

 - **Starting Point** â†’ VPN exclusiva para las mÃ¡quinas de Starting Point.
 - **Machines** â†’ VPN para el resto de mÃ¡quinas.
 - ⚠ Son VPNs **diferentes**.

Con la de Starting Point no se accede a Machines y viceversa.

## 3.

Seleccionar **Open VPN** (no PwnBox).

## 4.

Descargar el archivo `.ovpn` generado automÃ¡ticamente.

### Conectarse a la VPN desde Kali

# Pasar el archivo .ovpn a Kali (carpeta compartida, wget, o abrir HTB en Firefox dentro de Kali)

```bash
sudo openvpn nombre_archivo.ovpn
```

La terminal debe quedar abierta mostrando el proceso.

Cuando aparece `Initialization Sequence Completed` la conexiÃ³n es exitosa.

**Verificar la conexiÃ³n:**

ifconfig # Buscar el adaptador tun0 — esa es la IP de HTB

El adaptador **tun0** es la identidad del atacante dentro de la red de HTB.

Esa IP es la que hay que usar como `LHOST` en los exploits.

> [!important] **Importante:** la terminal con la VPN debe permanecer abierta durante toda la sesiÃ³n.

Si se cierra, se pierde la conexiÃ³n y las mÃ¡quinas dejan de ser accesibles.

### PwnBox (alternativa)

HTB ofrece una mÃ¡quina Parrot OS preconfigurada en la nube directamente en el navegador.

Tiene un lÃ­mite de horas diarias de uso en la cuenta gratuita.

El profesor recomienda usar la Kali propia para evitar consumir ese lÃ­mite y tener mÃ¡s control sobre el entorno.

## 5.

MetodologÃ­a en Hack The Box: el flujo estÃ¡ndar

El flujo de trabajo en HTB es idÃ©ntico al de las auditorÃ­as reales:

## 1.

Crear estructura de carpetas del proyecto 2.

Conectar la VPN (tun0) 3.

Levantar la mÃ¡quina (Start Machine â†’ obtener IP objetivo) 4.

EnumeraciÃ³n con Nmap 5.

Buscar en HackTricks el servicio encontrado 6.

Explotar segÃºn la metodologÃ­a 7.

Encontrar las flags (user.txt y root.txt) 8.

Validar en la plataforma

**Flags en HTB:** siempre estÃ¡n en el mismo sitio --- el **escritorio del usuario** comprometido (`/root/` si se es root, `/home/usuario/Desktop/` si es usuario normal).

Comando: `cat /root/flag.txt` o `ls` + `cat`.

**Las flags son dinÃ¡micas:** muchas mÃ¡quinas de HTB generan flags Ãºnicas por usuario para evitar que se compartan directamente.

Si la flag no valida, puede ser que se haya copiado con espacios extra o que la mÃ¡quina estÃ© en un servidor diferente.

## 6.

MÃ¡quina 1: Meow (Tier 0 --- Starting Point)

### Servicio identificado

```bash
mkdir meow && cd meow && mkdir recon nmap -sV -Pn -v -oA recon/meow IP_OBJETIVO
```

Puerto 23 abierto â†’ **Telnet**.

### ResoluciÃ³n

Telnet es un protocolo de administraciÃ³n remota antiguo que transmite todo en **texto plano** (incluyendo contraseÃ±as).

En esta mÃ¡quina, el usuario `root` no tiene contraseÃ±a asignada (mala configuraciÃ³n).

telnet IP_OBJETIVO

# Login: root

# Password: (vacÃ­o — solo Enter)

Una vez dentro:

id # â†’ root ls # â†’ flag.txt cat flag.txt

> [!important] **LecciÃ³n clave:** siempre probar `root`, `admin`, `administrator` con contraseÃ±a vacÃ­a antes de lanzar cualquier herramienta de fuerza bruta.

La mala configuraciÃ³n (cuenta sin contraseÃ±a) es mucho mÃ¡s frecuente de lo que parece en entornos reales.

**Preguntas del modo guiado respondidas en clase:** - VM = Virtual Machine - Herramienta para lanzar comandos = Terminal (o consola, intÃ©rprete) - VPN en HTB = OpenVPN - Prueba de conectividad ICMP = ping - Herramienta para encontrar puertos abiertos = Nmap - Servicio en puerto 23 = Telnet - Telnet = protocolo antiguo de administraciÃ³n remota en texto claro - Se sustituye por SSH

## 7.

MÃ¡quina 2: Fawn (Tier 0 --- Starting Point)

### Servicio identificado

```bash
mkdir fawn && cd fawn && mkdir recon nmap -sV -Pn -v -oA recon/fawn IP_OBJETIVO
```

Puerto 21 abierto â†’ **FTP** (vsftpd 3.0.3).

### TeorÃ­a de FTP repasada

- FTP (*File Transfer Protocol*) transmite datos y credenciales en **texto claro**.
- VersiÃ³n segura con TLS: **FTPS**.
- VersiÃ³n segura tunnelizada por SSH: **SFTP**.
- El acceso anÃ³nimo usa siempre el usuario `anonymous` (sin contraseÃ±a o con cualquier texto).
- Nmap con `-sC` detecta automÃ¡ticamente si el FTP permite login anÃ³nimo.

### ResoluciÃ³n

ftp IP_OBJETIVO

# Name: anonymous

# Password: (vacÃ­o)

# Login successful â†’ sesiÃ³n FTP anÃ³nima abierta

Dentro del FTP:

```bash
ls # Listar ficheros get flag.txt # Descargar el fichero mget * # Descargar todos los ficheros (multiple get)
```

Salir del FTP con `exit` o `quit`, luego:

```bash
cat flag.txt # Ver la flag descargada
```

**Diferencia entre** `get` **y** `mget`**:** - `get nombre_fichero` â†’ descarga un fichero concreto. - `mget *` â†’ descarga mÃºltiples ficheros (equivalente a `get *`).

**Preguntas del modo guiado respondidas:** - FTP = File Transfer Protocol - Puerto 21 = FTP - FTP no cifra = correcto, texto claro - Protocolo seguro similar = FTPS (extensiÃ³n con TLS) - Sistema operativo del objetivo = Unix (identificable por TTL \~64 o por el output de Nmap) - Comando menÃº de ayuda en FTP = `?` o `-h` - VersiÃ³n del servicio = vsftpd 3.0.3 (obtenida con `-sV`) - Usuario para acceso anÃ³nimo = `anonymous` - CÃ³digo de respuesta login exitoso = 230 - Comando para descargar fichero = `get`

## 8.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
-------------------------------------------- ---------------------------------------------------------------------------------------------------------------
 *JadeVox / HaddeVox / Hubdebox / Hablebox* **Hack The Box (HTB)** -- plataforma de prÃ¡ctica de hacking
 *Starting Point / Start plugin* **Starting Point** -- secciÃ³n de HTB con mÃ¡quinas para principiantes
 *Puntbox / pan box / phone box* **PwnBox** -- mÃ¡quina Parrot OS en la nube de HTB con tiempo limitado
 *Toon Zero / tun cero* **tun0** -- adaptador de red VPN que se crea al conectarse a HTB
 *Open UPN / Open VPN* **OpenVPN** -- software de VPN usado para conectarse a la red de HTB
 *iCconfig / i config / confirm* `ifconfig` -- comando Linux para ver interfaces de red e IPs
 *EMAD / animab / En el map* **Nmap** -- escÃ¡ner de puertos y servicios
 *Jatriz / Halftrix / Hatrix* **HackTricks** (book.hacktricks.xyz) -- referencia metodolÃ³gica por protocolo
 *USFTPD / vsftpd* **vsftpd** (*Very Secure FTP Daemon*) -- servidor FTP en Linux
 *CTPS / Tonerizarlos* **FTPS** (*FTP Secure*) -- FTP con capa TLS
 *actualizar por SCH / SFTP* **SFTP** (*SSH File Transfer Protocol*) -- FTP tunnelizado por SSH
 *MGate / mget* `mget` (*multiple get*) -- descarga mÃºltiples ficheros en FTP
 *tier 0 1 2* **Tier 0/1/2** -- niveles de dificultad de Starting Point (0 = Very Easy)
 *Pro labs / Prolabs* **Pro Labs** -- laboratorios de Active Directory avanzados de HTB (suscripciÃ³n aparte)
 *flash / flac / flag* **Flag** -- archivo de texto con cÃ³digo Ãºnico que prueba que se ha comprometido la mÃ¡quina
 *Earlugs / Sherlocks* **Sherlocks** -- retos defensivos de HTB (Blue Team, forense)
 *Fortress / fortres* **Fortress** -- laboratorios creados por empresas reales (AWS, Synack, Falabella)
 *MÃ¡quinas activas / retire* **Active / Retired machines** -- mÃ¡quinas activas (gratuitas, rotan) vs.Â retiradas (requieren suscripciÃ³n VIP)
 *CPTS / CPT s* **CPTS** (*Certified Penetration Testing Specialist*) -- certificaciÃ³n de HTB orientada a Active Directory
 *Firecilla* **FileZilla** -- cliente FTP grÃ¡fico (el profesor recomienda usar terminal en su lugar)

*Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.*

â†’

â†’

â†’

â†’
â†’

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Maquinas/Hack The Box- Starting Point — Tier 0.md|Hack The Box- Starting Point — Tier 0]— Hack The Box, SSH, Telnet
- [[resumen_master_clase20.md|resumen_master_clase20]— Hack The Box, SSH, Telnet
- [[../MODULO1/resumen_master_clase7.md|resumen_master_clase7]— Hack The Box, Kali Linux, Redes
- [[resumen_master_clase19.md|resumen_master_clase19]— Kali Linux, OSINT, SSH
- [[../MODULO1/resumen_master_clase1.md|resumen_master_clase1]— Hack The Box, Kali Linux, Redes
- [[../../transcripciones/Junio/19.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking.md|19.06.2026 Mr. Robot Explotación Web Completa File Upload, Reverse Shell y SUID Hijacking]— Hack The Box, Kali Linux, SSH

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]
- [[comandos/Telnet|Telnet]]

> #blue-team #certificaciones #empleabilidad #forense #hack-the-box #hydra #ia #kali #linux #metasploitable #nmap #osint #pentest #pivoting #redes #ssh #telnet #windows
