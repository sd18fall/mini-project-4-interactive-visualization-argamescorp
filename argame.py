"""AR Game file
@authors: Richard Ballaux, Viktor Deturck, Leon Santen"""
import pygame
import time

class Playboard():
    """this board includes the outlines, the ball, the paddles and the goals"""
    def __init__(self,width = 10000, height = 70000):
        pygame.init()
        screen_size = (width,height)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ("Pong-AR-Game")
        self.actors = {}
        self.width = width
        self.height = height
    def _draw_background(self):
        """eventually this needs to be the live feed of the camera"""
        """but for now we just stay with a white background"""
        WHITE = (255,255,255)
        self.screen.fill(WHITE)

    def _draw_actors(self):
        """this function draws all the actors in the window"""
        all_actors = self.actors.values()
        for actor in all_actors:
            actor.draw()

    def _redraw(self):
        self._draw_background()
        self._draw_actors()
        pygame.display.update()

    def main_loop(self):
        """Update graphics and check for pygame events."""
        running = True
        while running:
            time.sleep(0.01)
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
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

class Actor():
    """this is the master class of all the actors the game will have"""
    def __init__(self, playground, coordinates, image_loc):
        self.coordinates = coordinates
        self.playground = playground
        self.image = pygame.image.load(image_loc)
        self.image_rect = self.image.get_rect()

class Ball(Actor):
    """this is the ball that bounces on the walls, the paddles and that you try to get in the goal of the other player"""
    pass

class Boundry(Actor):
    """This is a class for the boundry lines"""
    pass

class Paddle(Actor):
    """This is the movable paddle"""
    pass
