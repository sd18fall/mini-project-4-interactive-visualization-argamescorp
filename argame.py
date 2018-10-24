"""
AR Game file

@authors: Richard Ballaux, Viktor Deturck, Leon Santen"""
import pygame
from pygame.locals import *
import time
import ObjectRecogImplementation as OR
from PIL import Image
import numpy as np



class PlayboardWindowView():
    """this board includes the outlines, the ball, the paddles and the goals"""
    def __init__(self,model,screen_size, menu):
        self.model=model
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ("Pong-AR-Game")
        self.myfont = pygame.font.SysFont("monospace", 42)
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True)
        self.ColorGreen = (0,250,0)
        self.ColorBlack = (0,0,0)

    def _draw_background(self, color = (0,0,0)):
        """draw background with plain Color
        color -- RGB format (R,G,B), values from 0 to 255, default color is black"""
        self.screen.fill(color)

        # newSurface = pygame.surfarray.make_surface(self.model.cameraImage)
        # self.screen.blit(newSurface,(0,0))
        #pygame.display.update()

    def draw(self):
        """draws corresponding to the state of menu.state the different menu settings or game"""

        if menu.state == "menu":
            self._draw_background()
            pygame.draw.rect(self.screen, (250,250,0), pygame.Rect(50, model.height/2-50, 100,100))
            menutext = self.myfont.render("Keep your cursor in the square to start the game", 1, self.ColorGreen)
            self.screen.blit(menutext, (50,50))
            self.model.cursor.draw(self.screen)
            pygame.display.update()

        if menu.state == "select_speed":
            self._draw_background((255, 224, 254))
            menutext = self.myfont.render("Select a speed by hovering over the desired speed", 1, self.ColorBlack)
            self.screen.blit(menutext, (50,50))
            #Square 1
            pygame.draw.rect(self.screen, (0,150,0), pygame.Rect(int((model.width/6)*1)-50, int(model.height/2)-150, 150,150))
            number = self.numberfont.render("1", 1, self.ColorBlack)
            self.screen.blit(number, (int((model.width/6)*1),model.height/2-115))
            #Square 2
            pygame.draw.rect(self.screen, (0,150,0), pygame.Rect(int((model.width/6)*2)-50, int(model.height/2)+150, 150,150))
            number = self.numberfont.render("2", 1, self.ColorBlack)
            self.screen.blit(number, (int((model.width/6)*2),model.height/2+185))
            #Square 3
            pygame.draw.rect(self.screen, (0,150,0), pygame.Rect(int((model.width/6)*3)-50, int(model.height/2)-150, 150,150))
            number = self.numberfont.render("3", 1, self.ColorBlack)
            self.screen.blit(number, (int((model.width/6)*3),model.height/2-115))
            #Square 4
            pygame.draw.rect(self.screen, (0,150,0), pygame.Rect(int((model.width/6)*4)-50, int(model.height/2)+150, 150,150))
            number = self.numberfont.render("4", 1, self.ColorBlack)
            self.screen.blit(number, (int((model.width/6)*4),model.height/2+185))
            #Square 5
            pygame.draw.rect(self.screen, (0,150,0), pygame.Rect(int((model.width/6)*5)-50, int(model.height/2)-150, 150,150))
            number = self.numberfont.render("5", 1, self.ColorBlack)
            self.screen.blit(number, (int((model.width/6)*5),model.height/2-115))

            self.model.cursor.draw(self.screen)
            pygame.display.update()


        if menu.state == "game":
            self._draw_background()
            for component in self.model.components:
                 component.draw(self.screen)
            #self.model.boundaryGroup.draw(self.screen)
            #self.model.ballGroup.draw(self.screen)
            #self.model.cursor.draw(self.screen)
            pygame.display.update()

