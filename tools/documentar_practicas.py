"""Dos informes con capturas reales y resultados enlazados a Playwright."""
from pathlib import Path
from collections import Counter
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[1]
IM=ROOT/'evidencias/capturas/imagenes'
OUT=ROOT/'output/pdf'
stats=json.loads((ROOT/'evidencias/estabilidad-ampliada/resumen.json').read_text(encoding='utf-8'))['stats']
captures=json.loads((ROOT/'evidencias/capturas/resumen.json').read_text(encoding='utf-8'))
assert stats['expected']==345 and not (stats['unexpected'] or stats['flaky'] or stats['skipped'])
assert captures['stats']['expected']==8 and captures['stats']['unexpected']==0
scope_file=ROOT/'documentacion/alcance-miniproyecto.json'
scope=json.loads(scope_file.read_text(encoding='utf-8')) if scope_file.exists() else {'confirmado':False,'proyecto':'TiendaUT'}
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold')
styles=getSampleStyleSheet()
for name,size,leading,color in [('Body',9.5,13,'#243746'),('Small',8,10.5,'#526879'),('Caption',8.4,11,'#526879'),('H',19,24,'#125678'),('Sub',12,16,'#125678'),('Cover',27,33,'#125678')]:
 styles.add(ParagraphStyle(name=name,fontName='ArialBold' if name in ('H','Sub','Cover') else 'Arial',fontSize=size,leading=leading,textColor=colors.HexColor(color),spaceAfter=8))
styles.add(ParagraphStyle(name='CodeCustom',fontName='Courier',fontSize=7.5,leading=10,backColor=colors.HexColor('#F0F5F8'),borderPadding=7,spaceAfter=10))
story=[]
def p(text,style='Body'):story.append(Paragraph(escape(text),styles[style]))
def title(text):p(text,'H')
def sub(text):p(text,'Sub')
def page():story.append(PageBreak())
class Captura(Flowable):
 def __init__(self,file,width,region):
  super().__init__();self.file=file;self.region=region;self.width=width;self.height=width*region[3]/region[2]
 def draw(self):
  with PILImage.open(self.file) as im:sw,sh=im.size
  x,y,w,h=self.region;scale=self.width/w
  c=self.canv;c.saveState();clip=c.beginPath();clip.rect(0,0,self.width,self.height);c.clipPath(clip,stroke=0)
  c.drawImage(str(self.file),-x*scale,-(sh-y-h)*scale,width=sw*scale,height=sh*scale)
  c.restoreState()

def img(filename,caption,width=475):
 file=IM/filename if not isinstance(filename,Path) else filename
 with PILImage.open(file) as im:w,h=im.size
 regions={
  '08-laboratorio-original.png':(220,0,1010,650),
  '09-suite-original.png':(220,0,1010,900),
  '17-estabilidad-345.png':(220,0,1010,580),
  '18-github-linux.png':(220,0,1010,550),
  '02-carrito-vacio.png':(0,0,600,550),
  '03-filtro-corregido.png':(0,0,600,300),
  '04-login-vacio.png':(0,0,600,h),
  '05-api-productos.png':(0,0,420,390),
  '06-error-api-controlado.png':(0,0,600,230),
  '12-inicio-flujo.png':(0,0,600,180),
  '13-login-flujo.png':(0,0,600,h),
  '14-catalogo-flujo.png':(0,0,600,550),
  '15-carrito-dos-productos.png':(0,0,600,300),
  '16-carrito-flujo-final.png':(0,0,600,300),
 }
 region=regions.get(file.name,(0,0,w,h))
 if file.name=='test-failed-1.png':region=(0,0,600,550)
 story.append(Captura(file,width,region))
 p(caption,'Caption')
