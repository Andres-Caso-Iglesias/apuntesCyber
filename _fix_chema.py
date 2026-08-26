from pathlib import Path

BASE = Path(r'C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad\apuntes Chema')

# Comprehensive fixes for all corruption patterns
def fix_encoding(text):
    # Standard Latin accents (Ã + char)
    text = text.replace('Ã¡', 'á')
    text = text.replace('Ã©', 'é')
    text = text.replace('Ã­', 'í')
    text = text.replace('Ã³', 'ó')
    text = text.replace('Ãº', 'ú')
    text = text.replace('Ã±', 'ñ')
    text = text.replace('Ã ', 'à')
    text = text.replace('Ã¨', 'è')
    text = text.replace('Ã¬', 'ì')
    text = text.replace('Ã²', 'ò')
    text = text.replace('Ã¹', 'ù')
    text = text.replace('Ã„', 'Ä')
    text = text.replace('Ã¶', 'ö')
    text = text.replace('Ã¼', 'ü')
    text = text.replace('Ã‡', 'Ç')
    text = text.replace('Ã€', 'À')
    text = text.replace('Ãˆ', 'È')
    text = text.replace('ÃŒ', 'Ì')
    text = text.replace('Ã"', 'Ó')
    text = text.replace('Ã™', 'Ù')
    text = text.replace('Ã‚', 'Â')
    text = text.replace('ÃŠ', 'Ê')
    text = text.replace('ÃŽ', 'Î')
    text = text.replace('Ã"','Ô')
    text = text.replace('Ã›', 'Û')
    text = text.replace('Ã‘', 'Ñ')
    text = text.replace('Ãœ', 'Ü')
    text = text.replace('Ã¦', 'æ')
    text = text.replace('Ã¸', 'ø')
    text = text.replace('Ã°', 'ð')
    text = text.replace('Ã¾', 'þ')
    text = text.replace('Ã\x81', 'Á')
    text = text.replace('Ã\x89', 'É')
    text = text.replace('Ã\x8d', 'Í')
    text = text.replace('Ã\x93', 'Ó')
    text = text.replace('Ã\x9a', 'Ú')
    
    # Middle dot and guillemets
    text = text.replace('Â·', '·')
    text = text.replace('Â«', '«')
    text = text.replace('Â»', '»')
    text = text.replace('Â¿', '¿')
    text = text.replace('Â¡', '¡')
    text = text.replace('Âº', 'º')
    text = text.replace('Âª', 'ª')
    
    # Em-dash and en-dash
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '—')
    text = text.replace('â€"', '–')
    
    # Arrow
    text = text.replace('→\'', '→')
    text = text.replace('â†', '→')
    
    # Not equal
    text = text.replace('â‰', '≠')
    
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
    
    # Box drawing characters
    text = text.replace('â"Œ', '┌')
    text = text.replace('â"€', '─')
    text = text.replace('â"‚', '│')
    text = text.replace('â"œ', '├')
    text = text.replace('â"', '┘')
    text = text.replace('â"¤', '┤')
    text = text.replace('â"', '└')
    text = text.replace('â–¼', '▼')
    
    # Check and cross
    text = text.replace('âœ…', '✓')
    text = text.replace('âš ', '⚠')
    text = text.replace('âŒ', '✗')
    
    # Degree symbol
    text = text.replace('Â°', '°')
    
    # Micro sign
    text = text.replace('Âµ', 'µ')
    
    # Copyright, registered, trademark
    text = text.replace('Â©', '©')
    text = text.replace('Â®', '®')
    text = text.replace('Â™', '™')
    
    # Section sign
    text = text.replace('Â§', '§')
    
    # Plus-minus
    text = text.replace('Â±', '±')
    
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
    text = text.replace('Â·', '·')
    
    # Euro sign
    text = text.replace('â‚¬', '€')
    
    # Stars
    text = text.replace('â­', '⭐')
    
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
