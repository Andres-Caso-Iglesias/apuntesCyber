> [!info] Ficha tÃ©cnica
> **MÃ¡ster de Ciberseguridad e Inteligencia Artificial** Â· **Clase 12**
> **MÃ³dulo:** MODULO2
> **Tema:** Clase 12
> **Fuente:** Apuntes Joselu Â· Evolve Academy

> [!tip] CÃ³mo leer estos apuntes
> Resumen estructurado de la clase 12. Contenido optimizado para estudio activo y repaso rÃ¡pido antes de exÃ¡menes.

---

---

--
Esta sesiÃ³n abre el mÃ³dulo de redes y la imparte Carlos GÃ³mez.

Aunque el tÃ­tulo anunciado era Wireshark, la clase toma su propio rumbo natural: antes de poder interpretar trÃ¡fico de red con ninguna herramienta, hay que entender quÃ© es una red, cÃ³mo viajan los datos, quÃ© son los protocolos, los puertos y los servicios, y cÃ³mo se construyen las direcciones IP desde sus fundamentos binarios.

La clase arranca ademÃ¡s con un caso real de ingenierÃ­a social activa que ilustra, antes de entrar en teorÃ­a, por quÃ© to do esto importa en un contexto ofensivo real.

### Caso real: ingenierÃ­a social sobre ingenierÃ­a social Antes de entrar en teorÃ­a, GÃ³mez comparte un caso en curso con un cliente.

Un grupo de estafadores monitoriza LinkedIn para detectar empleados nuevos, deduc e su email corporativo a partir del patrÃ³n de la empresa (inicial mÃ¡s apellido arroba dominio), y envÃ­a una suplantaciÃ³n del CEO pidiendo que compren tarjetas regalo de Apple y envÃ­en los cÃ³digos por foto.

El negocio es sencillo: los cÃ³digos de tarjetas re galo son dinero lÃ­quido revendible en mercados como G2A sin trazabilidad.

La respuesta del equipo es hacer ingenierÃ­a social sobre los propios atacantes: responden con entusiasmo exagerado, negocian el nÃºmero de tarjetas, y cuando llega el momento de envia r los cÃ³digos, argumentan que la polÃ­tica de empresa prohÃ­be adjuntos por email y ofrecen enviarlos por WhatsApp.

El atacante, para no revelar su nÃºmero real, pide que todo vaya por correo.

En ese momento le envÃ­an un enlace acortado generado con IPLogger , que redirige a la web de Apple pero registra la IP de quien lo abre.

### El resultado: en los primeros seis minutos el atacante abriÃ³ el enlace desde su IP real, dejando geolocalizaciÃ³n aproximada y datos del navegador.

Al detectar que algo no cuadraba, empez Ã³ a saltar entre nodos de VPN de varios paÃ­ses en segundos.

Para distinguir si una IP es VPN o residencial se usa IPInfo.io , que clasifica la IP como hosting, VPN, proxy, TOR o residencial.

Una IP residencia l con Microsoft Edge casi garantiza que no hay VPN activa.
> [!important] - La idea clave: el OSINT y la ingenierÃ­a social no son solo herramientas de ataque, son
tambiÃ©n herramientas de investigaciÃ³n y contraataque.

Los atacantes que no protegen su IP desde el primer clic se delatan solos

QuÃ© es una red y cuÃ¡ndo existe Una red existe cuando hay intercambio de informaciÃ³n entre dos o mÃ¡s dispositivos y al menos uno de ellos responde.

La respuesta es el requisito mÃ­nimo: sin respuesta hay envÃ­o, pero no comunicaciÃ³n, y por tanto no hay red.

La definiciÃ³n es mÃ¡s amplia de lo que parece.

No hace falta WiFi, no hace falta Internet, no hace falta ni siquiera un cable de red en sentido estricto:
- Dos ordenadores conectados por cable RJ45: red
- Un mÃ³vil conectado por USB a un ordena dor: red
- Un pendrive conectado a un ordenador: red, porque hay intercambio de informaciÃ³n
- Un ratÃ³n inalÃ¡mbrico conectado al ordenador: red, porque el handshake inicial y las
coordenadas continuas son intercambio de informaciÃ³n Internet es simplemente la re d de redes mÃ¡s grande que existe, fÃ­sicamente sustentada por cables de cobre y fibra Ã³ptica que conectan edificios, barrios, ciudades y continentes, incluyendo cables submarinos que cruzan ocÃ©anos.

