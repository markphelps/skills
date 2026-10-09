# Exemplars

`references/example/` is a 19-page excerpt of a manual written with this skill
(the safetensors file format at commit `e246a25`). It builds with no problems,
so its markup is known to work. Use it as the pattern for your own fragments; do
not copy its content or its subject.

Read the file that matches what you are about to make.

| You are about to write      | Read                                                    | What to notice                                                                                                                                           |
| --------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `manual.json`               | `example/manual.json`                                   | theme triple, edition line, one-sentence description, part decks                                                                                         |
| the cover plate             | `example/cover.html`, `example/extra.css`               | the first eight bytes set huge, a to-scale strip, the whole file as a hex dump, a numbered key; plate-only CSS lives in `extra.css`                      |
| the front matter            | `example/00-how-to-read.html`                           | revision in the first sentence, sources ranked, specimens table, `.swatches` colour key, one line per part, the honest note on what could not be fetched |
| a section that opens a part | `example/01-bytes.html` → `#what-it-is`                 | deck that states a number, to-scale strips of two specimens, ruled `.items`, a two-column stored / not-stored table                                      |
| a worked example            | `example/01-bytes.html` → `#worked-tiny`                | command that fetches the bytes, hex dump coloured by region, numbered decode steps with the arithmetic, `.cells` rows, the check script and its output   |
| a sequence diagram          | `example/02-writing-checking.html` → `#fig-save-seq`    | lifeline boxes, numbered steps, call above the arrow and payload below, a self-call loop, caption that states the finding                                |
| a boxes-and-arrows diagram  | `example/02-writing-checking.html` → `#fig-check-order` | one column of checks in order, each wired to the error it returns, colour by region                                                                      |
| a source excerpt            | `example/02-writing-checking.html` (listings)           | `data-src` with path, line range and commit; cuts marked `…`; a note under the listing saying what was cut                                               |
| the Reference part          | `example/r-reference.html`                              | glossary as a table, Sources and versions, "Not verified, and therefore not claimed", generated index of figures                                         |
| the research folder         | `example/research/`                                     | `SOURCES.md` (becomes the sources table), `notes.md` (claim → location), `make_specimens.py` and `parse.py` with saved output in `out/`                  |

`example/research/gen_figs.py` is the script that produced that book's hex dumps
and excerpts. It predates `kit/figs.py`; in a new manual import `hexdump`,
`excerpt` and `bars` from the kit instead of rewriting them, and pull the output
in with `<!--#include research/figs/name.html-->`.

It predates `data-value` and `data-include`: its numbers were copied from
`research/out/` by hand. In a new manual bind them instead
(`references/markup.md`, Data binding).

The excerpt is also weaker than the target in two ways, so do better than it:
its cover plate leaves empty space below the key, and the full manual it came
from had 35 numbered figures in 77 pages, short of one every two pages.

To see the pages, copy `references/example` beside the kit and run
`node kit/build.mjs example --png`.
