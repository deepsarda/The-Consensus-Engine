import re
import json

# Thinking regex
thinking_regex = re.compile(r"<think>.*?</think>", re.DOTALL)


def process_content_return_ouput_json(content: str, member_name: str) -> dict:
    # Trim <think> and </think> if present anywhere
    content = re.sub(thinking_regex, "", content).strip()

    # Cuz of reasoning, just find { and } and extract JSON. TODO: Think of a better way.
    try:
        start_index = content.find("{")
        end_index = content.rfind("}")

        if start_index != -1 and end_index != -1:
            json_str = content[start_index : end_index + 1]
            json_output = json.loads(json_str)
            return {
                "member_name": member_name,
                "output": json_output,
            }
        else:
            raise ValueError("No JSON object found")
    except (json.JSONDecodeError, ValueError) as e:
        return {
            "error": f"Parsing error for {member_name}: {str(e)}",
            "raw_output": content,
        }
