import glob
import os
import subprocess

import anndata as ad
import numpy as np
import polars as pl
import scanpy as sc

from ._data_loader import DataLoader


class LoadBI(DataLoader):
    def __init__(self) -> None:
        name = "bi"
        data_path = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE131928&format=file"
        meta_path = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE131928&format=file&file=GSE131928%5Fsingle%5Fcells%5Ftumor%5Fname%5Fand%5Fadult%5For%5Fpeidatric%2Exlsx"
        work_dir = os.path.dirname(__file__)
        super().__init__(
            name=name, 
            data_path=data_path,
            meta_path=meta_path,
            work_dir=work_dir
        )


    def fetch(self) -> None:
        cmd = f"sh {self.work_dir}/{self.name}.sh {self.data_path} {self.meta_path}"
        subprocess.call(cmd.split())
        return None


    def transpose(self) -> None:
        data_files = {
            (lambda v: "bi-10x" if "10X" in v else "bi-ss2")(fn): fn for fn in glob.glob(
                f"{self.work_dir}/{self.name}/*_TPM.tsv"
            )
        }
        fmt_func = {
            "bi-10x":lambda pldf: pl.DataFrame(
                np.log2(pldf.to_numpy() + 1),
                schema=pldf.columns
            ), # TPM -> log2(TPM + 1)
            "bi-ss2": lambda pldf: pl.DataFrame(
                np.log2(10 * (2 ** pldf.to_numpy() - 1) + 1),
                schema=pldf.columns
            ) # log2(TPM/10 + 1) -> log2(TPM + 1)
        }
        for name, fn in data_files.items():
            _data = pl.scan_csv(
                fn,
                separator="\t",
                infer_schema_length=10000
            )
            pl.concat(
                [
                    _data.select("GENE").collect(),
                    fmt_func[name](_data.drop("GENE").collect())
                ],
                how="horizontal"
            ).drop("GENE").transpose(
                include_header=True,
                header_name="index",
                column_names=_data.select("GENE").collect().to_numpy().ravel()
            ).lazy().sink_ipc(f"{self.work_dir}/{self.name}/{name}.feather")
        return None


    def adjust_format(self) -> None:
        data_files = {
            (lambda v: "bi-10x" if "10X" in v else "bi-ss2")(fn): fn for fn in glob.glob(
                f"{self.work_dir}/{self.name}/*_TPM.tsv"
            )
        }
        self.meta = pl.read_excel(
            f"{self.work_dir}/{self.name}/bi.xlsx",
            read_csv_options={
                "skip_rows": 43,
                "skip_rows_after_header": 2
            }
        )
        for name, fn in data_files.items():
            _data = pl.scan_csv(
                fn,
                separator="\t",
                infer_schema_length=10000
            )
            _data.drop("GENE").collect().transpose(
                include_header=True,
                column_names=_data.select("GENE").collect().to_numpy().ravel()
            )
        return None
