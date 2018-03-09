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
count = 0.0
for (X, y) in dsPoints:
    if count%2.0 ==0:
    #if X[0] <= 2003:
        train.append(X)
        trainY.append(y)
    elif count%2.0 != 0 and count <= 200:
    #elif X[0] <= 2004:
        test.append(X)
        testY.append(y)
    else:
        break
    count +=1

train = np.array(train)
trainY = np.array(trainY)
test = np.array(test)
testY = np.array(testY)

#possibly change these to numpy arrays
#use minmax fro scikit learn
np.random.seed(7)
def scale(train, trainY, test, testY):
    #fit scaler
    #we use -1, 1 bc tanh in rnn
    scaler = MinMaxScaler(feature_range=(-1,1))
    ansScaler = MinMaxScaler(feature_range=(-1,1))
    scaler = scaler.fit(train)
    #CHANGE THIS BC THEY ALREADY NP ARRAYS
    newArr = np.array(trainY)
    #because they are 1d
    newArr = newArr.reshape(1,-1)
    newArrTestY = np.array(testY)
    newArrTestY = newArrTestY.reshape(1,-1)
    ansScaler = ansScaler.fit(newArr)
    print(train[1])
    print(len(test))
    print(len(testY))
    print("THE ONE THAT WORKS", newArr)
    print("testy flipped", newArrTestY)
    trainScaled = scaler.transform(train)
    trainYScaled = ansScaler.transform(newArr)
    testScaled = scaler.transform(test)
    testYScaled = ansScaler.transform(newArrTestY)

    print(train[1])
    return scaler, trainScaled, trainYScaled, testScaled, testYScaled

def invert_scale(scaler, X, value):
    new_row = [x for x in X] + [value]
    array = np.array(new_row)
    array = reshape(1, len(arry))
    inverted = scaler.inverse_transform(array)
    return inverted[0,-1]
#fit an lstm network to training data
def fit_lstm(train, test, batch_size, nb_epoch, neurons):
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(1, 19), stateful=True))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer='adam')
    for i in range(nb_epoch):
        model.fit(train, test, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
        model.reset_states()
    return model

def forecast_lstm(model, batch_size, X):
    X = X.reshape(1,1, len(X))
    yhat = model.predict(X, batch_size=batch_size)
    return yhat[0,0]



#scalet, scaleTrain, scaleY, scaleTest, scaleTestY= scale(train, trainY, test, testY)
model = fit_lstm(train, trainY, 50, 1, 10)
score = model.evaluate(test, testY, 50, 1, 10)
print(score)
print("finished")
