# Resume Writer

A folder of Markdown files and agent instructions that turns your whole professional history into resumes aimed at specific jobs, run inside your own coding agent (any agent that reads `AGENTS.md`). You are interviewed once, in depth, about every role and project you have held; the facts are kept as plain text you can read and correct. Then, for each job you want, the agent writes a resume from those facts and the job's own words, and a script renders it to a two-page PDF that applicant-tracking systems parse cleanly. You never explain your history twice, and no resume contains a claim that is not in your file.

## How it works

Three kinds of input and one kind of output.

- **`profile.md`**: your contact line, your constraints (a confidential employer, a discreet search) and the framing decisions you have made along the way ("these two roles stay separate", "never list me as a founder"). Every resume reads it.
- **`interviews/`**: one file per role or project. The agent interviews you using the protocol in `docs/interview-protocol.md`, probing each story for the decision you made, the alternatives you rejected, the scope, the measured result and where AI did part of the work. It records the transcript and a list of standalone facts. This is the fact base every resume is written from.
- **`artifacts/`**: drop in your current resume, in any format, and the agent uses it to seed the interviews: one file per role it names, every claim marked as unverified, so the first questions have something to push against. Drop in examples of your work too (a deck, a spec, a report, code, a screenshot); the agent reads them and adds what they prove to your interviews.
- **`targets/`**: one file per job you want, as broad or specific as you know it: a title, a function, a company, or a pasted posting.
- **`resumes/<target>/`**: the output. One Markdown resume per target, plus its PDF, built from `resumes/base/` (your untargeted resume) by reordering and rewriting for the target. A resume that got a response is recorded on its target so the next one learns from it.

## Five-minute start

1. Clone this repository, install Google Chrome (the PDF renderer) and Python 3 with `pypdf` (`pip install pypdf`), and open your coding agent in the folder.
2. Say "set up my profile." The agent copies `_template/profile.md` to `profile.md` and fills it with you.
3. Drop your current resume into `artifacts/` (or paste it into the chat) and say "seed my interviews from it." Then say "interview me about <employer>." Repeat for every role and project, as many sessions as it takes. Drop work samples into `artifacts/` whenever you have them.
4. Say "add a target for <job>." Paste the posting if you have one.
5. Say "write the resume for <target>." The agent first tells you, plainly, how well your facts match the job, and if they do not, which job on the same path they do match: the aim is your next good job, not an application that overclaims. Open `resumes/<target>/<Your_Name>_Resume.pdf`, react, and let the agent revise. Each thing you confirm or reject is written into `profile.md`, so the next resume starts from your decisions.

## Your history stays on your machine

`profile.md`, `interviews/`, `artifacts/`, `targets/` and `resumes/` are in `.gitignore`. The public repository never carries your history, your targets or your resumes. To version them, work in a private fork or clone: make it private first, then delete those lines from `.gitignore`.

## How it differs from pasting a resume into a chatbot

A chatbot rewrites the resume you already have, so it can only rephrase what you remembered to put there, and it forgets you when the window closes. The harness interviews you first, so the facts it writes from include the things you never thought to list, and keeps them in files you own. Every bullet traces to a fact you stated, which is the difference between a tailored resume and an invented one, and the agent tells you when a target is out of reach and what is in reach on the same path, instead of writing you a resume for a job you would not get. Your framing decisions accumulate instead of being re-argued in each chat. And the PDF comes from a script that enforces two pages and checks its own text layer, so what the tracking system reads is what you wrote.

## Documents

- [`docs/design.md`](docs/design.md): the design, the decisions behind it and the alternatives rejected.
- [`docs/positioning.md`](docs/positioning.md): what hiring managers now weight and how the writing rules follow from it, with sources.
- [`docs/interview-protocol.md`](docs/interview-protocol.md): how the interview is run.
- [`AGENTS.md`](AGENTS.md): the rules your coding agent follows.

## License

MIT. See [`LICENSE`](LICENSE).
