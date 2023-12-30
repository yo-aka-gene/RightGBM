"""
Wrapper for rpy2
"""
import rpy2.robjects as ro


class R:
    def __init__(self) -> None:
        self.renv = ro.packages.importr("renv")


    def library(
        self, 
        pkg: str
    ) -> ro.packages.InstalledSTPackage:
        return ro.packages.importr(pkg)


    def install_packages(
        self, 
        pkg: str,
        auto_snapshot: bool = True
    ) -> ro.packages.InstalledSTPackage:
        self.renv.install(pkg)
        if auto_snapshot:
            self.renv.snapshot()
        return self.library(pkg)


    def __call__(self, rscript: str):
        return ro.r(rscript)


    def assign(self, varname: str, var) -> None:
        ro.r.assign(varname, var)


    def __getitem__(self, item):
        return ro.r[item]
