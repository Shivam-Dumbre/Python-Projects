import shutil
import tempfile
from pathlib import Path
import pytest

from organizer.config import load_settings
from organizer.organizer import organize_files

@pytest.fixture
def temp_env(tmp_path):

    watch_dir = tmp_path / "Downloads"
    dest_root = tmp_path / "Sorted"
    watch_dir.mkdir()
    dest_root.mkdir()

    (watch_dir / "photo.jpg").write_text("fake image data")
    (watch_dir / "video.mp4").write_text("fake video data")
    (watch_dir / "doc.pdf").write_text("fake doc data")
    (watch_dir / "archive.zip").write_text("fake archive data")
    (watch_dir / "random.xyz").write_text("random file")

    return watch_dir, dest_root


def test_file_organizing(temp_env, tmp_path):
    watch_dir, dest_root = temp_env

    settings = load_settings(Path("configs/config.yaml"))
    settings.watch_dir = watch_dir
    settings.dest_root = dest_root
    settings.dry_run = True

    organize_files(settings)

    assert (dest_root / "Images" / "photo.jpg").exists()
    assert (dest_root / "Videos" / "video.mp4").exists()
    assert (dest_root / "Documents" / "doc.pdf").exists()
    assert (dest_root / "Archives" / "archive.zip").exists()
    assert (dest_root / "Others" / "random.xyz").exists()
