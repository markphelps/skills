# Sources and versions

Ranked: the lecture's own slides first, then the course's study material, then
the paper the lecture teaches, then anything else.

| #   | Source                                                                                                | Version / date read                    | Used for                                                                                                              |
| --- | ----------------------------------------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| S1  | CME 295 Lecture 1 slides, `cme295.stanford.edu/slides/fall26-cme295-lecture1.pdf`                     | fall 2026, 118 slides, read 2026-10-13 | everything in Lecture 1; slide numbers cited as "slide n"                                                             |
| S2  | CME 295 Lecture 2 slides, `…/fall26-cme295-lecture2.pdf`                                              | fall 2026, 138 slides                  | encoder-only vs decoder-only (18–21), LLM characteristics (31–34), next-token prediction (90–96), MHA/GQA/MQA (80–83) |
| S3  | CME 295 VIP cheatsheet, github.com/afshinea/stanford-cme-295-transformers-large-language-models `en/` | commit c086dee (2026-09-13)            | attention formula wording, MHA, decoder-only, cross-entropy, prefill vs decode, KV caching                            |
| S4  | Vaswani et al., "Attention Is All You Need", arXiv:1706.03762                                         | v7                                     | equations (§3.2.1 Eq. 1, §3.2.2, §3.3, §3.5), base-model sizes, masking (§3.1, §3.2.3), regularization (§5.4)         |
| S5  | course syllabus, `cme295.stanford.edu/syllabus/`                                                      | read 2026-10-13                        | lecture dates and topics, recording link                                                                              |
| C1  | `research/check/attention.py` → `research/captures/*.json`                                            | run 2026-10-13, numpy 2.5.3            | every computed number: toy attention weights, head outputs, mask, pass and dot-product counts, loss values            |

Not used: the lecture recording (not readable here), the Super Study Guide book
(not available here; the cheatsheet summarises it).
