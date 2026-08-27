# John the Ripper / Hashcat — Cracking de Hashes

> [!info] Herramientas
> John the Ripper (CPU) y Hashcat (GPU) para crackear hashes de contraseñas.
## Identificar Hashes

> [!tip] Primer paso
> Antes de crackear, identificá el tipo de hash.

```bash

# Identificar hash
hashid HASH

# Mostrar modos de hashcat
hashid -m HASH

# Modos de john
hashid -j HASH

# Identificar desde archivo
hashid -f hashfile.txt
```

### Patrones de Identificación

| Hash | Longitud | Ejemplo |
|------|----------|---------|
| MD5 | 32 hex | `5d41402abc4b2a76b9719d911017c592` |
| SHA1 | 40 hex | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| SHA256 | 64 hex | `2cf24dba5fb0a30e26e83b2ac5b9e29e...` |
| NTLM | 32 hex | `aad3b435b51404eeaad3b435b51404ee:hash` |
| BCrypt | 60 chars | `$2a$10$N9qo8uLOickgx2ZMRZoMy...` |

### Online Crackers

| Sitio | Uso | |
| ----------------------------------------------------- | --------------------------- | --------------- |
| `crackstation.net` | Multi-formato | |
| `hashes.com` | Multi-formato | |
| | `cmd5.com` | MD5, SHA1, NTLM |
| | | |
## John the Ripper — Básico

> [!important] Uso básico
> John detecta automáticamente el formato del hash.

```bash

# Crackear hashes (auto-detect)
john hashfile.txt

# Con diccionario
john --wordlist=/usr/share/wordlists/rockyou.txt hashfile.txt

# Mostrar cracks
john --show hashfile.txt

# Listar formatos soportados
john --list=formats
```

### Formatos Específicos

| Formato | Comando |
|---------|---------|
| MD5 | `--format=raw-md5` |
| SHA256 | `--format=raw-sha256` |
| BCrypt | `--format=bcrypt` |
| DES Crypt | `--format=descrypt` |
| MD5 Crypt | `--format=md5crypt` |
| NetLM | `--format=netlm` |
| NetNTLMv2 | `--format=netntlmv2` |

### Opciones

| Comando | Descripción |
|---------|-------------|
| `--fork=4` | 4 procesos paralelos |
| `--pot=john.pot` | Archivo pot personalizado |
| `--session=mysession` | Nombre de sesión |
| | `--restore=mysession` | Restaurar sesión |
|-----------------------------------------------------------------------|---------------------|
## Hashcat — Básico

> [!tip] GPU vs CPU
> Hashcat usa GPU (más rápido). Necesitás especificar el modo (`-m`).

```bash

# MD5 (mode 0)
hashcat -m 0 hashfile.txt rockyou.txt

# NTLM (mode 1000)
hashcat -m 1000 hashfile.txt rockyou.txt

# SHA-512 Unix (mode 1800)
hashcat -m 1800 hashfile.txt rockyou.txt

# BCrypt (mode 3200)
hashcat -m 3200 hashfile.txt rockyou.txt

# Mostrar cracks
hashcat --show
```

### Modos Comunes

| Modo | Hash |
|------|------|
| `0` | MD5 |
| `100` | SHA1 |
| `1400` | SHA-256 |
| `1000` | NTLM |
| `1800` | sha512crypt |
| `3200` | bcrypt |
| `5600` | NetNTLMv2 |
| | `9600` | MS-SQL |
|-------------------------------------------------------|----------------------------------|
## Tipos de Ataque

> [!note] Attack Modes
> Hashcat soporta diferentes estrategias de cracking.

| Modo | Descripción | Ejemplo |

| `-a 0` | Dictionary | `hashcat -m 0 -a 0 hash.txt rockyou.txt` |
| `-a 1` | Combination | `hashcat -m 0 -a 1 hash.txt rock1.txt rock2.txt` |
| `-a 3` | Brute force (mask) | `hashcat -m 0 -a 3 hash.txt ?a?a?a?a?a?a` |
| `-a 6` | Hybrid wordlist+mask | `hashcat -m 0 -a 6 hash.txt rock1.txt ?a?a?a` |
| `-a 7` | Hybrid mask+wordlist | `hashcat -m 0 -a 7 hash.txt ?a?a?a rock1.txt` |

---

## Masks / Placeholders

