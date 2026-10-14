# Transcription

The transcript is the record of what the student wrote. It stays in `research/`
and is never printed, but it decides what the book covers, which topics get the
most space and which mistakes get a callout, so it has to be faithful, complete
and honest about doubt.

## Before you start

1. Watch for the usual collisions in handwriting (`l`/`1`/`I`, `O`/`0`, `u`/`v`,
   `cl`/`d`) and resolve them from context.
2. Skim the lecture's slides first. Knowing the vocabulary is what resolves most
   doubtful words ("attn" next to "Encoder-Decoder" is attention; "PE" after
   "Positional Encoding" is its abbreviation).

## The transcript file

`research/transcription/transcript.md`, one table per photo:

```
## Page 1 (page-1.jpg)
| L | Text | Note |
|---|---|---|
| 1 | Stanford CME Transformers + LLMs | underlined, arrow to the right |
| 12 | Self attention (Enc-Enc) | written "Enc-En[d?]"; read as Enc-Enc from context |
```

- **Number lines from the first written line** of each photo. A line is one line
  of the paper; a sentence that wraps keeps one number per paper line only if
  the student's layout matters, otherwise one row per sentence.
- **Keep the student's words**: spelling, abbreviations ("diff", "attn", "w/"),
  capitalisation, quotation marks, `+` for "and". Do not complete sentences or
  fix grammar.
- **Mark structure in the Note column**: underlined, circled, boxed, starred,
  arrows, brackets that group lines, margin labels (`{margin: Decoding}`),
  indentation that shows nesting.
- **Struck-out text** is kept as `~~text~~`; it is part of the record and
  sometimes shows a correction the student made during the lecture.
- **Diagrams**: describe each one in words under the table: what is drawn, what
  connects to what, and which slide it reproduces if you can tell. A redrawn
  version of that slide's figure is often the best figure for that section.

## Doubt

Mark a reading you are not sure of with `[?]` in the transcript and list it at
the end:

```
| Where | Read as | Alternative | Matters? |
|---|---|---|---|
| p1 L12 | Enc-Enc | Enc-End | no: "Enc-End" is not a term; Enc-Enc matches slide 69 |
| p2 L5 | under "Encoder" | belongs to encoder-decoder attention | yes: it changes which attention it describes |
```

- Resolve from context where you can, and say what resolved it.
- If the doubt changes the meaning (a variable name, a sign, a number, which
  topic a line belongs to), it becomes an **ask** row in the gap ledger and a
  question for the student in the conversation.

## Coverage table

End the transcript with the lecture's topics by slide range and whether the
notes cover them: `yes`, `partly` (say what is missing) or `no`. This table
drives the gap ledger. The book prints only the slide ranges and the sections
that cover them, never what the notes covered.

## When the student corrects you

Fix the transcript and anything written from it, and read the rest of that
student's pages with the same correction in mind.
