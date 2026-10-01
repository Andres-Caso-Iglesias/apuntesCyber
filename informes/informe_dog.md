# INFORME RED TEAM — HackTheBox "Dog"
**Target:** 10.129.231.223 · **Fecha:** 2026-09-28 · **Estado:** COMPLETADO (ambas flags)

---

## 1. Reconocimiento / Enumeración

### Escaneo de puertos
Los escaneos iniciales con `--min-rate 2000` daban **falsos "filtered"** (rate-limiting del firewall/VPN).
Solución: `--min-rate 400-60` con `-sS` **y** `-sT` (ambos coincidieron) + verificación manual con `/dev/tcp`.

| Puerto | Estado | Servicio | Versión |
|--------|--------|----------|---------|
| 22/tcp | open | ssh | OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu) |
| 80/tcp | open | http | Apache httpd 2.4.41 (Ubuntu) |

- Resto de 65533 puertos: **closed** (RST). Host vivo, sin más servicios.
- OS: **Linux / Ubuntu 20.04.6 LTS**, kernel `5.4.0-208-generic`, hostname `dog`.
- UDP: no concluyente (firewall drop).
- Escaneos: `nmap_syn_slow.*`, `nmap_ct_slow.*`, `nmap_full_safe.*`, `nmap_fast_open.txt`.

### Web (puerto 80)
- **Backdrop CMS 1.27.1** (fork de Drupal), tema `basis`, admin theme `seven`.
- Versión confirmada por `core/misc/backdrop.js?v=1.27.1`.
- Headers: `X-Generator: Backdrop CMS 1`, `X-Backdrop-Cache: HIT`.
- Login: `/?q=user/login` (clean URLs desactivadas, usa `?q=`).
- `robots.txt` expone rutas `/admin`, `/node/add`, `/user/*`.
- Directorio indexado: `/modules/` (listing abierto).

---

## 2. Vulnerabilidades encontradas

### [HALLAZGO-1] Severidad: **CRÍTICO** — Repositorio Git expuesto en la raíz web
- **Evidencia:**
  ```
  $ curl http://10.129.231.223/.git/HEAD
  ref: refs/heads/master
  $ curl http://10.129.231.223/.git/index   → 344.667 bytes (2.873 entradas)
  $ curl http://10.129.231.223/.git/logs/HEAD
  8204779c764abd4c9d8d95038b6d22b6a7515afa root <dog@dog.htb> commit (initial): todo: customize url aliases...
  ```
- **Impacto:** dump completo del código fuente del sitio (**2.871 archivos**) con dumper propio (`git_dump.py`).
- **Remediación:** bloquear `/.git` en Apache + no versionar el docroot en producción.

### [HALLAZGO-2] Severidad: **CRÍTICO** — Credenciales de base de datos filtradas
- **Evidencia:** `dumped/settings.php:15`
  ```php
  $database = 'mysql://root:BackDropJ2024DS2024@127.0.0.1/backdrop';
  $settings['hash_salt'] = 'aWFvPQNGZSz1DQ701dD4lC5v1hQW34NefHvyZUzlThQ';
  ```
- MySQL solo escucha en 127.0.0.1 (3306 cerrado externamente) → no explotable directamente.
- **Pero la contraseña es reutilizada** (ver Hallazgo-4).
- Otros datos filtrados: email `tiffany@dog.htb` (`update.settings.json`), config web-accesible en `/files/config_83dddd18e1ec67fd8ff5bba2453c7fb3/`.

### [HALLAZGO-3] Severidad: **ALTO** — Backdrop CMS 1.27.1 RCE autenticado
- **Ref:** EDB-52021 / `searchsploit backdrop` → *Backdrop CMS 1.27.1 - Authenticated Remote Command Execution*.
- Requiere usuario con permisos de instalador → **obtenidos** (ver acceso).

### [HALLAZGO-4] Severidad: **CRÍTICO** — Reutilización de contraseña MySQL → cuenta OS
- `johncusack:BackDropJ2024DS2024` valida en `su` → `uid=1001(johncusack)`.

### [HALLAZGO-5] Severidad: **ALTO** — Sudo rule → privesc root
- `sudo -l` como johncusack:
  ```
  User johncusack may run the following commands on dog:
      (ALL : ALL) /usr/local/bin/bee
  ```
- `bee` es la CLI de Backdrop (`/backdrop_tool/bee/bee.php`) y expone **`bee eval`** (PHP arbitrario).
- Ejecutado como **root** (`EUID=0`).

---

## 3. Vector de acceso conseguido

