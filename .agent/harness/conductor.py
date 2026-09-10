"""Thin conductor loop. Reads files, calls the model, logs. No reasoning here."""
import os, sys
from context_budget import build_context
from hooks.post_execution import log_execution
from llm import call_model

RESERVED = 40000
MAX_CTX = int(os.getenv("AGENT_MAX_CONTEXT", "128000"))


SYSTEM_PREAMBLE = (
    "You are CyberTron, an agent with externalized memory, skills, and protocols.\n"
    "Your memory, skills, and constraints are in the context below.\n"
    "Read them before acting and follow constraints strictly.\n"
    "This standalone harness does not provide shell, file-write, network, or other tool execution.\n"
    "Do not claim to have run commands, changed files, queried systems, or updated memory unless actual tool output or execution evidence is present in the conversation.\n"
    "When hands-on action is required, provide the operator with the exact read-only or approved command to run and explain the expected result.\n"
    "Treat proposed actions as recommendations, not completed actions.\n\n"
)


def run(user_input: str) -> str:
    context, used = build_context(user_input, budget=MAX_CTX - RESERVED)
    system = SYSTEM_PREAMBLE + context
    try:
        result = call_model(system, user_input)
        log_execution("conductor", user_input[:100], result[:500], True)
        return result
    except Exception as e:
        log_execution("conductor", user_input[:100], str(e), False)
        raise


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or sys.stdin.read()
    print(run(prompt))
