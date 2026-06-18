# ufr ss26 fm4sd papers

papers for [foundation models for structured data (fm4sd) seminar](https://ml.informatik.uni-freiburg.de/teaching/summer-semester-2026/seminar-seminar-on-foundation-models-for-structured-data/).

- tabular foundation models
  - group 1
    - tabpfn — [arxiv](https://arxiv.org/abs/2207.01848)
    - tabpfnv2 — [nature](https://www.nature.com/articles/s41586-024-08328-6) · [pmc](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11711098/)
    - tabpfn 2.5 — [arxiv](https://arxiv.org/abs/2511.08667)
  - group 2
    - tabicl — [arxiv](https://arxiv.org/abs/2502.05564)
    - tabiclv2 — [arxiv](https://arxiv.org/abs/2602.11139)
  - group 3
    - talent — [arxiv](https://arxiv.org/abs/2407.04057)
    - tabarena — [arxiv](https://arxiv.org/abs/2506.16791)
  - group 4
    - stopfns — [arxiv](https://arxiv.org/abs/2305.11097) · [pmlr](https://proceedings.mlr.press/v202/nagler23a)
- time series
  - group 5
    - fev-bench — [arxiv](https://arxiv.org/abs/2509.26468)
    - gift-eval — [arxiv](https://arxiv.org/abs/2410.10393)
    - impermanent — [arxiv](https://arxiv.org/abs/2603.08707)
  - group 6
    - patch-tst — [arxiv](https://arxiv.org/abs/2211.14730)
  - group 7
    - chronos-2 — [arxiv](https://arxiv.org/abs/2510.15821)
    - chronos (brief summary) — [arxiv](https://arxiv.org/abs/2403.07815)
  - group 8
    - panda — [arxiv](https://arxiv.org/abs/2505.13755)
- causal reasoning
  - group 9
    - avici — [arxiv](https://arxiv.org/abs/2205.12934)
  - group 10
    - bcnp — [arxiv](https://arxiv.org/abs/2412.16577)
  - group 11
    - do-pfn — [arxiv](https://arxiv.org/abs/2506.06039)
  - group 12
    - use what you know — [arxiv](https://arxiv.org/abs/2602.14972)

## how 2 set up

i can not host the papers and their sources in this repo because of licenses, but you should definitely grab the tex sources and download under `papers/papername` (gitignored):

```sh
wget https://arxiv.org/pdf/<id> -O <id>.pdf      # pdf
wget https://arxiv.org/src/<id> -O <id>.tar.gz   # tex
mkdir -p src && tar -xzf <id>.tar.gz -C src
rm <id>.tar.gz
```

then feed the source + [`skills/teacher.md`](skills/teacher.md) to your agent and happy working :)

i recommend working with cli tools - [claude](https://code.claude.com/docs/en/overview) · [codex](https://developers.openai.com/codex/cli) · [cursor](https://cursor.com/docs/cli/overview)
