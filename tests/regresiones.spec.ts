import { test, expect } from '@playwright/test';

test('conserva el filtro escrito antes de que responda la API', async ({ page }) => {
  let liberar!: () => void;
  const permiso = new Promise<void>(resolve => { liberar = resolve; });
  await page.route('**/api/productos', async route => {
    await permiso;
    await route.continue();
  });
  await page.goto('/catalogo.html');
  await page.getByLabel('Buscar producto').fill('monitor');
  liberar();
  await expect(page.getByTestId('producto')).toHaveCount(1);
  await expect(page.getByTestId('producto')).toContainText('Monitor 24 pulgadas');
});

test('avisa cuando la petición de productos se interrumpe', async ({ page }) => {
  const errores: string[] = [];
  page.on('pageerror', error => errores.push(error.message));
  await page.route('**/api/productos', route => route.abort());
  await page.goto('/catalogo.html');
  await expect(page.getByRole('alert')).toHaveText('No pudimos cargar los productos');
  await expect(page.getByTestId('producto')).toHaveCount(0);
  expect(errores).toEqual([]);
});
