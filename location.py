class Location:
    def __init__(self, icon, bg, w, h, x, y):
        self.icon = icon
        self.bg = bg
        self.w, self.h = w, h
        self.x, self.y = x, y  # координаты верхнего левого угла

        self.start_coords = x + 100, y + 100

        self.chars = []

    def render(self, screen):
        screen.blit(self.bg, (0, 0))

    def set_char(self, char_list):
        self.chars = char_list

    def add_char(self, char):
        char.loc = self
        self.chars.append(char)

    def remove_char(self, char):
        for i in range(len(self.chars)):
            if self.chars[i] == char:
                ind = i
                break
        self.chars.pop(ind)
