#!/usr/bin/env bash
# Do not output dependencies and omit packages that are already in comfyUI dependency
# and are core to comfyUI's other functions
# This is mainly to not mess up with comfyUI environment
uv pip compile pyproject.toml -o requirements.txt --no-deps \
    --no-emit-package torch \
    --no-emit-package numpy \
    --no-emit-package pillow
