# AGENTS.md — Resume Writer

This folder turns a person's full professional history into resumes targeted at specific jobs. You, the coding agent, run the whole pipeline; the user supplies facts and taste. Read `profile.md` before anything else, then this file. The design and its alternatives: `docs/design.md`.

## The first goal: solicit detail

**Getting detail out of the user is the biggest goal of this harness, ahead of any one resume.** A resume can only be as strong as the fact base under it, and the user has always done more than they have written down. So interview at any point where more information could help, not only at step 3:

- When a bullet has no number, no scope or no result, and the user asks for it to be stronger, the answer is a round of questions, not better wording.
- When the user mentions something new in passing (a project adopted, a figure, a tool, a decision), record it in **Facts** and ask what else stands behind it.
- When a target rewards something the facts barely cover, ask before concluding the user lacks it.
- When editing reveals a claim the facts do not support, ask instead of softening or dropping it.

Open a round without waiting to be asked, say which file to answer, and keep working on what does not depend on the answers. Never fill a gap by guessing, inferring or rounding up.

## Layout

| Path | Role | Tracked? |
|---|---|---|
| `profile.md` | Contact line, constraints (confidential employers, discreet search), standing framing decisions. Every resume reads it. | no |
| `interviews/<employer-or-project>.md` | The fact base: one file per role or project, transcript plus one-fact-per-line **Facts**. Common to every resume. | no |
| `artifacts/` | Where the user drops things in: an existing resume to seed the interviews, and work samples (documents, decks, specs, code, screenshots). You read them to extract facts into `interviews/`, never cite them directly. | no |
| `targets/<target>.md` | One job target, at any specificity: a title, a function, a company, or a pasted posting. | no |
| `resumes/<target>/resume.md` | One resume per target, its rendered PDF beside it, and `versions/` holding every snapshot (`vNN.md`) with a `log.md`. `resumes/base/` is the untargeted resume every targeted one starts from. | no |
| `_template/` | Skeletons for the four file kinds. Copy, never edit in place. | yes |
| `docs/` | `design.md`, `positioning.md` (what hiring now rewards), `interview-protocol.md`, `writing.md` (the two drafting passes), `style-guide.md` (the rules every resume holds to). | yes |
| `build_resume.py` | Snapshots a version and renders a resume Markdown to an ATS-safe PDF auto-fitted to the page limit, with the user's format choices from `profile.md` (`--pages N`, default 2; `--font`, default Helvetica; `--divider` for the contact-line symbol): `python3 build_resume.py resumes/<target>/resume.md --pages N --font NAME --snapshot "note" --open`. | yes |

Untracked paths are in `.gitignore`: the user's history never enters the public repository. A user who wants it versioned works in a private fork and deletes those lines.

## The pipeline

