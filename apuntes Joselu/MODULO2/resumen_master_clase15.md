> [!info] Ficha técnica
> **Máster de Ciberseguridad e Inteligencia Artificial** · **Clase 15**
> **Módulo:** MODULO2
> **Tema:** Clase 15
> **Fuente:** Apuntes Joselu · Evolve Academy

> [!tip] Cómo leer estos apuntes
> Resumen estructurado de la clase 15. Contenido optimizado para estudio activo y repaso rápido antes de exámenes.

---

---

| Esta sesión la imparte Yuba González y es la continuación directa de la clase anterior sobre el modelo OSI. Si en la primera sesión construimos el marco conceptual capa por capa, hoy cerramos el modelo con las capas que quedaban pendientes, añadimos la perspectiva práctica con Wireshark, y terminamos con una demostración en vivo que hace tangible todo lo que llevamos semanas aprendiendo: por qué importa que una aplicación use HTTPS y no HTTP. La clase abre también con un bloque extenso sobre inteligencia | artificial que conecta con el enfoque del máster de integrar IA en el trabajo diario. |
|---|---|

| IA en ciberseguridad: el cambio de chip necesario Antes de entrar en materia técnica, Yuba dedica tiempo a contextualizar el momento actual de la IA, que considera rele vante para todos los perfiles del sector. Los tres grandes players son Anthropic (Claude), OpenAI | (ChatGPT y Codex) y Google | (Gemini y Google Labs). Anthropic tiene tres modelos: Haiku (el más ligero), Sonnet (uso diario) y Opus (el más potente y caro), co brados por tokens. El cambio de mentalidad que propone no es aprender a usar herramientas concretas, sino cambiar el foco de "¿cómo hago esto?" a "¿cómo consigo que una IA lo haga por mí?". En hacking este cambio ya está ocurriendo: muchos perfiles integra n IA para construir herramientas propias de enumeración, auditoría web automática o gestión de proyectos, con una suscripción de veinte euros al mes. Dos recomendaciones prácticas para el desarrollo con IA: |
|---|---|---|
- Terminar funcionalidades antes de añadir nuevas. El error más común es estar mejorando
continuamente sin tener nunca un producto funcional. Mejor un MVP que funcione que una herramienta perfecta que nunca se usa
- Usar gates o puertas entre etapas. Dado que la IA no es determinista (el mismo input
puede da r outputs diferentes), conviene definir requisitos que deben cumplirse antes de pasar a la siguiente fase, para evitar que el proceso se desvíe sin control

Repaso del modelo OSI: lo esencial por capa Antes de continuar con las capas pendientes, Yuba conso lida lo visto en la sesión anterior con los conceptos que deben quedar grabados de cada capa:
- Capa 1 (Física): todo lo que se puede tocar. Cables, antenas, conectores. Los ataques
requieren presencia física
- Capa 2 (Enlace): red local, direcciones MAC, prot ocolo ARP para vincular IPs con MACs.
Ataques: ARP Spoofing, MAC Spoofing, VLAN Hopping
- Capa 3 (Red): IPs, routers, comunicación entre redes distintas. Rangos privados no
enrutables desde Internet. Ataques: IP Spoofing, escaneo con Nmap
- Capa 4 (Transporte) : TCP y UDP, puertos. El puerto es el número de apartamento dentro
del edificio -IP
- Capa 5 (Sesión): HTTP es stateless, las sesiones y tokens resuelven eso. Ataques: robo de
cookies, session fixation, robo de tokens OAuth

Capa 5 — Sesión: ataques y defensa s El punto central de la capa de sesión para un atacante es que si consigue robar el identificador de sesión, no necesita la contraseña . Puede acceder como usuario legítimo sin conocer sus credenciales. Los ataques más relevantes:
- Robo de cookies mediante XSS: una vulnerabilidad de Cross -Site Scripting permite
ejecutar JavaScript en el navegador de la víctima y enviar su cookie de sesión al atacante. Esto se verá en detalle con una máquina práctica
- Session fixation: el atacante fuerza a la víctima a usar un identificador de sesión que él ya
conoce. Si la aplicación no rota el ID al autenticarse, el atacante puede usar esa sesión
- Token theft en entornos cloud: equivalente al pass -the-ticket de Directorio Activo, pero
robando tokens OAuth ya emitidos Contramed idas: flags de seguridad en cookies (Secure, HttpOnly, SameSite), rotación de tokens, doble factor de autenticación, bloqueos de IP por intentos fallidos. La ausencia de alguna de estas flags es una vulnerabilidad reportable en cualquier auditoría web.

