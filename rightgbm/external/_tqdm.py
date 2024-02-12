"""
Wrapper func for tqdm
"""
try:
    from tqdm.notebook import tqdm
except ImportError:
    from tqdm import tqdm


def generic_tqdm(
    iterable=None,
    desc=None,
    total=None,
    *args,
    **kwargs
) -> tqdm:
    return tqdm(
        iterable=iterable,
        desc=desc,
        total=total,
        *args,
        **kwargs
    )
