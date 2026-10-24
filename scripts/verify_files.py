"""Verify that the downloaded project matches the delivered manifest."""
from pathlib import Path
import hashlib,sys
root=Path(__file__).resolve().parents[1]
failed=[];count=0
for line in (root/'MANIFEST.sha256').read_text().splitlines():
 expected,name=line.split('  ',1);p=root/name;count+=1
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:failed.append(name)
if failed:
 print('Missing or changed files:');print('\n'.join(failed));sys.exit(1)
print(f'PASS: all {count} packaged files match their SHA-256 checksums.')
