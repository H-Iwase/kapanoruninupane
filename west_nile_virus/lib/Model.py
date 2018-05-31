# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from sklearn import svm, ensemble
from sklearn import grid_search
import numpy as np
from scipy.optimize import fmin

class Model(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def fit(self, data, label):
        return self.model.fit(data, label)

    @abstractmethod
    def predict(self, data):
        return self.model.predict_proba(data)[:,1]

class SVM(Model):
    def __init__(self, C=1.0, gamma='auto', kernel='rbf', optimization=False, tuned_param=[{'C':[0.1], 'kernel':['rbf'], 'gamma':[0.1]}]):
        if(optimization):
            self.model = grid_search.GridSearchCV(svm.SVC(probability=True), tuned_param, cv=5, scoring='%s_weighted' % 'recall')
        else:
            self.model = svm.SVC(C=C, gamma=gamma, kernel=kernel, probability=True)

class RandomForest(Model):
    def __init__(self, n_estimators=1000, n_jobs=-1, min_samples_split=2):
        self.model = ensemble.RandomForestClassifier(n_estimators=n_estimators, n_jobs=n_jobs, min_samples_split=min_samples_split)

class GLM(Model):
    """
    x:locate, y:trap, p:probability 
    p = 1/(1+exp(-(ax + by + c)))
    n:NumMosquitos, p_w:WnvPresent
    P(p_w=0) = (1 - p)^n
    P(p_w=1) = 1 - (1 - p)^n
    P(p_w) = ((1-p)^n)^(1-p_w)(1-(1-p)^n)^p_w
    a,b,c = argmax PI((1-p)^n)^(1-p_w)(1-(1-p)^n)^p_w
    a,b,c = argmin -Sigma{n(1-p_w)log(1-p)+p_wlog(1-(1-p)^n)}
    """
    def __init__(self, xtol=1e-4, ftol=1e-4, maxiter=10000, maxfun=15000):
        self.xtol = xtol
        self.ftol = ftol
        self.maxiter = maxiter
        self.maxfun = maxfun
        self.W = None
        self.count = 0

    def p(self, W, X):
        return 1.0/(1.0+np.exp(-np.dot(X,W)))

    def log_likelihood(self, W, X, n, pw):
        tmp = self.p(W, X)
        return n*(1.0-pw)*np.log(1.0-tmp)+pw*np.log(1.0-np.power(1-tmp,n))

    def func(self, W, X):
        C = np.ones(X.shape[0])
        X = np.c_[X,C]
        summary = 0.0
        for i in range(X.shape[0]):
            summary += self.log_likelihood(W, X[i, 2:], X[i,0], X[i,1])
        return summary

    def callback(self, W):
        self.count += 1
        if self.count % 100 == 0:
            print(self.count, W)

    def fit(self, data, label, param=None):
        if param is None:
            param = np.ones(label.size)
        training_data = (np.c_[param, label, data],)
        self.W = fmin(self.func,
                      np.r_[np.array([np.random.rand()/1000.0 for i in range(data.shape[1]+1)])],
                      args=training_data,
                      callback=self.callback,
                      xtol=self.xtol,
                      ftol=self.ftol,
                      maxiter=self.maxiter,
                      maxfun=self.maxfun)
        self.count = 0
        return

    def predict(self, data):
        C = np.ones(data.shape[0])
        data = np.c_[data, C]
        return self.p(self.W, data)

    
