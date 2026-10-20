#!/usr/bin/env python3
"""Fetch only the recorded analysis baseline; never reset an existing checkout."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASELINE=json.loads((ROOT/'data/upstream.json').read_text())
DESTINATION=ROOT/'.upstream/DeepInfer'

def git(*args):
    return subprocess.check_output(['git','-C',str(DESTINATION),*args],text=True).strip()

if DESTINATION.exists():
    if not (DESTINATION/'.git').exists(): sys.exit(f'Refusing to modify existing non-Git directory: {DESTINATION}')
    actual=git('rev-parse','HEAD')
    if actual!=BASELINE['commit']: sys.exit(f'Existing checkout is {actual}; expected {BASELINE["commit"]}. Use a separate checkout for new research.')
    if git('status','--porcelain'): sys.exit('Upstream checkout has local changes. Preserve them before verification.')
else:
    DESTINATION.mkdir(parents=True)
    git('init')
    git('remote','add','origin',BASELINE['repository'])
    git('fetch','--depth','1','origin',BASELINE['commit'])
    git('checkout','--detach','FETCH_HEAD')
assert git('rev-parse','HEAD')==BASELINE['commit']
print(f'Pinned upstream ready: {BASELINE["commit"]}\n{DESTINATION}')
