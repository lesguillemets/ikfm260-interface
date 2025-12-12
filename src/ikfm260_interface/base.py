from pathlib import Path
import polars as pl

from ikfm260_interface.filehandle.base import get_id_from_filename


def gen_file_info_expr(source_file: Path, file_kind: str) -> list[pl.Expr]:
    participant_id = get_id_from_filename(source_file)
    return [
        # participant_id is created from file name
        pl.lit(participant_id).alias("participant_id"),
        # add which file the data came from
        pl.lit(source_file.name).alias(f"{file_kind}_file_name"),
    ]


def add_file_info(df: pl.DataFrame, source_file: Path, file_kind: str) -> pl.DataFrame:
    return df.with_columns(gen_file_info_expr(source_file, file_kind))
