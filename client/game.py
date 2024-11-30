import pygame
from button import Button, TextButton
from board import Board
from top_bar import TopBar
from leader_board import Leaderboard
from player import Player
from bottombar import BottomBar
from chat import Chat
from network import Network



class Game:

    BG = (255, 255, 255)
    COLORS = {
        (255, 255, 255): 0,
        (0, 0, 0): 1,
        (255, 0, 0): 2,
        (0, 255, 0): 3,
        (0, 0, 255): 4,
        (255, 255,0): 5,
        (255,140, 0): 6,
        (165, 42, 42): 7,
        (128, 0, 128):8
    }




    def __init__(self, win, connection=None):
        pygame.font.init()
        self.connection = connection
        self.win = win
        self.leaderboard = Leaderboard(50, 124)
        self.board = Board(304, 124)
        self.top_bar = TopBar(10, 10, 1200, 100)
        self.top_bar.changeround(1)
        self.drawcolor = (0, 0, 0)
        self.player = []
        self.skipbutton = TextButton(87, 830, 124, 59, (255,255, 0), "Skip")
        self.bottombar = BottomBar(304, 880, self)
        self.chat = Chat(1040, 124)
        self.drawcolor = (0, 0, 0)

        

    def add_player(self, player):
        self.players.append(player)
        self.leaderboard.add_player(player)



    def draw(self):
        self.win.fill(self.BG)
        self.leaderboard.draw(self.win)
        self.top_bar.draw(self.win)
        self.board.draw(self.win)
        self.skipbutton.draw(self.win)
        if self.drawing:
            self.bottombar.draw(self.win)
        self.chat.draw(self.win)
        pygame.display.update()




    def check_clicks(self):
        """
        handles clicks on buttons and screen
        :return: None
        """

        mouse = pygame.mouse.get_pos()
        
        # Check click on skip button

        if self.skipbutton.click(*mouse) and not self.drawing:
            print("Clicked skip button")
            skips = self.connection.send({1:[]})


        clickedboard = self.board.click(*mouse)

        if clickedboard:
            self.board.update(*clickedboard, self.drawcolor)
            self.connection.send({8:[*clickedboard, self.COLORS[tuple(self.drawcolor)]]})


    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)


            try:

                # get board
                response = self.connection.send({3:[]})
                if response:
                    self.board.compressed_board = response
                    self.board.translate_board()


                # get time
                response = self.connection.send({9:[]})
                self.top_bar.time = response


                # ge chat
                response = self.connection.send({2:[]})
                self.chat.updatechat(response)


                # get round informatio
                self.top_bar.word = self.connection.send({6:[]})
                self.top_bar.round = self.connection.send({5:[]})
                self.drawing = self.connection.send({11:[]})
                self.top_bar.drawing = self.drawing
                self.top_bar.maxround = len(self.players)


                # get player updates
                '''response = self.connection.send({0:[]})
                self.players = []


                for player in response:
                    p = Player(player)
                    self.add_player(p)'''


            except:
                run = False
                break


            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break


                if pygame.mouse.get_pressed()[0]:

                    self.check_clicks()
                    self.bottombar.buttonevents()



                if event.type == pygame.KEYDOWN:
                    if not self.drawing:
                        if event.key == pygame.K_RETURN:
                            self.connection.send({0:[self.chat.typing]})
                            self.chat.typing = ""

                    else:
                        # gets the key name
                        keyname = pygame.key.name(event.key)


                        # converts to uppercase the key name
                        keyname = keyname.lower()
                        self.chat.type(keyname)


        pygame.quit()


