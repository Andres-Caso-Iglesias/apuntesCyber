

> [!info] Relacionado con
> [[Portafolio y Visibilidad]] · [[MOC - Ciberseguridad]] · [[Certificaciones - ISO 27001 y eJPTv2]] · [[Normativa - ISO 27001, GDPR, ENS]]

---

## ① Ciberseguridad ≠ Programación

| Aspecto | Programación | Ciberseguridad |
|---------|------------|----------------|
| **Formación** | Bootcamp 6-9 meses = suficiente | **Mínimo** 1-2 años (experiencia práctica) |
| **Evidencia** | GitHub con código funcional | Portfolio + certificaciones + práctica + presencia pública |
| **Entrada** | Jr dev al instante | Junior level = muy difícil (requisitos altísimos) |
| **Demanda** | Alta pero saturada | Alta pero filtrada por barrera de entrada |
| **Diferenciador** | Código limpio + diseño | Hacker con visibilidad + certificaciones reconocidas |

> [!warning] REALIDAD
> En ciberseguridad, el simple hecho de "haber aprendido" no basta. Necesitas **evidencia visible** de tus habilidades.

> [!important] LOS 6 SEGUNDOS
> Un reclutador toma la decisión de seguir leyendo o descartar tu perfil en los **primeros 6 segundos**. Lo que diferencia: evidencia real, no el CV.

| Elemento | Impacto en selección |
|---------|---------------------|
| CV + LinkedIn | Mínimo indispensable. Si solo tienes esto, eres uno más |
| Portafolio técnico | Te coloca automáticamente en el top de candidatos |
| CTFs y certificaciones | Demuestra habilidad práctica verificable |
| Contribuciones Open Source | Código real, visible, verificable |
| Artículos técnicos | Visibilidad y demostración de conocimiento |

### Salarios de referencia (mercado español)

| Nivel | Salario |
|-------|---------|
| Junior 1 (con eJPT) | 24.500 – 28.000€ iniciales |
| Junior (pocos años) | ~30.000€ |
| Senior / Gestión | 55.000€+ |
| Dirección | 120.000€+ |

---

## ②bis Proceso de selección en ciberseguridad

```
CV/LinkedIn filtra → Prueba técnica / CTF → Entrevista técnica → Entrevista cultural → Oferta
```

| Fase | Qué evalúan |
|------|-----------|
| Prueba técnica | CTF corto, análisis de vulnerabilidades, ejercicio de código |
| Entrevista técnica | Herramientas, metodologías, CVEs conocidos, laboratorios |
| Entrevista cultural | Soft skills, trabajo en equipo, comunicación con clientes |
| Negociación | Conoce tu valor: investiga salarios del sector antes |

> [!tip] PREPARACIÓN
> Para entrevistas técnicas: estudia el **OWASP Top 10**, practica explicar vulnerabilidades (XSS, SQLi, LFI) **en voz alta**, y ten 2-3 laboratorios de HTB que puedas explicar en detalle.

---

## ② Nivel junior en ciberseguridad

- No existe el "casi junior" → no te contratan si no puedes **demostrar** lo que sabes
- Los hackers buenos trabajan para sí mismos (bug bounty, CTFs) o son contratados
- **No esperes a tener título para empezar a demostrar** → CTFs y plataformas
- Las certificaciones no te garantizan nada pero **abren puertas** (y exigen conocimiento real)
- Las empresas no contratan "alguien que estudia" → contratan **alguien que hackea**

> [!important] CLAVE
> Las empresas buscan personas que **demuestren** habilidades, no personas que estudien. La práctica constante es lo que marca la diferencia.

---

## ③ Competencias que se valoran (no solo técnicas)

| Competencia | Ejemplo en entrevista |
|------------|----------------------|
| **Mentalidad de aprendizaje continuo** | Certificaciones + estudios propios + blog |
| **Resolución de problemas** | Experiencia en retos/CDF |
| **Pensamiento crítico** | Experiencia en pentesting/auditoría |
| **Comunicación** | Hablar claro, explicar hallazgos técnicos |
| **Adaptabilidad** | Stack overflow → aprendizaje autónomo |

> [!tip] PARA ENTREVISTA TÉCNICA
> - **No memorices** → **comprende** el porqué de cada técnica
> - **No repitas** → **genera** soluciones propias
> - **No te limites** → **practica** y **aplica** en entornos reales
> - **No te compares** → **comprométete** a mejorar cada día

---

## ④ Entrevista técnica: qué preguntan

### Preguntas frecuentes

- ¿Cuáles son las 3 fases de un pentest?
- ¿Cómo hacer enumeración de un dominio?
- ¿Qué es y cómo funciona un ataque de fuerza bruta?
- ¿Qué es el secuestro de sesiones?
- ¿Cómo mitigar una vulnerabilidad XSS?

### Qué se evalúa

- **Conocimientos técnicos** (no memorizados)
- **Razonamiento** ante situaciones prácticas
- **Habilidad para resolver problemas**
- **Habilidad para comunicar** soluciones de forma clara

---

## ⑤ Certificaciones principales

### EC-Council (CEH)

| Aspecto | Detalle |
|---------|---------|
| **Formato** | Examen teórico (125 preguntas, 4 horas) + 20 horas prácticas (iLabs) |
| **Mínimo** | 65% para aprobar |
| **Coste** | ~$400 USD (examen + 1 año acceso iLabs) |
| **Para qué sirve** | Requisito de muchas empresas (filtros RH), base para pentesting |
| **Qué cubre** | Metodología completa de hacking ético |

