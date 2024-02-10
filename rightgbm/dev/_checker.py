from typing import Any, Tuple, Union

def typechecker(
    val: Any, 
    valtype: Union[type, Tuple[type]], 
    argname: str = None
):
    if (argname is not None) & (not isinstance(argname, str)):
        raise TypeError("assign argname as a str")
    if not isinstance(val, valtype):
        msg = f"{'' if argname is None else argname + ' is '}expected to be {valtype}, got {val}{type(val)}"
        raise TypeError(msg)