| Capa 6 — Presentación: cifrado TLS La capa de presentación traduce, codifica y cifra. Su elemento más importante es TLS/SSL , que es lo que convierte HTTP en HTTPS. Para entender TLS hay que entender primero dos tipos de cifrado: Cifrado simétrico: | una sola clave cifra y descifra. Es rápido y eficiente, como un candado donde la misma llave abre y cierra. El problema: ¿cómo llega esa llave al otro extremo sin que nadie la intercepte por el camino? Cifrado asimétrico: | dos claves matemáticamente relaci onadas. La pública la conoce todo el mundo; la privada solo su propietario. Lo que se cifra con la pública solo puede descifrarse con la privada, y viceversa. Resuelve el problema del transporte de claves, pero es más lento. TLS combina ambos: usa cifrado asimétrico al inicio para que ambos extremos acuerden una clave simétrica compartida, y a partir de ese momento usa la clave simétrica para todo. Velocidad del simétrico con seguridad del asimétrico. Para auditar la configuración TLS de un servidor existe la herramienta testssl.sh : |
|---|---|---|
```bash

# Descargar y ejecutar testssl

```bash
git clone https://github.com/drwetter/testssl.sh cd testssl.sh
```
```

./testssl.sh dominio.com

Esta herramienta identifica versiones TLS habilitadas, suites de cifrado débiles (especialmente las basadas en CBC) y vulnerabilidades conocidas. Lanzarla contra un servidor de cliente suele producir dos o tres vulnerabilidades reportables de manera inmediata, sin necesidad de ninguna interacción activa.
> [!important] - La id ea clave: si un servidor tiene habilitado TLS 1.1 junto a TLS 1.3, un atacante puede
forzar que la comunicación use la versión antigua, que tiene vulnerabilidades conocidas, y descifrar el tráfico. Esto se llama downgrade de protocolo

| Capa 7 — Aplicación: | donde vive el usuario La capa de aplicación es la que tiene más superficie de ataque porque es la más expuesta. Aquí viven HTTP, FTP, SSH, DNS, SMTP, RDP y todos los protocolos que reconocemos por nombre. Los códigos de respuesta HTTP son señales que guía n al pentester: 1xx | Informativos | (raramente visibles) 2xx | Éxito | 200 OK, 201 Created, 204 No Content 3xx | Redirecciones | 301 Moved, 302 Found 4xx | Error del cliente | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests 5xx | Error del servidor 500 Internal Server Error, 502 Bad Gateway Para el pentester, un 401 confirma que el recurso existe pero requiere autenticación. Un 403 confirma que existe pero está prohibido. Un 500 pue de revelar información sobre el servidor cuando se combina con una inyección. Estos códigos, aunque son una convención y los desarrolladores pueden ignorarla, suelen seguirse y orientan el trabajo de reconocimiento. Los ataques de esta capa (SQLi, XSS, CSR F, SSRF, problemas de autenticación) tienen sesiones completas dedicadas en el módulo de hacking web. Burp Suite | y OWASP WebGoat/PortSwigger Academy | son las herramientas y plataformas de referencia para aprenderlos. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

