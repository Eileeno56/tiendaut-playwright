# Estado GitHub actualizado el 21 de octubre de 2026

Repositorio y Actions verificados: [Eileeno56/tiendaut-playwright](https://github.com/Eileeno56/tiendaut-playwright).

# Playwright - dos prácticas con evidencias

## Documentos principales

1. `output/pdf/practica-1-con-evidencias.pdf`: Práctica 1, siete requisitos, laboratorio E1-E8, análisis y correcciones, tres pruebas nuevas, capturas de antes/después, estabilidad y estado de GitHub.
2. `output/pdf/practica-2-con-evidencias.pdf`: aplicación de los requisitos del mini-proyecto a TiendaUT, matriz de ocho E2E y API, dos recorridos completos, Page Objects, casos negativos, calidad y CI. Se usa TiendaUT como adaptación al único proyecto recibido, según la indicación de trabajar con el ZIP.

La aclaración del estudiante fue documentar **dos prácticas completas**. Cada PDF incluye capturas reales y pies que explican qué se verificó. No se redujo la bitácora obligatoria a dos defectos.

`documentacion/REVISION-DE-REQUISITOS.md` distingue cada requisito realizado de los pendientes externos. El informe anterior de ocho páginas queda en el ZIP de la primera entrega. Este nuevo ZIP incluye solo los dos informes principales y la guía original de referencia.

## Instalar y ejecutar

Node probado: 24.18.0. Playwright: 1.64.1. Credenciales didácticas: alumno / utvm2026.

```bash
npm ci
npx playwright install
npm run lint
npm run test:estabilidad
npm run test:evidencias
```

Ejecutar las suites una a la vez: cada una inicia su servidor en localhost:3000. Detener antes otros servidores en ese puerto. `npm start` permite abrir el sitio manualmente.

La suite ampliada tiene 23 casos: cinco repeticiones en tres navegadores son 345 ejecuciones. El archivo `tests/flujos-completos.spec.ts` incorpora los recorridos Inicio > Login > Catálogo e Inicio > Catálogo > Buscar > Agregar dos > Vaciar. Usa LoginPage, CatalogoPage y beforeEach. Se conservan los casos negativos, API, fixture y pruebas de calidad existentes.

## Capturas y reportes reales

`evidencias/capturas/imagenes/` contiene PNG del navegador y del reporte HTML. `playwright.evidencias.config.ts` ejecuta ocho pruebas documentales separadas, adjunta datos reales de API/calidad y guarda trazas. Las capturas se toman después de verificar el estado con aserciones.

```bash
npx playwright show-report evidencias/laboratorio-original/reporte
npx playwright show-report evidencias/suite-original/reporte
npx playwright show-report evidencias/estabilidad-ampliada/reporte
npx playwright show-report evidencias/capturas/reporte
```

`tools/capturar_reportes.cjs` captura la interfaz de los reportes reales. La bitácora detallada y el índice de cada fallo están en documentacion/BITACORA.md e INDICE-EVIDENCIAS.md. `documentacion/RESULTADOS-AMPLIADOS.md` resume la ejecución actual. La entrega inicial de 315 casos y los intentos fallidos se conservan por separado.

## Laboratorio intencional

`npm run test:laboratorio` conserva E1-E8 como ejemplos didácticos separados de la aceptación. Después de corregir el sitio, E6 y E8 pueden pasar. Los ocho fallos originales y sus capturas/trazas se conservaron antes de cambiar el sitio. `npx eslint tests/ --no-ignore` muestra el await deliberadamente ausente en E7.

## Alcance y entrega

GitHub ya está verificado: https://github.com/Eileeno56/tiendaut-playwright/actions/runs/39695106242 terminó en verde con 345/345. El artefacto se publicó, descargó y verificó; evidencia en evidencias/github y documentacion/GITHUB.md. Repositorio público: https://github.com/Eileeno56/tiendaut-playwright. El docente puede abrir el enlace. Main exige el check test. La segunda ejecución también pasó 345/345 sin regenerar referencias: https://github.com/Eileeno56/tiendaut-playwright/actions/runs/39696522338.

La guía exige un mini-proyecto del equipo para la Práctica 2. Solo se recibió TiendaUT: la Práctica 2 se aplica y documenta sobre este proyecto. Si el profesor exige otro sistema del equipo, deberá aplicarse a ese sistema. La Práctica 3 pide un sistema integrador y requisitos del cliente que no se proporcionaron; no se declara realizada y no es una de las dos prácticas documentadas.

Las referencias visuales Windows se revisaron. Las tres referencias Linux se revisaron, incorporaron y el workflow compara con --update-snapshots=none. El margen de aserciones es 20 segundos, justificado en la bitácora tras investigar dos fallos de espera en Firefox.
