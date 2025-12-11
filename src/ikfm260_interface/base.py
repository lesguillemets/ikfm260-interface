from pathlib import Path
import polars as pl

from ikfm260_interface.filehandle.base import get_id_from_filename


def add_file_info(df: pl.DataFrame, source_file: Path, file_kind) -> pl.DataFrame:
    participant_id = get_id_from_filename(source_file)
    return df.with_columns(
        [
            # participant_id is created from file name
            pl.lit(participant_id).alias("participant_id"),
            # add which file the data came from
            pl.lit(source_file.name).alias(f"{file_kind}_file_name"),
        ]
    )