```
1. ffuf  → detecta /.git/HEAD (200)
2. dumper → settings.php → MySQL root:BackDropJ2024DS2024 + hash_salt
3. usuarios enumerados (config update_emails = tiffany@dog.htb, admin/people)
4. LOGIN WEB OK → tiffany:BackDropJ2024DS2024  → rol Administrator (acceso total)
   (los 8 usuarios CMS tienen rol Administrator: tiffany, rosa, axel, morris, john,
    dogBackDropSystem, jobert, jPAdminB)
5. RCE → subida de módulo malicioso shell.tgz en /?q=admin/installer/manual
   → batch core/authorize.php (op=do_nojs → op=finished) → "Installed shell successfully"
   → webshell /modules/shell/shell.php  → uid=33(www-data)
6. Persistencia → /var/www/html/x.php (docroot escritura www-data)
7. Post-explotación → su johncusack con la pass MySQL (reutilización) → user.txt
8. Root → sudo bee eval (EUID=0) → root.txt
```

**Cadena completa:** *Recon → Fuzz → Secret Exposure (.git) → Credential Reuse → Auth Bypass (admin) → RCE (upload) → Privesc (sudo/bee)*

Mapeo MITRE ATT&CK: T1595.003 (Active Scanning: Wordlist), **T1552.001 (Unsecured Credentials: Files)**,
T1078 (Valid Accounts), **T1190 (Exploit Public-Facing Application)**, T1505.003 (Server Software Component: Web Shell),
T1548.003 (Abuse Elevation Control: sudo), T1078.003 (Local Accounts).

---

## 4. Usuario / ruta de escalada

| Fase | Identidad | Nota |
|------|-----------|------|
| Inicial | anónimo | - |
| Web | `tiffany` (Administrator) | pass `BackDropJ2024DS2024` |
| RCE | `www-data` (uid 33) | webshell + x.php |
| User | `johncusack` (uid 1001) | pass reutilizada de MySQL |
| Root | `root` (uid 0) | `sudo /usr/local/bin/bee ev '<php>'` con `--root /var/www/html` |

---

## 5. FLAGS CAPTURADAS

```
user.txt : 4bdef848a743e0034b7cc7ea6b49e850   /home/johncusack/user.txt
root.txt : 680c119b50b25091985e45ff1de25bcb   /root/root.txt
```
Guardadas en `/home/kali/htb/dog/flags.txt`.

---

## 6. Evidencia / artefactos en `/home/kali/htb/dog/`
`flags.txt`, `dumped/` (repo completo), `git_dump.py` + `git_dump.log`, `nmap_*.gnmap/nmap/xml`,
`ffuf_*.json`, `login*.py`, `upload_and_run.py`, `shell.tgz`, `bee_help.txt`, `dblog.html`,
`people.html`, `batch_finished.html`, `robots.txt`, `http_headers.txt`.

### Artefactos en el target — ✅ LIMPIADO (2026-09-28)
- `/var/www/html/x.php` (backdoor webshell) — **eliminado** → verifica 404
- `/modules/shell/` (módulo malicioso) — **eliminado** del docroot, sin registro en DB `system`
- `/tmp/pwn.sh`, `/tmp/shell.tgz`, `/tmp/update-extraction-e0d10bd3/`, `/tmp/.htaccess`, `/tmp/q*.sql` — **eliminados** (`/tmp` limpio)
- Sesiones web creadas durante la operación (hostname 10.10.% / hoy) — **borradas** de la tabla `sessions`
- Sin persistencias en cron (`/etc/cron.d`, `/var/spool/cron`) ni `authorized_keys`
- Verificación final: `x.php` → 404, `modules/shell/shell.php` → 404, `/` → 200 (sitio operativo)
- No se modificó `.git` (vulnerabilidad preexistente de la máquina) ni logs de Apache

---

## 7. Remediaciones recomendadas
1. Bloquear `/.git`, `/.svn`, `/files/config_*` en el servidor web.
2. **Nunca** dejar `settings.php` en un repo con el docroot; separar config y usar secrets distintos por sistema.
3. **No reutilizar** la contraseña de BD como contraseña de usuario/SSH.
4. Restringir `/admin/installer/manual` y la subida de módulos a cuentas dedicadas, con revisión.
5. Limitar `sudo` a comandos concretos; `bee` no debe correr como root sin contención (PHP arbitrario).
6. Desactivar directory listing (`Options -Indexes`) en `/modules/`.
7. Usar `AllowOverride`+reglas para denegar scripts en directorios de uploads.
