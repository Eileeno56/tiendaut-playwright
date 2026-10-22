# Bitácora de análisis de defectos

Práctica 1 · TiendaUT · 15 de octubre de 2026 · America/Mexico_City.

Método: leer el mensaje, ubicar la acción, reproducir contra el sitio original, inspeccionar las trazas (acciones, DOM y red), clasificar, corregir y confirmar. Las trazas se inspeccionaron como JSON; no se afirma haber usado gráficamente Trace Viewer. Los archivos originales y sus capturas se conservan en el índice.

Laboratorio original: 8 fallos previstos. Suite original aislada con las tres pruebas nuevas: 12 pasan y 7 fallan. Validación corregida: 63/63. Estabilidad: 315/315, cero fallos, flaky o saltos. GitHub remoto pendiente de acceso.

## E1 - Elemento inexistente

- Mensaje: `locator.click: Test timeout of 8000ms exceeded; Comprar ahora`
- Clasificación: Prueba.
- Evidencia y causa raíz: El requisito y el HTML ofrecen Agregar al carrito, no Comprar ahora. El snapshot no contiene el botón buscado.
- Corrección: En una prueba funcional usar el botón real dentro de un producto concreto. Se mantiene la demostración original.
- Verificación: carrito.spec.ts agrega teclado y mouse con locators acotados.

## E2 - Localizador ambiguo

- Mensaje: `strict mode violation; resolved to 4 elements`
- Clasificación: Prueba.
- Evidencia y causa raíz: Hay cuatro productos y cuatro botones con el mismo nombre; el locator global no identifica uno.
- Corrección: Filtrar el producto por nombre antes de localizar su botón. No usar first para ocultar ambigüedad.
- Verificación: carrito.spec.ts comprueba el contador 2 tras agregar dos productos específicos.

## E3 - Texto esperado equivocado

- Mensaje: `Expected Bienvenidos a TiendaUT; Received Bienvenido a TiendaUT`
- Clasificación: Prueba.
- Evidencia y causa raíz: La prueba agrega una s al encabezado especificado en el capítulo 3. El DOM conserva el singular correcto.
- Corrección: Usar Bienvenido a TiendaUT según el requisito; no cambiar el sitio para satisfacer una expectativa incorrecta.
- Verificación: inicio.spec.ts verifica título y encabezado correctos.

## E4 - Redirección esperada con contraseña inválida

- Mensaje: `Expected /catalogo\.html/; Received /login.html`
- Clasificación: Prueba.
- Evidencia y causa raíz: Se ingresa alumno/mal. El requisito permite entrar solo con alumno/utvm2026; el sitio debe rechazar la contraseña mal.
- Corrección: Para el caso negativo verificar alerta y permanencia en login; para el positivo usar las credenciales válidas.
- Verificación: login.spec.ts cubre ambos caminos sin modificar el requisito.

## E5 - Servidor ausente en otro puerto

- Mensaje: `net::ERR_CONNECTION_REFUSED at http://localhost:3999/`
- Clasificación: Entorno/configuración de prueba.
- Evidencia y causa raíz: La navegación apunta al puerto 3999, mientras webServer inicia la aplicación en el 3000.
- Corrección: Usar baseURL y page.goto('/'); iniciar el servidor mediante webServer.
- Verificación: Las pruebas de inicio y API usan el puerto configurado.

## E6 - Excepción al vaciar

- Mensaje: `reiniciarContador is not defined`
- Clasificación: Sitio.
- Evidencia y causa raíz: El listener asigna carrito=0 y llama una función inexistente. No actualiza el texto del contador.
- Corrección: Asignar contador.textContent = String(carrito) en el listener.
- Verificación: CP-17 agrega un producto, comprueba 1, vacía, comprueba 0 y exige pageerror vacío.

## E7 - Aserción sin await

- Mensaje: `toBeVisible; element(s) not found; Test ended`
- Clasificación: Prueba.
- Evidencia y causa raíz: La promesa no se espera y apunta al encabezado No existe. La traza muestra que termina el test con la aserción pendiente; ESLint detecta missing-playwright-await en línea 48.
- Corrección: Esperar la aserción con await y usar el encabezado del requisito. Se conserva el fallo en la suite didáctica.
- Verificación: inicio.spec.ts usa await expect(...).toHaveText(...); lint normal excluye solo el archivo didáctico.

