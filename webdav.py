import av
import requests
import torch
from fractions import Fraction
from requests.auth import HTTPBasicAuth
from PIL import Image, ImageOps
from datetime import datetime
import numpy as np
from io import BytesIO

class UploadImagesToWebDAV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "url":("STRING",),
                "username": ("STRING",),
                "password": ("STRING",)
            }
        }

    RETURN_TYPES=()
    OUTPUT_NODE = True
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "save_images"
    
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
            _ = requests.put(full_url, data=img_buf, auth=HTTPBasicAuth(username, password))

        return []

class UploadWebMToWebDAV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_frames": ("IMAGE",),
                "fps": ("FLOAT", {"default": 24.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                "crf": ("FLOAT", {"default": 32.0, "min": 0, "max": 63.0, "step": 1, "tooltip": "Higher crf means lower quality with a smaller file size, lower crf means higher quality higher filesize."}),
                "url":("STRING",),
                "username": ("STRING",),
                "password": ("STRING",),
                "dufs_chunk_size_mb":("INT", {"default": 0, "min": 0, "max": 128, "step": 1, "tooltip": "Chunked upload size for dufs"})
            }
        }

    RETURN_TYPES=()
    OUTPUT_NODE = True
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "save_video"
    
    def save_video(self,
        video_frames, fps, crf, url, username, password, chunk_size
    ):
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        buf = BytesIO()
        container = av.open(buf, format="webm", mode="w")
        stream = container.add_stream("libvpx-vp9", rate=Fraction(round(fps * 1000), 1000))
        stream.width = video_frames.shape[-2]
        stream.height = video_frames.shape[-3]
        stream.pix_fmt = "yuv420p"
        stream.bit_rate = 0
        stream.options = {'crf': str(crf)}
        for frame in video_frames:
            frame = av.VideoFrame.from_ndarray(torch.clamp(frame[..., :3] * 255, min=0, max=255).to(device=torch.device("cpu"), dtype=torch.uint8).numpy(), format="rgb24")
            for packet in stream.encode(frame):
                container.mux(packet)
        container.mux(stream.encode())
        container.close()
        full_url = f"{url}/{stamp}.webm"
        _ = buf.seek(0)
        if chunk_size == 0:
            _ = requests.put(full_url, data=buf, auth=HTTPBasicAuth(username, password))
        else:
            size_bytes = chunk_size * 1024 * 1024
            chunk = buf.read(size_bytes)
            if chunk:
                _ = requests.put(full_url, data=chunk, auth=HTTPBasicAuth(username, password))
            while True:
                chunk = buf.read(size_bytes)
                if not chunk:
                    break
                _ = requests.patch(full_url, data=chunk, auth=HTTPBasicAuth(username, password),
                    headers = {"X-Update-Range": "append"})
        
        return []

class LoadImageFromWebDAV:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url":("STRING",),
                "username": ("STRING",),
                "password": ("STRING",)
            }
        }

    RETURN_TYPES=("IMAGE", )
    CATEGORY = "Chaser Custom Nodes"
    FUNCTION = "load_image"
    
    def load_image(self,
        url, username, password
    ):
        resp = requests.get(url, auth=HTTPBasicAuth(username, password))
        img_buf = BytesIO(resp.content)
        img = Image.open(img_buf)
        img = ImageOps.exif_transpose(img)
        if img.mode == 'I':
            img = img.point(lambda i: i * (1 / 255))
        image = img.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image, )