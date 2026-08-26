> [!info] Ficha tÃ©cnica
> **Programa:** MÃ¡ster en Ciberseguridad â€” Evolve Academy
> **Bloque:** 07 â€” Pivoting y movilidad lateral
> **Contenido:** TÃºneles SSH (local/remote/dynamic), ProxyChains, socat, port forwarding con RDP

---

## â‘  QuÃ© es el pivoting

En una red con varias mÃ¡quinas conectadas, solo la primera mÃ¡quina comprometida ("visible") suele tener conectividad directa desde el exterior. El pivoting usa ese acceso como **trampolÃ­n** para alcanzar otras mÃ¡quinas de la red interna.
> [!tip] AnalogÃ­a
> Se entra primero en una casa (mÃ¡quina visible), desde ahÃ­ se descubren otras casas conectadas (subredes internas), y se repite el proceso hasta llegar al nÃºcleo de la infraestructura.

---

## â‘¡ TÃºneles SSH: las tres modalidades

### Local port forwarding
Redirige un puerto local hacia un servicio accesible solo desde la mÃ¡quina pivote:

```bash
ssh -L 8080:192.168.10.5:80 usuario@pivote_IP
# Ahora http://localhost:8080 apunta al servicio interno 192.168.10.5:80
```

### Remote port forwarding
Expone un servicio de tu mÃ¡quina local hacia la red remota a travÃ©s del pivote (Ãºtil para recibir una reverse shell desde una mÃ¡quina que solo alcanza al pivote):

```bash
ssh -R 4444:localhost:4444 usuario@pivote_IP
# Un host en la red del pivote puede conectar a pivote_IP:4444 y llegar a ti
```

### Dynamic port forwarding (proxy SOCKS)
Convierte el tÃºnel en un proxy SOCKS genÃ©rico, permitiendo enrutar **cualquier trÃ¡fico** (no solo un puerto) a travÃ©s del pivote:

```bash
ssh -D 1080 usuario@pivote_IP
# Ahora 127.0.0.1:1080 es un proxy SOCKS hacia toda la red interna del pivote
```

---

## â‘¢ ProxyChains: forzar herramientas a usar el tÃºnel

```bash
# Editar /etc/proxychains.conf y aÃ±adir al final:
socks4 127.0.0.1 1080

# Ejecutar cualquier herramienta a travÃ©s del proxy SOCKS:
proxychains nmap -sT -Pn 192.168.10.0/24
proxychains curl http://192.168.10.5
proxychains firefox
```

> [!note] Podencia del SOCKS dinÃ¡mico
> Con SOCKS dinÃ¡mico + ProxyChains se puede escanear con Nmap una subred interna completa a la que solo se llega a travÃ©s de la mÃ¡quina pivote â€” exactamente el mismo Nmap de siempre, pero con el trÃ¡fico enrutado por el tÃºnel.

---

## â‘£ socat como alternativa ligera

Cuando no hay acceso SSH pleno pero sÃ­ ejecuciÃ³n de comandos en el pivote, socat crea redirecciones de trÃ¡fico punto a punto:

```bash
# En el pivote, redirigir el puerto 3389 (RDP) de una mÃ¡quina interna
# hacia un puerto expuesto:
socat TCP-LISTEN:3390,fork TCP:192.168.10.20:3389

# Desde el atacante, conectar por RDP a pivote_IP:3390
```

---

## â‘¤ Port forwarding sobre RDP

Los mismos conceptos de tÃºnel se aplican en entornos Windows: redirigir el protocolo de escritorio remoto a travÃ©s de un pivote permite alcanzar servidores internos que no exponen RDP directamente al exterior.

```bash
# Usando plink.exe (versiÃ³n de lÃ­nea de comandos de PuTTY):
plink.exe -ssh -L 3389:192.168.10.20:3389 usuario@pivote_IP
```

---

## â‘¥ MetodologÃ­a de pivoting completa

1. **Identificar**, desde la mÃ¡quina comprometida, las interfaces y rutas hacia otras subredes: `ip a`, `netstat -rn`, `arp -a`
2. **Establecer el tÃºnel adecuado:** un puerto concreto â†’ local forwarding; explorar una subred entera â†’ SOCKS dinÃ¡mico
3. **Enumerar la nueva subred** a travÃ©s del tÃºnel con las mismas herramientas de siempre (`proxychains nmap`)
4. **Repetir** el ciclo de explotaciÃ³n y escalada de privilegios en cada nueva mÃ¡quina alcanzada

> [!important] Flujo cÃ­clico
> Pivoting no es un paso Ãºnico: es un ciclo repetitivo de enumeraciÃ³n â†’ explotaciÃ³n â†’ escalada â†’ nuevo pivote hasta alcanzar el objetivo.

â†’

