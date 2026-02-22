param(
    [string]$BackupDir = "backups",
    [string]$FileName = "xp_dump_{0}.sql" -f (Get-Date -Format "yyyyMMdd_HHmmss")
)

$fullPath = Join-Path $BackupDir $FileName

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

Write-Host "Creando dump de la base de datos XP_DB en el contenedor CONTAINER_XP..."

docker exec CONTAINER_XP sh -c "pg_dump -U osantonio XP_DB" > $fullPath

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dump creado correctamente en: $fullPath"
} else {
    Write-Error "Error al crear el dump de la base de datos."
}

