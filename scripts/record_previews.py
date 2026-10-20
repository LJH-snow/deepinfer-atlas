#!/usr/bin/env python3
"""Record preview provenance after UI export and bind HTML image aspect ratios."""
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT=Path(__file__).resolve().parents[1]
report=json.loads((ROOT/'output/exports.json').read_text())
assert report['ok'], 'Export report is not successful'
records=[]
for slug in ['architecture','request','scope']:
    artifact=ROOT/f'site/diagrams/{slug}.html';artifact_hash=hashlib.sha256(artifact.read_bytes()).hexdigest()
    expected=[r for r in report['records'] if r['diagram']==slug]
    assert all(r['artifactSha']==artifact_hash for r in expected), f'{slug}: stale export source'
    files={}
    for extension in ['png','svg']:
        path=ROOT/f'site/assets/{slug}.{extension}'
        files[extension]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    width,height=struct.unpack('>II',(ROOT/files['png']['path']).read_bytes()[16:24]);files['png'].update(width=width,height=height)
    for page in (ROOT/'content').glob('*.html'):
        s=page.read_text();pattern=rf'(<img src="assets/{slug}\.png"[^>]*?width=")\d+(" height=")\d+("[^>]*>)'
        s=re.sub(pattern,lambda m:m[1]+str(width)+m[2]+str(height)+m[3],s);page.write_text(s)
    records.append({'diagram':slug,'artifact_sha256':artifact_hash,'files':files,'method':'Archify viewer export menu, light theme, reset view'})
(ROOT/'data/previews.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('Bound 3 PNG/SVG preview pairs to the final HTML artifacts and exact image ratios.')
