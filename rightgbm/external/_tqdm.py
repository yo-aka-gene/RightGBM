"""
Wrapper func for tqdm
"""
def in_ipython():
    try:
        get_ipython()
        return True
    except NameError:
        return False


if in_ipython():
    from tqdm.notebook import tqdm
else:
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
