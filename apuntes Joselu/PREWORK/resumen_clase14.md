> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 14**
> **Módulo:** PREWORK
> **Tema:** Clase 14
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 14. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

--
Resumen – Clase 14: Metodologías de Pentesting y Enumeración Máster de Ciberseguridad e Inteligencia Artificial – Evolve Academy 1.

Introducción: las cinco fases de la auditoría técnica La metodología estándar del pentesting se articula en cinco fases: 1.Enumeración (reconocimiento e información) 2.Explotación 3.Escalada de privilegios 4.Post-explotación 5.Reporte Esta sesión se centra en la primera fase —la enumeración— con énfasis en la parte pasiva y en Google Dorking.

La parte activa se verá en las sesiones prácticas con Kali Linux y Nmap.

Distribución del tiempo en una auditoría de dos semanas (80 horas): Fase Horas Enumeración 40 h (50 %) Explotación 20 h (25 %) Post-explotación 10 h (12,5 %) Reporte 10 h (12,5 %) La enumeración ocupa la mitad del tiempo total: cuanto mejor se enumera, más eficiente y menos frustrante es la explotación. 2.

Metodologías por tipo de auditoría OWASP Top 10 (aplicaciones web) Estándar en constante evolución (versiones 2017, 2021, 2023).

Cada versión actualiza las pruebas a realizar para adaptarse a nuevas tecnologías y vulnerabilidades, aunque los puntos de control fundamentales siguen siendo los mismos: Broken Access Control, fallos criptográficos, inyección, diseño inseguro, misconfiguraciones, etc.

Recurso de referencia: owasp.org.

OSSTMM v3 (redes) Open Source Security Testing Methodology Manual , versión 3.

Cubre todos los puntos de control 1

para auditorías de redes (tanto internas como externas).

Es fundamental saber qué puntos aplican a cada cliente específico (ej. si no hay redes Bluetooth, no se auditan).

MITRE ATT&CK (Red Team avanzado) La matriz más completa para ejercicios de Red Team.

Documenta todas las tácticas, técnicas y sub-técnicas utilizadas por grupos de ciberdelincuentes reales.

Sus fases principales son:
- Reconocimiento (Reconnaissance)
- Desarrollo de recursos ( Resource Development )
- Acceso inicial (Initial Access)
- Ejecución (Execution)
- Persistencia (Persistence)
- Escalada de privilegios ( Privilege Escalation )
- Evasión de defensas ( Defense Evasion)
- Acceso por credenciales ( Credential Access)
- Descubrimiento (Discovery)
- Movimiento lateral ( Lateral Movement)
- Recolección (Collection)
- Comando y control ( Command and Control ) — cuando se inyecta una shell con acceso
remoto
- Exfiltración (Exfiltration)
- Impacto (Impact)
Recurso: attack.mitre.org.

Cada técnica incluye ejemplos de ataque, mitigaciones recomendadas y cómo detectarla.

Es obligatorio seleccionar únicamente las técnicas que aplican al cliente antes de comenzar el ejercicio. 3.

### La enumeración: la fase más importante La enumeración consiste en recopilar toda la información posible del objetivo de forma sistemática y sin realizar ninguna acción de explotación.

Una buena enumeración hace que todas las fases posteriores sean más eficientes.

> [!important] Importante: incluso después de conseguir acceso a un sistema (explotación), hay una segunda ronda de enumeración interna para identificar vías de escalada de privilegios.

Herramientas de gestión de evidencias que se verán durante el máster: CherryTree, Notion y Obsidian, para mantener ordenada toda la información recopilada en cada fase. 2

## 4.

Enumeración pasiva vs. enumeración activa Tipo Descripción Legalidad Ruido generado Pasiva Se consulta a Internet sobre el objetivo sin interactuar directamente con su infraestructuraLegal Ninguno Activa Se interactúa directamente con la infraestructura del objetivo (ej. escaneos Nmap)Legal solo con permiso Detectable por el Blue Team Regla de oro: siempre pasiva primero; activa después.

Menos ruido = menos posibilidades de ser detectado antes de tener suficiente información para explotar. 5.

### Enumeración pasiva: herramientas y fuentes Shodan (shodan.io) Motor de búsqueda de dispositivos conectados a Internet.

Buscar por nombre de organización o dominio devuelve las IPs expuestas con sus puertos abiertos, tecnologías y versiones.

Ejemplo de la sesión: búsqueda de “Cepsa” → 5 resultados con IPs, un portal sin certificado SSL con tecnología GoAnywhere, puertos 443 y 8022 activos, servidor alojado en Amazon Web Services.

Truco: al entrar en el detalle de una IP en Shodan, el campo “dominio” relacionado puede revelar muchas más IPs asociadas (ej. cepsacorp.com → intranet interna accesible).

Censys (search.censys.io) Similar a Shodan pero con mejor rendimiento en búsquedas por nombre de organización y dominio.

Devuelve más resultados que Shodan (ej. en la demo: Censys encontró 96 servidores Apache, 286 Microsoft, etc. frente a 5 de Shodan).

Ambas son complementarias y deben usarse siempre en paralelo.

Subdominios Los subdominios (ej. dev.cepsa.com, intra.cepsa.com) son puertas de entrada muy vulnerables porque las organizaciones suelen olvidarse de ellos.

Se identifican con herramientas como Sublist3r (fuzzing de subdominios con diccionarios) o mediante búsquedas en Shodan/Censys.

Son prioritarios porque: - Suelen tener menor nivel de seguridad que el dominio principal. - A través de ellos se puede pivotar al dominio principal. 3

