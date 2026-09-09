#!/usr/bin/env python3
"""
Inject Links — Inyecta las secciones de enlace generadas por neural_linker.py
en cada archivo markdown. Agrega enlaces bidireccionales al final del archivo.
"""

import json
import os
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "_neural_network"
SECTIONS_FILE = OUTPUT_DIR / "link_sections.json"


def inject_links():
    """Inyecta o reemplaza las secciones de enlace en cada archivo."""
    if not SECTIONS_FILE.exists():
        print("❌ No se encontró link_sections.json. Ejecutá neural_linker.py primero.")
        return

    with open(SECTIONS_FILE, 'r', encoding='utf-8') as f:
        sections = json.load(f)

    print(f"⚡ Procesando {len(sections)} archivos...")
    print()

    injected = 0
    updated = 0
    skipped = 0

    for file_path, section in sections.items():
        # Excluir MOCs y archivos de mapa de contenidos
        if "MOC" in file_path or "Mapa de Contenidos" in file_path:
            continue

        full_path = BASE_DIR / file_path

        if not full_path.exists():
            print(f"  ⚠️ No existe: {file_path}")
            skipped += 1
            continue

        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"  ❌ Error leyendo {file_path}: {e}")
            skipped += 1
            continue

        # Si ya tiene la sección, reemplazarla
        if "## 🔗 Red de Conocimiento" in content:
            # Cortar antes de la sección existente
            idx = content.index("## 🔗 Red de Conocimiento")
            # Buscar el separador --- que va antes de la sección
            separator_idx = content.rfind("\n---\n", 0, idx)
            if separator_idx != -1:
                new_content = content[:separator_idx] + "\n" + section
            else:
                new_content = content[:idx].rstrip() + "\n" + section
            action = "updated"
        else:
            # Inyectar al final
            new_content = content.rstrip() + "\n" + section
            action = "injected"

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            if action == "updated":
                print(f"  🔄 {file_path}")
                updated += 1
            else:
                print(f"  ✅ {file_path}")
                injected += 1
        except Exception as e:
            print(f"  ❌ Error escribiendo {file_path}: {e}")
            skipped += 1

    print()
    print(f"✅ Completado: {injected} nuevos, {updated} actualizados, {skipped} saltados")


if __name__ == "__main__":
    inject_links()
