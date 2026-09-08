# 🕵️ Anonimato, Ingeniería Social y Enumeración Web

> [!info] Ficha técnica
> **Instructor:** Carlos Gómez Pintado · **Módulo:** Ingeniería social / Enumeración web ofensiva
> **Entorno:** Kali Linux · Máquina Rockstar de HackerLabs (autorizada)

> [!tip] Cómo leer estos apuntes
> La sesión mezcla dos bloques. El bloque de **infraestructura anónima** (Monero, VPS, dominios, QRishing, IP logger) se documenta con enfoque defensivo y de atribución: entender cómo se construye para reconocerla, no para replicarla. El bloque de **laboratorio** (máquina Rockstar) sí es práctica ofensiva en entorno autorizado.

---

## ① Objetivos de la sesión

- Entender cómo el cibercrimen construye una infraestructura anónima (VPN sin logs, Monero, VPS y dominios pagados con cripto) para saber detectarla, atribuirla y protegerse.
- Aprender a hacer seguimiento de un posible estafador con un IP logger (uso defensivo/atribución).
- Conocer técnicas de ingeniería social actuales, en especial el QRishing como evolución del phishing y el smishing.
- Comprender el modelo as-a-Service del cibercrimen (SaaS / RaaS) y por qué se detiene a los operadores.
- Resolver la máquina Rockstar (HackerLabs): descubrimiento de host, enumeración web y fuzzing de parámetros hasta obtener acceso por SSH.

---

## ② Conceptos clave

| Concepto | Definición |
|----------|-----------|
| **Anonimato** | Cualidad de operar sin identidad atribuible. En la práctica se rompe por comodidad (reutilizar nick, IP o contraseñas) |
| **VPN** | Túnel cifrado hacia servidores alquilados en un CPD; actúa como proxy con IP cambiante. No garantiza anonimato si el proveedor guarda logs |
| **Tabla de enrutado** | Registro que correlaciona la IP real del usuario con la IP de VPN asignada en cada instante. Es lo que permite desanonimizar bajo orden judicial |
| **Monero (XMR)** | Criptomoneda orientada a privacidad; sus wallets no dejan trazabilidad pública |
| **VPS** | Virtual Private Server. Servidor virtual donde se aloja contenido |
| **Calentar un dominio** | Enviar correos progresivamente durante ~1 mes para subir la reputación (domain authority) |
| **Phishing / Smishing / QRishing** | Ingeniería social por web falsa / por SMS / mediante códigos QR maliciosos |
| **IP logger** | Servicio que, tras un clic, registra IP y geolocalización aproximada |
| **SaaS / RaaS** | Software-as-a-Service / Ransomware-as-a-Service: uno desarrolla/vende, otro ejecuta y asume el riesgo |

---

## ③ Anonimato: cómo se construye y cómo se rompe

> [!warning] Enfoque de la sección
> Se describe la arquitectura que usan los ciberdelincuentes para que sepas identificarla, atribuirla y protegerte. No es una guía para replicarla.

### La comodidad rompe el anonimato

> [!important] Regla mental de la clase
> Para una acción que se quiera desligar de la identidad: **cuenta nueva + IP nueva** (new account, new IP). No reutilizar alias ni patrones.

### Cómo funciona realmente una VPN

Una VPN mete tu tráfico en una red privada de servidores alquilados en un CPD y sale a Internet por ellos. Cambia tu IP de salida, pero el proveedor sigue sabiendo quién eres.

```
1. Usuario (IP real)
 ↓
2. Servidor VPN / proxy en CPD (IP de salida)
 ↓
3. Servidor destino en Internet
 ↓
4. Respuesta enrutada de vuelta usando la tabla IP real ↔ IP VPN
```

> [!warning] Por qué la mayoría de VPN no da anonimato real
> El proveedor guarda la tabla de enrutado (~5 años según la clase). Con orden judicial puede entregarla y desanonimizar al usuario. Ejemplos de VPN que colaboran: NordVPN, PureVPN, Surfshark, ProtonVPN, Sophos, Check Point.

