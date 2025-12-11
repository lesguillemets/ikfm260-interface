from pathlib import Path


def is_denormed_file(f: Path) -> bool:
    return f.stem.split("_")[-1] == "denorm"
