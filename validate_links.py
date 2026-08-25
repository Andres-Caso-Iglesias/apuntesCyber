#!/usr/bin/env python3
"""
Validador de enlaces wiki [[ ]] en toda la biblioteca.
Uso: python validate_links.py [--fix] [--report]
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set

ROOT = Path(r"C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad")
WIKI_LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def find_all_md_files() -> List[Path]:
    return list(ROOT.rglob("*.md"))

def build_file_index(files: List[Path]) -> Dict[str, Path]:
    """Mapea nombre base (sin .md) y rutas relativas a Path real."""
    index = {}
    for f in files:
        # Clave 1: nombre sin extensión
        index[f.stem.lower()] = f
        # Clave 2: ruta relativa desde ROOT (normalizada, CON slash)
        rel = f.relative_to(ROOT).as_posix().lower()
        rel_no_ext = rel.replace('.md', '')
        index[rel_no_ext] = f
        # Clave 3: también guardar con guiones en lugar de slashes
        index[rel_no_ext.replace('/', '-')] = f
        # Clave 4: solo nombre archivo sin extensión (para links simples)
        index[f.name.lower().replace('.md', '')] = f
        # Clave 5: con guiones en lugar de espacios
        index[f.stem.lower().replace(' ', '-')] = f
    return index

def normalize_link(link: str) -> str:
    """Normaliza un link wiki para búsqueda."""
    # Quitar alias [[archivo|alias]] -> archivo
    target = link.split('|')[0].strip()
    # QUITAR ANCHOR: quitar todo después de # (sección interna)
    target = target.split('#')[0]
    # Normalizar: minúsculas, espacios a guiones, quitar .md
    # También reemplazar / por - para coincidir con claves del índice
    return target.lower().replace(' ', '-').replace('.md', '').replace('/', '-')

def resolve_wiki_link(link: str, index: Dict[str, Path]) -> Tuple[bool, Path | None]:
    """Intenta resolver un link [[...]] a un archivo real."""
    # Manejar pipes escapados (\|) en el contenido
    link = link.replace('\\|', '|')
    target = link.split('|')[0].strip()
    # QUITAR ANCHOR: quitar todo después de # (sección interna)
    target = target.split('#')[0]
    
    # Probar variaciones normalizadas
    variants = [
        target.lower(),
        target.lower().replace(' ', '-'),
        target.lower().replace(' ', ''),
        normalize_link(target),
    ]
    
    for var in variants:
        if var in index:
            return True, index[var]
    
    # Búsqueda parcial (contiene)
    for idx_key, idx_path in index.items():
        if any(v in idx_key for v in variants if v):
            return True, idx_path
    
    return False, None

def find_wiki_links(content: str) -> List[str]:
    """Encuentra todos los links [[...]] en el contenido, ignorando bloques de código."""
    links = []
    in_code_block = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            links.extend(WIKI_LINK_RE.findall(line))
    return links

def validate_all() -> Dict:
    files = find_all_md_files()
    index = build_file_index(files)
    
    results = {
        'total_files': len(files),
        'total_links': 0,
        'resolved': 0,
        'broken': [],
        'by_file': {}
    }
    
    for f in files:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"Error leyendo {f}: {e}")
            continue
            
        links = find_wiki_links(content)
        results['total_links'] += len(links)
        
        file_broken = []
        for link in links:
            ok, target = resolve_wiki_link(link, index)
            if ok:
                results['resolved'] += 1
            else:
                rel_path = f.relative_to(ROOT).as_posix()
                results['broken'].append((rel_path, link))
                file_broken.append(link)
        
        if file_broken:
            results['by_file'][str(f.relative_to(ROOT))] = file_broken
    
    return results

def print_report(results: Dict):
    print(f"\n{'='*60}")
    print(f"VALIDACION DE ENLACES WIKI [[ ]]")
    print(f"{'='*60}")
    print(f"Archivos .md escaneados: {results['total_files']}")
    print(f"Total enlaces [[ ]] encontrados: {results['total_links']}")
    print(f"Resueltos correctamente: {results['resolved']}")
    print(f"ROTOS: {len(results['broken'])}")
    if results['total_links'] > 0:
        print(f"Tasa de éxito: {results['resolved']/max(1,results['total_links'])*100:.1f}%")
    
    if results['broken']:
        print(f"\n[ROTOS] ENLACES ROTOS ({len(results['broken'])}):")
        # Agrupar por archivo destino solicitado
        by_target = {}
        for file_rel, link in results['broken']:
            if link not in by_target:
                by_target[link] = []
            by_target[link].append(file_rel)
        
        for link, files in sorted(by_target.items(), key=lambda x: -len(x[1])):
            print(f"\n  [[{link}]] -- referenciado en {len(files)} archivo(s):")
            for f in files[:5]:
                print(f"    [FILE] {f}")
            if len(files) > 5:
                print(f"    ... y {len(files)-5} mas")
    
    if results['by_file']:
        print(f"\n[STATS] POR ARCHIVO ORIGEN (top 10 con mas rotos):")
        sorted_files = sorted(results['by_file'].items(), key=lambda x: -len(x[1]))
        for file_rel, broken_links in sorted_files[:10]:
            print(f"  {file_rel}: {len(broken_links)} rotos")
            for link in broken_links[:3]:
                print(f"    -> [[{link}]]")
            if len(broken_links) > 3:
                print(f"    ... y {len(broken_links)-3} mas")

if __name__ == "__main__":
    results = validate_all()
    print_report(results)
    
    if '--fix' in sys.argv:
        print("\n⚠️  Modo --fix no implementado (requiere lógica de renombrado seguro)")
    
    sys.exit(1 if results['broken'] else 0)