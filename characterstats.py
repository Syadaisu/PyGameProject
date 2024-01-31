class CharacterStats:
    def __init__(self, health, strength, level):
        self.health = health
        self.strength = strength
        self.level = level
        self.max_health = health

    def increase_stat(self, stat, amount):
        if hasattr(self, stat):
            setattr(self, stat, getattr(self, stat) + amount)

    def decrease_stat(self, stat, amount):
        if hasattr(self, stat):
            setattr(self, stat, getattr(self, stat) - amount)

    def get_stat(self, stat):
        if hasattr(self, stat):
            return getattr(self, stat)
        else:
            return None