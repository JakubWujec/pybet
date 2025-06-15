from typing import List, TypeVar, Callable, Dict

T = TypeVar("T")
K = TypeVar("K")


def list_to_dict(_list: List[T], key_func: Callable[[T], K]) -> Dict[K, T]:
    return {key_func(item): item for item in _list}
