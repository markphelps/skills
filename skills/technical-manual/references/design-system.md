# Design system, as measured

Measured on 2026-10-08 from three manuals built with Paged.js and Chrome: _GGUF_
(105 pp., cfahlgren1), _Apache Parquet_ (155 pp., cfahlgren1) and _Pi_ (221 pp.,
lucataco). Sizes are read from the PDFs' text runs, colours from their drawing
operators. The kit's `manual.css` already uses these values; this file is for
changing the CSS knowingly, or for checking a page against the originals.

## Page

|               | Value                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Trim          | US Letter, 612 × 792 pt                                                                                                       |
| Text block    | 58 pt from each side (body lines start at x = 58, end at about 553.5), ≈ 495 pt wide                                          |
| Running head  | baseline 46 pt from the top: section title left, short book name right, 7.2 pt sans, grey                                     |
| Footer        | baseline 37 pt from the bottom: `NAME / TECHNICAL MANUAL` left in 6 pt spaced mono capitals, page number right in 7.4 pt mono |
| Front matter  | roman page numbers, no running head                                                                                           |
| Section start | always a new page                                                                                                             |
| Part opener   | full-bleed dark page, no head or foot from the page template                                                                  |

## Type

| Role                                | Font                                   | Size (pt)    | Notes                                                   |
| ----------------------------------- | -------------------------------------- | ------------ | ------------------------------------------------------- |
| Body                                | Source Sans 3 Regular                  | 9.3 (Pi 9.4) | line height ≈ 1.55                                      |
| Lede (first paragraph of a section) | Source Sans 3                          | 10           | one size up from body                                   |
| Section number                      | JetBrains Mono, accent                 | 7.4          | spaced: `1 . 1`, `R . 6`                                |
| Section title                       | Manrope SemiBold                       | 21           |                                                         |
| Deck                                | Source Serif 4 Italic                  | 10.4         | grey, at most ~70% of the measure                       |
| Subhead (h2)                        | Manrope SemiBold (Pi: Medium)          | 12.4         |                                                         |
| Inline code                         | JetBrains Mono, accent ink             | 8.3          |                                                         |
| Inline source location              | JetBrains Mono, light grey             | 6.8–7.3      | `src/gguf.cpp:228`, follows the clause                  |
| Figure header                       | JetBrains Mono, spaced capitals        | 6.5–6.6      | `FIG. 1.2` grey, title in accent, kind/provenance right |
| Figure body text                    | Source Sans 3 / JetBrains Mono         | 7.3–8        | labels in boxes; hex at 6.5–7.1                         |
| Caption                             | Source Sans 3; lead SemiBold           | 8.2          | bold finding, then provenance                           |
| Table body                          | Source Sans 3; code cells mono         | 7.4          |                                                         |
| Table header                        | JetBrains Mono Medium, spaced capitals | 6.2–6.5      | grey                                                    |
| Callout text                        | Source Sans 3                          | 8.4          | label in 6.2 pt spaced mono                             |
| Listing                             | JetBrains Mono                         | 7.0–7.3      | header: bold file name, grey path, language right       |
| Sources line                        | JetBrains Mono                         | 6.2–6.8      | `Sources:` in bold                                      |
| Contents entry                      | Source Sans 3 8.3, numbers in mono 7   |              | dotted rule leader, mono page number                    |
| Part opener title                   | Manrope SemiBold                       | ≈ 31         | white on dark; kicker `PART 1` in spaced mono accent    |
| Cover title                         | Manrope Bold                           | ≈ 38–40      | "Technical Manual" in Source Serif Italic, accent       |

## Colour

Neutrals. Rules and table hairlines are darker than you would guess; that is
what makes the pages look engraved rather than washed out.

| Token                          | Warm (GGUF)         | Cool (Parquet, Pi)                                 |
| ------------------------------ | ------------------- | -------------------------------------------------- |
| paper                          | `#faf8f3`           | `#faf8f3` / `#faf7f2`                              |
| panel (figure, listing ground) | `#eeece2`–`#f3f1e9` | `#f4f2ea`                                          |
| rule                           | `#cbc8b9`           | `#cbc8b9` / `#d6d0c5`                              |
| ink                            | `#1d1a17`           | `#161d27` / `#232a34`                              |
| ink-2                          | `#45403a`           | `#3b4452`                                          |
| ink-3                          | `#68625b`           | `#5f6772`                                          |
| ink-4                          | `#8f8981`           | `#878e97`                                          |
| dark (cover, part opener)      | `#16120f`           | `#0f1826` (navy)                                   |
| accent                         | `#c9793f`           | `#2a5f88` (Parquet); `#e08a4c` orange on navy (Pi) |
| accent ink (inline code)       | `#7a3e12`           | `#24405e`                                          |

Region colours (fill / edge / ink), from GGUF's figures. Parquet and Pi use the
same families, slightly cooler. These are `k1`–`k7` in the kit.

| Token | Family | Fill      | Edge      | Ink       |
| ----- | ------ | --------- | --------- | --------- |
| k1    | orange | `#f5e6d9` | `#c9793f` | `#7a3e12` |
| k2    | teal   | `#e1f0f1` | `#5fb0ae` | `#0f5a61` |
| k3    | blue   | `#e3ecf4` | `#3f74a0` | `#214d72` |
| k4    | violet | `#ebe7f4` | `#6c5a9e` | `#45377a` |
| k5    | rose   | `#f5e4ea` | `#d08aa0` | `#a64d68` |
| k6    | green  | `#e4efe4` | `#6fa47c` | `#3d7a4d` |
| k7    | amber  | `#f5ecd9` | `#d9b25a` | `#6e4a0f` |
| k0    | grey   | `#eeece2` | `#cbc8b9` | `#68625b` |

Callout grounds reuse the region fills: Footgun on rose, Why it matters / Verify
on blue, Rule of thumb on teal, Doc ≠ code on amber, What this means for you on
panel with an accent top rule. Pi's sequence diagrams colour each participant's
lifeline box and arrows with its own region colour; that is the one place a
colour means "who" rather than "what kind of byte".

## Components seen, and their kit equivalents

| In the manuals                                                                                              | Kit                                       |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Section head: mono number, title, italic deck, hairline                                                     | generated from `data-title` / `data-deck` |
| Figure frame: panel, accent left rule, mono header strip                                                    | `figure.fig` (generated frame)            |
| Byte strip with sizes under each region                                                                     | `.strip` / `figs.strip`                   |
| Hex dump with coloured cells and ASCII                                                                      | `.hex` / `figs.hexdump`                   |
| Cell rows for a decode                                                                                      | `.cells`                                  |
| Measured horizontal bars, value at the end                                                                  | `.bars` / `figs.bars`                     |
| Sequence diagram, numbered steps on the left                                                                | `figs.sequence`                           |
| State machine / flow as stacked boxes with line numbers (`poll steering · :176`)                            | SVG with kit classes                      |
| Indented tree in mono with italic grey notes                                                                | `.tree`                                   |
| Quoted rule with a label (`CORE RULE`)                                                                      | `blockquote.rule`                         |
| Ruled term list (`**Term.** text`, hairline between)                                                        | `.items`                                  |
| Callouts: Footgun, Verify, Rule of thumb, Why it matters, What this means for you, Doc ≠ code, Experimental | `.callout.<kind>`                         |
| Step walk-through after a numbered figure (`1 · Submit.`)                                                   | `.steps`                                  |
| Listing with header strip                                                                                   | `pre.listing`                             |
| Terminal command / output                                                                                   | `pre.term`, `pre.out`                     |
| Index of figures, Contents with part chips                                                                  | generated                                 |
