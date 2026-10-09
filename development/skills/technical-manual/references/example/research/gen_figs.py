"""Generate HTML fragments (hex dumps, strips) for the manual from the specimen bytes.
Output: research/figs/*.html, pulled into manual/src/*.html by assemble.py. Run: python3 gen_figs.py"""
import os, sys, html, struct
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from parse import parse
S, F = f"{H}/specimens", f"{H}/figs"; os.makedirs(F, exist_ok=True)

def hexdump(b, klass, start=0, base=0, mark=None):
    """b: bytes to show; klass(abs_offset)->css class; base: absolute offset of b[0]; rows start on 16-byte lines."""
    rows = []
    first = (base // 16) * 16
    end = base + len(b)
    for row in range(first, end, 16):
        cells, asc = [], []
        for o in range(row, row + 16):
            if o < base or o >= end:
                cells.append('<b style="visibility:hidden">00</b>'); asc.append(" ")
            else:
                v = b[o - base]
                cells.append(f'<b class="{klass(o)}">{v:02x}</b>')
                asc.append(html.escape(chr(v)) if 32 <= v < 127 else "·")
        rows.append(f'<div><i>{row:06x}</i>{"".join(cells)}<u>{"".join(asc)}</u></div>')
    return '<div class="hex">\n' + "\n".join(rows) + "\n</div>"

def region_class(r):
    raw = r["raw"]; n = r["n"]
    ms = raw.find(b'"__metadata__"'); me = -1
    if ms >= 0:
        me = raw.index(b"}", ms) + 1
    def k(o):
        if o < 8: return "k1"
        if o < 8 + r["json_len"]:
            return "k3" if ms >= 0 and 8 + ms <= o < 8 + me else "k2"
        if o < 8 + n: return "k0"
        return "k4"
    return k

def write(name, s):
    open(f"{F}/{name}.html", "w").write(s + "\n"); print("wrote", name, len(s))

tiny = open(f"{S}/tiny.safetensors", "rb").read(); rt = parse(f"{S}/tiny.safetensors")
write("hex-tiny", hexdump(tiny, region_class(rt)))
write("hex-tiny-head", hexdump(tiny[:16], region_class(rt)))
mixed = open(f"{S}/mixed.safetensors", "rb").read(); rm = parse(f"{S}/mixed.safetensors")
write("hex-mixed-head", hexdump(mixed[:64], region_class(rm)))
# data section of mixed: alternate two shades by tensor so boundaries show: use k4 for data, and outline by tensor index parity via extra class
def kdata(o):
    for i, t in enumerate(rm["tensors"]):
        if t["abs_begin"] <= o < t["abs_end"]: return "k4" if i % 2 == 0 else "k4 alt"
    return region_class(rm)(o)
write("hex-mixed-data", hexdump(mixed[512:], kdata, base=512))
mlp = open(f"{S}/mlp.safetensors", "rb").read(); rp = parse(f"{S}/mlp.safetensors")
write("hex-mlp-head", hexdump(mlp[:80], region_class(rp)))
# first row of layer.0.weight
t = [x for x in rp["tensors"] if x["name"] == "layer.0.weight"][0]
write("hex-mlp-l0", hexdump(mlp[t["abs_begin"]:t["abs_begin"] + 32], lambda o: "k4", base=t["abs_begin"]))
print("layer.0.weight abs_begin", t["abs_begin"], "first 4 floats", struct.unpack("<4f", mlp[t["abs_begin"]:t["abs_begin"] + 16]))
print("mixed header text:", rm["raw"].decode())
print("mlp header text:", rp["raw"].decode())

# ---- source excerpts, copied from the pinned checkout -----------------------------------------
import subprocess
R = f"{H}/src"
COMMIT = subprocess.run(["git", "-C", R, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True).stdout.strip()
def excerpt(name, path, ranges, lang, title=None):
    lines = open(f"{R}/{path}").read().split("\n")
    parts = ["\n".join(lines[a - 1:b]) for a, b in ranges]
    body = "\n    …\n".join(parts)
    loc = ", ".join(f"{a}–{b}" for a, b in ranges)
    write(name, f'<pre class="listing" data-name="{title or os.path.basename(path)}" data-src="{path}:{loc} @ {COMMIT}" data-lang="{lang}">\n{html.escape(body, quote=False)}\n</pre>')
excerpt("src-read-metadata", "safetensors/src/tensor.rs", [(390, 425)], "rust", "read_metadata")
excerpt("src-validate", "safetensors/src/tensor.rs", [(627, 631), (637, 664)], "rust", "Metadata::validate")
excerpt("src-prepare", "safetensors/src/tensor.rs", [(227, 255)], "rust", "prepare")
excerpt("src-structs", "safetensors/src/tensor.rs", [(538, 546), (795, 806)], "rust", "HashMetadata, TensorInfo")
excerpt("src-tryfrom", "safetensors/src/tensor.rs", [(550, 559)], "rust", "TryFrom<HashMetadata>")
excerpt("src-write-file", "safetensors/src/tensor.rs", [(309, 315), (326, 341)], "rust", "buffered_write_to_file")
excerpt("src-get-tensor", "bindings/python/src/lib.rs", [(1162, 1177)], "rust", "Open::get_tensor")
excerpt("src-open", "bindings/python/src/lib.rs", [(786, 794), (814, 824)], "rust", "Open::new")
excerpt("src-flatten", "bindings/python/py_src/safetensors/numpy.py", [(10, 25)], "python", "numpy._flatten")
excerpt("src-consts", "safetensors/src/tensor.rs", [(10, 11)], "rust", "constants")
excerpt("src-pread", "bindings/python/src/lib.rs", [(2119, 2131)], "rust", "PySafeSlice::__getitem__")
excerpt("src-torch-flatten", "bindings/python/py_src/safetensors/torch.py", [(575, 581)], "python", "torch._flatten_as_ptr")
