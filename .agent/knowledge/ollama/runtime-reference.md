# Ollama Runtime Reference

CyberTron's local Ollama API is expected to be available at:

http://127.0.0.1:11434

Useful read-only endpoints:

- `/api/tags` lists locally available models.
- `/api/ps` shows currently loaded models.
- `nvidia-smi` should be used to verify GPU and VRAM utilization.
- The preferred CyberTron primary model is `qwen3.5:9b`.

If Ollama works directly but another application cannot reach it, investigate
the application integration or container networking before changing Ollama.
