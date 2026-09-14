#!/usr/bin/env python3
"""
Neural Linker — Motor de enlace automático para la red neuronal de ciberseguridad.
Analiza todos los .md, extrae conceptos, y genera enlaces bidireccionales.
"""

import os
import re
import json
import sys
import hashlib
from pathlib import Path
from collections import defaultdict, OrderedDict
from typing import Dict, List, Set, Tuple, Any, Optional

# ============================================================
# LRU CACHE — Least Recently Used
# ============================================================

class LRUCache:
    """
    Cache LRU (Least Recently Used) con capacidad fija.
    
    Usa OrderedDict para operaciones O(1):
    - get: busca y mueve al frente (más reciente)
    - put: inserta/actualiza, elimina el menos usado si está lleno
    
    Caso de uso en neural_linker:
    - Cache de texto extraído de archivos (I/O pesado)
    - Cache de conceptos detectados (regex costoso)
    - Cache de similitud entre pares de archivos
    """
    
    def __init__(self, capacity: int = 500):
        """Inicializa el cache con capacidad fija."""
        self.capacity = capacity
        self._cache = OrderedDict()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Busca un valor en el cache.
        Si existe: lo mueve al frente (más reciente) y retorna el valor.
        Si no existe: retorna None y cuenta como miss.
        """
        if key in self._cache:
            self._cache.move_to_end(key)
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        return None
    
    def put(self, key: Any, value: Any) -> None:
        """
        Inserta o actualiza un valor en el cache.
        Si el cache está lleno, elimina el elemento menos usado.
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)  # Elimina el menos reciente
    
    def get_or_compute(self, key: Any, compute_fn, *args, **kwargs) -> Any:
        """
        Busca en cache; si no existe, ejecuta compute_fn y guarda el resultado.
        Patrón memoize: ideal para funciones costosas.
        """
        value = self.get(key)
        if value is not None:
            return value
        value = compute_fn(*args, **kwargs)
        self.put(key, value)
        return value
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del cache."""
        total = self._hits + self._misses
        return {
            "capacity": self.capacity,
            "size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{(self._hits / total * 100):.1f}%" if total > 0 else "0%",
        }
    
    def reset_stats(self) -> None:
        """Resetea estadísticas sin limpiar el cache."""
        self._hits = 0
        self._misses = 0
    
    def clear(self) -> None:
        """Limpia el cache y las estadísticas."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __contains__(self, key: Any) -> bool:
        return key in self._cache


# Instancias globales de cache
_text_cache = LRUCache(capacity=500)      # Cache de texto extraído
_concepts_cache = LRUCache(capacity=500)  # Cache de conceptos detectados
_similarity_cache = LRUCache(capacity=1000)  # Cache de similitud entre pares


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "_neural_network"
OUTPUT_DIR.mkdir(exist_ok=True)

