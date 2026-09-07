

> [!info] Relacionado con
> [[Vulnerabilidades Web — OWASP Top 10 y Burp Suite]] · [[Burp Suite - Framework de Auditoría]] · [[OWASP Top 10 - CVE CVSS CWE]] · [[XXE — XML External Entity]]

---

## ① Definición

**Path Traversal** = navegar fuera del directorio previsto usando `../` para acceder a ficheros del sistema.

> [!important] Path Traversal ≠ LFI
> **Path Traversal** es el mecanismo (`../`). **LFI (Local File Inclusion)** es la consecuencia (incluír un fichero que no debería). Son cosas diferentes, aunque a menudo van juntas.

---

## ② Los 6 casos de validación y bypass

### Caso 1: No hay validación

```
../../etc/passwd
```

> [!tip] El caso más fácil
> No se valida nada. Navegas directamente con `../`. El servidor te devuelve el fichero.

### Caso 2: Bloquea `../` → usar ruta absoluta

```
/etc/passwd
```

> [!note] Si bloquea `../` pero acepta rutas absolutas
> En sistemas Unix, puedes acceder directamente con `/etc/passwd` sin `../`.

### Caso 3: Eliminación no recursiva → doble encoding

```
....//....//....//etc/passwd
```

> [!warning] El servidor reemplaza `../` una sola vez
> Si el código hace `str_replace("../", "", $path)`, la cadena `....//` se convierte en `../` después del reemplazo. Es recursivo por diseño.

### Caso 4: URL encoding → `%2e%2e%2f`

```
%2e%2e%2f%2e%2e%2fetc/passwd
```

**Double encoding:**

```
%252e%252e%252f%252e%252e%252fetc/passwd
```

> [!warning] Double encoding
> Si el servidor decodifica una vez, `%252e` se convierte en `%2e`, que a su vez se decodifica en `.`. Es el bypass clásico cuando hay validación de primer nivel.

### Caso 5: Validación de prefijo → incluir ruta + ../../

```
/etc/../../etc/passwd
/var/www/../../etc/passwd
```

> [!note] Si el servidor exige un prefijo
> Algunas aplicaciones concatenan una ruta base. Si el prefijo es `/var/www/`, inyecta `/var/www/../../etc/passwd` para subir de nivel.

### Caso 6: Validación de extensión → null byte

```
../../etc/passwd%00.png
```

> [!warning] Null byte (solo PHP < 5.3.4)
> El `%00` corta la cadena en PHP antiguo. La extensión `.png` pasa la validación pero el fichero se lee completo. **No funciona en versiones modernas.**

---

## ③ Checklist mental (flowchart)

```
¿El parámetro acepta rutas?
 → SÍ → Probar ../../etc/passwd directo
 → ¿Funciona? → Path Traversal confirmado
 → Bloquea ../ → Probar ruta absoluta (/etc/passwd)
 → ¿Funciona? → Sin validación de ruta absoluta
 → No funciona → Probar eliminación no recursiva (....//)
 → ¿Funciona? → str_replace sin recursión
 → No funciona → Probar URL encoding (%2e%2e%2f)
 → ¿Funciona? → Sin decodificación
 → No funciona → Probar double encoding (%252e)
 → ¿Funciona? → Decodificación parcial
 → No funciona → Probar null byte (%00.ext)
 → ¿Funciona? → PHP antiguo
 → No funciona → Validación robusta → buscar otro vector
```

---

## ④ Ficheros clave a probar

| Fichero | Qué nos da |
|---------|-----------|
| `/etc/passwd` | Usuarios del sistema, shells, home dirs |
| `/etc/shadow` | Hashes de contraseñas (necesita root) |
| `/var/www/html/config.php` | Credenciales de BD, API keys |
| `~/.ssh/id_rsa` | Clave privada SSH del usuario |
| `/proc/self/environ` | Variables de entorno |

> [!tip] Empezar SIEMPRE por /etc/passwd
> Es el fichero de prueba. Si no puedes leerlo, Path Traversal no funciona. Si lo lees, escala a ficheros de configuración.

---

## ⑤ PortSwigger y BSCP

> [!info] PortSwigger Web Security Academy
> Todos los labs de Path Traversal están en la plataforma. Son el recurso oficial para practicar los 6 casos.

> [!info] BSCP (Burp Suite Certified Practitioner)
> El examen BSCP cubre Path Traversal en profundidad. Dominar los 6 casos es **obligatorio** para aprobar.

---

## ⑥ Herramientas

| Herramienta | Objetivo |
|------------|----------|
| **Burp Suite (Repeater)** | Testing manual de cada caso con payloads |
| **Burp Intruder** | Iterar encoding, null bytes, rutas |
| **SecLists** | Wordlists de Path Traversal payloads |
| **curl** | Testing rápido desde terminal |

---

## Checklist de repaso

- [ ] ¿Distingo Path Traversal de LFI?
- [ ] ¿Sé los 6 casos de validación y sus bypasses?
- [ ] ¿Puedo seguir el flowchart mental sin mirar los apuntes?
- [ ] ¿Sé qué ficheros probar y qué información dan?
- [ ] ¿Entiendo cuándo funciona cada encoding?
- [ ] ¿He practicado los labs de PortSwigger?

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[XXE — XML External Entity.md|XXE — XML External Entity]]— Burp Suite, Path Traversal / LFI, XXE
- [[../../apuntes Andres/08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco.md|08.07.2026 Path Traversal, LFI y Escalada - Máquina Banco]]— Burp Suite, SSH, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase48.md|resumen_master_clase48]]— Burp Suite, Path Traversal / LFI, XXE
- [[../../write-ups/Banco-THL.md|Banco-THL]]— Burp Suite, Path Traversal / LFI, SSH
- [[../../apuntes Andres/11.07.2026 Owasp Top 10 XXE Labs II.md|11.07.2026 Owasp Top 10 XXE Labs II]]— Burp Suite, SSH, XXE
- [[../../apuntes Joselu/MODULO3/resumen_master_clase49.md|resumen_master_clase49]]— Burp Suite, Path Traversal / LFI, XXE

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/XXE — XML External Entity.md|XXE]]

> #burpsuite #lfi #ssh #xxe
