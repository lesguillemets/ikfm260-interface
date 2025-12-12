import polars as pl
from pathlib import Path

from ikfm260_interface.base import gen_file_info_expr, COND_EMO_MAP_EXPR


QR_SCHEMA_OVERRIDES = {
    "x": pl.Int8,
    "y": pl.Int8,
    "condition1": pl.Int8,
    "condition2": pl.Int8,
    "layout": pl.Int8,
    "emotion": pl.Int8,
    "procedure": pl.Int8,
}


def load_qr_data(file_path: Path) -> pl.LazyFrame:
    """
    Reads facemimic TSV data nicely
    file_path: Path to the TSV file
    """

    df = pl.scan_csv(
        file_path,
        separator=",",
        schema_overrides=QR_SCHEMA_OVERRIDES,
        has_header=True,
    )

    # Add some helpful transformations
    df = df.with_columns(COND_EMO_MAP_EXPR + gen_file_info_expr(file_path, "qr"))

    return df


def read_qr_files(files: list[Path]) -> pl.DataFrame:
    """
    まとめてデータとして読む（被験者IDはファイル名から取って追記する）
    files: list[Path] to the TSV files
    """
    dfs = []
    for file in files:
        df = load_qr_data(file)
        dfs.append(df)
    combined_df = pl.concat(dfs, how="vertical")
    return combined_df
