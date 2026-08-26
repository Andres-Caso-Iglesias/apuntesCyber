> [!info] Ficha técnica
> **Programa:** Máster en Ciberseguridad — Evolve Academy
> **Bloque:** 07 — Pivoting y movilidad lateral
> **Contenido:** Túneles SSH (local/remote/dynamic), ProxyChains, socat, port forwarding con RDP

---

## ① Qué es el pivoting

En una red con varias máquinas conectadas, solo la primera máquina comprometida ("visible") suele tener conectividad directa desde el exterior. El pivoting usa ese acceso como **trampolín** para alcanzar otras máquinas de la red interna.
> [!tip] Analogía
> Se entra primero en una casa (máquina visible), desde ahí se descubren otras casas conectadas (subredes internas), y se repite el proceso hasta llegar al núcleo de la infraestructura.

---

## ② Túneles SSH: las tres modalidades

### Local port forwarding
Redirige un puerto local hacia un servicio accesible solo desde la máquina pivote:

```bash
ssh -L 8080:192.168.10.5:80 usuario@pivote_IP
# Ahora http://localhost:8080 apunta al servicio interno 192.168.10.5:80
```

### Remote port forwarding
Expone un servicio de tu máquina local hacia la red remota a través del pivote (útil para recibir una reverse shell desde una máquina que solo alcanza al pivote):

```bash
ssh -R 4444:localhost:4444 usuario@pivote_IP
# Un host en la red del pivote puede conectar a pivote_IP:4444 y llegar a ti
```

### Dynamic port forwarding (proxy SOCKS)
Convierte el túnel en un proxy SOCKS genérico, permitiendo enrutar **cualquier tráfico** (no solo un puerto) a través del pivote:

```bash
ssh -D 1080 usuario@pivote_IP
# Ahora 127.0.0.1:1080 es un proxy SOCKS hacia toda la red interna del pivote
```

---

## ③ ProxyChains: forzar herramientas a usar el túnel

```bash
# Editar /etc/proxychains.conf y añadir al final:
socks4 127.0.0.1 1080

# Ejecutar cualquier herramienta a través del proxy SOCKS:
proxychains nmap -sT -Pn 192.168.10.0/24
proxychains curl http://192.168.10.5
proxychains firefox
```

> [!note] Podencia del SOCKS dinámico
> Con SOCKS dinámico + ProxyChains se puede escanear con Nmap una subred interna completa a la que solo se llega a través de la máquina pivote — exactamente el mismo Nmap de siempre, pero con el tráfico enrutado por el túnel.

---

## ④ socat como alternativa ligera

Cuando no hay acceso SSH pleno pero sí ejecución de comandos en el pivote, socat crea redirecciones de tráfico punto a punto:

```bash
# En el pivote, redirigir el puerto 3389 (RDP) de una máquina interna
# hacia un puerto expuesto:
socat TCP-LISTEN:3390,fork TCP:192.168.10.20:3389

# Desde el atacante, conectar por RDP a pivote_IP:3390
```

---

## ⑤ Port forwarding sobre RDP

Los mismos conceptos de túnel se aplican en entornos Windows: redirigir el protocolo de escritorio remoto a través de un pivote permite alcanzar servidores internos que no exponen RDP directamente al exterior.

```bash
# Usando plink.exe (versión de línea de comandos de PuTTY):
plink.exe -ssh -L 3389:192.168.10.20:3389 usuario@pivote_IP
```

---

## ⑥ Metodología de pivoting completa

1. **Identificar**, desde la máquina comprometida, las interfaces y rutas hacia otras subredes: `ip a`, `netstat -rn`, `arp -a`
2. **Establecer el túnel adecuado:** un puerto concreto → local forwarding; explorar una subred entera → SOCKS dinámico
3. **Enumerar la nueva subred** a través del túnel con las mismas herramientas de siempre (`proxychains nmap`)
4. **Repetir** el ciclo de explotación y escalada de privilegios en cada nueva máquina alcanzada

> [!important] Flujo cíclico
> Pivoting no es un paso único: es un ciclo repetitivo de enumeración → explotación → escalada → nuevo pivote hasta alcanzar el objetivo.


