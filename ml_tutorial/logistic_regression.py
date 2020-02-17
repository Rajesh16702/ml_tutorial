# AUTOGENERATED! DO NOT EDIT! File to edit: 02_logistic_regression.ipynb (unless otherwise specified).

__all__ = ['load_data', 'plot_data', 'sigmoid', 'predict', 'decision_boundary', 'classify', 'cost_function', 'train',
           'update_weights', 'get_accuracy']

# Cell
import numpy as np
import pandas as pd
import altair as alt

def load_data(file_name):
    """
    Read the csv data file with name `file_name`
    and return a Pandas DataFrame.
    """
    data = pd.read_csv(file_name)
    return data

# Cell
def plot_data(data):
    """
    Create the scattor plot of the `data` and
    return the chart object
    """
    base = alt.Chart(data).mark_point(size=100,filled=True).encode(
        alt.X("studied"),
        alt.Y("slept",scale=alt.Scale(domain=[0,11])),
        alt.Color("passed:N")
    )
    return base

# Cell
def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))

# Cell
def predict(examples,parameters):
    """
    Compute the probability of being y=1 for all the `examples` given `parameters`.
    Return a 1D array of probabilities.
    """
    z = np.dot(examples,parameters)
    return sigmoid(z)

# Cell
def decision_boundary(prob):
    """
    Convert a probability `prob` into a class and
    return 1 if `prob` >= 0.5, otherwise return 0
    """
    return 1 if prob >= .5 else 0

# Cell
def classify(predictions):
    """
    Convert a array of probabilities of the `predictions` into an array of classes.
    Return an N-element array of 0s (False) and 1s (True)
    """
    vec_decision_boundary = np.vectorize(decision_boundary)
    return vec_decision_boundary(predictions)

# Cell
def cost_function(examples, labels, parameters):
    """
    Compute the cost using Mean Absolute Error
    `examples`: array of (examples,features) of shape (100,3),
    `labels`: array of labels with shape (100,1),
    `parameters`: array of parameters w of shape (3,1), and
     return a 1D matrix of predictions
    """
    observations = len(labels)

    predictions = predict(examples, parameters)

    #Take the error when label=1
    class1_cost = -labels*np.log(predictions)

    #Take the error when label=0
    class2_cost = (1-labels)*np.log(1-predictions)

    #Take the sum of both costs
    cost = class1_cost - class2_cost

    #Take the average cost
    cost = cost.sum() / observations

    return cost


# Cell
def train(examples, labels, parameters, learning_rate, iterations):
    """
    Train the logistic regression model
    `examples`   : training examples,
    `labels`     : class labels, i.e. 0 or 1,
    `parameters` : parameters to be fit, i.e. w,
    `learning Rate` : learning rate of the gradient descent,
    `iterations` : number of gradient descent iterations, and
    return the parameters w and an array of all the costs

    """
    cost_history = []

    for i in range(1,iterations + 1):
        parameters = update_weights(examples, labels, parameters, learning_rate)

        #Calculate error for auditing purposes
        cost = cost_function(examples, labels, parameters)
        cost_history.append(cost)

        # Log Progress
        if i % 1000 == 0:
            print("iter: {:d}, cost: {:.4f}".format(i,cost))

    return parameters, cost_history

# Cell
def update_weights(examples, labels, parameters, learning_rate):
    """
    update the vector of parameters using the gradient descent rule
    `examples`: array of examples with shape (200, 3),
    `labels`: array of class labels for examples with shape (200, 1),
    `parameters`: vector of parameters with shape (3, 1), and
    return the new vector of parameters
    """
    N = len(examples)

    #1 - Get Predictions
    predictions = predict(examples, parameters)

    #2 Transpose features from (200, 3) to (3, 200)
    # So we can multiply w the (200,1)  cost matrix.
    # Returns a (3,1) matrix holding 3 partial derivatives --
    # one for each feature -- representing the aggregate
    # slope of the cost function across all observations
    gradient = np.dot(examples.T,  predictions - labels)

    #3 Take the average cost derivative for each feature
    gradient /= N

    #4 - Multiply the gradient by our learning rate
    gradient *= learning_rate

    #5 - Subtract from our weights to minimize cost
    parameters -= gradient

    return parameters

# Cell
def get_accuracy(predicted_labels, actual_labels):
    """
    Measure the accuracy of the model
    `predicted_labels`: labels that the model is predicted,
    `actual_labels`: actual labels of the examples
    """
    diff = predicted_labels - actual_labels
    return 1.0 - (np.count_nonzero(diff) / len(diff))