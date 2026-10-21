> Actualización del 21 de octubre de 2026: el repositorio ya está publicado, Actions pasó 345/345 y el artefacto se descargó. Ver [GITHUB.md](GITHUB.md). Las menciones de GitHub pendiente más abajo corresponden al estado de la entrega inicial. La protección de rama sigue limitada por el plan privado.

# Revisión del documento y del alcance solicitado

La guía tiene 57 páginas. El capítulo 19 (páginas 53-54) define tres prácticas distintas; los capítulos anteriores explican cómo realizar las pruebas y el Anexo B pide la bitácora.

La aclaración del estudiante es **documentar dos prácticas completas**, no solamente dos casos. La entrega principal se reorganiza por Práctica 1 y Práctica 2 y añade capturas dentro de cada informe. La bitácora completa se conserva como respaldo de los requisitos escritos.

## Práctica 1: requisitos de la página 53

| Punto | Trabajo requerido | Estado y evidencia |
|---|---|---|
| 1 | Descomprimir, instalar, subir a repositorio nuevo | Descomprimido e instalado. Repositorio local inicializado. Publicación remota pendiente de acceso a GitHub. |
| 2 | Ejecutar E1-E8 y registrar mensaje, evidencia, clasificación y propuesta | Ejecutado: ocho fallos originales; bitácora completa, capturas, videos y trazas preservados. |
| 3 | Ejecutar Chromium y analizar cada fallo con los seis pasos | Ejecutado y analizado; run aislado original: 12 aprobadas y 7 fallidas. |
| 4 | Corregir el sitio sin cambiar expectativas para esconder fallos | Corregidos carrito, filtro tardío, logo, favicon, accesibilidad y manejo de errores de API. Pruebas originales intactas. |
| 5 | Añadir vaciado sin errores, login vacío y contrato de todos los productos | Tres pruebas en tests/practica.spec.ts, más regresiones y recorridos completos. |
| 6 | Cinco repeticiones en Chromium, Firefox y WebKit sin fallos | Primera suite final: 315/315. Se vuelve a ejecutar la suite ampliada de 23 casos: resultado en estabilidad-ampliada/resumen.json. |
| 7 | Verificar Actions en verde y el artefacto publicado | Workflow preparado; ejecución remota y artefacto de GitHub pendientes. Un reporte local no prueba este punto. |

## Práctica 2: requisitos de la página 53

La guía exige aplicar el trabajo al mini-proyecto del equipo. TiendaUT es el único proyecto de software recibido. Se aplica la Práctica 2 a TiendaUT por la indicación de trabajar con el ZIP. Es una adaptación explícita: si se exige otro proyecto propio del equipo, habrá que proporcionar ese sistema.

| Requisito | Preparación verificable en TiendaUT |
|---|---|
| Mínimo ocho E2E, dos recorridos completos, dos negativos y una API | Matriz específica y dos recorridos nuevos en tests/flujos-completos.spec.ts; se reutilizan pruebas funcionales, negativas y de API existentes. |
| Page Object y beforeEach o fixtures | LoginPage, CatalogoPage, fixtures.ts y beforeEach. |
| Consola, red y accesibilidad con axe | tests/analisis.spec.ts y prueba documental que adjunta calidad.json. |
| baseURL, webServer y trace | playwright.config.ts. |
| Pipeline con lint, pruebas y reporte | Archivo YAML preparado; verificación remota pendiente de cuenta. |
| Bitácora de todos los fallos encontrados | BITACORA.md, defectos.json, INDICE-EVIDENCIAS.md y evidencias históricas. |

## Práctica 3: requisito externo

La página 54 exige el sistema integrador, identificar con el cliente de tres a cinco flujos, ejecutar calidad sobre sus pantallas y configurar protección de integración. No se recibieron ese sistema ni los requisitos del cliente. No puede declararse realizada usando únicamente la tienda de ejemplo. No forma parte de las dos prácticas que se van a documentar.

## Evidencia visual

Las capturas de evidencias/capturas/imagenes provienen de navegadores reales y de los reportes HTML originales. Las pruebas documentales vuelven a ejecutar acciones y aserciones antes de capturar. No se construyeron pantallas de resultados para simular ejecuciones o Actions.
