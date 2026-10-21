import { defineConfig } from 'eslint/config';
import tseslint from 'typescript-eslint';
import playwright from 'eslint-plugin-playwright';

export default defineConfig([
  { ignores: ['tests/errores-intencionales.spec.ts'] },
  {
    files: ['tests/**/*.ts'],
    extends: [playwright.configs['flat/recommended']],
    languageOptions: { parser: tseslint.parser },
    rules: {
      'playwright/expect-expect': ['error', { assertFunctionNames: ['esperarError'] }],
    },
  },
]);
