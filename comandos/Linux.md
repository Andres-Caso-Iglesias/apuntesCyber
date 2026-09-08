# Comandos Linux y Editor vi

> [!info] Herramienta
> Referencia completa de comandos Linux: navegación, archivos, permisos, procesos, red, texto, forense y editores.
## Navegación de Directorios

> [!tip] Comandos básicos
> Estos son los comandos que usás todo el tiempo en la terminal.

| Comando | Descripción |

| `pwd` | Directorio actual (Print Working Directory) |
| `ls` | Listar contenido |
| `cd` | Cambiar directorio |
| `tree` | Estructura en árbol |
| `du` | Espacio en disco usado |
| `df` | Espacio disponible |

### ls - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-l` | Lista larga |
| `-a` | Mostrar ocultos |
| `-h` | Tamaño legible (KB, MB) |
| `-R` | Recursivo |
| `-t` | Ordenar por fecha |
| `-S` | Ordenar por tamaño |
| `-r` | Invertir orden |
| `-1` | Una línea por entrada |

### cd - Rutas

| Parámetro | Descripción |
|-----------|-------------|
| `~` | Home del usuario |
| `..` | Subir un nivel |
| `-` | Directorio anterior |
| `ruta` | Ir a ruta específica |

### tree - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-L n` | Profundidad máxima |
| `-a` | Mostrar ocultos |
| `-d` | Solo directorios |
| | `-f` | Ruta completa |
|-----------------------------------------------------|---------------------------------------|
## Gestión de Archivos

> [!important] Archivos y directorios
> Crear, mover, copiar, eliminar y buscar archivos.

| Comando | Descripción |

| `cp` | Copiar archivos/directorios |
| `mv` | Mover o renombrar |
| `rm` | Eliminar archivos |
| `mkdir` | Crear directorios |
| `rmdir` | Eliminar directorios vacíos |
| `touch` | Crear archivo vacío o actualizar timestamp |
| `ln` | Crear enlaces |
| `find` | Buscar archivos |
| `locate` | Buscar por nombre (rápido, usa BD) |
| `stat` | Info detallada de archivo |
| `file` | Determinar tipo de archivo |

### cp - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-r` | Recursivo (directorios) |
| `-p` | Preservar atributos |
| `-v` | Verbose |
| `-i` | Confirmar antes de sobrescribir |
| `-u` | Solo si más nuevo |
| `-a` | Archivo (equiv. -dpr) |

### find - Búsqueda

```bash
# Buscar por nombre
find / -name "archivo.txt"

# Buscar archivos de tipo f/d
find / -type f -name "*.log"

# Por tamaño
find / -size +100M

# Por modificación
find / -mtime -7

# Ejecutar comando en resultados
find / -name "*.txt" -exec rm {} \;
| ```
## Permisos y Propietarios

> [!warning] Seguridad
> Los permisos determinan quién puede acceder a qué.

| Comando | Descripción |

| `chmod` | Cambiar permisos |
| `chown` | Cambiar propietario |
| `chgrp` | Cambiar grupo |
| `umask` | Máscara de permisos |
| `sudo` | Ejecutar con privilegios |
| `su` | Cambiar de usuario |
| `passwd` | Cambiar contraseña |
| `id` | UID, GID y grupos |
| `groups` | Grupos del usuario |
| `who` / `w` | Usuarios conectados |

### chmod - Modos

| Modo | Descripción |
|------|-------------|
| `u/g/o/a` | Usuario/Grupo/Otros/Todos |
| `+/-/=` | Añadir/Quitar/Asignar |
| `r/w/x` | Lectura/Escritura/Ejecución |

```bash
# Ejemplos
chmod 755 archivo # rwxr-xr-x
chmod u+x script.sh # dar ejecución al owner
chmod -R 644 /dir # recursivo
```

### sudo - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-u usuario` | Ejecutar como otro usuario |
| `-i` | Shell interactivo root |
| `-s` | Shell actual como root |
| `-l` | Listar permisos |
| | `-k` | Invalidar caché |
|---------------------------------------------------------|-------------------------------|
## Procesos

> [!note] Gestión de procesos
> Matar, monitorizar y gestionar procesos en ejecución.

| Comando | Descripción |

| `ps` | Mostrar procesos |
| `top` | Monitor en tiempo real |
| `htop` | Monitor mejorado (interactivo) |
| `kill` | Enviar señales a procesos |
| `killall` | Matar por nombre |
| `jobs` | Trabajos en segundo plano |
| `bg` / `fg` | Background / Foreground |
| `nohup` | Ejecutar inmune a desconexión |
| `nice` | Ejecutar con prioridad |
| `renice` | Cambiar prioridad |
| `systemctl` | Controlar servicios systemd |

