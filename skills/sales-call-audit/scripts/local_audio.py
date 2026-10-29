#!/usr/bin/env python3
"""No-key, local recording evidence. Run via run_local_audio.py for automatic setup."""
import argparse, hashlib, json, math, os, sys, tarfile, time, urllib.request
from pathlib import Path
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_VERBOSITY'] = 'error'
SR = 16000
ASR_REPO = 'Systran/faster-whisper-small'
ASR_REV = '536b0662742c02347bc0e980a01041f333bce120'
SEG_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-segmentation-models/sherpa-onnx-pyannote-segmentation-3-0.tar.bz2'
SEG_HASH = '24615ee884c897d9d2ba09bb4d30da6bb1b15e685065962db5b02e76e4996488'
EMB_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/nemo_en_titanet_small.onnx'
EMB_HASH = 'ad4a1802485d8b34c722d2a9d04249662f2ece5d28a7a039063ca22f515a789e'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def download(url, path, digest, offline):
    if path.exists():
        if sha(path) != digest: raise ValueError(f'Cached model checksum mismatch: {path.name}')
        return
    if offline: raise RuntimeError(f'Offline model missing: {path.name}. Run setup online once.')
    print(f'Downloading public model: {path.name}', flush=True)
    part = path.with_suffix(path.suffix+'.part')
    with urllib.request.urlopen(url, timeout=120) as response, part.open('wb') as f:
        while block := response.read(1024*1024): f.write(block)
    if sha(part) != digest: raise ValueError('Downloaded model checksum mismatch')
    part.replace(path)


def diarize(audio, cache, offline, speakers):
    import sherpa_onnx as so
    archive = cache/'segmentation.tar.bz2'; emb = cache/'nemo_en_titanet_small.onnx'
    download(SEG_URL, archive, SEG_HASH, offline); download(EMB_URL, emb, EMB_HASH, offline)
    # Copy only known regular members; never extract arbitrary archive paths.
    with tarfile.open(archive) as tar:
        for name in ('model.onnx','LICENSE','README.md'):
            member = tar.getmember('sherpa-onnx-pyannote-segmentation-3-0/'+name)
            if not member.isfile(): raise ValueError('Unexpected model archive member')
            data = tar.extractfile(member).read()
            target = cache/('segmentation-'+name)
            if not target.exists() or target.read_bytes()!=data: target.write_bytes(data)
    cfg = so.OfflineSpeakerDiarizationConfig(
        segmentation=so.OfflineSpeakerSegmentationModelConfig(
            pyannote=so.OfflineSpeakerSegmentationPyannoteModelConfig(model=str(cache/'segmentation-model.onnx')),
            num_threads=2),
        embedding=so.SpeakerEmbeddingExtractorConfig(model=str(emb),num_threads=2),
        clustering=so.FastClusteringConfig(num_clusters=speakers,threshold=0.5),
        min_duration_on=0.3,min_duration_off=0.5)
    if not cfg.validate(): raise RuntimeError('Invalid diarization configuration')
    detector = so.OfflineSpeakerDiarization(cfg)
    if detector.sample_rate!=SR: raise RuntimeError('Unexpected diarization sample rate')
    result=detector.process(audio).sort_by_start_time()
    return [dict(start=float(x.start),end=float(x.end),speaker=f'speaker_{x.speaker:02d}') for x in result]


def assign(start,end,intervals):
    scores={}
    for r in intervals:
        overlap=max(0,min(end,r['end'])-max(start,r['start']))
        scores[r['speaker']]=scores.get(r['speaker'],0)+overlap
    ranked=sorted(scores.items(),key=lambda x:x[1],reverse=True)
    duration=max(end-start,0.001)
    if not ranked or ranked[0][1]/duration<0.5: return 'unknown'
    if len(ranked)>1 and ranked[1][1]>0.2*duration: return 'unknown'
    return ranked[0][0]


def nonspeech_gaps(spans,duration,min_gap=.3):
    gaps=[];cursor=0.
    for s in sorted(spans,key=lambda x:x['start']):
        start=max(0,min(duration,float(s['start'])));end=max(start,min(duration,float(s['end'])))
        if start-cursor>=min_gap: gaps.append(dict(start=cursor,end=start,duration=start-cursor))
        cursor=max(cursor,end)
    if duration-cursor>=min_gap: gaps.append(dict(start=cursor,end=duration,duration=duration-cursor))
    return gaps


