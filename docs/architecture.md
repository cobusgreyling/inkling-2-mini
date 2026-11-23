# Architecture

Inkling 2 Mini is a **looped transformer**. The published checkpoint stores 24 decoder layers. Layers 6 through 17 run three times per token, on shared weights. Layers 0–5 and 18–23 run once. That is 48 layer visits from 24 stored layers.

`loop_config` in [`config.json`](https://huggingface.co/thinkingmachines/Inkling-2-Mini/raw/main/config.json), read 23 November 2026:

| Field | Value |
| --- | --- |
| `core_start` | 6 |
| `core_end` | 18 (exclusive) |
| `num_passes` | 3 |
| `gate_rank` | 64 |
| `is_varloop` | false |
| `model_type` | `inkling2_loop` |
| class | `Inkling2LoopForConditionalGeneration` |

The announcement counts the same span as layers 7–18 when numbering from 1. `core_end` is exclusive, so checkpoint layers 6–17 are announcement layers 7–18.

## Visit schedule

| Stage | Layers | Times run | Global layer in the block |
| --- | --- | --- | --- |
| Prelude | 0–5 | 1 | 5 |
| Core, pass 1 | 6–17 | 1 | 11 and 17 |
| Core, pass 2 | 6–17 | 1, same weights | 11 and 17 |
| Core, pass 3 | 6–17 | 1, same weights | 11 and 17 |
| Coda | 18–23 | 1 | 23 |

`local_layer_ids` lists 20 local layers. The four missing indexes are 5, 11, 17, and 23: one full-attention layer at the end of each block of six. The local window is 1,024 (`sliding_window_size` and `rel_extent`).

The two extra passes re-read two full-attention layers, not only the local layers.

## Attention residuals and the message

Blocks are six layers (`n_layers_per_attn_res_block`). Thinking Machines uses attention residuals: a layer reads earlier block outputs and learns its own mix, instead of adding every layer into one running residual stream. The citation in the launch post is [Attention Residuals](https://arxiv.org/abs/2603.15031) (Kimi Team, 2026).

Each later pass starts again from the prelude output. Passes 2 and 3 also read a message from the previous pass. The config sets `gate_rank` to 64. The launch post says the gate starts closed, so the early part of training matches a model that does not loop, and the gate opens as training continues.

The pass count on this checkpoint is fixed. `is_varloop` is false. The research sibling [TML-d24-varloop-research](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) is the one trained across one to five passes.

## Text stack

| Field | Value |
| --- | --- |
| Hidden size | 2,304 |
| Query heads / KV heads / head dim | 24 / 8 / 128 |
| Routed experts | 128 |
| Experts per token | 8 |
| Shared experts | 0 |
| Expert intermediate size | 1,152 |
| `route_scale` | 8 |
| Vocabulary rows / usable ids | 201,024 / 200,058 |
| `model_max_length` | 1,048,576 |
| Logit soft cap | 30 |
| Short conv kernel | 4 |

Parameter counts below are the lab's figures from the [20 November 2026 announcement](https://thinkingmachines.ai/news/inkling-2-mini/), not a sum over the safetensors.

| Count | Billion |
| --- | --- |
| Total parameters | 26.4 |
| Unique parameters active on one pass | 3.4 |
| Weight activations at three passes | 5.4 |

The two extra passes add about 1.0B weight activations each. Those are repeated reads of the core, not new weights.

Training started at 8 experts chosen from 384 (the lab's "sparsity of 48"). At midtraining, two-thirds of the experts were removed and the 128 most-used experts in each layer were kept. A further 1T tokens, distilled from a larger internal Inkling model, retrained the survivors. Post-training was supervised fine-tuning on a mix close to Inkling 2 Small, then reinforcement learning of 2.2T tokens over 2,000 steps, plus on-policy distillation.

## Vision

The vision tower in the same config has 23 layers, hidden size 1,024, 16 heads, native patches of 20, and a 2×2 merge before projection. The lab's input list for this model is text and image. The config does not define a video token id. First-generation Inkling accepts audio. Inkling 2 Mini does not.

## Numerics

`quantization_config.quant_algo` in the config is `NVFP4`. The announcement says the last four layers are MXFP8 and that the checkpoint is deployed in the precision it was trained in. The stated memory footprint is about 20GB. The supported local floor in the launch material is a Mac with 32GB of memory, a DGX Spark, or a GPU with about 32GB.

The diagram is [`assets/architecture.svg`](../assets/architecture.svg). The arithmetic is checked by `python -m unittest`.
