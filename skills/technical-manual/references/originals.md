# The manuals this style comes from

Manuals built with the same process. Measurements from them are in
`design-system.md`, `figure-catalog.md` and `style-samples.md`; this file says
where they are and what to look at.

- https://huggingface.co/buckets/cfahlgren1/technical-manuals (GGUF, Apache
  Parquet, Pi Durable)
- https://huggingface.co/buckets/lucataco/technical-manuals (Pi)

| File                                 | Pages | Subject kind                                   |
| ------------------------------------ | ----- | ---------------------------------------------- |
| `GGUF-Technical-Manual.pdf`          | 105   | file format, dark cover                        |
| `Parquet-Technical-Manual.pdf`       | 155   | file format, paper cover with a numbered plate |
| `Pi-Durable-Technical-Manual.pdf`    | 190   | library / runtime, paper cover                 |
| `Pi-Technical-Manual.pdf` (lucataco) | 221   | library / CLI, navy cover, orange accent       |

They are not bundled here. If the environment can open that page, look at a few
pages before designing figures; the bucket may refuse plain HTTP fetches, in
which case use a browser. If it cannot be reached, carry on: the rules in
`SKILL.md` and the exemplar are sufficient.

Pages worth seeing (PDF page numbers):

- **Covers.** GGUF p. 1: magic bytes set huge over a coloured hex dump of a real
  header. Parquet p. 1: "Plate I", an elevation of the file with twelve numbered
  callouts and a key. Pi Durable p. 1: a timeline of a crash and what survives
  it, with four small figures beneath.
- **Front matter.** GGUF p. 4, Parquet pp. 4–5, Pi Durable pp. 4–6 ("How to read
  this book").
- **Part opener.** GGUF p. 5, Parquet p. 6.
- **Byte layout drawn to scale.** GGUF p. 7 (Fig. 1.2), GGUF p. 10 (Fig. 1.4).
- **Hex walk.** GGUF p. 25 (Figs 2.10, 2.11).
- **Checks as boxes and arrows.** GGUF p. 27 (Fig. 2.12).
- **Worked example with a check script.** GGUF pp. 54–55.
- **Measured bar chart.** GGUF p. 12 (Fig. 1.5), Parquet p. 8 (Fig. 1.2).
- **Level grid and annotated page body.** Parquet p. 36 (Figs 3.5, 3.6).
- **Sequence diagram with numbered commits.** Pi Durable p. 20 (Fig. 1.4).
- **Source excerpt beside a defaults table.** Parquet p. 48.
- **Rule / break it and… / do instead table.** Pi Durable p. 163.
- **Pi (lucataco).** p. 1 cover plate (a run as swimlanes); p. 6 part opener; p.
  9 structure figure with Why it matters and What this means for you; p. 16
  numbered sequence; p. 31 core rule quote and state figure; p. 38 decision
  chain; p. 51 loop as a state figure with line numbers; p. 88 trees; p. 172 a
  frame byte by byte; p. 213 documentation versus code table.
- **Reference.** GGUF pp. 101–104 (tensor names, glossary, sources and versions
  with the not-verified list, index of figures).

How the three differ, so you can choose: the format manuals lead with bytes
(strips, hex, cells) and close sections with Verify or Footgun callouts; the
library manual leads with sequence diagrams and stored records, and closes most
sections with a "What this means for you" box of three or four imperatives.
