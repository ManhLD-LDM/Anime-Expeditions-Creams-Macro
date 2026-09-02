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
    assert (ext_dir / "Ải 1 Thử Nghiệm.png").exists()


def test_save_image_in_custom_external_folder_and_vision_discovery(tmp_path, monkeypatch):
    import cv2
    import numpy as np
    import base64

    assets_dir = tmp_path / "Assets"
    ext_dir = assets_dir / "external"
    ui_dir = assets_dir / "ui"
    ext_dir.mkdir(parents=True)
    ui_dir.mkdir(parents=True)

    monkeypatch.setattr(Api, "_image_manager_root", lambda self, cat: str(ext_dir) if cat == "external" else str(ui_dir))
    monkeypatch.setattr(vision, "EXTERNAL_ASSETS_DIR", str(ext_dir))
    monkeypatch.setattr(vision, "UI_ASSETS_DIR", str(ui_dir))

    # Create dummy 100x100 BGR image and base64 encode
    dummy = np.zeros((100, 100, 3), dtype=np.uint8)
    ok, buf = cv2.imencode(".png", dummy)
    assert ok
    data_uri = "data:image/png;base64," + base64.b64encode(buf.tobytes()).decode("ascii")

    api = Api()
    # 1. Save "lobby" into folder "Test"
    res1 = api.save_image_search_crop("external", "lobby", 0, 0, 0, 0, data_uri=data_uri, folder_name="Test")
    assert res1["ok"] is True
    assert res1["folder"] == "Test"
    assert (ext_dir / "Test" / "lobby.png").exists()

    # 2. Save "boss" into same folder "Test"
    res2 = api.save_image_search_crop("external", "boss", 0, 0, 0, 0, data_uri=data_uri, folder_name="Test")
    assert res2["ok"] is True
    assert res2["folder"] == "Test"
    assert (ext_dir / "Test" / "boss.png").exists()

    # 3. Save another "lobby" into folder "Test" (should create lobby_alt2.png)
    res3 = api.save_image_search_crop("external", "lobby", 0, 0, 0, 0, data_uri=data_uri, folder_name="Test")
    assert res3["ok"] is True
    assert (ext_dir / "Test" / "lobby_alt2.png").exists()

    # 4. Verify vision discovery finds both lobby.png and lobby_alt2.png from subfolder Test
    paths = vision.template_variant_paths("lobby", template_dir=str(ui_dir))
    assert str(ext_dir / "Test" / "lobby.png") in paths
    assert str(ext_dir / "Test" / "lobby_alt2.png") in paths

    # 5. Verify rename within folder
    rename_res = api.rename_vision_template("external", "lobby", "lobby_custom", folder_name="Test")
    assert rename_res["ok"] is True
    assert (ext_dir / "Test" / "lobby_custom.png").exists()
    assert (ext_dir / "Test" / "lobby_custom_alt2.png").exists()
    assert not (ext_dir / "Test" / "lobby.png").exists()

    # 6. Verify delete within folder
    del_res = api.delete_vision_template_image("external", "lobby_custom", "lobby_custom_alt2.png", folder_name="Test")
    assert del_res["ok"] is True
    assert not (ext_dir / "Test" / "lobby_custom_alt2.png").exists()
    assert (ext_dir / "Test" / "lobby_custom.png").exists()

