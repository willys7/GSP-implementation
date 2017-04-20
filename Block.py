
class Block(object):
    def __init__(self, name, prop={}):
        self.name = name
        self.props = prop

    def add_prop(self, name, value=False):
        self.props[name] = value

    def check_prop(self, name):
        if name in self.props:
            return self.props[name]
        else:
            return False

    def set_prop(self, name, value):
        self.props[name] = value