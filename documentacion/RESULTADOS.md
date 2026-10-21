> Actualización del 21 de octubre de 2026: el repositorio ya está publicado, Actions pasó 345/345 y el artefacto se descargó. Ver [GITHUB.md](GITHUB.md). Las menciones de GitHub pendiente más abajo corresponden al estado de la entrega inicial. La protección de rama sigue limitada por el plan privado.

# Resultados comprobados

Fecha: 15 de octubre de 2026 (America/Mexico_City). Windows; Node 24.18.0; Playwright 1.64.1; axe 4.14.0.

| Comprobación | Resultado |
|---|---|
| Laboratorio original | 8 fallos didácticos |
| Suite original aislada | 12 aprobadas / 7 fallidas |
| Validación corregida | 63 / 63 |
| Estabilidad inicial (5 s) | 313 aprobadas / 2 fallidas |
| Chromium (5 repeticiones) | 105 / 105 |
| Firefox (5 repeticiones) | 105 / 105 |
| WebKit (5 repeticiones) | 105 / 105 |
| Total estabilidad | 315 / 315 |
| Fallos / flaky / saltos | 0 / 0 / 0 |
| Duración de estabilidad | 401.1 segundos |
| ESLint | Sin errores |
| GitHub Actions remoto | Pendiente de publicación |

Comando real de estabilidad, sin actualizar referencias:

```bash
npx playwright test --repeat-each=5 --fail-on-flaky-tests --output=evidencias/estabilidad/resultados
```

HTML en evidencias/estabilidad/reporte mediante PLAYWRIGHT_HTML_OUTPUT_DIR; JSON en evidencias/estabilidad/resumen.json mediante PW_RESULTS_JSON. Los recuentos provienen del JSON real. Recursos /, login, catálogo, logo, favicon y API: HTTP 200 y MIME correctos (recursos.log).

Las ocho demostraciones no forman parte de los 315 casos de aceptación. La creación inicial de referencias es preparación; la estabilidad posterior sí compara sin actualizarlas. Axe cubre el catálogo y no constituye certificación integral de accesibilidad. GitHub y protección de rama no se ejecutaron desde este entorno.