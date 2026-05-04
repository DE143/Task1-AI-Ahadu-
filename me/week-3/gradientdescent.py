import numpy as np

def gradient_descent(x,y,theta,learning_rate, iterations):
    m=len(y) # number of training examples
    for _ in range(iterations):
        prediction = np.dot(x, theta)
        error = prediction-y
        gradient = (1/m) * np.dot(x.T, error)
        theta -= learning_rate * gradient
    return theta

# Example usage:
x = np.array([[11, 21], [1, 22], [22, 2], [10, 3]]) # feature matrix
y = np.array([1, 22, 2, 13]) # target values
theta = np.array([0.1, 0.1]) # initial parameters
learning_rate = 0.001
iterations = 1000

print("gradient descent:  \n", gradient_descent(x, y, theta, learning_rate, iterations))