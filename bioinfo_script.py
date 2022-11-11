#!/usr/bin/python3
#This script is adapted from Francois Chollet's book "Deep Learning in Python"
#My goal with this is just to get practice for ML classification problems

import tensorflow
from keras.datasets import imdb
import numpy as np
#dataset is a list of imdb reviews, labeled as positive or negative. our goal is review sentiment prediction :)

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words = 10000)
#train_data and test_data are review lists, train_labels and test_labels are their sentiment
#we limit to the 10000 most frequent words in order to make the data more managable
#each record in the data is a a list of words by their popularity index

def vectorize_sequences(sequences, dimension=10000):
	results = np.zeros(len(sequences), dimension)
	for i, sequence in enumerate(sequences):
		results[i, sequence] = 1.
	return results
#a list of lists isn't a tensor, so we need to make it one
#vectorization is our solution: a list [3, 5] becomes a 10,000 dimensional vector of all zeros except for 1s at 3 and 5

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)
#vectorized data

y_train = np.asarray(train_labels).astype('float32')
y_train = np.asarray(test_labels).astype('float32') 
#labels are already 1 or 0, so vectorization is trivial

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(16, activation = 'relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation = 'relu'))
model.add(layers.Dense(1, activation = 'sigmoid'))
#two layers for the tensor operation relu(dot(W, input) + b), allowing a hypothesis space for learning
#final layers collapses it into a sigmoid function for sentiment probability

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
#adds our optimize & loss function

x_val = x_train[:10000]
partial_x_train = x_train[10000:]
y_val = y_train[:10000]
partial_y_train = y_train[10000:]
#sets a side a portial of data for validation

history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))

#The model part is finished! The rest is just using matplotlib for success statistics ^_^

import matplotlib.pyplot as plt
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len('acc') + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label= 'Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig('TrainValLoss.png')

