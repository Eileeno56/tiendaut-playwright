import { defineConfig } from '@playwright/test';
import config from './playwright.config';

export default defineConfig({
  ...config,
  testIgnore: [],
  testMatch: '**/errores-intencionales.spec.ts',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  projects: config.projects?.filter(project => project.name === 'chromium'),
});
