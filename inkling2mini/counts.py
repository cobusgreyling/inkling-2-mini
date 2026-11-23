"""Schedule arithmetic for a looped transformer.

Inkling 2 Mini stores 24 layers. The core, layers [core_start, core_end),
runs num_passes times. The prelude and the coda run once. That is the loop.
"""


def layer_visits(stored_layers: int, core_start: int, core_end: int, num_passes: int) -> int:
    if not 0 <= core_start < core_end <= stored_layers:
        raise ValueError("core span must sit inside the stored stack")
    if num_passes < 1:
        raise ValueError("num_passes must be at least 1")
    core = core_end - core_start
    once = stored_layers - core
    return once + core * num_passes


def full_attention_layers(stored_layers: int, block: int = 6) -> list[int]:
    """Global layers sit at the end of every attention-residual block."""
    if stored_layers % block != 0:
        raise ValueError("stored layers must divide into equal blocks")
    return [index for index in range(stored_layers) if index % block == block - 1]


def effective_active_billion(unique_active: float, extra_per_pass: float, num_passes: int) -> float:
    """Lab accounting: the first pass is the unique active count.

    Each later pass adds about extra_per_pass billion weight activations,
    because those weights are read again. They are not new parameters.
    """
    if num_passes < 1:
        raise ValueError("num_passes must be at least 1")
    return round(unique_active + extra_per_pass * (num_passes - 1), 1)
