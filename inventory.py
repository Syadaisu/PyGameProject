class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity=1):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity=1):
        if item in self.items:
            self.items[item] -= quantity
            if self.items[item] <= 0:
                self.items[item] = 0
        else:
            print("Item not in inventory")
    def get_item(self, item):
        if item in self.items:
            return self.items[item]
        else:
            return 0
    def get_inventory(self):
        return self.items