"""Serves the map catalog (Assets/map/<Category>/<Map name>.png) to the
Place Unit picker in Creation -- lets a player click a spot on a reference
map image (or a live Roblox snapshot, see main.get_roblox_snapshot) to read
off an X/Y position instead of guessing coordinates blind.
"""
import base64
import os

from . import constants

MAPS_DIR = os.path.join(constants.ASSETS_DIR, "map")
EXTERNAL_DIR = os.path.join(constants.ASSETS_DIR, "external")

_IMAGE_EXTS = (".png", ".jpg", ".jpeg")


def list_categories() -> list:
    cats = []
    if os.path.isdir(MAPS_DIR):
        cats.extend(d for d in os.listdir(MAPS_DIR) if os.path.isdir(os.path.join(MAPS_DIR, d)))
    if os.path.isdir(EXTERNAL_DIR):
        for d in os.listdir(EXTERNAL_DIR):
            full = os.path.join(EXTERNAL_DIR, d)
            if os.path.isdir(full):
                if any(f.lower().endswith(_IMAGE_EXTS) for f in os.listdir(full)):
                    cats.append(f"External: {d}")
    return sorted(set(cats), key=str.lower)


def list_maps(category: str) -> list:
    if category.startswith("External:"):
        sub = category.split(":", 1)[1].strip()
        folder = os.path.join(EXTERNAL_DIR, sub)
    else:
        folder = os.path.join(MAPS_DIR, category)
    if not os.path.isdir(folder):
        return []
    return sorted(
        os.path.splitext(f)[0] for f in os.listdir(folder)
        if f.lower().endswith(_IMAGE_EXTS)
    )


def map_image_data_uri(category: str, name: str) -> str:
    if category.startswith("External:"):
        sub = category.split(":", 1)[1].strip()
        folder = os.path.join(EXTERNAL_DIR, sub)
    else:
        folder = os.path.join(MAPS_DIR, category)
    for ext in _IMAGE_EXTS:
        path = os.path.join(folder, f"{name}{ext}")
        if os.path.isfile(path):
            mime = "image/png" if ext == ".png" else "image/jpeg"
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return ""

