import warnings
AVOID = [
        "clear_text",
        "clear_sequential",
        
        ]

def empty_warning(func):
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if func.__name__ in AVOID:
            return result
        if len(''.join(result)) == 0:
            warnings.warn(f'The results out of {func.__name__} function are empty!')
        return result
    return wrapped

def show_empty_warning(cls):
    class Wrapper:
        def __init__(self, *args, **kwargs):
            self.decorated_obj = cls(*args, **kwargs)

        def __getattribute__(self, attribute):
            try:
                item = super().__getattribute__(attribute)
                return item
            except AttributeError:
                pass
            item = self.decorated_obj.__getattribute__(attribute)
            if type(item) == type(self.__init__):  
                return empty_warning(item)  
            else:
                return item

    return Wrapper