# Mapa de conceptos → patrones regex (con word boundaries donde aplica)
# Para keywords cortas o ambiguas se usa \b para evitar falsos positivos
CONCEPT_MAP = {
    # Vulnerabilidades Web (keywords específicas, no necesitan boundary)
    "sqli": ["sql injection", "sqli", "sqlmap", "inyecci[oó]n sql", "union select", "blind sql", "prepared statement"],
    "xss": ["cross-site scripting", "stored xss", "reflected xss", "dom xss", r"\bxss\b"],
    "xxe": ["xml external entity", r"\bxxe\b"],
    "ssrf": ["server-side request forgery", "blind ssrf", r"\bssrf\b"],
    "ssti": ["server-side template injection", "template injection", r"\bssti\b"],
    "lfi": ["local file inclusion", "path traversal", "directory traversal", r"\blfi\b"],
    "rfi": ["remote file inclusion", r"\brfi\b"],
    "command-injection": ["command injection", "remote code execution", "os command injection", r"\brce\b"],
    "file-upload": ["file upload", "webshell", "reverse shell php", "upload de ficheros"],
    "idor": [r"\bidor\b", "insecure direct object reference"],
    "open-redirect": ["open redirect"],
    "csrf": ["cross-site request forgery", r"\bcsrf\b"],
    "auth-bypass": ["auth bypass", "authentication bypass"],

    # Herramientas (nombres únicos que no matchean en otro contexto)
    "nmap": [r"\bnmap\b", "network mapper", "escaneo de puertos"],
    "metasploit": [r"\bmetasploit\b", "meterpreter", "msfconsole", "msfvenom"],
    "burpsuite": ["burp suite", r"\bburp\b", "repeater", "intruder"],
    "hydra": [r"\bhydra\b", "thc-hydra", "fuerza bruta", "brute force"],
    "ffuf": [r"\bffuf\b", "fuzzing directorios", "web fuzzing"],
    "feroxbuster": [r"\bferoxbuster\b", "fuzzing recursivo"],
    "gobuster": [r"\bgobuster\b", "directory brute", "dns brute", "vhost brute"],
    "sqlmap": [r"\bsqlmap\b"],
    "wpscan": [r"\bwpscan\b"],
    "john": ["john the ripper", r"\bhashcat\b", "cracking hashes", "crack hashes"],
    "smb-impacket": [r"\bimpacket\b", r"\bsmbclient\b", r"\bpsexec\b", r"\bwmiexec\b", r"\bsmbexec\b", r"\bnetexec\b", r"\bcrackmapexec\b"],
    "wireshark": [r"\bwireshark\b", "packet capture", "captura de paquetes", "filtro bpf"],
    "netcat": [r"\bnetcat\b", r"\bncat\b", "reverse shell", "bind shell"],
    "ssh": [r"\bssh\b", "tunel ssh", "ssh tunnel", "port forwarding"],
    "telnet": [r"\btelnet\b"],
    "tmux": [r"\btmux\b"],
    "dirsearch": [r"\bdirsearch\b"],
    "google-dorks": ["google dorks", r"\bdork\b", "site:", "inurl:", "intitle:"],

    # Sistemas Operativos (keywords específicas)
    "linux": [r"\blinux\b", r"\bbash\b", r"\bchmod\b", r"\bsudo\b", r"\bsuid\b", r"\bcron\b", r"\bgtfobins\b", r"\blinpeas\b"],
    "windows": [r"\bwindows\b", r"\bpowershell\b", "active directory", r"\bbloodhound\b", r"\bwinpeas\b", r"\bmimikatz\b"],
    "kali": [r"\bkali\b"],

    # Redes (keywords que NO matchean en otros contextos)
    "redes": [r"\bred\b", r"\bnetwork\b", r"\btopolog[ií]a", r"\bosi\b", r"\btcp/ip\b", r"\bsubnet\b", r"\bcidr\b", r"\bpuerto[s]?\b"],
    "wifi": [r"\bwifi\b", r"\bwpa\b", "evil twin", r"\baircrack\b", "enterprise wifi"],
    "pivoting": [r"\bpivoting\b", "movilidad lateral", r"\bproxychains\b", r"\bsocat\b", r"\bchisel\b"],

    # Metodologias
    "pentest": [r"\bpentest\b", "penetration testing", "fases del pentest", r"\bmetodolog[ií]a\b"],
    "osint": [r"\bosint\b", "reconocimiento pasivo", r"\bshodan\b", r"\bwhois\b", r"\btheharvester\b"],
    "esteganografia": ["esteganograf[ií]a", r"\bsteghide\b", r"\bbinwalk\b", r"\bexif\b"],

    # Explotacion
    "escalada-privilegios": ["escalada de privilegios", "privilege escalation", r"\bsudo -l\b", r"\bcapabilities\b", r"\bcron job\b", r"\bpath hijacking\b"],
    "reverse-shell": ["reverse shell", "shell reversa", "bind shell", "tty upgrade", "estabilizar shell", "python pty"],
    "post-explotacion": ["post-explotaci[oó]n", "post exploitation", "lateral movement", r"\bexfiltration\b"],

    # Defensa (keywords más específicas)
    "blue-team": ["blue team", r"\bsoc\b", r"\bsiem\b", r"\bwazuh\b", r"\bmitre\b", r"\bedr\b"],
    "forense": [r"\bforense\b", r"\bforensic\b", r"\bvolatility\b", "cadena de custodia"],
    "normativa": ["iso 27001", r"\bgdpr\b", r"\bens\b", "pci dss", r"\bdora\b", r"\bnis2\b", r"\bnormativa\b", r"\bgrc\b"],

    # Maquinas
    "wordpress": [r"\bwordpress\b", r"\bwp-admin\b", r"\bwp-login\b", r"\bwp-content\b"],
    "metasploitable": [r"\bmetasploitable\b", r"\bdvwa\b"],
    "hack-the-box": ["hack the box", r"\bhtb\b", r"\bhackthebox\b"],
    "vulnhub": [r"\bvulnhub\b"],

    # Empleabilidad
    "certificaciones": [r"\bcertificaci[oó]n\b", r"\bejpt\b", r"\boscp\b", r"\bcrest\b"],
    "empleabilidad": [r"\bempleabilidad\b", "mercado laboral", r"\bportafolio\b", r"\blinkedin\b"],

    # IA
    "ia": ["inteligencia artificial", "machine learning", "deep learning", r"\bllm[s]?\b", "vibe coding", r"\bchatgpt\b", r"\bclaude\b"],
}