> [!info] El caso Mullvad (según la clase)
> Se presenta Mullvad como VPN que habría rechazado múltiples solicitudes de colaboración y no es nominal (no pide registro con datos personales). La afirmación es del instructor y no está verificada.

> [!tip] Idea legal que repite el instructor
> Una VPN es una herramienta **legal**; lo que puede ser ilegal es el uso. Símil: comprar una espada es legal; atravesar a alguien con ella, no.

### La cadena de anonimización del cibercrimen

```
1. VPN sin logs / no nominal (p. ej. Mullvad)
 ↓
2. Criptomoneda no trazable (Monero / XMR)
 ↓
3. VPS pagado con Monero + acceso por clave SSH (sin usuario/contraseña)
 ↓
4. Dominio pagado con cripto en registrador que admite pago anónimo
 ↓
5. Dominio 'calentado' ~1 mes para ganar reputación
```

> [!info] Nota de estudio / seguridad
> Documentamos el concepto (por qué Monero se asocia a operaciones ilícitas) sin detalle operativo para romper trazabilidad. El objetivo es reconocer el patrón en una investigación, no reproducirlo.

### Alojamiento del sitio malicioso y calentamiento

Un phishing es, en el fondo, una web: una carpeta con ficheros relacionados, con permisos, expuesta a Internet. Por eso necesita un VPS y un dominio. El calentamiento consiste en enviar correos de forma progresiva durante ~1 mes para que el dominio gane reputación y no lo marquen como spam.

> [!info] Continuidad
> La próxima clase (Carlos Castillo) cubrirá el montaje de un servidor de phishing real con GoPhish, plantillas y captura de credenciales — desde la perspectiva de red team autorizado y concienciación.

### Tor y la 'red cebolla'

Tor enruta la conexión saltando por varios nodos (como capas de cebolla) hasta un nodo de salida que alcanza el exterior; para devolver la respuesta se recorre el camino inverso.

> [!warning] Matiz del instructor sobre nodos de salida
> Hoy una gran parte de los nodos de salida estarían controlados por autoridades, lo que reduciría el anonimato frente a los inicios de Tor. Con VPS privados baratos pagados con Monero, para muchos casos ya no compensa depender solo de Tor.

---

## ④ Ingeniería social: IP logger y QRishing

### IP logger (geolocalización tras un clic)

Un IP logger genera un enlace que, al abrirse, registra la IP del visitante y puede pedirle la ubicación. El uso que enseña el instructor es de **atribución**: darle un enlace verosímil a un estafador que te ha timado para obtener su IP y timestamp.

> [!success] Uso legítimo mostrado en clase
> El objetivo del ejercicio es **atribución de un atacante** que te ha estafado, no espiar a terceros al azar. Con una IP + timestamp, la policía puede pedir a la operadora qué persona tenía esa IP en ese momento.

> [!warning] Vector adicional mencionado (no demostrado)
> Un IP logger no se autoejecuta en una imagen, pero sí podría dispararse desde documentos con macros (formatos ofimáticos). Se menciona como vector, no se demuestra en clase.

### QRishing (la evolución de la ingeniería social)

Como el phishing por enlace y el smishing están muy 'quemados', la ingeniería social evoluciona hacia el **QRishing**: incrustar el enlace malicioso en un código QR. El diseño cuidado del QR reduce la desconfianza de la víctima.

> [!danger] Lección defensiva del QRishing
> - No escanees QR de origen desconocido (pegatinas en la calle, carteles, cartas de restaurante manipuladas).
> - Un QR llamativo y 'profesional' **NO** es garantía de confianza.
> - Desconfía de cualquier QR que lleve a un login o pida permisos de ubicación; verifica el dominio destino antes de introducir credenciales.

> [!info] Herramientas de clonado de UI mencionadas
> Para el front de un phishing se citan asistentes de IA / plataformas tipo Lovable, Emergent, etc., capaces de replicar visualmente una web a partir de su URL o capturas. Solo replican el front, en contexto autorizado.

