---
name: course-notes
description:
  Turn photos or screenshots of a student's course notes (handwritten or typed)
  into detailed, source-checked study notes as a typeset PDF that anyone taking
  the course can use. The notes decide what is covered and emphasised; the book
  itself is standalone, cited to the course's slides, textbook and papers, never
  quoting or mentioning the original notes; the depth adapts to the reader's
  familiarity (1–5), down to a background part that teaches whatever a beginner
  is missing (the math, the science, the history or the vocabulary the course
  builds on); common mistakes are called out; the hard topics are worked through
  with computed examples; self-check questions close each lecture. Use this
  whenever someone shares photos of lecture notes, asks to expand, clean up,
  fill in or check their notes, wants study notes or a study guide from their
  notes, or asks what they missed in a lecture, even if they never say "course
  notes".
---

# Course notes

You are turning a student's notes from one lecture into the study notes anyone
in the course would want: the whole lecture in its own order, with the hard
parts explained properly. The student's pages are the **input**, not the
content. They tell you what the lecture said, which parts the student found
hard, and which misreadings are plausible. The book is written for any reader
and never quotes, mentions or addresses the original notes or their author.

> **Never add from memory.** Every fact cites the course's own material first:
> the lecture's slides, then the course textbook or study guide, then the papers
> the lecture teaches.

The output is a Letter-size PDF in the house style of the technical-manual kit
(cream paper, Manrope / Source Sans / Source Serif italic / JetBrains Mono):
cited body text, focus callouts for the hard topics, "Common mistake" callouts,
and pointers forward. One lecture is one part; the book grows over the term.

What stays private: the transcript, the gap ledger and the questions about the
student's own pages live in `research/` and in the conversation, not in the
book.

## Files in this skill

| Path                          | Read when                                                                                                                                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/transcription.md` | Before reading the photos. Line-by-line transcription, conventions, uncertainty, diagrams, the coverage table.                                                                                                    |
| `references/levels.md`        | In step 0 and before writing. The 1–5 familiarity scale: how to ask, what each level changes, finding prerequisites, writing for beginners.                                                                       |
| `references/gaps.md`          | After transcription. How to align notes with the slides, the kinds of gap, the gap ledger, what to ask the student.                                                                                               |
| `references/markup.md`        | Before writing. The note layers, callouts, figures, data binding, figure generators.                                                                                                                              |
| `references/example/`         | Before writing your first lecture. CME 295 Lecture 1: gap ledger, sources, check script, figures and the finished standalone fragments (the student's photos and transcript are not included). It builds cleanly. |
| `assets/kit/`                 | Copied into the workspace: stylesheet, build script, figure generators.                                                                                                                                           |

## Prerequisites

Check these before step 1, and ask the user to install anything missing before
the work starts.

| Tool                  | Used for                                           | Check                         | Install                                                                 |
| --------------------- | -------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| Node.js 18+ and `npm` | the kit's build (`kit/build.mjs`)                  | `node --version`              | https://nodejs.org or a version manager                                 |
| Chromium              | Paged.js typesetting and PDF output                | the example build (see Build) | `npx playwright-core install chromium` in the kit folder, or Chrome     |
| `pdftoppm` (Poppler)  | page images (`--png`) for the page check in step 7 | `command -v pdftoppm`         | macOS `brew install poppler`; Debian/Ubuntu `apt install poppler-utils` |
| Python 3 with `numpy` | check scripts and figure generators                | `python3 -c "import numpy"`   | `pip install numpy`                                                     |

Without `pdftoppm` the build still writes the PDF but skips the page images, so
the pages cannot be looked at. If the user declines to install it, say in the
hand-over that the pages were not checked.

## Workflow

### 0. The course (once per course)

Settle, from the request or by asking (one question at a time):

- **Course and term**, e.g. "Stanford CME 295, fall 2026". The term decides
  which slide deck is the right one; courses revise slides every year.
- **Which lecture** the photos are from, and its date.
- **What the student finds hard.** Ask if they have not said. These become
  _focus_ topics: they get worked examples, a focus callout and self-check
  questions. This is the most valuable thing to know.
- **Familiarity, 1 to 5.** Ask with the scale written out
  (`references/levels.md`): 1 new to the subject and what it builds on, 3
  comfortable with the background but new to the topic, 5 a dense review. It
  decides how much the book teaches around each idea, including whether it opens
  with a Background part on the prerequisites. Ask too whether any hard topic
  sits lower than the rest.
- **Where the materials are.** Find them yourself first: search for the course
  website and syllabus, then the posted slides, the course's own study guide or
  cheatsheet, and the paper a lecture is built on. Confirm the site you found
  with the student ("Is this the course: cme295.stanford.edu, fall 2026?")
  before relying on it. Ask for a link or an upload only when nothing public
  turns up, or the materials sit behind a login or a paywall (Canvas, Ed, a
  textbook). If there are no slides at all, ask what the lecture followed (a
  textbook chapter, a recording) and cite that.

Record the answers once in `research/COURSE.md`, headed
`# <Course> · <School> · <term>` (course, term, website, syllabus, lecture list
with dates, familiarity level, focus topics, lectures done) so later lectures
skip these questions (in a new conversation, use what the conversation or memory
already holds about the course before asking again); ask only for the new
lecture's number, what was hard in it, and whether the last book's level felt
right.

