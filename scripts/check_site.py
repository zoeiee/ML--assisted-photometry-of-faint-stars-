from pathlib import Path
from html.parser import HTMLParser
import json,re
P=Path(__file__).resolve().parents[1];D=P/'public'
class Check(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.tags=set()
 def handle_starttag(self,t,a):
  self.tags.add(t);a=dict(a)
  if 'id' in a:self.ids.add(a['id'])
  for key in ['src','href']:
   if key in a:self.links.append(a[key])
h=Check();h.feed((D/'index.html').read_text())
for u in h.links:
 if u.startswith('#'):assert u[1:] in h.ids,u
 elif not u.startswith(('http:','https:','data:')):assert (D/u).is_file(),u
for t in ['d-title','d-article','d-byline','d-abstract','d-cite','d-footnote','d-math','d-bibliography']:assert t in h.tags,t
js=(D/'vendor/template.v2.js').read_text();original=(D/'vendor/template.v2.original.js').read_text();assert js==original.replace('https://distill.pub/third-party/katex/','vendor/katex/')
for font in re.findall(r'url\(([^)]+)\)',(D/'vendor/katex/katex.min.css').read_text()):assert (D/'vendor/katex'/font).exists()
assert 'Python' not in json.dumps(json.loads((P/'vercel.json').read_text()))
print('PASS: article local assets, anchors, native Distill tags, vendored framework patch, math font paths, Vercel JSON')
print('NOT RUN: browser rendering, console, responsive screenshots, interactive event QA, Vercel-host deployment')
