# Instrucciones de base de datos

## Escenario 1: levantar el servicio de PostgreSQL
Usa este flujo cuando necesitas iniciar el contenedor local de base de datos. El proyecto se crea con el nombre `XP`.

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

## Escenario 4: agregar la base de datos en PGAdmin
Usa este flujo para registrar la conexión al contenedor en PGAdmin.

1. Abre PGAdmin y crea un nuevo Server.
2. En la pestaña General, asigna un nombre, por ejemplo: `XP local`.
3. En la pestaña Connection, usa estos datos:
   - Host name/address: `localhost`
   - Port: `5432`
   - Maintenance database: `XP_DB`
   - Username: `osantonio`
   - Password: `galapago`
4. Guarda el server y conéctate para ver la base de datos.
