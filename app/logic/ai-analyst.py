import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import *
from sklearn.metrics import accuracy_score
from sklearn.datasets import *
import matplotlib.pyplot as plt
import tensorflow as tf

import keras

from keras import Sequential

model = Sequential()

model.add(keras.Input((64,)))
model.add(keras.Dense())


import time

data =  load_sample_images()




