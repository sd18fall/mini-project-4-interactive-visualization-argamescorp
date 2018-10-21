"""
Menu structure that changes the settings for the game with a controller

@authors: Richard Ballaux, Viktor Deturck, Leon Santen
"""

import pygame
from pygame.locals import *
import time

class PlayboardWindowView():
    """this board includes the outlines, the ball, the paddles and the goals"""
    def __init__(self,model,screen_size, menu):
        self.model=model
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ("Pong-AR-Game")
        self.myfont = pygame.font.SysFont("monospace", 40)
        self.myfontColor = (0,250,0)
        #self.counter = 0
    def _draw_background(self):
        """eventually this needs to be the live feed of the camera"""
        """but for now we just stay with a white background"""
        WHITE = (0,0,0)
        self.screen.fill(WHITE)

    def draw(self):
        """self.counter += 1
        if self.counter >1000:
            menu.state = "game" """

        if menu.state == "menu":
            self._draw_background()
            pygame.draw.rect(self.screen, (250,250,0), pygame.Rect(50, model.height/2-50, 100,100))
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.myfontColor)
            self.screen.blit(menutext, (50,50))
            self.model.cursor.draw(self.screen)
            pygame.display.update()
        if menu.state == "game":
            self._draw_background()
            for component in self.model.components:
                component.draw(self.screen)
            pygame.display.update()

class Menu():
    """State machine that regulates whether or not we see the menu or the game"""
    def __init__(self):
        self.state = "menu" #states are "menu" and "game"



class ArPongModel():
    """encodes a model of the game state"""
    def __init__(self,windowSize,boundryOffset, boundryThickness,ballRadius, ballSpeed):
        self.width = windowSize[0]
        self.height = windowSize[1]
        boundryLength = self.width-2*boundryOffset[0]
        self.upperboundry = Boundry(boundryOffset[0],boundryOffset[1],boundryThickness,boundryLength)
        self.lowerboundry = Boundry(boundryOffset[0],self.height-boundryOffset[1],boundryThickness,boundryLength)
        self.ball = Ball(50,50,ballRadius,ballSpeed)
        paddleWidth = 10
        paddleHeight = 100
        cursorRadius = 20
        self.leftPaddle = Paddle(10,self.height/2,paddleHeight,paddleWidth)
        self.rightPaddle = Paddle(self.width-10-paddleWidth,self.height/2,paddleHeight,paddleWidth)
        self.cursor = Cursor(self.width/2,self.height/2, cursorRadius)
        self.score = Score()
        self.components = (self.upperboundry,self.lowerboundry,self.ball,self.leftPaddle,self.rightPaddle,self.score)
        self.ball.x=100
        self.ball.y=100
        self.triggerarea1 = CursorRecognition(300, [50,self.height/2-50,150,self.height/2+50])

    def update(self):
        """updates all the components the model has when state is "game" to prevent the ball from moving before game settings selected"""


        if menu.state == "menu":
            self.triggerarea1.areaSurveillance(self.cursor, "game")
            #self.cursor.update()
            #!!! When running this update function window closes automatically



        if menu.state == "game":
            self.ball.update()
            #the paddles dont need the update because the handle_event can access the position of the paddles
            #self.leftPaddle.update()
            #self.rightPaddle.update()
            self.score.update()




                # elif event.type is pygame.MOUSEBUTTONDOWN:
                #     if self.add_tile_type == 'lava':
                #         self._add_lava(event.pos)
                #     if self.add_tile_type =='swamp':
                #         self._add_swamp(event.pos)
                # elif event.type is pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         self.paul.run_astar(self.cake.cell_coordinates, self)
                #         self.paul.get_path()
                #     elif event.key == pygame.K_l:
                #         self.add_tile_type = 'lava'
                #     elif event.key==pygame.K_s:
                #         self.add_tile_type = 'swamp'

class ArPongMouseController():
    """handles input first from the mouse and later on from the camera"""
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEMOTION:

            if menu.state == "menu":
                self.model.cursor.update(event.pos[0], event.pos[1])

            if menu.state == "game":
                self.model.rightPaddle.update(event.pos[1]-self.model.rightPaddle.height/2.0)
                self.model.leftPaddle.update(event.pos[0]-self.model.leftPaddle.height/2.0)

class Ball():
    """this is the ball that bounces on the walls, the paddles and that you try to get in the goal of the other player"""
    def __init__(self,x,y,radius,speed):
        self.x=x
        self.y=y
        self.radius=radius
        self.speed=speed
        #the direction needs to be between 0-1
        self.direction = (1,1)

    def update(self):
        """after one loop has gone by, move the ball in the direction of the movement"""
        self.x=self.x + self.direction[0]*self.speed
        self.y = self.y + self.direction[1]*self.speed


    def draw(self,screen):
        """draw the ball on its new position"""
        pygame.draw.circle(screen, (66, 134, 244), (self.x,self.y), self.radius)

class Boundry():
    """This is a class for the boundry lines"""
    def __init__(self,x,y,height,width):
        self.x=x
        self.y=y
        self.height=height
        self.width = width

    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color(69, 244, 66),pygame.Rect(self.x,self.y,self.width,self.height))

class Cursor():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 20, 147), (self.x,self.y), self.radius)


    def update(self, x, y):
        self.x = x
        self.y = y

class CursorRecognition():
    """Takes an
    counter_limit: int, the limit for when "something" should be triggered
    triggerArea: list of form: [x1,y1,x2,y2] - 1 referring to lower left corner of rectangle, 2 referring to upper right corner of rectangle

    counts up every loop the XY object is still in the same area

    >>>
    """
    def __init__(self, counter_limit, area):
        self.counter = 0 #Counter for area
        self.limit = counter_limit
        self.triggerArea = area

    def areaSurveillance(self, cursor, new_state, new_ball_speed = 1):
        if int(cursor.x) in range(int(self.triggerArea[0]), int(self.triggerArea[2]+1)):
            if int(cursor.y) in range(int(self.triggerArea[1]), int(self.triggerArea[3]+1)):
                self.counter += 1
            else:
                self.counter = 0
        else:
            self.counter = 0

        if self.counter == self.limit:
            menu.state = new_state
            model.ball.speed = new_ball_speed



class Paddle(Boundry):
    """This is the movable paddle"""
    def __init__(self, x, y,height, width):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        super(Paddle,self).__init__(x,y,height,width)


    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color(244, 65, 65),pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self,y):
         """maybe used to change position although the position is accessed by the handle_event"""
         self.y=y

class Score():
    """this is the score"""
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.position = (0.0)

    def draw(self,screen):
        """print score for now, needs to print the score on the screen"""
        print("Player 1: ", self.player1)
        print("Player 2: ", self.player2)

    def update(self):
        """needs to count the score"""
        pass

def Main(model,view,controller):
    """Update graphics and check for pygame events."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(0.001)


if __name__ == '__main__':
    pygame.init()
    screenSize = (1500,1000)
    menu = Menu()
    menu.state = "menu"
    #arguments are screenSize, the boundryOffset, boundryThickness, ballRadius, ballSpeed
    model = ArPongModel(screenSize,(50,50),10,20,1)
    view = PlayboardWindowView(model,screenSize, menu)
    view._draw_background()
    controller = ArPongMouseController(model)
    Main(model,view,controller)
