from pathlib import Path

BASE = Path(r'C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad')

# Fix the corrupted warning symbol bytes
def fix_encoding(content):
    # Fix corrupted warning symbol: c3 af c2 b8 c2 8f -> e2 9a a0 (warning)
    content = content.replace(b'\xc3\xaf\xc2\xb8\xc2\x8f', b'\xe2\x9a\xa0')
    
    # Fix corrupted warning symbol: c3 af c2 b8 -> e2 9a a0 (warning)
    content = content.replace(b'\xc3\xaf\xc2\xb8', b'\xe2\x9a\xa0')
    
    # Fix corrupted em-dash: c3 a2 e2 82 ac e2 80 9d -> e2 80 94 (em-dash)
    content = content.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b'\xe2\x80\x94')
    
    # Fix corrupted em-dash: c3 a2 e2 82 ac e2 80 9c -> e2 80 9c (left double quotation)
    content = content.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9c', b'\xe2\x80\x9c')
    
    # Fix corrupted em-dash: c3 a2 e2 82 ac e2 80 98 -> e2 80 98 (left single quotation)
    content = content.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x98', b'\xe2\x80\x98')
    
    # Fix corrupted em-dash: c3 a2 e2 82 ac e2 80 99 -> e2 80 99 (right single quotation)
    content = content.replace(b'\xc3\xa2\xe2\x82\xac\xe2\x80\x99', b'\xe2\x80\x99')
    
    return content

files_fixed = 0
for f in BASE.rglob('*.md'):
    with open(f, 'rb') as fh:
        content = fh.read()
    
    fixed = fix_encoding(content)
    
    if fixed != content:
        with open(f, 'wb') as fh:
            fh.write(fixed)
        files_fixed += 1
        print(f'Fixed: {f.name}')

print(f'\nTotal files fixed: {files_fixed}')
