param(
    [Parameter(Mandatory = $true)]
    [string]$DumpFile
)

if (-not (Test-Path $DumpFile)) {
    Write-Error "El archivo de dump no existe: $DumpFile"
    exit 1
}

Write-Host "Restaurando base de datos XP_DB en el contenedor CONTAINER_XP desde: $DumpFile"

Get-Content $DumpFile | docker exec -i CONTAINER_XP sh -c "psql -U osantonio -d XP_DB"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Restauración completada correctamente."
} else {
    Write-Error "Error al restaurar la base de datos."
}

