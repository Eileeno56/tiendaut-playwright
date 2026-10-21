"""Genera el informe desde los resultados reales y la bitácora estructurada."""
from pathlib import Path
import json
from collections import Counter
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT/'documentacion/defectos.json').read_text(encoding='utf-8'))
result = json.loads((ROOT/'evidencias/estabilidad/resumen.json').read_text(encoding='utf-8'))
counts, statuses = Counter(), Counter()
def walk(suite):
    for spec in suite.get('specs', []):
        for test in spec['tests']:
            counts[test['projectName']] += 1
            statuses[test['status']] += 1
    for child in suite.get('suites', []):
        walk(child)
for suite in result['suites']:
    walk(suite)
stats = result['stats']
assert stats['expected'] == 315 and stats['unexpected'] == 0 and stats['flaky'] == 0 and stats['skipped'] == 0, stats
assert dict(counts) == {'chromium':105,'firefox':105,'webkit':105}, counts
duration = round(stats['duration']/1000,1)

md = ['# Bitácora de análisis de defectos', '', 'Práctica 1 · TiendaUT · 15 de octubre de 2026 · America/Mexico_City.', '',
      'Método: leer el mensaje, ubicar la acción, reproducir contra el sitio original, inspeccionar las trazas (acciones, DOM y red), clasificar, corregir y confirmar. Las trazas se inspeccionaron como JSON; no se afirma haber usado gráficamente Trace Viewer. Los archivos originales y sus capturas se conservan en el índice.', '',
      'Laboratorio original: 8 fallos previstos. Suite original aislada con las tres pruebas nuevas: 12 pasan y 7 fallan. Validación corregida: 63/63. Estabilidad: 315/315, cero fallos, flaky o saltos. GitHub remoto pendiente de acceso.', '']
index = ['# Índice de evidencias', '', 'Rutas relativas a este documento. Abrir los reportes con npx playwright show-report desde la raíz del proyecto.', '']
for r in records:
    md += [f"## {r['id']} - {r['titulo']}", '', f"- Mensaje: `{r['mensaje']}`", f"- Clasificación: {r['clase']}.", f"- Evidencia y causa raíz: {r['causa']}", f"- Corrección: {r['correccion']}", f"- Verificación: {r['verificacion']}", '']
    index += [f"## {r['id']} - {r['titulo']}", '']
    if r['grupo'] in ('laboratorio', 'suite'):
        folder = 'laboratorio-original' if r['grupo'] == 'laboratorio' else 'suite-original'
        for directory in (ROOT/f'evidencias/{folder}/resultados').glob(r['patron']):
            for name in ['trace.zip','test-failed-1.png','error-context.md','video.webm']:
                p=directory/name
                if p.exists():
                    index.append(f'- [{name}](../{p.relative_to(ROOT).as_posix()})')
    else:
        index.append('- [Recursos HTTP](../evidencias/analisis/recursos.log) · [Lint final](../evidencias/analisis/lint-final.log) · [Auditoría del laboratorio](../evidencias/analisis/lint-con-laboratorio.log)')
        if r['id']=='ENV2':
            index.append('- [Log del intento interferido](../evidencias/intento-interferido/ejecucion.log)')
        if r['id']=='ENV3':
            index.append('- [Log de estabilidad inicial](../evidencias/estabilidad-inicial/ejecucion.log)')
            for p in (ROOT/'evidencias/estabilidad-inicial/resultados').glob('*/trace.zip'):
                index.append(f'- [Traza Firefox](../{p.relative_to(ROOT).as_posix()})')
    index.append('')
(ROOT/'documentacion/BITACORA.md').write_text('\n'.join(md),encoding='utf-8')
(ROOT/'documentacion/INDICE-EVIDENCIAS.md').write_text('\n'.join(index),encoding='utf-8')

rows=[['Comprobación','Resultado'],['Laboratorio original','8 fallos didácticos'],['Suite original aislada','12 aprobadas / 7 fallidas'],['Validación corregida','63 / 63'],['Estabilidad inicial (5 s)','313 aprobadas / 2 fallidas'],['Chromium (5 repeticiones)',f"{counts['chromium']} / 105"],['Firefox (5 repeticiones)',f"{counts['firefox']} / 105"],['WebKit (5 repeticiones)',f"{counts['webkit']} / 105"],['Total estabilidad','315 / 315'],['Fallos / flaky / saltos','0 / 0 / 0'],['Duración de estabilidad',f'{duration} segundos'],['ESLint','Sin errores'],['GitHub Actions remoto','Pendiente de publicación']]
summary=['# Resultados comprobados','','Fecha: 15 de octubre de 2026 (America/Mexico_City). Windows; Node 24.18.0; Playwright 1.64.1; axe 4.14.0.','','| Comprobación | Resultado |','|---|---|']
summary.extend(f'| {a} | {b} |' for a,b in rows[1:])
summary += ['', 'Comando real de estabilidad, sin actualizar referencias:', '', '```bash', 'npx playwright test --repeat-each=5 --fail-on-flaky-tests --output=evidencias/estabilidad/resultados', '```', '',
 'HTML en evidencias/estabilidad/reporte mediante PLAYWRIGHT_HTML_OUTPUT_DIR; JSON en evidencias/estabilidad/resumen.json mediante PW_RESULTS_JSON. Los recuentos provienen del JSON real. Recursos /, login, catálogo, logo, favicon y API: HTTP 200 y MIME correctos (recursos.log).', '',
 'Las ocho demostraciones no forman parte de los 315 casos de aceptación. La creación inicial de referencias es preparación; la estabilidad posterior sí compara sin actualizarlas. Axe cubre el catálogo y no constituye certificación integral de accesibilidad. GitHub y protección de rama no se ejecutaron desde este entorno.']
