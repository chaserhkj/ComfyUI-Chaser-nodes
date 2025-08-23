import requests
from requests.auth import HTTPDigestAuth
from PIL import Image
from datetime import datetime
import numpy as np
from io import BytesIO

class UploadImagesToWebDAV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("Image",),
                "url":("STRING",),
                "username": ("STRING",),
                "password": ("STRING",)
            }
        }

    RETURN_TYPES=()
    OUTPUT_NODE = True
    CATEGORY = "Chaser Custom Nodes"
    
    def save_images(self,
        images, url, username, password
    ):
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        
        for (i, img) in enumerate(images):
            img = 255. * img.cpu().numpy()
            img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
            img_buf = BytesIO()
            img.save(img_buf, format='PNG')
            full_url = f"{url}/{stamp}_{i}.png"
            _ = img_buf.seek(0)
            _ = requests.put(full_url, data=img_buf, auth=HTTPDigestAuth(username, password))