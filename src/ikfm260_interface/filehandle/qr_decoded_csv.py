"""
qr_decoded.csv 関連
"""

from pathlib import Path

from ikfm260_interface.filehandle.base import gather_files_HandA
from ikfm260_interface.consts import FILE_SUFFIXES


def get_qr_csv(d: Path) -> tuple[list[Path], list[Path]]:
    """
    H, A の順に，与えられたディレクトリから探す
    d: 探すべきディレクトリ
    """
    file_prefix = FILE_SUFFIXES["QR"]
    return gather_files_HandA(d, f"*{file_prefix}")