(ROOT/'documentacion/RESULTADOS.md').write_text('\n'.join(summary),encoding='utf-8')

pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold')
styles=getSampleStyleSheet()
for name,size,leading,after,color in [('Body',9,12,6,'#263544'),('TitleCustom',25,30,18,'#125678'),('HeadingCustom',17,22,14,'#125678'),('Case',11,15,6,'#125678')]:
    styles.add(ParagraphStyle(name=name,fontName='Arial' if name=='Body' else 'ArialBold',fontSize=size,leading=leading,spaceAfter=after,textColor=colors.HexColor(color)))
story=[]
def para(text,style='Body'):
    story.append(Paragraph(escape(text),styles[style]))
def block(r):
    para(f"{r['id']} | {r['titulo']}",'Case')
    for label,key in [('Mensaje','mensaje'),('Clasificación','clase'),('Causa y evidencia','causa'),('Corrección','correccion'),('Verificación','verificacion')]:
        story.append(Paragraph(f'<b>{label}.</b> {escape(r[key])}',styles['Body']))
    story.append(Spacer(1,5))

para('TIENDAUT / UNIDAD II','Case')
para('Práctica 1: pruebas con Playwright','TitleCustom')
para('Informe de ejecución y bitácora de defectos','HeadingCustom')
para('Gestión del Proceso de Desarrollo de Software. 15 de octubre de 2026. Zona horaria: America/Mexico_City.')
story.append(Spacer(1,16))
para('315 / 315 ejecuciones aprobadas','HeadingCustom')
para('21 casos de aceptación x 5 repeticiones x 3 navegadores. Cero fallos, pruebas inestables o saltos. ESLint sin errores.')
para('Alcance','Case')
para('Se resolvió la Práctica 1 del capítulo 19 con el ZIP suministrado: ocho demostraciones analizadas, defectos corregidos, tres pruebas requeridas y dos regresiones adicionales. Las prácticas 2 y 3 requieren proyectos del equipo y un sistema con cliente que no fueron proporcionados.')
para('Estado de entrega','Case')
para('Código, evidencias, bitácora, casos de prueba y workflow preparados. La publicación del repositorio y la comprobación de Actions permanecen pendientes: no hay cuenta, sesión de navegador o conector GitHub disponible. La validación local no sustituye la ejecución remota.')
para('Archivos de consulta','Case')
para('README.md reúne los comandos. documentacion/BITACORA.md contiene el detalle editable e INDICE-EVIDENCIAS.md enlaza trazas, capturas y videos. evidencias/estabilidad/resumen.json conserva el resultado verificable.')
story.append(PageBreak())
for start,end,title in [(0,4,'Laboratorio original / E1 a E4'),(4,8,'Laboratorio original / E5 a E8'),(8,11,'Consola, red y accesibilidad'),(11,15,'Carga, carrito y referencia visual')]:
    para(title,'HeadingCustom')
    for r in records[start:end]:block(r)
    story.append(PageBreak())
para('Hallazgos complementarios','HeadingCustom')
for r in records[15:18]:block(r)
story.append(PageBreak())
para('Análisis estático y estabilidad del entorno','HeadingCustom')
for r in records[18:]:block(r)
story.append(PageBreak())
para('Resultados y reproducción','HeadingCustom')
table=Table(rows,colWidths=[270,205],hAlign='LEFT')
table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'Arial'),('FONTNAME',(0,0),(-1,0),'ArialBold'),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#125678')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#EDF4F7'),colors.white]),('LEFTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story.append(table);story.append(Spacer(1,15))
para('Reproducción','Case')
para('Ejecutar npm ci, npx playwright install, npm run lint y npm run test:estabilidad. Abrir la evidencia con npx playwright show-report evidencias/estabilidad/reporte. Detener antes otros servidores en el puerto 3000.')
para('Referencias visuales y límites','Case')
para('Los tres PNG de inicio en Windows se revisaron y la estabilidad los compara sin actualizarlos. El workflow conserva la creación de referencias Linux ausentes del ZIP: su primer run no acredita comparación frente a una imagen Linux aprobada. Revisar e incorporar esas imágenes para exigir comparación estricta. Axe audita el catálogo.')
para('Método y fuentes','Case')
para('Leer mensaje, ubicar acción, reproducir, inspeccionar traza, clasificar, corregir y confirmar. Las trazas se analizaron programáticamente; los reportes HTML quedan disponibles para exploración. Fuentes: guía suministrada, capítulos 11, 12, 14, 15 y 19, Anexo B; código del ZIP; logs y trazas locales; documentación oficial playwright.dev/docs/test-snapshots y playwright.dev/docs/api/class-testconfig.')

out=ROOT/'output/pdf/informe-practica-playwright.pdf';out.parent.mkdir(parents=True,exist_ok=True)
def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#BBD0DC'));c.line(50,43,A4[0]-50,43)
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#617687'))
    c.drawString(50,30,'TiendaUT | Práctica 1 | Evidencias locales verificadas')
    c.drawRightString(A4[0]-50,30,str(doc.page))
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=43,bottomMargin=58,title='Práctica Playwright - TiendaUT',author='').build(story,onFirstPage=footer,onLaterPages=footer)
print(json.dumps({'pdf':str(out),'stats':stats,'por_navegador':dict(counts)},ensure_ascii=False,indent=2))