### 1. Transcribe

Read `references/transcription.md`, then transcribe every photo into
`research/transcription/transcript.md`, line by line, with page and line
numbers. Keep spelling, abbreviations and struck-out words. Describe each
diagram in words. Mark every reading you are not sure of, and say whether the
doubt changes the meaning. Finish with a coverage table: the lecture's topics by
slide range against what the notes cover.

### 2. Gather the sources

Get the lecture's slides for the student's term and read all of them, recording
slide numbers; the slide number is the citation the student can check. Get the
course study guide or cheatsheet and the paper(s) the lecture teaches. Record
each with its version in `research/SOURCES.md`. If the shell cannot download a
file, read it through the browser or a fetch tool; never fall back to memory for
what the slides say.

### 3. The gap ledger

Write `research/GAPS.md` by walking the slides against the transcript
(`references/gaps.md`): what is **missing**, what is **thin**, what needs a
**fix**, and what you must **ask** because only the student knows. Tie each row
to a source and to the section of the book that will handle it. Missing and thin
rows become ordinary sections; fix rows become "Common mistake" callouts; ask
rows are asked in the conversation and never printed.

### 4. The check kit

Skip this step when the lecture has nothing to compute (a history or literature
lecture); its worked examples come from cited cases, documents and timelines
instead.

