
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import sys

import math
import matplotlib.pyplot as plt
import numpy
import pandas
import sklearn.metrics
import sklearn.model_selection
import sklearn.linear_model
import sklearn.preprocessing



def load_train_test_data(train_ratio=.5):
    data = pandas.read_csv('Exercise_3\HTRU_2.csv', header=None, names=['x%i' % (i) for i in range(8)] + ['y'])
    X = numpy.asarray(data[['x%i' % (i) for i in range(8)]])
    X = numpy.hstack((numpy.ones((X.shape[0],1)), X))
    y = numpy.asarray(data['y'])

    return sklearn.model_selection.train_test_split(X, y, test_size = 1 - train_ratio, random_state=0)


def scale_features(X_train, X_test, low=0, upp=1):
    minmax_scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(low, upp)).fit(numpy.vstack((X_train, X_test)))
    X_train_scale = minmax_scaler.transform(X_train)
    X_test_scale = minmax_scaler.transform(X_test)
    return X_train_scale, X_test_scale


def cross_entropy(y, y_hat):
    loss = 0
    for i in range(len(y)):
        loss += -(y[i]*math.log(y_hat[i]) + (1-y[i])*math.log(1-y_hat[i]))
    return loss


def logreg_sgd(X, y, alpha=0.001, epochs=10000, eps=1e-4):
    n, d = X.shape
    theta = numpy.zeros((d, 1))  # Make sure theta is a column vector

    for epoch in range(epochs):
        prev_theta = copy.deepcopy(theta)

        for i in range(n):
            xi = X[i, :].reshape((1, d))
            yi = y[i]

            gradient = (predict_prob(xi, theta) - yi) * xi.T
            theta -= alpha * gradient

        if numpy.all(numpy.abs(theta - prev_theta) < eps):
            break

    return theta




def predict_prob(X, theta):
    return 1./(1+numpy.exp(-numpy.dot(X, theta)))


def plot_roc_curve(y_test, y_prob):
    # TODO: compute tpr and fpr of different thresholds
    # tpr = []
    # fpr = []
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("roc_curve.png")


def main(argv):
    X_train, X_test, y_train, y_test = load_train_test_data(train_ratio=.5)
    X_train_scale, X_test_scale = scale_features(X_train, X_test, 0, 1)

    theta = logreg_sgd(X_train_scale, y_train)
    print(theta)
    y_prob = predict_prob(X_train_scale, theta)
    print("Logreg train accuracy: %f" % (sklearn.metrics.accuracy_score(y_train, y_prob > .5)))
    print("Logreg train precision: %f" % (sklearn.metrics.precision_score(y_train, y_prob > .5)))
    print("Logreg train recall: %f" % (sklearn.metrics.recall_score(y_train, y_prob > .5)))
    y_prob = predict_prob(X_test_scale, theta)
    print("Logreg test accuracy: %f" % (sklearn.metrics.accuracy_score(y_test, y_prob > .5)))
    print("Logreg test precision: %f" % (sklearn.metrics.precision_score(y_test, y_prob > .5)))
    print("Logreg test recall: %f" % (sklearn.metrics.recall_score(y_test, y_prob > .5)))
    plot_roc_curve(y_test.flatten(), y_prob.flatten())


if __name__ == "__main__":
    main(sys.argv)