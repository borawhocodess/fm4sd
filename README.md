# ufr ss26 fm4sd papers

started out from papers for [foundation models for structured data (fm4sd) seminar](https://ml.informatik.uni-freiburg.de/teaching/summer-semester-2026/seminar-seminar-on-foundation-models-for-structured-data/) at ufr ss26, then i added some more papers i found related.

## how 2 set up

cant host the papers and their sources in this repo because of licenses, but definitely grab the tex sources and download under `papers/papername` (gitignored):

```sh
wget https://arxiv.org/pdf/<id> -O <id>.pdf      # pdf
wget https://arxiv.org/src/<id> -O <id>.tar.gz   # tex
mkdir -p src && tar -xzf <id>.tar.gz -C src
rm <id>.tar.gz
```

recommend working with cli tools - [claude](https://code.claude.com/docs/en/overview) · [codex](https://developers.openai.com/codex/cli) · [cursor](https://cursor.com/docs/cli/overview)

## papers

- general
  - pfns — [arxiv](https://arxiv.org/abs/2112.10510) · [video](https://youtu.be/XnngBWe2WYE) · [video](https://www.youtube.com/watch?v=0Pi9ARZjIGg)
  - priorfitted — [arxiv](https://arxiv.org/abs/2505.23947)
- tabular
  - tabpfn — [arxiv](https://arxiv.org/abs/2207.01848) · [video](https://www.youtube.com/watch?v=9cE8lqQiLyM)
  - tabpfnv2 — [nature](https://www.nature.com/articles/s41586-024-08328-6) · [pmc](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11711098/) · [video](https://youtu.be/qFnYgM2Yvfs) · [video](https://www.youtube.com/watch?v=SOXK7AJLOY4) · [video](https://www.youtube.com/watch?v=9IkwXGe2Gaw)
  - tabpfn 2.5 — [arxiv](https://arxiv.org/abs/2511.08667) · [video](https://www.youtube.com/watch?v=IpqBLWueeog)
  - tabicl — [arxiv](https://arxiv.org/abs/2502.05564)
  - tabiclv2 — [arxiv](https://arxiv.org/abs/2602.11139) · [video](https://youtu.be/MvEkj7TOmj8)
  - talent — [arxiv](https://arxiv.org/abs/2407.04057)
  - tabarena — [arxiv](https://arxiv.org/abs/2506.16791) · [video](https://youtu.be/mcPRMcJHW2Y)
  - sfopfn — [arxiv](https://arxiv.org/abs/2305.11097) · [pmlr](https://proceedings.mlr.press/v202/nagler23a)
  - nanotabpfn — [arxiv](https://arxiv.org/abs/2511.03634)
  - modded-nanotabpfn — [github](https://github.com/borawhocodess/modded-nanotabpfn)
  - tabpfn-3 — [arxiv](https://arxiv.org/abs/2605.13986)
  - tabdpt — [arxiv](https://arxiv.org/abs/2410.18164)
  - limix — [arxiv](https://arxiv.org/abs/2509.03505)
  - limix-2m — [arxiv](https://arxiv.org/abs/2606.04485)
  - tabh2o — [arxiv](https://arxiv.org/abs/2605.18383)
  - realmlp — [arxiv](https://arxiv.org/abs/2407.04491) · [video](https://www.youtube.com/watch?v=UCHJzbs27z4)
  - metafeatures — [arxiv](https://arxiv.org/abs/2605.28418)
  - tabpfnv2closerlook — [arxiv](https://arxiv.org/abs/2502.17361)
  - beyondarena — [arxiv](https://arxiv.org/abs/2606.30410)
  - tfm-retouche — [arxiv](https://arxiv.org/abs/2605.06047)
  - tabfm — [blog](https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/)
  - tabpack — [arxiv](https://arxiv.org/abs/2607.05380)
  - drifttabpfn — [arxiv](https://arxiv.org/abs/2411.10634)
  - mitra — [arxiv](https://arxiv.org/abs/2510.21204)
  - tabflex — [arxiv](https://arxiv.org/abs/2506.05584)
  - tabm — [arxiv](https://arxiv.org/abs/2410.24210)
  - tabstar — [arxiv](https://arxiv.org/abs/2505.18125)
  - real-tabpfn — [arxiv](https://arxiv.org/abs/2507.03971)
- relational
  - rdbbench — [arxiv](https://arxiv.org/abs/2607.03659)
  - rdl-survey — [arxiv](https://arxiv.org/abs/2506.16654)
  - rt — [arxiv](https://arxiv.org/abs/2510.06377)
  - kumorfm — [pdf](https://kumo.ai/research/kumo_relational_foundation_model.pdf)
  - kumorfm-2 — [arxiv](https://arxiv.org/abs/2604.12596)
  - openrfm — [arxiv](https://arxiv.org/abs/2606.04320)
  - plurel — [arxiv](https://arxiv.org/abs/2602.04029)
  - rdblearn — [arxiv](https://arxiv.org/abs/2602.18495) · [arxiv](https://arxiv.org/abs/2602.13697)
- time series
  - forecasting
    - fev-bench — [arxiv](https://arxiv.org/abs/2509.26468)
    - gift-eval — [arxiv](https://arxiv.org/abs/2410.10393)
    - impermanent — [arxiv](https://arxiv.org/abs/2603.08707)
    - patch-tst — [arxiv](https://arxiv.org/abs/2211.14730) · [video](https://www.youtube.com/watch?v=Z3-NrohddJw)
    - chronos-2 — [arxiv](https://arxiv.org/abs/2510.15821) · [video](https://www.youtube.com/watch?v=wSc76uFpFKg) · [video](https://www.youtube.com/watch?v=PeJReI9Sm0U)
    - chronos — [arxiv](https://arxiv.org/abs/2403.07815) · [video](https://www.youtube.com/watch?v=EEZ6DefhCvE) · [video](https://www.youtube.com/watch?v=6eDVkNBxURo)
    - panda — [arxiv](https://arxiv.org/abs/2505.13755)
    - tabpfn-ts — [arxiv](https://arxiv.org/abs/2501.02945)
    - toto-2 — [arxiv](https://arxiv.org/abs/2605.20119)
    - ts-icl — [arxiv](https://arxiv.org/abs/2606.05878)
    - tiny-tsm — [arxiv](https://arxiv.org/abs/2511.19272)
    - tempopfn — [arxiv](https://arxiv.org/abs/2510.25502)
    - tirex — [arxiv](https://arxiv.org/abs/2505.23719)
    - tirex-2 — [arxiv](https://arxiv.org/abs/2607.01204)
  - classification
    - timee — [arxiv](https://arxiv.org/abs/2607.07500)
    - mantis — [arxiv](https://arxiv.org/abs/2502.15637)
    - rocketpfn — [arxiv](https://arxiv.org/abs/2606.21786)
- causal
  - avici — [arxiv](https://arxiv.org/abs/2205.12934)
  - bcnp — [arxiv](https://arxiv.org/abs/2412.16577)
  - do-pfn — [arxiv](https://arxiv.org/abs/2506.06039) · [video](https://youtu.be/yTbY4SpPJcE)
  - use what you know — [arxiv](https://arxiv.org/abs/2602.14972)
  - tabcausal — [arxiv](https://arxiv.org/abs/2605.31156)
  - causalfm — [arxiv](https://arxiv.org/abs/2506.10914)
  - dcd-pfn — [arxiv](https://arxiv.org/abs/2606.21212)
  - foundcause — [arxiv](https://arxiv.org/abs/2606.17516)
  - tabpfn-cfm — [arxiv](https://arxiv.org/abs/2606.26467)
  - tabpfnunderstandcausal — [arxiv](https://arxiv.org/abs/2511.07236) · [video](https://www.youtube.com/watch?v=9_on4JV9zDg)
  - activa — [arxiv](https://arxiv.org/abs/2503.01290)
  - causalpfn — [arxiv](https://arxiv.org/abs/2506.07918)
  - dag-fm — [arxiv](https://arxiv.org/abs/2607.11510)
- other
  - lifelongicl — [arxiv](https://arxiv.org/abs/2606.25342)
  - rlfm — [arxiv](https://arxiv.org/abs/2606.18812)
  - lejepa — [arxiv](https://arxiv.org/abs/2511.08544) · [video](https://www.youtube.com/watch?v=gVEr2cnDE_8&t=1944s)

## queue

not placed yet:

- general
  - martingale — [arxiv](https://arxiv.org/abs/2103.15671)
  - pfnuq — [arxiv](https://arxiv.org/abs/2505.11325)
- tabular
  - flextab — [arxiv](https://arxiv.org/abs/2606.30336)
  - enterprisetabgap — [arxiv](https://arxiv.org/abs/2606.30452)
  - gotabpfn — [arxiv](https://arxiv.org/abs/2606.05441)
  - shapinggeometry — [openreview](https://openreview.net/forum?id=IYnHchzvYB)
  - tabgenfm — [arxiv](https://arxiv.org/abs/2605.09424) · [openreview](https://openreview.net/forum?id=RcsaxrdpfE)
  - tabattnbench — [openreview](https://openreview.net/forum?id=rwtcugrpDq)
  - tabshallow — [openreview](https://openreview.net/forum?id=kCnZUf1VYC)
  - tabbarrier — [openreview](https://openreview.net/forum?id=TUYc2XUdwz)
  - tjepa — [arxiv](https://arxiv.org/abs/2410.05016)
  - tablora — [arxiv](https://arxiv.org/abs/2607.10077)
  - ptnas — [openreview](https://openreview.net/pdf?id=3ADqf6jn9r)
- time series
  - baguan-ts — [openreview](https://openreview.net/forum?id=xO10rIopwe)
  - simpletimebench — [openreview](https://openreview.net/forum?id=iIRdd86Xkr)
- causal
  - tscausalfm — [openreview](https://openreview.net/forum?id=CAaTQAfq7c)
  - causalfewshot — [openreview](https://openreview.net/forum?id=2yvEiFhNCT)
  - partialcausalid — [openreview](https://openreview.net/forum?id=jCbehzZBsk)
  - causalorder — [openreview](https://openreview.net/forum?id=U4KiOBxY1X)
  - causaltab — [openreview](https://openreview.net/forum?id=og3UVhP7M1)
  - posttreatmentcfm — [openreview](https://openreview.net/forum?id=ULoLF1aOo1)
  - macetnp — [arxiv](https://arxiv.org/abs/2507.05526)
  - cdfm — [arxiv](https://arxiv.org/abs/2607.11508)
- mechanistic interpretability
  - tabular
    - tabfmmechanistic — [arxiv](https://arxiv.org/abs/2605.21288)
    - onelayerenough — [arxiv](https://arxiv.org/abs/2605.06510)
    - looking-glass — [arxiv](https://arxiv.org/abs/2601.08181)
    - where-computation — [arxiv](https://arxiv.org/abs/2606.12917)
    - kernelicl — [arxiv](https://arxiv.org/abs/2602.02162)
  - circuits
    - circuits-framework — [blog](https://transformer-circuits.pub/2021/framework/index.html)
    - induction-heads — [arxiv](https://arxiv.org/abs/2209.11895)
    - ioi — [arxiv](https://arxiv.org/abs/2211.00593)
    - grokking — [arxiv](https://arxiv.org/abs/2301.05217)
  - representations
    - superposition — [arxiv](https://arxiv.org/abs/2209.10652)
    - monosemanticity — [blog](https://transformer-circuits.pub/2023/monosemantic-features/index.html)
    - othello-gpt — [arxiv](https://arxiv.org/abs/2210.13382)
  - icl
    - icl-regression — [arxiv](https://arxiv.org/abs/2208.01066)
    - icl-learning-alg — [arxiv](https://arxiv.org/abs/2211.15661)
    - icl-gd — [arxiv](https://arxiv.org/abs/2212.07677)
    - task-vectors — [arxiv](https://arxiv.org/abs/2310.15916)
    - function-vectors — [arxiv](https://arxiv.org/abs/2310.15213)
