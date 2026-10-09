"""Create the specimen files used throughout the manual.
Written with the reference library built from the pinned commit (safetensors 0.9.0-dev.0 @ e246a25).
Deterministic: fixed seeds, no timestamps. Run: python3 make_specimens.py"""
import hashlib, os, numpy as np, safetensors
from safetensors.numpy import save_file
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specimens")
os.makedirs(D, exist_ok=True)

# 1. tiny: the smallest useful file, one 2x2 int32 tensor.
save_file({"test": np.arange(4, dtype=np.int32).reshape(2, 2)}, f"{D}/tiny.safetensors")

# 2. mixed: every awkward case in one small file.
rng = np.random.default_rng(7)
mixed = {
    "bias":   np.array([0.5, -1.0, 2.0], dtype=np.float32),
    "alpha":  np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64),
    "ids":    np.array([10, 20, 30], dtype=np.int64),
    "half":   np.array([1.0, -2.0], dtype=np.float16),
    "mask":   np.array([True, False, True, True, False]),
    "bytes":  np.array([1, 2, 3], dtype=np.uint8),
    "scalar": np.array(3.25, dtype=np.float32),
    "empty":  np.zeros((0, 4), dtype=np.float32),
}
save_file(mixed, f"{D}/mixed.safetensors", metadata={"format": "np", "note": "specimen"})

# 3. mlp: a model-shaped file, 6 float32 tensors, about 2.2 MB.
rng = np.random.default_rng(42)
mlp = {
    "embed.weight":    rng.standard_normal((1000, 256), dtype=np.float32),
    "layer.0.weight":  rng.standard_normal((512, 256), dtype=np.float32),
    "layer.0.bias":    rng.standard_normal((512,), dtype=np.float32),
    "layer.1.weight":  rng.standard_normal((256, 512), dtype=np.float32),
    "layer.1.bias":    rng.standard_normal((256,), dtype=np.float32),
    "head.weight":     rng.standard_normal((10, 256), dtype=np.float32),
    "head.bias":       rng.standard_normal((10,), dtype=np.float32),
    "step":            np.array(1200, dtype=np.int64),
}
save_file(mlp, f"{D}/mlp.safetensors", metadata={"format": "np"})

# 4. wide: many tensors, to measure header growth (200 tensors of 64 float32).
rng = np.random.default_rng(3)
wide = {f"blocks.{i:03d}.attn.q_proj.weight": rng.standard_normal((8, 8), dtype=np.float32) for i in range(200)}
save_file(wide, f"{D}/wide.safetensors")

# 5. big: 256 MiB of float32 in 16 tensors, for load timings.
rng = np.random.default_rng(5)
big = {f"w{i:02d}": rng.standard_normal((4096, 1024), dtype=np.float32) for i in range(16)}
save_file(big, f"{D}/big.safetensors")

print("library", safetensors.__version__, "numpy", np.__version__)
for f in sorted(os.listdir(D)):
    p = f"{D}/{f}"; b = open(p, "rb").read()
    print(f"{f:22s} {len(b):>11,d} bytes  sha256 {hashlib.sha256(b).hexdigest()[:16]}")
