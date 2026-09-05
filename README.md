# Placement Prep Agent

A quiz agent for campus placement prep (DSA + aptitude) that actually
remembers what you're weak on — across sessions, not just within one
chat window — and targets those topics next time instead of asking
generic questions every run.

Built as a weekend project to explore long-term memory in LLM agents
(the "does it remember me tomorrow" problem, not the "does it remember
5 messages ago" problem).

## The idea

Most quiz/practice tools either ask random questions every time, or
rely on you manually tracking your own weak spots in a notes app. This
does the tracking for you: after every session it looks at how you did
per topic, updates a persistent status (`weak` / `solid`), and the
*next* session opens by targeting whatever's still flagged weak —
without you telling it what to focus on.

The demo that actually shows this: run a session, get flagged weak on
a topic, close the terminal, come back later, run it again — it opens
on that exact topic instead of a random one.

## How it works

```
you answer  ->  Groq grades it  ->  logged to SQLite  ->  Groq classifies
                                                            weak/solid
                                                                |
                                                                v
next session reads current weak topics  <-----------------------
```

Three separate pieces, kept deliberately separate rather than one big
prompt, so each is easy to reason about and debug on its own:

- **`memory.py`** — the persistence layer. Two SQLite tables: `topics`
  (current status per topic) and `sessions` (full history of every
  question asked). This is the actual "long-term memory" — a plain
  relational table, not a vector DB. The memory here is structured
  state (topic -> status), not free-text conversation history that
  needs semantic search, so a table is the simpler, more auditable
  tool for the job.
- **`llm.py`** — all Groq calls, three of them, each doing one job:
  generate a question, grade an answer (LLM-as-judge, so "42",
  "42.0", and "the answer is 42" all count as correct), and classify
  a topic as weak/solid from a batch of results.
- **`quiz.py`** — the loop: pick the weakest topic -> ask -> grade ->
  log -> update memory. Also seeded with a real starting topic map
  (DSA, Quant, Reasoning, Verbal) so it's usable immediately, not an
  empty shell.
- **`progress.py`** — read-only view of what the agent currently
  believes about you, for checking the memory actually updated.

## Setup

```bash
git clone <this-repo>
cd placement-prep-agent
pip install -r requirements.txt
export GROQ_API_KEY=your-key-here   # free key: console.groq.com/keys
```

## Usage

```bash
python quiz.py       # run a 3-question session
python progress.py   # view current weak/solid map without running a session
```

Nothing resets between runs — `prep_agent.db` persists on disk, so the
second run picks up exactly where the first left off.

## Design decisions worth calling out

- **SQLite over a vector DB / Mem0-style framework** — the memory
  here is structured facts (topic, status, timestamp), not
  unstructured text that needs embedding + semantic retrieval. Adding
  a vector store would be solving a problem this project doesn't have.
- **Three separate LLM calls over one mega-prompt** — generation,
  grading, and status-extraction are different jobs with different
  failure modes. Keeping them separate means a bad grading call
  doesn't silently corrupt question generation, and each is testable
  on its own.
- **LLM-as-judge for grading** — a plain string match would reject
  correct answers that are just formatted differently. The tradeoff
  is the grader can itself be wrong, so this is a place worth manual
  spot-checking rather than trusting blindly.

## What's next

- Timed mode — flag *correct but slow* answers as a separate weak
  signal, since speed under exam pressure is its own skill.
- A small Streamlit front end for a shareable link instead of a
  terminal-only demo.
- A weak -> solid progress chart across sessions.
- A deliberate test where a weak topic is fixed mid-testing, to
  confirm the memory update reflects the fix instead of getting stuck
  on stale status — the real failure mode any memory system has to
  prove it doesn't have.