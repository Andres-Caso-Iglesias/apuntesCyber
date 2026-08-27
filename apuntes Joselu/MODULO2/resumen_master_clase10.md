> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 10**
> **Módulo:** MODULO2
> **Tema:** Clase 10
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 10. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Esta sesión la imparte Carlos Gómez y es la continuación directa de lo que vimos en las dos clases anteriores de OSINT.

Si antes aprendimos a mapear la superficie de exposición de una organización y a buscar credenciales filtradas, hoy el foco se desplaza hacia una técnica concreta de investigación de personas: el username pivot.

La clase tiene un tono más práctico que las anteriores, con herramientas instaladas en directo, fallos incluidos, y termina con una demostración de lo que se puede llegar a constr uir automatizando todo este flujo con IA y código.

### Username pivot: el principio de reutilización aplicado a alias La mayoría de personas usa el mismo alias en todas las plataformas donde se registra.

Cuando ese alias está ocupado en un sitio nuevo, hace l o más natural: añade un número, cambia una letra o concatena algo reconocible.

Esto se llama iterar sobre el alias, y es exactamente lo que hacemos nosotros para seguir el rastro.

El principio sobre el que descansa todo el username pivot son dos ideas que reaparecerán a lo largo del curso en BruteForce, password spraying y otras técnicas:
- Reutilización: el mismo alias o la misma contraseña en múltiples sitios
- Iteración: cuando no puede reutilizar exactamente, el usuario crea variaciones predecibles
del orig inal El caso real que ilustra esto mejor que cualquier explicación: un investigador de seguridad de renombre mundial iba a dar una charla sobre la seguridad de las contraseñas usando el patrón fuck_twitter25, fuck_instagram25, fuck_github25.

Le detectaron el patrón, le comprometieron todas las cuentas en menos de una hora, y cambió su charla en el último momento para decir que las contraseñas son una mierda.

### La moraleja: lo que parece inteligente desde dentro es perfectamente predecible desde fuera.

> [!important] - La idea clave: no hace falta que alguien use la misma contraseña para todo.

Basta con que
use un patrón.

Y casi todo el mundo usa un patrón

### Falsos positivos: el trabajo real del OSINT Las herramientas de búsqueda de usernames funcionan enviando una petición a ca da plataforma y comprobando el código de respuesta HTTP.

Si la plataforma devuelve un 200 OK , la herramienta asume que el perfil existe.

El problema es que muchas plataformas devuelven 200 aunque el usuario no exista, simplemente redirigiendo a su página p rincipal en lugar de dar un error 404.

Esto genera falsos positivos : la herramienta dice que el usuario existe, pero lo que realmente ha ocurrido es que la plataforma no sabe dar un error bien formado.

El proceso correcto para descartar falsos positivos:
- Abrir cada resultado manualmente y verificar que la página corresponde efectivamente a un
perfil real, no a una redirección genérica
- Comprobar que el contenido del perfil es coherente con lo que sabemos del objetivo: fechas
de actividad, intereses, estilo d e escritura
- Cruzar los resultados con al menos dos fuentes diferentes antes de dar un resultado por
válido Un perfil que en una herramienta aparece como positivo porque la plataforma devuelve 200 en cualquier URL, en otra puede no aparecer porque esa herra mienta sí valida el contenido.

Por eso se usan varias en paralelo.
- La metáfora útil: los falsos positivos son como las alarmas de los coches que saltan con el
viento.

La alarma suena, pero no significa que haya ladrón.

El trabajo del analista es distinguir cuándo el ruido es señal real

### Las herramientas: Sherlock, Maigret y WhatsMyName Las tres herramientas principales para búsqueda de usernames en fuentes abiertas tienen coberturas diferentes y se complementan:

- WhatsMyName (whatsmyname.io ): aproximadamente 600 plataformas categorizadas.

Tiene versión web y produce resultados rápidos
- Maigret : cerca de 3.000 plataformas.

Se mete dentro de las páginas y extrae información
adicional más allá de confirmar si existe el perfil.

Permite exportar en múltiples formatos: TXT, CSV , HTML, PDF, XMind
- Sherlock : aproximadamente 400 plataformas, más rápido, orientado a CLI con opciones de
output limpio Instalación en Kali:
```bash

# Sherlock

```bash
pip install sherlock -project --break-system-packages
```

# Maigret

```bash
pip install maigret --break-system-packages
```

# Uso básico

```

sherlock username --output username.txt maigret username --txt username2.txt El parámetro --break -system -packages es necesario en versiones modernas de Kali porque el sistema tiene instaladas versiones de dependencias que entran en conflicto con las que requieren estas herramientas.

El comando lanza el error pero después funciona correctamente.

