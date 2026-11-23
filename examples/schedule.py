"""Print the loop schedule from the checked-in spec. No network, no key."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from inkling2mini.counts import effective_active_billion, full_attention_layers, layer_visits
from inkling2mini.ids import PLAYGROUND_MODEL_ID, PLAYGROUND_URL, TINKER_ID_64K

spec = json.loads((ROOT / "data" / "spec.json").read_text())
loop = spec["loop"]
params = spec["parameters"]

visits = layer_visits(loop["stored_layers"], loop["core_start"], loop["core_end"], loop["num_passes"])
active = effective_active_billion(
    params["unique_active_billion"],
    params["extra_billion_per_later_pass"],
    loop["num_passes"],
)

print("Inkling 2 Mini is a looped transformer.")
print(f"Stored layers: {loop['stored_layers']}")
print(f"Core layers [{loop['core_start']}, {loop['core_end']}) x {loop['num_passes']}")
print(f"Layer visits per token: {visits}")
print(f"Global attention layers: {full_attention_layers(loop['stored_layers'], loop['block_size'])}")
print(f"Unique active / effective active: {params['unique_active_billion']}B / {active}B")
print(f"Tinker id: {TINKER_ID_64K}")
print(f"Playground: {PLAYGROUND_URL}")
print(f"Playground model id: {PLAYGROUND_MODEL_ID}")
