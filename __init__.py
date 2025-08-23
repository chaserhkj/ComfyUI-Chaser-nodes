from .webdav import UploadImagesToWebDAV, UploadWebMToWebDAV, LoadImageFromWebDAV

NODE_CLASS_MAPPINGS = {
    "UploadImagesToWebDAV": UploadImagesToWebDAV,
    "UploadWebMToWebDAV": UploadWebMToWebDAV,
    "LoadImageFromWebDAV": LoadImageFromWebDAV,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UploadImagesToWebDAV": "Upload image(s) to WebDAV",
    "UploadWebMToWebDAV": "Upload video as WebM to WebDAV",
    "LoadImageFromWebDAV": "Load image from WebDAV"
}