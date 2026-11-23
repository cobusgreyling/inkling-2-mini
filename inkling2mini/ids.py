"""Public identifiers. No credentials live in this module."""

PLAYGROUND_URL = "https://tinker.thinkingmachines.ai/playground"

# Playground pin for Inkling 2 Mini. This is a model id, not an API key.
PLAYGROUND_MODEL_ID = (
    "tml-6MKyT15KbuUIcelkTPFNPzYbzl5RtVCSBam4XReulRqjl0D61xgQv2WUevvlUX4JAAAAA"
)

# Tinker base-model ids. Sampling on both rows goes to 1M tokens.
# Training context is 64K on the first id and 256K on the second.
TINKER_ID_64K = "thinkingmachines/Inkling-2-Mini"
TINKER_ID_256K = "thinkingmachines/Inkling-2-Mini:peft:262144"

HF_ID = "thinkingmachines/Inkling-2-Mini"
VARLOOP_HF_ID = "thinkingmachines/TML-d24-varloop-research"

OAI_BASE_URL = "https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1"
ANTHROPIC_BASE_URL = "https://tinker.thinkingmachines.dev/services/tinker-prod/anthropic/api"

COMPARE_HF_ID = "Qwen/Qwen3.8-27B"
