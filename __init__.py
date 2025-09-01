from .webdav import UploadImagesToWebDAV, UploadWebMToWebDAV, LoadImageFromWebDAV
from .exprs import IntExpr, FloatExpr

NODE_CLASS_MAPPINGS = {
    "UploadImagesToWebDAV": UploadImagesToWebDAV,
    "UploadWebMToWebDAV": UploadWebMToWebDAV,
    "LoadImageFromWebDAV": LoadImageFromWebDAV,
    "EvalIntExpr": IntExpr,
    "EvalFloatExpr": FloatExpr
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UploadImagesToWebDAV": "Upload image(s) to WebDAV",
    "UploadWebMToWebDAV": "Upload video as WebM to WebDAV",
    "LoadImageFromWebDAV": "Load image from WebDAV",
    "EvalIntExpr": "Evaluate S-Expr with integer output",
    "EvalFloatExpr": "Evaluate S-Expr with float output"
}