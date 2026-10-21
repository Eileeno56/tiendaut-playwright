const { chromium, expect } = require('@playwright/test');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');

async function capturar(browser, nombre, carpeta, esperado, puerto) {
  const cli = path.join(path.dirname(require.resolve('playwright/package.json')), 'cli.js');
  const child = spawn(process.execPath, [cli, 'show-report', carpeta, '--host', '127.0.0.1', '--port', String(puerto)], {
    windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'], env: { ...process.env, CODEX_CI: '1' },
  });
  try {
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('No inició el visor HTML')), 20000);
      child.stdout.on('data', data => {
        if (data.toString().includes('Serving HTML report')) { clearTimeout(timeout); resolve(); }
      });
      child.once('error', error => { clearTimeout(timeout); reject(error); });
      child.once('exit', code => { clearTimeout(timeout); reject(new Error(`El visor terminó: ${code}`)); });
    });
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(`http://127.0.0.1:${puerto}`);
    await expect(page.locator('body')).toContainText(esperado, { timeout: 20000 });
    await page.screenshot({ path: `evidencias/capturas/imagenes/${nombre}.png`, fullPage: false });
    await fs.writeFile(`evidencias/capturas/${nombre}.txt`, await page.locator('body').innerText());
    await page.close();
  } finally {
    child.kill();
  }
}

(async () => {
  await fs.mkdir('evidencias/capturas/imagenes', { recursive: true });
  const browser = await chromium.launch();
  try {
    if (process.argv.includes('--github')) {
      await capturar(browser, '18-github-linux', 'evidencias/github/artefacto/playwright-report', 'Passed', 9339);
    } else {
    await capturar(browser, '08-laboratorio-original', 'evidencias/laboratorio-original/reporte', 'Failed', 9334);
    await capturar(browser, '09-suite-original', 'evidencias/suite-original/reporte', 'Failed', 9335);
    await capturar(browser, '10-estabilidad-315', 'evidencias/estabilidad/reporte', 'Passed', 9336);
    await capturar(browser, '11-pruebas-de-evidencia', 'evidencias/capturas/reporte', 'Passed', 9337);
    await capturar(browser, '17-estabilidad-345', 'evidencias/estabilidad-ampliada/reporte', 'Passed', 9338);
    }
    console.log('Capturas tomadas de los reportes HTML reales.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
