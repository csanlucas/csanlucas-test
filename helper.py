from collections import Iterable

def reduce_nested_list(nested_list = []):
    for item in nested_list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in reduce_nested_list(item):
                yield x
        else:        
            yield item
