> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 6**
> **Módulo:** MODULO1
> **Tema:** Clase 6
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 6. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy

## 1. Apertura: ingeniería social en vivo -- el timo del CEO

Carlos abre la clase con un caso real en directo que ilustra perfectamente la fase de OSINT e ingeniería social:

**El ataque original:** un grupo de estafadores monitoriza LinkedIn para detectar nuevos empleados de empresas objetivo. Usando herramientas OSINT (Apollo.io, LinkedIn scraping) deducen el correo y/o teléfono del recién incorporado siguiendo el patrón de la empresa (inicial+apellido@empresa.com). Les envían un correo o WhatsApp suplantando al CEO solicitando la compra de tarjetas de regalo de Apple con el pretexto de un regalo para empleados. Las tarjetas de regalo se venden después en mercados como G2A a precio reducido (lavado de dinero digital).

**La contramedida usada en clase:** 1. Responder al atacante con entusiasmo exagerado para ganar su confianza. 2. Indicar que "política de empresa" prohíbe adjuntos por seguridad, forzando a que pida el enlace de otra forma. 3. Generar con **IPLogger** una URL trampa disfrazada de archivo de tarjetas Apple (mapper.info/tarjetas/apple.zip). 4. Enviar el enlace trampa. Al hacer clic, se captura la IP real del atacante (antes de que activase su VPN). 5. Verificar con **ipinfo.io** si la IP es residencial (real) o de hosting/VPN.

**Resultado:** se capturó la IP real del atacante, se identificó que tenía un servidor cloud (Nextcloud) usado para centralizar las operaciones, y se documentó el recorrido de VPN (casa → EE.UU. × 5 → Reino Unido → Japón → Alemania → Letonia) activado 6 minutos después de hacer clic, cuando se dieron cuenta de su error. La IP y los datos fueron reportados a la Policía Nacional.

**Herramientas clave mencionadas:** - **IPLogger / IP Tracker**: genera URLs trampa que registran la IP de quien hace clic. - **ipinfo.io**: clasifica una IP como Residencial, VPN, Proxy, TOR, Hosting o Residential Proxy. - **Apollo.io**: herramienta de marketing/OSINT para obtener emails y teléfonos corporativos a partir de LinkedIn.

## 2. Fundamentos de redes: qué es una red y la importancia para el hacker

Una **red** es un conjunto de dos o más dispositivos que intercambian información y reciben respuesta. Sin respuesta, no hay comunicación --- y sin comunicación, no hay red.

**La regla más importante para un atacante:** solo se puede interceptar o atacar lo que está en la **misma red**. Si el atacante está en una red diferente, es físicamente imposible llegar al objetivo sin saltar de red en red.

Ejemplo del hotel: si el atacante está en la misma subred Wi-Fi que la víctima, puede lanzar un sniffer y capturar todo el tráfico. Si la víctima está en el 5G y el atacante en el Wi-Fi, son redes distintas y no hay comunicación posible entre ellos.

**Punto de intercepción:** la comunicación puede escucharse antes del cifrado (texto claro legible) o después del cifrado (texto incomprensible). Como atacante, la forma más eficiente no es interceptar el canal (obtendrías paquetes cifrados inútiles) sino comprometer los **endpoints** (origen o destino) donde la información aún está en claro.

## 3. Cómo funciona Internet físicamente

Internet es, literalmente, **cables gordos conectando otros cables gordos**, desde el cable de fibra óptica que llega a cada piso hasta los cables submarinos que cruzan océanos.

- **Último kilómetro:** cada edificio se conecta mediante cable (cobre o fibra) a una caja de distribución del barrio, que se conecta a otra más grande del distrito, que llega al ISP.
- **ISP (Proveedor de Servicios de Internet):** punto central donde convergen todas las comunicaciones y se enrutan hacia su destino.
- **Cable submarino:** conecta continentes. Su ubicación exacta es secreta; existen tratados internacionales para protegerlos. Si se daña un cable secundario, puede dejar sin Internet a toda una ciudad. Si se daña el principal, se acaba el LOL.
- **Evolución del medio físico:** cobre trenzado (DSL) → fibra óptica (pulsos de luz = 1, ausencia = 0, binario) → satélite (5G, Starlink).

**Cómo funciona una petición a YouTube:** mi dispositivo (WiFi) → router → ISP → servidor DNS (puede estar en Helsinki) → balanceadores de carga de YouTube → switches → servidor concreto (mirror) → respuesta al revés. Todo esto ocurre en milisegundos y puede verse con el comando **traceroute**.

