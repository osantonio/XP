# Instrucciones de base de datos

## Escenario 1: levantar el servicio de PostgreSQL
Usa este flujo cuando necesitas iniciar el contenedor local de base de datos.

```powershell
docker compose -f .\scripts\docker-compose.yml up -d
```

Verificar estado:

```powershell
docker compose -f .\scripts\docker-compose.yml ps
```

Ver logs (opcional):

```powershell
docker compose -f .\scripts\docker-compose.yml logs -f db
```

Detener servicios (opcional):

```powershell
docker compose -f .\scripts\docker-compose.yml down
```

## Escenario 2: crear un respaldo (dump)
Usa este flujo cuando necesitas guardar el estado actual de la base de datos en un archivo.

```powershell
.\scripts\db_dump.ps1
```

El archivo se guarda en la carpeta `backups` con fecha y hora en el nombre.

## Escenario 3: restaurar un respaldo
Usa este flujo cuando necesitas cargar un dump previamente generado.

```powershell
.\scripts\db_restore.ps1 -DumpFile <ruta_al_dump.sql>
```

Asegúrate de que el contenedor `CONTAINER_XP` esté en ejecución antes de restaurar.
