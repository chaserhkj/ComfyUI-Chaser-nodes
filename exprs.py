from .exprs_eval import eval_s_expr
from sexpdata import Symbol, loads


class _NumericType(str):
    def __ne__(self, other)-> bool:
        if other == "INT" or other == "FLOAT":
            return False
        else:
            return True
numeric_type = _NumericType("*")

ARG_COUNT=4
class IntExpr:
    @classmethod
    # Dynamic variable input is ported from https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/modules/impact/util_nodes.py
    def INPUT_TYPES(cls):
        return {
            "required":{
                "expression": ("STRING", {"multiline": True})
            },
            "optional": dict( (f"arg{k}", (numeric_type, {"defaultInput": True})) for k in range(ARG_COUNT))
        }
    RETURN_TYPES = ("INT", )
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "execute"

    def execute(self, **kwargs):
        args = dict((Symbol(k), v) for k, v in kwargs.items() if k.startswith("arg"))
        s_expr = loads(kwargs["expression"])
        return eval_s_expr(s_expr, args)

class FloatExpr:
    @classmethod
    # Dynamic variable input is ported from https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/modules/impact/util_nodes.py
    def INPUT_TYPES(cls):
        return {
            "required":{
                "expression": ("STRING", {"multiline": True})
            },
            "optional": dict( (f"arg{k}", (numeric_type, {"defaultInput": True})) for k in range(ARG_COUNT))
        }
    RETURN_TYPES = ("FLOAT", )
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "execute"

    def execute(self, **kwargs):
        args = dict((Symbol(k), v) for k, v in kwargs.items() if k.startswith("arg"))
        s_expr = loads(kwargs["expression"])
        return eval_s_expr(s_expr, args)