class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Borders = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False

    def draw(self):
        if self.visited:
            pygame.draw_borders.Rect(screen)
