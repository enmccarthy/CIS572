from mmdataprocess import smallds as dsPoints
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing import sequence
from sklearn.preprocessing import MinMaxScaler

#TODO import tournament data and test on that
#figure out what data I want
#normalize to -1 to 1 using skikit minmax

train = []
test = []
trainY = []
testY = []
for (X, y) in dsPoints:
    if X[0] <= 2003:
        train.append(X)
        trainY.append(y)
    elif X[0] <= 2004:
        test.append(X)
        testY.append(y)
    else:
        break

train = np.array([train] + [trainY])
print(train)
test = np.array(test + testY)

#possibly change these to numpy arrays
#use minmax fro scikit learn
np.random.seed(7)
def scale(train, test):
    #fit scaler
    #we use -1, 1 bc tanh in rnn
    scaler = MinMaxScaler(feature_range=(-1,1))
    scaler = scaler.fit(train)
    #transform train
    train = train.reshape(train.shape[0], train.shape[1])
    print("reshape", train)
    trainScaled = scaler.transform(train)
    test = test.reshape(test.shape[0], test.shape[1])
    testScaled = scaler.transform(test)
    return scaler, trainScaled, testScaled

def invert_scale(scaler, X, value):
    new_row = [x for x in X] + [value]
    array = np.array(new_row)
    array = reshape(1, len(arry))
    inverted = scaler.inverse_transform(array)
    return inverted[0,-1]
#fit an lstm network to training data
def fit_lstm(train, batch_size, nb_epoch, neurons):
    X, y = train[:, 0:-1], train[:, -1]
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer='adam')
    for i in range(nb_epochs):
        model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
        model.reset_states()
    return model

def forecast_lstm(model, batch_size, X):
    X = X.reshape(1,1, len(X))
    yhat = model.predict(X, batch_size=batch_size)
    return yhat[0,0]



scalet, scaleTrain, scaleTest= scale(train, test)

print scalet
