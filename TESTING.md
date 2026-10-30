# Release checks

Automated checks cover project installation for Claude Code and Codex, repeated installation, preservation of an existing modified skill, bundled profile portability, and relative reference integrity. Run `python tests/test_install.py`. These package checks ran locally. Automated GitHub Actions checks are not enabled because the current GitHub connection lacks workflow write permission; cross-platform checks remain pending.

Local Apple Silicon audio validation processed two public call excerpts (106 and 137 seconds). A cached run completed with network socket connections blocked. Known-pitch and gap fixtures passed; a silent recording produced no invented words. The repository launcher was additionally tested with PATH restricted to system tools, so it downloaded its own uv and Python before processing real audio. The package resolver reused its download cache; this was not a clean operating-system image.

Remaining validation: independent fresh Claude Code/Codex sessions from the published URL, Windows/Linux audio execution, multilingual and long-call accuracy, and independent human review of coaching. First-run execution is automated, but neither instant processing nor universally prompt-free installation is claimed.

Integration references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [uv installer options](https://docs.astral.sh/uv/reference/installer/).

## Coaching expansion validation

The coaching lab adds ten original worked scenarios and an interactive practice loop. Five fictional behavioral cases are supplied in [evaluations/coaching-cases.md](evaluations/coaching-cases.md). They are evaluation prompts with criteria, not claimed automated passes. Three real transcript moments were re-read and used for owner-local, author-reviewed feedback examples: corrected reporting premise, missed training-process follow-up, and an assumed missing roadmap. No private call transcript or real-case output was added to this repository. Independent fresh-session model evaluation remains pending.

## Full-library release — October 29, 2026

The earlier 25-card summary is replaced by 100 detailed cards in ten modules. Every retained line of the supplied handbook and both course caption files was read; [coverage](skills/sales-call-audit/brand/alex/library/coverage.json) records hashes, ranges, and exclusions. The entire retained caption file of the third public call demonstration was also read as practice evidence, with its repeated teaser deduplicated conceptually.

Run `python tests/test_library.py` as well as `python tests/test_install.py`. The library test checks 100 unique complete cards, Markdown/data parity, source-range bounds, twelve fictional retrieval probes, no-result/filter behavior, and execution of the lookup helper from both installed project locations. These checks passed locally.

Four complete retained real Trellus transcripts (218 turns) were read and normalized through a fresh project installation. Text and final turns matched the inputs exactly. Four author-created diagnosis queries retrieved the intended cards first. Private feedback examples covered a corrected diagnosis, contradictory support claims, connection failure as an alternative to price rejection, and a positive purchase-intent follow-up with payment still unverified. These were author-reviewed outputs. The queries were supplied after reading the calls; this is not a blind automatic diagnosis benchmark. Neither the transcripts nor the feedback containing private call excerpts are public.

Independent model/human review remains pending; no conversion lift is established. Audio implementation was unchanged, so its earlier real-audio validation was not rerun for this content release.

## Video-link intake — October 30, 2026

The existing launcher now accepts a local recording or HTTP(S) video URL. URL setup installs pinned yt-dlp with its default/EJS dependencies and the Deno binary redistribution automatically in the isolated runtime. The downloader selects one media stream, saves original media plus minimal provenance in a new `.source/` directory, and invokes the existing local audio pipeline. No cookies or downloader configuration are imported.

`python tests/test_video_input.py` checks malformed/credential-bearing URL rejection, playlist/live metadata rejection, original-file preservation, provenance output, and offline URL rejection before setup. Downloader behavior in those tests is mocked and is not evidence of site compatibility. Existing installation and library tests pass. The existing offline local-file path also passed a three-second silence regression after adding the URL dependencies, producing zero invented words.

An unavailable YouTube test link returned an explicit failure without creating transcription evidence. Windows/Linux URL execution remains untested; platform/site access restrictions still apply.

A real run starting from the previously supplied YouTube sales-call URL completed the full 2,539.7-second recording: 3,933 estimated words, 463 turns, and delivery measurements in 754.3 seconds of local audio processing (download/setup time separate). The downloaded-media hash matches the evidence source hash; duration and word timestamp bounds passed. The run used cached transcription models but newly installed downloader/Deno dependencies. Automatic diarization produced 133 clusters across the compilation, which must not be interpreted as 133 people. A high-cluster warning was added; speaker identities and transcription accuracy are not independently validated. This is a successful URL/download/transcription integration test, not proof of accurate speaker attribution or coaching quality.
