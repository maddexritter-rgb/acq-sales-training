#!/usr/bin/env python3
"""One-command local audio setup/run. No account, key, or recording upload."""
import argparse,hashlib,json,os,shutil,subprocess,sys,venv
from pathlib import Path
REQ=['faster-whisper==1.2.1','sherpa-onnx==2.0.1','praat-parselmouth==0.4.7','numpy==2.2.6']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('output',type=Path)
    p.add_argument('--cache',type=Path,default=Path(os.environ.get('LOCALAPPDATA',str(Path.home()/'.cache')))/'sales-call-audit-local')
    p.add_argument('--offline',action='store_true')
    args,extra=p.parse_known_args()
    uv=shutil.which('uv')
    interpreter=sys.executable
    if not (3,10)<=sys.version_info[:2]<(3,14):
        interpreter=next((shutil.which(x) for x in ('python3.11','python3.12','python3.13','python3.10') if shutil.which(x)),None)
        if interpreter is None and uv: interpreter='3.11'
        if interpreter is None:p.error('A supported Python is needed. Install Python 3.11 or uv, then retry; no API key is needed.')
    from download_video import validate_url
    is_url=args.input.lower().startswith(('http://','https://'))
    if is_url:
        try:validate_url(args.input)
        except ValueError as e:p.error(str(e))
        if args.offline:p.error('A video URL requires internet. Use its downloaded local file for offline transcription.')
    elif not Path(args.input).is_file():p.error('Recording file not found; supply a local file or HTTP(S) video URL')
    requirements=REQ+(['yt-dlp[default]==2026.10.26','deno==2.9.8'] if is_url else [])
    if args.output.exists():p.error('Output directory already exists; choose a new one')
    args.cache=args.cache.resolve();runtime=args.cache/'runtime'
    py=runtime/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    stamp=runtime/'installed.json'
    signature=hashlib.sha256(json.dumps(requirements).encode()).hexdigest()
    ready=py.exists() and stamp.exists() and set(requirements).issubset(json.loads(stamp.read_text()).get('requirements',[]))
    if not ready:
        if args.offline:p.error('Offline runtime missing. Run online once to install dependencies and models.')
        print('First-use setup: installing local audio dependencies. No account or API key needed.',flush=True)
        runtime.parent.mkdir(parents=True,exist_ok=True)
        uv=shutil.which('uv')
        if not py.exists():
            if uv:subprocess.run([uv,'venv','--python',interpreter,str(runtime)],check=True)
            else:subprocess.run([interpreter,'-m','venv',str(runtime)],check=True)
        command=[uv,'pip','install','--python',str(py)] if uv else [str(py),'-m','pip','install']
        subprocess.run(command+requirements,check=True)
        stamp.write_text(json.dumps({'requirements_hash':signature,'requirements':requirements}))
    if is_url:
        source_dir=Path(str(args.output.resolve())+'.source')
        if source_dir.exists():p.error('Source directory already exists; use its recording locally or choose a new output name')
        print('Downloading the video audio, then transcribing locally.',flush=True)
        result=subprocess.run([str(py),str(Path(__file__).with_name('download_video.py')),args.input,str(source_dir)])
        if result.returncode:return result.returncode
        input_path=Path(json.loads((source_dir/'source.json').read_text())['media_path'])
    else:input_path=Path(args.input)
    command=[str(py),str(Path(__file__).with_name('local_audio.py')),str(input_path.resolve()),str(args.output.resolve()),'--cache',str(args.cache)]+extra
    if args.offline:command.append('--offline')
    return subprocess.run(command).returncode
if __name__=='__main__':sys.exit(main())
