from utils import Enemy

class Boar(Enemy):
    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.hp = 100 + difficulty * 5
        self.damage = 8 + difficulty
        self.actions = [self.attack, ]

    def attack(self, target):
        target.hp -= self.damage

class Defias(Enemy):
    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.hp = 120 + difficulty * 6
        self.normal_damage = 10 + difficulty * 2
        self.dagger_damage = 6 + difficulty
        self.actions = [self.attack, self.swap_daggers, ]
    
    def attack(self, target):
        target.hp -= self.normal_damage
    
    def swap_daggers(self, target):
        self.actions.pop(self.actions.index(self.attack))
        self.actions.pop(self.actions.index(self.swap_daggers))
        self.actions.append(self.dagger_attack)
    
    def dagger_attack(self, target):
        target.hp -= self.dagger_damage
        target.hp -= self.dagger_damage

class Worgen(Enemy):
    def __init__(self, difficulty=0):
        self.difficulty = difficulty
        self.hp = 150 + difficulty * 7
        self.max_hp = self.hp
        self.damage = 12 + difficulty * 2
        self.actions = [self.attack, ]

    def attack(self, target):
        target.hp -= self.damage
        if self.hp < self.max_hp/2:
            self.actions = [self.enrage, ]
    
    def enrage(self, target):
        target.hp -= self.damage*2