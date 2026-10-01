# REPORTE DE AUDITORÍA - NETMON (Hack The Box)

## Resumen Ejecutivo

| Campo | Valor |
|-------|-------|
| **Máquina** | Netmon |
| **IP Objetivo** | 10.129.230.176 |
| **IP Atacante** | 10.10.14.194 |
| **Sistema Operativo** | Windows Server 2016 Standard |
| **Estado** | COMPLETADA - Flags obtenidas |

---

## Fase 1: Reconocimiento

### Puertos Abiertos (Nmap)
```
21/tcp   - FTP (Microsoft ftpd) - Anonymous login habilitado
80/tcp   - HTTP (PRTG Network Monitor 18.1.37.13946)
135/tcp  - MSRPC
139/tcp  - NetBIOS-SSN
445/tcp  - Microsoft-DS (SMB)
5985/tcp - WinRM HTTP
```

### Hallazgos Clave
- **FTP Anónimo**: Acceso completo al filesystem del sistema
- **PRTG Network Monitor v18.1.37.13946**: Versión vulnerable a CVE-2018-9276
- **SMB**: Windows Server 2008 R2 - 2012

---

## Fase 2: Enumeración y Explotación

### Vector de Ataque
1. **FTP Anónimo** → Acceso a `C:\ProgramData\Paessler\PRTG Network Monitor\`
2. **Archivo de Configuración** → `PRTG Configuration.old.bak` contiene credenciales
3. **Credenciales Encontradas**: `prtgadmin` / `PrTg@dmin2018` (backup 2018)
4. **Año Incrementado**: `PrTg@dmin2019` (configuración actualizada en 2019)
5. **CVE-2018-9276**: Command Injection autenticado → RCE como SYSTEM

### Vulnerabilidades Explotadas
- **CVE-2018-19410**: Missing Authorization (attempted)
- **CVE-2018-9276**: OS Command Injection (exitoso)
  - CVSS: 9.8 (Critical)
  - Impacto: Remote Code Execution

---

## Fase 3: Post-explotación

### Usuario Creado
- **Username**: `pentest`
- **Password**: `P3nT3st!`
- **Grupo**: Administrators

### Flags Obtenidas

```
user.txt: afd5ba547da4b5535a30972265109bcf
         Ubicación: C:\Users\Public\Desktop\user.txt

root.txt: d563f89aa7109067f741335cd2b39535
         Ubicación: C:\Users\Administrator\Desktop\root.txt
```

---

## Tecnologías Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| Nmap | Escaneo de puertos y servicios |
| FTP Client | Enumeración de archivos |
| cURL | requests HTTP, login |
| prtg-decryptor | Descifrado de credenciales |
| 46527.sh (ExploitDB) | CVE-2018-9276 exploit |
| SMBClient | Acceso a archivos, obtención de flags |

---

## MITRE ATT&CK Mapping

| Táctica | Técnica |
|---------|---------|
| Reconocimiento | T1592 - Gather Victim Host Information |
| Initial Access | T1078 - Valid Accounts |
| Initial Access | T1133 - External Remote Services |
| Execution | T1059 - Command and Scripting Interpreter |
| Privilege Escalation | T1078 - Valid Accounts |
| Credential Access | T1552 - Unsecured Credentials |
| Collection | T1005 - Data from Local System |

---

## Remediación Sugerida

1. **Actualizar PRTG** a versión 18.2.39+ para parchear CVE-2018-9276 y CVE-2018-19410
2. **Deshabilitar FTP anónimo** o restringir acceso a directorios sensibles
3. **Cambiar credenciales por defecto** y usar contraseñas robustas
4. **Implementar least privilege** - PRTG no debería correr como SYSTEM
5. **Monitorear logs** de acceso a configuraciones de PRTG