> [!warning] RECOMENDACIÓN
> Haz el **CEH Master** o **CEH Practical** si puedes. Las empresas lo valoran mucho.

### CompTIA Security+

| Aspecto | Detalle |
|---------|---------|
| **Nivel** | Fundamental |
| **Para qué** | Puerta de entrada, muchas empresas lo exigen |
| **Qué cubre** | Conceptos básicos de seguridad |

### Ruta recomendada de certificaciones ofensivas

```
eJPT → PNPT o eCPPT → OSCP
```

- **eJPT** (INE): primera cert ofensiva práctica, objetivo inmediato del máster
- **PNPT** (TCM Security): práctica, asequible, muy valorada en la comunidad
- **eCPPT** (eLearnSecurity): siguiente paso al eJPT
- **OSCP** (Offensive Security): **estándar de oro** del pentesting; objetivo a 1-2 años

### Otras por área

| Certificación | Nivel | Enfoque |
|--------------|-------|---------|
| **OSCP** | Avanzado | Pentesting práctico (el más respetado) |
| **OSEP** | Avanzado | Evasión y desarrollo de herramientas propias |
| **OSWE** | Avanzado | Pentesting web |
| **OSWP** | Avanzado | WiFi |
| **CompTIA PenTest+** | Intermedio | Ofensivo general |
| **CISSP** | Senior/Gestión | Seguridad empresarial |
| **CISM** | Gestión | Gestión de seguridad |
| **CompTIA CySA+** | Analista | Análisis de seguridad (defensivo) |
| **GSEC / GCFA / GCIH (SANS)** | Defensiva | Entrada / Forense / Incidentes y threat hunting |
| **BSCP (Burp Suite)** | Web | Explotación XSS y SQLi con Burp |
| **CRTP (Altered Security)** | AD | Ataques avanzados a Active Directory |
| **Cloud (AWS/GCP/Azure Security)** | Cloud | Especialización cloud |

---

## ⑥ Plataformas de práctica (CTFs)

| Plataforma | Tipo | Coste |
|-----------|------|-------|
| **Hack The Box** | Retos y máquinas | Gratis (básico) |
| **TryHackMe** | Guiado, walkthroughs | Gratis (básico) |
| **VulnHub** | Máquinas descargables | Gratis |
| **PentesterLab** | Ejercicios web | Pago |
| **Bug Bounty** | Programas reales | Pago si encuentras bugs |

### Otras plataformas y eventos

| Plataforma | Nota |
|-----------|------|
| **CTFtime.org** | Calendario de competiciones CTF a nivel mundial |
| **PicoCTF** | Orientada a estudiantes, buena para empezar |
| **PortSwigger Web Academy** | La mejor para aprender y practicar hacking web |
| **Bug Bounty (HackerOne, Bugcrowd)** | Un CVE propio tiene muchísimo valor en el CV |

### Momentos clave para buscar trabajo

| Momento | Observación |
|---------|------------|
| Enero–Febrero | Presupuestos nuevos, mucho contratar a inicio de año |
| Septiembre–Octubre | Vuelta de vacaciones, segundo pico |
| Ferias / conferencias | Networking presencial (RootedCON, NavajaNegra); conecta en LinkedIn ese mismo día |
| **Evitar** | Agosto y diciembre: menor actividad de RRHH |

> [!tip] IMPORTANCIA DE LOS CTF
> No es solo aprender: es **demostrar** que puedes resolver problemas en entornos reales. Las empresas los valoran muchísimo. **Las certificaciones son el primer paso para que las empresas vean lo que sabes.**

> [!important] WRITEUPS
> Resolver un CTF y **documentar el proceso** (writeup) demuestra mucho más que solo resolver el reto. Publicar writeups en blog o GitHub = visibilidad + portafolio.

---

## Checklist de repaso

- [ ] ¿Entiendo por qué ciberseguridad ≠ programación en cuanto a barrera de entrada?
- [ ] ¿Conozco las principales certificaciones y cuándo sacar cada una?
- [ ] ¿Sé qué preguntan en una entrevista técnica de ciberseguridad?
- [ ] ¿Tengo claro que necesito evidencia visible (portfolio + CTFs + presencia)?
- [ ] ¿Conozco las plataformas de práctica y sé cómo diferenciar?









---

## 🔗 Red de Conocimiento

### Documentos Relacionados

- [[Portafolio y Visibilidad.md|Portafolio y Visibilidad]] — Esteganografia, Hack The Box, Seguridad
- [[../../README.md|README]] — Esteganografia, Hack The Box, Redes
- [[../04 - OSINT y Recopilacion/Esteganografía y Metadatos.md|Esteganografía y Metadatos]] — Esteganografia, Hack The Box, Redes
- [[../05 - Auditoria Web/Burp Suite - Framework de Auditoría.md|Burp Suite - Framework de Auditoría]] — Esteganografia, Hack The Box, Seguridad
- [[../../apuntes Chema/Empleabilidad en Ciberseguridad.md|Empleabilidad en Ciberseguridad]] — Hack The Box, Redes, XSS

### 🌐 Cross-Dominio

- [[../../../programacion/Docker/containers_seguridad.md|containers_seguridad]] — Programacion: Desarrollo Web, Funcional, Seguridad
- [[../../../programacion/Docker/compose_avanzado.md|compose_avanzado]] — Programacion: Docker, Funcional, Seguridad

> #burpsuite #certificaciones #docker #empleabilidad #esteganografia #funcional #git #hack_the_box #hydra #normativa #osint #pentest #redes #seguridad #vulnhub #web #xss
