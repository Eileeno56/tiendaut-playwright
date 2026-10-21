import { test, expect } from '@playwright/test';

test('Vaciar carrito deja el contador en 0 sin errores de JavaScript', async ({ page }) => {
  const errores: string[] = [];
  page.on('pageerror', error => errores.push(error.message));
  await page.goto('/catalogo.html');
  const teclado = page.getByTestId('producto').filter({ hasText: 'Teclado mecánico' });
  await teclado.getByRole('button', { name: 'Agregar al carrito' }).click();
  await expect(page.getByTestId('contador-carrito')).toHaveText('1');
  await page.getByRole('button', { name: 'Vaciar carrito' }).click();
  await expect(page.getByTestId('contador-carrito')).toHaveText('0');
  expect(errores).toEqual([]);
});

test('Iniciar sesión con los campos vacíos muestra el mensaje de error', async ({ page }) => {
  await page.goto('/login.html');
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(page.getByRole('alert')).toHaveText('Usuario o contraseña incorrectos');
  await expect(page).toHaveURL(/login\.html/);
});

test('cada producto de la API tiene nombre y precio mayor que 0', async ({ request }) => {
  const respuesta = await request.get('/api/productos');
  expect(respuesta.ok()).toBeTruthy();
  const productos = await respuesta.json();
  expect(productos.length).toBeGreaterThan(0);
  for (const producto of productos) {
    expect(typeof producto.nombre).toBe('string');
    expect(producto.nombre.trim().length).toBeGreaterThan(0);
    expect(typeof producto.precio).toBe('number');
    expect(Number.isFinite(producto.precio)).toBeTruthy();
    expect(producto.precio).toBeGreaterThan(0);
  }
});
