# GitHub verificado - 21 de octubre de 2026

Repositorio público: https://github.com/Eileeno56/tiendaut-playwright

Ejecución verificada: https://github.com/Eileeno56/tiendaut-playwright/actions/runs/39695106242

- Instalación de dependencias: correcta.
- ESLint: correcto.
- Chromium, Firefox y WebKit: 115/115 cada uno; total 345/345.
- Fallos, flaky y saltos: cero.
- Publicación de playwright-report: correcta; artefacto descargado y verificado.
- Datos de evidencia: evidencias/github/verificacion.json, actions-jobs.json, actions-artifacts.json, artefacto/ y logs/.

Las tres referencias Linux generadas en la primera ejecución se revisaron y se añadieron a tests/red-y-visual.spec.ts-snapshots/. El workflow ahora usa --update-snapshots=none para comparar estrictamente y no generar referencias durante la validación.

## Protección de rama activada

El repositorio se hizo público con autorización explícita del estudiante. Main exige el check test y una rama actualizada antes de integrar cambios. Se conserva la respuesta de GitHub en evidencias/github/proteccion-rama.json. El error 403 anterior correspondía al plan privado; no es el estado actual.

## Segunda ejecución con comparación estricta

https://github.com/Eileeno56/tiendaut-playwright/actions/runs/39696522338 terminó en verde con 345/345, cero fallos y cero flaky, sin regenerar snapshots. El artefacto se descargó en evidencias/github/comparacion-estricta. Se fija Ubuntu 24.04 en el workflow para que coincida con el entorno de las referencias aprobadas.

## Entrega al docente

Compartir el enlace público del repositorio y los dos informes. No necesita invitación para verlos. No se marcó la tarea como entregada en Classroom.
