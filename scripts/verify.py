#!/usr/bin/env python3
"""Verify links, evidence excerpts, diagram mappings and frozen artifact receipts."""
from __future__ import annotations
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import struct
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--require-upstream',action='store_true');args=parser.parse_args()
base=json.loads((ROOT/'data/upstream.json').read_text());rows=json.loads((ROOT/'data/evidence.json').read_text());errors=[];counts={}
def check(condition,message):
    if not condition:errors.append(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
class Document(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.refs=[];self.images=[];self.h1=0;self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if tag=='img':self.images.append(a)
files=[p for p in (ROOT/'site').rglob('*.html') if '.visual-check.' not in p.name]
documents={}
for path in files:
    doc=Document();doc.feed(path.read_text());documents[path.resolve()]=doc
    check(doc.lang=='zh-CN',f'{path.relative_to(ROOT)}: incorrect language')
    check(doc.h1==1,f'{path.relative_to(ROOT)}: expected one h1, got {doc.h1}')
local_count=0;source_urls=set()
for path,doc in documents.items():
    for ref in doc.refs:
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc:
            if parts.hostname=='github.com' and '/deepseek-ai/DeepInfer/' in parts.path and ('/blob/' in parts.path or '/tree/' in parts.path):
                check(base['commit'] in parts.path,f'Unpinned source: {ref}');source_urls.add(ref)
            continue
        if not parts.path and not parts.fragment:continue
        target=(path.parent/unquote(parts.path)).resolve() if parts.path else path
        if target.is_dir():target=target/'index.html'
        check(target.is_relative_to(ROOT/'site'),f'Local link escapes site: {path.name}: {ref}')
        check(target.exists(),f'Broken local link: {path.relative_to(ROOT)}: {ref}')
        if parts.fragment and target in documents:check(unquote(parts.fragment) in documents[target].ids,f'Missing anchor: {path.name}: {ref}')
        local_count+=1
    for image in doc.images:
        check('alt' in image,f'{path.name}: missing image alt')
        check('width' in image and 'height' in image,f'{path.name}: image dimensions missing')
        image_path=(path.parent/image['src']).resolve()
        if image_path.exists() and image_path.suffix=='.png':
            raw=image_path.read_bytes();width,height=struct.unpack('>II',raw[16:24]);declared=int(image['width'])/int(image['height'])
            check(abs(width/height-declared)<.006,f'{path.name}: incorrect image aspect ratio: {image["src"]}')
counts.update(html_documents=len(files),local_references=local_count,pinned_source_urls=len(source_urls))
ids={r['id'] for r in rows};check(len(ids)==len(rows),'Duplicate evidence IDs');check(len(rows)==base['evidence_count'],'Evidence count mismatch')
up=ROOT/'.upstream/DeepInfer'
if up.exists():
    sha=subprocess.check_output(['git','-C',str(up),'rev-parse','HEAD'],text=True).strip();check(sha==base['commit'],'Upstream HEAD mismatch')
    for r in rows:
        path=up/r['path'];check(path.is_file(),f'{r["id"]}: missing source')
        if not path.is_file():continue
        lines=path.read_text().splitlines();excerpt='\n'.join(lines[r['start']-1:r['end']])
        check(r['end']<=len(lines),f'{r["id"]}: out of bounds')
        check(r['anchor'] in lines[r['start']-1],f'{r["id"]}: anchor moved')
        check(all(c in excerpt for c in r['checks']),f'{r["id"]}: expected symbol/call absent')
        check(digest(path)==r['file_sha256'],f'{r["id"]}: source file changed')
        check(hashlib.sha256(excerpt.encode()).hexdigest()==r['excerpt_sha256'],f'{r["id"]}: excerpt changed')
        expected=f'https://github.com/deepseek-ai/DeepInfer/blob/{base["commit"]}/{r["path"]}#L{r["start"]}-L{r["end"]}'
        check(r['url']==expected,f'{r["id"]}: source URL mismatch')
    counts['verified_source_excerpts']=len(rows)
else:
    counts['verified_source_excerpts']=0
    if args.require_upstream:errors.append('Pinned upstream missing; run scripts/fetch_upstream.py')
    else:print('Source excerpt verification skipped: run scripts/fetch_upstream.py and verify.py --require-upstream.')
maps=json.loads((ROOT/'data/diagram-map.json').read_text());viewports={(1440,900),(1600,1000),(1920,1080),(2048,1320)}
for name,mapping in maps.items():
    spec_path=ROOT/f'diagrams/specs/{name}.json';spec=json.loads(spec_path.read_text());artifact=ROOT/f'site/diagrams/{name}.html'
    nodes=spec.get('components',spec.get('participants',[]));relationships=spec.get('connections',spec.get('messages',[]))
    check({n['id'] for n in nodes}==set(mapping['nodes']),f'{name}: node evidence map mismatch')
    check({e['id'] for e in relationships}==set(mapping['relationships']),f'{name}: relationship evidence map mismatch')
    for key in ['nodes','relationships']:
        for name_id,evidence_ids in mapping[key].items():check(bool(evidence_ids) and set(evidence_ids)<=ids,f'{name}/{name_id}: unknown evidence')
    validation=json.loads((ROOT/f'diagrams/receipts/{name}.validate.json').read_text());receipt=json.loads((ROOT/f'diagrams/receipts/{name}.deliver.json').read_text())
    check(validation.get('ok'),f'{name}: validation failed')
    checker=validation.get('checker',validation);check(len(checker.get('checks',[]))==9 and all(c['ok'] for c in checker.get('checks',[])),f'{name}: not 9/9 showcase')
    check(checker.get('composition',{}).get('summary')=={'errors':0,'warnings':0},f'{name}: composition diagnostics remain')
    check(receipt.get('ok'),f'{name}: delivery failed')
    check(receipt.get('specification',{}).get('sha256')==digest(spec_path),f'{name}: frozen spec mismatch')
    check(receipt.get('artifact',{}).get('sha256')==digest(artifact),f'{name}: artifact mismatch')
    visual=json.loads((ROOT/f'site/diagrams/{name}.visual-check.json').read_text());check(visual.get('ok'),f'{name}: desktop visual containment failed')
    check(visual.get('artifact',{}).get('sha256')==digest(artifact),f'{name}: stale visual evidence')
    check(viewports <= {(v['width'],v['height']) for v in visual['containment']['viewports']},f'{name}: missing desktop viewport')
    check(all(v['ok'] and v['readabilityOk'] for v in visual['containment']['viewports']),f'{name}: visual measurement failure')
# Check README/document entry points as files, including preview and release material.
markdown_references=0
for path in [ROOT/'README.md', ROOT/'README.en.md', *(ROOT/'docs').glob('*.md')]:
    import re
    for ref in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',path.read_text()):
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc or not parts.path:continue
        target=(path.parent/unquote(parts.path)).resolve()
        check(target.exists(),f'{path.relative_to(ROOT)}: broken Markdown link {ref}')
        markdown_references+=1
for preview in json.loads((ROOT/'data/previews.json').read_text()):
    check(digest(ROOT/f'site/diagrams/{preview["diagram"]}.html')==preview['artifact_sha256'],f'{preview["diagram"]}: stale preview source')
    for info in preview['files'].values():check(digest(ROOT/info['path'])==info['sha256'],f'{info["path"]}: changed preview bytes')
counts['markdown_references']=markdown_references

counts.update(evidence_records=len(rows),diagram_node_mappings=sum(len(m['nodes']) for m in maps.values()),diagram_relationship_mappings=sum(len(m['relationships']) for m in maps.values()))
result={'ok':not errors,'counts':counts,'errors':errors}
report=ROOT/'output/static-verification.json';report.parent.mkdir(exist_ok=True);report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if not errors else 1)
