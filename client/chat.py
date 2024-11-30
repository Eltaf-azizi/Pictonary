"""
Represents the chat for the game.
"""
import pygame


class Chat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = 224
        self.HEIGHT = 800
        self.BORDERTHICKNESS = 5
        self.content = []
        self.typing = ""
        self.chatfont = pygame.font.SysFont("comicsans", 20)
        self.typefont = pygame.font.SysFont("comicsans", 30)
        self.CHATGAP = 20


    
    def updatechat(self, content):
        self.content = content

    
    def draw(self, win):
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y + self.HEIGHT - 40,self.WIDTH, 40))
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y + self.HEIGHT - 40), (self.x + self.WIDTH, self.y + self.HEIGHT - 40), self.BORDERTHICKNESS)

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT), self.BORDERTHICKNESS)

        while len(self.content) * self.CHATGAP > self.HEIGHT - 60:
             
            self.content = self.content[:-1]


        for i, chat in enumerate(self.content):
                txt = self.chatfont.render(chat, 1, (0, 0, 0))
                win.blit(txt, (self.x + 8, 10 + self.y + i*self.CHATGAP))
        

        typechat = self.typefont.render(self.typing, 1, (0, 0, 0))
        win.blit(typechat, (self.x + 4, self.y + self.HEIGHT - 17 - typechat.get_height()/2))



    def type(self, char):

        if char == "backspace":
             if len(self.typing) > 0:
                  self.typing = self.typing[:-1]
        
        elif char == "space":
             self.typing += " "
            

        elif len(char) == 1:
             self.typing += char



        if len(self.typing) >= 24:
            self.typing = self.typing[:24]



