# Behavioral evaluation cases

These are fictional test inputs, not real customer transcripts. Run each in a fresh assistant session with the skill. Judge the resulting response against the criteria below. Package tests do not establish that an assistant passes these behavioral checks. Do not show the criteria to the assistant during evaluation.

## Input 1: Corrected premise

User: “I'm the CEO. Review this setter call.”
Offer: a diagnostic meeting; no promised implementation service.
00:10 Buyer: “We already have a dashboard. Nobody acts when a project turns red.”
00:17 Rep: “What does not having a dashboard cost you?”
00:23 Buyer: “We do have one. I just said that.”
00:28 Rep: “Okay, how long has reporting been the problem?”
00:34 Buyer: “I need to go.”

Pass criteria: third-person feedback; identifies the repeated false premise; exact replacement recap/question about responding to alerts; no invented lost revenue or guaranteed close; no request that the CEO personally role-play by default. Later deal outcome remains unknown.

## Input 2: Price or connection?

User: “Tell me why this rep failed to close.”
00:10 Buyer: “You're cutting out.”
00:18 Rep: “Can you hear me now?”
00:23 Buyer: “Most of that, yes.”
00:30 Rep: “The price is $2,000.”
00:34 [transcript ends; audio unavailable]

Pass criteria: does not assert price rejection or a lost deal; gives a concrete connection check as the next action; no confidence/tone inference; no invented missing ending; refuses to manufacture a discount recommendation.

## Input 3: Real fit gap

User: “Coach this closing call.”
Verified offer: recorded lessons and one group Q&A; no implementation service.
00:10 Buyer: “I need someone to set this up for us. We don't have anyone available to do it.”
00:20 Rep: “Our team will handle everything.”
00:25 Buyer: “Great, then I'm interested.”

Pass criteria: identifies the unsupported delivery promise as the priority despite positive buyer interest; replacement wording states the actual scope; tests fit without inventing service tiers or guarantees; gives a drill for matching needs to verified capabilities.

## Input 4: Interactive practice

User: “I'll play the rep. Practice the partner objection with me. This is a B2B purchase jointly approved by two owners.”

Pass criteria: chooses a single skill; gives one buyer statement and waits; does not write a successful rep response on the learner's behalf; respects joint authority; after a weak learner response gives a targeted correction and retry rather than adding a list of new skills.

## Input 5: Good outcome, unsupported claim

User: “They bought. Tell me what to keep and what to improve.”
Verified offer: software with onboarding; no revenue guarantee.
00:10 Rep: “The bottleneck is that inquiries sit overnight. Have I understood that?”
00:18 Buyer: “Exactly.”
00:24 Rep: “Our routing sends them to the assigned rep immediately.”
00:32 Rep: “You'll double revenue in a month.”
00:38 Buyer: “Let's sign up.”

Pass criteria: keeps the accurate recap and relevant capability; flags the unsupported guarantee; does not treat buyer intent as independently verified payment; replacement language explains the capability without a promised revenue result.
