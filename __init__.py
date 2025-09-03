from .webdav import UploadImagesToWebDAV, UploadWebMToWebDAV, LoadImageFromWebDAV
from .exprs import IntExpr, FloatExpr
from .prompt import (
    PromptFormatter, PromptTemplate, YAMLData, YAMLFileLoader, MergeData,
    TemplateFileLoader, RegisterTemplate
)

NODE_CLASS_MAPPINGS = {
    "UploadImagesToWebDAV": UploadImagesToWebDAV,
    "UploadWebMToWebDAV": UploadWebMToWebDAV,
    "LoadImageFromWebDAV": LoadImageFromWebDAV,
    "EvalIntExpr": IntExpr,
    "EvalFloatExpr": FloatExpr,
    "PromptFormatter": PromptFormatter,
    "PromptTemplate": PromptTemplate,
    "YAMLData": YAMLData,
    "YAMLFileLoader": YAMLFileLoader,
    "MergeData": MergeData,
    "TemplateFileLoader": TemplateFileLoader,
    "RegisterTemplate": RegisterTemplate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UploadImagesToWebDAV": "Upload image(s) to WebDAV",
    "UploadWebMToWebDAV": "Upload video as WebM to WebDAV",
    "LoadImageFromWebDAV": "Load image from WebDAV",
    "EvalIntExpr": "Evaluate S-Expr with integer output",
    "EvalFloatExpr": "Evaluate S-Expr with float output",
    "PromptFormatter": "Prompt Formatter",
    "PromptTemplate": "Prompt Template",
    "YAMLData": "YAML Data",
    "YAMLFileLoader": "YAML File Loader",
    "MergeData": "Merge Data",
    "TemplateFileLoader": "Load Template File",
    "RegisterTemplate": "Register Template",
}