"""Facts and arithmetic for the Inkling 2 Mini looped transformer."""

from inkling2mini.counts import effective_active_billion, full_attention_layers, layer_visits
from inkling2mini.ids import (
    HF_ID,
    PLAYGROUND_MODEL_ID,
    PLAYGROUND_URL,
    TINKER_ID_64K,
    TINKER_ID_256K,
    VARLOOP_HF_ID,
)

__all__ = [
    "HF_ID",
    "PLAYGROUND_MODEL_ID",
    "PLAYGROUND_URL",
    "TINKER_ID_256K",
    "TINKER_ID_64K",
    "VARLOOP_HF_ID",
    "effective_active_billion",
    "full_attention_layers",
    "layer_visits",
]
