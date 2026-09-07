

> **Relacionado:** [[Metodología de Explotación]] · [[Escalada de Privilegios]] · [[Reverse Shells y Post-Explotación]]

---

## 1. Qué es el pivoting

En una red con varias máquinas conectadas, solo la primera máquina comprometida ("visible") suele tener conectividad directa desde el exterior. El pivoting usa ese acceso como **trampolín** para alcanzar otras máquinas de la red interna.

> **Analogía:** Se entra primero en una casa (máquina visible), desde ahí se descubren otras casas conectadas (subredes internas), y se repite el proceso hasta llegar al núcleo de la infraestructura.

**Cuándo usar pivoting:**
- Después de comprometer una máquina y descubrir que tiene múltiples interfaces de red
- Cuando necesitas alcanzar subredes internas que no son accesibles directamente
- Para moverte lateralmente dentro de una red corporativa tras una explotación inicial

---

## 2. Identificación de subredes desde la máquina comprometida

Antes de establecer cualquier túnel, necesitas saber hacia dónde se puede ir:

```bash
# Interfaces de red y subredes
ip a

# Tabla de rutas
netstat -rn
route -n

# Tabla ARP (hosts vecinos)
arp -a

# Conexiones activas (puede revelar subredes internas)
ss -tuln
netstat -tuln
```

> **Clave:** Si ves interfaces como `192.168.10.0/24` o `10.0.5.0/24` diferentes a la tuya, esas son subredes internas candidatas a pivoting.

---

## 3. Túneles SSH: las tres modalidades

### Local port forwarding
Redirige un puerto local hacia un servicio accesible solo desde la máquina pivote:

```bash
ssh -L 8080:192.168.10.5:80 usuario@pivote_IP
# Ahora http://localhost:8080 apunta al servicio interno 192.168.10.5:80
```

**Uso típico:** Acceder a un panel de administración interno, base de datos, o servicio web que solo se ve desde la red interna.

### Remote port forwarding
Expone un servicio de tu máquina local hacia la red remota a través del pivote (útil para recibir una reverse shell desde una máquina que solo alcanza al pivote):

```bash
ssh -R 4444:localhost:4444 usuario@pivote_IP
# Un host en la red del pivote puede conectar a pivote_IP:4444 y llegar a ti
```

**Uso típico:** Recibir una reverse shell cuando tu máquina atacante no es alcanzable directamente desde la víctima.

### Dynamic port forwarding (proxy SOCKS)
Convierte el túnel en un proxy SOCKS genérico, permitiendo enrutar **cualquier tráfico** (no solo un puerto) a través del pivote:

```bash
ssh -D 1080 usuario@pivote_IP
# Ahora 127.0.0.1:1080 es un proxy SOCKS hacia toda la red interna del pivote
```

**Uso típico:** Escanear una subred completa, usar Nmap, curl, o cualquier herramienta a través del túnel.

---

## 4. ProxyChains: forzar herramientas a usar el túnel

```bash
# Editar /etc/proxychains.conf y añadir al final:
socks4 127.0.0.1 1080

# Ejecutar cualquier herramienta a través del proxy SOCKS:
proxychains nmap -sT -Pn 192.168.10.0/24
proxychains curl http://192.168.10.5
proxychains firefox
```

> **Potencia del SOCKS dinámico:** Con SOCKS dinámico + ProxyChains se puede escanear con Nmap una subred interna completa a la que solo se llega a través de la máquina pivote — exactamente el mismo Nmap de siempre, pero con el tráfico enrutado por el túnel.

### Limitaciones de ProxyChains
- No funciona con herramientas que usen UDP (ProxyChains solo soporta TCP)
- Nmap con ProxyChains: solo escaneos TCP connect (`-sT`), no SYN (`-sS`)
- Algunas herramientas que hacen resolución DNS propia pueden ignorar el proxy

---

## 5. socat como alternativa ligera

Cuando no hay acceso SSH pleno pero sí ejecución de comandos en el pivote, socat crea redirecciones de tráfico punto a punto:

```bash
# En el pivote, redirigir el puerto 3389 (RDP) de una máquina interna
# hacia un puerto expuesto:
socat TCP-LISTEN:3390,fork TCP:192.168.10.20:3389

# Desde el atacante, conectar por RDP a pivote_IP:3390
```

### Otros usos de socat en pivoting

