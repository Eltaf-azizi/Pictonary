import pygame


class Button:

    def __init__(self, x, y, width, height, color, bordercolor=(0, 0, 0)):
        self.x = x
        self.x = y
        self.WIDTH = width
        self.HEIGHT = height
        self.color = color
        self.bordercolor = bordercolor
        self.BORDERWIDTH = 2


    def draw(self, win):
        pygame.draw.rect(win, self.bordercolor, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(win, self.color, (self.x + self.BORDERWIDTH, self.y + self.BORDERWIDTH,self.width - self.BORDERWIDTH*2, self.height - self.BORDERWIDTH* 2), 0)
        


    def click(self, x, y):
        """
        if user clicked on button
        :param x: float
        :param y: float
        :return: bool
        """

        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True # user clicked button

        return False
    

class TextButton():
    def __init__(self, x, y, width, height, color, text, bordercolor=(0, 0, 0)):
        super().__init__(x, y, width, height, color, bordercolor)
        self.text = text
        self.textfont = pygame.font.SysFont("comicsans", 30)


    def changefontsize(self, size):
        self.textfont = pygame.font.SysFont("comicsans", size)


    def draw(self, win):
        super().draw(win)
        txt = self.textfont.render(self.text, 1, (0, 0, 0))
        win.blit(txt, (self.x + self.width/2 - txt.get_width()/2, self.y + self.height/2 - txt.get_height()/2))


