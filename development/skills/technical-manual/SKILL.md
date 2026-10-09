---
name: technical-manual
description:
  Write a dense, book-length technical manual (print-ready PDF) about a file
  format, protocol, library, runtime or system, grounded in its actual spec and
  source code at a pinned version, with captured bytes and runs, measured
  numbers and many data-driven diagrams. Use this whenever the user asks for a
  "technical manual", "engineering manual", "deep dive book", "internals guide",
  "the definitive guide to X", a from-first-idea-to-exact-bytes explainer, or
  wants to really understand how X works on disk, on the wire or in the code,
  even if they only say "write me a manual on X" or "document how X actually
  works".
---

# Technical manual

You are writing a reference book an engineer keeps open while writing a parser,
debugging a crash, or deciding how to configure a writer. It runs from the first
idea down to the exact bytes or stored rows. The method has one rule:

> **Nothing is written from memory. Every claim traces to a pinned source or a
> captured artefact, and every figure is drawn from that same data.**

What that produces:

- **Pinned, ranked evidence.** One subject at one commit. Code outranks the
  spec; where they disagree, the book says so.
- **The real thing on the page.** Real hex, real headers, real stored records,
  cut from captures and decoded by hand, then checked against the reference
  implementation.
- **Figures as data.** Byte strips, hex walks, sequence diagrams and bar charts
  generated from captures, about one every two pages, in one colour code that
  holds for the whole book.
- **Plain, exact prose.** Short declarative sentences with numbers and names in
  them, and a Sources line closing every section.

The output is a Letter-size PDF in a fixed house style (cream paper, dark part
openers, Manrope / Source Sans 3 / Source Serif 4 italic / JetBrains Mono),
typeset with Paged.js from HTML fragments by the kit in `assets/kit/`.

## Files in this skill

