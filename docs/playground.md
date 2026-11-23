# Tinker playground

Open [the Tinker playground](https://tinker.thinkingmachines.ai/playground) and select **Inkling 2 Mini**.

The playground model id for this reference is:

```text
tml-6MKyT15KbuUIcelkTPFNPzYbzl5RtVCSBam4XReulRqjl0D61xgQv2WUevvlUX4JAAAAA
```

That string identifies the model in the playground. It is not an API key. This repository does not contain a Tinker API key. Put `TINKER_API_KEY` in your own environment or in a gitignored `.env`. See [`.env.example`](../.env.example).

## What you are running

The playground model is the fixed looped transformer:

- 24 stored layers
- layers 6–17 repeated three times
- 48 layer visits per token
- `is_varloop: false`

Effort changes how much chain-of-thought the model writes. It does not change the three passes. Named levels, from the Tinker docs:

| Name | Value |
| --- | --- |
| none | 0.0 |
| minimal | 0.1 |
| low | 0.2 |
| medium | 0.7 |
| high (default) | 0.9 |
| xhigh, max | 0.99 |

`0.0` conditions the model toward no written reasoning. The middle layers still loop.

## API ids

Use these on the API. Do not send the playground pin as the `model` field.

| Use | Id |
| --- | --- |
| Train to 64K, sample to 1M | `thinkingmachines/Inkling-2-Mini` |
| Train to 256K, sample to 1M | `thinkingmachines/Inkling-2-Mini:peft:262144` |
| Weights | [`thinkingmachines/Inkling-2-Mini`](https://huggingface.co/thinkingmachines/Inkling-2-Mini) |
| Variable loop, research | [`thinkingmachines/TML-d24-varloop-research`](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) |

Prices on the Tinker [models page](https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/), per million tokens: prefill $0.15, cached prefill $0.015, sample $0.50. Training is $0.75 on the 64K row and $1.50 on the 256K row. Sampling prices match across the two rows.
