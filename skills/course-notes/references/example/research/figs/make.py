"""Figures for the Lecture 1 notes, drawn from research/captures/*.json (run check/attention.py first)."""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for kit in (os.path.join(HERE, "..", "..", "kit"), os.path.join(HERE, "..", "..", "..", "kit")):  # kit inside or beside the notes folder
    sys.path.insert(0, kit)
import figs  # noqa: E402

C = os.path.join(HERE, "..", "captures")
att = json.load(open(f"{C}/toy_attention.json"))
tvi = json.load(open(f"{C}/train_vs_inference.json"))
toks = att["tokens"]


def write(name, s):
    open(os.path.join(HERE, name + ".html"), "w").write(s + "\n")


def query_fan(weights, klass, label):
    """Slide 60 redrawn: every key wired to the query, line width = attention weight."""
    W, box_y, q_y = 640, 18, 118
    widths = [max(46, 9 + 5.6 * len(t)) for t in toks]
    gap = (W - sum(widths)) / (len(toks) + 1)
    xs, x = [], gap
    for w in widths:
        xs.append(x + w / 2); x += w + gap
    qx = xs[2]
    out = [f'<svg viewBox="0 0 {W} 150">']
    for i, (t, w, cx) in enumerate(zip(toks, widths, xs)):
        k = klass if i == max(range(len(toks)), key=lambda j: weights[j]) else "box"
        out.append(f'<rect class="{k}" x="{cx - w / 2:.1f}" y="{box_y}" width="{w:.1f}" height="22"/>')
        out.append(f'<text x="{cx:.1f}" y="{box_y + 15}" text-anchor="middle" class="m">{html.escape(t)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{box_y + 36}" text-anchor="middle" class="s">w = {weights[i]:.2f}</text>')
        out.append(f'<path class="ln" style="stroke-width:{0.4 + 6 * weights[i]:.2f}" d="M{cx:.1f} {box_y + 42} L{qx:.1f} {q_y - 12}"/>')
    out.append(f'<rect class="k5" x="{qx - 52:.1f}" y="{q_y - 12}" width="104" height="22"/>')
    out.append(f'<text x="{qx:.1f}" y="{q_y + 3}" text-anchor="middle" class="m t5">q · teddy bear</text>')
    out.append(f'<text x="{W - 4}" y="{q_y + 3}" text-anchor="end" class="lab">{html.escape(label)}</text>')
    out.append("</svg>")
    return "\n".join(out)


write("fan-head1", query_fan(att["head1"]["weights"], "k1", "head 1 · looks for describers"))
write("fan-head2", query_fan(att["head2"]["weights"], "k2", "head 2 · looks for actions"))

write("bars-heads", "\n".join([
    '<div class="fig-sub">Head 1: query from "teddy bear", keys look for adjectives</div>',
    figs.bars(list(zip(toks, att["head1"]["weights"])), label_width="22%", klass="k1", fmt=lambda v: f"{v:.3f}"),
    '<div class="fig-sub">Head 2: same query word, keys look for verbs</div>',
    figs.bars(list(zip(toks, att["head2"]["weights"])), label_width="22%", klass="k2", fmt=lambda v: f"{v:.3f}"),
    '<div class="fig-sub">One head asked to do both</div>',
    figs.bars(list(zip(toks, att["one_head_mixed"]["weights"])), label_width="22%", klass="k0", fmt=lambda v: f"{v:.3f}"),
]))

# causal mask as a grid of cells, rows = the position doing the attending
rows = ['<div class="cells" style="--lbl:44pt;--cw:30pt"><span class="lbl"></span>' +
        "".join(f'<span class="lbl" style="min-width:30pt;text-align:center;font-size:6.2pt">{html.escape(t)}</span>' for t in tvi["target_in"]) + "</div>"]
for i, t in enumerate(tvi["target_in"]):
    cells = "".join(f'<b class="{"k6" if m else "k0 hatch"}">{"✓" if m else ""}</b>' for m in tvi["mask"][i])
    rows.append(f'<div class="cells" style="--lbl:44pt;--cw:30pt"><span class="lbl">{html.escape(t)}</span>{cells}'
                f'<span class="lbl" style="min-width:60pt;padding-left:8pt">→ {html.escape(tvi["labels"][i])}</span></div>')
write("mask", "\n".join(rows))
print("wrote", sorted(f for f in os.listdir(HERE) if f.endswith(".html")))
