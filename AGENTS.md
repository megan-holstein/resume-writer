# AGENTS.md — Resume Writer

This folder turns a person's full professional history into resumes targeted at specific jobs. You, the coding agent, run the whole pipeline; the user supplies facts and taste. Read `profile.md` before anything else, then this file. The design and its alternatives: `docs/design.md`.

## Layout

| Path | Role | Tracked? |
|---|---|---|
| `profile.md` | Contact line, constraints (confidential employers, discreet search), standing framing decisions. Every resume reads it. | no |
| `interviews/<employer-or-project>.md` | The fact base: one file per role or project, transcript plus one-fact-per-line **Facts**. Common to every resume. | no |
| `artifacts/` | Where the user drops things in: an existing resume to seed the interviews, and work samples (documents, decks, specs, code, screenshots). You read them to extract facts into `interviews/`, never cite them directly. | no |
| `targets/<target>.md` | One job target, at any specificity: a title, a function, a company, or a pasted posting. | no |
| `resumes/<target>/resume.md` | One resume per target, its rendered PDF beside it, and `versions/` holding every snapshot (`vNN.md`) with a `log.md`. `resumes/base/` is the untargeted resume every targeted one starts from. | no |
| `_template/` | Skeletons for the four file kinds. Copy, never edit in place. | yes |
| `docs/` | `design.md`, `positioning.md` (what hiring now rewards), `interview-protocol.md`. | yes |
| `build_resume.py` | Snapshots a version and renders a resume Markdown to an ATS-safe two-page PDF: `python3 build_resume.py resumes/<target>/resume.md --snapshot "note" --open`. | yes |

Untracked paths are in `.gitignore`: the user's history never enters the public repository. A user who wants it versioned works in a private fork and deletes those lines.

## The pipeline

1. **Profile.** If `profile.md` is missing, copy `_template/profile.md` and fill it with the user in chat.
2. **Seed.** If the user has an existing resume, in any format (PDF, Word, Markdown, or pasted into the chat), read it and create one `interviews/<employer-or-project>.md` per role and project it names, with its title, dates and every claim copied under **Facts** marked `[from prior resume, unverified]`. The seed is the first thing to question, not a fact base: a prior resume is what the user remembered to write once, and the interview exists to go past it. The user drops the file into `artifacts/`; a resume found anywhere in the folder or pasted in chat is treated as a seed.
3. **Interview, in writing.** Follow `docs/interview-protocol.md`: append a round of five to ten questions to `interviews/<employer-or-project>.md` with a blank `**A:**` under each, open the file in the user's editor, and wait. When the user says the round is answered, read it, add every fact to **Facts**, and append the next round. Repeat until a round has no follow-ups and no new ground. One file per role or project. A round serves the fact base, not one target. When the user drops something into `artifacts/`, read it and add what it proves to the relevant interview's **Facts**, marked with the artifact's filename.
4. **Target.** Copy `_template/target.md` to `targets/<target>.md` (kebab-case). If the user gives a posting, paste it verbatim and mine it: list the responsibilities, the must-have skills and the employer's own words for them at the end of the file under **Scorecard**.
5. **Assess fit, honestly.** Before writing, set the target's **Scorecard** against the **Facts** and write the verdict into the target file under **Fit**: what the facts support, what they do not, and how large the gap is. If the user is not qualified for the target as posted, say so plainly, and name the adjacent target on the same career path that the facts do support (the same function one level down, the same level in a less selective employer, the role that leads to this one). The purpose is the user's next good job, not their dream job this week; a resume that overclaims costs them the interview and the reference. The user decides whether to apply anyway; the resume still carries nothing the facts do not.
6. **Draft in two passes** (`docs/writing.md`). Copy `resumes/base/resume.md` (or `_template/resume.md` for the first resume) to `resumes/<target>/resume.md`. **Expansion pass:** write every fact the target rewards, in full, with no regard for length; every bullet traces to a line in `interviews/*/Facts`; nothing is invented, inferred or rounded up. **Compression pass:** a separate agent (a subagent where your harness has them, otherwise a fresh session) is given the draft, `profile.md` and `docs/writing.md` only, and cuts it to two pages, keeping every fact and number and cutting only words; if the facts do not fit it lists what it would drop and you decide. Diff the two to confirm nothing was lost.
7. **Hand the draft to the user before building.** Open `resume.md` in the user's Markdown editor and stop; the user edits the text directly and says when to build. Then read the file back: every edit they made is a decision, so record the ones that generalize in `profile.md` (dated, in their words where possible) before going on. Never build a PDF from a draft the user has not seen.
8. **Build, with a version.** `python3 build_resume.py resumes/<target>/resume.md --snapshot "<what changed and why>"`. The script copies the Markdown to `resumes/<target>/versions/vNN.md`, logs the note in `versions/log.md`, auto-fits to two pages and verifies the PDF text layer. Every build the user might want back is snapshotted; a quick rebuild after a typo fix may skip `--snapshot`. If it warns that content does not fit at the tightest preset, propose trims; never shrink type further and never edit a PDF by hand. **Restore**: when the user prefers an older version, copy `versions/vNN.md` over `resume.md` and build with a snapshot noting the restore; versions are never deleted or edited.
9. **Record.** Append the outcome to the target's **Status**. When the user confirms or overturns a framing decision, write it into `profile.md` the same turn, dated, with their words. No other log is kept.

## Writing rules

- **Honest to the user first.** A gap is reported, not papered over with wording. Strong framing of a true fact is the job; a framing the user could not defend in an interview is not.
- **Facts over activity.** A bullet states a decision or action, its scope and its measured result. Drop implementation detail an employer no longer pays for (the algorithm, the migration steps) unless the target asks for it. `docs/positioning.md` says what hiring managers now weight and why.
- **Dense, truncated bullets.** No filler verbs, no adjectives doing a number's job, few em dashes and colons. One fact per clause.
- **Standard vocabulary.** Name the practice as a job posting or senior colleague would (change control, demand management, governance, release engineering), not in the user's private coinage. Correct the user's wording when it is sloppy; that is part of the job.
- **Active voice; inanimate things do not want.** A system *requires* or *blocks*; an agent *runs*, *generates*, *is prompted*. Never *wants*, *tries*, *understands*.
- **Confidentiality from `profile.md` is absolute.** A fact marked `[generalized]` stays generalized in every resume.
- **The master is Markdown; the PDF is output.** Edit `resume.md`, rerun the script. The user edits the Markdown too; their edits are decisions, not noise. Links render as plain text, headings uppercase, no tables or images: the format exists so strict ATS parsers extract every keyword.

## Markdown rules

One paragraph, one line; never hard-wrap prose. Sub-entries: a header led by italics (`*Role* — dates`) nests under the bold header above it and indents with its bullets.
