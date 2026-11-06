# Interview protocol

How the agent interviews the user to build `interviews/`. Interviewing is a session of its own: the agent that interviews does not write resumes in the same session, so the questions serve the fact base and not one target.

## Before the first question

Read `profile.md` for confidential employers and standing decisions, every existing file in `interviews/` so nothing is asked twice, and `docs/positioning.md` so the probing surfaces the evidence hiring managers now weight: judgment and autonomy, demonstrated creative use of AI tools, range across domains, management of agents, and working and deciding in the open.

## Seeding from a prior resume

If the user has a resume, it is read first (from `artifacts/` or pasted in chat) and turned into skeleton interview files: one per role or project, with the title and dates, and each claim under **Facts** marked `[from prior resume, unverified]`. The interview then works through each claim: is it true as written, what is the number behind it, what decision did it take, what did it leave out. A claim the user confirms loses its marker; one they correct is rewritten in their words; one they disown is deleted. Then ask what the resume never mentioned.

## Order

The user's choice; by default most recent role first, then projects, then earlier roles. The user may stop at any point. Save the file for a role as soon as that role is done, not at the end of the session.

## Method

- Plain chat, one to three open questions per turn. Never a questionnaire.
- Structure each story as **CAR**: the Challenge (what was broken, missing or at risk, and for whom), the Action (what the user decided and did, and the alternatives they rejected), the Result (what changed, measured where possible).
- Probe every story for: scope (who it served, how many, how often), the decision that was theirs and what it would have cost to decide otherwise, what would have happened without them, who they influenced or aligned and how, the number, and where AI tools or agents did part of the work and what the user kept for human judgment.
- Ask for the enterprise name of what they did when they describe it in their own words: an intake process is demand management or governance; a merge queue with an admission policy is change control; a workshop series is an enablement program. Record both their words and the standard term.
- Correct sloppy or private vocabulary plainly; the fact base is written in the profession's language.
- When the user names an artifact (a deck, a spec, a report), ask them to drop it in `artifacts/`, then read it and add what it proves to **Facts** with the filename.

## Confidentiality

For an employer `profile.md` marks confidential, record what the user says, mark anything that must stay vague `[generalized]`, and do not push for specifics no resume can carry.

## The file

Copy `_template/interview.md` to `interviews/<employer-or-project>.md`. **Transcript** holds the dated questions and answers, lightly cleaned, the user's wording kept; a later session appends a new dated section. **Facts** holds every claim, number, decision and outcome as a standalone line, one per line, marked `[generalized]` or `[unverified]` where needed. No resume prose in the file. One paragraph per line; no hard wrapping.

## Closing a session

Tell the user which files were written and that they return to their writing session with them.
