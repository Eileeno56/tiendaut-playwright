import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',              // carpeta donde viven las pruebas
  testIgnore: '**/errores-intencionales.spec.ts', // el laboratorio tiene configuración propia
  workers: 2,
  timeout: 60_000,
  expect: { timeout: 20_000 }, // margen para la planificación del navegador en este entorno
  fullyParallel: true,             // ejecuta pruebas en paralelo
  forbidOnly: !!process.env.CI,    // en CI falla si alguien dejó un test.only
  retries: process.env.CI ? 2 : 0, // reintentos solo en CI
  reporter: [['html', { open: 'never' }], ['list'], ['json', { outputFile: process.env.PW_RESULTS_JSON || 'test-results/resumen.json' }]],

  use: {
    baseURL: 'http://localhost:3000', // permite escribir page.goto('/login.html')
    trace: 'retain-on-failure',       // guarda la "caja negra" de cada prueba fallida
    screenshot: 'only-on-failure',    // captura de pantalla al fallar
    video: 'retain-on-failure',       // video al fallar
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
  ],

  // Levanta el sitio automáticamente antes de probar
  webServer: {
    command: 'node server.js',
    url: 'http://localhost:3000',
    reuseExistingServer: false, // cada ejecución controla el ciclo de vida de su servidor
  },
});
