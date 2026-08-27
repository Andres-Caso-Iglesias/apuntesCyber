#!/usr/bin/env python3
"""
Validate Neural Network — Verifica enlaces rotos y coherencia de la red neuronal.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent


def validate_links():
    """Valida todos los wikilinks del vault."""
    print("[VALIDATE] Validando red neuronal...")
    print()

    all_files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md'):
                all_files.append(Path(root) / f)

    # Build index of all file stems (Obsidian resolves by stem, not full path)
    # Use .name (filename) and strip .md manually to avoid Path.stem issues with dots in names
    stem_to_files = defaultdict(list)
    for fp in all_files:
        # Get filename without .md extension
        fname = fp.name
        if fname.endswith('.md'):
            stem = fname[:-3]
        else:
            stem = fname
        stem_to_files[stem].append(fp)

    broken_links = []
    total_links = 0
    valid_links = 0
    duplicate_stems = {}

    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        # Find all wikilinks — handle both [[link]] and [[link|display]]
        links = re.findall(r'\[\[([^\]]+?)\]\]', content)
        # For links with |, take only the part before |
        cleaned_links = []
        for link in links:
            if '|' in link:
                link = link.split('|')[0]
            cleaned_links.append(link.strip())
        links = cleaned_links
        total_links += len(links)

        for link in links:
            # Obsidian resolves links by filename without .md
            # Handle path-based links like "apuntes Andres/file" -> extract filename
            link_name = link.split('/')[-1] if '/' in link else link
            # Strip .md if present
            link_stem = link_name[:-3] if link_name.endswith('.md') else link_name
            # Also try the full link as path
            full_stem = link[:-3] if link.endswith('.md') else link

            # Check both
            found = link_stem in stem_to_files or full_stem in stem_to_files

            if not found:
                broken_links.append({
                    "file": str(filepath.relative_to(BASE_DIR)),
                    "link": link,
                    "reason": "Target not found"
                })
            else:
                valid_links += 1
                resolved_stem = link_stem if link_stem in stem_to_files else full_stem
                targets = stem_to_files[resolved_stem]
                if len(targets) > 1:
                    duplicate_stems[resolved_stem] = [str(t.relative_to(BASE_DIR)) for t in targets]

    # Report
    print("=" * 60)
    print("RED NEURONAL — REPORTE DE VALIDACION")
    print("=" * 60)
    print()
    print(f"  Total archivos: {len(all_files)}")
    print(f"  Total enlaces: {total_links}")
    print(f"  Enlaces validos: {valid_links}")
    print(f"  Enlaces rotos: {len(broken_links)}")
    print()

    if broken_links:
        print("ENLACES ROTOS:")
        print("-" * 40)
        for bl in broken_links[:30]:
            print(f"  {bl['file']}")
            print(f"    -> [[{bl['link']}]]")
            print(f"       Reason: {bl['reason']}")
            print()
        if len(broken_links) > 30:
            print(f"  ... y {len(broken_links) - 30} mas")
        print()

    if duplicate_stems:
        print("STEMS DUPLICADOS (puede causar enlaces ambiguos):")
        print("-" * 40)
        for stem, paths in sorted(duplicate_stems.items())[:15]:
            print(f"  '{stem}' -> {len(paths)} archivos:")
            for p in paths:
                print(f"    - {p}")
            print()
        if len(duplicate_stems) > 15:
            print(f"  ... y {len(duplicate_stems) - 15} mas")
        print()

    # Concept distribution
    print("DISTRIBUCION POR DIRECTORIO:")
    print("-" * 40)
    dir_counts = defaultdict(int)
    for fp in all_files:
        rel = str(fp.relative_to(BASE_DIR))
        top_dir = rel.split(os.sep)[0] if os.sep in rel else rel.split('/')[0]
        dir_counts[top_dir] += 1
    for d, c in sorted(dir_counts.items(), key=lambda x: -x[1]):
        print(f"  {d}: {c} archivos")
    print()

    # Network density
    print(f"  Densidad de red: {valid_links/len(all_files):.1f} enlaces/archivo")
    print()

    if not broken_links:
        print("  TODOS LOS ENLACES SON VALIDOS")
    else:
        print(f"  {len(broken_links)} enlaces requieren atencion")

    return broken_links, duplicate_stems


if __name__ == "__main__":
    validate_links()
