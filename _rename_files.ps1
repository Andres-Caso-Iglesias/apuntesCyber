$base = "C:\Users\intri\Desktop\biblioteca_programacion\evolve\Ciber\apuntes\ciberseguridad"
Set-Location $base

$files = @(
    "apuntes Chema\Maquinas\Vaccine (Tier 2) — Repaso en profundidad.md"
    "apuntes Chema\Maquinas\Rockstar — Escalada Linux y LFI.md"
    "apuntes Chema\Maquinas\HTB Starting Point — Repaso e inicio de Tier 2.md"
    "apuntes Chema\Maquinas\HackTheBox Starting Point — Tier 1.md"
    "apuntes Chema\Maquinas\Hack The Box- Starting Point — Tier 0.md"
    "apuntes Chema\Maquinas\Fuzzing de parámetros con x8 — Rockstar.md"
    "apuntes Chema\Maquinas\Auditoría de CMS — WordPress (máquina Academy).md"
    "apuntes Chema\IA\IA — Redes Neuronales.md"
    "apuntes Chema\IA\IA — Introducción y VibeCoding.md"
    "apuntes Chema\IA\IA — De los cimientos a la cima.md"
)

foreach ($f in $files) {
    $newName = ($f -replace " — ", " - ") -replace "—", "-"
    $newLeaf = Split-Path $newName -Leaf
    if (Test-Path -LiteralPath $f) {
        Rename-Item -LiteralPath $f -NewName $newLeaf
        Write-Host "OK: $f -> $newLeaf"
    } else {
        Write-Host "NO EXISTE: $f"
    }
}
