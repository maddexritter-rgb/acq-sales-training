#!/usr/bin/env python3
"""Download one accessible video/audio URL into a new private source directory."""
import argparse,hashlib,json,os,sys
from pathlib import Path
from urllib.parse import urlsplit

def validate_url(value):
    parsed=urlsplit(value)
    if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Supply an HTTP(S) video URL without embedded credentials.')
    return value

def single_video(info):
    if not info or info.get('_type') in ('playlist','multi_video') or 'entries' in info:
        raise ValueError('Supply one video URL, not a playlist or channel.')
    if info.get('is_live') or info.get('live_status') in ('is_live','is_upcoming','post_live'):
        raise ValueError('Use a completed recording rather than a live or upcoming stream.')

def download(url, folder):
    from yt_dlp import YoutubeDL
    validate_url(url)
    folder=Path(folder).resolve();folder.mkdir(parents=True,exist_ok=False)
    # The isolated runtime supplies Deno and bundled EJS; no user cookie/config loading.
    deno=Path(sys.executable).parent/('deno.exe' if os.name=='nt' else 'deno')
    opts={'format':'bestaudio/best', 'noplaylist':True,'playlistend':1,
          'outtmpl':str(folder/'recording.%(ext)s'),'overwrites':False,
          'socket_timeout':30,'retries':3,'fragment_retries':3,
          'max_filesize':2*1024**3,'quiet':True,'noprogress':True,
          'js_runtimes':{'deno':{'path':str(deno)}},'remote_components':set()}
    with YoutubeDL(opts) as ydl:
        info=ydl.extract_info(url,download=False);single_video(info)
        info=ydl.extract_info(url,download=True);single_video(info)
        media=Path(ydl.prepare_filename(info)).resolve()
    if media.parent!=folder or not media.is_file() or media.stat().st_size==0:
        raise ValueError('No complete media file was downloaded (possibly size/access restriction).')
    digest=hashlib.sha256()
    with media.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
    manifest={'source_url':url,'webpage_url':info.get('webpage_url'),'title':info.get('title'),
              'video_id':info.get('id'),'duration':info.get('duration'),'extractor':info.get('extractor'),
              'media_path':str(media),'sha256':digest.hexdigest(),'download_complete':True}
    (folder/'source.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return media

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('url');p.add_argument('directory',type=Path);a=p.parse_args()
    try:download(a.url,a.directory)
    except Exception as e:
        print(f'Video download failed: {e}\nUse an accessible single-video link, an authorized recorder transcript, or an uploaded recording. No cookies or login bypass were attempted. Partial downloads, if any, are preserved.',file=sys.stderr)
        return 1
    return 0
if __name__=='__main__':sys.exit(main())
