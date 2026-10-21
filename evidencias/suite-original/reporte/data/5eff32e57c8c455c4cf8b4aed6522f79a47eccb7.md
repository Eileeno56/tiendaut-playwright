# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: red-y-visual.spec.ts >> la página de inicio se ve igual que la referencia
- Location: tests\red-y-visual.spec.ts:14:5

# Error details

```
Error: A snapshot doesn't exist at C:\Users\user\Documents\labra\tiendaut-playwright\tests\red-y-visual.spec.ts-snapshots\inicio-chromium-win32.png, writing actual.
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - navigation [ref=e2]:
    - link "Iniciar sesión" [ref=e3] [cursor=pointer]:
      - /url: /login.html
    - link "Catálogo" [ref=e4] [cursor=pointer]:
      - /url: /catalogo.html
  - heading "Bienvenido a TiendaUT" [level=1] [ref=e5]
  - paragraph [ref=e6]: Tu tienda de tecnología universitaria.
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
  11 |   await expect(page.getByText('No pudimos cargar los productos')).toBeVisible();
  12 | });
  13 | 
  14 | test('la página de inicio se ve igual que la referencia', async ({ page }) => {
  15 |   await page.goto('/');
> 16 |   await expect(page).toHaveScreenshot('inicio.png');
     |   ^ Error: A snapshot doesn't exist at C:\Users\user\Documents\labra\tiendaut-playwright\tests\red-y-visual.spec.ts-snapshots\inicio-chromium-win32.png, writing actual.
  17 | });
  18 | 
```