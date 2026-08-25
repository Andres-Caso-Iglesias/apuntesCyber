

> [!info] Relacionado con
> [[Wireshark - Análisis de Tráfico]] · [[OSINT - Metodología y Fuentes]] · [[Enumeración Web]] · [[Metodología de Explotación]]

---

## ① ¿Qué es Nmap?

**Nmap** (Network Mapper) es la herramienta de referencia para descubrir hosts, puertos y servicios en una red. Primer paso de **cualquier** auditoría.

---

## ② Metodología de escaneo en 3 fases

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ 1. Escaneo rápido│ ──→ │ 2. Todos los │ ──→ │ 3. Scripts sobre │
│ (top 1000) │ │ puertos (-p-) │ │ puertos hall. │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### Fase 1 — Escaneo rápido

```bash
[[Nmap]] -oN recon/initial.txt <IP>
```

### Fase 2 — Todos los puertos

```bash
[[Nmap]] -p- -oN recon/allports.txt <IP>
# -p- escanea los 65,535 puertos
# Presionar VV durante el escaneo para ver progreso
```

### Fase 3 — Scripts y versiones

```bash
[[Nmap]] -sC --script default,vuln -sV -Pn -p <PUERTOS> -oA recon/full <IP>
```

| Flag | Función |
|------|---------|
| `-sC` | Scripts por defecto |
| `-sV` | Detectar versiones |
| `-Pn` | Omitir host discovery |
| `-oA` | Guardar en 3 formatos (normal, grepeable, XML) |
| `vuln` | Scripts de CVEs (más intrusiva) |

---

## ③ Comandos esenciales

### Descubrimiento de hosts

```bash
[[Nmap]] -sn 10.0.2.0/24 # hosts activos en el rango
sudo netdiscover -r 10.0.2.0/24 # por ARP (más sigiloso)
```

### Escaneo de puertos

```bash
[[Nmap]] <IP> # escaneo básico (top 1000)
[[Nmap]] -sCV <IP> # + scripts + versiones
[[Nmap]] -p- <IP> # TODOS los puertos
[[Nmap]] -sV -p22,80,443 <IP> # puertos concretos
```

### Guardar resultados

```bash
[[Nmap]] -oN archivo.txt <IP> # formato normal
[[Nmap]] -oG archivo.txt <IP> # formato grepeable
[[Nmap]] -oX archivo.xml <IP> # formato XML
[[Nmap]] -oA nombre <IP> # los 3 formatos a la vez
```

---

## ④ Detección de OS por TTL

| TTL | Sistema operativo |
|-----|------------------|
| 64 | Linux/Unix |
| 128 | Windows |
| 255 | Cisco / dispositivos |

---

## ⑤ Scripts útiles

```bash
# Scripts de enumeración
[[Nmap]] --script smb-enum-shares <IP> # shares SMB
[[Nmap]] --script http-enum <IP> # rutas HTTP
[[Nmap]] --script dns-brute <IP> # subdominios

# Scripts de vulnerabilidades
[[Nmap]] --script vuln <IP> # buscar CVEs
[[Nmap]] --script http-sql-injection <IP> # SQLi
```

---

## ⑥ Conexión con otras áreas

| Área | Cómo usa Nmap |
|------|--------------|
| [[OSINT - Metodología y Fuentes]] | Descubrir hosts en la red |
| [[Enumeración Web]] | Descubrir puertos 80/443 |
| [[Fuzzing Web con ffuf]] | Servicios para fuzzear |
| [[Metodología de Explotación]] | Primer paso de cualquier pentest |
| [[Wireshark - Análisis de Tráfico]] | Detectar escaneos Nmap |

---

## ⑦ Errores comunes

> [!warning] ERRORES
> - **Olvidar `-p-`**: solo ves los 1000 puertos comunes, te pierdes los no estándar.
> - **Lanzar `vuln` sin `-Pn`**: si el host no responde a ping, Nmap lo descarta.
> - **No guardar resultados**: pierdes el trabajo de enumeración.
> - **Confundir servicio esperado con real**: sin `-sCV`, Nmap muestra el servicio por defecto del puerto, no el real.

---

## Checklist de repaso

- [ ] ¿Sé hacer un escaneo en 3 fases (rápido → completo → scripts)?
- [ ] ¿Conozco los flags más importantes (-sC, -sV, -p-, -Pn, -oA)?
- [ ] ¿Sé guardar resultados en diferentes formatos?
- [ ] ¿Entiendo la diferencia entre netdiscover y nmap?
- [ ] ¿Sé interpretar el TTL para detectar el OS?

---

## Enlaces relacionados

- [[comandos/Nmap]] — Cheat sheet de comandos
