from pathlib import Path
from typing import Iterable
from ikfm260_interface.consts import ID_PAT

import logging

logger = logging.getLogger(__name__)


def is_group_a(p: Path) -> bool:
    """
    Aのほうのやつですか
    """
    return "TCA" in p.name


def is_group_h(p: Path) -> bool:
    """
    Hのほうのやつですか
    """
    return "TCH" in p.name


def gather_files_HandA(d: Path, pat: str) -> tuple[list[Path], list[Path]]:
    """
    与えられたディレクトリからパターンに合致するファイルを探して，
    H, A, の tupleで返す． ID ごとに一番容量の大きいファイルを探す過程で
    ID のないファイルは失われる．
    d: 探すべきディレクトリ
    """
    assert d.is_dir()
    h_files = []
    a_files = []
    for file in get_largest_for_each_id((d.glob(pat))):
        if is_group_h(file):
            h_files.append(file)
        elif is_group_a(file):
            a_files.append(file)
        else:
            logger.warn(f"no id for {file}")
    return h_files, a_files


def get_id_from_filename(p: Path) -> str | None:
    """
    ファイル名からIDを抽出
    """
    mat = ID_PAT.search(p.name)
    if mat is not None:
        return "7" + mat.group(0)
    else:
        return None


def get_largest_for_each_id(files: Iterable[Path]) -> list[Path]:
    """
    if there are more than one files for each ID, the largest file should be the proper run
    files: list of (Path, ID)
    """
    # we could group then sort but...
    id_to_file = {}
    for f in files:
        id_ = get_id_from_filename(f)
        if id_ is None:
            # ID ないのはスキップ
            # TODO: 単に足してもいいのかもしれない
            logger.warning(f"skipping {f} as it doesn't contain an ID")
            continue
        if id_ not in id_to_file:
            # 初めて見た ID
            id_to_file[id_] = f
        else:
            # 既出の ID のなかでは一番大きいファイルを使う
            if f.stat().st_size > id_to_file[id_].stat().st_size:
                id_to_file[id_] = f
    # the result is sorted by ID
    return [f for (_id, f) in sorted(id_to_file.items())]
