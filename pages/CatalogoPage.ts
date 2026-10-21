import { type Page, type Locator } from '@playwright/test';

export class CatalogoPage {
  readonly buscador: Locator;
  readonly productos: Locator;
  readonly contador: Locator;
  readonly vaciar: Locator;

  constructor(readonly page: Page) {
    this.buscador = page.getByLabel('Buscar producto');
    this.productos = page.getByTestId('producto');
    this.contador = page.getByTestId('contador-carrito');
    this.vaciar = page.getByRole('button', { name: 'Vaciar carrito' });
  }

  async abrir() { await this.page.goto('/catalogo.html'); }
  async buscar(texto: string) { await this.buscador.fill(texto); }
  async agregar(nombre: string) {
    await this.productos.filter({ hasText: nombre })
      .getByRole('button', { name: 'Agregar al carrito' }).click();
  }
  async vaciarCarrito() { await this.vaciar.click(); }
}
