from pathlib import Path
import tempfile, subprocess, sys, re, json
r=Path(__file__).resolve().parents[1];s=r/'skills/sales-call-audit';installer=s/'scripts/install_skill.py'
for p in r.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not target.startswith(('http:','https:','#')):assert (p.parent/target).exists(),(p,target)
with tempfile.TemporaryDirectory() as td:
 for host,dot in [('codex','.agents'),('claude','.claude')]:
  cmd=[sys.executable,str(installer),host,'--project',td]
  a=subprocess.run(cmd,capture_output=True,text=True);assert a.returncode==0,a.stderr
  installed=Path(td)/dot/'skills/sales-call-audit';assert (installed/'brand/alex/quote-bank.json').exists()
  a=subprocess.run(cmd,capture_output=True,text=True);assert 'already_installed' in a.stdout
  p=installed/'SKILL.md';p.write_text(p.read_text()+'\nLocal customization\n')
  a=subprocess.run(cmd,capture_output=True,text=True);assert a.returncode!=0
  assert p.read_text().endswith('Local customization\n')
print('Relative references, both install locations, idempotency, existing customization preservation: PASS')