| Path                           | Read when                                                                                                                                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/grounding.md`      | Before research. Research folder, source ranking, pinning, what to look for in code, the capture kit, citation forms, disagreements, `OUTLINE.md` and `CLAIMS.md` formats, the claim audit. |
| `references/markup.md`         | Before writing the first fragment. Data binding, every component's HTML, the figure generators, SVG and arrow conventions, callout kinds.                                                   |
| `references/exemplars.md`      | Before drawing your first figures. A guide to `references/example/`, a 19-page excerpt that builds cleanly.                                                                                 |
| `references/figure-catalog.md` | When outlining figures. Every figure kind the reference manuals use, with counts, what each is for, title and caption patterns, recurring compositions, cover plates.                       |
| `references/style-samples.md`  | Before writing prose. Short excerpts of decks, ledes, titles, subheads, Sources lines and callouts, with the pattern each shows; front matter and Reference contents of each book.          |
| `references/design-system.md`  | When touching CSS or checking a page. Measured page geometry, type scale, palettes (warm and cool), component inventory.                                                                    |
| `references/originals.md`      | When you want to see the reference manuals (GGUF, Parquet, Pi Durable, Pi) and which pages to look at.                                                                                      |
| `assets/kit/`                  | Copied into the workspace: stylesheet, build script, figure generators.                                                                                                                     |

## Prerequisites

Check these before Phase 0, and ask the user to install anything missing before
the research starts. Do not discover a missing tool at Phase 6.

| Tool                  | Used for                                        | Check                         | Install                                                                 |
| --------------------- | ----------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| Node.js 18+ and `npm` | the kit's build (`kit/build.mjs`)               | `node --version`              | https://nodejs.org or a version manager                                 |
| Chromium              | Paged.js typesetting and PDF output             | the example build (see Build) | `npx playwright-core install chromium` in the kit folder, or Chrome     |
| `pdftoppm` (Poppler)  | page images (`--png`) for Phase 6 and hand-over | `command -v pdftoppm`         | macOS `brew install poppler`; Debian/Ubuntu `apt install poppler-utils` |
| Python 3 and `git`    | figure generators (`kit/figs.py`), capture kit  | `python3 --version`           | system package manager                                                  |

Without `pdftoppm` the build still writes the PDF but skips the page images, and
you cannot do the visual check in Phase 6. If the user declines to install it,
say in the hand-over that the pages were not looked at.

## Workflow

Do the phases in order. No prose is written before phases 1–3 exist on disk: the
book is a rendering of the research folder, not something written alongside it.

### Phase 0. Scope card

Settle these and write them at the top of `research/OUTLINE.md`:

- **Subject and pin.** `package@version` and `repo@commit`, or `spec@commit`
  plus the implementations you will read, and the date read. Default to the
  latest release.
- **Reader.** One paragraph: what they already know, and what they have not
  read.
- **Promises.** 4–7 "After this book you can…" capabilities. Every part serves
  one.
- **Specimens.** The 3–12 real files or runs the book dissects: public and
  recognisable where possible, one small enough to show whole, one large enough
  to show scale.
- **Angle.** The job the reader's team has (e.g. reading the format over HTTP),
  if any. It earns its own part and the "why it matters" callouts.
- **Theme.** `"warm"` (orange on brown-black, dark cover) or `"cool"` (blue on
  navy, paper cover).
- **Size.** Let the subject decide. A full manual is 6–10 parts, 40–55 sections,
  100–190 pages and 60–80 figures; a small format honestly covered may be 40–80
  pages. Every section starts a new page, so a point that will not fill most of
  a page goes under an `h2` in a neighbour.

If the user gave only a topic, propose the card in one message and confirm it
before the research, because research is the expensive part. If they are not
there to answer, take the card as proposed and say so at the top of the
hand-over.

### Phase 1. Research folder

Copy the kit and set up the folder laid out in `references/grounding.md` §1.
Clone each repo at its pin; build or install the code you will run from that
same commit and record its version. Read the spec end to end and the code that
implements each part, writing `research/notes/<part>.md` as claim → `file:line`,
with quoted rules, defaults as found in source, and every spec–code
disagreement. Fill `research/SOURCES.md` as you go. With subagents, split the
reading by part or by implementation and ask for evidence only (§4).

If the environment cannot reach the repo or spec, stop and tell the user what
you need. A manual in this style that is not grounded is worse than none.

### Phase 2. Capture kit

Write scripts in `research/capture/` that produce every artefact the book will
show: real headers by range request, decoder traces over the specimens, storage
dumps, event logs, crash and kill runs, malformed inputs fed to the reader,
measurements. Each writes JSON (for figures and bound values) and TXT (for
listings) into `research/captures/`; `research/capture/run.sh` regenerates all
of it; `capture/README.md` says which values are stable across runs. If
published files cannot be fetched, write specimens with the reference
implementation, keep the script, and say so in the front matter and the
not-verified list. Parse each specimen two ways (your script and the reference
library) before drawing it.

### Phase 3. Outline

Write `research/OUTLINE.md` in the format of `references/grounding.md` §8: for
every section its number, title, deck (the section's claim), the promise it
serves, its sources, its figures with their data source, and its callouts. Order
the parts by one stated principle: why it exists → the mental model → the layout
byte by byte (or record by record) → what it carries → the hard core with worked
examples → how it is written and by whom → how it is loaded, run or read in
practice → the reader's angle → Reference. For a format the spine is the file
from outside in; for a library it is one request traced through the layers, then
each layer. Plan at least one figure per section and about one per two pages
overall, choosing each figure's kind from `references/figure-catalog.md`. Plan
the Reference part from the patterns in `references/style-samples.md`:
structures and enums for a format, the user-facing surface (flags, settings, env
vars, keys) plus a "Documentation versus code" table for a library.

### Phase 4. Write

One file per part. Follow the section anatomy and voice below,
`references/markup.md`, and the calibration excerpts in
`references/style-samples.md`. Bind every captured number with `data-value` and
every shown output or excerpt with `data-include`, so prose cannot drift from
the data. Cite inline with `<cite>` at the end of the clause. Log each claim
that is not obvious from a single cited line in `research/CLAIMS.md`. Close each
section with its Sources line.

### Phase 5. Figures

Generate data figures with `kit/figs.py` (`hexdump`, `strip`, `bars`,
`sequence`, `excerpt`), one small script per figure in `research/figs/`, pulled
in with `<!--#include research/figs/name.html-->`. Hand-place flows, structures
and state machines in SVG with the kit classes. A figure a capture could not
produce is tagged `illustrative` and its caption says so. Build the cover plate
last, from a real specimen: an exploded or annotated artefact with numbered
callouts and a key. Look at `references/exemplars.md` first.

### Phase 6. Build, look, audit

Build, fix every problem the build prints, then read the page images:
overflowing figures, orphaned headings, half-empty pages, illegible or misplaced
labels, a colour used off its meaning. Fix layout by resizing or splitting a
figure, reordering blocks, or merging a thin section into its neighbour; never
delete a sourced fact to make a page fit. Then run the claim audit
(`references/grounding.md` §9) with a reviewer that did not write the book, and
fix, delete or mark unverified everything that fails.

### Phase 7. Hand over

Give the user the PDF, the pins, and the not-verified list in two or three
sentences. Keep `research/` with the manual; it is the proof.

## Grounding rules

1. **Every section ends with a Sources line** naming the spec sections, source
   files (with line ranges or function names), captures and scripts it was
   written from. The build refuses sections without one.
2. **Never invent bytes, offsets, ids, timings, sizes or outputs.** If it is
   shown, a capture produced it. Illustrative figures are labelled
   `illustrative`.
3. **Pin and print the revision.** Commits shortened to 7 characters, in the
   front matter, the Sources table and beside every excerpt.
