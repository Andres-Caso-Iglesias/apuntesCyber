#!/usr/bin/env python3
"""Renombra archivos de Chema usando guiones largos a guiones normales."""
import os
from pathlib import Path

BASE = Path(r"C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad")

EM_DASH = "\u2014"  # —

FILES_TO_RENAME = [
    f"apuntes Chema\\Maquinas\\Vaccine (Tier 2) {EM_DASH} Repaso en profundidad.md",
    f"apuntes Chema\\Maquinas\\Rockstar {EM_DASH} Escalada Linux y LFI.md",
    f"apuntes Chema\\Maquinas\\HTB Starting Point {EM_DASH} Repaso e inicio de Tier 2.md",
    f"apuntes Chema\\Maquinas\\HackTheBox Starting Point {EM_DASH} Tier 1.md",
    f"apuntes Chema\\Maquinas\\Hack The Box- Starting Point {EM_DASH} Tier 0.md",
    f"apuntes Chema\\Maquinas\\Fuzzing de par\u00e1metros con x8 {EM_DASH} Rockstar.md",
    f"apuntes Chema\\Maquinas\\Auditor\u00eda de CMS {EM_DASH} WordPress (m\u00e1quina Academy).md",
    f"apuntes Chema\\IA\\IA {EM_DASH} Redes Neuronales.md",
    f"apuntes Chema\\IA\\IA {EM_DASH} Introducci\u00f3n y VibeCoding.md",
    f"apuntes Chema\\IA\\IA {EM_DASH} De los cimientos a la cima.md",
]

for old_rel in FILES_TO_RENAME:
    old_path = BASE / old_rel
    # Reemplazar em-dash por guion normal
    new_leaf = old_path.name.replace("\u2014", "-")
    new_path = old_path.parent / new_leaf
    
    if old_path.exists():
        old_path.rename(new_path)
        print(f"OK: {old_rel} -> {new_leaf}")
    else:
        print(f"NO EXISTE: {old_rel}")
