#!usr/bin/python3
import pygame, time
import numpy as np
from bird import *
from pipe import *
import ga
import matplotlib.pyplot as plt

# Control Parameters and setting up the window
# Info stores the information about the screen and actions
info = {"width":600, "height":600 ,"population_count":500 ,"generation_count":0, "speedup_cycles":3, "screen":None }

# Pygame setup
pygame.init()
# Defining the font
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
# Setting up the screen
info["screen"] = pygame.display.set_mode([ info["width"], info["height"] ])
# Setting up the Title
pygame.display.set_caption("NeuroEvolution Flappy Bird")
# Setting up the clock
clock = pygame.time.Clock()
# Getting the current time
#useful for calculating the elapsed time since the start of the program
a = time.time()  
# Setting up the done variable
done = False

# Go
# Framecount is used to keep track of the number of frames
framecount = 0
# Best score is used to keep track of the best score
best_score = 0
# Birds is a list of birds
birds = ga.new_generation(info)
# Saved birds is a list of birds from the previous generation
savedBirds = []
# Pipes is a list of pipes
pipes = []
# Appending a pipe to the list of pipes
pipes.append(Pipe(info))

# matplotlib setup
# x_plot is a list of x coordinates for plotting
x_plot = [0]
# y_plot is a list of y coordinates for plotting
y_plot = [0]
# Plotting initialize
plt.ion()
# Setting up the title of the plot
plt.title("Top scores per generation")
# Setting up the x label of the plot
plt.xlabel("Generation")
# Setting up the y label of the plot
plt.ylabel("Score")

while not done:
    for CYCLES in range(0,info["speedup_cycles"]):
        clock.tick(500)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP) :
                info["speedup_cycles"] += 1
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN) and info["speedup_cycles"] > 3  :
                info["speedup_cycles"] -= 1    
                              
        info["screen"].fill((75,75,75))

        # Do stuff
        framecount += 1
        if (framecount % 200 == 0): pipes.append(Pipe(info)) # Add pipes to screen
        for b in birds: # Bird takes some action
            b.think(pipes)
            b.update()
            #b.show()
        for p in pipes: # Pipe animation
            #p.show()
            p.update()
            for b in birds: # Kill bird if it hits pipe
                if p.hits(b):
                    savedBirds.append(birds.pop(birds.index(b)))

            if p.offscreen(): pipes.pop(pipes.index(p)) 
    
        # New generation, all birds dead
        if len(birds) == 0:
            info["generation_count"] += 1
            print("\nGeneration ",info["generation_count"], " completed\n")
            birds,best_score = ga.new_generation(info,savedBirds)
            savedBirds = []
            pipes = [Pipe(info,special=True)]
            framecount = 0
            # Plotting
            x_plot.append(info["generation_count"]) ; y_plot.append(best_score)
            plt.plot(x_plot, y_plot); plt.show(); plt.pause(0.0001)

    # Update drawing ( outside cycles loop)    
    for b in birds: b.show()
    for p in pipes: p.show()
    text1 = "Generation " + str(info["generation_count"]) 
    text2 = "Frame skip: " + str(info["speedup_cycles"])
    text3 = "Prev gen best: " + str(best_score)
    text4 = "Time elapsed (min): " + str(    (time.time() - a)//60    )
    text5 = "Surviving birds: " + str(info["population_count"] - len(savedBirds)) + "/" + str(info["population_count"])
    info["screen"].blit( myfont.render(text1, False, (255, 165, 0)) ,(info["width"]-250 ,0))
    info["screen"].blit( myfont.render(text2, False, (255, 165, 0)) ,(info["width"]-250 ,15))
    info["screen"].blit( myfont.render(text3, False, (255, 165, 0)) ,(info["width"]-250 ,30))
    info["screen"].blit( myfont.render(text4, False, (255, 165, 0)) ,(info["width"]-250 ,45))
    info["screen"].blit( myfont.render(text5, False, (255, 165, 0)) ,(info["width"]-250 ,60))
    pygame.display.flip()

pygame.quit()


