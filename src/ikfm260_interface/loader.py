from pathlib import Path
import polars as pl

from ikfm260_interface.qr_decoded import load_qr_data
from ikfm260_interface.mesh import load_mesh_data


def experiment_loader(qr_path: Path, mesh_path: Path) -> pl.DataFrame:
    df_qr = load_qr_data(qr_path).collect()
    df_mesh = load_mesh_data(mesh_path)
    df = df_qr.join(df_mesh, on="participant_id", how="left")
    return df
