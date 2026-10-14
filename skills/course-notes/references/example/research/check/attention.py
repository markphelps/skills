"""Check kit for CME 295 Lecture 1 notes.

Everything numeric in the notes comes from this script's output (research/captures/*.json).
Two kinds of numbers:
  * paper values  - from Vaswani et al. 2017 (base model), recomputed here (d_k = d_model / h, parameter counts)
  * toy values    - a 6-token example built by hand so that the two heads behave in a readable way.
                    Real heads are learned and are rarely this clean; the notes say so.
Run: python3 research/check/attention.py
"""
import json, math, os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "captures")
os.makedirs(OUT, exist_ok=True)
r = lambda a, n=3: np.round(np.asarray(a, dtype=float), n).tolist()


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.T / math.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    w = softmax(scores)
    return w @ V, scores, w


# ---------------------------------------------------------------- 1. paper values (base model)
d_model, h, N, d_ff = 512, 8, 6, 2048
d_k = d_v = d_model // h
paper = {
    "d_model": d_model, "h": h, "N": N, "d_ff": d_ff, "d_k": d_k, "d_v": d_v,
    "attn_params_per_layer": 3 * h * d_model * d_k + h * d_v * d_model,   # W_Q, W_K, W_V for all heads + W_O
    "ffn_params_per_layer": 2 * d_model * d_ff,                            # two linear maps, biases ignored
    "label_smoothing": 0.1, "dropout": 0.1,
}
paper["one_big_head_params"] = 3 * d_model * d_model + d_model * d_model
json.dump(paper, open(f"{OUT}/paper.json", "w"), indent=1)

# ---------------------------------------------------------------- 2. toy single query: "teddy bear" attends
tokens = ["a", "cute", "teddy bear", "is", "reading", "."]
# 4 features per token: [adjective-ness, noun-ness, verb-ness, function-word-ness]
X = np.array([
    [0.0, 0.0, 0.0, 1.0],   # a
    [1.0, 0.1, 0.0, 0.0],   # cute
    [0.1, 1.0, 0.0, 0.0],   # teddy bear
    [0.0, 0.0, 0.3, 0.8],   # is
    [0.0, 0.1, 1.0, 0.0],   # reading
    [0.0, 0.0, 0.0, 0.6],   # .
])
# head 1: a noun's query looks for adjectives ("which word describes me?")
WQ1 = np.array([[0, 0], [2, 0], [0, 0], [0, 0]], float)
WK1 = np.array([[2, 0], [0, 0], [0, 0], [0, 0]], float)
# head 2: a noun's query looks for verbs ("what am I doing?")
WQ2 = np.array([[0, 0], [2, 0], [0, 0], [0, 0]], float)
WK2 = np.array([[0, 0], [0, 0], [2, 0], [0, 0]], float)
WV1 = np.array([[1, 0], [0, 0], [0, 1], [0, 0]], float)   # value keeps (adjective, verb) features
WV2 = WV1.copy()

q_tb = 2  # index of "teddy bear"
single = {}
for name, WQ, WK, WV in [("head1", WQ1, WK1, WV1), ("head2", WQ2, WK2, WV2)]:
    Q, K, V = X @ WQ, X @ WK, X @ WV
    out, scores, w = attention(Q[q_tb:q_tb + 1], K, V)
    single[name] = {"q": r(Q[q_tb]), "K": r(K), "V": r(V), "scores": r(scores[0]),
                    "weights": r(w[0]), "output": r(out[0]),
                    "top": tokens[int(np.argmax(w[0]))]}
# what one head over the full 4 dims would do with both query directions mixed
WQb = np.array([[0, 0], [2, 2], [0, 0], [0, 0]], float) / math.sqrt(2)
WKb = np.array([[2, 0], [0, 0], [0, 2], [0, 0]], float) / math.sqrt(2)
_, sb, wb = attention((X @ WQb)[q_tb:q_tb + 1], X @ WKb, X @ WV1)
single["one_head_mixed"] = {"weights": r(wb[0]), "top2": [tokens[i] for i in np.argsort(-wb[0])[:2]]}
single["tokens"] = tokens
single["X"] = r(X, 2)
json.dump(single, open(f"{OUT}/toy_attention.json", "w"), indent=1)

