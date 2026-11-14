"""Extract body paragraphs and modern Word text boxes, without duplicate fallbacks.
Usage: python scripts/extract-manuscript.py /path/to/manuscript.docx
The original manuscript's wording and chapter labels remain unchanged.
"""
from docx import Document
from pathlib import Path
import sys,json,re,html
x=Document(sys.argv[1]);items=[]
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','mc':'http://schemas.openxmlformats.org/markup-compatibility/2006'}
def add(text,index):
 text=re.sub(r'\s+',' ',text).strip()
 if not text:return
 heading=text in ['Acknowledgement','Epilogue','AUTHOR NOTE'] or bool(re.fullmatch(r'Chapter \d+',text))
 items.append({'text':text,'heading':heading,'sourceParagraph':index})
for i,p in enumerate(x.paragraphs):
 if i<16:continue
 add(p.text,i)
 for box in p._p.xpath('.//w:txbxContent'):
  if any(a.tag=='{'+ns['mc']+'}Fallback' for a in box.iterancestors()):continue
  for b in box.findall('w:p',ns):add(''.join(b.xpath('.//w:t/text()')),i)
Path('dist/manuscript.json').write_text(json.dumps(items,ensure_ascii=False))
import subprocess;subprocess.run([sys.executable,str(Path(__file__).with_name('render-book.py'))],check=True)
print(json.dumps({'paragraphs':len(items),'words':sum(len(p['text'].split()) for p in items)}))