### kill - Señales

| Señal | Descripción |
|-------|-------------|
| `-9` | SIGKILL (forzado) |
| `-15` | SIGTERM (graceful) |
| `-l` | Listar todas las señales |

```bash
# Matar proceso por PID
kill -9 1234

# Matar por nombre
killall nginx

# Prioridad (-20 max, 19 min)
nice -n 10 ./script.sh
| ```
## Red

> [!important] Conectividad
> Configuración de red, transferencia de archivos y diagnóstico.

| Comando | Descripción |

| `ip` | Configurar interfaces (reemplaza ifconfig) |
| `ping` | Verificar conectividad ICMP |
| `curl` | Transferir datos con URLs |
| `wget` | Descargar archivos de la web |
| `ssh` | Conexión segura remota |
| `scp` | Copia segura entre equipos |
| `netstat` | Conexiones de red |
| `ss` | Conexiones de socket (reemplaza netstat) |
| `nmap` | Escanear puertos |
| `traceroute` | Ruta de paquetes |

### ip - Subcomandos

| Subcomando | Descripción |
|------------|-------------|
| `addr` | Interfaces |
| `route` | Rutas |
| `link` | Dispositivos |
| `-4/-6` | IPv4/IPv6 |
| `-s` | Estadísticas |

### curl - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-O` | Guardar archivo |
| `-o nombre` | Nombre personalizado |
| `-L` | Seguir redirecciones |
| `-I` | Solo cabeceras |
| `-X` | Método HTTP |
| `-H` | Cabecera custom |
| `-d` | Datos POST |
| `-u user:pass` | Autenticación |

### ssh - Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `-p puerto` | Puerto específico |
| `-i clave` | Clave privada |
| `-L` | Túnel local |
| `-R` | Túnel remoto |
| `-v` | Verbose |
| `-N` | Sin shell |

### netstat / ss

| Parámetro | Descripción |
|-----------|-------------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Escuchando |
| `-n` | Numérico |
| | `-p` | Con proceso |
|------------------------------------------------------------------------------|---------------------------------|
## Manipulación de Texto

> [!tip] Procesamiento de texto
> Linux es FAMOSO por su capacidad de procesar texto. Dominá estos comandos.

| Comando | Descripción |

| `cat` | Mostrar contenido de archivos |
| `less` | Visor página por página |
| `head` | Primeras líneas |
| `tail` | Últimas líneas |
| `grep` | Buscar patrones |
| `sed` | Editor de flujo |
| `awk` | Procesar texto (lenguaje) |
| `sort` | Ordenar líneas |
| `uniq` | Eliminar duplicados |
| `cut` | Extraer columnas |
| `wc` | Contar líneas/palabras/bytes |
| `diff` | Comparar archivos |
| `tr` | Traducir caracteres |
| `tee` | Escribir a archivo y pantalla |

### grep - Búsqueda

```bash
# Búsqueda básica
grep "texto" archivo

# Case insensitive
grep -i "texto" archivo

# Recursivo
grep -r "texto" /dir/

# Invertir (no coincidir)
grep -v "texto" archivo

# Regex extendida
grep -E "patron1|patron2" archivo

# Contexto (-A después, -B antes, -C ambos)
grep -C 3 "error" log.txt
```

### sed - Sustitución

```bash
# Reemplazar primera ocurrencia
sed 's/antiguo/nuevo/' archivo

# Reemplazar todas
sed 's/antiguo/nuevo/g' archivo

# Editar en sitio (in-place)
sed -i 's/antiguo/nuevo/g' archivo

# Eliminar líneas
sed '/patron/d' archivo
```

### awk - Procesamiento

```bash
# Imprimir campo 1
awk '{print $1}' archivo

# Separador personalizado
awk -F: '{print $1}' /etc/passwd

# Condición
awk '$3 > 100' archivo

# Printf formateado
awk '{printf "%-20s %s\n", $1, $2}' archivo
```
## Forense y Esteganografía

> [!warning] Análisis forense
> Herramientas para extraer información de archivos ocultos y binarios.

| Comando | Descripción |

| `strings` | Extraer cadenas de texto de binarios |
| `exiftool` | Leer/escribir metadatos |
| `binwalk` | Analizar/extraer archivos ocultos |
| `steghide` | Ocultar/extraer datos en imágenes |
| `stegseek` | Romper esteganografía de steghide |
| `md5sum` | Calificar hash MD5 |

```bash
# Extraer strings
strings -n 10 archivo.bin

# Metadatos de imagen
exiftool imagen.jpg

# Buscar archivos ocultos
binwalk -e imagen.bin

# Extraer datos de imagen
steghide extract -sf imagen.jpg
```
# Romper steghide
| stegseek imagen.jpg rockyou.txt | # Hash MD5 | ``` |
|---|---|---| ## Editor vi / vim | > [!abstract] Modos |
> vi tiene 3 modos principales: **NORMAL** (navegar/editar), **INSERT** (escribir), **COMMAND** (guardar/salir).