1. **Profile.** If `profile.md` is missing, copy `_template/profile.md` and fill it with the user in chat.
2. **Seed.** If the user has an existing resume, in any format (PDF, Word, Markdown, or pasted into the chat), read it and create one `interviews/<employer-or-project>.md` per role and project it names, with its title, dates and every claim copied under **Facts** marked `[from prior resume, unverified]`. The seed is the first thing to question, not a fact base: a prior resume is what the user remembered to write once, and the interview exists to go past it. The user drops the file into `artifacts/`; a resume found anywhere in the folder or pasted in chat is treated as a seed.
3. **Interview, in writing.** Follow `docs/interview-protocol.md`: append a round of five to ten questions to `interviews/<employer-or-project>.md` with a blank `**A:**` under each, open the file in the user's editor, and wait. When the user says the round is answered, read it, add every fact to **Facts**, and append the next round. Repeat until a round has no follow-ups and no new ground. One file per role or project. A round serves the fact base, not one target. When the user drops something into `artifacts/`, read it and add what it proves to the relevant interview's **Facts**, marked with the artifact's filename.
4. **Target.** Copy `_template/target.md` to `targets/<target>.md` (kebab-case). If the user gives a posting, paste it verbatim and mine it: list the responsibilities, the must-have skills and the employer's own words for them at the end of the file under **Scorecard**.
5. **Assess fit, honestly.** Before writing, set the target's **Scorecard** against the **Facts** and write the verdict into the target file under **Fit**: what the facts support, what they do not, and how large the gap is. If the user is not qualified for the target as posted, say so plainly, and name the adjacent target on the same career path that the facts do support (the same function one level down, the same level in a less selective employer, the role that leads to this one). The purpose is the user's next good job, not their dream job this week; a resume that overclaims costs them the interview and the reference. The user decides whether to apply anyway; the resume still carries nothing the facts do not.
6. **Draft in two passes** (`docs/writing.md`), sections in this order: education, experience and projects first, then skills derived from them, then the summary last. Copy `resumes/base/resume.md` (or `_template/resume.md` for the first resume) to `resumes/<target>/resume.md`. **Expansion pass:** write every fact the target rewards, in full, with no regard for length; every bullet traces to a line in `interviews/*/Facts`; nothing is invented, inferred or rounded up. **Compression pass:** a separate agent (a subagent where your harness has them, otherwise a fresh session) is given the draft, `profile.md`, `docs/writing.md` and `docs/style-guide.md` only, and cuts it to the page limit in `profile.md` (two pages unless it says otherwise), keeping every fact and number and cutting only words; if the facts do not fit it lists what it would drop and you decide. Diff the two to confirm nothing was lost.
7. **Hand the draft to the user before building.** Open `resume.md` in the user's Markdown editor and stop; the user edits the text directly and says when to build. Then read the file back: every edit they made is a decision, so record the ones that generalize in `profile.md` (dated, in their words where possible) before going on. Never build a PDF from a draft the user has not seen.
8. **Build, with a version.** `python3 build_resume.py resumes/<target>/resume.md --pages N --snapshot "<what changed and why>"`, with `N` the page limit from `profile.md` (or the target file, where a target overrides it), plus `--font` and `--divider` when `profile.md` sets them; omit any of them for the defaults (two pages, Helvetica, the divider the Markdown already uses). The script warns if the chosen font is not installed and Chrome substituted another; tell the user rather than ship the fallback. The script copies the Markdown to `resumes/<target>/versions/vNN.md`, logs the note in `versions/log.md`, auto-fits to the page limit and verifies the PDF text layer. Every build the user might want back is snapshotted; a quick rebuild after a typo fix may skip `--snapshot`. If it warns that content does not fit at the tightest preset, propose trims; never shrink type further and never edit a PDF by hand. **Restore**: when the user prefers an older version, copy `versions/vNN.md` over `resume.md` and build with a snapshot noting the restore; versions are never deleted or edited.
9. **Record.** Append the outcome to the target's **Status**. When the user confirms or overturns a framing decision, write it into `profile.md` the same turn, dated, with their words. No other log is kept.

## Writing rules

The full rules, with examples, are in `docs/style-guide.md`; they hold for every user and every resume. In short:

- **Honest to the user first.** A gap is reported, not papered over with wording. Strong framing of a true fact is the job; a framing the user could not defend in an interview is not.
- **Facts over activity.** A bullet states a decision or action, its scope and its measured result. Drop implementation detail an employer no longer pays for (the algorithm, the migration steps) unless the target asks for it. `docs/positioning.md` says what hiring managers now weight and why.
- **Dense, truncated bullets.** No filler verbs, no adjectives doing a number's job, no semicolons anywhere, no colons in a bullet or the summary, few em dashes. One fact per clause.
- **Standard vocabulary, even where the user never used the word.** Name the practice as a job posting or senior colleague would (change control, demand management, governance, release engineering), not in the user's private coinage or plain description. The fact must show the practice was done; the user need not have known its name. Correct the user's wording when it is sloppy; that is part of the job.
- **No invented phrases.** Headers, group labels and skill entries are phrases postings and resumes in the field already use; a label coined to carry a nuance is replaced by the nearest conventional one.
- **Say the good.** A bullet states the claim at its true scale, with a number wherever the facts hold one, and carries no hedge, caveat or account of how the number was reached; qualifications stay in the interview file.
- **Verb-first, no "I".** Every bullet opens with an action verb: present tense for ongoing work in a current role, past for everything finished.
- **Active voice; inanimate things do not want.** A system *requires* or *blocks*; an agent *runs*, *generates*, *is prompted*. Never *wants*, *tries*, *understands*.
- **Confidentiality from `profile.md` is absolute.** A fact marked `[generalized]` stays generalized in every resume.
- **The master is Markdown; the PDF is output.** Edit `resume.md`, rerun the script. The user edits the Markdown too; their edits are decisions, not noise. Links render as plain text, headings uppercase, no tables or images: the format exists so strict ATS parsers extract every keyword.

## Markdown rules

One paragraph, one line; never hard-wrap prose. Sub-entries: a header led by italics (`*Role* — dates`) nests under the bold header above it and indents with its bullets.
