# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: documentacion.spec.ts >> evidencia: contrato real de productos
- Location: evidencias\capturas\documentacion.spec.ts:46:5

# Error details

```
Test timeout of 60000ms exceeded.
```

```
Error: locator.check: Test timeout of 60000ms exceeded.
Call log:
  - waiting for getByRole('checkbox')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]: "[{\"id\":1,\"nombre\":\"Teclado mecánico\",\"precio\":899},{\"id\":2,\"nombre\":\"Mouse inalámbrico\",\"precio\":349},{\"id\":3,\"nombre\":\"Monitor 24 pulgadas\",\"precio\":2799},{\"id\":4,\"nombre\":\"Audífonos USB\",\"precio\":459}]"
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | import AxeBuilder from '@axe-core/playwright';
  3   | import { mkdir } from 'node:fs/promises';
  4   | import path from 'node:path';
  5   | import { LoginPage } from '../../pages/LoginPage';
  6   | import { CatalogoPage } from '../../pages/CatalogoPage';
  7   | 
  8   | const carpeta = path.resolve('evidencias/capturas/imagenes');
  9   | test.beforeAll(async () => { await mkdir(carpeta, { recursive: true }); });
  10  | 
  11  | test('evidencia: agregar y vaciar sin errores JavaScript', async ({ page }, testInfo) => {
  12  |   const errores: string[] = [];
  13  |   page.on('pageerror', error => errores.push(error.message));
  14  |   await page.goto('/catalogo.html');
  15  |   await page.getByTestId('producto').filter({ hasText: 'Teclado mecánico' })
  16  |     .getByRole('button', { name: 'Agregar al carrito' }).click();
  17  |   await expect(page.getByTestId('contador-carrito')).toHaveText('1');
  18  |   await page.screenshot({ path: path.join(carpeta, '01-carrito-con-producto.png'), fullPage: true });
  19  |   await page.getByRole('button', { name: 'Vaciar carrito' }).click();
  20  |   await expect(page.getByTestId('contador-carrito')).toHaveText('0');
  21  |   expect(errores).toEqual([]);
  22  |   await page.screenshot({ path: path.join(carpeta, '02-carrito-vacio.png'), fullPage: true });
  23  |   await testInfo.attach('errores-javascript.json', { body: JSON.stringify(errores), contentType: 'application/json' });
  24  | });
  25  | 
  26  | test('evidencia: filtrar antes de recibir productos', async ({ page }) => {
  27  |   let liberar!: () => void;
  28  |   const permiso = new Promise<void>(resolve => { liberar = resolve; });
  29  |   await page.route('**/api/productos', async route => { await permiso; await route.continue(); });
  30  |   await page.goto('/catalogo.html');
  31  |   await page.getByLabel('Buscar producto').fill('monitor');
  32  |   liberar();
  33  |   await expect(page.getByTestId('producto')).toHaveCount(1);
  34  |   await expect(page.getByTestId('producto')).toContainText('Monitor 24 pulgadas');
  35  |   await page.screenshot({ path: path.join(carpeta, '03-filtro-corregido.png'), fullPage: true });
  36  | });
  37  | 
  38  | test('evidencia: login vacío presenta alerta', async ({ page }) => {
  39  |   await page.goto('/login.html');
  40  |   await page.getByRole('button', { name: 'Entrar' }).click();
  41  |   await expect(page.getByRole('alert')).toHaveText('Usuario o contraseña incorrectos');
  42  |   await expect(page).toHaveURL(/login\.html/);
  43  |   await page.locator('main').screenshot({ path: path.join(carpeta, '04-login-vacio.png') });
  44  | });
  45  | 
  46  | test('evidencia: contrato real de productos', async ({ page }, testInfo) => {
  47  |   const respuesta = await page.goto('/api/productos');
  48  |   expect(respuesta?.ok()).toBeTruthy();
  49  |   const productos = await respuesta!.json();
  50  |   expect(productos).toHaveLength(4);
  51  |   for (const producto of productos) {
  52  |     expect(producto.nombre.trim().length).toBeGreaterThan(0);
  53  |     expect(producto.precio).toBeGreaterThan(0);
  54  |   }
> 55  |   await page.getByRole('checkbox').check();
      |                                    ^ Error: locator.check: Test timeout of 60000ms exceeded.
  56  |   await page.screenshot({ path: path.join(carpeta, '05-api-productos.png'), clip: { x: 0, y: 0, width: 800, height: 600 } });
  57  |   await testInfo.attach('productos.json', { body: JSON.stringify(productos, null, 2), contentType: 'application/json' });
  58  | });
  59  | 
  60  | test('evidencia: API 500 presenta aviso', async ({ page }) => {
  61  |   await page.route('**/api/productos', route => route.fulfill({ status: 500, body: 'Error interno' }));
  62  |   await page.goto('/catalogo.html');
  63  |   await expect(page.getByRole('alert')).toHaveText('No pudimos cargar los productos');
  64  |   await page.screenshot({ path: path.join(carpeta, '06-error-api-controlado.png'), fullPage: true });
  65  | });
  66  | 
  67  | test('evidencia: consola, red y accesibilidad del catálogo', async ({ page }, testInfo) => {
  68  |   const consola: string[] = [];
  69  |   const red: string[] = [];
  70  |   page.on('console', message => { if (message.type() === 'error') consola.push(message.text()); });
  71  |   page.on('pageerror', error => consola.push(error.message));
  72  |   page.on('response', response => { if (response.status() >= 400) red.push(`${response.status()} ${response.url()}`); });
  73  |   await page.goto('/catalogo.html');
  74  |   await expect(page.getByTestId('producto')).toHaveCount(4);
  75  |   const axe = await new AxeBuilder({ page }).analyze();
  76  |   expect(consola).toEqual([]);
  77  |   expect(red).toEqual([]);
  78  |   expect(axe.violations).toEqual([]);
  79  |   await page.screenshot({ path: path.join(carpeta, '07-catalogo-auditado.png'), fullPage: true });
  80  |   await testInfo.attach('calidad.json', {
  81  |     body: JSON.stringify({ consola, red, violaciones: axe.violations, reglasComprobadas: axe.passes.length }, null, 2),
  82  |     contentType: 'application/json',
  83  |   });
  84  | });
  85  | 
  86  | test('evidencia: recorrido completo de acceso', async ({ page }) => {
  87  |   await page.goto('/');
  88  |   await expect(page.getByRole('heading', { level: 1 })).toHaveText('Bienvenido a TiendaUT');
  89  |   await page.screenshot({ path: path.join(carpeta, '12-inicio-flujo.png'), fullPage: true });
  90  |   await page.getByRole('link', { name: 'Iniciar sesión' }).click();
  91  |   const login = new LoginPage(page);
  92  |   await login.usuario.fill('alumno');
  93  |   await login.password.fill('utvm2026');
  94  |   await page.locator('main').screenshot({ path: path.join(carpeta, '13-login-flujo.png') });
  95  |   await login.botonEntrar.click();
  96  |   await expect(page).toHaveURL(/catalogo\.html/);
  97  |   await expect(page.getByTestId('producto')).toHaveCount(4);
  98  |   await page.screenshot({ path: path.join(carpeta, '14-catalogo-flujo.png'), fullPage: true });
  99  | });
  100 | 
  101 | test('evidencia: recorrido completo del carrito', async ({ page }) => {
  102 |   await page.goto('/');
  103 |   await page.getByRole('link', { name: 'Catálogo', exact: true }).click();
  104 |   const catalogo = new CatalogoPage(page);
  105 |   await expect(catalogo.productos).toHaveCount(4);
  106 |   await catalogo.buscar('monitor');
  107 |   await catalogo.agregar('Monitor 24 pulgadas');
  108 |   await expect(catalogo.contador).toHaveText('1');
  109 |   await catalogo.buscar('mouse');
  110 |   await catalogo.agregar('Mouse inalámbrico');
  111 |   await expect(catalogo.contador).toHaveText('2');
  112 |   await page.screenshot({ path: path.join(carpeta, '15-carrito-dos-productos.png'), fullPage: true });
  113 |   await catalogo.vaciarCarrito();
  114 |   await expect(catalogo.contador).toHaveText('0');
  115 |   await page.screenshot({ path: path.join(carpeta, '16-carrito-flujo-final.png'), fullPage: true });
  116 | });
  117 | 
```