---

## ⑤ Modelo 'as-a-Service' del cibercrimen (SaaS / RaaS)

El cibercrimen ya no lo mueven solo los técnicos:

```
1. Desarrollador: crea el ransomware / panel y lo vende (cuota fija)
 ↓
2. Broker de acceso inicial: vende credenciales / RCE de una víctima
 ↓
3. Cliente/operador: compra ambos, ejecuta el ataque y asume el riesgo
 ↓
4. El desarrollador cobra además un % del rescate
```

> [!tip] Por qué se pilla a los operadores
> Los operadores suelen tener cero conocimiento técnico y cometen fallos graves: paneles con credenciales por defecto (p. ej. cPanel admin sin contraseña), reutilización de alias, mala gestión de su propio anonimato. Por eso se detiene al operador antes que al desarrollador.

---

## ⑥ Si eres víctima de una ciberestafa

**Ciberresponsabilidad bancaria:** los bancos suelen tener un ciberseguro con ciberresponsabilidad asociada. Si aportas la denuncia policial + los movimientos bancarios sellados, el banco puede tener que reintegrar el dinero. Aplica a casos como pagos falsos de la 'DGT', reservas de piso falsas o compras fraudulentas.

> [!warning] Aviso
> Son pautas generales de la clase, no asesoramiento legal. Los procedimientos y la confidencialidad varían según el caso y la entidad; ante una estafa real, denuncia y consulta con profesionales.

---

## ⑦ Laboratorio: máquina Rockstar (HackerLabs)

### 7.1 Descubrimiento de host y sistema operativo

```bash
# Ver nuestra IP e interfaz (eth0)
ip a

# Descubrir hosts en el rango de red /24
sudo netdiscover -r 10.0.2.0/24
```

La interfaz de trabajo era eth0 con IP 10.0.2.3. Se descartan 127.0.0.1 (localhost) y las interfaces Docker. La .1 y la .2 suelen ser gateway/router de VirtualBox; se buscó un host más alto y la víctima resultó ser **10.0.2.9**.

> [!info] Repaso de redes aplicado
> Rango /24: los 3 primeros octetos son fijos y el último varía de 0 a 255. /16 fija 2 octetos, /8 fija 1, y /0 abarca todas las direcciones (equivale a 0.0.0.0 en un listener).

**ICMP y detección de SO por TTL:**

| TTL aprox. | SO probable |
|------------|-------------|
| 64 | Linux / Unix |
| 128 | Windows |
| 192 | Solaris (según la clase) |
| 254 | macOS / otros (según la clase) |

> [!info] Detalle AWS
> Amazon (AWS) no trae ICMP habilitado por defecto, para dificultar el ping sweep. Los 3 primeros dígitos de la MAC identifican al fabricante.

### 7.2 Escaneo de puertos y servicios (Nmap)

```bash
nmap -sVC --open --min-rate 1500 10.0.2.9
```

Se encontraron 2 puertos: **22 (SSH)** y **80 (HTTP)**. Con esta combinación en un CTF se ataca primero el 80: al 22 no se entra sin credenciales.

### 7.3 Enumeración web

Metodología del instructor (símil del coche): ir de más a menos. El servidor (Apache) sería el chasis; primero se comprueba si la versión tiene vulnerabilidades conocidas, y luego se baja al detalle.

```bash
# Directorios con Gobuster
gobuster dir -u http://10.0.2.9 -w /usr/share/wordlists/dirb/common.txt

# Directorios + ficheros por extensión con Feroxbuster
feroxbuster -u http://10.0.2.9 -w /usr/share/wordlists/dirb/common.txt -x php,py,txt,html
```

> [!info] Directorios vs. ficheros y códigos de estado
> Una web es una carpeta con ficheros y subcarpetas. La diferencia clave: el fichero tiene extensión (y por tanto puede ejecutar/mostrar contenido). Por eso se añade `-x` con las extensiones a probar.

