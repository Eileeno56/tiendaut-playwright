import { defineConfig } from '@playwright/test';
import config from './playwright.config';

export default defineConfig({
  ...config,
  testDir: './evidencias/capturas',
  testIgnore: [],
  workers: 1,
  retries: 0,
  outputDir: './evidencias/capturas/resultados',
  reporter: [
    ['list'],
    ['html', { outputFolder: 'evidencias/capturas/reporte', open: 'never' }],
    ['json', { outputFile: 'evidencias/capturas/resumen.json' }],
  ],
  use: { ...config.use, trace: 'on', screenshot: 'on' },
  projects: config.projects?.filter(project => project.name === 'chromium'),
});
