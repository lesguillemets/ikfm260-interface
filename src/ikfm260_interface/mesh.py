from pathlib import Path

import numpy as np
import polars as pl

from ikfm260_interface.filehandle.base import get_id_from_filename
from ikfm260_interface.filehandle.mesh_numpy import is_denormed_file


def load_mesh_data(f: Path) -> pl.DataFrame:
    """
    input file : np.ndarray of shape (n_frames, n_landmarks, [x,y,z])
    """
    dat = np.load(f)
    is_denorm = is_denormed_file(f)
    participant_id = get_id_from_filename(f)

    df = numpy_landmarks_to_df(dat)
    return df.with_columns(
        [
            pl.lit(is_denorm).alias("is_denorm"),
            pl.lit(participant_id).alias("participant_id"),
            # add which file the data came from
            pl.lit(f.name).alias("mesh_file_name"),
        ]
    )


def numpy_landmarks_to_df(dat: np.ndarray) -> pl.DataFrame:
    n_frames, n_landmarks, _ = dat.shape
    reshaped = dat.reshape(n_frames, -1)
    # lm_0_x, lm_0_y, ...
    col_names = [f"lm_{coord}_{i}" for i in range(n_landmarks) for coord in "xyz"]
    df = pl.from_numpy(reshaped, schema=col_names)
    df = df.with_columns(pl.Series("frame", range(n_frames)))
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
