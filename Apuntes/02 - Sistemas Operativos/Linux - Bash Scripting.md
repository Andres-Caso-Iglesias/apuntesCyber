

> [!info] Relacionado con
> [[Linux - Fundamentos]] · [[Consolas - Bash y PowerShell]] · [[Explotación de Servicios - Linux]]

---

## ① Estructura básica de un script

```bash
#!/bin/bash
# La primera línea es el 'shebang': indica qué intérprete usar

[[Linux#nano|nano]] mi_script.sh # crear
[[Linux#chmod|chmod]] +x mi_script.sh # dar permiso de ejecución
./mi_script.sh # ejecutar
```

> [!important] SHEBANG
> `#!/bin/bash` al inicio es **obligatorio**. Sin él, puede interpretarse con `sh` (shell básica) con diferencias de sintaxis.

> [!warning] ERRORES COMUNES (vistos en clase)
> - Escribir `*` en lugar de `#` al inicio del shebang: `*` se interpreta como comodín, no como comentario.
> - No mover el script al PATH: funciona con `./nombre` desde su carpeta, pero no es un "comando" hasta que se mueve a una ruta del PATH.
> - Ruta destino incorrecta al mover (ej. `bin` en vez de `/usr/local/bin`): usar `echo $PATH` para confirmar rutas.
> - `sudo su` innecesario: basta `sudo` delante del comando concreto.

### Comando personalizado completo

```bash
# 1. Crear con nano: primera línea #!/bin/bash
# 2. chmod +x nombre_comando
# 3. Mover al PATH: sudo mv nombre_comando /usr/local/bin/
# 4. Invocar desde cualquier parte escribiendo su nombre
```

---

## ② Variables

```bash
#!/bin/bash
nombre='Kali' # Asignar (SIN espacios alrededor del =)
ip='192.168.1.1'
echo "Hola $nombre" # Usar (con $)

# Variables especiales:
$0 # nombre del script
$1 # primer argumento
$# # número de argumentos
$? # código de retorno (0=éxito)
$$ # PID del script

# Capturar salida de un comando:
fecha=$(date)
usuarios=$([[Linux#cat|cat]] /etc/passwd | [[Linux#grep|grep]] bash | [[Linux#cut|cut]] -d: -f1)
```

> [!danger] ERROR COMÚN
> `nombre='valor'` ✅ correcto
> `nombre = 'valor'` ❌ error (espacios)

---

## ③ Entrada de usuario

```bash
#!/bin/bash
read -p 'IP objetivo: ' ip_objetivo
read -sp 'Contraseña: ' password # -s = silencioso
echo

# Argumentos desde CLI: ./script.sh 192.168.1.1 80
ip=$1
puerto=$2

if [ $# -lt 2 ]; then
 echo 'Uso: $0 <ip> <puerto>'
 exit 1
fi
```

---

## ④ Condicionales

```bash
#!/bin/bash
if [ condición ]; then
 # comandos si es verdad
elif [ otra_condición ]; then
 # comandos si la segunda es verdad
else
 # si ninguna es verdad
fi
```

### Comparaciones

| Tipo | Operadores |
|------|-----------|
| **Numéricas** | `-eq` (igual), `-ne`, `-lt` (<), `-gt` (>), `-le`, `-ge` |
| **Strings** | `=` (igual), `!=`, `-z` (vacío), `-n` (no vacío) |
| **Ficheros** | `-f` (fichero), `-d` (directorio), `-x` (ejecutable), `-r` (legible) |

### Ejemplo real

```bash
 if [[Linux#ping|ping]] -c1 -W1 $ip &>/dev/null; then
 echo "$ip está activo"
else
 echo "$ip no responde"
fi
```

---

## ⑤ Bucles

```bash
# FOR — iterar sobre lista
for ip in 192.168.1.1 192.168.1.2 192.168.1.3; do
 echo "Probando $ip"
done

# FOR con rango
for i in $(seq 1 254); do
 [[Linux#ping|ping]] -c1 -W1 192.168.1.$i &>/dev/null && echo "192.168.1.$i activo"
done

# WHILE — mientras condición
contador=1
while [ $contador -le 10 ]; do
 echo "Intento $contador"
 contador=$((contador + 1))
done

# WHILE para leer fichero
while read linea; do
 echo "Procesando: $linea"
done < lista.txt
```

