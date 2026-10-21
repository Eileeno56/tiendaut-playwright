# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: analisis.spec.ts >> Análisis de calidad del catálogo >> ninguna petición de red responde con error
- Location: tests\analisis.spec.ts:19:7

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByTestId('producto')
Expected: 4
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByTestId('producto') with timeout 5000ms
  - waiting for getByTestId('producto')
    6 × locator resolved to 0 elements
      - unexpected value "0"

```

# Page snapshot

```yaml
- main [ref=e2]:
  - heading "Catálogo" [level=1] [ref=e3]
  - paragraph [ref=e4]: "Carrito: 0 productos"
  - text: Buscar producto
  - textbox "Buscar producto" [ref=e5]
  - button "Vaciar carrito" [ref=e6]
  - img "TiendaUT" [ref=e7]
  - list [ref=e8]:
    - listitem [ref=e9]:
      - heading "Teclado mecánico" [level=2] [ref=e10]
      - text: $899
      - button "Agregar al carrito" [ref=e11]
    - listitem [ref=e12]:
      - heading "Mouse inalámbrico" [level=2] [ref=e13]
      - text: $349
      - button "Agregar al carrito" [ref=e14]
    - listitem [ref=e15]:
      - heading "Monitor 24 pulgadas" [level=2] [ref=e16]
      - text: $2799
      - button "Agregar al carrito" [ref=e17]
    - listitem [ref=e18]:
      - heading "Audífonos USB" [level=2] [ref=e19]
      - text: $459
      - button "Agregar al carrito" [ref=e20]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import AxeBuilder from '@axe-core/playwright';
  3  | 
  4  | test.describe('Análisis de calidad del catálogo', () => {
  5  | 
  6  |   test('no hay errores en la consola del navegador', async ({ page }) => {
  7  |     const mensajes: string[] = [];
  8  |     page.on('console', (msg) => {
  9  |       if (msg.type() === 'error') mensajes.push(msg.text());
  10 |     });
  11 |     page.on('pageerror', (err) => mensajes.push(err.message));
  12 | 
  13 |     await page.goto('/catalogo.html');
  14 |     await expect(page.getByTestId('producto')).toHaveCount(4);
  15 | 
  16 |     expect(mensajes, 'Errores encontrados en consola').toEqual([]);
  17 |   });
  18 | 
  19 |   test('ninguna petición de red responde con error', async ({ page }) => {
  20 |     const fallidas: string[] = [];
  21 |     page.on('response', (res) => {
  22 |       if (res.status() >= 400) fallidas.push(`${res.status()} ${res.url()}`);
  23 |     });
  24 | 
  25 |     await page.goto('/catalogo.html');
> 26 |     await expect(page.getByTestId('producto')).toHaveCount(4);
     |                                                ^ Error: expect(locator).toHaveCount(expected) failed
  27 | 
  28 |     expect(fallidas).toEqual([]);
  29 |   });
  30 | 
  31 |   test('la página no tiene violaciones de accesibilidad', async ({ page }) => {
  32 |     await page.goto('/catalogo.html');
  33 |     await expect(page.getByTestId('producto')).toHaveCount(4);
  34 | 
  35 |     const resultados = await new AxeBuilder({ page }).analyze();
  36 |     const resumen = resultados.violations.map(v => `${v.id}: ${v.help} (${v.nodes.length})`);
  37 | 
  38 |     expect(resumen).toEqual([]);
  39 |   });
  40 | });
  41 | 
```