# Mapeo de archivos a nombres legibles para Obsidian
FILE_DISPLAY_NAMES = {}

# Tags por directorio
DIR_TAGS = {
    "Apuntes": "apuntes-organizados",
    "comandos": "cheat-sheet",
    "write-ups": "write-up",
    "informes": "informe-tecnico",
    "transcripciones": "transcripcion",
    "apuntes Chema": "notas-chema",
    "apuntes Andres": "notas-andres",
    "apuntes Joselu": "notas-joselu",
    "apuntes evolve": "bloque-master",
}


# ============================================================
# MOTOR DE ANÁLISIS
# ============================================================

def get_all_markdown_files() -> List[Path]:
    """Encuentra todos los archivos .md del proyecto."""
    files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        # Ignorar directorios ocultos y el de salida
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != "_neural_network"]
        for f in filenames:
            if f.endswith('.md'):
                # Excluir MOCs y archivos de mapa de contenidos
                if "MOC" in f or "Mapa de Contenidos" in root:
                    continue
                files.append(Path(root) / f)
    return sorted(files)


def extract_text_content(filepath: Path) -> str:
    """
    Extrae el contenido de texto de un .md (sin código).
    Usa LRU cache para evitar re-leer archivos del disco.
    """
    cache_key = str(filepath)
    cached = _text_cache.get(cache_key)
    if cached is not None:
        return cached
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return ""

    # Remover bloques de código
    content = re.sub(r'```[\s\S]*?```', '', content)
    # Remover inline code
    content = re.sub(r'`[^`]+`', '', content)
    result = content.lower()
    
    _text_cache.put(cache_key, result)
    return result


def detect_concepts(text: str) -> Set[str]:
    """
    Detecta qué conceptos están presentes en el texto usando regex.
    Usa LRU cache para evitar re-evaluar patrones regex.
    """
    # Usar hash del texto como key (textos largos se hashean)
    cache_key = hashlib.md5(text.encode('utf-8', errors='ignore')).hexdigest()
    cached = _concepts_cache.get(cache_key)
    if cached is not None:
        return cached
    
    found = set()
    for concept, patterns in CONCEPT_MAP.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.add(concept)
                break
    
    _concepts_cache.put(cache_key, found)
    return found


