from sprites import Button

class Shop:
    def __init__(self):
        self.items = {"Sword": 10, "Health Potion": 5}  # Items for sale and their prices

    def buy_item(self, item, inventory):
        if item in self.items:
            inventory.add_item(item)
            return True
        else:
            return False

class ShopButton(Button):
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        super().__init__(x, y, width, height, fg, bg, content, fontsize)

    def is_pressed(self, mouse_pos, mouse_pressed, inventory=None, shop=None):
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                if inventory and shop:
                    return shop.buy_item(self.content, inventory)
                else:
                    return True
        return False