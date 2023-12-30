"""
Wrapper for juliapkg
"""
import os
import juliapkg as jlp


class Pkg:
    def __init__(
        self,
        target: str = f"{os.path.dirname(__file__)}/juliapkg.json"
    ) -> None:
        self.target = target
        self.status(target=target)


    def status(self, target=None):
        target = self.target if target is None else target
        jlp.status(target=target)


    def require_julia(self, compat, target=None):
        target = self.target if target is None else target
        jlp.require_julia(compat, target=target)


    def add(self, pkg, *args, target=None, **kwargs):
        target = self.target if target is None else target
        jlp.add(pkg, *args, target=target, **kwargs)


    def rm(self, pkg, target=None):
        target = self.target if target is None else target
        jlp.rm(pkg, target=target)


    def resolve(self, force=False, dry_run=False):
        jlp.resolve(force=force, dry_run=dry_run)


    def executable(self):
        jlp.executable()


    def project(self):
        jlp.project()