### Abrir / Salir | | Comando | Modo | Descripción |

| `vi archivo` | - | Abrir archivo |
| `:w` | COMMAND | Guardar |
| `:q` | COMMAND | Salir |
| `:wq` | COMMAND | Guardar y salir |
| `:q!` | COMMAND | Salir sin guardar |
| `:w archivo` | COMMAND | Guardar como |
| `ZZ` | NORMAL | Guardar y salir |

### Entrar en INSERT

| Tecla | Descripción |
|-------|-------------|
| `i` | Antes del cursor |
| `I` | Inicio de línea |
| `a` | Después del cursor |
| `A` | Final de línea |
| `o` | Nueva línea abajo |
| `O` | Nueva línea arriba |
| `Esc` | Volver a NORMAL |

### Movimiento (NORMAL)

| Tecla | Descripción |
|-------|-------------|
| `h j k l` | ←↓↑→ |
| `w / b` | Palabra adelante/atrás |
| `0 / $` | Inicio/fin de línea |
| `gg / G` | Inicio/fin de archivo |
| `:N` | Ir a línea N |
| `Ctrl+f/b` | Página siguiente/anterior |
| `%` | Ir a paréntesis/llave par |

### Edición (NORMAL)

| Tecla | Descripción |
|-------|-------------|
| `x` | Borrar carácter |
| `dd` | Borrar línea |
| `yy` | Copiar línea |
| `p / P` | Pegar después/antes |
| `u` | Deshacer |
| `Ctrl+r` | Rehacer |
| `r` | Reemplazar carácter |
| `cw` | Cambiar palabra |
| `.` | Repetir última acción |

### Buscar y Reemplazar

| Comando | Descripción |
|---------|-------------|
| `/texto` | Buscar adelante |
| `?texto` | Buscar atrás |
| `n / N` | Siguiente/anterior |
| `:%s/a/b/g` | Reemplazar todo |
| `:%s/a/b/gc` | Con confirmación |
| `:nohl` | Quitar resaltado |

### Selección Visual

| Tecla | Descripción |
|-------|-------------|
| `v` | Selección por carácter |
| `V` | Selección por línea |
| `Ctrl+v` | Selección en bloque |
| `y` | Copiar selección |
| `d` | Borrar selección |
| `>` | Indentar |
| | `<<` | Des-indentar |
|---------------------------------------|--------------------------|
## Editor nano

> [!warning] Emergencias
> Editor básico. Usá vi/vim si podés.

| Atajo | Descripción |

| `Ctrl+O` | Guardar |
| `Ctrl+X` | Salir |
| `Ctrl+K` | Cortar línea |
| `Ctrl+U` | Pegar |
| `Ctrl+W` | Buscar |
| `Ctrl+\` | Buscar y reemplazar |
| `Ctrl+A` | Inicio de línea |
| `Ctrl+E` | Final de línea |
| `Ctrl+Y` | Página anterior |
| `Ctrl+V` | Página siguiente |

---

#checklist
- [ ] Navegación con `cd`, `ls`, `pwd` dominada
- [ ] Archivos con `cp`, `mv`, `rm`, `find` practicados
- [ ] Permisos con `chmod` y `chown` entendidos
- [ ] Procesos con `ps`, `kill`, `top` manejados
- [ ] Red con `ip`, `ping`, `curl`, `ssh` configurada
- [ ] Texto con `grep`, `sed`, `awk` procesado
- [ ] vi/vim con modos NORMAL, INSERT, COMMAND dominado


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Chema/OSINT y Esteganografía.md|OSINT y Esteganografía]] — Esteganografía, Forense Digital, Linux
- [[../apuntes Joselu/MODULO2/resumen_master_clase13.md|resumen_master_clase13]] — Esteganografía, Forense Digital, Linux
- [[../Apuntes/comandos/SSH.md|SSH]] — Linux, Redes, SSH
- [[../apuntes evolve/BLOQUE 10.md|BLOQUE 10]] — Forense Digital, Linux, Redes
- [[../Apuntes/08 - Metodologías/Metodología - Explotación Linux.md|Metodología - Explotación Linux]] — Forense Digital, Linux, Redes
- [[../apuntes Joselu/MODULO2/resumen_master_clase8.md|resumen_master_clase8]] — Forense Digital, Linux, OSINT

### 🛠️ Herramientas

- [[comandos/SSH|SSH]]

> #esteganografia #forense #linux #osint #redes #ssh
