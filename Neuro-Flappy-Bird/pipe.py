import numpy as np
import pygame

# Pipe class
class Pipe:
    # Constructor
    # Input: info - dictionary containing the information about the screen and actions
    #        special - boolean value to indicate if the pipe is special
    # Output: None
    def __init__(self,info,special=None):
        self.info = info
        self.spacing = 150
        
        # Top and bottom of pipe
        # The pipe is centered at 10% up and 70% down
        self.top = np.random.uniform(0.1*self.info["height"],0.7*self.info["height"])  #np.random.random()*self.info["height"]/2
        self.bottom = self.info["height"] - (self.top + self.spacing) #np.random.random()*self.info["height"]/2

        # Starts at the edge of the screen
        self.x = self.info["width"]
        # Width of pipe
        self.w = 40
        # How fast the pipe moves to the left
        self.speed = 1
        # Highlight if the bird hits the pipe
        self.highlight = False
        # Colour of the pipe
        self.colour = (255,255,255)
        # Special pipe
        if special:
            self.colour = (128,128,128)

    # Show the pipe on the screen
    def show(self):
        if self.highlight:
            colour = (255,0,0)
        else:
            colour = self.colour

        # Draw the top and bottom of pipe
        pygame.draw.rect(self.info["screen"], colour, [self.x,0,self.w,self.top])
        pygame.draw.rect(self.info["screen"], colour, [self.x,self.info["height"]-self.bottom,self.w,self.bottom])

    # Update the pipe's position
    def update(self):
        self.x -= self.speed
    
    # Check if the pipe is offscreen ie out of the screen
    def offscreen(self):
        return self.x < -self.w
    
    # Check if the bird hits the pipe
    def hits(self,bird):
        if (bird.y < self.top) or (bird.y > self.info["height"] - self.bottom ):
            if (bird.x > self.x) and (bird.x < self.x + self.w):
                self.highlight = True
                return True
            else:
                self.highlight = False
                return False
        else:
            self.highlight = False
            return False




        