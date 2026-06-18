from __future__ import annotations

import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.voice_traits_summary_and_response import (  # noqa: E402
    VOICE_TRAIT_TOOL_NAME,
    VOICE_TRAIT_TOOL_SCHEMA,
    normalize_voice_trait_tool_arguments,
)


def demo_tool_call() -> dict:
    return {
        "type": "function_call",
        "name": VOICE_TRAIT_TOOL_NAME,
        "call_id": "call_demo_voice_trait_carryover",
        "arguments": {
            "extracted_traits_summary": (
                "English input with informal, support-seeking register; subdued pace, "
                "low-energy delivery, and uncertainty markers. No identity or diagnostic "
                "claim is inferred."
            ),
            "response_to_extracted_traits_summary": (
                "Respond in English with calm, gentle, low-pressure wording. Keep the "
                "answer short, concrete, and warm without imitating vocal style or "
                "explicitly labeling the user's affect."
            ),
        },
    }


def main() -> None:
    tool_call = demo_tool_call()
    normalized = normalize_voice_trait_tool_arguments(tool_call["arguments"])
    function_call_output = {
        "type": "function_call_output",
        "call_id": tool_call["call_id"],
        "output": json.dumps(normalized, ensure_ascii=False),
    }

    print("\n=== Tool available to the model ===")
    print(json.dumps(VOICE_TRAIT_TOOL_SCHEMA, indent=2, ensure_ascii=False))
    print("\n=== Model-emitted ancillary tool call ===")
    print(json.dumps(tool_call, indent=2, ensure_ascii=False))
    print("\n=== No-op protocol echo ===")
    print(json.dumps(function_call_output, indent=2, ensure_ascii=False))
    print("\n=== Carryover available for final spoken answer ===")
    print(json.dumps(normalized, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
