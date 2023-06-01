import numpy as np
import pygame
from nn import *

# Bird class
class Bird:

    # Constructor
    # Input: info - dictionary containing the information about the screen and actions
    #        brain - neural network object
    # Output: None
    def __init__(self,info, brain = None):
        self.info = info
        self.y = self.info["height"]/2
        self.x = 25

        # Physics Attributes
        self.gravity = 0.6
        # lift is the force applied when the bird flaps its wings
        # lift is a negative value because the y-axis is inverted in pygame
        self.lift = -15
        self.velocity = 0

        # Score and fitness
        self.score = 0
        self.fitness = 0
        if brain:
            self.brain = brain.deepcopy()
        else:
            # Neural Network with 5 input nodes, 4 hidden nodes and 1 output node
            self.brain = NeuralNetwork_1([5,4,1])
    
    # Show the bird on the screen
    def show(self):
        # circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle( self.info["screen"], (0,255,0), np.array([self.x, self.y]), 10)
    
    # Update the bird's position
    def update(self):
        self.score += 1
        self.velocity += self.gravity
        # Limiting the velocity
        self.velocity = np.clip(self.velocity, -10,10)
        self.y += self.velocity

        if (self.y > self.info["height"]):
            self.y = self.info["height"]
            self.velocity = 0
        if (self.y < 0):
            self.y = 0
            self.velocity = 0
    
    # Flap the bird's wings
    def up(self):
        self.velocity += self.lift

    # Think about the next move
    # Input: pipes - list of pipes
    # Output: None
    def think(self,pipes):
        # Find out the closest pipe
        closest = None
        closestdistance = 10000000
        for P in pipes:
            d = P.x + P.w - self.x
            if d < closestdistance and d > 0:
                closest = P
                closestdistance = d

        # Generate input features and predict using brain
        # Input features: y position of bird, top of closest pipe, bottom of closest pipe, x position of closest pipe, velocity of bird
        input = [0,0,0,0,0]
        input[0] = self.y/self.info["height"]

        input[1] = closest.top/self.info["height"]
        input[2] = closest.bottom/self.info["height"]
        input[3] = closest.x/self.info["width"]
        input[4] = self.velocity/10

        # Predict
        # Output is a list of size 1
        output = self.brain.predict(input)
        if output[0] > 0.5:
            self.up()

    # Mutate the bird's brain
    def mutate(self,q):
        self.brain.mutate(q)



        