Los ISP son el punto de convergencia donde llegan todas es as fibras y se enrutan hacia su destino.
- La metÃ¡fora Ãºtil: si tiras del cable de tu casa con suficiente fuerza, acabas conectado con
alguien en China.

Internet es literalmente eso, una red fÃ­sica de cables cada vez mÃ¡s gordos que se agregan hasta llegar a un punto central

Protocolos: TCP y UDP Un protocolo es el idioma que usan dos dispositivos para comunicarse.

Los dos grandes protocolos de la capa de transporte son TCP y UDP , y elegir uno u otro tiene consecuencias directas en seguridad y rendimiento.

TCP exige un apretÃ³n de manos antes de enviar nada.

Este proceso se llama three -way handshake : Cliente â†’ Servidor: SYN (quiero hablar) Servidor â†’ Cliente: SYN + ACK (de acuerdo) Cliente â†’ Servidor: ACK (perfecto, hablamos) Solo despuÃ©s de este intercambio comienza la transferencia de datos.

Esto garantiza que ambos extremos estÃ¡n disponibles y listos.

Sobre TCP corren todos los protocolos que conocemos: HTTP , HTTPS, FTP, SMB, DNS en consultas normales, etcÃ©tera.

UDP no hace handshake.

Lanza paquetes y el que estÃ© atento los recoge.

Es mÃ¡s rÃ¡pido y se usa en contextos donde la velocidad prima sobre la fiabilidad: streaming de vÃ­deo, juegos online, comunicaciones industriales ( Modbus , SCADA ), y tambiÃ©n en la retransmis iÃ³n de la propia clase.

Ver UDP en trÃ¡fico de red de una empresa estÃ¡ndar es una seÃ±al de alerta que merece investigaciÃ³n.

Puertos y servicios: la estructura de un servidor Un servidor es una mÃ¡quina con puertas numeradas.

Cada puerta es un puerto , y en c ada puerto corre exactamente un servicio .

La regla es absoluta: un puerto, un servicio.

Los puertos van del 0 al 65.535 y existen en dos dimensiones: externos (expuestos a Internet o a la red) e internos (solo accesibles desde dentro del propio servidor).

Un servidor puede tener MySQL en el puerto 3306 externo y MariaDB en el puerto 3306 interno sin conflicto, porque son espacios completamente separados.

Lo que es vulnerable nunca es el puerto ni el protocolo en sÃ­, sino una versiÃ³n concreta de un servicio .

El ejemplo de clase es Drupal: Drupal 7 era vulnerable a Drupalgeddon (RCE con criticidad 9.9), sacaron Drupal 8 para corregirlo, y a los dos dÃ­as de lanzarlo descubrieron Drupalgeddon 2, todavÃ­a mÃ¡s crÃ­tico.

Una actualizaciÃ³n que introducÃ­a una vulnerabi lidad peor que la que corregÃ­a.

Eso es lo que le costÃ³ a Drupal la carrera contra WordPress.

La lecciÃ³n para auditorÃ­as: no se busca si FTP es vulnerable, se busca si la versiÃ³n concreta de FTP que tiene ese servidor tiene un CVE asociado.
> [!important] - La idea clave: cada puerto expuesto a Internet es una puerta de entrada potencial.

Comprometer un servicio externo significa cruzar de la IP externa a la red interna, y desde ahÃ­ el movimiento lateral es la siguiente fase

DNS: el sistema de nombres de Internet Las mÃ¡quin as no entienden nombres de dominio, solo IPs.

El sistema DNS (Domain Name Server) es la infraestructura que traduce unos en otros.

FÃ­sicamente son servidores distribuidos por todo el mundo, sincronizados entre sÃ­, que mantienen tablas de correlaciÃ³n entre nombres de dominio e IPs.

Cuando escribimos youtube.com en el navegador, la peticiÃ³n va al router, el router consulta al servidor DNS mÃ¡s cercano, el DNS devuelve la IP correspondiente, y el router la usa para enrutar la peticiÃ³n hacia el destino real.