def acoustics(audio,words):
    import numpy as np
    import parselmouth
    frames=[]
    # Bounded pitch analysis; never classify emotion from pitch or level.
    for offset in range(0,len(audio),30*SR):
        block=audio[offset:offset+30*SR]
        if len(block)<SR//10: continue
        pitch=parselmouth.Sound(block,sampling_frequency=SR).to_pitch_ac(time_step=.01,pitch_floor=60,pitch_ceiling=500)
        for t,f in zip(pitch.xs(),pitch.selected_array['frequency']):
            if f>0: frames.append((float(t+offset/SR),float(f)))
    ts=np.array([x[0] for x in frames]);hz=np.array([x[1] for x in frames])
    for w in words:
        s,e=w['start'],w['end'];wave=audio[max(0,int(s*SR)):min(len(audio),int(e*SR))]
        f=hz[(ts>=s)&(ts<e)]
        w['acoustics']={'rms_dbfs':round(float(20*np.log10(max(float(np.sqrt(np.mean(wave**2))),1e-9))),2) if len(wave) else None,
                        'voiced_pitch_hz_median':round(float(np.median(f)),2) if len(f)>=3 else None,
                        'pitch_frames':int(len(f))}
    return {'pitch_method':'Praat autocorrelation, 60–500 Hz, 10ms step, 30s analysis windows',
            'level_method':'RMS dBFS of original decoded mono signal over ASR word bounds; not calibrated SPL',
            'pitch_frames':len(frames)}


