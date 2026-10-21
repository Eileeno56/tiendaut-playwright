# Casos nuevos y trazabilidad

Fuente: Práctica Playwright.pdf, capítulo 19, Práctica 1, página 53.

| ID | Requisito / precondición | Pasos y datos | Resultado esperado | Automatización |
|---|---|---|---|---|
| CP-17 | Vaciar un carrito con contenido, sin errores JS | Abrir catálogo, agregar Teclado mecánico, comprobar 1, pulsar Vaciar carrito | Contador 0; colección pageerror vacía | tests/practica.spec.ts, prueba 1 |
| CP-18 | Validar credenciales vacías | Abrir login, dejar ambos campos vacíos, pulsar Entrar | Alerta Usuario o contraseña incorrectos; URL sigue en login.html | tests/practica.spec.ts, prueba 2 |
| CP-19 | Contrato de todos los productos | GET /api/productos | Respuesta exitosa, colección no vacía; cada nombre es texto no vacío; precio numérico finito mayor que 0 | tests/practica.spec.ts, prueba 3 |
| RG-01 | Conservar un filtro escrito antes de la respuesta | Retener petición mediante page.route y una promesa, escribir monitor con getByLabel, liberar petición | Exactamente un producto: Monitor 24 pulgadas | tests/regresiones.spec.ts, prueba 1 |
| RG-02 | Manejar interrupción de red | Abortar /api/productos con page.route | Alerta No pudimos cargar los productos; cero productos y cero pageerror | tests/regresiones.spec.ts, prueba 2 |

Las tres pruebas obligatorias se ejecutaron primero contra el sitio original: CP-17 falló (contador 1 en lugar de 0); CP-18 y CP-19 pasaron. Las dos regresiones adicionales verifican situaciones de carga asíncrona sin usar pausas fijas.

Se conservan las 16 pruebas normales originales, el Page Object LoginPage y el fixture. No se relajaron aserciones. Las ocho demostraciones E1-E8 se conservan con sus errores deliberados y se ejecutan exclusivamente con la configuración de laboratorio; su resultado rojo es material didáctico, no parte de la suite de aceptación.
