# REPORTE DE PENETRATION TESTING - MÁQUINA LEGACY (HTB)

## RESUMEN EJECUTIVO

| Campo | Valor |
|-------|-------|
| **Objetivo** | Legacy - Hack The Box |
| **IP** | 10.129.227.181 |
| **Estado** | **PWNED** |
| **Severidad** | CRITICO |
| **Fecha** | 2026-09-11 |

---

## FASE 1: RECONOCIMIENTO

### Escaneo de Puertos (Nmap)
```
Puertos Abiertos:
- 135/tcp - Microsoft RPC
- 139/tcp - NetBIOS-SSN  
- 445/tcp - SMB (microsoft-ds)

Sistema Operativo: Windows XP (Service Pack 3)
Nombre: LEGACY
Grupo: HTB
```

---

## FASE 2: IDENTIFICACIÓN DE VULNERABILIDADES

```
[HALLAZGO] Severidad: CRITICO
- MS08-067 (CVE-2008-4250): VULNERABLE
  Remote Code Execution via NetAPI
  
- MS17-010 (CVE-2017-0143): VULNERABLE  
  EternalBlue - Remote Code Execution via SMBv1
```

---

## FASE 3: EXplotación

**Exploit utilizado**: exploit/windows/smb/ms08_067_netapi
**Payload**: windows/meterpreter/reverse_tcp
**LHOST**: 10.10.14.194
**LPORT**: 4444

**Resultado**: Sesión Meterpreter abierta como NT AUTHORITY\SYSTEM

---

## FASE 4: POST-EXPLOTACIÓN

### Hashes Obtenidos
```
Administrator:500:b47234f31e261b47587db580d0d5f393:b1e8bd81ee9a6679befb976c0b9b6827
john:1003:dc6e5a1d0d4929c2969213afe9351474:54ee9a60735ab539438797574a9487ad
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
```

### Flags Obtenidas

| Flag | Hash |
|------|------|
| **user.txt** | `e69af0e4f443de7e36876fda4ec7644f` |
| **root.txt** | `993442d258b0e0ec917cae9e695d5713` |

---

## MAPEO MITRE ATT&CK

| Táctica | Técnica |
|---------|---------|
| Reconocimiento | T1595 - Active Scanning |
| Acceso Inicial | T1190 - Exploit Public-Facing Application |
| Ejecución | T1203 - Exploitation for Client Execution |
| Persistencia | T1053.005 - Scheduled Task |
| Elevación de Privilegios | T1068 - Exploitation for Privilege Escalation |
| Credenciales | T1003 - OS Credential Dumping |

---

## REMEDIACIÓN SUGERIDA

1. **Actualizar sistema operativo** - Windows XP está EOL (End of Life)
2. **Aplicar parches de seguridad** - MS08-067 y MS17-010
3. **Deshabilitar SMBv1** si no es necesario
4. **Segmentación de red** - Aislar sistemas legacy
5. **Monitoreo de tráfico SMB** para detectar explotación

---




---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes evolve/BLOQUE 3.md|BLOQUE 3]] — Escalada de Privilegios, Metasploit, Post-Explotación
- [[../apuntes Joselu/PREWORK/resumen_clase3.md|resumen_clase3]] — Escalada de Privilegios, Post-Explotación, Redes
- [[../apuntes evolve/BLOQUE 15.md|BLOQUE 15]] — Escalada de Privilegios, Hack The Box, Metasploit
- [[../apuntes Chema/Maquinas/Vaccine.md|Vaccine]] — Escalada de Privilegios, Hack The Box, Metasploit
- [[../Apuntes/06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]] — Escalada de Privilegios, Hack The Box, Metasploit
- [[../comandos/Metasploit.md|Metasploit]] — Metasploit, Post-Explotación, Redes

### 🛠️ Herramientas

- [[comandos/Metasploit|Metasploit]]
- [[comandos/Nmap|Nmap]]

> #blue-team #escalada-privilegios #hack-the-box #metasploit #nmap #pentest #post-explotacion #redes #windows