## 4. El sistema DNS

Los **servidores DNS** (*Domain Name System*) son la "guía telefónica de Internet": tablas de correlación que relacionan nombres de dominio con IPs.

- Cuando escribimos youtube.com, nuestro router lo envía a un servidor DNS que responde con la IP real (ej. 137.128.3.52).
- Los servidores DNS están distribuidos por todo el mundo y sincronizados entre sí.
- Cuando creamos un dominio nuevo, la propagación puede tardar hasta **48 horas** porque el nuevo registro debe sincronizarse con todos los servidores DNS del mundo.
- Se puede verificar si un dominio ya se ha propagado en distintos servidores con herramientas específicas.

**DNS en ciberseguridad:** - nslookup dominio.com --- resuelve un dominio a su IP. - whois dominio.com --- información del registrante del dominio. - Los subdominios son registros A independientes que apuntan a IPs distintas. - Detectar mal configurados o expuestos es una técnica de enumeración fundamental.

## 5. Protocolos de red: TCP vs. UDP

Todo el tráfico de Internet usa uno de estos dos grandes protocolos de la **capa de transporte**:

| Característica | TCP | UDP |
|---|---|---|
| Capa OSI | Transporte (capa 4) | Transporte (capa 4) Entorno principal | Empresas (IT) | Industria (OT), gaming, streaming Autenticación previa | Sí (**3-way handshake**) | No Fiabilidad | Alta (verifica entrega) | Baja (envío sin confirmación) Velocidad | Más lento | Más rápido Subprotocolos | HTTP, HTTPS, FTP, SMB, DNS... | Modbus, SCADA, CAN Bus... Uso en auditorías | El 99% de las veces | CTFs con puertos UDP; entornos OT/industrial |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**El 3-way handshake de TCP** (apretón de manos): 1. Cliente → Servidor: SYN (seq=0) --- "¿nos sincronizamos?" 2. Servidor → Cliente: SYN-ACK (seq=1, ack=0) --- "sí, de acuerdo" 3. Cliente → Servidor: ACK (ack=1) --- "confirmado, hablamos"

Solo tras este intercambio comienza la transmisión de datos. En UDP no existe: el emisor lanza el paquete y quien lo recibe, lo recibe.

**Alerta en SOC/SIEM:** detectar tráfico UDP inesperado en una red empresarial IT es señal de anomalía. En CTF puede haber puertos abiertos solo en UDP.

## 6. Puertos y servicios: la arquitectura de un servidor

Un servidor es como un edificio con **puertas numeradas**. Cada puerta es un **puerto**. Detrás de cada puerta corre un **servicio** (programa).

**Regla fundamental:** en un puerto solo puede correr un servicio a la vez. Se puede tener la web en el 80 y el FTP en el 81, pero no dos servicios en el mismo puerto.

Puertos más importantes para auditorías:

| Puerto | Protocolo/Servicio | Importancia ofensiva |
|---|---|---|
| 21 | FTP | Transferencia de ficheros, a veces con credenciales en claro 22 | SSH | Acceso remoto seguro; objetivo de fuerza bruta 80 | HTTP | Web sin cifrado; Man-in-the-Middle trivial 443 | HTTPS | Web cifrada 445 | SMB/Samba | Compartición de recursos; EternalBlue 3389 | RDP | Escritorio remoto Windows; BlueKeep, fuerza bruta 8088 | HP Data Protector | Versiones antiguas tienen RCE crítica |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Lo vulnerable es el servicio, no el servidor:** un Windows Server 2008 R2 sin el servicio SMB expuesto no es vulnerable a EternalBlue. El servicio es lo que define si existe la vulnerabilidad.

**Demostración en Shodan:** el profesor busca en tiempo real servidores con Windows Server 2008/2007 SP1 y HP Data Protector v8.x para mostrar cómo hay **millones** de servidores reales todavía expuestos y vulnerables a exploits de 2017.

## 7. Estructura de una dirección IP y subnetting

### Anatomía de una IPv4

Una IP tiene **4 octetos** separados por puntos. Cada octeto es un número binario de 8 bits.

Los **pesos binarios** de cada bit (de derecha a izquierda): 2⁰=1, 2¹=2, 2²=4, 2³=8, 2⁴=16, 2⁵=32, 2⁶=64, 2⁷=128.