Hallazgos: `index.php` y `db.php`. `db.php` devuelve 0 words (página en blanco): un PHP que se ejecuta pero no imprime nada resulta en 0 bytes.

> [!warning] Diccionarios: no confundir usos
> `rockyou` es de contraseñas (no sirve para directorios); listas tipo `directory-list` / `common.txt` son de directorios. Gobuster, Feroxbuster y Dirsearch son equivalentes.

### 7.4 Fuzzing de parámetros: descubrir el parámetro oculto

Como `index.php` reacciona pero no se ve nada útil, se busca un parámetro que cambie su comportamiento. La herramienta idónea es **x8**, pero su instalación por Docker falló.

> [!warning] x8 con Docker falló
> Instalación prevista: `git clone`, `cd x8`, `docker build -t x8 .`. Al fallar Docker, la alternativa fue compilar con Cargo (`cargo build --release`) o escribir un fuzzer propio en Python.

Comprobación manual previa con curl:

```bash
curl -X POST http://10.0.2.9/index.php --data "parametro=valor"
```

### 7.5 Los dos scripts propios: descubrir NOMBRE y descubrir VALOR

| Script | Qué incógnita resuelve | Diccionario | Analogía |
|--------|----------------------|-------------|----------|
| **x8_lite.py** | El nombre del parámetro oculto | Nombres de parámetro | Reimplementa el motor de x8 |
| **valfuzz.py** | El valor de un parámetro ya conocido | Valores (rockyou.txt) | Estilo ffuf/wfuzz con marcador FUZZ |

**`x8_lite.py`** — descubrimiento de nombres:

```bash
python3 x8_lite.py -u http://10.0.2.9/index.php -X POST \
 -w /usr/share/wordlists/dirb/common.txt --verify
```

> [!info] Cómo trabaja x8_lite por dentro
> Fases: LEARN (aprende el baseline) → BATCH (muchos parámetros a la vez) → COMPARE (diff contra baseline) → BISECT (búsqueda binaria) → CUSTOM (admin=true, debug=1...) → VERIFY (reconfirma uno a uno).

**`valfuzz.py`** — fuzzing de valores:

```bash
python3 valfuzz.py -u http://10.0.2.9/index.php -X POST \
 -d "backdoor=FUZZ" -w /usr/share/wordlists/rockyou.txt

# Afinar marcando como HIT solo si la respuesta contiene 'uid='
python3 valfuzz.py -u http://10.0.2.9/index.php -X POST \
 -d "backdoor=FUZZ" -w rockyou.txt --match-keyword "uid="
```

> [!warning] No confundir uno con otro
> **x8_lite.py** consume un diccionario de **nombres** de parámetro (la incógnita es qué parámetro existe). **valfuzz.py** usa un nombre fijo y un diccionario de **valores** (la incógnita es qué valor lo activa). Son fases consecutivas, no alternativas.

**Flujo completo del tramo:**

```
1. index.php responde pero no muestra nada útil (500)
 ↓
2. x8_lite.py → descubre el NOMBRE del parámetro: 'backdoor'
 ↓
3. valfuzz.py → fuzzea el VALOR de 'backdoor' (500 → 200)
 ↓
4. La respuesta revela usuario y contraseña
 ↓
5. Acceso por SSH con esas credenciales
```

> [!success] Resultado del tramo
> El valor 'anómalo' del parámetro `backdoor` devolvió un usuario y una contraseña válidos, con los que se logró acceso por SSH (puerto 22). Los valores concretos no se documentan por ser específicos del CTF.

---

## ⑧ Herramientas utilizadas

