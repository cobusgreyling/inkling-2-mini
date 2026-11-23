"""Read a Tinker key from the environment. Never print it. Never hard-code it."""

import os


def api_key() -> str:
    key = os.environ.get("TINKER_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "Set TINKER_API_KEY in your environment. This repository does not contain a key."
        )
    return key
