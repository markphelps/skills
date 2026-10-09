# Markup reference

Every component the kit styles. Fragments are plain HTML; the build adds
numbers, frames and headers.

## Data binding

Numbers and listings are read from captures at build time, so the prose cannot
drift from the data. A missing file or path is a build error.

```html
<!-- a value from a JSON capture; path is dotted (or a JSON pointer) -->
<span data-value="research/captures/tiny.json#header_len">64</span> bytes
<span data-value="research/captures/tiny.json#tensors.0.offsets"></span>
<!-- data-format: int (thousands separators), hex, bytes (KiB/MiB), pct (0.0003 → 0.03%), fixed2 -->
<span data-value="research/captures/sizes.json#total" data-format="int"></span>

<!-- lines of a text capture or source file; data-src is filled in for listings that lack one -->
<pre
  class="listing"
  data-name="parse.py output"
  data-include="research/captures/parse.txt"
  data-lines="2-4"
  data-lang="text"
></pre>
<pre class="term" data-include="research/captures/curl-head.txt"></pre>

<!-- a generated fragment (hex dump, sequence diagram, strip): written by a script, pulled in whole -->
<!--#include research/figs/hex-tiny.html-->
```

Bind every number that came from a capture. A number you can only state by
reading code (a constant, a limit) is cited with `<cite>` instead.

```html
<!-- inline -->
<code>general.alignment</code> <cite>src/gguf.cpp:228–254</cite>
<cite>spec §5.2</cite> <a class="xref" href="#id">text</a>
<!-- <cite> goes at the end of the clause it supports; <span class="src"> is the same style -->

<!-- byte strip: flex sets relative width -->
<div class="strip">
  <div class="k1" style="flex:.6">magic<small>4 B</small></div>
  <div class="k2" style="flex:3">metadata<small>1.71 MB</small></div>
  <div class="k0 hatch gap"></div>
  <div class="k4" style="flex:2">tensor data</div>
  <div class="more">…</div>
</div>
<div class="strip-labels">
  <span>one sequential read</span><span class="r">aligned to 32</span>
</div>

<!-- hex dump: 16 <b> per row, hex offsets; class "x" hides a cell in a partial row; generate with figs.hexdump -->
<div class="hex">
  <div><i>000000</i><b class="k1">47</b>…<u>GGUF············</u></div>
</div>

<!-- cells: --cw sets cell width (multi-byte groups), --lbl the label column -->
<div class="cells" style="--lbl:48pt">
  <span class="lbl">q</span><b class="k3">7</b><b>4</b><span class="sp"></span
  ><b class="k6">10</b>
</div>

<!-- any coloured box: add "alt" for a second shade of the same colour (adjacent items of one kind) -->
<b class="k4 alt">3f</b>

<!-- boxes without arrows -->
<div class="flow" style="--cols:3">
  <div class="k2"><b>prepare</b><small>sort, offsets, JSON</small></div>
  …
</div>

<!-- colour-code key, front matter -->
<div class="swatches">
  <div class="k1"><b>k1</b>header fields</div>
  <div class="k2"><b>k2</b>metadata</div>
  …
</div>

<!-- bars: --w is the bar length; choose and state the scale -->
<div class="bars" style="--label:34%">
  <div>
    <span>Llama-3.2-1B Q4_K_M</span>
    <div><b class="k2" style="--w:84%"></b><i>7.83 MB</i></div>
  </div>
</div>

<!-- inside a figure -->
<div class="fig-sub">First 32 bytes</div>
<div class="fig-note">Any failure returns NULL.</div>
<div class="legend">
  <span class="k1">fixed header</span><span class="k2">key</span>
</div>

<!-- table: mono header labels are automatic; .n right-aligns numbers, .m sets mono -->
<table>
  <thead>
    <tr>
      <th>Offset</th>
      <th>Field</th>
      <th class="n">Bytes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="m">0</td>
      <td>magic</td>
      <td class="n">4</td>
    </tr>
  </tbody>
</table>
<p class="note">Values 4–6 are removed. The spec's own list stops at 18.</p>
<!-- outcome cells in accept/reject tables -->
<td class="ok">accepted</td>
<td class="bad">rejected</td>

<!-- source excerpt or program; data-src is required -->
<pre
  class="listing"
  data-name="column_writer.cc"
  data-src="arrow/cpp/src/parquet/column_writer.cc:1036 @ beccec0"
  data-lang="cpp"
>
…escaped code…
</pre>
<p class="note">Two long lines are wrapped; nothing else is changed.</p>

<!-- command and its output -->
<pre class="term">
$ curl -sL -r 114468224-114468241 https://…/file.gguf | xxd</pre
>
<pre class="out">saved answer: [{"type":"text","text":"Paris."}]</pre>

<!-- callouts -->
<div class="callout footgun" data-label="Footgun"><p>…</p></div>
<div class="callout verify" data-label="Verify"><p>…</p></div>
<div class="callout rule" data-label="Rule of thumb"><p>…</p></div>
<div class="callout why" data-label="Why it matters for the Hub"><p>…</p></div>
<div class="callout takeaway" data-label="What this means for you">
  <ul>
    <li>…</li>
  </ul>
</div>
<div class="callout experimental" data-label="Experimental"><p>…</p></div>
<div class="callout unverified" data-label="Unverified">
  <p>What could not be checked, and why.</p>
</div>
<div class="callout doc" data-label="Doc ≠ code">
  <p>What the docs say, what the code does, both cited.</p>
</div>

<!-- the one rule a section rests on, quoted whole -->
<blockquote class="rule" data-label="Core rule">
  “Successful streams emit <code>start</code> before …”
  <cite>ai/types.ts:753</cite>
</blockquote>

<!-- a tree in text (session files, schemas); d1..d6 indent; <i> is a grey note -->
<div class="tree">
  <div>header · session 01a1 <i>line 1 · not an entry</i></div>
  <div class="d1">└ f99f · thinking_level_change <i>line 3</i></div>
</div>

<!-- walk-through after a numbered figure -->
<div class="steps">
  <p>
    <b>1 · Submit.</b> The editor's <code>onSubmit</code> …
    <cite>interactive-mode.ts:1247</cite>
  </p>
</div>

<!-- in the Reference part -->
<div data-generate="figure-index"></div>
```

