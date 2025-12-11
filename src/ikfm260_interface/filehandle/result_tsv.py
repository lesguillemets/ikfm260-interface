from pathlib import Path

from ikfm260_interface.filehandle.base import get_largest_for_each_id

import logging

logger = logging.getLogger(__name__)


def get_result_tsv(d: Path) -> tuple[list[Path], list[Path]]:
    """
    H, A の順に，与えられたディレクトリから探す
    d: 探すべきディレクトリ
    """
    assert d.is_dir()
    the_files = tuple(
        (get_largest_for_each_id(d.glob(f"*TC{g}*.tsv")) for g in ("H", "A"))
    )

    return the_files[0], the_files[1]  # FIXME: type annotation?


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", type=Path, required=True)
    args = parser.parse_args()
    h_files, a_files = get_result_tsv(args.dir)
    print("H:")
    for f in h_files:
        print(f"\t{f}")
    print("A:")
    for f in a_files:
        print(f"\t{f}")
