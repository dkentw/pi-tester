class VariablesPool(object):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