| Encapsulación: cómo viajan realmente lo s datos Cuando escribimos una contraseña en una web y pulsamos enter, el dato atraviesa las siete capas hacia abajo en nuestra máquina y las siete hacia arriba en el servidor. Cada capa añade su propia información al paquete, como una muñeca rusa. Una petición HTTPS completa contiene, de fuera hacia dentro: Trama Ethernet (capa 2) | → MACs origen/destino Paquete IP (capa 3) | → IPs origen/destino Segmento TCP (capa 4) | → puertos origen/destino, flags Registro TLS (cap. 6) → cifrado, v ersión TLS Petición HTTP (c.7) → método, cabeceras, cuerpo Esto explica por qué un atacante en la red local ve cosas distintas que un atacante en Internet: el primero puede acceder a las capas 2 y 3; el segundo solo ve lo que está expuesto en capa 7. |
|---|---|---|---|

Wireshark en práctica: capturar credenciales en texto claro

La demostración final une todo lo visto. Wireshark tiene tres zonas principales: la lista de paquetes arriba, los detalles del paquete seleccionado en el centro (desplegable capa por capa), y los bytes en crudo en hexadecimal abajo. Con un servidor HTTP (sin cifrado) corriendo en local, el flujo es:
```bash

# Servidor HTTP simple en Python

```

python3 -m http.server 8080

# Capturar con filtro HTTP en Wireshark

# Filtro: http

# Luego: click derecho → Follow → HTTP Stream

| En el stream HTTP se ve en texto plano el POST del formulario de login, incluyendo usuario y contraseña. Con HTTPS el mismo stream aparece cifrado e ilegible. Esta demostración, visible en directo en Wireshark, es la respuesta práctica | a una pregunta que lleva semanas implícita en el módulo: ¿por qué importa tanto el cifrado, los metadatos, las capas? |
|---|---|
> [!important] - La idea clave: si una aplicación usa HTTP en una red corporativa, cualquier atacante con
acceso a esa red y Wireshark abierto puede captu rar las credenciales de cualquier usuario que inicie sesión. No hace falta explotar nada. Solo escuchar

Recapitulación integrada Con esta sesión cerramos el modelo OSI. Sabemos que cada capa tiene su responsabilidad y sus vulnerabilidades, que un ataque r eal encadena capas distintas, y que la defensa funciona solo si es también por capas. Hemos visto el cifrado TLS como el mecanismo que protege la capa de presentación, las sesiones y tokens como solución al problema de memoria de HTTP, y hemos comprobado e n vivo con Wireshark que la diferencia entre HTTP y HTTPS no es teórica: es la diferencia entre ver unas credenciales en texto claro o ver datos ilegibles. A partir de aquí arranca la fase activa: Metasploitable, enumeración de servicios y las primeras máq uinas vulnerables.

---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[resumen_master_clase14.md|resumen_master_clase14]— Redes, SSH, XSS
- [[../../Apuntes/01 - Fundamentos de Redes/Redes - Modelo OSI y TCP-IP.md|Redes - Modelo OSI y TCP-IP]— Redes, SSH, XSS
- [[../MODULO3/resumen_master_clase25.md|resumen_master_clase25]— Redes, SSH, XSS
- [[../../Apuntes/06 - Explotacion y Post-Explotacion/Explotación Avanzada de Servicios Vulnerables II — Metasploitable.md|Explotación Avanzada de Servicios Vulnerables II — Metasploitable]— Redes, SSH, XSS
- [[../../apuntes Chema/Maquinas/Explotación avanzada de servicios vulnerables II.md|Explotación avanzada de servicios vulnerables II]— Redes, SSH, XSS
- [[../PREWORK/resumen_clase12.md|resumen_clase12]— Redes, SSH, Wireshark

### 🛠️ Herramientas

- [[comandos/BurpSuite|Burp Suite]]
- [[comandos/Nmap|Nmap]]
- [[comandos/SSH|SSH]]

### 🎯 Vulnerabilidades Relacionadas

- [[Apuntes/05 - Auditoria Web/SQL Injection.md|SQL Injection]]
- [[Apuntes/05 - Auditoria Web/SSRF — Server-Side Request Forgery.md|SSRF]]
- [[Apuntes/05 - Auditoria Web/Vulnerabilidades Web — OWASP Top 10 y Burp Suite.md|XSS]]

> #burpsuite #ia #linux #metasploitable #nmap #redes #sqli #ssh #ssrf #wireshark #xss
