from pathlib import Path
import re

BASE = Path(r'C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad\apuntes Chema')

# More aggressive fix - replace all remaining corrupted patterns
def fix_encoding(text):
    # Em-dash: â€" -> —
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '–')
    
    # Bullet: â€¢ -> •
    text = text.replace('â€¢', '•')
    
    # Arrow: →' -> →
    text = text.replace('→\'', '→')
    text = text.replace('â†', '→')
    
    # Not equal: â‰ -> ≠
    text = text.replace('â‰', '≠')
    
    # Info: â„¹ -> ℹ
    text = text.replace('â„¹', 'ℹ')
    
    # Warning: âš  -> ⚠
    text = text.replace('âš ', '⚠')
    
    # Check: âœ" -> ✓
    text = text.replace('âœ"', '✓')
    text = text.replace('âœ…', '✓')
    
    # Cross: âŒ -> ✗
    text = text.replace('âŒ', '✗')
    
    # Ballot box: â˜ -> ☐
    text = text.replace('â˜', '☐')
    
    # Euro sign: â‚¬ -> €
    text = text.replace('â‚¬', '€')
    
    # Stars: â­ -> ⭐
    text = text.replace('â­', '⭐')
    
    # Box drawing characters
    text = text.replace('â"Œ', '┌')
    text = text.replace('â"€', '─')
    text = text.replace('â"‚', '│')
    text = text.replace('â"œ', '├')
    text = text.replace('â"', '┘')
    text = text.replace('â"¤', '┤')
    text = text.replace('â"', '└')
    text = text.replace('â–¼', '▼')
    
    # Circled numbers
    text = text.replace('â‘ ', '①')
    text = text.replace('â‘¡', '②')
    text = text.replace('â‘¢', '③')
    text = text.replace('â‘£', '④')
    text = text.replace('â‘¤', '⑤')
    text = text.replace('â‘¥', '⑥')
    text = text.replace('â‘¦', '⑦')
    text = text.replace('â‘§', '⑧')
    text = text.replace('â‘¨', '⑨')
    text = text.replace('â‘©', '⑩')
    text = text.replace('â‘ª', '⑪')
    text = text.replace('â‘«', '⑫')
    text = text.replace('â‘¬', '⑬')
    text = text.replace('â‘­', '⑭')
    text = text.replace('â‘®', '⑮')
    
    # Various accented characters
    text = text.replace('Ã"', 'Ó')
    text = text.replace('Ã‰', 'É')
    text = text.replace('Ã\x81', 'Á')
    text = text.replace('Ã\x8d', 'Í')
    text = text.replace('Ã\x93', 'Ó')
    text = text.replace('Ã\x9a', 'Ú')
    text = text.replace('Ãš', 'Ú')
    text = text.replace('Ã¡', 'á')
    text = text.replace('Ã©', 'é')
    text = text.replace('Ã­', 'í')
    text = text.replace('Ã³', 'ó')
    text = text.replace('Ãº', 'ú')
    text = text.replace('Ã±', 'ñ')
    
    # Middle dot
    text = text.replace('Â·', '·')
    
    # Copyright and registered
    text = text.replace('Â©', '©')
    text = text.replace('Â®', '®')
    text = text.replace('Â™', '™')
    
    # Section sign
    text = text.replace('Â§', '§')
    
    # Degree
    text = text.replace('Â°', '°')
    
    # Plus-minus
    text = text.replace('Â±', '±')
    
    # Micro
    text = text.replace('Âµ', 'µ')
    
    # Paragraph
    text = text.replace('Â¶', '¶')
    
    # Broken bar
    text = text.replace('Â¦', '¦')
    
    # Logical not
    text = text.replace('Â¬', '¬')
    
    # Soft hyphen
    text = text.replace('Â¯', '¯')
    
    # Acute accent
    text = text.replace('Â´', '´')
    
    # Cedilla
    text = text.replace('Â¸', '¸')
    
    # Superscript
    text = text.replace('Â¹', '¹')
    text = text.replace('Â²', '²')
    text = text.replace('Â³', '³')
    
    # Fractions
    text = text.replace('Â¼', '¼')
    text = text.replace('Â½', '½')
    text = text.replace('Â¾', '¾')
    
    # Currency
    text = text.replace('Â¤', '¤')
    
    # Multiplication and division
    text = text.replace('Â×', '×')
    
    # Guillemets
    text = text.replace('Â«', '«')
    text = text.replace('Â»', '»')
    
    # Ordinals
    text = text.replace('Âº', 'º')
    text = text.replace('Âª', 'ª')
    
    # Inverted punctuation
    text = text.replace('Â¿', '¿')
    text = text.replace('Â¡', '¡')
    
    return text

files_fixed = 0
for f in BASE.rglob('*.md'):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    fixed = fix_encoding(content)
    
    if fixed != content:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
        files_fixed += 1
        print(f'Fixed: {f.name}')

print(f'\nTotal files fixed: {files_fixed}')
