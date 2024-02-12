import glob
import os
import subprocess

import anndata as ad
import numpy as np
import polars as pl
import scanpy as sc

from ._data_loader import DataLoader
from rightgbm.external.tqdm import tqdm
import rightgbm.external.polars as epl


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


    def to_feather(self) -> None:
        data_files = {
            (lambda v: "bi-10x" if "10X" in v else "bi-ss2")(fn): fn for fn in glob.glob(
                f"{self.work_dir}/{self.name}/*_TPM.tsv"
            )
        }
        meta = pl.read_excel(
            f"{self.work_dir}/{self.name}/bi.xlsx",
            read_csv_options={
                "skip_rows": 43,
                "skip_rows_after_header": 2
            }
        ).lazy()

        # convert units into log2(TPM + 1)
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
        for name, fn in tqdm(
            data_files.items(), 
            desc="Generating .feather files", 
            total=len(data_files)
        ):
            # filter out meta data for pediatric samples and unrelated samples
            corresponding_meta = meta.filter(
                (
                    pl.col("processed data file") == "_".join(
                        os.path.basename(fn).split("_")[1:]
                    )
                ) & (
                    pl.col("adult/pediatric") == "adult")
            ).rename(
            # rename "adult/pediatric" to avoid bugs in i/o of h5ad files
                {"adult/pediatric": "adult or pediatric"}
            )
            valid_samples = corresponding_meta.select("Sample name").collect(
                streaming=True
            ).to_numpy().ravel().tolist()
            _data = pl.scan_csv(
                fn,
                separator="\t",
                infer_schema_length=10000
            )

            # export data as feather files in self.work_dir
            pl.concat(
                [
                    _data.select("GENE").collect(),
                    fmt_func[name](_data.drop("GENE").collect()) # convert units for the matrix
                ],
                how="horizontal"
            ).drop("GENE").transpose(
                include_header=True,
                header_name="index",
                column_names=_data.select("GENE").collect().to_numpy().ravel()
            ).lazy().filter(
                pl.col("index").is_in(valid_samples) # remove pediatric samples
            ).sink_ipc(f"{self.work_dir}/{name}.feather")

            # export meta data as feather files in self.work_dir
            corresponding_meta.sink_ipc(
                f"{self.work_dir}/{name}_meta.feather"
            )
        return None


    def to_h5ad(self) -> None:
        for name in tqdm(["bi-10x", "bi-ss2"], desc="Generating .h5ad files"):
            # generate AnnData and export as .h5ad files in self.work_dir
            ad.AnnData(
                pl.read_ipc(
                    f"{self.work_dir}/{name}.feather"
                ).to_pandas().set_index("index"),
                obsm=epl.meta2obsm(
                    pl.read_ipc(
                        f"{self.work_dir}/{name}_meta.feather"
                    )
                ),
                uns={
                    "unit": "$\log_2(TPM+1)$",
                    "name": "bi-10x",
                    "alias": "BI-10X"
                }
            ).write(f"{self.work_dir}/{name}.h5ad")
        return None