def extract_existing_links(filepath: Path) -> Set[str]:
    """Extrae wikilinks existentes de un archivo."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return set()

    # Buscar [[...]] y [[...|display]]
    raw_links = re.findall(r'\[\[([^\]]+?)\]\]', content)
    links = set()
    for link in raw_links:
        if '|' in link:
            link = link.split('|')[0]
        links.add(link.strip())
    return links


def get_relative_path(from_file: Path, to_file: Path) -> str:
    """Calcula la ruta relativa Obsidian entre dos archivos."""
    try:
        rel = os.path.relpath(to_file, from_file.parent)
        # Convertir \ a / para Obsidian
        return rel.replace('\\', '/')
    except ValueError:
        return str(to_file.name)


def compute_file_similarity(concepts_a: Set[str], concepts_b: Set[str]) -> float:
    """
    Calcula similitud Jaccard entre dos conjuntos de conceptos.
    Usa LRU cache para evitar recalcular pares ya procesados.
    """
    # Key ordenado para que (A,B) y (B,A) den el mismo resultado
    key = tuple(sorted([frozenset(concepts_a), frozenset(concepts_b)]))
    cache_key = str(key)
    
    cached = _similarity_cache.get(cache_key)
    if cached is not None:
        return cached
    
    if not concepts_a or not concepts_b:
        result = 0.0
    else:
        intersection = concepts_a & concepts_b
        union = concepts_a | concepts_b
        result = len(intersection) / len(union)
    
    _similarity_cache.put(cache_key, result)
    return result


def find_related_files(
    current_file: Path,
    all_files_data: Dict[Path, Dict],
    top_n: int = 8
) -> List[Tuple[Path, float, Set[str]]]:
    """Encuentra los archivos más relacionados con uno dado."""
    current_concepts = all_files_data[current_file]["concepts"]
    if not current_concepts:
        return []

    similarities = []
    for other_file, other_data in all_files_data.items():
        if other_file == current_file:
            continue
        sim = compute_file_similarity(current_concepts, other_data["concepts"])
        if sim > 0.05:  # Umbral mínimo de similitud
            shared = current_concepts & other_data["concepts"]
            similarities.append((other_file, sim, shared))

    # Ordenar por similitud descendente
    similarities.sort(key=lambda x: (-x[1], -len(x[2])))
    return similarities[:top_n]


def get_concept_display_name(concept: str) -> str:
    """Nombre legible de un concepto."""
    names = {
        "sqli": "SQL Injection",
        "xss": "XSS",
        "xxe": "XXE",
        "ssrf": "SSRF",
        "ssti": "SSTI",
        "lfi": "Path Traversal / LFI",
        "rfi": "RFI",
        "command-injection": "Command Injection / RCE",
        "file-upload": "File Upload",
        "idor": "IDOR",
        "open-redirect": "Open Redirect",
        "csrf": "CSRF",
        "auth-bypass": "Auth Bypass",
        "nmap": "Nmap",
        "metasploit": "Metasploit",
        "burpsuite": "Burp Suite",
        "hydra": "Hydra",
        "ffuf": "FFUF",
        "feroxbuster": "Feroxbuster",
        "gobuster": "GoBuster",
        "sqlmap": "SQLMap",
        "wpscan": "WPScan",
        "john": "John / Hashcat",
        "smb-impacket": "SMB / Impacket",
        "wireshark": "Wireshark",
        "netcat": "Netcat / Reverse Shells",
        "ssh": "SSH",
        "telnet": "Telnet",
        "tmux": "Tmux",
        "dirsearch": "DirSearch",
        "google-dorks": "Google Dorks",
        "linux": "Linux",
        "windows": "Windows",
        "kali": "Kali Linux",
        "redes": "Redes",
        "wifi": "WiFi / Hardware",
        "pivoting": "Pivoting / Movilidad Lateral",
        "pentest": "Metodología Pentest",
        "osint": "OSINT",
        "esteganografia": "Esteganografía",
        "escalada-privilegios": "Escalada de Privilegios",
        "reverse-shell": "Reverse Shells",
        "post-explotacion": "Post-Explotación",
        "blue-team": "Blue Team / SOC",
        "forense": "Forense Digital",
        "normativa": "Normativa / GRC",
        "wordpress": "WordPress",
        "metasploitable": "Metasploitable / DVWA",
        "hack-the-box": "Hack The Box",
        "vulnhub": "VulnHub",
        "certificaciones": "Certificaciones",
        "empleabilidad": "Empleabilidad",
        "ia": "IA en Ciberseguridad",
    }
    return names.get(concept, concept.replace("-", " ").title())


# ============================================================
# GENERACIÓN DE ENLACES
# ============================================================

def generate_link_section(
    current_file: Path,
    related_files: List[Tuple[Path, float, Set[str]]],
    existing_links: Set[str],
    all_files_data: Dict[Path, Dict]
) -> str:
    """Genera la sección de enlaces para un archivo."""
    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔗 Red de Conocimiento")
    lines.append("")

    current_concepts = all_files_data[current_file]["concepts"]

    # 1. Enlaces a conceptos relacionados (otros archivos con mismos conceptos)
    if related_files:
        lines.append("### Documentos Relacionados")
        lines.append("")
        for related_path, sim, shared_concepts in related_files:
            rel_path = get_relative_path(current_file, related_path)
            display = all_files_data[related_path].get("display_name", related_path.stem)
            concept_str = ", ".join(sorted([get_concept_display_name(c) for c in list(shared_concepts)[:3]]))
            lines.append(f"- [[{rel_path}|{display}]] — {concept_str}")
        lines.append("")

    # 2. Herramientas mencionadas (enlaces a cheat sheets)
    tool_concepts = {"nmap", "metasploit", "burpsuite", "hydra", "ffuf", "feroxbuster",
                     "gobuster", "sqlmap", "wpscan", "john", "smb-impacket", "wireshark",
                     "netcat", "ssh", "telnet", "tmux", "dirsearch", "google-dorks"}
    mentioned_tools = current_concepts & tool_concepts
    if mentioned_tools:
        lines.append("### 🛠️ Herramientas")
        lines.append("")
        for tool in sorted(mentioned_tools):
            tool_file = BASE_DIR / "comandos" / f"{tool_map_filename(tool)}.md"
            if tool_file.exists():
                lines.append(f"- [[comandos/{tool_map_filename(tool)}|{get_concept_display_name(tool)}]]")
        lines.append("")

    # 3. Vulnerabilidades relacionadas (excluyendo auto-referencia)
    vuln_concepts = {"sqli", "xss", "xxe", "ssrf", "ssti", "lfi", "rfi", "command-injection",
                     "file-upload", "idor", "open-redirect", "csrf", "auth-bypass"}
    mentioned_vulns = current_concepts & vuln_concepts
    # Remover el concepto del propio archivo para evitar auto-referencia
    current_filename = current_file.stem.lower()
    vuln_file_map = {
        "sqli": ("Apuntes/05 - Auditoria Web/SQL Injection.md", "SQL Injection"),
        "xss": ("Apuntes/05 - Auditoria Web/Vulnerabilidades Web - OWASP Top 10 y Burp Suite.md", "XSS"),
        "xxe": ("Apuntes/05 - Auditoria Web/XXE - XML External Entity.md", "XXE"),
        "ssrf": ("Apuntes/05 - Auditoria Web/SSRF - Server-Side Request Forgery.md", "SSRF"),
        "ssti": ("Apuntes/05 - Auditoria Web/SSTI - Server-Side Template Injection.md", "SSTI"),
        "lfi": ("Apuntes/05 - Auditoria Web/Path Traversal - 6 Casos y Bypasses.md", "Path Traversal / LFI"),
        "command-injection": ("Apuntes/06 - Explotacion y Post-Explotacion/Reverse Shells y Post-Explotación.md", "Command Injection / RCE"),
    }
    if mentioned_vulns:
        lines.append("### 🎯 Vulnerabilidades Relacionadas")
        lines.append("")
        for vuln in sorted(mentioned_vulns):
            if vuln in vuln_file_map:
                vuln_path, vuln_name = vuln_file_map[vuln]
                # Evitar auto-referencia
                vuln_filename = Path(vuln_path).stem.lower()
                if vuln_filename != current_filename:
                    lines.append(f"- [[{vuln_path}|{vuln_name}]]")
        lines.append("")

    # 4. Tags de conceptos
    if current_concepts:
        tags = " ".join([f"#{c}" for c in sorted(current_concepts)])
        lines.append(f"> {tags}")
        lines.append("")

    return "\n".join(lines)


def tool_map_filename(tool: str) -> str:
    """Mapea nombre de concepto a nombre de archivo de cheat sheet."""
    mapping = {
        "nmap": "Nmap",
        "metasploit": "Metasploit",
        "burpsuite": "BurpSuite",
        "hydra": "Hydra",
        "ffuf": "FFUF",
        "feroxbuster": "Feroxbuster",
        "gobuster": "GoBuster",
        "sqlmap": "SQLMap",
        "wpscan": "WPScan",
        "john": "John_Hashcat",
        "smb-impacket": "SMB_Impacket",
        "wireshark": "Wireshark",
        "netcat": "Metasploit",  # Netcat se usa junto con Metasploit para reverse shells
        "ssh": "SSH",
        "telnet": "Telnet",
        "tmux": "Tmux",
        "dirsearch": "DirSearch",
        "google-dorks": "Google_Dorks",
    }
    return mapping.get(tool, tool)


# ============================================================
# PROCESAMIENTO PRINCIPAL
# ============================================================

def process_all_files(use_cache: bool = True):
    """Procesa todos los archivos y genera el grafo de conocimiento."""
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Deshabilitar cache si se solicita
    if not use_cache:
        _text_cache.clear()
        _concepts_cache.clear()
        _similarity_cache.clear()
        print("[NEURAL] Cache deshabilitado (--no-cache)")
    
    print("[NEURAL] Neural Linker — Analizando red de conocimiento...")
    print(f"   Directorio base: {BASE_DIR}")
    print()

    # 1. Encontrar todos los archivos
    all_files = get_all_markdown_files()
    print(f"📄 Archivos encontrados: {len(all_files)}")
    print()

    # 2. Analizar cada archivo
    all_files_data = {}
    for filepath in all_files:
        text = extract_text_content(filepath)
        concepts = detect_concepts(text)
        existing_links = extract_existing_links(filepath)

        # Nombre legible
        rel_path = str(filepath.relative_to(BASE_DIR))
        display_name = filepath.stem

        all_files_data[filepath] = {
            "text": text,
            "concepts": concepts,
            "existing_links": existing_links,
            "display_name": display_name,
            "rel_path": rel_path,
        }

    # 3. Estadísticas de conceptos
    concept_counter = defaultdict(int)
    for data in all_files_data.values():
        for c in data["concepts"]:
            concept_counter[c] += 1

    print("📊 Conceptos más frecuentes:")
    for concept, count in sorted(concept_counter.items(), key=lambda x: -x[1])[:15]:
        print(f"   {get_concept_display_name(concept)}: {count} archivos")
    print()

    # Estadísticas del cache
    print("💾 Estadísticas del LRU Cache:")
    print(f"   Texto extraído: {_text_cache.stats['hits']} hits / {_text_cache.stats['misses']} misses ({_text_cache.stats['hit_rate']})")
    print(f"   Conceptos detectados: {_concepts_cache.stats['hits']} hits / {_concepts_cache.stats['misses']} misses ({_concepts_cache.stats['hit_rate']})")
    print(f"   Similitud calculada: {_similarity_cache.stats['hits']} hits / {_similarity_cache.stats['misses']} misses ({_similarity_cache.stats['hit_rate']})")
    print()

    # 4. Generar relaciones
    relationships = {}
    total_links = 0
    for filepath in all_files:
        related = find_related_files(filepath, all_files_data, top_n=6)
        relationships[filepath] = related
        total_links += len(related)

    print(f"🔗 Enlaces generados: {total_links}")
    print()

    # 5. Generar reporte JSON
    report = {
        "total_files": len(all_files),
        "total_concepts": len(concept_counter),
        "total_links": total_links,
        "concept_frequency": dict(sorted(concept_counter.items(), key=lambda x: -x[1])),
        "files_by_concept": {},
        "relationship_graph": {},
    }

    # Archivos por concepto
    for concept in sorted(concept_counter.keys()):
        files_with_concept = [
            str(fp.relative_to(BASE_DIR))
            for fp, data in all_files_data.items()
            if concept in data["concepts"]
        ]
        report["files_by_concept"][concept] = files_with_concept

    # Grafo de relaciones
    for filepath, related in relationships.items():
        rel = str(filepath.relative_to(BASE_DIR))
        report["relationship_graph"][rel] = [
            {
                "file": str(r[0].relative_to(BASE_DIR)),
                "similarity": round(r[1], 3),
                "shared_concepts": sorted(list(r[2]))
            }
            for r in related
        ]

    # Guardar reporte
    report_path = OUTPUT_DIR / "neural_graph.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"📋 Reporte guardado: {report_path}")

    # 6. Generar secciones de enlace para cada archivo
    print()
    print("⚡ Generando enlaces por archivo...")

    link_sections = {}
    for filepath in all_files:
        related = relationships[filepath]
        existing = all_files_data[filepath]["existing_links"]

        # Solo generar si tiene conceptos
        if not all_files_data[filepath]["concepts"]:
            continue

        link_section = generate_link_section(filepath, related, existing, all_files_data)
        link_sections[str(filepath.relative_to(BASE_DIR))] = link_section

    # Guardar secciones de enlace
    sections_path = OUTPUT_DIR / "link_sections.json"
    with open(sections_path, 'w', encoding='utf-8') as f:
        json.dump(link_sections, f, indent=2, ensure_ascii=False)
    print(f"   Secciones de enlace: {len(link_sections)} archivos")
    print(f"   Guardado en: {sections_path}")

    # 7. Resumen
    print()
    print("=" * 60)
    print("✅ NEURAL LINKER — COMPLETADO")
    print("=" * 60)
    print(f"   📄 Archivos analizados: {len(all_files)}")
    print(f"   🧠 Conceptos detectados: {len(concept_counter)}")
    print(f"   🔗 Enlaces generados: {total_links}")
    print(f"   📋 Reporte: {report_path}")
    print(f"   ⚡ Secciones: {sections_path}")
    print()
    print("   Para inyectar los enlaces en cada archivo, ejecuta:")
    print("   python inject_links.py")
    print()


if __name__ == "__main__":
    # Flags de línea de comandos
    use_cache = "--no-cache" not in sys.argv
    process_all_files(use_cache=use_cache)
