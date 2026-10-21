import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { CatalogoPage } from '../pages/CatalogoPage';

test.describe('Flujos críticos completos de TiendaUT', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); });

  test('FC-01: desde inicio, iniciar sesión y consultar el catálogo cargado', async ({ page }) => {
    await page.getByRole('link', { name: 'Iniciar sesión' }).click();
    await expect(page).toHaveURL(/login\.html/);
    const login = new LoginPage(page);
    await login.iniciarSesion('alumno', 'utvm2026');
    const catalogo = new CatalogoPage(page);
    await expect(page).toHaveURL(/catalogo\.html/);
    await expect(page.getByRole('heading', { name: 'Catálogo', exact: true })).toBeVisible();
    await expect(catalogo.productos).toHaveCount(4);
    await expect(catalogo.contador).toHaveText('0');
  });

  test('FC-02: desde inicio, buscar, agregar dos productos y vaciar el carrito', async ({ page }) => {
    const errores: string[] = [];
    page.on('pageerror', error => errores.push(error.message));
    await page.getByRole('link', { name: 'Catálogo', exact: true }).click();
    const catalogo = new CatalogoPage(page);
    await expect(catalogo.productos).toHaveCount(4);
    await catalogo.buscar('monitor');
    await expect(catalogo.productos).toHaveCount(1);
    await catalogo.agregar('Monitor 24 pulgadas');
    await expect(catalogo.contador).toHaveText('1');
    await catalogo.buscar('mouse');
    await expect(catalogo.productos).toHaveCount(1);
    await catalogo.agregar('Mouse inalámbrico');
    await expect(catalogo.contador).toHaveText('2');
    await catalogo.vaciarCarrito();
    await expect(catalogo.contador).toHaveText('0');
    expect(errores).toEqual([]);
  });
});
