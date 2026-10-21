import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { LoginPage } from '../../pages/LoginPage';
import { CatalogoPage } from '../../pages/CatalogoPage';

const carpeta = path.resolve('evidencias/capturas/imagenes');
test.beforeAll(async () => { await mkdir(carpeta, { recursive: true }); });

test('evidencia: agregar y vaciar sin errores JavaScript', async ({ page }, testInfo) => {
  const errores: string[] = [];
  page.on('pageerror', error => errores.push(error.message));
  await page.goto('/catalogo.html');
  await page.getByTestId('producto').filter({ hasText: 'Teclado mecánico' })
    .getByRole('button', { name: 'Agregar al carrito' }).click();
  await expect(page.getByTestId('contador-carrito')).toHaveText('1');
  await page.screenshot({ path: path.join(carpeta, '01-carrito-con-producto.png'), fullPage: true });
  await page.getByRole('button', { name: 'Vaciar carrito' }).click();
  await expect(page.getByTestId('contador-carrito')).toHaveText('0');
  expect(errores).toEqual([]);
  await page.screenshot({ path: path.join(carpeta, '02-carrito-vacio.png'), fullPage: true });
  await testInfo.attach('errores-javascript.json', { body: JSON.stringify(errores), contentType: 'application/json' });
});

test('evidencia: filtrar antes de recibir productos', async ({ page }) => {
  let liberar!: () => void;
  const permiso = new Promise<void>(resolve => { liberar = resolve; });
  await page.route('**/api/productos', async route => { await permiso; await route.continue(); });
  await page.goto('/catalogo.html');
  await page.getByLabel('Buscar producto').fill('monitor');
  liberar();
  await expect(page.getByTestId('producto')).toHaveCount(1);
  await expect(page.getByTestId('producto')).toContainText('Monitor 24 pulgadas');
  await page.screenshot({ path: path.join(carpeta, '03-filtro-corregido.png'), fullPage: true });
});

test('evidencia: login vacío presenta alerta', async ({ page }) => {
  await page.goto('/login.html');
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(page.getByRole('alert')).toHaveText('Usuario o contraseña incorrectos');
  await expect(page).toHaveURL(/login\.html/);
  await page.locator('main').screenshot({ path: path.join(carpeta, '04-login-vacio.png') });
});

test('evidencia: contrato real de productos', async ({ page }, testInfo) => {
  const respuesta = await page.goto('/api/productos');
  expect(respuesta?.ok()).toBeTruthy();
  const productos = await respuesta!.json();
  expect(productos).toHaveLength(4);
  for (const producto of productos) {
    expect(producto.nombre.trim().length).toBeGreaterThan(0);
    expect(producto.precio).toBeGreaterThan(0);
  }
  // El control Pretty-print pertenece al visor JSON del navegador.
  // Se activa mediante teclado, sin depender de su DOM interno.
  await page.keyboard.press('Tab');
  await page.keyboard.press('Space');
  await page.screenshot({ path: path.join(carpeta, '05-api-productos.png'), clip: { x: 0, y: 0, width: 800, height: 600 } });
  await testInfo.attach('productos.json', { body: JSON.stringify(productos, null, 2), contentType: 'application/json' });
});

test('evidencia: API 500 presenta aviso', async ({ page }) => {
  await page.route('**/api/productos', route => route.fulfill({ status: 500, body: 'Error interno' }));
  await page.goto('/catalogo.html');
  await expect(page.getByRole('alert')).toHaveText('No pudimos cargar los productos');
  await page.screenshot({ path: path.join(carpeta, '06-error-api-controlado.png'), fullPage: true });
});

test('evidencia: consola, red y accesibilidad del catálogo', async ({ page }, testInfo) => {
  const consola: string[] = [];
  const red: string[] = [];
  page.on('console', message => { if (message.type() === 'error') consola.push(message.text()); });
  page.on('pageerror', error => consola.push(error.message));
  page.on('response', response => { if (response.status() >= 400) red.push(`${response.status()} ${response.url()}`); });
  await page.goto('/catalogo.html');
  await expect(page.getByTestId('producto')).toHaveCount(4);
  const axe = await new AxeBuilder({ page }).analyze();
  expect(consola).toEqual([]);
  expect(red).toEqual([]);
  expect(axe.violations).toEqual([]);
  await page.screenshot({ path: path.join(carpeta, '07-catalogo-auditado.png'), fullPage: true });
  await testInfo.attach('calidad.json', {
    body: JSON.stringify({ consola, red, violaciones: axe.violations, reglasComprobadas: axe.passes.length }, null, 2),
    contentType: 'application/json',
  });
});

test('evidencia: recorrido completo de acceso', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Bienvenido a TiendaUT');
  await page.screenshot({ path: path.join(carpeta, '12-inicio-flujo.png'), fullPage: true });
  await page.getByRole('link', { name: 'Iniciar sesión' }).click();
  const login = new LoginPage(page);
  await login.usuario.fill('alumno');
  await login.password.fill('utvm2026');
  await page.locator('main').screenshot({ path: path.join(carpeta, '13-login-flujo.png') });
  await login.botonEntrar.click();
  await expect(page).toHaveURL(/catalogo\.html/);
  await expect(page.getByTestId('producto')).toHaveCount(4);
  await page.screenshot({ path: path.join(carpeta, '14-catalogo-flujo.png'), fullPage: true });
});

test('evidencia: recorrido completo del carrito', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Catálogo', exact: true }).click();
  const catalogo = new CatalogoPage(page);
  await expect(catalogo.productos).toHaveCount(4);
  await catalogo.buscar('monitor');
  await catalogo.agregar('Monitor 24 pulgadas');
  await expect(catalogo.contador).toHaveText('1');
  await catalogo.buscar('mouse');
  await catalogo.agregar('Mouse inalámbrico');
  await expect(catalogo.contador).toHaveText('2');
  await page.screenshot({ path: path.join(carpeta, '15-carrito-dos-productos.png'), fullPage: true });
  await catalogo.vaciarCarrito();
  await expect(catalogo.contador).toHaveText('0');
  await page.screenshot({ path: path.join(carpeta, '16-carrito-flujo-final.png'), fullPage: true });
});
