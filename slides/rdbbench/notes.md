# Notes

*Claude notes for next sessions, to remember when the human doesn't have time to question all the details.*

## Deck conventions

- One paper sentence per frame, verbatim, in paper reading order. Frame title = current subsection (falls back to section) via `\currentheading`.
- Citations render as `\cit{Author et al., year}` — small gray footnote text, not a real `\citep`/hyperlink. When one sentence has multiple citations, combine them into a single `\cit{}` line, in the order they appear in that sentence.
- Paper `Figure~\ref{...}` / `Table~\ref{...}` mentions become plain text ("the figure" / "the table") — frames aren't captioned/labeled figure/table environments, so a literal `\ref` would be undefined at compile time.
- Tables/figures must sit right after the sentence that actually references them — check the paper's real `\label`/`\ref` pairs, not wherever LaTeX floated it in the paper source (those often don't match). Got this wrong twice before fixing: Figure 1 (Multi-Table Hops) and the Benchmarking Protocols table were both initially placed where the paper's float landed, not where the text referencing them actually is.
- Large images need explicit `height=X\textheight,keepaspectratio` on `\includegraphics` — width alone overflows the frame vertically once caption text is added below.
- Table/figure frames carry a caption paragraph (`\footnotesize`/`\scriptsize`) transcribed from the paper's `\caption{}`, placed below the content.
- Minor paper typos get silently normalized, not copied verbatim: stray spacing/punctuation (`64, GB` → `64 GB`), inconsistent caps (`TABPFN` → `TabPFN`), inconsistent `hop=0` vs `hop = 0` spacing (deck always uses spaced `hop = 0`).

## Bibliography gotchas (papers/rdbbench/src/Benchmarking_DRDB_Refined.bbl)

- `\citep{relationaltransformer2025}` is a broken/malformed bib entry in the paper itself (garbled author field) but is the same paper as `RT_Ranjan2025` (same arXiv ID 2510.06377) — always cite as "Ranjan et al., 2025", ignore the broken entry text.
- `rabbani2025_benchmark` and `rabbani2025attention` are duplicate bib entries for the identical paper — both correctly render as "Rabbani et al., 2025", that's not an error to fix.

## Status

Full deck (Abstract through Conclusions + References) transcribed and verified sentence-by-sentence against the paper, 215 pages, builds clean with no overfull/underfull warnings beyond two pre-existing benign ones (title page, one figure). Nothing left to fill in content-wise.
