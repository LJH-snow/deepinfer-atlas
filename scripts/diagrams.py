#!/usr/bin/env python3
"""Regenerate trusted HTML and automated visual evidence with Archify 2.16."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
candidates=[Path(os.environ['ARCHIFY_HOME'])] if 'ARCHIFY_HOME' in os.environ else [Path.home()/'.agents/skills/archify',Path.home()/'.codex/skills/archify']
ARCHIFY=next((p for p in candidates if (p/'bin/archify.mjs').is_file()),None)
if ARCHIFY is None:sys.exit('Archify 2.16 is needed only for diagram regeneration. Set ARCHIFY_HOME to its package directory. Existing HTML remains usable.')
if 'version: "2.16"' not in (ARCHIFY/'SKILL.md').read_text():sys.exit('Expected Archify skill version 2.16. Review schema/runtime changes before changing the pinned tool version.')
receipts=ROOT/'diagrams/receipts';receipts.mkdir(exist_ok=True)
for name in ['architecture','request','scope']:
    spec=ROOT/f'diagrams/specs/{name}.json';kind=json.loads(spec.read_text())['diagram_type'];output=ROOT/f'site/diagrams/{name}.html'
    for action,args in [('validate',[kind,str(spec),'--quality','showcase']),('deliver',[kind,str(spec),str(output),'--quality','showcase']),('visual-check',[str(output)])]:
        result=subprocess.run(['node',str(ARCHIFY/'bin/archify.mjs'),action,*args,'--json'],text=True,capture_output=True)
        receipt=receipts/f'{name}.{action if action != "visual-check" else "visual-command"}.json';receipt.write_text(result.stdout)
        if result.returncode:
            sys.stderr.write(result.stderr);sys.stderr.write(result.stdout);sys.exit(f'{name}: {action} failed; later stages were not run.')
        data=json.loads(result.stdout)
        if not data.get('ok'):sys.exit(f'{name}: command returned an unsuccessful receipt.')
        print(f'{name}: {action} passed')
print('Automated checks passed. Actual screenshot review and PNG re-export are still required; never infer perceptual acceptance from this command.')
