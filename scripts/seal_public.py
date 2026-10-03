"""Seal the canonical bytes of every tracked public file except this seal."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf-8').split('\0')
seal={}
for rel in sorted(filter(None,paths)):
    if rel=='archive/public_manifest.json':continue
    p=ROOT/rel
    b=p.read_bytes()
    if p.suffix.lower() not in ('.pdf','.docx','.png','.jpg'):b=b.replace(b'\r\n',b'\n')
    seal[rel]=hashlib.sha256(b).hexdigest()
(ROOT/'archive/public_manifest.json').write_text(json.dumps(seal,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Sealed',len(seal),'tracked public files')