4. **Quote, do not paraphrase, when wording carries weight,** with the location.
5. **Defaults are the values in source at the pin,** not the documentation's.
   Say when they differ.
6. **Others' measurements are quoted exactly and attributed;** your re-runs
   appear beside them, never instead.
7. **Say what kind of fact it is.** "The spec says", "ggml checks", "every
   specimen has", "an estimate from the constants, not a documented figure".
8. **Disagreements are features.** Spec versus code, writer versus writer, docs
   versus behaviour: state both, cite both, follow the code.
9. **Unverifiable claims are deleted, or kept in an Unverified callout with the
   reason,** and collected under "Not verified, and therefore not claimed" in
   the Reference part.
10. **Code excerpts are real,** cut from the pinned checkout with path, lines
    and commit; cuts are marked `…` and the note beneath says what was cut.

## The book

`manual.json` drives the build:

```json
{
  "title": "GGUF",
  "short": "GGUF",
  "slug": "GGUF",
  "edition": "Hub Engineering Edition · 2026.09",
  "description": "A source-grounded guide to the single-file model format: the byte layout, the metadata conventions, tensor naming, every quantization block, sharding, loading, and reading headers over the network.",
  "author": "Prepared for …",
  "theme": "warm",
  "cover": { "plate": "cover.html" },
  "front": "00-how-to-read.html",
  "parts": [
    {
      "title": "Orientation",
      "short": "Orientation",
      "deck": "Why a model became a single self-describing file, and what that decision still costs.",
      "file": "01-orientation.html"
    },
    {
      "title": "Reference",
      "number": "R",
      "deck": "Tables to keep open while writing a parser.",
      "file": "r-reference.html"
    }
  ]
}
```

`theme` is `"warm"`, `"cool"`, or an object
`{ "preset": "cool", "accent": "#…", "accentInk": "#…", "dark": "#…" }`;
`cover.style` (`"dark"` or `"paper"`) overrides the preset's cover. The build
generates the cover frame, Contents, part openers with their mini-contents,
section and figure numbers, cross-reference page numbers, running heads and the
index of figures. You write the cover plate, the front matter and the sections.

- **Cover plate.** A hero figure made from a real specimen that teaches
  something on its own: magic bytes set huge over the first hex rows, or "Plate
  I", an elevation of the file with a numbered key. The description is one
  sentence listing what the book covers.
- **Front matter** (`00`, "How to read this book"): one
  `<div data-title="How to read this book" data-deck="…">` with `h2` subheads
  and a Sources line. Figures are not numbered here, so use tables and
  `.swatches`. It covers what the book documents and at which revision; who it
  is for and the promises; how it was made (sources ranked, specimens table,
  capture kit); conventions (offsets, types, units, cross-references, the colour
  code, how measured and unverified claims are marked); one line per part. For a
  library, a first example the reader can run.
- **Parts.** A title of two to four words and a deck stating the part's idea.
- **Reference** (`"number": "R"`): lookup tables that restate the book (every
  field, enum, key, default, error), a Glossary, "Sources and versions" (source
  · revision · used for) with the not-verified list, and
  `<div data-generate="figure-index"></div>`.

## A section

```html
<section
  class="sec"
  id="what-readers-check"
  data-title="What readers check"
  data-deck="The format has no checksum, so every guarantee comes from a reader that refuses bad input. The readers differ in what they refuse."
>
  <p>
    Lede: what this section establishes, what you will be able to do with it,
    and the order it goes in.
  </p>
  <figure class="fig" …>…</figure>
  <h2>ggml: structural validity</h2>
  <p>… <cite>src/gguf.cpp:228–420</cite></p>
  <p class="sources">
    ggml src/gguf.cpp gguf_reader (:228–420), gguf_init_from_file_impl
    (:440–910); research/captures/malformed.json
  </p>
</section>
```

- **Title.** A plain noun phrase or claim: "The fixed header", "Why the
  tokenizer dominates the header", "Reading starts at the end", "Worked example:
  a real Q4_0 block". Never a pun or question.
- **Deck.** One or two italic sentences giving the finding, concrete enough to
  be wrong.