| Herramienta | Objetivo | Fase | Nivel | Notas |
|-------------|----------|------|-------|-------|
| netdiscover | Descubrir hosts del rango | Reconocimiento | Practicada | .1/.2 suelen ser gateway |
| ping / ICMP | Host vivo y SO por TTL | Reconocimiento | Recurrente | TTL 64→Linux, 128→Windows |
| Nmap | Puertos y versiones | Enumeración | Recurrente | Primer paso habitual |
| Gobuster | Descubrir directorios | Enum. web | Practicada | Equivalente a Dirb/Dirsearch |
| Feroxbuster | Directorios + ficheros | Enum. web | Practicada | -x para extensiones |
| curl | Peticiones POST manuales | Enum./pruebas | Practicada | Verbo con -X, cuerpo con --data |
| x8 | Fuzzing de parámetros | Enum. web | Introducida | Falló por Docker |
| x8_lite.py (propio) | Descubrir NOMBRE de parámetro | Enum. web | Practicada | Motor tipo x8 |
| valfuzz.py (propio) | Descubrir VALOR de un parámetro | Enum. web | Practicada | Estilo ffuf/wfuzz |
| SSH | Acceso remoto | Acceso inicial | Practicada | Vía de entrada final |
| IP Logger | IP + geolocalización tras clic | Ing. social / atribución | Introducida | Uso defensivo |
| GoPhish | Campañas de phishing | Ing. social | Mencionada | Se verá con Castillo |
| SmartLead (warmup) | Calentar dominios | Infraestructura | Mencionada | Sube domain authority |
| Mullvad VPN | VPN no nominal | Anonimato | Mencionada | Afirmaciones no verificadas |
| Monero (XMR) | Cripto de privacidad | Anonimato / pagos | Mencionada | Concepto; sin detalle operativo |
| Lovable / Emergent (IA) | Clonar UI de webs | Ing. social | Mencionada | Solo front; contexto autorizado |

---

## ⑨ Conexión con sesiones anteriores

- **Netdiscover, ping/TTL y Nmap** enlazan con el flujo de reconocimiento ya visto: primero descubrir el host, luego el SO, luego los servicios.
- **Gobuster y Feroxbuster** consolidan la fase de enumeración web.
- **El fuzzing de parámetros** con x8/curl amplía el concepto de fuzzing hacia los parámetros de un endpoint.
- **El repaso de redes** (/24, /16, /8, /0, 0.0.0.0) refuerza los fundamentos de subnetting.

---

## ⑩ Resumen final

La sesión tiene dos mitades. En la primera, Carlos Gómez Pintado explica cómo el cibercrimen construye anonimato (VPN sin logs, Monero, VPS y dominio pagados con cripto, calentamiento de dominio, Tor) y cómo se rompe ese anonimato por comodidad o por la tabla de enrutado del proveedor; introduce el IP logger para atribución, el QRishing como evolución de la ingeniería social, y el modelo as-a-Service (RaaS).

En la segunda mitad se resuelve la máquina Rockstar de HackerLabs: descubrimiento con netdiscover, host vivo por ping (Linux por TTL), Nmap revela 22 y 80, enumeración web con Gobuster/Feroxbuster (`index.php` y `db.php`), y fuzzing de parámetros en dos fases: `x8_lite.py` descubre el nombre del parámetro oculto (`backdoor`) y `valfuzz.py` descubre el valor que lo activa (respuesta 500 → 200), revelando credenciales para entrar por SSH.

---

## ⑪ Checklist de repaso

- [ ] Explicar qué es la tabla de enrutado de una VPN y por qué rompe el anonimato
- [ ] Recitar la cadena de anonimización del cibercrimen y para qué sirve cada pieza
- [ ] Diferenciar phishing, smishing y QRishing, y dar la lección defensiva de cada uno
- [ ] Explicar el modelo RaaS y por qué se detiene antes al operador que al desarrollador
- [ ] Descubrir el host víctima con netdiscover e inferir el SO por TTL
- [ ] Enumerar la web con Gobuster/Feroxbuster e interpretar los códigos de estado
- [ ] Explicar el fuzzing de parámetros (nombre y valor) y por qué el cambio 500→200 es la señal
- [ ] Distinguir cuándo usar x8_lite.py (descubre el NOMBRE) y cuándo valfuzz.py (descubre el VALOR)
- [ ] Describir las fases internas de x8_lite.py (learn, batch, bisect, verify) y por qué van por lotes
- [ ] Reproducir el comando `curl -X POST --data` para probar un parámetro manualmente

