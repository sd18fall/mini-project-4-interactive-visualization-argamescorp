"""AR Game file

how do we do the collision detection
@authors: Richard Ballaux, Viktor Deturck, Leon Santen"""
import pygame
from pygame.locals import *
import time

class PlayboardWindowView():
    """this board includes the outlines, the ball, the paddles and the goals"""
    def __init__(self,model,screen_size):
        self.model=model
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ("Pong-AR-Game")
    def _draw_background(self):
        """eventually this needs to be the live feed of the camera"""
        """but for now we just stay with a white background"""
        WHITE = (255,255,255)
        self.screen.fill(WHITE)

    def draw(self):
        self._draw_background()
        for component in self.model.components:
            component.draw(self.screen)
        pygame.display.update()

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
        self.leftPaddle = Paddle(10,self.height/2,paddleHeight,paddleWidth)
        self.rightPaddle = Paddle(self.width-10-paddleWidth,self.height/2,paddleHeight,paddleWidth)
        self.score = Score()
        self.components = (self.upperboundry,self.lowerboundry,self.ball,self.leftPaddle,self.rightPaddle,self.score)
        self.ball.x=100
        self.ball.y=100

    def update(self):
        """updates all the components the model has"""
        self.ball.update()
        self.leftPaddle.update()
        self.rightPaddle.update()
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
            self.model.rightPaddle.y=event.pos[1]-self.model.rightPaddle.height/2.0
            self.model.leftPaddle.y=event.pos[0]-self.model.leftPaddle.height/2.0




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


class Paddle():
    """This is the movable paddle"""
    def __init__(self, x, y,height, width):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color(244, 65, 65),pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self):
        """maybe used to change position although the position is accessed by the handle_event"""
        pass

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
        time.sleep(0.01)


if __name__ == '__main__':
    pygame.init()
    size = (1000,1000)
    model = ArPongModel(size,(50,50),10,30,1)
    view = PlayboardWindowView(model,size)
    view._draw_background()
    controller = ArPongMouseController(model)
    Main(model,view,controller)
