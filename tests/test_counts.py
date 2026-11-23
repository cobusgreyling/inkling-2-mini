import json
import re
import unittest
from pathlib import Path

from inkling2mini.counts import effective_active_billion, full_attention_layers, layer_visits

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "data" / "spec.json").read_text())

# A real credential assignment. Empty values and environment lookups are allowed.
KEY_ASSIGNMENT = re.compile(
    r"(?i)(api[_-]?key|secret|token|bearer)\s*=\s*['\"]?[A-Za-z0-9+/_=-]{12,}"
)


class LoopScheduleTest(unittest.TestCase):
    def test_forty_eight_visits_from_twenty_four_layers(self):
        loop = SPEC["loop"]
        visits = layer_visits(
            loop["stored_layers"],
            loop["core_start"],
            loop["core_end"],
            loop["num_passes"],
        )
        self.assertEqual(visits, 48)
        self.assertEqual(visits, loop["visits"])

    def test_effective_active_counts_rereads(self):
        params = SPEC["parameters"]
        effective = effective_active_billion(
            params["unique_active_billion"],
            params["extra_billion_per_later_pass"],
            SPEC["loop"]["num_passes"],
        )
        self.assertEqual(effective, 5.4)
        self.assertEqual(effective, params["effective_active_billion"])

    def test_global_layers_close_each_block(self):
        layers = full_attention_layers(SPEC["loop"]["stored_layers"], SPEC["loop"]["block_size"])
        self.assertEqual(layers, [5, 11, 17, 23])
        self.assertEqual(layers, SPEC["text"]["full_attention_layers"])

    def test_core_is_the_middle_twelve(self):
        loop = SPEC["loop"]
        self.assertEqual(loop["core_end"] - loop["core_start"], 12)
        self.assertFalse(loop["is_varloop"])
        self.assertEqual(loop["gate_rank"], 64)


class NoSecretsTest(unittest.TestCase):
    def test_repo_does_not_contain_an_api_key(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.suffix.lower() not in {".py", ".md", ".json", ".html", ".svg", ".txt", ".example", ""}:
                continue
            text = path.read_text(errors="ignore")
            private_key = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
            if private_key in text or re.search(r"\bsk-[A-Za-z0-9]{20,}", text):
                offenders.append(str(path.relative_to(ROOT)))
            for match in KEY_ASSIGNMENT.finditer(text):
                offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)[:48]}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
