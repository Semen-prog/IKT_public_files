class User:
    def __init__(self):
        self.name = None
        self.war = None
        self.duration = None
        self.year_start = None
        self.precipitation = None
        self.temp = None
        self.attacker = None
        self.defender = None

    def update(self, changes):
        for [s, typ] in changes:
            if s == '':
                continue
            if typ == 1:
                self.name = s
            elif typ == 2:
                self.war = s
            elif typ == 3:
                self.duration = s
            elif typ == 4:
                self.year_start = s
            elif typ == 5:
                self.precipitation = s
            elif typ == 6:
                self.temp = s
            elif typ == 7:
                self.attacker = s
            else:
                self.defender = s