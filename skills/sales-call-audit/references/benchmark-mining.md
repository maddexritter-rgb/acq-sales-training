# Learning from a team archive

Use real calls to illustrate and test coaching standards. Do not label every technique in a successful call as a best practice.

## Inventory before bulk download

1. Bootstrap the connector to identify the accessible team and users. Establish retention/coverage instead of assuming access means all-time completeness.
2. Count records and inspect actual platform, disposition, call stage, duration, transcript availability, and recording metadata. Include unanswered attempts in total dials; report them separately from useful conversations.
3. Use bounded time windows for metadata-first retrieval. If a query hits its limit, split the time interval and deduplicate by exact session ID. Verify timestamp units and boundary behavior empirically. Do not claim completeness if a smallest window remains capped. Never silently drop tied timestamps.
4. Select substantive, complete conversations across reps, time periods, offers, and outcomes. Start with a manageable pilot. Fetch complete transcripts only for selected calls; keep raw records private.

## Trellus connector observations

Available tools at build time: `trellus_bootstrap`, `trellus_metric_details`, `trellus_search_sessions`, `trellus_get_session`. Discover their current schemas at runtime.

- `trellus_metric_details` accepts `selects: [{cnf: []}]` and a single `group_by: {column_name: "user_log.disposition"}`. Grouping by platform was also verified. No-date results mean the accessible reporting corpus, not independently verified lifetime coverage.
- Search can return exact session IDs, duration, resource/rep ID, user-log disposition/source, objection flags, turn arrays, privacy flags, and audio-file metadata. Fetch details for source evidence.
- Detailed records use `turnData.starts`, `ends`, `texts`, and `isCustomers`; starts/ends in inspected records are seconds. `wordData` may be empty. Do not assume word-level timing exists.
- In inspected records the disposition source was `DISPOSITION_SOURCE_AI_EVAL`. Treat these labels as machine-generated metadata; verify the dialogue and deal evidence separately.
- Audio uploaded keys are storage references, not automatically playable URLs. Do not invent a download URL from them.
- Phone redaction can also corrupt numeric CRM IDs and occasionally session IDs. Keep redaction on normally. If exact identifiers are required, request only those fields with redaction disabled and retain them privately; do not reproduce contact data in the public package. Never pass a redacted identifier to a detail call.
- Verified filter syntax: `cnf: [[{"column_name":"duration","operator":"GE","value_safe":300}]]`. Outer groups are AND; inner entries are OR. Request time bounds use microseconds; returned `started_at` uses Unix seconds. Search is capped; split capped time windows and deduplicate. Official reference: https://www.trellus.ai/developers/api
- Recording download can require admin or call ownership even when transcripts are readable. Respect that restriction; do not derive storage URLs to bypass it. Offer an exported transcript. Audio ingestion and transcript ingestion have separate test statuses.

## Outcomes and objections

Maintain separate fields for call-stage result and later deal outcome. Verified paid/closed-won status needs the authoritative record, its date, and a reliable contact/deal join. A spoken intention, meeting booked, connected disposition, or positive sentiment is not closed-won. Record refunds/cancellations if available instead of counting every initial commitment as durable success.

For each objection episode retain privately: session ID, rep ID, call stage, offer, source time range, preceding discovery, buyer concern, rep response, immediate buyer reaction, eventual outcome and evidence, and reviewer status. Context is essential: the same sentence can help one buyer and miss another's concern.

Build candidate examples for timing, money, decision-maker, preference/fit, and stalls, with trust/proof as an additional tag. Compare won, lost, and pending calls with similar stage/offer/lead source. Look for counterexamples and missed opportunities in wins. Avoid selecting only strong reps or dramatic objections. These comparisons are observational; they do not establish causation.

Promote examples from `candidate` to `source-verified` to `sales-lead-reviewed` explicitly. Only describe them as outcome-verified when the outcome itself is verified. A representative pilot does not equal an exhaustive archive analysis. Keep held-out calls for evaluating whether the skill finds useful coaching beyond its example bank.
