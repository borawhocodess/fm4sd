# Notes

*Claude notes for next sessions, to remember when the human doesn't have time to question all the details.*

## 2026-07-06

Fidelity check against `papers/bcnp/src/main.tex` — not perfectly 1:1. What's exact vs. approximated:

**1:1 (verified against the compiled paper):**
- Prose sentences transcribed near-verbatim.
- All named citations (author names + years) checked against the actual rendered PDF text via `pdftotext -raw` + substring search, not guessed from bib keys. Two bib keys lied about the year/name: `dhir2023causal` actually renders as "Dhir et al., 2024"; `lopez2015towards` renders as "Lopez-Paz et al., 2015" (not "Lopez et al."). Also note: `lachapelle2019gradient` appears in avici's bibliography as "2020" but is a *different* paper's bib entry here — the same key can render a different year in a different paper's `.bbl`, so always re-verify per-paper, never reuse a prior paper's citation-year lookup.
- One real gap caught only on the audit pass, now fixed: `\cite{lee2019set}` at the end of the transformer permutation-equivariance derivation (source line ~828, "...permutation equivariance with respect rows of the inputs \cite{lee2019set}.") was dropped from the first draft of the A.1 Transformers section and had to be added back as "(Lee et al., 2019)".
- Section/subsection/appendix numbering extracted by actually compiling `main.tex` (`\appendix` switches 4→A, 5→B, 6→C) and reading the rendered headers, not assumed from `\section`/`\subsection` source order.
- All 15 Appendix C result tables and the 3 main-text comparison tables copied with exact numeric values from the source `.tex`.
- Hyperparameter tables (DiBS, BayesDAG) in Appendix B.3 copied with exact values from source lines ~926-981.

**Not 1:1 — known gaps:**
1. **Dropped parenthetical `\citep{}` citations**: as with avici, supporting citations that aren't the grammatical subject of a sentence were dropped throughout — heaviest in Section 1 Introduction (e.g. `\citep{pearl2009causality}`, `\citep{toth2022active}`, `\citep{agrawal2019abcd, zhang2023active, jain2023gflownets, tigas2023differentiable}`, `\citep{janzing2010causal}`, `\citep{annadani2021variational, cundy2021bcd}`, `\citep{wenzel2020good}`, `\citep{garnelo2018neural}`, `\citep{requeima2023neural, muller2021transformers}`, `\citep{zheng2018dags}`). Only `\citet{}`-style narrative citations (author named directly in the sentence) were kept.
2. **Dropped footnotes**: 2 total, both just GitHub repo URLs (DiBS: `github.com/larslorch/dibs`, BayesDAG: `github.com/microsoft/Project-BayesDAG`) attached to the `\paragraph{DiBS:}`/`\paragraph{BayesDAG:}` headers in Appendix B.3. No substantive content lost (unlike avici's LAMB footnote, which had a real worked example).
3. **No `\newtheorem` environments in this paper at all** — unlike sfopfn, bcnp has no formal theorem/lemma/proposition statements, so none of the sfopfn-era label/brace bugs were relevant here.
4. **Table structure mostly kept 1:1** since bcnp's tables are already compact (4-5 columns); no column-merging was needed, unlike avici's denser domain-spec tables.
5. **Two raw TikZ figures reused directly**: the encoder diagram (source `\subsection{Encoder}`) and decoder diagram (source `\subsection{Decoder}`) were copy-pasted wholesale from `main.tex` into their own frames — renders pixel-identical, cheapest and most faithful option since both are native TikZ, not external images.
6. **Inline cross-references not individually re-verified**: pointers like "Section 4.2" / "Appendix B.1" typed as plain text reuse the section numbers already verified for headers, but each pointer sentence wasn't separately checked the way citations were.

If asked to close the gap further: item 1 (dropped `\citep`s) is the largest volume of missing material but is uniformly non-substantive supporting citations, consistent with the policy already applied to avici.