def run(args):
    import numpy as np, av
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio
    from faster_whisper.vad import get_speech_timestamps,VadOptions
    from huggingface_hub import snapshot_download
    started=time.monotonic()
    if not args.input.is_file(): raise ValueError('Input recording not found')
    if args.output.exists(): raise ValueError('Output directory exists; choose a new output directory')
    args.cache.mkdir(parents=True,exist_ok=True)
    if args.offline: os.environ['HF_HUB_OFFLINE']='1'
    with av.open(str(args.input)) as container:
        streams=list(container.streams.audio)
        if not streams: raise ValueError('No audio stream in recording')
        if len(streams)!=1: raise ValueError('Multiple audio streams: export the intended dialogue stream first; no stream silently omitted')
        channels=streams[0].codec_context.channels
    print('Decoding recording locally',flush=True)
    audio=decode_audio(str(args.input),sampling_rate=SR)
    duration=len(audio)/SR
    if not len(audio) or not np.all(np.isfinite(audio)): raise ValueError('Empty or invalid decoded audio')
    print(f'Decoded {duration:.1f}s. Measuring speech activity.',flush=True)
    vad=get_speech_timestamps(audio,VadOptions(min_silence_duration_ms=300,speech_pad_ms=0),sampling_rate=SR)
    spans=[dict(start=x['start']/SR,end=x['end']/SR) for x in vad]
    words=[];segments=[];diar=[];warnings=[]
    if channels>1: warnings.append('Multiple channels mixed to mono. Channel-specific separation and acoustic measurements are not available.')
    language=None
    if spans:
        print('Preparing local transcription model (first use downloads weights)',flush=True)
        model_path=snapshot_download(repo_id=ASR_REPO,revision=ASR_REV,cache_dir=str(args.cache/'hf'),
                    local_files_only=args.offline,token=False,allow_patterns=['config.json','model.bin','tokenizer.json','vocabulary.*','preprocessor_config.json'])
        model=WhisperModel(model_path,device='cpu',compute_type='int8',cpu_threads=args.threads)
        print('Transcribing locally; no recording is uploaded',flush=True)
        generated,info=model.transcribe(audio,language=args.language,word_timestamps=True,beam_size=5,
                    condition_on_previous_text=False,vad_filter=True,vad_parameters=dict(min_silence_duration_ms=300))
        language=info.language
        for seg in generated:
            segments.append(dict(start=float(seg.start),end=float(seg.end),text=seg.text,avg_logprob=float(seg.avg_logprob)))
            for w in seg.words or []:
                words.append(dict(word_id=len(words)+1,start=float(w.start),end=float(w.end),text=w.word,
                                  asr_probability=float(w.probability)))
        print(f'Transcribed {len(words)} words. Separating speakers.',flush=True)
        if not args.no_diarization:
            try: diar=diarize(audio,args.cache,args.offline,args.speakers)
            except Exception as exc:
                warnings.append(f'Diarization unavailable: {type(exc).__name__}. Speaker identity remains unknown. No cloud fallback.')
        for w in words:
            w['speaker']=assign(w['start'],w['end'],diar)
            w['review_flags']=[]
            if w['asr_probability']<.5:w['review_flags'].append('low_asr_probability')
            if w['end']-w['start']<.02 or w['end']-w['start']>1.5:w['review_flags'].append('uncertain_word_boundary')
        if any(w['review_flags'] for w in words):warnings.append('Some word probabilities or boundaries require review; use review_flags before quoting or timing a word.')
    else: warnings.append('No speech detected. No transcript was invented; review audio if speech was expected.')
    print('Measuring pitch and recording level',flush=True)
    acoustic_meta=acoustics(audio,words) if words else {}
    turns=[]
    for w in words:
        if turns and turns[-1]['speaker']==w['speaker'] and w['start']-turns[-1]['end']<=1.5:
            turn=turns[-1];turn['text']+=w['text'];turn['end']=max(turn['end'],w['end']);turn['word_ids'].append(w['word_id'])
        else:turns.append(dict(turn_id=len(turns)+1,start=w['start'],end=w['end'],speaker=w['speaker'],role='unknown',text=w['text'],word_ids=[w['word_id']]))
    for turn in turns:
        turn['text']=turn['text'].strip()
        tw=[words[i-1] for i in turn['word_ids']]
        pitches=[w['acoustics']['voiced_pitch_hz_median'] for w in tw if w['acoustics']['voiced_pitch_hz_median'] is not None]
        elapsed=turn['end']-turn['start']
        turn['delivery']={'elapsed_wpm':round(len(tw)*60/elapsed,1) if elapsed>=3 else None,
                          'word_count':len(tw),
                          'pitch_hz_p10_p50_p90': [round(float(x),1) for x in np.percentile(pitches,[10,50,90])] if len(pitches)>=5 else None,
                          'interpretation':'Measurements over estimated word bounds; no emotional or intention label'}
    gaps=nonspeech_gaps(spans,duration)
    for gap in gaps:
        before=[w for w in words if w['end']<=gap['start']+.15]
        after=[w for w in words if w['start']>=gap['end']-.15]
        prev=before[-1] if before else None;nxt=after[0] if after else None
        gap.update(before_word_id=prev['word_id'] if prev else None,after_word_id=nxt['word_id'] if nxt else None,
                   scope='within_speaker_candidate' if prev and nxt and prev['speaker']==nxt['speaker']!='unknown' else 'unassigned_or_turn_gap')
    rates=[]
    for start in np.arange(0,duration,30.):
        end=min(duration,float(start+30));ws=[w for w in words if start<=(w['start']+w['end'])/2<end]
        rates.append(dict(start=float(start),end=end,words=len(ws),window_wpm=round(len(ws)*60/(end-start),1)))
    payload=dict(schema_version='local-audio-1',source_id=sha(args.input),source_type='local_recording',
        timing_unit='seconds',source_offset_seconds=args.source_offset,source_duration_seconds=duration,
        role_mapping_status='unconfirmed',observed_call_result='unknown',verified_deal_outcome='unknown',
        engine='faster-whisper',model=ASR_REPO,model_revision=ASR_REV,language=language,
        speaker_method='sherpa-onnx automatic clusters' if diar else 'unavailable',turns=turns,words=words,
        asr_segments=segments,speaker_intervals=diar,speech_intervals=spans,nonspeech_gaps=gaps,
        rate_windows=rates,acoustic_method=acoustic_meta,elapsed_seconds=round(time.monotonic()-started,2),
        warnings=warnings,limitations=['ASR may omit fillers/restarts or invent words; consequential excerpts need playback.',
        'Word timing and speaker clusters are estimates. Speaker labels do not establish rep/buyer roles.',
        'Non-speech intervals are VAD estimates, not proof of deliberate pauses. Noise, edits and connection loss can produce gaps.',
        'Pitch and level measurements do not establish emotion, confidence, intention, emphasis or buyer trust.',
        'Overlapping voices can corrupt transcription, diarization and pitch. No reliable interruption count is provided.'])
    # Stage only complete results. Never overwrite the original or an earlier run.
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'evidence.json').write_text(json.dumps(payload,indent=2,allow_nan=False))
    (args.output/'transcript.txt').write_text('\n'.join(f"[{t['start']:.2f}–{t['end']:.2f}] {t['speaker']}: {t['text']}" for t in turns))
    (args.output/'measurement-notes.md').write_text('# Local recording evidence\n\n'+f'{len(words)} words, {len(turns)} turns, {len(gaps)} non-speech gaps >=0.3s.\n\n'+'\n'.join('- '+x for x in warnings+payload['limitations']))
    print(json.dumps(dict(status='complete' if words else 'no_speech_detected',words=len(words),turns=len(turns),speakers=len(set(x['speaker'] for x in diar)),seconds=payload['elapsed_seconds'],output=str(args.output),warnings=warnings)),flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--cache',type=Path,required=True);p.add_argument('--offline',action='store_true')
    p.add_argument('--language',default=None,help='ISO language code; default automatic detection')
    p.add_argument('--speakers',type=int,default=-1,help='Known count; default automatic clustering, not necessarily accurate')
    p.add_argument('--no-diarization',action='store_true');p.add_argument('--threads',type=int,default=4)
    p.add_argument('--source-offset',type=float,default=0.,help='Offset of this excerpt within its parent recording; times stay excerpt-relative')
    args=p.parse_args()
    if args.threads<1 or args.speakers==0 or args.speakers< -1 or args.source_offset<0 or not math.isfinite(args.source_offset):p.error('Invalid numeric option')
    try:run(args)
    except Exception as exc:
        print(f'Local transcription failed ({type(exc).__name__}): {exc}',file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
