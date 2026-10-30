import importlib.util,json,sys,tempfile,types
from pathlib import Path
r=Path(__file__).resolve().parents[1];p=r/'skills/sales-call-audit/scripts/download_video.py'
spec=importlib.util.spec_from_file_location('download_video',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for url in ['file:///etc/passwd','ftp://example.com/a','https://user:pass@example.com/a','https:///a']:
    try:m.validate_url(url)
    except ValueError:pass
    else:raise AssertionError(url)
assert m.validate_url('https://example.com/video?a=1&b=2')
for info in [None,{'_type':'playlist'},{'entries':[]},{'is_live':True},{'live_status':'is_upcoming'}]:
    try:m.single_video(info)
    except ValueError:pass
    else:raise AssertionError(info)
m.single_video({'id':'completed','live_status':'was_live'})
class FakeDL:
    calls=[]
    def __init__(self,opts):self.opts=opts;FakeDL.calls.append(opts)
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def extract_info(self,url,download):
        if download:Path(self.prepare_filename({})).write_bytes(b'test media')
        return {'id':'test','title':'test','duration':1,'webpage_url':url}
    def prepare_filename(self,info):return self.opts['outtmpl'].replace('%(ext)s','webm')
sys.modules['yt_dlp']=types.SimpleNamespace(YoutubeDL=FakeDL)
with tempfile.TemporaryDirectory() as td:
    dest=Path(td)/'source';media=m.download('https://example.com/video',dest)
    assert media.read_bytes()==b'test media'
    assert json.loads((dest/'source.json').read_text())['download_complete']
    assert FakeDL.calls[0]['noplaylist'] and FakeDL.calls[0]['overwrites']==False
    try:m.download('https://example.com/video',dest)
    except FileExistsError:pass
    else:raise AssertionError('Existing download overwritten')
print('URL validation, playlist/live rejection, downloaded-file provenance, existing-source protection: PASS (mock downloader)')
import subprocess
with tempfile.TemporaryDirectory() as td:
    result=subprocess.run([sys.executable,str(p.with_name('run_local_audio.py')),'https://example.com/video',str(Path(td)/'evidence'),'--offline','--cache',str(Path(td)/'cache')],capture_output=True,text=True)
    assert result.returncode!=0 and 'requires internet' in result.stderr
    assert not (Path(td)/'cache').exists()
print('Offline URL rejected before dependency setup: PASS')
