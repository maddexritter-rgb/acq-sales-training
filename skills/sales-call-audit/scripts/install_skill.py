"""Install a self-contained project skill without overwriting existing work."""
import argparse, hashlib, json, shutil, tempfile
from pathlib import Path

def inventory(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('host',choices=['codex','claude']);p.add_argument('--project',required=True,type=Path)
    a=p.parse_args();source=Path(__file__).resolve().parent.parent
    project=a.project.resolve()
    if not project.is_dir():p.error('Project directory must already exist')
    target=project/('.agents' if a.host=='codex' else '.claude')/'skills'/'sales-call-audit'
    if target.exists() or target.is_symlink():
        if target.is_dir() and inventory(source)==inventory(target):
            print(json.dumps({'status':'already_installed','path':str(target)}));return
        p.error(f'Existing installation differs; preserved unchanged: {target}')
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.sales-coach-install-',dir=target.parent) as td:
        stage=Path(td)/'skill';shutil.copytree(source,stage,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        stage.rename(target)
    print(json.dumps({'status':'installed','path':str(target),'next':'Read SKILL.md directly and continue the requested audit now.'}))
if __name__=='__main__':main()
