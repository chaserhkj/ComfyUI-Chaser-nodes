
def split_around_brackets(input_str):
    raw_split = input_str.split(",")
    result = []
    nested = []
    for tag in raw_split:
        if tag.strip().startswith("(") and tag.strip().endswith(")"):
            result.append(tag)
            continue
        if tag.strip().startswith("("):
            nested.append(tag.strip())
            continue
        if nested:
            nested.append(tag.strip())
            if tag.strip().endswith(")"):
                result.append(", ".join(nested))
                nested = []
        else:
            result.append(tag)
    return result

def split_prompt(input_str):
    # Do line-based preprocessing as well
    lines = input_str.split("\n")
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if not l.startswith("#")]
    lines = [l + "," if not l.endswith(",") else l for l in lines]
    lines = "\n".join(lines)
    tags = split_around_brackets(lines)
    tags = [t.strip() for t in tags]
    tags = [t for t in tags if t]
    return tags

class PromptFormatter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "prefix": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "format_prompt"

    def format_prompt(self, prompt, prefix=""):
        combined_tags = split_prompt(prefix) + split_prompt(prompt)
        formatted = ", ".join(combined_tags)
        return (formatted, )