# Sources

Figures in this repo come from public documents. Scores in the comparison are Thinking Machines' launch table unless a row says otherwise. This repository did not re-run the benchmarks.

- Announcement, 20 November 2026: https://thinkingmachines.ai/news/inkling-2-mini/
- Checkpoint config, read 23 November 2026: https://huggingface.co/thinkingmachines/Inkling-2-Mini/raw/main/config.json
- Qwen3.8-27B config, read 23 November 2026: https://huggingface.co/Qwen/Qwen3.8-27B/raw/main/config.json
- Qwen3.8-27B model card: https://huggingface.co/Qwen/Qwen3.8-27B
- Tinker models and pricing: https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/
- Tinker OpenAI-compatible API: https://tinker-docs.thinkingmachines.ai/inference/openai/overview/
- Chat completions, including effort and images: https://tinker-docs.thinkingmachines.ai/inference/openai/chat-completions/
- Playground: https://tinker.thinkingmachines.ai/playground
- Attention residuals: https://arxiv.org/abs/2603.15031
- Universal Transformers: https://arxiv.org/abs/1807.03819
- Variable-loop research weights: https://huggingface.co/thinkingmachines/TML-d24-varloop-research

Parameter totals (26.4B, 3.4B active, 5.4B with the loop) are the lab's published counts. The visit count, 48, is also what `python -m unittest` checks from `data/spec.json`.

No API key is stored in this repository.