Callouts are rare, a few per part, and each kind has one job. **Footgun**: a
trap that gives wrong results without an error, with the exact values that
collide. **Verify**: the command that re-derives what the section just showed.
**Rule of thumb**: a decision the reader can apply without rereading. **Why it
matters**: the consequence for the reader's angle. **What this means for you**:
three or four imperative bullets closing a section of a library manual.
**Experimental**: a stability warning quoted from the project. **Unverified**: a
claim worth keeping that could not be checked, with the reason; it also goes in
the Reference list. **Doc ≠ code**: the shipped documentation and the source
disagree; give both, and collect every one in a "Documentation versus code"
table in the Reference part.

Escape `<`, `>` and `&` in listings. Long tables break across pages; figures,
listings and callouts do not, so keep each under about two thirds of a page and
split larger ones into two figures. Put book-specific CSS (cover-plate type
sizes, a numbered key) in `manual/extra.css`.

## Generated figures (`kit/figs.py`)

Write a small script per figure under `research/figs/` that reads a capture and
calls one of these, then include the output. Re-running the capture and the
script regenerates the figure.

```python
import sys, json; sys.path.insert(0, "kit"); import figs
cap = json.load(open("research/captures/tiny.json"))
open("research/figs/strip-tiny.html", "w").write(figs.strip(
    [("N", 8, "k1", "8 B"), ("JSON header", cap["header_len"], "k2", f'{cap["header_len"]} B'),
     ("data", cap["data_len"], "k4", f'{cap["data_len"]} B')]))
open("research/figs/hex-tiny.html", "w").write(figs.hexdump(open(cap["path"], "rb").read(),
    lambda o: "k1" if o < 8 else "k2" if o < 8 + cap["header_len"] else "k4"))
```

| Function                                     | Makes                                                                                                       |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `hexdump(data, klass, base)`                 | 16-byte rows from an absolute offset; `klass(offset)` colours each byte                                     |
| `strip(regions, min_frac)`                   | a byte strip with widths proportional to real sizes; `min_frac` widens tiny boxes (then say "not to scale") |
| `bars(rows, label_width, klass, fmt, scale)` | a measured bar chart; pass `scale` for log scales and say so in `data-tag`                                  |
| `sequence(participants, steps)`              | a sequence diagram laid out from data: lifelines, numbered steps, self-calls, arrow kinds                   |
| `excerpt(repo, path, ranges, lang)`          | a listing cut from the pinned checkout, stamped with path, lines and commit                                 |

```python
figs.sequence(
  [("host", "host"), ("w", "serialize_to_file", "tensor.rs", "k2"), ("dst", "destination")],
  [{"from": "host", "to": "w", "call": "save_file(t, path)", "payload": "8 tensors", "n": 1},
   {"from": "w", "to": "w", "call": "prepare()", "payload": "sort, offsets, pad", "n": 2},
   {"from": "w", "to": "dst", "call": "persist(path)", "payload": "rename", "kind": "async", "n": 3},
   {"from": "w", "to": "host", "call": "Ok(())", "kind": "ret", "n": 4}])
```

## SVG

SVG conventions: `viewBox="0 0 640 H"` (640 = full frame width), no inline
colours or fonts. Use the classes: rect `k0`–`k7` or `box`; text default sans,
`m` mono, `s` small grey, `lab` spaced capitals, `t1`–`t7` coloured to match a
region; `ln` for plain lines. Arrows are `path.arrow` plus one kind, each with
one meaning book-wide:

| Class                   | Means                                        |
| ----------------------- | -------------------------------------------- |
| `arrow`                 | a call or a step that happens                |
| `arrow ret` (or `dash`) | a return, or an inferred or optional step    |
| `arrow async`           | asynchronous, eventual, or in the background |
| `arrow err`             | the failure path                             |
| `arrow data`            | bulk bytes moving (a write, a copy, a fetch) |
| `arrow soft`            | context, not the point of the figure         |

Sequence diagrams: lifeline boxes across the top, dashed lifelines, horizontal
arrows labelled above with the call and below in `s` with the payload, circled
step numbers down the left that the prose and tables refer to. A step a
participant performs on itself is a short loop arrow on its own lifeline with
the label to the right, clear of the next lifeline.

In SVG, the build flags labels that overlap each other or run outside the
drawing. It does not see a label crossing a line or sitting on the wrong box, so
look at every diagram.
