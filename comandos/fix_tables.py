#!/usr/bin/env python3
"""Fix broken table formatting in markdown files.
Converts pipe-separated two-column text back to readable markdown,
while preserving genuine markdown tables.
"""
import os
import re
import sys

DIR = r"C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad\comandos"
SKIP = {"00 - Indice de Comandos.md", "fix_tables.py"}

def is_table_line(line):
    """Check if a line looks like a table row: starts/ends with | and has content between."""
    stripped = line.strip()
    if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 4:
        # Check it has at least one interior |
        inner = stripped[1:-1]
        if "|" in inner:
            return True
    return False

def is_separator_line(line):
    """Check if line is a table separator like |---|---|"""
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return False
    inner = stripped[1:-1]
    parts = inner.split("|")
    for part in parts:
        part = part.strip()
        if part and not re.match(r'^[-:\s]+$', part):
            return False
    return True

def is_metadata_header(line):
    """Check if line is part of the metadata header block."""
    stripped = line.strip()
    if stripped.startswith("| > Contenido extraido del documento original."):
        return True
    if stripped.startswith("| EVOLVE ACADEMY") or stripped.startswith("| Apuntes") or stripped.startswith("| Explotación") or stripped.startswith("| Hack The Box") or stripped.startswith("| Sesión"):
        return True
    if "Instructor:" in stripped or "Instructor:" in stripped:
        return True
    if "Temas:" in stripped or "Temas:" in stripped:
        return True
    if stripped.startswith("| Campo") or stripped.startswith("| Sesión") or stripped.startswith("| Plataforma"):
        return True
    return False

def split_pipe_line(line):
    """Split a pipe-separated line into two parts.
    Returns (part1, part2) or (line, None) if not splittable.
    """
    stripped = line.strip()
    # Remove leading | and trailing |
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    stripped = stripped.strip()
    
    # Split on ' | ' (space-pipe-space) - the most common separator
    parts = stripped.split(" | ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    # Try splitting on ' |' or '| ' if no space-pipe-space
    parts = stripped.split("|", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    return stripped, None

def process_file(filepath):
    """Process a single markdown file, fixing broken table formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output = []
    i = 0
    in_metadata = False
    skip_next_separator = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines (preserve them)
        if not stripped:
            output.append('\n')
            i += 1
            continue
        
        # Detect metadata header block (after > [!note] line)
        if stripped.startswith("> [!note]"):
            output.append(line)
            i += 1
            # Check if next lines are metadata
            while i < len(lines):
                next_stripped = lines[i].strip()
                if not next_stripped:
                    output.append(lines[i])
                    i += 1
                    continue
                if is_table_line(next_stripped):
                    # Check if this is the metadata header
                    if (next_stripped.startswith("| > Contenido extraido") or 
                        next_stripped.startswith("| EVOLVE") or
                        next_stripped.startswith("| Apuntes") or
                        next_stripped.startswith("| Explotación") or
                        next_stripped.startswith("| Hack The Box") or
                        next_stripped.startswith("| Sesión") or
                        "Instructor:" in next_stripped or
                        "Temas:" in next_stripped or
                        next_stripped.startswith("| Campo") or
                        next_stripped.startswith("| Continuación") or
                        next_stripped.startswith("| Bloque")):
                        in_metadata = True
                        # Skip this metadata line, convert to text
                        p1, p2 = split_pipe_line(next_stripped)
                        if p2:
                            # For metadata, just output as combined text
                            if p1.startswith("| >"):
                                # Skip the "contenido extraido" line entirely
                                pass
                            else:
                                output.append(p1 + '\n')
                                if p2:
                                    output.append(p2 + '\n')
                        i += 1
                        continue
                    elif is_separator_line(next_stripped):
                        # Skip separator line in metadata
                        i += 1
                        continue
                    else:
                        break
                elif is_separator_line(next_stripped):
                    i += 1
                    continue
                else:
                    break
            in_metadata = False
            continue
        
        # Check if this is a separator line (|---|---|)
        if is_separator_line(stripped):
            # Check if the previous non-empty output line and next line look like table content
            # Find last non-empty output line
            last_content = ""
            for j in range(len(output)-1, -1, -1):
                if output[j].strip():
                    last_content = output[j].strip()
                    break
            
            # If last content was a pipe line and next is a pipe line, this is a real table
            next_line = lines[i+1].strip() if i+1 < len(lines) else ""
            if (is_table_line(last_content) and is_table_line(next_line) and
                not is_metadata_header_line(last_content)):
                output.append(line)
            # Otherwise skip separator (it's from broken formatting)
            i += 1
            continue
        
        # Check if this is a pipe line that should be split
        if is_table_line(stripped):
            # Check if this is actually a genuine table row
            # by looking at context: is there a header+separator above?
            is_genuine_table = False
            
            # Look back in output for a separator line
            for j in range(len(output)-1, max(0, len(output)-5), -1):
                if output[j].strip():
                    if is_separator_line(output[j].strip()):
                        is_genuine_table = True
                        break
                    elif is_table_line(output[j].strip()):
                        continue
                    else:
                        break
            
            if is_genuine_table:
                # Keep as table row
                output.append(line)
            else:
                # Split into two lines
                p1, p2 = split_pipe_line(stripped)
                if p2:
                    output.append(p1 + '\n')
                    output.append(p2 + '\n')
                else:
                    output.append(p1 + '\n')
            i += 1
            continue
        
        # Regular line - keep as is
        output.append(line)
        i += 1
    
    # Clean up: remove excessive blank lines (more than 1 consecutive)
    cleaned = []
    blank_count = 0
    for line in output:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                cleaned.append(line)
        else:
            blank_count = 0
            cleaned.append(line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned)
    
    return len(cleaned)

def is_metadata_header_line(line):
    """Check if a line is part of the metadata header."""
    stripped = line.strip()
    if stripped.startswith("| > Contenido extraido"):
        return True
    if stripped.startswith("| EVOLVE ACADEMY") or stripped.startswith("| Apuntes") or stripped.startswith("| Explotación") or stripped.startswith("| Hack The Box") or stripped.startswith("| Sesión"):
        return True
    if "Instructor:" in stripped or "Temas:" in stripped:
        return True
    if stripped.startswith("| Campo") or stripped.startswith("| Continuación") or stripped.startswith("| Bloque"):
        return True
    return False

def main():
    fixed = 0
    skipped = 0
    errors = []
    
    for fname in sorted(os.listdir(DIR)):
        if not fname.endswith('.md') or fname in SKIP:
            continue
        
        filepath = os.path.join(DIR, fname)
        try:
            count = process_file(filepath)
            fixed += 1
            print(f"  FIXED: {fname} ({count} lines)")
        except Exception as e:
            errors.append((fname, str(e)))
            print(f"  ERROR: {fname}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Files fixed: {fixed}")
    print(f"Files skipped: {skipped}")
    if errors:
        print(f"Errors: {len(errors)}")
        for fname, err in errors:
            print(f"  - {fname}: {err}")

if __name__ == "__main__":
    main()
