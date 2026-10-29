# Local audio: no account or API key

## User experience

The user supplies a recording and asks for feedback. The assistant preserves the original, runs the command below, reads the resulting evidence, maps speaker clusters to roles using the conversation, and delivers the normal third-person coaching. Do not make the user operate a terminal when the host can execute it. During initial setup, explain that software and public model weights are being downloaded; subsequent runs use the cache. If execution or downloads are unavailable, state that specific limitation and accept a transcript. A text-only chat cannot execute this package.

From the skill directory, run with a new output directory:

```sh
bash scripts/start.sh /absolute/path/call.mp4 /absolute/path/call-evidence
```

Supports common audio/video containers through PyAV. Python 3.10–3.13 is required for the runtime (3.11 tested); the bootstrap selects an installed compatible Python or uses installed uv to obtain 3.11. The shell launcher automatically obtains private uv and Python if missing. On Windows use `powershell -File scripts/start.ps1 INPUT OUTPUT`; this route has not yet been executed on a Windows machine. Dependencies are installed in an isolated cache, not globally. Allow several GB of free disk and enough memory for the recording. First use requires internet for packages and roughly 0.5 GB of model weights; no account, API key, or per-minute service fee. Local compute still uses the user's hardware. No audio upload is performed.

Options: `--language en` when language is known; `--speakers 2` only when the number of speakers is known; otherwise automatic clustering. Use `--offline` after one successful online run to prohibit model retrieval and require cached dependencies. Set `SALES_COACH_CACHE` to choose the runtime/model location when using the launcher. `--source-offset 1020` records the offset of an excerpt, without changing its relative times. Inputs and existing output directories are never overwritten. Multiple audio streams require an explicitly selected dialogue stream; stereo channels are mixed to mono with a warning.

## Evidence to read

Read `evidence.json` directly; do not convert it as AssemblyAI JSON. Its timestamps are seconds. `transcript.txt` is a convenient reading view, and `measurement-notes.md` records limits. Machine-generated words include estimated start/end, ASR probability, uncertain-boundary flags, speaker cluster, and available acoustic measurements. These are estimates, not a verbatim certification. Read all turns and review flags before selecting a coaching moment.

Speaker clusters are not identities. Infer rep/buyer from content when clear; otherwise ask one concise role question and avoid speaker-specific claims meanwhile. Short replies and cross-talk are particularly error-prone. If diarization fails, keep unknown speakers and report the failure; do not silently claim complete speaker separation.

The output includes:
- Non-speech gaps of at least 0.3 seconds, estimated with voice activity detection. These can be pauses, edits, connection loss, or missed quiet speech. Only call a gap the rep's deliberate pause when listening supports it.
- Words per minute over 30-second windows and sufficiently long estimated turns. Window rates include gaps; short replies are not useful pace comparisons. Word counts are best suited to languages with whitespace-separated words.
- Median voiced pitch per word and pitch percentiles per turn using Praat; recording level in dBFS per word. These do not establish emotional state, confidence, intent, sarcasm, trust, or a calibrated physical loudness. Compare within the same speaker and recording; recording gain and compression can change level.

For feedback, use a measurement only when it materially supports the recommendation. Prefer an observed action: “The rep asked the question, then started explaining before the buyer answered. Suggested rep response: … [wait].” For an unlistened gap say “The detector estimates a 1.2-second non-speech gap,” not “The buyer hesitated.” Never invent a finding from this example. Verify timing and words around the actual moment. Preserve uncertainty instead of interpreting a pitch change as proof of lost trust.

## Runtime and coverage

CPU int8 faster-whisper small supplies transcription and word timing. Sherpa-onnx with public segmentation and speaker embedding weights estimates speaker clusters. Praat/Parselmouth measures pitch; NumPy measures recording level. The runner pins primary dependency versions and the ASR revision and checks downloaded diarization model hashes. Transitive packages resolve at installation time; this is not a fully locked binary distribution.

Tested on Apple Silicon with two real public sales-call excerpts. Other operating systems, multilingual accuracy, very long calls, poor audio and overlapping speakers are not validated by this release. Local processing can be slower than real time on weaker hardware. ASR can omit fillers, miss names or invent words; important quotes require review. There is no hidden paid fallback.

## Third-party components

The ZIP contains our runner and instructions, not dependency binaries or model weights. First use fetches dependencies and weights separately under their own terms. Preserve their notices when redistributing them. Sources: [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [sherpa-onnx models](https://k2-fsa.github.io/sherpa/onnx/speaker-diarization/models.html), [Parselmouth](https://parselmouth.readthedocs.io/en/stable/). Faster-whisper is MIT; sherpa-onnx is Apache-2.0; Parselmouth/Praat includes GPL terms. Segmentation license and README are retained in the model cache. Do not describe the whole dependency/model stack as MIT or license-free.
