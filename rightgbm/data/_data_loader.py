from abc import abstractmethod
import os
import subprocess

from rightgbm.dev import typechecker

class DataLoader:
    def __init__(
        self,
        name: str,
        data_path: str,
        meta_path: str,
        work_dir: str = os.path.dirname(__file__)
    ) -> None:
        typechecker(name, str, "name")
        typechecker(data_path, str, "data_path")
        typechecker(meta_path, str, "meta_path")
        typechecker(work_dir, str, "work_dir")
        self.name = name
        self.data_path = data_path
        self.meta_path = meta_path
        self.work_dir = work_dir
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

    @abstractmethod
    def fetch(self) -> None:
        # code to download files from designated source and export them
        pass


    @abstractmethod
    def to_feather(self) -> None:
        # transpose data ma†rices from original data source if needed to optimize data formats
        # for operations in python/julia
        # data are exported as .feather files in liu of .csv
        # those files are intermediate files
        # some files need to be subtracted some data or separated into multiple files
        pass


    @abstractmethod
    def to_h5ad(self) -> None:
        # code to adjust format of data and export them as designated file format
        pass


    @abstractmethod
    def clear_intermediate_files(
        self,
        dirname: str
    ) -> None:
        typechecker(dirname, str, "dirname")
        subprocess.call(f"rm -rf {dirname}".split())
        return None


    @abstractmethod
    def pipeline(
        self,
        basename: str,
        clear: bool = False,
        dirname: str = None
    ) -> None:
        typechecker(basename, str, "basename")
        typechecker(clear, bool, "clear")
        if (
            not os.path.exists(f"{self.work_dir}/{basename}.feather")
        ) or (
            not os.path.exists(f"{self.work_dir}/{basename}_meta.feather")
        ):
            self.fetch()
            self.to_feather()
        if not os.path.exists(f"{self.work_dir}/{basename}.h5ad"):
            self.to_h5ad()
        if clear:
            dirname = self.name if dirname is None else dirname
            typechecker(dirname, str, "dirname")
            self.clear_intermediate_files(dirname=dirname)
