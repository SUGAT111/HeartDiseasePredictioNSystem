import numpy as np
import pandas as pd

# Logistic Regression
class LogisticRegressionModel:
    def __init__(self, learning_rate=0.0001, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X, Y):
        self.m, self.n = X.shape
        self.W = np.zeros(self.n)
        self.b = 0
        self.X = X
        self.Y = Y

        for _ in range(self.iterations):
            self.update_weights()

    def update_weights(self):
        linear_model = np.dot(self.X, self.W) + self.b
        Y_pred = self.sigmoid(linear_model)
        
        dW = (1 / self.m) * np.dot(self.X.T, (Y_pred - self.Y))
        db = (1 / self.m) * np.sum(Y_pred - self.Y)
        
        self.W -= self.learning_rate * dW
        self.b -= self.learning_rate * db

    def predict(self, X):
        linear_model = np.dot(X, self.W) + self.b
        Y_pred = self.sigmoid(linear_model)
        return Y_pred
    
    def predict_class(self, X, threshold=0.5):
        Y_pred = self.predict(X)
        return [1 if i >= threshold else 0 for i in Y_pred]

def find():
    df = pd.read_csv("C:\\SaugatProjectIII\\predictor\\heartdata.csv")
    X = df.iloc[:, :-1].values
    Y = df.iloc[:, -1].values  
    return X, Y
