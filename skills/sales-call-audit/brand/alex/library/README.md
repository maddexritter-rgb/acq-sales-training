# Coaching library

100 original decision cards across ten modules, distilled after reading all retained text of the supplied handbook and both courses. This is an operational coaching reference, not the paid handbook, a transcript archive, or a claim that every historical teaching should be followed literally.

Read the call first. Identify its job, buyer's actual concern, observed outcome, and strongest competing explanation. Choose one primary intervention and at most two supporting cards. A search hit proposes a candidate; the call must justify using it. In particular, a price mentioned just before a disconnection does not establish a money objection.

| Situation | Read | Useful starting cards |
|---|---|---|
| Wrong call objective, poor context, distraction, bad connection | [Context](01-context.md) | CTX01, CTX04, CTX05 |
| Vague problem, repeated questions, buyer correction | [Discovery](02-discovery.md) | DIS05, DIS06, DIS09 |
| Generic pitch, unclear support, contradictory promises | [Offer](03-offer.md) | OFF01, OFF07, OFF09 |
| Unclear hesitation, stacked rebuttals, refusal | [Objection diagnosis](04-objection-diagnosis.md) | OBJ02, OBJ03, OBJ08, OBJ10 |
| Budget, cash timing, value, previous bad purchase, guarantees | [Money and risk](05-money-risk.md) | MON01, MON03, MON05, MON06 |
| Dates, workload, stakeholders, procurement | [Timing and authority](06-time-authority.md) | TIM01, TIM06, TIM09 |
| Ask, booking, payment status, onboarding, referrals | [Close and handoff](07-close-handoff.md) | CLS01, CLS04, CLS06, CLS08 |
| Dense wording, question stacking, delivery, script changes | [Delivery and script](08-delivery-script.md) | DEL01, DEL03, DEL08 |
| Manager review, drills, ramp, repeated behavior | [Manager practice](09-manager-practice.md) | MGR01, MGR02, MGR04, MGR05 |
| No-shows, follow-up, notes, lead mix, funnel metrics | [Operations](10-funnel-operations.md) | OPS01, OPS02, OPS05, OPS08 |

Each card contains an observable trigger, action, original suggested wording, conditional next move, practice criterion, boundary, and supporting source-section ranges. The ranges support the teaching interpretation; the original example lines and evidence safeguards are this implementation's adaptations, not quotations or claims that the trainer stated every sentence.

For targeted retrieval, run `python3 scripts/find_coaching.py "buyer corrects missing reports"` from the skill folder, or request a known card with `--id DIS06`. `--module 02-discovery` restricts the search. The helper is standard-library Python with no API or downloads. With no Python available, read the relevant Markdown module directly. [cards.json](cards.json) and the Markdown modules contain the same authored cards; JSON exists for retrieval, not a second instruction source.

Before adapting a technique that appears to conflict with another source, read [source distinctions](source-distinctions.md). For complete scripts or uncertain offer claims, use the [offer facts template](offer-facts-template.md); populate it only from the user's evidence. Do not delay a useful first audit to make the user complete a form.

Coverage and exclusions: [coverage.json](coverage.json). Real-call test outputs remain private. The public [example](first-audit.md) is fictional.
