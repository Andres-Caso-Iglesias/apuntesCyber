

> [!info] Relacionado con
> [[Linux - Bash Scripting]] · [[Consolas - Bash y PowerShell]] · [[Explotación de Servicios - Linux]] · [[Escalada de Privilegios]]

---

## ① Sistema de ficheros

Linux organiza todo en una jerarquía desde la raíz `/`:

```
/
├── home/ ← Directorios personales (/home/kali)
├── etc/ ← Ficheros de configuración
├── var/ ← Logs, bases de datos
├── tmp/ ← Temporales (se borran al reiniciar)
├── bin, usr/bin ← Ejecutables
├── root/ ← Home del root
└── dev/ ← Dispositivos
```

> [!important] Concepto clave
> **TODO es un fichero** en Linux: discos, impresoras, procesos... Esto permite manipularlo todo con los mismos comandos.

---

## ② Navegación esencial

```bash
[[Linux#pwd|pwd]] # dónde estoy
[[Linux#ls|ls]] -la # listar con detalles y ocultos
[[Linux#cd|cd]] /ruta/absoluta # ir a ruta absoluta
[[Linux#cd|cd]] ruta/relativa # ir a ruta relativa
[[Linux#cd|cd]] .. # subir un nivel
[[Linux#cd|cd]] ~ # ir al home
[[Linux#cd|cd]] - # volver al directorio anterior
```

> [!tip] RUTAS
> **Absoluta**: empieza por `/` y funciona desde cualquier sitio.
> **Relativa**: parte desde donde estás. **Crucial en escalada de privilegios.**

---

## ③ Gestión de ficheros

```bash
[[Linux#mkdir|mkdir]] -p a/b/c # crear árbol de directorios
[[Linux#touch|touch]] fichero.txt # crear fichero vacío
[[Linux#cp|cp]] origen destino # copiar
[[Linux#mv|mv]] origen destino # mover/renombrar
[[Linux#rm|rm]] fichero # borrar
[[Linux#rm|rm]] -rf directorio/ # ⚠ BORRADO RECURSIVO SIN CONFIRMACIÓN
[[Linux#cat|cat]] fichero.txt # ver contenido
[[Linux#less|less]] fichero.txt # paginado (q para salir)
[[Linux#head|head]] -n 20 fichero.txt # primeras 20 líneas
[[Linux#tail|tail]] -n 20 fichero.txt # últimas 20 líneas
```

> [!danger] PELIGRO
> `rm -rf /` o `rm -rf /*` con root borra **TODO** el sistema. **NUNCA ejecutar contra la raíz.**

---

## ④ Permisos en Linux

Cada fichero tiene tres grupos de permisos:

```
 -rwxr-xr-- 1 kali kali 1234 jun 1 fichero.sh
 ^^^ ^^^ ^^^
 owner group others
```

| Permiso | Significado | Octal |
|---------|------------|-------|
| **r** | Leer | 4 |
| **w** | Escribir | 2 |
| **x** | Ejecutar | 1 |
| **SUID (s)** | Ejecuta con permisos del propietario | 4000 |
| **SGID (s)** | Ejecuta con permisos del grupo | 2000 |
| **Sticky (t)** | Solo el propietario puede borrar | 1000 |

```bash
[[Linux#chmod|chmod]] 755 fichero.sh # rwxr-xr-x
[[Linux#chmod|chmod]] +x fichero.sh # añadir ejecución
[[Linux#chown|chown]] usuario:grupo fich # cambiar propietario
```

> [!warning] HACKING
> Los ficheros con **SUID de root** (`[[Linux#find|find]] / -perm -4000`) son vectores clásicos de **escalada de privilegios**.

---

## ⑤ Redirección y pipes

```bash
comando > fichero.txt # stdout a fichero (sobreescribe)
comando >> fichero.txt # stdout añadiendo al final
comando 2> errores.txt # redirigir stderr
comando 2>/dev/null # descartar errores
cmd1 | cmd2 # pipe: stdout → stdin
```

### Ejemplos prácticos

```bash
[[Nmap]] -sV 192.168.1.1 | [[Linux#grep|grep]] open > puertos_abiertos.txt
cat /etc/passwd | [[Linux#grep|grep]] bash
ls -la | sort -k5 -n # ordenar por tamaño
```

> [!tip] PIPE
> El pipe `|` es la herramienta más potente de la terminal. Encadena comandos sin ficheros intermedios.

---

## ⑥ Búsqueda

```bash
[[Linux#grep|grep]] 'patrón' fichero.txt # buscar patrón
[[Linux#grep|grep]] -r 'patrón' directorio/ # recursivo
[[Linux#find|find]] / -name 'fichero.txt' # buscar por nombre
[[Linux#find|find]] / -perm -4000 2>/dev/null # ficheros con SUID ← ESCALADA
which python3 # ruta del ejecutable
[[Linux#locate|locate]] fichero.txt # búsqueda rápida en DB
```

---

## ⑦ Procesos

```bash
[[Linux#ps|ps]] aux # listar todos los procesos
[[Linux#top|top]] / [[Linux#htop|htop]] # monitor en tiempo real
[[Linux#kill|kill]] -9 PID # matar proceso (SIGKILL)
[[Linux#kill|kill]] -15 PID # terminar educadamente (SIGTERM)
comando & # background
[[Linux#fg|fg]] # traer al frente
```

---

## ⑧ Variables y alias

```bash
alias ll='ls -la' # atajo
export PATH=$PATH:/nueva # añadir ruta al PATH
echo $PATH # ver rutas de búsqueda
```

---

## ⑨ Historial y limpieza

```bash
history # ver historial
history | [[Linux#grep|grep]] [[Nmap]] # buscar en historial
history -c # limpiar en memoria
cat /dev/null > ~/.bash_history # vaciar fichero
export HISTFILE=/dev/null # deshabilitar en sesión
```

> [!info] FORENSE
> El historial se guarda en varios sitios (`~/.bash_history`, `/var/log/auth.log`). Conocer dónde es clave tanto para atacar como para defender.

---

## Checklist de repaso

- [ ] ¿Navego cómodamente por el sistema de ficheros?
- [ ] ¿Entiendo los permisos y cómo se leen?
- [ ] ¿Sé usar pipes y redirecciones?
- [ ] ¿Sé buscar ficheros con find y grep?
- [ ] ¿Conozco los permisos SUID y por qué importan?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 10.md|BLOQUE 10]— Forense Digital, Linux, Windows
- [[Linux - Bash Scripting.md|Linux - Bash Scripting]— Forense Digital, Linux, Windows
- [[../../apuntes Chema/Fundamentos de Linux.md|Fundamentos de Linux]— Escalada de Privilegios, Forense Digital, Linux
- [[../../apuntes evolve/BLOQUE 6.md|BLOQUE 6]— Escalada de Privilegios, Linux, Windows
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]— Escalada de Privilegios, Forense Digital, Linux
- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]— Escalada de Privilegios, Linux, Windows

> #escalada-privilegios #forense #linux #windows
