# Anonimato e Ingeniería Social

> [!info] Nota consolidada del contenido de Chema (sesión completa, ~372 líneas originales)
> Anonimato, ingeniería social y técnicas de匿anonymización aplicadas al pentesting ético.

---

## Anonimato: Definición

> [!abstract] Definición
> **Anonimato** = operar sin que la identidad sea atribuible a una persona real.

**Principio fundamental**: el anonimato **se rompe por comodidad**. Cada paso de conveniencia es un punto de fuga de identidad.

---

## VPN: Cómo funciona realmente

### Enrutado de una conexión con VPN

```
Tu PC ──▶ VPN Server ──▶ Internet ──▶ Destino
 (tú ──────────▶ proveedor VPN ve tu IP real)
 (destino ve ──▶ IP del VPN server, no la tuya)
```

| Capa | ¿Quién ve qué? |
|------|-----------------|
| **Tu proveedor de internet** | Ve que te conectas al VPN server (tráfico cifrado) |
| **Proveedor VPN** | Ve tu IP real y a dónde te conectas |
| **Destino** | Ve la IP del VPN server, no la tuya |
| **ISP del destino** | Ve la IP del VPN server |

> [!warning] La VPN NO da anonimato real
> - El proveedor VPN **conoce tu IP real** y las páginas que visitas
> - Si el proveedor VPN es comprometido o recibe orden judicial, tu identidad queda expuesta
> - La VPN **oculta tu IP del destino**, pero no te anonimiza del proveedor VPN

> [!tip] ¿Cuándo sí es útil la VPN?
> - Para evitar geo-restricciones (no es anonimato, es evasión)
> - Para cifrar tráfico en WiFi público
> - Para acceso a redes corporativas (VPN de empresa)
> - **Nunca** para anonimato real en operaciones de seguridad

---

## Cadena de anonimización

> [!important] Cadena completa para operar de forma anónima
> Cada eslabón es una capa de protección. Romper uno compromete la cadena.

```
┌──────────┐    ┌──────────┐    ┌───────────────┐    ┌──────────┐
│ VPN      │───▶│ Monero   │───▶│ VPS con cripto│───▶│Dominio   │
│          │    │ (XMR)    │    │               │    │calentado │
└──────────┘    └──────────┘    └───────────────┘    └──────────┘
 Oculta IP Pago anónimo Infraestructura Dominio con
 delISP sin trazable sin datos personales historial previo
```

### Capa 1: VPN
- Oculta tu IP del ISP y del destino
- **No** oculta tu identidad del proveedor VPN

### Capa 2: Monero (XMR)
- Criptomoneda con firmas anilladas y direcciones ocultas
- **No** se puede rastrear como Bitcoin (que tiene blockchain pública)
- Se usa para pagar hosting, dominios, servicios

### Capa 3: VPS con cripto
- Servidor virtual pagado con Monero
- Sin datos personales (no necesita nombre, dirección, tarjeta)
- Acceso solo por SSH/Tor

### Capa 4: Dominio calentado
- Dominio registrado con historial previo (no recién creado)
- Se le da "vida" antes de usarlo en operaciones
- Un dominio nuevo es un **flag** para OSINT defensivo

> [!danger] Cualquier paso por comodidad rompe la cadena
> - Usar Bitcoin en vez de Monero → trazable
> - Comprar VPS con tarjeta de crédito → identificable
> - Registrar dominio con datos reales → atribuible
> - Conectarte sin VPN una vez → tu IP real en logs

---

## Tor: La Red Cebolla

```
Tu PC ──▶ Nodo de entrada ──▶ Nodo medio ──▶ Nodo de salida ──▶ Internet
 (sabe que eres tú) (no sabe nada) (no sabe de dónde vienes)
```

> [!warning] Limitaciones de Tor
> - **Nodo de salida comprometido**: puede ver tráfico no cifrado (HTTPS mitiga esto)
> - **Exit node logging**: el nodo de salida puede registrar IPs de destino
> - **Velocidad**: muy lento por el circuito de 3 nodos
> - **Fingerprints del navegador**: Tor Browser tiene una fingerprint distinta que puede identificarse
> - **Relay de correlación**: un adversario global puede correlacionar entrada y salida por timing

---

## Ingeniería Social

> [!danger] La ingeniería social ataca al factor humano, no a la tecnología
> La más efectiva de las técnicas ofensivas porque explota la confianza y la descuidad.

### Evolución de técnicas

| Técnica | Descripción | Vector |
|---------|-------------|--------|
| **Phishing** | Emails/sitios falsos que suplantan identidad | Email, web |
| **Smishing** | Phishing por SMS | SMS |
| **QRishing** | Phishing mediante códigos QR (evolución reciente) | QR codes |

