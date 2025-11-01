class Color:
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def __str__(self) -> str:
        return "(%s, %s, %s)" % (self.r, self.g, self.b)