Por eso los cambios de DNS pueden tardar hasta 48 horas en propagarse: cada servidor DNS del planeta tiene que actualizar su tabla.
```bash

# Herramientas para consultar DNS

```

nslookup youtube.com # Traduce nombre a IP ping youtube.com # TambiÃ©n resuelve y muestra la IP whois youtube.com # Informaci Ã³n del registrador del dominio

Direccionamiento IP: binario, octetos y mÃ¡scaras de red Una direcciÃ³n IPv4 tiene cuatro octetos separados por puntos.

Cada octeto puede valer entre 0 y 255, porque son ocho bits en binario y la suma de las potencias de dos d el 0 al 7 es exactamente 255: 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255 Dos IPs estÃ¡n reservadas en cada red y no se asignan a equipos: la terminada en .0 (identificador de red) y la terminada en .255 (direcciÃ³n de broadcast).

La notaciÃ³n CIDR (barra seguid a de un nÃºmero) indica cuÃ¡ntos bits son comunes a todos los dispositivos de esa red.

En una red 10.10.7.0/24, los primeros 24 bits no cambian y el Ãºltimo octeto es el espacio de host: 253 IPs utilizables.

En una /16 el espacio de host son los Ãºltimos dos o ctetos, lo que da mÃ¡s de 64.000 IPs posibles.

La mÃ¡scara de red es la representaciÃ³n en decimal de esos bits fijos puestos todos a 1.

Una /24 tiene mÃ¡scara 255.255.255.0.

Una /16 tiene 255.255.0.0.

IPv6 existe porque el espacio de IPv4 es finito.

Usa seis grupos de cuatro dÃ­gitos hexadecimales separados por dos puntos.

El hexadecimal tiene 16 valores posibles (del 0 al F), lo que equivale a cuatro bits, manteniendo la compatibilidad con la infraestructura binaria subyacente.

En la prÃ¡ctica ofensiva, IPv6 im porta porque muchos firewalls monitorizan IPv4 pero ignoran IPv6: si un host tiene ambas y el firewall solo filtra una, se puede usar la otra como canal de bypass.

Broadcast y protocolo ARP

La direcciÃ³n .255 de cada red es la de broadcast : enviar a esa di recciÃ³n manda el paquete a todos los dispositivos de la red simultÃ¡neamente.

Se usa cuando no se sabe exactamente a quiÃ©n va dirigida una peticiÃ³n.

Sobre broadcast funciona ARP (Address Resolution Protocol), el protocolo que permite a los dispositivos descubrir quiÃ©n es quiÃ©n dentro de una red local.

ARP pregunta a todos los vecinos, recibe respuestas y construye una tabla interna de correspondencias entre IPs y direcciones MAC fÃ­sicas.

ARP tiene dos implicaciones directas en auditorÃ­a: la herramienta NetDiscover usa ARP para descubrir hosts en una red local, y AWS bloquea ARP deliberadamente para que los clientes no puedan enumerar los servidores vecinos en la misma infraestruct ura.

El laboratorio del examen final del mÃ¡ster estÃ¡ hosteado en AWS, por lo que NetDiscover no encontrarÃ¡ nada: hay que usar otros mÃ©todos de descubrimiento.

Los ataques de ARP flooding o MAC flooding saturan las tablas de los switches hasta desbordamient o.

Cuando un switch no puede mantener su tabla, abre todas las puertas para no interrumpir las comunicaciones, permitiendo que el trÃ¡fico fluya hacia todos los puertos y facilitando la captura con un sniffer.

RecapitulaciÃ³n integrada Al salir de esta sesi Ã³n entendemos que una red es cualquier intercambio de informaciÃ³n entre dispositivos, que TCP garantiza la conexiÃ³n mediante handshake mientras UDP prioriza velocidad sin verificaciÃ³n, y que lo que se compromete en un ataque nunca es abstractamente "un ser vidor" sino una versiÃ³n concreta de un servicio corriendo en un puerto especÃ­fico.

Sabemos construir y leer una IP en binario, entender quÃ© significa una mÃ¡scara de red, y por quÃ© IPv6 puede ser un vector de bypass ignorado.

La prÃ³xima sesiÃ³n entrarÃ¡ en el modelo OSI y en Wireshark, donde todo lo visto hoy se volverÃ¡ visible en tiempo real dentro de los paquetes de red.

â†’

â†’