---

## ⑫ Próxima sesión (anticipo)

> [!warning] Pendiente
> Este contenido aún no se ha impartido; se anticipa a partir de lo dicho al final de la clase:
> - Escalada de privilegios de Rockstar mediante cron (tarea programada) y demás vectores.
> - Repaso de lo hecho hasta ahora antes de continuar.
> - Nueva máquina de HackerLabs (mencionada como 'Banco').
> - Inicio del bloque de phishing con GoPhish a cargo de Carlos Castillo.

---

## ⑬ Notas de fidelidad al material

- El instructor de esta sesión es **Carlos Gómez Pintado**. La clase de phishing con GoPhish la impartirá **Carlos Castillo** en la sesión siguiente.
- El bloque de infraestructura anónima se documenta con enfoque defensivo/atribución, sin detalle operativo para replicar la técnica.
- Las afirmaciones sobre Mullvad (solicitudes rechazadas) y sobre los TTL de Solaris/macOS se atribuyen a la clase y no se verifican de forma independiente.
- Los valores concretos de credenciales de Rockstar no se transcriben por ser específicos del CTF; se documenta el método.
- La fecha exacta de la sesión no aparece en el material.

---

## ⑭ Actualización del registro de herramientas

| Herramienta | Cambio | Nivel resultante |
|-------------|--------|-----------------|
| x8 | Alta (fuzzing de parámetros) | Introducida |
| x8_lite.py (propio) | Alta (descubrimiento de NOMBRES) | Practicada |
| valfuzz.py (propio) | Alta (fuzzing de VALORES) | Practicada |
| curl | Uso explícito con -X POST --data | Practicada |
| Feroxbuster | Uso con -x para ficheros por extensión | Practicada |
| Gobuster | Uso dir con diccionario | Practicada |
| netdiscover | Descubrimiento con -r sobre /24 | Practicada |
| SSH | Acceso con credenciales / clave id_rsa | Practicada |
| IP Logger | Alta (atribución de estafadores) | Introducida |
| GoPhish | Alta (se profundizará con Castillo) | Mencionada |
| SmartLead (warmup) | Alta (calentamiento de dominios) | Mencionada |
| Mullvad VPN | Alta (VPN no nominal) | Mencionada |
| Monero (XMR) | Alta (cripto de privacidad) | Mencionada |
| Tor | Alta/repaso (red cebolla) | Mencionada |
| Lovable / Emergent (IA) | Alta (clonado de UI) | Mencionada |


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Andres/10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor.md|10.07.2026 Repaso y Explotación Avanzada Máquinas Nike y Castor]] — DirSearch, GoBuster, Linux
- [[Maquinas/Explotación de Máquinas Locales I.md|Explotación de Máquinas Locales I]] — DirSearch, GoBuster, Linux
- [[Apuntes_Sesion27_XXE_LFI_Nike.md|Apuntes_Sesion27_XXE_LFI_Nike]] — DirSearch, GoBuster, Linux
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Máquinas Locales I — Oopsie y Archetype.md|Explotación de Máquinas Locales I — Oopsie y Archetype]] — DirSearch, GoBuster, Linux
- [[../Apuntes/02 - Sistemas Operativos/Consolas - Bash y PowerShell.md|Consolas - Bash y PowerShell]] — Kali Linux, Linux, Windows
- [[Auditoria web.md|Auditoria web]] — DirSearch, GoBuster, Linux

### 🛠️ Herramientas

- [[comandos/DirSearch|DirSearch]]
- [[comandos/Feroxbuster|Feroxbuster]]
- [[comandos/FFUF|FFUF]]
- [[comandos/GoBuster|GoBuster]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

> #dirsearch #escalada-privilegios #feroxbuster #ffuf #gobuster #kali #linux #nmap #pentest #redes #ssh #windows