## E8 - Buscador sin etiqueta

- Mensaje: `locator.fill: Test timeout of 8000ms exceeded; getByLabel('Buscar producto')`
- Clasificación: Prueba + accesibilidad del sitio.
- Evidencia y causa raíz: El input original tiene placeholder pero carece de label. getByLabel no encuentra una asociación accesible.
- Corrección: Añadir label for=buscar; mantener getByLabel para verificar la corrección accesible.
- Verificación: RG-01 escribe mediante getByLabel y filtra correctamente; axe catálogo sin violaciones.

## D1 - Consola con recurso 404

- Mensaje: `Failed to load resource: 404 (Not Found)`
- Clasificación: Sitio / recurso faltante.
- Evidencia y causa raíz: La traza Network muestra GET /logo.png con estado 404; el HTML solicita una imagen inexistente.
- Corrección: Crear public/logo.png y servir PNG con image/png.
- Verificación: analisis.spec.ts exige consola vacía y red sin estados >=400.

## D2 - Red con petición fallida

- Mensaje: `404 http://localhost:3000/logo.png`
- Clasificación: Sitio / mismo defecto de D1.
- Evidencia y causa raíz: La prueba de red detecta la misma causa que consola. Son dos fallos de prueba, no dos recursos distintos.
- Corrección: Recurso PNG válido y tipo MIME correcto.
- Verificación: Las pruebas originales de consola y red pasan.

## D3 - Accesibilidad del catálogo

- Mensaje: `image-alt (1); region (12)`
- Clasificación: Sitio / accesibilidad.
- Evidencia y causa raíz: axe identifica la imagen sin alt y doce nodos fuera de landmarks. El buscador también carece de label (E8), aunque este run no lo reporta como violación independiente.
- Corrección: Alt descriptivo en el logo, contenido dentro de main y etiqueta explícita del buscador. Se añadió main a inicio y login.
- Verificación: La auditoría axe original del catálogo exige cero violaciones.

## D4 - Condición de carrera del buscador

- Mensaje: `toHaveCount: Expected 1; Received 4`
- Clasificación: Sitio / condición de carrera.
- Evidencia y causa raíz: La acción fill comienza a 62119.992 ms; la API comienza a 62037.252 y dura 821.254 ms. El filtro se escribe antes de recibir los productos; el callback original llama pintar() sin el valor actual.
- Corrección: Tras cargar la API llamar pintar(document.getElementById('buscar').value). Se conserva sin cambios la prueba original.
- Verificación: carrito.spec.ts y RG-01; este último retiene la respuesta hasta terminar la escritura, sin depender de velocidad o sleeps.

## D5 - Vaciado no refleja el estado

- Mensaje: `toHaveText: Expected 0; Received 1`
- Clasificación: Sitio / mismo defecto de E6.
- Evidencia y causa raíz: La prueba nueva agrega un producto antes de vaciar: el contador visual permanece en 1 al lanzarse ReferenceError.
- Corrección: Actualizar explícitamente el contador tras poner carrito en 0.
- Verificación: CP-17 exige contador cero y ausencia de errores JavaScript.

## D6 - Sin aviso cuando falla la API

- Mensaje: `No pudimos cargar los productos: element(s) not found`
- Clasificación: Sitio / resiliencia.
- Evidencia y causa raíz: La ruta interceptada devuelve 500; el código intenta parsear Error interno como JSON y no tiene catch. El usuario nunca recibe un aviso.
- Corrección: Comprobar r.ok, capturar rechazo de fetch/JSON, limpiar la lista y mostrar una alerta accesible.
- Verificación: Prueba original con 500 y RG-02 con route.abort; ambas esperan el mensaje.

## V1 - Referencia visual inicial ausente

- Mensaje: `A snapshot doesn't exist; inicio-chromium-win32.png`
- Clasificación: Entorno / inicialización de referencia.
- Evidencia y causa raíz: El ZIP no contiene snapshots. El primer run genera la captura y falla; no prueba una regresión del sitio.
- Corrección: Revisar la imagen de inicio y crear las referencias de cada navegador; después comparar sin actualizar imágenes.
- Verificación: La estabilidad se ejecuta sin --update-snapshots; los tres PNG Windows se entregan en tests.

## D7 - Favicon faltante