For anything computable in the lecture (a formula, a worked example, an
algorithm's steps, sizes of a model, a probability), write a small script in
`research/check/` that computes it and saves JSON to `research/captures/`. The
notes bind to those numbers, so they are computed, not recalled. Toy examples
are fine and often clearer than real ones; label them toy, and say how they
differ from the real thing.

### 5. Write

Write at the reader's level (`references/levels.md`). At levels 1–3, first list
the lecture's prerequisites in `research/PREREQS.md` and write the Background
sections the level needs, with their own check script; at levels 1–2 every
formula or formal statement gets an "In plain words" reading and every new term
is defined where it first appears. Set `"level"` in `manual.json`; the build
checks the rules for that level.

One file per lecture. Follow the lecture's own order and cover the whole
lecture. For each topic:

1. **A section** with a title, an italic deck that states the point, and a lede
   that says what the section does.
2. **The content**: what the slides say, cited by slide; formulas from the
   slides or paper; a figure. When the student sketched a slide's figure, redraw
   that slide's figure with real or computed values, and cite the slide.
3. **Common mistakes** in a `.callout.fix` labelled "Common mistake": state the
   plausible wrong reading in general terms (never as a quote from the notes),
   say what the source says, and cite it. The student's own errors are the best
   guide to which mistakes are worth a callout.
4. **Focus topics** (the ones the student found hard) get a `.callout.focus`
   with the whole idea in two or three sentences, a worked example from the
   check kit, and a step-by-step walk-through.
5. **Where this goes next**: one line pointing to the later lecture that builds
   on the point.

Topics the student's pages skip get the same treatment as the rest, scaled to
the lecture's emphasis; a long stretch of slides can be one short summary
section. Never say which parts the notes covered.

### 6. Reference

The Reference part holds, cumulatively across lectures: self-check questions and
answers, formulas and sizes, a glossary, open questions the slides leave
unresolved (for office hours), sources and versions, and an index of figures.
The front matter maps the lecture's slide ranges to sections.

### 7. Build, look, ask

Build, fix every problem, look at every page. Then send the student the PDF and,
in the conversation, the first open question about their pages from the ledger,
one at a time. When they answer, update the transcript and the notes, and
rebuild.

### Next lecture

Add a part to the same book and a folder `research/lecture-N/`. Keep the
glossary and formula sheet cumulative. When a later lecture revisits a topic,
cross-reference the earlier section instead of repeating it.

## Voice

Write like a good TA writing study notes for the whole class: direct, specific,
warm without padding.

- No second person and no reference to the source notes: no "you wrote", "your
  notes", "not in the notes", "the handwritten pages". The book reads as if
  written from the lecture alone.
- Lead with the idea, then the mechanism, then a number. "Three quarters of the
  attention goes to 'cute'" beats "attention is distributed".
- Quote the slide when its wording is the point.
- When a common reading is wrong, say what the source says; do not soften it
  into vagueness.
- No hype, no filler, no "simply", no "obviously". A student who struggles with
  a topic needs the steps, not reassurance.

## Grounding rules

1. The transcript records the student's words exactly. A misreading is fixed in
   the transcript.
2. Every expansion carries a `<cite>`: `slide 62`, `L2 slide 20`,
   `Vaswani §3.2.1`, `cheatsheet`. Every section ends with a Sources line. The
   build refuses a common-mistake callout without a cite.
3. The slides of the student's term outrank everything else; a paper outranks
   the web; the web is context only. When the slides and a paper differ, say so.
4. Computed numbers come from the check kit and are bound with `data-value`. Toy
   numbers are labelled toy.
5. What could not be checked (the recording, a paywalled book) is listed under
   "Not checked".

## Build

```bash
cp -r "<this skill's folder>/assets/kit" kit
(cd kit && npm install)                    # pagedjs, fonts, highlight.js, playwright-core
python3 research/check/<script>.py         # captures first
python3 research/figs/make.py              # then figures from the captures
node kit/build.mjs . --png                 # -> <slug>-Course-Notes.pdf and build/pages/*.png
```

`manual.json` sets `"kind": "Course Notes"` so the cover and footers say so. To
check the install, copy `references/example` beside the kit and build it: 35
pages, no problems. The build needs a Chromium; it tries Playwright's, then
`PLAYWRIGHT_BROWSERS_PATH`, `CHROME_PATH` and common install paths.

The build reports missing sources, uncited common-mistake callouts, broken
bindings and references, and layout problems.

## Before you hand it over

- Every line of every photo appears in the transcript.
- Every uncertain reading that changes the meaning is an open question for the
  student, asked in the conversation.
- The book has no "you", "your", quotes from the notes, or mention of them; grep
  for it.
- Every focus topic has a worked example, a walk-through and a self-check
  question.
- The book meets its level: at 1–2, every prerequisite in `research/PREREQS.md`
  has a Background section, and no term is used before it is defined.
- Every topic in the coverage table, including those the notes skip, has a
  section.
- Every number is bound to a capture or cited to a slide or paper.
- You have looked at every page, and you are sending one question, not a list.
