import numpy as np
import nnfs
from nnfs.datasets import spiral_data
nnfs.init()

np.random.seed(0)

'''X = [[1.0,2.0,3.0,2.5],
     [2.0,5.0,-1.0,2.0],
     [-1.5,2.7,3.3,-0.8]]'''

X,y = spiral_data(samples= 100,classes=3)
'''inputs = [0,2,-1,3.3,-2.7,1.1,2.2,-100] 
output = []

for i in inputs:
    if i>0:
        output.append(i)
    elif i<=0:
        output.append(0)
print(output)'''

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):  
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Loss:
    def calculate(self, output,y):
        sample_losses = self.forward(output,y)
        data_loss = np.mean(sample_losses)
        return data_loss    

class Loss_CategoricalClassentropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)

        if len(y_true.shape) == 1:
            correct_confidence = y_pred_clipped [range(samples), y_true]

        elif len(y_true.shape) == 2:
            correct_confidence = np.sum(y_pred_clipped*y_true, axis=1)

        negative_log_likelihood = -np.log(correct_confidence)
        return negative_log_likelihood

class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0,inputs) 

class Activation_Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities




dense1 = Layer_Dense(2,3)
activation1 = Activation_ReLU() 

dense2 = Layer_Dense(3,3)
activation2 = Activation_Softmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

print(activation2.output[:5])

loss_function = Loss_CategoricalClassentropy()
loss = loss_function.calculate(activation2.output, y)

print("Loss:", loss)