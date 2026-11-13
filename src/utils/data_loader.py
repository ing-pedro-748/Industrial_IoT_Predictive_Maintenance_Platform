"""Utilities to load CARE to Compare V6 from local disk or a zip archive."""
from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd


def resolve_dataset_dir(override: Optional[str] = None) -> Path:
    """Resolve the directory containing CARE_To_Compare.zip or CARE_To_Compare/."""
    if override is not None:
        return Path(override)
    try:
        import google.colab  # type: ignore

        return Path("/content")
    except Exception:
        root = Path.cwd()
        if root.name == "notebooks":
            root = root.parent
        return root / "data" / "raw" / "care_to_compare"


def find_zip(dataset_dir: Path) -> Optional[Path]:
    candidates = [
        dataset_dir / "CARE_To_Compare.zip",
        dataset_dir / "data" / "raw" / "care_to_compare" / "CARE_To_Compare.zip",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def find_extracted(dataset_dir: Path) -> Optional[Path]:
    candidates = [
        dataset_dir / "CARE_To_Compare",
        dataset_dir / "data" / "raw" / "care_to_compare" / "CARE_To_Compare",
    ]
    for p in candidates:
        if p.exists() and p.is_dir():
            return p
    return None


class DatasetSource:
    """Unified access to files either on disk or inside the zip archive."""

    def __init__(self, dataset_dir: Optional[Path] = None):
        self.dataset_dir = Path(dataset_dir) if dataset_dir is not None else resolve_dataset_dir()
        self.extracted = find_extracted(self.dataset_dir)
        self.zip_path = find_zip(self.dataset_dir)

    def read_bytes(self, rel: str) -> bytes:
        if self.extracted is not None:
            p = self.extracted / rel
            if p.exists():
                return p.read_bytes()
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as z:
                return z.read("CARE_To_Compare/" + rel)
        raise FileNotFoundError(f"Cannot locate {rel} in {self.dataset_dir}")

    def read_text(self, rel: str, encoding: str = "utf-8") -> str:
        return self.read_bytes(rel).decode(encoding, errors="replace")

    def read_csv(self, rel: str, **kwargs) -> pd.DataFrame:
        return pd.read_csv(io.BytesIO(self.read_bytes(rel)), **kwargs)

    def list_files(self, suffix: str = "") -> list[str]:
        if self.extracted is not None:
            return [str(p.relative_to(self.extracted)) for p in self.extracted.rglob("*") if p.is_file() and (not suffix or p.name.endswith(suffix))]
        if self.zip_path is not None:
            with zipfile.ZipFile(self.zip_path) as z:
                return [i.filename.replace("CARE_To_Compare/", "") for i in z.infolist() if not i.is_dir() and (not suffix or i.filename.endswith(suffix))]
        return []
