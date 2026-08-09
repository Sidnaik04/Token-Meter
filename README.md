# token-meter

**Measure LLM token usage and API cost from your terminal.**

`token-meter` is a lightweight CLI tool that sends a prompt to an LLM through [LiteLLM](https://github.com/BerriAI/litellm), then reports the input/output token usage and estimated API cost.

It supports both **one-shot CLI execution** and an **interactive REPL**, with OpenAI and Gemini models available through a single interface.

---

## Features

* Token usage tracking

  * Input tokens
  * Output tokens
* Cost breakdown

  * Input cost
  * Output cost
  * Total cost
* OpenAI and Gemini support through LiteLLM
* Interactive REPL
* One-shot CLI mode
* Prompt input from files
* JSON output for scripting and automation
* Rich terminal output for interactive use
* Configurable maximum output tokens
* API key kept in memory only
* Model validation and user-friendly errors
* Provider and model switching inside the REPL

---

## Installation

### Requirements

* Python **3.11+**
* [`uv`](https://docs.astral.sh/uv/)
* An OpenAI or Gemini API key

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd token-meter
```

Install dependencies:

```bash
uv sync
```

You can now run the CLI with:

```bash
uv run token-meter
```

---

# Usage

`token-meter` supports two modes.

### Interactive REPL

Run the command without a complete set of arguments:

```bash
uv run token-meter
```

You'll be guided through provider, model, and API key selection.

```text
Choose provider:
1. OpenAI
2. Gemini

Provider: 1

Choose model for OpenAI:
1. gpt-4o-mini
2. gpt-4o
3. o1-mini

Model: 1

Enter OpenAI API key: ********

Token Meter REPL
Type /model, /provider, /exit, or /quit.

token-meter> Explain backpropagation
```

The API key and selected configuration remain in memory for the duration of the session.

### REPL commands

| Command     | Description                         |
| ----------- | ----------------------------------- |
| `/model`    | Switch the current model            |
| `/provider` | Switch provider, model, and API key |
| `/exit`     | Exit the REPL                       |
| `/quit`     | Exit the REPL                       |

Empty lines are ignored, and unknown slash commands do not trigger an API request.

---

# One-Shot Mode

For users who want a single API call without entering the REPL:

```bash
uv run token-meter \
  --model gpt-4o-mini \
  --prompt "Explain backpropagation in one sentence." \
  --api-key YOUR_OPENAI_API_KEY
```

Example output:

```text
                Token Meter
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Metric        ┃ Value          ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Model         │ gpt-4o-mini    │
│ Input Tokens  │ 15             │
│ Output Tokens │ 47             │
│ Input Cost    │ $0.00000225    │
│ Output Cost   │ $0.00002820    │
│ Total Cost    │ $0.00003045    │
└───────────────┴────────────────┘
```

The exact token counts and costs depend on the prompt, model, and provider pricing.

---

## Gemini

Gemini models use LiteLLM's model format:

```bash
uv run token-meter \
  --model gemini/gemini-2.5-flash \
  --prompt "Explain backpropagation in one sentence." \
  --api-key YOUR_GEMINI_API_KEY
```

The same command structure and output format are used for both providers.

---

# JSON Output

Use `--json` when the result needs to be consumed programmatically:

```bash
uv run token-meter \
  --model gpt-4o-mini \
  --prompt "What are embeddings?" \
  --api-key YOUR_OPENAI_API_KEY \
  --json
```

Example:

```json
{
  "model": "gpt-4o-mini",
  "input_tokens": 15,
  "output_tokens": 47,
  "input_cost_usd": 0.00000225,
  "output_cost_usd": 0.0000282,
  "total_cost_usd": 0.00003045
}
```

This makes `token-meter` useful in shell scripts and other developer tooling.

---

# Prompt Files

For longer prompts, use `--prompt-file`:

```bash
uv run token-meter \
  --model gpt-4o-mini \
  --prompt-file ./prompt.txt \
  --api-key YOUR_OPENAI_API_KEY
```

`--prompt` and `--prompt-file` are mutually exclusive.

---

# Maximum Output Tokens

The default maximum completion length is **256 tokens**.

You can override it:

```bash
uv run token-meter \
  --model gpt-4o-mini \
  --prompt "Explain transformers in detail." \
  --api-key YOUR_OPENAI_API_KEY \
  --max-tokens 500
```

The default limit provides a safety boundary against accidentally generating unnecessarily large responses.

---

# Supported Models

Token Meter currently validates model names for the following providers.

### OpenAI

```text
gpt-*
o1-*
```

Examples:

```text
gpt-4o-mini
gpt-4o
o1-mini
```

### Gemini

```text
gemini/*
```

Examples:

```text
gemini/gemini-2.5-flash
gemini/gemini-2.5-pro
```

Provider-specific API communication and pricing are handled by LiteLLM.

---

# API Keys & Security

API keys can be passed directly through the CLI:

```bash
--api-key YOUR_API_KEY
```

Keys are kept **in process memory only** and are not written to disk by Token Meter.

Never commit API keys to Git.

For example, avoid:

```bash
git add .
git commit -m "add api key"
```

if your API key has been placed in a tracked file.

A `.env.example` file is included for documenting local credentials, while `.env` is ignored by Git.

---

# Architecture

The project intentionally keeps the CLI, API execution, pricing, and presentation layers separate.

```text
                         token-meter
                              │
                 ┌────────────┴────────────┐
                 │                         │
           One-shot mode              REPL mode
                 │                         │
                 └────────────┬────────────┘
                              │
                           runner.py
                              │
                           LiteLLM
                              │
                           pricing.py
                              │
                         formatter.py
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  Rich                JSON
```

### Project structure

```text
token-meter/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── uv.lock
│
├── src/
│   └── token_meter/
│       ├── __init__.py
│       ├── cli.py
│       ├── repl.py
│       ├── runner.py
│       ├── pricing.py
│       ├── formatter.py
│       └── exceptions.py
│
└── tests/
```
---

# Development

Install the project and development dependencies:

```bash
uv sync
```

Run Ruff:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run the CLI locally:

```bash
uv run token-meter --help
```

---