"""Empaqueta código, documentos y evidencias sin dependencias instaladas."""
from pathlib import Path
import zipfile
import hashlib
import json

root = Path(__file__).resolve().parents[1]
out = root.parent/'entrega-practicas-1-y-2.zip'
excluded = {'.git', 'node_modules', '__pycache__', '.pytest_cache'}
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if rel.as_posix() == 'output/pdf/informe-practica-playwright.pdf':
            continue  # la nueva entrega contiene solo los dos informes principales
        if p.is_file() and not (set(rel.parts) & excluded):
            z.write(p, root.name+'/'+rel.as_posix())
    for name in ['Practica Playwright.pdf','tiendaut-playwright.zip']:
        original=root.parent/name
        if original.exists():
            z.write(original,'material-original/'+name)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert not any('/node_modules/' in n or '/.git/' in n for n in z.namelist())
    names=z.namelist()
    for name in ['package-lock.json','documentacion/BITACORA.md','output/pdf/practica-1-con-evidencias.pdf','output/pdf/practica-2-con-evidencias.pdf','evidencias/estabilidad-ampliada/resumen.json']:
        assert root.name+'/'+name in names, name
digest=hashlib.sha256(out.read_bytes()).hexdigest()
out.with_suffix('.sha256.txt').write_text(digest+'  '+out.name+'\n',encoding='utf-8')
print(json.dumps({'archivo':str(out),'archivos':len(names),'bytes':out.stat().st_size,'sha256':digest},indent=2))