def table(rows,widths):
 data=[[Paragraph(escape(str(x)),styles['Small']) for x in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDECF2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7F9')]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,8))
def code(text):story.append(Preformatted(text,styles['CodeCustom']))
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#BBD0DC'));c.line(50,43,A4[0]-50,43)
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#526879'))
 c.drawString(50,29,'GPDS - Unidad II | TiendaUT | Capturas de ejecuciones reales')
 c.drawRightString(A4[0]-50,29,str(doc.page))
def build(name):
 OUT.mkdir(parents=True,exist_ok=True)
 SimpleDocTemplate(str(OUT/name),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=57,title=name,author='').build(story,onFirstPage=footer,onLaterPages=footer)


def evidencia_github():
 page();title('GitHub: ejecución y artefacto verificados')
 img('19-github-actions.jpg','Captura real de la página pública de GitHub Actions: estado Success y un artefacto publicado. El reporte de Playwright descargado y la segunda ejecución estricta también están incluidos en las evidencias.',360)
 sub('Ejecución del 21 de octubre de 2026')
 table([['Comprobación remota','Resultado'],['Instalación y ESLint','Correctos'],['Chromium / Firefox / WebKit','115 / 115 en cada navegador'],['Total / fallos / flaky / saltos','345 / 0 / 0 / 0'],['Artefacto playwright-report','Publicado y descargado; JSON y logs comprobados']],[220,255])
 p('Repositorio: https://github.com/Eileeno56/tiendaut-playwright','Small')
 p('Ejecución: https://github.com/Eileeno56/tiendaut-playwright/actions/runs/39695106242','Small')
 p('La verificación y los adjuntos están en evidencias/github/. El repositorio es público y el docente puede abrirlo sin invitación. Main exige el check test. La segunda ejecución también pasó 345/345 sin actualizar referencias: actions/runs/39696522338. El bloqueo inicial del plan privado queda registrado como antecedente, no como estado actual.','Small')

p('GESTIÓN DEL PROCESO DE DESARROLLO DE SOFTWARE','Sub')
p('Práctica 1','Cover');title('Cazadores de defectos en TiendaUT')
p('Desarrollo, análisis, corrección y evidencia visual. Pruebas locales: 15 de octubre de 2026. Verificación en GitHub: 21 de octubre de 2026. Fuente de requisitos: guía suministrada, capítulo 19, página 53 y Anexo B.')
sub('Objetivo y materiales')
p('Analizar el sitio del ZIP con Playwright, clasificar los fallos, corregir su causa y comprobar estabilidad. Entorno: Windows, Node 24.18.0, Playwright 1.64.1 y axe 4.14.0. Se instalaron dependencias y Chromium, Firefox y WebKit.')
table([['Requisito','Cumplimiento comprobado'],['1. Descomprimir e instalar / publicar','Realizado y publicado en Eileeno56/tiendaut-playwright.'],['2. E1-E8 y bitácora','Ocho fallos originales conservados y clasificados.'],['3. Suite Chromium y seis pasos','12 pruebas aprobadas y 7 fallidas antes de corregir.'],['4. Corregir el sitio','Carrito, filtro tardío, recursos, accesibilidad y API corregidos.'],['5. Tres pruebas nuevas','Vaciado, login vacío y contrato de todos los productos.'],['6. Cinco repeticiones / tres navegadores','315/315 en la entrega inicial; 345/345 en la suite ampliada.'],['7. Actions y artefacto remoto','GitHub Actions en verde; artefacto publicado y descargado.']],[180,295])
p('Este informe documenta la primera de las dos prácticas solicitadas por el estudiante. Para legibilidad, las figuras muestran detalles de capturas reales; los PNG completos se entregan con los reportes HTML, logs, JSON y trazas. Las evidencias locales no se presentan como una ejecución de GitHub.','Small')
page();title('1. Laboratorio: ocho fallos reproducidos')
img('08-laboratorio-original.png','Figura 1. Reporte HTML real del laboratorio original: 8 ejecutadas, 8 fallidas. Los fallos son intencionales; View Trace conserva su evidencia.',450)
table([['ID','Mensaje clave / clasificación','Propuesta de corrección'],['E1','Timeout: Comprar ahora / prueba','Usar el botón real del producto.'],['E2','Strict mode: 4 botones / prueba','Acotar por nombre de producto.'],['E3','Bienvenidos vs. Bienvenido / prueba','Ajustar al encabezado del requisito.'],['E4','URL sigue en login / prueba','Contraseña inválida: esperar alerta, no redirección.'],['E5','Connection refused:3999 / entorno','Usar baseURL y servidor en 3000.'],['E6','reiniciarContador no existe / sitio','Actualizar el contador al vaciar.'],['E7','Test ended y await ausente / prueba','Esperar la aserción y elegir el encabezado real.'],['E8','getByLabel sin label / prueba y sitio','Añadir una etiqueta accesible al buscador.']],[30,213,232])
p('La bitácora extensa y el enlace a cada captura, video y trace.zip están en documentacion/BITACORA.md e INDICE-EVIDENCIAS.md. Los ocho ejemplos se conservan separados de la suite de aceptación.','Small')
page();title('2. Análisis de los fallos del sitio')
img('09-suite-original.png','Figura 2. Ejecución original aislada de Chromium, incluidas las tres pruebas nuevas: 12 aprobadas y 7 fallidas.',450)
sub('Método de seis pasos aplicado')
p('1) Leer Expected/Received y el mensaje. 2) Ubicar la acción o aserción. 3) Reproducir con el sitio original. 4) Inspeccionar acciones, DOM y red de la traza. 5) Clasificar como sitio, prueba o entorno. 6) Corregir y volver a comprobar. Las trazas se inspeccionaron programáticamente; se entregan para abrirlas con Trace Viewer.')
sub('Causas corregidas')
p('El filtro escrito antes de la API se descartaba; Vaciar carrito llamaba una función inexistente; faltaban logo y favicon; la imagen carecía de alt y el contenido de landmarks; el buscador carecía de etiqueta; un error de API no producía aviso. No se cambiaron las expectativas funcionales originales para ocultar estos defectos.')
p('La falta inicial de una imagen de referencia visual se clasificó como preparación del entorno, no como defecto funcional. También se conservó un intento interferido por el cierre del servidor y dos esperas vencidas en Firefox.','Small')
page();title('3. Carrito: evidencia antes y después')
original=ROOT/'evidencias/suite-original/resultados/practica-Vaciar-carrito-de-cdc44-0-sin-errores-de-JavaScript-chromium/test-failed-1.png'
img(original,'Figura 3. Antes de corregir: después de pulsar Vaciar carrito, el contador permanece en 1. La prueba esperaba 0.',330)
img('02-carrito-vacio.png','Figura 4. Después de corregir: se agregó un producto, se comprobó 1 y se vació. El contador termina en 0; la prueba también exige cero pageerror.',330)
p('Causa: reiniciarContador no existía. Corrección: carrito = 0 y contador.textContent = String(carrito). Evidencia: practica.spec.ts, prueba de vaciado; nueva captura reproducida con aserciones en evidencias/capturas/documentacion.spec.ts.','Small')
page();title('4. Buscador: condición de carrera corregida')
original=ROOT/'evidencias/suite-original/resultados/carrito-Carrito-de-compras-el-buscador-filtra-los-productos-chromium/test-failed-1.png'
img(original,'Figura 5. Antes: el buscador contiene monitor, pero aparecen los cuatro productos; la prueba esperaba uno.',400)
img('03-filtro-corregido.png','Figura 6. Después: se escribe monitor antes de liberar la respuesta de API y aparece solo Monitor 24 pulgadas.',400)
p('La traza original registra la escritura antes de terminar la API. Ahora se vuelve a pintar con el valor actual del buscador al recibir los datos. La regresión retiene la petición mediante una promesa y la libera después de escribir; no usa esperas fijas.','Small')
page();title('5. Las tres pruebas obligatorias añadidas')
sub('CP-17: vaciar el carrito sin errores JavaScript')
p('Precondición: carrito con un teclado. Acción: Vaciar carrito. Esperado: contador 0 y lista de pageerror vacía. Su resultado visual está en la figura 4.')
sub('CP-18: iniciar sesión con campos vacíos')
img('04-login-vacio.png','Figura 7. Usuario y contraseña vacíos: aparece Usuario o contraseña incorrectos; la URL sigue siendo login.html.',425)
sub('CP-19: contrato de todos los productos de API')
img('05-api-productos.png','Figura 8. Respuesta real de /api/productos. La prueba recorre todos los productos y exige nombre no vacío y precio numérico finito mayor que cero.',400)
p('Implementación: tests/practica.spec.ts. Los datos y los resultados comprobados se conservan en el JSON de Playwright; no se infiere el éxito solamente de estas imágenes.','Small')
page();title('6. Estabilidad y resultado comprobado')
img('17-estabilidad-345.png','Figura 9. Reporte real de la suite ampliada: 345 aprobadas, cero fallidas, flaky o saltadas. No se actualizaron las imágenes de referencia durante esta comprobación.',475)
table([['Navegador','Casos x repeticiones','Resultado'],['Chromium','23 x 5','115/115'],['Firefox','23 x 5','115/115'],['WebKit','23 x 5','115/115'],['Total','23 x 5 x 3','345/345']],[150,175,150])
p('La entrega inicial validó 21 casos (315 ejecuciones); se añadieron dos recorridos completos y se repitió la suite total. No se reemplazó la evidencia histórica. La configuración usa dos workers, 20 segundos para aserciones y 60 por prueba; el margen se justificó tras dos fallos de espera en Firefox y no equivale a una mejora de rendimiento del sitio.')
code('npm ci\nnpx playwright install\nnpm run lint\nnpx playwright test --repeat-each=5 --fail-on-flaky-tests')
page();title('7. Red, calidad e integración continua')
img('06-error-api-controlado.png','Figura 10. Un 500 de la API se simula con page.route. El sitio informa No pudimos cargar los productos en una alerta; ya no queda sin explicación.',425)
sub('Calidad comprobada')
p('La captura del catálogo auditado y el adjunto calidad.json acreditan consola sin errores, ninguna respuesta de red >=400 en el camino normal y cero violaciones axe en el catálogo. El caso 500 se valida por separado porque su error de red es intencional.')
sub('GitHub Actions: verificado en verde')
p('El 21 de octubre se publicó el repositorio Eileeno56/tiendaut-playwright y se ejecutó el workflow en Ubuntu. Instalación, ESLint, 345 pruebas y publicación de artefactos terminaron correctamente. Se descargó playwright-report y se comprobaron sus resultados, logs y referencias visuales Linux.')
p('La primera ejecución Linux creó las referencias ausentes; se revisaron y se incorporaron al código. El workflow ahora exige comparar sin regenerarlas. Con autorización del estudiante, el repositorio se hizo público y se activó la protección de main, que exige el check test. Se fija Ubuntu 24.04 para mantener estable el entorno de las capturas. Ver la evidencia remota en la página siguiente.','Small')
evidencia_github()
build('practica-1-con-evidencias.pdf')

story=[]
p('GESTIÓN DEL PROCESO DE DESARROLLO DE SOFTWARE','Sub')
p('Práctica 2','Cover');title('Mini-proyecto: automatización de TiendaUT')
if scope['confirmado']:
 p('Proyecto seleccionado por el estudiante: TiendaUT. Se aplica el trabajo al proyecto disponible del ZIP, usando sus funcionalidades reales de acceso y catálogo.')
elif scope.get('asumido_por_zip'):
 p('La segunda práctica se aplica a TiendaUT, el proyecto disponible en el ZIP, siguiendo la indicación de trabajar con ese archivo. Es una adaptación del mini-proyecto: si el profesor exige el sistema propio del equipo, deberá aplicarse a ese sistema.')
else:
 p('Aplicación de referencia al único proyecto recibido: TiendaUT. Falta confirmar que este es el mini-proyecto del equipo. Si el equipo usa otro sistema, este informe y las pruebas deben aplicarse a ese sistema antes de declarar cumplido ese requisito.')
p('Objetivo: cubrir recorridos críticos, casos negativos, API, análisis de calidad y configuración de CI. Requisitos: capítulo 19, página 53 de la guía. Fecha: 15 de octubre de 2026.')
table([['Requisito','Implementación y evidencia'],['Ocho E2E y dos recorridos completos','Matriz de casos de la página siguiente; FC-01 y FC-02.'],['Dos negativos y una API','Contraseña incorrecta, campos vacíos, API 500 y contrato de productos.'],['Page Object y preparación común','LoginPage y CatalogoPage; beforeEach y fixture loginPage.'],['Consola, red y axe','Tres auditorías originales y adjunto calidad.json.'],['baseURL, webServer y trace','playwright.config.ts; trace retain-on-failure.'],['Pipeline y reporte','GitHub Actions en verde y reporte publicado como artefacto.'],['Bitácora completa','BITACORA.md, INDICE-EVIDENCIAS.md y trazas históricas.']],[175,300])
p('Los dos recorridos completos fueron añadidos expresamente. Se verificó toda la suite ampliada: 345/345 en tres navegadores. Las ocho pruebas documentales aparte capturan los estados después de verificarlos; no aumentan artificialmente el recuento de aceptación.','Small')
page();title('1. Diseño y trazabilidad de casos')
table([['ID / tipo','Pasos y resultado esperado','Archivo'],['E2E-01 / crítico','Inicio > login válido > catálogo con cuatro productos y contador 0.','flujos-completos.spec.ts / FC-01'],['E2E-02 / crítico','Inicio > catálogo > buscar monitor y agregar > buscar mouse y agregar > contador 2 > vaciar y verificar 0.','flujos-completos.spec.ts / FC-02'],['E2E-03 / negativo','Contraseña equivocada: alerta y permanencia en login.','login.spec.ts'],['E2E-04 / negativo','Campos vacíos: alerta y permanencia en login.','practica.spec.ts'],['E2E-05 / funcional','Filtrar monitor y comprobar exactamente un resultado.','carrito.spec.ts'],['E2E-06 / negativo','API 500: presentar aviso al usuario.','red-y-visual.spec.ts'],['E2E-07 / negativo','Red interrumpida: aviso y cero excepciones JavaScript.','regresiones.spec.ts'],['E2E-08 / funcional','Inicio: título TiendaUT y encabezado correcto.','inicio.spec.ts'],['API-01 / API','GET exitoso: cada producto tiene nombre y precio válido mayor que 0.','practica.spec.ts']],[90,270,115])
sub('Aislamiento y criterios')
p('Cada prueba recibe un contexto nuevo. Los recorridos completos preparan el inicio con beforeEach; el fixture loginPage y los Page Objects encapsulan la pantalla. Se usan getByRole, getByLabel y testid acordados; las aserciones reintentan, sin waitForTimeout. Los datos de acceso son únicamente los de la tienda didáctica.')
p('TiendaUT no implementa pago ni confirmación de pedido. Por ello se verifica acceso y gestión del carrito, sin inventar un checkout inexistente.','Small')
page();title('2. FC-01: acceso y catálogo cargado')
img('12-inicio-flujo.png','Figura 1a. Estado inicial del recorrido: la página de inicio ofrece el enlace Iniciar sesión.',450)
img('13-login-flujo.png','Figura 1. El recorrido comienza en Inicio, abre Iniciar sesión y completa alumno / contraseña de demostración.',450)
img('14-catalogo-flujo.png','Figura 2. Después de Entrar se verifica catalogo.html, encabezado Catálogo, cuatro productos y contador inicial 0.',350)
p('Resultado esperado y obtenido: navegación válida y catálogo cargado. Implementación: LoginPage y CatalogoPage, test FC-01. El resultado se verifica en Chromium, Firefox y WebKit durante cinco repeticiones por navegador.','Small')
page();title('3. FC-02: búsqueda y gestión del carrito')
img('15-carrito-dos-productos.png','Figura 3. Tras buscar monitor, agregarlo, buscar mouse y agregarlo, el contador muestra 2.',450)
img('16-carrito-flujo-final.png','Figura 4. Se pulsa Vaciar carrito y se verifica contador 0. El flujo de aceptación también exige ausencia de pageerror.',450)
p('Inicio > Catálogo > monitor > agregar > mouse > agregar > contador 2 > vaciar > contador 0. CatalogoPage concentra buscador, productos, contador y acciones. El flujo prepara y verifica su propio estado; no depende de otra prueba.','Small')
page();title('4. Casos negativos con resultado visible')
img('04-login-vacio.png','Figura 5. Formulario vacío: el sitio presenta la alerta de error y permanece en login. El caso con contraseña equivocada se verifica igualmente.',450)
img('06-error-api-controlado.png','Figura 6. Respuesta 500 controlada: aparece una alerta de carga fallida. También existe una prueba que aborta la petición de red.',450)
p('Las capturas muestran estados del navegador. La comprobación de URL, texto y errores se hace con aserciones dentro de Playwright y queda registrada en los reportes, no solamente a partir de la apariencia de la pantalla.','Small')
page();title('5. API y análisis de calidad')
img('05-api-productos.png','Figura 7. JSON real de la API. Cada producto se valida por nombre y precio; la captura no sustituye las comprobaciones del contrato.',340)
sub('Resultado de la auditoría automatizada')
attachments=[]
def collect(s):
 for spec in s.get('specs',[]):
  for test in spec['tests']:
   for run in test['results']:attachments.extend(run.get('attachments',[]))
 for child in s.get('suites',[]):collect(child)
for s in captures['suites']:collect(s)
quality=next(a for a in attachments if a['name']=='calidad.json')
if quality.get('path'):q=json.loads(Path(quality['path']).read_text(encoding='utf-8'))
else:
 import base64
 q=json.loads(base64.b64decode(quality['body']))
assert q['consola']==[] and q['red']==[] and q['violaciones']==[]
code(json.dumps(q,ensure_ascii=False,indent=2))
p('El JSON anterior proviene del adjunto real de la prueba documental. Axe analiza el catálogo con los productos cargados. Cero violaciones detectadas no equivale a certificación completa de accesibilidad ni a una revisión de todas las pantallas.')
sub('Trazabilidad de defectos')
p('Se mantiene la bitácora de todos los fallos del desarrollo: E1-E8, consola/red, accesibilidad, carrera del buscador, vaciado, error de API, referencia visual inicial y problemas de entorno. Cada entrada explica evidencia, clasificación, causa, corrección y verificación; la documentación principal se divide únicamente en estas dos prácticas.')
page();title('6. Ejecución, evidencia y pipeline')
img('17-estabilidad-345.png','Figura 8. Resultado real común a las dos prácticas: 23 casos x 5 repeticiones x 3 navegadores = 345 aprobados.',475)
p('Chromium 115/115; Firefox 115/115; WebKit 115/115. Cero fallos, flaky o saltos. ESLint sin errores. Resultado fuente: evidencias/estabilidad-ampliada/resumen.json. Evidencia documental: ocho pruebas separadas, con trazas y PNG.')
sub('Reproducir y consultar')
code('npm ci\nnpx playwright install\nnpm run lint\nnpm run test:estabilidad\nnpx playwright test --config=playwright.evidencias.config.ts')
sub('Integración continua comprobada')
p('El repositorio ya está publicado y GitHub Actions terminó en verde con npm ci, lint y 345 pruebas. Se publicó y descargó el artefacto playwright-report. La captura de la página siguiente muestra GitHub Actions con estado Success. El repositorio es público y main exige el check test para integrar cambios.')
if not scope['confirmado'] and not scope.get('asumido_por_zip'):p('También falta confirmar que TiendaUT corresponde al mini-proyecto del equipo. El código y las capturas prueban trabajo real sobre esta aplicación; no prueban que se haya trabajado en un proyecto distinto que no se proporcionó.','Small')
evidencia_github()
build('practica-2-con-evidencias.pdf')
print('Dos informes creados con capturas reales; requisitos externos identificados.')
