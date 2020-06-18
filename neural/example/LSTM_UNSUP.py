from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from datetime import datetime


def LSTM_Prepare(fname):
    """Prepare data for LSTM model

    Args:
        fname (string): Raw data csv path

    Returns:
        [tuple]: Train data, Test Data and Data Scaler
    """
    # load dataset
    dataset = read_csv(fname, header=0, index_col=0)
    values = dataset.values
    idx = list(dataset.index)
    # integer encode direction
    encoder = LabelEncoder()
    values[:, 4] = encoder.fit_transform(values[:, 4])
    # ensure all data is float
    values = values.astype("float32")
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    # frame as supervised learning

    # split into train and test sets
    values = scaled
    n_train_hours = 365 * 24
    train = values[:n_train_hours, :]
    test = values[n_train_hours:, :]
    # split into input and outputs
    train_X, train_y = train, train[:, 0]
    test_X, test_y = test, test[:, 0]
    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
    return train_X, train_y, test_X, test_y, scaler, idx


def LSTM_Exec(train_X, train_y, test_X, test_y, visualize):
    """Execute LSTM model

    Args:
        train_X (ndarray): Input Data
        train_y (ndarray): Target Data
        test_X (ndarray): Validation Data
        test_y (ndarray): Validation Data
        visualize (boolean): Wheather to plot input and output data.

    Returns:
        Sequential: Returns Sequential model
    """
    # design network
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss="mae", optimizer="adam")
    # fit network
    history = model.fit(
        train_X,
        train_y,
        epochs=50,
        batch_size=72,
        validation_data=(test_X, test_y),
        verbose=2,
        shuffle=False,
    )
    if visualize is True:
        # plot history
        pyplot.plot(history.history["loss"], label="train")
        pyplot.plot(history.history["val_loss"], label="test")
        pyplot.legend()
        pyplot.show()
    return model


def LST_Predict(train_X, train_y, test_X, test_y, model, scaler):
    """[summary]

    Args:
        train_X (ndarray): [description]
        train_y (ndarray): [description]
        test_X (ndarray): [description]
        test_y (ndarray): [description]
        model (Sequential): Keras Sequential model
        scaler ([type]): [description]

    Returns:
        [type]: [description]
    """
    # make a prediction
    yhat = model.predict(test_X)
    print(yhat.shape)
    print(test_X.shape)
    test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
    # invert scaling for forecast
    inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
    print(inv_yhat.shape)
    inv_yhat = scaler.inverse_transform(inv_yhat)
    inv_yhat = inv_yhat[:, 0]
    print(inv_yhat[-1])

    # invert scaling for actual
    test_y = test_y.reshape((len(test_y), 1))
    inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
    inv_y = scaler.inverse_transform(inv_y)
    inv_y = inv_y[:, 0]
    return inv_y, inv_yhat


def LSTM_Eval(inv_y, inv_yhat):
    """Evaluate LSTM model

    Args:
        inv_y (array): Actual
        inv_yhat (array): Forecast
    """
    # calculate RMSE
    rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
    print("Test RMSE: %.3f" % rmse)


def LSTM_RUN(fname, visualize=False):
    """ Run LSTM forecast model

    Args:
        fname (string): Path of CSV data
        visualize (bool, optional): Wheater to visualize data.
        Defaults to False.
    """

    train_X, train_y, test_X, test_y, scaler, idx = LSTM_Prepare(fname)
    model = LSTM_Exec(train_X, train_y, test_X, test_y, False)
    inv_y, inv_yhat = LST_Predict(
        train_X, train_y, test_X, test_y, model, scaler
    )
    pyplot.plot(inv_y, label="actual")
    pyplot.plot(inv_yhat, label="predicted")
    dates_list = [
        datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        for date in idx[8761::24]
    ]
    pyplot.xticks(list(inv_y[::24]).index, labels=dates_list)
    pyplot.xlabel("Timestep")

    pyplot.legend()
    pyplot.savefig("test.png")
    # print(inv_y[-10:], inv_yhat[-10:])
    LSTM_Eval(inv_y, inv_yhat)
