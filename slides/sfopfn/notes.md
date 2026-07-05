# Notes

*Claude notes for next sessions, to remember when the human doesn't have time to question all the details.*

## 2026-07-05

- **Beamer/metropolis label bug**: wrapping a labeled theorem environment like
  `\begin{theorem}\label{...} ... \end{theorem}` inside an extra brace group
  for font sizing, i.e.

  ```latex
  {\small
  \begin{theorem}\label{thm:foo}
  ...
  \end{theorem}
  }
  ```

  silently breaks `\label`: the label never gets written to the `.aux` file,
  so any later `\ref{thm:foo}` fails as "undefined reference" with no error
  pointing at the real cause. This happens with this exact combination of
  beamer + metropolis theme + a custom `\newtheorem` (e.g. `remark`,
  `assumption`, `proposition`, which beamer doesn't predefine out of the box).
  Fix: use a bare `\small` declaration instead (it's automatically scoped to
  the enclosing `\begin{frame}...\end{frame}`, no extra braces needed).

  Also had to drop two packages that broke compilation under this same setup:
  - `cleveref` corrupts beamer's colorbox setup for any custom `\newtheorem`
    environment (`remark`, `assumption`, etc.) — throws
    `Undefined control sequence: \beamer@colbox@sep`.
  - `enumitem` causes infinite macro recursion in `\labelenumi`
    (`TeX capacity exceeded, input stack size=10000`) with a plain
    `\begin{enumerate}` under beamer + metropolis.

  Neither package was actually needed (plain `\ref` and plain lists work
  fine), so both were just removed rather than worked around.

- **Pre-existing quirk in the paper's own macros**: `papers/sfopfn/src/latex-shortcuts/math.tex`
  defines `\G` as `\providecommand{\G}{}` and never gives it content —
  unlike `\C` and `\P`, which get a proper `\renewcommand` right after their
  `\providecommand`. `\G` is used in the paper for the limiting Gaussian
  process in Theorem thm:asym-q (`\sqrt{m}(q_{\wh\btheta} - q_{\btheta^*})`
  converges to a Gaussian process `\G`). Since `\G` is never assigned
  `\mathds{G}` or similar, it silently renders as nothing wherever it's
  used — in the slides, and presumably in the paper's own compiled PDF too.
  Not fixed since it's the paper's shared source file, not something I was
  asked to touch — just flagging it here in case it's news.

- **Two typos in the paper's own source, confirmed by recompiling it** (not
  yet decided whether to reproduce them in the slides or keep the cleaned-up
  version — currently the slides use the cleaned-up version):
  - Symmetry lemma (Lemma 5.1, `pfn-theory.tex` line 372): stray `P` —
    `\E_{\Dcal_n \sim P^n}[\wt f(\Dcal_n)] &= \E_{\Dcal_n \sim P^n}P[f(\Dcal_n)]`
    — renders visibly as an extra floating `P` before the bracket.
  - Proof of Theorem 3.1 (posterior consistency) conclusion
    (`pfn-theory.tex` line 721): `p*(y \mid \bx)` missing the `^`, so it
    renders as a plain asterisk next to `p` instead of a superscript, unlike
    every other occurrence of `p^*` in the paper.
