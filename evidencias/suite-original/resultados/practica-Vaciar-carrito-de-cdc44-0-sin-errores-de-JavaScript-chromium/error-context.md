# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: practica.spec.ts >> Vaciar carrito deja el contador en 0 sin errores de JavaScript
- Location: tests\practica.spec.ts:3:5

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator:  getByTestId('contador-carrito')
Expected: "0"
Received: "1"
Timeout:  5000ms

Call log:
  - Expect "toHaveText" getByTestId('contador-carrito') with timeout 5000ms
  - waiting for getByTestId('contador-carrito')
    14 × locator resolved to <span data-testid="contador-carrito">1</span>
       - unexpected value "1"

```

```yaml
- text: "1"
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('Vaciar carrito deja el contador en 0 sin errores de JavaScript', async ({ page }) => {
  4  |   const errores: string[] = [];
  5  |   page.on('pageerror', error => errores.push(error.message));
  6  |   await page.goto('/catalogo.html');
  7  |   const teclado = page.getByTestId('producto').filter({ hasText: 'Teclado mecánico' });
  8  |   await teclado.getByRole('button', { name: 'Agregar al carrito' }).click();
  9  |   await expect(page.getByTestId('contador-carrito')).toHaveText('1');
  10 |   await page.getByRole('button', { name: 'Vaciar carrito' }).click();
> 11 |   await expect(page.getByTestId('contador-carrito')).toHaveText('0');
     |                                                      ^ Error: expect(locator).toHaveText(expected) failed
  12 |   expect(errores).toEqual([]);
  13 | });
  14 | 
  15 | test('Iniciar sesión con los campos vacíos muestra el mensaje de error', async ({ page }) => {
  16 |   await page.goto('/login.html');
  17 |   await page.getByRole('button', { name: 'Entrar' }).click();
  18 |   await expect(page.getByRole('alert')).toHaveText('Usuario o contraseña incorrectos');
  19 |   await expect(page).toHaveURL(/login\.html/);
  20 | });
  21 | 
  22 | test('cada producto de la API tiene nombre y precio mayor que 0', async ({ request }) => {
  23 |   const respuesta = await request.get('/api/productos');
  24 |   expect(respuesta.ok()).toBeTruthy();
  25 |   const productos = await respuesta.json();
  26 |   expect(productos.length).toBeGreaterThan(0);
  27 |   for (const producto of productos) {
  28 |     expect(typeof producto.nombre).toBe('string');
  29 |     expect(producto.nombre.trim().length).toBeGreaterThan(0);
  30 |     expect(typeof producto.precio).toBe('number');
  31 |     expect(Number.isFinite(producto.precio)).toBeTruthy();
  32 |     expect(producto.precio).toBeGreaterThan(0);
  33 |   }
  34 | });
  35 | 
```