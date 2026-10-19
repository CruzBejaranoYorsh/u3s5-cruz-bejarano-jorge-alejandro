<!-- # : título principal del README (lo primero que se ve en GitHub) -->
# Proyecto Django — CRUZ BEJARANO JORGE ALEJANDRO

<!-- ## : subtítulo de la sección con el enlace a producción -->
## Demo en vivo (producción)
<!-- la URL pública de tu Web Service u3s6-… en Render -->
https://u3s5-cruz-bejarano-jorge-alejandro.onrender.com/servicios/

<!-- ## : subtítulo con lo que se hizo esta semana -->
## Semana 6 — Autenticación, sesiones y seguridad
Registro, login y logout propios; cada usuario ve y edita solo sus
propios servicios, probado con dos cuentas.

<!-- ## : subtítulo de la sección con la prueba de aislamiento -->
## Prueba de aislamiento
Creé servicios con usuario_a y usuario_b e inicié sesión con cada cuenta.
Cada usuario solo vio sus propios servicios en el listado.
Al intentar editar o eliminar el servicio de la otra cuenta, recibí un error por parte de django, pues no tenia permiso de acceder
a su pagina.
