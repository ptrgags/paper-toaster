class LSystem:
    def __init__(self, rules, axiom):
        self.rules = rules
        self.axiom = axiom
    
    def generate(self):
        production = self.axiom
        while True:
            yield production
            s = ''
            for c in production:
                if c in self.rules:
                    s += self.rules[c]
                else:
                    s += c
            production = s