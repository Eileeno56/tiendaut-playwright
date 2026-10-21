# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: analisis.spec.ts >> Análisis de calidad del catálogo >> ninguna petición de red responde con error
- Location: tests\analisis.spec.ts:19:7

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 3

- Array []
+ Array [
+   "404 http://localhost:3000/logo.png",
+ ]
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - heading "Catálogo" [level=1] [ref=e2]
  - paragraph [ref=e3]: "Carrito: 0 productos"
  - textbox "Buscar producto" [ref=e4]
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
  26 |     await expect(page.getByTestId('producto')).toHaveCount(4);
  27 | 
> 28 |     expect(fallidas).toEqual([]);
     |                      ^ Error: expect(received).toEqual(expected) // deep equality
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