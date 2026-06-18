from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = REPO_ROOT / "prompts"


PROMPT_PARTS = [
    "system_prompt_with_trait_tool.txt",
    "voice_traits_extraction_guidelines.txt",
    "response_to_extracted_voice_traits_guidelines.txt",
    "voice_trait_tool_contract.txt",
]


def build_experiment_prompt() -> str:
    parts = []
    for filename in PROMPT_PARTS:
        path = PROMPT_DIR / filename
        parts.append(path.read_text(encoding="utf-8").strip())
    return "\n\n".join(part for part in parts if part)


def main() -> None:
    prompt = build_experiment_prompt()
    print(prompt)


if __name__ == "__main__":
    main()

