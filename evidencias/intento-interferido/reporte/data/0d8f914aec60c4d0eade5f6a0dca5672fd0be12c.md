# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login-pom.spec.ts >> login incorrecto usando Page Object
- Location: tests\login-pom.spec.ts:11:5

# Error details

```
Error: page.goto: net::ERR_CONNECTION_RESET at http://localhost:3000/login.html
Call log:
  - navigating to "http://localhost:3000/login.html", waiting until "load"

```

# Test source

```ts
  1  | import { type Page, type Locator, expect } from '@playwright/test';
  2  | 
  3  | export class LoginPage {
  4  |   readonly page: Page;
  5  |   readonly usuario: Locator;
  6  |   readonly password: Locator;
  7  |   readonly botonEntrar: Locator;
  8  |   readonly mensajeError: Locator;
  9  | 
  10 |   constructor(page: Page) {
  11 |     this.page = page;
  12 |     this.usuario = page.getByLabel('Usuario');
  13 |     this.password = page.getByLabel('Contraseña');
  14 |     this.botonEntrar = page.getByRole('button', { name: 'Entrar' });
  15 |     this.mensajeError = page.getByRole('alert');
  16 |   }
  17 | 
  18 |   async abrir() {
> 19 |     await this.page.goto('/login.html');
     |                     ^ Error: page.goto: net::ERR_CONNECTION_RESET at http://localhost:3000/login.html
  20 |   }
  21 | 
  22 |   async iniciarSesion(usuario: string, password: string) {
  23 |     await this.usuario.fill(usuario);
  24 |     await this.password.fill(password);
  25 |     await this.botonEntrar.click();
  26 |   }
  27 | 
  28 |   async esperarError(texto: string) {
  29 |     await expect(this.mensajeError).toHaveText(texto);
  30 |   }
  31 | }
  32 | 
```