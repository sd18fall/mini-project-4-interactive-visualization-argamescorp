"""AR Game file

how do we do the collision detection
@authors: Richard Ballaux, Viktor Deturck, Leon Santen"""
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
    def _draw_background(self):
        """eventually this needs to be the live feed of the camera"""
        """but for now we just stay with a white background"""
        WHITE = (0,0,0)
        self.screen.fill(WHITE)

    def draw(self):

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
            #self.model.boundaryGroup.draw(self.screen)
            pygame.display.update()

class Menu():
    """State machine that regulates whether or not we see the menu or the game"""
    def __init__(self):
        self.state = "menu" #states are "menu" and "game"


class ArPongModel():
    """encodes a model of the game state"""
    def __init__(self,windowSize,boundaryOffset, boundaryThickness,ballRadius, ballSpeed):
        self.width = windowSize[0]
        self.height = windowSize[1]
        boundaryLength = self.width-2*boundaryOffset[0]
        self.upperboundary = boundary(boundaryOffset[0],boundaryOffset[1],boundaryThickness,boundaryLength)
        self.lowerboundary = boundary(boundaryOffset[0],self.height-boundaryOffset[1],boundaryThickness,boundaryLength)
        self.ball = Ball(50,50,ballRadius,ballSpeed)
        paddleWidth = 10
        paddleHeight = 100
        cursorRadius = 20
        self.leftPaddle = Paddle(10,self.height/2,paddleHeight,paddleWidth)
        self.rightPaddle = Paddle(self.width-10-paddleWidth,self.height/2,paddleHeight,paddleWidth)
        self.cursor = Cursor(self.width/2,self.height/2, cursorRadius)
        self.score = Score()
        self.components = (self.upperboundary,self.lowerboundary,self.ball,self.leftPaddle,self.rightPaddle,self.score)
        self.ball.x=500
        self.ball.y=500

        self.triggerarea1 = CursorRecognition(300, [50,self.height/2-50,150,self.height/2+50])
        #initialize the sprite groups for collision detection
        self.boundaryGroup = pygame.sprite.Group()
        self.boundaryGroup.add(self.upperboundary)
        self.boundaryGroup.add(self.lowerboundary)

        self.paddleGroup = pygame.sprite.Group()
        self.paddleGroup.add(self.leftPaddle)
        self.paddleGroup.add(self.rightPaddle)

        self.ballGroup = pygame.sprite.Group()
        self.ballGroup.add(self.ball)

        rightGoalGroup = pygame.sprite.Group()
        leftGoalGroup = pygame.sprite.Group()


    def update(self):
        """updates all the components the model has"""

        if menu.state == "menu":
            self.triggerarea1.areaSurveillance(self.cursor, menu, "state", "game")
            #self.cursor.update()
            #!!! When running this update function window closes automatically


        if menu.state == "game":
            self.ball.update()
            #the paddles dont need the update because the handle_event can access the position of the paddles
            #self.leftPaddle.update()
            #self.rightPaddle.update()
            self.score.update()
            boundaryBounce = pygame.sprite.spritecollide(self.ball,self.boundaryGroup,False,False)
            print(boundaryBounce)
            if len(boundaryBounce)>0:
                self.ball.movingDirection[1] = -self.ball.movingDirection[1]

            # paddleBounce = pygame.sprite.spritecollide(self.ball,self.paddleGroup,False)
            # if len(paddleBounce)>0:
            #     self.ball.movingDirection[0] = -self.ball.movingDirection[0]


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





class Ball(pygame.sprite.Sprite):
    """this is the ball that bounces on the walls, the paddles and that you try to get in the goal of the other player"""
    def __init__(self,x,y,radius,speed):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.radius=radius
        self.speed=speed
        #the movingDirection needs to be between 0-1
        self.movingDirection = [1,1]

        self.rect = pygame.Surface([2*self.radius,2*self.radius]).get_rect()
        self.rect.center = [self.x,self.y]


    def update(self):
        """after one loop has gone by, move the ball in the movingDirection of the movement"""
        self.x=self.x + self.movingDirection[0]*self.speed
        self.y = self.y + self.movingDirection[1]*self.speed


    def draw(self,screen):
        """draw the ball on its new position"""
        pygame.draw.circle(screen, (66, 134, 244), (self.x,self.y), self.radius)

class boundary(pygame.sprite.Sprite):
    """This is a class for the boundary lines"""
    def __init__(self,x,y,height,width):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.height=height
        self.width = width

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill([69,244,66])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x+width/2,self.y+height/2]

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
    """Recognizes a cursor that hovers over an area and triggers a change of an attribute of an object_to_change.
    counts up every loop the XY object is still in the same area.

    counter_limit -- int, the limit for when "something" should be triggered
    triggerArea -- list of form: [x1,y1,x2,y2] - 1 referring to lower left corner of rectangle, 2 referring to upper right corner of rectangle
    """
    def __init__(self, counter_limit, area):
        self.counter = 0 #Counter for area
        self.limit = counter_limit
        self.triggerArea = area

    def areaSurveillance(self, cursor, object_to_change, attribute_of_object, change_attribute_to):
        """With a specific cursor as an input, change the attribute of an object to a specific value

        cursor -- cursor.x should be x coordinate, cursor.y should be y coordinate
        object_to_change -- pass in the class object to change
        attribute_of_object -- as a string, pass in the attribute of the corresponding class object to change
        change_attribute_to -- pass in the value object.attribute needs to be changed to when triggered
        """
        if int(cursor.x) in range(int(self.triggerArea[0]), int(self.triggerArea[2]+1)):
            if int(cursor.y) in range(int(self.triggerArea[1]), int(self.triggerArea[3]+1)):
                self.counter += 1
            else:
                self.counter = 0
        else:
            self.counter = 0

        if self.counter == self.limit:
            setattr(object_to_change, attribute_of_object, change_attribute_to)


class Paddle(boundary):
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
        # print("Player 1: ", self.player1)
        # print("Player 2: ", self.player2)

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
    #arguments are screenSize, the boundaryOffset, boundaryThickness, ballRadius, ballSpeed
    model = ArPongModel(screenSize,(50,50),10,20,1)
    view = PlayboardWindowView(model,screenSize, menu)
    view._draw_background()
    controller = ArPongMouseController(model)
    Main(model,view,controller)
