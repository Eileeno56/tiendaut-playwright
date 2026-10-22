> Actualización del 21 de octubre de 2026: el repositorio ya está publicado, Actions pasó 345/345 y el artefacto se descargó. Ver [GITHUB.md](GITHUB.md). Las menciones de GitHub pendiente más abajo corresponden al estado de la entrega inicial. Después de la autorización del estudiante, el repositorio es público y main exige el check test; la limitación del plan privado se resolvió.

# Resultados de la suite ampliada

Se añadieron dos flujos completos y CatalogoPage; las pruebas originales se conservaron.

| Comprobación | Resultado |
|---|---|
| chromium: 23 casos x 5 repeticiones | 115/115 |
| firefox: 23 casos x 5 repeticiones | 115/115 |
| webkit: 23 casos x 5 repeticiones | 115/115 |
| Total | 345/345 |
| Fallos / flaky / saltos / reintentos locales | 0 / 0 / 0 / 0 |
| ESLint | Sin errores; lint-ampliado.log |
| Duración | 434.9 s |

Fuente: evidencias/estabilidad-ampliada/resumen.json. Los 315 casos aprobados de la entrega inicial se conservan como evidencia histórica independiente. No hubo actualización de snapshots durante ninguna de las dos comprobaciones finales.

Los informes principales ahora corresponden a dos prácticas completas; las capturas documentales se validan aparte con npm run test:evidencias. GitHub remoto permanece pendiente de acceso a cuenta. La aplicación de la segunda práctica se ha preparado sobre TiendaUT y se presenta como adaptación al proyecto suministrado; si se exige otro sistema, habrá que proporcionarlo.