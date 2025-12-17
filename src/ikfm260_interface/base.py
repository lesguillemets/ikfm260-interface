from pathlib import Path
from typing import overload
import polars as pl

from ikfm260_interface.filehandle.base import get_id_from_filename
from ikfm260_interface.consts import CONDITION1_MAP, CONDITION2_MAP, EMOTION_MAP


def gen_file_info_expr(source_file: Path, file_kind: str) -> list[pl.Expr]:
    participant_id = get_id_from_filename(source_file)
    return [
        # participant_id is created from file name
        pl.lit(participant_id).alias("participant_id"),
        # add which file the data came from
        pl.lit(source_file.name).alias(f"{file_kind}_file_name"),
    ]


@overload
def add_file_info(
    df: pl.DataFrame, source_file: Path, file_kind: str
) -> pl.DataFrame: ...


@overload
def add_file_info(
    df: pl.LazyFrame, source_file: Path, file_kind: str
) -> pl.LazyFrame: ...


def add_file_info(
    df: pl.DataFrame | pl.LazyFrame, source_file: Path, file_kind: str
) -> pl.DataFrame | pl.LazyFrame:
    return df.with_columns(gen_file_info_expr(source_file, file_kind))


COND_EMO_MAP_EXPR: list[pl.Expr] = [
    # Create meaningful condition labels using dictionary mapping
    pl.col("condition1").replace_strict(CONDITION1_MAP).alias("VisualFeedback"),
    pl.col("condition2").replace_strict(CONDITION2_MAP).alias("Reference"),
    pl.col("emotion").replace_strict(EMOTION_MAP).alias("emotion_str"),
]
