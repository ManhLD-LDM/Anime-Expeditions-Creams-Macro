"""Serves the map catalog (Assets/map/<Category>/<Map name>.png) to the
Place Unit picker in Creation -- lets a player click a spot on a reference
map image (or a live Roblox snapshot, see main.get_roblox_snapshot) to read
off an X/Y position instead of guessing coordinates blind.
"""
import base64
import os

from . import constants

MAPS_DIR = os.path.join(constants.ASSETS_DIR, "map")

_IMAGE_EXTS = (".png", ".jpg", ".jpeg")
_DEFAULT_CATEGORIES = ("Story", "Raid", "Tower", "Event", "Expedition")


def list_categories() -> list:
    """Returns the list of map category folders inside Assets/map.
    Ensures standard categories (Story, Raid, Tower, Event, Expedition) exist."""
    if not os.path.isdir(MAPS_DIR):
        os.makedirs(MAPS_DIR, exist_ok=True)
    for cat in _DEFAULT_CATEGORIES:
        os.makedirs(os.path.join(MAPS_DIR, cat), exist_ok=True)
    return sorted(
        (d for d in os.listdir(MAPS_DIR) if os.path.isdir(os.path.join(MAPS_DIR, d))),
        key=lambda x: (_DEFAULT_CATEGORIES.index(x) if x in _DEFAULT_CATEGORIES else 999, x.lower()),
    )


def list_maps(category: str) -> list:
    folder = os.path.join(MAPS_DIR, category)
    if not os.path.isdir(folder):
        return []
    return sorted(
        os.path.splitext(f)[0] for f in os.listdir(folder)
        if f.lower().endswith(_IMAGE_EXTS)
    )


def map_image_data_uri(category: str, name: str) -> str:
    folder = os.path.join(MAPS_DIR, category)
    for ext in _IMAGE_EXTS:
        path = os.path.join(folder, f"{name}{ext}")
        if os.path.isfile(path):
            mime = "image/png" if ext == ".png" else "image/jpeg"
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    return ""

