# Style samples

Short excerpts from the reference manuals (_GGUF_, _Apache Parquet_, _Pi_), each
followed by the pattern it shows. Use them to calibrate tone; write your own
sentences about your own subject.

## Decks: the section's claim in one or two sentences

> GGUF writes the fastest-moving dimension first. Get this backwards and every
> size calculation, block count and viewer label is wrong. _(GGUF 4.2)_

> One answered question that needs one file read is two model calls, 29 session
> events and 8 JSONL lines. _(Pi 1.3, first sentence)_

> A session file is append-only and every entry names its parent, so one file
> holds a whole tree of conversations. _(Pi, "Sessions: the JSONL tree", first
> sentence)_

> `Q4_K_M` is not a type. It is a policy that assigns a type to every tensor.
> _(GGUF 5.9, first two clauses)_

> Twenty-four bytes decide whether the rest of the file is readable. _(GGUF 2.1,
> first clause)_

Patterns:

- A **count** the reader would not guess ("fourteen packages… a chain of three",
  "42 providers", "sixteen gaps survive at this commit").
- A **mechanism and its consequence** joined by "so": "…every entry names its
  parent, so one file holds a whole tree".
- A **correction of the obvious reading**: "is not a type", "the run is over at
  agent_settled, not at agent_end", "Failures do not throw; they arrive as the
  last event".
- A **stake**: "Get this backwards and every … is wrong."
- Decks in the Reference part are plain descriptions: "The vocabulary of the
  format and its ecosystem, as this book uses it." "Every figure in the book,
  with the claim it makes."

## Section titles

Plain and specific, often a claim: _The header has no length_, _Why the
tokenizer dominates the header_, _Reading starts at the end_, _Why Parquet
defeats deduplication_, _Contracts that bite_, _From prompt() to agent_settled_,
_agent_end is not the end_, _Worked example: a real Q4_K super-block_,
_Documentation versus code_. Code names appear in titles as they are spelled.

## Subheads (h2)

Labels that each make one point: _Field by field_, _What is not stored_, _Where
the alignment is measured from_, _The two hand-overs_, _Who writes it_, _What it
costs_, _Measured_, _Before and after_, _The specimen_, _The captured event
stream_, _Two packages_, _Choosing the model_, _When it triggers_, _What the
model sees afterwards_.

## Ledes: what the section will do, in order

> This section lists what the reference reader validates and what the JavaScript
> parser adds, and closes with a complete minimal parser. _(GGUF 2.7)_

> This section decodes the first 208 bytes of
> `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`, then jumps to the two boundaries where
> one region hands over to the next. _(GGUF 2.6)_

Pattern: "This section [verb]s X, [verb]s Y, and closes with Z." Set a size up
from body.

## Sources lines

> Sources: ggml docs/gguf.md gguf*tensor_info_t; include/ggml.h (GGML_MAX_DIMS
> 4, GGML_MAX_NAME 64); src/gguf.cpp:640–770; gguf-py constants.py
> Keys.General.TENSOR_EXTRA*_; research/headers/tinyllama.json _(GGUF 2.4)\*

> Sources: ai/models.ts (calculateCost :1198, getAuth :742, refresh :551 …).
> ai/types.ts:1058–1073 … _(Pi 2.4)_

Patterns:

- Semicolon-separated; each entry is `repo path (symbol :line, symbol :line)` or
  `path:lines`.
- The pin appears once per repo where it first matters:
  `apache/parquet-format @ bf09939`.
- Research files are named too:
  `research/capture/one-turn.mjs; research/out/one-turn.txt`.
- **Path aliases**: Pi defines short prefixes in its front matter (`CA/` for
  `packages/coding-agent/`, `ai/` for `packages/ai/src/`) and uses them
  everywhere. Define yours in "How to read this book" when paths are long.

## Callouts

- **Footgun**: names the exact collision. GGUF: two enums in one file use
  overlapping small integers, so `general.file_type = 15` and tensor type 15
  mean different things.
- **Doc ≠ code** (Pi): marks every place shipped docs and code disagree, then
  the Reference part collects all of them in one numbered table re-checked at
  the pin.
- **What this means for you** (Pi): three to five imperatives. "Expect Pi to
  call a model, run tools and write JSONL, and nothing more, until you load
  extensions."
- **Core rule** (Pi): the one sentence of the spec a section rests on, quoted in
  full with its location, as a labelled block quote.

## Front matter, as the three books do it

- GGUF: _What it is grounded in_ · _Conventions_ · _How the parts are ordered_.
- Parquet: _Who this is for_ · _How it was made_ · _How the parts are ordered_ ·
  _Conventions_.
- Pi: _Who this is for_ · _How it was made_ (with _The capture kit_) ·
  _Conventions_ · _A first conversation you can run_ · _How the parts are
  ordered_ · _Colour in figures_ · _How the counts were made_.

## Reference parts

- GGUF: value types and the container · `ggml_type` table · standard keys ·
  tensor names · glossary · sources and versions (with _Not verified, and
  therefore not claimed_) · index of figures.
- Parquet: Thrift structures and field ids · enumerations · encodings and codecs
  by type · writer knobs · glossary · index of figures.
- Pi: environment variables · CLI reference · slash commands and keybindings ·
  settings reference · source file index (file, size at the pin, symbols,
  section) · documentation versus code · glossary · sources and versions · index
  of figures.

A library manual's Reference is the surface a user touches (flags, settings, env
vars, keys); a format manual's is the structures and enums a parser needs.
