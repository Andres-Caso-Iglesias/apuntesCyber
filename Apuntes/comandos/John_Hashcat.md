# John the Ripper / Hashcat — Cheat Sheet

> Cracking de hashes.

---

## John the Ripper

### Uso básico

```bash
john <hashfile>                   # Crackear hashes
john --wordlist=<wordlist> <hashfile>  # Con wordlist
john --show <hashfile>            # Mostrar hashes crackeados
```

### Formatos

```bash
john --list=formats               # Listar formatos soportados
john --format=raw-md5 <hashfile>  # Especificar formato
john --format=raw-sha256 <hashfile>
john --format=bcrypt <hashfile>
```

### Modos

```bash
john --wordlist=rockyou.txt hash.txt           # Wordlist
john --incremental hash.txt                    # Incremental (fuerza bruta)
john --single hash.txt                         # Single mode (reglas)
john --rules hash.txt                          # Con reglas
```

### Extracción de hashes

```bash
# Linux
unshadow /etc/passwd /etc/shadow > hashes.txt

# SAM (Windows)
secretsdump.py -sam SAM -system SYSTEM LOCAL

# MySQL
mysql -u root -p -e "SELECT user, authentication_string FROM mysql.user;"
```

## Hashcat

### Uso básico

```bash
hashcat -m <type> <hashfile> <wordlist>
hashcat -m 0 hash.txt rockyou.txt          # MD5
hashcat -m 100 hash.txt rockyou.txt        # SHA1
hashcat -m 1400 hash.txt rockyou.txt       # SHA256
hashcat -m 3200 hash.txt rockyou.txt       # bcrypt
```

### Tipos de hash

```bash
hashcat --hash-info                   # Ver info de tipos
# -m 0    MD5
# -m 100  SHA1
# -m 1400 SHA256
# -m 1000 NTLM
# -m 3200 bcrypt
# -m 5500 NetNTLMv1
# -m 5600 NetNTLMv2
```

### Modos de ataque

```bash
# Dictionary
hashcat -m 0 hash.txt wordlist.txt

# Rule-based
hashcat -m 0 hash.txt wordlist.txt -r rules/best64.rule

# Brute force
hashcat -m 0 hash.txt -a 3 ?a?a?a?a?a?a

# Mask
hashcat -m 0 hash.txt -a 3 ?u?l?l?l?l?d?d
```

### Masks

```bash
?a   # Todos los caracteres
?l   # Minúsculas
?u   # Mayúsculas
?d   # Dígitos
?s   # Especiales
?h   # Hex lowercase
?H   # Hex uppercase
```

### GPU

```bash
hashcat -m 0 hash.txt wordlist.txt -d 1     # Device 1
hashcat -m 0 hash.txt wordlist.txt --force   # Forzar
hashcat -m 0 hash.txt wordlist.txt -o out.txt  # Output
```

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Explotación de Servicios - Linux]] — Cracking de hashes en pentesting
- [[Escalada de Privilegios]] — Hashes como vector de escalada

> #john #hashcat #herramientas #hashes #cracking
