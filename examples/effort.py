"""Reasoning effort on a looped transformer.

Effort changes how much the model writes. It does not change the loop.
Inkling 2 Mini always runs the middle 12 layers three times. is_varloop is false.
"""

EFFORT = {
    "none": 0.0,
    "minimal": 0.1,
    "low": 0.2,
    "medium": 0.7,
    "high": 0.9,
    "xhigh": 0.99,
}


def main() -> None:
    print("Inkling effort presets. Default is high (0.9). Pass a name or a number in [0.0, 0.99].")
    for name, value in EFFORT.items():
        print(f"  {name:<8} {value}")
    print()
    print("The three loop passes still run at effort 0. The gate and the weights do not change.")
    print("To vary the pass count, use the research checkpoint TML-d24-varloop-research.")


if __name__ == "__main__":
    main()
