# The loop in the middle

![Twenty-four glass slabs. A gold ribbon passes through the middle twelve three times.](../assets/loop.jpg)

Inkling 2 Mini is a looped transformer. Thinking Machines Lab released it on 20 November 2026, with Apache 2.0 weights, and put it on the [Tinker playground](https://tinker.thinkingmachines.ai/playground) the same day.

The checkpoint stores 24 decoder layers. For every token, layers 6 through 17 run three times on the same weights. Layers 0–5 and layers 18–23 run once. The token is processed by 48 layer applications. The file on disk stays the size of 24 layers.

That reuse is the architecture. The mixture-of-experts path and the 4-bit experts are how a 26.4B model fits in about 20GB. The loop is the part this release adds. The lab describes it as the first looped transformer they have shipped.

The playground model id for this reference is `tml-6MKyT15KbuUIcelkTPFNPzYbzl5RtVCSBam4XReulRqjl0D61xgQv2WUevvlUX4JAAAAA`. On the API the id is `thinkingmachines/Inkling-2-Mini`. This repository does not contain an API key.

## Forty-eight visits

The published `config.json` names the schedule.

| Field | Value |
| --- | --- |
| `core_start` | 6 |
| `core_end` | 18, exclusive |
| `num_passes` | 3 |
| `gate_rank` | 64 |
| `is_varloop` | false |

`core_end` is exclusive, so the repeated layers are 6 through 17. Twelve layers. The announcement counts that same span as layers 7–18 when it numbers from 1.

| Stage | Layers | Runs |
| --- | --- | --- |
| Prelude | 0–5 | once |
| Core | 6–17 | three times, shared weights |
| Coda | 18–23 | once |

Visits = (24 − 12) + (12 × 3) = 48.

Attention is hybrid. `local_layer_ids` lists 20 layers. The four indexes left out are 5, 11, 17, and 23. Each block of six ends on a full-attention layer. The local window is 1,024 tokens. The loop includes the global layers at 11 and 17, so each extra pass takes two more looks at the full context, from weights that are already on the chip.

`is_varloop` is false. Effort changes how much chain-of-thought the model writes. It does not change the three passes. The research checkpoint `TML-d24-varloop-research` is the one trained with a variable pass count.

Open [`site/index.html`](../site/index.html) to watch the schedule: the prelude lights once, the core lights three times, the coda lights once. Taller slabs in that page are the global layers.

## Why the middle

The lab's reason is the old one from Universal Transformers. Middle layers carry abstract work. The first layers and the last layers spend more of their capacity translating between embeddings and that internal space. They tested the claim. At training step 2,000, with three passes and the same training compute, looping the middle 12 layers was worth an estimated 1.51× to 1.91× in compute-equivalent gain. Looping the last 12 layers was worth 1.24× to 1.36×. The middle-loop variant won 27 of 28 evaluations.

A non-looping comparison on their scaling ladder cost 7.5% less to train and needed 140% more inference compute to match the looped model's loss on 512k-token agentic traces.

## The message between passes

![A copper filament of the previous pass carried into the next.](../assets/message.jpg)

Inkling 2 Mini uses attention residuals, the design in the Kimi paper of that name. A layer does not add into one running residual that every later layer must inherit. The stack is cut into blocks of six (`n_layers_per_attn_res_block`). Each block keeps the sum of its own layers. A layer reads the earlier block outputs and learns its own mix.

Every pass starts from the prelude's output, the state that entered layer 6. Passes 2 and 3 also read a message: the previous pass's outputs on the two middle blocks. The checkpoint sets `gate_rank` to 64. The launch post says the gate is learned, starts closed, and opens over training. Closed, a loop behaves like a stack that does not loop. That is how they turn the loop on without a shock at the start of training.

## Experts, then a cut

The feed-forward path is a mixture of experts with no shared expert. The config records 128 routed experts, 8 chosen per token, intermediate size 1,152, and `route_scale` 8.

Training did not start there. It started at 8 experts chosen from 384, which the lab calls a sparsity of 48. At one point in midtraining they dropped two-thirds of the experts and kept the 128 most used in each layer. The cut is why the checkpoint is small enough for a laptop. A further 1 trillion tokens, distilled from a larger internal Inkling model, trained the remaining experts to cover the work of the ones that were removed.

After that: supervised fine-tuning on a mix close to Inkling 2 Small, reinforcement learning of 2.2 trillion tokens over 2,000 steps, and on-policy distillation for alignment.

The lab's parameter accounting, which this repo does not re-sum from the shards:

| | Billion |
| --- | --- |
| Total parameters | 26.4 |
| Unique parameters active on one pass | 3.4 |
| Weight activations at three passes | 5.4 |

The two extra passes add about a billion weight activations each. Those are repeated reads. They are not new parameters. Tinker's pricing table rounds the total to 26B and lists 5.4B active, which is the looped figure.

## What the loop does not store

Facts sit in parameters. The launch post is explicit that more passes improve long-context work, such as GraphWalks and MRCR v2, and do not improve knowledge tests such as AA-Omniscience, SimpleQA, SimpleVQA, and WorldVQA. Inkling 2 Mini's factuality score sits with other models of this size. The lab's answer for the knowledge gap is tools. On their table it leads the open models they compare of similar size on BrowseComp, DeepSearchQA, and MCP Atlas.

## A shorter chain of thought

Looping raises the amount of serial compute a token can do before the model has to write anything down. That is the monitorability question: reasoning that never appears in the chain of thought cannot be read by a chain-of-thought monitor.

The measurements are on the variable-loop research model, because Mini's pass count is fixed. On a subset of Think Fast, the no-chain-of-thought time horizon went from 16 seconds of human task-time at one pass to 37 seconds at three, then flattened. A serial lookup task, N-Hop, kept improving out to ten passes, past the five the model was trained with. The written chain of thought got shorter and, in the lab's reading, stayed legible. Their tests of agentic sabotage did not trend upward as passes were added. They call this preliminary.

## Numerics

`quantization_config.quant_algo` in the config is NVFP4. The announcement says the last four layers are MXFP8, and that the weights ship in the precision they were trained in, so there is no extra quantization step after training. The stated footprint is about 20GB. The local floor they name is a Mac with 32GB of memory, a DGX Spark, or a GPU around that size. The flight-simulator demo in the announcement ran on a MacBook Pro with an M5 Pro and 48GB, offline.

The text stack around the loop: hidden size 2,304, 24 query heads, 8 key-value heads, head dimension 128, vocabulary 201,024 rows of which 200,058 are usable, context length 1,048,576 in `model_max_length`. The vision tower has 23 layers, hidden size 1,024, 16 heads, 20-pixel patches, and a 2×2 merge. Inputs are text and image. The config has no video token. First-generation Inkling accepts audio. This model does not.

The field-by-field sheet is [docs/architecture.md](../docs/architecture.md). The comparison with Qwen3.8-27B is [the next essay](side-by-side-qwen3-8-27b.md).

## Sources

The schedule and the widths are from the Hugging Face config, read 23 November 2026. The training story, the compute-equivalent ranges, and the monitorability numbers are from the [20 November announcement](https://thinkingmachines.ai/news/inkling-2-mini/). Attention residuals: [arXiv:2603.15031](https://arxiv.org/abs/2603.15031). Universal Transformers: [arXiv:1807.03819](https://arxiv.org/abs/1807.03819). A full list is [docs/sources.md](../docs/sources.md).
