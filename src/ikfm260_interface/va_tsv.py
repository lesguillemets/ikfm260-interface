import polars as pl
from pathlib import Path
from ikfm260_interface.base import add_file_info
from ikfm260_interface.consts import CONDITION1_MAP, CONDITION2_MAP, EMOTION_MAP


def read_va_data(file_path: Path) -> pl.DataFrame:
    """
    Reads facemimic TSV data nicely
    file_path: Path to the TSV file
    """

    df = pl.read_csv(
        file_path,
        separator="\t",
        schema_overrides={
            "index": pl.Int8,
            "condition1": pl.Int8,
            "condition2": pl.Int8,
            "layout": pl.Int8,
            "emotion": pl.Int8,
            "procedure": pl.Int8,
        },
        has_header=True,
    )

    # Add some helpful transformations
    df = add_file_info(df, file_path, "va_tsv").with_columns(
        [
            pl.col("x").cast(pl.Int8),
            pl.col("y").cast(pl.Int8),
            pl.col("gender").cast(bool).alias("gender_b"),
            # Create meaningful condition labels using dictionary mapping
            pl.col("condition1").replace_strict(CONDITION1_MAP).alias("VisualFeedback"),
            pl.col("condition2").replace_strict(CONDITION2_MAP).alias("Reference"),
            pl.col("emotion").replace_strict(EMOTION_MAP).alias("emotion_str"),
            # Add distance from origin
            (pl.col("x") ** 2 + pl.col("y") ** 2).sqrt().alias("distance_from_origin"),
        ]
    )

    return df


def read_va_files(files: list[Path]) -> pl.DataFrame:
    """
    まとめてデータとして読む（被験者IDはファイル名から取って追記する）
    files: list[Path] to the TSV files
    """
    dfs = []
    for file in files:
        df = read_va_data(file)
        dfs.append(df)
    combined_df = pl.concat(dfs, how="vertical")
    return combined_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=Path, required=True)
    args = parser.parse_args()
    pl.Config.set_tbl_rows(-1)
    pl.Config.set_tbl_cols(-1)
    df = read_va_files([args.file])
    print(df)
    print(df.describe())
