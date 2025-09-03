import yaml
from jinja2 import Template
import os

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

class PromptTemplate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True}),
                "data": ("PYDICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "apply_template"

    def apply_template(self, template, data):
        return (Template(template).render(**data), )

class YAMLData:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "yaml_string": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("PYDICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "parse_yaml"

    def parse_yaml(self, yaml_string):
        parsed = yaml.safe_load(yaml_string)
        return (parsed, )

class YAMLFileLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "yaml_file": (cls._yaml_options(),{}),
            },
        }

    RETURN_TYPES = ("PYDICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "load_yaml"

    @staticmethod
    def _yaml_options() -> list[str]:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        return sorted(
            f for f in os.listdir(dir_path)
            if f.lower().endswith((".yaml", ".yml")) and os.path.isfile(os.path.join(dir_path, f))
        )

    def load_yaml(self, yaml_file: str):
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yaml_file)
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return (data, )

class MergeData:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_dict": ("PYDICT", {"forceInput": True}),
            },
            "optional": {
                "override_dict": ("PYDICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("PYDICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "merge_dicts"

    def merge_dicts(self, base_dict, override_dict = None):
        merged = base_dict.copy()
        if override_dict:
            merged.update(override_dict)
        return (merged, )