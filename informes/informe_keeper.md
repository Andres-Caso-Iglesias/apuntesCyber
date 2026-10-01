# HTB Keeper — Informe de explotación

- **Máquina:** Keeper (Easy, Linux)
- **IP:** 10.129.229.41
- **Fecha:** 2026-09-23
- **Flags:** user.txt y root.txt obtenidas

## Resumen

Ruta: Request Tracker (credenciales por defecto) → contraseña en claro de usuario → SSH → dump KeePass (CVE-2023-32784) → clave PuTTY → root SSH.

## Fase 1 — Reconocimiento

| Puerto | Servicio | Versión |
|--------|----------|---------|
| 22/tcp | SSH | OpenSSH 8.9p1 Ubuntu |
| 80/tcp | HTTP | nginx 1.18.0 (Ubuntu) |

- `/etc/hosts`: `10.129.229.41 keeper.htb tickets.keeper.htb`
- Puerto 80 con link a `tickets.keeper.htb/rt/` → **Request Tracker 4.4.4**

## Fase 2 — Credenciales por defecto RT

- Login en RT con **`root:password`** (credencial por defecto oficial)
- Admin → Users → usuario **lnorgaard** (id=27)
- Comentario: `Initial password set to Welcome2023!`

## Fase 3 — Foothold SSH

```bash
ssh lnorgaard@10.129.229.41   # Welcome2023!
```

- Correo en `/var/mail/*`: mención al ticket **#300000** (crash dump de KeePass)
- **user.txt:** `e0454833904b36b6b99db0a68da5150f`

## Fase 4 — Root vía KeePass dump (CVE-2023-32784)

1. En home: `RT30000.zip` (~87 MB) → `KeePassDumpFull.dmp` + `passcodes.kdbx`
2. Dumper: [vdohney/keepass-password-dumper](https://github.com/vdohney/keepass-password-dumper) (cambiado `net7.0` → `net6.0`)
3. Candidatos parciales: `●{ø,...}dgrød med fløde`
4. **Master password real: `rødgrød med fløde`** (el writeup decía `dgrød med fløde`; la `r` inicial no la recupera la CVE)
5. Abrir `.kdbx` con `pykeepass` (keepass2 no instalado sin sudo)
6. Entry **root** con contraseña `F4><3K0nd!` (**no sirve para SSH**) y nota con clave PuTTY `rsa-key-20230519` (`key.ppk`)

## Fase 5 — Root SSH

- `puttygen` no disponible → conversor PPK→OpenSSH propio en Python (validado con `ssh-keygen -y`)
- Archivo: `/home/kali/keeper/key.pem` (permiso 400)

```bash
ssh -i /home/kali/keeper/key.pem root@10.129.229.41
```

- **root.txt:** `570bbc17c0c3873e76cadf4de3f8fb96`

## Credenciales

| Usuario | Credencial | Uso |
|---------|------------|-----|
| root (RT) | `password` | Request Tracker |
| lnorgaard | `Welcome2023!` | SSH foothold |
| KeePass master | `rødgrød med fløde` | passcodes.kdbx |
| root (KeePass) | `F4><3K0nd!` | No válida para SSH |
| root (SSH) | key.pem (desde key.ppk) | Root final |

## Desviaciones del writeup

- Master password: **`rødgrød med fløde`**, no `dgrød med fløde`
- Sin `puttygen` ni `keepass2` (apt requiere sudo) → Python (`pykeepass` + conversor DER/PKCS#1)
- Descarga del zip vía **SFTP** (paramiko); `http.server` colgó
- `keeper.htb` en /etc/hosts no hizo falta (solo `tickets.keeper.htb`)

## Archivos

- `/home/kali/keeper/key.pem` — clave root SSH
- `/home/kali/keeper/key.ppk` — clave PuTTY original
- `/home/kali/keeper/extracted/` — dump + kdbx
- `/home/kali/keeper/nmap_full.*` — evidencia recon
