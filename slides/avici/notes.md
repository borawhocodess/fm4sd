# Notes

*Claude notes for next sessions, to remember when the human doesn't have time to question all the details.*

## 2026-07-06

Fidelity check against `papers/avici/src/main.tex` — not perfectly 1:1. What's exact vs. approximated:

**1:1 (verified against the compiled paper):**
- Prose sentences transcribed near-verbatim.
- All 25 named citations (author names + years) checked against the actual rendered PDF text, not guessed from bib keys — several bib keys lie about the year (e.g. `lachapelle2019gradient` actually renders as "Lachapelle et al., 2020").
- Section/subsection numbering extracted by compiling the real paper (`\appendix` switches to letters A–E).
- Table numbers/values copied directly from the source `.tex`.

**Not 1:1 — known gaps:**
1. **Dropped footnotes**: 3 total. Two are just repo URLs (GeneNetWeaver, SERGIO GitHub), but one has real content — the LAMB optimizer paragraph (`main.tex` line 1114) has a footnote with a worked example: "With 8 GPU devices, this corresponds to a learning rate of $3\cdot10^{-5}\cdot\sqrt{8\cdot27} \approx 4.4\cdot10^{-4}$." This was never added anywhere in the slides.
2. **Dropped parenthetical `\citep{}` citations**: supporting citations that weren't the grammatical subject of a sentence were dropped throughout (heaviest in Section 1 Introduction and Section 2.2 Related Work). Only citations where the sentence names the author directly (`\citet{}`-style) were kept.
3. **Figure layout re-composed, not reproduced**: same underlying image assets (`img/*.pdf`), but panel arrangement/sizing is my own judgment call, not the source's exact `subfigure`/`subcaption` geometry. Concretely split across frames that are one figure in the paper: `fig_results_generalization` (radar row + scaling row → 2 slides) and `fig_calibration_combined` (plot + ECE table → 2 slides).
4. **Table structure simplified for space**: numbers are exact, but columns were sometimes merged or headers shortened. Worst case: the GRN "Measurement Noise" domain-spec table collapsed several source columns into comma-separated text in fewer cells. Also dropped `threeparttable`/`tablenotes` wrappers everywhere, keeping the footnote text as a plain caption line instead.
5. **Inline cross-references not individually re-verified**: things like "Section 5.1" / "Appendix E.4" typed as plain text use the section numbers already verified for headers, but each individual pointer sentence wasn't separately checked against the compiled paper the way citations were.

If asked to close the gap: the LAMB footnote (item 1) is the only one with genuine lost content — worth adding first if this comes up again.
