"""Stream a reply. Reasoning and answer arrive on separate fields."""

import sys
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples._key import api_key
from inkling2mini.ids import OAI_BASE_URL, TINKER_ID_256K


def main() -> None:
    client = OpenAI(base_url=OAI_BASE_URL, api_key=api_key())
    stream = client.chat.completions.create(
        model=TINKER_ID_256K,
        messages=[{"role": "user", "content": "What is 17 * 23?"}],
        stream=True,
        stream_options={"include_usage": True},
        reasoning_effort="medium",
    )
    part = None
    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            for name, text in (
                ("Reasoning", delta.reasoning_content),
                ("Answer", delta.content),
            ):
                if not text:
                    continue
                if name != part:
                    print(f"\n[{name}]")
                    part = name
                print(text, end="", flush=True)
        if chunk.usage:
            print("\nTokens:", chunk.usage.total_tokens)


if __name__ == "__main__":
    main()
