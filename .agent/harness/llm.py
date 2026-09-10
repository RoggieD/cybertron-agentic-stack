"""CyberTron shared model-call helper.

Default provider: local Ollama.
Optional providers: Grok/xAI, OpenAI, Anthropic, MiniMax.
"""
import json
import os
import urllib.error
import urllib.request


MINIMAX_REGIONS = {
    "global_en": {
        "openai_base_url": "https://api.minimax.io/v1",
        "anthropic_base_url": "https://api.minimax.io/anthropic",
    },
    "cn_zh": {
        "openai_base_url": "https://api.minimaxi.com/v1",
        "anthropic_base_url": "https://api.minimaxi.com/anthropic",
    },
}

MINIMAX_MODELS = {
    "MiniMax-M3": {"context_window": 1000000},
    "MiniMax-M2.7": {"context_window": 204800},
}

MINIMAX_DEFAULT_MODEL = "MiniMax-M3"

DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_MODEL = "qwen3.5:9b"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"

XAI_BASE_URL = "https://api.x.ai/v1"
DEFAULT_GROK_MODEL = "grok-4.6"


def _provider():
    return os.getenv("AGENT_PROVIDER", DEFAULT_PROVIDER).lower()


def llm_available():
    """Return True when the selected provider has the required configuration."""
    provider = _provider()

    if provider == "ollama":
        return True

    if provider == "grok":
        return bool(os.getenv("XAI_API_KEY"))

    if provider == "anthropic":
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))

    if provider == "minimax":
        return bool(os.getenv("MINIMAX_API_KEY"))

    return False


def _call_ollama(system, user, *, temperature, max_tokens, model):
    """Call CyberTron's local Ollama API using Python's standard library."""
    base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL).rstrip("/")
    model = model or os.getenv("AGENT_MODEL", DEFAULT_OLLAMA_MODEL)

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    request = urllib.request.Request(
        f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    timeout = int(os.getenv("AGENT_OLLAMA_TIMEOUT", "300"))

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ollama HTTP {exc.code}: {body[:500]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Unable to reach Ollama at {base_url}: {exc.reason}"
        ) from exc

    try:
        return data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected Ollama response: {str(data)[:500]}"
        ) from exc


def _call_grok(system, user, *, temperature, max_tokens, model):
    """Call xAI Grok through its OpenAI-compatible API."""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY is not configured")

    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url=XAI_BASE_URL,
    )

    response = client.chat.completions.create(
        model=model or os.getenv("AGENT_MODEL", DEFAULT_GROK_MODEL),
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    return response.choices[0].message.content


def _minimax_region():
    region = os.getenv("AGENT_MINIMAX_REGION", "global_en").lower()
    if region not in MINIMAX_REGIONS:
        raise ValueError(f"unknown MiniMax region: {region}")
    return region


def _call_minimax(system, user, *, temperature, max_tokens, model):
    region = _minimax_region()
    base_urls = MINIMAX_REGIONS[region]

    model = model or os.getenv("AGENT_MODEL", MINIMAX_DEFAULT_MODEL)

    if model not in MINIMAX_MODELS:
        raise ValueError(
            f"unknown MiniMax model: {model}. "
            f"Supported: {', '.join(MINIMAX_MODELS)}"
        )

    api_key = os.getenv("MINIMAX_API_KEY", "")
    wire = os.getenv("AGENT_MINIMAX_WIRE", "openai").lower()

    if wire == "anthropic":
        from anthropic import Anthropic

        client = Anthropic(
            api_key=api_key,
            base_url=base_urls["anthropic_base_url"],
        )

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )

        return response.content[0].text

    if wire == "openai":
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=base_urls["openai_base_url"],
        )

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )

        return response.choices[0].message.content

    raise ValueError(f"unknown MiniMax wire: {wire}")


def call_model(system, user, *, temperature=0.3, max_tokens=4096, model=None):
    provider = _provider()

    if provider == "ollama":
        return _call_ollama(
            system,
            user,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
        )

    if provider == "grok":
        return _call_grok(
            system,
            user,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
        )

    if provider == "anthropic":
        from anthropic import Anthropic

        client = Anthropic()

        response = client.messages.create(
            model=model or os.getenv("AGENT_MODEL", "claude-sonnet-4-5"),
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )

        return response.content[0].text

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI()

        response = client.chat.completions.create(
            model=model or os.getenv("AGENT_MODEL", "gpt-4o"),
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )

        return response.choices[0].message.content

    if provider == "minimax":
        return _call_minimax(
            system,
            user,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
        )

    raise ValueError(f"unknown provider: {provider}")
