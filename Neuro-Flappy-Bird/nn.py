import numpy as np
import copy

# Simple numpy NN

# Neural Network class
class NeuralNetwork_1:
    # Constructor
    # Input: sizes - list of number of nodes in each layer
    #        weights - list of weights and biases
    # Output: None
    def __init__(self,sizes,weights=None):
        self.num_layers = len(sizes)
        self.sizes = sizes
        if not weights:
            self.biases = [np.random.randn(y, 1)*2 for y in sizes[1:]]
            self.weights = [np.random.randn(y, x)*2 for x, y in zip(sizes[:-1], sizes[1:])]
        else:
            self.biases, self.weights = copy.deepcopy(weights[0]), copy.deepcopy(weights[1])
    
    # Important function
    # Predict the output
    # Input: a - list of input values
    # Output: inp - list of output values
    def predict(self,a):
        # Reshaping the input to a 2d array
        # IMPORTANT LINE !!!
        inp = np.reshape( np.array(a), (5,-1) )
        for b, w in zip(self.biases, self.weights): 
            inp = sigmoid(np.dot(w, inp)+b)
        return inp
    
    # Copy the NN
    def deepcopy(self):
        return NeuralNetwork_1(self.sizes, weights = [self.biases, self.weights] )
    
    # Mutate the NN
    def mutate(self,q=0.1):
        for item in self.biases:
            row,col = item.shape
            for i in range(0,row):
                for j in range(0,col):
                    # Mutate with probability q
                    if np.random.random() < q : item[i,j] *= (np.random.random()*2 -1)*0.1 + 1

        for item in self.weights:
            row,col = item.shape
            for i in range(0,row):
                for j in range(0,col):
                    if np.random.random() < q : item[i,j] *= (np.random.random()*2 -1)*0.1 + 1

# Sigmoid function
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))