- Mensaje: `Revisión del ZIP: public/favicon.ico no existe`
- Clasificación: Sitio / recurso faltante.
- Evidencia y causa raíz: El PDF menciona este defecto, pero las trazas de las pruebas originales aquí no registran una petición al favicon. Se distingue revisión de archivos de evidencia dinámica.
- Corrección: Crear public/favicon.ico y servir image/x-icon.
- Verificación: Recurso incluido; comprobación HTTP directa documentada en recursos.log.

## ENV1 - Certificado del registro npm

- Mensaje: `UNABLE_TO_VERIFY_LEAF_SIGNATURE`
- Clasificación: Entorno.
- Evidencia y causa raíz: La primera consulta npm no confía en la cadena de certificados del entorno.
- Corrección: Usar NODE_USE_SYSTEM_CA=1 durante la instalación para confiar en el almacén del sistema, sin desactivar validación TLS.
- Verificación: npm ci terminó correctamente; 102 paquetes instalados y cero vulnerabilidades en esa instalación.

## ENV2 - Ejecuciones compartían servidor

- Mensaje: `ERR_CONNECTION_REFUSED en localhost:3000 en intento-interferido`
- Clasificación: Entorno / interferencia entre ejecuciones.
- Evidencia y causa raíz: El laboratorio y la suite original compartieron servidor con reuseExistingServer; al terminar el primero, el segundo perdió el servidor.
- Corrección: Repetir la suite original de manera aislada y configurar reuseExistingServer:false. No atribuir esos fallos al login ni a la API.
- Verificación: Run original aislado: 12 pasan y 7 fallan; resultados válidos en suite-original. El intento interferido se conserva separado.

## LINT1 - Aserción dentro del Page Object

- Mensaje: `Test has no assertions en login-pom.spec.ts`
- Clasificación: Configuración de análisis estático.
- Evidencia y causa raíz: expect-expect no reconoce la aserción encapsulada en LoginPage.esperarError.
- Corrección: Registrar esperarError en assertFunctionNames, sin deshabilitar la regla para las demás pruebas. El plugin instalado compara el nombre final del método.
- Verificación: npm run lint termina sin errores; el laboratorio deliberado se audita aparte con --no-ignore.

## ENV3 - Presupuesto de espera insuficiente en Firefox

- Mensaje: `toHaveCount: Expected 4; Received 0; Timeout 5000ms en repeticiones 4 y 5`
- Clasificación: Entorno / inestabilidad de ejecución.
- Evidencia y causa raíz: Dos verificaciones de carga vencen en el primer intento de estabilidad. Las trazas muestran API 200 en 1897 ms y 862 ms, pero el snapshot al fallar ya contiene cuatro productos: el navegador termina de procesar después del límite. No se reportó una violación axe; el fallo ocurrió antes de ejecutar axe. Se conserva el intento completo en estabilidad-inicial.
- Corrección: Configurar expect.timeout=20000 y timeout=60000, mantener dos workers y repetir toda la suite sin retries locales ni actualización de imágenes. No se cambian los valores esperados ni los locators. El requisito no establece un SLA de cinco segundos.
- Verificación: Primer intento completo: 313 aprobadas y 2 fallidas; evidencia en estabilidad-inicial. Resultado posterior de las 315 ejecuciones en estabilidad. El margen temporal no representa una mejora de rendimiento del sitio.


## ENV4 - Captura del visor JSON

- Mensaje: locator.check agota el tiempo buscando el checkbox del visor interno.
- Clasificación: automatización documental; el contrato API había pasado.
- Corrección: usar teclado para activar la presentación y repetir las ocho capturas.
- Evidencia original: evidencias/capturas-intento-visor; resultado posterior: evidencias/capturas/resumen.json.
- Suite de aceptación ampliada: 345/345, sin fallos ni reintentos.


## Verificación remota - 21 de octubre de 2026

GitHub Actions pasó 345/345; instalación, lint y subida de artefacto terminaron correctamente. Reporte y logs descargados en evidencias/github. La protección de main devolvió 403 por el plan del repositorio privado; no se declara activada. Las referencias Linux se revisaron y se incorporaron para comparaciones estrictas posteriores.


## Publicación y protección autorizadas

El estudiante autorizó hacer público el repositorio para el docente. Se activó la protección de main que exige test. La segunda ejecución estricta, 39696522338, pasó 345/345 sin regenerar referencias; reporte descargado en github/comparacion-estricta. El 403 del plan privado es un antecedente ya resuelto.
