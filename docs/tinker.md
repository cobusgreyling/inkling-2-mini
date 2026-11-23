# Calling Inkling 2 Mini

Sampling and training go through Tinker. The key is `TINKER_API_KEY` in the environment of the process that calls the API. Do not commit it, and do not paste it into this repo.

OpenAI-compatible base URL, from the [inference overview](https://tinker-docs.thinkingmachines.ai/inference/openai/overview/):

```text
https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1
```

Anthropic-compatible base URL:

```text
https://tinker.thinkingmachines.dev/services/tinker-prod/anthropic/api
```

Model strings:

```text
thinkingmachines/Inkling-2-Mini
thinkingmachines/Inkling-2-Mini:peft:262144
```

## Chat

[`examples/chat.py`](../examples/chat.py) sends one turn at low effort. [`examples/stream.py`](../examples/stream.py) prints reasoning and the answer as separate fields. Both refuse to start when `TINKER_API_KEY` is unset. They never print the key.

```bash
pip install -r requirements.txt
export TINKER_API_KEY    # set this in your shell; leave it out of the repo
python examples/chat.py
```

Send earlier assistant turns back with `reasoning_content` when you build a multi-turn client. Images on this API are base64 data URLs, PNG, JPEG, GIF, or WebP, at most 2 MiB before encoding. The chat-completions docs say image input is supported on Inkling models. The server does not download `http` or `https` image links. `response_format` is not supported.

A scalar effort in `[0.0, 0.99]` can be sent with `extra_body` when the SDK's type for `reasoning_effort` only accepts strings. Raw HTTP puts `reasoning_effort` at the top level of the JSON. The names and numbers are listed by [`examples/effort.py`](../examples/effort.py).

## Cookbook

`tinker-cookbook` selects the renderer from the model name. For a sampling client, `base_model` is `thinkingmachines/Inkling-2-Mini`. Install the cookbook when you need rendering, tools, or a training loop. The scripts in `examples/` use the OpenAI-compatible endpoint and do not import the cookbook.

## Weights

Apache 2.0 weights are on Hugging Face at `thinkingmachines/Inkling-2-Mini`. Local runtimes called out around the release include vLLM, SGLang, llama.cpp, Ollama, and Unsloth. This repo does not vendor the weights.