El **máximo** valor de un octeto: 128+64+32+16+8+4+2+1 = **255** (todos los bits a 1). El **mínimo** valor asignable: **1** (el 0 está reservado como nombre de red).

### Notación CIDR y subnetting

La barra tras la IP (ej. /24) indica cuántos **bits son comunes** a todos los hosts de esa red (bits de red). Los bits restantes son para identificar hosts individuales.

| CIDR | Bits de red | Hosts disponibles | Uso típico |
|---|---|---|---|
| /8 | 8 | 255×255×255 ≈ 16 millones | Grandes corporaciones /16 | 16 | 255×255 = **65.025** | Redes empresariales grandes /24 | 24 | **254** (253 útiles) | Redes empresariales estándar /32 | 32 | 1 solo host | Rutas específicas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Regla práctica:** en auditorías internas se trabaja casi siempre con /24 (254 IPs) o /16 (65.025 IPs). Una red /16 es suficiente para cualquier empresa --- 64.000 IPs para servidores y empleados es más que suficiente para cualquier organización normal.

**Máscaras de red:** - /24 → máscara 255.255.255.0 - /16 → máscara 255.255.0.0 - /8 → máscara 255.0.0.0 - /21 → máscara 255.255.248.0 (raro, desperdicia IPs, evitar)

**Truco para Nmap en auditorías:** si el cliente especifica el alcance como 10.10.7.0/24, solo se auditan esas 254 IPs. No se amplía el alcance sin autorización.

### IPv6: por qué existe y su uso en bypass de firewall

IPv6 existe porque las IPv4 (4.300 millones de direcciones) se están agotando. Usa **6 grupos de 4 dígitos hexadecimales** (base 16, de 0 a F), separados por dos puntos.

Valor práctico para el hacker hoy: **bypass de firewall**. Si un servidor tiene IPv4 e IPv6, y el firewall solo monitoriza la IPv4, el atacante puede enviar los paquetes por la IPv6 y pasar desapercibido.

## 8. Conceptos y términos clave corregidos

| Término en la transcripción | Corrección / Aclaración |
|---|---|
| IPMapper / iplogger | **IPLogger** -- servicio que genera URLs trampa para capturar IPs de quien hace clic ipinfo / IP info | **ipinfo.io** -- servicio para clasificar una IP (Residencial, VPN, Hosting, TOR...) polo.io / Apollo | **Apollo.io** -- plataforma de OSINT/marketing para extraer contactos corporativos de LinkedIn G2A | **G2A** -- marketplace de claves de videojuegos y tarjetas de regalo (frecuentemente usadas para monetizar estafas) Nextcloud / on cloud | **Nextcloud** -- plataforma cloud open source para compartir ficheros (detectada en el servidor del estafador) sniper de red | **Sniffer de red** -- herramienta que captura paquetes de red (ej. Wireshark) traseroutt / tracert | **Traceroute** (tracert en Windows) -- muestra los saltos de red hasta llegar al destino SSL o TLS | **SSL/TLS** -- protocolos de cifrado de comunicaciones web tree way handshake / apretón de manos | **3-way handshake** (SYN → SYN-ACK → ACK) -- proceso de establecimiento de conexión TCP barra 24 / barra 16 | **CIDR notation /24, /16** -- notación de subredes que indica los bits comunes DSL / fibra óptica | **DSL** (cable de cobre) y **fibra óptica** (pulsos de luz) -- medios físicos de transmisión IPTV / PTV | **PTV** -- operadora de telecomunicaciones usada como ejemplo de despliegue de red fofa / fofas | **FOFA** -- motor de búsqueda de activos expuestos en Internet (alternativa a Shodan/Censys) HP Data Protector | **HP Data Protector** -- software de backup con vulnerabilidades RCE críticas en versiones antiguas mirror | **Mirror (servidor espejo)** -- copia de servidor para distribuir carga (balanceo) fibra oscura | **Dark fiber** -- fibra óptica instalada pero no activa comercialmente; a veces usada por grandes empresas para redes privadas dedicadas Modbus / Scada / Cambus | **Modbus**, **SCADA**, **CAN Bus** -- protocolos UDP industriales (redes OT) OT | **OT** (*Operational Technology*) -- tecnología operacional industrial (fábricas, infraestructuras críticas) ISP | **ISP** (*Internet Service Provider*) -- proveedor de servicios de Internet Apollo.io / Polo.io | **Apollo.io** -- herramienta de enriquecimiento de datos para scraping de LinkedIn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial -- Wolf Academy.