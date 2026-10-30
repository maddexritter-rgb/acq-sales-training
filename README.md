# ACQ Sales Training

Give Claude Code or Codex a sales call. Get specific feedback, better wording, and a focused practice drill.

## Start here

Paste this into **Claude Code or Codex**, alongside a recording, its local file path, or a video URL:

> Install https://github.com/maddexritter-rgb/acq-sales-training into this project and review this sales call. Follow its INSTALL.md, handle setup, and give me the most important improvement with exact replacement wording.

The assistant handles installation and local transcription, then gives feedback in the conversation. No transcription account, API key, or manual Python configuration. First use downloads software and models and can take several minutes. Later calls reuse the cache. Normal host permission prompts still apply.

Already in this repository? Say: **“Review this call: /path/to/recording.mp4”**. Or paste a YouTube or other supported video link—the assistant downloads its audio with yt-dlp and continues through local transcription to feedback. For a transcript, paste it or attach TXT, SRT, VTT, or provider JSON. Connected recorder transcripts also work when your assistant has access.

## What comes back

- The most important observable behavior to improve, with the call moment that supports it.
- Suggested words for the rep, where to wait, and how to respond to the buyer's answer.
- Relevant short attributed training guidance and one practice drill.

Feedback is written as an observer, so a rep, manager, or owner can submit the call. The assistant does not assume the uploader is the rep. Unknown deal outcomes remain unknown.

## Recording support

Local transcription, estimated speaker turns and word timing, speech-gap detection, pace, pitch, and recording-level measurements. No paid transcription fallback. Models and recordings are processed locally; the transcript is read by your chosen assistant under its own data handling terms. Local transcription does not mean the entire AI coaching conversation is offline.

The included launchers automate runtime setup on macOS/Linux and provide a Windows PowerShell route. Apple Silicon execution has been tested; Windows/Linux launchers and dependency compatibility still need real-machine validation. Expect several GB of available disk and slower runs on weaker computers. Background noise, overlap, names, and short replies can cause errors. Verify important quotes; pitch alone does not establish emotion or intent.

This is a skill for an existing Claude Code/Codex installation with permission to execute local programs and download dependencies. It is not a standalone hosted application. The coaching uses distilled training material; it is not personally authored or reviewed by the quoted trainer. No private prospect recordings or full training books are included.

See [installation instructions](INSTALL.md), [the skill](skills/sales-call-audit/SKILL.md), and [audio implementation and third-party notices](skills/sales-call-audit/references/local-audio.md).

## Coaching depth

The bundled learning material contains 100 detailed source-backed decision cards across ten coaching areas and ten worked scenarios with replacement dialogue, buyer-response branches, and practice criteria. It was built after reading every retained text line of both supplied video courses and the entire extracted handbook text. Each card provides a trigger, a specific intervention, original suggested wording, conditional next steps, a practice check, boundaries, and source-section references. Full courses, the paid handbook, private source indexes, and real prospect transcripts are not distributed. The distilled guidance itself is public and readable.

Ask for a focused call review, a script rewrite, or interactive practice. During practice the coach gives one buyer line, waits for the learner, and corrects one behavior before the next attempt.

Explore the [coaching library](skills/sales-call-audit/brand/alex/library/README.md), see [an example first audit](skills/sales-call-audit/brand/alex/library/first-audit.md), or inspect [source coverage](skills/sales-call-audit/brand/alex/library/coverage.json). The first response stays focused; the deeper library supports follow-up questions, scripts, and practice.

## Video-link intake

The launcher automatically installs yt-dlp and YouTube JavaScript support. No separate downloader setup or API key is required. Supply one completed, accessible video; playlists and live streams are not accepted. Private, blocked, DRM-protected, or unsupported videos may need an upload or an authorized transcript connector. First-use setup and transcription take time; processing is not instant. Downloads stay local and are preserved alongside the evidence folder.