# ---------------------------------------------------------------- 3. multi-head shapes on the toy
Wo = np.eye(4)
heads = []
for WQ, WK, WV in [(WQ1, WK1, WV1), (WQ2, WK2, WV2)]:
    out, _, _ = attention(X @ WQ, X @ WK, X @ WV)
    heads.append(out)
concat = np.concatenate(heads, axis=1)             # 6 x 4
mha = concat @ Wo
json.dump({"head_out_shape": list(heads[0].shape), "concat_shape": list(concat.shape),
           "mha_shape": list(mha.shape), "teddy_bear_concat": r(concat[q_tb])},
          open(f"{OUT}/toy_mha.json", "w"), indent=1)

# ---------------------------------------------------------------- 4. training vs inference (decoder)
rng = np.random.default_rng(0)
target = ["[BOS]", "Un", "ours", "en", "peluche", "mignon", "lit"]   # decoder input at training time
labels = ["Un", "ours", "en", "peluche", "mignon", "lit", "[EOS]"]    # what each position must predict
T, d = len(target), 8
Y = rng.normal(size=(T, d))
Wq, Wk, Wv = (rng.normal(size=(d, d)) / math.sqrt(d) for _ in range(3))
causal = np.tril(np.ones((T, T), bool))

# training: one pass over all positions, causal mask
train_out, _, train_w = attention(Y @ Wq, Y @ Wk, Y @ Wv, mask=causal)

# inference: one position at a time, recomputing over the prefix, then with a KV cache
step_out, kcache, vcache = [], [], []
for t in range(T):
    o, _, _ = attention((Y[:t + 1] @ Wq)[-1:], Y[:t + 1] @ Wk, Y[:t + 1] @ Wv)
    step_out.append(o[0])
    kcache.append(Y[t] @ Wk); vcache.append(Y[t] @ Wv)
cache_out = [attention((Y[t] @ Wq)[None], np.array(kcache[:t + 1]), np.array(vcache[:t + 1]))[0][0] for t in range(T)]

p_correct = 0.4     # toy probability for the correct first word
eps, V_toy = 0.1, 10
smoothed = [(1 - eps) + eps / V_toy, eps / V_toy]
tvi = {
    "target_in": target, "labels": labels, "mask": causal.astype(int).tolist(),
    "max_diff_train_vs_steps": float(np.abs(train_out - np.array(step_out)).max()),
    "max_diff_steps_vs_cache": float(np.abs(np.array(step_out) - np.array(cache_out)).max()),
    "dots_training_pass_computed": T * T, "dots_training_pass_used": int(causal.sum()),
    "dots_inference_no_cache": int(sum((t + 1) ** 2 for t in range(T))),
    "dots_inference_with_cache": int(sum(t + 1 for t in range(T))),
    "forward_passes_training": 1, "forward_passes_inference": T,
    "ce_loss_example": {"p": p_correct, "loss": round(-math.log(p_correct), 3)},
    "ce_loss_if_p_0_9": round(-math.log(0.9), 3),
    "label_smoothing_example": {"eps": eps, "V": V_toy, "correct": round(smoothed[0], 3), "each_other": round(smoothed[1], 3)},
    "masked_weights_row_lit": r(train_w[T - 1], 2), "masked_weights_row_ours": r(train_w[2], 2),
}
json.dump(tvi, open(f"{OUT}/train_vs_inference.json", "w"), indent=1)

print(json.dumps({"paper": paper, "head1_top": single["head1"]["top"], "head2_top": single["head2"]["top"],
                  "head1_w": single["head1"]["weights"], "head2_w": single["head2"]["weights"],
                  "mixed": single["one_head_mixed"], "tvi": {k: v for k, v in tvi.items() if k.startswith(("max", "dots", "forward", "ce", "label"))}}, indent=1))
