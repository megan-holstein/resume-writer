# Writing a resume: two passes

Dense prose is produced in two passes by two different agents, never in one. The first writes long; the second cuts. One agent doing both in one pass produces the spacious middle: too tidy to be complete, too wordy to be dense.

## Pass 1: the expansion draft

A drafting agent writes `resume.md` with no regard for length. For each role it puts in every fact from `interviews/<role>.md` **Facts** that the target's **Scorecard** rewards, in full sentences, with the scope, the decision, the alternative rejected and the result all present. It orders bullets by what the target weights most (`docs/positioning.md`). It uses the standard vocabulary from the start. It may run to four pages. Its job is completeness and order; it makes no attempt to be brief.

## Pass 2: the compression pass

A second agent, given only `resume.md`, `profile.md` and this file (not the interviews, so it cannot add), rewrites it to two pages. Its brief:

- **Keep every fact, number, name, date and professional term.** Cutting is of words, never of information. If two pages cannot hold every fact, it stops and lists the bullets it would drop, lowest-value first, for the orchestrator to decide; it does not decide alone.
- **Cut filler.** Articles where the sentence still reads without them; `that`, `which`, `in order to`, `the ability to`, `responsible for`, `a variety of`; hedges (`helped`, `supported`, `worked on`); any clause that restates what a number already says; any adjective doing a number's job.
- **Compound the phrases.** `measurement of tool usage before and after` becomes `before-and-after usage measurement`; `a process for taking in and reviewing proposals` becomes `intake and investment review`.
- **One subject per bullet, stated once.** No repeated `I`, no repeated role name, no repeated employer.
- **Targets:** summary at most 90 words and written as prose (it keeps its articles; bullets may drop theirs); a bullet at most 30 words, two lines at the roomiest preset; a skills line at most two lines.
- **Do not change meaning.** No stronger verb, no larger scope, no rounding up. `about half` stays `about half`. A fact marked `[generalized]` in the source stays as vague as it is written.
- **Style stays:** active voice, verb-first bullets, present tense for a current role, past for a past one, no em dashes, no semicolons, colons only before a list.
- Output the full file, nothing else.

## Then

The orchestrator diffs the two passes to confirm no fact was lost, hands the result to the user in their editor (`AGENTS.md` step 7), and builds with a snapshot after the user's edits.
