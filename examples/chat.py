"""One chat turn on Inkling 2 Mini, the looped transformer.

The key stays in the environment. Nothing in this file is a credential.
"""

import sys
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples._key import api_key
from inkling2mini.ids import OAI_BASE_URL, TINKER_ID_64K


def main() -> None:
    client = OpenAI(base_url=OAI_BASE_URL, api_key=api_key())
    response = client.chat.completions.create(
        model=TINKER_ID_64K,
        messages=[
            {
                "role": "user",
                "content": "In one sentence, what does a looped transformer reuse?",
            }
        ],
        max_completion_tokens=256,
        reasoning_effort="low",
    )
    message = response.choices[0].message
    if message.reasoning_content:
        print(message.reasoning_content)
        print()
    print(message.content)


if __name__ == "__main__":
    main()
