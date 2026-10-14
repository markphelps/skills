# Finding the gaps

The gap ledger, `research/GAPS.md`, is the plan for the book. It is private: it
compares the student's pages with the slides, and the book never shows that
comparison. Every missing, thin and fix row becomes something on a page; every
ask row becomes a question in the conversation. Build it by walking the slides
with the transcript beside you.

## Walk the slides

For each slide or run of slides on one topic:

1. Is it in the notes? Find the transcript lines, or none.
2. If yes, does the note say what the slide says? Compare term by term:
   definitions, formulas, the order of steps, which component does what.
3. What does the slide show that the note leaves out? Formulas and figures are
   the usual omission; students write the words and skip the math.
4. Did the lecture assume something the notes never define? Prerequisites and
   earlier slides.

Then read the notes on their own:

- **Undefined terms**: a word used before it is explained (PE, head, mask).
- **Skipped steps**: a derivation or a pipeline with a jump in it.
- **Misplaced lines**: a statement under the wrong heading (a question that
  belongs to cross-attention written under the encoder).
- **Plausible but wrong**: the classic misconception for the topic. For a
  Transformer: "a head is the projection matrices", "the value is the token's
  embedding", "masking is needed at inference".

## Kinds

| Kind    | Means                                       | In the book                                                                     |
| ------- | ------------------------------------------- | ------------------------------------------------------------------------------- |
| missing | in the lecture, not in the notes            | an ordinary section or paragraph, cited to the slides                           |
| thin    | in the notes, but too short to study from   | the full treatment, with a worked example if computable                         |
| fix     | the note says something the source does not | a "Common mistake" callout stating the misreading in general terms, with a cite |
| ask     | only the student can resolve it             | a question in the conversation, never in the book                               |

## The ledger

```
| id | kind | note | what the source says | source | where in the book |
|----|------|------|----------------------|--------|-------------------|
| F1 | fix | p2 L9: head described as the projection matrices | a head is one whole attention computation with its own W_Q, W_K, W_V | Vaswani §3.2.2; slide 76 | 1.4 |
| A1 | ask | p2 L5: cross-attention's question written under the encoder | that is what encoder-decoder attention answers | Vaswani §3.2.3 | conversation |
```

Put the student's focus topics at the top of the ledger and mark the rows that
serve them.

## Asking the student

- One question at a time, the one that changes the most first.
- Ask about what only they know: what they heard, what they meant, a word you
  cannot read. Do not ask what a source can answer.
- Quote their line and give the two readings: "p. 2, line 5: was that line said
  about the encoder, or about encoder-decoder attention?"
- Questions worth taking to office hours (the slides are ambiguous, or two
  sources disagree) go in the book's "Open questions" table; questions about the
  student's own pages do not.
