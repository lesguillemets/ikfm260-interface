import polars as pl
from pathlib import Path

from ikfm260_interface.base import add_file_info
from ikfm260_interface.consts import CONDITION1_MAP, CONDITION2_MAP, EMOTION_MAP


def read_qr_data(file_path: Path) -> pl.DataFrame:
    """
    Reads facemimic TSV data nicely
    file_path: Path to the TSV file
    """

    df = pl.read_csv(
        file_path,
        separator=",",
        schema_overrides={
            "x": pl.Int8,
            "y": pl.Int8,
            "condition1": pl.Int8,
            "condition2": pl.Int8,
            "layout": pl.Int8,
            "emotion": pl.Int8,
            "procedure": pl.Int8,
        },
        has_header=True,
    )

    # Add some helpful transformations
    df = add_file_info(df, file_path, "qr").with_columns(
        [
            # Create meaningful condition labels using dictionary mapping
            pl.col("condition1").replace_strict(CONDITION1_MAP).alias("VisualFeedback"),
            pl.col("condition2").replace_strict(CONDITION2_MAP).alias("Reference"),
            pl.col("emotion").replace_strict(EMOTION_MAP).alias("emotion_str"),
        ]
    )

    return df


def read_qr_files(files: list[Path]) -> pl.DataFrame:
    """
    まとめてデータとして読む（被験者IDはファイル名から取って追記する）
    files: list[Path] to the TSV files
    """
    dfs = []
    for file in files:
        df = read_qr_data(file)
        dfs.append(df)
    combined_df = pl.concat(dfs, how="vertical")
    return combined_df