class Menu():
    """State machine that regulates whether or not we see the menu or the game
    The different states are:
    - "menu"
    - "select_speed"
    - "game"

    Instruction for adding a state:
    - You don't need to add a state in the Menu() class. Just update the docstring to keep the documentation updated
    - Add an if-statement with the state name to the draw() function in the class PlayboardWindowView()
    - Add an if-statement with the state name t0 the handle_event() function in the class ArPongMouseController()
    """
    def __init__(self):
        self.state = "menu"
        self.settings_ballSpeed = 5
        self.settings_cursorColor = (255, 20, 147)

class ArPongModel():
    """encodes a model of the game state"""
    def __init__(self,windowSize,boundaryOffset, boundaryThickness,camera):
        self.width = windowSize[0]
        self.height = windowSize[1]
        boundaryLength = self.width-2*boundaryOffset[0]
        self.upperboundary = Boundary(boundaryOffset[0],boundaryOffset[1],boundaryThickness,boundaryLength)
        self.lowerboundary = Boundary(boundaryOffset[0],self.height-boundaryOffset[1],boundaryThickness,boundaryLength)
        self.newGame()
        paddleWidth = 10
        paddleHeight = 100
        cursorRadius = 20
        self.leftPaddle = Paddle(10,self.height/2,paddleHeight,paddleWidth)
        self.rightPaddle = Paddle(self.width-10-paddleWidth,self.height/2,paddleHeight,paddleWidth)
        self.score = Score()
        self.components = (self.upperboundary,self.lowerboundary,self.ball,self.leftPaddle,self.rightPaddle,self.score)

        self.cursor = Cursor(int(self.width/2),int(self.height/2), cursorRadius)
        #Trigger areas
        self.triggerarea1 = CursorRecognition(50, [50, self.height/2-50, 100,100])
        self.triggerNumber1 = CursorRecognition(50, [int((self.width/6)*1)-50, int(self.height/2)-150, 150,150])
        self.triggerNumber2 = CursorRecognition(50, [int((self.width/6)*2)-50, int(self.height/2)+150, 150,150])
        self.triggerNumber3 = CursorRecognition(50, [int((self.width/6)*3)-50, int(self.height/2)-150, 150,150])
        self.triggerNumber4 = CursorRecognition(50, [int((self.width/6)*4)-50, int(self.height/2)+150, 150,150])
        self.triggerNumber5 = CursorRecognition(50, [int((self.width/6)*5)-50, int(self.height/2)-150, 150,150])

        self.camera = camera
        self.objectCoordinates, self.cameraImage = OR.getCoords(self.camera)

        #initialize the sprite groups for collision detection
        self.boundaryGroup = pygame.sprite.Group()
        self.boundaryGroup.add(self.upperboundary)
        self.boundaryGroup.add(self.lowerboundary)

        self.paddleGroup = pygame.sprite.Group()
        self.paddleGroup.add(self.leftPaddle)
        self.paddleGroup.add(self.rightPaddle)

    def newGame(self):
        self.ball = Ball(int(self.width/5),int(self.height/5),20)


    def update(self):
        """updates all the components the model has dependent on what state menu.state is in"""
        #self.objectCoordinates, self.cameraImage = OR.getCoords(self.camera)

        if menu.state == "menu":
            self.triggerarea1.areaSurveillance(self.cursor, "select_speed", menu, "state", "select_speed")

        if menu.state == "select_speed":
            self.triggerNumber1.areaSurveillance(self.cursor, "game", menu, "settings_ballSpeed", 5)
            self.triggerNumber2.areaSurveillance(self.cursor, "game", menu, "settings_ballSpeed", 10)
            self.triggerNumber3.areaSurveillance(self.cursor, "game", menu, "settings_ballSpeed", 15)
            self.triggerNumber4.areaSurveillance(self.cursor, "game", menu, "settings_ballSpeed", 22)
            self.triggerNumber5.areaSurveillance(self.cursor, "game", menu, "settings_ballSpeed", 28)



        if menu.state == "game":
            self.ball.update()
            #the paddles dont need the update because the handle_event can access the position of the paddles
            #self.leftPaddle.update()
            #self.rightPaddle.update()

            boundaryBounce = pygame.sprite.spritecollide(self.ball,self.boundaryGroup,False)
            if len(boundaryBounce)>0:
                self.ball.movingDirection[1] = -self.ball.movingDirection[1]

            paddleBounce = pygame.sprite.spritecollide(self.ball,self.paddleGroup,False)
            if len(paddleBounce)>0:
                self.ball.movingDirection[0] = -self.ball.movingDirection[0]
            #give the players
            if self.ball.x < 5:
                self.score.update(0)
                del self.ball
                self.newGame()
            if self.ball.x > self.width-5:
                self.score.update(1)
                del self.ball
                self.newGame()