- **Lede.** What the section covers and in what order ("This section lists…, and
  closes with…"). No scene-setting. The build sets it a size up.
- **Subheads (`h2`)** each make one point: "Field by field", "Endianness is
  inferred, not declared", "What is not stored", "Who writes it", "What it
  costs", "Measured".
- **Body.** A paragraph or two, then a figure, table or listing; rarely more
  than half a page of unbroken prose. Ruled `.items` for parallel points.
- **Worked examples** are their own sections: fetch real bytes (show the
  command), draw them, decode step by step with the arithmetic, then the short
  script that checks against the reference library.
- **Close** with a callout where one earns its place, then the Sources line.

## Voice

Write like an engineer who has read the source and is telling a colleague what
is there.

- Declarative, present tense, mostly short sentences. "Nothing in the file
  points backwards and nothing points to the header, so the first three regions
  can only be read sequentially."
- Numbers with units and names in code font, constantly: fields, functions,
  constants, error strings. "11,906 bytes for 201 tensors, about 59 B each."
- Mechanism, then consequence. "Arrays record an element count but not a byte
  length. That single decision shapes …"
- Say what the thing does not do and what it costs ("What the format
  deliberately does not do").
- "You" only when giving the reader something to do or decide.
- No hype, hedging, warm-up, rhetorical questions, "let's", or summaries that
  repeat the section. If a sentence has no number, name or mechanism in it, cut
  it. Nothing is powerful, robust, seamless, simple or elegant; show the
  measurement.
- First use of a term defines it in passing, and it goes in the Glossary. One
  term per thing, the name the source uses.
- Cross-reference instead of repeating:
  `<a class="xref" href="#mmap">the loader</a>` prints as "the loader (p. 76)".

## Figures

At least one figure, table or listing in every section and a numbered figure
about every two pages. A figure shows what prose cannot: proportion, position,
order, correspondence.

| Showing                                      | Figure                                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| where things sit in a file, record or packet | byte strip (`figs.strip`), to scale when proportion is the point          |
| actual bytes                                 | hex dump (`figs.hexdump`) coloured by region with an ASCII column         |
| how a value is decoded                       | cell rows (`.cells`) with the arithmetic beneath                          |
| who talks to whom, in what order             | sequence diagram (`figs.sequence`) with numbered steps the text refers to |
| checks, pipelines, lineage, state machines   | boxes and arrows (SVG)                                                    |
| a measured quantity across specimens         | bar chart (`figs.bars`), value at the bar end                             |
| alternatives side by side                    | a table inside the frame                                                  |
| structure                                    | tree or nested boxes (SVG)                                                |

- `data-title` is two to four words; `data-tag` gives kind and provenance
  (`byte layout · real file`, `measured · log scale`, `spec § 3.2`,
  `sequence · tensor.rs:302–377`, `illustrative`); the kinds are in
  `references/figure-catalog.md`.
- **The caption opens with a bold finding**, a sentence the reader could quote,
  then says what was drawn from which specimen or capture. The index of figures
  lists these findings.
- **One colour code for the whole book.** Assign each of `k1`–`k7` one meaning
  in the front matter (for a format: header, metadata, index, data…; for a
  system: host, model, storage, task…). `k0` grey is padding, unused or elided;
  `hatch` is wasted or skipped bytes. Arrow kinds (call, return, async, error,
  data, context) also keep one meaning each. In sequence diagrams a colour may
  instead mark the participant, as long as the front matter says so.
- **Real values in the boxes**: actual sizes and offsets from a named specimen.
- **Text never overlaps or leaves its box.** Prefer the generators, which lay
  out from data.

## Build

```bash
cp -r "<this skill's folder>/assets/kit" kit
(cd kit && npm install)                        # pagedjs, fonts, highlight.js, playwright-core
node kit/build.mjs manual --png                # -> manual/<slug>-Technical-Manual.pdf, manual/build/pages/*.png
node kit/build.mjs manual --png --dpi 130      # sharper pages for proofreading small type
```

To check the install, copy `references/example` beside the kit and run
`node kit/build.mjs example --png`: 19 pages, no problems, and page images in
`example/build/pages/`. The build needs a Chromium; it tries Playwright's, then
`PLAYWRIGHT_BROWSERS_PATH`, `CHROME_PATH` and common install paths
(`npx playwright-core install chromium` fetches one). `--png` needs `pdftoppm`
(see Prerequisites).

The build prints page, section, figure and bound-value counts, then every
problem: sections without sources, decks, or any figure, table or listing;
figures without a finding or provenance; listings without a source; missing
captures or paths in `data-value` and `data-include`; broken references; blocks
wider than the page or split across pages; half-empty pages from an oversized
block; a few lines spilling onto a new page; labels that do not fit their box;
overlapping SVG labels; filler words. Notes follow (figure density, illustrative
figures). Fix every problem, then read the page images yourself: the build
cannot see a wrong number or a label on the wrong box.

## Before you hand it over

- `research/capture/run.sh` regenerates every capture and generated figure, and
  the book rebuilds clean afterwards.
- Every number in the book is bound to a capture or cited to a line.
- The claim audit ran, and every failed claim is fixed, removed or marked
  unverified.
- Every promise in the front matter is served by a part.
- The colour and arrow codes mean the same thing on page 7 and page 107.
- Spec–code differences are stated where they occur; pins are printed in the
  front matter and the Sources table; the not-verified list exists and is
  honest.
- You have looked at every page image.
