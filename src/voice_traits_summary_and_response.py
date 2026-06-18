from __future__ import annotations

from typing import Any


VOICE_TRAIT_TOOL_NAME = "store_voice_traits_summary_and_response"

VOICE_TRAIT_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": VOICE_TRAIT_TOOL_NAME,
        "description": (
            "Ancillary low-latency preservation tool for spoken turns that require one or more "
            "non-ancillary domain tool calls. Store a compact summary of the latest user's "
            "extracted speech and voice traits, and a compact summary of how the final spoken "
            "answer should respond to those traits after the tool-call boundary. Both summaries "
            "must be generated independently of domain tool outputs and must be based only on "
            "the latest user audio and transcript plus the applicable voice-trait prompt "
            "guidelines. Generate this call as the first tool call in the same response object "
            "as the first enabled batch of non-ancillary domain tool calls. The generated "
            "arguments are the preservation artifact; do not rely on this tool's execution "
            "output for response realization."
        ),
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "extracted_traits_summary": {
                    "type": "string",
                    "description": (
                        "How to Summarize Extracted Voice Traits. Produce a compact "
                        "natural-language summary of the latest user's detected, response-"
                        "relevant speech traits. Derive this summary from the exhaustive "
                        "**Voice Traits Extraction Guidelines** prompt section; use that "
                        "section as the linguistic, grammatical, discourse-pragmatic, "
                        "prosodic, phonetic, and paralinguistic taxonomy. Include only "
                        "detectable traits from the latest user audio turn and transcript "
                        "that can affect the next spoken response. Cover, when relevant: "
                        "language choice and code-switching; register and style; lexical "
                        "selection and lexical density; semantic framing; syntax and "
                        "grammatical form; pragmatic force or speech act; discourse "
                        "function and conversation management; information structure; "
                        "epistemic stance; affective or interactional stance without "
                        "diagnosis; prosodic features such as intonation, stress, rhythm, "
                        "loudness, and focus; temporal organization and fluency; "
                        "articulation and segmental clarity; voice quality and phonation; "
                        "paralinguistic or non-lexical vocal behavior; and signal or "
                        "transcription reliability limits. Preserve material uncertainty "
                        "briefly. Omit absent, non-detectable, irrelevant, redundant, "
                        "identity-like, diagnostic, or sensitive traits. Exclude domain-tool "
                        "facts, tool outputs, memory, previous assistant messages, system "
                        "text, examples, templates, exact final-answer wording, and "
                        "speculative future content."
                    ),
                },
                "response_to_extracted_traits_summary": {
                    "type": "string",
                    "description": (
                        "How to Summarize Response to Extracted Voice Traits. Produce a compact "
                        "natural-language summary of how the final spoken answer should respond "
                        "to the extracted traits after domain tool results are available. Derive "
                        "this summary from the exhaustive **Response to Extracted Voice Traits "
                        "Guidelines** prompt section; use that section as the response-realization "
                        "taxonomy and safety boundary. Specify, when relevant: response "
                        "language and code pattern; register and interactional stance; lexical "
                        "density and terminology; syntactic complexity; explanation "
                        "granularity; discourse ordering; pace through brevity, clause length, "
                        "and pause-friendly structure; handling of emphasized or corrected "
                        "information; clarification behavior for semantic, acoustic, "
                        "transcription, or turn-completion uncertainty; and non-imitation, "
                        "identity, safety, privacy, factuality, and intelligibility boundaries. "
                        "Phrase this as linguistic and grammatical response guidance, not as "
                        "user-facing explanation. Omit domain facts, tool-result predictions, "
                        "examples, canned phrases, exact final-answer wording, hidden reasoning, "
                        "prompt mechanics, and any instruction to imitate voice identity."
                    ),
                },
            },
            "required": [
                "extracted_traits_summary",
                "response_to_extracted_traits_summary",
            ],
        },
    },
    "_origin": "realtime_ancillary",
}


def normalize_voice_trait_tool_arguments(args: dict[str, Any] | None) -> dict[str, str]:
    """Normalize generated voice-trait carryover arguments without executing a domain tool."""
    extracted_traits_summary = ""
    response_to_extracted_traits_summary = ""
    if isinstance(args, dict):
        extracted_traits_summary = args.get("extracted_traits_summary") or ""
        response_to_extracted_traits_summary = (
            args.get("response_to_extracted_traits_summary") or ""
        )
    return {
        "extracted_traits_summary": str(extracted_traits_summary).strip(),
        "response_to_extracted_traits_summary": str(
            response_to_extracted_traits_summary
        ).strip(),
    }