class ArPongMouseController():
    """handles input from the mouse"""
    def __init__(self,model):
        self.model = model

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            if menu.state == "menu" or "select_speed":
                self.model.cursor.update(event.pos[0], event.pos[1])

            if menu.state == "game":
                self.model.rightPaddle.update(event.pos[1]-self.model.rightPaddle.height/2.0)
                self.model.leftPaddle.update(event.pos[0]-self.model.leftPaddle.height/2.0)

class ArPongObjectRecogController():
    """handles the input from the camera"""
    def __init__(self,model):
        self.model = model

    def update(self):
        self.model.objectCoordinates, self.model.cameraImage = OR.getCoords(self.model.camera)
        #print(self.model.objectCoordinates)
        self.model.cursor.update(self.model.objectCoordinates[0][0],self.model.objectCoordinates[0][1])
        if self.model.objectCoordinates[0][0] != -1:
            self.model.leftPaddle.update(self.model.objectCoordinates[0][1]-self.model.leftPaddle.height/2.0)
        if self.model.objectCoordinates[0][0] != -1:
            self.model.rightPaddle.update(self.model.objectCoordinates[1][1]-self.model.rightPaddle.height/2.0)


class Ball(pygame.sprite.Sprite):
    """this is the ball that bounces on the walls, the paddles and that you try to get in the goal of the other player
    x -- initial x coordinate of the ball
    y -- initial y coordinate of the ball
    radius -- radius of the ball
    """
    def __init__(self,x,y,radius):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.radius=radius
        #the movingDirection needs to be between 0-1
        self.movingDirection = [1,-1]

        self.image = pygame.Surface([2*self.radius,2*self.radius])
        self.image.fill([69,0,66])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]


    def update(self):
        """after one loop has gone by, move the ball in the movingDirection of the movement
        This function uses menu.settings_ballSpeed to as the speed parameter. This ensures that it can be changed by the areaSurveillance method"""
        self.x=self.x + self.movingDirection[0]*menu.settings_ballSpeed
        self.rect.x = self.rect.x + self.movingDirection[0]*menu.settings_ballSpeed
        self.y = self.y + self.movingDirection[1]*menu.settings_ballSpeed
        self.rect.y = self.rect.y + self.movingDirection[1]*menu.settings_ballSpeed

    def draw(self,screen):
        """draw the ball on its new position"""
        pygame.draw.circle(screen, (66, 134, 244), (self.x,self.y), self.radius)

class Boundary(pygame.sprite.Sprite):
    """This is a class for the Boundary lines"""
    def __init__(self,x,y,height,width):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.height=height
        self.width = width

        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x+width/2,self.y+height/2]

    def draw(self,screen):
        """draws the boundaries of the game"""
        pygame.draw.rect(screen,pygame.Color(69, 244, 66),pygame.Rect(self.x,self.y,self.width,self.height))

class Paddle(Boundary):
    """This is the movable paddle
    x -- x coordinate of upper left corner
    y -- y coordinate of upper left corner
    height -- y lenght of rectangle
    width -- x lenght of rectangle
    """
    def __init__(self, x, y,height, width):
        """ Initialize a paddle with the specified height, width,
            and position (x,y) """
        super(Paddle,self).__init__(x,y,height,width)


    def draw(self,screen):
        pygame.draw.rect(screen,pygame.Color(244, 65, 65),pygame.Rect(self.x,self.y,self.width,self.height))

    def update(self,y):
         """maybe used to change position although the position is accessed by the handle_event"""
         self.y=y
         self.rect.y=y

