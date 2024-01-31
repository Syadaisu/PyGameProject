class PlayerStats:
    def __init__(self, health=100, strength=10, defense=10):
        self.health = health
        self.strength = strength
        self.defense = defense

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