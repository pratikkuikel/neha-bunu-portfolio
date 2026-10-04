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
content=''.join(('<h2>'+html.escape(i['text'])+'</h2>') if i['heading'] else '<p>'+html.escape(i['text'])+'</p>' for i in items)
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>The Sky She Left Me — Complete text edition</title><link rel="stylesheet" href="/styles.css"><style>body{padding:30px 20px;background:#f8f5ed}main{max-width:700px;margin:auto;font:20px/1.7 Literary,serif}h1{font-size:60px;letter-spacing:-2px}h2{font-size:38px;margin-top:60px}a{text-decoration:underline}p{margin-bottom:18px}</style></head><body><main><a href="/">Neha Kharel · Back to the author website</a><h1>The Sky She Left Me</h1><p>Neha Kharel · Complete text edition</p>'''+content+'</main></body></html>'
Path('dist/book.html').write_text(page)
print(json.dumps({'paragraphs':len(items),'words':sum(len(p['text'].split()) for p in items)}))
