# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: carrito.spec.ts >> Carrito de compras >> el buscador filtra los productos
- Location: tests\carrito.spec.ts:31:7

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByTestId('producto')
Expected: 1
Received: 4
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByTestId('producto') with timeout 5000ms
  - waiting for getByTestId('producto')
    5 × locator resolved to 0 elements
      - unexpected value "0"
    9 × locator resolved to 4 elements
      - unexpected value "4"

```

# Page snapshot

```yaml
- generic [ref=e1]:
  - heading "Catálogo" [level=1] [ref=e2]
  - paragraph [ref=e3]: "Carrito: 0 productos"
  - textbox "Buscar producto" [active] [ref=e4]: monitor
  - button "Vaciar carrito" [ref=e5]
  - list [ref=e7]:
    - listitem [ref=e8]:
      - heading "Teclado mecánico" [level=2] [ref=e9]
      - text: $899
      - button "Agregar al carrito" [ref=e10]
    - listitem [ref=e11]:
      - heading "Mouse inalámbrico" [level=2] [ref=e12]
      - text: $349
      - button "Agregar al carrito" [ref=e13]
    - listitem [ref=e14]:
      - heading "Monitor 24 pulgadas" [level=2] [ref=e15]
      - text: $2799
      - button "Agregar al carrito" [ref=e16]
    - listitem [ref=e17]:
      - heading "Audífonos USB" [level=2] [ref=e18]
      - text: $459
      - button "Agregar al carrito" [ref=e19]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Carrito de compras', () => {
  4  |   test.beforeEach(async ({ page }) => {
  5  |     await page.goto('/catalogo.html');
  6  |   });
  7  | 
  8  |   test('muestra los 4 productos del catálogo', async ({ page }) => {
  9  |     // La API tarda ~800 ms: toHaveCount reintenta hasta que se cumpla
  10 |     await expect(page.getByTestId('producto')).toHaveCount(4);
  11 |   });
  12 | 
  13 |   test('agregar dos productos actualiza el contador', async ({ page }) => {
  14 |     await test.step('Agregar el teclado', async () => {
  15 |       await page.getByTestId('producto')
  16 |         .filter({ hasText: 'Teclado mecánico' })
  17 |         .getByRole('button', { name: 'Agregar al carrito' })
  18 |         .click();
  19 |     });
  20 | 
  21 |     await test.step('Agregar el mouse', async () => {
  22 |       await page.getByTestId('producto')
  23 |         .filter({ hasText: 'Mouse inalámbrico' })
  24 |         .getByRole('button', { name: 'Agregar al carrito' })
  25 |         .click();
  26 |     });
  27 | 
  28 |     await expect(page.getByTestId('contador-carrito')).toHaveText('2');
  29 |   });
  30 | 
  31 |   test('el buscador filtra los productos', async ({ page }) => {
  32 |     await page.getByPlaceholder('Buscar producto').fill('monitor');
  33 | 
  34 |     const productos = page.getByTestId('producto');
> 35 |     await expect(productos).toHaveCount(1);
     |                             ^ Error: expect(locator).toHaveCount(expected) failed
  36 |     await expect(productos.first()).toContainText('Monitor 24 pulgadas');
  37 |   });
  38 | });
  39 | 
```