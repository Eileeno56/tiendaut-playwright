> Actualización del 21 de octubre de 2026: el repositorio ya está publicado, Actions pasó 345/345 y el artefacto se descargó. Ver [GITHUB.md](GITHUB.md). Las menciones de GitHub pendiente más abajo corresponden al estado de la entrega inicial. Después de la autorización del estudiante, el repositorio es público y main exige el check test; la limitación del plan privado se resolvió.

# Inventario de la entrega

Los archivos originales permanecen sin modificaciones en la carpeta superior.

## Código original modificado

- eslint.config.mjs
- public/login.html
- public/index.html
- public/catalogo.html
- .github/workflows/playwright.yml
- README.md
- package.json
- server.js
- playwright.config.ts

## Código nuevo

- playwright.laboratorio.config.ts: separa demostraciones intencionales de aceptación.
- tests/practica.spec.ts: tres casos obligatorios.
- tests/regresiones.spec.ts: filtro antes de respuesta y red interrumpida.
- public/logo.png y public/favicon.ico: recursos reales servidos con MIME correcto.
- tools/generar_informe.py: genera bitácora e informe a partir de resultados reales.

## Evidencias

- laboratorio-original: 8 fallos didácticos originales.
- suite-original: 12 casos aprobados y 7 fallidos en ejecución aislada.
- intento-interferido: ejecución descartada por cierre de servidor; se conserva para transparencia.
- correccion: primera validación de 63 casos y creación de referencias visuales ausentes.
- estabilidad: cinco repeticiones por navegador, sin actualizar referencias.
- analisis: extracción de trazas, lint y verificación HTTP.

## Alcance externo pendiente

Publicar en GitHub, verificar la ejecución remota, aprobar referencias Linux y configurar protección de rama requiere acceso a una cuenta. No se declara realizado.