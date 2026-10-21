# Publicación y comprobación pendiente en GitHub

El entorno de trabajo no expone un conector de GitHub, una sesión de navegador ni credenciales de GitHub CLI. Por ello no se creó un repositorio remoto ni se afirma que Actions esté en verde. La comprobación local no sustituye una ejecución de GitHub Actions.

El workflow `.github/workflows/playwright.yml` queda preparado para push y pull request a main/master: Node 24, npm ci, npm run lint, instalación de los tres navegadores y cinco repeticiones de la suite, con rechazo de pruebas flaky. Publica playwright-report, test-results y las referencias visuales durante 30 días incluso si hay fallos.

Cuando haya una cuenta disponible:

1. Crear un repositorio vacío llamado tiendaut-playwright (privado si se desea).
2. Abrir terminal dentro de este proyecto. Ejecutar git init -b main si aún no existe .git, git add ., git commit -m "Completa práctica Playwright y bitácora". Usar la identidad Git propia.
3. Agregar el remoto con git remote add origin URL_DEL_REPOSITORIO y ejecutar git push -u origin main.
4. En Actions abrir Playwright Tests y verificar npm ci, lint y las 315 ejecuciones de aceptación. Registrar la URL y el resultado real de ese run en la bitácora.
5. Descargar el artefacto playwright-report; comprobar que incluye HTML, resumen JSON y las trazas de cualquier fallo.
6. En Settings > Branches (o Rulesets), exigir el check del job test para integrar a main. Esta protección requiere acceso de administración; no está configurada desde este entorno.

## Referencias visuales por plataforma

Se entregan referencias revisadas de Windows para Chromium, Firefox y WebKit. El workflow conserva la política del ZIP `--update-snapshots=missing`: Linux genera las imágenes que le falten. Esto permite arrancar CI, pero su primera ejecución NO demuestra ausencia de regresión visual frente a una referencia Linux previamente aprobada.

Después de revisar las imágenes Linux del artefacto, incorporarlas a tests/red-y-visual.spec.ts-snapshots y retirar `--update-snapshots=missing` (o usar `--update-snapshots=none`) del workflow para exigir comparación estricta también en Linux. Nunca usar actualización de snapshots para ocultar diferencias inesperadas.

Documentación oficial consultada: https://playwright.dev/docs/test-snapshots y https://playwright.dev/docs/api/class-testconfig.
