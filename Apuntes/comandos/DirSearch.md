# DirSearch — Cheat Sheet

> Fuzzing de directorios (Python).

---

## Sintaxis básica

```bash
dirsearch -u <URL>
```

## Uso básico

```bash
dirsearch -u http://10.10.10.x
dirsearch -u http://10.10.10.x -e php,txt,html
```

## Opciones

```bash
-u <url>                         # URL objetivo
-e <ext>                         # Extensiones (php,txt,html)
-w <wordlist>                    # Wordlist
-t <threads>                     # Threads (default: 30)
-r <recursive>                   # Recursividad
--exclude-status <code>          # Excluir status codes
--include-status <code>          # Incluir status codes
--exclude-text <text>            # Excluir por texto
--include-text <text>            # Incluir por texto
-p <proxy>                       # Proxy
--cookie <cookie>                # Cookie
--user-agent <ua>                # User-Agent
--random-agent                   # User-Agent aleatorio
-o <file>                        # Output
```

## Ejemplos

```bash
# Con extensiones
dirsearch -u http://10.10.10.x -e php,html,txt,bak

# Con wordlist
dirsearch -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt

# Con proxy
dirsearch -u http://10.10.10.x -p http://127.0.0.1:8080
```









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Feroxbuster.md|Feroxbuster]] — DirSearch, FFUF, GoBuster
- [[GoBuster.md|GoBuster]] — DirSearch, FFUF, GoBuster
- [[../../comandos/DirSearch.md|DirSearch]] — DirSearch, FFUF, GoBuster
- [[../02 - Sistemas Operativos/Migrar VM VirtualBox a VMware.md|Migrar VM VirtualBox a VMware]] — DirSearch, GoBuster, Linux
- [[../../apuntes Chema/Maquinas/Fuzzing de parámetros con x8 - Rockstar.md|Fuzzing de parámetros con x8 - Rockstar]] — DirSearch, GoBuster, Linux

### 🌐 Cross-Dominio

- [[../../../programacion/XML/xpath_xslt.md|xpath_xslt]] — Programacion: Linux, Python, Redes
- [[../../../cloud/github_actions.md|github_actions]] — Cloud: Linux, Python, Redes

> #dirsearch #feroxbuster #ffuf #gobuster #linux #linux_ciber #python #redes
