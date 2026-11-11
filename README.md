# Resume Writer

A folder you open in your coding agent (Claude Code, Codex, Gemini CLI, or any agent that reads `AGENTS.md`). The agent interviews you about your career, keeps what you tell it as plain text files, and writes you a resume for each job you want, with a PDF ready to upload. You need no programming.

## The idea in one paragraph

Most resumes are written from the last resume, so they only ever get shorter and vaguer. Here the agent first interviews you in depth about every job and project you have had and saves the answers as a list of facts. Then, for each job you apply to, it writes a fresh resume from those facts and from the job posting. Getting that detail out of you is the main thing the harness does: the agent comes back with more questions whenever a line could be stronger with a number or a fact it does not have. Every line on the resume comes from something you actually said. The facts are written once; the resumes are written as many times as you need.

## What you do, step by step

**1. Set up.** Clone this repository. Install Google Chrome (it renders the PDF) and Python 3 with the `pypdf` package (`pip install pypdf`). Open your coding agent in the folder.

**2. Tell the agent who you are.** Say *"set up my profile."* It asks for your contact details and anything it must respect: that you are job-hunting while employed, that an employer is confidential, and so on. This goes in `profile.md`.

**3. Give it your old resume.** Drag your current resume (PDF, Word, anything) into the `artifacts/` folder, or paste it into the chat, and say *"seed my interviews from it."* The agent makes one file per job in `interviews/`, with every claim from your resume marked "unverified." This gives the interview something to start from.

**4. Get interviewed, in writing.** Say *"interview me about <employer>."* The agent writes five to ten questions into `interviews/<employer>.md`, each with a blank space for your answer, and opens the file. You answer in your editor, in as many words as you like (write `skip` to pass), and tell the agent you are done. It reads your answers, records the facts, and writes the next round of questions: follow-ups on what you said, then new ground. Rounds continue until it has nothing left to ask. Answer when you have time, over days if you want; the file is the record. Drop examples of your work (a deck, a report, a spec) into `artifacts/` and the agent reads them for more facts.

**5. Name a job you want.** Say *"add a target for <job>."* It can be as vague as "AI strategy roles at banks" or as exact as a posting you paste in. This goes in `targets/<job>.md`.

**6. Get the honest verdict.** Before writing anything, the agent compares the job's requirements with your facts and tells you plainly whether you are a fit. If you are not, it says so, and names the job on the same path that you are a fit for (one level down, a less selective employer, the role that leads to this one). The goal is your next good job, not an application that overclaims. You decide whether to go ahead.

**7. Read and edit the draft.** Say *"write the resume for <job>."* The agent writes `resumes/<job>/resume.md` in two passes, a long draft with every relevant fact and then a cut by a second agent that removes words but never facts, and opens it in your editor, as plain text, before any PDF exists. Change whatever you want directly in the file, then say *"build."* The agent reads your edits, saves the decisions behind them to `profile.md` so the next resume starts from them, and builds the PDF next to the file.

**8. Every build is a version.** Each time the agent builds, it first copies the Markdown to `resumes/<job>/versions/v01.md`, `v02.md`, … and writes a line in `versions/log.md` saying what changed. If you liked an earlier one better, say *"go back to v02"* and it becomes the current resume (as a new version, so nothing is ever lost).

**9. Repeat steps 5 to 8 for every job.** The interviews are shared, so the second resume takes minutes.

## The folders

| Folder or file | What goes there | Who writes it |
|---|---|---|
| `profile.md` | Your contact line, your constraints, your standing decisions | The agent, from what you say |
| `interviews/` | One file per job or project: the interview and the facts it produced | The agent, from what you say |
| `artifacts/` | Your old resume and examples of your work | You drop them in |
| `targets/` | One file per job you want: the posting, the fit verdict, what happened | The agent, from what you say |
| `resumes/` | One folder per target with the resume, its PDF and a `versions/` history; `base/` is the untargeted version | The agent, then you edit |
| `_template/`, `docs/`, `AGENTS.md`, `build_resume.py` | The method itself | Already written; do not edit |

## Your information stays private

Everything about you (`profile.md`, `interviews/`, `artifacts/`, `targets/`, `resumes/`) is listed in `.gitignore`, so if you push this repository nothing about you goes with it. If you want your own copy versioned, make a private fork and delete those lines from `.gitignore`.

## Why not just ask a chatbot?

A chatbot rewrites the resume you paste, so it can only rephrase what you already remembered to write, and it forgets you when you close the window. Here the agent asks first, so the facts include things you never thought to list; it keeps them in files you own and can edit; it refuses to put anything on the resume you did not say; it hands you the text to edit before it makes a PDF, and keeps every version so you can go back; and it tells you when a job is out of reach rather than writing a resume that will not get an interview.

## More

- [`docs/positioning.md`](docs/positioning.md): what hiring managers now look for and why the resumes are written the way they are, with sources.
- [`docs/style-guide.md`](docs/style-guide.md): the style rules every resume follows (industry terms, no invented phrases, state the good and leave the qualifying to the interview, a number in every bullet, verb-first, no colons).
- [`docs/interview-protocol.md`](docs/interview-protocol.md): how the interview is run.
- [`docs/design.md`](docs/design.md): the design decisions and the alternatives rejected.
- [`AGENTS.md`](AGENTS.md): the rules the agent follows.

## License

MIT. See [`LICENSE`](LICENSE).