> [!tip] AUTOMATIZACIÓN
> El bucle for con [[Linux#ping|ping]] es la base de un **escáner de hosts casero**. Más lento que [[Nmap]] pero didáctico.

---

## ⑥ Funciones

```bash
#!/bin/bash
mi_funcion() {
 local nombre=$1 # 'local' limita la variable a la función
 echo "Hola, $nombre!"
}

mi_funcion 'Chema'

# Función con retorno
esta_activo() {
 [[Linux#ping|ping]] -c1 -W1 $1 &>/dev/null
 return $? # 0=éxito, 1=fallo
}

if esta_activo '192.168.1.1'; then
 echo 'Host activo'
fi
```

---

## ⑦ Script completo: mini scanner de hosts

```bash
#!/bin/bash
RED=$1
ACTIVOS=()

if [ -z "$RED" ]; then
 echo "Uso: $0 <prefijo_red> (ej: 192.168.1)"
 exit 1
fi

echo "[*] Escaneando $RED.0/24..."
for i in $(seq 1 254); do
 ip="$RED.$i"
if [[Linux#ping|ping]] -c1 -W1 $ip &>/dev/null; then
 echo "[+] $ip — ACTIVO"
 ACTIVOS+=("$ip")
 fi
done

echo "[*] Hosts activos: ${#ACTIVOS[@]}"
for host in "${ACTIVOS[@]}"; do
 echo " → $host"
done
```

---

## ⑧ Limpieza de rastros

```bash
history -c && history -w # borrar historial en memoria y disco
export HISTFILE=/dev/null # deshabilitar historial esta sesión
shred -u ~/.bash_history # borrado seguro
```

> [!info] FORENSE
> Como defensor, los logs deben enviarse a un **SIEM remoto** para que el atacante no pueda borrarlos.

---

## ⑨ Inyección de comandos — donde el scripting se vuelve ataque

Los operadores de Bash son exactamente los que se explotan en **Command Injection**:

```bash
# Escenario: el servidor ejecuta
find /home/web -name "$INPUT"

# Ataque con punto y coma (si no sanitiza):
INPUT="hola.txt ; id"
# → find /home/web -name "hola.txt" ; id  → ejecuta id como el usuario web
```

| Operador | Comportamiento |
|----------|---------------|
| `\|` (pipe) | La salida del primero es la entrada del segundo |
| `;` | Ejecuta ambos **siempre** → base de la inyección |
| `&&` | El segundo solo si el primero tuvo éxito (salida 0) |
| `\|\|` | El segundo solo si el primero falló |
| `&` | Ejecuta en segundo plano |

**Defensa**: envolver la entrada en comillas dobles (`"$INPUT"`) hace que el `;` se interprete como texto literal. Mecanismo análogo a la SQL Injection: se altera el flujo introduciendo caracteres con significado propio en el lenguaje subyacente.

> [!info] LinPEAS / WinPEAS
> Scripts de enumeración automática de escalada de privilegios (autor: **Carlos Polop**). Lanzan decenas de comandos `find`, `uname` y comprobaciones de permisos, y colorean los resultados según criticidad.

---

## Checklist de repaso

- [ ] ¿Sé crear y ejecutar un script con shebang?
- [ ] ¿Distingo asignación de variables con y sin espacios?
- [ ] ¿Sé usar if/elif/else con comparaciones numéricas y de strings?
- [ ] ¿Domino los bucles for y while?
- [ ] ¿Puedo escribir una función con retorno?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../informes/Informe_Blue.md|Informe_Blue]] — Linux, Nmap, Windows
- [[../../apuntes Chema/Bash Scripting.md|Bash Scripting]] — Blue Team / SOC, Linux, Windows
- [[../comandos/Netcat.md|Netcat]] — Linux, Linux, Windows
- [[../comandos/Nmap.md|Nmap]] — Linux, Linux, Windows
- [[../../apuntes Chema/Fundamentos de Linux.md|Fundamentos de Linux]] — Linux, Nmap, Windows

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #blue_team #cli #forense #linux #linux_ciber #metasploit #nmap #redes #windows_ciber
