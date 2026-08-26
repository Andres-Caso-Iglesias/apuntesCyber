from pathlib import Path
import re

BASE = Path(r'C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad\apuntes Chema')

# More aggressive fix - replace all remaining corrupted patterns
def fix_encoding(text):
    # Fix Â followed by non-breaking spaces
    text = text.replace('Â\xa0', '\xa0')
    text = text.replace('Â ', ' ')
    
    # Fix checkmark: âœ— -> ✓
    text = text.replace('âœ—', '✓')
    
    # Fix em-dash: â€" -> —
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '–')
    
    # Fix bullet: â€¢ -> •
    text = text.replace('â€¢', '•')
    
    # Fix arrow: →' -> →
    text = text.replace('→\'', '→')
    text = text.replace('â†', '→')
    
    # Fix not equal: â‰ -> ≠
    text = text.replace('â‰', '≠')
    
    # Fix info: â„¹ -> ℹ
    text = text.replace('â„¹', 'ℹ')
    
    # Fix warning: âš  -> ⚠
    text = text.replace('âš ', '⚠')
    
    # Fix check: âœ" -> ✓
    text = text.replace('âœ"', '✓')
    text = text.replace('âœ…', '✓')
    
    # Fix cross: âŒ -> ✗
    text = text.replace('âŒ', '✗')
    
    # Fix ballot box: â˜ -> ☐
    text = text.replace('â˜', '☐')
    
    # Fix euro sign: â‚¬ -> €
    text = text.replace('â‚¬', '€')
    
    # Fix stars: â­ -> ⭐
    text = text.replace('â­', '⭐')
    
    # Fix box drawing characters
    text = text.replace('â"Œ', '┌')
    text = text.replace('â"€', '─')
    text = text.replace('â"‚', '│')
    text = text.replace('â"œ', '├')
    text = text.replace('â"', '┘')
    text = text.replace('â"¤', '┤')
    text = text.replace('â"', '└')
    text = text.replace('â–¼', '▼')
    
    # Fix circled numbers
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
    
    # Fix various accented characters
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
    
    # Fix middle dot
    text = text.replace('Â·', '·')
    
    # Fix copyright and registered
    text = text.replace('Â©', '©')
    text = text.replace('Â®', '®')
    text = text.replace('Â™', '™')
    
    # Fix section sign
    text = text.replace('Â§', '§')
    
    # Fix degree
    text = text.replace('Â°', '°')
    
    # Fix plus-minus
    text = text.replace('Â±', '±')
    
    # Fix micro
    text = text.replace('Âµ', 'µ')
    
    # Fix paragraph
    text = text.replace('Â¶', '¶')
    
    # Fix broken bar
    text = text.replace('Â¦', '¦')
    
    # Fix logical not
    text = text.replace('Â¬', '¬')
    
    # Fix soft hyphen
    text = text.replace('Â¯', '¯')
    
    # Fix acute accent
    text = text.replace('Â´', '´')
    
    # Fix cedilla
    text = text.replace('Â¸', '¸')
    
    # Fix superscript
    text = text.replace('Â¹', '¹')
    text = text.replace('Â²', '²')
    text = text.replace('Â³', '³')
    
    # Fix fractions
    text = text.replace('Â¼', '¼')
    text = text.replace('Â½', '½')
    text = text.replace('Â¾', '¾')
    
    # Fix currency
    text = text.replace('Â¤', '¤')
    
    # Fix multiplication and division
    text = text.replace('Â×', '×')
    
    # Fix guillemets
    text = text.replace('Â«', '«')
    text = text.replace('Â»', '»')
    
    # Fix ordinals
    text = text.replace('Âº', 'º')
    text = text.replace('Âª', 'ª')
    
    # Fix inverted punctuation
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