Dehashed / Intelligence X (próxima sesión) Plataformas de credenciales filtradas.

Se verán en la siguiente sesión junto a los foros de la dark web. 6.

Google Dorking (enumeración pasiva avanzada) El Google Dorking es el uso de operadores avanzados de Google para realizar búsquedas precisas sobre objetivos específicos.

Es completamente legal y pasivo (no se interactúa con la infraestructura del objetivo).

Filtros principales Filtro Sintaxis Uso site site:mueve.es Busca solo en ese dominio/subdominio inurl inurl:admin Busca la palabra en la URL de las páginas indexadas intext intext:contraseña Busca la palabra en el cuerpo del texto de las páginas intitle intitle:login Busca la palabra en el título (H1, H2, H3) de las páginas filetype filetype:pdf Busca archivos de ese tipo concreto Operadores lógicos y comodines Operador Uso Ejemplo "frase exacta" Búsqueda literal de la cadena "contraseña admin" AND Ambas condiciones deben cumplirsecontraseña AND admin OR Al menos una condición contraseña OR password
-término Excluye ese término del
resultadocontraseña -admin
* Comodín (cualquier valor) site:*.mueve.es (todos los
subdominios) Ejemplos prácticos de la sesión
- site:mueve.es contraseña → encontró la página de restablecimiento de contraseña, lo
que podría ser explotable con ingeniería social o IDOR.
- site:mueve.es + portales de login, áreas restringidas detectadas.
- filetype:pdf site:mueve.es intext:password → busca PDFs en el dominio que
contengan la palabra password. 4
- site:*.mueve.es → todos los subdominios de mueve.es indexados en Google.

> [!note] Nota: los operadores AND/OR son también la base de las inyecciones SQL, por lo que entenderlos bien aquí tiene doble utilidad.

### Recurso adicional: GHDB (Google Hacking Database ) en exploit-db.com, que recopila dorks ya construidos para encontrar paneles de administración, archivos de configuración expuestos, credenciales en texto claro, etc. 7.

Flujo completo de enumeración pasiva El flujo que se sigue en una auditoría real es: 1.Buscar el dominio en Shodan → obtener IPs y tecnologías. 2.Buscar el dominio en Censys → ampliar la lista de IPs y servicios. 3.Enumerar subdominios con Sublist3r o fuzzing. 4.Usar Google Dorking sobre todos los dominios y subdominios encontrados. 5.Consultar Dehashed / Intelligence X para credenciales filtradas. 6.Revisar foros de la dark web para información sobre la organización. 7.Consolidar todo en un listado de IPs y subdominios objetivo → base para la enumeración activa con Nmap. 8.

Conceptos y términos clave corregidos Término en la transcripción Corrección / Aclaración weldorking / vueldo aquí / weld orking / google dos quinGoogle Dorking – uso de operadores avanzados de Google para búsquedas de reconocimiento was top ten / o was top ten OWASP Top 10 – estándar de vulnerabilidades en aplicaciones web OSSTMM OSSTMM (Open Source Security Testing Methodology Manual ) – metodología de auditoría de redes mitra attack / mitre MITRE ATT&CK – matriz de tácticas y técnicas de ciberdelincuentes reales attack punto mitre punto or attack.mitre.org – web oficial de la matriz MITRE ATT&CK de hashed e inteligencia x Dehashed e Intelligence X – plataformas de credenciales filtradas census / censi search Censys (search.censys.io) – motor de búsqueda de activos expuestos su blister Sublist3r – herramienta de enumeración de subdominios 5

Término en la transcripción Corrección / Aclaración cherry tree CherryTree – herramienta de gestión de notas y evidencias de auditorías obsidian Obsidian – herramienta de gestión de notas en formato markdown go anywhere GoAnywhere MFT – plataforma de transferencia segura de archivos (detectable en Shodan) comandante control Command and Control (C2) – infraestructura de control remoto del atacante cepsa / mueve Cepsa / Moeve – empresa energética española usada como ejemplo de auditoría intracepsa / club front Intranet / Cloudfront – portal interno y CDN de AWS not rl inurl: – operador de Google Dorking para búsqueda en URLs play work Prework – contenido previo al inicio del máster esté un 3 / es 3 Kali Linux – distribución Linux orientada a pentesting Resumen elaborado para uso académico en el Máster de Ciberseguridad e Inteligencia Artificial – Wolf Academy. 6



---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[../../apuntes Chema/Introducción a Consolas - Bash y PowerShell.md|Introducción a Consolas - Bash y PowerShell]] — Kali Linux, Linux, Windows
- [[resumen_clase4.md|resumen_clase4]] — IA en Ciberseguridad, Nmap, OSINT
- [[../../apuntes Andres/04.09.2026 OWASP API Top 10 Labs.md|04.09.2026 OWASP API Top 10 Labs]] — IA en Ciberseguridad, Linux, Windows
- [[resumen_clase3.md|resumen_clase3]] — IA en Ciberseguridad, Nmap, Windows
- [[../../apuntes evolve/BLOQUE 3.md|BLOQUE 3]] — Nmap, OSINT, Post-Explotación
- [[../../Apuntes/02 - Sistemas Operativos/Consolas - Bash y PowerShell.md|Consolas - Bash y PowerShell]] — Linux, Nmap, Windows

### 🛠️ Herramientas

- [[comandos/Google_Dorks|Google Dorks]]
- [[comandos/Nmap|Nmap]]

### 🎯 Vulnerabilidades Relacionadas


> #blue-team #escalada-privilegios #google-dorks #ia #idor #kali #linux #nmap #osint #pentest #post-explotacion #redes #windows