```bash
# Forward de un puerto TCP arbitrario
socat TCP-LISTEN:8080,fork TCP:192.168.10.5:80

# Crear un túnel inverso (reverse shell a través del pivote)
# En el pivote:
socat TCP-LISTEN:4444,fork TCP:192.168.10.20:4444
```

---

## 6. Port forwarding sobre RDP

Los mismos conceptos de túnel se aplican en entornos Windows: redirigir el protocolo de escritorio remoto a través de un pivote permite alcanzar servidores internos que no exponen RDP directamente al exterior.

```bash
# Usando plink.exe (versión de línea de comandos de PuTTY):
plink.exe -ssh -L 3389:192.168.10.20:3389 usuario@pivote_IP
```

### Alternativa con sshuttle (VPN sobre SSH)

```bash
# Crear una VPN ligera sobre SSH que enrute toda una subred
sshuttle -r usuario@pivote_IP 192.168.10.0/24

# Ahora puedes acceder directamente a cualquier host de 192.168.10.0/24
# como si estuvieras en esa red
```

---

## 7. Metodología de pivoting completa

```
1. COMPROMETER máquina visible
 ↓
2. IDENTIFICAR interfaces y subredes (ip a, netstat -rn, arp -a)
 ↓
3. SELECCIONAR tipo de túnel:
 - Puerto concreto → local forwarding
 - Subred entera → SOCKS dinámico + ProxyChains
 - Sin SSH → socat
 ↓
4. ENUMERAR la nueva subred a través del túnel
 (proxychains nmap -sT -Pn <subred>)
 ↓
5. EXPLOTAR máquinas descubiertas
 ↓
6. ESCALAR privilegios
 ↓
7. REPETIR el ciclo desde la nueva máquina comprometida
```

> **Importante:** Pivoting no es un paso único: es un ciclo repetitivo de enumeración → explotación → escalada → nuevo pivote hasta alcanzar el objetivo.

---

## 8. Errores comunes en pivoting

| Error | Consecuencia |
|-------|-------------|
| No verificar todas las interfaces de la máquina pivote | Se pierden subredes internas |
| Usar `-sS` con ProxyChains | No funciona (Solo TCP connect con `-sT`) |
| Olvidar que el tráfico queda registr logs del pivote | Detección por SOC o EDR |
| No verificar conectividad antes de escanear | Falsos negativos en enumeración |
| Confiar solo en SSH para pivoting | Hay alternativas (socat, sshuttle, plink) cuando SSH no está disponible |

---

## 9. Checklist de repaso

- [ ] Identifico todas las interfaces y subredes desde la máquina comprometida
- [ ] Sé cuándo usar local vs remote vs dynamic forwarding
- [ ] Configuro ProxyChains correctamente para SOCKS dinámico
- [ ] Uso socat cuando SSH no está disponible
- [ ] Verifico conectividad antes de escanear a través de un túnel
- [ ] Recuerdo que pivoting es un ciclo, no un paso único

---

> **Siguiente tema:** Redes WiFi y Hardware — Auditoría WiFi y Car Hacking

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 7.md|BLOQUE 7]]— Escalada de Privilegios, Redes, SSH
- [[../../apuntes Joselu/PREWORK/resumen_clase16.md|resumen_clase16]]— Escalada de Privilegios, Post-Explotación, SSH
- [[../../transcripciones/Julio/11.07.2026 Owasp Top 10 XXE  Labs II.md|11.07.2026 Owasp Top 10 XXE  Labs II]]— Escalada de Privilegios, Post-Explotación, SSH
- [[../06 - Explotacion y Post-Explotacion/Explotación de Servicios - Windows.md|Explotación de Servicios - Windows]]— Escalada de Privilegios, Post-Explotación, Redes
- [[../11 - Forense Digital/Análisis Forense y Memoria.md|Análisis Forense y Memoria]]— Escalada de Privilegios, Post-Explotación, Redes
- [[../../apuntes Joselu/PREWORK/resumen_clase3.md|resumen_clase3]]— Escalada de Privilegios, Post-Explotación, Redes

### 🛠️ Herramientas

- [[comandos/Netcat|Netcat / Reverse Shells]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

> #blue-team #escalada-privilegios #netcat #nmap #pentest #pivoting #post-explotacion #redes #reverse-shell #ssh #wifi #windows
