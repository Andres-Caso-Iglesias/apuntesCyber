#!/usr/bin/env python3
"""Fix broken pipe-separated formatting in markdown files."""
import os
import re

DIR = r"C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad\comandos"
SKIP = {"00 - Indice de Comandos.md", "fix_tables.py", "fix_tables2.py"}

def is_pipe_line(s):
    """Line starts with | and ends with | and has content."""
    t = s.strip()
    return t.startswith("|") and t.endswith("|") and len(t) > 4 and "|" in t[1:-1]

def is_separator(s):
    """|---|---| style separator."""
    t = s.strip()
    if not t.startswith("|") or not t.endswith("|"):
        return False
    inner = t[1:-1]
    return all(re.match(r'^[-:\s]*$', p) for p in inner.split("|") if p.strip())

def split_pipe(s):
    """Split ' | text1 | text2 |' into (text1, text2)."""
    t = s.strip().strip("|")
    # Try space-pipe-space first
    parts = t.split(" | ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # Fallback to pipe
    parts = t.split("|", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return t.strip(), None

def process(filepath):
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    out = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        s = raw.strip()

        # --- Blank lines: keep ---
        if not s:
            out.append("\n")
            i += 1
            continue

        # --- Lines that are NOT pipe lines: keep as-is ---
        if not is_pipe_line(s):
            out.append(raw)
            i += 1
            continue

        # --- It IS a pipe line. Decide: genuine table or broken format? ---

        # Look backwards in 'out' for a separator (|---|---|)
        # that would make this a genuine table data row.
        genuine = False
        for j in range(len(out) - 1, max(0, len(out) - 6), -1):
            ps = out[j].strip()
            if not ps:
                continue
            if is_separator(ps):
                genuine = True
                break
            if is_pipe_line(ps):
                continue  # keep scanning back
            break  # hit non-pipe, non-separator, non-blank: stop

        if genuine:
            # Keep as table row
            out.append(raw)
            i += 1
            continue

        # --- Not a genuine table: split into two lines ---
        p1, p2 = split_pipe(s)
        out.append(p1 + "\n")
        if p2:
            out.append(p2 + "\n")
        i += 1

    # Collapse 3+ consecutive blank lines into 2
    final = []
    blanks = 0
    for line in out:
        if line.strip() == "":
            blanks += 1
            if blanks <= 2:
                final.append(line)
        else:
            blanks = 0
            final.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(final)

    return len(final)


def main():
    fixed = 0
    for fname in sorted(os.listdir(DIR)):
        if not fname.endswith(".md") or fname in SKIP:
            continue
        fp = os.path.join(DIR, fname)
        try:
            count = process(fp)
            fixed += 1
            print(f"  OK  {fname}  ({count} lines)")
        except Exception as e:
            print(f"  ERR {fname}: {e}")

    print(f"\nDone. {fixed} files processed.")


if __name__ == "__main__":
    main()