Automatización: unificar outputs de varias herramientas El flujo manual de lanzar cada herramienta por separado, revisar los resultados y compararlos es ineficiente.

El objetivo es reducirlo a un único comando que reciba un username y devuelva un output ya limpio y sin duplicados.

El primer script que se construye en clase to ma dos ficheros TXT con resultados de diferentes herramientas y genera uno solo con las URLs únicas:

```bash

#!/bin/bash

# Script de unificación de resultados OSINT

# Uso: osint fichero1.txt fichero2.txt

if [ "$#" -ne 2 ]; then echo "Uso: $0 fichero1.txt fichero2.txt"
```

exit 1 fi

fichero1="$1" fichero2="$2" output="${fichero1%.*}_${fichero2%.*}_joined.txt"

```bash
cat "$fichero1" "$fichero2" | sort -u > "$output" echo "Resultado guardado en: $output" wc -l "$output" El resultado práctico de la clase: lanzando Sherlock y Maigret por separado sobre el mismo username se obtenían 23 y 31 resultados respectivamente (54 en total).
```

Después de unificar y eliminar duplicados, el fichero final tenía 37 entradas únicas, eliminando 17 comprobaciones redundantes.

El segund o script va un paso más allá: recibe directamente el username como parámetro, lanza las dos herramientas en paralelo, espera a que ambas terminen y produce el fichero unificado automáticamente.
```bash

#!/bin/bash

# Uso: osint_full username

```

username="$1" mkdir -p reports

sherlock "$username" --output "reports/${username}_sherlock.txt" & maigret "$username" --txt "reports/${username}_maigret.txt" &

wait # Espera a que ambos procesos terminen

# Unificación y limpieza de duplicados

```bash
cat "reports/${username}_s herlock.txt" "reports/${username}_maigret.txt" \
```
 | grep "^http" \
 | sort -u > "reports/${username}_final.txt"

# Limpieza de ficheros intermedios

```bash
rm "reports/${username}_sherlock.txt" "reports/${username}_maigret.txt"
```

```bash
echo "Resultados guardados en reports/${username}_final.txt" wc -l "reports/${username}_final.txt" Para instalarlo como comando global del sistema:
```
```bash
```bash
chmod +x osint_full sudo mv osint_full /usr/local/sbin/osint_full
```

```

Lo que se puede construir: vigilancia digital automatizada La cla se termina con una demostración de la herramienta que Castillo ha construido en dos tardes usando estas mismas técnicas como base.

El sistema incluye monitorización de dominios y subdominios en tiempo real, detección de credenciales filtradas integrada con la API de LeakRadar, alertas de cambios en la superficie de exposición, búsqueda de menciones en la dark web, y módulo de dominios similares para detección de phishing dirigido contra la organización monitorizada.

El coste de infraestructura: la suscripci ón a Claude Code (160€/mes compartida entre dos personas) y la API de LeakRadar (30€/mes en el plan básico).

La primera venta de una herramienta similar: 15.000€ más 800€ mensuales de mantenimiento.
> [!important] - La idea clave: la diferencia entre hacer OSINT a mano y t enerlo automatizado no es solo de
velocidad.

Es de calidad de cobertura: a mano revisas lo que recuerdas revisar, automatizado revisas todo siempre

Recapitulación integrada Al cerrar esta sesión, sabemos que una investigación de OSINT sobre personas empie za por los alias, que los alias se reutilizan y se iteran de forma predecible, y que herramientas como Maigret y Sherlock cubren miles de plataformas pero producen falsos positivos que hay que filtrar manualmente o mediante código.

El script de unificación que hemos construido es el primer paso hacia una herramienta propia de vigilancia digital: recibe un username, lanza múltiples fuentes en paralelo y entrega un único resultado limpio.

La práctica 1 del máster consistirá en construir una herramienta de est e tipo, elegida libremente, que demuestre la capacidad de automatizar un flujo completo de ciberseguridad con IA y código.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../MODULO1/resumen_master_clase7.md|resumen_master_clase7]— IA en Ciberseguridad, Kali Linux, Linux
- [[resumen_master_clase9.md|resumen_master_clase9]— IA en Ciberseguridad, Kali Linux, Linux
- [[../PREWORK/resumen_clase14.md|resumen_clase14]— IA en Ciberseguridad, Kali Linux, Linux
- [[resumen_master_clase13.md|resumen_master_clase13]— IA en Ciberseguridad, Linux, OSINT
- [[resumen_master_clase8.md|resumen_master_clase8]— IA en Ciberseguridad, Linux, OSINT
- [[../../apuntes Chema/Migrar una Máquina Virtual de VirtualBox a VMware Workstation.md|Migrar una Máquina Virtual de VirtualBox a VMware Workstation]— Kali Linux, Linux

> #ia #kali #linux #osint
