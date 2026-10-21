# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login.spec.ts >> Inicio de sesión >> con contraseña incorrecta muestra un mensaje de error
- Location: tests\login.spec.ts:17:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/login.html
Call log:
  - navigating to "http://localhost:3000/login.html", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Inicio de sesión', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/login.html');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/login.html
  6  |   });
  7  | 
  8  |   test('con credenciales válidas entra al catálogo', async ({ page }) => {
  9  |     await page.getByLabel('Usuario').fill('alumno');
  10 |     await page.getByLabel('Contraseña').fill('utvm2026');
  11 |     await page.getByRole('button', { name: 'Entrar' }).click();
  12 | 
  13 |     await expect(page).toHaveURL(/catalogo\.html/);
  14 |     await expect(page.getByRole('heading', { name: 'Catálogo' })).toBeVisible();
  15 |   });
  16 | 
  17 |   test('con contraseña incorrecta muestra un mensaje de error', async ({ page }) => {
  18 |     await page.getByLabel('Usuario').fill('alumno');
  19 |     await page.getByLabel('Contraseña').fill('equivocada');
  20 |     await page.getByRole('button', { name: 'Entrar' }).click();
  21 | 
  22 |     await expect(page.getByRole('alert')).toHaveText('Usuario o contraseña incorrectos');
  23 |     await expect(page).toHaveURL(/login\.html/); // no debe avanzar
  24 |   });
  25 | });
  26 | 
```