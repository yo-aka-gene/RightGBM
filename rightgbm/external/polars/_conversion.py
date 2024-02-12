"""
Utility functions for polars data conversion
"""
from typing import Dict, Union
import numpy as np
import polars as pl


from rightgbm.dev import typechecker

def meta2obsm(
    meta: Union[pl.LazyFrame, pl.DataFrame]
) -> Dict[str, np.ndarray]:
    typechecker(meta, (pl.DataFrame, pl.LazyFrame), "meta")
    meta = meta.collect(
        streaming=True
    )if isinstance(meta, pl.LazyFrame) else meta
    dictionary = meta.to_dict(as_series=False)
    return {k: np.array(v) for k, v in dictionary.items()}

