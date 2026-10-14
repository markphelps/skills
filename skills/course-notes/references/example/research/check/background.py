"""Check kit for the Background part (level 2): the hand-sized numbers the math primer uses.

Reuses the toy sentence of attention.py, so the same vectors appear in the primer and in 1.3.
Run: python3 research/check/background.py   ->  research/captures/background.json
"""
import json, math, os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "captures")
os.makedirs(OUT, exist_ok=True)
r = lambda a, n=3: np.round(np.asarray(a, dtype=float), n).tolist()

tokens = ["a", "cute", "teddy bear", "is", "reading", "."]
X = np.array([[0.0, 0.0, 0.0, 1.0], [1.0, 0.1, 0.0, 0.0], [0.1, 1.0, 0.0, 0.0],
              [0.0, 0.0, 0.3, 0.8], [0.0, 0.1, 1.0, 0.0], [0.0, 0.0, 0.0, 0.6]])
cute, teddy, reading = X[1], X[2], X[4]

# 0.2 dot product: multiply position by position, add up
dot = {
    "small": {"a": [1, 2], "b": [3, 1], "products": [3, 2], "value": 1 * 3 + 2 * 1},
    "cute_teddy": round(float(cute @ teddy), 3),
    "cute_cute": round(float(cute @ cute), 3),
    "cute_reading": round(float(cute @ reading), 3),
    "cute_teddy_products": r(cute * teddy),
}

# 0.3 matrices: the query of "teddy bear" is its row of X times W_Q (head 1 of attention.py)
WQ1 = np.array([[0, 0], [2, 0], [0, 0], [0, 0]], float)
Q = X @ WQ1
mat = {
    "X_shape": list(X.shape), "W_shape": list(WQ1.shape), "Q_shape": list(Q.shape),
    "teddy_row": r(teddy), "W": r(WQ1), "teddy_query": r(Q[2]),
    "teddy_query_col0_terms": r(teddy * WQ1[:, 0]),
    "KT_shape": [2, 6], "QKT_shape": [6, 6], "QKT_entries": 36,
}

# 0.4 exponent and softmax, on the scaled scores of 1.3
scores = np.array([0.0, 2 * 2 / math.sqrt(2), 2 * 0.2 / math.sqrt(2), 0.0, 0.0, 0.0])
e = np.exp(scores)
sm = e / e.sum()
small = np.array([2.0, 1.0, 0.0])
se = np.exp(small)
softmax = {
    "small_scores": r(small), "small_exp": r(se), "small_sum": round(float(se.sum()), 3),
    "small_weights": r(se / se.sum()),
    "scores": r(scores), "exp": r(e), "sum": round(float(e.sum()), 3), "weights": r(sm),
    "weights_sum": round(float(sm.sum()), 3),
    "sqrt2": round(math.sqrt(2), 3),
}

# 0.5 a layer and one step of training (gradient descent on one weight)
x, target, w0, lr = 2.0, 6.0, 1.0, 0.05
pred0 = w0 * x
loss0 = (pred0 - target) ** 2
grad = 2 * (pred0 - target) * x
w1 = w0 - lr * grad
loss1 = (w1 * x - target) ** 2
steps = [w0]
w = w0
for _ in range(20):
    w = w - lr * 2 * (w * x - target) * x
    steps.append(round(w, 4))
relu = {"inputs": [-1.5, 0.0, 2.0], "outputs": [max(0.0, v) for v in [-1.5, 0.0, 2.0]]}
train = {"x": x, "target": target, "w0": w0, "pred0": pred0, "loss0": loss0, "grad": grad,
         "lr": lr, "w1": round(w1, 3), "pred1": round(w1 * x, 3), "loss1": round(loss1, 3),
         "w_after_20": round(steps[-1], 3), "best_w": target / x, "relu": relu}

# 0.6 log and cross-entropy
ce = {f"p_{str(p).replace('.', '_')}": round(-math.log(p), 3) for p in [1.0, 0.9, 0.4, 0.1, 0.01]}
ce["p_1_0"] = 0.0

# 1.3 why divide by sqrt(d_k): spread of q . k for random vectors (mean 0, variance 1 parts)
rng = np.random.default_rng(0)
spread = []
for d in [2, 16, 64]:
    q = rng.standard_normal((20000, d)); k = rng.standard_normal((20000, d))
    dots = (q * k).sum(1)
    spread.append({"d": d, "std": round(float(dots.std()), 2), "std_scaled": round(float((dots / math.sqrt(d)).std()), 2),
                   "sqrt_d": round(math.sqrt(d), 2)})

json.dump({"tokens": tokens, "spread": spread, "X": r(X), "dot": dot, "matrix": mat, "softmax": softmax,
           "train": train, "ce": ce}, open(f"{OUT}/background.json", "w"), indent=1)
print(json.dumps({"dot": dot, "matrix": mat["teddy_query"], "softmax": softmax["weights"],
                  "train": {k: train[k] for k in ["loss0", "grad", "w1", "loss1", "w_after_20"]}, "ce": ce}))
