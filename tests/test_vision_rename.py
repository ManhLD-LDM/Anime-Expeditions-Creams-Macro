import os
import pytest
from main import Api
from core import vision

def test_rename_vision_template_success(tmp_path, monkeypatch):
    assets_dir = tmp_path / "Assets"
    ext_dir = assets_dir / "external"
    ext_dir.mkdir(parents=True)

    folder = ext_dir / "my_stage"
    folder.mkdir()
    (folder / "my_stage.png").write_bytes(b"data1")
    (folder / "my_stage_alt2.png").write_bytes(b"data2")

    monkeypatch.setattr(Api, "_image_manager_root", lambda self, cat: str(ext_dir) if cat == "external" else None)

    api = Api()
    res = api.rename_vision_template("external", "my_stage", "spirit_city_custom")
    assert res["ok"] is True
    assert res["new_name"] == "spirit_city_custom"

    assert not folder.exists()
    new_folder = ext_dir / "spirit_city_custom"
    assert new_folder.exists()
    assert (new_folder / "spirit_city_custom.png").exists()
    assert (new_folder / "spirit_city_custom_alt2.png").exists()

def test_rename_vision_template_duplicate_rejected(tmp_path, monkeypatch):
    assets_dir = tmp_path / "Assets"
    ext_dir = assets_dir / "external"
    ext_dir.mkdir(parents=True)

    folder1 = ext_dir / "stage1"
    folder1.mkdir()
    (folder1 / "stage1.png").write_bytes(b"data1")

    folder2 = ext_dir / "stage2"
    folder2.mkdir()
    (folder2 / "stage2.png").write_bytes(b"data2")

    monkeypatch.setattr(Api, "_image_manager_root", lambda self, cat: str(ext_dir) if cat == "external" else None)

    api = Api()
    res = api.rename_vision_template("external", "stage1", "stage2")
    assert res["ok"] is False
    assert res["reason"] == "name_already_exists"


def test_save_image_search_crop_unicode_and_full_frame(tmp_path, monkeypatch):
    import cv2
    import numpy as np
    import base64

    assets_dir = tmp_path / "Assets"
    ext_dir = assets_dir / "external"
    ext_dir.mkdir(parents=True)

    monkeypatch.setattr(Api, "_image_manager_root", lambda self, cat: str(ext_dir) if cat == "external" else None)

    # Create dummy 100x100 BGR image and base64 encode
    dummy = np.zeros((100, 100, 3), dtype=np.uint8)
    ok, buf = cv2.imencode(".png", dummy)
    assert ok
    data_uri = "data:image/png;base64," + base64.b64encode(buf.tobytes()).decode("ascii")

    api = Api()
    # Test saving with Vietnamese Unicode name and full frame fallback (w=0, h=0)
    res = api.save_image_search_crop("external", "Ải 1 Thử Nghiệm", 0, 0, 0, 0, data_uri=data_uri)
    assert res["ok"] is True
    assert res["name"] == "Ải 1 Thử Nghiệm"
    saved_folder = ext_dir / "Ải 1 Thử Nghiệm"
    assert saved_folder.exists()
    assert (saved_folder / "Ải 1 Thử Nghiệm.png").exists()

