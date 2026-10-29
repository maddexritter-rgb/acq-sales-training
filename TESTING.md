# Release checks

Automated checks cover project installation for Claude Code and Codex, repeated installation, preservation of an existing modified skill, bundled profile portability, and relative reference integrity. Run `python tests/test_install.py`. These package checks ran locally. Automated GitHub Actions checks are not enabled because the current GitHub connection lacks workflow write permission; cross-platform checks remain pending.

Local Apple Silicon audio validation processed two public call excerpts (106 and 137 seconds). A cached run completed with network socket connections blocked. Known-pitch and gap fixtures passed; a silent recording produced no invented words. The repository launcher was additionally tested with PATH restricted to system tools, so it downloaded its own uv and Python before processing real audio. The package resolver reused its download cache; this was not a clean operating-system image.

Remaining validation: independent fresh Claude Code/Codex sessions from the published URL, Windows/Linux audio execution, multilingual and long-call accuracy, and independent human review of coaching. First-run execution is automated, but neither instant processing nor universally prompt-free installation is claimed.

Integration references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [uv installer options](https://docs.astral.sh/uv/reference/installer/).

## Coaching expansion validation

The coaching lab adds ten original worked scenarios and an interactive practice loop. Five fictional behavioral cases are supplied in [evaluations/coaching-cases.md](evaluations/coaching-cases.md). They are evaluation prompts with criteria, not claimed automated passes. Three real transcript moments were re-read and used for owner-local, author-reviewed feedback examples: corrected reporting premise, missed training-process follow-up, and an assumed missing roadmap. No private call transcript or real-case output was added to this repository. Independent fresh-session model evaluation remains pending.
