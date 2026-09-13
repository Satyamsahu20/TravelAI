import json
import time

from langchain_core.messages import HumanMessage, SystemMessage

from config import get_llm

llm = get_llm()


def _llm_text(system: str, prompt: str, max_retries: int = 3) -> str:
    """Call the LLM and return plain text, with retry on transient errors."""
    response = None
    for attempt in range(max_retries):
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=system),
                    HumanMessage(content=prompt),
                ]
            )
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"\n⚠️ LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(3 * (attempt + 1))

    content = response.content

    # Some Gemini responses return a list of content blocks instead of a plain string
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)
        return "".join(text_parts)

    return content


def _json_from_llm(text: str) -> dict:
    print("\n========== RAW LLM RESPONSE ==========")
    print(text)
    print("======================================\n")

    start = text.index("{")
    end = text.rindex("}") + 1

    json_text = text[start:end]

    print("\n========== EXTRACTED JSON ==========")
    print(json_text)
    print("====================================\n")

    return json.loads(json_text)