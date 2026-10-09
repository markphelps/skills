# Grounding

How to build the evidence a manual is written from, and how to prove the
finished book against it. Read this before research starts.

## Contents

1. The research folder
2. Ranking sources
3. Pinning
4. What to look for in the code
5. The capture kit
6. Citation forms
7. Disagreements
8. The outline file
9. The claim ledger and the audit

## 1. The research folder

```
manual/
  research/
    SOURCES.md        pins, authority order, specimens, citation forms   -> "Sources and versions"
    OUTLINE.md        parts, sections, decks, promises, planned figures
    CLAIMS.md         non-obvious claims and the evidence for each       -> the audit
    notes/<part>.md   claim -> location notes, quoted rules, defaults as found
    repos/<name>/     clones at the pinned commit (do not edit)
    specimens/        the real files the book dissects (or how to fetch their bytes)
    capture/          scripts that drive the subject; run.sh runs them all; README.md
    captures/         what the scripts wrote: *.json for figures and values, *.txt for listings
    figs/             generated figure fragments (*.html), one script per figure
```

`research/capture/run.sh` must regenerate every file in `captures/` and `figs/`
from nothing but the pinned repos and the specimens. If it cannot, the book
cannot be re-checked.

## 2. Ranking sources

1. **Source code at the pin.** What actually runs. Defaults, limits and error
   paths come from here.
2. **The specification.** What is promised. Quote it word for word with its
   section.
3. **Captures and real artefacts.** What the code did on real input, recorded by
   your scripts.
4. **README, changelog, design notes.** What the authors say about it, and why.
5. **Tests.** What the authors check; useful for edge cases they thought of.
6. **The web.** Blog posts, issues, talks. Context only; never the sole source
   of a fact.

When two sources disagree, the higher one wins and the book says so where it
matters.

## 3. Pinning

- One subject at one revision: `package@version` and `repo@commit`, or
  `spec@commit` plus each implementation at its own commit. Record the date
  read.
- Build or install the code you run from the same commit, and print its version
  in a capture. A release from a package registry can be dozens of commits
  behind the source you are reading.
- Record every pin in `SOURCES.md` with what it was used for, as it happens.

## 4. What to look for in the code

Read the spec end to end, then the code path that implements each section. Note,
with `file:line`:

- **Defaults and constants** as written in source, and where the docs state
  something else.
- **Limits** and what happens at them: maximum sizes, counts, depths, timeouts.
- **Every error path** in the reader or loader, in the order the checks run.
- **Version gates and feature flags**: what changes behaviour, and where it is
  read.
- **Who writes it**: each writer's choices (ordering, padding, page sizes,
  defaults) and any fingerprint it leaves (a `created_by` string, a key order).
- **What is accepted but not specified**, and what is specified but not
  enforced.
- **Comments that state intent or warn** ("never", "must", "do not"), quoted.

With subagents, give each one part or one implementation and ask for evidence
only: every statement returned with a `file:line` or `spec §`, quoted where
wording matters, nothing paraphrased without a pointer. You write the prose;
they bring the pointers.

## 5. The capture kit

Scripts in `research/capture/` that drive the real subject and record what it
does:

- **Real headers by range request** for large published files, never the whole
  file.
- **Decoders run on specimens**: every offset, size and count the book will
  state.
- **Storage dumps** for systems: every row, record or file the subject wrote, in
  stored order.
- **Event and transcript logs** of a run, with a fake provider or fixture so
  there is no network or key.
- **Crash and kill runs**: kill the process at a chosen step, reopen, record
  what survived.
- **Malformed inputs**: hand-built bad files fed to the reader, with each
  outcome and message.
- **Measurements**: timings, memory, bytes read, with the machine and versions
  recorded.

Each script writes JSON (structured, for `data-value` and figure scripts) and,
where the book shows output, TXT exactly as printed (for `data-include`).
`capture/README.md` says which values are stable across runs (ids, offsets,
counts) and which are not (timestamps, pids, timings), so the book only quotes
the stable ones as exact.

## 6. Citation forms

Inline, at the end of the clause the citation supports:

| Kind                        | Form                                                                              |
| --------------------------- | --------------------------------------------------------------------------------- |
| source lines                | `<cite>src/gguf.cpp:464–480</cite>`                                               |
| a function                  | `<cite>gguf_init_from_file_impl</cite>` or `<cite>tensor.rs read_metadata</cite>` |
| spec section                | `<cite>spec §5.2</cite>`, `<cite>README §Format</cite>`                           |
| a capture                   | `<cite>research/captures/malformed.json</cite>`                                   |
| another party's measurement | named in the sentence: "the Hub team measured 0.9 s"                              |

Every file cited inline in a section also appears in that section's Sources
line.

## 7. Disagreements

State both sides, cite both, and say which one the code follows. The shape of
the sentence (the citations here are placeholders, not facts to reuse):

> The spec allows nested arrays <cite>docs/gguf.md §Arrays</cite>; ggml rejects
> them with "nested arrays are not supported" <cite>src/gguf.cpp:512</cite>.
> Files on the Hub have none.

Collect them in a section of their own when there are more than three, and list
each in the outline so none is lost.

## 8. The outline file

`research/OUTLINE.md`, written before any chapter. One block per section:

```
## Part 2 · The file, byte by byte   (promise P2: decode any header by hand)
2.3 Strings and arrays
  deck:    Arrays record an element count but not a byte length, so a reader cannot skip one.
  serves:  P2
  sources: docs/gguf.md §Arrays; src/gguf.cpp:330–380 gguf_reader::read(std::string)
  figures: strip (array encoding, tinyllama tokens) <- captures/tinyllama.json
           hex (first 3 tokens) <- specimens/tinyllama.gguf @ 0x2c0
  callouts: footgun (string array cannot be skipped)
```

The promises are the 4–7 capabilities the front matter lists ("After this book
you can…"). Every part serves at least one, and every promise is served by some
part.

## 9. The claim ledger and the audit

`research/CLAIMS.md` records each claim that is not obvious from a single cited
line: a number derived from several sources, a statement about all writers, a
"never", a disagreement, a measurement.

Example rows (the shape only; the values are placeholders):

```
| id  | claim (as printed)                                   | section | evidence                                   | status   |
|-----|------------------------------------------------------|---------|--------------------------------------------|----------|
| C14 | The tokenizer arrays are 99.23% of the header        | 3.4     | captures/tinyllama.json regions; parse.py  | verified |
| C15 | No Hub specimen uses big-endian                      | 2.1     | captures/headers/*.json endianness         | verified |
| C16 | llama.cpp ignores general.alignment above 2^30       | 2.5     | src/gguf.cpp:601 (only checks power of 2)  | FAILED   |
```

Before handing over, run the audit with a reviewer that did not write the book
(a subagent when available): give it `CLAIMS.md`, the chapter files and the
research folder, and ask it to open every cited `file:line`, re-run or read
every cited capture, and mark each claim verified or failed with the reason.
Then fix or delete every failed claim, or move it into an Unverified callout and
the "Not verified, and therefore not claimed" list. Sample sentences outside the
ledger too: pick ten at random per part and check them the same way.
