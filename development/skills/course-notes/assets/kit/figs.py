"""Generate figure fragments from real data, so no byte or source line is typed by hand.
Write the result to research/figs/<name>.html and pull it in with <!--#include research/figs/<name>.html-->."""
import html, os, subprocess

def hexdump(data: bytes, klass=lambda offset: "", base: int = 0) -> str:
    """16-byte rows from absolute offset `base`. klass(offset) returns the region class ("k1", "k2 alt", …)."""
    rows, first, end = [], (base // 16) * 16, base + len(data)
    for row in range(first, end, 16):
        cells, asc = [], []
        for o in range(row, row + 16):
            if o < base or o >= end:
                cells.append('<b class="x">00</b>'); asc.append(" ")
            else:
                v = data[o - base]
                cells.append(f'<b class="{klass(o)}">{v:02x}</b>')
                asc.append(html.escape(chr(v)) if 32 <= v < 127 else "·")
        rows.append(f'<div><i>{row:06x}</i>{"".join(cells)}<u>{"".join(asc)}</u></div>')
    return '<div class="hex">\n' + "\n".join(rows) + "\n</div>"

def excerpt(repo: str, path: str, ranges, lang: str, name: str = None) -> str:
    """Lines [(a, b), …] (1-based, inclusive) of a file in a checkout, as a listing stamped with path, lines and commit."""
    commit = subprocess.check_output(["git", "-C", repo, "rev-parse", "--short=7", "HEAD"], text=True).strip()
    lines = open(os.path.join(repo, path), encoding="utf-8").read().split("\n")
    body = "\n    …\n".join("\n".join(lines[a - 1:b]) for a, b in ranges)
    loc = ", ".join(f"{a}–{b}" for a, b in ranges)
    return (f'<pre class="listing" data-name="{name or os.path.basename(path)}" data-src="{path}:{loc} @ {commit}" '
            f'data-lang="{lang}">\n{html.escape(body, quote=False)}\n</pre>')

def bars(rows, label_width="34%", klass="k2", fmt=str, scale=None) -> str:
    """rows: [(label, value)] or [(label, value, klass)]. scale maps a value to 0..1 (default: linear to the max)."""
    top = max(r[1] for r in rows) or 1
    scale = scale or (lambda v: v / top)
    out = [f'<div class="bars" style="--label:{label_width}">']
    for r in rows:
        k = r[2] if len(r) > 2 else klass
        out.append(f'<div><span>{html.escape(str(r[0]))}</span><div><b class="{k}" style="--w:{max(scale(r[1]), 0.004) * 86:.1f}%"></b><i>{html.escape(fmt(r[1]))}</i></div></div>')
    return "\n".join(out) + "\n</div>"


def _w(text: str, mono: bool = False, size: float = 9.6) -> float:
    """Estimated rendered width in SVG px (kit fonts at the kit's default sizes)."""
    return len(text) * (0.585 if mono else 0.54) * size


def sequence(participants, steps, width: int = 640) -> str:
    """Sequence diagram laid out from data, so labels and lifelines cannot collide by hand-placement.

    participants: [(id, label), (id, label, sublabel), (id, label, sublabel, klass)]  klass: "box" or "k1".."k7"
    steps: [{"from": id, "to": id, "call": "submit()", "payload": "req-1", "kind": "call|ret|async|err|data",
             "n": 1}]   from == to draws a self-call loop. "n" (optional) prints a circled step number.
    Returns an <svg> for the body of a <figure class="fig">.
    """
    ps = [p + (None,) * (4 - len(p)) for p in participants]
    left = 30
    col = (width - left) / len(ps)
    x = {p[0]: left + col * (i + 0.5) for i, p in enumerate(ps)}
    head_h = 34 if any(p[2] for p in ps) else 24
    out, y = [], 6 + head_h + 16
    for pid, label, sub, k in ps:
        bw = min(col - 10, max(_w(label, True, 8.6), _w(sub or "", False, 8.4)) + 18)
        out.append(f'<rect class="{k or "box"}" x="{x[pid] - bw / 2:.1f}" y="6" width="{bw:.1f}" height="{head_h}"/>')
        out.append(f'<text x="{x[pid]:.1f}" y="{6 + (15 if sub else 16)}" text-anchor="middle" class="m" style="font-size:8.6px">{html.escape(label)}</text>')
        if sub:
            out.append(f'<text x="{x[pid]:.1f}" y="{6 + 27}" text-anchor="middle" class="s">{html.escape(sub)}</text>')
    rows = []
    for st in steps:
        a, b = x[st["from"]], x[st["to"]]
        kind = st.get("kind", "call")
        cls = "arrow" + ("" if kind == "call" else f" {kind}")
        call, payload = st.get("call", ""), st.get("payload")
        if st.get("n") is not None:
            rows.append(f'<circle cx="12" cy="{y:.1f}" r="7" class="box"/><text x="12" y="{y + 3:.1f}" text-anchor="middle" class="m" style="font-size:7.6px">{st["n"]}</text>')
        if a == b:   # self-call loop to the right of the lifeline
            rows.append(f'<path class="{cls}" d="M{a:.1f} {y - 6:.1f} h20 v12 h-18"/>')
            rows.append(f'<text x="{a + 26:.1f}" y="{y - 1:.1f}" class="m" style="font-size:8.4px">{html.escape(call)}</text>')
            if payload:
                rows.append(f'<text x="{a + 26:.1f}" y="{y + 10:.1f}" class="s">{html.escape(payload)}</text>')
            y += 32 if payload else 26
            continue
        mid = (a + b) / 2
        rows.append(f'<text x="{mid:.1f}" y="{y - 4:.1f}" text-anchor="middle" class="m" style="font-size:8.4px">{html.escape(call)}</text>')
        end = b - 2 if b > a else b + 2
        rows.append(f'<path class="{cls}" d="M{a:.1f} {y:.1f} H{end:.1f}"/>')
        if payload:
            rows.append(f'<text x="{mid:.1f}" y="{y + 11:.1f}" text-anchor="middle" class="s">{html.escape(payload)}</text>')
        y += 34 if payload else 24
    height = y + 4
    lines = [f'<path class="ln dash soft" d="M{x[p[0]]:.1f} {6 + head_h} V{height - 2:.1f}"/>' for p in ps]
    return (f'<svg viewBox="0 0 {width} {height:.0f}">\n' + "\n".join(out + lines + rows) + "\n</svg>")


def strip(regions, min_frac: float = 0.0) -> str:
    """Byte strip from real sizes. regions: [(label, size_bytes, klass), (label, size, klass, sublabel)].
    Widths are proportional to size. min_frac widens boxes narrower than that fraction of the total so their
    label fits; if any box was widened the strip is no longer to scale and the caption must say so."""
    total = sum(r[1] for r in regions) or 1
    cells, widened = [], False
    for r in regions:
        label, size, k = r[0], r[1], r[2]
        sub = r[3] if len(r) > 3 else None
        frac = size / total
        if frac < min_frac:
            frac, widened = min_frac, True
        small = f"<small>{html.escape(sub)}</small>" if sub else ""
        cells.append(f'<div class="{k}" style="flex:{frac:.5f}">{html.escape(label)}{small}</div>')
    note = "<!-- widened: not to scale -->" if widened else "<!-- to scale -->"
    return f'<div class="strip">{note}' + "".join(cells) + "</div>"
