from abc import abstractmethod
import os

from rightgbm.dev import typechecker

class DataLoader:
    def __init__(
        self,
        name: str,
        data_path: str,
        meta_path: str,
        save_dir: str = os.path.dirname(__file__)
    ) -> None:
        typechecker(name, str, "name")
        typechecker(data_path, str, "data_path")
        typechecker(meta_path, str, "meta_path")
        typechecker(save_dir, str, "save_dir")
        self.name = name
        self.data_path = data_path
        self.meta_path = meta_path
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    @abstractmethod
    def fetch(self) -> None:
        # code to download files from designated source and export them
        pass


    @abstractmethod
    def adjust_format(self) -> None:
        # code to adjust format of data and export them as designated file format
        pass
