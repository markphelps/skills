# Markup

Fragments are plain HTML. The build adds section and figure numbers, frames,
running heads, Contents, part openers and the index of figures.
`references/example/01-lecture-1.html` uses every component below.

## The book

```json
{
  "title": "CME 295",
  "short": "CME 295",
  "kind": "Course Notes",
  "slug": "CME295-Lecture-1",
  "edition": "Fall 2026 · Lecture 1 · checked against the slides",
  "description": "One sentence saying what these notes are and what they were checked against.",
  "theme": "cool",
  "cover": { "style": "paper", "plate": "cover.html" },
  "front": "00-how-to-read.html",
  "parts": [
    {
      "title": "Lecture 1 · Transformers",
      "short": "Lecture 1",
      "deck": "…",
      "file": "01-lecture-1.html"
    },
    {
      "title": "Reference",
      "number": "R",
      "deck": "…",
      "file": "r-reference.html"
    }
  ]
}
```

The front matter is one
`<div data-title="How to read these notes" data-deck="…">` holding the layer
legend (`.swatches`), the sources table, and a table mapping the lecture's slide
ranges to sections. The cover plate is the lecture's key figure redrawn with
computed values (the one the student sketched, if they did), labelled by its
slide.

The book is standalone: it never says "you", never quotes the original notes,
and never says what they covered. With `"kind": "Course Notes"` the build
refuses `.mine`, `.callout.gap`, `.callout.ask` and `u.unsure`, and flags second
person and mentions of the notes.

## A section

```html
<section
  class="sec"
  id="attention"
  data-title="Attention: query, key, value"
  data-deck="Each token asks a question (its query), every token offers a label (its key)…"
>
  <p>Lede: what this section does.</p>
  …
  <p class="sources">
    Lecture 1 slides 58–62; Vaswani §3.2.1; research/captures/toy_attention.json
  </p>
</section>
```

## The layers

```html
<!-- body text: ordinary prose, a <cite> at the end of each clause it supports -->
<p>Slide 60 draws the idea for one token: … <cite>slides 58–60</cite></p>

<!-- callouts -->
<div class="callout focus" data-label="Focus">
  <p>The whole idea in two or three sentences.</p>
</div>
<div class="callout fix" data-label="Common mistake">
  <p>
    It is tempting to read the value as the token's embedding. It is not: …
    <cite>slide 100</cite> <cite>Vaswani §3.2.2</cite>
  </p>
</div>
<div class="callout why" data-label="Where this goes next">
  <p>Lecture 2 … <cite>L2 slides 80–83</cite></p>
</div>
<div class="callout why" data-label="In the lecture">
  <p>The end-to-end example, slides 79–115, … <cite>slides 106–115</cite></p>
</div>
```

For the reader's level (`levels.md`):

```html
<p>Each token becomes a <dfn>vector</dfn>, an ordered list of numbers, …</p>
<!-- once, at first use -->
<blockquote class="rule" data-label="Scaled dot-product attention">
  Attention(Q, K, V) = softmax(QKᵀ / √d<sub>k</sub>) V
</blockquote>
<div class="callout plain" data-label="In plain words">
  <p>
    Score every token against every other, turn each row of scores into weights,
    and average the values with them.
  </p>
  <dl>
    <dt>Q, K, V</dt>
    <dd>the queries, keys and values of all tokens, one row per token</dd>
    <dt>Kᵀ</dt>
    <dd>K transposed: rows become columns (0.3)</dd>
  </dl>
</div>
<div class="callout prereq" data-label="Uses">
  <p>0.2 dot product · 0.4 softmax</p>
</div>
<div class="callout analogy" data-label="Analogy">
  <p>… and where it breaks: …</p>
</div>
<section class="sec" id="bg-dot" data-background data-title="The dot product" …>
  <!-- Background part -->
</section>
```

`manual.json` takes `"level": 1–5` (and optional `"levels": {"topic": n}`); a
Background part is an ordinary part with `"number": "0"` placed first.

A common-mistake callout must contain a `<cite>`; the build refuses it
otherwise. State the mistake in general terms ("A head is often described as…"),
never as a quote from the notes.

## Worked examples

```html
<div class="steps">
  <p>
    <b>1 · Score.</b> … the scaled score is
    <span
      data-value="research/captures/toy_attention.json#head1.scores.1"
    ></span>
    …
  </p>
  <p><b>2 · Normalise.</b> …</p>
</div>
<blockquote class="rule" data-label="Scaled dot-product attention">
  Attention(Q, K, V) = softmax(QKᵀ / √d<sub>k</sub>) V <cite>slide 62</cite>
</blockquote>
```

Bind every computed number with `data-value="file.json#dotted.path"` (optional
`data-format`: `int`, `hex`, `bytes`, `pct`, `fixedN`). Pull generated fragments
in with `<!--#include research/figs/name.html-->`. A missing file or path fails
the build.

## Figures and tables

```html
<figure
  class="fig"
  id="fig-fan"
  data-title="Your sketch, computed"
  data-tag="toy · research/captures/toy_attention.json"
>
  <!--#include research/figs/fan-head1.html-->
  <figcaption>
    <b>Three quarters of the attention goes to "cute".</b> What was drawn, and
    from which capture.
  </figcaption>
</figure>
```

- `data-title`: two to four words. `data-tag`: kind and provenance
  (`toy · capture`, `comparison · slides 69, 71`, `timeline · slides 17–22`,
  `schematic`).
- The caption opens with a bold finding a reader could quote.
- Tables: `<th>` gets mono capitals automatically; `td.n` right-aligns numbers,
  `td.m` sets mono; `td.yes`, `td.part`, `td.no` colour a status cell.
- Generators in `kit/figs.py`: `bars(rows)`, `strip(regions)`,
  `hexdump(bytes, klass)`, `sequence(participants, steps)`,
  `excerpt(repo, path, ranges, lang)`.
  `references/example/ research/figs/make.py` shows them used with captures,
  plus a custom SVG (the query fan).
- Other components: `.cells` rows (a mask, a decode), `.flow` boxes, `.tree`,
  `.items` (ruled term list), `.legend`, `pre.listing` (needs `data-src`),
  `pre.term`, `pre.out`.
- SVG: `viewBox="0 0 640 H"`, no inline colours; classes `k0`–`k7` and `box` for
  rects, `m`, `s`, `lab`, `t1`–`t7` for text, `ln` and `arrow` (`ret`, `async`,
  `err`, `data`, `soft`) for lines.
- Colours: `k5` rose for common mistakes; `k6` green for pointers forward. Use
  the others (`k1` orange, `k2` teal, `k3` blue, `k4` violet, `k7` amber) for
  content, one meaning each per book.

## Reference part

```html
<ol class="check">
  <li>Question…</li>
</ol>
<!-- Self-check -->
<ol class="answers">
  <li>Answer… (1.3; slide 62)</li>
</ol>
<div class="items">
  <p><b>Term</b>: definition.</p>
</div>
<!-- Glossary -->
<div data-generate="figure-index"></div>
```
