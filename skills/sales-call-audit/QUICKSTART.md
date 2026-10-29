# Sales-call audit — start here

This is an AI skill package for a host that can read skill instructions and your files. It includes a local transcription runner with no account or API key. It is not a standalone web application; recording ingestion requires a host that can execute local programs.

1. Extract this folder and load its SKILL.md in your skill-capable assistant, or attach the instruction and reference files to your assistant.
2. Supply a transcript, or authorize an available recorder connector to retrieve one. No connector is required for uploaded text. For audio/video, the assistant runs the bundled local setup and transcriber, then audits its transcript. First use downloads software and model weights; later runs can work offline. See [local audio](references/local-audio.md).
3. Say: “Audit this sales call. I sell [offer], the rep is [name], and the goal was [next step]. The outcome is [known result or unknown]. Give me the most important improvement and role-play it with me.”
4. You should receive evidence, what worked, one priority improvement, suggested wording, a drill, and any material limits.

If no transcript is available from a share link, export TXT/SRT/VTT or provider JSON from your recorder. Do not provide account passwords or payment credentials. Fathom is supported through host connector discovery or readable exports; no live Fathom connection was tested for this release.

## Optional local normalization
Requires Python 3, no packages or network. From this folder:

```sh
python3 scripts/normalize_transcript.py call.json evidence.json
python3 scripts/normalize_transcript.py call.vtt evidence.json
python3 scripts/normalize_transcript.py call.txt evidence.json
```

Trellus detail JSON and raw AssemblyAI JSON are recognized. Plain text uses stable line references with unknown timing/roles; SRT/VTT preserve cue times but require role confirmation. For another JSON schema, let the assistant inspect and adapt it explicitly. Never infer a format just from the recorder's name.

## Customize without changing the method
Supply your own offer facts, qualification criteria, approved proof, pricing, and an optional next-step link in a separate profile. Feedback is written as a third-person observer, suitable for reps, managers, and executives. The bundled brand profile and quote bank supply short attributed training quotes without video links. Keep the bundled brand folder with the skill to retain those quotes. The coaching must not borrow another company's promises or prices. The package contains generalized lessons, not private prospect transcripts or an impersonation of a trainer.

## Release status
Transcript pilot, not a validated predictor of sales results. Real Trellus transcript retrieval and local upload normalization were tested. Local recording ingestion was tested on two public call excerpts on Apple Silicon, including a cached run with network connections blocked. A live Fathom connector and other operating systems remain untested. A human sales leader has not yet reviewed the coaching. Start with one call, check its quotes and role mapping, then use the practice drill.

## Script rewrites

Ask: “Rewrite this discovery section using the coaching method. Keep the offer facts unchanged. Give the rep exact words, places to wait, and branches for different buyer answers.” For a full script, supply the approved offer and intended next step; missing material facts stay explicit. The result is an original draft based on the training, not a script personally written or approved by the trainer.

## V4 source coverage

The owner indexed the complete retained handbook and both supplied course transcripts. The handbook text has now been reviewed throughout; video review remains focused on documented ranges. The portable package includes 25 distilled decision cards, a voice profile, and seven brief source-checked quotations. Indexing is not equivalent to reviewing every minute of every video. Full transcripts, raw handbook, and private calls are not included.

## V5 recording support

Supply the recording and say “Audit this call.” The assistant transcribes it locally, estimates speaker turns, measures speech gaps, pace, pitch and recording level, then gives the same observer-style feedback. No provider API key is required. The launcher obtains Python automatically; permission to run local software is needed; a chat that only accepts text cannot run the audio tools. The first setup needs internet; a completed setup supports `--offline`. These measurements help identify moments to review; they do not prove emotion or intent.
