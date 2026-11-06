# Interview protocol

How the agent interviews the user to build `interviews/`. The interview is written, not spoken: the agent writes questions into the interview file with a blank answer space under each, the user answers in their own editor at their own pace, and the agent reads the answers, extracts facts and writes the next round of questions. This builds the record as it goes and costs almost no tokens, because the agent reads and writes a file once per round instead of holding a conversation.

## Before the first round

Read `profile.md` for confidential employers and standing decisions, every existing file in `interviews/` so nothing is asked twice, and `docs/positioning.md` so the questions surface the evidence hiring managers now weight: judgment and autonomy, demonstrated creative use of AI tools, range across domains, management of agents, and working and deciding in the open.

## Seeding from a prior resume

If the user has a resume, it is read first (from `artifacts/` or pasted in chat) and turned into skeleton interview files: one per role or project, with the title and dates, and each claim under **Facts** marked `[from prior resume, unverified]`. Round 1 then asks about each claim: is it true as written, what is the number behind it, what decision did it take, what did it leave out. A claim the user confirms loses its marker; one they correct is rewritten in their words; one they disown is deleted. Later rounds ask what the resume never mentioned.

## A round

1. The agent copies `_template/interview.md` to `interviews/<employer-or-project>.md` if it does not exist, and appends a `### Round N (YYYY-MM-DD)` section under **Transcript** with five to ten questions. Each question is followed by a line reading `**A:**` and a blank line for the answer. The agent opens the file in the user's Markdown editor and says which file to answer.
2. The user answers in the file, in as many sentences as they like, skipping any question with `skip`. They tell the agent when the round is done.
3. The agent reads the answers, adds every claim, number, decision and outcome to **Facts** (one per line, in the user's words where given, marked `[generalized]` or `[unverified]` as needed), and writes the next round: follow-ups on what the answers opened, then new ground. A round with no follow-ups and no new ground closes the interview for that role; the agent says so.

Questions are open and specific. Structure each story as **CAR**: the Challenge (what was broken, missing or at risk, and for whom), the Action (what the user decided and did, and the alternatives they rejected), the Result (what changed, measured where possible). Probe for scope (who it served, how many, how often), the decision that was theirs and what it would have cost to decide otherwise, what would have happened without them, who they influenced and how, the number, and where AI tools or agents did part of the work and what the user kept for human judgment. When the user describes a practice in their own words, the next round asks whether the standard name fits (an intake process is demand management or governance; a merge queue with an admission policy is change control; a workshop series is an enablement program) and records both.

## Rules

- Take the user's word. When they confirm a claim already on a resume, record it and move on; do not ask for its source. Record their opinions in the transcript, and build no question or resume material on an opinion unless they offer it as resume material. Probing is for new stories, not for re-auditing the user.
- Correct sloppy or private vocabulary plainly in the **Facts**; the fact base is written in the profession's language.
- For an employer `profile.md` marks confidential, mark anything that must stay vague `[generalized]` and do not ask for specifics no resume can carry.
- When the user names an artifact (a deck, a spec, a report), the next round asks them to drop it in `artifacts/`; the agent reads it and adds what it proves to **Facts** with the filename.
- Interviewing and writing stay separate: a round is written to serve the fact base, not one target.
- One paragraph per line; no hard wrapping. Never rewrite an earlier round; append.
