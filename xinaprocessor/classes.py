from typing import Callable, Iterable, Any, NamedTuple


class Operation(NamedTuple):
    fnc: Callable[[Any], Any]


class Sequential:
    def __init__(self):
        super().__init__()
        self.operations = []

    def add(self, fnc: Callable[[Any], Any]):
        operation = Operation(fnc)
        self.operations.append(operation)

    def apply(self, lst: Iterable[str]):
        output = lst
        for op in self.operations:
            output = list(op.fnc(output))
        return output

    def clear(self):
        self.operations = []

    def __len__(self):
        return len(self.operations)

    def __getitem__(self, item):
        if item < 0 or item >= len(self):
            raise IndexError(
                f"Index must be in range [0,{len(self)}]. Your input: f{item}")
        return self.operations[item]
