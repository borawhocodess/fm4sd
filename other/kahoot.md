### g1

q. in each tabpfnv2 layer, the order is:
- ✓ feature attention, then sample attention, then mlp
- ✗ one attention over the whole row, then mlp
- ✗ feature and sample attention in parallel, then mlp
- ✗ column-then-row embedding, then an icl transformer

q. what are tabpfn-2.5's 64 "thinking" rows?
- ✓ rows learned during pretraining that can act as attention sinks
- ✗ added only at inference, not during pretraining
- ✗ the 64 nearest-neighbor rows of each test point
- ✗ the 64 svd components added as new rows

### g2

q. what does tabiclv2's repeated feature grouping do?
- ✓ puts each feature in multiple groups via circular shifts
- ✗ collapses multiple columns into one token
- ✗ shuffles feature order every forward pass
- ✗ groups features by correlation before encoding
- ✗ applies pca to group related columns repeatedly

q. which component had the largest effect in tabiclv2's ablation?
- ✓ the synthetic prior
- ✗ qassmax
- ✗ repeated feature grouping
- ✗ the muon optimizer

### g3

q. what does tabarena's "improvability" metric measure?
- ✓ how many % higher a method's error is than the best method's, averaged over datasets
- ✗ how much a method's error drops after hyperparameter tuning
- ✗ its win rate against the single best method
- ✗ how much elo it could still gain before saturating

q. how does talent rank methods across all its datasets?
- ✓ by average performance rank (lower is better), per friedman
- ✗ by an "improvability" % gap to the best method
- ✗ by elo from pairwise win/tie/loss
- ✗ by normalized score, best=1 and median=0

### g4

skip (us)

### g5

q. why geometric mean over arithmetic for the skill score?
- ✓ so ½ and 2x errors cancel symmetrically
- ✗ more robust to datasets with many series
- ✗ matches m4/m5 competition exactly
- ✗ arithmetic penalizes slow models

q. what makes impermanent leak-proof?
- ✓ forecasts submitted before ground truth exists
- ✗ test set is private and never released
- ✗ uses repos unseen during pretraining
- ✗ models retrained on each new cutoff

### g6

q. why does patching help more than just reducing computation?
- ✓ a single timestep has no local semantic meaning on its own
- ✗ it removes the need for positional encoding
- ✗ patches share weights across channels
- ✗ it prevents the model from overfitting long horizons

q. why mask patches instead of individual timesteps in pretraining?
- ✓ single timesteps can be trivially recovered by interpolation
- ✗ patch masking is faster to compute
- ✗ timestep masking causes positional encoding to fail
- ✗ patches make the reconstruction loss scale-invariant

### g7

q. why sinh⁻¹ is used in standardization?
- ✓ smooths the training loss by compressing outliers
- ✗ converts values into discrete bins
- ✗ removes need for mean/std
- ✗ normalizes series across different sampling frequencies

q. what gets patched + embedded together?
- ✓ scaled value, relative time index, mask
- ✗ scaled value, frequency label, domain id
- ✗ scaled value, mask, group id
- ✗ scaled value, time id, quantile level

### g8

q. panda optimizes for "weather" or "climate"?
- ✓ weather — short-term pointwise accuracy
- ✗ climate — long-term attractor fidelity
- ✗ both, via a joint loss
- ✗ neither — attractor reconstruction only

q. why does panda add channel attention?
- ✓ strong deterministic coupling between channels
- ✗ reduces compute via weight sharing
- ✗ allows variable-length forecasts
- ✗ replaces positional encoding

### g9

q. does the avici variational family guarantee acyclic graphs?
- ✓ no, acyclicity is only encouraged in expectation
- ✗ no, avici ignores acyclicity entirely
- ✗ yes, the spectral radius constraint forces it exactly
- ✗ only when trained on interventional data

q. which factor mattered most in the avici ablations?
- ✓ the axes over which attention is performed
- ✗ the number of blocks L
- ✗ the model of the variational parameters
- ✗ the number of update steps

### g10

q. how does bcnp model the presence of edges?
- ✓ a lower triangular matrix of bernoulli variables
- ✗ a softmax over the possible parents of each node
- ✗ a lower triangular matrix of gaussian weights
- ✗ a permutation matrix sampled via gumbel-sinkhorn

q. which is not a question the bcnp experiments aim to answer?
- ✓ can interventional data improve the posterior?
- ✗ do samples match the true posterior when it is known?
- ✗ how does it compare to explicit bayesian and meta-learning models?
- ✗ how does it do on realistic data from an unknown distribution?

### g11

q. which assumption does do-pfn not make?
- ✓ unconfoundedness
- ✗ a prior over scms generates the data
- ✗ observational data is i.i.d.
- ✗ the treatment variable is binary

q. which of the case studies is not identifiable?
- ✓ unobserved confounder
- ✗ front-door criterion
- ✗ back-door criterion
- ✗ confounder + mediator

### g12

q. what does 0 mean in the partial ancestor matrix?
- ✓ relationship unknown
- ✗ not an ancestor
- ✗ no direct edge
- ✗ zero parents

q. which is not in the best-performing model?
- ✓ hard attention mask
- ✗ feature positional encodings
- ✗ attention sinks
- ✗ bar distribution
