from .webdav import UploadImagesToWebDAV, UploadWebMToWebDAV

NODE_CLASS_MAPPINGS = {
    "UploadImagesToWebDAV": UploadImagesToWebDAV,
    "UploadWebMToWebDAV": UploadWebMToWebDAV,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UploadImagesToWebDAV": "Upload image(s) to WebDAV",
    "UploadWebMToWebDAV": "Upload video as WebM to WebDAV",
}