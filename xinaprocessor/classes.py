from typing import Callable, Iterable, Any, NamedTuple


class Operation(NamedTuple):
    apply_fn: Callable[[Any], Any]
    map_fn: Callable[[Any], Any]


class Sequential:
    def __init__(self):
        super().__init__()
        self.operations = []

    def add(self, apply_fn: Callable[[Any], Any], map_fn: Callable[[Any], Any]):
        operation = Operation(apply_fn=apply_fn, map_fn=map_fn)
        self.operations.append(operation)

    def apply(self, map_list: Iterable[str]):
        output = map_list
        for op in self.operations:
            output = list(op.map_fn(op.apply_fn, output))
        return output

    def __len__(self):
        return len(self.operations)

    def __getitem__(self, item):
        assert item > -1 and item < len(self)
        return self.operations[item]
