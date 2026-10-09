# Figure catalog

Every figure in the three reference manuals carries a kind (or a provenance) in
the right of its header strip. This is the full set, with counts, what each kind
is for, and how to make it with the kit. Use it to choose the figure before you
draw it, and to tag it.

## How many, and how dense

| Manual           | Pages | Sections | Numbered figures | Pages per figure | Callouts                                                                                           |
| ---------------- | ----- | -------- | ---------------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| GGUF (format)    | 105   | ≈ 45     | 59               | 1.8              | 11 Footgun, 4 Verify, 4 Rule of thumb, 5 Why it matters                                            |
| Parquet (format) | 155   | ≈ 43     | 78               | 2.0              | 2 Rule of thumb, 1 Verify                                                                          |
| Pi (library)     | 221   | 36       | 59               | 3.7              | 23 What this means for you, 18 Footgun, 12 Doc ≠ code, 5 Rule of thumb, 4 Why it matters, 1 Verify |

Format manuals run a figure every two pages and use callouts sparingly. The
library manual has fewer figures but more tables and listings, and closes most
sections with a "What this means for you" box. Every section in all three ends
with a Sources line.

## Kinds

| Kind (tag)     | Parquet | Pi  | Shows                                                                                       | Kit                                         |
| -------------- | ------- | --- | ------------------------------------------------------------------------------------------- | ------------------------------------------- |
| BYTE LAYOUT    | 18      | 2   | where fields sit in a file, page, frame or record; often a whole specimen "exploded"        | `figs.strip`, `.hex`, `.cells`              |
| WORKED EXAMPLE | 12      | –   | one real value decoded step by step: a varint, a page header, a bit-packed run, a point     | `.cells` + arithmetic rows, `figs.hexdump`  |
| MEASURED       | 18      | 1   | a quantity from your captures across specimens, writers or settings                         | `figs.bars`, a table in the frame           |
| STRUCTURE      | 18      | 9   | what contains what: structs, layers of a package, a schema, what ships vs. what is left out | nested boxes in HTML (`.flow`) or SVG       |
| LEVEL GRID     | 4       | –   | a value-by-value grid of derived columns (repetition/definition levels, size stats)         | table or `.cells` rows                      |
| FLOW           | 3       | 13  | the path one call or one byte takes through stages                                          | SVG boxes and `arrow`                       |
| SEQUENCE       | –       | 11  | who calls whom, in order, with numbered steps the text walks through                        | `figs.sequence` + `.steps`                  |
| DECISION       | –       | 12  | how a value is resolved or a branch is chosen (precedence, trust, fallback)                 | SVG boxes with labelled yes/no edges        |
| STATE          | –       | 2   | a loop or state machine with its exits                                                      | SVG, stacked boxes with source line numbers |
| COMPARISON     | –       | 4   | two or more things side by side (docs vs. code, modes vs. streams)                          | table in the frame                          |
| TREE           | –       | 2   | parent links: a session file, a schema                                                      | `.tree`                                     |
| LAYERS         | –       | 2   | a dependency stack                                                                          | stacked `.flow` rows                        |
| TIMELINE       | 2       | 1   | events in time: releases, batches into pages, one run event by event                        | SVG with an axis                            |
| ALGORITHM      | 2       | –   | an algorithm's loop with its data (a bloom probe, a chunker)                                | SVG, or `.cells` per iteration              |
| TABLE          | 2       | –   | a matrix that is the point of the section                                                   | table in the frame                          |

GGUF tags with provenance instead of kind, and that is equally good:
`BYTE LAYOUT · REAL FILE`, `TINYLLAMA · BYTES 0–23`,
`TINYLLAMA · OFFSET 1,697,530`, `MEASURED · LOG SCALE`,
`MEASURED · 5 SPECIMENS`, `GGUF_INIT_FROM_FILE_IMPL` (the function drawn),
`SPEC § SPECIFICATION`, `TO SCALE`, `HISTORY`, `DESIGN`,
`SCHEMATIC + MEASURED TOTALS`, `ILLUSTRATIVE`, `TINYLLAMA + ILLUSTRATIVE`. The
rule: the tag tells the reader what kind of truth the picture is.

## Titles and captions

- **Figure titles** are two to six words in capitals, a noun phrase or a claim:
  `FILE ANATOMY`, `THE FIXED HEADER`, `A TABLE CUT TWICE`,
  `ONE PROMPT, ONE TOOL CALL, 29 EVENTS`, `AGENT_END IS NOT THE END`,
  `WHERE THE CUT LANDS`, `TEN IDS, 19 BYTES`.
- **Caption leads** (the bold first sentence, which the index of figures lists)
  state the finding: "A parser reads 0.26% of the file." "Two populations."
  "Eleven checks in file order." "32 weights from 18 bytes." "The prompt is on
  disk before the model sees it." "One opening, any number of blocks, exactly
  one terminal event." "Each line's parentId is the line before it."
- **The rest of the caption** says what was drawn and from where, and ends with
  its status: "From research/out/one-turn.txt." "Drawn to scale." "Schematic."
  "Verified against agent-session.ts at 28dcce2." "Real bytes from the pinned
  build."

## Recurring compositions

- **A specimen, exploded.** The whole small file as a strip, then each region
  enlarged below with its own strip, offsets under the boundaries (Parquet 2.1,
  safetensors exemplar 1.1).
- **Two specimens drawn to scale twice.** The same layout for a tiny and a huge
  file, so the proportion is the finding (GGUF 1.2).
- **Hex walk at the boundaries.** The first rows, then a jump to where one
  region hands over to the next, each byte coloured by the field a parser
  assigns it to (GGUF 2.10–2.11).
- **Numbered sequence, then walked.** A sequence diagram with circled numbers,
  followed by `1 · Submit.`, `2 · …` paragraphs that explain each step with its
  source location (Pi 1.4).
- **Checks in file order.** Every validation as a box in the order the reader
  runs it, each with the error it returns; the failure exit in rose (GGUF 2.12,
  Pi 3.1).
- **What ships / what is built in / what is left out.** Three columns of boxes
  (Pi 1.1).
- **Before and after.** The same bytes or pages before and after one edit
  (Parquet 8.2–8.10).
- **Docs versus code.** A numbered table: doc says (file) · code does
  (file:line) · see (section), one row per gap, re-checked at the pin (Pi R.6).

## Cover plates

- GGUF: dark cover; the magic bytes `47 47 55 46` set huge with their letters
  beneath, the next header fields decoded, then a coloured hex dump of the real
  header with a key.
- Parquet: paper cover on a faint grid; "Plate I · Anatomy of a Parquet file",
  an elevation of the file with twelve numbered callouts, two circular
  enlargements and a key.
- Pi: navy cover; "Plate I · One prompt, two turns, eight lines", a timeline of
  one real run with swimlanes (user, agent loop, model stream, tool, session
  file), numbered events and a key.

Each plate is one real capture of the subject that teaches its central idea
before page one.
