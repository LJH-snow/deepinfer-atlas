#!/usr/bin/env python3
"""Generate readable HTML with only the Python standard library; also stage dist/."""
from __future__ import annotations
import html
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / 'data/upstream.json').read_text())
EVIDENCE = {row['id']: row for row in json.loads((ROOT / 'data/evidence.json').read_text())}
PAGES = [
    ('index', '首页', 'DeepInfer 非官方可视化源码导读，约 10 分钟建立从入口到设备执行的源码地图。', '00'),
    ('architecture', '架构总览', '从 LLM.generate 到调度、模型执行与设备缓存，理解 DeepInfer 模块如何协作。', '01'),
    ('request', '请求时序', '跟随一次真实离线请求，理解批次、prefill、decode、采样和输出的循环。', '02'),
    ('scope', '开源边界', '区分已发布的引擎、待集成的能力和官方完整生产系统中的服务。', '03'),
    ('performance', '性能优化', '定位 CPU 与设备的异步调度，以及 DSpark 变长验证的关键源码。', '04'),
    ('source-map', '源码地图', '按问题和深度选择阅读路线，沿固定 commit 的符号进入源码。', '05'),
    ('evidence', '版本与证据', '逐条源码或官方文档证据，包含固定 commit 链接、符号、行号及校验摘要。', '06'),
    ('about', '使用与归属', '本地阅读、图形操作、导出、重新生成与上游归属说明。', '07'),
]

class Headings(HTMLParser):
    def __init__(self):
        super().__init__(); self.items = []; self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == 'h2': self.current = [dict(attrs).get('id'), '']
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data
    def handle_endtag(self, tag):
        if tag == 'h2' and self.current is not None:
            if not self.current[0]: raise ValueError(f'Heading requires an id: {self.current[1]}')
            self.items.append(self.current); self.current = None

def source_link(match):
    row = EVIDENCE[match.group(1)]
    kind = '源码' if row['kind'] == 'source' else '官方文档'
    return (f'<a class="source" href="{html.escape(row["url"], quote=True)}" title="{html.escape(row["path"])}:{row["start"]}">'
            f'<span class="kind">{kind} {row["id"]}</span><code translate="no">{html.escape(row["symbol"])}</code><span aria-hidden="true">↗</span></a>')

def evidence_rows():
    rows = []
    for row in EVIDENCE.values():
        kind = '源码确认' if row['kind'] == 'source' else '官方文档描述'
        rows.append(f'''<section class="evidence-row" id="{row['id']}">
<h3><code>{row['id']}</code> · {html.escape(row['symbol'])}<span class="badge">{kind}</span></h3>
<p>{html.escape(row['claim'])}</p>
<a class="evidence-path" href="{row['url']}"><code translate="no">{row['path']}:{row['start']}-{row['end']}</code> ↗</a>
<details><summary>核对锚点与摘要</summary><p>起始行：<code>{html.escape(row['anchor'])}</code></p><p class="checksum">片段 SHA-256：<code>{row['excerpt_sha256']}</code></p></details>
</section>''')
    return '\n'.join(rows)

def build():
    template = (ROOT / 'templates/base.html').read_text()
    site = ROOT / 'site'
    for index, (slug, title, description, chapter) in enumerate(PAGES):
        body = (ROOT / f'content/{slug}.html').read_text()
        body = re.sub(r'\{\{src:([ED]\d+)\}\}', source_link, body)
        body = body.replace('{{evidence_rows}}', evidence_rows()).replace('{{commit}}', BASELINE['commit']).replace('{{short_commit}}', BASELINE['commit'][:12]).replace('{{evidence_count}}', str(BASELINE['evidence_count']))
        navigation = ''.join(f'<a href="{other}.html"'+(' aria-current="page"' if other == slug else '')+f'>{label}</a>' for other,label,_,_ in PAGES[1:7])
        if slug == 'index':
            main = f'<div class="home">{body}</div>'
        else:
            toc = Headings(); toc.feed(body)
            toc_links = ''.join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor,label in toc.items)
            previous = PAGES[max(0,index-1)]; following = PAGES[min(len(PAGES)-1,index+1)]
            next_nav = f'<nav class="page-next" aria-label="连续阅读"><a href="{previous[0]}.html">← {previous[1]}</a><a href="{following[0]}.html">{following[1]} →</a></nav>' if index < len(PAGES)-1 else ''
            main = f'''<div class="article-shell"><aside class="toc"><details open><summary>本页内容</summary><nav aria-label="页内导航">{toc_links}</nav></details><p class="reading-note">所有源码链接固定到<br><code>{BASELINE['commit'][:12]}</code><br>原始函数名保留英文。</p></aside><article class="article"><header class="article-header"><p class="chapter">{chapter} / DEEPINFER ATLAS</p><h1>{title}</h1><p class="lead">{description}</p></header>{body}{next_nav}</article></div>'''
        values = {'title':title,'description':description,'main':main,'navigation':navigation,'commit':BASELINE['commit'],'short_commit':BASELINE['commit'][:12]}
        result = template
        for key,value in values.items(): result = result.replace('{{'+key+'}}',value)
        if '{{' in result: raise ValueError(f'Unresolved template in {slug}')
        (site / f'{slug}.html').write_text(result)
    (site / '.nojekyll').touch()
    resources = site/'resources'; resources.mkdir(exist_ok=True)
    for path in (ROOT/'docs').glob('*.md'): shutil.copyfile(path,resources/path.name)
    for path in [ROOT/'LICENSE', ROOT/'THIRD_PARTY_NOTICES.md']:
        if path.exists(): shutil.copyfile(path,resources/path.name)
    data_dir=site/'data';data_dir.mkdir(exist_ok=True)
    for path in (ROOT/'data').glob('*.json'):shutil.copyfile(path,data_dir/path.name)
    dist=ROOT/'dist'
    if dist.exists(): shutil.rmtree(dist)
    # Visual QA sidecars stay in the repository; deploy the three trusted HTML artifacts only.
    shutil.copytree(site,dist,ignore=shutil.ignore_patterns('*.visual-check.*'))
    print(f'Built {len(PAGES)} pages and 3 standalone diagrams into site/ and dist/. No runtime dependencies.')

if __name__ == '__main__': build()
