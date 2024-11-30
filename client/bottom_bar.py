import pygame

from button import Button, TextButton

class BottomBar:


    COLORS = {
        0: (255, 255, 255),
        1: (0, 0, 0),
        2: (255, 0, 0),
        3: (0, 255, 0),
        4: (0, 0, 255),
        5: (255, 255,0),
        6: (255,140, 0),
        7: (165, 42, 42),
        8: (128, 0, 128)
    }
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.WIDTH = 720
        self.HEIGHT = 100
        self.BORDERTHICKNESS = 5
        self.game = game
        self.clearbutton = TextButton(self.x + self.WIDTH - 149, self.y + 24, 100, 49, (128, 128, 128), "Clear")
        self.eraserbutton = TextButton(self.x + self.WIDTH - 300, self.y + 24, 100, 49, (128, 128, 128), "Eraser")
        self.colorbuttons = [Button(self.x + 20, self.y + 5, 30, 30, self.COLORS[0]),
                            Button(self.x + 50, self.y + 5, 30, 30, self.COLORS[1]),
                            Button(self.x + 80, self.y + 5, 30, 30, self.COLORS[2]),
                            Button(self.x + 20, self.y + 35, 30, 30, self.COLORS[3]),
                            Button(self.x + 40, self.y + 35, 30, 30, self.COLORS[4]),
                            Button(self.x + 80, self.y + 35, 30, 30, self.COLORS[5]),
                            Button(self.x + 20, self.y + 5, 30, 30, self.COLORS[6]),
                            Button(self.x + 50, self.y + 5, 30, 30, self.COLORS[7]),
                            Button(self.x + 80, self.y + 5, 30, 30, self.COLORS[8])]



    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), self.BORDERTHICKNESS)
        self.clearbutton.draw(win)
        self.eraserbutton.draw(win)

        for btn in self.colorbuttons:
            btn.draw(win)



    def buttonevents(self):
        """
        handle all button press events here
        :return: None
        """

        mouse = pygame.mouse.get_pos()

        if self.clearbutton.click(*mouse):
            self.game.board.clear()
            self.connection.send({1:[]})

        
        if self.eraserbutton.click(*mouse):
            self.game.drawcolor = (249, 249, 249)


        
        for btn in self.colorbuttons:
            if btn.click(*mouse):
                self.game.drawcolor = btn.color
