class claw(object):
    
    def __init__(self):
        self.empty = True
        self.holding = '#'

    def pickup(self, block_name):
        self.holding = block_name
        self.empty = False

    def put_down(self, block_name):
        self.holding = '#'
        self.empty = True

    def is_empty(self):
        return self.empty