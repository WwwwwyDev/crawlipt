from inspect import signature
from functools import wraps
from crawlipt.error import ParamTypeError


def check(exclude: list | str):
    """
    Turn the function into a strongly typed function, check if the parameter type is legal, and if not, directly assert.
    \n You could use @check to Turn the function into a strongly typed function.
    :param exclude: Sort the parameters that need to be checked
    :return: Decorator
    """
    if not callable(exclude):
        if exclude is None:
            exclude = []
        assert isinstance(exclude, list) or isinstance(exclude, str)
        if isinstance(exclude, str):
            exclude = [exclude]
        exclude = set(exclude)

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            args_dict = {}
            index = 0
            for name, type_ in signature(func).parameters.items():
                if name in kwargs:
                    break
                if index >= len(args):
                    break
                args_dict[name] = args[index]
                index += 1
            for name, type_ in signature(func).parameters.items():
                if type_.default != type_.empty and name not in kwargs:
                    args_dict[name] = type_.default
            all_kwargs = {**args_dict, **kwargs}
            for name, type_ in signature(func).parameters.items():
                if not callable(exclude) and name in exclude:
                    continue
                if name == "self":
                    continue
                if type_.annotation == type_.empty:
                    raise ParamTypeError(f"Parameter {name} must be indicated the type.")
                if name not in all_kwargs:
                    raise ParamTypeError(f"Parameter {name} is not in the defined parameter list.")
                if all_kwargs[name] is None and type_.default is not type_.empty:
                    continue
                if all_kwargs[name] == "__PRE_RETURN__":
                    continue
                if isinstance(all_kwargs[name], str) and all_kwargs[name].startswith("__v-") and all_kwargs[
                    name].endswith("__"):
                    continue
                if isinstance(all_kwargs[name], int) and type_.annotation is float:
                    all_kwargs[name] = float(all_kwargs.get(name))
                if not isinstance(all_kwargs[name], type_.annotation):
                    raise ParamTypeError(f"Parameter {name} must be {type_.annotation}.")
            return func(*args, **kwargs)

        return inner_wrapper

    if callable(exclude):
        return wrapper(exclude)
    return wrapper


def alias(name: str = ""):
    """
    Add an alias to your newly added action or condition so that the script can resolve to this function through the alias
    :param name: The name of func
    :return: Decorator
    """
    if not callable(name):
        assert isinstance(name, str)

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            if callable(name) or not name:
                return func(*args, **kwargs)
            func.__crawlipt_func_name__ = name
            return func(*args, **kwargs)

        inner_wrapper.__crawlipt_func_name__ = name
        return inner_wrapper

    if callable(name):
        return wrapper(name)
    return wrapper
