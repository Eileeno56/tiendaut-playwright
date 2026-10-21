# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: red-y-visual.spec.ts >> si la API falla, el catálogo debe avisar al usuario
- Location: tests\red-y-visual.spec.ts:3:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('No pudimos cargar los productos')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByText('No pudimos cargar los productos') with timeout 5000ms
  - waiting for getByText('No pudimos cargar los productos')

```

```yaml
- heading "Catálogo" [level=1]
- paragraph: "Carrito: 0 productos"
- textbox "Buscar producto"
- button "Vaciar carrito"
- img
- list:
  - listitem: Cargando...
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('si la API falla, el catálogo debe avisar al usuario', async ({ page }) => {
  4  |   // Interceptamos la petición y respondemos con un error 500 simulado
  5  |   await page.route('**/api/productos', (route) =>
  6  |     route.fulfill({ status: 500, body: 'Error interno' }),
  7  |   );
  8  | 
  9  |   await page.goto('/catalogo.html');
  10 | 
> 11 |   await expect(page.getByText('No pudimos cargar los productos')).toBeVisible();
     |                                                                   ^ Error: expect(locator).toBeVisible() failed
  12 | });
  13 | 
  14 | test('la página de inicio se ve igual que la referencia', async ({ page }) => {
  15 |   await page.goto('/');
  16 |   await expect(page).toHaveScreenshot('inicio.png');
  17 | });
  18 | 
```