> [!abstract] Placeholders para brute force
| Placeholder | Descripción |
|-------------|-------------|
| `?l` | lowercase (a-z) |
| `?u` | uppercase (A-Z) |
| `?d` | digit (0-9) |
| `?s` | special (!@#$...) |
| `?a` | all (?l?u?d?s) |
| `?b` | 0x00-0xff |

### Ejemplos de Masks

| Mask | Descripción |
|------|-------------|
| `?d?d?d?d?d?d` | 6 dígitos (PIN) |
| `?l?l?l?l?l?l?l` | 7 minúsculas |
| `?u?l?l?l?l?d?d` | 1 mayúscula + 4 min + 2 dígitos |
| `?a?a?a?a?a?a?a?a` | 8 all (lento) |

```bash
# PIN de 6 dígitos
hashcat -a 3 -m 0 hash.txt ?d?d?d?d?d?d

# 8 caracteres mixtos
hashcat -a 3 -m 0 hash.txt ?u?l?l?l?l?d?d?d
| ```
## Rules

> [!tip] Reglas de transformación
> Las reglas modifican las palabras del diccionario para generar variaciones.

```bash

# John rules
john --wordlist=rockyou.txt --rules hash.txt
john --wordlist=rockyou.txt --rules=all hash.txt

# Hashcat rules
hashcat -m 0 -r rules/best64.rule hash.txt rockyou.txt
hashcat -m 0 -r rules/d3ad0ne.rule hash.txt rockyou.txt
```

---

## Formatos de Hash

### Linux

| Formato | Ejemplo |
|---------|---------|
| MD5 Crypt | `$1$salt$hash` |
| SHA-256 | `$5$salt$hash` |
| SHA-512 | `$6$salt$hash` |
| BCrypt | `$2a$10$hash` |

### Windows

| Formato | Ejemplo |
|---------|---------|
| LM | 32 hex (legacy) |
| NTLM | 32 hex |
| NetLM | 32 hex |
| NetNTLMv2 | `hash:challenge` |
| DCC2 | `$mscc$hash` |

### Web / Apps

| Formato | Ejemplo |
|---------|---------|
| MD5 | 32 hex |
| SHA1 | 40 hex |
| PHPass | `$P$hash` |
| BCrypt | `$2y$hash` |
| | Argon2 | `$argon2i$hash` |
|------------------------------------------------------------|-------------------------------------|
## Wordlists

> [!important] Diccionarios comunes
> La calidad del wordlist determina el éxito del cracking.

| Wordlist | Tamaño | Uso |

| `/usr/share/wordlists/rockyou.txt` | 14M | El clásico |
| Seclists/Common-Credentials | Variado | Passwords comunes |
| Seclists/Usernames/ | Variado | Nombres de usuario |

### Crear Wordlists

```bash
# Con crunch: 8 chars, 4 lowercase + 4 digits
crunch 8 8 -t @@@@%%%% -o wordlist.txt

# Lista simple
echo -e "admin\nroot\npassword" > users.txt

# Scraping web con cewl
cewl -d 3 -m 5 http://target > wordlist.txt
```

---

## Formato de Hash para John/Hashcat

```bash
# John - Pass-the-Hash
impacket-psexec -hashes :HASH user@IP

# Hashcat - formato
-hashes :NTLM_HASH # Solo NTLM
-hashes LM_HASH:NTLM_HASH # LM + NTLM
```

---

#checklist
- [ ] Hash identificado correctamente
- [ ] Herramienta elegida (John o Hashcat)
- [ ] Diccionario seleccionado
- [ ] Reglas/masks configuradas
- [ ] Hash crackeado
- [ ] Credenciales obtenidas

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../apuntes Joselu/PREWORK/resumen_clase13.md|resumen_clase13]— Hydra, John / Hashcat, Linux
- [[../apuntes evolve/BLOQUE 5.md|BLOQUE 5]— Hydra, John / Hashcat, Linux
- [[../write-ups/Castor-THL.md|Castor-THL]— Hydra, John / Hashcat, Linux
- [[../Apuntes/02 - Sistemas Operativos/Linux - Fundamentos.md|Linux - Fundamentos]— Linux, Windows
- [[../apuntes evolve/BLOQUE 10.md|BLOQUE 10]— Linux, Windows
- [[../apuntes evolve/BLOQUE 11.md|BLOQUE 11]— Hydra, Linux, Windows

### 🛠️ Herramientas

- [[comandos/Hydra|Hydra]]
- [[comandos/John_Hashcat|John / Hashcat]]

> #hydra #john #linux #windows
