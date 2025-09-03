import yaml
from jinja2 import Environment, DictLoader, Template
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

    RETURN_TYPES = ("STRING", "TAGS")
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "format_prompt"

    def format_prompt(self, prompt, prefix=""):
        combined_tags = split_prompt(prefix) + split_prompt(prompt)
        formatted = ", ".join(combined_tags)
        return (formatted, combined_tags)

class PromptTemplate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template": ("STRING", {"multiline": True}),
            },
            "optional": {
                "tmpl_dict": ("TMPL_DICT", {"forceInput": True}),
                "data": ("PYDICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "apply_template"

    def apply_template(self, template, data={}, tmpl_dict=None):
        env_config = {
            "variable_start_string": "[",
            "variable_end_string": "]"
        }
        if tmpl_dict:
            env = Environment(loader=DictLoader(tmpl_dict), **env_config)
        else:
            env = Environment(**env_config)
        tmpl = env.from_string(template)
        return (tmpl.render(**data), )

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

class TemplateFileLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template_file": (cls._template_options(), {}),
            },
            "optional": {
                "tmpl_dict": ("TMPL_DICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("TMPL_DICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "load_template"

    @staticmethod
    def _template_options() -> list[str]:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        return sorted(
            f for f in os.listdir(dir_path)
            if f.lower().endswith((".j2", ".jinja", ".txt")) and os.path.isfile(os.path.join(dir_path, f))
        )

    def load_template(self, template_file: str, tmpl_dict=None):
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), template_file)
        with open(full_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        name = os.path.splitext(template_file)[0]
        if tmpl_dict:
            result = tmpl_dict.copy()
        else:
            result = {}
        result[name] = template_str
        return (result, )

class RegisterTemplate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template_name": ("STRING", {"forceInput": True}),
                "template_source": ("STRING", {"multiline": True}),
            },
            "optional": {
                "tmpl_dict": ("TMPL_DICT", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("TMPL_DICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "register_template"

    def register_template(self, template_name, template_source, tmpl_dict=None):
        # Start with the supplied dict or an empty one
        result = tmpl_dict.copy() if tmpl_dict else {}
        # Add/overwrite the template
        result[template_name] = template_source
        return (result, )

class SetData:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("*", {"forceInput": True}),
                "key": ("STRING",), 
            },
        }

    RETURN_TYPES = ("PYDICT", )
    OUTPUT_NODE = False
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "set_data"

    def set_data(self, data, key):
        return ({key: data}, )