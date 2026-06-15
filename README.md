# ufr ss26 fm4sd papers

papers for the [foundation models for structured data (fm4sd) seminar](https://ml.informatik.uni-freiburg.de/teaching/summer-semester-2026/seminar-seminar-on-foundation-models-for-structured-data/) at the university of freiburg, summer semester 2026.

- tabular foundation models
  - group 1
    - [tabpfn](https://arxiv.org/abs/2207.01848)
    - [tabpfnv2 (nature)](https://www.nature.com/articles/s41586-024-08328-6)
    - [tabpfn 2.5](https://arxiv.org/abs/2511.08667)
  - group 2
    - [tabicl](https://arxiv.org/abs/2502.05564)
    - [tabiclv2](https://arxiv.org/abs/2602.11139)
  - group 3
    - [talent](https://arxiv.org/pdf/2407.04057)
    - [tabarena](https://arxiv.org/abs/2506.16791)
  - group 4
    - [statistical foundation of prior-data fitted networks](https://proceedings.mlr.press/v202/nagler23a) ([arxiv](https://arxiv.org/abs/2305.11097))
- time series
  - group 5
    - [fev-bench](https://arxiv.org/abs/2509.26468)
    - [gift-eval](https://arxiv.org/pdf/2410.10393)
    - [impermanent](https://arxiv.org/abs/2603.08707)
  - group 6
    - [patch-tst](https://arxiv.org/abs/2211.14730)
  - group 7
    - [chronos-2](https://arxiv.org/abs/2510.15821) (+ brief summary of [chronos](https://arxiv.org/abs/2403.07815))
  - group 8
    - [panda](https://arxiv.org/abs/2505.13755)
- causal reasoning
  - group 9
    - [avici](https://arxiv.org/abs/2205.12934)
  - group 10
    - [bcnp](https://arxiv.org/abs/2412.16577)
  - group 11
    - [do-pfn](https://arxiv.org/abs/2506.06039)
  - group 12
    - [use what you know](https://arxiv.org/abs/2602.14972)

## how 2 set up

i can not host the papers and their sources in this repo because of licenses. but you should definitely grab the tex sources and put them in `papers/` (gitignored):

```sh
wget https://arxiv.org/pdf/<id>   # pdf
wget https://arxiv.org/src/<id>   # tex source
```
