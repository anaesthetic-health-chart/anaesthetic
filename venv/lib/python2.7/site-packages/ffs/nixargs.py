"""
ffs.nixargs

Parsing flags into python keyword arguments
"""
def argmap(dikt):
    """
    Decprator that wraps function signatures.

    If we have a nixargs keyword argument, transform the arguments to
    the function.

    DIKT is a dictionary containing tuples of argparse style *args
    mapped to the keyword arg name to map to. We convert the args into
    keyword arguments according to this scheme, maintaining other args.

    If the nixargs string contains a flag that is not in DIKT, a ValueError
    will be raised.

    Arguments:
    - `dikt`: dict

    Return: callabla
    Exceptions: ValueError
    """
    def argparsing(fn):
        "Decorate FN"

        def argpuller(*args,**kwargs):
            "Actually parse the args!"
            if 'nixargs' in kwargs:
                kwargs2 = kwargs.copy()
                flags = kwargs['nixargs'].split()
                del kwargs2['nixargs']
                for flag in flags:
                    if flag in dikt:
                        kwargs2[dikt[flag]] = True
                    else:
                        raise ValueError('{0} not a valid flag'.format(flag))
            else:
                kwargs2 = kwargs
            return fn(*args,**kwargs2)

        return argpuller

    return argparsing
