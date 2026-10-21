# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: errores-intencionales.spec.ts >> Laboratorio de errores @laboratorio >> E2 - el locator encuentra varios elementos (strict mode)
- Location: tests\errores-intencionales.spec.ts:13:7

# Error details

```
Error: locator.click: Error: strict mode violation: getByRole('button', { name: 'Agregar al carrito' }) resolved to 4 elements:
    1) <button>Agregar al carrito</button> aka getByRole('listitem').filter({ hasText: 'Teclado mecánico$899 Agregar' }).getByRole('button')
    2) <button>Agregar al carrito</button> aka getByRole('listitem').filter({ hasText: 'Mouse inalámbrico$349 Agregar' }).getByRole('button')
    3) <button>Agregar al carrito</button> aka getByRole('listitem').filter({ hasText: 'Monitor 24 pulgadas$2799' }).getByRole('button')
    4) <button>Agregar al carrito</button> aka getByRole('listitem').filter({ hasText: 'Audífonos USB$459 Agregar al' }).getByRole('button')

Call log:
  - waiting for getByRole('button', { name: 'Agregar al carrito' })

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
  2  | 
  3  | // Pruebas que FALLAN A PROPÓSITO para estudiar los mensajes de error.
  4  | // Ejecútalas con:  npm run test:laboratorio
  5  | 
  6  | test.describe('Laboratorio de errores @laboratorio', () => {
  7  |   test('E1 - el elemento no existe (timeout)', async ({ page }) => {
  8  |     test.setTimeout(8000);
  9  |     await page.goto('/catalogo.html');
  10 |     await page.getByRole('button', { name: 'Comprar ahora' }).click();
  11 |   });
  12 | 
  13 |   test('E2 - el locator encuentra varios elementos (strict mode)', async ({ page }) => {
  14 |     await page.goto('/catalogo.html');
  15 |     await expect(page.getByTestId('producto')).toHaveCount(4);
> 16 |     await page.getByRole('button', { name: 'Agregar al carrito' }).click();
     |                                                                    ^ Error: locator.click: Error: strict mode violation: getByRole('button', { name: 'Agregar al carrito' }) resolved to 4 elements:
  17 |   });
  18 | 
  19 |   test('E3 - el texto no coincide (Expected vs Received)', async ({ page }) => {
  20 |     await page.goto('/');
  21 |     await expect(page.getByRole('heading', { level: 1 })).toHaveText('Bienvenidos a TiendaUT');
  22 |   });
  23 | 
  24 |   test('E4 - la URL no es la esperada', async ({ page }) => {
  25 |     await page.goto('/login.html');
  26 |     await page.getByLabel('Usuario').fill('alumno');
  27 |     await page.getByLabel('Contraseña').fill('mal');
  28 |     await page.getByRole('button', { name: 'Entrar' }).click();
  29 |     await expect(page).toHaveURL(/catalogo\.html/);
  30 |   });
  31 | 
  32 |   test('E5 - el servidor no está levantado', async ({ page }) => {
  33 |     await page.goto('http://localhost:3999/');
  34 |   });
  35 | 
  36 |   test('E6 - el sitio lanza un error de JavaScript', async ({ page }) => {
  37 |     const errores: string[] = [];
  38 |     page.on('pageerror', (error) => errores.push(error.message));
  39 | 
  40 |     await page.goto('/catalogo.html');
  41 |     await page.getByRole('button', { name: 'Vaciar carrito' }).click();
  42 | 
  43 |     expect(errores).toEqual([]);
  44 |   });
  45 | 
  46 |   test('E7 - olvidé el await', async ({ page }) => {
  47 |     await page.goto('/');
  48 |     expect(page.getByRole('heading', { name: 'No existe' })).toBeVisible(); // sin await
  49 |   });
  50 | 
  51 |   test('E8 - getByLabel sobre un campo sin etiqueta', async ({ page }) => {
  52 |     test.setTimeout(8000);
  53 |     await page.goto('/catalogo.html');
  54 |     await page.getByLabel('Buscar producto').fill('mouse');
  55 |   });
  56 | });
  57 | 
```