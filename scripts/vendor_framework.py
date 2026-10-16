"""Vendor official Distill distribution and its math assets; retain provenance."""
import urllib.request,hashlib,json,re,concurrent.futures
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'website/vendor';P.mkdir(exist_ok=True)
def get(url,path):
    data=urllib.request.urlopen(url,timeout=45).read();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);return {'url':url,'sha256':hashlib.sha256(data).hexdigest(),'file':str(path.name)}
records=[]
for url,name in [('https://distill.pub/template.v2.js','template.v2.original.js'),('https://distill.pub/third-party/katex/katex.min.js','katex/katex.min.js'),('https://distill.pub/third-party/katex/katex.min.css','katex/katex.min.css'),('https://raw.githubusercontent.com/distillpub/template/bf862cc4fe8abd56a94759453801fd04529fad9b/LICENSE','LICENSE')]:
    records.append(get(url,P/name))
css=(P/'katex/katex.min.css').read_text();fonts=set(re.findall(r'url\(([^)]+)\)',css))
def font(f):return get('https://distill.pub/third-party/katex/'+f,P/'katex'/f)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:records+=list(ex.map(font,fonts))
original=(P/'template.v2.original.js').read_text();(P/'template.v2.js').write_text(original.replace('https://distill.pub/third-party/katex/','vendor/katex/'))
(P/'provenance.json').write_text(json.dumps({'distribution':'Official template.v2.js; not asserted to equal the referenced source commit','retrieved':'2026-10-16','modifications':'Only KaTeX asset URLs changed to local relative paths','assets':records},indent=2))
print('Vendored',len(records),'assets')
