import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def logistic_loss_and_gradient(X, y, w):
    fx = sigmoid(np.dot(w.T, X))
    loss = np.mean((y - fx) ** 2)
    gradient = -2 * np.dot(X, ((y - fx) * fx * (1 - fx)).T)  # derivative w.r.t. w
    return loss, gradient

def logistic(X, y, learning_rate=0.01, epochs=1000):
    P, N = X.shape
    X = np.vstack((np.ones((1, N)), X))  # Add a row of ones for the bias term
    y = y.reshape(1, -1)  # Make sure y is a row vector
    w = np.zeros((P + 1, 1))
    
    for epoch in range(epochs):
        loss, gradient = logistic_loss_and_gradient(X, y, w)
        w -= learning_rate * gradient  # Update rule
        
        # Optional: print out loss to monitor training
        if epoch % 100 == 0:
            print(f'Epoch {epoch}: Loss {loss}')
    
    return w
