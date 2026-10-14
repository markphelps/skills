# Familiarity levels

The reader's familiarity with the subject, from 1 to 5, decides how much the
book teaches before and around each idea. Ask for it in step 0, record it in
`research/COURSE.md` and in `manual.json` as `"level"`, and print it in the
edition line so a reader picking the book up knows who it was written for:
`Fall 2026 · Lecture 1 · Level 2: no linear algebra assumed`, or
`Level 1: no prior biology`, or `Level 3: assumes the survey course`.

The scale is the same for every subject. What changes is what counts as a
prerequisite: math for an ML course, chemistry for a biology course, a period's
events and names for a history course, legal vocabulary for a law course.

## Asking

One question, with the scale written out so the answer is not a guess:

> How familiar are you with this subject, 1 to 5? 1 · new to it, and to what it
> builds on · 2 · a general idea, but rusty or new on what it builds on · 3 ·
> comfortable with the background, new to this topic · 4 · have worked with it ·
> 5 · know it well, want a dense review

Name "what it builds on" for the course when asking (the math, the chemistry,
the earlier survey course), so the answer is about the right thing.

Then, if the student named hard topics, ask whether any topic sits lower than
the rest. A per-topic level overrides the book's level for that topic's
sections: `"levels": {"attention": 2}`. Raise or lower the level when the
student says the last book was too hard or too slow; never change it silently.

## What each level does

|                                                | 1                                                               | 2                                             | 3                                   | 4                            | 5                                             |
| ---------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------- | ----------------------------------- | ---------------------------- | --------------------------------------------- |
| Assumes                                        | general education only                                          | some exposure; the background is rusty or new | the background the course builds on | the field's basics           | the topic itself                              |
| Background part                                | yes, from first principles                                      | yes, what the lecture assumes                 | a one-page refresher table          | no                           | no                                            |
| New terms                                      | `<dfn>` at first use, plus an everyday analogy                  | `<dfn>` at first use                          | `<dfn>` for field terms only        | glossary only                | glossary only                                 |
| Each formula, model or dense passage           | plain words + every symbol or term named + a small example      | plain words + every symbol or term named      | a one-line reading                  | as is                        | as is, plus variants                          |
| Order inside a section                         | picture or story, intuition, example, then the formal statement | intuition, example, formal statement          | statement, then example             | statement, then the argument | the result, then the nuances                  |
| Worked examples                                | the smallest case, every step shown                             | a small case, steps shown                     | a typical case                      | real cases                   | real cases, edge cases, debates               |
| Primary-source detail (sizes, dates, variants) | in Reference only                                               | a short table                                 | in the section                      | in the section               | expanded, with the sources' caveats           |
| Self-check                                     | recall and "explain in one sentence"                            | recall and small applications                 | applications                        | derivations or arguments     | design, trade-off or interpretation questions |
| Length                                         | longest: the lecture plus its prerequisites                     | about twice level 4                           |                                     |                              | shortest                                      |

At every level the facts, sources and corrections are the same. The level
changes how much scaffolding surrounds them, never what is true.

## Finding the prerequisites (levels 1–3)

Before writing, list every concept the lecture uses but does not teach, in
`research/PREREQS.md`, one row each: the concept, where the lecture first relies
on it (slide), and the level at or below which it gets taught. Examples:

- a Transformer lecture: vector, dot product, matrix product, transpose,
  softmax, probability distribution, cross-entropy, layers and weights,
  gradient;
- a cell-biology lecture: atoms and bonds, proteins and amino acids, the cell's
  parts, DNA → RNA → protein;
- a lecture on the French Revolution: the Estates system, absolute monarchy, the
  Enlightenment's key ideas, the map and the calendar of 1789;
- a contract-law lecture: offer, acceptance, consideration, what a precedent is,
  how to read a case citation.

Each row the reader's level needs becomes a short section in the **Background**
part (sections with `data-background`, numbered 0.1, 0.2, …), in dependency
order, each with:

- the idea in one sentence, before any notation;
- a small example, every step shown: computed by the check kit
  (`research/check/background.py`) when it has numbers, otherwise a short case,
  document or timeline from a citable source;
- the notation or vocabulary the lecture will use for it, read aloud;
- one line on where the lecture uses it ("Attention scores are dot products,
  1.3").

Background facts are general knowledge, not the course's: cite the course's own
refresher, textbook or assigned reading if it has one, and otherwise a standard
reference (a textbook chapter, a reference work), never memory alone. Keep each
section to a page.

## Writing at levels 1–2

- **Define at first use.** Wrap the term in `<dfn>` where it first appears and
  define it in the same sentence: "a <dfn>vector</dfn>, an ordered list of
  numbers". Define each term once; after that, point back to the section.
- **Every formal statement gets a reading.** Directly after each
  `blockquote.rule` (a formula, a legal test, a definition, a key quotation), a
  `.callout.plain` labelled "In plain words": one sentence saying what it does
  or means, then a `<dl>` naming every symbol or term. The build refuses a rule
  without one at levels 1–2.
- **Intuition first.** A section opens with what the idea is for, then a picture
  or a tiny example, and only then the notation.
- **Analogies** go in a `.callout.analogy`, at most one per section, and say
  where the analogy breaks.
- **"You need" boxes.** A section that relies on background opens with a
  `.callout.prereq` naming the background sections it uses: "Uses 0.2 dot
  product, 0.4 softmax."
- **No unexplained jumps.** "It follows that", "clearly" and "simply" mark a
  skipped step: write the step.

## Writing at levels 4–5

Cut the scaffolding, not the sources. Merge the worked example into a sentence,
move intuition callouts out, and spend the space on what the reader does not
know yet: exact sizes and costs, where the slides simplify the paper, what
changed in later models.