class Score():
    """this is the score"""
    def __init__(self):
        self.player1 = 0
        self.player2 = 0
        self.numberfont = pygame.font.SysFont("monospace", 85, bold=True)

    def draw(self,screen):
        """print score for now, needs to print the score on the screen"""
        # print("Player 1: ", self.player1)
        # print("Player 2: ", self.player2)

        score1 = self.numberfont.render(str(self.player1), 1, (255,255,255))
        screen.blit(score1, (100,100))
        score2 = self.numberfont.render(str(self.player2), 1, (255,255,255))
        screen.blit(score2, (model.width-100,100))

    def update(self,player):
        """needs to count the score"""
        if player == 0:
            self.player1 +=1
        if player == 1:
            self.player2 +=1


class Cursor():
    """Cursor representation for navigating through the settings
    x -- initial x coordinate of the cursor
    y -- initial y coordinate of the cursor
    radius -- radius of the cursor
    """
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        #print(self.x, self.y)
        pygame.draw.circle(screen, menu.settings_cursorColor, (self.x,self.y), self.radius)

    def update(self, x, y):
        self.x = x
        self.y = y

class CursorRecognition():
    """Recognizes a cursor that hovers over an area and triggers a change of an attribute of an object_to_change.
    counts up every loop the XY object is still in the same area.

    counter_limit -- int, the limit for when "something" should be triggered
    area -- list of form: same as pygame draw rectangle - [upper left corner x, upper left corner y, length in x direction, length in y direction]
    """
    def __init__(self, counter_limit, area):
        self.counter = 0 #Counter for area
        self.limit = counter_limit
        self.input = area
        self.triggerArea = [self.input[0], self.input[1]+self.input[3], self.input[0]+self.input[2], self.input[1]]

    def areaSurveillance(self, cursor, change_state_to, object_to_change, attribute_of_object, change_attribute_to):
        """With a specific cursor as an input, change the attribute of an object to a specific value

        cursor -- cursor.x should be x coordinate, cursor.y should be y coordinate
        change_state_to -- changes state of game. To stay in same state just input the same state here
        object_to_change -- pass in the class object to change
        attribute_of_object -- as a string, pass in the attribute of the corresponding class object to change
        change_attribute_to -- pass in the value object.attribute needs to be changed to when triggered
        """
        if int(cursor.x) in range(int(self.triggerArea[0]), int(self.triggerArea[2]+1)):
            if int(cursor.y) in range(int(self.triggerArea[3]+1), int(self.triggerArea[1])):  # y-coordinates flipped since y coordinates are upside down
                self.counter += 1
            else:
                self.counter = 0
        else:
            self.counter = 0

        if self.counter == self.limit:
            menu.state = change_state_to
            setattr(object_to_change, attribute_of_object, change_attribute_to)

def Main(model,view,controller):
    """Update graphics and check for pygame events.
    model -- an object of the type ArPongModel()
    view -- an object of the type PlayboardWindowView()
    controller -- an object ArPongMouseController()
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            #controller.handle_event(event)
        controller.update()
        model.update()
        view.draw()
        clock.tick(fps)

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    screenSize = [1500,1000]
    camera = OR.setup(screenSize)
    menu = Menu()
    menu.state = "menu"
    #arguments are screenSize, the BoundaryOffset, BoundaryThickness, ballRadius, ballSpeed
    model = ArPongModel(screenSize,(50,50),10,camera)
    view = PlayboardWindowView(model,screenSize, menu)
    view._draw_background()
    #controller = ArPongMouseController(model)
    controller = ArPongObjectRecogController(model)
    Main(model,view,controller)
