"""
メッシュのファイルを polars として読み込む
"""

from pathlib import Path

import numpy as np
import polars as pl

from ikfm260_interface.filehandle.mesh_numpy import is_denormed_file
from ikfm260_interface.base import add_file_info


def load_mesh_data(f: Path) -> pl.DataFrame:
    """
    input file : np.ndarray of shape (n_frames, n_landmarks, [x,y,z])
    """
    dat = np.load(f)
    is_denorm = is_denormed_file(f)

    df = numpy_landmarks_to_df(dat)
    df = add_file_info(df, f, "mesh")
    return df.with_columns(
        pl.lit(is_denorm).alias("is_denorm"),
    )


def numpy_landmarks_to_df(dat: np.ndarray) -> pl.DataFrame:
    n_frames, n_landmarks, _ = dat.shape
    reshaped = dat.reshape(n_frames, -1)
    # lm_0_x, lm_0_y, ...
    col_names = [f"lm_{coord}_{i}" for i in range(n_landmarks) for coord in "xyz"]
    df = pl.from_numpy(reshaped, schema=col_names)
    df = df.with_columns(pl.Series("Frame", range(1, n_frames + 1)))
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=Path, required=True)
    args = parser.parse_args()
    pl.Config.set_tbl_rows(-1)
    pl.Config.set_tbl_cols(-1)
    df = load_mesh_data(args.file)
    print(df)
    print(df.describe())
