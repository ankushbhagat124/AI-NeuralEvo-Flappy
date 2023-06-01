import numpy as np
from bird import *
import copy,random

# Creating a new generation of birds
# Input: info - dictionary containing the information about the screen and actions
#        saved_birds - list of birds from the previous generation
# Output: newB - list of birds for the new generation
#         best_score - best score of the previous generation

def new_generation(info,saved_birds = None):
    if not saved_birds: # First generation
        # Initiate Bird ojects using contructor and return a list of birds
        return [Bird(info) for i in range(0,info["population_count"])]    
    else:
        # Make new generation
        # Calculate fitness
        sum = 0
        for b in saved_birds:
            sum += b.score
        for b in saved_birds:
            # increasing the contrast between high and low fitness values, making the selection process more focused on the best-performing individuals that have a higher chance of being selected for reproduction
            b.fitness = (b.score/sum)**3

        # Prev gen scores and fitness
        for b in saved_birds: 
            print("Score, Fitness : ",b.score, b.fitness )
        
        # Best score of the last bird in the list from previous generation
        best_score = copy.deepcopy(saved_birds[-1].score)
        print("Best score of previous generation: ",best_score)

        # Selection of best ones
        newB = []
        for i in range(0,info["population_count"]):
            newB.append(pickone(info,saved_birds))

        return newB,best_score

# Selecting a bird from the previous generation
# Input: info - dictionary containing the information about the screen and actions
#        s - list of birds from the previous generation
# Output: child - a bird object for the new generation

def pickone(info,s):
   
    # Method 0: Daniel Shiffman's algo
    # Method 1: Simply select any of top 10

    method = 0

    if method == 0:
        # Daniel Shiffman's algo
        index = 0
        r = np.random.random()

        while r > 0 and index < len(s):
            # Current r greater than fitness then continue to next bird
            r = r -  s[index].fitness 
            index += 1

        index -= 1
        # create a new Bird object, referred to as child, with the same brain as the selected bird (s[index].brain).
        child = Bird(info, brain= s[index].brain )
        # Mutate the child's brain with mutation's probability of 0.2
        # The mutation probability involves striking a balance between exploration and exploitation. If the mutation probability is too low, the algorithm might converge prematurely, missing out on potentially better solutions. On the other hand, if the mutation probability is too high, the algorithm might exhibit excessive exploration, leading to slower convergence or instability.
        child.mutate(q=0.6)
        return child

    elif method == 1: # Simply select any of top 10
        index = np.random.randint(1,10)
        child = Bird(info, brain= s[-index].brain )
        child.mutate(q=1)
        return child