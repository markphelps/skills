"""Independent parser: struct + json only, no safetensors import.
Prints the layout of a file and returns it as a dict. Run: python3 parse.py specimens/tiny.safetensors"""
import json, struct, sys
BITS = {"BOOL":8,"U8":8,"I8":8,"F8_E5M2":8,"F8_E4M3":8,"F8_E8M0":8,"F8_E4M3FNUZ":8,"F8_E5M2FNUZ":8,"I16":16,"U16":16,"F16":16,"BF16":16,
        "I32":32,"U32":32,"F32":32,"C64":64,"F64":64,"I64":64,"U64":64,"F4":4,"F6_E2M3":6,"F6_E3M2":6}
def parse(path):
    b = open(path, "rb").read()
    (n,) = struct.unpack("<Q", b[:8])
    raw = b[8:8 + n]
    hdr = json.loads(raw)
    meta = hdr.pop("__metadata__", None)
    pad = len(raw) - len(raw.rstrip(b" "))
    tensors = sorted(hdr.items(), key=lambda kv: kv[1]["data_offsets"])
    rows = []
    for name, t in tensors:
        s, e = t["data_offsets"]
        nel = 1
        for d in t["shape"]: nel *= d
        assert e - s == nel * BITS[t["dtype"]] // 8, name
        rows.append(dict(name=name, dtype=t["dtype"], shape=t["shape"], begin=s, end=e, abs_begin=8 + n + s, abs_end=8 + n + e, nbytes=e - s))
    data_len = rows[-1]["end"] if rows else 0
    assert 8 + n + data_len == len(b)
    return dict(path=path, file_size=len(b), n=n, json_len=n - pad, pad=pad, data_start=8 + n, data_len=data_len, metadata=meta, tensors=rows, header_order=list(hdr.keys()), raw=raw)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = parse(p)
        print(f"== {p}\nfile_size={r['file_size']} N={r['n']} json_len={r['json_len']} pad={r['pad']} data_start={r['data_start']} data_len={r['data_len']}")
        print("metadata:", r["metadata"]); print("header key order:", r["header_order"][:12], "..." if len(r["header_order"]) > 12 else "")
        for t in r["tensors"][:40]:
            print(f"  {t['name']:34s} {t['dtype']:5s} {str(t['shape']):14s} rel [{t['begin']:>10},{t['end']:>10})  abs [{t['abs_begin']:>10},{t['abs_end']:>10})  {t['nbytes']:>10} B")
        if len(r["tensors"]) > 40: print(f"  ... {len(r['tensors'])-40} more")