> [!note] QRishing: la evolución más peligrosa
> Un código QR puede redirigir a cualquier URL. En publicidad, carteles, menús de restaurantes, etc. El usuario **no ve la URL** antes de escanear. Es phishing sin sospecha previa.

### IP Logger: uso defensivo/attribution

> [!tip] Uso legítimo: atribución en pentesting
> Un IP logger (como Grabify) puede usarse para:
> - **Atribución defensiva**: identificar el origen de un ataque
> - **Pentesting consentido**: demostrar que se puede rastrear a un usuario
> - **No** para vigilancia ilegal ni stalking

---

## Modelo as-a-Service (SaaS/RaaS)

> [!abstract] Cómo funciona el crimen organizado en ciberseguridad

| Modelo | Descripción | Ejemplo |
|--------|-------------|---------|
| **RaaS** | Ransomware as a Service | LockBit, BlackCat — operadores alquilan ransomware |
| **PhaaS** | Phishing as a Service | Kits de phishing listos para usar |
| **CaaS** | Cracking as a Service | Fuerza bruta por encargo |

> [!warning] ¿Por qué se pillan al operador?
> - **Operational Security (OpSec) fallida**: un paso por comodidad rompe el anonimato
> - **Colaboración con fuerzas del orden**: proveedores VPN, ISPs, hosting cooperan
> - **Errores humanos**: reutilizar emails, contraseñas, patrones de comportamiento
> - **On-chain analysis**: aunque Monero es difícil, Bitcoin y otras cryptos son trazables

---

## Fuzzing de parámetros

> [!info] Dos herramientas complementarias para fuzzing web

### x8_lite.py — Nombres de parámetros

- Fuzzing de **nombres** de parámetros HTTP
- Descubre parámetros ocultos o no documentados
- Uso: `python3 x8_lite.py -u http://target/page -w wordlist.txt`

### valfuzz.py — Valores de parámetros

- Fuzzing de **valores** de parámetros conocidos
- Testea inyecciones, overflow, valores especiales
- Uso: `python3 valfuzz.py -u http://target/page?param=FUZZ -w wordlist.txt`

> [!tip] Diferencia clave
> `x8_lite` pregunta: **¿qué parámetros existen?**
> `valfuzz` pregunta: **¿qué valores son vulnerables?**

---

## Checklist de repaso

- [ ] Entiendo que la VPN oculta IP pero no garantiza anonimato real
- [ ] Conozco la cadena de anonimización: VPN → Monero → VPS → dominio
- [ ] Sé que Tor tiene limitaciones (exit nodes, correlación)
- [ ] Reconozco phishing, smishing y QRishing como evolución de ingeniería social
- [ ] Entiendo el modelo RaaS/PhaaS y por qué se pillan a los operadores
- [ ] Distingo x8_lite (nombres) de valfuzz (valores)
- [ ] Recuerdo: el anonimato se rompe por comodidad

---

## Defensive Lessons

> [!danger] Lecciones defensivas

- **No escanear QR de origen desconocido** — QRishing es la evolución más peligrosa del phishing
- **Desconfiar de dominios nuevos** — un dominio recién creado es un red flag
- **Verificar la URL antes de introducir credenciales** — phishing sigue siendo la técnica #1
- **Usar 2FA** — incluso si las credenciales se filtran, 2FA detiene el ataque
- **No confiar en VPN como solución mágica** — son una capa, no son anonimato

---

## Tags

#anonimato #vpn #tor #monero #ingenieria-social #phishing #qrishing #raas #fuzzing #blue-team #opsec

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes evolve/BLOQUE 9.md|BLOQUE 9]]— Hydra, Redes, WiFi / Hardware
- [[../../comandos/Hydra.md|Hydra]]— Hydra, Redes, SSH
- [[../10 - Redes WiFi y Hardware/Auditoría WiFi y Car Hacking.md|Auditoría WiFi y Car Hacking]]— Hydra, OSINT, WiFi / Hardware
- [[../../comandos/SSH.md|SSH]]— Hydra, Redes, SSH
- [[../../transcripciones/Julio/15.07.2026 IA Introducción y Vibe Coding.md|15.07.2026 IA Introducción y Vibe Coding]]— Hydra, Redes, SSH
- [[../../apuntes Joselu/MODULO1/resumen_master_clase6.md|resumen_master_clase6]]— Redes, SSH, WiFi / Hardware

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/SSH|SSH]]

> #hydra #osint #redes #ssh #wifi
